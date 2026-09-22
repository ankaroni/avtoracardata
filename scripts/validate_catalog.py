#!/usr/bin/env python3
import csv,json,re
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"dist"
required=["makes-models.csv","engines.csv","catalog.json","bulgaria-makes.csv","variants.csv"]
for n in required:
    assert (p/n).exists(),f"missing {n}"
with (p/"catalog.json").open(encoding="utf-8") as f: j=json.load(f)
assert j["market"]=="BG"
assert j["pickerHierarchy"]==["make","model","variant"]
seen_models=set(); bad=[]; variant_count=0; covered_models=0
for make in j["makes"]:
    for model in make["models"]:
        mk=(make["name"].casefold(),model["name"].casefold())
        assert mk not in seen_models,f"duplicate model: {make['name']} / {model['name']}"
        seen_models.add(mk)
        variants=model.get("variants",[])
        if variants: covered_models+=1
        names=set()
        for x in variants:
            n=x["name"].strip(); variant_count+=1
            key=n.casefold()
            assert key not in names,f"duplicate variant: {make['name']} / {model['name']} / {n}"
            names.add(key)
            if re.fullmatch(r"\d{4}",n) or re.search(r"\(\d{4}\)",n): bad.append((make["name"],model["name"],n))
if bad: raise AssertionError(f"year-like public variants: {bad[:20]}")
report={"makes":len(j["makes"]),"models":len(seen_models),"modelsWithVariants":covered_models,"variants":variant_count,"variantCoveragePct":round(covered_models*100/len(seen_models),2) if seen_models else 0}
(p/"coverage.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report))
