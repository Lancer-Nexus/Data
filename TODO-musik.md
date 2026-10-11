# TODO: Mehrere Musiktitel pro Raum (Gamecode)

## Ausgangslage

In `SDK/audio/Music.ini` hat jeder Musiktitel einen Nickname und eine Datei:

```ini
[Sound]
nickname = music_bar_br04
file = audio\music\music_bar_br04.wav
type = music
attenuation = -15
streamer = true
```

Die Räume verweisen über einen Nickname auf die Musik. Das steht in `[Room_Sound]`:

```ini
[Room_Sound]
music = music_bar_br04
```

Ein Raum kann heute nur **einen** Musiktitel haben. Die Syntax `music = <nickname>, oneshot` wird ebenfalls genutzt (22 von 363 `music`-Zeilen).

Die 16 Dateien `music_bar_br04`, `music_bar_generic04` usw. sind inzwischen einzeln eingebunden. Vorher spielten mehrere Nicknames dieselbe Datei. Die Bar-Räume bekommen dadurch eine andere Musik als vorher.

## Ziel

Ein Raum soll **mehrere Musiktitel** haben, die **wechseln** (z. B. zufällig oder der Reihe nach). Das Ändern dieser Liste soll **in der INI** möglich sein, ohne Code anzupassen.

## Audioformat

Seit der Konvertierung liegt die Musik als Ogg Vorbis vor (`.ogg`, siehe `WISSEN.md`, Abschnitt 15). Das Audit des Clients nennt keine Loop-Start/Ende-Metadaten; Schleifen gelten für den ganzen Track. Vorbis hat kein MP3-Padding und ist für Schleifen besser geeignet.

## Aufgaben für den Gamecode

Umgesetzt im Client durch den Patch `2171-room-music-playlists.patch` (Repository `Client`, Commit `7a3518ce8`):

- [x] Auswertung von `[Room_Sound] music` geprüft: `RoomSound` speichert jetzt `MusicTracks`, `Music` bleibt der erste Titel.
- [x] Mehrere Nicknames in `music` werden akzeptiert, z. B. `music = music_bar_generic04, music_bar_generic05, music_bar_generic06`.
- [x] Wechselmodus: zufällig, ohne direkte Wiederholung; der nächste Titel startet, wenn der aktuelle endet.
- [x] `oneshot`: Bei mehreren Titeln mit `oneshot` wird einmalig ein Titel gespielt und nicht gewechselt. Ohne `oneshot` spielt jeder Titel einmal, danach folgt der nächste.
- [x] Abwärtskompatibilität: Ein einzelner Nickname verhält sich wie zuvor (Schleife, außer bei `oneshot`), geprüft in `RoomMusicPlaylistTests`.
- [x] Kopplung: Wechsel am Titelende, nicht an Raumwechsel oder Timer. Beim Betreten eines Raums wird ein neuer Titel gewählt.
- [ ] Wiedergabetest im Client mit einem Raum mit mehreren Titeln (z. B. `Br0104Bar.ini`) und mit `.ogg`-Dateien (siehe oben).

## Spätere Änderungen in der INI

Nach der Code-Änderung soll sich die Liste direkt in den Raum-INIs pflegen lassen:

- [ ] Syntax in `docs` bzw. im Changelog festhalten.
- [ ] Bar-Räume mit mehreren Titeln umstellen, z. B. Generic-Räume mit den Titeln `music_bar_generic01` bis `music_bar_generic10`.
- [ ] `tools/sync_inis_to_nap.py` laufen lassen, damit `NAP/` aktuell ist.

## Betroffene Räume (Stand heute)

Bar-Nicknames in Raum-INIs, mit Anzahl der Verweise:

| Nickname | Verweise |
|---|---:|
| `music_bar_generic04` | 15 |
| `music_bar_generic06` | 15 |
| `music_bar_generic07` | 14 |
| `music_bar_generic01` | 13 |
| `music_bar_generic03` | 13 |
| `music_bar_generic05` | 13 |
| `music_bar_generic09` | 13 |
| `music_bar_generic10` | 12 |
| `music_bar_generic02` | 12 |
| `music_bar_generic08` | 11 |
| andere Bar-Nicknames (br, ku, li, rh) | je 1–3 |

Insgesamt 172 Verweise in Raum-INIs auf 30 Bar-Nicknames.

## Hinweise

- Die Raum-INIs liegen unter `SDK/universe/systems/<system>/bases/rooms/`.
- Die Nicknames in `Music.ini` bleiben bestehen. Für einen Wechsel müssen nur die `music`-Zeilen der Räume geändert werden.
