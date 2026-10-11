# Lancer Nexus Data

Datenrepository des [Lancer Nexus](https://github.com/Lancer-Nexus)-Projekts: Spieldaten für Freelancer (Stand der Original-CD 1.0 und des Patches 1.3, mit Korrekturen unter 1.3.1).

## Inhalt

| Pfad | Inhalt | Im Git |
|---|---|---|
| `SDK/` | INI-Dateien (Spielkonfiguration, Universum, Missionen, Ausrüstung, Schiffe …) in der Version 1.3.1 | ja |
| `SDK/changelog.md` | Änderungen 1.0 → 1.3 → 1.3.1 mit Diff je Datei | ja |
| `SDK/exe/` | `Freelancer.ini`, `DACOM.ini`, `dacomsrv.ini` aus dem Spielverzeichnis | ja |
| `NAP/` | Spieldaten (Modelle, Töne, Texturen, Skripte, Videos …) als Klassencontainer | nur die Klassenordner (Inhalt ignoriert) |
| `classes.md` | Einteilung der Spieldaten in Klassen und Regeln | ja |
| `missing.md` | Dateien, auf die die INIs verweisen, die aber auf der CD fehlen | ja |
| `tools/` | Skripte zum Aufbau von `NAP/` aus der CD | ja |
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
NAP/Sounds/audio/…/x.wav   →   im Spiel: audio/…/x.wav
```

Die Klassen sind in [`classes.md`](classes.md) beschrieben: `Models`, `Sounds`, `Script`, `UI`, `Effects`, `Material`, `Video`, `Mission`, `System`, `World`.

Von `NAP/` werden nur die Klassenordner ins Repo übernommen (mit einer leeren `.gitkeep`). Die Dateien darin stammen aus der Original-CD, sind groß (rund 855 MB) und bleiben per `.gitignore` außerhalb.

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
   - schreibt die Dateien klein geschrieben nach `NAP/<Klasse>/<Pfad>`,
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

### Nur die INIs aktualisieren

```bash
python3 tools/sync_inis_to_nap.py            # kopiert SDK/*.ini nach NAP/<Klasse>/<Pfad>
python3 tools/sync_inis_to_nap.py --dry-run
```

Die Klasse einer INI richtet sich nach ihrem Hauptordner (`audio` → `Sounds`, `universe` → `World` usw.). INIs im Wurzelverzeichnis gehen nach `System`. `SDK/exe/` wird nicht übernommen.

## Bekannte Grenzen

- **Fehlende Dateien:** 32 Dateien, auf die die INIs verweisen, sind auf der CD nicht vorhanden (vor allem Kollisionsmodelle `*_col.cmp` und einige Sprachdateien). Sie stehen in `missing.md`.
- **Programmdateien:** `exe/` und `dlls/` der CD sind nicht Teil von `NAP/`. Sie liegen nur im lokalen Ordner `Freelancer-Daten` und werden von den Skripten nicht verarbeitet.
- **Groß-/Kleinschreibung:** Alles ist klein geschrieben. Dateien, die intern (in `.thn`, `.page` oder `.3db`) mit anderer Schreibweise referenziert werden, werden nicht geprüft.
- **Version:** Die CD enthält Version 1.0. Die Korrekturen aus 1.3 und 1.3.1 kommen aus `SDK/`, nicht aus der CD.

## Rechtliches

Die Spieldaten gehören den Rechteinhabern von Freelancer. Dieses Repo enthält nur die INI-Dateien und Skripte. `NAP/` ist ignoriert und darf nicht hochgeladen werden. Die Skripte setzen eine eigene Kopie der CD oder ISO voraus.
