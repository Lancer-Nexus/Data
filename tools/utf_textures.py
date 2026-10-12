#!/usr/bin/env python3
"""Liest Texturen (Breite, Höhe, Format) aus Freelancer-UTF-Dateien (.txm, .mat, .3db, .cmp ...).

UTF: Kopf mit 'UTF ', Baum aus 44-Byte-Einträgen, Namenstabelle, Datenblock.
Texturbibliotheken (.txm) enthalten je Textur einen Knoten mit 'MIPS' (DDS/TGA) oder 'MIP0'.
"""
import os
import struct

HEADER = struct.Struct('<4sIIIIIIIIII')  # sig, ver, tree_off, tree_size, ?, entry_size, names_off, names_alloc, names_used, data_off


class Node:
    __slots__ = ('name', 'flags', 'child', 'size', 'offset', 'children')

    def __init__(self):
        self.children = []


def parse(path):
    b = open(path, 'rb').read()
    if b[:4] != b'UTF ':
        raise ValueError('kein UTF')
    ver, tree_off, tree_size, _, entry_size, names_off, _, names_used, data_off = struct.unpack_from('<IIIIIIIII', b, 4)
    nodes = {}
    pos = tree_off
    end = tree_off + tree_size
    entries = []
    while pos + entry_size <= end:
        nxt, name_off, flags, _, child_or_data, alloc, size, size2 = struct.unpack_from('<8I', b, pos)
        n = Node()
        n.flags = flags
        n.child = child_or_data
        n.size = size
        n.offset = pos - tree_off
        e = b.index(b'\0', names_off + name_off)
        n.name = b[names_off + name_off:e].decode('latin-1')
        entries.append((pos - tree_off, nxt, n))
        nodes[pos - tree_off] = (nxt, n)
        pos += entry_size

    def children(off):
        res = []
        while True:
            nxt, n = nodes[off]
            res.append(n)
            if nxt == 0:
                break
            off = nxt
        return res

    def build(n):
        if n.flags & 0x10 and n.child:
            n.children = children(n.child)
            for c in n.children:
                build(c)
        return n

    root = build(nodes[0][1])
    return b, data_off, root


def _dims(blob):
    if blob[:4] == b'DDS ' and len(blob) >= 20:
        h, w = struct.unpack_from('<II', blob, 12)
        fourcc = blob[84:88].decode('latin-1').strip('\0') if len(blob) >= 88 else ''
        return w, h, 'DDS' + (':' + fourcc if fourcc else '')
    if len(blob) >= 18:
        # TGA: Typ 2/10 (Truecolor), Breite/Höhe an Offset 12
        t = blob[2]
        w, h = struct.unpack_from('<HH', blob, 12)
        bpp = blob[16]
        if t in (1, 2, 3, 9, 10, 11) and 0 < w <= 8192 and 0 < h <= 8192:
            return w, h, f'TGA{bpp}'
    return None


def textures(path):
    """{texturname_klein: (breite, hoehe, format)} aus einer .txm (oder anderen UTF mit Texturknoten)."""
    b, data_off, root = parse(path)
    out = {}

    def walk(n, trail):
        for c in n.children:
            low = c.name.lower()
            if not (c.flags & 0x10):
                blob = b[data_off + c.child:data_off + c.child + c.size]
                d = _dims(blob)
                if d and low in ('mips', 'mip0'):
                    out[trail[-1].name.lower()] = d
            else:
                walk(c, trail + [c])
    walk(root, [root])
    return out


if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        for k, v in sorted(textures(p).items()):
            print(f'{os.path.basename(p)}\t{k}\t{v[0]}x{v[1]}\t{v[2]}')
