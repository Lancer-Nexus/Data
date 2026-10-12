# TODO: Plugins des HD-Packs analysieren und portieren

Die HD-Edition lädt über `EXE/dacom.ini` rund 20 Plugin-DLLs. Dieses Dokument fasst zusammen, was sie tun, woher der Quellcode stammt und was für eine Portierung in den neuen Quellcode zu beachten ist. Der Quellcode der Plugins liegt als Referenz in `reference/freelancer-plugins/` (`adoxa/` von Jason Hood, `github/` aus GitHub-Repos). Herkunft, Stand und Lizenzen stehen in `reference/freelancer-plugins/README.md`.

## 1. Wie die Plugins geladen werden

Alle sind Client-Plugins für `Freelancer.exe` Version 1.1. Sie stehen im Abschnitt `[Libraries]` der `EXE/dacom.ini` und werden in dieser Reihenfolge geladen:

| Reihenfolge | DLL | Status | Quelle |
|---:|---|---|---|
| 1 | `jflp.dll` | aktiv | Jason's Freelancer Patch (adoxa), Quelle `reference/freelancer-plugins/adoxa/jflp/` |
| 2 | `console.dll` | aktiv | adoxa |
| 3 | `DelayDisplay.dll` | aktiv | FLHDE (Nachbau eines Plugins von M0tah) |
| 4 | `HudShift.dll` | aktiv | adoxa |
| 5 | `MP3codec.dll` | aktiv | adoxa |
| 6 | `MPRep.dll` | aktiv | adoxa |
| 7 | `numeric.dll` | aktiv | adoxa |
| 8 | `ranks.dll` | aktiv | adoxa |
| 9 | `storyfactions.dll` | aktiv | adoxa |
| 10 | `Territory.dll` | aktiv | adoxa |
| 11 | `TurretZoom.dll` | aktiv, Parameter: `inverse max=1000 shift=200 ctrl=20 alt=4 s+c=0.4 c+a=0.2 switch=100 interval=500 adjust=0.75` | adoxa |
| 12 | `MultiIntro.dll` | aktiv | FLHDE (GPL-3.0) |
| 13 | `flplusplus.dll` | aktiv | FLHDE (BSD-3-Clause) |
| 14 | `WheelScroll.dll` | aktiv | adoxa |
| 15 | `Zone.dll upper` | aktiv, Parameter: `upper` | adoxa |
| 16 | `FLSharp.dll` | aktiv | BC46 (MIT) |
| 17 | `HUDless.dll` | aktiv | adoxa |
| 18 | `Hail.dll` | aktiv | adoxa |
| 19 | `TargetScreen.dll` | aktiv | FLHDE (MIT, Nachbau von Venemons Dynamic Target Screen) |
| 20 | `VersionText.dll` | aktiv | BC46 |
| – | `cyrillic_chat.dll`, `HudFacility.dll`, `HudWeaponGroups.dll`, `HudTarget.dll`, `HudStatus.dll`, `LightingBugFix.dll` | auskommentiert | |

Serverseitig lädt das Pack zusätzlich `FLHook.dll` (TheStarport, GPL-3.0). Nicht Teil dieses Dokuments.

## 2. Gemeinsame technische Eigenschaften der adoxa-Plugins

- Es sind **Binärpatches im Prozessspeicher**. Die DLLs überschreiben beim Laden feste Adressen in `Freelancer.exe` (z. B. `0x45B026`, `0x4A7FD6`, `0x5E28C8`) oder in `common.dll` (feste RVAs) und setzen eigene Hooks mit `naked`-Assembler.
- Sie sind an **eine Programmversion** gebunden. `storyfactions` und `MPRep` prüfen vor dem Patchen Referenzwerte (`*(DWORD*)(offset+1) == erwarteter Wert`) und brechen sonst ab.
- Konfiguration über **eigene INI-Dateien**, die sie mit dem `INI_Reader` aus `common.dll` lesen (Klasse mit 0x1568 Bytes, Methoden `open`, `read_header`, `read_value`, `get_name_ptr`, `close`).
- Texte stehen teils als **Stringressourcen in der DLL selbst** (Ranks, Zone).
- Hash-Funktion für Nicknames: `CreateID`, z. B. `GaugeBars` = `0x91B7BDCC`.

