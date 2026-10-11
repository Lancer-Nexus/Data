#!/usr/bin/env python3
"""Übernimmt die INIs des HD-Packs in SDK/ (normalisiert).

Quelle: Staging von tools/import_hd_pack.py (DATA/ und EXE/freelancer.ini).
Regeln:
  - HD-Werte gelten. Unterschiede in Format/Zahlenschreibweise werden ignoriert.
  - Dateinamen der SDK bleiben (PascalCase). Neue INIs bekommen PascalCase.
  - Verweise auf INIs zeigen auf die SDK-Namen, Verweise auf Daten sind klein
    geschrieben (Leerzeichen -> _, Planeten flach, Videos wie in NAP).
  - Korrekturen der Version 1.3.1 bleiben erhalten (siehe PATCHES).

Aufruf:
    python3 tools/import_hd_inis.py            # Bericht
    python3 tools/import_hd_inis.py --apply    # schreiben
"""
import argparse
import collections
import csv
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SDK = os.path.normpath(os.path.join(HERE, '..', 'SDK'))
STAGING = os.path.expanduser('~/Dokumente/Freelancer-HD-Staging')

ASSET_EXT = ('.3db', '.cmp', '.dfm', '.vms', '.sph', '.anm', '.mat', '.txm', '.ale', '.pte',
             '.sur', '.thn', '.page', '.wmv', '.tga', '.bmp', '.wav', '.utf', '.db', '.ttf')
HD_NAME_MAP = {'movies/fl_intro_en_hd.wmv': 'movies/fl_intro.wmv'}
BAR_NICKS = ['bar_br04', 'bar_br05', 'bar_generic04', 'bar_generic05', 'bar_generic06', 'bar_generic07',
             'bar_generic08', 'bar_generic09', 'bar_generic10', 'bar_ku03', 'bar_ku04', 'bar_ku05',
             'bar_rh02', 'bar_rh03', 'bar_rh04', 'bar_rh05']
CONCAVE_FIXES = {
    r'solar\dockable\manufacturing_platform.cmp': r'solar\dockable\manufacturing_platform_lod.cmp',
    r'solar\dockable\rh_battleship.cmp': r'ships\rheinland\rh_battleship\rh_battleship.cmp',
    r'solar\dockable\jump_gate.cmp': r'solar\dockable\jump_gatel.cmp',
}


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def key(n):
    return re.sub(r'[^a-z0-9]', '', n.lower().replace('.ini', ''))


def pascal(stem):
    if stem.lower() == 'initialworld':
        return 'InitialWorld'
    return ''.join(p[:1].upper() + p[1:] for p in re.split(r'[_\-]+', stem) if p)


def fmt(text):
    """Format der SDK: CRLF, ein Leerzeile vor Blöcken, keine Einrückung (wie in der Formatierung des Repos)."""
    raw = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    res, adj, prev_blank = [], [], True
    for raw_l in raw:
        l = raw_l.strip()
        if l == '':
            prev_blank = True
            continue
        if l.startswith('['):
            j = len(res)
            while j > 0 and res[j - 1].startswith(';') and adj[j - 1]:
                j -= 1
            head, hadj = res[j:], adj[j:]
            del res[j:], adj[j:]
            if res:
                res.append('')
                adj.append(False)
            res.extend(head)
            adj.extend(hadj)
            res.append(l)
            adj.append(False)
        else:
            res.append(l)
            adj.append(not prev_blank)
        prev_blank = False
    return '\r\n'.join(res) + '\r\n'


def num(v):
    v = v.strip()
    try:
        f = float(v)
        return repr(round(f, 4)) if f != int(f) else str(int(f))
    except ValueError:
        return re.sub(r'[\\/]+', '/', v).lower()


def records(text):
    out, sec = [], ''
    for l in text.replace('\r', '').split('\n'):
        c = l.split(';')[0].strip()
        if not c:
            continue
        if c.startswith('['):
            sec = c.lower()
            continue
        if '=' in c:
            k, v = c.split('=', 1)
            out.append((sec, k.strip().lower(), tuple(num(x) for x in v.split(','))))
        else:
            out.append((sec, c.lower(), ()))
    return out


def sdk_files():
    idx, allf = {}, {}
    for r, _, fs in os.walk(SDK):
        for f in fs:
            if not f.lower().endswith('.ini'):
                continue
            rel = os.path.relpath(os.path.join(r, f), SDK).replace(os.sep, '/')
            d = os.path.dirname(rel).lower()
            idx[(d, key(f))] = rel
            allf[rel] = os.path.join(r, f)
    return idx, allf


def hd_files(staging):
    out = {}
    data = os.path.join(staging, 'DATA')
    for r, _, fs in os.walk(data):
        for f in fs:
            if f.lower().endswith('.ini'):
                out[os.path.relpath(os.path.join(r, f), data).replace(os.sep, '/')] = os.path.join(r, f)
    fl = os.path.join(staging, 'EXE', 'freelancer.ini')
    if os.path.isfile(fl):
        out['__exe__/freelancer.ini'] = fl
    return out


def target_path(hdrel, idx):
    """Zielpfad in SDK/ (relativ) und ob die Datei neu ist."""
    if hdrel == '__exe__/freelancer.ini':
        return 'exe/Freelancer.ini', False
    d = os.path.dirname(hdrel).lower()
    base = os.path.basename(hdrel)
    k = key(base)
    if (d, k) in idx:
        return idx[(d, k)], False
    name = pascal(base[:-4].replace(' ', '_')) + '.ini'
    return (d + '/' + name) if d else name, True


