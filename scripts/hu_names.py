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



def apply_fuveszkonyv(plants, fk):
    """Király G. (szerk.): Új magyar füvészkönyv — the botanical authority, parsed from OCR text into
    {"Genus species": [name, clean]}; clean = every word recurs in the book (OCR spelling check)."""
    book = {key(k): v for k, v in fk.items()}
    st = dict(confirmed=0, replaced=0, filled=0, suggested=0, course_disagree=[])
    for p in plants:
        hit = book.get(key(p["latin"]))
        if not hit:
            continue
        name, clean = hit
        if p["hu"] and not p.get("verify"):  # course sheet or already checked: never touched
            if not same(name, p["hu"]) and not any(same(name, a) for a in p["aliases"]) and clean and "src" not in p:
                st["course_disagree"].append(f"{p['latin']}: tanfolyami lista = {p['hu']} | Füvészkönyv = {name}")
            continue
        alt = p.setdefault("alt", [])
        if p["hu"] and same(p["hu"], name):
            st["confirmed"] += 1
            p["src"] = "Wikidata/iNaturalist + Új magyar füvészkönyv egyezik"
            p.pop("verify", None)
        elif clean:
            if p["hu"]:
                st["replaced"] += 1
                alt.append(f"{p['hu']} (Wikidata/iNaturalist)")
            else:
                st["filled"] += 1
            p["hu"], p["src"] = name, "Új magyar füvészkönyv"
            p.pop("verify", None)
        else:  # OCR spelling doubtful: offer, don't apply
            st["suggested"] += 1
            if f"{name} (Füvészkönyv, OCR)" not in alt:
                alt.append(f"{name} (Füvészkönyv, OCR)")
        p["alt"] = [a for a in alt if not same(a.rsplit(" (", 1)[0], p["hu"])]
        if not p["alt"]:
            del p["alt"]
    return st


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
    if sys.argv[1] == "--fuveszkonyv":  # python scripts/hu_names.py --fuveszkonyv fk.json
        plants = json.loads(DATA.read_text(encoding="utf-8"))
        st = apply_fuveszkonyv(plants, json.load(open(sys.argv[2], encoding="utf-8")))
        DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps({k: (v if k != "course_disagree" else len(v)) for k, v in st.items()}, ensure_ascii=False))
        print("\n".join(st["course_disagree"]))
    else:
        main(*sys.argv[1:3])
