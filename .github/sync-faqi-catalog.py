#!/usr/bin/env python3
"""校验法器总分类登记与依赖图观察，生成只读视图；不执行被审工具或推断等级。"""
import argparse
import configparser
import datetime
import hashlib
import json
import os
import posixpath
from pathlib import Path, PurePosixPath
from html import escape
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
# 从.github平铺模块导入，不复制实现或依赖当前cwd。
sys.path.insert(0, str(ROOT / '.github'))
import source_archive
import book_views
import tool_explanations
import jsonschema
import yaml
MARKER = "<!-- generated: sync-faqi-catalog.py -->"
MAX_BYTES = 2 * 1024 * 1024
# 固定来源仍指向迁移前提交；这些目录的新路径需回映到该提交中的原路径。
MOVED_ROOTS = {"assets", "docs", "metadata", "prompts", "research", "scripts", "skills", "tools"}
MIGRATED_PATH_PATTERN = re.compile(rb"(?<![A-Za-z0-9_.-])\.github/(assets|docs|metadata|prompts|research|scripts|skills|tools)\b")
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
    require(source_archive.source_is_file(path), f"输入文件不存在：{path}")
    return source_archive.read_bytes(path, MAX_BYTES)


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
    process = subprocess.run(["git", "--no-replace-objects", "-C", str(source_archive.physical_path(repository)), *args],
                             capture_output=True, timeout=20)
    require(process.returncode == 0, "固定Git来源不可读取；请核对修订与submodule初始化")
    return process.stdout


def git_blob(repository, revision, path):
    spec = revision + ":" + path
    size = int(git_output(repository, "cat-file", "-s", spec).strip())
    require(size <= MAX_BYTES, "Git来源超过2 MiB")
    return git_output(repository, "show", spec)


def path_at_revision(root, revision, current_path):
    parts = PurePosixPath(current_path).parts
    candidates = [current_path]
    if len(parts) > 1 and parts[0] == ".github" and parts[1] in MOVED_ROOTS:
        candidates.append(PurePosixPath(*parts[1:]).as_posix())
    for candidate in candidates:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(root), "ls-tree", "--full-tree", revision, "--", f":(literal){candidate}"],
            capture_output=True,
            timeout=20,
        )
        if result.returncode == 0 and any(
            line.partition(b"\t")[2].decode("utf-8") == candidate
            for line in result.stdout.splitlines()
        ):
            return candidate
    raise ContractError("固定来源修订中找不到迁移前后对应路径")


