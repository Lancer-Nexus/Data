#!/usr/bin/env python3
"""Passt die Formkoordinaten ([Shape] x, y, w, h) in SDK-INIs an hochskalierte Texturen an.

Für jede Textur eines hochskalierten Containers (Liste: `--containers`, Standard
tools/upscaled_containers.txt, Klasse/pfad) wird die Ausdehnung aller Formen bestimmt. Reichen
die Formen höchstens bis zur halben Texturgröße, werden x, y, w, h mit dem Faktor 4 multipliziert.
Mehrfach ausführbar: nach der Anpassung füllen die Formen die Textur wieder aus.

  python3 tools/scale_shape_inis.py [--dry-run]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import utf_textures as ut  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..'))
NAP = os.path.join(ROOT, 'NAP')
SDK = os.path.join(ROOT, 'SDK')
FACTOR = 4


def parse_ini(lines):
    """-> Liste von Formen: {'tex': name, 'keys': {k: zeilenindex}, 'vals': {k: float}} und {name: datei}."""
    shapes, files = [], {}
    sec, cur, last_tex = None, None, ''
    tex_cur = {}
    for i, raw in enumerate(lines):
        c = raw.split(';')[0].strip()
        if not c:
            continue
        if c.startswith('['):
            if sec == 'texture' and 'name' in tex_cur and 'file' in tex_cur:
                files[tex_cur['name'].lower()] = re.sub(r'[\\/]+', '/', tex_cur['file']).lower()
            sec = c.strip('[]').lower()
            tex_cur = {}
            cur = None
            if sec == 'shape':
                cur = {'tex': last_tex, 'keys': {}, 'vals': {}, 'tn': ''}
                shapes.append(cur)
            continue
        if '=' not in c:
            continue
        k, v = (s.strip() for s in c.split('=', 1))
        k = k.lower()
        if sec == 'texture':
            tex_cur[k] = v
            if k == 'name':
                last_tex = v.lower()
            if 'name' in tex_cur and 'file' in tex_cur:
                files[tex_cur['name'].lower()] = re.sub(r'[\\/]+', '/', tex_cur['file']).lower()
        elif sec == 'shape' and cur is not None:
            if k in ('x', 'y', 'w', 'h'):
                try:
                    cur['vals'][k] = float(v)
                    cur['keys'][k] = i
                except ValueError:
                    pass
            elif k == 'texture_name':
                cur['tn'] = v.lower()
    return shapes, files


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--containers', default=os.path.join(HERE, 'upscaled_containers.txt'))
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    up = {re.sub(r'^[^/]+/', '', l.strip().lower()) for l in open(a.containers, encoding='utf-8')
          if l.strip() and not l.startswith('#')}
    # Index NAP: klassenloser Pfad -> Datei
    idx = {}
    for c in os.listdir(NAP):
        for r, _, fs in os.walk(os.path.join(NAP, c)):
            for f in fs:
                p = os.path.join(r, f)
                idx[os.path.relpath(p, os.path.join(NAP, c)).replace(os.sep, '/').lower()] = p
    changed_files = scaled = 0
    for r, _, fs in os.walk(SDK):
        for f in fs:
            if not f.lower().endswith('.ini'):
                continue
            path = os.path.join(r, f)
            raw = open(path, 'rb').read()
            if b'[shape]' not in raw.lower():
                continue
            text = raw.decode('latin-1')
            nl = '\r\n' if '\r\n' in text else '\n'
            lines = text.split(nl)
            shapes, files = parse_ini(lines)
            ext = {}
            for s in shapes:
                tn = s['tn'] or s['tex']
                v = s['vals']
                if len(v) < 4 or tn not in files:
                    continue
                e = ext.setdefault(tn, [0, 0])
                e[0] = max(e[0], v['x'] + v['w'])
                e[1] = max(e[1], v['y'] + v['h'])
            todo = set()
            for tn, (mx, my) in ext.items():
                fp = files[tn]
                if fp not in up or fp not in idx or mx <= 0 or my <= 0:
                    continue
                try:
                    t = ut.textures(idx[fp])
                except Exception:  # noqa: BLE001
                    continue
                d = t.get(tn) or t.get(tn + '_0')
                if d and d[0] >= 2 * mx and d[1] >= 2 * my:
                    todo.add(tn)
            if not todo:
                continue
            n = 0
            for s in shapes:
                if (s['tn'] or s['tex']) in todo and len(s['vals']) == 4:
                    for k, i in s['keys'].items():
                        val = int(round(s['vals'][k] * FACTOR))
                        lines[i] = re.sub(r'(=\s*)[-\d.]+', lambda m: m.group(1) + str(val), lines[i], count=1)
                    n += 1
            scaled += n
            changed_files += 1
            print(f'{os.path.relpath(path, SDK)}: {n} Formen ({", ".join(sorted(todo))})')
            if not a.dry_run:
                open(path, 'wb').write(nl.join(lines).encode('latin-1'))
    print(f'{changed_files} Dateien, {scaled} Formen' + (' (Probelauf)' if a.dry_run else ''))


if __name__ == '__main__':
    main()