**Folge für die Portierung:** Die Adressen und Patches sind nicht übertragbar. Gebraucht wird die Funktionalität, nicht der Code. Im neuen Quellcode soll jede Funktion als normales Feature mit eigener INI-Konfiguration umgesetzt werden.

## 3. Die vier Plugins zu den neuen INIs

### Story Factions (`storyfactions.dll`, v1.01)

- **Zweck:** Legt fest, welche Fraktionen aus der Reputationsliste ausgeblendet werden. Die Liste im Spiel ist fest einprogrammiert, die INI ersetzt sie vollständig.
- **Konfiguration:** `DATA\storyfactions.ini`, Abschnitt `[StoryFactions]`, ein Fraktions-Nickname pro Zeile ohne Wert (z. B. `fc_ln_grp`, `fc_kn_grp`, `fc_rn_grp`, `fc_n_grp`, `fc_or_grp`, `fc_f_grp`, `fc_q_grp`, `fc_ouk_grp`, `fc_uk_grp`). Fehlt die Datei oder ist sie leer, gilt die eingebaute Liste.
- **Technik:** Patcht `common.dll` an RVA `0xBF800` (Version 1.0) bzw. `0xBF930` (Version 1.1). An fünf Stellen (`+0x001`, `+0x00A`, `+0x4E2`, `+0x530`, `+0x571`) wird der Zeiger auf ein NULL-terminiertes Array von C-Strings ersetzt. Der gepatchte Bereich ist `0x575` Bytes groß.
- **Portierung:** Eine konfigurierbare Liste von Fraktions-Nicknames, die vom Reputationsfenster als „Story-Fraktionen“ ausgeschlossen werden. Konfiguration im Datenordner, Format wie oben.

### Territory (`Territory.dll`, v1.03)

- **Zweck:** Ändert die Meldung beim Betreten eines Systems („X System, Y Space.“) und fügt Häuser auf der Nav-Map hinzu. Im Original sind die Territorien fest einprogrammiert.
- **Konfiguration:** `DATA\UNIVERSE\Territory.ini`.
  - `[Settings]`: `caps` (Großschreibung erzwingen, Standard: ja), `codepage` (z. B. `UTF-8`, `OEM`, `MAC` oder Zahl).
  - `[Houses]`: `format` oder `format_id` (Meldung, erstes `%s` = System, zweites = Haus, höchstens 63 Zeichen, `^` = Zeilenumbruch), `house` (Name direkt) oder `house_id = [Zahl][, Zahl]` (Ressourcen-ID, optional eigene für die Nav-Map), `systems = system[-system][, ...]`, `NavMap = X, Y[, Schrift]`.
  - `[Systems]`: `format`/`format_id` mit einem `%s` für den Systemnamen, `systems`.
  - Systeme per Ressourcennummer oder Nickname, Bereiche wie `Li01-5` oder `196609-13`.
- **Technik:** Hooks in `Freelancer.exe` an den Meldungsroutinen (`0x45AC3E`–`0x45B278`), Haus-Beschriftungen der Nav-Map (`0x490358`–`0x4A037E`, die vier Häuser Li, Br, Ku, Rh sind fest), `CreateTextControl` bei `0x5A0E30`, Stringressourcen über `0x4347E0`, Zielpuffer `0x66DC60`.
- **Portierung:** Datengetriebene Territorien statt fester Liste, Nav-Map-Beschriftung aus INI, Formatstrings mit Platzhaltern.

### Ranks (`ranks.dll`, v1.00)

