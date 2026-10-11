# Plan: Videos hochskalieren (KI) und in ein modernes Format bringen

## Ausgangslage

| Datei (NAP/Video/movies) | Video | Auflösung | Bildrate | Dauer | Größe |
|---|---|---|---|---|---:|
| `fl_intro.wmv` | VC-1 (WMV9) | 1440×960 | 59,94 fps | 3 min 44 s | 104 MB |
| `da_logo_final.wmv` | VC-1 | 1440×960 | 59,94 fps | 16 s | 52 MB |
| `mgs_logo_final.wmv` | VC-1 | 1280×960 | 59,94 fps | 10 s | 24 MB |

Ton: WMA (wmav2), 128 kbit/s. Die Dateien sind die HD-Versionen aus der HD-Edition, siehe `WISSEN.md`.

Vorhanden: ffmpeg/ffprobe, NVIDIA RTX 5060 Laptop (8 GB), 31 GB RAM, 20 Kerne.
Nicht vorhanden: KI-Upscaler (Real-ESRGAN, waifu2x, Upscayl).

## Wichtige Vorab-Frage: Abspielbarkeit im Spiel

Freelancer ist ein Spiel von 2003 und spielt Videos über die Windows-Medienwiedergabe ab (`Movie.dll` im Spielverzeichnis). Das hat zwei Folgen:

- Ein Format, das Windows nicht mitbringt, ist für das Spiel nur abspielbar, wenn ein Codec nachinstalliert ist. Das ist nicht garantiert.
- Die bisherigen Dateien sind WMV (VC-1). Eine Umstellung ist daher **zweistufig**:
  1. **Master** als MP4 (H.264 + AAC), für C# und Weitergabe.
  2. **Spielversion** in dem Format, das die Engine sicher abspielt (WMV/VC-1 oder MPEG-2). Diese Version wird in `NAP/Video/movies/` abgelegt, damit die INI-Verweise (`movies\fl_intro.wmv`) gültig bleiben.

Ob das Spiel ein modernes Format abspielt, muss am Spielrechner getestet werden. Das ist offen.

## Anforderung: C# muss das Format lesen können

Das Format muss in C# (.NET, Windows) zur Verfügung stehen. Gewählt wird deshalb:

- **Container:** MP4 (`.mp4`)
- **Video:** H.264 (AVC)
- **Ton:** AAC

Begründung:
- Windows Media Foundation spielt MP4/H.264/AAC ohne zusätzliche Codecs ab. Das nutzt z. B. WPF `MediaElement`.
- Auch WMV (bisheriges Format) liest Media Foundation, daher bleibt die Spielversion für die Engine unverändert, bis getestet ist, ob MP4 dort läuft.
- Nicht gewählt:
  - **AV1 und WebM/VP9:** brauchen unter Windows zusätzliche Codec-Pakete, sind in .NET-Standardbibliotheken nicht zuverlässig verfügbar.
  - **H.265 (HEVC):** Windows braucht dafür eine Erweiterung, die nicht überall installiert ist. Als Option für später offen.

Für Tests in C#: Ein kleines Konsolenprojekt mit `MediaPlayer` aus Windows Media Foundation oder mit WPF `MediaElement` reicht, um die MP4-Datei abzuspielen.

## Ziel

- Master: MP4, H.264 + AAC, Auflösung 2× (2880×1920) bzw. 2560×1920. Zu entscheiden.
- Bildrate: 59,94 fps unverändert.
- Keine Änderung am Inhalt oder an der Länge.
- Spielversion: WMV bleibt, bis getestet ist, ob die Engine MP4 abspielt.

## Aufgaben

- [ ] Entscheiden: Ziel-Auflösung (2× oder 2560×1920).
- [ ] Testen: Abspielen der MP4-Datei in einem C#-Testprojekt (Media Foundation / WPF MediaElement).
- [ ] Testen: Abspielen der MP4-Datei im Spiel auf dem Zielrechner. Ergebnis hier festhalten.
- [ ] Upscaler wählen und installieren: Real-ESRGAN (Python/PyTorch mit CUDA oder ncnn-Vulkan-Binary). Modell z. B. `realesr-animevideov3` für Zeichnungen oder `realesrgan-x4plus` für Fotos. Die Logos sind Grafik, das Intro gemischt.
- [ ] Probelauf auf `da_logo_final.wmv` (16 s), Ergebnis prüfen (Kanten, Artefakte, Flimmern, Farben).
- [ ] Vollständiger Lauf für `mgs_logo_final.wmv` und `fl_intro.wmv`.
- [ ] Umkodieren mit ffmpeg: MP4 (H.264 + AAC) als Master.
- [ ] Ton prüfen: WMA-Ton übernehmen oder neu kodieren, Synchronität mit dem Bild kontrollieren.
- [ ] Ergebnisse in `NAP/Video/movies/` ablegen, Dateinamen wie die INI-Verweise. Die Originale bleiben in einem separaten Ordner außerhalb des Repos.
- [ ] `build_nap.py` anpassen: Die Videos dürfen nicht von der CD überschrieben werden. Das Skript würde die CD-Fassung zurückbringen, bis die Frage zu den HD-Videos entschieden ist.
- [ ] `WISSEN.md` und `classes.md` aktualisieren.

## Grobe Rechnung

- `fl_intro.wmv`: 224 s × 59,94 fps ≈ 13 400 Bilder. Bei 2× mit Real-ESRGAN auf dieser GPU ist mit einigen Bildern pro Sekunde zu rechnen. Das ergibt eher **Stunden** als Minuten. Genauer Wert nach dem Probelauf.
- Speicher: Die Bilder einzeln als PNG auszugeben wird groß. Zwischenstand besser als verlustfreie Folge, die gleich weiterkodiert wird.

## Qualitätshinweis

KI-Upscaling erzeugt Details, die im Original nicht vorhanden sind. Bei Logos und Grafik ist das in der Regel unkritisch, bei Logos mit Text sollte der Text nach dem Lauf kontrolliert werden.
