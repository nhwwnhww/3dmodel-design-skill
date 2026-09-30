"""Check externally measured numeric invariants. Does not measure a model."""
import argparse
import json
import math
from pathlib import Path

def evaluate(data):
    checks=data.get('checks')
    if not isinstance(checks,list) or not checks: raise ValueError('nonempty checks list required')
    results=[]
    for c in checks:
        if not isinstance(c,dict): raise ValueError('each check must be an object')
        for key in ('name','unit','method','source_revision'):
            if not isinstance(c.get(key),str) or not c[key].strip(): raise ValueError('missing '+key)
        values=[c.get(k) for k in ('actual','min','max')]
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in values):
            raise ValueError('actual/min/max must be finite numbers')
        actual,low,high=values
        if low>high: raise ValueError('min exceeds max')
        results.append({'name':c['name'],'passed':low<=actual<=high,'actual':actual,'unit':c['unit']})
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);a=p.parse_args()
    try:
        result=evaluate(json.loads(a.input.read_text(encoding='utf-8-sig')))
        print(json.dumps({'status':'numeric_records_checked','checks':result,'limitation':'Measured inputs are user supplied, not independently verified.'},indent=2))
        return 0 if all(x['passed'] for x in result) else 1
    except (OSError,ValueError,TypeError,AttributeError) as exc:
        print(json.dumps({'status':'input_error','error':str(exc)}));return 2
if __name__=='__main__': raise SystemExit(main())
