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

`NAP/` enthält zehn Klassenordner: `Effects`, `Material`, `Mission`, `Models`, `Script`, `Sounds`, `System`, `UI`, `Video`, `World`. Die Zuordnung steht in `classes.md`. Sie folgt der Dateiendung und sonst dem Hauptordner.

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

Die früheren Verweis- und Fehlzielzahlen sind veraltet. `tools/check_ini_references.py` prüft Dateiverweise reproduzierbar; den vollständigen NAP-Datenbestand verwenden, weil HD-Dateien im lokalen CD-Rohdatenbaum fehlen können.

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

Die mit `tools/check_ini_references.py` ermittelte Fehlziel-Liste steht in `missing.md`. Ihre aktuelle Zahl ist nur mit dem vollständigen NAP-Datenbestand reproduzierbar. Die wichtigsten bekannten Gruppen:

- **Schiffs-Kollisionsmodelle** `*_col.cmp`: 5 Stück. Die Modelle selbst sind vorhanden, die Kollisionsmodelle nicht.
- **Station und TLR:** einige Verweise haben keinen eindeutigen Ersatz.
- **Interface und HUD:** `interface/baseside/*.3db`, `hud_commsicon.3db` u. a.

Korrekturen wurden nur gemacht, wenn eine andere Quelle denselben Namen für dieselbe Rolle nutzt. Das ist bei `jump_gatel`, `manufacturing_platform_lod` und `rh_battleship` der Fall.

## 9. Externe Quellen, die wir geprüft haben

| Quelle | Befund |
|---|---|
| Discovery-Freelancer `Navmap` | Enthält INI-Dumps mehrerer Versionen, aber keine Binärdateien. Nutzbar für Namen. |
| `FLHDE/freelancer-hd-edition` (lokal `~/Dokumente/GitHub/freelancer-hd-edition`) | Teilweise Daten: 1565 Nicht-INI-Dateien gegenüber 7117 bei uns. Eigene INIs mit anderen Werten. |
| `treewyrm/freelancer` | TypeScript-Bibliothek für die Formate. Läuft mit Node 22 oder 24, Tests bestehen. Schreiben über den Einstieg `dist/ini/index.js` ist nicht geprüft. |
| FLCompanion | Windows-Anwendung, nicht geprüft. |

Die HD-Edition hat Modelle und Texturen, die bei uns fehlen oder anders sind. Ob sie übernommen werden, ist noch nicht entschieden.

## 10. Werkzeuge

| Datei | Zweck |
|---|---|
| `tools/build_nap.py` | Baut `NAP/` aus der ISO oder den CABs. Benennt um, ordnet Klassen zu, entfernt Dateien, die nicht mehr aus der Quelle stammen. |
| `tools/sync_inis_to_nap.py` | Kopiert die INIs aus `SDK/` nach `NAP/`. Mehrfach ausführbar. |

Wichtig: `build_nap.py` schließt zwei README-Kopien aus (`EXCLUDE`), weil wir sie entfernt haben. Sie würden sonst wieder erscheinen.

## 11. Git

- `main`: Ursprünglicher Upload.
- `sdk-1.3.1`: Die gesamte Arbeit. Hier auch die Commits, die in diesem Dokument beschrieben sind.
- Remote `origin` hat den Branch. Der Push braucht eine Anmeldung im Terminal.

## 12. Offene Punkte

- Mehrere Musiktitel pro Raum (Gamecode, siehe `TODO-musik.md`).
- Die 21 fehlenden Dateien, mit offenen Entscheidungen zu den Kollisionsmodellen.
- Entscheidung, ob HD-Modelle und HD-Texturen übernommen werden und welche INI-Werte dazu nötig sind.
- Prüfung, ob die Modelle und Texturen intern auf Materialien verweisen, die nur in HD liegen. Das ist mit `treewyrm` möglich.
- Die Engine selbst ist nicht im Repo. Alles, was über die Auswertung der INIs hinausgeht, ist nicht geprüft.
