#!/usr/bin/env python3
"""总表维护的相关行为契约；离线保存隔离工件，不验证功法效果。"""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from html import unescape
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import source_archive

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / '.github/extensions/sync-gongfa-catalog.py'
ARTIFACTS = None
catalog = None
TEMPLATE = Path(__file__).resolve().parents[1] / '.github/context/assets/templates/tool-explanation-template-v0.md'
V1_TEMPLATE = Path(__file__).resolve().parents[1] / '.github/context/assets/templates/tool-explanation-template-v1.md'
STALE_EXPLANATION_LABELS = (
    '冻结候选', '候选快照', '尚未独立语义复核', '未独立语义复核',
    '尚未独立语义核验', '不代表独立语义批准',
)


def template_rows(path):
    rows = []
    for line in path.read_text(encoding='utf-8').splitlines():
        parts = line.split('|')
        if len(parts) == 5 and parts[1].strip().isdigit():
            rows.append((int(parts[1].strip()), parts[2].strip()))
    return rows


def v0_field_names():
    return [name for _number, name in template_rows(TEMPLATE)]


def v1_field_names():
    return [name for _number, name in template_rows(V1_TEMPLATE)]


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)


def parse_pipe_row(line):
    cells = []
    current = []
    index = 1
    while index < len(line) - 1:
        if line[index:index + 2] == r'\|':
            current.append('|')
            index += 2
        elif line[index] == '|':
            cells.append(''.join(current).strip())
            current = []
            index += 1
        else:
            current.append(line[index])
            index += 1
    cells.append(''.join(current).strip())
    return cells


class CatalogMaintenanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents, cls.binding = catalog.load_inputs(ROOT)

    def isolated_project(self):
        root = Path(tempfile.mkdtemp(prefix='project-', dir=ARTIFACTS))
        target = root / '.github/context/gongfa'
        target.mkdir(parents=True)
        shutil.copyfile(ROOT / '.github/context/gongfa/data.json', target / 'data.json')
        template_dir = root / '.github/context/assets/templates'
        template_dir.mkdir(parents=True)
        shutil.copyfile(V1_TEMPLATE, template_dir / V1_TEMPLATE.name)
        return root

    def command(self, root, *options):
        argv = [sys.executable, str(SCRIPT), '--root', str(root), *options]
        result = subprocess.run(argv, cwd=ARTIFACTS, capture_output=True, text=True, timeout=60)
        log = Path(tempfile.mkdtemp(prefix='command-', dir=ARTIFACTS))
        save(log / 'result.json', {'argv': argv, 'cwd': str(ARTIFACTS), 'exit_code': result.returncode, 'timeout_seconds': 60})
        for name, text in [('stdout.log', result.stdout), ('stderr.log', result.stderr)]:
            with (log / name).open('x', encoding='utf-8') as stream:
                stream.write(text)
        return result

    def test_current_all_classified_content_and_two_bad_summaries_keep_original_opinions(self):
        rows = catalog.merge_rows(deepcopy(self.documents))
        self.assertEqual(Counter(row['namespace'] for row in rows), {'registry': 411})
        self.assertEqual(len(rows), 411)
        self.assertEqual(len({(r['namespace'], r['original_id'], r['content_version']) for r in rows}), 411)
        undetermined = {r['original_id'] for r in rows if r['grading_status'] == 'undetermined'}
        self.assertEqual(undetermined, {
            'gongfa-candidate-html211-e001-a663456869',
            'gongfa-candidate-html96-vc029-6cca304cec',
        })
        by_id = {(r['namespace'], r['original_id']): r for r in rows}
        self.assertEqual(by_id['registry', 'gongfa-first-principles']['grade_id'], 'di-advanced')
        self.assertEqual(by_id['registry', 'gongfa-candidate-solve24-psoa-programming-minimal-reproduction-47a914cf5a']['grade_id'],
                         'di-initial')
        undetermined_html96 = 'gongfa-candidate-html96-vc029-6cca304cec'
        self.assertIn('一个分布式系统最多只能保证一致性、可用性和分区容错性中的两项。',
                      by_id['registry', undetermined_html96]['original_text'])
        self.assertEqual(by_id['registry', 'gongfa-candidate-html211-e001-a663456869']['grading_status'], 'undetermined')
        self.assertIn('失去50%容量时剩余单位需要承担2倍总流量。',
                      by_id['registry', 'gongfa-candidate-html211-e001-a663456869']['original_text'])
        self.assertEqual(sum(r['entry_status'] == '已登记' for r in rows), 411)
        lambda_index = next(index for index, row in enumerate(rows) if row['original_id'] == 'gongfa-lambda-calculus')
        glue_index = next(index for index, row in enumerate(rows) if row['original_id'] == 'gongfa-glue-coding')
        self.assertEqual(lambda_index + 1, glue_index)
        self.assertEqual(rows[lambda_index]['name'], 'Lambda 演算')
        self.assertEqual(rows[lambda_index]['grade_id'], 'tian-advanced')
        self.assertIn('天级上品', rows[lambda_index]['reason'])
        rendered = catalog.book_views.render_sources(ROOT, 'gongfa')
        chapters = [line for line in rendered.splitlines() if line.startswith('## ')]
        self.assertEqual(chapters[chapters.index('## 拼好码') + 1], '## Lambda 演算')
        self.assertEqual(sum(r['entry_status'] == '登记库候选' for r in rows), 0)
        self.assertEqual(self.documents['registry']['assessments'], [])
        self.assertEqual(len(self.documents['registry']['gongfa']), 411)
        self.assertTrue(all(item['entry_status'] == 'registered' for item in self.documents['registry']['gongfa']))
        registry_item = next(item for item in self.documents['registry']['gongfa'] if item['id'] == 'gongfa-first-principles')
        profile = registry_item['content']['profile']
        profile_parts = [profile['summary'], '问题：' + profile['problem'], '机制：' + profile['mechanism']]
        for key, label in (('conditions', '条件'), ('limitations', '限制'), ('expected_outcomes', '预期结果')):
            if profile[key]:
                profile_parts.append(label + '：' + '；'.join(profile[key]))
        self.assertEqual(' '.join(profile_parts), by_id['registry', 'gongfa-first-principles']['explanation'])
        entries_by_anchor = {entry['source_ref']['heading_id']: entry
                             for entry in self.documents['registry']['gongfa']
                             if entry['source_ref']['source_id'] == 'source-classified-candidates-20261007'}
        self.assertEqual(len(entries_by_anchor), 331)
        self.assertEqual(set(entries_by_anchor), {
            *(f"html211:{item['candidate_id']}" for item in self.documents['html211_candidates']['candidates']),
            *(f"html96:{item['candidate_id']}" for item in self.documents['html96_candidates']['candidates']),
            *(f"solve24:{item['source_id']}" for item in self.documents['solve24_analysis']['items']),
        })
        proposal_items = {
            (item['gongfa_id'], item['content_version']): item
            for batch in self.documents['registry']['grade_proposals'] for item in batch['items']
        }
        candidate_grades = [
            (f"html211:{grade['candidate_id']}", grade)
            for grade in self.documents['html211_grades']['items']
        ] + [
            (f"html96:{grade['candidate_id']}", grade)
            for grade in self.documents['html96_grades']['items']
        ] + [
            (f"solve24:{item['source_id']}", item['editorial_analysis'])
            for item in self.documents['solve24_analysis']['items']
        ]
        for anchor, previous in candidate_grades:
            entry = entries_by_anchor[anchor]
            current = proposal_items[entry['id'], entry['content_version']]
            grade = previous.get('provisional_grade_id', previous.get('grade_id'))
            self.assertEqual(current['grade_id'], grade, anchor)
            self.assertEqual(current['task_family'], previous['task_family'], anchor)
            self.assertEqual(current['reason'], previous['reason'], anchor)
            self.assertEqual(current['falsifier'], previous['falsifier'], anchor)
            self.assertEqual(current['confidence'], previous['confidence'], anchor)
            self.assertEqual(current['content_sha256'], entry['content']['text_sha256'], anchor)
        for anchor in ('html211:E001', 'html96:VC029'):
            entry = entries_by_anchor[anchor]
            proposal = proposal_items[entry['id'], entry['content_version']]
            self.assertIsNone(proposal['grade_id'])
            self.assertEqual(proposal['grading_status'], 'undetermined')
            row = by_id['registry', entry['id']]
            self.assertEqual(row['grading_status'], 'undetermined')
            self.assertEqual(row['explanation_fields'][5]['content'].split('登记状态：', 1)[1].split('；', 1)[0], '已登记')
            self.assertIn('.github/metadata/gongfa/source-classified-candidates-20261007.json',
                          row['explanation_fields'][6]['content'])
        self.assertEqual(self.documents['html211_candidates']['registry_updated'], False)
        self.assertEqual(self.documents['html96_candidates']['registry_updated'], False)
        self.assertEqual(self.documents['explanations_v1']['template_sha256'], catalog.tool_explanations.template_sha256(ROOT))
        self.assertEqual(len(self.documents['explanations_v1']['items']), 411)
        self.assertTrue(all(item['object_key'].startswith('registry:')
                            for item in self.documents['explanations_v1']['items']))
        views = catalog.render_views(ROOT, rows, self.binding)
        markdown = views['README.md']
        self.assertIn('- 共**411条内容记录**；已登记411条，待登记0条，未登记来源条目0条。', markdown)
        self.assertNotIn('[控制论与科学方法论](#控制论与科学方法论)', markdown)
        self.assertFalse('catalog.xlsx' in markdown, '活动阅读视图只有Markdown，历史Excel仅作原始载荷保存')
        self.assertLess(len(markdown.encode('utf-8')), 512 * 1024, 'README只作为轻量导航，不再展开全部功法表格与文集正文')
        self.assertNotIn('| 序号 | 说明项 | 内容 |', markdown)
        self.assertIn('## 原文文集', markdown)
        self.assertIn('<a id="doc-glue-coding"></a>', markdown)
        self.assertIn('tian.md#', markdown)
        self.assertIn('huang.md#', markdown)
        field_names = v1_field_names()
        self.assertEqual(18, len(field_names))
        total_tables = 0
        for tier in ('tian', 'di', 'xuan', 'huang'):
            page = views[tier + '.md']
            tier_rows = [row for row in rows if row['grade_id'] and row['grade_id'].startswith(tier + '-')]
            if tier == 'huang':
                tier_rows += [row for row in rows if row['grade_id'] is None]
                self.assertIn('## 未明确品级（不归属黄阶）', page)
            starts = [index for index, line in enumerate(page.splitlines()) if line == '| 序号 | 说明项 | 内容 |']
            self.assertEqual(len(tier_rows), len(starts), f'{tier}页面只包含本阶记录及明确标记的未定级记录')
            total_tables += len(starts)
            lines = page.splitlines()
            for row, start in zip(tier_rows, starts):
                table_rows = lines[start:start + 20]
                self.assertEqual(20, len(table_rows))
                self.assertEqual('|:---:|:---|:---|', table_rows[1])
                cells = [parse_pipe_row(line) for line in table_rows]
                self.assertTrue(all(len(cell) == 3 for cell in cells), '每张表严格为三列')
                self.assertEqual(field_names, [cell[1] for cell in cells[2:]])
                display_name = re.sub(r'^\d+(?:\.\d+)+[ \t]+', '', row['name'], count=1)
                self.assertEqual(display_name, unescape(cells[2][2]))
                anchor = catalog.tool_explanations.anchor_for(row['key'])
                self.assertIn(f'{tier}.md#{anchor}', markdown)
                self.assertIn(f'<a id="{anchor}"></a>', markdown, '旧README对象锚点应保留为跳转入口')
        self.assertEqual(len(rows), total_tables, '所有对象恰好进入一个阶级页或黄阶页中的未定级附录')
        self.assertIn('第一性原理', views['di.md'])
        self.assertIn('天阶高级', views['tian.md'])
        self.assertNotIn('天高', views['tian.md'])
        self.assertNotIn('地高', views['tian.md'])

    def test_numbered_chapter_prefixes_are_removed_from_all_rendered_views(self):
        rows = catalog.merge_rows(deepcopy(self.documents))
        views = catalog.render_views(ROOT, rows, self.binding)
        prefix = re.compile(r'^\d+(?:\.\d+)+[ \t]+')
        numbered = [row for row in rows if prefix.match(row['name'])]
        self.assertEqual(len(numbered), 101)
        self.assertIn('3.5 效应局部化', [row['name'] for row in numbered])
        duplicate_display = [row for row in rows
                             if prefix.sub('', row['name'], count=1) == '信息隐藏']
        self.assertEqual(len(duplicate_display), 2)
        self.assertEqual(len({catalog.tool_explanations.anchor_for(row['key'])
                              for row in duplicate_display}), 2)
        for row in numbered:
            match = prefix.match(row['name'])
            display_name = row['name'][match.end():]
            anchor = catalog.tool_explanations.anchor_for(row['key'])
            tier = row['grade_id'].split('-', 1)[0] if row['grade_id'] else 'huang'
            page = views[tier + '.md']
            link = next(line for line in page.splitlines() if line.endswith(f'(#{anchor})'))
            decoded_link = unescape(link)
            self.assertIn(f'[{display_name}](#{anchor})', decoded_link)
            self.assertNotIn(row['name'], decoded_link)
            section = page.split(f'<a id="{anchor}"></a>', 1)[1].split('<a id="', 1)[0]
            decoded_section = unescape(section)
            self.assertIn(f'### {display_name}', decoded_section)
            self.assertIn(f'| 1 | 工具的名称 | {display_name} |', decoded_section)
            readme_link = next(line for line in views['README.md'].splitlines()
                               if f'{tier}.md#{anchor})' in line)
            decoded_readme_link = unescape(readme_link)
            self.assertIn(f'[{display_name}](', decoded_readme_link)
            self.assertNotIn(row['name'], decoded_readme_link)

    def test_user_confirmed_candidate_review_replaces_stale_labels_in_active_views(self):
        items = [item for item in self.documents['explanations_v1']['items']
                 if item['object_key'].startswith('registry:gongfa-candidate-')]
        self.assertEqual(len(items), 331)
        stale_labels = STALE_EXPLANATION_LABELS
        for item in items:
            fields = {field['name']: field['content'] for field in item['fields']}
            self.assertEqual(list(fields), v1_field_names())
            self.assertIn('用户确认说明正式通过审阅', fields['关联信息'])
            self.assertNotIn('既有既有初评', fields['关联信息'])
            for label in stale_labels:
                self.assertNotIn(label, '\n'.join(fields.values()), item['object_key'])

        rows = catalog.merge_rows(deepcopy(self.documents))
        views = catalog.render_views(ROOT, rows, self.binding)
        self.assertIn('331条已登记说明已由用户确认正式通过审阅', views['README.md'])
        for name in ('README.md', 'tian.md', 'di.md', 'xuan.md', 'huang.md'):
            for label in stale_labels:
                self.assertNotIn(label, views[name], name)

    def test_book_citation_is_scoped_to_the_101_exact_source_records(self):
        html_sha = '38fae80333632ff3e077990fd953f8e7a97fe918497563901c125c4be799f326'
        book_url = 'https://book.douban.com/subject/35088343/'
        catalogue_url = 'https://jp.tfswufe.edu.cn/opac/book/d741c0e6dd191cb4fec62706743b745d'
        expected_ids = {f'A{number:03}' for number in range(1, 102)}
        candidates = {item['candidate_id']: item
                      for item in self.documents['html211_candidates']['candidates']
                      if item['source_selection'].get('file') == '编程的原则.html'
                      and item['source_selection'].get('actual_html_sha256') == html_sha}
        self.assertEqual(expected_ids, set(candidates))

        cited = {}
        for item in self.documents['explanations_v1']['items']:
            fields = {field['name']: field['content'] for field in item['fields']}
            provenance = fields['出处']
            start = provenance.find('{')
            if start < 0:
                continue
            metadata = json.loads(provenance[start:provenance.rfind('}') + 1])
            selection = metadata.get('source_selection', {})
            if selection.get('file') != '编程的原则.html' or selection.get('actual_html_sha256') != html_sha:
                continue
            candidate_id = metadata['candidate_record'].split(':', 1)[1]
            self.assertNotIn(candidate_id, cited)
            cited[candidate_id] = (metadata, fields['相关图书'])

        self.assertEqual(expected_ids, set(cited))
        for candidate_id, (metadata, related_book) in cited.items():
            candidate = candidates[candidate_id]
            self.assertEqual(candidate['source_selection'], metadata['source_selection'], candidate_id)
            self.assertEqual(candidate['declared_upstream'], metadata['declared_upstream'], candidate_id)
            for fact in ('上田勋著', '支鹏浩译', '编程的原则：改善代码质量的101个方法',
                         '人民邮电出版社', '2020年6月', '978-7-115-53914-4',
                         book_url, catalogue_url, metadata['declared_upstream'],
                         '尚未逐项独立核对原书/EPUB或纸本页码', '许可证尚未核验'):
                self.assertIn(fact, related_book, candidate_id)

    def test_stale_status_scan_covers_all_441_explanation_items_without_rewriting_them(self):
        expected_counts = {'gongfa': 411, 'faqi': 30}
        bundles = source_archive.bundles(ROOT)
        self.assertEqual(set(expected_counts), set(bundles))
        hits = []
        total = 0
        for kind, expected_count in expected_counts.items():
            payload = bundles[kind]['data'].get('explanations_v1')
            self.assertIsNotNone(payload, f'{kind}缺少当前v1说明载荷')
            items = payload['items']
            self.assertEqual(expected_count, len(items), kind)
            total += len(items)
            for item in items:
                for field in item['fields']:
                    for label in STALE_EXPLANATION_LABELS:
                        if label in field['content']:
                            hits.append(f"{kind}:{item['object_key']}:{field['name']}:{label}")
        self.assertEqual(441, total)
        self.assertEqual([], hits, '仅报告过时状态词候选，不自动改写说明：' + chr(10) + chr(10).join(hits))

    def test_v1_template_appends_the_three_argument_fields_without_changing_v0(self):
        rows = template_rows(V1_TEMPLATE)
        self.assertEqual(list(range(1, 19)), [number for number, _name in rows])
        self.assertEqual(
            v0_field_names() + ['结论', '连接规则', '依据'],
            [name for _number, name in rows],
        )
        contract = V1_TEMPLATE.read_text(encoding='utf-8')
        self.assertIn('图尔敏', contract)
        self.assertIn('Warrant', contract)
        self.assertIn('仅列字段交叉引用', contract)

    def test_active_v1_payload_migrates_all_441_records_with_toulmin_warrants(self):
        expected_counts = {'gongfa': 411, 'faqi': 30}
        expected_names = v0_field_names() + ['结论', '连接规则', '依据']
        bundles = source_archive.bundles(ROOT)
        total = 0
        for kind, expected_count in expected_counts.items():
            data = bundles[kind]['data']
            self.assertNotIn('explanations_v0', data, f'{kind}不得保留双版本活跃载荷')
            payload = data.get('explanations_v1')
            self.assertIsNotNone(payload, f'{kind}缺少当前v1说明载荷')
            self.assertEqual(expected_count, len(payload['items']), kind)
            self.assertEqual(payload['template_sha256'], catalog.tool_explanations.template_sha256(ROOT))
            total += len(payload['items'])
            for item in payload['items']:
                fields = {field['name']: field['content'] for field in item['fields']}
                self.assertEqual(expected_names, list(fields), item['object_key'])
                self.assertIn(fields['提炼共同规律。'], fields['结论'], item['object_key'])
                warrant = fields['连接规则']
                self.assertTrue(warrant.startswith('推理桥梁：'), item['object_key'])
                self.assertIn('证据命题：', warrant, item['object_key'])
                self.assertIn('推理根据：', warrant, item['object_key'])
                self.assertGreater(len(warrant), 200, item['object_key'])
                self.assertIn('由于', warrant, item['object_key'])
                self.assertIn('因此', warrant, item['object_key'])
                self.assertIn('不据此外推未观察效果、许可或正式评级', warrant, item['object_key'])
                condition = ' '.join(fields['明确这些规律成立的前提与适用条件。'].split()).strip(' ；;，,。\n')
                boundary = warrant.split('成立边界：', 1)[1].split('不据此外推未观察效果、许可或正式评级。', 1)[0]
                if condition not in boundary:
                    self.assertIn('以第15项列出的适用条件、限制及其待核状态为准', boundary, item['object_key'])
                self.assertNotIn('仅当第18项支持第11项机制适用于第9项问题', warrant, item['object_key'])
                self.assertIn('第7项', fields['依据'], item['object_key'])
                self.assertIn('第11项', fields['依据'], item['object_key'])
        self.assertEqual(441, total)
        gongfa_items = {
            item['object_key']: {field['name']: field['content'] for field in item['fields']}
            for item in bundles['gongfa']['data']['explanations_v1']['items']
        }
        performance_sources = ('html211:D008', 'html211:D009', 'html211:D010')
        archive_path = '.github/metadata/gongfa/source-classified-candidates-20261007.json'
        archive_document = bundles['gongfa']['data']['documents'][archive_path]
        archive = json.loads(archive_document['data'])
        archived_candidates = {
            item['candidate_id']: item
            for item in archive['documents']['html211_candidates']['candidates']
        }
        pareto_source = archived_candidates['D008']['original_text']
        self.assertIn('80/20是近似经验，不是固定比例', pareto_source)
        self.assertIn('热点需要通过测量确认', pareto_source)
        for object_key in (
            'registry:gongfa-candidate-html211-d008-6fd753377e@r1',
            'registry:gongfa-candidate-html211-d009-4d61eda424@r1',
            'registry:gongfa-candidate-html211-d010-5015859ffd@r1',
        ):
            warrant = gongfa_items[object_key]['连接规则']
            self.assertIn('热点需要通过测量确认', warrant, object_key)
            self.assertIn('80/20是近似经验，不是固定比例', warrant, object_key)
            self.assertNotIn('实测热点', warrant, object_key)
            basis = gongfa_items[object_key]['依据']
            self.assertIn(archive_document['sha256'], basis, object_key)
            for source_id in performance_sources:
                self.assertIn(source_id, basis, object_key)
            for candidate_id in ('D008', 'D009', 'D010'):
                source = archived_candidates[candidate_id]
                selection = source['source_selection']
                self.assertIn(source['text_sha256'], basis, object_key)
                self.assertIn(f"passages {selection['start']}–{selection['end']}", basis, object_key)

    def test_historical_archive_status_words_are_identified_as_historical(self):
        rows = catalog.merge_rows(deepcopy(self.documents))
        markdown = catalog.render_views(ROOT, rows, self.binding)['README.md']
        self.assertIn(
            '原文档中的候选/复核状态只表示记录时点；当前登记和说明审阅状态以本总表及对象页为准。',
            markdown,
        )

    def test_candidate_promotion_preserves_the_frozen_undetermined_set(self):
        entries = self.documents['registry']['gongfa']
        by_anchor = {entry['source_ref']['heading_id']: entry for entry in entries
                     if entry['source_ref']['source_id'] == 'source-classified-candidates-20261007'}
        self.assertEqual(len(by_anchor), 331)
        self.assertEqual({anchor for anchor, entry in by_anchor.items()
                          if entry['name'] in {'灾备容量负载放大模型', 'CAP 定理 (CAP Theorem)'}},
                         {'html211:E001', 'html96:VC029'})
        for entry in by_anchor.values():
            self.assertEqual(entry['entry_status'], 'registered')
            self.assertEqual(entry['source_ref']['selection'], 'candidate-record')
            self.assertEqual(entry['source_ref']['stop_before'], None)
            self.assertEqual(entry['content']['text_sha256'], sha256(
                entry['content']['original_text'].encode('utf-8')).hexdigest())

    def test_registry_candidate_count_is_separate_from_historical_sources(self):
        documents = deepcopy(self.documents)
        candidate = deepcopy(next(item for item in documents['registry']['gongfa']
                                  if item['id'] == 'gongfa-first-principles'))
        candidate['id'] = 'gongfa-isolated-candidate-count'
        candidate['name'] = '隔离候选计数'
        candidate['entry_status'] = 'candidate'
        candidate['ontology_type'] = None
        documents['registry']['gongfa'].append(candidate)
        rows = catalog.merge_rows(documents)
        self.assertEqual(sum(row['entry_status'] == '登记库候选' for row in rows), 1)
        self.assertEqual(412, len(rows))
        self.assertIn('合计412条', '\n'.join(catalog.notes(rows, self.binding)))

    def test_registry_updates_follow_explicit_correction_and_never_inherit_a_new_version(self):
        documents = deepcopy(self.documents)
        batch = documents['registry']['grade_proposals'][0]
        correction = deepcopy(batch)
        correction['id'] = 'test-explicit-correction'
        correction['supersedes'] = batch['id']
        correction['assessed_at'] = '2026-10-08T00:00:00Z'
        for item in correction['items']:
            if item['gongfa_id'] == 'gongfa-first-principles':
                item['grade_id'] = 'xuan-intermediate'
                item['reason'] = '隔离夹具的显式更正。'
        documents['registry']['grade_proposals'].append(correction)
        new_version = deepcopy(next(item for item in documents['registry']['gongfa'] if item['id'] == 'gongfa-first-principles'))
        new_version['content_version'] = 'r2'
        new_version['predecessor_version'] = 'r1'
        new_version['content']['original_text'] = '新版本的限定内容尚无初评。'
        new_version['content']['text_sha256'] = sha256('新版本的限定内容尚无初评。'.encode('utf-8')).hexdigest()
        documents['registry']['gongfa'].append(new_version)
        selected = {row['content_version']: row for row in catalog.merge_rows(documents) if row['namespace'] == 'registry' and row['original_id'] == 'gongfa-first-principles'}
        self.assertEqual(selected['r1']['grade_id'], 'xuan-intermediate')
        self.assertEqual(selected['r1']['reason'], '隔离夹具的显式更正。')
        self.assertIsNone(selected['r2']['grade_id'])
        self.assertEqual(selected['r2']['grading_status'], 'unrated')
        another = deepcopy(correction)
        another['id'] = 'test-another-context'
        another['supersedes'] = None
        another['application_context'] = '隔离夹具的不同任务情境'
        documents['registry']['grade_proposals'].append(another)
        row = next(r for r in catalog.merge_rows(documents) if r['namespace'] == 'registry' and r['original_id'] == 'gongfa-first-principles' and r['content_version'] == 'r1')
        self.assertEqual(row['grading_status'], 'multiple-contexts')
        self.assertIsNone(row['grade_id'])
        self.assertIn('test-another-context', row['reason'])

    def test_portable_inputs_reject_drift_and_out_of_project_paths(self):
        root = self.isolated_project()
        result = self.command(root, '--write')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.command(root, '--check').returncode, 0)
        data_path = root / '.github/context/gongfa/data.json'
        before = data_path.read_bytes()
        self.assertEqual({p.name for p in data_path.parent.iterdir()},
                         {'data.json', 'README.md', 'tian.md', 'di.md', 'xuan.md', 'huang.md'})
        bundle = json.loads(before)
        index_key = '.github/metadata/gongfa/catalog-sources.json'
        source_index = json.loads(bundle['documents'][index_key]['data'])
        snapshot_key = '.github/metadata/gongfa/' + source_index['snapshot']['path']
        snapshot = bundle['documents'][snapshot_key]
        snapshot['data'] += '\n'
        snapshot['sha256'] = sha256(snapshot['data'].encode()).hexdigest()
        data_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding='utf-8')
        self.assertEqual(self.command(root, '--check').returncode, 1)
        source_index['snapshot']['path'] = '../outside.json'
        index = bundle['documents'][index_key]
        index['data'] = json.dumps(source_index)
        index['sha256'] = sha256(index['data'].encode()).hexdigest()
        data_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding='utf-8')
        self.assertEqual(self.command(root, '--check').returncode, 1)

    def test_markdown_text_safety_stale_detection_and_generated_file_ownership(self):
        documents = deepcopy(self.documents)
        item = documents['html96_candidates']['candidates'][0]
        grade = documents['html96_grades']['items'][0]
        entry = next(record for record in documents['registry']['gongfa']
                     if record['source_ref']['heading_id'] == 'html96:' + item['candidate_id'])
        item['name'] = grade['name'] = entry['name'] = '<script>bad</script>|=2+2'
        rows = catalog.merge_rows(documents)
        hostile_row = next(row for row in rows if row['namespace'] == 'registry' and row['original_id'] == entry['id'])
        if 'explanation_fields' not in hostile_row:
            hostile_row['explanation_fields'] = [{'name': label, 'content': item['name'] if index == 0 else '隔离安全测试'}
                                                 for index, label in enumerate(v1_field_names())]
        hostile_row['explanation_fields'][0]['content'] = item['name']
        root = Path(tempfile.mkdtemp(prefix='markdown-', dir=ARTIFACTS))
        target = root / '.github/context/gongfa'
        target.mkdir(parents=True)
        catalog.write_views(root, rows, self.binding)
        catalog.check_views(root, rows, self.binding)
        markdown = (target / 'README.md').read_text()
        self.assertNotIn('<script>bad</script>', markdown)
        self.assertIn('&lt;script&gt;bad&lt;/script&gt;&#124;=2+2', markdown)
        target_tier = hostile_row['grade_id'].split('-', 1)[0] if hostile_row['grade_id'] else 'huang'
        target_page = (target / (target_tier + '.md')).read_text()
        self.assertNotIn('<script>bad</script>', target_page)
        self.assertIn('&lt;script&gt;bad&lt;/script&gt;&#124;=2+2', target_page)
        self.assertEqual({p.name for p in target.iterdir()},
                         {'README.md', 'tian.md', 'di.md', 'xuan.md', 'huang.md'})
        (target / 'README.md').write_text(markdown.replace('天阶高级', '改动品级', 1))
        with self.assertRaises(ValueError): catalog.check_views(root, rows, self.binding)
        for text in ['超限' * (4 * 1024 * 1024), '非法\x01字符']:
            bad = deepcopy(rows)
            bad[0]['name'] = text
            with self.assertRaises(ValueError): catalog.write_views(root, bad, self.binding)
        hand_written = Path(tempfile.mkdtemp(prefix='owned-', dir=ARTIFACTS))
        own_target = hand_written / '.github/context/gongfa'
        own_target.mkdir(parents=True)
        (own_target / 'README.md').write_text('手工内容，不能覆盖。', encoding='utf-8')
        with self.assertRaises(ValueError): catalog.write_views(hand_written, rows, self.binding)
        self.assertEqual((own_target / 'README.md').read_text(), '手工内容，不能覆盖。')


def main():
    global ARTIFACTS, catalog
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path)
    args = parser.parse_args()
    ARTIFACTS = args.artifacts or Path(tempfile.mkdtemp(prefix='gongfa-catalog-test-'))
    if args.artifacts:
        ARTIFACTS.mkdir(parents=True, exist_ok=False)
    ARTIFACTS = ARTIFACTS.resolve()
    spec = importlib.util.spec_from_file_location('gongfa_catalog', SCRIPT)
    catalog = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(catalog)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CatalogMaintenanceTest))
    save(ARTIFACTS / 'result.json', {'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
                                   'success': result.wasSuccessful(), 'script_sha256': sha256(SCRIPT.read_bytes()).hexdigest()})
    print('测试工件：' + str(ARTIFACTS))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
