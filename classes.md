# Klassen der Spieldaten

Die Spieldaten liegen in `NAP/`. Jeder Klassenordner ist ein Container. Das Spiel lädt alle Container in einen virtuellen Root, in dem die Ordner wie im Original erreichbar sind. Der Klassenname ist deshalb nicht Teil des Pfads.

Beispiel: `NAP/Sounds/audio/…/x.wav` ist im Spiel unter `audio/…/x.wav` erreichbar.

Die Pfade in den INIs (`SDK/`) bleiben unverändert gültig. Geprüft: alle 17036 Verweise aus den INIs lösen sich über den virtuellen Root auf.

## Klassen

| Klasse | Dateien | Zuordnung |
|---|---:|---|
| `Models` | 2154 | `.3db`, `.cmp`, `.dfm`, `.vms`, `.sph`, `.anm` (Schiffe, Charaktere, Equipment, Solar, Basen) |
| `Sounds` | 1809 | `.wav`, `.utf` (alle Pfade), Ordner `audio/` |
| `Script` | 1506 | `.thn` (Thorn-Skripte), Ordner `scripts/` |
| `UI` | 806 | `.page`, `.sur`, Ordner `interface/`, `screens/` |
| `Effects` | 597 | `.ale`, `.pte`, Ordner `fx/` |
| `Material` | 237 | `.mat`, `.txm`, `.tga`, `.bmp` |
| `Video` | 3 | `.wmv`, Ordner `movies/` |
| `Mission` | 2 | übrige Dateien aus `missions/` |
| `System` | 1 | Ordner `ai/`, `.db` |
| `World` | 1 | übrige Dateien aus `universe/`, `solar/`, `bases/`, `randommissions/` |

Gesamt: 7116 Dateien. Die Zuordnung erfolgt nach Dateiendung, bei übrigen Dateien nach dem ersten Ordner.

Nicht im Container: `exe/` und `dlls/` (Programmdateien, nicht Teil der Daten) und die INIs (liegen in `SDK/`).

Fehlende Dateien: siehe [missing.md](missing.md).
