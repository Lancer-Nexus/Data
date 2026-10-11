#!/usr/bin/env python3
"""Erzeugt einige Normal Maps und Cube Maps als Zusatzkarten für Texturen.

Normal Maps: aus der Helligkeit einer vorhandenen Textur abgeleitet (Höhenkarte -> Sobel,
tangentiale Normalen, +Y oben, Z nach außen), kachelbar (wrap), unkomprimiertes DDS 24 Bit mit
Mip-Kette (Normalen beim Verkleinern renormiert). Eine Bibliothek: NAP/Material/fx/normalmaps.txm,
je Karte ein Texturknoten `nm_<name>` mit einem Blatt `MIPS`.

Cube Maps: prozedural (Sterne, Sonne, Nebel), 256 px je Fläche, DDS A8R8G8B8 mit Mip-Kette,
Flächenfolge +X -X +Y -Y +Z -Z. Je Karte eine Materialbibliothek NAP/Material/fx/<name>.mat mit
einem Texturknoten `<name>` und einem Blatt `CUBE` (wie `envmapbasic.mat`).

Die Zuordnung steht in SDK/fx/SurfaceMaps.ini (diese Datei wird nicht erzeugt, nur geprüft).
Die erzeugten Dateien stehen in tools/extra_maps.txt (Schutz vor `build_nap.py`).

  python3 tools/make_surface_maps.py [--preview <Ordner>]
Voraussetzung: Pillow, numpy.
"""
import argparse
import io
import os
import struct
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import utf_write as W  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..'))
NAP = os.path.join(ROOT, 'NAP')
TEMPLATE = os.path.join(NAP, 'Material', 'fx', 'envmapbasic.mat')

# name -> (Container (NAP-relativ), Texturname, Stärke)
NORMALS = {
    # Schiffe
    'li_elite_hull':    ('Material/ships/liberty/li_playerships.mat', 'elite_256.tga', 2.5),
    'li_engine_grill':  ('Material/ships/liberty/li_playerships.mat', 'engine_grill01.tga', 3.5),
    'li_equip_gen':     ('Material/ships/liberty/li_playerships.mat', 'equip_gen.tga', 2.5),
    # Stationen und Basen
    'bw_dig_site_16':   ('Models/bases/generic/bw_pygar_airlock.cmp', 'dig_site_16.tga', 3.0),
    'bw_dig_site_18':   ('Models/bases/generic/bw_pygar_airlock.cmp', 'dig_site_18.tga', 3.0),
    'li_ceiling_gen01': ('Models/bases/liberty/li_manhattan_trader02.cmp', 'ceiling_gen01.tga021111195321', 2.5),
    # Planeten und Solar
    'planet_rock01':    ('Material/solar/planets/detailmap_rock01.txm', 'detailmap_rock01', 3.0),
    'planet_crater_hi': ('Material/solar/planets/detailmap_crater_high.txm', 'detailmap_crater_high', 3.0),
    'planet_ground01':  ('Material/solar/planets/detailmap_ground01.txm', 'detailmap_ground01', 2.5),
}
CUBES = ('envcube_space', 'envcube_sun', 'envcube_nebula')
NORMAL_SIZE = 1024
CUBE_SIZE = 256


def read_texture(container, name):
    _, root = W.load(os.path.join(NAP, container))
    for trail, leaf in W.walk(root):
        if leaf.name.upper() in ('MIPS', 'MIP0') and trail and trail[-1].lower() == name.lower():
            return Image.open(io.BytesIO(leaf.data)).convert('RGB')
    raise KeyError(f'{name} in {container}')


def height_from(img):
    a = np.asarray(img.resize((NORMAL_SIZE, NORMAL_SIZE), Image.LANCZOS), np.float32) / 255
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    # leichte Glättung (wrap), damit Kompressionsrauschen keine Körnung ergibt
    k = np.array([1, 4, 6, 4, 1], np.float32) / 16
    for ax in (0, 1):
        lum = sum(w * np.roll(lum, s, axis=ax) for s, w in zip(range(-2, 3), k))
    return lum


def normal_from_height(h, strength):
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5   # Zeilenrichtung (nach unten)
    s = strength * 8.0
    n = np.stack([-dx * s, dy * s, np.ones_like(h)], -1)   # +Y oben
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def normal_mips(n):
    out = [n]
    while out[-1].shape[0] > 1:
        p = out[-1]
        q = (p[0::2, 0::2] + p[1::2, 0::2] + p[0::2, 1::2] + p[1::2, 1::2]) / 4
        q /= np.maximum(np.linalg.norm(q, axis=-1, keepdims=True), 1e-6)
        out.append(q)
    return out


