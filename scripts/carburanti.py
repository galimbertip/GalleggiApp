#!/usr/bin/env python3
"""
Scarica gli open data ufficiali del MIMIT (Osservatorio prezzi carburanti) e li divide
in "zone" JSON da 0,5° x 0,5° (circa 55 x 40 km), così GalleggiApp scarica solo la zona
in cui ti trovi. Uso:  python scripts/carburanti.py [cartella_uscita]
Fonte: https://www.mimit.gov.it/it/open-data/elenco-dataset/carburanti-prezzi-praticati-e-anagrafica-degli-impianti
"""
import csv, io, json, os, sys, time, math, urllib.request
from datetime import datetime, timezone

URL_ANAG = "https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv"
URL_PREZZI = "https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv"
OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
TILE = 0.5   # gradi per zona

def download(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (GalleggiApp; open data carburanti)"})
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read()
            for enc in ("utf-8-sig", "cp1252", "latin-1"):
                try: return raw.decode(enc)
                except UnicodeDecodeError: pass
        except Exception as e:
            last = e; time.sleep(10 * (i + 1))
    raise RuntimeError(f"download fallito {url}: {last}")

def table(text):
    """Trova la riga di intestazione (quella con 'idImpianto'), il separatore, e restituisce (intestazione, righe, nota)."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    hi = next(i for i, l in enumerate(lines) if "idimpianto" in l.lower().replace(" ", ""))
    head = lines[hi]
    sep = max(["|", ";", ",", "\t"], key=head.count)
    rdr = csv.reader(io.StringIO("\n".join(lines[hi:])), delimiter=sep, quotechar='"')
    rows = [r for r in rdr if r and any(x.strip() for x in r)]
    hdr = [h.strip().strip('"').lower().replace(" ", "").replace("_", "") for h in rows[0]]
    return hdr, rows[1:], " ".join(lines[:hi]).strip(), sep

def col(hdr, *names, default=None):
    for n in names:
        if n in hdr: return hdr.index(n)
    if default is not None: return default
    raise KeyError(f"colonna mancante {names} in {hdr}")

def num(s):
    s = (s or "").strip().strip('"')
    if not s: return None
    if "," in s and "." not in s: s = s.replace(",", ".")
    try: return float(s)
    except ValueError: return None

def fuel_kind(desc):
    d = desc.lower()
    if "adblue" in d or "idrogeno" in d or "gnl" in d and "gnc" not in d: return None
    if "gpl" in d: return "G"
    if "metano" in d or "gnc" in d: return "M"
    if "gasolio" in d or "diesel" in d or "hvo" in d: return "D"
    if any(k in d for k in ("benzina", "super", "senza piombo", "hi-q", "hiq", "v-power", "excellium", "verde")): return "B"
    return None

def main():
    t_anag = download(URL_ANAG); t_prez = download(URL_PREZZI)
    ha, ra, nota_a, sep_a = table(t_anag)
    hp, rp, nota_p, sep_p = table(t_prez)
    ia = dict(id=col(ha, "idimpianto"), gest=col(ha, "gestore", default=1), band=col(ha, "bandiera", default=2),
              nome=col(ha, "nomeimpianto", default=4), ind=col(ha, "indirizzo", default=5), com=col(ha, "comune", default=6),
              prov=col(ha, "provincia", default=7), lat=col(ha, "latitudine", default=8), lng=col(ha, "longitudine", default=9))
    ip = dict(id=col(hp, "idimpianto"), desc=col(hp, "desccarburante", default=1), prezzo=col(hp, "prezzo", default=2),
              self=col(hp, "isself", default=3), dt=col(hp, "dtcomu", default=4))
    prices, dates = {}, {}
    for r in rp:
        try:
            sid = r[ip["id"]].strip(); k = fuel_kind(r[ip["desc"]]); p = num(r[ip["prezzo"]])
        except IndexError: continue
        if not k or p is None or not (0.3 < p < 5): continue
        s = r[ip["self"]].strip().lower() in ("1", "true", "si", "sì", "self")
        slot = prices.setdefault(sid, {}).setdefault(k, [None, None])   # [self, servito]
        i = 0 if s else 1
        if slot[i] is None or p < slot[i]: slot[i] = round(p, 3)
        dt = r[ip["dt"]].strip() if len(r) > ip["dt"] else ""
        try:
            d = datetime.strptime(dt[:19], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d")
            if d > dates.get(sid, ""): dates[sid] = d
        except ValueError: pass
    tiles, n = {}, 0
    for r in ra:
        try:
            sid = r[ia["id"]].strip(); lat = num(r[ia["lat"]]); lng = num(r[ia["lng"]])
        except IndexError: continue
        if sid not in prices or lat is None or lng is None or not (35 < lat < 48 and 6 < lng < 19.5): continue
        key = f"{math.floor(lat / TILE)}_{math.floor(lng / TILE)}"
        name = (r[ia["nome"]].strip() or r[ia["gest"]].strip())[:60]
        tiles.setdefault(key, []).append([sid, name, r[ia["band"]].strip()[:30], r[ia["ind"]].strip()[:80],
            f'{r[ia["com"]].strip()} ({r[ia["prov"]].strip()})', round(lat, 5), round(lng, 5), prices[sid], dates.get(sid, "")])
        n += 1
    if n < 1000: raise RuntimeError(f"troppi pochi distributori ({n}): formato cambiato? intestazioni {ha} / {hp}")
    os.makedirs(f"{OUT}/z", exist_ok=True)
    for k, v in tiles.items():
        with open(f"{OUT}/z/{k}.json", "w", encoding="utf-8") as f: json.dump(v, f, ensure_ascii=False, separators=(",", ":"))
    meta = {"fonte": "MIMIT – Osservatorio prezzi carburanti (open data, IODL 2.0)", "estrazione": nota_p or nota_a,
            "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"), "distributori": n, "zone": len(tiles),
            "zona_gradi": TILE, "colonne": {"anagrafica": ha, "prezzi": hp}, "separatori": [sep_a, sep_p],
            "formato": "[id, nome, bandiera, indirizzo, comune, lat, lng, {B|D|G|M: [self, servito]}, data_prezzi]"}
    with open(f"{OUT}/meta.json", "w", encoding="utf-8") as f: json.dump(meta, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: meta[k] for k in ("estrazione", "distributori", "zone", "separatori")}, ensure_ascii=False))

if __name__ == "__main__":
    main()
