"""Read-only evidence integrity checker; does NOT verify physical truth or file semantics."""
import argparse
import hashlib
import json
import math
from pathlib import Path

REQUIRED = {
    'build': (['command', 'tool_versions'], ['build_log', 'model']),
    'visual': (['views', 'sections', 'findings'], ['views', 'sections']),
    'dfam': (['orientation', 'supports', 'walls', 'material_basis'], ['report']),
    'slice': (['slicer', 'version', 'profile', 'warnings', 'layer_review'], ['project_3mf', 'preview']),
    'prototype': (['printer', 'material', 'observations', 'feedback'], ['report', 'photo']),
    'release': (['license', 'originality', 'limitations'], ['listing', 'instructions']),
    'assembly': (['fit_table', 'motion_path'], ['report']),
}
VIEWS = {'front', 'back', 'left', 'right', 'top', 'bottom', 'iso'}

def present(value):
    if isinstance(value, str):
        return bool(value.strip()) and value.strip().lower() not in {'unknown','pending','tbc','todo'}
    return bool(value)

def input_digest(manifest):
    """Bind evidence to inputs, declared configuration, and behavior requirements."""
    data = {k: manifest.get(k) for k in ('inputs','profile','behavioral_claims','assembly_required')}
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def checked_file(root, relative, expected):
    if not isinstance(relative,str) or not relative or Path(relative).is_absolute():
        raise ValueError('artifact/input path must be project-relative')
    base=Path(root).resolve(); path=(base/relative).resolve()
    if not path.is_relative_to(base):
        raise ValueError('path escapes project root: '+relative)
    if not path.is_file(): raise ValueError('missing file: '+relative)
    if path.stat().st_size == 0: raise ValueError('empty file: '+relative)
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected: raise ValueError('SHA256 mismatch: '+relative)

def validate(manifest, root, only=None):
    """Return blockers; complete records are not automatic engineering approval."""
    errors=[]
    if not isinstance(manifest,dict): return ['manifest must be an object']
    if manifest.get('schema_version') != 1: errors.append('schema_version must be 1')
    if not present(manifest.get('revision')): errors.append('revision missing')
    profile=manifest.get('profile',{})
    if not isinstance(profile,dict): return errors+['profile must be an object']
    for key in ('printer','nozzle_mm','material','plate','layer_height_mm'):
        if not present(profile.get(key)): errors.append('profile missing '+key)
    for key in ('nozzle_mm','layer_height_mm'):
        val=profile.get(key)
        if isinstance(val,bool) or not isinstance(val,(int,float)) or not math.isfinite(val) or val<=0:
            errors.append('profile '+key+' must be a positive finite number')
    if not isinstance(manifest.get('assembly_required'),bool): errors.append('assembly_required must be boolean')
    claims=manifest.get('behavioral_claims')
    if not isinstance(claims,list) or any(not isinstance(c,str) or not present(c) for c in claims):
        errors.append('behavioral_claims must be a list of nonempty strings')
    inputs=manifest.get('inputs')
    if not isinstance(inputs,dict) or not inputs: return errors+['inputs must be a nonempty path-to-SHA256 map']
    for path,sha in inputs.items():
        try: checked_file(root,path,sha)
        except (ValueError,OSError) as exc: errors.append(str(exc))
    try: digest=input_digest(manifest)
    except (ValueError,TypeError): return errors+['manifest contains non-JSON or non-finite values']
    gates=manifest.get('gates')
    if not isinstance(gates,dict): return errors+['gates must be an object']
    needed = list(only) if only else ['build','visual','dfam','slice','prototype','release']
    if only is None and (manifest.get('assembly_required') or claims): needed.append('assembly')
    for name in needed:
        gate=gates.get(name)
        if not isinstance(gate,dict): errors.append(name+': missing gate');continue
        if gate.get('status')!='passed': errors.append(name+': not passed')
        if not present(gate.get('reviewer')): errors.append(name+': reviewer missing')
        if gate.get('revision')!=manifest.get('revision'): errors.append(name+': stale revision')
        if gate.get('input_digest')!=digest: errors.append(name+': stale input/config digest')
        details=gate.get('details',{})
        if not isinstance(details,dict): errors.append(name+': invalid details');details={}
        keys,roles=REQUIRED[name]
        for key in keys:
            if not present(details.get(key)): errors.append(name+': missing detail '+key)
        if name=='visual':
            views=details.get('views')
            if not isinstance(views,list) or any(not isinstance(v,str) for v in views) or not VIEWS.issubset(set(views)):
                errors.append('visual: all seven views required')
            sections=details.get('sections')
            if not isinstance(sections,list) or len(sections)<2 or any(not isinstance(s,str) or not present(s) for s in sections):
                errors.append('visual: two described critical sections required')
        if name=='slice' and details.get('slicer')!='Bambu Studio': errors.append('slice: Bambu Studio required')
        if name=='prototype' and isinstance(claims,list) and claims:
            behavior=details.get('behavior_tests',{})
            if not isinstance(behavior,dict): behavior={}
            for claim in claims:
                if isinstance(claim,str) and not present(behavior.get(claim)):
                    errors.append('prototype: missing physical behavior test '+claim)
        artifacts=gate.get('artifacts')
        if not isinstance(artifacts,list): artifacts=[]
        found=set()
        for entry in artifacts:
            if not isinstance(entry,dict): errors.append(name+': invalid artifact entry');continue
            role=entry.get('role')
            if isinstance(role,str): found.add(role)
            try: checked_file(root,entry.get('path'),entry.get('sha256'))
            except (ValueError,OSError) as exc: errors.append(name+': '+str(exc))
        for role in roles:
            if role not in found: errors.append(name+': missing artifact role '+role)
    return errors

def main(only=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--digest',action='store_true',help='Print declared input digest only; does not validate evidence')
    args=parser.parse_args()
    try:
        manifest=json.loads(args.manifest.read_text(encoding='utf-8-sig'))
        if args.digest:
            print(input_digest(manifest)); return 0
        errors=validate(manifest,args.manifest.parent,only)
    except (OSError,ValueError,TypeError,AttributeError) as exc:
        print(json.dumps({'status':'input_error','error':str(exc)}));return 2
    print(json.dumps({'status':'blocked' if errors else 'evidence_records_complete',
        'scope':list(only) if only else 'release', 'blockers':errors,
        'limitation':'Integrity and completeness only; no image, geometry, slicing, physical truth, license or platform approval.'},ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
