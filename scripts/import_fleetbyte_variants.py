#!/usr/bin/env python3
"""Import Make -> Model -> commercial Variant records from FleetByte Catalog."""
import csv,json,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"fleetbyte-variants.csv"
BASE="https://fleetcatalog.disturbingbyte.pt/v1"
FIELDS=["make","model","variant","sort_order","source","verified"]
UA="VtoraCatalog/1.0 (+https://github.com/ankaroni/avtoracardata)"

def get(path,params=None):
    url=BASE+path
    if params: url+="?"+urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code==429:
                time.sleep(65); continue
            if 400<=e.code<500: raise
            time.sleep(min(2**attempt,30))
        except (urllib.error.URLError,TimeoutError):
            time.sleep(min(2**attempt,30))
    raise RuntimeError(f"API unavailable after retries: {url}")

def pages(path,params=None):
    page=1
    while True:
        p=dict(params or {}); p.update(page=page,pageSize=100)
        d=get(path,p)
        items=d.get("items")
        if not isinstance(items,list): raise ValueError(f"Unexpected response for {path}: {d}")
        yield from items
        total=int(d.get("total",len(items)))
        if page*100>=total: break
        page+=1

rows={}
if OUT.exists():
    with OUT.open(encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            rows[(r["make"].casefold(),r["model"].casefold(),r["variant"].casefold())]=r

def save():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        w.writerows(sorted(rows.values(),key=lambda r:(r["make"].casefold(),r["model"].casefold(),int(r["sort_order"] or 999999),r["variant"].casefold())))

for make in pages("/makes"):
    make_name=str(make.get("name","")).strip()
    make_id=make.get("id")
    if not make_name or not make_id: continue
    for model in pages(f"/makes/{make_id}/models"):
        model_name=str(model.get("name","")).strip()
        model_id=model.get("id")
        if not model_name or not model_id: continue
        for i,v in enumerate(pages(f"/models/{model_id}/variants"),1):
            # API records are approved public catalog entries; name is the display variant.
            name=str(v.get("name") or "").strip()
            if not name: continue
            row={"make":make_name,"model":model_name,"variant":name,"sort_order":str(i*10),"source":"fleetbyte-catalog","verified":"true"}
            rows[(make_name.casefold(),model_name.casefold(),name.casefold())]=row
        save()
        time.sleep(1.05)
print(f"saved {len(rows)} verified variants to {OUT}")
