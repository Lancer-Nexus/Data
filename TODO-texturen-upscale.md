# TODO: Originaltexturen hochskalieren (KI)

Ziel: Die Texturen, die noch im CD-Original vorliegen, im gleichen Verhältnis wie das HD-Pack vergrößern.

## 1. Ausgangslage

- **Noch original:** 605 Texturen, davon 528 mit eigenen Daten und 77 Duplikate (gleiche Pixeldaten). Verteilung der eindeutigen:

| Gruppe | Texturen |
|---|---:|
| Basen und Stationen (`bases/…`) | 164 |
| Symbole (`equipment/models/commodities/nn_icons`) | 127 |
| Interface | 110 |
| Solar | 32 |
| Effekte (`fx/…`) | 29 |
| Detail-/Kachelstrukturen (`dtl_…`) | 25 |
| Hintergründe (`bases/backdrops`) | 24 |
| Ausrüstung | 11 |
| Sonstige / Schiffe | 6 |

- **Größen:** 64×64 (169), 256×256 (165), 32×32 (106), 128×128 (80), sonstige 8.
- **Formate:** TGA8, TGA32, DXT1, DXT3 (meist), vereinzelt TGA16/24, DXT5. 153 Texturen haben einen Alphakanal (TGA32, DXT3, DXT5).
- **Herausgelöst:** `tools/extract_textures.py` schreibt alle als PNG (RGBA) mit `manifest.csv`. Ausgabe liegt außerhalb des Repos (`~/Dokumente/Freelancer-Textures/original/`, 16 MB).

## 2. Verhältnis des HD-Packs (gemessen an 6214 Texturen)

| CD → HD | Texturen | Anteil |
|---|---:|---:|
| 256 → 1024 (×4) | 3180 | größter Anteil |
| 128 → 512 (×4) | 1286 | |
| 64 → 256 (×4) | 489 | |
| 256 → 2048 (×8) | 325 | Planeten und einige Materialien |
| 128 → 1024 (×8) | 257 | |
| 32 → 128 (×4) | 192 | |
| 32 → 32, 256 → 256 (×1) | 253 + 118 | unverändert gelassen |

**Regel für die Originale:** Faktor 4 (256 → 1024, 128 → 512, 64 → 256, 32 → 128). Faktor 8 nur, wo das HD-Pack es für gleichartige Texturen getan hat (Planeten). Kleine 16×16-Texturen unverändert.

## 3. Modelle (getestet)

| Modell | Lizenz | Architektur | Stärke | Schwäche |
|---|---|---|---|---|
| **4x-PBRify_UpscalerV4** (Kim2091) | **CC0-1.0** | DAT, 4× | gebaut für Spieltexturen der 2000er, saubere Kanten und Flächen, entfernt Kompressionsartefakte | langsamer als ESRGAN, etwas rau bei kleinen Symbolen |
| **4xTextures_GTAV_rgt-s** (Helaman) | CC-BY-4.0 | RGT-S, 4× | viel Oberflächendetail, auf Spieltexturen trainiert | erfindet bei kleinen Symbolen sichtbar Details |
| **RealESRGAN_x4plus** | BSD-3-Clause | ESRGAN, 4× | glatt und plausibel bei kleinen Bildern | Säume an harten Linien |

Alle drei laufen über `spandrel` und PyTorch (CUDA 12.8) auf der RTX 5060, je Textur wenige Sekunden. Weitere genannte Kandidaten (nicht getestet): 4x-RealisticRescaler, 4x-GameAI-2.0, 4x-SGI. UltraSharp und Remacri sind CC-BY-NC-SA, also nicht für alle Zwecke geeignet.

**Testgrundlage:** sechs Texturen (Hintergrund, Station mit DXT3, DXT1-Plasma, Detailkachel, 32-px-Symbol, 64-px-Schiffssymbol). Das ist wenig, die Empfehlung ist vorläufig.

## 4. Empfehlung

| Gruppe | Modell | Anmerkung |
|---|---|---|
| Basen, Stationen, Hintergründe, Solar, Ausrüstung | **PBRify V4** | Standard, freie Lizenz |
| Symbole (nn_icons), Interface | **x4plus** | glatt, wenig erfundene Details |
| Detailkacheln (`dtl_`) | PBRify mit Wrap-Padding | Kachelbarkeit sichern, Nähte prüfen |
| Effekte (`fx/`) | x4plus, Alpha getrennt | additive Texturen, Ergebnis prüfen |
| Rauhe Oberflächen, wenn mehr Detail gewünscht | GTAV | optional, Lizenz CC-BY (Namensnennung) |

