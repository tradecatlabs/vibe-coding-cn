#!/usr/bin/env python3
"""从唯一JSON原始资料生成Markdown总表、词表及文集；默认只检查，不评级或写登记。

运行：make sync-gongfa-catalog / make check-gongfa-catalog。
依赖：.github/requirements-gongfa.txt；复用原登记校验器与成熟Markdown解析器。
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from html import escape
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[2]
# 生成入口仍在Extensions；共用模块与校验器直接平铺于.github，不保留旧包副本。
sys.path.insert(0, str(ROOT / '.github'))
import source_archive
import book_views
import tool_explanations

spec = importlib.util.spec_from_file_location('gongfa_protocol', ROOT / '.github/check-gongfa.py')
protocol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(protocol)
MARKER = '<!-- generated: sync-gongfa-catalog.py -->'
GRADES = [f'{tier}-{level}' for tier in ('huang', 'xuan', 'di', 'tian')
          for level in ('initial', 'intermediate', 'advanced')]
GRADE_LABELS = {f'{tier}-{level}': tier_label + level_label
                for tier, tier_label in [('huang', '黄阶'), ('xuan', '玄阶'), ('di', '地阶'), ('tian', '天阶')]
                for level, level_label in [('initial', '初级'), ('intermediate', '中级'), ('advanced', '高级')]}
TYPE_LABELS = {'explanatory-content': '解释型', 'normative-allocation-content': '准则型',
               'method-specification': '方法型', 'dao-content': '复合（保留上位）', None: '待分类'}
BATCH_LABELS = {'registry': '登记库'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(text):
    return sha256(text.encode('utf-8')).hexdigest()


def as_text(value):
    return '' if value is None else value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)


def unique(items, key):
    result = {}
    for item in items:
        identity = key(item)
        require(identity not in result, '来源对象、内容版本或初评意见重复')
        result[identity] = item
    return result


def load_inputs(root):
    root = root.resolve(strict=True)
    registry_path = protocol.safe_path(root, '.github/metadata/gongfa/registry.json')
    registry_sha = sha256(protocol.bounded_read(registry_path, 32 * 1024 * 1024)).hexdigest()
    registry, registry_summary = protocol.validate(root, registry_path)
    require(sha256(protocol.bounded_read(registry_path, 32 * 1024 * 1024)).hexdigest() == registry_sha, 'registry.json读取期间变化，请重跑')
    index_path = protocol.safe_path(root, '.github/metadata/gongfa/catalog-sources.json')
    index = protocol.load_json(index_path, 1024 * 1024)
    require(set(index) == {'schema_version', 'kind', 'snapshot', 'candidate_counts'} and index['schema_version'] == '1.0.0'
            and index['kind'] == 'catalog_candidate_source_index_not_registry', 'catalog-sources.json协议形态不符')
    reference = index['snapshot']
    require(set(reference) == {'path', 'sha256'} and re.fullmatch(r'source-[a-z0-9-]+\.json', reference['path']), '来源快照须为本目录source-*.json')
    require(not (root / '.github/metadata/gongfa' / reference['path']).is_symlink(), '来源快照不能是软链接')
    snapshot_path = protocol.safe_path(root, '.github/metadata/gongfa/' + reference['path'])
    raw = protocol.bounded_read(snapshot_path, 32 * 1024 * 1024)
    require(sha256(raw).hexdigest() == reference['sha256'], '来源快照SHA-256不符')
    snapshot = protocol.load_json(snapshot_path)
    require(sha256(protocol.bounded_read(snapshot_path, 32 * 1024 * 1024)).hexdigest() == reference['sha256'], '来源快照读取期间变化')
    require(set(snapshot) == {'schema_version', 'kind', 'captured_at', 'scope', 'source_input_bindings',
                            'independent_semantic_approval', 'source_books_and_licenses_verified', 'formal_assessments_created', 'documents'}
            and snapshot['schema_version'] == '1.0.0' and snapshot['kind'] == 'frozen_classified_candidate_source_not_registry', '来源快照协议形态不符')
    require(snapshot['independent_semantic_approval'] is False and snapshot['source_books_and_licenses_verified'] is False
            and snapshot['formal_assessments_created'] == 0, '历史来源快照的审批、来源核验或正式评级字段不符')
    protocol.timestamp(snapshot['captured_at'], 'candidate_snapshot/captured_at')
    documents = snapshot['documents']
    require(set(documents) == {'html211_candidates', 'html211_grades', 'html96_candidates', 'html96_grades', 'solve24_analysis', 'solve_raw'}, '来源快照文档集合不符')
    counts = {'html211': len(documents['html211_candidates']['candidates']), 'html96': len(documents['html96_candidates']['candidates']),
              'solve24': len(documents['solve24_analysis']['items'])}
    require(counts == index['candidate_counts'], '来源批次范围与索引不一致')
    reviewed = {item['source_id'] for item in documents['solve24_analysis']['items']}
    require({item['source_id'] for item in documents['solve_raw']['items']} == reviewed, 'Solve原条目须仅含已审范围')
    archive = source_archive.bundles(root).get('gongfa')
    require(archive is not None and 'explanations_v1' in archive['data'], '功法data.json缺少v1说明载荷')
    binding = {'registry_sha256': registry_sha, 'candidate_sha256': reference['sha256'], 'candidate_snapshot': reference['path'],
               'candidate_counts': counts, 'source_captured_at': snapshot['captured_at'],
               'registry_assessments': registry_summary['assessments'],
               'archive_sha256': {str(path.relative_to(root)): digest for path, digest in source_archive.bundle_bindings(root).items()
                                  if path.parent.name == 'gongfa'}}
    return {**documents, 'registry': registry, 'explanations_v1': archive['data']['explanations_v1']}, binding


def merge_rows(documents):
    rows = []
    registry = documents['registry']
    sources = unique(registry['sources'], lambda item: item['id'])
    batches = unique(registry['grade_proposals'], lambda batch: batch['id'])
    links = {batch['id']: batch['supersedes'] for batch in batches.values()}
    protocol.check_chains(links, 'grade_proposals/supersedes', reject_forks=True)
    superseded = {value for value in links.values() if value is not None}
    opinions = defaultdict(list)
    for batch in batches.values():
        if batch['id'] not in superseded:
            unique(batch['items'], lambda item: (item['gongfa_id'], item['content_version']))
            for item in batch['items']:
                opinions[item['gongfa_id'], item['content_version']].append((item, batch))
    entries = unique(registry['gongfa'], lambda item: (item['id'], item['content_version']))
    candidate_source_id = 'source-classified-candidates-20261007'
    candidate_source = sources.get(candidate_source_id)
    require(candidate_source is not None and candidate_source['kind'] == 'classified_candidate_archive',
            '候选来源未绑定冻结登记源')
    promoted_by_anchor = {
        item['source_ref']['heading_id']: item for item in entries.values()
        if item['source_ref']['source_id'] == candidate_source_id
    }
    require(len(promoted_by_anchor) == len(candidate_source['included_anchors'])
            and set(promoted_by_anchor) == set(candidate_source['included_anchors']),
            '候选登记范围与冻结来源锚点不一致')
    checked_candidate_anchors = set()

    def verify_promoted_candidate(namespace, candidate_id, name, ontology_type, original_text,
                                  content_version, grade_id, grading_status, task_family,
                                  classification_reason, reason, confidence, falsifier, assessed_at):
        anchor = namespace + ':' + candidate_id
        entry = promoted_by_anchor.get(anchor)
        require(entry is not None, '来源记录未逐条登记：' + anchor)
        require(entry['id'] == protocol.candidate_registry_id(namespace, candidate_id)
                and entry['name'] == name and entry['ontology_type'] == ontology_type
                and entry['content_version'] == content_version and entry['entry_status'] == 'registered'
                and entry['content']['original_text'] == original_text
                and entry['content']['text_sha256'] == digest(original_text)
                and entry['source_ref']['selection'] == 'candidate-record',
                '候选登记身份、正文或来源不一致：' + anchor)
        proposals = opinions[entry['id'], content_version]
        require(len(proposals) == 1, '候选原初评必须且只能迁移一次：' + anchor)
        proposal, batch = proposals[0]
        require((proposal['grade_id'], proposal.get('grading_status', 'provisional'),
                 proposal['ontology_type'], proposal['task_family'], proposal['classification_reason'],
                 proposal['reason'], proposal['confidence'], proposal['falsifier'],
                 proposal['content_sha256'], batch['assessed_at']) ==
                (grade_id, grading_status, ontology_type, task_family, classification_reason,
                 reason, confidence, falsifier, digest(original_text), assessed_at),
                '候选既有初评或正文摘要迁移不一致：' + anchor)
        checked_candidate_anchors.add(anchor)
        return entry

    for item in entries.values():
        content = item['content']
        require(content['text_sha256'] == digest(content['original_text']), '登记正文SHA-256不符')
        proposals = opinions[item['id'], item['content_version']]
        for grade, _batch in proposals:
            require(grade['content_sha256'] == content['text_sha256'], '登记初评正文绑定不符')
        grade = proposals[0][0] if len(proposals) == 1 else {}
        batch = proposals[0][1] if len(proposals) == 1 else {}
        status = ('undetermined' if proposals[0][0].get('grading_status') == 'undetermined' else 'provisional') if len(proposals) == 1 else 'multiple-contexts' if proposals else 'unrated'
        detail = as_text([{'batch_id': b['id'], 'application_context': b['application_context'],
                           'baseline_assumption': b['baseline_assumption'], 'assessed_at': b['assessed_at'], 'item': g} for g, b in proposals])
        reference = item['source_ref']
        boundary = '选区说明：' + content['selection_note']
        profile = content['profile']
        explanation_parts = [profile['summary'], '问题：' + (profile['problem'] or '待核'),
                             '机制：' + (profile['mechanism'] or '待核')]
        for field, label in [('conditions', '条件'), ('limitations', '限制'), ('expected_outcomes', '预期结果')]:
            if profile[field]:
                explanation_parts.append(label + '：' + '；'.join(profile[field]))
        explanation = ' '.join(explanation_parts)
        for field, label in [('conditions', '条件'), ('limitations', '限制')]:
            if content['profile'][field]:
                boundary += '\n' + label + '：' + as_text(content['profile'][field])
        source_record = sources[reference['source_id']]
        source_summary = {key: source_record[key] for key in
                          ('id', 'kind', 'path', 'captured_at', 'snapshot_path', 'snapshot_sha256', 'text_normalization')
                          if key in source_record}
        rows.append({'namespace': 'registry', 'original_id': item['id'], 'name': item['name'], 'ontology_type': item['ontology_type'],
                     'grade_id': grade.get('grade_id'), 'grading_status': status,
                     'entry_status': '已登记' if item['entry_status'] == 'registered' else '登记库候选',
                     'task_family': grade.get('task_family', ''), 'explanation': explanation,
                     'original_text': content['original_text'], 'boundary': boundary,
                     'reason': grade.get('reason', detail if proposals else '当前内容版本未初评；不继承旧版本意见。'),
                     'falsifier': grade.get('falsifier', ''), 'confidence': grade.get('confidence', ''), 'content_version': item['content_version'],
                     'source': as_text({'source': source_summary, 'selection': reference, 'original_proposal_context': detail}),
                     'content_sha256': content['text_sha256'], 'relations': '', 'assessed_at': batch.get('assessed_at', '')})
    for namespace in ('html211', 'html96'):
        candidates = unique(documents[namespace + '_candidates']['candidates'], lambda item: item['candidate_id'])
        grade_document = documents[namespace + '_grades']
        grades = unique(grade_document['items'], lambda item: item['candidate_id'])
        require(set(candidates) == set(grades), 'HTML候选与原初评范围不符')
        for item in candidates.values():
            grade = grades[item['candidate_id']]
            require(grade['content_sha256'] == item['text_sha256'] == digest(item['original_text']), 'HTML限定正文绑定不符')
            require(grade['source_selection'] == item['source_selection'] and grade['ontology_type'] == item['ontology_type']
                    and grade['name'] == item['name'], 'HTML选区、类型或名称与原意见不符')
            require(grade['grading_status'] in {'provisional', 'undetermined'}
                    and (grade['provisional_grade_id'] is None) == (grade['grading_status'] == 'undetermined'), '空品级状态不符')
            verify_promoted_candidate(
                namespace, item['candidate_id'], item['name'], item['ontology_type'], item['original_text'], 'r1',
                grade['provisional_grade_id'], grade['grading_status'], grade['task_family'],
                item['classification_reason'], grade['reason'], grade['confidence'], grade['falsifier'],
                grade_document['created_at'])
    analyzed = unique(documents['solve24_analysis']['items'], lambda item: item['source_id'])
    raw_items = unique(documents['solve_raw']['items'], lambda item: item['source_id'])
    require(set(analyzed) == set(raw_items), 'Solve来源记录与原文范围不符')
    for item in analyzed.values():
        raw, grade = raw_items[item['source_id']], item['editorial_analysis']
        require(raw['source_version'] == item['source_version'] and raw['source_selection'] == item['source_selection']
                and grade['source_id'] == item['source_id'], 'Solve版本、选区或意见外键不符')
        text = as_text(raw['original_entry'])
        verify_promoted_candidate(
            'solve24', item['source_id'], raw['name'], grade['ontology_type'], text, item['source_version'],
            grade['grade_id'], 'provisional', grade['task_family'], grade['classification_reason'],
            grade['reason'], grade['confidence'], grade['falsifier'], documents['solve24_analysis']['assessed_at'])
    require(checked_candidate_anchors == set(promoted_by_anchor), '来源记录存在未核验登记或额外身份')
    names = defaultdict(list)
    for row in rows:
        row['key'] = row['namespace'] + ':' + row['original_id'] + ('@' + row['content_version'] if row['namespace'] == 'registry' else '')
        require(row['ontology_type'] in TYPE_LABELS and (row['grade_id'] is None or row['grade_id'] in GRADES), '未知类型或词表外品级')
        require(row['confidence'] in {'', 'low', 'medium'}, '未知置信标签')
        names[row['name']].append(row['key'])
    unique(rows, lambda row: row['key'])
    for row in rows:
        others = [key for key in names[row['name']] if key != row['key']]
        if others:
            row['relations'] += '\n同名限定内容未自动合并：' + '；'.join(others)
    rank = {grade: i for i, grade in enumerate(GRADES)}
    payload = documents.get('explanations_v1', {})
    presentation_order = {
        item['object_key']: position
        for position, item in enumerate(payload.get('items', []))
        if isinstance(item, dict) and isinstance(item.get('object_key'), str)
    }
    source_order = {row['key']: position for position, row in enumerate(rows)}
    rows.sort(key=lambda row: (
        -rank.get(row['grade_id'], -1),
        presentation_order.get(row['key'], len(presentation_order) + source_order[row['key']]),
    ))
    explanations = {item.get('object_key'): item.get('fields') for item in payload.get('items', [])
                    if isinstance(item, dict)} if isinstance(payload, dict) else {}
    for row in rows:
        row['explanation_fields'] = explanations.get(row['key'])
    return rows


# 章节编号保留在冻结来源和登记名中；阅读视图只显示标题正文。
CHAPTER_NUMBER_PREFIX = re.compile(r'^\d+(?:\.\d+)+[ \t]+')


def display_name(name):
    return CHAPTER_NUMBER_PREFIX.sub('', name, count=1)


def navigation_labels(rows):
    visible_names = [display_name(row['name']) for row in rows]
    counts = Counter(visible_names)
    return {
        row['key']: name if counts[name] == 1 else f"{name}（{row['key']}）"
        for row, name in zip(rows, visible_names)
    }


def render_explanation_object(row):
    fields = [dict(field) for field in row['explanation_fields']]
    fields[0]['content'] = display_name(fields[0]['content'])
    return tool_explanations.render_object(row['key'], display_name(row['name']), fields)


def grade_label(row):
    return GRADE_LABELS[row['grade_id']] if row['grade_id'] else {'undetermined': '暂不可判', 'unrated': '未初评', 'multiple-contexts': '多情境意见'}[row['grading_status']]


def grid(rows):
    result = []
    for number, row in enumerate(rows, 1):
        values = [number, grade_label(row), row['name'], TYPE_LABELS[row['ontology_type']], row['entry_status'], BATCH_LABELS[row['namespace']],
                  row['task_family'], row['original_text'], row['boundary'], row['reason'], row['falsifier'], row['confidence'], row['original_id'],
                  row['content_version'], row['source'], row['content_sha256'], row['relations'], row['assessed_at']]
        for value in values:
            if isinstance(value, str):
                require(len(value.encode('utf-16-le')) // 2 <= 32767, 'Excel单元格超过32767 UTF-16单位，不能静默截断')
                require(not re.search(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\ufffe\uffff]', value), 'Excel原文含不支持的字符，不能静默清洗')
        result.append(values)
    return result


def notes(rows, binding):
    counts = Counter(row['namespace'] for row in rows)
    return ['全部功法总表（保留原初评，不重评）',
            f"合计{len(rows)}条；" + '；'.join(f'{BATCH_LABELS[ns]} {counts[ns]}' for ns in BATCH_LABELS)
            + '；输入：' + digest(binding['registry_sha256'] + binding['candidate_sha256']),
            f"品级是编者前瞻；历史来源快照保留原状态；当前正式评级记录数：{binding['registry_assessments']}。同名未合并。"]


TIERS = (('tian', '天阶'), ('di', '地阶'), ('xuan', '玄阶'), ('huang', '黄阶'))
VIEW_NAMES = ('README.md', *(tier + '.md' for tier, _label in TIERS))
# v1全量说明视图约4.2MiB；保留增长余量，同时限制读取与生成预算。
MAX_VIEW_BYTES = 5 * 1024 * 1024


def source_navigation(root):
    keys = book_views.source_keys(root, 'gongfa')
    toc = book_views.source_toc(root, 'gongfa') if keys else []
    anchors = []
    for line in toc:
        match = re.search(r'\]\(#([^)]+)\)', line)
        if match and match.group(1) not in anchors:
            anchors.append(match.group(1))
    document_anchors = {book_views.chapter_id(key) for key in keys}
    lines = ['## 原文文集', '',
             '原始文档、字节摘要和选择器保存在唯一资料源[data.json](data.json)的`documents`中；本页只保留历史入口，不重复展开原文。', '',
             '原文档中的候选/复核状态只表示记录时点；当前登记和说明审阅状态以本总表及对象页为准。', '',
             '### 原始文档', '']
    for key in keys:
        anchor = book_views.chapter_id(key)
        lines.extend((f'<a id="{escape(anchor, quote=True)}"></a>',
                      f'- `{escape(key)}`：原始字节与摘要见[data.json](data.json)'))
    legacy = [anchor for anchor in anchors if anchor not in document_anchors]
    if legacy:
        lines.extend(('', '<!-- 兼容已发布阅读视图中的章节锚点 -->'))
        lines.extend(f'<a id="{escape(anchor, quote=True)}"></a>' for anchor in legacy)
    return lines


def validate_rows(rows):
    keys = [row['key'] for row in rows]
    require(len(set(keys)) == len(keys), '功法对象身份重复')
    for row in rows:
        fields = row.get('explanation_fields')
        require(isinstance(fields, list) and len(fields) == 18, '对象缺少完整v1说明：' + row['key'])
        require([field.get('name') for field in fields] == list(tool_explanations.FIELD_NAMES), '对象v1栏目不符：' + row['key'])
        require(fields[0]['content'] == row['name'], '对象v1名称与登记身份不符：' + row['key'])
        for value in row.values():
            if isinstance(value, str):
                require(len(value.encode('utf-8')) <= MAX_VIEW_BYTES, '字段超过阅读视图预算')
                require(not re.search(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', value), '阅读视图不接受控制字符')


def render_markdown(rows, binding, root=None):
    labels = navigation_labels(rows)
    counts = Counter(row['entry_status'] for row in rows)
    provisional = sum(row['grading_status'] == 'provisional' for row in rows)
    undetermined = sum(row['grading_status'] == 'undetermined' for row in rows)
    by_tier = {tier: [row for row in rows if row['grade_id'] and row['grade_id'].startswith(tier + '-')]
               for tier, _label in TIERS}
    pending = [row for row in rows if row['grade_id'] is None]
    lines = [MARKER, '# 功法总表', '', '## 字多不看', '',
             f"- 共**{len(rows)}条内容记录**；已登记{counts['已登记']}条，待登记{counts['登记库候选']}条，未登记来源条目{counts['未入登记库']}条。不是独立功法去重后的总数。",
             f'- 原前瞻初评{provisional}条，暂不可判{undetermined}条；不是正式效果评级，亦不把缺测默认补成黄阶。',
             f"- {sum(binding['candidate_counts'].values())}条已登记说明已由用户确认正式通过审阅；历史来源快照保留原样，书目/许可核验、实际效果与正式评级仍分别维护。",
             '- [data.json](data.json)是唯一原始数据源，原始文档、历史来源选区、意见、来源和附件均保留其中。', '',
             '输入绑定：`' + digest(binding['registry_sha256'] + binding['candidate_sha256']) + '`。', '',
             '## 快速导航', '']
    for tier, label in TIERS:
        lines.append(f'- [{label}（{len(by_tier[tier])}条）]({tier}.md)')
    lines += [f'- [未明确品级（{len(pending)}条；不归属任何阶）](huang.md#未明确品级不归属黄阶)',
              '- [全部记录导航](#全部记录)', '- [原文文集](#原文文集)', '- [品级词表](#品级词表)', '',
              '<details>', '<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>', '',
              '- [全部记录](#全部记录)', '- [原文文集](#原文文集)', '- [品级词表](#品级词表)', '- [数据与边界](#数据与边界)',
              '<!-- source-toc -->', '', '</details>', '', '## 使用方式', '',
              '按阶打开对应文档；对象身份、字段说明与表格都由data.json和已登记模板生成。修改资料后运行make sync-gongfa-catalog，不手改阅读视图。同名条目在导航中附稳定对象ID，不表示身份合并。', '',
              '## 正文', '', '## 全部记录', '']
    for tier, label in TIERS:
        lines.extend((f'### {label}', ''))
        for row in by_tier[tier]:
            anchor = tool_explanations.anchor_for(row['key'])
            lines.extend((f'<a id="{anchor}"></a>',
                          tool_explanations.render_file_link(row['key'], labels[row['key']], tier + '.md') + f' — {grade_label(row)}'))
        if tier == 'huang' and pending:
            lines.extend(('', '### 未明确品级（不归属任何阶）', ''))
            for row in pending:
                anchor = tool_explanations.anchor_for(row['key'])
                lines.extend((f'<a id="{anchor}"></a>',
                              tool_explanations.render_file_link(row['key'], labels[row['key']], 'huang.md') + f' — {grade_label(row)}'))
        lines.append('')
    if root is not None:
        lines += source_navigation(root)
    registry, _summary = protocol.validate(root, root / '.github/metadata/gongfa/registry.json') if root and source_archive.bundles(root) else (None, None)
    grades = protocol.render_grades(registry) if registry else ''
    lines += ['## 品级词表', '', grades, '', '## 数据与边界', '',
              '本工具只维护data.json原始资料和分阶阅读视图。用户已确认这批说明正式通过审阅；原始来源快照与历史意见保持原样。审阅通过不替代原著/许可核验、实际效果验证或正式评级；历史附件保留为JSON原始载荷，不再维护第二个活动视图。', '',
              '## 更新与核对', '', '```bash', 'make sync-gongfa-catalog', 'make check-gongfa-catalog', 'make test-gongfa-catalog', '```', '',
              '内容新版本不继承旧初评；同对象不同情境的活动意见并列保留，不按最高档或最新时间裁决。',
              '本视图不执行方法，也不证明原著、许可证或真实效果；未知内容仍逐项标待核。', '']
    text = '\n'.join(lines)
    source_toc = book_views.source_toc(root, 'gongfa') if root is not None else []
    return text.replace('<!-- source-toc -->', '\n'.join(source_toc))


def render_grade_markdown(rows, tier):
    labels = navigation_labels(rows)
    label = dict(TIERS)[tier]
    tier_rows = [row for row in rows if row['grade_id'] and row['grade_id'].startswith(tier + '-')]
    pending = [row for row in rows if row['grade_id'] is None] if tier == 'huang' else []
    lines = [MARKER, f'# 功法总表：{label}', '',
             f'本页包含{len(tier_rows)}条{label}记录。品级沿用已有前瞻初评，不是正式效果评级。',
             '- [返回总索引](README.md)；其他阶：[天阶](tian.md)、[地阶](di.md)、[玄阶](xuan.md)、[黄阶](huang.md)。', '',
             f'## {label}记录', '']
    for row in tier_rows:
        lines.append(tool_explanations.render_index_link(row['key'], labels[row['key']]))
    lines.append('')
    for row in tier_rows:
        lines.append(render_explanation_object(row))
    if pending:
        lines.extend(('## 未明确品级（不归属黄阶）', '',
                      f'以下{len(pending)}条没有可沿用的明确品级；仅为减少文件数暂置本页附录，不视为黄阶。', ''))
        for row in pending:
            lines.append(tool_explanations.render_index_link(row['key'], labels[row['key']]))
        lines.append('')
        for row in pending:
            lines.append(render_explanation_object(row))
    return '\n'.join(lines)


def render_views(root, rows, binding, explanations=None):
    if explanations is not None:
        names = {row['key']: row['name'] for row in rows}
        fields_by_key = tool_explanations.validate_payload(root, explanations, names)
        for row in rows:
            row['explanation_fields'] = fields_by_key[row['key']]
    validate_rows(rows)
    views = {'README.md': render_markdown(rows, binding, root)}
    views.update({tier + '.md': render_grade_markdown(rows, tier) for tier, _label in TIERS})
    require(sum(len(text.encode('utf-8')) for text in views.values()) <= MAX_VIEW_BYTES,
            '分阶阅读视图合计超过4MiB预算')
    return views


def view_path(root, name='README.md'):
    require(name in VIEW_NAMES, '未知功法阅读视图文件名')
    nominal = root.resolve() / '.github/context/gongfa' / name
    require(not nominal.is_symlink(), '生成目标不能是软链接')
    path = protocol.safe_path(root.resolve(), '.github/context/gongfa/' + name)
    require(path == nominal, '生成目录不能通过软链接重定向')
    return path


def output_bytes(root, rows, binding, explanations=None):
    views = render_views(root, rows, binding, explanations)
    return {view_path(root, name): text.encode('utf-8') for name, text in views.items()}


def check_views(root, rows, binding, explanations=None):
    for path, expected in output_bytes(root, rows, binding, explanations).items():
        require(protocol.bounded_read(path, MAX_VIEW_BYTES) == expected,
                path.name + '陈旧或手改；运行make sync-gongfa-catalog')


def write_views(root, rows, binding, explanations=None):
    outputs = output_bytes(root, rows, binding, explanations)
    before = {}
    for path in outputs:
        current = protocol.bounded_read(path, MAX_VIEW_BYTES) if path.exists() else None
        require(current is None or MARKER.encode() in current[:200], '拒绝覆盖非本工具生成的Markdown：' + path.name)
        before[path] = current
    source_archive.check_unchanged(root)
    if all(before[path] == raw for path, raw in outputs.items()):
        return
    parent = next(iter(outputs)).parent
    parent.mkdir(parents=True, exist_ok=True)
    temporaries = {}
    for path, raw in outputs.items():
        if before[path] == raw:
            continue
        with tempfile.NamedTemporaryFile(prefix='.gongfa-', suffix='.tmp', dir=parent, delete=False) as stream:
            stream.write(raw)
            temporaries[path] = Path(stream.name)
    source_archive.check_unchanged(root)
    for path, temporary in temporaries.items():
        require(not path.is_symlink() and
                (protocol.bounded_read(path, MAX_VIEW_BYTES) if path.exists() else None) == before[path],
                '提交视图前目标被并行修改；保留临时文件，不覆盖目标：' + path.name)
        temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        documents, binding = load_inputs(root)
        rows = merge_rows(documents)
        explanations = documents['explanations_v1']
        if args.write:
            write_views(root, rows, binding, explanations)
        check_views(root, rows, binding, explanations)
        _documents, fresh_binding = load_inputs(root)
        require(fresh_binding == binding, '输入在生成/检查期间变化；视图不宣称最新，请重跑')
        print(json.dumps({'records': len(rows), 'batches': dict(Counter(row['namespace'] for row in rows)),
                          'provisional': sum(row['grading_status'] == 'provisional' for row in rows),
                          'undetermined': sum(row['grading_status'] == 'undetermined' for row in rows),
                          'registered': sum(row['entry_status'] == '已登记' for row in rows),
                          'formal_assessments': binding['registry_assessments'], 'mode': 'write' if args.write else 'check'}, ensure_ascii=False))
        return 0
    except Exception as error:
        # 第三方异常可能包含输入值；只报告已控的位置/规则或异常类别。
        detail = str(error) if type(error) in (ValueError, protocol.ContractError, source_archive.ArchiveError) and not isinstance(error, json.JSONDecodeError) else type(error).__name__
        print('GONGFA_CATALOG_ERRORS\n' + detail, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
