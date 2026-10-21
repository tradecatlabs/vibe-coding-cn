"""把既有文集渲染到单一阅读视图；原文与历史选择器仍以JSON载荷为准。"""
from html import escape
import importlib.util
import os
from pathlib import Path
import posixpath
import re
from urllib.parse import quote, unquote, urlsplit

from markdown_it import MarkdownIt

import source_archive

# 复用现有链接检查器的GitHub标题语义，不维护另一种slug算法。
_spec = importlib.util.spec_from_file_location('book_link_rules', Path(__file__).resolve().parent / 'check-local-links.py')
_links = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_links)
slug = _links.github_slug


def chapter_id(path):
    return 'doc-' + Path(path).stem


def relocated(path, fragment=''):
    """把历史导航转成当前阅读地址；冻结原文字节不改写。"""
    name = posixpath.basename(path)
    if posixpath.dirname(path) in {'.github/scripts', '.github/extensions'} and (
            (name.startswith(('check-', 'test-')) and name.endswith('.py'))
            or name in {'requirements-gongfa.txt', 'requirements-faqi.txt'}):
        return '.github/' + name, fragment
    if posixpath.dirname(path) in {'.github/lib', '.github/extensions/lib', '.github/scripts/lib'}:
        if name in {'README.md', 'AGENTS.md'}:
            return '.github/AGENTS.md', '维护脚本与共享库'
        if name == '__init__.py':
            return '.github/source_boundaries.py', fragment
    aliases = {
        '.github/metadata/faqi/README.md': '.github/context/faqi/README.md',
        '.github/metadata/faqi/AGENTS.md': '.github/context/AGENTS.md',
        '.github/metadata/gongfa/AGENTS.md': '.github/context/AGENTS.md',
        '.github/skills/claude-official-skills/README.md': '.github/skills/README.md',
        '.github/skills/claude-official-skills/AGENTS.md': '.github/skills/AGENTS.md',
    }
    if path in aliases:
        return aliases[path], fragment
    if path.rstrip('/') == '.github/docs/gongfa':
        return '.github/context/gongfa/README.md', fragment or '原文文集'
    if path.startswith('.github/docs/gongfa/'):
        kind = 'faqi' if Path(path).name == 'faqi-system.md' else 'gongfa'
        target = f'.github/context/{kind}/README.md'
        if Path(path).name in {'README.md', 'AGENTS.md'}:
            return target, '数据与边界' if fragment else ''
        return target, chapter_id(path) + ('-' + fragment if fragment else '')
    if path.startswith('.github/metadata/gongfa/'):
        if Path(path).name in {'catalog.md', 'README.md', 'AGENTS.md'}:
            return '.github/context/gongfa/README.md', ('品级词表' if '品级' in fragment or 'grade' in fragment else '数据与边界') if fragment else ''
        return '.github/context/gongfa/data.json', ''
    if path in {'.github/metadata/faqi.json', '.github/metadata/faqi.schema.json'}:
        return '.github/context/faqi/data.json', ''
    if path == '.github/tools/faqi-catalog.md':
        return '.github/context/faqi/README.md', fragment or '法器总表'
    aliases = {
        '.github/skills/auto-skill/scripts/Skill_Seekers-development': '.github/extensions/Skill_Seekers-development',
        '.github/skills/auto-skill/scripts/skill-seekers-src': '.github/extensions/Skill_Seekers-development',
        '.github/skills/auto-skill/scripts/skill-seekers-configs': '.github/extensions/Skill_Seekers-development/api/configs_repo',
        '.github/skills/claude-official-skills': '.github/extensions/claude-official-skills',
    }
    prefixes = {
        '.github/docs/getting-started': '.github/context/getting-started',
        '.github/docs': '.github/context',
        '.github/assets/external-resources': '.github/context/external-resources',
        '.github/assets/ai-citation': '.github/context/ai-citation',
        '.github/assets': '.github/context/assets',
        '.github/metadata': '.github/context/metadata',
        '.github/research': '.github/context/research',
        '.github/prompts': '.github/context/prompts',
        '.github/scripts/lib': '.github',
        '.github/extensions/lib': '.github',
        '.github/lib': '.github',
        '.github/scripts': '.github/extensions',
        '.github/skills/auto-skill/scripts': '.github/extensions',
        '.github/tools/config': '.github/extensions/codex-config',
        '.github/tools/prompts-library': '.github/extensions/prompts-library',
        '.github/tools/chat-vault': '.github/extensions/chat-vault',
        '.github/tools/external/.tmux': '.github/extensions/oh-my-tmux',
        '.github/tools/external/html-tools-main/README.md': '.github/extensions/html-tools-main.md',
        '.github/tools/external/html-tools-main': '.github/extensions',
        '.github/tools/external': '.github/extensions',
        '.github/tools': '.github/extensions',
        **aliases,
    }
    for old, new in sorted(prefixes.items(), key=lambda item: len(item[0]), reverse=True):
        if path == old or path.startswith(old + '/'):
            path = new + path[len(old):]
            break
    retired = {
        '.github/extensions/prompts-library': ('b0e3454bb865b95bdc70127a431214c384542dee', 'tree'),
        '.github/extensions/chat-vault': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'tree'),
        '.github/extensions/my-nvim': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'tree'),
        '.github/extensions/codex-config': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'tree'),
        '.github/extensions/MCPlayerTransfer': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'tree'),
        '.github/extensions/XHS-image-to-PDF-conversion': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'tree'),
        '.github/extensions/xhs graphic production - 1.0.html': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'blob'),
        '.github/extensions/xhs graphic production.html': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'blob'),
        '.github/extensions/html-tools-main.md': ('44e6fe37a6a871e9327d9f15b23cfef0b7dcbb58', 'blob'),
        '.github/context/assets': ('71bf460cfa894ad45163a9591d2043422974a681', 'tree'),
        '.github/context/external-resources': ('71bf460cfa894ad45163a9591d2043422974a681', 'tree'),
        '.github/skills/auto-tmux': ('71bf460cfa894ad45163a9591d2043422974a681', 'tree'),
    }
    for prefix, (revision, root_route) in sorted(retired.items(), key=lambda item: len(item[0]), reverse=True):
        if path == prefix or path.startswith(prefix + '/'):
            # 原正文保持冻结字节；退役实现只链接到最后仍存在的已发布修订，不能冒充当前入口。
            route = root_route if path == prefix else 'blob'
            return ('https://github.com/tradecatlabs/vibe-coding-cn/' + route
                    + '/' + revision + '/' + quote(path, safe='/')), fragment
    return path, fragment


