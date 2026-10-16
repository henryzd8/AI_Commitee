import dataclasses
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from item_generator import get_family, ProblemFamily
from item_generator import generator as g
from item_generator.catalog import _parse_catalog, CATALOG_PATH
from item_generator.templates import Candidate, InventoryTemplate
from item_generator.workflow import prepare
from item_generator.harness_export import export


class UsabilityTests(unittest.TestCase):
    def test_legacy_400_sample_fingerprint_unchanged(self):
        fixture=json.loads(Path(__file__).with_name('legacy_fingerprint.json').read_text())
        rows=[]
        for i in range(40):
            for history in (False,True):
                for j in range(fixture['samples_per_family']):
                    row=g.instance(i,fixture['split'],fixture['seed'],j,history)
                    rows.append({k:row[k] for k in ('item_id','problem','final_answer','intermediate_values')})
        self.assertEqual(g.digest(rows),fixture['sha256'])

    def test_catalog_order_does_not_change_families_or_samples(self):
        raw=json.loads(CATALOG_PATH.read_text())
        forward=_parse_catalog(json.dumps(raw))
        backward=_parse_catalog(json.dumps(raw[::-1]))
        self.assertEqual([f.describe() for f in forward],[f.describe() for f in backward])
        self.assertEqual(forward[0].generate(seed='A'),backward[0].generate(seed='A'))

    def test_bad_catalog_and_family_ids_fail_helpfully(self):
        raw=json.loads(CATALOG_PATH.read_text())
        raw[1]['seed_slot']=raw[0]['seed_slot']
        with self.assertRaisesRegex(ValueError,'seed_slot'):
            _parse_catalog(json.dumps(raw))
        with self.assertRaisesRegex(ValueError,'Unknown probe family'):
            get_family('missing')
        with self.assertRaises(ValueError):InventoryTemplate('bad',('add','unknown','mul'))
        with self.assertRaises(ValueError):_parse_catalog('null')
        self.assertEqual(get_family('F01').generate(seed=42),get_family('F01').generate(seed='42'))

    def test_custom_branched_template_needs_no_engine_changes(self):
        class TicketTemplate:
            domain='ticket revenue'
            def sample(self,rng):
                a,b=rng.randint(20,30),rng.randint(10,15)
                # Two independent subtotals, then combined revenue, then a fee.
                return Candidate(f'{a} adult tickets at 12 and {b} child tickets at 7; subtract a fee of 9.',
                                 tuple(map(Fraction,(a*12,b*7,a*12+b*7,a*12+b*7-9))),(a,12,b,7,9))
            def solve(self,text):
                import re
                a,p,b,q,fee=map(int,re.findall(r'\d+',text))
                return tuple(map(Fraction,(a*p,b*q,a*p+b*q,a*p+b*q-fee)))
            def describe(self):return {'type':'tickets','domain':self.domain}
        family=ProblemFamily('T01','TH01',100,False,TicketTemplate(),get_family('F01').history)
        row=family.generate(seed='A')
        self.assertEqual(row['final_answer'],family.probe.solve(row['problem'])[-1])

    def test_wrong_independent_solver_fails_immediately(self):
        base=get_family('F01')
        class Broken:
            domain='broken'
            def sample(self,rng):return Candidate('Start with 10.',tuple(map(Fraction,(20,50,200))),(10,))
            def solve(self,text):return (20,50,201)
        with self.assertRaisesRegex(ValueError,'solver disagrees'):
            dataclasses.replace(base,probe=Broken()).generate(seed='A')

    def test_prepare_manifest_and_runner_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'run'
            self.assertEqual(prepare('exploration','A',out),(100,400))
            manifest=json.loads((out/'manifest.json').read_text())
            for name,expected in manifest['files'].items():
                self.assertEqual(sha256((out/name).read_bytes()).hexdigest(),expected)
            self.assertEqual(manifest['seed'],'A')
            self.assertIn('pending',manifest['collision_status'])
            original=(out/'probes.jsonl').read_bytes()
            with self.assertRaises(ValueError):prepare('exploration','B',out)
            self.assertEqual(original,(out/'probes.jsonl').read_bytes())

    def test_confirmation_guard_applies_to_family_and_prepare(self):
        with self.assertRaisesRegex(ValueError,'locked'):
            get_family('F01').generate(seed='A',split='confirmatory')
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'confirm'
            with self.assertRaises(ValueError):prepare('confirmatory','A',out)
            self.assertFalse(out.exists())

    def test_collision_repeat_keeps_original_history_link(self):
        probe=get_family('F01').generate(seed='A',split='exploration')
        histories=g.generate_histories([probe])
        replaced=g.replace_collision(probe,[str(probe['final_answer'])])
        again=g.replace_collision(replaced,[])
        self.assertEqual(again['original_item_id'],probe['item_id'])
        self.assertEqual(g.generate_histories([again]),histories)
        probes,hs=export([again],histories)
        self.assertEqual(probes[0]['history_item_ids'],[r['item_id'] for r in hs])

    def test_cli_preview_prepare_review_and_clear_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            def cli(*args):
                return subprocess.run([sys.executable,'-m','item_generator',*args],capture_output=True,text=True)
            preview=cli('preview','F01','--count','1')
            self.assertEqual(preview.returncode,0,preview.stderr)
            self.assertIn('Final answer:',preview.stdout)
            prepared=cli('prepare','exploration',str(root/'run'),'--seed','A')
            self.assertEqual(prepared.returncode,0,prepared.stderr)
            review=cli('review',str(root/'review.md'),'--samples','1')
            self.assertEqual(review.returncode,0,review.stderr)
            self.assertEqual((root/'review.md').read_text(encoding='utf-8').count('**Sample 1.**'),80)
            bad=cli('preview','bad-id')
            self.assertNotEqual(bad.returncode,0)
            self.assertIn('Unknown probe family',bad.stderr)
            self.assertNotIn('Traceback',bad.stderr)
            self.assertNotEqual(cli('preview','F01','--count','0').returncode,0)

    def test_nonpositive_preview_count_and_bad_json(self):
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/'bad.jsonl';file.write_text('{bad}\n')
            from item_generator.files import read_rows
            with self.assertRaisesRegex(ValueError,'line 1'):
                read_rows(file)
