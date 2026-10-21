#!/usr/bin/env python3
"""原始资料JSON存储的行为契约；保存隔离输入与结果，不调用模型或第三方程序。"""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ARTIFACTS = Path(tempfile.mkdtemp(prefix='source-archive-test-'))
MODULE = Path(__file__).with_name('source_archive.py')
spec = importlib.util.spec_from_file_location('source_archive_test_subject', MODULE)
archive = importlib.util.module_from_spec(spec)


def document(raw, mode='100644'):
    try:
        data, encoding = raw.decode('utf-8'), 'utf-8'
    except UnicodeDecodeError:
        data, encoding = base64.b64encode(raw).decode('ascii'), 'base64'
    return {'mode': mode, 'encoding': encoding, 'data': data, 'sha256': hashlib.sha256(raw).hexdigest()}


class SourceArchiveTest(unittest.TestCase):
    def setUp(self):
        self.root = ARTIFACTS / self._testMethodName
        self.path = self.root / '.github/context/gongfa/data.json'
        self.path.parent.mkdir(parents=True)
        self.data = {'format': 'vibe-coding-cn/source-archive@1', 'kind': 'gongfa',
                     'source_revision': 'a' * 40, 'documents': {}, 'locations': {}, 'live_sources': {}, 'projections': []}
        archive.clear_cache()

    def save(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')

    def test_original_bytes_are_distinct_from_live_implementation(self):
        old = '.github/metadata/gongfa/source-original.txt'
        self.data['documents'][old] = document('原始\r\n资料\n'.encode('utf-8'))
        self.data['locations'][old] = '.github/extensions/current.txt'
        self.data['live_sources'][old] = {'path': '.github/extensions/current.txt',
                                         'sha256': hashlib.sha256(b'current implementation').hexdigest()}
        live = self.root / '.github/extensions/current.txt'
        live.parent.mkdir(parents=True)
        live.write_bytes(b'current implementation')
        self.save()
        self.assertEqual(archive.read_bytes(self.root / old), '原始\r\n资料\n'.encode('utf-8'))
        self.assertEqual(archive.physical_path(self.root / old), live)
        archive.check_live(self.root)
        live.write_bytes(b'unreviewed change')
        with self.assertRaises(ValueError): archive.check_live(self.root)

    def test_binary_and_symlink_payloads_roundtrip_without_dereference(self):
        self.data['documents'] = {'.github/metadata/gongfa/history.xlsx': document(b'\x00\xff\x01'),
                                  '.github/skills/original-ref': document(b'../fixed-source', '120000')}
        self.save()
        self.assertEqual(archive.read_bytes(self.root / '.github/metadata/gongfa/history.xlsx'), b'\x00\xff\x01')
        self.assertTrue(archive.source_is_symlink(self.root / '.github/skills/original-ref'))
        self.assertEqual(archive.source_readlink(self.root / '.github/skills/original-ref'), '../fixed-source')
        target = self.root / 'exported'
        archive.export_documents(self.root, 'gongfa', target)
        self.assertEqual((target / '.github/metadata/gongfa/history.xlsx').read_bytes(), b'\x00\xff\x01')
        self.assertTrue((target / '.github/skills/original-ref').is_symlink())

    def test_rejects_corruption_unsafe_ids_and_bad_json(self):
        for identity in ['../outside', '.github/../outside', '.github/config/auth.json', '.github/.env']:
            with self.subTest(identity=identity):
                self.data['documents'] = {identity: document(b'not a credential')}
                self.save(); archive.clear_cache()
                with self.assertRaises(ValueError): archive.read_bytes(self.root / '.github/metadata/gongfa/registry.json')
        self.data['documents'] = {'.github/metadata/gongfa/registry.json': document(b'{}')}
        self.data['documents']['.github/metadata/gongfa/registry.json']['sha256'] = '0' * 64
        self.save(); archive.clear_cache()
        with self.assertRaises(ValueError): archive.read_bytes(self.root / '.github/metadata/gongfa/registry.json')
        for raw in ['{"format":"x","format":"y"}', '{"format":NaN}']:
            self.path.write_text(raw); archive.clear_cache()
            with self.assertRaises(ValueError): archive.read_bytes(self.root / '.github/metadata/gongfa/registry.json')

    def test_rejects_missing_current_location_target(self):
        old = '.github/metadata/gongfa/source-original.txt'
        self.data['documents'][old] = document(b'archived source')
        self.data['locations'][old] = '.github/extensions/retired-entry.sh'
        self.save()
        with self.assertRaisesRegex(ValueError, '当前位置映射目标不存在'):
            archive.read_bytes(self.root / old)

    def test_rejects_live_path_escape_and_changed_input(self):
        old = '.github/metadata/gongfa/registry.json'
        self.data['documents'][old] = document(b'{}')
        self.data['locations'][old] = '../outside'
        self.save()
        with self.assertRaises(ValueError): archive.read_bytes(self.root / old)
        self.data['locations'] = {}; self.save(); archive.clear_cache()
        self.assertEqual(archive.read_bytes(self.root / old), b'{}')
        self.path.write_text(self.path.read_text() + '\n')
        with self.assertRaises(ValueError): archive.check_unchanged(self.root)
        archive.clear_cache()
        self.path.rename(self.path.with_suffix('.original'))
        self.path.symlink_to(self.path.with_suffix('.original'))
        with self.assertRaises(ValueError): archive.read_bytes(self.root / old)

    def test_book_view_namespaces_headings_links_and_preserves_code(self):
        import book_views
        text = '# 示例\n\n<a id="目标"></a>\n## 目标\n\n[另一篇](other.md#目标)\n\n[other.md](other.md)\n\n[other[0..4]复核](other.md)\n\n````text\n### 代码不是目录\n```\n````\n'
        text += ('\n[校验](../../scripts/check-gongfa.py)\n'
                 '\n[测试](../../extensions/test-source-archive.py)\n'
                 '\n[依赖](../../scripts/requirements-gongfa.txt)\n'
                 '\n[共享库](../../scripts/lib/README.md)\n'
                 '\n[资料读取](../../scripts/lib/source_archive.py)\n'
                 '\n[视图模块](../../extensions/lib/book_views.py)\n'
                 '\n[分类模块](../../lib/taxonomy.py)\n'
                 '\n[资源边界](../../lib/__init__.py)\n')
        retired_links = {
            '../../tools/chat-vault/README.md': 'chat-vault/README.md',
            '../../tools/external/my-nvim/README.md': 'my-nvim/README.md',
            '../../tools/config/.codex/README.md': 'codex-config/.codex/README.md',
            '../../tools/external/MCPlayerTransfer/README.md': 'MCPlayerTransfer/README.md',
            '../../tools/external/XHS-image-to-PDF-conversion/README.md': 'XHS-image-to-PDF-conversion/README.md',
            '../../tools/external/html-tools-main/xhs%20graphic%20production%20-%201.0.html': 'xhs%20graphic%20production%20-%201.0.html',
            '../../tools/external/html-tools-main/xhs%20graphic%20production.html': 'xhs%20graphic%20production.html',
            '../../tools/external/html-tools-main/README.md': 'html-tools-main.md',
            '../../tools/prompts-library/README.md': 'prompts-library/README.md',
        }
        for index, link in enumerate(retired_links):
            text += f'\n[历史{index}]({link})\n'
        retired_cloud_links = {
            '../../skills/auto-tmux/SKILL.md': ('blob', '.github/skills/auto-tmux/SKILL.md'),
            '../../context/assets/': ('tree', '.github/context/assets'),
            '../../context/assets/templates/tool-explanation-template-v1.md': (
                'blob', '.github/context/assets/templates/tool-explanation-template-v1.md'),
            '../../context/external-resources/README.md': (
                'blob', '.github/context/external-resources/README.md'),
        }
        for index, link in enumerate(retired_cloud_links):
            text += f'\n[云端退役{index}]({link})\n'
        self.data['documents'] = {
            '.github/docs/gongfa/example.md': document(text.encode()),
            '.github/docs/gongfa/other.md': document('# 另一篇\n\n## 目标\n'.encode())}
        self.save()
        rendered = book_views.render_sources(self.root, 'gongfa')
        index = self.root / '.github/context/metadata/taxonomy.yml'
        index.parent.mkdir(parents=True)
        index.write_text('documents:\n  gongfa:\n  - path: .github/context/gongfa/README.md#doc-other\n  - path: .github/context/gongfa/README.md#doc-example\n')
        self.assertEqual(rendered, book_views.render_sources(self.root, 'gongfa'), '阅读内容与顺序只由本集合JSON决定')
        self.assertIn('id="doc-example-目标"', rendered)
        self.assertIn('#doc-other-目标', rendered)
        self.assertIn('[other.md](#doc-other)', rendered)
        self.assertIn('[other[0..4]复核](#doc-other)', rendered)
        self.assertIn('[校验](../../check-gongfa.py)', rendered)
        self.assertIn('[测试](../../test-source-archive.py)', rendered)
        self.assertIn('[依赖](../../requirements-gongfa.txt)', rendered)
        self.assertIn('[共享库](../../AGENTS.md#维护脚本与共享库)', rendered)
        self.assertIn('[资料读取](../../source_archive.py)', rendered)
        self.assertIn('[视图模块](../../book_views.py)', rendered)
        self.assertIn('[分类模块](../../taxonomy.py)', rendered)
        self.assertIn('[资源边界](../../source_boundaries.py)', rendered)
        for index, target in enumerate(retired_links.values()):
            revision = ('b0e3454bb865b95bdc70127a431214c384542dee'
                        if target == 'prompts-library/README.md'
                        else '44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58')
            expected = (f'https://github.com/tradecatlabs/vibe-coding-cn/blob/{revision}'
                        '/.github/extensions/' + target)
            self.assertIn(f'[历史{index}]({expected})', rendered)
        for index, (route, path) in enumerate(retired_cloud_links.values()):
            expected = (f'https://github.com/tradecatlabs/vibe-coding-cn/{route}/'
                        f'71bf460cfa894ad45163a9591d2043422974a681/{path}')
            self.assertIn(f'[云端退役{index}]({expected})', rendered)
        self.assertIn('### 代码不是目录', rendered)
        self.assertNotIn('id="doc-example-代码不是目录"', rendered)
        self.assertEqual(rendered.count('id="doc-example-目标"'), 1)
        from markdown_it import MarkdownIt
        self.assertIn('<h2>示例</h2>', MarkdownIt('commonmark').render(rendered))
        toc = '\n'.join(book_views.source_toc(self.root, 'gongfa'))
        self.assertIn('](#doc-example-目标)', toc)
        self.assertIn('](#doc-other-目标)', toc)
        self.assertNotIn('代码不是目录', toc)

    def test_v1_explanations_remain_separate_from_frozen_source_documents(self):
        explanation = {'template_sha256': 'a' * 64, 'items': []}
        self.data['explanations_v1'] = explanation
        self.save()
        archive.clear_cache()
        bundle = archive.bundles(self.root)['gongfa']
        self.assertEqual(explanation, bundle['data']['explanations_v1'])
        self.assertNotIn('explanations_v1', bundle['bytes'])

    def test_retired_v0_explanation_payload_is_rejected(self):
        self.data['explanations_v0'] = {'template_sha256': 'a' * 64, 'items': []}
        self.save()
        archive.clear_cache()
        with self.assertRaises(ValueError):
            archive.bundles(self.root)

    def test_independent_raw_input_remains_readable(self):
        raw_root = self.root / 'standalone-input'
        path = raw_root / '.github/metadata/gongfa/registry.json'
        path.parent.mkdir(parents=True)
        path.write_bytes(b'{"independent":"input"}\n')
        self.assertEqual(archive.read_bytes(path), b'{"independent":"input"}\n')


if __name__ == '__main__':
    try:
        spec.loader.exec_module(archive)
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SourceArchiveTest))
        report = {'success': result.wasSuccessful(), 'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors)}
    except (OSError, ImportError) as error:
        report = {'success': False, 'error': type(error).__name__}
    report['test_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ARTIFACTS / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'artifacts': str(ARTIFACTS), **report}, ensure_ascii=False))
    raise SystemExit(0 if report['success'] else 1)
