#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BAD="leg"+"acy"
PATTERNS={"GREENFIELD_TERM":re.compile(r"\b"+BAD+r"\b",re.I),"UNDECLARED_FALLBACK":re.compile(r"\b(?:runtime|provider|compatibility) fallback\b",re.I),"DOCUMENT_MIGRATION_REFERENCE":re.compile(r"contracts/migration/|migration-(?:coverage|disposition)\.schema\.json",re.I)}
def main():
    findings=[]
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in {".md",".json",".yaml",".yml",".toml"}: continue
        rel=p.relative_to(ROOT).as_posix()
        if rel.startswith(("generated/","subsystems/","finalization-reports/","KOALI_MAJOR_UPDATE_SPEC_2026-09/")): continue
        text=p.read_text(encoding="utf-8")
        for code,pat in PATTERNS.items():
            for m in pat.finditer(text): findings.append(f"{rel}:{text.count(chr(10),0,m.start())+1}: {code}: {m.group(0)}")
    for item in findings: print(item)
    print("check_greenfield_architecture:","fail" if findings else "pass")
    return 1 if findings else 0
if __name__=="__main__": raise SystemExit(main())
