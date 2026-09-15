#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
META=re.compile(r"\A<!-- KOA:DOC-META:BEGIN GENERATED\n(.*?)\nKOA:DOC-META:END -->",re.S)
def main():
    failures=[]
    for p in sorted(ROOT.rglob("*.md")):
        rel=p.relative_to(ROOT).as_posix()
        if rel.startswith(("generated/","subsystems/","finalization-reports/","KOALI_MAJOR_UPDATE_SPEC_2026-09/")): continue
        text=p.read_text(encoding="utf-8"); m=META.match(text)
        if not m: continue
        try:d=json.loads(m.group(1))
        except Exception as e: failures.append(f"{rel}: invalid metadata: {e}"); continue
        if d.get("status") in {"active","accepted"} and d.get("language")!="en": failures.append(f"{rel}: active language is not en")
    for item in failures: print("FAIL:",item)
    print("check_language:","fail" if failures else "pass")
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
