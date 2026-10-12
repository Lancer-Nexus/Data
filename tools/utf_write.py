#!/usr/bin/env python3
"""Schreibt Freelancer-UTF-Container (.txm, .mat, .3db, .cmp ...) neu.

Ergänzung zu utf_textures.py (nur Lesen). Der Baum wird vollständig geladen, Blätter lassen sich
ersetzen, `save()` baut Baum, Namenstabelle und Datenblock neu auf. Der Kopf (Bytes vor dem Baum)
wird übernommen und nur in den Offset-/Größenfeldern angepasst.

Selbsttest: `python3 tools/utf_write.py --selftest <datei> ...` lädt, speichert, liest erneut
und vergleicht Baum und Daten.
"""
import struct
import sys

from atomic_file import atomic_open

ENTRY = struct.Struct('<11I')  # next, name, flags, zero, child/data, alloc, size, size2, t1, t2, t3


class Node:
    __slots__ = ('name', 'flags', 'children', 'data')

    def __init__(self, name, flags, children=None, data=None):
        self.name = name
        self.flags = flags
        self.children = children
        self.data = data

    @property
    def is_dir(self):
        return self.children is not None


def load(path):
    """-> (header_bytes, root). header_bytes = alles vor dem Baum."""
    b = open(path, 'rb').read()
    if b[:4] != b'UTF ':
        raise ValueError('kein UTF')
    tree_off, tree_size, _, entry_size, names_off, _, _, data_off = struct.unpack_from('<8I', b, 8)
    if entry_size != 44:
        raise ValueError(f'unerwartete Eintragsgröße {entry_size}')

    def entry(off):
        return struct.unpack_from('<8I', b, tree_off + off)

    def name_at(o):
        e = b.index(b'\0', names_off + o)
        return b[names_off + o:e].decode('latin-1')

    def read_chain(off):
        res = []
        while True:
            nxt, nm, flags, _, cd, _, size, _ = entry(off)
            if flags & 0x10:
                n = Node(name_at(nm), flags, children=read_chain(cd) if cd else [])
            else:
                n = Node(name_at(nm), flags, data=b[data_off + cd:data_off + cd + size])
            res.append(n)
            if nxt == 0:
                return res
            off = nxt

    return b[:tree_off], read_chain(0)[0]


def save(path, header, root):
    names = bytearray()
    name_off = {}

    def nm(s):
        if s not in name_off:
            name_off[s] = len(names)
            names.extend(s.encode('latin-1') + b'\0')
        return name_off[s]

    nm(root.name)  # Wurzelname zuerst (Offset 0)
    # Einträge in Breitensuche: Geschwister eines Verzeichnisses liegen zusammenhängend.
    order = [root]
    child_pos = {}  # id(dir) -> Index des ersten Kindes
    i = 0
    while i < len(order):
        n = order[i]
        if n.is_dir and n.children:
            child_pos[id(n)] = len(order)
            order.extend(n.children)
        i += 1
    index = {id(n): k for k, n in enumerate(order)}
    sib_next = {}
    for n in order:
        if n.is_dir:
            for a, c in zip(n.children, n.children[1:]):
                sib_next[id(a)] = index[id(c)]
    data = bytearray()
    entries = bytearray()
    for n in order:
        nxt = sib_next.get(id(n), 0) * 44
        if n.is_dir:
            cd = child_pos.get(id(n), 0) * 44
            size = 0
        else:
            cd = len(data)
            size = len(n.data)
            data.extend(n.data)
            data.extend(b'\0' * ((-len(data)) % 4))
        entries.extend(ENTRY.pack(nxt, nm(n.name), n.flags, 0, cd, size, size, size, 0, 0, 0))
    # Namen in Reihenfolge der Einträge bereits vergeben; entries sind schon gepackt
    used = len(names)
    names.extend(b'\0' * ((-len(names)) % 4))
    tree_off = len(header)
    names_off = tree_off + len(entries)
    data_off = names_off + len(names)
    h = bytearray(header)
    struct.pack_into('<II', h, 8, tree_off, len(entries))
    struct.pack_into('<III', h, 24, names_off, len(names), used)
    struct.pack_into('<I', h, 36, data_off)
    with atomic_open(path, 'wb') as f:
        f.write(bytes(h) + bytes(entries) + bytes(names) + bytes(data))


def walk(node, trail=()):
    """Alle Blätter: (Pfad-Tupel der Verzeichnisnamen, Knoten)."""
    for c in node.children:
        if c.is_dir:
            yield from walk(c, trail + (c.name,))
        else:
            yield trail, c


def _selftest(path):
    import os
    import tempfile
    h, r = load(path)
    tmp = os.path.join(tempfile.mkdtemp(), 'x')
    save(tmp, h, r)
    h2, r2 = load(tmp)

    def flat(n, p=''):
        if n.is_dir:
            out = [(p + '/' + n.name, None, n.flags)]
            for c in n.children:
                out += flat(c, p + '/' + n.name)
            return out
        return [(p + '/' + n.name, n.data, n.flags)]
    return flat(r) == flat(r2)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--selftest':
        bad = 0
        for p in sys.argv[2:]:
            ok = _selftest(p)
            bad += not ok
            print('OK ' if ok else 'FEHLER', p)
        sys.exit(1 if bad else 0)
    print(__doc__)
