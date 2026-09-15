#!/usr/bin/env python3
from __future__ import annotations
import re
from _contract_first import ROOT
PATTERNS=[re.compile(r"<TBD>",re.I),re.compile(r"\b(?:TODO|FIXME):"),re.compile(r"\[\[UNRESOLVED\]\]",re.I)]
def main():
 errors=[]
 for p in sorted(ROOT.rglob("*"),key=lambda x:x.as_posix().casefold()):
  if not p.is_file() or p.suffix.lower() not in {".md",".json",".yaml",".yml",".toml"}:continue
  rel=p.relative_to(ROOT).as_posix()
  if rel.startswith(("generated/","subsystems/","finalization-reports/","KOALI_MAJOR_UPDATE_SPEC_2026-09/","00-governance/templates/")):continue
  try:text=p.read_text(encoding="utf-8")
  except UnicodeDecodeError:continue
  for pat in PATTERNS:
   m=pat.search(text)
   if m:errors.append(f"{rel}:{text.count(chr(10),0,m.start())+1}: unresolved marker {m.group(0)}")
 for e in errors:print("FAIL:",e)
 print("check_no_unresolved_state:","fail" if errors else "pass")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
