"""Apply book_names.py results: confirm matching names, fill empty ones conservatively, offer the rest.
Course-sheet names are never touched. Usage: python scripts/apply_book_names.py results.json "Source label" book1.txt [...]"""
import json, re, sys
from enrich import DATA
from hu_names import same

JUNK = {"az", "a", "egy", "nagyon", "például", "gyakori", "előzőhöz", "amely", "éppoly", "feltűnő", "balesetveszélyes",
        "fehérek", "sárga", "fehér", "piros", "kék", "lila", "törpe", "pirosló", "középtermetű", "nagytermetű", "kistermetű", "magas", "alacsony", "v", "is", "nem", "már", "még", "alkotó", "nyírt"}


def main(results, label, *books):
    words = {}
    for b in books:
        for w in re.findall(r"[a-záéíóöőúüű\-]{3,}", open(b, encoding="utf-8").read().lower()):
            words[w] = words.get(w, 0) + 1
    res = json.load(open(results, encoding="utf-8"))
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    st = dict(confirmed=0, filled=0, offered=0)
    for p in plants:
        r = res.get(p["id"])
        if not r or (p["hu"] and not p.get("verify")):  # course sheet / already checked
            continue
        cands = [(n, w) for n, w in r["book"]
                 if not any(x in JUNK for x in n.split()) and all(words.get(x, 0) >= 2 for x in n.split())]
        if not cands:
            continue
        alt = p.get("alt", [])
        if p["hu"] and any(same(p["hu"], n) for n, _ in cands):
            st["confirmed"] += 1
            p["src"] = f"{p.get('src', 'Wikidata/iNaturalist')} + {label} egyezik"
            p.pop("verify", None)
        elif not p["hu"] and cands[0][1] >= 3 and len(cands[0][0].split()) >= 1:
            st["filled"] += 1
            p["hu"], p["src"], p["verify"] = cands[0][0], label, True
        for n, w in cands:
            chip = f"{n} ({label})"
            if w >= 2 and not same(n, p["hu"] or "") and chip not in alt:
                alt.append(chip)
                st["offered"] += 1
        if alt:
            p["alt"] = alt
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(st, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:])
