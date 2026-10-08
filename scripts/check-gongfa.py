#!/usr/bin/env python3
"""离线校验功法JSON、冻结来源和评级引用；不联网，不执行原文，不计算品级。

运行：make check-gongfa；依赖见requirements-gongfa.txt，Python3.10+。
--render-grades输出词表；--render-catalog输出分类/初评表，不修改文件或计算品级。
"""

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
TIERS = [('huang', '黄阶'), ('xuan', '玄阶'), ('di', '地阶'), ('tian', '天阶')]
LEVELS = [('initial', '初级'), ('intermediate', '中级'), ('advanced', '高级')]
PROFILE_FIELDS = ('problem', 'mechanism', 'conditions', 'limitations', 'expected_outcomes', 'questions')


class ContractError(ValueError):
    """只携带位置与失败条件，不回显输入值或原文。"""


def require(condition, position, reason):
    if not condition:
        raise ContractError(position + ': ' + reason)


def bounded_read(path, limit):
    with path.open('rb') as stream:
        data = stream.read(limit + 1)
    require(len(data) <= limit, str(path), '超过文件大小上限')
    return data


def load_json(path, limit=32 * 1024 * 1024):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, str(path), '重复JSON键')
            result[key] = value
        return result

    def constant(_value):
        raise ContractError(str(path) + ': 禁止NaN和Infinity')

    return json.loads(bounded_read(path, limit).decode('utf-8'),
                      object_pairs_hook=pairs, parse_constant=constant)


def safe_path(root, name):
    relative = PurePosixPath(name)
    require(not relative.is_absolute() and all(part not in ('.', '..') and not part.startswith('.')
            for part in relative.parts) and '\\' not in name and ':' not in name,
            'path', '必须使用仓库内相对路径，禁止敏感隐藏路径和路径穿越')
    path = (root / name).resolve()
    require(path.is_relative_to(root), 'path', '路径或软链接越出仓库')
    return path


def no_remote_refs(node):
    if isinstance(node, dict):
        if '$ref' in node:
            require(node['$ref'].startswith('#/'), 'schema', '只允许本地Schema引用')
        for value in node.values():
            no_remote_refs(value)
    elif isinstance(node, list):
        for value in node:
            no_remote_refs(value)


def index_unique(records, key, position):
    result = {}
    for number, record in enumerate(records):
        identity = key(record)
        require(identity not in result, position + '/' + str(number), 'ID或ID/版本重复')
        result[identity] = record
    return result


def markdown_sections(text):
    pattern = re.compile(r'<a id="([^"]+)"></a>\s*\n(#{1,6})[ \t]+[^\n]+\n')
    headers = list(pattern.finditer(text))
    sections = {}
    for number, match in enumerate(headers):
        anchor = match.group(1)
        require(anchor not in sections, 'snapshot', 'Markdown锚点重复')
        end = len(text)
        for following in headers[number + 1:]:
            if len(following.group(2)) <= len(match.group(2)):
                end = following.start()
                break
        body = re.sub(r'\n---\s*$', '', text[match.end():end].strip()).strip()
        sections[anchor] = body
    return sections


