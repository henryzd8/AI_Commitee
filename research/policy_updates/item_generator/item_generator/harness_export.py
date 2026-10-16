"""Explicit adapter to the task-3 Item schema; preserve raw generator files."""
from collections import defaultdict
from hashlib import sha256
from .catalog import get_family

SPLITS={'screening':'screen','exploration':'explore','manipulation':'manip','validation':'calib','confirmatory':'confirm'}


def export(probes,histories):
    grouped=defaultdict(list)
    seen=set()
    for row in histories:
        if row['item_id'] in seen: raise ValueError('duplicate history item')
        seen.add(row['item_id'])
        grouped[row['probe_item_id']].append(row)
    if len({r['item_id'] for r in probes})!=len(probes): raise ValueError('duplicate probe')
    def convert(row,split,role):
        return {'item_id':row['item_id'],'family_id':row['family_id'],'role':role,
                'split':SPLITS[split], 'seed':int.from_bytes(sha256(str(row['seed']).encode()).digest()[:4],'big'),
                'index':row['instance_index'],'text':row['problem'],
                'steps':[{'name':k,'value':v} for k,v in row['intermediate_values'].items()],
                'final_answer':row['final_answer'],'paraphrase_id':row['paraphrase_id'] if role=='probe' else None,
                'history_item_ids':[], 'heldout_family':get_family(row['family_id']).heldout}
    out_probes,out_histories=[],[]
    used=set()
    for probe in probes:
        source=probe.get('original_item_id',probe['item_id'])
        hs=sorted(grouped[source],key=lambda h:h['history_turn'])
        if [h['history_turn'] for h in hs]!=[1,2,3,4]: raise ValueError('exactly four distinct history turns required')
        if any(h['family_id']!=probe['family_id'] or h['kind']!='history' for h in hs): raise ValueError('history family/role mismatch')
        if source in used: raise ValueError('multiple probes share a history source')
        used.add(source)
        p=convert(probe,probe['split'],'probe'); p['history_item_ids']=[h['item_id'] for h in hs]
        out_probes.append(p)
        out_histories.extend(convert(h,probe['split'],'history') for h in hs)
    if set(grouped)!=used: raise ValueError('unexpected orphan history items')
    return out_probes,out_histories