def normalize_migrated_paths(raw):
    """仅还原已批准的根目录前缀迁移，继续校验来源的原始字节。"""
    return MIGRATED_PATH_PATTERN.sub(rb"\1", raw)


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
    schema_path = safe_path(root, ".github/metadata/faqi.schema.json")
    schema_raw = bounded_read(schema_path)
    schema = load_json(schema_raw)
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    require(not errors, "法器JSON不符合Schema，定位：" + ("/".join(map(str, errors[0].absolute_path)) if errors else ""))
    time = datetime.datetime.fromisoformat(data["reviewed_at"])
    require(time.tzinfo is not None, "初审时间须含时区")
    bindings = {input_path: digest(raw), schema_path: digest(schema_raw), **source_archive.bundle_bindings(root)}
    archive_data = source_archive.bundles(root)["faqi"]["data"]
    retired_submodules = set(archive_data.get("retired_submodules", []))
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
    source_repositories = {source["repository"] for source in sources.values() if source["repository"] != "."}
    require(retired_submodules <= source_repositories, "退役子模块没有对应的冻结来源记录")
    for repository in retired_submodules:
        require(not any(path == repository or path.startswith(repository + "/")
                        for path in archive_data["locations"]), "退役子模块仍有当前位置映射")
        require(not any(path == repository or path.startswith(repository + "/")
                        for path in archive_data["live_sources"]), "退役子模块仍有当前实现绑定")
        archived_sources = [source for source in sources.values() if source["repository"] == repository]
        require(archived_sources and all(source["path"] in archive_data["documents"] for source in archived_sources),
                "退役子模块缺少冻结来源字节")
    for source in sources.values():
        path = safe_path(root, source["path"])
        require(source["path"].startswith((".github/tools/", ".github/skills/")), "实现/说明来源不属于批准工具范围")
        license_document = re.fullmatch(r"(?:LICENSE(?:\.[A-Za-z0-9._-]+)?|COPYING(?:\.[A-Za-z0-9._-]+)?)", path.name, re.IGNORECASE)
        source_type_allowed = (
            path.suffix in {".py", ".sh", ".c", ".lua", ".html", ".md", ".toml", ".conf"}
            or path.name == "README"
            or (
                source["purpose"] == "support"
                and (
                    license_document is not None
                    or path.suffix in {".awk", ".1", ".eps"}
                    or path.name == "README.ja"
                )
            )
        )
        require(source_type_allowed, "来源不是公开代码、配置或说明")
        repository = root if source["repository"] == "." else safe_path(root, source["repository"])
        require(path.is_relative_to(repository), "来源文件不属于声明仓库")
        relative = path.relative_to(repository).as_posix()
        if repository == root:
            require(source["revision"] == data["source_revision"], "父仓库来源修订错配")
            historical_path = path_at_revision(root, source["revision"], source["path"])
            body = git_blob(root, source["revision"], historical_path)
            current = bounded_read(path)
            comparable = normalize_migrated_paths(current) if historical_path != source["path"] else current
            # 已批准的默认分支迁移只改安装源地址；原修订、SHA、指令仍逐字核对。
            if (
                source["path"] in {
                    ".github/tools/config/.codex/install.sh", ".github/tools/config/.codex/README.md",
                }
                and b"https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/" in body
            ):
                comparable = comparable.replace(
                    b"https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/main/",
                    b"https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/",
                )
            require(comparable == body and digest(body) == source["sha256"], f"来源文件/SHA漂移：{source['id']}")
        else:
            historical_repository = path_at_revision(root, data["source_revision"], source["repository"])
            tree = git_output(root, "ls-tree", data["source_revision"], "--", historical_repository).decode().split()
            require(len(tree) >= 3 and tree[0] == "160000" and tree[2] == source["revision"], "submodule来源与父仓库指针错配")
            if source["repository"] in retired_submodules:
                body = source_archive.read_bytes(path)
                current = body
                require(digest(body) == source["sha256"], f"冻结来源文件/SHA漂移：{source['id']}")
            else:
                require(git_output(repository, "rev-parse", "HEAD").decode().strip() == source["revision"], "submodule工作树修订漂移")
                body = git_blob(repository, source["revision"], relative)
                current = bounded_read(path)
                require(body == current and digest(body) == source["sha256"], f"来源文件/SHA漂移：{source['id']}")
        lines = body.decode("utf-8").splitlines(keepends=True)
        start, end = source["lines"]
        require(1 <= start < end <= len(lines) + 1, f"来源半开选区越界：{source['id']}")
        selected = "".join(lines[start - 1:end - 1]).encode("utf-8")
        require(digest(selected) == source["selection_sha256"], f"选区SHA不符：{source['id']}")
        if source["repository"] not in retired_submodules:
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
        require(source_archive.source_is_directory(safe_path(root, entry["path"])), "本地入口缺少原始来源容器")
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
        require(path in local and source_archive.source_is_directory(safe_path(root, path)), "排除记录不属于原始本地入口")
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
    module_bytes = source_archive.raw_read(modules_path)
    archived_modules = source_archive.read_bytes(modules_path)
    historical_modules = git_blob(root, data["source_revision"], ".gitmodules")
    comparable_modules = (archived_modules if archived_modules == historical_modules
                          else normalize_migrated_paths(archived_modules))
    require(comparable_modules == historical_modules, "冻结submodule注册快照与来源修订不符")

    def parse_modules(raw):
        config = configparser.RawConfigParser()
        config.read_string(raw.decode("utf-8"))
        return {section: {"path": config[section]["path"], "url": config[section]["url"]}
                for section in config.sections()}

    historical_module_map = parse_modules(archived_modules)
    current_module_map = parse_modules(module_bytes)
    historical_paths = {module["path"] for module in historical_module_map.values()}
    require(retired_submodules <= historical_paths, "退役子模块不在冻结Git模块清单中")
    expected_current_modules = {}
    for section, module in historical_module_map.items():
        old_path = module["path"]
        if old_path in retired_submodules:
            continue
        expected_current_modules[section] = {
            "path": archive_data["locations"].get(old_path, old_path),
            "url": module["url"],
        }
    require(current_module_map == expected_current_modules,
            "当前Git模块须与冻结来源迁移映射及显式退役清单完全一致")
    bindings[modules_path] = digest(module_bytes)
    module_urls = {module["path"]: module["url"] for module in historical_module_map.values()}
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
        historical_path = path_at_revision(root, data["source_revision"], reference["path"])
        original = git_blob(root, data["source_revision"], historical_path)
        if reference["state"] == "empty-placeholder":
            require(not source_archive.source_is_symlink(path) and bounded_read(path) == original == b"" and reference["target"] is None and reference["related_object_id"] is None,
                    "空占位文件被伪称来源链接")
            bindings[path] = digest(b"")
        else:
            target = reference["target"]
            require(isinstance(target, str) and target, "引用软链接缺少目标")
            target_path = PurePosixPath(target)
            target_repository = posixpath.normpath(posixpath.join(PurePosixPath(reference["path"]).parent.as_posix(), target))
            require(not target_path.is_absolute() and chr(92) not in target and target_path.as_posix() == target and
                    target_repository in module_urls,
                    "引用软链接必须使用规范相对路径并指向已登记submodule")
            require(source_archive.source_is_symlink(path) and source_archive.source_readlink(path) == target and original in {target.encode("utf-8"), b""},
                    "软链接状态、当前目标或固定历史基线漂移")
            related_object_id = reference["related_object_id"]
            require(related_object_id is None or related_object_id in objects, "引用入口关联未知对象")
            if related_object_id is not None:
                implementation = sources[objects[related_object_id]["implementation"]]
                require(implementation["repository"] == target_repository, "引用软链接目标与关联法器来源错配")
            # source_revision保留旧Git状态；当前软链接由登记目标、规范仓内路径和submodule来源共同约束。
    return data, sources, objects, resources, decisions, bindings


