"""SCAFFOLD ONLY: Multi-view and section capture. No integration implemented."""
import argparse
import json

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract',action='store_true',help='Show future input/output contract')
    args=parser.parse_args()
    report={'status':'not_implemented','tool':"shoot.py",'contract':"Future adapter: local model + units + seven cameras + two named cut planes -> PNGs and model-hash metadata. Needs tested Playwright/Chromium viewer or Blender integration. Must await model load, detect blank/error frames, bind local server to loopback, and require actual image review. Manual fallback: export and inspect CAD/Blender screenshots."}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 2
if __name__=='__main__': raise SystemExit(main())
