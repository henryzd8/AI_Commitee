"""One-call preparation for task 3; no model calls and no implicit confirmation."""
from .catalog import load_families
from .generator import generate, generate_histories, source_hash, digest, families
from .harness_export import export
from .files import write_bundle


def prepare(split, seed, directory, registration=None):
    from pathlib import Path
    if Path(directory).exists():
        raise ValueError('Output directory already exists; choose a new run name.')
    probes = generate(split,seed,registration)
    histories = generate_histories(probes)
    runner_probes, runner_histories = export(probes,histories)
    documents = {
        'probes.jsonl':(probes,True), 'histories.jsonl':(histories,True),
        'items.jsonl':(runner_probes,True), 'history_items.jsonl':(runner_histories,True),
        'families.json':([f.describe() for f in load_families()],False),
    }
    write_bundle(directory,documents,{
        'format_version':1,'split':split,'seed':str(seed),'probe_count':len(probes),
        'history_count':len(histories),'generator_hash':source_hash(),'family_hash':digest(families()),
        'registration':registration,
        'status':'development inputs; family approval and static screening pending',
        'collision_status':'pending model histories; check all R/P histories before probe calls',
    })
    return len(probes),len(histories)
