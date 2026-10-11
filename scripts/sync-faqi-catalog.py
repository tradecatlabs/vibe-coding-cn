#!/usr/bin/env python3
"""校验法器总分类登记与依赖图观察，生成只读视图；不执行被审工具或推断等级。"""
import argparse
import configparser
import datetime
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from urllib.parse import quote, urlsplit

import jsonschema
from tabulate import tabulate
import yaml

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- generated: sync-faqi-catalog.py -->"
MAX_BYTES = 2 * 1024 * 1024
DECISIONS = {
    "software_candidate": "软件实现候选",
    "hosted_entry_candidate": "托管入口候选",
    "excluded_content": "排除：资料/规约内容",
    "excluded_model": "排除：模型名称所指",
    "pending_identity": "待核：对象身份",
    "related_local_source": "关联已审本地来源",
    "restricted_service_pending": "待核：受限服务所指",
}
GRADE_TIERS = (("tian", "天阶"), ("di", "地阶"), ("xuan", "玄阶"), ("huang", "黄阶"))
GRADE_LEVELS = (("initial", "初级"), ("intermediate", "中级"), ("advanced", "高级"))
GRADE_LABELS = {
    f"faqi-{tier}-{level}": f"{tier_label}{level_label}"
    for tier, tier_label in (("tian", "天阶"), ("di", "地阶"), ("xuan", "玄阶"), ("huang", "黄阶"))
    for level, level_label in GRADE_LEVELS
}


class ContractError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def bounded_read(path):
    require(path.is_file(), f"输入文件不存在：{path}")
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, f"输入超过2 MiB：{path}")
    return raw


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON含重复键")
        result[key] = value
    return result


def invalid_constant(_):
    raise ContractError("不是严格JSON数值")


def load_json(raw):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_constant=invalid_constant)


def safe_path(root, value, *, alias=False):
    parts = PurePosixPath(value)
    require(not parts.is_absolute() and ".." not in parts.parts and "\\" not in value,
            "来源路径越界")
    require(parts.as_posix() == value and parts.parts, "来源路径不是规范相对路径")
    lowered = [p.lower() for p in parts.parts]
    require(not any(p in {".git", ".history", ".venv", "output", "logs", "node_modules"} or
                    p.startswith(".env") or p in {"auth.json", "credentials.json", "credentials.toml"} or
                    p.endswith((".db", ".sqlite", ".sqlite3", ".pem", ".key")) for p in lowered),
            "拒绝凭据、历史、日志或数据库来源")
    path = root / value
    for parent in [path, *path.parents]:
        if parent == root:
            break
        require(not parent.is_symlink() or (alias and parent == path), "来源含未授权软链接")
    require(path.resolve().is_relative_to(root), "来源软链接越界")
    return path


def git_output(repository, *args):
    process = subprocess.run(["git", "--no-replace-objects", "-C", str(repository), *args],
                             capture_output=True, timeout=20)
    require(process.returncode == 0, "固定Git来源不可读取；请核对修订与submodule初始化")
    return process.stdout


def git_blob(repository, revision, path):
    spec = revision + ":" + path
    size = int(git_output(repository, "cat-file", "-s", spec).strip())
    require(size <= MAX_BYTES, "Git来源超过2 MiB")
    return git_output(repository, "show", spec)


class UniqueYamlLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        require(not self.check_event(yaml.AliasEvent), "资源YAML不接受别名展开")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            require(isinstance(key, str) and key not in result, "资源YAML含非文本或重复键")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def indexed(items, key, label):
    values = {item[key]: item for item in items}
    require(len(values) == len(items), f"{label}重复")
    return values


