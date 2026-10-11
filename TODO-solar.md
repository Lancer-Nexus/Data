# TODO: Solar-INIs aus der HD-Edition prüfen

## Was übernommen wurde

Aus `DATA/SOLAR/` der HD-Edition, 78 Dateien in `SDK/solar/`:

| Ordner | Dateien | Stand |
|---|---:|---|
| `nebula/` | 64 | übernommen, 59 mit anderen Werten, 5 identisch |
| `rings/` | 10 | übernommen, alle identisch (`Shapes.ini` war schon übernommen) |
| Wurzel | `SolarArch.ini`, `StarArch.ini`, `Asteroidarch.ini`, `Loadouts.ini` | übernommen |

Asteroiden (`asteroids/`) und Schwarze Löcher (`blackhole/`) sind separat übernommen, siehe `TODO-asteroiden.md` und `TODO-blackhole.md`.

## Pfade in SolarArch.ini

Die HD-Edition enthält keine Planetendateien. Ihre `SolarArch.ini` verweist aber auf die Struktur von 1.3: `solar\planets\planet_x\planet_x.mat` und `solar\planets\detailmaps\x.txm`. Unser `NAP/` hat diese Dateien flach in `solar/planets/`. Die Verweise wurden deshalb angepasst:
- `solar\planets\planet_x\planet_x.mat` → `solar\planets\planet_x.mat`
- `solar\planets\detailmaps\x.txm` → `solar\planets\x.txm`

Alle 932 Asset-Verweise der Datei lösen sich danach auf.

Die Verweise auf INIs wurden auf unsere Dateinamen umgestellt (z. B. `rock_shapes.ini` → `RockShapes.ini`).

## Zu prüfen im Spiel

- [ ] Ob die Nebel mit den HD-Werten korrekt aussehen (59 Dateien geändert). Die Dateien sind inhaltlich nicht mehr gleich mit der Version 1.3.
- [ ] Ob die Planeten mit den flachen Materialpfaden geladen werden und die Texturen stimmen.
- [ ] Ob die Sterne (`StarArch.ini`) und Sonnen-Einstellungen funktionieren.
- [ ] Ob die Loadouts für die Sonnen- und Asteroidenstationen laden.
- [ ] Ob die HD-Werte in `SolarArch.ini` (z. B. Planetenradien, Atmosphären) dem Original entsprechen oder ob Felder fehlen.

## Offen

- [ ] 7 Verweise auf `solar/asteroids/roids.txm` lösen sich nicht auf (Datei fehlt auf der CD, siehe `missing.md`).
- [ ] Die Änderungen sind noch nicht committet.
