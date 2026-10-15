"""Assumption-driven correlated Bernoulli dry runs, not empirical power claims."""
import numpy as np
from scipy.special import expit, logit
from scipy.stats import beta
from .statistics import CELLS, analyze


def synthetic(seed=1, families=40, items_per_family=15, effect=.05, baseline=.10,
              family_sd=.7, item_sd=1.2, family_slope_sd=.4, model_slope_sd=.3,
              coupling=.5, shuffle=False):
    if not 0<baseline<1 or not 0<=coupling<=1 or effect<0: raise ValueError('invalid simulation assumptions')
    rng=np.random.default_rng(seed)
    models=[f'M{i}' for i in range(4)]
    model_slopes=rng.normal(0,model_slope_sd,4)
    rows=[]
    for family in range(families):
        intercept=rng.normal(0,family_sd); slope=rng.normal(0,family_slope_sd)
        for item in range(items_per_family):
            item_shift=rng.normal(0,item_sd)
            for m,model in enumerate(models):
                for channel in ('C3','C4'):
                    for direction in ('loosen','tighten'):
                        p=float(expit(logit(baseline)+intercept+item_shift))
                        # Positive heterogeneous risk difference; achieved RD is reported.
                        increase=effect*np.exp(slope+model_slopes[m])
                        probabilities=np.clip([p+increase,p,p,p,p],0,1)
                        shared=rng.random(); independent=rng.random(5)
                        u=np.where(rng.random(5)<coupling,shared,independent)
                        ys=(u<probabilities).astype(int)
                        # Coherent refusal subset in tightening; not semantic refusal.
                        refusal=(rng.random(5)<.10)&(ys==0) if direction=='tighten' else (rng.random(5)<.10)&(ys==1)
                        if shuffle:
                            order=rng.permutation(5); ys=ys[order]; refusal=refusal[order]
                        for c,cell in enumerate(CELLS):
                            rows.append({'item_id':f'F{family}-I{item}','family_id':f'F{family}',
                                         'model_id':model,'channel':channel,'direction':direction,
                                         'condition':cell[0],'history_type':cell[1],'remedy':cell[2],
                                         'y':int(ys[c]),'refuse_proxy':int(refusal[c]),'truncated':False})
    return rows,models


def power(config,repetitions=100,seed=2026,**assumptions):
    if repetitions<2: raise ValueError('at least two repetitions required')
    successes={name:0 for name in ('H1-L','H1-T','H3-L','H3-T','H6','harm_joint','any_primary')}
    effects=[]; invalid=0
    for i in range(repetitions):
        rows,models=synthetic(seed+i,**assumptions)
        try: report=analyze(rows,models,config,bootstrap_reps=0)
        except ValueError: invalid+=1; continue
        for name in successes:
            if name=='harm_joint': success=report['harm_gate_pass']
            elif name=='any_primary': success=any(report['tests'][k]['reject'] for k in ('H1-L','H1-T','H3-L','H3-T','H6'))
            else: success=report['tests'][name]['reject']
            successes[name]+=int(success)
        effects.append(report['tests']['H1-L']['estimate'])
    valid=repetitions-invalid
    return {'assumptions':assumptions,'repetitions':repetitions,'invalid_replicates':invalid,
            'rates':{k:{'estimate':v/valid if valid else None,
                        'monte_carlo_se':float(np.sqrt((v/valid)*(1-v/valid)/valid)) if valid else None,
                        'monte_carlo_ci95':([0. if v==0 else float(beta.ppf(.025,v,valid-v+1)),
                                             1. if v==valid else float(beta.ppf(.975,v+1,valid-v))] if valid else None)} for k,v in successes.items()},
            'achieved_mean_H1_L':float(np.mean(effects)) if effects else None,
            'note':'Planning assumptions only. Requested effect is a heterogeneous increment scale, not guaranteed marginal RD. Joint harm power is simulated, not multiplied.'}
