#!/usr/bin/env python3
import csv,json,sys
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"dist"
required=["makes-models.csv","engines.csv","catalog.json","bulgaria-makes.csv"]
missing=[x for x in required if not (p/x).exists()]
if missing: raise SystemExit("missing: "+", ".join(missing))
with (p/"makes-models.csv").open(encoding="utf-8") as f:
 r=list(csv.DictReader(f))
 assert r and all(x.get("make") and x.get("model") for x in r)
with (p/"engines.csv").open(encoding="utf-8") as f:
 e=list(csv.DictReader(f))
 assert e and all(x.get("make") and x.get("model") and x.get("generation") for x in e)
j=json.loads((p/"catalog.json").read_text(encoding="utf-8"))
assert j["market"]=="BG" and j["makes"]
print(f"OK: {len(r)} models, {len(e)} engines, {len(j['makes'])} makes")
