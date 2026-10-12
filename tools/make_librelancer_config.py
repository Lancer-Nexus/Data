#!/usr/bin/env python3
"""Convert SDK Freelancer.ini to a librelancer.ini for the virtual NAP root."""
import argparse
from pathlib import Path

from atomic_file import atomic_open


def convert(source, skip_movies=False, omit_hde=False):
    section = ''
    lines = []
    found_resources = False
    found_data = False
    for line in source.splitlines():
        value = line.split(';', 1)[0].strip()
        if value.startswith('[') and value.endswith(']'):
            section = value[1:-1].casefold()
            lines.append(line)
            if section == 'resources':
                if found_resources:
                    raise ValueError('duplicate Resources section')
                found_resources = True
                lines.append('DLL = resources.dll ; explicit index 0 for librelancer.ini')
            continue
        if '=' in value:
            key, entry = (part.strip().casefold() for part in value.split('=', 1))
            if section == 'freelancer' and key == 'data path':
                line = 'data path = DATA'
                found_data = True
            if section == 'resources' and key == 'dll':
                if entry == 'resources.dll' or (omit_hde and entry == 'hderesources.dll'):
                    continue
            if skip_movies and section == 'startup' and key == 'movie_file':
                continue
        lines.append(line)
    if not found_resources or not found_data:
        raise ValueError('Freelancer data path or Resources section missing')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1] / 'SDK/exe/Freelancer.ini')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--skip-movies', action='store_true')
    parser.add_argument('--omit-hde-resources', action='store_true', help='local smoke only when the final HD Edition resource DLL is unavailable')
    args = parser.parse_args()
    if args.output.name.casefold() != 'librelancer.ini' or args.source.resolve() == args.output.resolve():
        parser.error('output must be a separate librelancer.ini')
    source = args.source.read_bytes()
    try:
        text = source.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = source.decode('cp1252')
    converted = convert(text, args.skip_movies, args.omit_hde_resources)
    with atomic_open(args.output, 'w', encoding='utf-8', newline='\n') as stream:
        stream.write(converted)
    print(f'Created {args.output}; supply the resource DLLs in the configured order')


if __name__ == '__main__':
    main()
