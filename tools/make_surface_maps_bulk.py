#!/usr/bin/env python3
"""Erzeugt Normal Maps für alle geeigneten Schiffs- und Basistexturen (Massenlauf).

Ergänzung zu make_surface_maps.py (handgewählte Beispielkarten). Ablauf:
  1. Texturen aus Material/ships, Models/ships und Models/bases lesen (UTF-Container).
  2. Aussortieren: Namen von Lichtern, Fenstern, Schildern, Hintergründen u. ä., Texturen unter 256 px,
     inhaltlich gleiche Texturen (MD5) nur einmal, Namen mit verschiedenem Inhalt (nicht eindeutig
     zuordenbar), Texturen, die schon eine Karte aus make_surface_maps.py haben.
  3. Je Karte: Höhenkarte aus Helligkeit, Stärke so, dass p95 der Neigung bei 28° und p99 höchstens
     bei 60° liegt (wie `--tune`), BC5. Karten ohne erkennbares Relief (über 90 % unter 1°) entfallen.
  4. Bibliotheken `Material/fx/normalmaps_<gruppe>_<nr>.txm` (höchstens 48 MB je Datei),
     INI `SDK/fx/SurfaceMapsAuto.ini`, Parameter `tools/surface_maps_auto.json`,
     Schutzliste `tools/extra_maps_auto.txt`, Bericht `surface-maps-auto-bewertung.md`.

Schiffskarten 1024 px, Basiskarten 512 px (die Texturen sind größtenteils KI-hochskaliert,
mehr Auflösung bringt der Normal Map nichts).

  python3 tools/make_surface_maps_bulk.py [--limit N] [--jobs 8] [--dry-run]
Voraussetzung: Pillow, numpy, etcpak.
"""
import argparse
import collections
import concurrent.futures as cf
import hashlib
import io
import json
import os
import re
import struct
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_surface_maps as M  # noqa: E402
import utf_write as W  # noqa: E402

ROOT = M.ROOT
NAP = M.NAP
ROOTS = [('ships', 'Material/ships', 1024), ('ships', 'Models/ships', 1024), ('bases', 'Models/bases', 512)]
BAD = re.compile(r'illum|light|alpha|banner|sign|window|glass|plasma|\.avi|fade|neon|sky|city|debris|damage|'
                 r'dmg|logo|text|number|flag|glow|lamp|beam|fx_|^sun|star|cloud|atmo|flare|decal|arrow|icon|'
                 r'inv_|nav_|hud|font|_lod|mask|shadow|cockpit|pilot|face|head|skin|map_|billboard|screen|'
                 r'monitor|tv|video|poster|ad_|advert|sprite|particle', re.I)
MAX_FILE_BYTES = 48 * 1024 * 1024
PARAMS_JSON = os.path.join(HERE, 'surface_maps_auto.json')
EXTRA_LIST = os.path.join(HERE, 'extra_maps_auto.txt')
INI_PATH = os.path.join(ROOT, 'SDK', 'fx', 'SurfaceMapsAuto.ini')
REPORT = os.path.join(ROOT, 'surface-maps-auto-bewertung.md')


def slug(name):
    base = re.sub(r'\.(tga|bmp|psd|dds)\d*$', '', name.lower())
    s = re.sub(r'[^a-z0-9]+', '_', base).strip('_')
    return s or 'tex'


