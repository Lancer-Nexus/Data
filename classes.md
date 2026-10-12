# Klassen der Spieldaten

Die Spieldaten liegen in `NAP/`. Jeder Klassenordner ist ein Container. Das Spiel lädt alle Container in einen virtuellen Root, in dem die Ordner wie im Original erreichbar sind. Der Klassenname ist deshalb nicht Teil des Pfads.

Beispiel: `NAP/Sounds/audio/…/x.ogg` ist im Spiel unter `audio/…/x.ogg` erreichbar.

Die Pfade in den INIs (`SDK/`) bleiben unverändert gültig. Geprüft: alle Verweise aus den INIs (19712 Datei-Verweise, `tools/check_refs.py`) bis auf die in `missing.md` genannten lösen sich über den virtuellen Root auf.

## Klassen

| Klasse | Dateien | Zuordnung |
|---|---:|---|
| `Models` | 2327 | `.3db`, `.cmp`, `.dfm`, `.vms`, `.sph`, `.anm` (Schiffe, Charaktere, Equipment, Solar, Basen) |
| `Sounds` | 1814 | `.ogg` (1620), `.flac` (80), `.utf`, Ordner `audio/`; die CD-WAVs sind gewandelt (siehe `WISSEN.md`, Abschnitt 15) |
| `Script` | 1524 | `.thn` (Thorn-Skripte), Ordner `scripts/` |
| `UI` | 806 | `.page`, `.sur`, Ordner `interface/`, `screens/` |
| `Effects` | 626 | `.ale`, `.pte`, Ordner `fx/` |
| `Material` | 263 | `.mat`, `.txm`, `.tga`, `.bmp` |
| `Video` | 3 | `.wmv`, Ordner `movies/` (aus dem HD-Pack: `fl_intro`, `da_logo_final`, `mgs_logo_final`) |
| `Surface` | 41 | Zusatzkarten zu Texturen (Normal, Roughness, Metallic, Cube Maps) und ihre INIs `fx/SurfaceMaps*.ini`; nicht aus der CD, erzeugt mit `tools/make_surface_maps*.py` |
| `Equipment` | 4 | Schriftdateien `fonts/*.ttf` aus dem HD-Pack |
| `System` | 1 | Ordner `ai/`, `.db` |
| `World` | 1 | übrige Dateien aus `universe/`, `solar/`, `bases/`, `randommissions/` |

Stand: 7369 Dateien ohne INIs (CD-Daten plus HD-Pack, Stand nach der Phase 6) und dazu 41 Zusatzkarten in `Surface`. Dazu kommen 1266 INIs aus `SDK/`, die `tools/sync_inis_to_nap.py` in die Klassen kopiert (`Mission` besteht nur aus INIs). Die Zuordnung erfolgt nach Dateiendung, bei übrigen Dateien nach dem ersten Ordner. Die Klasse `Equipment` entstand mit dem HD-Pack (Zuordnung in `build_nap.py`, Tabelle `DIR_CLASS`).

Nicht im Container: `exe/` und `dlls/` (Programmdateien, nicht Teil der Daten).

Fehlende Dateien: siehe [missing.md](missing.md). Texturen im Zustand HD oder hochskaliert: siehe `TODO-texturen-upscale.md`.
