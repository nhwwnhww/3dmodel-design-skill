"""AABB screening only. All bounds must already share an assembly frame in mm."""
import argparse
import itertools
import json
import math
from pathlib import Path

def bounds(value):
    if not isinstance(value,list) or len(value)!=2 or any(not isinstance(v,list) or len(v)!=3 for v in value):
        raise ValueError('bounds must be [[xmin,ymin,zmin],[xmax,ymax,zmax]]')
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for row in value for x in row):
        raise ValueError('bounds must be finite numeric coordinates')
    if any(value[0][i]>=value[1][i] for i in range(3)): raise ValueError('bounds require positive extent on every axis')
    return value

def screen(a,b):
    a,b=bounds(a),bounds(b)
    overlap=[min(a[1][i],b[1][i])-max(a[0][i],b[0][i]) for i in range(3)]
    state='disjoint' if min(overlap)<0 else ('possible_contact' if min(overlap)==0 else 'possible_overlap')
    return {'screen':state,'axis_overlap_mm':overlap}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);a=p.parse_args()
    try:
        data=json.loads(a.input.read_text(encoding='utf-8-sig'))
        if data.get('units')!='mm': raise ValueError('units must be mm')
        parts=data['parts']
        if not isinstance(parts,dict) or len(parts)<2: raise ValueError('at least two named parts required')
        for item in parts.values(): bounds(item)
        result=[{'parts':[x,y],**screen(parts[x],parts[y])} for x,y in itertools.combinations(parts,2)]
        print(json.dumps({'status':'screened_only','pairs':result,'limitation':'No exact collision, clearance, fit or motion verification.'},indent=2));return 0
    except (OSError,ValueError,TypeError,KeyError,AttributeError) as exc:
        print(json.dumps({'status':'input_error','error':str(exc)}));return 2
if __name__=='__main__': raise SystemExit(main())
