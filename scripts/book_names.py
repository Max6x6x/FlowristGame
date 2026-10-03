"""Find the Hungarian name a textbook uses next to each plant's Latin name.
Patterns: "Latin – magyar", "Latin (magyar)", "magyar (Latin)", "Latin, magyar;"
Books stay local (git-ignored); only names (facts) are extracted.
Usage: python scripts/book_names.py out.json book1.txt [book2.txt ...]"""
import json, re, sys
from collections import Counter
from enrich import DATA, looks_latin

L = "a-záéíóöőúüű"
STOP = {"fajták", "fajta", "hibridek", "hibrid", "fajok", "faj", "nemzetség", "változat", "kultivár", "és", "vagy", "pl", "lásd",
        "termesztése", "termesztés", "szaporítása", "virágzás", "levél", "levelek", "virág", "virágok", "magas", "cm", "m"}
HUN = rf"([{L}][{L}\-]+(?:\s+[{L}\-]+){{0,2}})"


def latin_forms(latin):
    base = re.sub(r"'[^']*'?|\([^)]*\)|\b(x|×|sp|var|subsp)\b\.?", " ", latin).split()
    if len(base) < 2 or not base[1][0].islower():
        return []
    g, e = base[0], base[1]
    return [rf"{g}\s+{e}", rf"{g[0]}\.\s*{e}"]


def ok(name):
    w = name.split()
    return (1 <= len(w) <= 3 and not looks_latin(name) and not any(x in STOP for x in w)
            and len(name) >= 4 and not re.search(r"\d", name))


def scan(text, latin):
    """Locate the Latin name first (cheap), then read the Hungarian phrase right before/after it."""
    found = Counter()
    after = [(re.compile(rf"^\s*[–-]\s*{HUN}"), 3),         # heading: "Aglaonema modestum – rákvirág"
             (re.compile(rf"^\s*\(\s*{HUN}\s*\)"), 2),      # "Betula pendula (nyír)"
             (re.compile(rf"^\s*,\s*{HUN}\s*[;,.)]"), 1)]   # "Cymbidium lowianum, barnás csónakorchidea;"
    before = re.compile(rf"{HUN}\s*\(\s*$")                 # "nyírfa (Betula pendula)"
    for f in latin_forms(latin):
        for m in re.finditer(f, text):
            tail = text[m.end():m.end() + 60]
            for pat, weight in after:
                a = pat.match(tail)
                if a and ok(a.group(1).strip().lower()):
                    found[a.group(1).strip().lower()] += weight
            if text[m.end():m.end() + 2].lstrip().startswith(")"):
                b = before.search(text[max(0, m.start() - 60):m.start()])
                if b and ok(b.group(1).strip().lower()):
                    found[b.group(1).strip().lower()] += 2
    return found


def main(out, *books):
    texts = [re.sub(r"\s+", " ", open(b, encoding="utf-8").read()) for b in books]
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    res = {}
    for p in plants:
        c = Counter()
        for t in texts:
            c += scan(t, p["latin"])
        if c:
            res[p["id"]] = {"latin": p["latin"], "current": p["hu"], "verify": bool(p.get("verify")),
                            "course": bool(p["hu"]) and not p.get("verify") and "src" not in p, "book": c.most_common(3)}
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(res), "plants found in the books")


if __name__ == "__main__":
    main(*sys.argv[1:])
