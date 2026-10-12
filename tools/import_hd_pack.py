#!/usr/bin/env python3
"""Importiert das HD-Pack (freelancer-hd-edition) in NAP/.

Quelle ist der Git-Stand (HEAD) des HD-Repos, nicht der Arbeitsbaum. Es werden
DATA/ (ohne INIs) und EXE/freelancer.ini exportiert. INIs gehören zu SDK/ und
werden getrennt behandelt (siehe PLAN-hd-pack.md, Phase 3).

Ablauf:
  1. Export von HEAD in einen Staging-Ordner (außerhalb des Repos).
  2. Manifest: HD-Pfad -> NAP/<Klasse>/<Pfad> mit Aktion (gleich / überschreiben / neu).
  3. Mit --apply werden 'überschreiben' und 'neu' nach NAP/ kopiert und
     tools/hd_overrides.txt aktualisiert.

Aufruf:
    python3 tools/import_hd_pack.py --hd-repo ~/Dokumente/GitHub/freelancer-hd-edition
    python3 tools/import_hd_pack.py --hd-repo ... --apply
"""
import argparse
import csv
import filecmp
import importlib.util
import os
import shutil
import subprocess
import sys
import collections

from atomic_file import atomic_copy, atomic_open
import utf_write

HERE = os.path.dirname(os.path.abspath(__file__))
NAP = os.path.normpath(os.path.join(HERE, '..', 'NAP'))
OVERRIDES = os.path.join(HERE, 'hd_overrides.txt')

# Namen im HD-Pack, die auf unsere Dateinamen abgebildet werden (klein geschrieben, relativ zu DATA/).
HD_NAME_MAP = {
    'movies/fl_intro_en_hd.wmv': 'movies/fl_intro.wmv',
}


def load_build_nap():
    spec = importlib.util.spec_from_file_location('build_nap', os.path.join(HERE, 'build_nap.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def export_head(hd_repo, staging):
    os.makedirs(staging, exist_ok=True)
    marker = os.path.join(staging, '.exported')
    head = subprocess.run(['git', '-C', hd_repo, 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    if os.path.isfile(marker) and open(marker).read().strip() == head:
        return head
    for sub in ('DATA', 'EXE'):
        shutil.rmtree(os.path.join(staging, sub), ignore_errors=True)
    # DATA vollständig, aus EXE nur freelancer.ini
    p = subprocess.Popen(['git', '-C', hd_repo, 'archive', 'HEAD', 'DATA', 'EXE/freelancer.ini'], stdout=subprocess.PIPE)
    extraction = subprocess.run(['tar', '-x', '-C', staging], stdin=p.stdout)
    p.stdout.close()
    if p.wait() != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)
    extraction.check_returncode()
    with atomic_open(marker, 'w') as f:
        f.write(head)
    return head


def same(a, b):
    return os.path.getsize(a) == os.path.getsize(b) and filecmp.cmp(a, b, shallow=False)


def build_manifest(staging, bn):
    rows = []
    targets = collections.defaultdict(list)
    data = os.path.join(staging, 'DATA')
    for r, _, fs in os.walk(data):
        for f in fs:
            src = os.path.join(r, f)
            rel = os.path.relpath(src, data).replace(os.sep, '/')
            low = rel.lower()
            if low.endswith('.ini'):
                rows.append((rel, '', '', 'ini', 'INI: Phase 3 (SDK)', src))
                continue
            norm = bn.rename(low)            # Leerzeichen, Planeten, Detailmaps
            norm = HD_NAME_MAP.get(norm, norm)
            cls = bn.classify(low)
            key = f'{cls}/{norm}'
            targets[key].append(rel)
            dst = os.path.join(NAP, cls, norm)
            if os.path.isfile(dst):
                action = 'gleich' if same(src, dst) else 'überschreiben'
            else:
                action = 'neu'
            rows.append((rel, cls, norm, action, '', src))
    conflicts = {k: v for k, v in targets.items() if len(v) > 1}
    return rows, conflicts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hd-repo', required=True, help='Pfad zum lokalen HD-Repo')
    ap.add_argument('--staging', default=os.path.expanduser('~/Dokumente/Freelancer-HD-Staging'))
    ap.add_argument('--manifest', help='CSV-Ausgabe (Standard: <staging>/hd-manifest.csv)')
    ap.add_argument('--apply', action='store_true', help='Dateien nach NAP/ kopieren')
    args = ap.parse_args()

    hd_repo = os.path.abspath(os.path.expanduser(args.hd_repo))
    staging = os.path.abspath(os.path.expanduser(args.staging))
    head = export_head(hd_repo, staging)
    print('HD-Stand:', head)

    bn = load_build_nap()
    rows, conflicts = build_manifest(staging, bn)
    manifest = args.manifest or os.path.join(staging, 'hd-manifest.csv')
    with open(manifest, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['hd_pfad', 'klasse', 'ziel', 'aktion', 'grund'])
        for rel, cls, norm, action, reason, _ in rows:
            w.writerow([rel, cls, norm, action, reason])
    print('Manifest:', manifest)

    c = collections.Counter(r[3] for r in rows)
    print('Aktionen:', dict(c))
    byext = collections.Counter((r[3], os.path.splitext(r[0])[1].lower()) for r in rows if r[3] in ('überschreiben', 'neu'))
    print('überschreiben/neu nach Endung:', byext.most_common(12))
    if conflicts:
        print('KONFLIKTE:', len(conflicts), list(conflicts.items())[:3])
        sys.exit(1)

    if not args.apply:
        print('Nur Manifest (ohne --apply nichts geschrieben).')
        return

    # Validate all HD source files before changing any installed asset.
    for rel, cls, norm, action, _, src in rows:
        if action not in ('überschreiben', 'neu', 'gleich'):
            continue
        if os.path.getsize(src) == 0:
            raise ValueError(f'Leere HD-Quelldatei: {rel}')
        with open(src, 'rb') as stream:
            magic = stream.read(4)
        if magic == b'UTF ':
            utf_write.load(src)

    n = 0
    applied = []
    for rel, cls, norm, action, _, src in rows:
        if action not in ('überschreiben', 'neu'):
            continue
        dst = os.path.join(NAP, cls, norm)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        atomic_copy(src, dst)
        applied.append(f'{cls}/{norm}')
        n += 1
    existing = set()
    if os.path.isfile(OVERRIDES):
        existing = {l.strip() for l in open(OVERRIDES, encoding='utf-8') if l.strip() and not l.startswith('#')}
    # alle HD-Dateien (auch bereits gleiche) gelten als Ausnahmen
    allhd = {f'{r[1]}/{r[2]}' for r in rows if r[3] in ('überschreiben', 'neu', 'gleich')}
    merged = sorted(existing | allhd)
    with atomic_open(OVERRIDES, 'w', encoding='utf-8') as f:
        f.write('# HD-Dateien in NAP/, die build_nap.py nicht überschreibt und nicht entfernt (Format: Klasse/Pfad).\n')
        f.write('\n'.join(merged) + '\n')
    print(f'kopiert: {n} Dateien; Ausnahmeliste: {len(merged)} Einträge')


if __name__ == '__main__':
    main()
