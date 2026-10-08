#!/usr/bin/env python3
"""功法JSON协议的CLI集成测试；仅使用隔离文件，不联网、不实际评级。

运行：python3 scripts/test-gongfa.py --artifacts /tmp/gongfa-test-run
产物：每个输入与CLI输出、result.json和JUnit XML。需要功法检查器的依赖。
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = None
EXPECTED_INITIAL_IDS = {
    'gongfa-compositional-description', 'gongfa-network-effects', 'gongfa-occams-razor',
    'gongfa-glue-principle', 'gongfa-first-principles', 'gongfa-abductive-debugging',
}
# 清单来自收录范围，不调用被测提取器产生期望。
EXPECTED_WEBSITE_NAMES = {
    '固定点收敛系统', '递归式 AI 治理', '拼好码', '吸引子', '有限样本生成推断',
    'AI-native', '拍扁', '符号序列空间与有效知识子集', '合成模型', '解空间',
    '近端因果机制', '目的导向的行动选择', '预测加工与模型更新', '受约束的状态变换',
    '最小先验条件下的代理增强型任务求解', 'Projection 表示转换', '状态分类工具',
}
# 本轮清单由已读独立方法及真实锚点确定，不从registry反向生成。
EXPECTED_EXPANSION_ANCHORS = {
    'gongfa-top-down-system-design': 'concept-system-building-一自顶向下先看整体再拆细节',
    'gongfa-bottom-up-system-building': 'concept-system-building-二自底向上先做组件再组系统',
    'gongfa-divide-and-conquer': 'concept-system-building-三分而治之把复杂问题拆成小问题',
    'gongfa-problem-definition-framework': 'concept-problem-solving-5-搭建体系',
    'gongfa-methodology-delivery-loop': 'philosophy-methodology-toolbox-总体作业流',
    'gongfa-cybernetic-feedback-method': 'philosophy-methodology-toolbox-控制论与科学方法论',
    'gongfa-recursive-generator-optimization': 'concept-recursive-self-optimizing-system',
    'gongfa-specification-before-implementation': 'philosophy-programming-dao-规约先于实现',
    'gongfa-state-ownership-questions': 'philosophy-programming-dao-10-时间视角',
}
# 仓内续收范围来自逐节阅读，不以文件数或标题数充当独立功法数。
EXPECTED_REPO_CONTINUATION_ANCHORS = {
    'gongfa-high-cohesion': 'philosophy-programming-dao-高内聚',
    'gongfa-low-coupling': 'philosophy-programming-dao-低耦合',
    'gongfa-stable-interface-contract': 'philosophy-programming-dao-稳定接口不稳定实现',
    'gongfa-explicit-dependencies': 'philosophy-programming-dao-隐藏的依赖最危险',
    'gongfa-invariant-constraints': 'philosophy-programming-dao-不变式保持世界稳定',
    'gongfa-reasonable-code': 'philosophy-programming-dao-9-可推理性',
    'gongfa-least-surprise': 'philosophy-programming-dao-16-最小惊讶原则',
    'gongfa-validated-abstraction': 'philosophy-software-engineering-truths-5-重复代码不一定坏错误抽象更坏',
    'gongfa-technical-debt-ledger': 'philosophy-software-engineering-truths-14-技术债不是罪假装没有技术债才是罪',
    'gongfa-performance-by-measurement': 'philosophy-software-engineering-truths-16-性能问题要靠测量不要靠感觉',
    'gongfa-controllable-failure': 'philosophy-software-engineering-truths-18-稳定不是没有故障而是故障可控',
    'gongfa-decision-rationale-documentation': 'philosophy-software-engineering-truths-23-文档不是装饰品',
    'gongfa-dataset-first-architecture': 'reference-engineering-practice-7-dataset-first-数据服务结构',
    'gongfa-dataset-service-construction': 'reference-engineering-practice-新建数据服务流程',
    'gongfa-external-source-dataset-adaptation': 'reference-engineering-practice-外部源码接入流程',
    'gongfa-symbol-name-index-maintenance': 'reference-engineering-practice-1-变量名维护方案',
    'gongfa-input-state-transform-separation': 'reference-engineering-practice-33-消费端-生产端-状态变量-变换函数',
    'gongfa-shared-resource-concurrency': 'reference-engineering-practice-34-并发concurrency',
    'gongfa-dry-reuse': 'reference-engineering-practice-54-dry-原则不要重复',
    'gongfa-input-scale-complexity-constraints': 'reference-engineering-practice-三新手常见复杂度误区',
    'gongfa-cache-lifecycle-isolation': 'reference-engineering-practice-六缓存误用',
}


class GongfaProtocolTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = ARTIFACTS / 'fixture'
        cls.fixture.mkdir()
        shutil.copytree(ROOT / 'metadata/gongfa', cls.fixture / 'metadata/gongfa')
        cls.baseline = json.loads((cls.fixture / 'metadata/gongfa/registry.json').read_text())
        cls.sequence = 0

    def run_catalog(self, document, label, extra_args=()):
        type(self).sequence += 1
        stem = ARTIFACTS / ('%03d-%s' % (self.sequence, label))
        path = stem.with_suffix('.json')
        path.write_text(json.dumps(document, ensure_ascii=False, allow_nan=False) + '\n')
        return self.run_path(path, stem, extra_args)

    def run_path(self, path, stem, extra_args=()):
        command = [sys.executable, str(ROOT / 'scripts/check-gongfa.py'),
                   '--root', str(self.fixture), '--registry', str(path)] + list(extra_args)
        process = subprocess.run(command, capture_output=True, text=True, timeout=20)
        stem.with_suffix('.log').write_text(process.stdout + process.stderr)
        stem.with_suffix('.command.json').write_text(json.dumps({
            'command': command, 'returncode': process.returncode,
            'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        }, ensure_ascii=False, indent=2) + '\n')
        return process

    def test_complete_initial_collection(self):
        process = self.run_catalog(self.baseline, 'initial-collection')
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        summary = json.loads(process.stdout)
        self.assertEqual(summary['grade_values'], 12)
        self.assertGreaterEqual(summary['content_versions'], 49)
        self.assertEqual(summary['rated_assessments'], 0)
        entries = self.baseline['gongfa']
        for identity in EXPECTED_INITIAL_IDS:
            matches = [entry for entry in entries if entry['id'] == identity]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['content_version'], 'r1')
            self.assertEqual(matches[0]['entry_status'], 'registered')
        site = [entry for entry in entries if entry['source_ref']['source_id'] ==
                'tradecatlabs-vibe-coding-methodology-page']
        self.assertEqual({entry['name'] for entry in site}, EXPECTED_WEBSITE_NAMES)
        by_id = {entry['id']: entry for entry in entries}
        self.assertEqual(by_id['gongfa-ai-native']['content']['profile']['questions'], [
            '更一般地，它追问机器自主性上升后，行动权、控制权与最终责任如何重新分配。'])
        self.assertTrue(any('持续操控' in item for item in
                            by_id['gongfa-predictive-processing-update']['content']['profile']['limitations']))
        self.assertTrue(any('MRE' in item for item in
                            by_id['gongfa-phenomenological-reduction']['content']['profile']['expected_outcomes']))
        self.assertIsNotNone(by_id['gongfa-state-space-thinking']['content']['profile']['problem'])
        for identity, boundary in [
                ('gongfa-fixed-point-convergence', '缺乏稳定性'),
                ('gongfa-attractor-model', '指标投机'),
                ('gongfa-minimal-prior-agent-assisted-solving', '操作风险')]:
            with self.subTest(identity=identity):
                self.assertTrue(any(boundary in item for item in
                                    by_id[identity]['content']['profile']['limitations']))
        self.assertTrue(any('人工介入' in item for item in
                            by_id['gongfa-recursive-ai-governance']['content']['profile']['expected_outcomes']))
        for identity, anchor in EXPECTED_EXPANSION_ANCHORS.items():
            with self.subTest(identity=identity):
                self.assertIn(identity, set(by_id))
                entry = by_id[identity]
                self.assertEqual(entry['source_ref']['heading_id'], anchor)
                self.assertEqual(entry['entry_status'], 'registered')
                self.assertEqual(entry['content_version'], 'r1')
                self.assertIn(entry['ontology_type'], {
                    'explanatory-content', 'normative-allocation-content',
                    'method-specification', 'dao-content'})
        for identity, field, phrase in [
                ('gongfa-compositional-description', 'questions', '同一个'),
                ('gongfa-glue-principle', 'questions', '官方能力'),
                ('gongfa-first-principles', 'questions', '前提'),
                ('gongfa-phenomenological-reduction', 'conditions', '复现'),
                ('gongfa-top-down-system-design', 'limitations', '返工'),
                ('gongfa-bottom-up-system-building', 'limitations', '拼不起来'),
                ('gongfa-divide-and-conquer', 'limitations', '集成'),
                ('gongfa-recursive-generator-optimization', 'conditions', '压缩性')]:
            with self.subTest(identity=identity, field=field):
                self.assertIn(identity, set(by_id))
                self.assertTrue(any(phrase in item for item in by_id[identity]['content']['profile'][field]))
        # 网络效应r1只收一句解释，不得借同文章后面的操作版补造条件。
        self.assertEqual(by_id['gongfa-network-effects']['content']['profile']['conditions'], [])
        self.assertEqual(by_id['gongfa-network-effects']['content']['profile']['limitations'], [])
        causal = by_id['gongfa-proximate-causal-mechanism']['content']['profile']
        self.assertTrue(all('若存在' not in item for item in causal['conditions']))
        self.assertTrue(any('共同原因' in item for item in causal['limitations']))
        self.assertTrue(all(entry['ontology_type'] is not None for entry in entries))
        self.assertTrue(all(entry['entry_status'] == 'registered' for entry in entries))
        proposals = self.baseline.get('grade_proposals', [])
        self.assertTrue(proposals, '应有实际人工初评批次，而非只保留未评级条目')
        targets = {(entry['id'], entry['content_version']) for entry in entries}
        self.assertEqual({(item['gongfa_id'], item['content_version'])
                          for batch in proposals for item in batch['items']}, targets)
        self.assertEqual(summary['proposed_grades'], len(entries))
        for batch in proposals:
            self.assertEqual(batch['basis'], 'expert_judgment')
            self.assertEqual(batch['status'], 'provisional')

    def test_repository_continuation(self):
        by_id = {entry['id']: entry for entry in self.baseline['gongfa']}
        for identity, anchor in EXPECTED_REPO_CONTINUATION_ANCHORS.items():
            with self.subTest(identity=identity):
                self.assertIn(identity, by_id)
                entry = by_id[identity]
                self.assertEqual(entry['source_ref']['heading_id'], anchor)
                self.assertEqual(entry['content_version'], 'r1')
                self.assertEqual(entry['entry_status'], 'registered')
        batches = [batch for batch in self.baseline['grade_proposals']
                   if batch['id'] == 'gongfa-author-repo-expansion-20261007']
        self.assertEqual(len(batches), 1)
        self.assertIsNone(batches[0]['supersedes'])
        self.assertEqual({item['gongfa_id'] for item in batches[0]['items']},
                         set(EXPECTED_REPO_CONTINUATION_ANCHORS))
        original = [batch for batch in self.baseline['grade_proposals']
                    if batch['id'] == 'gongfa-author-initial-20261007']
        self.assertEqual(len(original), 1)
        self.assertTrue(set(EXPECTED_REPO_CONTINUATION_ANCHORS).isdisjoint(
            item['gongfa_id'] for item in original[0]['items']))
        prefix = by_id['gongfa-dataset-first-architecture']
        self.assertEqual(prefix['source_ref']['selection'], 'markdown-prefix')
        self.assertIn('不适合直接照抄', prefix['content']['original_text'])
        self.assertNotIn('service-root/', prefix['content']['original_text'])
        self.assertNotIn('新建数据服务流程', prefix['content']['original_text'])
        self.assertEqual(by_id['gongfa-stable-interface-contract']['content']['original_text'],
                         '- API 是契约\n- 实现是细节\n- 不破坏契约，就是负责')
        for identity in ('gongfa-high-cohesion', 'gongfa-stable-interface-contract',
                         'gongfa-input-scale-complexity-constraints'):
            profile = by_id[identity]['content']['profile']
            self.assertEqual(profile['conditions'], [])
            self.assertIn('conditions', profile['missing_fields'])

    def proposal_batch(self):
        entry = self.baseline['gongfa'][0]
        policy = self.baseline['policies'][0]
        return {
            'id': 'test-initial-grading', 'vocabulary_id': 'gongfa-grade-vocabulary-v1',
            'policy_id': policy['id'], 'policy_version': policy['version'],
            'status': 'provisional', 'basis': 'expert_judgment',
            'assessor': '隔离协议测试，不是独立效果评审', 'assessed_at': '2026-10-07T12:00:00Z',
            'application_context': '解释软件系统中对象、状态与变化的受控案例',
            'baseline_assumption': '同目标和预算下采用现行需求、设计与验证流程',
            'limits': ['人工初评不是实际效果或独立实验结论。'], 'supersedes': None,
            'items': [{
                'gongfa_id': entry['id'], 'content_version': entry['content_version'],
                'content_sha256': entry['content']['text_sha256'],
                'ontology_type': 'explanatory-content', 'grade_id': 'xuan-initial',
                'task_family': '系统变化的解释与诊断',
                'classification_reason': '限定内容解释对象、状态、过程及关系，不规定一次执行。',
                'reason': '隔离测试中的人工建议，不宣称已取得基线增益。',
                'confidence': 'low',
                'falsifier': '若受控案例中不能识别对象同一性与变化，此建议应下调。',
            }],
        }

    def test_provisional_grading_record_shape(self):
        document = copy.deepcopy(self.baseline)
        proposal = self.proposal_batch()
        document['grade_proposals'] = [proposal]
        process = self.run_catalog(document, 'valid-provisional-grading')
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(json.loads(process.stdout)['proposed_grades'], 1)
        table = self.run_catalog(document, 'render-provisional-catalog', ['--render-catalog'])
        self.assertEqual(table.returncode, 0, table.stdout + table.stderr)
        self.assertIn('| `gongfa-compositional-description` | 组合描述模型 | 解释型 | 玄阶初级 |', table.stdout)
        self.assertIn('所选初评批次：`test-initial-grading`', table.stdout)
        self.assertIn('| `gongfa-network-effects` | 网络效应 | 解释型 | 本批未初评 |', table.stdout)
        for label in ('bad-grade', 'null-type', 'bad-type', 'unknown-target', 'unknown-policy',
                      'wrong-content-digest', 'duplicate-target', 'duplicate-batch',
                      'missing-task', 'missing-reason', 'missing-falsifier', 'fake-rated',
                      'fake-experiment', 'missing-history', 'history-cycle', 'history-scope'):
            with self.subTest(label=label):
                damaged = copy.deepcopy(document)
                batch = damaged['grade_proposals'][0]
                item = batch['items'][0]
                if label == 'bad-grade': item['grade_id'] = 'sheng-initial'
                elif label == 'null-type': item['ontology_type'] = None
                elif label == 'bad-type': item['ontology_type'] = 'software-artifact'
                elif label == 'unknown-target': item['gongfa_id'] = 'unknown-gongfa'
                elif label == 'unknown-policy': batch['policy_id'] = 'unknown-policy'
                elif label == 'wrong-content-digest': item['content_sha256'] = '0' * 64
                elif label == 'duplicate-target': batch['items'].append(copy.deepcopy(item))
                elif label == 'duplicate-batch': damaged['grade_proposals'].append(copy.deepcopy(batch))
                elif label == 'missing-task': item['task_family'] = ''
                elif label == 'missing-reason': item['reason'] = ''
                elif label == 'missing-falsifier': item['falsifier'] = ''
                elif label == 'fake-rated': batch['status'] = 'rated'
                elif label == 'fake-experiment': batch['basis'] = 'experimental_result'
                elif label == 'missing-history': batch['supersedes'] = 'missing-batch'
                else:
                    previous = copy.deepcopy(batch)
                    previous['id'] = 'older-test-grading'
                    damaged['grade_proposals'].append(previous)
                    batch['supersedes'] = previous['id']
                    if label == 'history-cycle': previous['supersedes'] = batch['id']
                    else: previous['application_context'] = '另一应用范围'
                process = self.run_catalog(damaged, label)
                self.assertNotEqual(process.returncode, 0, process.stdout + process.stderr)
        repeated = copy.deepcopy(proposal)
        repeated['id'] = 'corrected-test-grading'
        repeated['supersedes'] = proposal['id']
        document['grade_proposals'].append(repeated)
        self.assertEqual(self.run_catalog(document, 'valid-grading-correction').returncode, 0)
        self.assertNotEqual(self.run_catalog(document, 'ambiguous-catalog', ['--render-catalog']).returncode, 0)
        explicit = self.run_catalog(document, 'explicit-catalog',
                                    ['--render-catalog', '--proposal-batch', proposal['id']])
        self.assertEqual(explicit.returncode, 0, explicit.stdout + explicit.stderr)

    def assessment(self, status='unrated'):
        entry = self.baseline['gongfa'][0]
        policy = self.baseline['policies'][0]
        return {
            'id': 'test-assessment', 'gongfa_id': entry['id'],
            'content_version': entry['content_version'],
            'vocabulary_id': 'gongfa-grade-vocabulary-v1',
            'policy_id': policy['id'], 'policy_version': policy['version'],
            'status': status, 'grade_id': None, 'scope': None, 'evidence_refs': [],
            'reason': '隔离测试：尚无可用判级结果', 'assessor': 'test-fixture',
            'assessed_at': '2026-10-07T00:00:00Z', 'supersedes': None,
        }

    def test_supported_non_rating_changes(self):
        for label in ('rename', 'new-policy-version', 'unrated', 'undetermined'):
            with self.subTest(label=label):
                document = copy.deepcopy(self.baseline)
                if label == 'rename':
                    document['gongfa'][0]['name'] = '同一内容的展示名称'
                elif label == 'new-policy-version':
                    policy = copy.deepcopy(document['policies'][0])
                    policy['version'] = '0.2.0'
                    document['policies'].append(policy)
                else:
                    document['assessments'].append(self.assessment(label))
                process = self.run_catalog(document, label)
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_isolated_rating_record_shape(self):
        # 只验证合成记录的协议形态；这不是本库功法的实际效果证据。
        document = copy.deepcopy(self.baseline)
        references = {}
        for role in ('task-set', 'baseline', 'conditions', 'criteria', 'evidence'):
            relative = 'metadata/gongfa/test-' + role + '.json'
            payload = json.dumps({'fixture_role': role}).encode()
            (self.fixture / relative).write_bytes(payload)
            references[role] = {'path': relative, 'sha256': hashlib.sha256(payload).hexdigest()}
        policy = document['policies'][0]
        policy.update(status='defined', unresolved=[], evaluation_contract={
            'task_set_ref': references['task-set'], 'baseline_ref': references['baseline'],
            'conditions_ref': references['conditions'], 'criteria_ref': references['criteria'],
        })
        assessment = self.assessment()
        assessment.update(status='rated', grade_id='huang-initial', evidence_refs=[references['evidence']],
                          scope={key: value for key, value in policy['evaluation_contract'].items()
                                 if key != 'criteria_ref'})
        document['assessments'] = [assessment]
        process = self.run_catalog(document, 'isolated-rated-shape')
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        for label in ('no-evidence', 'no-scope', 'undefined-contract', 'missing-policy-rule',
                      'bad-evidence-digest', 'scope-mismatch', 'unresolved-defined-policy',
                      'draft-policy'):
            with self.subTest(label=label):
                damaged = copy.deepcopy(document)
                record, damaged_policy = damaged['assessments'][0], damaged['policies'][0]
                if label == 'no-evidence':
                    record['evidence_refs'] = []
                elif label == 'no-scope':
                    record['scope'] = None
                elif label == 'undefined-contract':
                    damaged_policy['evaluation_contract'] = None
                elif label == 'missing-policy-rule':
                    damaged_policy['rules'].pop()
                elif label == 'bad-evidence-digest':
                    record['evidence_refs'][0]['sha256'] = '0' * 64
                elif label == 'scope-mismatch':
                    record['scope']['baseline_ref'] = references['conditions']
                elif label == 'unresolved-defined-policy':
                    damaged_policy['unresolved'] = ['还没固定阈值']
                elif label == 'draft-policy':
                    damaged_policy['status'] = 'draft'
                process = self.run_catalog(damaged, label)
                self.assertNotEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_reject_invalid_catalogs(self):
        labels = [
            'tier-order', 'level-order', 'missing-grade', 'extra-tier', 'wrong-tier-level',
            'duplicate-content-version', 'unknown-source', 'bad-anchor', 'bad-text',
            'bad-text-digest', 'bad-snapshot-digest', 'missing-entry', 'default-grade',
            'path-traversal', 'unknown-policy', 'unknown-content-version',
            'unrated-with-grade', 'draft-rated', 'unknown-field', 'self-supersedes',
            'wrong-superseded-target', 'duplicate-policy-version', 'bad-captured-at',
            'predecessor-self', 'predecessor-missing', 'correction-cycle', 'correction-fork',
            'grade-as-type', 'non-content-type',
        ]
        for label in labels:
            with self.subTest(label=label):
                document = copy.deepcopy(self.baseline)
                tiers, entry = document['vocabulary']['tiers'], document['gongfa'][0]
                if label == 'tier-order':
                    tiers[0], tiers[1] = tiers[1], tiers[0]
                elif label == 'level-order':
                    tiers[0]['levels'][0], tiers[0]['levels'][1] = tiers[0]['levels'][1], tiers[0]['levels'][0]
                elif label == 'missing-grade':
                    tiers[0]['levels'].pop()
                elif label == 'extra-tier':
                    tiers.append(copy.deepcopy(tiers[-1]))
                elif label == 'wrong-tier-level':
                    tiers[0]['levels'][0]['id'] = 'tian-initial'
                elif label == 'duplicate-content-version':
                    document['gongfa'].append(copy.deepcopy(entry))
                elif label == 'unknown-source':
                    entry['source_ref']['source_id'] = 'missing-source'
                elif label == 'bad-anchor':
                    entry['source_ref']['heading_id'] = 'missing-anchor'
                elif label == 'bad-text':
                    entry['content']['original_text'] += '篡改原文'
                    entry['content']['text_sha256'] = hashlib.sha256(entry['content']['original_text'].encode()).hexdigest()
                elif label == 'bad-text-digest':
                    entry['content']['text_sha256'] = '0' * 64
                elif label == 'bad-snapshot-digest':
                    document['sources'][0]['snapshot_sha256'] = '0' * 64
                elif label == 'missing-entry':
                    document['gongfa'].pop()
                elif label == 'default-grade':
                    entry['grade_id'] = 'huang-initial'
                elif label == 'path-traversal':
                    document['sources'][0]['snapshot_path'] = '../outside.txt'
                elif label == 'unknown-field':
                    entry['permanent_power'] = 100
                elif label in ('grade-as-type', 'non-content-type'):
                    entry['ontology_type'] = 'huang-initial' if label == 'grade-as-type' else 'software-artifact'
                elif label == 'duplicate-policy-version':
                    document['policies'].append(copy.deepcopy(document['policies'][0]))
                elif label == 'bad-captured-at':
                    document['sources'][0]['captured_at'] = '2026-10-07T00:00:00'
                elif label.startswith('predecessor-'):
                    entry['predecessor_version'] = 'r1' if label == 'predecessor-self' else 'r999'
                elif label.startswith('correction-'):
                    first, second = self.assessment(), self.assessment()
                    second['id'] = 'second-assessment'
                    second['supersedes'] = first['id']
                    document['assessments'] = [first, second]
                    if label == 'correction-cycle':
                        first['supersedes'] = second['id']
                    else:
                        third = self.assessment()
                        third['id'], third['supersedes'] = 'third-assessment', first['id']
                        document['assessments'].append(third)
                else:
                    assessment = self.assessment()
                    document['assessments'].append(assessment)
                    if label == 'unknown-policy':
                        assessment['policy_id'] = 'missing-policy'
                    elif label == 'unknown-content-version':
                        assessment['content_version'] = 'r999'
                    elif label == 'unrated-with-grade':
                        assessment['grade_id'] = 'huang-initial'
                    elif label == 'draft-rated':
                        assessment.update(status='rated', grade_id='tian-advanced')
                    elif label == 'self-supersedes':
                        assessment['supersedes'] = assessment['id']
                    elif label == 'wrong-superseded-target':
                        other = self.assessment()
                        other['id'] = 'other-assessment'
                        other['gongfa_id'] = document['gongfa'][1]['id']
                        document['assessments'].append(other)
                        assessment['supersedes'] = other['id']
                process = self.run_catalog(document, label)
                self.assertNotEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_reject_non_json_and_changed_snapshot(self):
        for label, text in [('duplicate-key', '{"schema_version":"1.0.0","schema_version":"1.0.0"}'),
                            ('nan', '{"value":NaN}')]:
            with self.subTest(label=label):
                path = ARTIFACTS / (label + '.json')
                path.write_text(text)
                self.assertNotEqual(self.run_path(path, ARTIFACTS / label).returncode, 0)
        source = self.baseline['sources'][0]
        snapshot = self.fixture / source['snapshot_path']
        original = snapshot.read_bytes()
        try:
            snapshot.write_bytes(original + b' changed')
            self.assertNotEqual(self.run_catalog(self.baseline, 'changed-snapshot').returncode, 0)
        finally:
            snapshot.write_bytes(original)
        readme = self.fixture / 'metadata/gongfa/README.md'
        original_view = readme.read_text()
        try:
            readme.write_text(original_view.replace('| 黄阶初级 |', '| 黄阶最低档 |'))
            self.assertNotEqual(self.run_catalog(self.baseline, 'changed-grade-view').returncode, 0)
            repair = self.run_catalog(self.baseline, 'render-view-repair', ['--render-grades'])
            self.assertEqual(repair.returncode, 0, repair.stdout + repair.stderr)
            self.assertIn('| `huang-initial` | 黄阶初级 | 黄阶 | 初级 | 1 |', repair.stdout)
            self.assertIn('| `tian-advanced` | 天阶高级 | 天阶 | 高级 | 12 |', repair.stdout)
        finally:
            readme.write_text(original_view)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path)
    args = parser.parse_args()
    ARTIFACTS = args.artifacts or Path(tempfile.mkdtemp(prefix='gongfa-test-'))
    if args.artifacts:
        ARTIFACTS.mkdir(parents=True, exist_ok=False)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GongfaProtocolTest)
    test_names = [test.id() for test in suite]
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
               'success': result.wasSuccessful(), 'artifacts': str(ARTIFACTS)}
    (ARTIFACTS / 'result.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    xml = ET.Element('testsuite', name='gongfa-cli', tests=str(result.testsRun),
                     failures=str(len(result.failures)), errors=str(len(result.errors)))
    for name in test_names:
        node = ET.SubElement(xml, 'testcase', name=name)
        for test, traceback in result.failures + result.errors:
            if test.id().startswith(name):
                ET.SubElement(node, 'failure', message=str(test)).text = traceback
    ET.ElementTree(xml).write(ARTIFACTS / 'junit.xml', encoding='utf-8', xml_declaration=True)
    print(json.dumps(summary, ensure_ascii=False))
    sys.exit(0 if result.wasSuccessful() else 1)
