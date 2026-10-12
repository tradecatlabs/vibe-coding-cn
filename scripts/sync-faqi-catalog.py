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
from urllib.parse import urlsplit

import jsonschema
from tabulate import tabulate
import yaml

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- generated: sync-faqi-catalog.py -->"
MAX_BYTES = 2 * 1024 * 1024
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


def table_cell(value):
    value = str(value).replace("\r\n", "\n").replace("\r", "\n")
    escaped = html.escape(value, quote=False)
    for char, entity in (("\\", "&#92;"), ("`", "&#96;"), ("*", "&#42;"), ("_", "&#95;"),
                         ("~", "&#126;"), ("[", "&#91;"), ("]", "&#93;"), ("|", "&#124;")):
        escaped = escaped.replace(char, entity)
    return escaped.replace("\n", "<br>")


def table(rows, headers):
    # 对齐表格会把单个长解释扩展到整列；先用转义后UTF-8字节做保守预算。
    escaped_headers = [table_cell(header) for header in headers]
    widths = [len(header.encode("utf-8")) for header in escaped_headers]
    escaped_rows = []
    height = 5
    for row in rows:
        require(len(row) == len(headers), "生成表格的行列数不一致")
        values = [str(value) for value in row]
        escaped_row = [table_cell(value) for value in values]
        escaped_rows.append(escaped_row)
        height += max([1, *[len(value.splitlines()) for value in values]])
        for index, value in enumerate(escaped_row):
            widths[index] = max(widths[index], len(value.encode("utf-8")))
    require((sum(widths) + 3 * len(headers) + 1) * height + 20 <= MAX_BYTES,
            "Markdown表格列宽与行数超过2 MiB预算，不能静默截断")
    return tabulate(escaped_rows, headers=escaped_headers, tablefmt="pipe", disable_numparse=True) + "\n"


def render(data, objects):
    graph = data["dependency_graph"]
    assignments = data["provisional_grade_assignments"]
    grade_order = {
        f"faqi-{tier}-{level}": index
        for index, (tier, level) in enumerate(
            [(tier, level) for tier, _ in GRADE_TIERS for level, _ in reversed(GRADE_LEVELS)]
        )
    }
    names = {
        **{object_id: obj["name"] for object_id, obj in objects.items()},
        **{obj["id"]: obj["name"] for obj in graph["objects"]},
        **{item["id"]: item["node"] for item in graph["dependency_categories"]},
    }
    rows = [
        [GRADE_LABELS[item["grade_id"]], names[item["subject_id"]], item["basis"]]
        for item in sorted(assignments, key=lambda item: (grade_order[item["grade_id"]], item["subject_id"]))
    ]
    out = [
        MARKER,
        "# Vibe Coding法器重要性总表",
        "",
        "品级仅表示 Vibe Coding 重要性暂定，不代表效能验证；本页仅供浏览，完整登记见[metadata/faqi.json](../metadata/faqi.json)。",
        "",
        table(rows, ["品级", "名称", "解释"]),
    ]
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
        data, _, objects, resources, _, bindings = validate(root, input_path)
        rendered = render(data, objects)
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
