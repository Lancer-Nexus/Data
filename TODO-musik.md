# Mehrere Musiktitel pro Raum

Stand: 2026-10-12. Client-Unterstützung, Laufzeitnachweis und Umstellung der
generischen Bar-Räume sind umgesetzt. Original-CD-DATA-Dateien und Audiodateien
bleiben lokale Testdaten und werden nicht in Git übernommen; die angepassten
SDK-Raum-INIs und deren Changelog sind versioniert.

## Verhalten und Syntax

`[Room_Sound] music` akzeptiert einen oder mehrere Sound-Nicknames. Titel werden
beim Betreten eines Raums zufällig gewählt; nach Trackende folgt ein anderer
Titel ohne unmittelbare Wiederholung. Ein einzelner Titel wird wiederholt.
Mit dem Suffix `oneshot` wird ein Titel einmal abgespielt; bei mehreren Titeln
wird dafür ein zufälliger Titel gewählt und die Playlist endet anschließend.
Es gibt keinen Timerwechsel.

```ini
[Room_Sound]
music = music_bar_generic01, music_bar_generic02, music_bar_generic03
```

## Client-Umsetzung und Laufzeitnachweis

- [x] `[Room_Sound] music` vom Parser über `GameItemDb`, `BaseRoom` und
  `RoomGameplay` bis `SoundManager.PlayMusic` nachverfolgt.
- [x] Kommagetrennte Nicknames und das bestehende `oneshot`-Suffix unterstützen.
- [x] Zufällige Auswahl ohne direkte Wiederholung sowie Trackwechsel nach EOF
  umsetzen.
- [x] Verhalten für Mehrspur-`oneshot`, einzelne Titel und leere Werte festlegen.
- [x] Kompatibilität bestehender Einzeltitel sicherstellen.
- [x] Parser- und Auswahltests für Mehrspur, `oneshot`, Einzeltrack, Leerwert
  und direkte Wiederholungen ergänzen.
- [x] Playlist am 2026-10-12 im echten Debug-Client im Raum `Br01_04_Bar`
  ausgeführt. Der Lauf nutzte eine isolierte Kopie der lokalen Retail-DATA,
  startete `Br01_04_Base` direkt in der Bar und ersetzte dort die Musik durch
  zwei synthetische Ogg-Tracks (0,7 s und 0,9 s). Das Log zeigt den erfolgreichen
  Daten-/UI-Start und zehn Trackwechsel im Wechsel `test_bar_b` / `test_bar_a`,
  ohne Error-, Fatal- oder Exception-Einträge. OpenAL lief im Null-Treiber;
  der Lauf bestätigt Parser, Streamende und Playlist-Auswahl, aber keinen
  Hörtest der Original-Bar-Musik oder der Loop-Grenzqualität.

## Datenänderungen

- [x] Syntax und Rollout im `SDK/changelog.md` dokumentieren.
- [x] Alle 131 generischen Bar-Räume auf die zehn bestehenden Titel
  `music_bar_generic01` bis `music_bar_generic10` umstellen. Regional benannte
  Bar-Musik bleibt unverändert.
- [x] `tools/sync_inis_to_nap.py` ausgeführt: erster Lauf übertrug 1252
  SDK-INIs. Nach Erhalt der SDK-Zeilenenden wurden 131 Dateien aktualisiert;
  1121 blieben unverändert. Der finale Dry-Run meldete 1252 unveränderte
  Dateien. Alle 131 Bar-INIs in `NAP/World` sind byte-identisch.

Die zehn Titel sind in `SDK/audio/Music.ini` definiert; alle zehn lokalen
Retail-WAV-Dateien sind vorhanden. Vor der Umstellung verwiesen die 131
generischen Raumzeilen jeweils auf einen einzelnen Titel. Danach enthält jede
generische Bar-Playlist alle zehn Titel; die 41 regionalen Bar-Verweise blieben
unverändert.
