#!/usr/bin/env python3
"""Prueft einen hochskalierten Container gegen das Original: gleiche Texturen, Faktor 4,
Rueckrechnung (PSNR) und Alpha. Aufruf: verify_upscaled.py <original> <neu>"""
import io
import sys
import os
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import utf_write as W


def leaves(path):
    _, r = W.load(path)
    out = {}
    for trail, n in W.walk(r):
        if n.name.upper() in ('MIPS', 'MIP0'):
            out[trail] = n.data
    return out


def psnr(a, b, w=None):
    d = (a.astype(float) - b.astype(float)) ** 2
    if w is not None:  # Farbe nur dort zaehlen, wo sie sichtbar ist (Alpha)
        wt = w[:, :, None].astype(float) / 255
        m = (d * wt).sum() / max(wt.sum() * d.shape[2], 1e-9)
    else:
        m = d.mean()
    return 99.0 if m == 0 else 10 * np.log10(255 ** 2 / m)


a, b = leaves(sys.argv[1]), leaves(sys.argv[2])
if a.keys() != b.keys():
    print('FEHLER: Texturen unterschiedlich'); sys.exit(1)
worst = []
for k in a:
    o = Image.open(io.BytesIO(a[k])).convert('RGBA')
    n = Image.open(io.BytesIO(b[k])).convert('RGBA')
    if n.size != (o.size[0] * 4, o.size[1] * 4):
        print('FEHLER Groesse', k, o.size, n.size); sys.exit(1)
    d = n.resize(o.size, Image.LANCZOS)
    worst.append((psnr(np.asarray(o)[:, :, :3], np.asarray(d)[:, :, :3], np.asarray(o)[:, :, 3]), psnr(np.asarray(o)[:, :, 3], np.asarray(d)[:, :, 3]), k[-1]))
worst.sort()
print(f'{os.path.basename(sys.argv[2])}: {len(a)} Texturen, PSNR min {worst[0][0]:.1f} dB ({worst[0][2]}), '
      f'Mittel {sum(w[0] for w in worst) / len(worst):.1f} dB, Alpha min {min(w[1] for w in worst):.1f} dB')
