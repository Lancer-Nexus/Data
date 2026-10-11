#!/usr/bin/env python3
"""Kopiert die INI-Dateien aus SDK/ in die Klassencontainer unter NAP/.

Zielpfad: NAP/<Klasse>/<Pfad der INI>, z. B. SDK/audio/Sounds.ini -> NAP/Sounds/audio/Sounds.ini.

Die Klasse richtet sich nach dem Hauptordner, wie in classes.md beschrieben.
INIs im Wurzelverzeichnis von SDK/ gehen nach System/. Der Ordner exe/ wird ausgelassen,
weil er keine Spieldaten enthält.

Mehrfach ausführbar: identische Zieldateien bleiben unberührt, geänderte werden überschrieben.
Es wird nichts gelöscht.

Aufruf:
    python3 tools/sync_inis_to_nap.py            # ausführen
    python3 tools/sync_inis_to_nap.py --dry-run  # nur anzeigen
"""
import argparse
import collections
import filecmp
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SDK_DIR = os.path.normpath(os.path.join(HERE, '..', 'SDK'))
NAP_DIR = os.path.normpath(os.path.join(HERE, '..', 'NAP'))
ROOT_CLASS = 'System'
SKIP_TOP = {'exe'}


def rel_dir(path):
    """Verzeichnis eines relativen Pfads mit '/' als Trenner ('' für die Wurzel)."""
    return os.path.dirname(path).replace(os.sep, '/')


# Klasse je Hauptordner, wie in classes.md beschrieben. Ordner, die dort nicht stehen,
# gehen nach Models (Ausnahme: die Wurzel von SDK/ nach System).
DIR_CLASS = {
    'audio': 'Sounds',
    'ai': 'System',
    'interface': 'UI',
    'screens': 'UI',
    'cockpits': 'UI',
    'fonts': 'UI',
    'scripts': 'Script',
    'fx': 'Effects',
    'movies': 'Video',
    'missions': 'Mission',
    'universe': 'World',
    'solar': 'World',
    'bases': 'World',
    'randommissions': 'World',
    'ships': 'Models',
    'equipment': 'Models',
    'characters': 'Models',
}


def pick_class(rel):
    """Klasse einer INI anhand ihres Hauptordners. INIs in der Wurzel gehen nach System."""
    top = rel.split('/')[0]
    if os.path.basename(rel).lower().startswith('surfacemaps') and rel.lower().startswith('fx/'):
        return 'Shader'   # Zusatzkarten (Normal/Roughness/Metallic/Cube) liegen in eigener Klasse
    if '/' not in rel:
        return ROOT_CLASS
    return DIR_CLASS.get(top, 'Models')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='nur anzeigen, nichts kopieren')
    args = ap.parse_args()

    if not os.path.isdir(SDK_DIR):
        sys.exit(f'SDK-Ordner nicht gefunden: {SDK_DIR}')
    if not os.path.isdir(NAP_DIR):
        sys.exit(f'NAP-Ordner nicht gefunden: {NAP_DIR}')

    stats = collections.Counter()
    per_class = collections.Counter()

    for r, ds, fs in os.walk(SDK_DIR):
        ds[:] = sorted(d for d in ds if not (r == SDK_DIR and d in SKIP_TOP))
        for f in sorted(fs):
            if not f.lower().endswith('.ini'):
                continue
            src = os.path.join(r, f)
            rel = os.path.relpath(src, SDK_DIR).replace(os.sep, '/')
            cls = pick_class(rel)
            dst = os.path.join(NAP_DIR, cls, rel)
            if os.path.isfile(dst):
                if filecmp.cmp(src, dst, shallow=False):
                    stats['unveraendert'] += 1
                    continue
                action = 'aktualisiert'
            else:
                action = 'neu'
            stats[action] += 1
            per_class[cls] += 1
            if args.dry_run:
                print(f'[{action}] {cls}/{rel}')
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

    mode = 'Testlauf' if args.dry_run else 'Fertig'
    print(f'{mode}: neu {stats["neu"]}, aktualisiert {stats["aktualisiert"]}, '
          f'unveraendert {stats["unveraendert"]}')
    if per_class:
        print('nach Klasse:', ', '.join(f'{k} {v}' for k, v in sorted(per_class.items())))


if __name__ == '__main__':
    main()