def dds_header(w, h, mips, bpp, masks, cube=False):
    flags = 0x1 | 0x2 | 0x4 | 0x8 | 0x1000 | 0x20000
    pf_flags = 0x40 | (0x1 if masks[3] else 0)
    caps1 = 0x1000 | 0x8 | 0x400000
    caps2 = 0xFE00 if cube else 0
    hd = struct.pack('<4s7I44s', b'DDS ', 124, flags, h, w, w * bpp // 8, 0, mips, b'\0' * 44)
    pf = struct.pack('<8I', 32, pf_flags, 0, bpp, *masks)
    caps = struct.pack('<5I', caps1, caps2, 0, 0, 0)
    return hd + pf + caps


def encode_normal(n):
    levels = normal_mips(n)
    body = bytearray()
    for lv in levels:
        rgb = np.clip((lv * 0.5 + 0.5) * 255 + 0.5, 0, 255).astype(np.uint8)
        body += np.ascontiguousarray(rgb[:, :, ::-1]).tobytes()   # B, G, R
    return dds_header(n.shape[1], n.shape[0], len(levels), 24, (0xFF0000, 0xFF00, 0xFF, 0)) + bytes(body)


# ---- Cube Maps ------------------------------------------------------------

def face_dirs(size):
    u = (np.arange(size) + 0.5) / size * 2 - 1
    uu, vv = np.meshgrid(u, u)
    one = np.ones_like(uu)
    faces = [
        np.stack([one, -vv, -uu], -1),      # +X
        np.stack([-one, -vv, uu], -1),      # -X
        np.stack([uu, one, vv], -1),        # +Y
        np.stack([uu, -one, -vv], -1),      # -Y
        np.stack([uu, -vv, one], -1),       # +Z
        np.stack([-uu, -vv, -one], -1),     # -Z
    ]
    return [f / np.linalg.norm(f, axis=-1, keepdims=True) for f in faces]


def value_noise(d, rng_seed, freq, octaves=4):
    rng = np.random.default_rng(rng_seed)
    out = np.zeros(d.shape[:2], np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = 8 * 2 ** o
        lat = rng.random((n, n, n), dtype=np.float32)
        p = (d * 0.5 + 0.5) * (freq * 2 ** o) % n
        i0 = np.floor(p).astype(int)
        f = p - i0
        f = f * f * (3 - 2 * f)
        i1 = (i0 + 1) % n
        i0 = i0 % n
        c = 0
        for ox in (0, 1):
            for oy in (0, 1):
                for oz in (0, 1):
                    ix = (i1 if ox else i0)[..., 0]
                    iy = (i1 if oy else i0)[..., 1]
                    iz = (i1 if oz else i0)[..., 2]
                    wgt = ((f[..., 0] if ox else 1 - f[..., 0]) * (f[..., 1] if oy else 1 - f[..., 1]) *
                           (f[..., 2] if oz else 1 - f[..., 2]))
                    c = c + lat[ix, iy, iz] * wgt
        out += c * amp
        tot += amp
        amp *= 0.5
    return out / tot


def stars(dirs, size, count, seed, tint=(1, 1, 1)):
    """Punktförmige Sterne: je Stern ein Pixel (Bildfläche), leicht weich."""
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(count, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    img = [np.zeros((size, size, 3), np.float32) for _ in range(6)]
    a = np.abs(v)
    face = np.where((a[:, 0] >= a[:, 1]) & (a[:, 0] >= a[:, 2]), np.where(v[:, 0] > 0, 0, 1),
                    np.where(a[:, 1] >= a[:, 2], np.where(v[:, 1] > 0, 2, 3), np.where(v[:, 2] > 0, 4, 5)))
    for k in range(count):
        f = face[k]
        x, y, z = v[k]
        uu, vv = {0: (-z / x, -y / x), 1: (z / -x, -y / -x), 2: (x / y, z / y), 3: (x / -y, -z / -y),
                  4: (x / z, -y / z), 5: (-x / -z, -y / -z)}[f]
        px = int((uu * 0.5 + 0.5) * size)
        py = int((vv * 0.5 + 0.5) * size)
        if 0 <= px < size and 0 <= py < size:
            b = 0.3 + 0.7 * rng.random() ** 3
            c = np.array(tint) * (0.8 + 0.2 * rng.random(3))
            img[f][py, px] = np.maximum(img[f][py, px], c * b)
    out = []
    for im in img:
        bl = im.copy()
        for ax in (0, 1):
            bl = bl + 0.25 * (np.roll(im, 1, ax) + np.roll(im, -1, ax))
        out.append(np.clip(bl, 0, 1))
    return out


def make_cube(name, size):
    dirs = face_dirs(size)
    faces = []
    sun_dir = np.array([0.6, 0.35, 0.72]); sun_dir /= np.linalg.norm(sun_dir)
    star_img = stars(dirs, size, 3500 if name != 'envcube_sun' else 1200, 11)
    for i, d in enumerate(dirs):
        if name == 'envcube_space':
            band = value_noise(d, 3, 2, 3)
            base = np.stack([0.01 + 0.03 * band, 0.012 + 0.035 * band, 0.03 + 0.07 * band], -1)
            img = base + star_img[i]
            sun = np.clip(d @ sun_dir, 0, 1) ** 400
            img += sun[..., None] * np.array([0.5, 0.5, 0.55])
        elif name == 'envcube_sun':
            dot = np.clip(d @ sun_dir, -1, 1)
            core = np.clip((dot - 0.998) / 0.002, 0, 1)
            glow = np.clip(dot, 0, 1) ** 12
            amb = 0.02 + 0.03 * np.clip(-dot, 0, 1)
            img = (np.stack([amb * 0.8, amb * 0.9, amb * 1.2], -1)
                   + glow[..., None] * np.array([0.55, 0.38, 0.2])
                   + core[..., None] * np.array([1.0, 0.95, 0.85]) * 3.0
                   + star_img[i] * 0.6)
        else:  # nebula
            n1 = value_noise(d, 5, 3, 5)
            n2 = value_noise(d, 9, 2, 4)
            m = np.clip((n1 - 0.35) * 2.2, 0, 1)
            col = np.stack([0.55 * m + 0.2 * n2 * m, 0.15 * m + 0.35 * n2 * m, 0.7 * m + 0.1 * n2], -1)
            img = col * 0.45 + 0.015 + star_img[i] * 0.7
        faces.append(np.clip(img, 0, 1))
    return faces


def encode_cube(faces):
    size = faces[0].shape[0]
    mips = 0
    s = size
    while s >= 1:
        mips += 1
        s //= 2
    body = bytearray()
    for f in faces:
        cur = f
        while True:
            bgra = np.zeros(cur.shape[:2] + (4,), np.uint8)
            q = np.clip(cur * 255 + 0.5, 0, 255).astype(np.uint8)
            bgra[..., 0], bgra[..., 1], bgra[..., 2], bgra[..., 3] = q[..., 2], q[..., 1], q[..., 0], 255
            body += bgra.tobytes()
            if cur.shape[0] == 1:
                break
            cur = (cur[0::2, 0::2] + cur[1::2, 0::2] + cur[0::2, 1::2] + cur[1::2, 1::2]) / 4
    return dds_header(size, size, mips, 32, (0xFF0000, 0xFF00, 0xFF, 0xFF000000), cube=True) + bytes(body)


# ---- UTF ------------------------------------------------------------------

def build_library(textures, leaf_name):
    """textures: {Name: bytes}. Struktur und Flags nach envmapbasic.mat."""
    header, root = W.load(TEMPLATE)
    lib = root.children[0]
    tex = lib.children[0]
    leaf = tex.children[0]
    new_lib = W.Node(lib.name, lib.flags, children=[])
    for n, data in textures.items():
        new_lib.children.append(W.Node(n, tex.flags, children=[W.Node(leaf_name, leaf.flags, data=data)]))
    return header, W.Node(root.name, root.flags, children=[new_lib])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--preview', help='Ordner für Vorschaubilder (PNG)')
    a = ap.parse_args()
    out_dir = os.path.join(NAP, 'Material', 'fx')
    made = []

    nm = {}
    previews = {}
    for key, (container, tex, strength) in NORMALS.items():
        img = read_texture(container, tex)
        n = normal_from_height(height_from(img), strength)
        nm['nm_' + key] = encode_normal(n)
        previews[key] = np.clip((n * 0.5 + 0.5) * 255, 0, 255).astype(np.uint8)
    header, root = build_library(nm, 'MIPS')
    p = os.path.join(out_dir, 'normalmaps.txm')
    W.save(p, header, root)
    made.append('Material/fx/normalmaps.txm')
    print(f'normalmaps.txm: {len(nm)} Karten, {os.path.getsize(p) / 1e6:.1f} MB')

    for c in CUBES:
        faces = make_cube(c, CUBE_SIZE)
        header, root = build_library({c: encode_cube(faces)}, 'CUBE')
        p = os.path.join(out_dir, c + '.mat')
        W.save(p, header, root)
        made.append(f'Material/fx/{c}.mat')
        print(f'{c}.mat: {os.path.getsize(p) / 1e6:.2f} MB')
        previews[c] = faces

    with open(os.path.join(HERE, 'extra_maps.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Von tools/make_surface_maps.py erzeugte Zusatzkarten (Klasse/Pfad), nicht aus der CD\n')
        f.write('\n'.join(made) + '\n')

    if a.preview:
        os.makedirs(a.preview, exist_ok=True)
        for k, v in previews.items():
            if isinstance(v, list):   # Kreuzdarstellung
                s = v[0].shape[0]
                cross = np.zeros((s * 3, s * 4, 3), np.float32)
                pos = {0: (1, 2), 1: (1, 0), 2: (0, 1), 3: (2, 1), 4: (1, 1), 5: (1, 3)}
                for i, (r, c) in pos.items():
                    cross[r * s:(r + 1) * s, c * s:(c + 1) * s] = v[i]
                Image.fromarray((np.clip(cross, 0, 1) * 255).astype(np.uint8)).save(os.path.join(a.preview, k + '.png'))
            else:
                Image.fromarray(v).resize((512, 512), Image.LANCZOS).save(os.path.join(a.preview, k + '.png'))


if __name__ == '__main__':
    main()
