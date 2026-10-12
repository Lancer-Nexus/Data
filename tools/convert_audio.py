#!/usr/bin/env python3
"""Wandelt die WAV-Dateien in NAP/ in moderne Formate und stellt die INI-Verweise um.

Regel je Datei:
  * PCM-WAV (Format 1)                  -> FLAC (verlustfrei)
  * MP3 in WAV (Format 85, Freelancer)  -> Ogg Vorbis, Bitrate wie die MP3-Quelle (Kanäle und
                                           Abtastrate bleiben), kein Rückgriff auf den MP3-Container
Der Name behält Ordner und Stammnamen, nur die Endung wechselt (`.flac`, `.ogg`). Verweise in
SDK/**/*.ini (Pfad oder bloßer Dateiname) und der eine Verweis in einem `.thn` werden angepasst.

  python3 tools/convert_audio.py --stage <Ordner> [--limit N]     # nur konvertieren und prüfen
  python3 tools/convert_audio.py --stage <Ordner> --apply --backup <Ordner>
                                                                  # sichern, ersetzen, INIs ändern

Voraussetzung: ffmpeg (libvorbis, flac) und ffprobe. Ergebnis: tools/audio_converted.csv
(Klasse/alter Pfad, Klasse/neuer Pfad), die `build_nap.py` für den Schutz vor Überschreiben nutzt.
"""
import argparse
import concurrent.futures as cf
import csv
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
NAP = os.path.join(ROOT, 'NAP')
SDK = os.path.join(ROOT, 'SDK')
MAP_CSV = os.path.join(HERE, 'audio_converted.csv')


def wav_tag(path):
    with open(path, 'rb') as f:
        b = f.read(40)
    if b[:4] != b'RIFF' or b[8:12] != b'WAVE':
        return None
    return struct.unpack_from('<H', b, 20)[0]


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries',
                        'stream=codec_name,sample_rate,channels,bit_rate,duration', '-of', 'json', path],
                       capture_output=True, text=True)
    s = json.loads(r.stdout)['streams'][0]
    return {'sr': int(s['sample_rate']), 'ch': int(s['channels']),
            'br': int(s['bit_rate']) if s.get('bit_rate') not in (None, 'N/A') else 0,
            'dur': float(s['duration']) if s.get('duration') not in (None, 'N/A') else 0.0}


def decoded_seconds(path):
    """Echte Dauer durch Dekodieren (der WAV-Kopf von MP3-in-WAV ist ungenau)."""
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'null', '-', '-progress', 'pipe:1', '-nostats'],
                       capture_output=True, text=True)
    t = re.findall(r'out_time_us=(\d+)', r.stdout)
    return int(t[-1]) / 1e6 if t else 0.0


