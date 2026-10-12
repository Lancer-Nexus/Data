#!/usr/bin/env python3
"""Check Surface UTF bounds and DDS mip/cube payload sizes (no visual proof)."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct


def dds_info(data):
    if len(data) < 128 or data[:4] != b'DDS ':
        raise ValueError('DDS header missing or truncated')
    if struct.unpack_from('<I', data, 4)[0] != 124 or struct.unpack_from('<I', data, 76)[0] != 32:
        raise ValueError('invalid DDS header sizes')
    height, width = struct.unpack_from('<II', data, 12)
    mips = max(1, struct.unpack_from('<I', data, 28)[0])
    if not width or not height or mips > max(width, height).bit_length():
        raise ValueError('invalid DDS dimensions or mip count')
    flags = struct.unpack_from('<I', data, 80)[0]
    fourcc = data[84:88]
    blocks = {b'DXT1': 8, b'DXT3': 16, b'DXT5': 16, b'ATI1': 8,
              b'ATI2': 16, b'BC4U': 8, b'BC5U': 16}
    bits = struct.unpack_from('<I', data, 88)[0]
    if flags & 4 and fourcc not in blocks:
        raise ValueError(f'unsupported DDS format {fourcc!r}')
    if not flags & 4 and bits not in (8, 16, 24, 32):
        raise ValueError(f'unsupported DDS pixel size {bits}')
    caps = struct.unpack_from('<I', data, 112)[0]
    if caps & 0x200000:
        raise ValueError('volume DDS not supported by this Surface check')
    faces = 6 if caps & 0x200 else 1
    if faces == 6 and (caps & 0xfc00 != 0xfc00 or width != height):
        raise ValueError('cube must contain six square faces')
    expected = 128
    w, h = width, height
    for _ in range(mips):
        expected += faces * (((w + 3) // 4) * ((h + 3) // 4) * blocks[fourcc]
                             if flags & 4 else ((w * bits + 7) // 8) * h)
        w, h = max(1, w // 2), max(1, h // 2)
    if len(data) != expected:
        raise ValueError(f'DDS payload size {len(data)}, expected {expected}')
    return {'format': fourcc.decode('ascii') if flags & 4 else f'RGB{bits}',
            'width': width, 'height': height, 'mips': mips, 'faces': faces}


def check_utf(path):
    data = path.read_bytes()
    if len(data) < 40 or data[:4] != b'UTF ':
        raise ValueError('UTF header missing or truncated')
    tree, size, _, entry_size, names, names_size, _, payload = struct.unpack_from('<8I', data, 8)
    if entry_size != 44 or size % 44 or tree < 40 or tree + size > len(data):
        raise ValueError('invalid UTF tree bounds')
    if names < tree + size or names + names_size > payload or payload > len(data):
        raise ValueError('invalid UTF names/data bounds')
    visited = set()
    textures = []

    def chain(offset):
        while True:
            if offset in visited or offset % 44 or offset + 44 > size:
                raise ValueError('invalid or cyclic UTF entry')
            visited.add(offset)
            nxt, name, flags, _, child, _, length, *_ = struct.unpack_from('<11I', data, tree + offset)
            if name >= names_size or data.find(b'\0', names + name, names + names_size) < 0:
                raise ValueError('invalid UTF name')
            if flags & 0x10:
                if child:
                    chain(child)
            else:
                if child + length > len(data) - payload:
                    raise ValueError('UTF leaf exceeds file bounds')
                leaf = data[payload + child:payload + child + length]
                if leaf[:4] == b'DDS ':
                    textures.append(dds_info(leaf))
            if not nxt:
                break
            offset = nxt

    chain(0)
    if not textures:
        raise ValueError('no DDS textures in Surface library')
    return textures


def check_ini_links(surface):
    import utf_write
    sections = []
    for ini in sorted(surface.rglob('*.ini')):
        current = None
        for line in ini.read_text(encoding='utf-8-sig').splitlines():
            line = line.split(';', 1)[0].strip()
            if line.startswith('[') and line.endswith(']'):
                current = {'section': line[1:-1].casefold(), 'source': ini.name}
                sections.append(current)
            elif '=' in line and current is not None:
                key, value = line.split('=', 1)
                current[key.strip().casefold()] = value.strip()
    libraries, nodes, errors = {}, {}, []

    def texture_names(relative):
        path = (surface / relative.replace('\\', '/')).resolve()
        path.relative_to(surface.resolve())
        if path not in nodes:
            _, root = utf_write.load(path)
            nodes[path] = {trail[-1].casefold() for trail, leaf in utf_write.walk(root)
                           if trail and leaf.data[:4] == b'DDS '}
        return nodes[path]

    for section in sections:
        if section['section'] == 'texture':
            try:
                libraries[section['name'].casefold()] = texture_names(section['file'])
            except (KeyError, OSError, ValueError, struct.error) as error:
                errors.append({'path': section['source'], 'error': f'library: {error}'})
    references = 0
    for section in sections:
        try:
            if section['section'] == 'normalmap':
                available = libraries[section['library'].casefold()]
                for key in ('map', 'roughness_map', 'metallic_map'):
                    if key == 'map' or key in section:
                        references += 1
                        if section[key].casefold() not in available:
                            raise ValueError(f"missing {key}: {section[key]}")
            elif section['section'] == 'cubemap':
                references += 1
                if section['nickname'].casefold() not in texture_names(section['file']):
                    raise ValueError(f"missing cube: {section['nickname']}")
        except (KeyError, OSError, ValueError, struct.error) as error:
            errors.append({'path': section['source'], 'error': f'mapping: {error}'})
    return references, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--surface', type=Path, default=Path(__file__).resolve().parents[1] / 'NAP/Surface')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    records, errors, formats = [], [], collections.Counter()
    files = sorted(path for path in args.surface.rglob('*') if path.is_file() and path.name != '.gitkeep')
    if not files:
        errors.append({'path': str(args.surface), 'error': 'no Surface files'})
    for path in files:
        record = {'path': path.relative_to(args.surface).as_posix(), 'bytes': path.stat().st_size}
        try:
            if not record['bytes']:
                raise ValueError('empty file')
            if path.suffix.lower() in ('.txm', '.mat'):
                textures = check_utf(path)
                record['textures'] = len(textures)
                for item in textures:
                    formats[item['format']] += 1
            record['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        except (ValueError, struct.error) as error:
            errors.append({'path': record['path'], 'error': str(error)})
        records.append(record)
    references = None
    if not errors:
        references, link_errors = check_ini_links(args.surface)
        errors.extend(link_errors)
    result = {'scope': 'UTF bounds, DDS mip/cube payload sizes and Surface INI target nodes; no diffuse matching, active snapshot or visual validation',
              'iniNodeReferences': references,
              'files': records, 'formats': dict(formats), 'errors': errors}
    if args.output:
        from atomic_file import atomic_open
        with atomic_open(args.output, 'w', encoding='utf-8') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    print(f'{len(files)} Surface files; {sum(formats.values())} DDS textures; {len(errors)} errors')
    for error in errors[:10]:
        print(f"  {error['path']}: {error['error']}")
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
