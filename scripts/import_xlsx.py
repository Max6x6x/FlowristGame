"""One-time import: Növénylista xlsx -> data.json. Usage: python scripts/import_xlsx.py <file.xlsx>"""
import json, re, sys, unicodedata
from pathlib import Path
import openpyxl

OUT = Path(__file__).resolve().parent.parent / "data.json"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def split_names(s):
    # "mindignyíló begónia v. kerti begónia" / "vaníliavirág, perui kunkor" -> list
    parts = re.split(r"\s+(?:vagy|v\.?)\s+|\s*,\s*|\s*/\s*", s.strip())
    return [p.strip() for p in parts if p.strip()]


def main(path):
    ws = openpyxl.load_workbook(path).active
    plants, by_id, category = [], {}, ""
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        latin, hu, note = (str(c).strip() if c else "" for c in row[:3])
        if i < 3 or not latin:
            continue
        if latin.endswith(":"):
            category = latin[:-1]
            continue
        if latin.isupper():  # group banner, e.g. "FÁSSZÁRÚ NÖVÉNYEK"
            continue
        pid = slug(latin)
        if pid in by_id:  # same plant listed under several categories
            p = by_id[pid]
            if category not in p["categories"]:
                p["categories"].append(category)
            if hu and not p["hu"]:
                names = split_names(hu)
                p["hu"], p["aliases"] = names[0], names[1:]
            continue
        names = split_names(hu) if hu else []
        p = {"id": pid, "latin": latin, "hu": names[0] if names else "", "aliases": names[1:],
             "note": note, "categories": [category], "image": "", "credit": ""}
        by_id[pid] = p
        plants.append(p)
    OUT.write_text(json.dumps(plants, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(plants)} plants, {sum(1 for p in plants if p['hu'])} with Hungarian name -> {OUT}")


if __name__ == "__main__":
    main(sys.argv[1])