def scan():
    """-> (candidates, stats). candidate = dict(group, set, container, name, size, md5, blob_offset=None)"""
    seen_md5 = {}
    by_name = collections.defaultdict(set)
    stat = collections.Counter()
    curated = {v[1].lower() for v in M.NORMALS.values()}
    cands = []
    for group, rel, size in ROOTS:
        base = os.path.join(NAP, rel)
        for r, _, fs in os.walk(base):
            for f in sorted(fs):
                if not f.lower().endswith(('.mat', '.txm', '.cmp', '.3db')):
                    continue
                p = os.path.join(r, f)
                try:
                    _, tree = W.load(p)
                except Exception:  # noqa: BLE001
                    continue
                sub = os.path.relpath(p, base).split(os.sep)
                sset = sub[0] if group == 'bases' and len(sub) > 1 else 'all'
                for trail, leaf in W.walk(tree):
                    if leaf.name.upper() not in ('MIPS', 'MIP0') or not trail:
                        continue
                    d = leaf.data
                    if d[:4] == b'DDS ':
                        h, w = struct.unpack_from('<II', d, 12)
                    else:
                        w, h = struct.unpack_from('<HH', d, 12)
                    name = trail[-1]
                    stat['gesamt'] += 1
                    by_name[name.lower()].add(hashlib.md5(d).hexdigest())
                    if min(w, h) < 256:
                        stat['unter 256 px'] += 1
                        continue
                    if BAD.search(name):
                        stat['Name aussortiert'] += 1
                        continue
                    if name.lower() in curated:
                        stat['schon kuratiert'] += 1
                        continue
                    md5 = hashlib.md5(d).hexdigest()
                    if md5 in seen_md5:
                        stat['Duplikat'] += 1
                        continue
                    seen_md5[md5] = 1
                    cands.append({'group': group, 'set': sset, 'container': os.path.relpath(p, NAP).replace(os.sep, '/'),
                                  'name': name, 'size': size, 'md5': md5})
    # Namen mit verschiedenem Inhalt lassen sich über die INI nicht zuordnen
    amb = {n for n, s in by_name.items() if len(s) > 1}
    out = []
    for c in cands:
        if c['name'].lower() in amb:
            stat['Name nicht eindeutig'] += 1
        else:
            out.append(c)
    return out, stat


