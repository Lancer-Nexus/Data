# Plan: HD-Pack in SDK und NAP einpflegen

Stand: Plan, nichts davon ist ausgeführt. Er baut auf den bisherigen Übernahmen auf (Asteroiden, Schwarzes Loch, Solar, Videos, Musik, 352 Dateien in `tools/hd_overrides.txt`).

## 1. Ziel

1. Das HD-Pack (`freelancer-hd-edition`) vollständig einpflegen:
   - **INIs** in die SDK (`SDK/`),
   - **alle übrigen Daten** nach `NAP/` und die Originale dort überschreiben.
2. Alles dabei **normalisieren** und die **neuen Ziele** berücksichtigen (HD-Dateien, die es auf der CD nicht gibt).
3. Danach **alle INIs vergleichen** und die Änderungen des HD-Packs übernehmen, wieder normalisiert.
4. Zum Schluss prüfen, ob die **Texturmaße** stimmen (256 gegenüber 1024 usw.) und ob die **richtige Textur** referenziert wird.

## 2. Normalisierungsregeln (Standards)

| Bereich | Regel |
|---|---|
| Ordner und Dateien in `NAP/` | klein geschrieben, Leerzeichen → `_` |
| INI-Dateien in `SDK/` | PascalCase (`RockShapes.ini`), Ausnahme `InitialWorld.ini` |
| Verweise in INIs | klein geschrieben, `\` als Trenner, Dateinamen wie in `NAP/` |
| Format | CRLF, eine Leerzeile vor jedem Block, keine Leerzeichen am Zeilenende |
| Planeten | flach: `solar/planets/planet_x.mat`, `solar/planets/detailmap_x.txm` |
| Videos | `fl_intro_en_hd.wmv` → `fl_intro.wmv` (Name im Spiel bleibt) |
| Container | Klasse nach Endung/Hauptordner (`classes.md`), virtueller Root |
| Ausnahmen | `tools/hd_overrides.txt` listet HD-Dateien, die `build_nap.py` nicht überschreibt |

Neue Regel für den Import: HD-Namen werden auf diese Standards abgebildet; die Abbildung steht in einer Tabelle (Manifest), nicht verstreut im Code.

## 3. Ausgangslage

- **HD-Repo (lokal):** Im Arbeitsbaum fehlen 515 Dateien. Das sind die bereits übernommenen (Asteroiden-INIs 175, Starsphere 99, Musik 88, Planeten 80, Nebel 5 …). Im Git-Stand (`HEAD`) ist das Pack vollständig.
- **Rest im Arbeitsbaum:** 1251 Nicht-INI-Dateien und 1090 INIs.
- **Vergleich mit NAP (normalisiert):**
  - 1002 Dateien haben denselben Pfad, 1001 davon weichen ab (`.3db` 409, `.cmp` 221, `.dfm` 204, `.thn` 112, `.mat` 31 …).
  - 249 Dateien gibt es nur im HD-Pack (`.3db` 103, `.cmp` 70, `.ale` 29, `.thn` 18, `.tga` 15, `.utf` 5, `.txm` 5, `.ttf` 4).
- **Schon in `NAP/`:** 352 HD-Dateien (Liste in `hd_overrides.txt`).
- **Schon in der SDK:** Asteroiden (152), Schwarzes Loch (3), Solar (78), Musik-Lautstärken.
- **Nicht im Umfang bisher:** `EXE/`, `DLLS/`, `FLDOCS/`, `JFLP/` des HD-Packs (Spielprogramm und Patch 1.40).

## 4. Phasen

### Phase 0: Quelle festlegen

- Als Quelle gilt der Git-Stand (`HEAD`) des HD-Repos, nicht der Arbeitsbaum.
- Export in einen Staging-Ordner außerhalb des Repos (`git archive`), danach Prüfsummen-Liste (Manifest-Rohdaten).
- Nichts in `NAP/` oder `SDK/` schreiben.

### Phase 1: Manifest erzeugen (Trockenlauf)

Ein neues Werkzeug `tools/import_hd_pack.py` liest den Staging-Ordner und schreibt eine Tabelle (`hd-manifest.csv`) mit Spalten:

`hd_pfad | ziel_klasse | ziel_pfad | aktion | grund`

Aktionen: `überschreiben` (Original wird ersetzt), `neu` (nur im HD-Pack), `ähnlich` (Pfad weicht ab, z. B. Leerzeichen, Planeten-Ordner), `überspringen` (z. B. `EXE/`, wenn nicht gewünscht), `konflikt` (zwei HD-Dateien auf demselben Ziel).

Prüfen: Keine Kollisionen, Anzahl wie in Abschnitt 3, jede Datei hat genau ein Ziel.

### Phase 2: Nicht-INI-Daten nach NAP

- Dateien aus dem Manifest nach `NAP/<Klasse>/<Pfad>` kopieren, Originale überschreiben.
- `tools/hd_overrides.txt` aus dem Manifest neu erzeugen (statt Zeitstempel).
- `tools/build_nap.py` kennt die neuen Regeln (Videos, Planeten, Leerzeichen), sodass ein Neuaufbau aus der ISO dieselbe Struktur ergibt.
- Neue Dateien (nur HD) werden in Phase 3 über INI-Verweise eingebunden; bis dahin stehen sie ungenutzt in `NAP/`.
- Sicherung: Vor dem Überschreiben eine Liste der ersetzten CD-Dateien mit Prüfsumme (Rückweg über die ISO).

### Phase 3: INIs vergleichen und übernehmen

Pro Bereich (zuerst `solar`, `equipment`, `ships`, `characters`, `interface`, `fx`, `universe`, `missions`, `audio`) werden alle HD-INIs gegen die SDK verglichen, normalisiert (Kommentare, Leerzeichen, Zahlenformat egal):

| Kategorie | Behandlung |
|---|---|
| identisch | nichts tun |
| nur Format/Namen | nichts tun (SDK-Standard gilt) |
| geänderte Werte | übernehmen (HD gewinnt), im Changelog notieren |
| neue Abschnitte/Schlüssel | übernehmen, im TODO als „im Spiel prüfen“ markieren |
| neue Verweise auf HD-Dateien | übernehmen, Datei muss in `NAP/` existieren |
| Spiellogik (Missionen, Fraktionen, Preise) | getrennt behandeln, nicht automatisch übernehmen |

Normalisierung beim Übernehmen: INI-Namen auf PascalCase abbilden, Verweise klein, Planetenpfade flach, Format wie in `fmt`.

Pro Bereich ein Commit und eine `TODO-<bereich>.md` wie bisher.

### Phase 4: Verweise prüfen

- Alle Asset- und INI-Verweise in der SDK gegen `NAP/` (wie die letzte Prüfung, 17 035 + 2 555 Verweise).
- Ziel: Nur die bekannten fehlenden Ziele bleiben; `missing.md` aktualisieren.
- Zusätzlich prüfen, dass jede HD-Datei in `NAP/` referenziert wird oder bewusst ungenutzt ist (Liste).

### Phase 5: Texturen und Maße prüfen

Ziel: Die INIs müssen zur Auflösung der referenzierten Textur passen (256 gegenüber 1024 usw.) und auf die richtige Textur zeigen.

1. **Maße auslesen:** Für jede `.txm` und `.tga` (und die Texturen in `.mat`) Breite und Höhe lesen. Werkzeug: `treewyrm/freelancer` mit Node 24 (`~/.nvm/versions/node/v24.21.0`); alternativ ein eigener UTF-Leser in Python.
2. **Koordinaten gegen Maße:** In `Shapes.ini`-artigen Dateien (`x`, `y`, `w`, `h`) und HUD-Montagen (`ButtonMontage.ini`) prüfen, dass die Koordinaten innerhalb der Texturgröße liegen und dem Raster entsprechen (z. B. Formen für 256 passen nicht auf 1024).
3. **Richtige Version:** Je Textur festhalten, ob die CD- oder die HD-Version in `NAP/` liegt (Prüfsumme gegen Manifest), und ob die INI-Koordinaten zu dieser Version passen. Beispiel: `rings.txm` (1024) mit den HD-`Shapes.ini` — bereits geprüft.
4. **Ergebnis:** Tabelle `textur-pruefung.md` mit `Textur | Maße | Version | referenzierende INIs | Status`. Abweichungen kommen in eine TODO.

Besondere Kandidaten: `solar/rings`, `solar/nebula`, `solar/planets/*`, `interface/*`, `fx/*` (Partikel), Schriften.

### Phase 6: Abschluss (erledigt)

- `README.md`, `WISSEN.md`, `classes.md`, `missing.md` sind auf den Stand nach dem HD-Pack und der Hochskalierung gebracht (Abschnitt 13 und 14 in `WISSEN.md`).
- `SDK/changelog.md` enthält die Abschnitte zu den HD-INIs und zur Textur-Hochskalierung.
- Ein Probelauf von `build_nap.py --dry-run` braucht die ISO und ist hier nicht gelaufen; die Schutzlisten werden geladen (1946 Einträge).
- Commits pro Phase; Push durch dich.

## 5. Risiken

- **Engine:** Das HD-Pack setzt teilweise Änderungen am Spielprogramm voraus (`EXE/` mit dgVoodoo, `BinaryEdits.patch`). Texturen mit 1024 Pixeln und neue INI-Schlüssel funktionieren in Version 1.3 evtl. nicht.
- **Spiellogik:** HD-INIs enthalten auch Balance- und Missionsänderungen (Patch 1.40). Automatisches Übernehmen würde sie einführen.
- **Größe:** Zusätzliche Daten im Bereich von mehreren GB in `NAP/`.
- **Überschreiben:** Originale gehen verloren; Rückweg ist nur die ISO und das Manifest.
- **Normalisierung:** Abbildungsfehler (z. B. Ordner `planet_x/` gegenüber flach) führen zu fehlenden Verweisen. Phase 4 fängt das ab.

## 6. Entscheidungen (getroffen)

1. **Umfang:** Nur `DATA/` und die `Freelancer.ini` des HD-Packs (`EXE/`, `DLLS/`, `FLDOCS/`, `JFLP/` bleiben draußen).
2. **Spiellogik:** Die HD-Werte werden übernommen.
3. **Texturen:** Alle geänderten HD-Texturen werden übernommen. Die INIs richten sich immer nach Textur und Modell, nicht umgekehrt.
4. **Rückweg:** Kein Backup. `NAP/` ist Original plus SDK 1.3.1 plus HD-Pack und bleibt über die ISO und das Manifest nachvollziehbar.
