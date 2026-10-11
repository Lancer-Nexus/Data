# Wissen: Zusammenhänge der Freelancer-Daten

Diese Datei erklärt, wie die Teile des Repos zusammenhängen. Sie beschreibt den Stand nach den Prüfungen im Projekt. Offene Punkte stehen am Ende.

## 1. Herkunft der Daten

Die Grundlage ist die Original-CD von Freelancer (Version 1.0, Digital Anvil 2003). Sie liegt als ISO vor oder als gemountete CD mit zwei CAB-Archiven:

| Datei | Inhalt |
|---|---|
| `CAB1.CAB` | `data/` (INIs und Daten), `exe/` (Programme, Konfiguration), `dlls/` |
| `CAB2.CAB` | `data/` (überwiegend Modelle, Töne, Videos, Effekte) |

Die `data`-Ordner beider CABs enthalten zusammen 8368 Einträge: 1252 INIs und 7116 andere Dateien.

Die Version 1.3 (Patch) ist nicht auf der CD. Sie steckt im SDK-Ordner. Die Unterschiede zwischen 1.0 und 1.3 sind in `SDK/changelog.md` dokumentiert.

## 2. Zwei Teile: SDK und NAP

Das Repo trennt Konfiguration und Daten:

| Ordner | Inhalt | Im Git |
|---|---|---|
| `SDK/` | INI-Dateien (Spielregeln, Universum, Missionen, Ausrüstung, Musik) | ja |
| `NAP/` | Spieldaten (Modelle, Töne, Texturen, Skripte, Videos) als Klassencontainer | nur die Klassenordner mit `.gitkeep` |

Die INIs sagen dem Spiel, **welche** Daten es lädt und **wie** sie verwendet werden. Die Dateien in `NAP/` sind die Daten selbst. Ohne beide funktioniert das Spiel nicht.

## 3. Klassencontainer und virtueller Root

`NAP/` enthält elf Klassenordner: `Effects`, `Equipment`, `Material`, `Mission`, `Models`, `Script`, `Sounds`, `System`, `UI`, `Video`, `World`. Die Zuordnung steht in `classes.md`. Sie folgt der Dateiendung und sonst dem Hauptordner.

Das Spiel lädt alle Klassenordner in einen **virtuellen Root**. Dort liegen die Dateien so, wie die INIs sie erwarten. Der Klassenname gehört nicht zum Pfad:

```
NAP/Sounds/audio/sounds/fx/debri_explo_1.wav   ->   im Spiel: audio/sounds/fx/debri_explo_1.wav
```

Deshalb verweisen die INIs auf Pfade wie `audio\sounds\fx\debri_explo_1.wav`, ohne Klasse.

## 4. Verweise: wie INIs auf Dateien zeigen

