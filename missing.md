# Fehlende Dateien

Dateien, auf die die INIs im SDK verweisen, die aber nicht in `NAP/` liegen. Geprüft wurden alle Asset- und INI-Verweise in `SDK/**/*.ini` (ohne `exe/`) gegen den virtuellen Root von `NAP/` (Groß-/Kleinschreibung ignoriert).

**48 fehlende Ziele**, Fundstellen: **48**.

Hinweis: Verweise ohne Ordner (z. B. `ocean_blue.cmp` in `PetalDB.ini`) sind in der Prüfung als fehlend markiert, die Dateien liegen aber unter `bases/generic/`. Diese Zeilen sind unten gekennzeichnet.

## Liste

| Ziel | Verwendet in | Bemerkung |
|---|---|---|
| `dx_s059x_0101_blix.wav` | `audio/StorySounds.ini` |  |
| `exit.tga` | `interface/Intro.ini` |  |
| `interface/baseside/elite.3db` | `interface/baseside/Navbar.ini` |  |
| `interface/baseside/exit.3db` | `interface/baseside/Navbar.ini` |  |
| `interface/baseside/fighter.3db` | `interface/baseside/Navbar.ini` |  |
| `interface/baseside/frieghter.3db` | `interface/baseside/Navbar.ini` |  |
| `interface/baseside/unknown.3db` | `interface/baseside/Navbar.ini` |  |
| `interface/hud/hud_commsicon.3db` | `interface/Hud.ini` |  |
| `interface/hud/hudtarget.txm` | `interface/hud/HudTarget.ini` |  |
| `interface/intro/objects/multi_blackdragonmale.3db` | `characters/NewCharacter.ini` |  |
| `missions/encounters/spacepop/scenes/area_homedefender_defenders-df.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/area_patrol_fighters-f.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/area_scavenger_fighters-f.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/area_trade_freighters-f-fr.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/area_trade_gunboat-f-g.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/area_trade_traders-f-fr-t.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/area_trade_transports-f-t.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_patrol_fighters-f.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_piratepatrol_fighters-f.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_piratepatrol_laneattackers-la.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_piratepatrol_wingattack-al-w.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_policepatrol_fieldpatroller-fp.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_policepatrol_patroller-pt.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_trade_fighters-f.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_trade_freighters-f-fr.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_trade_independents-td.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `missions/encounters/spacepop/scenes/path_trade_smugglers-sm.ini` | `universe/systems/intro/Intro.ini` | INI fehlt auf der CD |
| `ocean_blue.cmp` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `ocean_green.cmp` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `ocean_green_btm.3db` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `ocean_green_top.3db` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `ocean_grey_btm.3db` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `ocean_grey_top.3db` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `ocean_lime.cmp` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `ocean_navy.cmp` | `PetalDB.ini` | liegt unter bases/generic/, Verweis ohne Ordner |
| `openingscreen.tga` | `interface/Intro.ini` |  |
| `ships/kusari/ku_battleship/ku_battleship_col.cmp` | `Concave.ini` | Kollisionsmodell fehlt auf der CD |
| `ships/liberty/li_dreadnought/li_dreadnought_col.cmp` | `Concave.ini` | Kollisionsmodell fehlt auf der CD |
| `ships/order/or_osiris/or_osiris_col.cmp` | `Concave.ini` | Kollisionsmodell fehlt auf der CD |
| `ships/utility/luxury_liner/luxury_liner_col.cmp` | `Concave.ini` | Kollisionsmodell fehlt auf der CD |
| `ships/utility/prison_liner/prison_liner_col.cmp` | `Concave.ini` | Kollisionsmodell fehlt auf der CD |
| `solar/asteroids/roids.txm` | `solar/asteroids/Shapes.ini` |  |
| `solar/dockable/tlr_a.3db` | `Concave.ini` |  |
| `solar/dockable/tlr_d.3db` | `Concave.ini` |  |
| `solar/dockable/tlr_tube_a.cmp` | `Concave.ini` |  |
| `solar/dockable/trading_depot.cmp` | `Concave.ini` |  |
| `solar/dockable/trading_outpost_lod_col.cmp` | `Concave.ini` | Kollisionsmodell fehlt auf der CD |
| `startupscreen.tga` | `interface/Intro.ini` |  |

## Hinweise

- Kollisionsmodelle `*_col.cmp` der Schiffe fehlen auf der CD. Die Modelle selbst liegen vor.
- Die Verweise auf `interface/baseside/*.3db`, `hud_commsicon.3db`, `hudtarget.txm`, `tlr_*`, `roids.txm` und `multi_blackdragonmale.3db` haben keinen eindeutigen Ersatz.

## Recherche (Verbleib der Dateien)

Stand: Websuche nach den fehlenden Dateien. Es wurde keine Quelle gefunden, die belegt, wo `*_col.cmp` oder die Dateien in `interface/baseside/`, `solar/dockable/` und `ships/` außerhalb der CD liegen.

- **Schwache Hinweise:**
  - Ein Forum-Beitrag berichtet, dass defekte Collision-Gruppen in Mods als `.3db` statt `.cmp` vorlagen. Das ist nicht überprüft, würde aber erklären, warum `*_col.cmp` auf der CD nicht vorkommt. Quelle: [The Starport, Forum-Thread „Collision group docking crash“](https://the-starport.com/forums/topic/828/collision-group-docking-crash/7?post_id=6359&lang=en-US)
  - Für eine Schiffsdefinition gehören `.cmp`, `.mat` und `.sur` zusammen, und die `[CollisionGroup]`-Einträge in `shiparch.ini` verweisen darauf. Quelle: [The Starport, Thread „Adding ships into FL Vanillia“](https://the-starport.com/forums/topic/5293/adding-ships-into-fl-vanillia)
- **Werkzeuge zum Prüfen:** [FLCompanion](https://github.com/ItsRaisu/FLCompanion) liest die INIs und meldet Fehler in Mods. [treewyrm/freelancer](https://github.com/treewyrm/freelancer) ist eine Bibliothek für die Dateiformate.
- **Mod-Community:** Die Discovery-Freelancer-Gemeinschaft ([DiscoveryGC](https://github.com/DiscoveryGC)) pflegt eigene Daten. Dort wäre der Verbleib der Collision-Modelle am ehesten zu klären. Das ist nicht geprüft.

Weitere Suchen zu `debri explo`, `med explo` und dem Format der Explosionsgeräusche ergaben nichts Brauchbares.
