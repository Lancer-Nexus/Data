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
  python3 tools/make_surface_maps.py --llm http://localhost:1234/v1 [--llm-model NAME] [--vision]

Parameter: Standardwerte stehen unten (NORMALS, CUBE_DEFAULTS). Gewählte Werte werden in
tools/surface_maps_params.json gespeichert und bei späteren Läufen ohne `--llm` wiederverwendet
(Läufe sind damit reproduzierbar). Mit `--llm` wählt ein Sprachmodell über eine OpenAI-kompatible
API (z. B. LM Studio) die Parameter je Karte als JSON. Es erzeugt keine Pixel. Die Antwort wird
gegen Grenzwerte geprüft, bei Fehlern oder ohne Server gelten die bisherigen Werte.
Voraussetzung: Pillow, numpy (für `--llm` nichts weiter, nur urllib).
"""
import argparse
import base64
import io
import json
import os
import struct
import sys
import urllib.error
import urllib.request

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import utf_write as W  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..'))
NAP = os.path.join(ROOT, 'NAP')
TEMPLATE = os.path.join(NAP, 'Material', 'fx', 'envmapbasic.mat')

# name -> (Container (NAP-relativ), Texturname, Stärke, Glättung, Beschreibung für das Sprachmodell)
NORMALS = {
    # Schiffe
    'li_elite_hull':    ('Material/ships/liberty/li_playerships.mat', 'elite_256.tga', 2.5, 1, 'Rumpfplatten eines Liberty-Spielerschiffs'),
    'li_engine_grill':  ('Material/ships/liberty/li_playerships.mat', 'engine_grill01.tga', 3.5, 1, 'Triebwerksgitter, runde Öffnungen'),
    'li_equip_gen':     ('Material/ships/liberty/li_playerships.mat', 'equip_gen.tga', 2.5, 1, 'Ausrüstungsplatten und Bedienfelder'),
    # Stationen und Basen
    'bw_dig_site_16':   ('Models/bases/generic/bw_pygar_airlock.cmp', 'dig_site_16.tga', 3.0, 1, 'Stationshülle Bretonia, Metallpaneele'),
    'bw_dig_site_18':   ('Models/bases/generic/bw_pygar_airlock.cmp', 'dig_site_18.tga', 3.0, 1, 'Stationshülle Bretonia, Metallpaneele'),
    'li_ceiling_gen01': ('Models/bases/liberty/li_manhattan_trader02.cmp', 'ceiling_gen01.tga021111195321', 2.5, 1, 'Deckenplatten einer Liberty-Basis'),
    'ku_k_panel01':     ('Material/ships/kusari/ku_playerships.mat', 'k_panel01_256.tga', 2.5, 1, 'Rumpfpaneele eines Kusari-Spielerschiffs'),
    'ku_k_wings':       ('Material/ships/kusari/ku_playerships.mat', 'k_wings.tga', 2.5, 1, 'Tragflächen eines Kusari-Schiffs'),
    'ku_metal03':       ('Material/ships/kusari/ku_playerships.mat', 'metal03.tga', 2.5, 1, 'allgemeine Metallfläche'),
    'br_player01':      ('Material/ships/bretonia/br_playerships.mat', 'b_player01_256.tga', 2.5, 1, 'Rumpf eines Bretonia-Spielerschiffs'),
    # Asteroiden (Gesteinsoberfläche; Billboards wie asteroid_belt_04 und Stadtkulissen sind ungeeignet)
    'ast_rock_4':       ('Material/solar/asteroids/rock_roids.txm', 'asteroid_rock_4', 3.0, 1, 'Gesteinsoberfläche eines Asteroiden'),
    # Planeten und Solar
    'planet_ice':       ('Material/solar/planets/detailmap_ice.txm', 'detailmap_ice', 3.0, 1, 'kachelnde Eisdetailkarte'),
    'planet_lava':      ('Material/solar/planets/detailmap_lava.txm', 'detailmap_lava', 3.0, 1, 'kachelnde Lavadetailkarte'),
    'planet_rock01':    ('Material/solar/planets/detailmap_rock01.txm', 'detailmap_rock01', 3.0, 1, 'kachelnde Felsdetailkarte eines Planeten'),
    'planet_crater_hi': ('Material/solar/planets/detailmap_crater_high.txm', 'detailmap_crater_high', 3.0, 1, 'kachelnde Kraterdetailkarte'),
    'planet_ground01':  ('Material/solar/planets/detailmap_ground01.txm', 'detailmap_ground01', 2.5, 1, 'kachelnde Bodendetailkarte'),
}
# Cube Maps: Art und Parameter. Standardwerte entsprechen der ersten Fassung.
CUBE_DEFAULTS = {
    'envcube_space': {'kind': 'space', 'desc': 'dunkler Weltraum mit vielen Sternen, schwacher Sonne und blauem Hauch',
                      'star_count': 3500, 'star_gain': 1.0, 'sun_dir': [0.6, 0.35, 0.72], 'sun_color': [0.5, 0.5, 0.55],
                      'sun_exp': 400, 'ambient': [0.01, 0.012, 0.03], 'seed': 11},
    'envcube_sun': {'kind': 'sun', 'desc': 'warme Sonne mit Schein, dunkler Umgebung, wenig Sternen',
                    'star_count': 1200, 'star_gain': 0.6, 'sun_dir': [0.6, 0.35, 0.72], 'sun_color': [0.55, 0.38, 0.2],
                    'sun_exp': 12, 'ambient': [0.016, 0.018, 0.024], 'seed': 11},
    'envcube_nebula': {'kind': 'nebula', 'desc': 'violetter Nebel mit kühlen Blautönen und Sternen',
                       'star_count': 3500, 'star_gain': 0.7, 'sun_dir': [0.6, 0.35, 0.72], 'sun_color': [0.55, 0.15, 0.7],
                       'sun_exp': 12, 'ambient': [0.015, 0.015, 0.015], 'seed': 11,
                       'nebula_a': [0.55, 0.15, 0.7], 'nebula_b': [0.2, 0.35, 0.1], 'nebula_cover': 0.35},
}
CUBES = tuple(CUBE_DEFAULTS)
NORMAL_SIZE = 1024
CUBE_SIZE = 256
PARAMS_FILE = os.path.join(HERE, 'surface_maps_params.json')


def read_texture(container, name):
    _, root = W.load(os.path.join(NAP, container))
    for trail, leaf in W.walk(root):
        if leaf.name.upper() in ('MIPS', 'MIP0') and trail and trail[-1].lower() == name.lower():
            return Image.open(io.BytesIO(leaf.data)).convert('RGB')
    raise KeyError(f'{name} in {container}')


def height_from(img, smooth=1):
    a = np.asarray(img.resize((NORMAL_SIZE, NORMAL_SIZE), Image.LANCZOS), np.float32) / 255
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    # leichte Glättung (wrap), damit Kompressionsrauschen keine Körnung ergibt
    k = np.array([1, 4, 6, 4, 1], np.float32) / 16
    for _ in range(int(smooth)):
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


# ---- Bewertung und Anpassung -----------------------------------------------

TARGET_P95 = 28.0          # Ziel: 95 % der Pixel neigen höchstens so viel (Grad)
GOOD_P95 = (12.0, 40.0)


def _blur3(a):
    return (a + np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5


def grad_mag(h):
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5
    return np.hypot(dx, dy)


def metrics(h, strength):
    g = grad_mag(h) * strength * 8.0
    tilt = np.degrees(np.arctan(g))
    b3 = _blur3(h)
    b15 = b3
    for _ in range(5):
        b15 = _blur3(b15)
    grain = float(np.std(h - b3) / max(np.std(b3 - b15), 1e-6))
    inner = np.abs(np.diff(h, axis=1)).mean() + 1e-6
    seam = float(max(np.abs(h[:, 0] - h[:, -1]).mean(), np.abs(h[0] - h[-1]).mean()) / inner)
    return {'mean': float(tilt.mean()), 'p95': float(np.percentile(tilt, 95)),
            'steep': float((tilt > 60).mean()), 'flat': float((tilt < 1).mean()),
            'grain': grain, 'seam': seam}


def verdict(m, tiling=False):
    issues = []
    if m['p95'] < GOOD_P95[0]:
        issues.append('zu flach')
    if m['p95'] > GOOD_P95[1]:
        issues.append('zu steil')
    if m['steep'] > 0.01:
        issues.append('über 1 % Pixel steiler als 60°')
    if m['flat'] > 0.85:
        issues.append('kaum Relief')
    if m['grain'] > 1.5:
        issues.append('körnig')
    if tiling and m['seam'] > 2.5:
        issues.append('sichtbare Naht beim Kacheln')
    return issues or ['gut']


def tune(h):
    """Stärke so wählen, dass p95 der Neigung bei TARGET_P95 liegt; bei Körnung eine Glättung mehr."""
    g = grad_mag(h) * 8.0
    g95, g99 = float(np.percentile(g, 95)), float(np.percentile(g, 99))
    if g95 <= 1e-9:
        return 1.0
    s = min(np.tan(np.radians(TARGET_P95)) / g95, np.tan(np.radians(60.0)) / max(g99, 1e-9))   # p99 höchstens 60°
    return float(np.clip(s, NORMAL_LIMITS['strength'][0], NORMAL_LIMITS['strength'][1]))


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


def make_cube(size, p):
    """p: Parameter (siehe CUBE_DEFAULTS). Art: space | sun | nebula."""
    dirs = face_dirs(size)
    sun_dir = np.array(p['sun_dir'], np.float64)
    sun_dir /= np.linalg.norm(sun_dir)
    star_img = stars(dirs, size, int(p['star_count']), int(p['seed']))
    amb = np.array(p['ambient'], np.float32)
    sun_col = np.array(p['sun_color'], np.float32)
    faces = []
    for i, d in enumerate(dirs):
        dot = np.clip(d @ sun_dir, -1, 1)
        if p['kind'] == 'space':
            band = value_noise(d, 3, 2, 3)
            img = amb + band[..., None] * np.array([0.03, 0.035, 0.07], np.float32)
            img = img + star_img[i] * p['star_gain']
            img += (np.clip(dot, 0, 1) ** p['sun_exp'])[..., None] * sun_col
        elif p['kind'] == 'sun':
            core = np.clip((dot - 0.998) / 0.002, 0, 1)
            glow = np.clip(dot, 0, 1) ** p['sun_exp']
            img = (amb * (1 + 1.5 * np.clip(-dot, 0, 1))[..., None]
                   + glow[..., None] * sun_col
                   + core[..., None] * np.array([1.0, 0.95, 0.85]) * 3.0
                   + star_img[i] * p['star_gain'])
        else:  # nebula
            n1 = value_noise(d, 5, 3, 5)
            n2 = value_noise(d, 9, 2, 4)
            m = np.clip((n1 - p.get('nebula_cover', 0.35)) * 2.2, 0, 1)
            a_, b_ = np.array(p.get('nebula_a', sun_col), np.float32), np.array(p.get('nebula_b', [0.2, 0.35, 0.1]), np.float32)
            col = m[..., None] * a_ + (n2 * m)[..., None] * b_
            img = col * 0.45 + amb + star_img[i] * p['star_gain']
        faces.append(np.clip(img, 0, 1).astype(np.float32))
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


# ---- Parameterwahl durch ein Sprachmodell (optional) ------------------------

NORMAL_LIMITS = {'strength': (0.5, 6.0), 'smooth': (0, 3)}
CUBE_LIMITS = {'star_count': (100, 8000), 'star_gain': (0.0, 1.5), 'sun_exp': (4, 600), 'seed': (0, 9999)}
VEC_KEYS = {'sun_dir': (-1.0, 1.0), 'sun_color': (0.0, 1.0), 'ambient': (0.0, 0.2),
            'nebula_a': (0.0, 1.0), 'nebula_b': (0.0, 1.0)}


def clamp_normal(d, base):
    out = dict(base)
    for k, (lo, hi) in NORMAL_LIMITS.items():
        try:
            out[k] = min(max(float(d[k]), lo), hi)
        except (KeyError, TypeError, ValueError):
            pass
    out['smooth'] = int(round(out['smooth']))
    return out


def clamp_cube(d, base):
    out = dict(base)
    if d.get('kind') in ('space', 'sun', 'nebula'):
        out['kind'] = d['kind']
    for k, (lo, hi) in CUBE_LIMITS.items():
        try:
            v = min(max(float(d[k]), lo), hi)
            out[k] = int(v) if k in ('star_count', 'seed') else v
        except (KeyError, TypeError, ValueError):
            pass
    for k, (lo, hi) in VEC_KEYS.items():
        v = d.get(k)
        if isinstance(v, list) and len(v) == 3:
            try:
                out[k] = [min(max(float(x), lo), hi) for x in v]
            except (TypeError, ValueError):
                pass
    if all(abs(x) < 1e-6 for x in out['sun_dir']):
        out['sun_dir'] = list(base['sun_dir'])
    cov = d.get('nebula_cover')
    if isinstance(cov, (int, float)):
        out['nebula_cover'] = min(max(float(cov), 0.15), 0.7)
    return out


class Llm:
    """Minimaler OpenAI-kompatibler Client (Chat Completions), z. B. LM Studio unter http://localhost:1234/v1."""

    def __init__(self, base, model=None, timeout=180):
        self.base = base.rstrip('/')
        self.timeout = timeout
        self.model = model or self._first_model()

    def _req(self, path, body=None):
        r = urllib.request.Request(self.base + path, data=None if body is None else json.dumps(body).encode(),
                                   headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(r, timeout=self.timeout) as f:
            return json.loads(f.read().decode('utf-8'))

    def _first_model(self):
        data = self._req('/models').get('data') or []
        if not data:
            raise RuntimeError('der Server meldet kein geladenes Modell')
        return data[0]['id']

    def json_answer(self, system, user, image_png=None):
        content = [{'type': 'text', 'text': user}]
        if image_png:
            content.append({'type': 'image_url',
                            'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(image_png).decode()}})
        body = {'model': self.model, 'temperature': 0, 'max_tokens': 600,
                'messages': [{'role': 'system', 'content': system},
                             {'role': 'user', 'content': content if image_png else user}]}
        text = self._req('/chat/completions', body)['choices'][0]['message']['content']
        text = text.strip()
        if text.startswith('```'):
            text = text.strip('`')
            text = text[text.index('{'):] if '{' in text else text
        i, j = text.find('{'), text.rfind('}')
        if i < 0 or j < i:
            raise ValueError('keine JSON-Antwort')
        return json.loads(text[i:j + 1])


SYS_NORMAL = ('Du stellst Parameter für die Ableitung einer Normal Map aus einer Spieltextur ein (Raumschiff-Spiel). '
              'Antworte nur mit einem JSON-Objekt: {"strength": Zahl 0.5-6, "smooth": ganze Zahl 0-3}. '
              'strength: Tiefe des Reliefs (harte Paneele und Gitter 3-4, feine Körnung 1-2). '
              'smooth: Glättungsdurchgänge gegen Rauschen (0 für scharfe Grafik, 2-3 für grobe Kompressionsartefakte).')
SYS_CUBE = ('Du stellst Parameter für eine prozedurale Cube Map (Weltraum-Umgebungsspiegelung) ein. '
            'Antworte nur mit einem JSON-Objekt mit den Schlüsseln: kind ("space"|"sun"|"nebula"), '
            'star_count (100-8000), star_gain (0-1.5), sun_dir [x,y,z], sun_color [r,g,b] (0-1), sun_exp (4-600, '
            'größer = kleinerer Schein), ambient [r,g,b] (0-0.2), nebula_a [r,g,b], nebula_b [r,g,b], '
            'nebula_cover (0.15-0.7, kleiner = mehr Nebel). Nicht genannte Schlüssel weglassen.')


def image_stats(img):
    a = np.asarray(img.convert('L').resize((256, 256)), np.float32) / 255
    gx = np.abs(np.diff(a, axis=1)).mean()
    gy = np.abs(np.diff(a, axis=0)).mean()
    return f'mittlere Helligkeit {a.mean():.2f}, Kontrast (Standardabweichung) {a.std():.2f}, Kantendichte {(gx + gy) / 2:.3f}'


def load_params():
    if os.path.isfile(PARAMS_FILE):
        with open(PARAMS_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {}


INI_HEADER = """; SurfaceMaps.ini - Zusatzkarten (Normal Maps, Cube Maps) zu Texturen.
; Nachbau fuer Lancer Nexus, im Original-Freelancer nicht vorhanden. Der Original-Client ignoriert diese Datei.
; Wird von tools/make_surface_maps.py erzeugt (Werte aus tools/surface_maps_params.json).
; Einlesen und Anwenden: Aufgabe der Engine (siehe TODO-surface-maps.md, Client/docs/surface-maps.md).
;
; [Texture]    Bibliothek, aus der Karten stammen (wie in den Shape-INIs).
;   file       Pfad der .txm
;   name       Name der Bibliothek, auf den [NormalMap] verweist
; [NormalMap]  Normal Map zu einer Diffuse-Textur (Dt_name im Material)
;   texture    Name der Diffuse-Textur (ohne Beachtung der Gross-/Kleinschreibung)
;   library    Name aus [Texture]
;   map        Texturknoten in der Bibliothek (tangentiale Normalen, RGB, +Y oben, Z nach aussen)
;   strength   Staerke der Abweichung, 1.0 = unveraendert, 0 = aus
; [CubeMap]    Cube Map als Umgebungsspiegelung. Bindung ueber vorhandene Schluessel in
;              ships\\Shiparch.ini und solar\\SolarArch.ini:
;                material_library = <file>
;                envmap_material  = <nickname>
;   nickname   Name des Texturknotens in der .mat (= envmap_material)
;   file       Pfad der .mat (= material_library)
;   kind       Hinweis: space | sun | nebula
;   strength   Vorschlag fuer die Staerke der Spiegelung (0..1)

[Texture]
file = fx\\normalmaps.txm
name = surface_normalmaps
"""
CUBE_STRENGTH = {'space': 0.35, 'sun': 0.5, 'nebula': 0.4}


def write_ini(path, normals, cubes):
    """normals: {key: (Textur, Beschreibung, params)}, cubes: {name: params}."""
    out = [INI_HEADER]
    for key, (tex, desc, pr) in normals.items():
        out.append(f"\n; {desc}\n[NormalMap]\ntexture = {tex}\nlibrary = surface_normalmaps\n"
                   f"map = nm_{key}\nstrength = {pr['strength']:g}\n")
    for name, pr in cubes.items():
        out.append(f"\n[CubeMap]\nnickname = {name}\nfile = fx\\{name}.mat\nkind = {pr['kind']}\n"
                   f"strength = {CUBE_STRENGTH[pr['kind']]:g}\n")
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(out))


def write_report(rows, tuned, path):
    L = ['# Bewertung der Normal Maps', '',
         'Erzeugt von `tools/make_surface_maps.py --evaluate` bzw. `--tune`. Die Kennzahlen beschreiben die erzeugten Karten, nicht ihre Wirkung im Spiel.', '',
         '| Kennzahl | Bedeutung | Zielbereich |', '|---|---|---|',
         '| Neigung Mittel / p95 | Winkel der Normalen gegen die Fläche (Grad); p95 = 95 % der Pixel neigen höchstens so | p95 12 bis 40 (Ziel 28) |',
         '| steil | Anteil der Pixel mit mehr als 60° | höchstens 1 % |',
         '| flach | Anteil der Pixel mit weniger als 1° | höchstens 85 % |',
         '| Körnung | Energie des Pixelrauschens im Verhältnis zur mittleren Struktur | höchstens 1,5 |',
         '| Naht | Kantenunterschied beim Kacheln im Verhältnis zum Nachbarpixel; nur für die kachelnden Planetenkarten bewertet | höchstens 2,5 |', '',
         '| Karte | Quelle | Stärke | Glättung | Neigung Mittel / p95 | steil | flach | Körnung | Naht | Urteil |',
         '|---|---|---:|---:|---|---:|---:|---:|---:|---|']
    for key, tex, base, m0, pr, m1 in rows:
        m = m1
        L.append(f"| `{key}` | `{tex}` | {pr['strength']:.2f} | {pr['smooth']} | {m['mean']:.1f}° / {m['p95']:.1f}° | "
                 f"{m['steep'] * 100:.1f} % | {m['flat'] * 100:.0f} % | {m['grain']:.2f} | "
                 f"{(format(m['seam'], '.2f') if key.startswith('planet_') else '–')} | {', '.join(verdict(m, key.startswith('planet_')))} |")
    if tuned:
        L += ['', '## Vor der Anpassung', '',
              '| Karte | Stärke → | Glättung → | p95 vorher → nachher | Urteil vorher |', '|---|---|---|---|---|']
        for key, tex, base, m0, pr, m1 in rows:
            L.append(f"| `{key}` | {base['strength']:.2f} → {pr['strength']:.2f} | {base['smooth']} → {pr['smooth']} | "
                     f"{m0['p95']:.1f}° → {m1['p95']:.1f}° | {', '.join(verdict(m0))} |")
    open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    print('Bericht:', path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--preview', help='Ordner für Vorschaubilder (PNG)')
    ap.add_argument('--llm', metavar='URL', help='OpenAI-kompatible API, z. B. http://localhost:1234/v1 (LM Studio)')
    ap.add_argument('--llm-model', help='Modellname (Standard: erstes geladenes Modell)')
    ap.add_argument('--vision', action='store_true', help='Bild an ein Vision-Modell mitsenden (nur mit --llm)')
    ap.add_argument('--cube-desc', action='append', default=[], metavar='NAME=TEXT',
                    help='Beschreibung einer Cube Map für das Sprachmodell, mehrfach möglich')
    ap.add_argument('--evaluate', action='store_true', help='Karten bewerten, Bericht surface-maps-bewertung.md schreiben')
    ap.add_argument('--tune', action='store_true', help='Stärke und Glättung nach der Bewertung anpassen (impliziert --evaluate)')
    ap.add_argument('--no-params', action='store_true', help='gespeicherte Parameter ignorieren (Standardwerte)')
    a = ap.parse_args()
    params = {} if a.no_params else load_params()
    llm = None
    if a.llm:
        try:
            llm = Llm(a.llm, a.llm_model)
            print('Sprachmodell:', llm.model)
        except (urllib.error.URLError, OSError, RuntimeError, ValueError, KeyError) as e:
            print('Warnung: Sprachmodell nicht erreichbar (%s), es gelten gespeicherte und Standardwerte' % e)
    for kv in a.cube_desc:
        if '=' in kv:
            k, v = kv.split('=', 1)
            if k in CUBE_DEFAULTS:
                CUBE_DEFAULTS[k]['desc'] = v
    out_dir = os.path.join(NAP, 'Material', 'fx')
    made = []

    nm = {}
    previews = {}
    chosen = {}
    report = []
    for key, (container, tex, strength, smooth, desc) in NORMALS.items():
        img = read_texture(container, tex)
        base = {'strength': strength, 'smooth': smooth}
        pr = clamp_normal(params.get('normal', {}).get(key, {}), base)
        if llm:
            try:
                buf = io.BytesIO()
                img.resize((256, 256)).save(buf, 'PNG')
                ans = llm.json_answer(SYS_NORMAL, f'Textur: {tex}\nBeschreibung: {desc}\nStatistik: {image_stats(img)}',
                                      buf.getvalue() if a.vision else None)
                pr = clamp_normal(ans, pr)
                print(f'  {key}: LLM -> {pr}')
            except Exception as e:  # noqa: BLE001
                print(f'  {key}: LLM-Antwort verworfen ({str(e)[:80]}), Standard {pr}')
        h = height_from(img, pr['smooth'])
        m0 = metrics(h, pr['strength'])
        before = dict(pr)
        if a.tune:
            pr = dict(pr)
            pr['strength'] = round(tune(h), 2)
            h = height_from(img, pr['smooth'])
            if metrics(h, pr['strength'])['grain'] > 1.5 and pr['smooth'] < NORMAL_LIMITS['smooth'][1]:
                pr['smooth'] += 1
                h = height_from(img, pr['smooth'])
                pr['strength'] = round(tune(h), 2)
        m1 = metrics(h, pr['strength'])
        report.append((key, tex, before, m0, pr, m1))
        chosen.setdefault('normal', {})[key] = pr
        n = normal_from_height(h, pr['strength'])
        nm['nm_' + key] = encode_normal(n)
        previews[key] = np.clip((n * 0.5 + 0.5) * 255, 0, 255).astype(np.uint8)
    header, root = build_library(nm, 'MIPS')
    p = os.path.join(out_dir, 'normalmaps.txm')
    W.save(p, header, root)
    made.append('Material/fx/normalmaps.txm')
    print(f'normalmaps.txm: {len(nm)} Karten, {os.path.getsize(p) / 1e6:.1f} MB')

    for c in CUBES:
        pr = clamp_cube(params.get('cube', {}).get(c, {}), CUBE_DEFAULTS[c])
        if llm:
            try:
                ans = llm.json_answer(SYS_CUBE, f'Cube Map {c}: {pr["desc"]}')
                pr = clamp_cube(ans, pr)
                print(f'  {c}: LLM -> {pr}')
            except Exception as e:  # noqa: BLE001
                print(f'  {c}: LLM-Antwort verworfen ({str(e)[:80]})')
        chosen.setdefault('cube', {})[c] = pr
        faces = make_cube(CUBE_SIZE, pr)
        header, root = build_library({c: encode_cube(faces)}, 'CUBE')
        p = os.path.join(out_dir, c + '.mat')
        W.save(p, header, root)
        made.append(f'Material/fx/{c}.mat')
        print(f'{c}.mat: {os.path.getsize(p) / 1e6:.2f} MB')
        previews[c] = faces

    write_ini(os.path.join(ROOT, 'SDK', 'fx', 'SurfaceMaps.ini'),
              {k: (NORMALS[k][1], NORMALS[k][4], chosen['normal'][k]) for k in NORMALS},
              {c: chosen['cube'][c] for c in CUBES})
    if a.evaluate or a.tune:
        write_report(report, a.tune, os.path.join(ROOT, 'surface-maps-bewertung.md'))
    if llm or a.tune or not os.path.isfile(PARAMS_FILE):
        chosen['_info'] = {'model': llm.model if llm else None, 'vision': bool(a.vision and llm)}
        with open(PARAMS_FILE, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(chosen, f, indent=1, ensure_ascii=False)
            f.write('\n')
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
                nv = v.astype(np.float32) / 255 * 2 - 1
                lit = np.clip(nv @ np.array([-0.5, 0.5, 0.7], np.float32) / 0.95, 0, 1)
                both = np.concatenate([v, np.repeat((lit * 255).astype(np.uint8)[..., None], 3, axis=2)], axis=1)
                Image.fromarray(both).resize((1024, 512), Image.LANCZOS).save(os.path.join(a.preview, k + '.png'))


if __name__ == '__main__':
    main()
