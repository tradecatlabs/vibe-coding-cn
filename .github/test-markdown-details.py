#!/usr/bin/env python3
"""验证代码围栏不会泄漏示例标签，且正文真实错误仍被 CLI 拒绝；保留隔离工件。"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


# 期望来自 CommonMark 0.31.2 §4.5 和字面 HTML 配对，不调用被测提取器计算。
CASES = [
    ("nested_backticks", "# 示例\n\n````markdown\n```html\n<details>\n```\n````\n", 0),
    ("nested_tildes", "# 示例\n\n~~~~markdown\n~~~html\n<details>\n~~~\n~~~~\n", 0),
    ("closer_with_info", "```markdown\n``` not-a-closer\n<details>\n```\n", 0),
    ("outer_details", "<details>\n<summary>有效</summary>\n\n````markdown\n```html\n<details>\n```\n````\n</details>\n", 0),
    ("longer_closer", "~~~text\n<details>\n~~~~~  \t\n", 0),
    ("mismatched_closer", "````markdown\n~~~\n<details>\n````\n", 0),
    ("plain_fence", "```html\n<details>\n```\n<details>\n<summary>正文</summary>\n</details>\n", 0),
    ("real_error", "````markdown\n<details>\n````\n<details>\n<summary>缺少结束</summary>\n", 1),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, default=Path(__file__).with_name("check-markdown-details.py"))
    parser.add_argument("--artifacts", type=Path)
    args = parser.parse_args()
    source = args.checker.resolve(strict=True).read_bytes()
    # 隔离CLI保留其真实公共布局依赖，不复制或改写被测围栏逻辑。
    layout = Path(__file__).with_name('lib').joinpath('__init__.py').read_bytes()
    if args.artifacts:
        artifacts = args.artifacts.resolve()
        artifacts.mkdir(parents=True, exist_ok=False)
    else:
        artifacts = Path(tempfile.mkdtemp(prefix="markdown-details-test-"))
    records = []

    class DetailsFenceTest(unittest.TestCase):
        def test_fences_and_real_html_errors(self):
            for name, markdown, expected in CASES:
                with self.subTest(case=name):
                    case = artifacts / name
                    script = case / '.github/check-markdown-details.py'
                    script.parent.mkdir(parents=True)
                    script.write_bytes(source)
                    library = script.parent / 'lib'
                    library.mkdir()
                    (library / '__init__.py').write_bytes(layout)
                    (case / "README.md").write_text(markdown, encoding="utf-8")
                    command = [sys.executable, str(script)]
                    completed = subprocess.run(command, capture_output=True, text=True, timeout=10)
                    (case / "stdout.log").write_text(completed.stdout, encoding="utf-8")
                    (case / "stderr.log").write_text(completed.stderr, encoding="utf-8")
                    records.append({"case": name, "command": command, "expected_exit_code": expected,
                                    "actual_exit_code": completed.returncode})
                    self.assertEqual(completed.returncode, expected, completed.stdout + completed.stderr)
                    if expected:
                        self.assertIn("README.md:4:", completed.stdout)
                        self.assertIn("MARKDOWN_DETAILS_ERRORS", completed.stdout)
                    else:
                        self.assertIn("OK markdown details checked", completed.stdout)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DetailsFenceTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"success": result.wasSuccessful(), "cases": records,
              "checker_sha256": hashlib.sha256(source).hexdigest(),
              "layout_sha256": hashlib.sha256(layout).hexdigest(),
              "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "specification": "https://spec.commonmark.org/0.31.2/#fenced-code-blocks"}
    (artifacts / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"success": report["success"], "cases": len(records), "artifacts": str(artifacts)}, ensure_ascii=False))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
