#!/usr/bin/env python3
"""Phase 5: Texturmaße und Verweise prüfen.

1. Maße aller .txm (Texturbibliotheken) in NAP/ lesen.
2. Fassung vergleichen: CD-Original gegen das, was in NAP/ liegt (HD oder CD).
3. INI-Koordinaten ([Shape] x, y, w, h) gegen die Größe der referenzierten Textur prüfen.
4. Texturnamen in .mat (Dt_name usw.) gegen vorhandene Texturen prüfen.

Aufruf:  python3 tools/check_textures.py [--cd <Ordner mit CD-Daten>] [--out textur-pruefung.md]
"""
import argparse
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import utf_textures as ut  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..'))
NAP = os.path.join(ROOT, 'NAP')
SDK = os.path.join(ROOT, 'SDK')


def nap_index():
    idx = {}
    for c in os.listdir(NAP):
        base = os.path.join(NAP, c)
        if not os.path.isdir(base):
            continue
        for r, _, fs in os.walk(base):
            for f in fs:
                rel = os.path.relpath(os.path.join(r, f), base).replace(os.sep, '/').lower()
                idx[rel] = (c, os.path.join(r, f))
    return idx


def cd_index(cd):
    idx = {}
    for r, _, fs in os.walk(cd):
        for f in fs:
            p = os.path.join(r, f)
            rel = os.path.relpath(p, cd).replace(os.sep, '/')
            m = re.match(r'cab\d/cab\d/data/(.*)', rel, re.I)
            if m:
                idx[m.group(1).lower().replace(' ', '_')] = p
    return idx


def load_overrides():
    p = os.path.join(HERE, 'hd_overrides.txt')
    s = set()
    if os.path.isfile(p):
        for l in open(p, encoding='utf-8'):
            l = l.strip()
            if l and not l.startswith('#'):
                s.add(re.sub(r'^[^/]+/', '', l.lower()))
    return s


def material_textures(path):
    """Texturnamen, auf die ein .mat verweist (Dt_name, Et_name, ...)."""
    b, data_off, root = ut.parse(path)
    names = set()

    def walk(n):
        for c in n.children:
            if not (c.flags & 0x10) and c.name.lower().endswith('_name'):
                blob = b[data_off + c.child:data_off + c.child + c.size]
                s = blob.split(b'\0')[0].decode('latin-1').strip().lower()
                if s:
                    names.add(s)
            elif c.flags & 0x10:
                walk(c)
    walk(root)
    return names


