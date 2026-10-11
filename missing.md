# Fehlende Dateien

Dateien, auf die die INIs im SDK verweisen, die aber nicht in `NAP/` liegen. Prüfung: alle Asset-Verweise (`.3db`, `.cmp`, `.wav`, `.thn`, …) in `SDK/**/*.ini`, Vergleich mit dem Inhalt von `NAP/` (Groß-/Kleinschreibung ignoriert).

**32 fehlende Ziele** mit insgesamt **55 Fundstellen**.

Die Dateien stammen von der Original-CD (`CAB1.CAB`, `CAB2.CAB`). Ein Eintrag bedeutet: Die Datei fehlt auf der CD oder liegt an einem anderen Pfad.

## Nach Typ

| Typ | Ziele |
|---|---:|
| `.cmp` | 11 |
| `.3db` | 9 |
| `.wav` | 8 |
| `.tga` | 2 |
| `.txm` | 2 |

## Liste

| Ziel | Verwendet in (INI:Zeile) |
|---|---|
| `1.wav` | `audio/GfSounds.ini:211`, `audio/Sounds.ini:906`, `audio/Sounds.ini:938` |
| `2.wav` | `audio/GfSounds.ini:261`, `audio/Sounds.ini:914`, `audio/Sounds.ini:946` |
| `3.wav` | `audio/GfSounds.ini:268`, `audio/Sounds.ini:922`, `audio/Sounds.ini:954` |
| `4.wav` | `audio/GfSounds.ini:275`, `audio/Sounds.ini:930`, `audio/Sounds.ini:962` |
| `acquired.wav` | `audio/InterfaceSounds.ini:34`, `audio/InterfaceSounds.ini:208` |
| `exit.tga` | `interface/Intro.ini:4` |
| `interface/baseside/elite.3db` | `interface/baseside/Navbar.ini:39` |
| `interface/baseside/exit.3db` | `interface/baseside/Navbar.ini:31` |
| `interface/baseside/fighter.3db` | `interface/baseside/Navbar.ini:37` |
| `interface/baseside/frieghter.3db` | `interface/baseside/Navbar.ini:38` |
| `interface/baseside/unknown.3db` | `interface/baseside/Navbar.ini:36`, `interface/baseside/Navbar.ini:46`, `interface/baseside/Navbar.ini:66`, `interface/baseside/Navbar.ini:79`, `interface/baseside/Navbar.ini:92`, `interface/baseside/Navbar.ini:105`, `interface/baseside/Navbar.ini:118`, `interface/baseside/Navbar.ini:131`, `interface/baseside/Navbar.ini:196` |
| `interface/hud/hud_commsicon.3db` | `interface/Hud.ini:5` |
| `interface/hud/hudtarget.txm` | `interface/hud/HudTarget.ini:2` |
| `interface/intro/objects/multi_blackdragonmale.3db` | `characters/NewCharacter.ini:7` |
| `off.wav` | `audio/Sounds.ini:977` |
| `openingscreen.tga` | `interface/Intro.ini:3` |
| `ships/kusari/ku_battleship/ku_battleship_col.cmp` | `Concave.ini:38` |
| `ships/liberty/li_dreadnought/li_dreadnought_col.cmp` | `Concave.ini:82` |
| `ships/order/or_osiris/or_osiris_col.cmp` | `Concave.ini:71` |
| `ships/utility/luxury_liner/luxury_liner_col.cmp` | `Concave.ini:52` |
| `ships/utility/prison_liner/prison_liner_col.cmp` | `Concave.ini:61` |
| `solar/asteroids/roids.txm` | `solar/asteroids/Shapes.ini:2`, `solar/asteroids/Shapes.ini:69`, `solar/asteroids/Shapes.ini:80`, `solar/asteroids/Shapes.ini:91`, `solar/asteroids/Shapes.ini:102`, `solar/asteroids/Shapes.ini:113`, `solar/asteroids/Shapes.ini:124` |
| `solar/dockable/jump_gate.cmp` | `Concave.ini:17` |
| `solar/dockable/manufacturing_platform.cmp` | `Concave.ini:6` |
| `solar/dockable/rh_battleship.cmp` | `Concave.ini:14` |
| `solar/dockable/tlr_a.3db` | `Concave.ini:26` |
| `solar/dockable/tlr_d.3db` | `Concave.ini:32` |
| `solar/dockable/tlr_tube_a.cmp` | `Concave.ini:29` |
| `solar/dockable/trading_depot.cmp` | `Concave.ini:9` |
| `solar/dockable/trading_outpost_lod_col.cmp` | `Concave.ini:2` |
| `up.wav` | `audio/InterfaceSounds.ini:10` |
| `vent.wav` | `audio/Sounds.ini:1124` |

## Hinweise

- Einige Ziele sind Kollisionsmodelle (`*_col.cmp`) und Sprachdateien (`*.wav`), die auf der Disc fehlen.
- Bei Verweisen ohne Pfad (z. B. `1.wav` in `Sounds.ini`) ist der Zielordner im INI nicht angegeben. Geprüft wurde nur der Dateiname.
- Verweise auf Windows-Entwicklerpfade (`\\lancer\project\…`) sind nicht enthalten.
