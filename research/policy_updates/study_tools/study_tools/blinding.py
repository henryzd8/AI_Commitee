"""Organizational blinding, not encryption. Never send the key to prompt tuners."""
import secrets
import hashlib
import json

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def blind(records):
    public,private=[],[]
    seen=set()
    for row in records:
        original=row['response_id']
        if original in seen: raise ValueError('duplicate response_id')
        seen.add(original)
        opaque=secrets.token_hex(16)
        # Whitelist only; arbitrary metadata can otherwise leak condition/model.
        public.append({'request_id':opaque,'problem':row['problem'],'response':row['response']})
        private.append({'request_id':opaque,'record':row,'public_hash':digest(public[-1])})
    secrets.SystemRandom().shuffle(public)
    return public, {'schema':'blinding-v0','key':private,
                    'warning':'private coordinator/independent analyst only; responses may reveal condition'}


def restore(public,manifest):
    key={r['request_id']:r for r in manifest['key']}
    ids=[r['request_id'] for r in public]
    if len(set(ids))!=len(ids) or set(ids)!=set(key): raise ValueError('missing/duplicate/unknown request IDs')
    rows=[]
    for r in public:
        entry=key[r['request_id']]
        if digest(r)!=entry['public_hash']: raise ValueError('public content edited')
        rows.append(entry['record'])
    return rows
