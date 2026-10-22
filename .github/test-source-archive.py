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
                 '\n[资源边界](../../lib/__init__.py)\n'
                 '\n[文档目录同步](../../extensions/sync-doc-toc.py)\n'
                 '\n[法器生成器](../../extensions/sync-faqi-catalog.py)\n'
                 '\n[功法生成器](../../extensions/sync-gongfa-catalog.py)\n'
                 '\n[研究抓取](../../extensions/fetch-research-raw.py)\n'
                 '\n[Claude旧初始化器入口](../../extensions/init_skill.py)\n'
                 '\n[Claude根级旧初始化器入口](../../init_skill.py)\n'
                 '\n[Claude官方初始化脚本历史来源](../../tools/external/claude-official-skills/skills/skill-creator/scripts/init_skill.py)\n'
                 '\n[Skill Seekers历史源码](../../tools/external/Skill_Seekers-development/README.md)\n')
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
        flattened_context_links = {
            '../../context/ai-citation/README.md': 'ai-citation-README.md',
            '../../context/metadata/taxonomy.yml': 'taxonomy.yml',
            '../../context/prompts/README.md': 'prompts-README.md',
            '../../context/getting-started/learning-map.md': 'god.md',
            # 单一代码块不产生章节锚点；历史定位保留在输入，当前入口指向整份提示词。
            '../../learning-map.md#milestone-2': 'god.md',
            '../getting-started/learning-map.md#ai-guidance-rules': 'god.md',
            '../getting-started/learning-map.md#milestone-0': 'god.md',
            '../../god.md#milestone-2': 'god.md',
            '../../context/tool-explanation-template-v1.md': 'tool-explanation-template-v1.md',
        }
        for index, link in enumerate(retired_cloud_links):
            text += f'\n[云端退役{index}]({link})\n'
        for index, link in enumerate(flattened_context_links):
            text += f'\n[平铺{index}]({link})\n'
        self.data['documents'] = {
            '.github/docs/gongfa/example.md': document(text.encode()),
            '.github/docs/gongfa/other.md': document('# 另一篇\n\n## 目标\n'.encode())}
        self.save()
        rendered = book_views.render_sources(self.root, 'gongfa')
        index = self.root / '.github/taxonomy.yml'
        index.parent.mkdir(parents=True, exist_ok=True)
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
        for label, target in (
            ('文档目录同步', 'sync-doc-toc.py'),
            ('法器生成器', 'sync-faqi-catalog.py'),
            ('功法生成器', 'sync-gongfa-catalog.py'),
            ('研究抓取', 'fetch-research-raw.py'),
        ):
            self.assertIn(f'[{label}](../../{target})', rendered)
        claude_initializer = (
            'https://github.com/anthropics/skills/blob/'
            '1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563/'
            'skills/skill-creator/scripts/init_skill.py')
        self.assertIn(f'[Claude旧初始化器入口]({claude_initializer})', rendered)
        self.assertIn(f'[Claude根级旧初始化器入口]({claude_initializer})', rendered)
        self.assertIn(f'[Claude官方初始化脚本历史来源]({claude_initializer})', rendered)
        self.assertIn(
            '[Skill Seekers历史源码](https://github.com/yusufkaraaslan/Skill_Seekers/blob/'
            '26638b248279a3b001b651475e0f28975f5ff069/README.md)', rendered)
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
        for index, target in enumerate(flattened_context_links.values()):
            self.assertIn(f'[平铺{index}](../../{target})', rendered)
        self.assertIn('### 代码不是目录', rendered)
        self.assertNotIn('id="doc-example-代码不是目录"', rendered)
        self.assertEqual(rendered.count('id="doc-example-目标"'), 1)
        from markdown_it import MarkdownIt
        self.assertIn('<h2>示例</h2>', MarkdownIt('commonmark').render(rendered))
        toc = '\n'.join(book_views.source_toc(self.root, 'gongfa'))
        self.assertIn('](#doc-example-目标)', toc)
        self.assertIn('](#doc-other-目标)', toc)
        self.assertNotIn('代码不是目录', toc)

    def test_god_prompt_is_one_expanded_copyable_code_block(self):
        from markdown_it import MarkdownIt
        import book_views
        text = Path(__file__).with_name('god.md').read_text(encoding='utf-8')
        tokens = MarkdownIt('commonmark').parse(text)
        self.assertEqual([token.type for token in tokens], ['fence'])
        prompt = tokens[0].content
        self.assertTrue(prompt.startswith('# 道成了肉身\n'))
        self.assertNotRegex(prompt, r'</?(?:details|summary|a)\b')
        self.assertNotRegex(prompt, r'\]\(#[^)]+\)')
        self.assertIn("printf 'local shell OK\\n'", prompt)
        first_reply = next(
            (line[2:] for line in prompt.splitlines() if line.startswith('> 我会先确认')),
            '',
        )
        self.assertEqual(first_reply.count('？'), 1)
        self.assertNotIn('command -v pi', prompt)
        self.assertNotIn('Get-Command pi -ErrorAction SilentlyContinue', prompt)
        for token in ('`', '://', 'pi --version', 'curl', 'npm', 'irm'):
            self.assertNotIn(token, first_reply)
        for contract in (
            '## 字多不看',
            '**本文目的：**帮助初学者借助网页版 Chat AI，按需检查或安装并验证 Pi CLI，再完成 OpenAI GPT 与本机 Bash 的配置和使用验证；实际操作由用户在本机完成。',
            '把本文全文交给网页版 Chat AI：首轮只问系统，之后每轮只引导一个本机动作并等你回报。',
            '有版本号就跳过 Pi 安装和安装网络检查',
            '状态或渠道不明就暂停，不盲目重装。',
            '目标不可达且你选择代理时才处理代理',
            '版本号只证明 CLI 可用；OpenAI GPT 与本机 Bash 的配置及使用验证随后另行完成。',
            '用户首次粘贴后，先简短说明路线，然后只询问操作系统',
            '第一轮不发命令、安装脚本或代理配置',
            '也不发链接或网络测试',
            '我会先确认你准备使用的系统和终端，再检查 Pi 是否已可用；已安装就不重装。你现在使用 Windows、macOS 还是 Linux？如果不知道终端怎么打开，告诉我即可。',
            '若用户不知道“终端”或如何打开',
            '安装/修复阶段仅核对当前路线实际需要的官方分发与依赖源',
            '只有 M0 确认目标终端没有可用 Pi 且用户明确决定安装，或用户明确决定修复/重装时，才进入 M1',
            '不要逐项探测未实际触发的安装源',
            'OpenAI API 的网络检查仅在 M4.1 阶段需要时执行',
            '若 `pi --version` 已成功，就跳过安装专用 M1/M2',
            '若曾安装或不确定，先问安装渠道（不记得可直接说明），按能确认的渠道当前官方资料核对现有安装、目标终端和 PATH',
            '若渠道或安装状态仍不明，先暂停，不直接重跑安装器',
            '若确认没有可复用的既有安装，说明安装目标与影响后仍须等用户明确决定安装',
            '仍找不到时回到 M0 核对既有安装渠道与目标终端，不再追加重复的 PATH 查询或盲目重装',
            '只有用户刚安装或更新 Pi、或刚修改 PATH 后，才先重开同一终端并重试一次',
            '用户只需回报版本号或“命令未找到”；启动失败时仅给简短脱敏错误摘要；不贴完整路径、完整 PATH、截图或完整日志',
            '默认优先使用对应系统的官方安装器',
            '不展示其他系统路线的命令',
            '请将本文全文复制给可用的网页版 Chat AI',
            '逐轮交互',
            '完成本文范围内的 Pi CLI 检查/安装、必要网络准备、OpenAI GPT 授权与模型选择、工具配置及一次安全的实际使用验证',
            '不得在 `pi --version`、单次模型回答或单个命令测试后提前宣告完成',
            '本文所说“完成”仅指 Pi CLI + OpenAI GPT + 本机 Bash 通路',
            '网页 AI 不能读取或操作用户终端',
            '每轮只引导一个检查或动作',
            '不索取密码、API Key、Token、cookie、私钥、订阅链接、`auth.json`',
            'Pi 以启动账户权限运行，并非安全沙箱',
            '须先说明具体目标与影响，等待用户明确决定',
            'Node.js 22.19.0 或更高版本',
            'irm https://pi.dev/install.ps1 | iex',
            '安装失败时只请用户提供脱敏错误摘要，不要要求完整日志、凭据或私人路径',
            '本文范围内的 Pi CLI、OpenAI GPT 与本机 Bash 配置及使用已完成',
            '不是 Pi 官方模式',
            '本指南的完成范围仅是 Pi CLI、OpenAI GPT 与本机 Bash 通路',
            '任务不包括创建项目、修改项目文件',
            '网络环境是 Pi 安装和 OpenAI 云端 GPT 的前置条件',
            'FlClash',
            'https://github.com/chen08209/FlClash/releases/latest',
            'https://xn--9kqz23b19z.com/#/register?code=35BcnKzl',
            '服务商注册链接不是个人订阅链接',
            '订阅链接属于凭据',
            '默认目标配置：启用 TUN、系统代理和全局模式',
            '启用前须说明流量路由范围、隐私影响和恢复方式',
            '用户拒绝或当前界面/系统不支持时',
            '也不得报告网络路线已完成',
            '`/login` 选择 OpenAI',
            '`api.openai.com`',
            'https://api.openai.com/v1/models',
            '只说明 API 端点有响应，不证明账户认证或 GPT 模型可用',
            '不要在测试命令里加入 API Key',
            'ChatGPT 网页订阅不等于 OpenAI API 额度',
        ):
            with self.subTest(prompt_contract=contract):
                self.assertIn(contract, prompt)
        self.assertLess(prompt.index('## 字多不看'), prompt.index('## 给网页版 Chat AI 的任务'))
        self.assertLess(prompt.index('## M1：网络环境'), prompt.index('## M2：预备行各样的善事'))
        html = MarkdownIt('commonmark').render(text)
        self.assertEqual(html.count('<pre>'), 1)
        self.assertEqual(book_views._links.markdown_anchors(Path(__file__).with_name('god.md')), set())
        self.assertEqual(book_views.relocated('.github/god.md', 'milestone-2'), ('.github/god.md', ''))
        self.assertEqual(book_views.relocated('.github/first-project.md', 'example'),
                         ('.github/first-project.md', 'example'))

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