def shapes_in(ini_text):
    """Liefert ({texturname: datei}, [Form-Dict]). Formen ohne texture_name gehören zur zuletzt
    deklarierten Textur (`_tex`)."""
    tex, out, cur, last_tex = {}, [], None, ''
    for raw in ini_text.replace('\r', '').split('\n'):
        c = raw.split(';')[0].strip()
        if not c:
            continue
        if c.startswith('['):
            if cur and cur[0] == 'shape':
                out.append(cur[1])
            sec = c.strip('[]').lower()
            cur = (sec, {}) if sec in ('shape', 'texture') else None
            if cur and sec == 'shape':
                cur[1]['_tex'] = last_tex
            continue
        if cur and '=' in c:
            k, v = c.split('=', 1)
            k, v = k.strip().lower(), v.strip()
            cur[1][k] = v
            if cur[0] == 'texture' and k == 'name':
                last_tex = v.lower()
            if cur[0] == 'texture' and 'name' in cur[1] and 'file' in cur[1]:
                tex[cur[1]['name'].lower()] = re.sub(r'[\\/]+', '/', cur[1]['file']).lower()
    if cur and cur[0] == 'shape':
        out.append(cur[1])
    return tex, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cd', default=os.path.expanduser(
        '/tmp/claude-1000/-home-masterbee-Dokumente-GitHub-Lancer-Nexus-LN-Data-SDK/a3140e15-4fcc-46e7-bf49-849dccc87094/scratchpad/cd'))
    ap.add_argument('--out', default=os.path.join(ROOT, 'textur-pruefung.md'))
    a = ap.parse_args()

    idx = nap_index()
    cd = cd_index(a.cd) if os.path.isdir(a.cd) else {}
    ov = load_overrides()

    # 1+2: Maße und Versionen
    inv, rows, changed, unreadable = {}, [], [], []
    names_all = set()
    for rel, (cls, p) in sorted(idx.items()):
        if not rel.endswith('.txm'):
            continue
        try:
            t = ut.textures(p)
        except Exception as e:  # noqa: BLE001
            unreadable.append((rel, str(e)))
            continue
        inv[rel] = t
        names_all.update(t)
        src = 'HD' if rel in ov else 'CD'
        cdt = None
        if rel in cd:
            try:
                cdt = ut.textures(cd[rel])
            except Exception:  # noqa: BLE001
                cdt = None
        for name, (w, h, fmt) in sorted(t.items()):
            ow = cdt.get(name) if cdt else None
            rows.append((rel, name, f'{w}x{h}', fmt, src, f'{ow[0]}x{ow[1]}' if ow else ''))
            if ow and (ow[0], ow[1]) != (w, h):
                changed.append((rel, name, f'{ow[0]}x{ow[1]}', f'{w}x{h}'))

    # Eingebettete Texturen in Modellen und Materialien (für die Namensauflösung)
    for rel, (cls, p) in sorted(idx.items()):
        if rel.endswith(('.3db', '.cmp', '.sph', '.mat', '.dfm', '.vms')):
            try:
                names_all.update(ut.textures(p))
            except Exception:  # noqa: BLE001
                pass
    base = lambda s: re.sub(r'\.(tga|dds|bmp)$', '', s)
    names_base = {base(n) for n in names_all}
    files_base = {base(os.path.basename(k)) for k in idx if k.endswith(('.tga', '.dds', '.bmp'))}

    # Standalone .tga/.bmp
    for rel, (cls, p) in sorted(idx.items()):
        if rel.endswith('.tga'):
            d = ut._dims(open(p, 'rb').read(64))
            if d:
                rows.append((rel, '(Datei)', f'{d[0]}x{d[1]}', d[2], 'HD' if rel in ov else 'CD', ''))

    # 3: Shape-Koordinaten gegen Texturgröße
    bad_shapes, shape_total, unknown_tex = [], 0, collections.Counter()
    extents = {}   # (ini, texturname) -> [maxX, maxY, texdatei]
    for r, _, fs in os.walk(SDK):
        for f in fs:
            if not f.lower().endswith('.ini'):
                continue
            path = os.path.join(r, f)
            text = open(path, 'rb').read().decode('latin-1')
            if '[Shape]' not in text and '[shape]' not in text.lower():
                continue
            tex, shapes = shapes_in(text)
            for s in shapes:
                try:
                    x, y, w, h = (float(s.get(k, 'nan')) for k in ('x', 'y', 'w', 'h'))
                except ValueError:
                    continue
                if any(v != v for v in (x, y, w, h)):
                    continue
                tn = (s.get('texture_name') or s.get('_tex') or s.get('name') or '').lower()
                fp = tex.get(tn)
                if not fp:
                    unknown_tex[(os.path.relpath(path, SDK), tn)] += 1
                    continue
                shape_total += 1
                dims = inv.get(fp, {}).get(tn) or inv.get(fp, {}).get(tn + '_0')   # animierte Texturen: Name + _0
                if not dims:
                    unknown_tex[(os.path.relpath(path, SDK), tn)] += 1
                    continue
                W, H = dims[0], dims[1]
                ek = (os.path.relpath(path, SDK).replace(os.sep, '/'), tn)
                e = extents.setdefault(ek, [0, 0, fp, W, H])
                e[0] = max(e[0], x + w)
                e[1] = max(e[1], y + h)
                if x + w > W or y + h > H:
                    bad_shapes.append((os.path.relpath(path, SDK).replace(os.sep, '/'),
                                       s.get('shape_name') or s.get('name'), tn, f'{int(x)},{int(y)} {int(w)}x{int(h)}', f'{W}x{H}'))

    # Formen decken nur einen Teil der Textur ab (INI für die CD-Größe, Textur ist größer)
    partial = []
    for (ini, tn), (mx, my, fp, W, H) in sorted(extents.items()):
        if W >= 2 * mx and H >= 2 * my and mx > 0 and my > 0:
            cdd = None
            if fp in cd:
                try:
                    cdd = ut.textures(cd[fp]).get(tn)
                except Exception:  # noqa: BLE001
                    cdd = None
            partial.append((ini, tn, f'{int(mx)}x{int(my)}', f'{W}x{H}', f'{cdd[0]}x{cdd[1]}' if cdd else ''))

    # 4: Materialien -> Texturnamen
    unresolved = collections.defaultdict(set)
    mat_total = 0
    for rel, (cls, p) in sorted(idx.items()):
        if not rel.endswith('.mat'):
            continue
        try:
            names = material_textures(p)
        except Exception:  # noqa: BLE001
            continue
        mat_total += len(names)
        for n in names:
            if base(n) not in names_base and base(n) not in files_base:
                unresolved[rel].add(n)

    # Bericht
    L = ['# Texturprüfung (Phase 5)', '',
         f'Geprüft: {len(inv)} Texturbibliotheken (`.txm`), {sum(len(v) for v in inv.values())} Texturen, '
         f'{shape_total} Formen, {mat_total} Texturnamen in Materialien.', '']
    src = collections.Counter((r[4]) for r in rows if r[2] != '')
    L += ['## Zusammenfassung', '', '| Prüfung | Ergebnis |', '|---|---:|',
          f'| Texturen mit anderer Größe als im CD-Original | {len(changed)} |',
          f'| Formen außerhalb der Textur | {len(bad_shapes)} |',
          f'| Texturen, die von den Formen nur zur Hälfte abgedeckt werden | {len(partial)} |',
          f'| Texturnamen in Materialien ohne Textur | {sum(len(v) for v in unresolved.values())} |',
          f'| nicht lesbare Dateien | {len(unreadable)} |', '']
    if changed:
        dist = collections.Counter((o, m) for _, _, o, m in changed)
        L += ['## Verteilung der Größenänderungen', '', '| CD | NAP | Texturen |', '|---|---|---:|']
        L += [f'| {o} | {m} | {n} |' for (o, m), n in dist.most_common()]
        L.append('')
    if changed:
        L += ['## Texturen mit geänderter Größe (CD → NAP)', '', '| Datei | Textur | CD | NAP |', '|---|---|---|---|']
        L += [f'| `{r}` | `{n}` | {o} | {m} |' for r, n, o, m in sorted(changed)]
        L.append('')
    if bad_shapes:
        L += ['## Formen außerhalb der Textur', '', '| INI | Form | Textur | Rechteck | Textur-Größe |', '|---|---|---|---|---|']
        L += [f'| `{i}` | `{s}` | `{t}` | {r} | {d} |' for i, s, t, r, d in bad_shapes[:200]]
        L.append('')
    if partial:
        L += ['## Formen decken nur einen Teil der Textur ab', '',
              'Die Rechtecke der Formen reichen nur bis zur halben Texturgröße oder weniger. Das deutet auf eine INI für eine kleinere Textur hin.',
              '', '| INI | Textur | Ausdehnung der Formen | Textur | CD-Original |', '|---|---|---|---|---|']
        L += [f'| `{i}` | `{n}` | {m} | {d} | {c} |' for i, n, m, d, c in partial]
        L.append('')
    if unresolved:
        L += ['## Texturnamen ohne Textur', '', '| Material | Namen |', '|---|---|']
        L += [f'| `{k}` | {", ".join(sorted(v)[:6])} |' for k, v in sorted(unresolved.items())[:120]]
        L.append('')
    if unreadable:
        L += ['## Nicht lesbar', ''] + [f'- `{r}`: {e}' for r, e in unreadable]
    open(a.out, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    print('Bericht:', a.out)
    print('Texturen:', sum(len(v) for v in inv.values()), '| geänderte Größe:', len(changed),
          '| Formen außerhalb:', len(bad_shapes), '/', shape_total, '| nur teilweise abgedeckt:', len(partial),
          '| Namen ohne Textur:', sum(len(v) for v in unresolved.values()), '| nicht lesbar:', len(unreadable))
    print('unbekannte Texturzuordnung (Formen):', sum(unknown_tex.values()))


if __name__ == '__main__':
    main()