def validate(root, input_path):
    raw = bounded_read(input_path)
    data = load_json(raw)
    schema_path = safe_path(root, "metadata/faqi.schema.json")
    schema_raw = bounded_read(schema_path)
    schema = load_json(schema_raw)
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    require(not errors, "法器JSON不符合Schema，定位：" + ("/".join(map(str, errors[0].absolute_path)) if errors else ""))
    time = datetime.datetime.fromisoformat(data["reviewed_at"])
    require(time.tzinfo is not None, "初审时间须含时区")
    bindings = {input_path: digest(raw), schema_path: digest(schema_raw)}
    ontology_path = safe_path(root, data["ontology"]["path"])
    ontology_raw = bounded_read(ontology_path)
    require(digest(ontology_raw) == data["ontology"]["sha256"], "本体来源SHA不符，不能静默沿用初审")
    bindings[ontology_path] = digest(ontology_raw)
    ontology = ontology_raw.decode("utf-8")
    type_ids = set(re.findall(r"^\| `([^`]+)` \|", ontology, re.MULTILINE))
    graph = data["dependency_graph"]
    graph_path = safe_path(root, graph["source_path"])
    graph_raw = bounded_read(graph_path)
    require(digest(graph_raw) == graph["source_sha256"], "依赖图来源SHA漂移，需重新核实对象映射")
    graph_text = graph_raw.decode("utf-8")
    require(f'<a id="{graph["source_anchor"]}"></a>' in graph_text, "依赖图锚点不存在")
    graph_time = datetime.datetime.fromisoformat(graph["observed_at"].replace("Z", "+00:00"))
    require(graph_time.tzinfo is not None, "依赖图观测时间须含时区")
    bindings[graph_path] = digest(graph_raw)
    sources = indexed(data["sources"], "id", "来源ID")
    objects = indexed(data["objects"], "id", "法器实现ID")
    footprints = set()
    for source in sources.values():
        path = safe_path(root, source["path"])
        require(source["path"].startswith(("tools/", "skills/")), "实现/说明来源不属于批准工具范围")
        require(path.suffix in {".py", ".sh", ".c", ".lua", ".html", ".md", ".toml", ".conf"} or path.name == "README",
                "来源不是公开代码、配置或说明")
        repository = root if source["repository"] == "." else safe_path(root, source["repository"])
        require(path.is_relative_to(repository), "来源文件不属于声明仓库")
        relative = path.relative_to(repository).as_posix()
        if repository == root:
            require(source["revision"] == data["source_revision"], "父仓库来源修订错配")
        else:
            tree = git_output(root, "ls-tree", data["source_revision"], "--", source["repository"]).decode().split()
            require(len(tree) >= 3 and tree[0] == "160000" and tree[2] == source["revision"], "submodule来源与父仓库指针错配")
            require(git_output(repository, "rev-parse", "HEAD").decode().strip() == source["revision"], "submodule工作树修订漂移")
        body = git_blob(repository, source["revision"], relative)
        current = bounded_read(path)
        require(body == current and digest(body) == source["sha256"], f"来源文件/SHA漂移：{source['id']}")
        lines = body.decode("utf-8").splitlines(keepends=True)
        start, end = source["lines"]
        require(1 <= start < end <= len(lines) + 1, f"来源半开选区越界：{source['id']}")
        selected = "".join(lines[start - 1:end - 1]).encode("utf-8")
        require(digest(selected) == source["selection_sha256"], f"选区SHA不符：{source['id']}")
        bindings[path] = digest(current)
    for obj in objects.values():
        require(obj["type_id"] in type_ids, "引用了不存在的本体类")
        require(obj["implementation"] in sources and set(obj["support"]) <= sources.keys(), "法器引用了未知来源")
        source = sources[obj["implementation"]]
        require(source["purpose"] == "implementation", "实现来源未被初审标注为程序实现选区")
        # 首批以独立程序/脚本/页面内容为单位；CLI/MCP和副本不据入口重复登记。
        footprint = source["sha256"]
        require(footprint not in footprints, "同一程序内容被复制为多个身份")
        footprints.add(footprint)
    local = indexed(data["local_entries"], "path", "本地入口")
    covered = set()
    for entry in local.values():
        require(safe_path(root, entry["path"]).is_dir(), "本地入口不是现存目录")
        require(set(entry["objects"]) <= objects.keys() and set(entry["sources"]) <= sources.keys(), "本地入口引用未知对象/来源")
        for oid in entry["objects"]:
            require(sources[objects[oid]["implementation"]]["path"].startswith(entry["path"] + "/"), "实现与本地入口所指错配")
        covered.update(entry["objects"])
    require(covered == objects.keys(), "法器实现未被本地入口覆盖")
    exclusions_by_path = {}
    exclusion_keys = set()
    excluded_implementation_sources = set()
    for exclusion in data["local_exclusions"]:
        path = exclusion["path"]
        key = (path, exclusion["name"])
        require(key not in exclusion_keys, "同一入口的范围排除对象重复")
        exclusion_keys.add(key)
        exclusions_by_path.setdefault(path, []).append(exclusion)
        require(path in local and safe_path(root, path).is_dir(), "排除记录不属于现存本地入口")
        source_id = exclusion["source"]
        require(source_id not in excluded_implementation_sources, "排除证据来源不能重复绑定")
        require(source_id in sources and sources[source_id]["purpose"] == "exclusion_evidence", "排除证据来源用途错误")
        evidence = sources[source_id]
        require(evidence["path"].startswith(path + "/") and source_id in local[path]["sources"], "排除证据来源与入口错配")
        require(set(exclusion["support_sources"]) <= sources.keys(), "排除佐证引用未知来源")
        require(set(exclusion["support_sources"]) <= set(local[path]["sources"]), "排除佐证与入口错配")
        require(all(sources[sid]["purpose"] == "support" for sid in exclusion["support_sources"]), "排除佐证来源用途错误")
        require(not any(obj["implementation"] == source_id for obj in objects.values()), "排除实现来源不能同时纳入法器对象")
        excluded_implementation_sources.add(source_id)
    empty_entries = {path for path, entry in local.items() if not entry["objects"]}
    require(empty_entries <= set(exclusions_by_path), "空纳入入口须有显式范围排除记录")
    require(not any(s["purpose"] == "exclusion_evidence" and sid not in excluded_implementation_sources for sid, s in sources.items()),
            "排除证据来源未绑定显式排除记录")
    resources = {}
    external_sources = indexed(data["external_sources"], "path", "外部来源")
    for value in external_sources.values():
        path = safe_path(root, value["path"])
        body = bounded_read(path)
        require(digest(body) == value["sha256"], "外部资源源SHA漂移；必须按新原文重审")
        content = yaml.load(body.decode("utf-8"), Loader=UniqueYamlLoader)
        require(isinstance(content, dict) and isinstance(content.get("resources"), list), "资源来源形态错误")
        require(len(content["resources"]) <= 4096, "资源数量超过4096")
        for index, row in enumerate(content["resources"]):
            require(isinstance(row, dict) and isinstance(row.get("id"), str), "资源行缺少ID")
            require(row["id"] not in resources, "原资源ID重复")
            resources[row["id"]] = {"row": row, "defaults": content.get("defaults", {}), "source": value["path"], "selector": f"/resources/{index}"}
        bindings[path] = digest(body)
    decisions = {}
    for review in data["external_reviews"]:
        for rid in review["resource_ids"]:
            require(rid not in decisions, "同一外部资源被多次分流")
            decisions[rid] = review
    require(decisions.keys() == resources.keys(), "外部资源覆盖缺失或含未批准新增ID")
    require(set(data["resource_notes"]) <= resources.keys(), "附注引用未知资源")
    related = {rid for rid, review in decisions.items() if review["decision"] == "related_local_source"}
    require(data["local_resource_links"].keys() == related, "本地来源关联缺失或范围扩大")
    graph_objects = indexed(data["dependency_graph"]["objects"], "id", "依赖图对象ID")
    require(not (graph_objects.keys() & objects.keys()), "依赖图对象与本地来源对象ID冲突；不得复制同一身份")
    for obj in graph_objects.values():
        require(obj["type_id"] in type_ids, "依赖图对象引用了不存在的本体类")
        require(obj["related_object_id"] is None or obj["related_object_id"] in objects, "依赖图运行实例关联未知本地对象")
        require(set(obj["resource_ids"]) <= resources.keys(), "依赖图对象引用未知外部资源ID")
        require(obj["grade_id"] is None and obj["grade_status"] == "pending", "草案量表未校准，不得登记法器等级")
    graph_links = indexed(data["dependency_graph"]["local_links"], "object_id", "依赖图本地关联对象")
    require(graph_links.keys() <= objects.keys(), "依赖图关联引用未知本地来源对象")
    graph_categories = indexed(data["dependency_graph"]["dependency_categories"], "node", "依赖图类别")
    require(all(item["disposition"] == "user_confirmed_in_scope" for item in graph_categories.values()),
            "用户已确认纳入的依赖类别不得降级为范围外或遗漏")
    category_ids = {item["id"] for item in graph_categories.values()}
    grade_assignments = indexed(data["provisional_grade_assignments"], "subject_id", "暂定品级记录")
    expected_grade_subjects = set(objects) | set(graph_objects) | category_ids
    require(grade_assignments.keys() == expected_grade_subjects, "暂定品级记录必须完整覆盖本次纳入对象，不能遗漏或增加条目")
    require(all(item["grade_id"] in GRADE_LABELS for item in grade_assignments.values()), "暂定品级ID不在法器四阶十二级词表中")
    modules_path = safe_path(root, ".gitmodules")
    module_bytes = bounded_read(modules_path)
    require(module_bytes == git_blob(root, data["source_revision"], ".gitmodules"), "submodule注册文件漂移")
    bindings[modules_path] = digest(module_bytes)
    config = configparser.RawConfigParser(); config.read_string(module_bytes.decode("utf-8"))
    module_urls = {config[s]["path"]: config[s]["url"] for s in config.sections()}
    for rid, oid in data["local_resource_links"].items():
        require(oid in objects, "来源关联引用未知法器")
        source = sources[objects[oid]["implementation"]]
        require(source["repository"] in module_urls, "来源关联不是已绑定的submodule")
        url = resources[rid]["row"].get("link", {}).get("url", "")
        def repo_url(value):
            parsed = urlsplit(value)
            require(parsed.scheme == "https" and parsed.hostname == "github.com" and not parsed.username and not parsed.query and not parsed.fragment,
                    "来源关联不是规范GitHub仓库地址")
            return parsed.path.rstrip("/").removesuffix(".git").lower()
        require(repo_url(url) == repo_url(module_urls[source["repository"]]), "资源行与本地仓库不是同一来源")
    for relation in data["relations"]:
        require(relation["subject"] in objects and relation["evidence"] in sources, "依赖关系缺对象/来源")
        require(relation["related_object_id"] is None or relation["related_object_id"] in objects, "依赖参照未知对象")
        require("`requires`" in ontology, "依赖谓词不在本体现有关系词表")
    indexed(data["references"], "path", "引用入口")
    for reference in data["references"]:
        path = safe_path(root, reference["path"], alias=True)
        original = git_blob(root, data["source_revision"], reference["path"])
        if reference["state"] == "empty-placeholder":
            require(not path.is_symlink() and bounded_read(path) == original == b"" and reference["target"] is None and reference["related_object_id"] is None,
                    "空占位文件被伪称来源链接")
            bindings[path] = digest(b"")
        else:
            require(path.is_symlink() and os.readlink(path) == reference["target"] and original.decode("utf-8") == reference["target"], "软链接状态或目标漂移")
            require(reference["related_object_id"] is None or reference["related_object_id"] in objects, "引用入口关联未知对象")
            # 符号链接绑定的是路径，不是目录内容或另一件软件身份。
    return data, sources, objects, resources, decisions, bindings


