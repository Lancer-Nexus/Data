#!/usr/bin/env python3
"""Skaliert die Originaltexturen eines UTF-Containers per KI um Faktor 4 hoch und schreibt den Container neu.

Ablauf je Textur: dekodieren (Pillow) -> RGB per Modell x4 (Alpha getrennt mit Lanczos) ->
Mip-Kette -> im selben Format kodieren (DXT1/DXT3/DXT5, DDS 24 Bit, TGA 8/16/24/32).
Voraussetzungen: torch, spandrel, Pillow, numpy, etcpak (siehe TODO-texturen-upscale.md).

  python3 tools/upscale_textures.py NAP/Models/bases/backdrops/bd_li02_04_icecrystal.3db --out ausgabe/
  python3 tools/upscale_textures.py --list-groups

Ohne `--out` wird der Container direkt ersetzt (nur für `--apply`). Container aus
tools/hd_overrides.txt (HD-Pack) werden übersprungen.
"""
import argparse
import hashlib
import io
import os
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import utf_write as W  # noqa: E402

MODELS = os.path.expanduser('~/Dokumente/Freelancer-Textures/models')
MODEL_FILES = {'pbrify': '4x-PBRify_UpscalerV4.pth', 'x4plus': 'RealESRGAN_x4plus.pth'}
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def model_for(container, tex):
    """Zuordnung laut TODO-texturen-upscale.md, Abschnitt 7."""
    c = container.replace('\\', '/').lower()
    if '/interface/' in c:
        return 'x4plus'
    return 'pbrify'


def overrides(redo=False):
    """Geschützte Container: HD-Pack und bereits hochskalierte (bei redo nur HD-Pack)."""
    out = set()
    for fn in ('hd_overrides.txt',) if redo else ('hd_overrides.txt', 'upscaled_containers.txt'):
        p = os.path.join(REPO, 'tools', fn)
        if os.path.exists(p):
            out |= {l.strip().lower() for l in open(p, encoding='utf-8') if l.strip() and not l.startswith('#')}
    return out


class Upscaler:
    def __init__(self, device='cuda'):
        import torch
        import spandrel
        self.torch = torch
        self.dev = device
        self.models = {}
        self.spandrel = spandrel

    def _get(self, key):
        if key not in self.models:
            d = self.spandrel.ModelLoader().load_from_file(os.path.join(MODELS, MODEL_FILES[key]))
            self.models[key] = d.model.eval().to(self.dev)
        return self.models[key]

    def rgb(self, key, arr):
        """arr: HxWx3 uint8 -> 4H x 4W x 3 uint8."""
        t = self.torch
        x = t.from_numpy(np.ascontiguousarray(arr)).permute(2, 0, 1).unsqueeze(0).float().to(self.dev) / 255
        with t.inference_mode():
            y = self._get(key)(x)
        return (y[0].clamp(0, 1).permute(1, 2, 0).cpu().numpy() * 255).round().astype(np.uint8)