def html_sections(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    articles = soup.select('article')
    require(len(articles) == 1, 'snapshot', '必须有一个已核对的article正文容器')
    result = {}
    for heading in articles[0].find_all('h3'):
        anchor = heading.get('id')
        require(anchor and anchor not in result, 'snapshot', '方法标题缺锚点或重复')
        paragraphs = []
        for sibling in heading.next_siblings:
            tag = getattr(sibling, 'name', None)
            if tag in ('h1', 'h2', 'h3'):
                break
            if tag == 'p' and sibling.get_text(' ', strip=True).startswith('#vibecoding方法论'):
                paragraphs.append(sibling)
        # 最后一节还包含公开来源说明；只接受一个明确标记的方法段落。
        require(len(paragraphs) == 1, 'snapshot', '方法原文标记缺失或存在多个候选方法段落')
        result[anchor] = re.sub(r'\s+', ' ', paragraphs[0].get_text(' ', strip=True)).strip()
    return result


def selected_text(source, sections, reference):
    anchor = reference['heading_id']
    require(anchor in sections, 'source_ref', '不存在的正文锚点')
    text, selection = sections[anchor], reference['selection']
    if source['kind'] == 'project_internal_publication':
        require(selection == 'html-paragraph' and reference['stop_before'] is None,
                'source_ref', 'HTML来源只取已核对的方法段落')
    else:
        require(selection.startswith('markdown-'), 'source_ref', '来源与提取方式错配')
        if selection == 'markdown-first-paragraph':
            blocks = [part for part in re.split(r'\n\s*\n', text)
                      if part.strip() and not part.lstrip().startswith(('>', '<a ', '#'))]
            require(bool(blocks), 'source_ref', '没有可提取的正文段落')
            text = blocks[0].strip()
        if selection == 'markdown-prefix':
            stop = reference['stop_before']
            require(stop and text.count(stop) == 1, 'source_ref', '限定范围终点缺失或不唯一')
            text = text.split(stop, 1)[0].strip()
        else:
            require(reference['stop_before'] is None, 'source_ref', '非前缀提取不得携带终点')
    return text


def check_chains(links, position, reject_forks=False):
    if reject_forks:
        require(all(count == 1 for count in Counter(value for value in links.values() if value is not None).values()),
                position, '纠正链分叉；不能推断唯一当前结论')
    visited = set()
    for start in links:
        path, current = set(), start
        while current is not None and current not in visited:
            require(current in links, position, '历史引用悬空')
            require(current not in path, position, '历史链存在循环')
            path.add(current)
            current = links[current]
        visited.update(path)


def timestamp(value, position):
    try:
        parsed = datetime.fromisoformat(value.replace('z', 'Z').replace('Z', '+00:00'))
    except ValueError:
        raise ContractError(position + ': 无法解析ISO时间') from None
    require(parsed.tzinfo is not None, position, '时间必须带时区')
    return parsed


def render_grades(document):
    lines = ['| 值标识 | 名称 | 大阶 | 细级 | 次序 |', '|---|---|---|---|---|']
    ordinal = 0
    for tier in document['vocabulary']['tiers']:
        for level in tier['levels']:
            ordinal += 1
            lines.append('| `' + level['id'] + '` | ' + tier['name'] + level['name'] + ' | ' +
                         tier['name'] + ' | ' + level['name'] + ' | ' + str(ordinal) + ' |')
    return '\n'.join(lines)


def render_catalog(document, batch_id=None):
    batches = document['grade_proposals']
    if batch_id is not None:
        matches = [batch for batch in batches if batch['id'] == batch_id]
        require(len(matches) == 1, 'catalog', '指定初评批次不存在或不唯一')
        batch = matches[0]
    else:
        require(len(batches) <= 1, 'catalog', '多个初评范围不能以最新时间自动裁决；请指定批次')
        batch = batches[0] if batches else None
    proposals = {(item['gongfa_id'], item['content_version']): item
                 for item in batch['items']} if batch else {}
    labels = {'dao-content': '复合型', 'explanatory-content': '解释型',
              'normative-allocation-content': '准则型', 'method-specification': '方法型'}
    grades = {level['id']: tier['name'] + level['name']
              for tier in document['vocabulary']['tiers'] for level in tier['levels']}
    scope = ('所选初评批次：`' + batch['id'] + '`；仅展示该批意见，不推断其他批次结论。'
             if batch else '尚无初评批次。')
    lines = ['# 功法分类与人工初评', '', '暂定品级是作者判断，不是已验证的效果等级。', '',
             scope, '', '| ID | 名称 | 分类 | 暂定品级 |', '|---|---|---|---|']
    for entry in document['gongfa']:
        item = proposals.get((entry['id'], entry['content_version']))
        ontology = item['ontology_type'] if item else entry['ontology_type']
        cells = [entry['id'], entry['name'], labels.get(ontology, '待分类'),
                 grades[item['grade_id']] if item else ('本批未初评' if batch else '未初评')]
        cells = [value.replace('|', '\\|').replace('\n', ' ') for value in cells]
        lines.append('| `' + cells[0] + '` | ' + ' | '.join(cells[1:]) + ' |')
    return '\n'.join(lines)


def validate(root, registry_path, check_view=True):
    document = load_json(registry_path)
    schema = load_json(root / 'metadata/gongfa/registry.schema.json', 1024 * 1024)
    no_remote_refs(schema)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document))
    if errors:
        # jsonschema的message可能含输入值；只报告位置与失败关键字。
        issue = errors[0]
        position = '/'.join(str(part) for part in issue.absolute_path) or '/'
        raise ContractError(position + ': Schema约束失败（' + issue.validator + '）')

    expected = [{'id': tier, 'name': name, 'levels': [{'id': tier + '-' + level, 'name': label}
                 for level, label in LEVELS]} for tier, name in TIERS]
    require(document['vocabulary']['tiers'] == expected, 'vocabulary', '四阶十二级、名称及顺序必须完全对应')
    if check_view:
        readme = bounded_read(safe_path(root, 'metadata/gongfa/README.md'), 1024 * 1024).decode('utf-8')
        start, end = '<!-- gongfa-grades:start -->', '<!-- gongfa-grades:end -->'
        require(readme.count(start) == 1 and readme.count(end) == 1, 'README', '词表视图标记必须唯一')
        require(readme.index(start) < readme.index(end), 'README', '词表视图标记顺序错误')
        view = readme.split(start, 1)[1].split(end, 1)[0].strip()
        require(view == render_grades(document), 'README', '只读品级视图与JSON不一致')
    grades = [level['id'] for tier in expected for level in tier['levels']]
    sources = index_unique(document['sources'], lambda item: item['id'], 'sources')
    entries = index_unique(document['gongfa'], lambda item: (item['id'], item['content_version']), 'gongfa')
    policies = index_unique(document['policies'], lambda item: (item['id'], item['version']), 'policies')
    assessments = index_unique(document['assessments'], lambda item: item['id'], 'assessments')
    cache, parsed, covered = {}, {}, {identity: set() for identity in sources}
    total_bytes = 0

    def artifact(reference):
        nonlocal total_bytes
        path = safe_path(root, reference['path'])
        if path not in cache:
            raw = bounded_read(path, 2 * 1024 * 1024)
            total_bytes += len(raw)
            require(total_bytes <= 50 * 1024 * 1024, 'artifacts', '总读取量超过50MiB预算')
            cache[path] = raw, hashlib.sha256(raw).hexdigest()
        raw, digest = cache[path]
        require(digest == reference['sha256'], 'artifact', '冻结文件摘要不一致')
        return raw

    for identity, source in sources.items():
        timestamp(source['captured_at'], 'sources/captured_at')
        require(PurePosixPath('metadata/gongfa') in PurePosixPath(source['snapshot_path']).parents,
                'sources/snapshot_path', '原始快照必须归本领域目录所有')
        raw = artifact({'path': source['snapshot_path'], 'sha256': source['snapshot_sha256']})
        if source['kind'] == 'repository_document':
            safe_path(root, source['path'])  # 当前导航不是历史快照，不要求当前文件仍逐字相同。
            sections = markdown_sections(raw.decode('utf-8'))
        else:
            for url in (source['url'], source['resolved_url']):
                parsed_url = urlsplit(url)
                require(parsed_url.scheme == 'https' and parsed_url.hostname and
                        parsed_url.username is None and parsed_url.password is None,
                        'sources/url', '发布来源须为无凭据的HTTPS地址')
            sections = html_sections(raw)
            require(set(sections) == set(source['included_anchors']), 'sources', '公开页面方法覆盖不完整')
        require(set(source['included_anchors']) <= set(sections), 'sources', '收录范围包含不存在的锚点')
        parsed[identity] = sections

    content_links = {}
    for number, entry in enumerate(document['gongfa']):
        position = 'gongfa/' + str(number)
        reference, content = entry['source_ref'], entry['content']
        identity = reference['source_id']
        require(identity in sources, position, '来源引用悬空')
        require(reference['heading_id'] in sources[identity]['included_anchors'], position, '条目越出声明收录范围')
        original = selected_text(sources[identity], parsed[identity], reference)
        require(content['original_text'] == original, position, '原文与冻结来源/限定范围不一致')
        require(content['text_sha256'] == hashlib.sha256(original.encode('utf-8')).hexdigest(), position, '原文摘要不一致')
        profile = content['profile']
        missing = {field for field in PROFILE_FIELDS if not profile[field]}
        require(set(profile['missing_fields']) == missing, position, '未提供字段须显式标记，不补造未知内容')
        key = entry['id'], entry['content_version']
        predecessor = entry['predecessor_version']
        content_links[key] = (entry['id'], predecessor) if predecessor is not None else None
        covered[identity].add(reference['heading_id'])
    check_chains(content_links, 'gongfa/predecessor_version')
    for identity, source in sources.items():
        require(covered[identity] == set(source['included_anchors']), 'sources', '声明收录范围有缺失条目')

    for number, policy in enumerate(document['policies']):
        position = 'policies/' + str(number)
        require([rule['grade_id'] for rule in policy['rules']] == grades, position, '每个等级须且只须有一条规则，顺序固定')
        if policy['status'] == 'defined':
            require(not policy['unresolved'] and policy['evaluation_contract'] is not None,
                    position, '定稿规约必须固定校准合同且无待定项')
        if policy['evaluation_contract'] is not None:
            for reference in policy['evaluation_contract'].values():
                artifact(reference)

    proposals = index_unique(document['grade_proposals'], lambda item: item['id'], 'grade_proposals')
    proposal_links = {}
    for number, batch in enumerate(document['grade_proposals']):
        position = 'grade_proposals/' + str(number)
        current_time = timestamp(batch['assessed_at'], position + '/assessed_at')
        require((batch['policy_id'], batch['policy_version']) in policies,
                position, '人工初评引用的规约版本不存在')
        targets = index_unique(batch['items'], lambda item: (item['gongfa_id'], item['content_version']),
                               position + '/items')
        for target, item in targets.items():
            require(target in entries, position, '初评对象内容版本不存在')
            require(item['content_sha256'] == entries[target]['content']['text_sha256'],
                    position, '初评所依据的限定内容摘要错配')
        previous = batch['supersedes']
        if previous is not None:
            require(previous in proposals, position, '被纠正初评批次不存在')
            older = proposals[previous]
            old_targets = {(item['gongfa_id'], item['content_version']) for item in older['items']}
            require(set(targets) == old_targets and batch['application_context'] == older['application_context']
                    and batch['baseline_assumption'] == older['baseline_assumption'],
                    position, '初评纠正链的对象或应用范围错配')
            require(current_time >= timestamp(older['assessed_at'], position + '/supersedes/assessed_at'),
                    position, '初评纠正时间早于旧批次')
        proposal_links[batch['id']] = previous
    check_chains(proposal_links, 'grade_proposals/supersedes', reject_forks=True)

    links = {}
    for number, assessment in enumerate(document['assessments']):
        position = 'assessments/' + str(number)
        current_time = timestamp(assessment['assessed_at'], position + '/assessed_at')
        target = assessment['gongfa_id'], assessment['content_version']
        policy_key = assessment['policy_id'], assessment['policy_version']
        require(target in entries, position, '被评内容版本不存在')
        require(policy_key in policies, position, '判级规约版本不存在')
        policy = policies[policy_key]
        if assessment['status'] == 'rated':
            require(policy['status'] == 'defined', position, '草案规约不能产生正式评级')
            contract = policy['evaluation_contract']
            require(assessment['scope'] == {key: value for key, value in contract.items() if key != 'criteria_ref'},
                    position, '评级条件与固定规约合同错配')
        if assessment['scope'] is not None:
            for reference in assessment['scope'].values():
                artifact(reference)
        for reference in assessment['evidence_refs']:
            artifact(reference)
        previous = assessment['supersedes']
        if previous is not None:
            require(previous in assessments, position, '被纠正评级不存在')
            older = assessments[previous]
            require((older['gongfa_id'], older['content_version'], older['scope']) ==
                    (assessment['gongfa_id'], assessment['content_version'], assessment['scope']),
                    position, '纠正记录的内容版本或适用范围错配')
            older_time = timestamp(older['assessed_at'], position + '/supersedes/assessed_at')
            require(current_time >= older_time, position, '纠正时间早于旧记录')
        links[assessment['id']] = previous
    check_chains(links, 'assessments/supersedes', reject_forks=True)
    summary = {'grade_values': len(grades), 'content_versions': len(entries), 'sources': len(sources),
               'registered': sum(entry['entry_status'] == 'registered' for entry in entries.values()),
               'candidates': sum(entry['entry_status'] == 'candidate' for entry in entries.values()),
               'assessments': len(assessments),
               'rated_assessments': sum(item['status'] == 'rated' for item in assessments.values()),
               'proposal_batches': len(proposals),
               'proposed_grades': sum(len(batch['items']) for batch in proposals.values())}
    return document, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--registry', type=Path)
    views = parser.add_mutually_exclusive_group()
    views.add_argument('--render-grades', action='store_true')
    views.add_argument('--render-catalog', action='store_true')
    parser.add_argument('--proposal-batch')
    args = parser.parse_args()
    if args.proposal_batch is not None and not args.render_catalog:
        parser.error('--proposal-batch必须与--render-catalog一起使用')
    root = args.root.resolve()
    path = args.registry or root / 'metadata/gongfa/registry.json'
    try:
        # 重建只读视图不要求旧视图已正确；其他数据/来源检查仍然有效。
        document, summary = validate(root, path, check_view=not args.render_grades)
        if args.render_grades:
            print(render_grades(document))
        elif args.render_catalog:
            print(render_catalog(document, args.proposal_batch))
        else:
            print(json.dumps(summary, ensure_ascii=False))
        return 0
    except (ContractError, OSError, UnicodeError, ValueError, RecursionError, SchemaError) as error:
        if isinstance(error, ContractError):
            detail = str(error)
        else:
            detail = '输入、文件或Schema无效（' + type(error).__name__ + '）；未执行原文'
        print('GONGFA_ERRORS\n' + str(path) + ': ' + detail, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