def text(value):
    escaped = html.escape(str(value), quote=False)
    return escaped.replace("`", "&#96;").replace("[", "&#91;").replace("]", "&#93;").replace("|", "&#124;")


def table(rows, headers):
    # 固定宽度表会把一个长名称扩散到每行；先用UTF-8字节做保守预算，避免格式化后才发现膨胀。
    widths = [len(str(h).encode("utf-8")) for h in headers]
    height = 5
    for row in rows:
        height += max([1, *[len(str(value).splitlines()) for value in row]])
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value).encode("utf-8")))
    require((sum(widths) + 3 * len(headers) + 1) * height + 20 <= MAX_BYTES,
            "代码表列宽与行数超过2 MiB预算，不能静默截断")
    # 原生代码表会隔离HTML/Markdown；在这里转义会把 >= 等原文字面改坏。
    return "```text\n" + tabulate(rows, headers=headers, tablefmt="psql", disable_numparse=True) + "\n```\n"


def render(data, sources, objects, resources, decisions):
    graph = data["dependency_graph"]
    graph_links = {item["object_id"]: item for item in graph["local_links"]}
    assignments = {item["subject_id"]: item for item in data["provisional_grade_assignments"]}
    grade_order = {grade: index for index, grade in enumerate(
        [f"faqi-{tier}-{level}" for tier, _ in GRADE_TIERS for level in ("advanced", "intermediate", "initial")])}
    grade_counts = {grade: sum(item["grade_id"] == grade for item in assignments.values()) for grade in grade_order}
    importance_levels = (("advanced", "高级"), ("intermediate", "中级"), ("initial", "初级"))
    distribution = []
    for tier, tier_label in GRADE_TIERS:
        tier_levels = [(label, grade_counts[f"faqi-{tier}-{level}"]) for level, label in importance_levels]
        total = sum(count for _, count in tier_levels)
        levels = "、".join(f"{label}{count}" for label, count in tier_levels if count)
        distribution.append(f"{tier_label}{total}条（{levels}）")
    distribution = "；".join(distribution)
    subject_details = {
        **{oid: {"name": obj["name"], "type": obj["type_id"]} for oid, obj in objects.items()},
        **{obj["id"]: {"name": obj["name"], "type": obj["type_id"]} for obj in graph["objects"]},
        **{item["id"]: {"name": item["node"], "type": "依赖类别"} for item in graph["dependency_categories"]},

    }

    def grade_display(subject_id):
        assignment = assignments[subject_id]
        status = "任务级暂定" if assignment["assignment_status"] == "task_scoped_provisional" else "用户指定重要性暂定"
        return f"{GRADE_LABELS[assignment['grade_id']]}（{status}）"

    out = [MARKER, "# Vibe Coding法器总分类与重要性分级表", "",
           "本视图由[法器总分类登记](../metadata/faqi.json)与外部资源原表生成；仅修改登记数据，不手改此文件。",
           "类型复用[唯一本体](../docs/gongfa/cultivation-ontology-taxonomy.md#唯一分类树)。对象身份、依赖角色与重要性分级分开；品级表示Vibe Coding重要性，不表示实现质量或任务效能。", "",
           "## 总体概览", "", f"登记版本：{data['format_version']}；更新：{data['reviewed_at']}；依赖图观测：{graph['observed_at']}。",
           f"本地来源实现 {len(objects)} 条，依赖图具名对象/实例 {len(graph['objects'])} 条，仓内实现关联到图节点 {len(graph['local_links'])} 条，用户确认纳入的依赖类别 {len(graph['dependency_categories'])} 条，重要性分级记录 {len(assignments)} 条，外部资源逐行分流 {len(resources)} 条。",
           "外部资源行是来源候选或入口，不等同独立法器对象；依赖图深度、节点数量、版本新旧均不推出重要性。", "",
           "## 重要性分级口径", "",
           "按用户指令，以Vibe Coding核心闭环重要性、对模型/Agent/工具执行/代码验证的作用及可替代性分层。天阶为定义性AI模型与Agent协作核心；地阶为代码变更、命令执行与运行基础；玄阶为上下文、质量、复用和产品交付增强；黄阶为可替代的专用或便利性支路。各阶高级、中级、初级表示该阶内重要性由高到低。",
           f"当前分布：{distribution}。这是用户指定的重要性分类，不代表功能质量、实际效果、具体身份已核或正式效能评级；正式效能规约仍为draft且阈值未校准。", "",
           "## 按天地玄黄品级主键汇总", "",
           "依赖角色和重要性决定暂定分组；任务烟测、版本观测及来源审查仅作独立事实，不直接决定品级。", "",
           ]
    for tier, tier_label in GRADE_TIERS:
        tier_rows = []
        for assignment in sorted((item for item in assignments.values() if item["grade_id"].split("-")[1] == tier),
                                 key=lambda item: (grade_order[item["grade_id"]], item["subject_id"])):
            detail = subject_details[assignment["subject_id"]]
            status = "任务级暂定" if assignment["assignment_status"] == "task_scoped_provisional" else "用户指定重要性暂定"
            tier_rows.append([assignment["grade_id"], assignment["subject_id"], detail["name"], detail["type"], status, assignment["scope"], assignment["basis"]])
        if not tier_rows:
            tier_rows = [["—", "—", "暂无记录", "—", "—", "—", "—"]]
        out += [f"### {tier_label}", "", table(tier_rows, ["品级ID", "对象ID", "对象", "本体类型", "赋级状态", "评定范围", "依据与限制"]), ""]
    out += ["## Vibe Coding依赖图中的现实对象", "",
           f"依赖图来源：[技术栈第十六节](../{quote(graph['source_path'], safe='/.-_')}#{quote(graph['source_anchor'], safe='-')})；SHA-256 `{graph['source_sha256']}`。运行时版本观测只绑定本次命令与PATH实例，不证明依赖源码或会话服务端版本。", "",
           table([[o['id'], o['name'], o['graph_node'], o['type_id'], '运行观测' if o['identity_status'] == 'runtime_observed' else '具名候选', o['version'] or '版本待核', grade_display(o['id'])] for o in graph['objects']], ["对象ID", "对象", "依赖图位置", "本体类型", "身份状态", "版本", "品级"])]
    for obj in graph["objects"]:
        resources_text = f"；外部资源：{', '.join(obj['resource_ids'])}" if obj["resource_ids"] else ""
        link_text = f"；相似本地来源参照：{obj['related_object_id']}（身份关联未证明）" if obj["related_object_id"] else ""
        out += [f"- `{obj['id']}`：{text(obj['evidence'])}{resources_text}{link_text}；品级分组：{grade_display(obj['id'])}；正式效能仍未验证。{text(obj['grade_reason'])}"]
    out += ["", "### 用户确认纳入的依赖类别", "",
            f"用户于 {graph['user_confirmation']['reviewed_at']} 确认此前列出的依赖类别均已核查并要求全部纳入。具体实现身份和版本仍按登记所据分别记录；品级按Vibe Coding重要性暂定，不等于效能验证。",
            "目标/验收合同、人类授权与取舍、Agent循环、构建/验证/交付过程及反馈仍按角色、内容、过程或关系分类，不因列入依赖范围自动成为软件法器。", "",
            table([[item['node'], '用户确认纳入', item['reason'], grade_display(item['id'])] for item in graph['dependency_categories']], ["依赖图类别", "纳入状态", "分类边界", "品级分组"]),
            "", "### 依赖图对应的仓内来源实现", "",
            "这些行指向已固定来源的本地程序内容；与上方实际运行实例分开，关联不意味着运行版相同。", "",
            table([[item['object_id'], objects[item['object_id']]['name'], item['graph_node'], item['relationship'], grade_display(item['object_id'])] for item in graph['local_links']], ["本地对象ID", "名称", "依赖图位置", "关系边界", "品级分组"]),
           "", "## 本地来源限定法器", "",
           "以下记录只指选定来源的程序指令内容；不同内容实现是否属于同一产品/派生版本，仍须另有演化证据。未出现在依赖图具体工具节点中的仓内工具仍保留在总表。", "",
           table([[o['id'], o['name'], o['type_id'], o['implementation'], graph_links.get(o['id'], {}).get('graph_node', '图中未具名'), grade_display(o['id'])] for o in objects.values()], ["实现ID", "名称", "本体类型", "实现来源ID", "依赖图位置", "品级分组"])]
    for obj in objects.values():
        source = sources[obj['implementation']]
        out += [f"### {obj['id']}", "", f"{text(obj['name'])}：{text(obj['boundary'])}",
                f"实现来源 `{source['id']}`，佐证来源 `{', '.join(obj['support'])}`；声明版本：{text(obj['declared_version'] or '未核/无明确发布版本声明')}。",
                f"暂定品级分组：{grade_display(obj['id'])}。", ""]
    out += ["## 按本次范围排除的本地程序所指", "",
            "下列源码确有程序实现所指，但应用户要求不作为本清单纳入对象；不代表它们不是软件。保留排除证据，重新纳入须满足各自复核条件。", ""]
    for exclusion in data["local_exclusions"]:
        out += [f"### {text(exclusion['name'])}", "", f"入口：`{exclusion['path']}`；证据选区 `{exclusion['source']}`；佐证选区 `{', '.join(exclusion['support_sources'])}`。",
                text(exclusion["rationale"]), "", f"重新纳入前：{text(exclusion['reopen_condition'])}", ""]
    out += [f"## {len(data['local_entries'])}个本地入口的分离结果", ""]
    for entry in data['local_entries']:
        out += [f"### {text(entry['path'])}", "", f"本次纳入对象：`{', '.join(entry['objects']) or '无（见范围排除记录）'}`。{text(entry['boundary'])}",
                f"佐证来源：`{', '.join(entry['sources'])}`。"]
        out += [f"- 待核：{text(p)}" for p in entry['pending']]
        out += [""]
    out += ["## 静态依赖与引用入口", "",
            "`requires`只记录源码/说明声明的依赖；相关本地实现ID是源码参照，不证明运行时加载了该版本，更不证明实际使用、符合协议或已获权限。", "",
            table([[r['subject'], r['predicate'], r['target_label'], r['related_object_id'] or '未知', r['evidence']] for r in data['relations']], ["主体实现", "谓词", "依赖所指", "相关来源实现", "证据ID"])]
    for r in data['relations']:
        out += [f"- `{r['subject']}`：{text(r['boundary'])}"]
    out += [""]
    for r in data['references']:
        out += [f"- `{r['path']}`：`{r['state']}`；目标 `{r['target'] or '无'}`。{text(r['boundary'])}"]
    out += ["", f"## {len(resources)}条外部资源逐行分流", "",
            "名称、原ID、状态、验证状态与风险只读自原YAML。`active`与`imported-unverified`不证明可用、许可或推荐。",
            "未核远端实现/版本的候选不登记为本地法器；模型名称所指与聊天平台分开。资料排除仅针对当前条目所指，不断言整个仓库没有程序。",
            "同名或同网址只产生重复入口核查线索，不自动合并软件身份；网络/金融分流不授权开户、交易、账户读取或实际网络操作。", ""]
    for group in data['external_reviews']:
        out += [f"### {DECISIONS[group['decision']]}", "", text(group['rationale']), ""]
        rows = []
        for rid in group['resource_ids']:
            source = resources[rid]; row = source['row']
            rows.append([rid, row['name'], row['status'], row.get('verification_status', source['defaults'].get('verification_status', 'unknown')), ', '.join(row.get('risk_flags', [])) or '无'])
        out += [table(rows, ["原资源ID", "名称", "原状态", "原验证状态", "原风险标记"])]
        for rid in group['resource_ids']:
            source = resources[rid]
            details = data['resource_notes'].get(rid, '')
            related = data['local_resource_links'].get(rid)
            if related:
                details += f" 对应本地来源参照 {related}；不把未版本化的仓库URL等同该固定源码版本。"
            out += [f"- `{rid}`：[原始资源行](../{source['source']}) `{source['selector']}`。{text(details)}"]
        out += [""]
    out += ["## 来源与选区", "", "选区是一基半开区间 `[start,end)`；SHA-256对应固定Git blob的完整字节与选区原字节，不归一化或复制源码。",
            "校验还核当前文件字节及submodule指针；源码存在和指针匹配不等于完整仓库语义、许可证或能力已审。", ""]
    for source in sources.values():
        out += [f"### {source['id']}", "", f"[来源文件](../{quote(source['path'], safe='/.-_')})：`{source['path']}`。",
                f"- 初审用途：`{source['purpose']}`（人工标注，不是自动语义批准）。",
                f"- 仓库：`{source['repository']}`；Git修订：`{source['revision']}`。",
                f"- 完整文件SHA-256：`{source['sha256']}`。",
                f"- 选区：`[{source['lines'][0]},{source['lines'][1]})`；SHA-256：`{source['selection_sha256']}`。", ""]
    out += ["## 维护与未完成事项", "", "```bash", "make sync-faqi-catalog", "make check-faqi-catalog", "make test-faqi-catalog", "```", "",
            "检查复用jsonschema/PyYAML，表格复用tabulate；依赖图、来源、ID、选区、范围或只读视图漂移均失败，不联网补证或静默升级。",
            "本表未批准独立审查、完整运行/效果、许可、部署、账户或硬件身份。重要性分级与正式效能评价分轴；任务合同、阈值校准、运行版与源码身份桥接及通用图节点的落地实例仍待核。", ""]
    return "\n".join(out).encode("utf-8")


