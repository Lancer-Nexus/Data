import csv, os, random, time
import numpy as np, torch, spandrel
from PIL import Image
R = os.path.expanduser('~/Dokumente/Freelancer-Textures')
rows = [r for r in csv.DictReader(open(f'{R}/original/manifest.csv', encoding='utf-8')) if not r['hinweis']]
def grp(r):
    c = r['container']; t = r['textur'].lower()
    if t.startswith('dtl'): return 'dtl'
    if c.startswith('interface/neuronet'): return 'neuronet'
    if c.startswith('interface'): return 'interface'
    if c.startswith('equipment'): return 'equipment'
    if c.startswith('bases/backdrops'): return 'backdrops'
    if c.startswith('bases'): return 'bases'
    if c.startswith('fx'): return 'fx'
    if c.startswith('solar') or c.startswith('universe'): return 'solar'
    return 'other'
random.seed(7)
by = {}
for r in rows: by.setdefault(grp(r), []).append(r)
N = {'bases':8,'neuronet':5,'interface':6,'equipment':6,'backdrops':4,'fx':5,'solar':5,'dtl':3}
sel = []
for g, n in N.items():
    sel += [(g, r) for r in random.sample(by[g], min(n, len(by[g])))]
dev='cuda'
M = {'x4plus':'RealESRGAN_x4plus.pth','PBRify':'4x-PBRify_UpscalerV4.pth'}
L = {k: spandrel.ModelLoader().load_from_file(f'{R}/models/{f}').model.eval().to(dev) for k,f in M.items()}
def up(m, im):
    x = torch.from_numpy(np.asarray(im.convert('RGB'))).permute(2,0,1).unsqueeze(0).float().to(dev)/255
    with torch.inference_mode(): y = m(x)
    return Image.fromarray((y[0].clamp(0,1).permute(1,2,0).cpu().numpy()*255).round().astype(np.uint8))
def psnr(a, b):
    d = np.asarray(a, float) - np.asarray(b, float); m = (d**2).mean()
    return 99 if m == 0 else 10*np.log10(255**2/m)
os.makedirs(f'{R}/test2', exist_ok=True)
CELL = 256; sheets = {}; log = []
for g, r in sel:
    im = Image.open(f'{R}/original/{r["datei"]}'); w, h = im.size
    base = im.convert('RGB')
    cells = [base.resize((w*4, h*4), Image.NEAREST)]
    row = {'grp': g, 'id': r['id'], 'size': f'{w}x{h}', 'ziel': f'{r["ziel_breite"]}x{r["ziel_hoehe"]}', 'fmt': r['format'], 'tex': r['textur'][:28]}
    for k, m in L.items():
        t0 = time.time(); o = up(m, im); dt = time.time()-t0
        cells.append(o)
        # Rueckrechnung: wieder auf Original verkleinern, Abweichung = Treue
        row[k+'_psnr'] = round(psnr(o.resize((w, h), Image.LANCZOS), base), 1)
        row[k+'_s'] = round(dt, 2)
    cells = [c.resize((CELL, int(CELL*c.size[1]/c.size[0])), Image.LANCZOS) for c in cells]
    sheets.setdefault(g, []).append((row, cells)); log.append(row)
for g, items in sheets.items():
    H = sum(max(c.size[1] for c in cells)+6 for _, cells in items)
    sh = Image.new('RGB', (CELL*3+16, H), (40,40,40)); y = 0
    for _, cells in items:
        for i, c in enumerate(cells): sh.paste(c, (i*(CELL+8), y))
        y += max(c.size[1] for c in cells)+6
    sh.save(f'{R}/test2/{g}.png')
with open(f'{R}/test2/ergebnis.csv','w',newline='') as f:
    wr = csv.DictWriter(f, fieldnames=list(log[0].keys())); wr.writeheader(); wr.writerows(log)
for r in log: print(r)
