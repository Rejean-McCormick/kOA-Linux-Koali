#!/usr/bin/env python3
from __future__ import annotations
import json
from _contract_first import ROOT,metadata,source_files

def main():
 errors=[];seen={}
 for p in source_files("*.md"):
  raw=p.read_bytes()
  if b"\r" in raw:errors.append(f"{p}: CR line endings remain")
  m=metadata(p)
  if not m:errors.append(f"{p}: metadata block missing or invalid");continue
  did=m.get("doc_id")
  if not isinstance(did,str) or not did:errors.append(f"{p}: doc_id missing")
  elif did in seen:errors.append(f"{p}: duplicate doc_id {did}")
  else:seen[did]=p
 for p in sorted((ROOT/"generated").glob("*.json")):
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except Exception as e:errors.append(f"{p}: invalid JSON: {e}");continue
  if d.get("generated") is not True:errors.append(f"{p}: generated marker missing")
 for p in sorted((ROOT/"generated").glob("*.md")):
  text=p.read_text(encoding="utf-8")
  lines=text.splitlines()
  heading_first=bool(lines and lines[0].startswith("# "))
  generated_marker_then_heading=bool(
   len(lines)>=3
   and lines[0].startswith("<!-- KOA:GENERATED ")
   and lines[1]==""
   and lines[2].startswith("# ")
  )
  if not (heading_first or generated_marker_then_heading):
   errors.append(f"{p}: generated Markdown heading missing")
 for e in errors:print("FAIL:",e)
 print("check_generated_blocks:","fail" if errors else "pass")
 return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
