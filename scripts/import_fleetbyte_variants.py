#!/usr/bin/env python3
"""Import verified Make -> Model -> Variant names from FleetByte Catalog.
Run manually to refresh data/fleetbyte-variants.csv. The API is public and
rate-limited; this script checkpoints after every model and resumes safely.
"""
import csv,json,time,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"fleetbyte-variants.csv"
BASE="https://fleetcatalog.disturbingbyte.pt/v1"
FIELDS=["make","model","variant","sort_order","source","verified"]

def get(path,params=None):
    url=BASE+path
    if params: url+="?"+urllib.parse.urlencode(params)
    while True:
        try:
            with urllib.request.urlopen(url,timeout=30) as r: return json.load(r)
        except Exception as e:
            print("retry",url,e); time.sleep(65)

def pages(path,params=None):
    page=1
    while True:
        p=dict(params or {}); p.update(page=page,pageSize=100)
        d=get(path,p); items=d.get("items",[])
        yield from items
        if page*100>=d.get("total",len(items)): break
        page+=1

rows={}
if OUT.exists():
    with OUT.open(encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f): rows[(r["make"].casefold(),r["model"].casefold(),r["variant"].casefold())]=r

def save():
    with OUT.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        w.writerows(sorted(rows.values(),key=lambda r:(r["make"].casefold(),r["model"].casefold(),r["variant"].casefold())))

for make in pages("/makes"):
    make_name=make["name"].strip()
    for model in pages(f'/makes/{make["id"]}/models'):
        model_name=model["name"].strip()
        for i,v in enumerate(pages(f'/models/{model["id"]}/variants'),1):
            name=(v.get("name") or v.get("trim") or "").strip()
            if not name: continue
            row={"make":make_name,"model":model_name,"variant":name,"sort_order":str(i*10),"source":"fleetbyte-catalog","verified":"true"}
            rows[(make_name.casefold(),model_name.casefold(),name.casefold())]=row
        save()
        time.sleep(1.05)
print("saved",len(rows),"verified variants to",OUT)
