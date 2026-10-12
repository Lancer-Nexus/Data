#!/usr/bin/env python3
"""Löst Texturen aus Freelancer-UTF-Dateien (.txm, .3db, .cmp, .mat, .dfm, .sph) als PNG heraus.

Standardmäßig nur die Originaltexturen (nicht aus dem HD-Pack, siehe tools/hd_overrides.txt).
Je Textur wird die größte Stufe (MIP0 bzw. oberste Stufe aus MIPS) gespeichert, dazu eine
manifest.csv mit Container, Texturname, Größe, Format, Zielgröße (Faktor 4 wie im HD-Pack).

Voraussetzung: Pillow. Ausgabe liegt außerhalb des Repos.

Aufruf:
    python3 tools/extract_textures.py --out ~/Dokumente/Freelancer-Textures/original
    python3 tools/extract_textures.py --out ... --all     # auch HD-Texturen
"""
import argparse
import csv
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import utf_textures as ut  # noqa: E402
import check_textures as ct  # noqa: E402

EXT = ('.txm', '.3db', '.cmp', '.mat', '.dfm', '.sph')


def texture_blobs(path):
    """Liefert (texturname, [(knoten, daten)]) je Textur."""
    b, data_off, root = ut.parse(path)
    out = []

    def walk(n):
        for c in n.children:
            if c.flags & 0x10:
                leafs = [x for x in c.children if not (x.flags & 0x10) and x.name.lower().startswith('mip')]
                if leafs:
                    out.append((c.name, [(x.name, b[data_off + x.child:data_off + x.child + x.size]) for x in leafs]))
                else:
                    walk(c)
    walk(root)
    return out


def best(blobs):
    """Größte Stufe: MIPS (DDS, oberste Stufe) oder MIP0 (sonst die größte)."""
    cand = []
    for node, blob in blobs:
        d = ut._dims(blob)
        if d:
            cand.append((d[0] * d[1], node, blob, d))
    if not cand:
        return None
    cand.sort(key=lambda x: -x[0])
    return cand[0]


def safe(s):
    return re.sub(r'[^A-Za-z0-9._-]+', '_', s)[:60]


def main():
    from PIL import Image
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    ap.add_argument('--all', action='store_true', help='auch HD-Texturen')
    ap.add_argument('--factor', type=int, default=4)
    a = ap.parse_args()

    idx = ct.nap_index()
    ov = ct.load_overrides()
    out = os.path.expanduser(a.out)
    os.makedirs(out, exist_ok=True)
    rows, errors, seen = [], [], set()
    n = 0
    for rel, (cls, p) in sorted(idx.items()):
        if not rel.endswith(EXT):
            continue
        if not a.all and rel in ov:
            continue
        try:
            textures = texture_blobs(p)
        except Exception as e:  # noqa: BLE001
            errors.append((rel, str(e)))
            continue
        for tname, blobs in textures:
            b = best(blobs)
            if not b:
                continue
            _, node, blob, d = b
            key = hashlib.md5(blob).hexdigest()
            n += 1
            fid = f'{n:05d}'
            png = os.path.join(out, f'{fid}_{safe(os.path.basename(rel))}_{safe(tname)}.png')
            try:
                im = Image.open(io.BytesIO(blob))
                im.load()
                has_alpha = im.mode in ('RGBA', 'LA', 'P') and 'A' in im.convert('RGBA').getbands()
                im.convert('RGBA').save(png)
            except Exception as e:  # noqa: BLE001
                errors.append((f'{rel}:{tname}', str(e)))
                continue
            rows.append((fid, rel, cls, tname, node, d[0], d[1], d[2], len(blobs), d[0] * a.factor, d[1] * a.factor,
                         key, os.path.relpath(png, out), 'duplikat' if key in seen else ''))
            seen.add(key)
    with open(os.path.join(out, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id', 'container', 'klasse', 'textur', 'knoten', 'breite', 'hoehe', 'format', 'stufen',
                    'ziel_breite', 'ziel_hoehe', 'md5', 'datei', 'hinweis'])
        w.writerows(rows)
    print(f'extrahiert: {len(rows)} | Duplikate (gleiche Daten): {sum(1 for r in rows if r[-1])} | Fehler: {len(errors)}')
    for e in errors[:5]:
        print('  Fehler:', e)
    print('Ausgabe:', out)


if __name__ == '__main__':
    main()
