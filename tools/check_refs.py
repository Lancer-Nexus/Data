#!/usr/bin/env python3
"""Prüft alle Datei-Verweise in SDK/**/*.ini gegen den virtuellen Root von NAP/ und schreibt missing.md.

Ein Verweis ist ein Wert (nach `=`, durch Kommas getrennt), der auf eine bekannte Dateiendung endet.
Er gilt als gefunden, wenn der Pfad (klein geschrieben, `\\` → `/`) im virtuellen Root von NAP/
oder als INI in SDK/ liegt. Verweise ohne Ordner werden zusätzlich über den Dateinamen gesucht und
dann als "liegt unter <Ordner>" vermerkt (die Engine sucht sie selbst).

  python3 tools/check_refs.py [--out missing.md] [--no-write]

Die Bemerkungen der vorhandenen missing.md bleiben erhalten (je Ziel).
"""
import argparse
import collections
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
NAP, SDK = os.path.join(ROOT, 'NAP'), os.path.join(ROOT, 'SDK')
EXTS = ('3db', 'cmp', 'mat', 'txm', 'tga', 'dds', 'bmp', 'jpg', 'wav', 'ogg', 'flac', 'utf', 'mp3', 'thn', 'ale', 'pte',
        'anm', 'dfm', 'sph', 'vms', 'wmv', 'ini', 'page', 'sur', 'dll')
TOKEN = re.compile(r'^[\w\-./\\ ]+\.(' + '|'.join(EXTS) + r')$', re.I)


def norm(s):
    return re.sub(r'/+', '/', s.strip().strip('"').replace('\\', '/')).lstrip('/').lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=os.path.join(ROOT, 'missing.md'))
    ap.add_argument('--no-write', action='store_true')
    a = ap.parse_args()

    have, by_name = set(), collections.defaultdict(list)
    for c in os.listdir(NAP):
        base = os.path.join(NAP, c)
        if not os.path.isdir(base):
            continue
        for r, _, fs in os.walk(base):
            for f in fs:
                rel = os.path.relpath(os.path.join(r, f), base).replace(os.sep, '/').lower()
                have.add(rel)
                by_name[os.path.basename(rel)].append(rel)
    for r, _, fs in os.walk(SDK):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), SDK).replace(os.sep, '/').lower()
            if not rel.startswith('exe/'):
                have.add(rel)
                by_name[os.path.basename(rel)].append(rel)

    miss = collections.defaultdict(set)
    total = 0
    for r, _, fs in os.walk(SDK):
        for f in fs:
            if not f.lower().endswith('.ini') or os.path.relpath(r, SDK).replace(os.sep, '/').startswith('exe'):
                continue
            path = os.path.join(r, f)
            rel_ini = os.path.relpath(path, SDK).replace(os.sep, '/')
            for line in open(path, 'rb').read().decode('latin-1').split('\n'):
                line = line.split(';')[0]
                if '=' not in line:
                    continue
                if f in ('SurfaceMaps.ini', 'SurfaceMapsAuto.ini') and line.split('=', 1)[0].strip().lower() == 'texture':
                    continue   # Texturname (Dt_name), keine Datei
                for tok in line.split('=', 1)[1].split(','):
                    tok = tok.strip()
                    if not TOKEN.match(tok):
                        continue
                    total += 1
                    n = norm(tok)
                    if n in have or 'universe/' + n in have:  # Universe.ini: Pfade relativ zu universe/
                        continue
                    miss[n].add(rel_ini)

    old = {}
    if os.path.exists(a.out):
        for l in open(a.out, encoding='utf-8'):
            m = re.match(r'\| `([^`]+)` \| (?:`[^`]+`(?:, `[^`]+`)*) \| (.*) \|$', l)
            if m:
                old[m.group(1)] = m.group(2)
    rows = []
    for n in sorted(miss):
        rem = ''
        if '/' not in n and by_name.get(n):
            rem = 'liegt unter ' + ', '.join(sorted({os.path.dirname(p) + '/' for p in by_name[n]})) + ', Verweis ohne Ordner'
        elif n in old and old[n]:
            rem = old[n]
        elif n.endswith('_col.cmp'):
            rem = 'Kollisionsmodell fehlt auf der CD'
        elif n.startswith('missions/encounters/spacepop/') and n.endswith('.ini'):
            rem = 'INI fehlt auf der CD'
        rows.append((n, sorted(miss[n]), rem))
    real = [r for r in rows if not r[2].startswith('liegt unter')]
    print(f'{total} Verweise geprüft, {len(rows)} nicht direkt auflösbar, davon {len(real)} fehlen wirklich')
    if a.no_write:
        for n, u, rem in rows:
            print(n, '|', ', '.join(u), '|', rem)
        return
    head = open(a.out, encoding='utf-8').read() if os.path.exists(a.out) else ''
    tail = head[head.index('## Hinweise'):] if '## Hinweise' in head else ''
    L = ['# Fehlende Dateien', '',
         'Dateien, auf die die INIs im SDK verweisen, die aber nicht in `NAP/` liegen. Erzeugt von `tools/check_refs.py` '
         f'(alle Datei-Verweise in `SDK/**/*.ini` ohne `exe/`, {total} Verweise, Groß-/Kleinschreibung ignoriert).', '',
         f'**{len(real)} fehlende Ziele**, dazu {len(rows) - len(real)} Verweise ohne Ordner, deren Datei an anderer Stelle liegt.', '',
         '## Liste', '', '| Ziel | Verwendet in | Bemerkung |', '|---|---|---|']
    for n, u, rem in rows:
        L.append(f'| `{n}` | ' + ', '.join(f'`{x}`' for x in u) + f' | {rem} |')
    L.append('')
    open(a.out, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n' + tail)
    print('geschrieben:', a.out)


if __name__ == '__main__':
    main()