def upscale_image(up, key, im, wrap, icon=False):
    """PIL-Bild -> PIL RGBA x4. Alpha getrennt per Lanczos."""
    rgba = im.convert('RGBA')
    w, h = rgba.size
    a_arr = np.asarray(rgba.getchannel('A'))
    if (a_arr < 250).mean() > 0.3 and icon:
        # Symbol mit Alpha als Form: Farbe ueber transparente Pixel ausbluten, Farbe und Alpha je per Modell
        from PIL import ImageFilter
        f = np.asarray(rgba).astype(np.float32)
        al = f[:, :, 3:4] / 255
        rad = max(w // 16, 1)
        pm = Image.fromarray((f[:, :, :3] * al).clip(0, 255).astype(np.uint8), 'RGB').filter(ImageFilter.GaussianBlur(rad))
        am = Image.fromarray(a_arr, 'L').filter(ImageFilter.GaussianBlur(rad))
        bl = np.asarray(pm).astype(np.float32) / np.maximum(np.asarray(am).astype(np.float32)[:, :, None] / 255, 1 / 255)
        filled = np.where(al >= 0.98, f[:, :, :3], np.where(al > 0, f[:, :, :3] * al + bl * (1 - al), bl))
        col = up.rgb(key, filled.clip(0, 255).astype(np.uint8))
        grey = up.rgb(key, np.repeat(a_arr[:, :, None], 3, axis=2))[:, :, 0]
        res = Image.fromarray(col, 'RGB').convert('RGBA')
        res.putalpha(Image.fromarray(grey, 'L'))
        return res
    if (a_arr < 250).mean() > 0.3:
        # Sprite/Glow: weiche Verläufe, die das Modell zu Körnung "verbessert" -> bikubisch, vormultipliziert
        f = np.asarray(rgba).astype(np.float32)
        al = f[:, :, 3] / 255

        def big(ch):  # float-Kanal bikubisch x4
            return np.asarray(Image.fromarray(ch, 'F').resize((w * 4, h * 4), Image.BICUBIC))
        ab = big(al).clip(0, 1)
        out = np.zeros((h * 4, w * 4, 4), np.float32)
        for c in range(3):
            out[:, :, c] = big(f[:, :, c] * al) / np.maximum(ab, 1 / 255)
        out[:, :, 3] = ab * 255
        return Image.fromarray(out.clip(0, 255).round().astype(np.uint8), 'RGBA')
    rgb = np.asarray(rgba)[:, :, :3]
    pad = 16 if wrap else 0
    if pad:
        rgb = np.pad(rgb, ((pad, pad), (pad, pad), (0, 0)), mode='wrap')
    out = up.rgb(key, rgb)
    if pad:
        out = out[pad * 4:-pad * 4, pad * 4:-pad * 4]
    res = Image.fromarray(out, 'RGB').convert('RGBA')
    a = rgba.getchannel('A')
    if a.getextrema() != (255, 255):
        a = a.resize((w * 4, h * 4), Image.BICUBIC)
        res.putalpha(a)
    return res


def mip_chain(img, min_size):
    levels = [img]
    while min(levels[-1].size) > min_size:
        w, h = levels[-1].size
        levels.append(levels[-1].resize((max(w // 2, 1), max(h // 2, 1)), Image.BOX))
    return levels


def _dxt_color(img):
    import etcpak
    w, h = img.size
    return etcpak.compress_bc1(img.convert('RGBA').tobytes(), w, h)


def encode_dds(img, header):
    """header: 128 Byte DDS-Kopf des Originals; Format daraus. -> bytes."""
    fcc = header[84:88]
    h = bytearray(header)
    rgba = img.convert('RGBA')
    if fcc in (b'DXT1', b'DXT3', b'DXT5'):
        import etcpak
        levels = mip_chain(rgba, 4)
        body = bytearray()
        for lv in levels:
            w, hh = lv.size
            if fcc == b'DXT1':
                body += etcpak.compress_bc1(lv.tobytes(), w, hh)
            elif fcc == b'DXT5':
                body += etcpak.compress_bc3(lv.tobytes(), w, hh)
            else:  # DXT3: Farbe wie BC1, Alpha explizit 4 Bit je Pixel
                col = etcpak.compress_bc1(lv.tobytes(), w, hh)
                a = np.asarray(lv.getchannel('A'))
                bw, bh = w // 4, hh // 4
                blocks = a.reshape(bh, 4, bw, 4).transpose(0, 2, 1, 3).reshape(bh * bw, 16) >> 4
                packed = (blocks[:, 0::2] | (blocks[:, 1::2] << 4)).astype(np.uint8)  # 8 Byte je Block
                for i in range(bh * bw):
                    body += packed[i].tobytes() + col[i * 8:i * 8 + 8]
        size = (rgba.size[0] // 4) * (rgba.size[1] // 4) * (8 if fcc == b'DXT1' else 16)
        struct.pack_into('<IIII', h, 12, rgba.size[1], rgba.size[0], size, 0)
        struct.pack_into('<I', h, 28, len(levels))
        return bytes(h) + bytes(body)
    # unkomprimiert: Kanalmasken aus dem Kopf (R, G, B, A bei Offset 92..104)
    bpp = struct.unpack_from('<I', header, 88)[0]
    if bpp not in (16, 24, 32):
        raise ValueError(f'DDS {bpp} Bit nicht unterstützt')
    masks = struct.unpack_from('<4I', header, 92)
    levels = mip_chain(rgba, 1)
    body = bytearray()
    for lv in levels:
        a = np.asarray(lv).astype(np.uint32)
        v = np.zeros(a.shape[:2], np.uint32)
        for ch, m in enumerate(masks):
            if not m:
                continue
            sh = (m & -m).bit_length() - 1
            bits = bin(m).count('1')
            v |= ((a[:, :, ch] >> (8 - bits)) << sh) & m
        if bpp == 16:
            body += v.astype('<u2').tobytes()
        elif bpp == 32:
            body += v.astype('<u4').tobytes()
        else:
            body += v.astype('<u4').view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
    struct.pack_into('<IIII', h, 12, rgba.size[1], rgba.size[0], rgba.size[0] * bpp // 8, 0)
    struct.pack_into('<I', h, 28, len(levels))
    return bytes(h) + bytes(body)


def tga_header(w, h, imgtype, bpp, cmap=False, desc=0):
    return struct.pack('<BBBHHBHHHHBB', 0, 1 if cmap else 0, imgtype, 0, 256 if cmap else 0,
                       24 if cmap else 0, 0, 0, w, h, bpp, desc)


def encode_tga(img, first_blob):
    """Ein TGA-Blatt je Stufe. -> Liste von Blobs (MIP0, MIP1 ...)."""
    imgtype, bpp = first_blob[2], first_blob[16]
    desc = first_blob[17]
    flip = not (desc & 0x20)  # Zeilenreihenfolge des Originals übernehmen
    rgba = img.convert('RGBA')

    def rows(a):
        return a[::-1] if flip else a

    if imgtype == 1:  # Palette, 8 Bit
        q = rgba.convert('RGB').quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pal = q.getpalette()[:768]
        pal += [0] * (768 - len(pal))
        pal_bgr = bytes(v for i in range(256) for v in (pal[i * 3 + 2], pal[i * 3 + 1], pal[i * 3]))
        idx = np.asarray(q)
        return [tga_header(rgba.size[0], rgba.size[1], 1, 8, cmap=True, desc=desc) + pal_bgr
                + np.ascontiguousarray(rows(idx)).tobytes()]
    out = []
    levels = mip_chain(rgba, 1)
    for lv in levels:
        a = np.asarray(lv)
        if bpp == 32:
            px = a[:, :, [2, 1, 0, 3]]
        elif bpp == 24:
            px = a[:, :, [2, 1, 0]]
        elif bpp == 16:
            r, g, b = (a[:, :, 0] >> 3).astype(np.uint16), (a[:, :, 1] >> 3).astype(np.uint16), (a[:, :, 2] >> 3).astype(np.uint16)
            px = ((r << 10) | (g << 5) | b).astype('<u2')
            if desc & 0x0f:  # Alpha-Bit nur, wenn der Kopf Attributbits meldet (sonst bleibt Bit 15 = 0)
                px = px | ((a[:, :, 3] >= 128).astype('<u2') << 15)
        else:
            raise ValueError(f'TGA {bpp} Bit nicht unterstützt')
        out.append(tga_header(lv.size[0], lv.size[1], 2, bpp, desc=desc) + np.ascontiguousarray(rows(px)).tobytes())
    return out


def process(path, outpath, up, stats, dry=False):
    header, root = W.load(path)
    # Texturverzeichnis = Verzeichnis, das MIPS oder MIP0 als Blatt hat
    cache = {}
    n = 0

    def visit(d, trail):
        nonlocal n
        try:
            _visit(d, trail)
        except Exception as e:  # noqa: BLE001
            stats.setdefault('fehler', []).append((path, d.name, str(e)))

    def _visit(d, trail):
        nonlocal n
        leaves = {c.name.upper(): c for c in d.children if not c.is_dir}
        if 'MIPS' in leaves or 'MIP0' in leaves:
            name = d.name
            key = model_for(path, name)
            icon = any(t in path.replace('\\', '/').lower() for t in ('/interface/', '/equipment/'))
            wrap = name.lower().startswith('dtl')
            if 'MIPS' in leaves:
                blob = leaves['MIPS'].data
                sig = hashlib.md5(blob + key.encode()).hexdigest()
                if sig not in cache:
                    im = Image.open(io.BytesIO(blob))
                    im.load()
                    cache[sig] = encode_dds(upscale_image(up, key, im, wrap, icon), blob[:128]) if not dry else blob
                leaves['MIPS'].data = cache[sig]
            else:
                blob = leaves['MIP0'].data
                sig = hashlib.md5(blob + key.encode()).hexdigest()
                if sig not in cache:
                    im = Image.open(io.BytesIO(blob))
                    im.load()
                    cache[sig] = encode_tga(upscale_image(up, key, im, wrap, icon), blob) if not dry else None
                new = cache[sig]
                if new is not None:
                    keep = [c for c in d.children if c.is_dir or not c.name.upper().startswith('MIP')]
                    tmpl = leaves['MIP0']
                    d.children = [W.Node(f'MIP{i}', tmpl.flags, data=b) for i, b in enumerate(new)] + keep
            n += 1
        for c in d.children:
            if c.is_dir:
                visit(c, trail + (c.name,))
    visit(root, ())
    stats['tex'] += n
    stats['uniq'] += len(cache)
    if not dry and n:
        os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
        W.save(outpath, header, root)
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('containers', nargs='+')
    ap.add_argument('--out', help='Ausgabeverzeichnis (Pfadstruktur ab NAP bleibt erhalten)')
    ap.add_argument('--apply', action='store_true', help='Container im NAP direkt ersetzen')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--redo', action='store_true',
                    help='auch Container aus upscaled_containers.txt bearbeiten (nach frischem Aufbau von NAP/)')
    a = ap.parse_args()
    if not (a.out or a.apply or a.dry_run):
        ap.error('--out, --apply oder --dry-run angeben')
    ov = overrides(a.redo)
    up = None if a.dry_run else Upscaler()
    stats = {'tex': 0, 'uniq': 0}
    for p in a.containers:
        rel = os.path.relpath(os.path.abspath(p), os.path.join(REPO, 'NAP')).replace('\\', '/')
        # hd_overrides.txt: Klasse/pfad
        if rel.lower() in ov:
            print('HD-Pack, uebersprungen:', rel)
            continue
        outp = p if a.apply else os.path.join(a.out or '.', rel)
        n = process(p, outp, up, stats, dry=a.dry_run)
        print(f'{rel}: {n} Texturen')
    print(f"gesamt {stats['tex']} Texturen, {stats['uniq']} verschiedene")
    for f in stats.get('fehler', []):
        print('FEHLER', *f)


if __name__ == '__main__':
    main()