def reference(value, original_path, output_path):
    value = value.strip()
    if not value or urlsplit(value).scheme or value.startswith(('/', '#')):
        if value.startswith('#') and original_path.startswith('.github/docs/gongfa/'):
            return '#' + chapter_id(original_path) + '-' + value[1:]
        return value
    path, marker, fragment = unquote(value).partition('#')
    original = posixpath.normpath(posixpath.join(posixpath.dirname(original_path), path))
    target, anchor = relocated(original, fragment)
    if urlsplit(target).scheme:
        return target + ('#' + anchor if anchor else '')
    relative = os.path.relpath(target, posixpath.dirname(output_path)).replace(os.sep, '/')
    if target == output_path:
        relative = '' if anchor else Path(output_path).name
    return relative + ('#' + anchor if anchor else '')


def rewrite_links(line, original_path, output_path):
    for pattern in _links.LINK_PATTERNS:
        def replace(match):
            value = match.group(1)
            new = reference(value, original_path, output_path)
            start = match.start(1) - match.start()
            end = match.end(1) - match.start()
            return match.group(0)[:start] + new + match.group(0)[end:]
        line = pattern.sub(replace, line)
    return line


def source_keys(root, kind):
    store = source_archive.bundles(Path(root)).get(kind)
    if not store:
        return []
    keys = [key for key in store['bytes'] if key.startswith('.github/docs/gongfa/') and key.endswith('.md')
            and Path(key).name not in {'README.md', 'AGENTS.md'}]
    # 顺序也来自本集合JSON中的原导航，不依赖另一本可编辑索引。
    original_index = '.github/docs/gongfa/README.md'
    order = []
    if original_index in store['bytes']:
        tokens = MarkdownIt('commonmark').parse(store['bytes'][original_index].decode('utf-8'))
        for token in tokens:
            for child in token.children or []:
                if child.type != 'link_open':
                    continue
                value = child.attrGet('href') or ''
                target = posixpath.normpath(posixpath.join(posixpath.dirname(original_index), unquote(value).split('#')[0]))
                if target in keys and target not in order:
                    order.append(target)
    return order + sorted(set(keys) - set(order))


