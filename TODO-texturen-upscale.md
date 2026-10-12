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
- [x] UTF-Schreiber (`tools/utf_write.py`) und DXT-Kompression (Python-Paket `etcpak`: BC1 für DXT1, BC3 für DXT5, DXT3 aus BC1-Farbe plus explizitem Alpha) umgesetzt, siehe 8.
- [ ] Kachelnde Texturen: Nahtprüfung (Wrap-Padding ist eingebaut, aber noch nicht an einer Kachel geprüft).
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

## 8. Werkzeuge und erster Durchlauf

- `tools/utf_write.py`: lädt einen UTF-Container als Baum, ersetzt Blätter, schreibt Baum, Namenstabelle und Daten neu (Kopf übernommen, Namen und Daten auf 4 Byte ausgerichtet). `--selftest <datei>` prüft Laden, Speichern, Laden auf identische Knoten und Daten.
- `tools/upscale_textures.py <container> --out <Ordner>`: skaliert alle Texturen eines Containers um Faktor 4 und schreibt ihn neu. Format bleibt erhalten: DXT1/DXT3/DXT5, DDS unkomprimiert, TGA 32/24/16 mit voller Mip-Kette, TGA8 als Palette (Median-Cut) ohne Mips wie im Original. Container aus `hd_overrides.txt` werden übersprungen. Identische Texturen werden nur einmal gerechnet.
- `tools/verify_upscaled.py <original> <neu>`: gleiche Textur-Menge, Faktor 4, Rückrechnung als PSNR (Farbe nach Alpha gewichtet).
- Sonderfall: Texturen, bei denen mehr als 30 % der Pixel (Alpha < 250) durchscheinend sind (Glows, Sprites), werden **bikubisch** vergrößert, nicht per Modell. PBRify verwandelte die weichen Verläufe von `tr_r_27` in Körnung.

Erster Durchlauf an sechs Containern (Backdrop, drei Basen-Container, Atmosphäre, FX): 105 Texturen, alle Container ohne Fehler geschrieben und wieder lesbar, Faktor 4 überall; PSNR der Rückrechnung im Mittel 35 bis 45 dB, schlechtester Wert 30 dB. Sichtprüfung an vier Texturen unauffällig.

**Nicht geprüft:** Ob Freelancer die neu geschriebenen Container lädt (kein Spieltest in dieser Umgebung). Vorher nicht auf das ganze NAP anwenden; erst einen einzelnen Container im Spiel prüfen.

## 9. Gesamtlauf und Ablage im NAP

- **Auswahl:** alle 343 Container mit Originaltexturen (605 Texturen, kein Fehler). Liste: `tools/upscaled_containers.txt`; `build_nap.py`, `check_textures.py` und `upscale_textures.py` behandeln sie wie `hd_overrides.txt` (nicht überschreiben/löschen, nicht ein zweites Mal hochskalieren).
- **Sicherung:** `~/Dokumente/Freelancer-Backup-NAP-vor-Upscale/` (die 343 Container, die sechs betroffenen SDK-INIs, Stand der Schutzliste, `MD5SUMS`). Wiederherstellen: Klassenordner nach `NAP/` kopieren und die Zeilen aus `upscaled_containers.txt` entfernen.
- **Alpha:** alle 153 Alpha-Texturen haben mehr als 30 % durchscheinende Pixel. Symbole (`/interface/`, `/equipment/`): Farbe über transparente Pixel ausgeblutet und je per Modell, Alpha ebenfalls per Modell (scharfe Konturen). Alle anderen (Glows, FX, Lichter): bikubisch, vormultipliziert.
- **Kacheln (`dtl_`):** Wrap-Padding 16 px senkt das Nahtverhältnis (Kante/Nachbarpixel) von 5,2 auf 1,6 (`dtl_tile01`, 128 px); ohne Padding wären es 3,8. Die Kachel war schon im Original nicht nahtlos, wird also nicht schlechter.
- **INIs:** `tools/scale_shape_inis.py` hat 40 Formen in zwei INIs ×4 genommen (`universe/heavens/Shapes.ini`, `solar/blackhole/Bhshapes.ini`). Prüfung danach: `check_textures.py` meldet 0 Formen außerhalb und 0 nur teilweise abgedeckte Texturen.
- **Rückrechnung** (Mittel je Container, 343 Container): Median 33 dB, unteres Zehntel bis 17,5 dB, Minimum 13 dB. Die niedrigen Werte haben fast nur kleine 32-px-Symbole, bei denen die Konturen absichtlich schärfer werden (Sichtprüfung der 14 schlechtesten ohne Auffälligkeit; `heavens/dust2` mit 16,5 dB nicht einzeln geprüft).
- **TGA16:** Bit 15 bleibt 0, wenn der Kopf keine Alpha-Bits meldet (Fehler beim ersten Lauf: Alpha 0, behoben und die drei Container neu geschrieben).
- **Nicht umgewandelt:** Vollbildgrafiken als Einzeldatei (`startupscreen.tga`, `front_freelancerlogo.tga`, 23 `.bmp` in `Material/interface/intro/images`); sie sind keine Texturkacheln und brauchen eine eigene Entscheidung.
- **Nicht geprüft:** Laden im Spiel. Fällt etwas auf, den betroffenen Container aus der Sicherung zurückkopieren und aus `upscaled_containers.txt` nehmen.
