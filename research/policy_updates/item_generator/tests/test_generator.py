import unittest
from item_generator import generator as g

class GeneratorTests(unittest.TestCase):

    def test_eighty_candidate_families_replay_and_invariants(self):
        signatures = set()
        for f in g.families():
            self.assertNotEqual(f['domain'], f['history_domain'])
            self.assertNotEqual(f['operations'], f['history_operations'])
            signatures.update((f['operations'], f['history_operations']))
        self.assertEqual(len(signatures), 80)
        for family in range(40):
            for history in (False, True):
                for i in range(5):
                    item = g.instance(family, 'development-test', 'A', i, history)
                    self.assertEqual(g.independent_solve(item['problem'])[-1], item['final_answer'])
                    self.assertNotIn(item['final_answer'], item['intermediate_values'].values())
                    import re
                    self.assertNotIn(item['final_answer'], map(int, re.findall('\\d+', item['problem'])))
                    self.assertTrue(100 <= item['final_answer'] <= 9999)

    def test_split_sizes_disjoint_reproducible(self):
        seen = set()
        for split, n in [('screening', 1600), ('exploration', 100), ('manipulation', 100), ('validation', 100)]:
            items = g.generate(split, 'A')
            self.assertEqual(len(items), n)
            self.assertFalse(seen & {r['item_id'] for r in items})
            seen.update((r['item_id'] for r in items))
            if split in ('exploration', 'validation'):
                self.assertEqual(len({r['family_id'] for r in items}), 32)
            self.assertEqual(items, g.generate(split, 'A'))
        self.assertEqual(sum(g.split_plan('confirmatory').values()), 600)
        self.assertEqual(set(g.split_plan('confirmatory').values()), {15})

    def test_confirmation_locked_without_generating(self):
        with self.assertRaises(ValueError):
            g.generate('confirmatory', 'C')
        with self.assertRaises(ValueError):
            g.generate('confirmatory', 'C', {'registration_url': 'x', 'registered_at': 'x', 'generator_hash': 'wrong'})

    def test_collision_uses_values_not_offsets_preserves_paraphrase(self):
        p = g.instance(0, 'fake', 'A', 0)
        next_p = g.instance(0, 'fake', 'A', 1000000)
        result = g.replace_collision(p, [f"Final answer: {p['final_answer']}", f"Other model: {next_p['final_answer']}"])
        self.assertGreaterEqual(result['collision_replacements'], 2)
        self.assertEqual(result['probe_request'], p['probe_request'])
        self.assertEqual(g.replace_collision(p, ['No numbers here'])['item_id'], p['item_id'])