## 5. Pipeline (Plan)

1. **Herauslösen** (fertig): PNG + `manifest.csv`.
2. **Hochskalieren:** RGB über das Modell, **Alpha getrennt** (bikubisch oder als eigenes Graustufenbild), danach zusammensetzen. Zielgröße aus Abschnitt 2.
3. **Duplikate** nur einmal rechnen (md5 im Manifest), Ergebnis auf alle Verwendungen verteilen.
4. **Zurückschreiben:** Neuen UTF-Container mit größerer `MIP0` bzw. `MIPS` erzeugen. Dafür braucht es einen UTF-Schreiber und, bei DXT, eine DXT-Kompression (Pillow reicht dafür nicht sicher). Mip-Stufen neu berechnen.
5. **Prüfen:** `tools/check_textures.py` (Größen, Formen, Namen), danach Sichtprüfung im Spiel.

## 6. Offen

- [x] Größerer Test an 42 Texturen quer durch die Gruppen (siehe 7).
- [ ] UTF-Schreiber und DXT-Kompression (z. B. `texconv`, `nvcompress` oder `ImageMagick`) auswählen und testen.
- [ ] Kachelnde Texturen: Nahtprüfung.
- [ ] Entscheiden, ob die 77 Duplikate gemeinsam bleiben (gleiche Pixel, mehrere Container) oder pro Container gerechnet werden.
- [ ] Nachweis, dass die Engine die größeren Texturen im selben Container lädt (Speicher, Mip-Stufen).
- [ ] Namensnennung für GTAV-Modell (CC-BY-4.0), falls eingesetzt.

## 7. Ergebnis des größeren Tests (42 Texturen)

Skript: `tools/upscale_textures_test.py` (Zufallsauswahl mit festem Seed aus den Originalen: Basen 8, Neuronet 5, Interface 6, Ausrüstung 6, Backdrops 4, FX 5, Solar 5, dtl 3; Modelle x4plus und PBRify). Kontaktbögen und `ergebnis.csv` liegen in `~/Dokumente/Freelancer-Textures/test2/` (nicht im Repo). Alle 42 Läufe fehlerfrei, PBRify 0,04 bis 1,4 s je Textur, x4plus 0,01 bis 0,5 s.

**Rückrechnung** (Ergebnis wieder auf Originalgröße verkleinert, PSNR gegen das Original; hoch = treu):

| Modell | PSNR Mittel | schlechtester Wert |
|---|---|---|
| PBRify | etwa 38 dB | 26,9 dB (loot_niobium) |
| x4plus | etwa 31 dB | 21,5 dB (loot_niobium) |

PBRify liegt in allen 42 Fällen vor x4plus, bei großen Backdrops und Kacheln mit 4 bis 5 dB, bei kleinen Symbolen mit 5 bis 10 dB.

**Sichtprüfung:**
- Basen-, Backdrop-, Ausrüstungs- und dtl-Texturen: PBRify entfernt die DXT-Blockartefakte und hält Kanten und Flächen sauber. x4plus ist ähnlich, schärft aber harte Kanten mit leichten Säumen.
- Interface- und Neuronet-Symbole (weiß auf schwarz): x4plus ergibt etwas härtere, glattere Konturen; PBRify ist weicher, aber ohne Artefakte. Beide brauchbar, x4plus wirkt besser.
- FX-Sprites: x4plus erfindet bei `debrisdust1` Linienstrukturen, die es im Original nicht gibt. PBRify bleibt bei der Körnung. Daher **PBRify für FX**, nicht x4plus.
- Rein weiße oder Verlaufstexturen: beide unauffällig, Verläufe werden ohne Banding geglättet.

**Angepasste Zuordnung:** PBRify für alles außer Interface und Neuronet; dort x4plus (Alpha getrennt). GTAV entfällt als Standard.

**Weiter offen:** Zurückschreiben (UTF-Schreiber, DXT-Kompression), Alpha-Behandlung, Wrap-Padding für dtl, Engine-Ladeprüfung.
