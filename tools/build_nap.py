#!/usr/bin/env python3
"""Baut NAP/ aus der Freelancer-CD neu auf.

Quelle: die ISO-Datei oder ein Verzeichnis mit CAB1.CAB und CAB2.CAB (z. B. die gemountete CD).
Ergebnis: alle Nicht-INI-Daten aus den `data`-Ordnern beider CABs, klein geschrieben und
in Klassencontainern NAP/<Klasse>/<Pfad> abgelegt (siehe classes.md). Die INIs kommen
anschließend über tools/sync_inis_to_nap.py aus SDK/ dazu.

Mehrfach ausführbar: vorhandene Dateien mit gleichem Inhalt bleiben unberührt, geänderte
werden überschrieben, Dateien, die nicht mehr aus der Quelle stammen, werden entfernt
(--no-prune schaltet das ab).

Aufruf:
    python3 tools/build_nap.py --source ~/Downloads/Freelancer.iso
    python3 tools/build_nap.py --source /media/masterbee/Freelancer --dry-run
    python3 tools/build_nap.py                       # fragt nach der ISO (Dateidialog)
"""
import argparse
import filecmp
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_NAP = os.path.normpath(os.path.join(HERE, '..', 'NAP'))
SYNC = os.path.join(HERE, 'sync_inis_to_nap.py')

# Dateien, die bewusst nicht in NAP/ liegen (rel. Pfad klein geschrieben, ohne Klasse).
EXCLUDE = {
    'missions/m01a/mission1 readme.doc',
    'missions/m01b/mission1 readme.doc',
}

# Klasse nach Dateiendung (Vorrang) und nach Hauptordner, wie in classes.md.
EXT_CLASS = {
    '.wav': 'Sounds', '.utf': 'Sounds',
    '.wmv': 'Video',
    '.mat': 'Material', '.txm': 'Material', '.tga': 'Material', '.bmp': 'Material',
    '.3db': 'Models', '.cmp': 'Models', '.dfm': 'Models', '.vms': 'Models', '.sph': 'Models', '.anm': 'Models',
    '.ale': 'Effects', '.pte': 'Effects',
    '.thn': 'Script',
    '.page': 'UI', '.sur': 'UI',
    '.db': 'System',
}
DIR_CLASS = {
    'audio': 'Sounds', 'movies': 'Video', 'fx': 'Effects', 'ai': 'System',
    'interface': 'UI', 'screens': 'UI', 'scripts': 'Script', 'missions': 'Mission',
    'universe': 'World', 'solar': 'World', 'bases': 'World', 'randommissions': 'World',
    'cockpits': 'Equipment', 'equipment': 'Equipment', 'ships': 'Equipment',
    'characters': 'Equipment', 'fonts': 'Equipment',
}
CLASS_OF_TOP_FALLBACK = 'Models'


