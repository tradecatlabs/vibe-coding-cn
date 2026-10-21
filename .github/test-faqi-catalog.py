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
import source_archive

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = None
TEMPLATE = ROOT / ".github/context/assets/templates/tool-explanation-template-v1.md"


def v1_field_names():
    names = []
    for line in TEMPLATE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and line.split("|")[1].strip().isdigit():
            names.append(line.split("|")[2].strip())
    return names


def v1_payload(subject_names):
    labels = v1_field_names()
    return {
        "template_sha256": hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),
        "items": [
            {
                "object_key": "faqi:" + subject_id,
                "fields": [
                    {"name": label, "content": name if index == 0 else "隔离夹具：" + label}
                    for index, label in enumerate(labels)
                ],
            }
            for subject_id, name in subject_names.items()
        ],
    }


class FaqiCatalogTest(unittest.TestCase):
    def invoke(self, label, *args, memory_limit=None):
        command = [sys.executable, str(ROOT / ".github/extensions/sync-faqi-catalog.py"), *map(str, args)]
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
        data = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
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
        directory = ROOT / ".github/context/faqi"
        catalog = (directory / "README.md").read_text(encoding="utf-8")
        self.assertEqual({p.name for p in directory.iterdir()},
                         {'data.json', 'README.md', 'tian.md', 'di.md', 'xuan.md', 'huang.md'})
        pages = {tier: (directory / f"{tier}.md").read_text(encoding="utf-8")
                 for tier in ("tian", "di", "xuan", "huang")}
        all_views = catalog + "\n" + "\n".join(pages.values())
        active_archive = json.loads((directory / "data.json").read_text(encoding="utf-8"))
        skill_seekers = next(item for item in active_archive["explanations_v1"]["items"]
                             if item["object_key"] == "faqi:faqi-skill-seekers")
        association = next(field["content"] for field in skill_seekers["fields"]
                           if field["name"] == "关联信息")
        self.assertIn("LICENSE文本标为MIT，但版权行仍为[Your Name/Username]占位符", association)
        self.assertIn("同修订pyproject.toml的authors字段列为Yusuf Karaaslan", association)
        self.assertIn("作者元数据不证明版权归属或授权", association)
        self.assertIn("本项目仍未批准该许可证", association)
        self.assertIn("本地入口=.github/extensions/Skill_Seekers-development", association)
        current_paths = {
            "faqi:faqi-skill-seekers": ".github/extensions/Skill_Seekers-development",
            "faqi:faqi-oh-my-tmux": ".github/extensions/oh-my-tmux",
            "faqi:faqi-tmux": ".github/extensions/tmux",
            "faqi:faqi-claude-skill-init": ".github/extensions/claude-official-skills",
        }
        associations = {
            item["object_key"]: next(field["content"] for field in item["fields"] if field["name"] == "关联信息")
            for item in active_archive["explanations_v1"]["items"]
        }
        for object_key, path in current_paths.items():
            self.assertIn(f"本地入口={path}", associations[object_key], object_key)
        self.assertNotIn(".github/tools/prompts-library", active_archive["locations"])
        self.assertFalse(any(path.startswith(".github/tools/prompts-library/")
                             for path in active_archive["live_sources"]))
        for archived_path in (
            ".github/tools/prompts-library/README.md",
            ".github/tools/prompts-library/main.py",
        ):
            self.assertIn(archived_path, active_archive["documents"])
            self.assertNotIn(archived_path, active_archive["locations"])
        for object_key in (
            "faqi:faqi-prompt-converter",
            "faqi:faqi-codex-config-installer",
            "faqi:faqi-auto-skill-create",
            "faqi:faqi-auto-skill-validate",
            "faqi:faqi-skill-seekers-adapter",
            "faqi:faqi-auto-tmux",
        ):
            self.assertIn("本地入口=无", associations[object_key], object_key)
            self.assertIn("已退役", associations[object_key], object_key)
        converter_association = associations["faqi:faqi-prompt-converter"]
        self.assertNotIn(".github/extensions/prompts-library", converter_association)
        for path in (
            ".github/skills/auto-skill/scripts/create-skill.sh",
            ".github/skills/auto-skill/scripts/validate-skill.sh",
            ".github/skills/auto-skill/scripts/skill-seekers.sh",
            ".github/skills/auto-tmux/scripts/auto-tmux.sh",
        ):
            self.assertNotIn(path, active_archive["locations"], path)
        fields_by_name = {field["name"]: field["content"] for field in skill_seekers["fields"]}
        implementation = fields_by_name["内部如何实现？"]
        cost = fields_by_name["付出了什么代价？"]
        applicability = fields_by_name["明确这些规律成立的前提与适用条件。"]
        conclusion = fields_by_name["结论"]
        warrant = fields_by_name["连接规则"]
        evidence = fields_by_name["依据"]
        self.assertIn("默认绑定127.0.0.1", implementation)
        self.assertIn("可通过--host指定其他地址", implementation)
        self.assertIn('allow_origins=["*"]', implementation)
        self.assertIn("所检server路径未配置应用层认证", implementation)
        self.assertIn("api_key参数最终加入子进程argv（--api-key）", cost)
        self.assertIn("形成进程参数暴露面", cost)
        self.assertIn("可被不可信调用者访问", cost)
        self.assertIn("仅固定修订26638b248279a3b001b651475e0f28975f5ff069的S67–S73选区", applicability)
        self.assertIn("未运行服务、导入或执行上游代码", applicability)
        self.assertIn("静态审阅结果：WARN", conclusion)
        self.assertIn("不要向不可信网络暴露HTTP MCP", conclusion)
        self.assertIn("来源S67/S68显示", warrant)
        self.assertIn("S67, S68, S69, S70, S71, S72, S73", evidence)
        self.assertIn("静态审阅结果：WARN", pages["xuan"])
        self.assertIn("固定修订许可观察", pages["xuan"])
        self.assertNotIn("dep-claude-code", all_views)
        self.assertNotIn("Claude Code（依赖图替代项）", all_views)
        self.assertIn("Vibe Coding 重要性暂定", catalog)
        self.assertIn("部分软件工件已退役但保留历史重要性记录", catalog)
        self.assertIn("不表示当前可运行", catalog)
        self.assertIn("Codex CLI", catalog)
        self.assertIn("<a id=\"doc-faqi-system\"></a>", catalog)
        self.assertIn("## 法器总表", catalog)
        self.assertNotIn("| 序号 | 说明项 | 内容 |", catalog)
        self.assertIn("天阶高级", pages["tian"])
        self.assertIn("法器对象ID=faqi-prompt-converter", all_views)
        self.assertIn("依赖图对象ID=dep-pi-cli", all_views)
        self.assertNotIn("依赖图位置", all_views)
        field_names = v1_field_names()
        self.assertEqual(18, len(field_names))
        import tool_explanations
        table_count = 0
        tier_counts = Counter(item["grade_id"].split("-")[1] for item in assignments)
        for tier, page in pages.items():
            tokens = MarkdownIt("default").parse(page)
            table_indexes = [index for index, token in enumerate(tokens) if token.type == "table_open"]
            self.assertEqual(tier_counts[tier], len(table_indexes), f"{tier}文档只包含对应阶级的法器对象")
            table_count += len(table_indexes)
            for table_index in table_indexes:
                table_end = next(index for index in range(table_index + 1, len(tokens)) if tokens[index].type == "table_close")
                table_tokens = tokens[table_index:table_end + 1]
                self.assertEqual(19, sum(token.type == "tr_open" for token in table_tokens), "一行表头加18项说明")
                inline = [token.content for token in table_tokens if token.type == "inline"]
                self.assertEqual(["序号", "说明项", "内容"], inline[:3])
                self.assertEqual(field_names, [inline[4 + index * 3] for index in range(18)])
                self.assertEqual(57, sum(token.type in {"th_open", "td_open"} for token in table_tokens), "每张表严格三列")
        self.assertEqual(len(assignments), table_count, "每个法器对象恰好出现在一个阶级文档中")
        for item in assignments:
            tier = item["grade_id"].split("-")[1]
            anchor = tool_explanations.anchor_for("faqi:" + item["subject_id"])
            self.assertIn(f"{tier}.md#{anchor}", catalog)
            self.assertIn(f'<a id="{anchor}"></a>', catalog, "旧README对象锚点应保留为跳转入口")
        self.assertIn(assignments[0]["scope"], all_views)
        self.assertIn(assignments[0]["basis"], all_views)
        # 首批父仓库来源必须在已发布主线可达，不能依赖仅本地存在的提交。
        published = subprocess.run(["git", "merge-base", "--is-ancestor", data["source_revision"], "refs/remotes/origin/main"], cwd=ROOT, capture_output=True, timeout=20)
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
        self.assertEqual(("symlink", "../../../tools/external/tmux", "faqi-tmux"), (
            aliases[".github/skills/auto-tmux/assets/tmux-src"]["state"],
            aliases[".github/skills/auto-tmux/assets/tmux-src"]["target"],
            aliases[".github/skills/auto-tmux/assets/tmux-src"]["related_object_id"],
        ))
        self.assertEqual(("symlink", "../../../tools/external/.tmux", "faqi-oh-my-tmux"), (
            aliases[".github/skills/auto-tmux/assets/oh-my-tmux"]["state"],
            aliases[".github/skills/auto-tmux/assets/oh-my-tmux"]["target"],
            aliases[".github/skills/auto-tmux/assets/oh-my-tmux"]["related_object_id"],
        ))

    def test_license_evidence_sources_are_support_only(self):
        data = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
        implementation = next(source for source in data["sources"] if source["id"] == "S18")
        relative_path = Path(".github/tools/external/.tmux/LICENSE.MIT")
        body = source_archive.read_bytes(ROOT / relative_path)
        line_count = len(body.decode("utf-8").splitlines(keepends=True))
        license_source_id = "S_TEST_LICENSE"
        self.assertNotIn(license_source_id, {source["id"] for source in data["sources"]})
        license_source = {
            "id": license_source_id, "purpose": "support", "path": relative_path.as_posix(),
            "repository": implementation["repository"], "revision": implementation["revision"],
            "sha256": hashlib.sha256(body).hexdigest(), "lines": [1, line_count + 1],
            "selection_sha256": hashlib.sha256(body).hexdigest(),
        }
        data["sources"].append(license_source)
        skill_object = next(
            item for item in data["objects"] if item["id"] == "faqi-oh-my-tmux"
        )
        skill_object["support"].append(license_source_id)
        local_entry = next(
            item
            for item in data["local_entries"]
            if item["path"] == ".github/tools/external/.tmux"
        )
        local_entry["sources"].append(license_source_id)
        result = self.invoke("license-document-as-support", "--input", self.input_copy("license-support", data), "--check")
        self.assertEqual(0, result.returncode, result.stderr.decode())
        self.assertFalse(data["limits"]["license_approved"], "记录许可证原文不等于项目批准")

        license_source["purpose"] = "implementation"
        result = self.invoke("license-document-as-implementation", "--input", self.input_copy("license-implementation", data), "--check")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("来源不是公开代码、配置或说明", result.stderr.decode())

        support_only_sources = ("S57", "S58", "S61", "S62", "S63", "S64")
        for source_id in ("S57", "S58", "S59", "S60", "S61", "S62", "S63", "S64"):
            data = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
            source = next(item for item in data["sources"] if item["id"] == source_id)
            self.assertEqual("support", source["purpose"])
            if source_id not in support_only_sources:
                continue
            source["purpose"] = "implementation"
            result = self.invoke(
                f"{source_id.lower()}-notice-as-implementation",
                "--input", self.input_copy(f"{source_id.lower()}-implementation", data), "--check",
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("来源不是公开代码、配置或说明", result.stderr.decode())

        data = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
        unsupported_image = next(item for item in data["sources"] if item["id"] == "S64")
        unsupported_image["path"] = ".github/tools/external/tmux/logo/icons/128x128/tmux.png"
        result = self.invoke(
            "unsupported-image-as-notice-source",
            "--input", self.input_copy("unsupported-image", data), "--check",
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("来源不是公开代码、配置或说明", result.stderr.decode())

    def test_rejects_unsupported_identity_and_source_claims_without_writing(self):
        original = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
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
        changed = copy.deepcopy(original); changed["references"][2]["state"] = "empty-placeholder"
        changed["references"][2]["target"] = None
        changed["references"][2]["related_object_id"] = None
        cases.append(("symlink-as-placeholder", changed))
        for label, data in cases:
            with self.subTest(label=label):
                view = ARTIFACTS / (label + ".md")
                result = self.invoke(label, "--input", self.input_copy(label, data), "--view", view, "--write")
                self.assertNotEqual(0, result.returncode)
                self.assertIn("FAQI_CATALOG_ERRORS", result.stderr.decode())
                self.assertFalse(view.exists())

    def test_repeatable_view_escaping_and_ownership(self):
        data = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
        input_path = self.input_copy("repeatable", data)
        view = ARTIFACTS / "safe-view.md"
        self.assertEqual(0, self.invoke("write-first", "--input", input_path, "--view", view, "--write").returncode)
        view_files = [view, *(view.parent / f"{tier}.md" for tier in ("tian", "di", "xuan", "huang"))]
        first = {path: path.read_bytes() for path in view_files}
        parser = MarkdownIt("default")
        table_column_counts = []
        total_tables = 0
        for path in view_files[1:]:
            tokens = parser.parse(path.read_bytes().decode("utf-8"))
            table_indexes = [index for index, token in enumerate(tokens) if token.type == "table_open"]
            total_tables += len(table_indexes)
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
                self.assertEqual(19, len(row_counts), "每个对象表格必须包含表头和18行说明")
                self.assertEqual({3}, set(row_counts), "表格必须严格为三列")
                table_column_counts.append(row_counts[0])
        self.assertEqual(30, total_tables)
        self.assertEqual([3] * 30, table_column_counts)
        import tool_explanations
        hostile_fields = [{"name": label, "content": label} for label in v1_field_names()]
        hostile_fields[1]["content"] = '<script>unexpected</script> ``` [link](javascript:void(0)) |'
        safe_table = tool_explanations.render_table(hostile_fields)
        safe_markup = parser.render(safe_table)
        self.assertNotIn("<script>", safe_markup)
        self.assertNotIn('href="javascript:', safe_markup)
        self.assertIn("&lt;script&gt;unexpected&lt;/script&gt;", safe_markup)
        self.assertIn("&#124;", safe_table)
        self.assertEqual(0, self.invoke("write-repeat", "--input", input_path, "--view", view, "--write").returncode)
        self.assertEqual(first, {path: path.read_bytes() for path in view_files})
        self.assertEqual(0, self.invoke("check-repeat", "--input", input_path, "--view", view, "--check").returncode)
        view.write_bytes(first[view] + b"\nmanual-drift\n")
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
        (root / ".github/metadata").mkdir(parents=True); (root / ".github/tools/config/.codex").mkdir(parents=True)
        (root / ".github/docs/gongfa").mkdir(parents=True)
        (root / ".github/assets/external-resources").mkdir(parents=True)
        for path in (".github/metadata/faqi.schema.json", ".github/docs/gongfa/cultivation-ontology-taxonomy.md", ".github/docs/gongfa/technology-stack.md"):
            (root / path).write_bytes(source_archive.read_bytes(ROOT / path))
        body = b'RAW_BASE="https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/.github/tools/config/.codex"\nprintf "fixture only\\n"\n'
        program = root / ".github/tools/config/.codex/install.sh"
        program.write_bytes(body)
        reference_path = root / ".github/skills/auto-tmux/assets/oh-my-tmux"
        reference_path.parent.mkdir(parents=True)
        reference_path.write_bytes(b"")
        gitmodules = b'[submodule "tmux"]\n\tpath = .github/tools/external/.tmux\n\turl = https://github.com/example/tmux.git\n'
        (root / ".gitmodules").write_bytes(gitmodules)
        for index, command in enumerate((
            ["git", "init", "--quiet", str(root)],
            ["git", "-C", str(root), "add", ".gitmodules", ".github/tools/config/.codex/install.sh", ".github/skills/auto-tmux/assets/oh-my-tmux"],
            ["git", "-C", str(root), "-c", "user.name=tradecatlabs", "-c", "user.email=288998340+tradecatlabs@users.noreply.github.com", "commit", "--quiet", "--no-gpg-sign", "-m", "test: isolated source fixture"],
        )):
            result = subprocess.run(command, capture_output=True, timeout=20, env={**os.environ, "GIT_AUTHOR_DATE": "2026-10-09T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-10-09T00:00:00+00:00"})
            (ARTIFACTS / f"fixture-git-{index}.json").write_text(json.dumps({"command": command, "exit_code": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr.decode()}, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(0, result.returncode, result.stderr.decode())
        revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], timeout=20).decode().strip()
        historical_placeholder = ARTIFACTS / "historical-empty-reference-placeholder"
        reference_path.rename(historical_placeholder)
        self.assertEqual(b"", historical_placeholder.read_bytes())
        reference_path.symlink_to("../../../tools/external/.tmux")
        for command in (
            ["git", "-C", str(root), "add", ".github/skills/auto-tmux/assets/oh-my-tmux"],
            ["git", "-C", str(root), "-c", "user.name=tradecatlabs", "-c", "user.email=288998340+tradecatlabs@users.noreply.github.com", "commit", "--quiet", "--no-gpg-sign", "-m", "test: restore registered submodule link"],
        ):
            result = subprocess.run(command, capture_output=True, timeout=20, env={**os.environ, "GIT_AUTHOR_DATE": "2026-10-09T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-10-09T00:00:00+00:00"})
            self.assertEqual(0, result.returncode, result.stderr.decode())
        data = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
        data["source_revision"] = revision
        source = {"id": "S01", "purpose": "implementation", "path": ".github/tools/config/.codex/install.sh", "repository": ".", "revision": revision, "sha256": hashlib.sha256(body).hexdigest(), "lines": [1, 3], "selection_sha256": hashlib.sha256(body).hexdigest()}
        data["sources"] = [source]
        data["objects"] = [{**data["objects"][0], "id": "faqi-fixture", "implementation": "S01", "support": []}]
        data["dependency_graph"]["local_links"] = [{"object_id": "faqi-fixture", "graph_node": "fixture node", "relationship": "仅用于隔离表格预算测试。"}]
        allowed_grade_subjects = {"faqi-fixture"} | {item["id"] for item in data["dependency_graph"]["objects"]} | {item["id"] for item in data["dependency_graph"]["dependency_categories"]}
        data["provisional_grade_assignments"] = [item for item in data["provisional_grade_assignments"] if item["subject_id"] in allowed_grade_subjects]
        data["provisional_grade_assignments"].append({"subject_id": "faqi-fixture", "grade_id": "faqi-huang-initial", "assignment_status": "user_directed_provisional", "scope": "宽表隔离夹具", "basis": "仅验证表格预算，不作效果判断。"})
        subject_names = {
            **{item["id"]: item["name"] for item in data["objects"]},
            **{item["id"]: item["name"] for item in data["dependency_graph"]["objects"]},
            **{item["id"]: item["node"] for item in data["dependency_graph"]["dependency_categories"]},
        }
        (root / ".github/context/faqi").mkdir(parents=True, exist_ok=True)
        template_copy = root / ".github/context/assets/templates/tool-explanation-template-v1.md"
        template_copy.parent.mkdir(parents=True, exist_ok=True)
        template_copy.write_bytes(TEMPLATE.read_bytes())
        archive_data = {
            "format": "vibe-coding-cn/source-archive@1", "kind": "faqi", "source_revision": "a" * 40,
            "documents": {}, "locations": {}, "live_sources": {}, "projections": [],
            "explanations_v1": v1_payload(subject_names),
        }
        (root / ".github/context/faqi/data.json").write_text(json.dumps(archive_data, ensure_ascii=False, indent=2), encoding="utf-8")
        source_archive.clear_cache()
        for dependency_object in data["dependency_graph"]["objects"]:
            dependency_object["resource_ids"] = []
            dependency_object["related_object_id"] = None
        data["local_entries"] = [{"path": ".github/tools/config/.codex", "objects": ["faqi-fixture"], "sources": ["S01"], "boundary": "隔离来源形态夹具，不证明工具能力", "pending": []}]
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
        data["resource_notes"] = {}; data["local_resource_links"] = {}
        data["references"] = [{
            "path": ".github/skills/auto-tmux/assets/oh-my-tmux",
            "state": "symlink",
            "target": "../../../tools/external/.tmux",
            "related_object_id": None,
            "boundary": "仅验证历史零字节占位入口可被明确替换为当前相对软链接；隔离夹具不证明目标仓库内容。"
        }]
        data["relations"] = []
        view = ARTIFACTS / "budget-view.md"
        result = self.invoke("wide-resource-compact-view", "--root", root, "--input", self.input_copy("wide-table", data), "--view", view, "--write", memory_limit=192 * 1024 * 1024)
        self.assertEqual(0, result.returncode, result.stderr.decode())
        registered_link = ARTIFACTS / "registered-reference-link"
        reference_path.rename(registered_link)
        reference_path.symlink_to("../../../tools/external/unregistered")
        bad_reference = copy.deepcopy(data)
        bad_reference["references"][0]["target"] = "../../../tools/external/unregistered"
        forbidden_reference_view = ARTIFACTS / "unregistered-reference-view.md"
        result = self.invoke("reject-unregistered-reference-target", "--root", root,
                             "--input", self.input_copy("unregistered-reference", bad_reference),
                             "--view", forbidden_reference_view, "--write")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("已登记submodule", result.stderr.decode())
        self.assertFalse(forbidden_reference_view.exists())
        unregistered_link = ARTIFACTS / "unregistered-reference-link"
        reference_path.rename(unregistered_link)
        registered_link.rename(reference_path)
        rendered = view.read_bytes()
        self.assertLess(len(rendered), 64 * 1024)
        self.assertNotIn(b"x" * 4096, rendered)
        view_files = [view, *(view.parent / f"{tier}.md" for tier in ("tian", "di", "xuan", "huang"))]
        table_count = 0
        for path in view_files[1:]:
            page_bytes = path.read_bytes()
            self.assertNotIn(b"x" * 4096, page_bytes)
            tokens = MarkdownIt("default").parse(page_bytes.decode("utf-8"))
            table_indexes = [index for index, token in enumerate(tokens) if token.type == "table_open"]
            table_count += len(table_indexes)
            self.assertEqual(len(table_indexes), page_bytes.count("| 序号 | 说明项 | 内容 |".encode()))
            for index in table_indexes:
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
                self.assertEqual([3] * 19, row_counts, "每张表严格三列并含18项")
        self.assertEqual(21, table_count, "隔离对象必须各自进入一张且仅一张阶级页v1表格")
        # 只允许已批准的同仓默认分支地址迁移，来源原 SHA 与指令仍固定。
        input_path = self.input_copy("branch-migration", data)
        main_body = b'RAW_BASE="https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/main/.github/tools/config/.codex"\nprintf "fixture only\\n"\n'
        program.write_bytes(main_body)
        result = self.invoke("approved-main-source", "--root", root, "--input", input_path, "--view", view, "--write")
        self.assertEqual(0, result.returncode, result.stderr.decode())
        for label, candidate in (
            ("wrong-source-owner", main_body.replace(b"/tukuaiai/", b"/other-owner/")),
            ("wrong-source-branch", main_body.replace(b"/main/", b"/unreviewed/")),
            ("changed-program", main_body + b'printf "changed behavior\\n"\n'),
        ):
            with self.subTest(label=label):
                program.write_bytes(candidate)
                forbidden = ARTIFACTS / (label + "-view.md")
                result = self.invoke(label, "--root", root, "--input", input_path, "--view", forbidden, "--write")
                self.assertNotEqual(0, result.returncode)
                self.assertIn("来源文件/SHA漂移", result.stderr.decode())
                self.assertFalse(forbidden.exists())
        # 后续真正冻结 main 版本时，不应被历史地址适配反向改坏。
        program.write_bytes(main_body)
        for command in (
            ["git", "-C", str(root), "add", ".github/tools/config/.codex/install.sh"],
            ["git", "-C", str(root), "-c", "user.name=tradecatlabs", "-c", "user.email=288998340+tradecatlabs@users.noreply.github.com", "commit", "--quiet", "--no-gpg-sign", "-m", "test: freeze main source"],
        ):
            result = subprocess.run(command, capture_output=True, timeout=20, env={**os.environ, "GIT_AUTHOR_DATE": "2026-10-13T00:00:00+00:00", "GIT_COMMITTER_DATE": "2026-10-13T00:00:00+00:00"})
            self.assertEqual(0, result.returncode, result.stderr.decode())
        revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], timeout=20).decode().strip()
        data["source_revision"] = revision
        data["sources"][0].update(revision=revision, sha256=hashlib.sha256(main_body).hexdigest(), selection_sha256=hashlib.sha256(main_body).hexdigest())
        result = self.invoke("frozen-main-source", "--root", root, "--input", self.input_copy("frozen-main", data), "--view", view, "--write")
        self.assertEqual(0, result.returncode, result.stderr.decode())

    def test_dependency_graph_table_and_grade_assignments_are_complete(self):
        data = json.loads(source_archive.read_text(ROOT / ".github/metadata/faqi.json"))
        graph = data["dependency_graph"]
        self.assertEqual(".github/docs/gongfa/technology-stack.md", graph["source_path"])
        self.assertGreaterEqual(len(graph["objects"]), 12)
        self.assertGreaterEqual(len(graph["dependency_categories"]), 7)
        self.assertEqual(9, len(graph["local_links"]))
        self.assertTrue(data["limits"]["grades_assigned"])
        result = self.invoke("dependency-graph-table", "--check")
        self.assertEqual(0, result.returncode, result.stderr.decode())

    def test_strict_json(self):
        original = source_archive.read_text(ROOT / ".github/metadata/faqi.json")
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
