#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
from typing import Any,Iterator
ROOT=Path(__file__).resolve().parents[1]
META_RE=re.compile(r"\A<!-- KOA:DOC-META:BEGIN GENERATED\n(.*?)\nKOA:DOC-META:END -->",re.S)
EXCLUDED=("generated/","subsystems/","finalization-reports/","KOALI_MAJOR_UPDATE_SPEC_2026-09/")
# Export inventory is not an authored normative document. Exact filename only.
EXPORT_ARTIFACTS={"CODE_SNAPSHOT_MANIFEST.md"}
def rel(p:Path)->str:return p.relative_to(ROOT).as_posix()
def load(path:str|Path)->Any:return json.loads((ROOT/path).read_text(encoding="utf-8"))
def records(path:str)->list[dict[str,Any]]:
 d=load(path)
 if isinstance(d,dict):
  value=d.get("records",[])
  return value if isinstance(value,list) else []
 return []
def source_files(pattern:str)->Iterator[Path]:
 for p in sorted(ROOT.rglob(pattern),key=lambda x:x.as_posix().casefold()):
  r=rel(p)
  if p.is_file() and not r.startswith(EXCLUDED) and r not in EXPORT_ARTIFACTS:yield p
def metadata(p:Path)->dict[str,Any]|None:
 m=META_RE.match(p.read_text(encoding="utf-8"))
 if not m:return None
 try:
  d=json.loads(m.group(1));return d if isinstance(d,dict) else None
 except Exception:return None
def local_ref_exists(base:Path,ref:str)->bool:
 target=ref.split("#",1)[0]
 if not target or "://" in target or target.startswith("urn:"):return True
 p=(base.parent/target).resolve() if target.startswith((".","..")) else (ROOT/target).resolve()
 try:p.relative_to(ROOT.resolve())
 except ValueError:return False
 return p.exists()
def walk(value:Any,path:str="$" ):
 yield path,value
 if isinstance(value,dict):
  for k,v in value.items():yield from walk(v,f"{path}.{k}")
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from walk(v,f"{path}[{i}]")
