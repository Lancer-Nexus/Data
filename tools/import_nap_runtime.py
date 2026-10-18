#!/usr/bin/env python3
"""Import Freelancer startup templates and resource DLLs into NAP/Runtime.

An installed HD Edition is preferred per file, with a retail installation as
fallback. Licensed source files are not tracked by Git.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_NAP = os.path.normpath(os.path.join(HERE, '..', 'NAP'))
FILES = ('newplayer.fl', 'mpnewcharacter.fl')
RESOURCE_DLLS = (
    'resources.dll', 'infocards.dll', 'misctext.dll', 'nameresources.dll',
    'equipresources.dll', 'offerbriberesources.dll', 'misctextinfo2.dll',
    'hderesources.dll',
)

sys.path.insert(0, HERE)
from atomic_file import atomic_copy


def find_case_insensitive(directory, name):
    if not os.path.isdir(directory):
        return None
    for entry in os.listdir(directory):
        if entry.casefold() == name.casefold():
            return os.path.join(directory, entry)
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hd-install-root',
                        help='lokale Freelancer-HD-Edition-Installation (wird bevorzugt)')
    parser.add_argument('--cd-install-root', required=True,
                        help='lokale Retail/CD-Installation als Rückfallquelle')
    parser.add_argument('--nap', default=REPO_NAP, help='NAP-Zielordner')
    parser.add_argument('--dry-run', action='store_true', help='nur Quelle und Aktion anzeigen')
    args = parser.parse_args()

    nap = os.path.abspath(args.nap)
    roots = []
    for label, value in (('HD', args.hd_install_root), ('CD', args.cd_install_root)):
        if value:
            root = os.path.abspath(os.path.expanduser(value))
            exe = find_case_insensitive(root, 'EXE')
            if exe is None:
                parser.error(f'{label}-EXE-Ordner nicht gefunden: {root}')
            roots.append((label, exe))
    if not roots:
        parser.error('Mindestens eine lokale Installation muss angegeben sein')

    sources = []
    for name in FILES:
        source = None
        for label, exe in roots:
            candidate = find_case_insensitive(exe, name)
            if candidate and os.path.isfile(candidate) and os.path.getsize(candidate) > 0:
                source = (label, candidate)
                break
        if source is None:
            parser.error(f'{name} fehlt in allen angegebenen EXE-Ordnern')
        sources.append((name, source[0], source[1], os.path.join(nap, 'Runtime', name)))

    for name in RESOURCE_DLLS:
        selected = None
        for label, exe in roots:
            candidate = find_case_insensitive(exe, name)
            if candidate and os.path.isfile(candidate) and os.path.getsize(candidate) > 0:
                selected = (label, candidate)
                break
        if selected is None:
            if name.casefold() == 'hderesources.dll':
                print(f'nicht vorhanden (in HD-Installation optional): {name}')
                continue
            parser.error(f'{name} fehlt in allen angegebenen EXE-Ordnern')
        sources.append((name, selected[0], selected[1], os.path.join(nap, 'Runtime', name)))

    # Validate the complete input set before writing any destination.
    for name, label, source, destination in sources:
        state = 'würde importieren' if args.dry_run else 'importiert'
        print(f'{state} ({label}): {source} -> {destination} ({os.path.getsize(source)} Bytes)')
        if not args.dry_run:
            atomic_copy(source, destination)


if __name__ == '__main__':
    main()