def ask_source():
    """Fragt über einen Dateidialog nach der ISO (zenity). Ohne Oberfläche: Eingabe im Terminal."""
    if shutil.which('zenity') and os.environ.get('DISPLAY'):
        r = subprocess.run(['zenity', '--file-selection',
                            '--title=Freelancer-CD-Abbild (ISO) auswählen',
                            '--file-filter=ISO-Abbild | *.iso *.ISO',
                            '--file-filter=Alle Dateien | *'],
                           capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            sys.exit('Abgebrochen: keine ISO ausgewählt.')
        return r.stdout.strip()
    path = input('Pfad zur Freelancer-ISO (oder Ordner mit CAB1.CAB/CAB2.CAB): ').strip()
    if not path:
        sys.exit('Abgebrochen: kein Pfad angegeben.')
    return path


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode not in (0, 1):  # 7z: 1 = Warnungen
        sys.exit(f'Fehler: {" ".join(cmd)}\n{r.stderr or r.stdout}')
    return r


def find_cabs(source, work):
    """Gibt die Pfade zu CAB1.CAB und CAB2.CAB zurück. Bei einer ISO werden sie vorher entpackt."""
    if os.path.isdir(source):
        names = {n.upper(): n for n in os.listdir(source)}
        cabs = [os.path.join(source, names[n]) for n in ('CAB1.CAB', 'CAB2.CAB') if n in names]
    elif os.path.isfile(source):
        cabdir = os.path.join(work, 'cabs')
        os.makedirs(cabdir, exist_ok=True)
        run(['7z', 'x', '-y', '-bso0', '-bsp0', source, 'CAB1.CAB', 'CAB2.CAB', f'-o{cabdir}'])
        cabs = [os.path.join(cabdir, n) for n in sorted(os.listdir(cabdir))]
    else:
        sys.exit(f'Quelle nicht gefunden: {source}')
    if len(cabs) != 2:
        sys.exit(f'CAB1.CAB und CAB2.CAB nicht gefunden in: {source}')
    return sorted(cabs)


def extract_data(cabs, work):
    """Entpackt die data-Ordner ohne INIs. Gibt Wurzel mit Unterordnern cab1/ cab2/ zurück."""
    out = os.path.join(work, 'extract')
    for cab in cabs:
        name = os.path.basename(cab).lower().replace('.cab', '')
        tgt = os.path.join(out, name)
        # Der Ordnername im CAB ist z. B. Cab1/data; Wildcards mit / funktionieren in 7z.
        top = name.capitalize()
        run(['7z', 'x', '-y', '-bso0', '-bsp0', cab, f'{top}/data/*', '-xr!*.ini', '-xr!*.INI', f'-o{tgt}'])
    return out


def collect(extract_root):
    """Liste (quelle, rel_klein) für alle Datendateien. Bricht bei Kollisionen ab."""
    items = {}
    for cab in sorted(os.listdir(extract_root)):
        base = os.path.join(extract_root, cab)
        for r, _, fs in os.walk(base):
            for f in fs:
                src = os.path.join(r, f)
                rel = os.path.relpath(src, base).replace(os.sep, '/')
                # Präfix "<Cab>/data/" entfernen
                parts = rel.split('/')
                if len(parts) < 3 or parts[1].lower() != 'data':
                    continue
                rel = '/'.join(parts[2:]).lower()
                if rel in items:
                    sys.exit(f'Kollision zwischen CABs: {rel}')
                items[rel] = src
    return items


def classify(rel):
    ext = os.path.splitext(rel)[1].lower()
    if ext in EXT_CLASS:
        return EXT_CLASS[ext]
    top = rel.split('/')[0]
    if top == 'scripts':
        return 'Script'
    return DIR_CLASS.get(top, CLASS_OF_TOP_FALLBACK)


def same_file(a, b):
    return os.path.getsize(a) == os.path.getsize(b) and filecmp.cmp(a, b, shallow=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', help='ISO-Datei oder Verzeichnis mit CAB1.CAB und CAB2.CAB (ohne Angabe: Dateidialog)')
    ap.add_argument('--nap', default=REPO_NAP, help='Zielordner (Standard: LN-Data/NAP)')
    ap.add_argument('--dry-run', action='store_true', help='nur anzeigen, nichts schreiben oder löschen')
    ap.add_argument('--no-prune', action='store_true', help='Dateien, die nicht mehr aus der Quelle stammen, behalten')
    ap.add_argument('--no-sync', action='store_true', help='INIs nicht aus SDK/ übernehmen')
    ap.add_argument('--work', help='Arbeitsordner (Standard: temporär, wird danach gelöscht)')
    ap.add_argument('--keep-work', action='store_true', help='Arbeitsordner behalten')
    args = ap.parse_args()

    source = os.path.abspath(os.path.expanduser(args.source or ask_source()))
    nap = os.path.abspath(args.nap)
    work = args.work or tempfile.mkdtemp(prefix='build_nap_')
    os.makedirs(work, exist_ok=True)
    try:
        cabs = find_cabs(source, work)
        print('Quelle:', ', '.join(os.path.basename(c) for c in cabs))
        extract_root = extract_data(cabs, work)
        items = collect(extract_root)
        target = {}
        for rel, src in items.items():
            if rel in EXCLUDE:
                continue
            target[f'{classify(rel)}/{rel}'] = src
        print(f'Datendateien aus der Quelle: {len(items)}, ausgeschlossen: {len(items) - len(target)}')

        # Bestehende Nicht-INI-Dateien in den Klassen
        existing = {}
        if os.path.isdir(nap):
            for cls in os.listdir(nap):
                cdir = os.path.join(nap, cls)
                if not os.path.isdir(cdir):
                    continue
                for r, _, fs in os.walk(cdir):
                    for f in fs:
                        if f.lower().endswith('.ini'):
                            continue
                        key = os.path.relpath(os.path.join(r, f), nap).replace(os.sep, '/')
                        existing[key] = os.path.join(r, f)

        new = [k for k in target if k not in existing]
        changed = [k for k in target if k in existing and not same_file(target[k], existing[k])]
        same = len(target) - len(new) - len(changed)
        stale = [k for k in existing if k not in target] if not args.no_prune else []
        print(f'neu {len(new)}, geändert {len(changed)}, unverändert {same}, entfernen {len(stale)}')

        if args.dry_run:
            for k in new[:20]:
                print('  [neu]', k)
            for k in changed[:20]:
                print('  [geändert]', k)
            for k in stale[:20]:
                print('  [entfernen]', k)
            return

        for k in new + changed:
            dst = os.path.join(nap, k)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(target[k], dst)
        for k in stale:
            os.remove(existing[k])
        # leere Ordner in den Klassen entfernen
        for cls in (os.listdir(nap) if os.path.isdir(nap) else []):
            cdir = os.path.join(nap, cls)
            if os.path.isdir(cdir):
                for r, ds, fs in os.walk(cdir, topdown=False):
                    if r != cdir and not os.listdir(r):
                        os.rmdir(r)
        print('Daten übernommen.')

        if not args.no_sync and os.path.abspath(nap) == REPO_NAP:
            subprocess.run([sys.executable, SYNC], check=True)
    finally:
        if not args.keep_work and not args.work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    main()
