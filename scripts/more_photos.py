"""Add up to 3 extra photos per plant (iNaturalist taxon photos, CC-licensed only) as hotlinks in data.json
under "more": [{"image": url, "credit": "..."}]. Skips plants that already have "more"; safe to re-run.
Usage: python scripts/more_photos.py"""
import json, time, urllib.parse
from enrich import DATA, candidates, get

EXTRA = 3


def taxon_id(name):
    url = "https://api.inaturalist.org/v1/taxa?" + urllib.parse.urlencode({"q": name, "per_page": 1, "is_active": "true"})
    time.sleep(1)  # iNat asks for <= 1 req/s
    res = json.loads(get(url))["results"]
    if res and res[0]["name"].split()[0].lower() == name.split()[0].lower():
        return res[0]["id"]


def extras(taxon):
    out = []
    # the primary photo is usually the taxon's default photo; don't repeat it
    skip = (taxon.get("default_photo") or {}).get("id")
    for tp in taxon.get("taxon_photos", []):
        ph = tp["photo"]
        if not ph.get("license_code") or ph.get("id") == skip:  # all rights reserved -> skip
            continue
        url = (ph.get("medium_url") or ph.get("url", "").replace("/square.", "/medium.")).replace("/medium.", "/large.")
        if not url:
            continue
        out.append({"image": url, "credit": "iNaturalist: " + ph.get("attribution", "")})
        if len(out) == EXTRA:
            break
    return out


def main():
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    todo = [p for p in plants if "more" not in p]
    ids = {}
    for n, p in enumerate(todo, 1):
        for c in candidates(p["latin"])[:1] + [c for c in candidates(p["latin"])[1:] if " " not in c][:1]:
            tid = taxon_id(c)
            if tid:
                ids[p["id"]] = tid
                break
        print(f"search {n}/{len(todo)} {p['latin']} -> {ids.get(p['id'])}")
    by_id = {p["id"]: p for p in plants}
    tids = sorted(set(ids.values()))
    taxa = {}
    for i in range(0, len(tids), 30):  # the taxa endpoint takes up to 30 ids per call
        time.sleep(1)
        for t in json.loads(get("https://api.inaturalist.org/v1/taxa/" + ",".join(map(str, tids[i:i + 30]))))["results"]:
            taxa[t["id"]] = t
        print(f"taxa {min(i + 30, len(tids))}/{len(tids)}")
    for pid, tid in ids.items():
        by_id[pid]["more"] = extras(taxa.get(tid, {}))
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"done: {sum(1 for p in plants if p.get('more'))} plants with extra photos, "
          f"{sum(len(p.get('more', [])) for p in plants)} photos")


if __name__ == "__main__":
    main()