def source_navigation(root):
    keys = book_views.source_keys(root, "faqi")
    toc = book_views.source_toc(root, "faqi") if keys else []
    anchors = []
    for line in toc:
        match = re.search(r"\]\(#([^)]+)\)", line)
        if match and match.group(1) not in anchors:
            anchors.append(match.group(1))
    document_anchors = {book_views.chapter_id(key) for key in keys}
    lines = ["## 原始说明", "",
             "冻结说明原文、字节摘要和选择器保存在唯一资料源[data.json](data.json)的`documents`中；本页只保留历史入口，不重复展开原文。", "",
             "### 原始文档", ""]
    for key in keys:
        anchor = book_views.chapter_id(key)
        lines.extend((f'<a id="{escape(anchor, quote=True)}"></a>',
                      f"- `{key}`：原始字节与摘要见[data.json](data.json)"))
    legacy = [anchor for anchor in anchors if anchor not in document_anchors]
    if legacy:
        lines.extend(("", "<!-- 兼容已发布阅读视图中的章节锚点 -->"))
        lines.extend(f'<a id="{escape(anchor, quote=True)}"></a>' for anchor in legacy)
    return lines


def render(data, objects, root, explanations, index_name="README.md"):
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", index_name) is not None,
            "索引文件名不规范")
    graph = data["dependency_graph"]
    assignments = data["provisional_grade_assignments"]
    grade_order = {
        f"faqi-{tier}-{level}": index
        for index, (tier, level) in enumerate(
            [(tier, level) for tier, _ in GRADE_TIERS for level, _ in reversed(GRADE_LEVELS)]
        )
    }
    graph_objects = {item["id"]: item for item in graph["objects"]}
    categories = {item["id"]: item for item in graph["dependency_categories"]}
    names = {
        **{object_id: obj["name"] for object_id, obj in objects.items()},
        **{object_id: obj["name"] for object_id, obj in graph_objects.items()},
        **{object_id: item["node"] for object_id, item in categories.items()},
    }
    expected = {"faqi:" + subject_id: names[subject_id] for subject_id in names}
    fields_by_key = tool_explanations.validate_payload(root, explanations, expected)
    ordered = sorted(assignments, key=lambda item: (grade_order[item["grade_id"]], item["subject_id"]))
    tier_items = {
        tier: [item for item in ordered if item["grade_id"].split("-")[1] == tier]
        for tier, _label in GRADE_TIERS
    }

    index = [
        MARKER, "# Vibe Coding法器重要性总表", "", "## 字多不看", "",
        f"目录登记{len(assignments)}个对象的Vibe Coding重要性；部分软件工件已退役但保留历史重要性记录，不表示当前可运行。各对象使用v1的18项说明表；Vibe Coding 重要性暂定不代表效能验证。",
        "原始登记、来源及历史见[data.json](data.json)；来源初审与当前迁移位置分开，视图不产生运行、许可或效果批准。", "",
        "## 快速导航", "",
    ]
    for tier, label in GRADE_TIERS:
        index.append(f"- [{label}（{len(tier_items[tier])}项）]({tier}.md)")
    index.extend(("- [法器总表](#法器总表)", "- [原始说明](#原始说明)", "",
                  "<details>", "<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>", "",
                  "- [法器总表](#法器总表)", "- [原始说明](#原始说明)",
                  *(book_views.source_toc(root, "faqi") if root else []), "", "</details>", "",
                  "## 使用方式", "", f"按重要性阶打开对应文档；原始数据只在data.json维护，运行make sync-faqi-catalog更新{index_name}及四阶文档。", "",
                  "## 正文", "", "## 法器总表", ""))
    for tier, label in GRADE_TIERS:
        index.extend((f"### {label}", ""))
        for item in tier_items[tier]:
            subject_id = item["subject_id"]
            object_key = "faqi:" + subject_id
            anchor = tool_explanations.anchor_for(object_key)
            index.extend((f'<a id="{anchor}"></a>',
                          tool_explanations.render_file_link(object_key, names[subject_id], tier + ".md")))
        index.append("")
    index.extend(source_navigation(root) if root else ["## 原始说明", ""])
    views = {index_name: "\n".join(index) + "\n"}

    for tier, label in GRADE_TIERS:
        items = tier_items[tier]
        page = [MARKER, f"# Vibe Coding法器重要性总表：{label}", "",
                f"本页包含{len(items)}项{label}对象。分级仅表示重要性暂定，不代表效能验证。",
                f"- [返回总索引]({index_name})；其他阶：" + "、".join(
                    f"[{other_label}]({other_tier}.md)" for other_tier, other_label in GRADE_TIERS if other_tier != tier
                ), "", f"## {label}对象", ""]
        for item in items:
            object_key = "faqi:" + item["subject_id"]
            page.append(tool_explanations.render_index_link(object_key, names[item["subject_id"]]))
        page.append("")
        for item in items:
            object_key = "faqi:" + item["subject_id"]
            page.append(tool_explanations.render_object(object_key, names[item["subject_id"]], fields_by_key[object_key]))
        views[tier + ".md"] = "\n".join(page)
    require(sum(len(text.encode("utf-8")) for text in views.values()) <= MAX_BYTES,
            "四阶法器视图合计超过2 MiB")
    return views


