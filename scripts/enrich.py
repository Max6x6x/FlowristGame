"""Fill missing Hungarian names + images in data.json from Wikidata, fallback iNaturalist.
Only fills empty fields, never overwrites, so it is safe to re-run. Usage: python scripts/enrich.py"""
import hashlib, json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, IMG = ROOT / "data.json", ROOT / "images"
UA = {"User-Agent": "FlowristGame/1.0 (personal study app; github.com/Max6x6x/FlowristGame)"}


def get(url, data=None, tries=4):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            if t == tries - 1:
                raise
            time.sleep(3 * (t + 1))


def candidates(latin):
    """'Coleus scutellarioides (Solenostemon s.)' -> ['Coleus scutellarioides', 'Solenostemon s.', 'Coleus']"""
    s = re.sub(r"'[^']*'", "", latin)  # cultivar
    alts = re.findall(r"\(([^)]*)\)", s)
    s = re.sub(r"\([^)]*\)", "", s)
    parts = [p for p in re.split(r"\s*/\s*", s)] + alts
    out = []
    for p in parts:
        words = [w for w in p.split() if w not in ("sp.", "sp", "x", "×")]
        if not words or not words[0][:1].isupper():
            continue
        out.append(" ".join(words[:2]))
        if len(words) > 2 and words[2] in ("var.", "subsp.", "ssp.") and len(words) > 3:
            out.insert(len(out) - 1, " ".join(words[:4]))
    genera = [c.split()[0] for c in out]
    return list(dict.fromkeys(out + genera))


def wikidata(names):
    vals = " ".join(json.dumps(n) for n in names)
    q = f"""SELECT ?name ?label ?common ?img WHERE {{
      VALUES ?name {{ {vals} }}
      ?item wdt:P225 ?name .
      OPTIONAL {{ ?item rdfs:label ?label FILTER(lang(?label)="hu") }}
      OPTIONAL {{ ?item wdt:P1843 ?common FILTER(lang(?common)="hu") }}
      OPTIONAL {{ ?item wdt:P18 ?img }} }}"""
    body = urllib.parse.urlencode({"query": q, "format": "json"}).encode()
    rows = json.loads(get("https://query.wikidata.org/sparql", body))["results"]["bindings"]
    res = {}
    for r in rows:
        n = r["name"]["value"]
        e = res.setdefault(n, {"hu": "", "img": ""})
        for k in ("common", "label"):
            v = r.get(k, {}).get("value", "")
            if v and v.lower() != n.lower() and not e["hu"]:
                e["hu"] = v
        if not e["img"] and "img" in r:
            e["img"] = r["img"]["value"]
    return res


def inat(name):
    url = "https://api.inaturalist.org/v1/taxa?" + urllib.parse.urlencode(
        {"q": name, "locale": "hu", "per_page": 1, "is_active": "true"})
    time.sleep(1)  # iNat asks for <= 1 req/s
    res = json.loads(get(url))["results"]
    # fuzzy search can return an unrelated taxon; require the same genus
    if not res or res[0]["name"].split()[0].lower() != name.split()[0].lower():
        return {"hu": "", "img": "", "credit": ""}
    t = res[0]
    ph = t.get("default_photo") or {}
    if not ph.get("license_code"):  # "all rights reserved" may not be republished in a public repo
        ph = {}
    cn = t.get("preferred_common_name") or ""
    species = t.get("rank") in ("species", "hybrid", "variety", "subspecies") and " " in name
    return {"hu": cn if species and cn.lower() != t["name"].lower() else "",
            "img": (ph.get("medium_url") or "").replace("/medium.", "/large."),
            "credit": ph.get("attribution", "")}


def looks_latin(s):
    """'Xerochrysum bracteatum' is a synonym, not a Hungarian name: binomial shape, no Hungarian accents,
    and a Latin ending or letter cluster. Misses e.g. 'Salix alba' — those stay flagged 'verify' anyway."""
    if not re.fullmatch(r"[A-Z][a-z]+(?: [a-z×-]+){1,3}", s) or re.search(r"[áéíóöőúüű]", s):
        return False
    return bool(re.search(r"(?:um|us|ae|ii|is|oides|ensis)\b|ph|th|rh|ch|x|q", s))


def main():
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    for p in plants:  # undo earlier auto-names that were Latin synonyms
        if p.get("verify") and looks_latin(p["hu"]):
            p["hu"], p["aliases"] = "", []
            del p["verify"]
    IMG.mkdir(exist_ok=True)
    todo = [p for p in plants if not p["hu"] or not p["image"]]
    allnames = sorted({c for p in todo for c in candidates(p["latin"])})
    wd = {}
    for i in range(0, len(allnames), 150):
        wd.update(wikidata(allnames[i:i + 150]))
        print(f"wikidata {min(i + 150, len(allnames))}/{len(allnames)}")
    for n, p in enumerate(todo, 1):
        cands = candidates(p["latin"])
        # names only from species-level hits: genus label ("petúnia") is not the official name ("kerti petúnia")
        hu = next((wd[c]["hu"] for c in cands if " " in c and c in wd and wd[c]["hu"]), "")
        # photos: iNaturalist first (usually the plant in bloom), Wikidata P18 as fallback
        img = credit = ""
        if not p["image"]:
            for c in cands:
                fb = inat(c)
                hu = hu or fb["hu"]
                if fb["img"]:
                    img, credit = fb["img"], "iNaturalist: " + fb["credit"]
                    break
            if not img:
                wimg = next((wd[c]["img"] for c in cands if c in wd and wd[c]["img"]), "")
                if wimg:
                    img = wimg.replace("http://", "https://") + "?width=960"  # Wikimedia only serves standard thumbnail steps without 429s
                    credit = "Wikimedia Commons: " + urllib.parse.unquote(wimg.rsplit("/", 1)[-1])
        elif not hu and cands:
            hu = inat(cands[0])["hu"]
        if hu and not p["hu"] and not looks_latin(hu):
            p["hu"], p["verify"] = hu, True
        if img and not p["image"]:
            try:
                # neutral file name: a Latin file name would give the answer away
                f = IMG / f"{hashlib.sha1(p['id'].encode()).hexdigest()[:10]}.jpg"
                f.write_bytes(get(img))
                p["image"], p["credit"] = f"images/{f.name}", credit
                time.sleep(0.3)
            except Exception as e:
                print("  image fail", p["latin"], e)
        print(f"{n}/{len(todo)} {p['latin']} | {p['hu'] or '-'} | {'img' if p['image'] else 'NO IMG'}")
        if n % 25 == 0:
            DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=1), encoding="utf-8")
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"done: {sum(1 for p in plants if p['hu'])} hu, {sum(1 for p in plants if p['image'])} images / {len(plants)}")


if __name__ == "__main__":
    main()