- **Zweck:** Zeigt einen Namen zum Level an („Pilot 12“).
- **Konfiguration:** `DATA\MISSIONS\ranks.ini`.
  - `[SP Ranks]`, `[MP Ranks]` (mehrfach erlaubt, je Fraktion mit `group = <nickname>`), `[Rank Settings]` (`just_levels`, `offset`).
  - Schlüssel: `next_rank = LEVEL[, ID]`, `set_ranks = INTERVAL, COUNT[, ID]`, `format`, `first_rank_id`.
  - Formatstring: `%%d` = Level, `%s` = Rangname.
  - `offset` wird durch 100 geteilt und von `0.38` abgezogen, um das Statusfenster nach links zu schieben.
- **Technik:** Patcht `Freelancer.exe` bei `0x4A7FD6+4` (Position der Statuswerte als Fließkommazahl) und `0x4A8A9D` (Formatstring). Die Rangnamen sind Stringressourcen in der DLL.
- **Portierung:** Rang-Tabelle in der Datenkonfiguration (pro Fraktion), Namen als lokalisierte Strings.

### HUD Shift (`HudShift.dll`, v2.12.1)

- **Zweck:** Verschiebt HUD-Elemente, damit sie bei Breitbild am Rand bleiben.
- **Konfiguration:** `DATA\INTERFACE\HudShift.ini`.
  - `[HUDShift]`: `Horizontal = auto` oder fester Wert (z. B. `0.17` bei 16:9), `Vertical`, `GaugeBars = x, y[,, Höhe]` (je Bildschirmhöhe), `PlayerStatus`, `TargetStatus`.
  - `[Group]` mit `nickname`, `location` (`left`, `right`, `top`, `bottom`), `position = Adresse, Wert[, Adresse, Wert]`. Die Adressen sind absolute Adressen von Float-Werten in `Freelancer.exe`.
  - Standard-INI enthält die berechneten Werte je Seitenverhältnis (16:9, 15:9, 16:10, 5:4).
- **Technik:** Schreibt Offsets direkt in Float-Variablen der EXE. Auflösung aus `0x679BC8` (Breite) und `0x679BCC` (Höhe), Hook auf Auflösungswechsel bei `0x424AD4`, Statusbalken in Bildschirmkoordinaten (`0x4D56C8`).
- **Portierung:** HUD-Layout mit Ankern (`left`/`right`/`top`/`bottom`) statt absoluter Adressen. Die Shift-Werte werden aus dem Seitenverhältnis berechnet.

## 4. Weitere Plugins von Jason Hood (Referenz im Repo)

| Plugin | Konfiguration/Aufruf | Hinweis für die Portierung |
|---|---|---|
| Zone | Parameter in `dacom.ini` (`upper`, `low=`, `medium=`, `high=`, `ultra=`), Texte als Ressourcen | Zonen-Namen beim Betreten/Verlassen; Farbe nach `property_flags` (Bits 3–5) |
| Wheel Scroll | – | Mausrad in Fenstern (Reputation, Kontakte, Waffen, Chat) |
| MP Rep | – | Ersetzt `GetGroupFeelingsTowards` im Multiplayer, Reputationen vom Server holen (Server-Patch `server.dll`, `0x0112A3` `1D→00`) |
| Turret Zoom | Parameter in `dacom.ini` | Mausrad für die Kamera der Turmansicht, Modifikatoren Shift/Ctrl/Alt |
| Hail | Eintrag `USER_RADIO` in `keylist.ini` | Taste für „Hail“ |
| HUDless | Zusätzliche Tasten `MINIMIZE HUD`, `OPEN LOG` | HUD, dann Cursor, dann beides wiederherstellen |
| MP3 Codec Fix | Umgebungsvariable `FL_MP3` | Abwärtskompatibilität, für neue Engine nicht nötig |
| Numeric Damage | – | Trefferpunkte (Hülle, Schild) numerisch, Adressen `0x4EF771`, `0x4EFD8E` |
| Console | Befehle zur Laufzeit, eigene Readme (`EXE/console_readme.txt`) | Einzelspieler-Konsole, mehrere Schiffe besitzen, 77 KB |

## 5. Plugins mit GitHub-Quellcode (als Referenz kopiert)

