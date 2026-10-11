# Lancer Nexus Data

Datenrepository des [Lancer Nexus](https://github.com/Lancer-Nexus)-Projekts: Spieldaten für Freelancer: Original-CD 1.0, Patch 1.3, Korrekturen 1.3.1 und das HD-Pack (FLHDE). Texturen, die das HD-Pack nicht anfasst, sind per KI um Faktor 4 hochskaliert.

## Inhalt

| Pfad | Inhalt | Im Git |
|---|---|---|
| `SDK/` | INI-Dateien (Spielkonfiguration, Universum, Missionen, Ausrüstung, Schiffe …) in der Version 1.3.1 | ja |
| `SDK/changelog.md` | Änderungen 1.0 → 1.3 → 1.3.1 mit Diff je Datei | ja |
| `SDK/exe/` | `Freelancer.ini`, `DACOM.ini`, `dacomsrv.ini` aus dem Spielverzeichnis | ja |
| `NAP/` | Spieldaten (Modelle, Töne, Texturen, Skripte, Videos …) als Klassencontainer | nur die Klassenordner (Inhalt ignoriert) |
| `classes.md` | Einteilung der Spieldaten in Klassen und Regeln | ja |
| `missing.md` | Dateien, auf die die INIs verweisen, die aber auf der CD fehlen | ja |
| `tools/` | Skripte: `NAP/` aus der CD aufbauen, HD-Pack übernehmen, Texturen prüfen und hochskalieren | ja |
| `BASE/`, `CLIENT/` | leer, für später vorgesehen | – |

Branches: `main` enthält den ursprünglichen Upload. Die Arbeit liegt auf `sdk-1.3.1`.

## SDK

Die INIs stammen aus dem SDK 1.3 und sind mit den Korrekturen aus 1.3.1 versehen. Konventionen:

- **Ordner** sind klein geschrieben (`universe/systems/li01/`).
- **Dateinamen** sind PascalCase (`EngineSounds.ini`). Ausnahme: `InitialWorld.ini`, weil `Freelancer.ini` das so referenziert.
- **Verweise** auf Dateien in den INIs sind klein geschrieben und stimmen exakt mit `NAP/` überein.
- **Formatierung:** Eine Leerzeile vor jedem Block, keine Leerzeichen am Zeilenende, keine doppelten Leerzeilen. Werte bleiben unverändert.

Alle Änderungen gegenüber der CD sind in `SDK/changelog.md` dokumentiert.

## NAP (Spieldaten)

`NAP/` ist der Container der Spieldaten. Das Spiel lädt alle Klassencontainer in einen virtuellen Root, in dem die Pfade wie im Original liegen. Der Klassenname ist also nicht Teil des Pfads:

```
NAP/Sounds/audio/…/x.ogg   →   im Spiel: audio/…/x.ogg
```

Die Klassen sind in [`classes.md`](classes.md) beschrieben: `Models`, `Sounds`, `Script`, `UI`, `Effects`, `Material`, `Video`, `Equipment`, `Mission`, `System`, `World`.

Von `NAP/` werden nur die Klassenordner ins Repo übernommen (mit einer leeren `.gitkeep`). Die Dateien darin stammen aus der Original-CD und dem HD-Pack, sind groß (rund 5,5 GB) und bleiben per `.gitignore` außerhalb.

## Anleitung: NAP aus der CD aufbauen

### Voraussetzungen

- Linux mit Python 3
- 7-Zip (Paket `p7zip-full`; Befehl `7z`)
- Optional: `zenity` für den Dateidialog. Ohne `zenity` wird der Pfad im Terminal abgefragt.
- Die Freelancer-CD als ISO-Datei (z. B. `Freelancer.iso`) oder als gemountete CD mit `CAB1.CAB` und `CAB2.CAB`
- Rund 1 GB freier Platz für den Arbeitsordner

### Schritte

1. **Repo auf den Stand bringen**
   ```bash
   cd LN-Data
   git checkout sdk-1.3.1
   ```

2. **Testlauf** (zeigt nur, was passieren würde):
   ```bash
   python3 tools/build_nap.py --source /pfad/zur/Freelancer.iso --dry-run
   ```
   Die Ausgabe nennt die Anzahl der Datendateien und, wie viele neu, geändert, unverändert oder zu entfernen sind. Ist `NAP/` noch leer, steht bei „unverändert“ 0.

3. **Aufbau:**
   ```bash
   python3 tools/build_nap.py --source /pfad/zur/Freelancer.iso
   ```
   Ohne `--source` öffnet sich ein Dateidialog, in dem du die ISO auswählst.

   Das Skript
   - entpackt die `data`-Ordner beider CABs (ohne INIs) in einen temporären Ordner,
   - schreibt die Dateien klein geschrieben nach `NAP/<Klasse>/<Pfad>`; Leerzeichen im Dateinamen werden zu `_` (z. B. `debri explo 1.wav` → `debri_explo_1.wav`),
   - übernimmt danach die INIs aus `SDK/` über `tools/sync_inis_to_nap.py`,
   - räumt den temporären Ordner wieder auf.

4. **Kontrolle:** `missing.md` enthält die Dateien, die die INIs referenzieren, die auf der CD aber fehlen. Im Normalfall ändert sich die Liste nicht.

### Optionen von `build_nap.py`

| Option | Wirkung |
|---|---|
| `--source PFAD` | ISO-Datei oder Ordner mit `CAB1.CAB` und `CAB2.CAB` |
| `--dry-run` | nur anzeigen, nichts schreiben oder löschen |
| `--no-prune` | Dateien in `NAP/` behalten, die nicht mehr aus der Quelle stammen |
| `--no-sync` | INIs nicht aus `SDK/` übernehmen |
| `--nap PFAD` | anderes Ziel als `NAP/` (z. B. zum Testen) |
| `--work PFAD` / `--keep-work` | Arbeitsordner festlegen bzw. behalten |

Das Skript ist mehrfach ausführbar. Gleiche Dateien bleiben unberührt, geänderte werden überschrieben. Ohne `--no-prune` werden Dateien entfernt, die nicht mehr aus der Quelle stammen. Die beiden Kopien von `mission1 readme.doc` sind bewusst ausgeschlossen (siehe `EXCLUDE` in `build_nap.py`).

Zwei Listen schützen veränderte Dateien: `tools/hd_overrides.txt` (1603 Dateien aus dem HD-Pack) und `tools/upscaled_containers.txt` (343 per KI hochskalierte Container). `build_nap.py` überschreibt und entfernt sie nicht. Nach einem frischen Aufbau aus der CD müssen daher das HD-Pack (`import_hd_pack.py --apply`) und die Hochskalierung (`python3 tools/upscale_textures.py <Container> --apply --redo`, Containerliste aus `upscaled_containers.txt`) erneut ausgeführt werden. Danach `scale_shape_inis.py` und `check_textures.py`.

### Nur die INIs aktualisieren

```bash
python3 tools/sync_inis_to_nap.py            # kopiert SDK/*.ini nach NAP/<Klasse>/<Pfad>
python3 tools/sync_inis_to_nap.py --dry-run
```

Die Klasse einer INI richtet sich nach ihrem Hauptordner (`audio` → `Sounds`, `universe` → `World` usw.). INIs im Wurzelverzeichnis gehen nach `System`. `SDK/exe/` wird nicht übernommen.

## Werkzeuge (`tools/`)

| Werkzeug | Zweck | Aufruf |
|---|---|---|
| `build_nap.py` | `NAP/` aus der ISO aufbauen, normalisieren, Klassen zuordnen | `python3 tools/build_nap.py --source <ISO>` (`--dry-run` zum Testen) |
| `sync_inis_to_nap.py` | INIs aus `SDK/` in die Klassencontainer kopieren | `python3 tools/sync_inis_to_nap.py` |
| `import_hd_pack.py` | HD-Pack (Daten) nach `NAP/` übernehmen, mit Manifest | `python3 tools/import_hd_pack.py --hd-repo <Pfad>` (`--apply` zum Schreiben) |
| `import_hd_inis.py` | HD-INIs normalisiert in `SDK/` übernehmen | `python3 tools/import_hd_inis.py` (`--apply` zum Schreiben) |
| `utf_textures.py` | Maße und Format der Texturen in UTF-Dateien (`.txm`, `.mat`, `.3db` …) lesen | `python3 tools/utf_textures.py NAP/Material/solar/rings/rings.txm` |
| `check_textures.py` | Texturmaße und Verweise prüfen, schreibt `textur-pruefung.md` | `python3 tools/check_textures.py` |
| `extract_textures.py` | Originaltexturen als PNG herauslösen (für KI-Hochskalierung), mit `manifest.csv` | `python3 tools/extract_textures.py --out <Ordner>` (braucht Pillow) |
| `convert_audio.py` | WAV-Dateien in FLAC (PCM) bzw. Ogg Vorbis (MP3-in-WAV) wandeln, INI-Verweise umstellen | `python3 tools/convert_audio.py --stage <Ordner> [--apply --backup <Ordner>]` (braucht ffmpeg) |
| `make_surface_maps.py` | Normal Maps (aus Texturen abgeleitet) und prozedurale Cube Maps erzeugen, Zusatzkarten per `SDK/fx/SurfaceMaps.ini` | `python3 tools/make_surface_maps.py [--preview <Ordner>]` (Pillow, numpy) |
| `check_refs.py` | Alle Datei-Verweise der INIs gegen `NAP/` prüfen, schreibt `missing.md` | `python3 tools/check_refs.py` |
| `scale_shape_inis.py` | `[Shape]`-Koordinaten in INIs an hochskalierte Texturen anpassen | `python3 tools/scale_shape_inis.py` (`--dry-run`) |
| `upscale_textures_test.py` | Modellvergleich an 42 zufälligen Texturen (Kontaktbögen) | `python3 tools/upscale_textures_test.py` |
| `utf_write.py` | UTF-Container laden, ändern, neu schreiben (Bibliothek, `--selftest`) | `python3 tools/utf_write.py --selftest <datei>` |
| `upscale_textures.py` | Texturen eines Containers per KI um Faktor 4 hochskalieren, selbes Format zurückschreiben | `python3 tools/upscale_textures.py <container> --out <Ordner>` (braucht torch, spandrel, etcpak) |
| `verify_upscaled.py` | Hochskalierten Container gegen das Original prüfen (Größe, PSNR) | `python3 tools/verify_upscaled.py <original> <neu>` |

### Textur-Prüfung (`check_textures.py`)

Das Werkzeug prüft nach einem Import oder nach dem Austausch von Texturen:

1. **Maße:** Breite, Höhe und Format (DDS/TGA) jeder Textur in allen `.txm`.
2. **Version:** Größe der Textur in `NAP/` gegenüber dem CD-Original. Zeigt, welche Texturen hochskaliert wurden (HD) und welche unverändert sind.
3. **Formen:** `[Shape]`-Rechtecke (`x`, `y`, `w`, `h`) in den INIs gegen die Größe der referenzierten Textur. Meldet Formen außerhalb der Textur und Texturen, die nur zur Hälfte abgedeckt werden (INI noch für die kleine Textur).
4. **Materialien:** Texturnamen in `.mat` (`Dt_name` usw.) gegen vorhandene Texturen, auch eingebettete und `.tga`.

Die CD-Originale für den Vergleich liest es aus einem Ordner mit den entpackten CABs (`--cd <Ordner>`). Die Ausgabe ist `textur-pruefung.md` im Wurzelverzeichnis (`--out` ändert das). Animierte Texturen (`name_0`) werden erkannt.

Der Bericht gilt für den jeweiligen Stand. Nach Änderungen an Texturen oder INIs neu erzeugen.

## Bekannte Grenzen

- **Fehlende Dateien:** 32 Ziele, auf die die INIs verweisen, fehlen in `NAP/` (Kollisionsmodelle `*_col.cmp`, 17 `spacepop`-INIs, einige Modelle und Grafiken). Sie stehen in `missing.md`; `tools/check_refs.py` erzeugt die Liste neu.
- **Audioformate:** Alle 1700 WAV-Dateien der CD sind in Ogg Vorbis (1620) und FLAC (80) gewandelt, die INIs zeigen auf die neuen Endungen. Der Original-Client kann diese Dateien nicht laden; LibreLancer muss sie nach Inhalt oder Endung dekodieren (nicht im Spiel geprüft). Sicherung: `~/Dokumente/Freelancer-Backup-Audio-vor-Konvertierung/`, Zuordnung `tools/audio_converted.csv`.
- **Hochskalierte Texturen:** Nicht im Spiel geprüft. Sicherung der Originale und Zurückholen: `TODO-texturen-upscale.md`, Abschnitt 9. Vollbildgrafiken (`startupscreen.tga` u. a.) sind nicht hochskaliert.
- **HD-Pack und Plugins:** Die HD-Plugin-DLLs (`storyfactions`, `Territory`, `ranks`, `HudShift`) gehören nicht zu den Daten; ihre INIs sind wirkungslos, solange die DLLs fehlen (`TODO-plugins.md`).
- **Programmdateien:** `exe/` und `dlls/` der CD sind nicht Teil von `NAP/`. Sie liegen nur im lokalen Ordner `Freelancer-Daten` und werden von den Skripten nicht verarbeitet.
- **Groß-/Kleinschreibung:** Alles ist klein geschrieben. Dateien, die intern (in `.thn`, `.page` oder `.3db`) mit anderer Schreibweise referenziert werden, werden nicht geprüft.
- **Version:** Die CD enthält Version 1.0. Die Korrekturen aus 1.3 und 1.3.1 kommen aus `SDK/`, nicht aus der CD. Die Werte des HD-Packs haben bei Abweichungen Vorrang.

## Rechtliches

Die Spieldaten gehören den Rechteinhabern von Freelancer. Dieses Repo enthält nur die INI-Dateien und Skripte. `NAP/` ist ignoriert und darf nicht hochgeladen werden. Die Skripte setzen eine eigene Kopie der CD oder ISO voraus.
