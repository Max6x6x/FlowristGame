# Növényismeret

Plant-name study app for the florist course list ("Növényismereti jegyzék"). Photo quiz: write the Latin and the official Hungarian name, with hints, zoom, and 20/50-question rounds. Static site on GitHub Pages: `index.html` + `data.json` + `images/`.

- **Admin tab** (only visible on devices set up with the link `https://max6x6x.github.io/FlowristGame/#token=<TOKEN>`): fix names, aliases, notes, replace photos. Saving commits to this repo using a fine-grained GitHub token (this repo only, *Contents: Read and write*), stored only in that browser. Without the token nobody can change anything.
- **Progress** (which plants she knows) is stored per device in the browser.

## Data scripts

```bash
python scripts/import_xlsx.py "Növénylista 2025.xlsx"   # one-time: sheet -> data.json (overwrites!)
python scripts/enrich.py                                # fills missing Hungarian names + photos; never overwrites
python scripts/test_scripts.py                          # self-check
```

Names in the course sheet are authoritative. Automatically found names (Wikidata/iNaturalist) carry `"verify": true` until confirmed in Admin. Photos: iNaturalist (CC licences, credit in `data.json`), Wikimedia Commons as fallback.