def work(job):
    container, name, size = job
    _, tree = W.load(os.path.join(NAP, container))
    img = None
    for trail, leaf in W.walk(tree):
        if leaf.name.upper() in ('MIPS', 'MIP0') and trail and trail[-1] == name:
            img = Image.open(io.BytesIO(leaf.data)).convert('RGB')
            break
    if img is None:
        return None
    M.NORMAL_SIZE = size
    h = M.height_from(img, 1)
    st = round(M.tune(h), 2)
    h2 = h
    m = M.metrics(h2, st)
    if m['grain'] > 1.5:
        h2 = M.height_from(img, 2)
        st = round(M.tune(h2), 2)
        m = M.metrics(h2, st)
        smooth = 2
    else:
        smooth = 1
    if m['flat'] > 0.90:
        return {'skip': 'kaum Relief', 'metrics': m, 'strength': st}
    if m['p95'] < 8.0:   # selbst mit der größten Stärke kaum Neigung: nur verstärktes Rauschen
        return {'skip': 'zu flach (p95 unter 8°)', 'metrics': m, 'strength': st}
    n = M.normal_from_height(h2, st)
    return {'data': M.encode_normal(n), 'strength': st, 'smooth': smooth, 'metrics': m, 'size': size}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--limit', type=int)
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cands, stat = scan()
    if a.limit:
        cands = cands[:a.limit]
    print('Kandidaten:', len(cands), dict(stat))
    if a.dry_run:
        return
    results = {}
    with cf.ProcessPoolExecutor(a.jobs) as ex:
        futs = {ex.submit(work, (c['container'], c['name'], c['size'])): c for c in cands}
        for i, f in enumerate(cf.as_completed(futs), 1):
            c = futs[f]
            try:
                results[c['md5']] = (c, f.result())
            except Exception as e:  # noqa: BLE001
                results[c['md5']] = (c, {'skip': 'Fehler: ' + str(e)[:60]})
            if i % 200 == 0:
                print(f'  {i}/{len(cands)}', flush=True)

    # Schlüssel eindeutig machen und in Bibliotheken packen
    used_keys = set()
    libs = collections.defaultdict(list)
    skipped = collections.Counter()
    params = {}
    for md5, (c, r) in sorted(results.items(), key=lambda kv: (kv[1][0]['group'], kv[1][0]['set'], kv[1][0]['name'])):
        if r is None or 'skip' in r:
            skipped[(r or {}).get('skip', 'Textur nicht gefunden')] += 1
            continue
        key = f"{c['group']}_{slug(c['name'])}"
        base, n = key, 2
        while key in used_keys:
            key, n = f'{base}_{n}', n + 1
        used_keys.add(key)
        c['key'] = key
        libs[(c['group'], c['set'])].append((c, r))
        params[key] = {'texture': c['name'], 'container': c['container'], 'md5': c['md5'], 'strength': r['strength'],
                       'smooth': r['smooth'], 'size': r['size'],
                       'p95': round(r['metrics']['p95'], 1), 'flat': round(r['metrics']['flat'], 3)}

    made, ini = [], []
    lib_names = {}
    for (group, sset), items in sorted(libs.items()):
        idx, cur, cur_bytes = 1, {}, 0
        chunks = []
        for c, r in items:
            if cur and cur_bytes + len(r['data']) > MAX_FILE_BYTES:
                chunks.append(cur)
                cur, cur_bytes = {}, 0
            cur['nm_' + c['key']] = (c, r['data'])
            cur_bytes += len(r['data'])
        if cur:
            chunks.append(cur)
        for i, ch in enumerate(chunks, 1):
            lname = f'normalmaps_{group}_{sset}_{i}' if sset != 'all' else f'normalmaps_{group}_auto_{i}'
            lname = re.sub(r'[^a-z0-9_]+', '_', lname.lower())
            header, root = M.build_library({k: v[1] for k, v in ch.items()}, 'MIPS')
            path = os.path.join(NAP, 'Material', 'fx', lname + '.txm')
            W.save(path, header, root)
            made.append(f'Material/fx/{lname}.txm')
            ini.append(f'\n[Texture]\nfile = fx\\{lname}.txm\nname = surface_{lname}\n')
            for k, (c, _) in ch.items():
                lib_names[c['key']] = 'surface_' + lname
            print(f'{lname}.txm: {len(ch)} Karten, {os.path.getsize(path) / 1e6:.1f} MB')
    body = []
    for (group, sset), items in sorted(libs.items()):
        for c, r in items:
            body.append(f"\n[NormalMap]\ntexture = {c['name']}\nlibrary = {lib_names[c['key']]}\n"
                        f"map = nm_{c['key']}\nstrength = {r['strength']:g}\n")
    with open(INI_PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write('; SurfaceMapsAuto.ini - automatisch erzeugte Normal Maps fuer Schiffs- und Basistexturen.\n'
                '; Syntax wie SurfaceMaps.ini. Erzeugt von tools/make_surface_maps_bulk.py, nicht von Hand aendern.\n'
                '; Eine Textur kommt hoechstens einmal vor; Namen mit verschiedenem Inhalt wurden ausgelassen.\n')
        f.write(''.join(ini) + ''.join(body))
    with open(PARAMS_JSON, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(params, f, indent=0, ensure_ascii=False, sort_keys=True)
        f.write('\n')
    with open(EXTRA_LIST, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Von tools/make_surface_maps_bulk.py erzeugte Normal-Map-Bibliotheken (Klasse/Pfad)\n')
        f.write('\n'.join(made) + '\n')
    write_report(cands, stat, skipped, params, libs, made)
    print('fertig:', len(params), 'Karten in', len(made), 'Dateien; übersprungen', dict(skipped))


def write_report(cands, stat, skipped, params, libs, made):
    total = sum(os.path.getsize(os.path.join(NAP, m)) for m in made)
    p95 = np.array([v['p95'] for v in params.values()]) if params else np.array([0.0])
    s = np.array([v['strength'] for v in params.values()]) if params else np.array([0.0])
    L = ['# Bewertung der automatisch erzeugten Normal Maps (Schiffe und Basen)', '',
         'Erzeugt von `tools/make_surface_maps_bulk.py`. Die Kennzahlen beschreiben die Karten, nicht ihre Wirkung im Spiel.', '',
         '## Auswahl', '', '| Schritt | Texturen |', '|---|---:|']
    for k, v in stat.most_common():
        L.append(f'| {k} | {v} |')
    L += [f'| **erzeugt** | **{len(params)}** |']
    for k, v in skipped.most_common():
        L.append(f'| übersprungen: {k} | {v} |')
    L += ['', '## Ergebnis', '', f'- Dateien: {len(made)}, zusammen {total / 1e6:.0f} MB',
          f"- Schiffe: {sum(1 for v in params.values() if v['size'] == 1024)} Karten (1024 px), Basen: {sum(1 for v in params.values() if v['size'] == 512)} (512 px)",
          f'- Stärke: Median {np.median(s):.2f}, Spanne {s.min():.2f} bis {s.max():.2f}; an der Untergrenze 0,5: {(s <= 0.5).sum()}, an der Obergrenze 6,0: {(s >= 6.0).sum()}',
          f'- p95 der Neigung: Median {np.median(p95):.1f}°, Spanne {p95.min():.1f}° bis {p95.max():.1f}°; unter 12° (flach): {(p95 < 12).sum()}, über 40°: {(p95 > 40).sum()}',
          '', '## Bibliotheken', '', '| Datei | Größe |', '|---|---:|']
    for m in made:
        L.append(f'| `{m}` | {os.path.getsize(os.path.join(NAP, m)) / 1e6:.1f} MB |')
    open(REPORT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