def unchanged(bindings, root, data):
    for path, expected in bindings.items():
        require(digest(bounded_read(path)) == expected, "输入被并行修改；不提交旧视图")
    for ref in data["references"]:
        path = safe_path(root, ref["path"], alias=True)
        if ref["state"] == "symlink":
            require(path.is_symlink() and os.readlink(path) == ref["target"], "来源链接被并行修改")
    repositories = {s["repository"]: s["revision"] for s in data["sources"] if s["repository"] != "."}
    for repository, revision in repositories.items():
        index = git_output(root, "ls-files", "--stage", "--", repository).decode().split()
        require(len(index) >= 3 and index[0] == "160000" and index[1] == revision, "当前submodule索引指针漂移")
        require(git_output(root / repository, "rev-parse", "HEAD").decode().strip() == revision, "submodule修订被并行修改")


def main():
    parser = argparse.ArgumentParser(description="法器总分类登记校验与依赖图只读视图维护，不执行被审程序")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--view", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    input_path = args.input.absolute() if args.input else root / "metadata/faqi.json"
    view = args.view.absolute() if args.view else root / "tools/faqi-catalog.md"
    try:
        require(not input_path.is_symlink() and input_path.parent.resolve() == input_path.parent and
                not view.is_symlink() and view.parent.resolve() == view.parent, "输入/输出含软链接")
        data, sources, objects, resources, decisions, bindings = validate(root, input_path)
        rendered = render(data, sources, objects, resources, decisions)
        require(len(rendered) <= MAX_BYTES, "生成视图超过2 MiB")
        before = bounded_read(view) if view.exists() else None
        unchanged(bindings, root, data)
        if args.write:
            require(before is None or before.startswith(MARKER.encode()), "拒绝覆盖非本工具生成的文件")
            view.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=view.parent, prefix=".faqi-catalog-", suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name); stream.write(rendered); stream.flush(); os.fsync(stream.fileno())
            unchanged(bindings, root, data)
            require(not view.is_symlink() and (bounded_read(view) if view.exists() else None) == before, "目标被并行修改；保留临时文件，不覆盖")
            os.replace(temporary, view)
        else:
            require(before == rendered, "法器视图缺失/陈旧或手改；运行make sync-faqi-catalog")
        unchanged(bindings, root, data)
        print(json.dumps({"status": "valid-master-classification-register", "objects": len(objects), "local_entries": len(data['local_entries']),
                          "local_exclusions": len(data['local_exclusions']), "external_resources": len(resources),
                          "dependency_objects": len(data['dependency_graph']['objects']),
                          "dependency_categories": len(data['dependency_graph']['dependency_categories']),
                          "provisional_grade_assignments": len(data['provisional_grade_assignments']),
                          "view_sha256": digest(rendered), **data['limits']}, ensure_ascii=False))
        return 0
    except (ContractError, OSError, ValueError, KeyError, TypeError, RecursionError, subprocess.TimeoutExpired, yaml.YAMLError, jsonschema.exceptions.SchemaError) as error:
        # 不回显输入对象或Git异常中的潜在敏感值；错误只定位契约位置。
        message = str(error) if isinstance(error, ContractError) else type(error).__name__
        print("FAQI_CATALOG_ERRORS\n" + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