def transform(text, hdrel, ref_map, bn):
    text = text.replace('\xa0', ' ')

    def fix_value(v):
        s = v.strip()
        if not s:
            return v
        lead = v[:len(v) - len(v.lstrip())]
        trail = v[len(v.rstrip()):]
        low = s.lower()
        if low.endswith(ASSET_EXT) and not low.startswith(('e:', '\\\\')):
            p = re.sub(r'[\\/]+', '/', low).replace(' ', '_')
            p = bn.rename(p)
            p = HD_NAME_MAP.get(p, p)
            return lead + p.replace('/', '\\') + trail
        if low.endswith('.ini') and not low.startswith(('e:', '\\\\')):
            parts = re.split(r'([\\/]+)', s)
            name = parts[-1]
            dirs = ''.join(parts[:-1])
            d = re.sub(r'[\\/]+', '/', dirs).strip('/').lower()
            k = key(name)
            fn = ref_map.get((d, k)) or ref_map.get(('', k)) or ref_map.get(('*', k))
            if fn:
                return lead + dirs + fn + trail
        return v

    out = []
    for line in text.split('\n'):
        if '=' in line and not line.lstrip().startswith(';'):
            head, rhs = line.split('=', 1)
            body, sep, comment = rhs.partition(';')
            vals = [fix_value(v) for v in body.split(',')]
            line = head + '=' + ','.join(vals) + (sep + comment if sep else '')
        out.append(line)
    return '\n'.join(out)


def patch(rel, text):
    low = rel.lower()
    if low.endswith('music.ini') and low.startswith('audio/'):
        lines = text.split('\n')
        nick = None
        for i, l in enumerate(lines):
            c = l.split(';')[0].strip()
            if c.lower().startswith('nickname'):
                nick = c.split('=', 1)[1].strip().lower()
            elif c.lower().startswith('file') and nick and nick.replace('music_', '', 1) in BAR_NICKS and nick.startswith('music_'):
                lines[i] = f'file = audio\\music\\{nick}.wav'
        text = '\n'.join(lines)
    if low == 'concave.ini':
        for a, b in CONCAVE_FIXES.items():
            text = re.sub(re.escape(a), lambda m, b=b: b, text, flags=re.I)
    if low.endswith('li02_01_cityscape.ini'):
        text = re.sub(r'^:gap\b', 'gap', text, flags=re.M)
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--staging', default=STAGING)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--report', help='CSV-Ausgabe')
    args = ap.parse_args()

    bn = load('build_nap')
    idx, sdk_all = sdk_files()
    hd = hd_files(args.staging)

    # Zielzuordnung und Referenztabelle
    mapping, ref_map = {}, {}
    for hdrel in hd:
        tgt, new = target_path(hdrel, idx)
        mapping[hdrel] = (tgt, new)
        d = os.path.dirname(tgt).lower()
        ref_map[(d, key(os.path.basename(tgt)))] = os.path.basename(tgt)
    for (d, k), rel in idx.items():
        ref_map.setdefault((d, k), os.path.basename(rel))
    # globale Schlüssel (eindeutig)
    byk = collections.defaultdict(set)
    for (d, k), fn in ref_map.items():
        byk[k].add(fn)
    for k, v in byk.items():
        if len(v) == 1:
            ref_map[('*', k)] = next(iter(v))

    rows, changed, new_files = [], [], []
    for hdrel, src in sorted(hd.items()):
        tgt, new = mapping[hdrel]
        text = open(src, 'rb').read().decode('latin-1')
        text = patch(tgt, transform(text, hdrel, ref_map, bn))
        out = fmt(text)
        if new:
            status = 'neu'
            new_files.append((tgt, out))
        else:
            sdkp = os.path.join(SDK, tgt)
            old = open(sdkp, 'rb').read().decode('latin-1')
            status = 'identisch' if records(old) == records(out) else 'geändert'
            if status == 'geändert':
                changed.append((tgt, out))
        rows.append((hdrel, tgt, status))

    c = collections.Counter(r[2] for r in rows)
    print('HD-INIs:', len(rows), dict(c))
    bydir = collections.Counter((os.path.dirname(t).split('/')[0] if '/' in t else '(wurzel)', s) for _, t, s in rows if s != 'identisch')
    print('geändert/neu nach Bereich:', sorted(bydir.items(), key=lambda x: -x[1])[:14])
    hd_targets = {m[0] for m in mapping.values()}
    sdk_only = sorted(r for r in sdk_all if r not in hd_targets and not r.startswith('exe/'))
    print('nur in der SDK (nicht im HD-Pack):', len(sdk_only), sdk_only[:6])

    rep = args.report or os.path.join(args.staging, 'hd-ini-report.csv')
    with open(rep, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['hd_pfad', 'sdk_pfad', 'status'])
        w.writerows(rows)
    print('Bericht:', rep)

    if not args.apply:
        print('Nur Bericht (ohne --apply nichts geschrieben).')
        return
    n = 0
    for tgt, out in changed + new_files:
        p = os.path.join(SDK, tgt)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as f:
            f.write(out.encode('latin-1', 'replace'))
        n += 1
    print('geschrieben:', n)


if __name__ == '__main__':
    main()
