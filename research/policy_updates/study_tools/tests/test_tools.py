import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np
from scipy.stats import ttest_1samp
from study_tools import statistics as st, gates, blinding, simulation

class StatisticsTests(unittest.TestCase):

    def test_cr2_dense_matrix_reference_unbalanced(self):
        x = np.array([1, 0, 2, 1, 3, 1, 0, 1, 4.0], float)
        clusters = ['a'] * 2 + ['b'] * 3 + ['c'] * 4
        n = len(x)
        residual = x - x.mean()
        M = np.eye(n) - np.ones((n, n)) / n
        variance = 0.0
        Q = np.zeros((n, n))
        for group in sorted(set(clusters)):
            idx = np.flatnonzero(np.array(clusters) == group)
            block = M[np.ix_(idx, idx)]
            eig, vec = np.linalg.eigh(block)
            A = vec * eig ** (-0.5) @ vec.T
            variance += (np.ones(len(idx)) @ A @ residual[idx]) ** 2 / n ** 2
            z = M[:, idx] @ A @ np.ones(len(idx))
            Q += np.outer(z, z)
        result = st.cr2(x, clusters)
        self.assertAlmostEqual(result['se'] ** 2, variance)
        self.assertAlmostEqual(result['df'], np.trace(Q) ** 2 / np.trace(Q @ Q))

    def test_balanced_matches_family_mean_t_test(self):
        x = np.array([0, 1, 1, 2, 2, 4, 5, 7.0])
        clusters = ['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd']
        r = st.cr2(x, clusters)
        self.assertAlmostEqual(r['df'], 3)
        expected = ttest_1samp(x.reshape(4, 2).mean(axis=1), 0)
        self.assertAlmostEqual(st.pvalue(r, alternative='two-sided'), expected.pvalue)

    def test_holm_known_values(self):
        self.assertEqual(st.holm({'a': 0.01, 'b': 0.04, 'c': 0.03}), {'a': 0.03, 'c': 0.06, 'b': 0.06})

    def test_actual_full_grid_direction_and_signs(self):
        rows, models = simulation.synthetic(14, items_per_family=3)
        vectors, clusters = st.paired_vectors(rows, models)
        self.assertEqual(len(clusters), 120)
        report = st.analyze(rows, models, gates.load_config()[0], bootstrap_reps=100)
        self.assertEqual(set(report['tests']), set(st.PRIMARY + ['H7a-L', 'H7a-T', 'H7b']))
        self.assertAlmostEqual(report['tests']['H6']['estimate'], np.mean(vectors['H6']))
        changed = copy.deepcopy(rows)
        for r in changed:
            c = (r['condition'], r['history_type'], r['remedy'])
            if c in st.CELLS[:2]:
                r['condition'], r['history_type'], r['remedy'] = st.CELLS[1 - st.CELLS.index(c)]
        swapped, _ = st.paired_vectors(changed, models)
        np.testing.assert_allclose(swapped['H1-L'], -np.array(vectors['H1-L']))

    def test_reject_missing_duplicate_truncated_wrong_model(self):
        rows, models = simulation.synthetic(3, items_per_family=1)
        for bad in (rows[:-1], rows + [rows[0]]):
            with self.assertRaises(ValueError):
                st.paired_vectors(bad, models)
        changed = copy.deepcopy(rows)
        changed[0]['truncated'] = True
        with self.assertRaises(ValueError):
            st.paired_vectors(changed, models)
        with self.assertRaises(ValueError):
            st.paired_vectors(rows, models + ['missing'])

    def test_zero_variance_not_significant(self):
        with self.assertRaises(ValueError):
            st.cr2([0] * 6, ['a', 'a', 'b', 'b', 'c', 'c'])

    def test_whole_missing_item_detected_against_manifest(self):
        rows, models = simulation.synthetic(5, items_per_family=1)
        planned = list({r['item_id']: {'item_id': r['item_id'], 'family_id': r['family_id']} for r in rows}.values())
        partial = [r for r in rows if r['item_id'] != planned[0]['item_id']]
        with self.assertRaises(ValueError):
            st.analyze(partial, models, gates.load_config()[0], expected_items=planned)

    def test_noninferiority_and_tost_boundaries(self):
        r = {'estimate': 0.03, 'se': 0.01, 'df': 39}
        self.assertEqual(st.pvalue(r, 0.03, 'less'), 0.5)
        r['estimate'] = 0
        self.assertLess(max(st.pvalue(r, -0.05, 'greater'), st.pvalue(r, 0.05, 'less')), 0.01)

