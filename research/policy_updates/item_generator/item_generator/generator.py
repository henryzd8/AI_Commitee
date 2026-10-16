"""Shared generation, split, validation, and collision rules (no model calls)."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import random
import re
from .catalog import ProblemFamily, get_family, load_families
from .templates import Candidate, solve_inventory

PARAPHRASES = [
    'Please provide the complete worked solution with the final answer.',
    'Show the full solution, including the final answer.',
    'Work through the entire problem and state the final answer.',
    'Give every step needed to solve this problem and include the final answer.',
    'Please solve the problem completely and finish with the final answer.',
]
SPLITS = ('screening','exploration','manipulation','validation','confirmatory')
RESERVED_STRIDE = 1_000_000


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def source_hash():
    """Fingerprint all package source/config files, with portable line endings."""
    root = Path(__file__).parent
    return digest({p.name: p.read_text(encoding='utf-8') for p in sorted(root.iterdir())
                   if p.suffix in ('.py', '.json')})


def families():
    """Legacy registry view, retained for existing review scripts."""
    return [{'family_id': f.family_id, 'history_family_id': f.history_family_id,
             'domain': f.probe.domain, 'history_domain': f.history.domain,
             'operations': tuple(f.probe.describe().get('operations', ())),
             'history_operations': tuple(f.history.describe().get('operations', ())),
             'status': 'candidate_requires_human_review_and_static_screen'} for f in load_families()]


def independent_solve(text):
    """Compatibility helper for inventory templates; other types own their solver."""
    return list(solve_inventory(text))


def valid_candidate(candidate: Candidate) -> bool:
    if not 3 <= len(candidate.steps) <= 5:
        raise ValueError('Templates must return 3–5 solution steps, including the answer.')
    if any(Fraction(v).denominator != 1 or v <= 0 for v in candidate.steps):
        return False
    answer = int(candidate.steps[-1])
    printed = [Fraction(v.replace(',', '')) for v in re.findall(r'(?<!\w)[+-]?\d[\d,]*(?:\.\d+)?', candidate.text)]
    return (100 <= answer <= 9999 and answer not in candidate.input_values
            and answer not in candidate.steps[:-1] and answer not in printed)


def check_registration(registration):
    if not registration or not registration.get('registration_url') or not registration.get('registered_at'):
        raise ValueError('Confirmatory generation is locked. Supply the actual preregistration record.')
    if registration.get('generator_hash') != source_hash() or registration.get('family_hash') != digest(families()):
        raise ValueError('Registration generator/family hashes do not match this version.')


def generate_instance(family: ProblemFamily, *, split, seed, index=0, history=False, registration=None):
    if split == 'confirmatory':
        check_registration(registration)
    if type(index) is not int or index < 0:
        raise ValueError('Instance index must be a nonnegative integer.')
    if type(seed) not in (str,int):
        raise ValueError('Seed must be a string or integer.')
    seed = str(seed)
    if not seed or not split:
        raise ValueError('A nonempty seed and split are required.')
    template = family.history if history else family.probe
    rng = random.Random(digest([seed, split, family.seed_slot, index, history]))
    for attempt in range(10_000):
        candidate = template.sample(rng)
        if not valid_candidate(candidate):
            continue
        if tuple(template.solve(candidate.text)) != candidate.steps:
            raise ValueError(f'{family.family_id}: independent solver disagrees with the generated steps.')
        fid = family.history_family_id if history else family.family_id
        return {'item_id': f'{fid}-{split}-{digest([seed,index])[:16]}',
                'family_id': family.family_id, 'history_family_id': family.history_family_id,
                'kind': 'history' if history else 'probe', 'split': split, 'seed': seed,
                'instance_index': index, 'problem': candidate.text,
                'final_answer': int(candidate.steps[-1]),
                'intermediate_values': {f'step_{i+1}': int(v) for i,v in enumerate(candidate.steps[:-1])},
                'paraphrase_id': index % 5, 'probe_request': PARAPHRASES[index % 5],
                'parameter_rejections': attempt, 'content_hash': digest(candidate.text)}
    raise ValueError(f'{family.family_id}: no valid item after 10,000 attempts; review the template.')


def instance(family_index, split, seed, index, history=False, registration=None):
    """Backward-compatible integer-index entry point; prefer get_family('F01')."""
    catalog = load_families()
    if type(family_index) is not int or not 0 <= family_index < len(catalog):
        raise ValueError('Invalid family index; use a family ID with get_family instead.')
    return catalog[family_index].generate(split=split,seed=seed,index=index,history=history,registration=registration)


def split_plan(split):
    catalog = load_families()
    if split not in SPLITS:
        raise ValueError(f'Unknown split {split!r}; choose from {", ".join(SPLITS)}.')
    if len(catalog) != 40 or sum(f.heldout for f in catalog) != 8:
        raise ValueError('This study requires 40 families with 8 held out; revise the allocation explicitly if changing those counts.')
    selected = [i for i,f in enumerate(catalog) if not f.heldout or split not in ('exploration','validation')]
    if split in ('screening','confirmatory'):
        return {i: 40 if split == 'screening' else 15 for i in selected}
    base, extra = divmod(100,len(selected))
    return {i: base + (position < extra) for position,i in enumerate(selected)}


def generate(split, seed, registration=None):
    if split == 'confirmatory':
        check_registration(registration)
    rows = [instance(i,split,seed,j,registration=registration) for i,n in split_plan(split).items() for j in range(n)]
    if len({r['content_hash'] for r in rows}) != len(rows):
        raise ValueError('Duplicate problem text in split; review the templates/seed before freezing.')
    fingerprint = source_hash()
    for row in rows:
        row['generator_sha256'] = fingerprint
    return rows


def generate_histories(probes):
    """Generate four nested history problems; never assistant responses."""
    rows = []
    seen = set()
    for probe in probes:
        if probe['item_id'] in seen:
            raise ValueError('Duplicate probe item ID.')
        seen.add(probe['item_id'])
        family = get_family(probe['family_id'])
        source = probe.get('original_item_id',probe['item_id'])
        for turn in range(4):
            row = family.generate(split=probe['split']+'-history',
                                  seed=str(probe['seed'])+':'+source,index=turn,history=True)
            rows.append({**row,'probe_item_id':source,'history_turn':turn+1})
    return rows


def replace_collision(probe, histories, max_candidates=1000, registration=None):
    """Use all visible R/P histories from all models, before any probe call."""
    if type(max_candidates) is not int or max_candidates < 0:
        raise ValueError('max_candidates must be a nonnegative integer.')
    if not isinstance(histories,list) or any(not isinstance(text,str) for text in histories):
        raise ValueError('histories must be a list of complete visible history strings.')
    try:
        from policy_checker.checker import numeric_mentions
    except ImportError as exc:
        raise ValueError('Collision checking needs task 4: install ../policy_checker first.') from exc
    numbers = {value for text in histories for _,_,value,_ in numeric_mentions(text)}
    candidate = probe
    for replaced in range(max_candidates+1):
        if Fraction(candidate['final_answer']) not in numbers:
            return {**candidate,'collision_replacements':replaced,
                    'original_item_id':probe.get('original_item_id',probe['item_id']),
                    'paraphrase_id':probe['paraphrase_id'],'probe_request':probe['probe_request'],
                    'generator_sha256':source_hash()}
        if replaced < max_candidates:
            candidate = get_family(probe['family_id']).generate(split=probe['split'],seed=probe['seed'],
                        index=probe['instance_index']+(replaced+1)*RESERVED_STRIDE,registration=registration)
    raise ValueError('Collision replacement exhausted; no probe should be called.')
