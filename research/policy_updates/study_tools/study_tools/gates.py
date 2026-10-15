"""Development gate definitions. Choices missing from the plan are explicit."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import json
import math
from scipy.stats import beta, t
from .statistics import cr2, paired_vectors


def load_config(path=None):
    raw = Path(path or Path(__file__).with_name('gates_v0.json')).read_bytes()
    return json.loads(raw), sha256(raw).hexdigest()


def binomial_bound(k,n,alpha,upper=False):
    if not 0 <= k <= n or n <= 0: raise ValueError('invalid binomial counts')
    if upper: return 1. if k==n else float(beta.ppf(1-alpha,k+1,n-k))
    return 0. if k==0 else float(beta.ppf(alpha,k,n-k+1))


def family_screen(records, models, config):
    """Static records: family_id,item_id,model_id,policy (R/P),given.

    One frozen screening frame only; 40 matched items/model/policy/family.
    Pooled bound = average simultaneous per-model CP lower bounds. Valid without
    pretending repeated outputs on the same items are independent across models.
    """
    table = defaultdict(dict)
    for r in records:
        if r['model_id'] not in models or r['policy'] not in ('R','P') or r['given'] not in (0,1):
            raise ValueError('invalid screening row')
        key = (r['family_id'],r['policy'],r['model_id'])
        if r['item_id'] in table[key]: raise ValueError('duplicate screen item')
        table[key][r['item_id']] = int(r['given']) if r['policy']=='P' else 1-int(r['given'])
    if not table: raise ValueError('empty screen')
    output = {}
    for family in sorted({k[0] for k in table}):
        details = {}
        reference = None
        for policy in ('R','P'):
            lower, upper = [], {}
            for model in models:
                rows = table[family,policy,model]
                if len(rows)!=40: raise ValueError('screen requires 40 matched items per family/model/policy')
                if reference is None: reference=set(rows)
                if set(rows)!=reference: raise ValueError('screen items must match across policies/models')
                k,n = sum(rows.values()),len(rows)
                lower.append(binomial_bound(k,n,config['family_lower_alpha']/len(models)))
                upper[model] = binomial_bound(k,n,config['model_upper_alpha'],True)
            pooled = sum(lower)/len(lower)
            details[policy] = {'pooled_lower':pooled,'model_upper':upper,
                               'pass':pooled>=config['family_pooled_lower'] and all(v>=config['model_upper_threshold'] for v in upper.values())}
        output[family] = {'policies':details,'pass':all(d['pass'] for d in details.values())}
    return {'families':output,'pass':all(v['pass'] for v in output.values()),
            'method':'mean of simultaneous per-model exact lower bounds; marginal model upper bounds'}


def manipulation(records, models, config):
    table = {}
    for r in records:
        key=(r['model_id'],r['channel'],r['item_id'],r['policy'])
        if key in table or r['given'] not in (0,1) or r['policy'] not in ('R','P'):
            raise ValueError('invalid/duplicate manipulation row')
        if r['model_id'] not in models or r['channel'] not in ('C3','C4'): raise ValueError('unexpected model/channel')
        table[key]=r
    out = {}
    for model in models:
        checks = {}
        for channel in ('C3','C4'):
            items=sorted({k[2] for k in table if k[:2]==(model,channel)})
            if len(items)!=100: raise ValueError('manipulation check requires 100 paired items')
            values,clusters=[],[]
            for item in items:
                try: p,r=table[model,channel,item,'P'],table[model,channel,item,'R']
                except KeyError as exc: raise ValueError('missing manipulation pair') from exc
                if p['family_id']!=r['family_id']: raise ValueError('family mismatch')
                values.append(p['given']-r['given']); clusters.append(p['family_id'])
            alpha=config['manipulation_lower_alpha']
            try:
                result=cr2(values,clusters)
                lower=result['estimate']-t.ppf(1-alpha,result['df'])*result['se']
                method='family CR2 lower one-sided bound'
            except ValueError:
                # Bounded independent-family fallback, also handles perfect separation.
                sizes=[clusters.count(g)/len(clusters) for g in set(clusters)]
                if len(sizes)<3: raise ValueError('too few manipulation families')
                lower=sum(values)/len(values)-math.sqrt(2*sum(w*w for w in sizes)*math.log(1/alpha))
                method='conservative family Hoeffding lower bound (degenerate variance)'
            checks[channel]={'lower':float(lower),'pass':bool(lower>=config['manipulation_lower_threshold']),'method':method}
        out[model]={'channels':checks,'eligible':all(c['pass'] for c in checks.values())}
    return out


def label_gate(report, config):
    if report.get('status')!='complete': return False
    overall=report.get('overall',{}); kappas=report.get('kappa_pre_adjudication',{})
    pairs=[(overall.get('given_sensitivity'),config['given_sensitivity']),
           (overall.get('given_specificity'),config['given_specificity']),
           (overall.get('refuse_proxy_agreement'),config['refusal_agreement']),
           (kappas.get('human_given'),config['kappa']),(kappas.get('human_refusal'),config['kappa'])]
    return all(v is not None and math.isfinite(v) and v>=cut for v,cut in pairs) and report.get('checks',{}).get('complete_overlap_binary_ratings') is True


def pilot(records,models,config):
    vectors,clusters=paired_vectors(records,models)
    futile=[]
    for name in ('H1-L','H1-T'):
        try: result=cr2(vectors[name],clusters)
        except ValueError: return 'PASS' # Insufficient evidence of futility, not efficacy.
        upper=result['estimate']+t.ppf(1-config['pilot_upper_alpha'],result['df'])*result['se']
        futile.append(result['estimate']<config['pilot_estimate_threshold'] and upper<config['pilot_upper_threshold'])
    return 'FAIL' if all(futile) else 'PASS'
