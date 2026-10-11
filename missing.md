# Fehlende Dateien

Dateien, auf die die INIs im SDK verweisen, die aber nicht in `NAP/` liegen. Geprüft wurden alle Asset-Verweise in `SDK/**/*.ini` (ohne Entwicklerpfade `E:\lancer\…` in `ButtonMontage.ini`) gegen den virtuellen Root von `NAP/` (Groß-/Kleinschreibung ignoriert).

**21 fehlende Ziele** mit insgesamt **35 Fundstellen**.

Die Dateien stammen von der Original-CD (`CAB1.CAB`, `CAB2.CAB`). Ein Eintrag bedeutet: Die Datei fehlt auf der CD oder liegt an einem anderen Pfad.

## Liste

| Ziel | Verwendet in (INI:Zeile) |
|---|---|
| `exit.tga` | `interface/Intro.ini:4` |
| `interface/baseside/elite.3db` | `interface/baseside/Navbar.ini:39` |
| `interface/baseside/exit.3db` | `interface/baseside/Navbar.ini:31` |
| `interface/baseside/fighter.3db` | `interface/baseside/Navbar.ini:37` |
| `interface/baseside/frieghter.3db` | `interface/baseside/Navbar.ini:38` |
| `interface/baseside/unknown.3db` | `interface/baseside/Navbar.ini:36`, `interface/baseside/Navbar.ini:46`, `interface/baseside/Navbar.ini:66`, `interface/baseside/Navbar.ini:79`, `interface/baseside/Navbar.ini:92`, `interface/baseside/Navbar.ini:105`, `interface/baseside/Navbar.ini:118`, `interface/baseside/Navbar.ini:131`, `interface/baseside/Navbar.ini:196` |
| `interface/hud/hud_commsicon.3db` | `interface/Hud.ini:5` |
| `interface/hud/hudtarget.txm` | `interface/hud/HudTarget.ini:2` |
| `interface/intro/objects/multi_blackdragonmale.3db` | `characters/NewCharacter.ini:7` |
| `openingscreen.tga` | `interface/Intro.ini:3` |
| `ships/kusari/ku_battleship/ku_battleship_col.cmp` | `Concave.ini:38` |
| `ships/liberty/li_dreadnought/li_dreadnought_col.cmp` | `Concave.ini:82` |
| `ships/order/or_osiris/or_osiris_col.cmp` | `Concave.ini:71` |
| `ships/utility/luxury_liner/luxury_liner_col.cmp` | `Concave.ini:52` |
| `ships/utility/prison_liner/prison_liner_col.cmp` | `Concave.ini:61` |
| `solar/asteroids/roids.txm` | `solar/asteroids/Shapes.ini:2`, `solar/asteroids/Shapes.ini:69`, `solar/asteroids/Shapes.ini:80`, `solar/asteroids/Shapes.ini:91`, `solar/asteroids/Shapes.ini:102`, `solar/asteroids/Shapes.ini:113`, `solar/asteroids/Shapes.ini:124` |
| `solar/dockable/tlr_a.3db` | `Concave.ini:26` |
| `solar/dockable/tlr_d.3db` | `Concave.ini:32` |
| `solar/dockable/tlr_tube_a.cmp` | `Concave.ini:29` |
| `solar/dockable/trading_depot.cmp` | `Concave.ini:9` |
| `solar/dockable/trading_outpost_lod_col.cmp` | `Concave.ini:2` |

## Hinweise

- Kollisionsmodelle `*_col.cmp` der Schiffe fehlen auf der CD. Die Modelle selbst (`ships/…/*.cmp`) sind vorhanden.
- Die Verweise auf `interface/baseside/*.3db`, `hud_commsicon.3db`, `hudtarget.txm`, `tlr_*`, `roids.txm` und `multi_blackdragonmale.3db` haben keinen eindeutigen Ersatz. Sie sind offen.
- Korrigierte Namen (Leerzeichen → `_`, Korrekturen in `Concave.ini`) stehen in `SDK/changelog.md`.


## Recherche (Verbleib der Dateien)

Stand: Websuche nach den fehlenden Dateien. Es wurde keine Quelle gefunden, die belegt, wo `*_col.cmp` oder die Dateien in `interface/baseside/`, `solar/dockable/` und `ships/` außerhalb der CD liegen.

- **Schwache Hinweise:**
  - Ein Forum-Beitrag berichtet, dass defekte Collision-Gruppen in Mods als `.3db` statt `.cmp` vorlagen. Das ist nicht überprüft, würde aber erklären, warum `*_col.cmp` auf der CD nicht vorkommt. Quelle: [The Starport, Forum-Thread „Collision group docking crash“](https://the-starport.com/forums/topic/828/collision-group-docking-crash/7?post_id=6359&lang=en-US)
  - Für eine Schiffsdefinition gehören `.cmp`, `.mat` und `.sur` zusammen, und die `[CollisionGroup]`-Einträge in `shiparch.ini` verweisen darauf. Quelle: [The Starport, Thread „Adding ships into FL Vanillia“](https://the-starport.com/forums/topic/5293/adding-ships-into-fl-vanillia)
- **Werkzeuge zum Prüfen:** [FLCompanion](https://github.com/ItsRaisu/FLCompanion) liest die INIs und meldet Fehler in Mods. [treewyrm/freelancer](https://github.com/treewyrm/freelancer) ist eine Bibliothek für die Dateiformate.
- **Mod-Community:** Die Discovery-Freelancer-Gemeinschaft ([DiscoveryGC](https://github.com/DiscoveryGC)) pflegt eigene Daten. Dort wäre der Verbleib der Collision-Modelle am ehesten zu klären. Das ist nicht geprüft.

Weitere Suchen zu `debri explo`, `med explo` und dem Format der Explosionsgeräusche ergaben nichts Brauchbares.
