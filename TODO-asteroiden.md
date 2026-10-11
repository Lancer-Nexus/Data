# TODO: Asteroiden-Werte aus der HD-Edition prüfen

## Was übernommen wurde

152 Dateien in `SDK/solar/asteroids/` wurden mit den Werten aus der HD-Edition (`DATA/SOLAR/ASTEROIDS/`) überschrieben. 4 Dateien waren schon identisch. Zwei Dateien, die nur in der SDK liegen (`Li01DebrisFieldSmall.ini`, `Shapes.ini`), sind unverändert.

Die HD-Dateien verweisen auf Formen-INIs mit Unterstrichen (`rock_shapes.ini`). Die Verweise wurden auf unsere Namen umgestellt (`RockShapes.ini`). Ansonsten ist der Inhalt übernommen.

Die Änderungen in den Werten:

| Schlüssel | Änderung | Dateien (ca.) |
|---|---|---:|
| `fill_dist` | ×2 oder ×1,2 | 98 bzw. 53 |
| `start_dist` | ×2 oder ×1,2 | 90 bzw. 7 |
| `fade_dist_percent`, `height`, `offset_dist` | teils gleich, teils geändert | je 6–77 |
| neue Abschnitte | `shape`, `exclusion`, `[ExclusionBand]`, `zone`, `render_parts`, `fade` | einzeln |

Rückgängig machen: `git checkout <commit-vor-übernahme> -- SDK/solar/asteroids` (der Stand vor der Übernahme ist der letzte Commit auf `sdk-1.3.1`).

## Zu prüfen im Spiel

- [ ] Ob die verdoppelten Abstände (`fill_dist`, `start_dist`) das Spielgefühl ändern: Asteroidenfelder sind jetzt größer und werden später sichtbar.
- [ ] Ob die Asteroidenfelder überhaupt geladen werden und keine Abstürze oder fehlenden Felder auftreten.
- [ ] Ob die Formen (`RockShapes.ini`, `DebrisShapes.ini`, `IceShapes.ini`, `MineShapes.ini`) mit den neuen Verweisen korrekt geladen werden.
- [ ] Ob die neuen Abschnitte (`shape`, `exclusion`, `zone`, `render_parts`, `fade`) von der Engine der Version 1.3 unterstützt werden. Sie stammen aus der HD-Edition, die ggf. eine neuere Engine nutzt.
- [ ] Ob die Dichte und die Farbe der Felder mit den übernommenen Werten zusammenpassen (`ambient_intensity`, `color_shift`).

## Offen

- [ ] 7 Verweise auf `solar/asteroids/roids.txm` lösen sich nicht auf. Die Datei fehlt auf der CD (siehe `missing.md`). Entscheidung: durch eine vorhandene Textur ersetzen oder so lassen.
- [ ] Die Änderungen sind noch nicht committet.
