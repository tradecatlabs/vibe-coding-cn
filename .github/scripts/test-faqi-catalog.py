#!/usr/bin/env python3
"""以真实离线CLI消费首批法器清单；保留输入、输出和JUnit，不执行被审工具。"""
import argparse
import copy
from collections import Counter
import hashlib
import json
import os
import resource
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = None


class FaqiCatalogTest(unittest.TestCase):
    def invoke(self, label, *args, memory_limit=None):
        command = [sys.executable, str(ROOT / ".github/scripts/sync-faqi-catalog.py"), *map(str, args)]
        def bound_memory():
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
        result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=45,
                                preexec_fn=bound_memory if memory_limit else None)
        (ARTIFACTS / (label + ".json")).write_text(json.dumps({
            "command": command, "exit_code": result.returncode,
            "stdout": result.stdout.decode(), "stderr": result.stderr.decode(),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return result

    def input_copy(self, label, data):
        path = ARTIFACTS / (label + "-input.json")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def test_current_source_review_is_consumable(self):
        result = self.invoke("current", "--check")
        self.assertEqual(0, result.returncode, result.stderr.decode())
        report = json.loads(result.stdout)
        self.assertEqual((10, 13, 9, 158, 12, 8), (
            report["objects"], report["local_entries"], report["local_exclusions"], report["external_resources"],
            report["dependency_objects"], report["dependency_categories"]))
        self.assertFalse(report["independent_review"])
        self.assertFalse(report["runtime_verified"])
        self.assertTrue(report["grades_assigned"])
        data = json.loads((ROOT / ".github/metadata/faqi.json").read_text(encoding="utf-8"))
        self.assertEqual("faqi-master-classification-register", data["kind"])
        dependency_objects = {o["id"]: o for o in data["dependency_graph"]["objects"]}
        self.assertNotIn("dep-claude-code", dependency_objects)
        self.assertEqual("1.1.0", dependency_objects["dep-pi-cli"]["version"])
        self.assertEqual("software-artifact", dependency_objects["dep-pi-cli"]["type_id"])
        self.assertIn("8类", data["dependency_graph"]["user_confirmation"]["statement"])
        self.assertEqual(8, len(data["dependency_graph"]["dependency_categories"]))
        self.assertTrue(all(item["disposition"] == "user_confirmed_in_scope" for item in data["dependency_graph"]["dependency_categories"]))
        self.assertTrue(all(o["grade_id"] is None and o["grade_status"] == "pending" for o in dependency_objects.values()))
        assignments = data["provisional_grade_assignments"]
        expected_subjects = ({o["id"] for o in data["objects"]} | set(dependency_objects) |
                             {node["id"] for node in data["dependency_graph"]["dependency_categories"]})
        self.assertEqual(expected_subjects, {item["subject_id"] for item in assignments})
        self.assertTrue(all(item["assignment_status"] == "user_directed_provisional" for item in assignments))
        self.assertEqual({
            "faqi-tian-advanced": 2, "faqi-tian-intermediate": 2,
            "faqi-di-advanced": 3, "faqi-di-intermediate": 5, "faqi-di-initial": 4,
            "faqi-xuan-advanced": 2, "faqi-xuan-intermediate": 4, "faqi-xuan-initial": 3,
            "faqi-huang-advanced": 3, "faqi-huang-intermediate": 1, "faqi-huang-initial": 1,
        }, Counter(item["grade_id"] for item in assignments))
        self.assertEqual(30, len(assignments))
        self.assertTrue(all(item["basis"] for item in assignments))
        self.assertTrue(all(link["object_id"] in {o["id"] for o in data["objects"]} for link in data["dependency_graph"]["local_links"]))
        catalog = (ROOT / ".github/tools/faqi-catalog.md").read_text(encoding="utf-8")
        self.assertNotIn("dep-claude-code", catalog)
        self.assertNotIn("Claude Code（依赖图替代项）", catalog)
        self.assertIn("Vibe Coding 重要性暂定", catalog)
        self.assertIn("天阶高级", catalog)
        self.assertIn("Codex CLI", catalog)
        self.assertNotIn("对象ID", catalog)
        self.assertNotIn("依赖图位置", catalog)
        tokens = MarkdownIt("default").parse(catalog)
        table_indexes = [index for index, token in enumerate(tokens) if token.type == "table_open"]
        self.assertEqual(1, len(table_indexes), "简表只保留一张表")
        table_index = table_indexes[0]
        thead_start = next(index for index in range(table_index + 1, len(tokens)) if tokens[index].type == "thead_open")
        thead_end = next(index for index in range(thead_start + 1, len(tokens)) if tokens[index].type == "thead_close")
        self.assertEqual(["品级", "名称", "解释"], [token.content for token in tokens[thead_start:thead_end] if token.type == "inline"])
        tbody_start = next(index for index in range(thead_end + 1, len(tokens)) if tokens[index].type == "tbody_open")
        tbody_end = next(index for index in range(tbody_start + 1, len(tokens)) if tokens[index].type == "tbody_close")
        self.assertEqual(len(assignments), sum(token.type == "tr_open" for token in tokens[tbody_start:tbody_end]))
        self.assertIn(assignments[0]["scope"] + "；" + assignments[0]["basis"], catalog)
        # 首批父仓库来源必须在已发布主线可达，不能依赖仅本地存在的提交。
        published = subprocess.run(["git", "merge-base", "--is-ancestor", data["source_revision"], "refs/remotes/origin/develop"], cwd=ROOT, capture_output=True, timeout=20)
        self.assertEqual(0, published.returncode, "父仓库来源不在已发布主线历史可达")
        objects = {o["id"]: o for o in data["objects"]}
        purposes = {s["id"]: s.get("purpose") for s in data["sources"]}
        # 用途来自实际读过的实现/说明选区，而非由对象引用反推。
        self.assertEqual("support", purposes["S01"])
        for sid in ("S02", "S06", "S08", "S09", "S10", "S12", "S16", "S18", "S21", "S23"):
            self.assertEqual("implementation", purposes[sid])
        expected_exclusion_sources = {"S04", "S25", "S26", "S27", "S28", "S29", "S32", "S34", "S36"}
        for sid in expected_exclusion_sources:
            self.assertEqual("exclusion_evidence", purposes[sid])
        exclusions = {(item["path"], item["name"]): item for item in data["local_exclusions"]}
        expected_excluded = {
            (".github/tools/chat-vault", "Chat Vault同步与查询程序"): "私人对话数据",
            (".github/tools/external/MCPlayerTransfer", "Minecraft基岩版角色迁移程序"): "LevelDB",
            (".github/tools/external/XHS-image-to-PDF-conversion", "小红书图片ZIP转PDF程序"): "原ZIP",
            (".github/tools/external/html-tools-main", "EPUB CSS清理网页程序"): "按用户指定",
            (".github/tools/external/html-tools-main", "Markdown预览与文本导出网页程序"): "按用户指定",
            (".github/tools/external/html-tools-main", "任务卡片PNG导出网页程序"): "按用户指定",
            (".github/tools/external/html-tools-main", "小红书内容卡片PNG导出网页程序"): "按用户指定",
            (".github/tools/external/html-tools-main", "Markdown同步预览与PNG导出网页程序"): "按用户指定",
            (".github/tools/external/my-nvim", "my-nvim的LazyVim引导配置程序"): "按用户指定",
        }
        self.assertEqual(set(expected_excluded), set(exclusions))
        self.assertEqual(expected_exclusion_sources, {item["source"] for item in data["local_exclusions"]})
        for key, evidence in expected_excluded.items():
            self.assertIn(evidence, exclusions[key]["rationale"])
        empty_paths = {entry["path"] for entry in data["local_entries"] if not entry["objects"]}
        self.assertEqual({key[0] for key in expected_excluded}, empty_paths)
        for excluded_id in (
            "faqi-chat-vault", "faqi-mc-player-transfer", "faqi-xhs-zip-pdf",
            "faqi-html-epub-css", "faqi-html-markdown-text", "faqi-html-task-card",
            "faqi-html-xhs-card", "faqi-html-markdown-sync-png", "faqi-my-nvim-lua",
        ):
            self.assertNotIn(excluded_id, objects)
        # 期望来自实现选区与本体：可执行配置不是CLI本体，技能说明不是脚本。
        for name in ("faqi-tmux", "faqi-oh-my-tmux", "faqi-codex-config-installer", "faqi-auto-tmux"):
            self.assertEqual("software-artifact", objects[name]["type_id"])
        self.assertNotIn("faqi-codex-cli", objects)
        decisions = {rid: r["decision"] for r in data["external_reviews"] for rid in r["resource_ids"]}
        self.assertEqual("excluded_model", decisions["tools-platforms-claude-opus-4-6-f751380c"])
        self.assertEqual("excluded_content", decisions["tools-platforms-prompt-jsonl-8e9b2066"])
        self.assertEqual("pending_identity", decisions["tools-platforms-zsh-d6d24951"])
        self.assertEqual("restricted_service_pending", decisions["network-payment-services-bybit-81d32c91"])
        self.assertEqual("related_local_source", decisions["repo-rules-scaffolds-tmux-9f36981a"])
        aliases = {a["path"]: a for a in data["references"]}
        for path in (".github/skills/auto-tmux/assets/tmux-src", ".github/skills/auto-tmux/assets/oh-my-tmux"):
            self.assertEqual("empty-placeholder", aliases[path]["state"])
            self.assertIsNone(aliases[path]["related_object_id"])

    def test_rejects_unsupported_identity_and_source_claims_without_writing(self):
        original = json.loads((ROOT / ".github/metadata/faqi.json").read_text(encoding="utf-8"))
        changed = copy.deepcopy(original)
        changed["objects"].append({**changed["objects"][0], "id": "faqi-duplicate-cli-mcp"})
        cases = [("same-content-two-identities", changed)]
        changed = copy.deepcopy(original); changed["objects"][0]["type_id"] = "model-artifact"
        cases.append(("model-as-tool", changed))
        changed = copy.deepcopy(original); changed["limits"]["runtime_verified"] = True
        cases.append(("invented-runtime", changed))
        changed = copy.deepcopy(original); changed["sources"][0]["sha256"] = "0" * 64
        cases.append(("source-drift", changed))
        changed = copy.deepcopy(original); changed["sources"][0]["lines"] = [1, 999999]
        cases.append(("selection-overrun", changed))
        changed = copy.deepcopy(original); changed["sources"][0]["path"] = "../../outside.py"
        cases.append(("path-escape", changed))
        changed = copy.deepcopy(original); changed["sources"][0]["path"] = ".github/tools/config/.codex/auth.json"
        cases.append(("credential-source", changed))
        changed = copy.deepcopy(original); changed["external_reviews"][0]["resource_ids"].pop()
        cases.append(("missing-resource", changed))
        changed = copy.deepcopy(original); changed["objects"][0]["grade"] = "天阶高级"
        cases.append(("grade-injection", changed))
        changed = copy.deepcopy(original); changed["provisional_grade_assignments"][0]["grade_id"] = "invented-grade"
        cases.append(("unsupported-provisional-grade", changed))
        changed = copy.deepcopy(original); changed["provisional_grade_assignments"].pop()
        cases.append(("missing-provisional-grade", changed))
        changed = copy.deepcopy(original); changed["dependency_graph"]["objects"][0]["type_id"] = "invented-platform"
        cases.append(("unknown-dependency-type", changed))
        changed = copy.deepcopy(original); changed["dependency_graph"]["source_sha256"] = "0" * 64
        cases.append(("dependency-graph-source-drift", changed))
        changed = copy.deepcopy(original); changed["objects"][0]["implementation"] = changed["sources"][0]["id"]
        cases.append(("description-as-implementation", changed))
        changed = copy.deepcopy(original)
        changed["local_entries"][0]["objects"], changed["local_entries"][1]["objects"] = changed["local_entries"][1]["objects"], changed["local_entries"][0]["objects"]
        cases.append(("wrong-entry-identity", changed))
        changed = copy.deepcopy(original); changed["sources"][1]["purpose"] = "support"
        cases.append(("unsupported-source-purpose", changed))
        changed = copy.deepcopy(original); changed["local_exclusions"] = []
        cases.append(("unrecorded-empty-entry", changed))
        changed = copy.deepcopy(original)
        changed["local_exclusions"].append(copy.deepcopy(next(item for item in changed["local_exclusions"] if item["source"] == "S04")))
        cases.append(("duplicate-exclusion-record", changed))
        for source_id, path, name, support in (
            ("S04", ".github/tools/chat-vault", "Chat Vault同步与查询程序", ["S03"]),
            ("S25", ".github/tools/external/html-tools-main", "EPUB CSS清理网页程序", ["S24"]),
            ("S32", ".github/tools/external/my-nvim", "my-nvim的LazyVim引导配置程序", ["S30", "S31"]),
        ):
            changed = copy.deepcopy(original)
            excluded_source = next(i for i, source in enumerate(changed["sources"]) if source["id"] == source_id)
            changed["sources"][excluded_source]["purpose"] = "implementation"
            resurrected = {"id": f"faqi-{source_id.lower()}-reintroduced", "name": name, "type_id": "software-artifact", "implementation": source_id, "support": support, "boundary": "反事实复入测试，不作新批准", "declared_version": None}
            changed["objects"].append(resurrected)
            entry = next(item for item in changed["local_entries"] if item["path"] == path)
            entry["objects"].append(resurrected["id"])
            cases.append((f"excluded-source-{source_id}-reclassified-as-implementation", changed))
        changed = copy.deepcopy(original); changed["sources"][1]["selection_sha256"] = "0" * 64
        cases.append(("selection-drift", changed))
        changed = copy.deepcopy(original); changed["objects"][0]["name"] = "程序\n```\n<script>"
        cases.append(("control-character-injection", changed))
        changed = copy.deepcopy(original); changed["references"][2]["state"] = "symlink"
        cases.append(("placeholder-as-link", changed))
        for label, data in cases:
            with self.subTest(label=label):
                view = ARTIFACTS / (label + ".md")
                result = self.invoke(label, "--input", self.input_copy(label, data), "--view", view, "--write")
                self.assertNotEqual(0, result.returncode)
                self.assertIn("FAQI_CATALOG_ERRORS", result.stderr.decode())
                self.assertFalse(view.exists())

    def test_repeatable_view_escaping_and_ownership(self):
        data = json.loads((ROOT / ".github/metadata/faqi.json").read_text(encoding="utf-8"))
        data["objects"][0]["name"] = '<script>unexpected</script> ``` [link](javascript:void(0)) |'
        input_path = self.input_copy("escaped", data)
        view = ARTIFACTS / "safe-view.md"
        self.assertEqual(0, self.invoke("write-first", "--input", input_path, "--view", view, "--write").returncode)
        first = view.read_bytes()
        parser = MarkdownIt("default")
        tokens = parser.parse(first.decode())
        markup = parser.render(first.decode())
        self.assertNotIn("<script>", markup)
        self.assertNotIn('href="javascript:', markup)
        table_column_counts = []
        for index, token in enumerate(tokens):
            if token.type != "table_open":
                continue
            row_counts = []
            current_count = 0
            for nested in tokens[index + 1:]:
                if nested.type == "table_close":
                    break
                if nested.type == "tr_open":
                    current_count = 0
                elif nested.type in {"th_open", "td_open"}:
                    current_count += 1
                elif nested.type == "tr_close":
                    row_counts.append(current_count)
            self.assertTrue(row_counts)
            self.assertEqual(1, len(set(row_counts)), "表格单元格中的管道符不能拆出额外列")
            table_column_counts.append(row_counts[0])
        self.assertEqual([3], table_column_counts, "Markdown浏览表只展示品级、名称和解释")
        self.assertIn("&lt;script&gt;unexpected&lt;/script&gt;", markup)
        self.assertEqual(0, self.invoke("write-repeat", "--input", input_path, "--view", view, "--write").returncode)
        self.assertEqual(first, view.read_bytes())
        self.assertEqual(0, self.invoke("check-repeat", "--input", input_path, "--view", view, "--check").returncode)
        view.write_bytes(first + b"\nmanual-drift\n")
        self.assertNotEqual(0, self.invoke("stale-view", "--input", input_path, "--view", view, "--check").returncode)
        plain = ARTIFACTS / "not-owned.md"; plain.write_text("必须保留的人工文档\n", encoding="utf-8")
        self.assertNotEqual(0, self.invoke("reject-non-owned", "--input", input_path, "--view", plain, "--write").returncode)
        self.assertEqual("必须保留的人工文档\n", plain.read_text(encoding="utf-8"))
        link = ARTIFACTS / "symlink.md"; link.symlink_to(plain)
        self.assertNotEqual(0, self.invoke("reject-output-link", "--input", input_path, "--view", link, "--write").returncode)
        self.assertEqual("必须保留的人工文档\n", plain.read_text(encoding="utf-8"))
        alias = ARTIFACTS / "input-parent-alias"; alias.symlink_to(ARTIFACTS, target_is_directory=True)
        forbidden = ARTIFACTS / "parent-link-view.md"
        result = self.invoke("reject-input-parent-link", "--input", alias / input_path.name, "--view", forbidden, "--write")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(forbidden.exists())

    def test_wide_external_resources_do_not_expand_compact_view(self):
        # 真实隔离Git/YAML输入；宽外部资源原表不进入三列浏览表。
        root = ARTIFACTS / "wide-table-fixture"; root.mkdir()
        (root / ".github/metadata").mkdir(parents=True); (root / ".github/tools/fixture").mkdir(parents=True)
        (root / ".github/docs/gongfa").mkdir(parents=True)
        (root / ".github/assets/external-resources").mkdir(parents=True)
        for path in (".github/metadata/faqi.schema.json", ".github/docs/gongfa/cultivation-ontology-taxonomy.md", ".github/docs/gongfa/technology-stack.md"):
            (root / path).write_bytes((ROOT / path).read_bytes())
        body = b"def identity(value):\n    return value\n"
        (root / ".github/tools/fixture/main.py").write_bytes(body)
        (root / ".gitmodules").write_bytes(b"")
        for index, command in enumerate((
            ["git", "init", "--quiet", str(root)],
            ["git", "-C", str(root), "add", ".gitmodules", ".github/tools/fixture/main.py"],
            ["git", "-C", str(root), "-c", "user.name=tradecatlabs", "-c", "user.email=288998340+tradecatlabs@users.noreply.github.com", "commit", "--quiet", "--no-gpg-sign", "-m", "test: isolated source fixture"],
        )):
            result = subprocess.run(command, capture_output=True, timeout=20, env={**os.environ, "GIT_AUTHOR_DATE": "2026-10-09T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-10-09T00:00:00+00:00"})
            (ARTIFACTS / f"fixture-git-{index}.json").write_text(json.dumps({"command": command, "exit_code": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr.decode()}, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(0, result.returncode, result.stderr.decode())
        revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], timeout=20).decode().strip()
        data = json.loads((ROOT / ".github/metadata/faqi.json").read_text(encoding="utf-8"))
        data["source_revision"] = revision
        source = {"id": "S01", "purpose": "implementation", "path": ".github/tools/fixture/main.py", "repository": ".", "revision": revision, "sha256": hashlib.sha256(body).hexdigest(), "lines": [1, 3], "selection_sha256": hashlib.sha256(body).hexdigest()}
        data["sources"] = [source]
        data["objects"] = [{**data["objects"][0], "id": "faqi-fixture", "implementation": "S01", "support": []}]
        data["dependency_graph"]["local_links"] = [{"object_id": "faqi-fixture", "graph_node": "fixture node", "relationship": "仅用于隔离表格预算测试。"}]
        allowed_grade_subjects = {"faqi-fixture"} | {item["id"] for item in data["dependency_graph"]["objects"]} | {item["id"] for item in data["dependency_graph"]["dependency_categories"]}
        data["provisional_grade_assignments"] = [item for item in data["provisional_grade_assignments"] if item["subject_id"] in allowed_grade_subjects]
        data["provisional_grade_assignments"].append({"subject_id": "faqi-fixture", "grade_id": "faqi-huang-initial", "assignment_status": "user_directed_provisional", "scope": "宽表隔离夹具", "basis": "仅验证表格预算，不作效果判断。"})
        for dependency_object in data["dependency_graph"]["objects"]:
            dependency_object["resource_ids"] = []
            dependency_object["related_object_id"] = None
        data["local_entries"] = [{"path": ".github/tools/fixture", "objects": ["faqi-fixture"], "sources": ["S01"], "boundary": "隔离来源形态夹具，不证明工具能力", "pending": []}]
        ids = []
        for file_index, source in enumerate(data["external_sources"]):
            rows = []
            for index in range(512 if file_index == 0 else 1):
                rid = f"fixture-{file_index}-{index}"; ids.append(rid)
                name = "x" * (512 * 1024) if file_index == index == 0 else "短名称"
                rows.append({"id": rid, "name": name, "status": "active"})
            raw = json.dumps({"defaults": {"verification_status": "imported-unverified"}, "resources": rows}, ensure_ascii=False).encode()
            self.assertLess(len(raw), 2 * 1024 * 1024)
            (root / source["path"]).write_bytes(raw); source["sha256"] = hashlib.sha256(raw).hexdigest()
        data["local_exclusions"] = []
        data["external_reviews"] = [{"decision": "software_candidate", "rationale": "隔离资源宽表夹具，不作语义初审", "resource_ids": ids}]
        data["resource_notes"] = {}; data["local_resource_links"] = {}; data["references"] = []; data["relations"] = []
        view = ARTIFACTS / "budget-view.md"
        result = self.invoke("wide-resource-compact-view", "--root", root, "--input", self.input_copy("wide-table", data), "--view", view, "--write", memory_limit=192 * 1024 * 1024)
        self.assertEqual(0, result.returncode, result.stderr.decode())
        rendered = view.read_bytes()
        self.assertLess(len(rendered), 64 * 1024)
        self.assertNotIn(b"x" * 4096, rendered)
        tokens = MarkdownIt("default").parse(rendered.decode("utf-8"))
        table_indexes = [index for index, token in enumerate(tokens) if token.type == "table_open"]
        self.assertEqual(1, len(table_indexes))

    def test_dependency_graph_table_and_grade_assignments_are_complete(self):
        data = json.loads((ROOT / ".github/metadata/faqi.json").read_text(encoding="utf-8"))
        graph = data["dependency_graph"]
        self.assertEqual(".github/docs/gongfa/technology-stack.md", graph["source_path"])
        self.assertGreaterEqual(len(graph["objects"]), 12)
        self.assertGreaterEqual(len(graph["dependency_categories"]), 7)
        self.assertEqual(9, len(graph["local_links"]))
        self.assertTrue(data["limits"]["grades_assigned"])
        result = self.invoke("dependency-graph-table", "--check")
        self.assertEqual(0, result.returncode, result.stderr.decode())

    def test_strict_json(self):
        original = (ROOT / ".github/metadata/faqi.json").read_text(encoding="utf-8")
        for label, text in (
            ("duplicate-json-key", original.replace('{', '{"format_version": 1,', 1)),
            ("non-json-number", original.replace('"format_version": 2', '"format_version": NaN', 1)),
            ("oversized-json", original + " " * (2 * 1024 * 1024 + 1)),
            ("non-json-infinity", original.replace('"format_version": 2', '"format_version": Infinity', 1)),
        ):
            with self.subTest(label=label):
                path = ARTIFACTS / (label + "-input.json"); path.write_text(text, encoding="utf-8")
                result = self.invoke(label, "--input", path, "--check")
                self.assertNotEqual(0, result.returncode)
                self.assertIn("FAQI_CATALOG_ERRORS", result.stderr.decode())


def main():
    global ARTIFACTS
    parser = argparse.ArgumentParser(description="法器初审清单离线CLI行为验证，保留隔离工件")
    parser.add_argument("--artifacts", type=Path)
    parser.add_argument("--current-only", action="store_true")
    args = parser.parse_args()
    if args.artifacts:
        ARTIFACTS = args.artifacts.resolve(); ARTIFACTS.mkdir(parents=True, exist_ok=False)
    else:
        ARTIFACTS = Path(tempfile.mkdtemp(prefix="faqi-catalog-test-"))
    suite = unittest.TestSuite([FaqiCatalogTest("test_current_source_review_is_consumable")]) if args.current_only else unittest.defaultTestLoader.loadTestsFromTestCase(FaqiCatalogTest)
    test_ids = [test.id() for test in suite]
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {"tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
               "passed": result.wasSuccessful(), "independent_review": False, "reviewed_tools_executed": False,
               "artifact_directory": str(ARTIFACTS)}
    (ARTIFACTS / "result.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    junit = ET.Element("testsuite", name="faqi-catalog", tests=str(result.testsRun), failures=str(len(result.failures)), errors=str(len(result.errors)))
    for test_id in test_ids:
        case = ET.SubElement(junit, "testcase", name=test_id)
        for kind, issues in (("failure", result.failures), ("error", result.errors)):
            for test, trace in issues:
                if test.id() == test_id or test.id().startswith(test_id + " "):
                    ET.SubElement(case, kind).text = trace
    ET.ElementTree(junit).write(ARTIFACTS / "junit.xml", encoding="utf-8", xml_declaration=True)
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
