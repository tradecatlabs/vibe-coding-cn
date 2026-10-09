#!/usr/bin/env python3
"""以真实离线CLI消费首批法器清单；保留输入、输出和JUnit，不执行被审工具。"""
import argparse
import copy
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

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = None


class FaqiCatalogTest(unittest.TestCase):
    def invoke(self, label, *args, memory_limit=None):
        command = [sys.executable, str(ROOT / "scripts/sync-faqi-catalog.py"), *map(str, args)]
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
        self.assertEqual((19, 13, 158), (
            report["objects"], report["local_entries"], report["external_resources"]))
        self.assertFalse(report["independent_review"])
        self.assertFalse(report["runtime_verified"])
        data = json.loads((ROOT / "metadata/faqi.json").read_text(encoding="utf-8"))
        # 首批父仓库来源必须在已发布主线可达，不能依赖仅本地存在的提交。
        published = subprocess.run(["git", "merge-base", "--is-ancestor", data["source_revision"], "refs/remotes/origin/develop"], cwd=ROOT, capture_output=True, timeout=20)
        self.assertEqual(0, published.returncode, "父仓库来源不在已发布主线历史可达")
        objects = {o["id"]: o for o in data["objects"]}
        purposes = {s["id"]: s.get("purpose") for s in data["sources"]}
        # 用途来自实际读过的实现/说明选区，而非由对象引用反推。
        self.assertEqual("support", purposes["S01"])
        for sid in ("S02", "S04", "S06", "S08", "S09", "S10", "S12", "S16", "S18", "S21", "S23", "S25", "S26", "S27", "S28", "S29", "S32", "S34", "S36"):
            self.assertEqual("implementation", purposes[sid])
        # 期望来自实现选区与本体：可执行配置不是CLI本体，技能说明不是脚本。
        for name in ("faqi-tmux", "faqi-oh-my-tmux", "faqi-my-nvim-lua",
                     "faqi-codex-config-installer", "faqi-auto-tmux"):
            self.assertEqual("software-artifact", objects[name]["type_id"])
        self.assertNotIn("faqi-codex-cli", objects)
        decisions = {rid: r["decision"] for r in data["external_reviews"] for rid in r["resource_ids"]}
        self.assertEqual("excluded_model", decisions["tools-platforms-claude-opus-4-6-f751380c"])
        self.assertEqual("excluded_content", decisions["tools-platforms-prompt-jsonl-8e9b2066"])
        self.assertEqual("pending_identity", decisions["tools-platforms-zsh-d6d24951"])
        self.assertEqual("restricted_service_pending", decisions["network-payment-services-bybit-81d32c91"])
        self.assertEqual("related_local_source", decisions["repo-rules-scaffolds-tmux-9f36981a"])
        aliases = {a["path"]: a for a in data["references"]}
        for path in ("skills/auto-tmux/assets/tmux-src", "skills/auto-tmux/assets/oh-my-tmux"):
            self.assertEqual("empty-placeholder", aliases[path]["state"])
            self.assertIsNone(aliases[path]["related_object_id"])

    def test_rejects_unsupported_identity_and_source_claims_without_writing(self):
        original = json.loads((ROOT / "metadata/faqi.json").read_text(encoding="utf-8"))
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
        changed = copy.deepcopy(original); changed["sources"][0]["path"] = "tools/config/.codex/auth.json"
        cases.append(("credential-source", changed))
        changed = copy.deepcopy(original); changed["external_reviews"][0]["resource_ids"].pop()
        cases.append(("missing-resource", changed))
        changed = copy.deepcopy(original); changed["objects"][0]["grade"] = "天阶高级"
        cases.append(("grade-injection", changed))
        changed = copy.deepcopy(original); changed["objects"][0]["implementation"] = changed["sources"][0]["id"]
        cases.append(("description-as-implementation", changed))
        changed = copy.deepcopy(original)
        changed["local_entries"][0]["objects"], changed["local_entries"][1]["objects"] = changed["local_entries"][1]["objects"], changed["local_entries"][0]["objects"]
        cases.append(("wrong-entry-identity", changed))
        changed = copy.deepcopy(original); changed["sources"][1]["purpose"] = "support"
        cases.append(("unsupported-source-purpose", changed))
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
        data = json.loads((ROOT / "metadata/faqi.json").read_text(encoding="utf-8"))
        data["objects"][0]["name"] = '<script>unexpected</script> ``` [link](javascript:void(0)) |'
        input_path = self.input_copy("escaped", data)
        view = ARTIFACTS / "safe-view.md"
        self.assertEqual(0, self.invoke("write-first", "--input", input_path, "--view", view, "--write").returncode)
        first = view.read_bytes()
        parser = MarkdownIt("commonmark")
        markup = parser.render(first.decode())
        self.assertNotIn("<script>", markup)
        self.assertNotIn('href="javascript:', markup)
        tables = "\n".join(t.content for t in parser.parse(first.decode()) if t.type == "fence")
        # psql代码表是原样文本：HTML转义不能把依赖版本和原名称改成字面实体。
        self.assertIn("tmux>=2.6及awk/perl/grep/sed", tables)
        self.assertIn(data["objects"][0]["name"], tables)
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

    def test_wide_resource_table_fails_within_budget_without_writing(self):
        # 真实隔离Git/YAML输入；一条长名称使列宽×行数放大，不能先耗尽内存再检查输出。
        root = ARTIFACTS / "wide-table-fixture"; root.mkdir()
        (root / "metadata").mkdir(); (root / "tools/fixture").mkdir(parents=True)
        (root / "docs/gongfa").mkdir(parents=True)
        (root / "assets/external-resources").mkdir(parents=True)
        for path in ("metadata/faqi.schema.json", "docs/gongfa/cultivation-ontology-taxonomy.md"):
            (root / path).write_bytes((ROOT / path).read_bytes())
        body = b"def identity(value):\n    return value\n"
        (root / "tools/fixture/main.py").write_bytes(body)
        (root / ".gitmodules").write_bytes(b"")
        for index, command in enumerate((
            ["git", "init", "--quiet", str(root)],
            ["git", "-C", str(root), "add", ".gitmodules", "tools/fixture/main.py"],
            ["git", "-C", str(root), "-c", "user.name=tradecatlabs", "-c", "user.email=288998340+tradecatlabs@users.noreply.github.com", "commit", "--quiet", "--no-gpg-sign", "-m", "test: isolated source fixture"],
        )):
            result = subprocess.run(command, capture_output=True, timeout=20, env={**os.environ, "GIT_AUTHOR_DATE": "2026-10-09T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-10-09T00:00:00+00:00"})
            (ARTIFACTS / f"fixture-git-{index}.json").write_text(json.dumps({"command": command, "exit_code": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr.decode()}, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(0, result.returncode, result.stderr.decode())
        revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], timeout=20).decode().strip()
        data = json.loads((ROOT / "metadata/faqi.json").read_text(encoding="utf-8"))
        data["source_revision"] = revision
        source = {"id": "S01", "purpose": "implementation", "path": "tools/fixture/main.py", "repository": ".", "revision": revision, "sha256": hashlib.sha256(body).hexdigest(), "lines": [1, 3], "selection_sha256": hashlib.sha256(body).hexdigest()}
        data["sources"] = [source]
        data["objects"] = [{**data["objects"][0], "id": "faqi-fixture", "implementation": "S01", "support": []}]
        data["local_entries"] = [{"path": "tools/fixture", "objects": ["faqi-fixture"], "sources": ["S01"], "boundary": "隔离来源形态夹具，不证明工具能力", "pending": []}]
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
        data["external_reviews"] = [{"decision": "software_candidate", "rationale": "隔离资源宽表夹具，不作语义初审", "resource_ids": ids}]
        data["resource_notes"] = {}; data["local_resource_links"] = {}; data["references"] = []; data["relations"] = []
        view = ARTIFACTS / "budget-view.md"
        result = self.invoke("wide-table-budget", "--root", root, "--input", self.input_copy("wide-table", data), "--view", view, "--write", memory_limit=192 * 1024 * 1024)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("FAQI_CATALOG_ERRORS", result.stderr.decode())
        self.assertFalse(view.exists())

    def test_strict_json(self):
        original = (ROOT / "metadata/faqi.json").read_text(encoding="utf-8")
        for label, text in (
            ("duplicate-json-key", original.replace('{', '{"format_version": 1,', 1)),
            ("non-json-number", original.replace('"format_version": 1', '"format_version": NaN', 1)),
            ("oversized-json", original + " " * (2 * 1024 * 1024 + 1)),
            ("non-json-infinity", original.replace('"format_version": 1', '"format_version": Infinity', 1)),
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
