"""Fill and cross-check official Hungarian names. Course-sheet names (no "verify" flag) are never changed.
Sources (parsed to local JSON files, not committed):
  - Maszlay B.: "Képes növénylista – Virágkötő OKJ 2021" (plantae.hu) — florist list, authoritative
  - TERRA Alapítvány: "Hazánk növényvilága" Latin index (terra.hu/haznov) — native flora, authoritative
Usage: python scripts/hu_names.py <maszlay.json> <terra.json>"""
import json, re, sys, time, unicodedata, urllib.parse
from enrich import DATA, candidates, get, looks_latin


def key(latin):
    """"Salix matsudana 'Tortuosa'" -> "salix matsudana|tortuosa"; a cultivar only matches the same cultivar."""
    cv = re.search(r"'([^']+)'?", latin)
    s = re.sub(r"'[^']*'?|\([^)]*\)|\b(x|×|sp|var|subsp)\b\.?", " ", latin.lower())
    return " ".join(s.split()[:2]) + ("|" + cv.group(1).lower().strip() if cv else "")


def clean(s):
    return re.sub(r"^\([^)]*\)\s*", "", s.strip())  # "(örökzöld) rákvirág" -> "rákvirág"


def same(a, b):
    f = lambda s: re.sub(r"[\s\-]", "", unicodedata.normalize("NFC", clean(s).lower()))
    return f(a) == f(b)



def main(maszlay_path, terra_path):
    lists = [("Maszlay: Virágkötő OKJ 2021 növénylista", {key(k): clean(v) for k, v in json.load(open(maszlay_path, encoding="utf-8")).items()}),
             ("TERRA: Hazánk növényvilága", {key(k): v[0].lower() + v[1:] for k, v in json.load(open(terra_path, encoding="utf-8")).items()})]
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    st = dict(filled_from_source=0, confirmed=0, differs_kept=0, still_verify=0, still_empty=0)
    disagree = []
    for n, p in enumerate(plants, 1):
        course = bool(p["hu"]) and not p.get("verify")
        # full name (incl. cultivar) only; candidates() would strip the cultivar and mis-assign
        hit = next(((src, d[key(p["latin"])]) for src, d in lists if key(p["latin"]) in d), None)
        if course:
            if hit and not same(hit[1], p["hu"]) and not any(same(hit[1], a) for a in p["aliases"]):
                disagree.append(f"{p['latin']}: tanfolyami lista = {p['hu']} | {hit[0].split(':')[0]} = {hit[1]}")
            continue
        # sources confirm, they never overwrite: Maszlay often uses short trade names ("nyírfa" for
        # "közönséges nyír") and TERRA an older style, while the exam wants the full botanical name
        if hit:
            src, name = hit
            short = src.split(":")[0]
            if not p["hu"]:
                st["filled_from_source"] += 1
                p["hu"], p["src"], p["verify"] = name, src, True
            elif same(p["hu"], name):
                st["confirmed"] += 1
                p["src"] = f"Wikidata/iNaturalist + {short} egyezik"
                p.pop("verify", None)
            else:
                st["differs_kept"] += 1
                alt = f"{name} ({short})"
                if alt not in p.get("alt", []):
                    p.setdefault("alt", []).append(alt)
        # ponytail: no fallback guessing; Wikipedia search returned wrong species ("banyán" for Ficus microcarpa)
        st["still_verify"] += bool(p.get("verify"))
        st["still_empty"] += not p["hu"]
        if n % 100 == 0:
            print(f"{n}/{len(plants)}", st, flush=True)
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(st, ensure_ascii=False))
    print(f"course-sheet names differing from a source ({len(disagree)}):")
    print("\n".join(disagree))


if __name__ == "__main__":
    main(*sys.argv[1:3])