| Plugin | Repo | Sprache | Lizenz | Zweck |
|---|---|---|---|---|
| flplusplus | `github.com/FLHDE/flplusplus` | C++ | BSD-3-Clause | Fehlerkorrekturen und Erweiterungen (Autor Callum McGing) |
| FLSharp | `github.com/BC46/FLSharp` | C++ | MIT | Hook-basierte Korrekturen und Verbesserungen |
| DelayDisplay | `github.com/FLHDE/DelayDisplay` | C++ | **keine** | Dekompilation des Plugins von M0tah (Original-Quellcode nie veröffentlicht). Als Referenz kopiert, vor Weitergabe Lizenz klären. Variante mit Lizenz: `TheStarport/FLUF`, `modules/delay_display` (AGPL-3.0). |
| MultiIntro | `github.com/FLHDE/MultiIntro-Updated` | C++ | GPL-3.0 | mehr als drei Intro-Bildschirme |
| TargetScreen | `github.com/FLHDE/DynamicTargetScreen` | C | MIT | dynamischer Zielbildschirm (Nachbau von Venemon) |
| cyrillic_chat | `github.com/FLHDE/cyrillic_chat` | C | MIT | kyrillischer Chat (deaktiviert) |
| Lighting Bug Fix | `github.com/FLHDE/fl-lighting-bug-fix` | C++ | MIT | Beleuchtungsfehler (deaktiviert) |
| VersionText | in der README `github.com/FLHDE/VersionText` verlinkt | – | – | Repo nicht gefunden (API: 404) |
| FLHook | `github.com/TheStarport/FLHook` | C++ | GPL-3.0 | Server-Erweiterung (Hook-Framework) |

**Lizenz:** GPL-3.0-Code (MultiIntro, FLHook) darf nicht ohne Weiteres in den neuen Quellcode übernommen werden. Für MIT/BSD gilt die Namensnennung.

## 6. Zuordnung INI → Plugin (neue INIs im SDK)

| Datei in `SDK/` | Gehört zu | Wirkung ohne Plugin |
|---|---|---|
| `Storyfactions.ini` | `storyfactions.dll` | keine |
| `universe/Territory.ini` | `Territory.dll` | keine |
| `missions/Ranks.ini` | `ranks.dll` | keine |
| `interface/HudShift.ini` | `HudShift.dll` | keine |

## 6a. Priorisierung für die Portierung

Grundlage: Lancer Nexus ist ein Mehrspielerprojekt mit serverseitiger Autorität (Gateway, Coordinator, Instanz). Die Einstufung ist ein **Vorschlag** und hängt davon ab, was die neue Engine schon mitbringt. Das ist hier nicht geprüft.

### A. Muss: Daten und INIs hängen davon ab

Ohne diese Funktionen sind die HD-INIs wirkungslos oder die Daten falsch.

| Funktion | Plugin | Warum | Konfiguration |
|---|---|---|---|
| Story-Fraktionen aus der Reputationsliste ausblenden | Story Factions | Welche Fraktionen der Spieler sieht, ist Spielinhalt | `Storyfactions.ini` |
| Territorien und Meldung beim Systemeintritt, Häuser auf der Nav-Map | Territory | Die Systeme gehören zu Häusern, im Original fest eingebaut | `universe/Territory.ini` |
| Rangnamen zum Level | Ranks | Progression, im Mehrspielermodus je Fraktion | `missions/Ranks.ini` |
| HUD-Layout je Seitenverhältnis | HUD Shift | ohne diese Funktion ist das HUD bei Breitbild falsch platziert | `interface/HudShift.ini` |

### B. Sollte: Mehrspieler und Spielbarkeit