def convert(job):
    src, dst = job
    tag = wav_tag(src)
    info = probe(src)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if dst.endswith('.flac'):
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src, '-c:a', 'flac', '-compression_level', '8', dst]
    else:
        br = max(48, min(256, round(info['br'] / 1000))) if info['br'] else 0
        q = ['-b:a', f'{br}k'] if br else ['-q:a', '5']
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src, '-c:a', 'libvorbis'] + q + [dst]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return src, dst, f'ffmpeg: {r.stderr.strip()[:200]}'
    out = probe(dst)
    if out['sr'] != info['sr'] or out['ch'] != info['ch']:
        return src, dst, f"Format weicht ab: {info['sr']}/{info['ch']} -> {out['sr']}/{out['ch']}"
    d0, d1 = decoded_seconds(src), decoded_seconds(dst)
    if abs(d1 - d0) > 0.1:
        return src, dst, f'Dauer weicht ab: {d0:.2f} -> {d1:.2f}'
    return src, dst, None


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--stage', required=True, help='Ordner für die konvertierten Dateien (Klasse/Pfad)')
    ap.add_argument('--limit', type=int, help='nur die ersten N Dateien (Test)')
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--apply', action='store_true', help='sichern, im NAP ersetzen, INIs umstellen')
    ap.add_argument('--backup', help='Sicherungsordner (mit --apply Pflicht)')
    a = ap.parse_args()
    if a.apply and not a.backup:
        ap.error('--apply braucht --backup')

    wavs = []
    for cls in sorted(os.listdir(NAP)):
        for r, _, fs in os.walk(os.path.join(NAP, cls)):
            for f in sorted(fs):
                if f.lower().endswith('.wav'):
                    wavs.append(os.path.join(r, f))
    if a.limit:
        wavs = wavs[:a.limit]
    jobs, plan = [], {}
    for p in wavs:
        rel = os.path.relpath(p, NAP).replace(os.sep, '/')
        tag = wav_tag(p)
        if tag not in (1, 85):
            print('übersprungen (Format', tag, '):', rel)
            continue
        ext = '.flac' if tag == 1 else '.ogg'
        new_rel = rel[:-4] + ext
        plan[rel] = new_rel
        jobs.append((p, os.path.join(a.stage, new_rel)))
    print(f'{len(jobs)} Dateien: {sum(v.endswith(".flac") for v in plan.values())} -> FLAC, '
          f'{sum(v.endswith(".ogg") for v in plan.values())} -> Ogg Vorbis')
    errs = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for i, (src, dst, err) in enumerate(ex.map(convert, jobs), 1):
            if err:
                errs.append((src, err))
            if i % 200 == 0:
                print(f'  {i}/{len(jobs)}')
    old = sum(os.path.getsize(s) for s, _ in jobs)
    new = sum(os.path.getsize(d) for _, d in jobs if os.path.exists(d))
    print(f'Größe: {old / 1e6:.0f} MB -> {new / 1e6:.0f} MB, Fehler: {len(errs)}')
    for s, e in errs[:20]:
        print('  FEHLER', os.path.relpath(s, NAP), e)
    if errs or not a.apply:
        if errs and a.apply:
            sys.exit('Abbruch: Fehler bei der Konvertierung, nichts geändert.')
        return

    # Sichern
    for rel in plan:
        d = os.path.join(a.backup, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(NAP, rel), d)
    # Zuordnung für Verweise: voller Pfad (ohne Klasse) und eindeutiger Dateiname
    by_path = {re.sub(r'^[^/]+/', '', k).lower(): re.sub(r'^[^/]+/', '', v) for k, v in plan.items()}
    by_name = {}
    for k, v in by_path.items():
        by_name.setdefault(os.path.basename(k), set()).add(v)
    unresolved = set()

    def newtok(m):
        tok = m.group(0)
        n = tok.replace('\\', '/').lstrip('/').lower()
        hit = by_path.get(n)
        if hit is None and '/' not in n and len(by_name.get(n, ())) == 1:
            hit = next(iter(by_name[n]))
        if hit is None:
            unresolved.add(tok)
            return tok
        return tok[:-4] + os.path.splitext(hit)[1]
    pat = re.compile(r'[\w\-./\\]+\.wav', re.I)
    changed = 0
    for r, _, fs in os.walk(SDK):
        for f in fs:
            if not f.lower().endswith('.ini') or os.path.relpath(r, SDK).startswith('exe'):
                continue
            p = os.path.join(r, f)
            t = open(p, 'rb').read().decode('latin-1')
            n = pat.sub(newtok, t)
            if n != t:
                open(p, 'wb').write(n.encode('latin-1'))
                changed += 1
    # .thn: gleiche Länge (.wav -> .ogg) lässt sich direkt ersetzen
    thn_done = []
    for r, _, fs in os.walk(os.path.join(NAP, 'Script')):
        for f in fs:
            if f.lower().endswith('.thn'):
                p = os.path.join(r, f)
                b = open(p, 'rb').read()
                if b'.wav' not in b.lower():
                    continue

                def sub(m):
                    h = by_path.get(m.group(0).decode('latin-1').replace('\\', '/').lower()) or \
                        (next(iter(by_name[os.path.basename(m.group(0).decode().lower())]))
                         if len(by_name.get(os.path.basename(m.group(0).decode().lower()), ())) == 1 else None)
                    if h and h.endswith('.ogg'):
                        return m.group(0)[:-4] + b'.ogg'
                    return m.group(0)
                nb = re.sub(rb'[\w\-./\\]+\.wav', sub, b, flags=re.I)
                if nb != b:
                    open(p, 'wb').write(nb)
                    thn_done.append(os.path.relpath(p, NAP))
    # Dateien tauschen
    for rel, nrel in plan.items():
        dst = os.path.join(NAP, nrel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(a.stage, nrel), dst)
        os.remove(os.path.join(NAP, rel))
    with open(MAP_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['alt', 'neu'])
        for k, v in sorted(plan.items()):
            w.writerow([k, v])
    print(f'ersetzt: {len(plan)} Dateien, INIs geändert: {changed}, .thn: {thn_done}')
    if unresolved:
        print('nicht aufgelöste Verweise (Datei fehlt oder nicht konvertiert):', len(unresolved))
        for t in sorted(unresolved)[:30]:
            print('  ', t)


if __name__ == '__main__':
    main()
