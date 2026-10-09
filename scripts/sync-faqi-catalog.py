#!/usr/bin/env python3
"""校验来源限定的法器初审，生成单一只读视图；不推断类别或执行被审工具。"""
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
    out = [MARKER, "# 法器清单与资源初审", "",
           "来源限定的静态初审，不是效果、可用性、许可证或独立语义批准。仅修改[法器初审数据](../metadata/faqi.json)，不手改此视图。",
           "类型与关系复用[唯一本体](../docs/gongfa/cultivation-ontology-taxonomy.md#唯一分类树)，不维护第二主树，不套功法四阶十二级。", "",
           "## 总体概览", "", f"初审时间：{data['reviewed_at']}；父仓库来源修订：`{data['source_revision']}`。",
           f"本地入口 {len(data['local_entries'])} 个，来源限定法器实现初审 {len(objects)} 条，外部资源逐行分流 {len(resources)} 条；不是按目录或资源行计算独立产品数。",
           "程序源码修订和下表声明版本不等于已核发布版、已安装版本或已部署入口；同内容副本、多入口不重复登记。", "",
           table([[DECISIONS[r['decision']], len(r['resource_ids'])] for r in data['external_reviews']], ["外部分流状态", "资源行数"]),
           "## 本地来源限定法器", "",
           "以下记录只指选定来源的程序指令内容；不同内容实现是否属于同一产品/派生版本，仍须另有演化证据。用途不作为主父。", "",
           table([[o['id'], o['name'], o['type_id'], o['implementation']] for o in objects.values()], ["实现ID", "名称", "已有类型ID", "实现来源ID"])]
    for obj in objects.values():
        source = sources[obj['implementation']]
        out += [f"### {obj['id']}", "", f"{text(obj['name'])}：{text(obj['boundary'])}",
                f"实现来源 `{source['id']}`，佐证来源 `{', '.join(obj['support'])}`；声明版本：{text(obj['declared_version'] or '未核/无明确发布版本声明')}。", ""]
    out += [f"## {len(data['local_entries'])}个本地入口的分离结果", ""]
    for entry in data['local_entries']:
        out += [f"### {text(entry['path'])}", "", f"纳入实现：`{', '.join(entry['objects']) or '无'}`。{text(entry['boundary'])}",
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
            "检查复用jsonschema/PyYAML，表格复用tabulate；来源、ID、选区、范围或只读视图漂移均失败，不联网补证或静默升级。",
            "此初审不维护等级、账户、设备、部署或运行证据。独立语义审查、运行/效果/许可核验、产品同一/版本演化及未逐模块展开的复合包仍待核。", ""]
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
    parser = argparse.ArgumentParser(description="法器初审来源校验与只读视图维护，不执行被审程序")
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
        print(json.dumps({"status": "valid-initial-source-review", "objects": len(objects), "local_entries": len(data['local_entries']),
                          "external_resources": len(resources), "view_sha256": digest(rendered), **data['limits']}, ensure_ascii=False))
        return 0
    except (ContractError, OSError, ValueError, KeyError, TypeError, RecursionError, subprocess.TimeoutExpired, yaml.YAMLError, jsonschema.exceptions.SchemaError) as error:
        # 不回显输入对象或Git异常中的潜在敏感值；错误只定位契约位置。
        message = str(error) if isinstance(error, ContractError) else type(error).__name__
        print("FAQI_CATALOG_ERRORS\n" + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
