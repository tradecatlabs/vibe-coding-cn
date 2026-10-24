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

    def test_god_prompt_renders_markdown_with_only_example_code_blocks(self):
        from markdown_it import MarkdownIt
        import book_views
        prompt = Path(__file__).with_name('god.md').read_text(encoding='utf-8')
        markdown = MarkdownIt('commonmark')
        tokens = markdown.parse(prompt)
        unrendered_emphasis = [
            child.content
            for token in tokens if token.type == 'inline'
            for child in (token.children or [])
            if child.type == 'text' and '**' in child.content
        ]
        self.assertEqual(unrendered_emphasis, [])
        self.assertEqual((tokens[0].type, tokens[0].tag), ('heading_open', 'h1'))
        self.assertTrue(prompt.startswith('# 道成了肉身\n'))
        self.assertNotRegex(prompt, r'</?(?:details|summary|a)\b')
        self.assertNotRegex(prompt, r'\]\(#[^)]+\)')
        self.assertNotIn('本代码块全文', prompt)
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
            '## 给网页版 Chat AI 的任务',
            '系统未知只问系统；终端未就绪先帮用户打开',
            '系统和终端已明确且没有检查结果时，安排 M0 的只读检查；已有结果直接复用',
            '每轮只给当前平台、当前阶段的一个动作',
            '等待回报后再继续；不一次展示全部路线',
            '不能访问或操作设备、代授权或声称已执行',
            '用户停止则只汇报已证实项并停止',
            '发命令前确认实际 shell',
            'Windows 用 PowerShell（不默认 WSL）',
            '只读检查不需额外请示',
            '绝不索取或转发密码、API Key、Token、cookie、私钥',
            '个人订阅 URL',
            '用户误贴凭据时不引用、不使用',
            'Pi 按启动账户权限运行，不是沙箱',
            '先说明目标、影响和恢复方式，等用户明确同意',
            '实际打开后才称已核验',
            'Android/Termux 只按[Pi 官方指南]',
            'Termux 未安装时说明官方来源和安装影响并等用户决定',
            '推荐 GitHub/F-Droid；Google Play 版已弃用',
            '来源不明或仍用旧版先暂停',
            '包更新、依赖安装、共享存储授权前说明影响并等同意',
            '仅需访问 Android 文件时启用共享存储',
            '在计划使用的终端复用已有 `pi --version` 结果：版本号记作 M3并跳过 M1/M2',
            '若“命令未找到”，仅在刚安装/更新或改 PATH 后重开终端重试一次',
            '仍失败就核对是否装过、安装渠道及目标终端',
            '状态/渠道不明则暂停，不盲目重装',
            '确认未安装或需修复后，先说明影响并等用户同意',
            '安装专用 M1/M2 仅在 M0 确认 CLI 不可用且用户同意安装/修复时使用',
            'M4.1 出现真实模型网络故障时，可按本节代理条件路线处理',
            '只检查所选安装路线实际需要的官方分发/依赖源',
            'GPT 网络按 M4.1 的登录路线和真实故障检查',
            '浏览器可达也不证明终端或模型服务可达',
            'API Key 与订阅 OAuth 使用不同服务，不能互相代测',
            '不探测未触发的安装源',
            '目标可达就不用代理',
            '确有不可达且用户选择后才处理代理',
            'FlClash 是客户端，不提供代理订阅',
            'https://github.com/chen08209/FlClash/releases/latest',
            '`code` 含义、服务状态、资质、价格、隐私和安全均未核实',
            '个人订阅 URL 是凭据',
            '绝不索取、转发或写入文件/截图/日志',
            '仅用户选 FlClash 时，目标为启用 TUN、系统代理、全局模式',
            '说明 TUN/全局模式的路由范围、系统权限、DNS/局域网/隐私/断网影响和恢复步骤',
            '拒绝或不支持就停止该路线，不换未授权方案、不报完成',
            '恢复时关闭本次启用的三项并还原原模式',
            '`--connect-timeout 5 --max-time 15`；超时不证明不可达、不自动重试',
            '只用界面显示的本地端口做临时配置，不猜端口、不改 shell 启动文件',
            'Node.js 22.19.0+ 与 npm',
            '仅已有 Nix 时可选，不为 Pi 安装 Nix',
            '安装脚本会下载并执行代码',
            '不得由 CI、脚本、非交互 shell 或管理员/root 执行',
            '部分系统包操作会请求 `sudo`',
            '绝不索取 sudo 密码',
            'irm https://pi.dev/install.ps1 | iex',
            '权限错误时停止，不用 `sudo npm`',
            '只证明 CLI 可用，不证明模型或工具接通',
            '目录不是沙箱，也不限制 Pi 访问当前账户可访问的路径',
            '先解释信任提示涉及的资源，不自动批准',
            '`/login`、`/model` 和问题只在 Pi 输入框输入',
            '已有该目录的会话直接复用',
            '仅复用环境、路线、模型未变且无新失败信号的证据',
            '超时、限额、模型不可用先按错误排查，不当作凭据失效',
            '换账号/路线须用户明确选择',
            '常规验证不 `/logout`、删除或覆盖 `auth.json`',
            'ChatGPT 订阅 OAuth',
            'OpenAI API Key',
            '账号可用且 `/login` 列出 `OpenAI (ChatGPT subscription)`',
            'provider `openai-codex`',
            '它不是 API Key/额度',
            '链接只用于本机浏览器',
            '最终授权码/回调 URL 仅在 Pi 明确要求时贴回本机 Pi',
            '绝不发给网页 AI',
            '本地回答不算 OpenAI GPT 验证',
            '仅 API Key 路线且确有连通故障时',
            'curl --connect-timeout 5 --max-time 15 -I https://github.com',
            'curl.exe --connect-timeout 5 --max-time 15 -I https://github.com',
            'curl --connect-timeout 5 --max-time 15 -i https://api.openai.com/v1/models',
            'curl.exe --connect-timeout 5 --max-time 15 -i https://api.openai.com/v1/models',
            '不要加入 Key/Authorization；OAuth 不用此端点',
            'HTTP 响应只证明端点响应，不证明认证或模型可用',
            '`auth.json` 可能含 API Key/OAuth Token',
            '成功证据只能是 Pi 会话中所选 OpenAI GPT 的实际回答',
            '网页版 AI 回复、CLI 版本、浏览器可达或 FlClash 已连接都不算',
            '本地模型不计 OpenAI GPT，也不静默切换',
            '让用户在 Pi 输入框中发送：',
            "printf 'local shell OK\\n'",
            '不要运行其他命令、读取文件、创建或修改文件、访问网络',
            '仍不可用或用户拒绝时，不报通过',
            '只有用户提供以下三项真实本机证据',
            '所选 OpenAI GPT 在 Pi 会话中回答了简单问题',
            '用户看到 Pi 调用本机 Bash 运行 M4.2 的只读命令并得到结果',
            '只装 CLI→模型未验证',
            '仅本地模型有回答→OpenAI GPT 未验证',
            '不代表其他工具、文件读写、自动化、隔离或生产就绪',
            '创建项目、装依赖、部署和业务开发不在范围内',
        ):
            with self.subTest(prompt_contract=contract):
                self.assertIn(contract, prompt)
        self.assertNotIn('确认环境后，让用户在计划使用 Pi 的终端单独运行：', prompt)
        self.assertNotIn('若尚未安装，说明其官方来源与安装影响', prompt)
        self.assertNotIn('先确认用户有权使用 OpenAI API', prompt)
        self.assertNotIn('完成 OpenAI GPT 主路线（ChatGPT 订阅 OAuth 或 OpenAI API Key）的授权后，让用户用 `/model` 选择该路线实际可用的 GPT 模型，并提出一个无需修改文件的简单问题。', prompt)
        self.assertNotIn('curl -I https://github.com', prompt)
        self.assertNotIn('curl.exe -I https://github.com', prompt)
        self.assertNotIn('curl -i https://api.openai.com/v1/models', prompt)
        self.assertNotIn('curl.exe -i https://api.openai.com/v1/models', prompt)
        self.assertLess(prompt.index('## 字多不看'), prompt.index('## 给网页版 Chat AI 的任务'))
        self.assertLess(prompt.index('## M1：网络环境'), prompt.index('## M2：预备行各样的善事'))
        self.assertLess(prompt.find('### M4.0：进入 Pi 交互界面'), prompt.find('\npi\n'))
        self.assertLess(prompt.index('\npi\n'), prompt.index('### M4.1：验证对话能力'))
        self.assertNotIn('模型能回答后，建议用户在空目录或非敏感目录启动 Pi。', prompt)
        self.assertEqual(
            [(token.info, token.content) for token in tokens if token.type == 'fence'],
            [
                ('text', 'pi --version\n'),
                ('bash', 'curl -fsSL https://pi.dev/install.sh | sh\n'),
                ('powershell', 'irm https://pi.dev/install.ps1 | iex\n'),
                ('text', 'pi\n'),
                ('text', "请只通过当前可用的本机 Bash 工具运行这一条只读命令：printf 'local shell OK\\n'\n"
                         '不要运行其他命令、读取文件、创建或修改文件、访问网络。只返回结果；若工具不可用，请直接说明。\n'),
            ],
        )
        html = markdown.render(prompt)
        for rendered in ('<h1>道成了肉身</h1>', '<h2>M0：检查现状</h2>',
                         '<h2>完整配置与使用的完成标准</h2>',
                         'href="https://pi.dev/docs/latest/termux"',
                         'href="https://www.biblegateway.com/passage/?search=John%201%3A14&amp;version=CUVS"'):
            with self.subTest(rendered_markdown=rendered):
                self.assertIn(rendered, html)
        self.assertEqual(html.count('<pre>'), 5)
        self.assertTrue({'道成了肉身', 'm0检查现状', '官方资料'}.issubset(
            book_views._links.markdown_anchors(Path(__file__).with_name('god.md'))))
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