def unchanged(bindings, root, data):
    source_archive.check_live(root)
    archives = source_archive.bundle_bindings(root)
    retired_submodules = set(source_archive.bundles(root)["faqi"]["data"].get("retired_submodules", []))
    for path, expected in bindings.items():
        if path == root / ".gitmodules" or path in archives:
            raw = source_archive.raw_read(path)
        else:
            raw = bounded_read(path)
        require(digest(raw) == expected, "输入被并行修改；不提交旧视图")
    for ref in data["references"]:
        path = safe_path(root, ref["path"], alias=True)
        if ref["state"] == "symlink":
            require(source_archive.source_is_symlink(path) and source_archive.source_readlink(path) == ref["target"], "来源链接被并行修改")
    repositories = {s["repository"]: s["revision"] for s in data["sources"]
                    if s["repository"] != "." and s["repository"] not in retired_submodules}
    for repository, revision in repositories.items():
        current_repository = source_archive.physical_path(root / repository).relative_to(root).as_posix()
        index = git_output(root, "ls-files", "--stage", "--", current_repository).decode().split()
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
    input_path = args.input.absolute() if args.input else root / ".github/metadata/faqi.json"
    view = args.view.absolute() if args.view else root / ".github/context/faqi/README.md"
    try:
        require(not input_path.is_symlink() and input_path.parent.resolve() == input_path.parent and
                not view.is_symlink() and view.parent.resolve() == view.parent, "输入/输出含软链接")
        data, _, objects, resources, _, bindings = validate(root, input_path)
        archive = source_archive.bundles(root).get("faqi")
        require(archive is not None and "explanations_v1" in archive["data"], "法器data.json缺少v1说明载荷")
        require(view.name not in {tier + ".md" for tier, _label in GRADE_TIERS}, "索引文件名不能与阶级文档冲突")
        rendered = render(data, objects, root, archive["data"]["explanations_v1"], view.name)
        outputs = {view: rendered[view.name]}
        outputs.update({view.parent / (tier + ".md"): rendered[tier + ".md"] for tier, _label in GRADE_TIERS})
        require(all(not path.is_symlink() for path in outputs), "生成目标不能是软链接")
        before = {path: bounded_read(path) if path.exists() else None for path in outputs}
        unchanged(bindings, root, data)
        if args.write:
            for path, previous in before.items():
                require(previous is None or previous.startswith(MARKER.encode()), "拒绝覆盖非本工具生成的文件：" + path.name)
            view.parent.mkdir(parents=True, exist_ok=True)
            temporaries = {}
            for path, raw in outputs.items():
                if before[path] == raw.encode("utf-8"):
                    continue
                with tempfile.NamedTemporaryFile(dir=view.parent, prefix=".faqi-catalog-", suffix=".tmp", delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(raw.encode("utf-8"))
                    stream.flush()
                    os.fsync(stream.fileno())
                temporaries[path] = temporary
            unchanged(bindings, root, data)
            for path, temporary in temporaries.items():
                require(not path.is_symlink() and
                        (bounded_read(path) if path.exists() else None) == before[path],
                        "目标被并行修改；保留临时文件，不覆盖：" + path.name)
                os.replace(temporary, path)
            for path, raw in outputs.items():
                require(bounded_read(path) == raw.encode("utf-8"), "写入后的法器视图与预期不符：" + path.name)
        else:
            for path, raw in outputs.items():
                require(before[path] == raw.encode("utf-8"), "法器视图缺失/陈旧或手改：" + path.name + "；运行make sync-faqi-catalog")
        unchanged(bindings, root, data)
        print(json.dumps({"status": "valid-master-classification-register", "objects": len(objects), "local_entries": len(data['local_entries']),
                          "local_exclusions": len(data['local_exclusions']), "external_resources": len(resources),
                          "dependency_objects": len(data['dependency_graph']['objects']),
                          "dependency_categories": len(data['dependency_graph']['dependency_categories']),
                          "provisional_grade_assignments": len(data['provisional_grade_assignments']),
                          "view_sha256": digest(outputs[view].encode("utf-8")),
                          "grade_view_sha256": {path.name: digest(raw.encode("utf-8")) for path, raw in outputs.items() if path != view},
                          **data['limits']}, ensure_ascii=False))
        return 0
    except (ContractError, OSError, ValueError, KeyError, TypeError, RecursionError, subprocess.TimeoutExpired, yaml.YAMLError, jsonschema.exceptions.SchemaError) as error:
        # 不回显输入对象或Git异常中的潜在敏感值；错误只定位契约位置。
        message = str(error) if isinstance(error, (ContractError, source_archive.ArchiveError)) else type(error).__name__
        print("FAQI_CATALOG_ERRORS\n" + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
