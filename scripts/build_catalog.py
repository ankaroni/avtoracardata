#!/usr/bin/env python3
import csv,json,re,urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/"dist"; DIST.mkdir(exist_ok=True)
BASE="https://raw.githubusercontent.com/gor3a/vehicle-makes-models/main/data/csv/"
FILES=["makes-models.csv","engines.csv"]

# Current Bulgarian used-car marketplace priority. This affects sorting only; no makes are deleted.
BG_PRIORITY=[
"Mercedes-Benz","BMW","Audi","Volkswagen","Toyota","Hyundai","Peugeot","Opel","Kia","Ford",
"Skoda","Renault","Citroen","Honda","Nissan","Volvo","Dacia","Mazda","Land Rover","Jeep",
"Fiat","Lexus","Mitsubishi","Seat","Suzuki","Porsche","Chevrolet","Alfa Romeo","Mini",
"Subaru","Tesla","Cupra","Jaguar","Infiniti","Dodge","SsangYong","KGM","Great Wall","Haval",
"BYD","MG","Smart"
]
ALIASES={"VW":"Volkswagen","Mercedes Benz":"Mercedes-Benz","Mercedes":"Mercedes-Benz","Citroën":"Citroen","Škoda":"Skoda"}

REPLACEMENTS=[
(r"\bBenzin\b","Petrol"),(r"\bOttomotor\b","Petrol"),(r"\bDieselkraftstoff\b","Diesel"),
(r"\bDieselmotor\b","Diesel"),(r"\bElektro\b","Electric"),(r"\bElektromotor\b","Electric"),
(r"\bPlug[- ]?in[- ]?Hybrid\b","Plug-in Hybrid"),(r"\bVollhybrid\b","Hybrid"),
(r"\bErdgas\b","CNG"),(r"\bAutogas\b","LPG"),
(r"\bSchaltgetriebe\b","Manual"),(r"\bAutomatikgetriebe\b","Automatic"),
(r"\bAutomatik\b","Automatic"),(r"\bAllradantrieb\b","AWD"),
(r"\bVorderradantrieb\b","FWD"),(r"\bHinterradantrieb\b","RWD"),
(r"\bKombilimousine\b","Hatchback"),(r"\bKombi\b","Estate/Wagon"),
(r"\bLimousine\b","Sedan"),(r"\bGeländewagen\b","SUV"),
(r"\bCabriolet\b","Convertible"),(r"\bKleinbus\b","Minibus"),
(r"\bKastenwagen\b","Van"),(r"\bPritsche\b","Pickup")
]
def clean(v):
    if v is None:return ""
    v=" ".join(str(v).strip().split())
    for pat,to in REPLACEMENTS:v=re.sub(pat,to,v,flags=re.I)
    return v

def dl(name):
    p=DIST/("_raw_"+name)
    urllib.request.urlretrieve(BASE+name,p)
    return p

def norm_make(v): return ALIASES.get(clean(v),clean(v))

def normalize_csv(name):
    src=dl(name); out=DIST/name
    with src.open(encoding="utf-8-sig",newline="") as f, out.open("w",encoding="utf-8",newline="") as g:
        r=csv.DictReader(f); fields=list(r.fieldnames or [])
        if "make" in fields:
            fields += ["market","market_priority"]
        w=csv.DictWriter(g,fieldnames=fields); w.writeheader()
        for row in r:
            row={k:clean(v) for k,v in row.items()}
            if "make" in row:
                row["make"]=norm_make(row["make"])
                try: rank=BG_PRIORITY.index(row["make"])+1
                except ValueError: rank=999
                row["market"]="BG" if rank<999 else "GLOBAL"
                row["market_priority"]=rank
            w.writerow(row)
    src.unlink(missing_ok=True)

def build_catalog():
    rows=[]
    with (DIST/"makes-models.csv").open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    rows.sort(key=lambda r:(int(r.get("market_priority") or 999),r["make"].lower(),r["model"].lower()))
    makes={}
    for r in rows:
        m=makes.setdefault(r["make"],{"name":r["make"],"market":r["market"],"priority":int(r["market_priority"]),"models":[]})
        m["models"].append({"name":r["model"],"yearFrom":int(r["year_start"]) if r.get("year_start","").isdigit() else None,
                            "yearTo":int(r["year_end"]) if r.get("year_end","").isdigit() else None})
    (DIST/"catalog.json").write_text(json.dumps({"market":"BG","makes":list(makes.values())},ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    with (DIST/"bulgaria-makes.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["priority","make"])
        for i,m in enumerate(BG_PRIORITY,1):w.writerow([i,m])

for fn in FILES: normalize_csv(fn)
build_catalog()
print("Vtora vehicle catalog generated.")
