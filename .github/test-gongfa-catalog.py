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


def v0_field_names():
    return [line.split('|')[2].strip() for line in TEMPLATE.read_text(encoding='utf-8').splitlines()
            if line.startswith('| ') and line.split('|')[1].strip().isdigit()]


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
        shutil.copyfile(TEMPLATE, template_dir / TEMPLATE.name)
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
        self.assertEqual(Counter(row['namespace'] for row in rows), {'registry': 80, 'html211': 211, 'solve24': 24, 'html96': 96})
        self.assertEqual(len(rows), 411)
        self.assertEqual(len({(r['namespace'], r['original_id'], r['content_version']) for r in rows}), 411)
        undetermined = {(r['namespace'], r['original_id']) for r in rows if r['grading_status'] == 'undetermined'}
        self.assertEqual(undetermined, {('html211', 'E001'), ('html96', 'VC029')})
        by_id = {(r['namespace'], r['original_id']): r for r in rows}
        self.assertEqual(by_id['registry', 'gongfa-first-principles']['grade_id'], 'di-advanced')
        self.assertEqual(by_id['solve24', 'psoa.programming.minimal-reproduction']['grade_id'], 'di-initial')
        self.assertIn('一个分布式系统最多只能保证一致性、可用性和分区容错性中的两项。', by_id['html96', 'VC029']['original_text'])
        self.assertIn('失去50%容量时剩余单位需要承担2倍总流量。', by_id['html211', 'E001']['original_text'])
        self.assertEqual(sum(r['entry_status'] == '已登记' for r in rows), 80)
        glue_index = next(index for index, row in enumerate(rows) if row['original_id'] == 'gongfa-glue-coding')
        self.assertEqual(rows[glue_index + 1]['name'], 'Lambda 演算')
        self.assertEqual(rows[glue_index + 1]['grade_id'], 'tian-advanced')
        self.assertIn('天级上品', rows[glue_index + 1]['reason'])
        rendered = catalog.book_views.render_sources(ROOT, 'gongfa')
        chapters = [line for line in rendered.splitlines() if line.startswith('## ')]
        self.assertEqual(chapters[chapters.index('## 拼好码') + 1], '## Lambda 演算')
        self.assertEqual(sum(r['entry_status'] == '登记库候选' for r in rows), 0)
        self.assertEqual(self.documents['registry']['assessments'], [])
        registry_item = next(item for item in self.documents['registry']['gongfa'] if item['id'] == 'gongfa-first-principles')
        profile = registry_item['content']['profile']
        profile_parts = [profile['summary'], '问题：' + profile['problem'], '机制：' + profile['mechanism']]
        for key, label in (('conditions', '条件'), ('limitations', '限制'), ('expected_outcomes', '预期结果')):
            if profile[key]:
                profile_parts.append(label + '：' + '；'.join(profile[key]))
        self.assertEqual(' '.join(profile_parts), by_id['registry', 'gongfa-first-principles']['explanation'])
        html_grade = next(item for item in self.documents['html211_grades']['items'] if item['candidate_id'] == 'E001')
        html_candidate = next(item for item in self.documents['html211_candidates']['candidates'] if item['candidate_id'] == 'E001')
        expected_html_explanation = (html_candidate['original_text'] + ' 用途/任务族：' + html_grade['task_family'] +
                                     ' 初评说明：' + html_grade['reason'])
        self.assertEqual(expected_html_explanation, by_id['html211', 'E001']['explanation'])
        solve_item = self.documents['solve24_analysis']['items'][0]
        solve_grade = solve_item['editorial_analysis']
        solve_row = by_id['solve24', solve_grade['source_id']]
        expected_solve_explanation = '；'.join((
            '用途/任务族：' + solve_grade['task_family'],
            '机制：' + solve_grade['mechanism'],
            '适用：' + '；'.join(solve_item['source_when']),
            '不适用：' + '；'.join(solve_item['source_not_when']),
            '前提：' + '；'.join(solve_item['source_preconditions']),
            '边界：' + solve_grade['editorial_caveat'],
        ))
        self.assertEqual(expected_solve_explanation, solve_row['explanation'])
        views = catalog.render_views(ROOT, rows, self.binding)
        markdown = views['README.md']
        self.assertIn('- 共**411条内容记录**；已登记80条，登记库候选0条，未入登记库的来源候选331条。', markdown)
        self.assertNotIn('[控制论与科学方法论](#控制论与科学方法论)', markdown)
        self.assertFalse('catalog.xlsx' in markdown, '活动阅读视图只有Markdown，历史Excel仅作原始载荷保存')
        self.assertLess(len(markdown.encode('utf-8')), 512 * 1024, 'README只作为轻量导航，不再展开全部功法表格与文集正文')
        self.assertNotIn('| 序号 | 说明项 | 内容 |', markdown)
        self.assertIn('## 原文文集', markdown)
        self.assertIn('<a id="doc-glue-coding"></a>', markdown)
        self.assertIn('tian.md#', markdown)
        self.assertIn('huang.md#', markdown)
        field_names = v0_field_names()
        self.assertEqual(15, len(field_names))
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
                table_rows = lines[start:start + 17]
                self.assertEqual(17, len(table_rows))
                self.assertEqual('|:---:|:---|:---|', table_rows[1])
                cells = [parse_pipe_row(line) for line in table_rows]
                self.assertTrue(all(len(cell) == 3 for cell in cells), '每张表严格为三列')
                self.assertEqual(field_names, [cell[1] for cell in cells[2:]])
                self.assertEqual(row['name'], unescape(cells[2][2]))
                anchor = catalog.tool_explanations.anchor_for(row['key'])
                self.assertIn(f'{tier}.md#{anchor}', markdown)
                self.assertIn(f'<a id="{anchor}"></a>', markdown, '旧README对象锚点应保留为跳转入口')
        self.assertEqual(len(rows), total_tables, '所有对象恰好进入一个阶级页或黄阶页中的未定级附录')
        self.assertIn('第一性原理', views['di.md'])
        self.assertIn('天阶高级', views['tian.md'])
        self.assertNotIn('天高', views['tian.md'])
        self.assertNotIn('地高', views['tian.md'])

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
        item['name'] = grade['name'] = '<script>bad</script>|=2+2'
        rows = catalog.merge_rows(documents)
        hostile_row = next(row for row in rows if row['namespace'] == 'html96' and row['original_id'] == item['candidate_id'])
        if 'v0_fields' not in hostile_row:
            hostile_row['v0_fields'] = [{'name': label, 'content': item['name'] if index == 0 else '隔离安全测试'}
                                        for index, label in enumerate(v0_field_names())]
        hostile_row['v0_fields'][0]['content'] = item['name']
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