class WorkflowTests(unittest.TestCase):

    def test_existing_checker_to_analysis_contract(self):
        from policy_checker.checker import Checker
        checker = Checker()
        rows, models = simulation.synthetic(9, families=4, items_per_family=1)
        scored = []
        for index, row in enumerate(rows):
            item = {'problem': 'Start with 200. Add 100. Add 200.', 'final_answer': 500, 'intermediate_values': {'step_1': 300}}
            given = bool(row['y']) if row['direction'] == 'tighten' else not bool(row['y'])
            raw = {**item, **row, 'response_id': str(index), 'response': f"Final answer: {item['final_answer']}" if given else 'Consider the relevant operations.', 'finish_reason': 'stop'}
            scored.append(checker.score(raw))
        vectors, _ = st.paired_vectors(scored, models)
        expected, _ = st.paired_vectors(rows, models)
        np.testing.assert_allclose(vectors['H1-L'], expected['H1-L'])
        np.testing.assert_allclose(vectors['H1-T'], expected['H1-T'])

    def test_blinding_no_metadata_leak_and_roundtrip(self):
        rows = [{'response_id': 'revealing-SWITCH', 'problem': 'P', 'response': 'R', 'condition': 'SWITCH', 'model_id': 'M', 'scoring': {'y': 1}}]
        public, key = blinding.blind(rows)
        self.assertEqual(set(public[0]), {'request_id', 'problem', 'response'})
        self.assertEqual(blinding.restore(public, key), rows)
        public[0]['response'] = 'edited'
        with self.assertRaises(ValueError):
            blinding.restore(public, key)

    def test_screen_perfect_pass_bad_model_fail(self):
        config, _ = gates.load_config()
        models = ['M1', 'M2', 'M3', 'M4']
        rows = [{'family_id': 'F1', 'item_id': str(i), 'model_id': m, 'policy': p, 'given': int(p == 'P')} for m in models for p in ('R', 'P') for i in range(40)]
        self.assertTrue(gates.family_screen(rows, models, config)['pass'])
        for r in rows:
            if r['model_id'] == 'M4':
                r['given'] = 1 - r['given']
        self.assertFalse(gates.family_screen(rows, models, config)['pass'])

    def test_label_gate_requires_actual_complete_metrics(self):
        config, _ = gates.load_config()
        self.assertFalse(gates.label_gate({'gate_pass': True}, config))
        r = {'status': 'complete', 'overall': {'given_sensitivity': 0.9, 'given_specificity': 0.9, 'refuse_proxy_agreement': 0.85}, 'kappa_pre_adjudication': {'human_given': 0.8, 'human_refusal': 0.8}, 'checks': {'complete_overlap_binary_ratings': True}}
        self.assertTrue(gates.label_gate(r, config))

    def test_manipulation_complete_separation_and_missing(self):
        rows = [{'model_id': 'M', 'channel': c, 'item_id': str(i), 'family_id': f'F{i % 40}', 'policy': p, 'given': int(p == 'P')} for c in ('C3', 'C4') for i in range(100) for p in ('P', 'R')]
        self.assertTrue(gates.manipulation(rows, ['M'], gates.load_config()[0])['M']['eligible'])
        with self.assertRaises(ValueError):
            gates.manipulation(rows[:-1], ['M'], gates.load_config()[0])
        for row in rows:
            if row['policy'] == 'P' and int(row['item_id']) % 11 == 0:
                row['given'] = 0
        json.dumps(gates.manipulation(rows, ['M'], gates.load_config()[0]), allow_nan=False)

    def test_cli_pilot_only_boolean(self):
        with tempfile.TemporaryDirectory() as temp:
            rows, models = simulation.synthetic(11, items_per_family=1, effect=0)
            input_path = Path(temp) / 'synthetic.jsonl'
            input_path.write_text('\n'.join((json.dumps(r) for r in rows)))
            result = subprocess.run([sys.executable, '-m', 'study_tools', 'pilot', str(input_path), '--models', *models], check=True, capture_output=True, text=True)
            self.assertIn(result.stdout.strip(), ['PASS', 'FAIL'])
            self.assertEqual(len(result.stdout.splitlines()), 1)
if __name__ == '__main__':
    unittest.main()
