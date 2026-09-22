#!/usr/bin/env python3
import csv,json,re
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"dist"
required=["makes-models.csv","engines.csv","catalog.json","bulgaria-makes.csv","variants.csv"]
missing=[x for x in required if not (p/x).exists()]
if missing: raise SystemExit("missing: "+", ".join(missing))
with (p/"makes-models.csv").open(encoding="utf-8") as f:
    models=list(csv.DictReader(f))
assert models and all(x.get("make") and x.get("model") for x in models)
with (p/"engines.csv").open(encoding="utf-8") as f:
    engines=list(csv.DictReader(f))
assert engines
j=json.loads((p/"catalog.json").read_text(encoding="utf-8"))
assert j["market"]=="BG"
assert j["pickerHierarchy"]==["make","model","variant"]
bad=[]
for make in j["makes"]:
    for model in make["models"]:
        for v in model.get("variants",[]):
            n=v["name"]
            if re.fullmatch(r"\d{4}",n) or re.search(r"\(\d{4}\)",n):
                bad.append((make["name"],model["name"],n))
if bad: raise SystemExit("year/generation leaked into variants: "+repr(bad[:20]))
print(f"OK: {len(models)} model rows, {len(engines)} engine rows, {len(j['makes'])} makes; picker=make>model>variant")