def render_sources(root, kind):
    output = f'.github/context/{kind}/README.md'
    sections = ['> 文集保留历史正文；已退役实现的相关链接指向已发布的固定Git修订，'
                '不是当前安装或运行入口。现存程序以Extensions清单为准。']
    for key in source_keys(root, kind):
        text = source_archive.read_text(Path(root) / key)
        tokens = MarkdownIt('commonmark').parse(text)
        protected = {line for token in tokens if token.type in {'fence', 'code_block'} and token.map
                     for line in range(*token.map)}
        headings = {token.map[0] for token in tokens if token.type == 'heading_open' and token.map}
        lines = text.splitlines()
        title = next((re.sub(r'^#+\s*', '', lines[line]).strip() for line in sorted(headings)), Path(key).stem)
        prefix = chapter_id(key)
        result = [f'<a id="{prefix}"></a>', '## ' + title, '',
                  '原始文集：`' + key + '`；下文为阅读呈现，原字节和来源保存在[data.json](data.json)。', '']
        used, emitted = {}, set()
        for number, line in enumerate(lines):
            if number in protected:
                result.append(line)
                continue
            def anchor(match):
                name = prefix + '-' + match.group(1)
                if name in emitted:
                    return ''
                emitted.add(name)
                return '<a id="' + escape(name, quote=True) + '"></a>'
            line = re.sub(r'<a\s+id=[\'"]([^\'"]+)[\'"]\s*></a>', anchor, line)
            if number in headings:
                label = re.sub(r'^#{1,6}\s+', '', line).rstrip(' #')
                value = slug(label)
                count = used.get(value, 0)
                used[value] = count + 1
                name = prefix + '-' + value + ('-' + str(count) if count else '')
                if name not in emitted:
                    result.append('<a id="' + name + '"></a>')
                    emitted.add(name)
                line = '**' + label + '**'
            result.append(rewrite_links(line, key, output))
        sections.append('\n'.join(result))
    return '\n\n'.join(sections) + ('\n' if sections else '')


def source_toc(root, kind):
    # 从实际Markdown语法节点取锚点；代码示例里的HTML不进入导航。
    tokens = MarkdownIt('commonmark').parse(render_sources(root, kind))
    prefixes = sorted((chapter_id(key) for key in source_keys(root, kind)), key=len, reverse=True)
    result, seen = [], set()
    def visit(nodes):
        for token in nodes:
            if token.type in {'html_inline', 'html_block'}:
                for name in re.findall(r'<a\s+id=[\"\']([^\"\']+)[\"\']', token.content):
                    if name in seen:
                        continue
                    prefix = next((value for value in prefixes if name == value or name.startswith(value + '-')), None)
                    if prefix is not None:
                        seen.add(name)
                        label = name[4:] if name == prefix else name[len(prefix) + 1:]
                        result.append(('' if name == prefix else '  ') + '- [' + label + '](#' + name + ')')
            if token.children:
                visit(token.children)
    visit(tokens)
    return result