| Funktion | Plugin | Warum |
|---|---|---|
| Reputation vom Server abfragen für politische Zonen, Patrouillen, Schiffskauf | MP Rep | Das Original wertet die Reputation clientseitig aus, im Mehrspielermodus sieht der Client sie nicht. Bei einer Serverarchitektur ist das ein Protokollpunkt. |
| Namen benannter Zonen beim Betreten anzeigen | Zone | Orientierung, Farbe nach Gefahr (`property_flags`) |
| Mausrad in Fenstern, Turmkamera | Wheel Scroll, Turret Zoom | Bedienung, kleiner Aufwand |
| Fehlerkorrekturen | FLSharp | siehe unten |
| Konfigurierbare Sichtweite/LOD, TTF-Schriften, Speicher- und Screenshot-Pfad, FPS-Limit | flplusplus | HD-Daten brauchen oft größere Sichtweite und eigene Schriften |
| Auflösungsliste und Hauptmonitor als Standard | FLSharp | Bei Breitbild und HD nötig |

**FLSharp-Fehler, die der neue Code nicht wiederholen darf:** Handelsrouten-Lichter bleiben aus, Wegpunkte werden im falschen System gelöscht, Mehrfachlauf-Waffen (Mündungsfeuer, Ton, Munitionszähler), `use_animation` aus `weapon_equip.ini`, Client-Server-Updates (mindestens alle 2 s, 40 ms Minimum, 750 ms in der Handelsroute), Rotationssperre beim Start, Kopieren/Einfügen in Eingabefeldern, Abstürze bei fehlerhaften Spielständen, Infokarten für dynamische Solare.

### C. Kann: Komfort

| Funktion | Plugin |
|---|---|
| HUD per Taste ausblenden | HUDless |
| Taste für Hail | Hail |
| Mehr als drei Intro-Bildschirme, zufällig | MultiIntro (GPL-3.0) |
| Waffen-Abklingzeit in der Kontaktliste | DelayDisplay |
| Dynamische Zielansicht | TargetScreen |
| Trefferpunkte numerisch | Numeric Damage |

### D. Entfällt oder gehört woanders hin

| Plugin | Grund |
|---|---|
| MP3 Codec Fix | Behebt Meldungen des alten Fraunhofer-Codecs, im neuen Audiosystem kein Thema |
| Lighting Bug Fix, cyrillic_chat | im HD-Pack deaktiviert, hängen am alten Renderer bzw. Eingabesystem |
| Console | Entwicklerwerkzeug für den Einzelspielermodus, im Mehrspielermodus nicht vorgesehen |
| JFLP.DLL | Sammelpatch für Steuerung und Anzeige, Funktionen einzeln bewerten |
| FLHook | Serverseitiges Framework, gehört zur Serverarchitektur und wird nicht portiert |

### Reihenfolge

1. **Schritt 1:** Funktionen aus A mit ihren vier INIs im neuen Code umsetzen, dabei die Formate unverändert lassen.
2. **Schritt 2:** MP Rep als Protokollpunkt mit dem Gateway abstimmen (Reputation, Besitz, Lease).
3. **Schritt 3:** Die Fehlerliste aus FLSharp als Abnahmetests übernehmen.
4. **Schritt 4:** Komfort (Zone, Wheel Scroll, Turret Zoom, flplusplus-Optionen).
5. **Schritt 5:** Optionales aus C nach Bedarf.

## 7. Aufgaben für die Portierung

- [ ] Entscheiden, welche Plugin-Funktionen im neuen Quellcode übernommen werden (Priorität: Story Factions, Territory, Ranks, HUD-Layout für Breitbild).
- [ ] Je Funktion eine Spezifikation aus Abschnitt 3 ableiten (Konfigurationsformat bleibt kompatibel zu den vorhandenen INIs).
- [ ] INI-Reader des neuen Quellcodes für `storyfactions.ini`, `Territory.ini`, `ranks.ini`, `HudShift.ini` erweitern.
- [ ] Prüfen, ob `Freelancer.ini` oder `dacom.ini` im neuen Quellcode dieselben Plugin-Einträge braucht, oder ob die Funktionen in der Engine bleiben.
- [ ] Testen, ob die vier INIs im Spiel wirkungslos bleiben, solange die DLLs fehlen. Das ist die Erwartung.
- [ ] Lizenz klären, bevor Code aus GPL-3.0-Quellen übernommen wird.
- [ ] Server: `FLHook` und `MPRep` (Server-Patch) separat bewerten.