- Ein Verweis ist ein Wert wie `Solar\dockable\jump_gatel.cmp` oder ein Name ohne Pfad wie `1.wav`.
- Pfade nutzen `\` oder `/`. Windows unterscheidet bei Dateinamen nicht zwischen Groß- und Kleinschreibung, Linux schon. Deshalb ist alles klein geschrieben, damit es auf beiden Systemen funktioniert.
- Mehrere Werte stehen durch Komma getrennt, z. B. `Act_CallThorn = missions\m07\x.thn, Player`.
- Ein Nickname ist ein Name im Spiel, den andere Stellen verwenden. Die Datei dahinter steht in der Zeile `file = …`. **Nickname und Dateiname sind nicht dasselbe.** Beispiel: `music_bar_br04` zeigt auf `music_bar_br02.wav`, bis wir es umgestellt haben.

`tools/check_refs.py` prüft 19 712 Datei-Verweise. 42 lösen sich nicht direkt auf, davon 32 fehlen wirklich (10 Verweise ohne Ordner finden ihre Datei an anderer Stelle). Sie stehen in `missing.md`.

## 5. Namenskonvention

| Was | Regel | Beispiel |
|---|---|---|
| Ordner | klein | `universe/systems/li01/` |
| Dateien in `NAP/` | klein, Leerzeichen durch `_` | `debri_explo_1.wav` |
| INI-Dateien in `SDK/` | PascalCase | `EngineSounds.ini` |
| Ausnahme | `InitialWorld.ini`, weil `Freelancer.ini` das so verweist | |

Die INI-Namen sind nur unsere Konvention. Die Engine liest die INIs über `Freelancer.ini` und die Abschnitte dort. `Freelancer.ini` liegt in `SDK/exe/`, weil es zum Spielprogramm gehört.

Namen mit Leerzeichen gibt es nicht mehr. Die Original-CD hatte sie, z. B. `debri explo 1.wav`. Die Verweise sind angepasst.

## 6. Musik

- `SDK/audio/Music.ini` enthält 188 Einträge mit Nickname, Datei, Typ, Lautstärke (`attenuation`) und Streaming.
- Räume verweisen über `[Room_Sound] music = <nickname>` darauf. Ein Raum hat genau einen Nickname, optional mit `, oneshot`.
- Die Bar-Räume nutzen 30 Nicknames (172 Verweise). 16 davon zeigen seit der letzten Änderung auf ihre eigene Datei. Vorher spielten mehrere dieselbe Datei.
- Mehrere Titel pro Raum sind nicht möglich, das ist Gamecode. Siehe `TODO-musik.md`.

## 7. Explosionsgeräusche

Die Dateien `debri explo 1–4` und `med explo 1–4` sind auf der CD vorhanden. Unsere erste Prüfung hat sie als fehlend gemeldet, weil der Tokenizer am Leerzeichen abbrach. Die Verweise zeigen wieder auf sie, die Dateien heißen jetzt mit `_`. Ein Zwischenstand mit `audio\null.wav` war falsch und ist korrigiert.

## 8. Fehlende Dateien

32 Ziele werden von INIs referenziert, sind aber weder auf der CD noch im HD-Pack vorhanden. Die Liste steht in `missing.md`, erzeugt von `tools/check_refs.py`. Die Gruppen:

- **Schiffs-Kollisionsmodelle** `*_col.cmp`: 5 Stück. Die Modelle selbst sind vorhanden, die Kollisionsmodelle nicht.
- **Intro-Szenen:** 17 `spacepop`-INIs in `universe/systems/intro/Intro.ini`.
- **Station und TLR:** `tlr_a.3db`, `tlr_d.3db`, `tlr_tube_a.cmp`, `trading_depot.cmp` ohne eindeutigen Ersatz.
- **Interface:** `interface/baseside/unknown.3db`, `hudtarget.txm`, `roids.txm`, `exit.tga`, `openingscreen.tga`.

Das HD-Pack hat `interface/baseside/{elite,exit,fighter,frieghter}.3db`, `hud_commsicon.3db` und `multi_blackdragonmale.3db` geliefert, die vorher fehlten. Korrekturen wurden nur gemacht, wenn eine andere Quelle denselben Namen für dieselbe Rolle nutzt (`jump_gatel`, `manufacturing_platform_lod`, `rh_battleship`).

## 9. Externe Quellen, die wir geprüft haben

| Quelle | Befund |
|---|---|
| Discovery-Freelancer `Navmap` | Enthält INI-Dumps mehrerer Versionen, aber keine Binärdateien. Nutzbar für Namen. |
| `FLHDE/freelancer-hd-edition` (lokal `~/Dokumente/GitHub/freelancer-hd-edition`) | Teilweise Daten: 1565 Nicht-INI-Dateien gegenüber 7117 bei uns. Eigene INIs mit anderen Werten. |
| `treewyrm/freelancer` | TypeScript-Bibliothek für die Formate. Läuft mit Node 22 oder 24, Tests bestehen. Schreiben über den Einstieg `dist/ini/index.js` ist nicht geprüft. |
| FLCompanion | Windows-Anwendung, nicht geprüft. |

Das HD-Pack ist übernommen (Abschnitt 13).

## 10. Werkzeuge

| Datei | Zweck |
|---|---|
| `tools/build_nap.py` | Baut `NAP/` aus der ISO oder den CABs. Benennt um, ordnet Klassen zu, entfernt Dateien, die nicht mehr aus der Quelle stammen. |
| `tools/sync_inis_to_nap.py` | Kopiert die INIs aus `SDK/` nach `NAP/`. Mehrfach ausführbar. |
| `tools/import_hd_pack.py`, `tools/import_hd_inis.py` | Übernehmen Daten und INIs des HD-Packs (Abschnitt 13). |
| `tools/utf_textures.py`, `tools/check_textures.py` | Texturmaße lesen, Formen und Materialnamen prüfen, Bericht `textur-pruefung.md`. |
| `tools/extract_textures.py`, `tools/upscale_textures.py`, `tools/utf_write.py`, `tools/scale_shape_inis.py`, `tools/verify_upscaled.py` | KI-Hochskalierung der Originaltexturen (Abschnitt 14). |
| `tools/check_refs.py` | Prüft alle Datei-Verweise der INIs, schreibt `missing.md`. |

Wichtig: `build_nap.py` schließt zwei README-Kopien aus (`EXCLUDE`), weil wir sie entfernt haben. Sie würden sonst wieder erscheinen. Dateien aus `hd_overrides.txt` und `upscaled_containers.txt` überschreibt und löscht es nicht.

## 11. Git

- `main`: Ursprünglicher Upload.
- `sdk-1.3.1`: Die gesamte Arbeit. Hier auch die Commits, die in diesem Dokument beschrieben sind.
- Remote `origin` hat den Branch. Der Push braucht eine Anmeldung im Terminal.

## 12. Offene Punkte

- Mehrere Musiktitel pro Raum (Gamecode, siehe `TODO-musik.md`).
- Die 32 fehlenden Ziele (`missing.md`), vor allem die Kollisionsmodelle.
- **Engine-Test:** HD-Daten (1024- und 2048-Texturen, neue INI-Schlüssel) und die hochskalierten Texturen sind nur strukturell geprüft, nicht im Spiel (`TODO-hd-pack.md`, `TODO-texturen-upscale.md`).
- Plugin-Funktionen des HD-Packs (`storyfactions`, `Territory`, `ranks`, `HudShift`): Quellcode als Referenz in `reference/freelancer-plugins/`, Umsetzung offen (`TODO-plugins.md`).
- Hochskalierung der Vollbildgrafiken (`startupscreen.tga` u. a.) und der 17 HD-Videos (Videos: `TODO-video.md`).
- Die Engine selbst ist nicht im Repo. Alles, was über die Auswertung der INIs und der Containerformate hinausgeht, ist nicht geprüft.

## 13. HD-Pack

Quelle: `FLHDE/freelancer-hd-edition`, nur `DATA/` und `EXE/freelancer.ini`. Entscheidungen (`PLAN-hd-pack.md`): HD-Werte gewinnen; geänderte HD-Texturen werden übernommen und die INIs richten sich nach Textur und Modell; kein Backup (Rückweg ist ISO plus Manifest).

- **Daten:** `import_hd_pack.py` hat 1250 Nicht-INI-Dateien nach `NAP/` übernommen (1001 überschrieben, 249 neu) und in `hd_overrides.txt` eingetragen. Namen sind nach unseren Regeln normalisiert (klein, `_`; Planeten flach; `fl_intro_en_hd.wmv` → `fl_intro.wmv`).
- **INIs:** `import_hd_inis.py` hat 254 INIs geändert und 10 neu aufgenommen (990 waren identisch). Zusätzlich Asteroiden (152 INIs), Black Hole, Solar (Nebel, Ringe) und `Music.ini`.
- **Texturen:** 302 Texturen haben eine andere Größe als auf der CD, überwiegend ×4 (256 → 1024, 128 → 512), Planeten ×8. Die Formkoordinaten in den INIs passen (0 außerhalb, 0 halb abgedeckt, `textur-pruefung.md`).
- **Nicht im Umfang:** `EXE/`, `DLLS/`, `FLDOCS/`, `JFLP/` des HD-Packs. Die Plugin-INIs sind ohne die DLLs wirkungslos.

## 14. Texturen hochskalieren

Texturen, die das HD-Pack nicht anfasst (343 Container, 605 Texturen), sind mit KI um Faktor 4 hochskaliert, im selben Format zurückgeschrieben und im NAP ersetzt. Das entspricht dem Verhältnis der HD-Texturen (gemessen an 6214: ×4 dominiert).

- **Modelle:** PBRify V4 (CC0) für Basen, Solar, FX, Backdrops und Ausrüstung; RealESRGAN x4plus (BSD-3) für Interface und Symbole. Alpha getrennt: Symbole per Modell, Glows und Sprites bikubisch.
- **Format:** DXT1/3/5, DDS unkomprimiert, TGA 8/16/24/32 bleiben erhalten (DXT über `etcpak`, eigener UTF-Schreiber).
- **INIs:** `scale_shape_inis.py` hat 40 Formen in zwei INIs ×4 genommen.
- **Sicherung:** `~/Dokumente/Freelancer-Backup-NAP-vor-Upscale/` (nicht im Repo). Liste der Container: `tools/upscaled_containers.txt`.
- **Offen:** Spieltest; Vollbildgrafiken. Einzelheiten und Zahlen: `TODO-texturen-upscale.md`.
