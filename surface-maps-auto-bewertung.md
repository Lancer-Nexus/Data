# Bewertung der automatisch erzeugten Normal Maps (Schiffe und Basen)

Erzeugt von `tools/make_surface_maps_bulk.py`. Die Kennzahlen beschreiben die Karten, nicht ihre Wirkung im Spiel.

## Auswahl

| Schritt | Texturen |
|---|---:|
| gesamt | 4057 |
| Name aussortiert | 730 |
| Duplikat | 364 |
| Name nicht eindeutig | 98 |
| schon kuratiert | 91 |
| unter 256 px | 76 |
| **erzeugt** | **2670** |
| übersprungen: zu flach (p95 unter 8°) | 18 |
| übersprungen: kaum Relief | 10 |

## Ergebnis

- Dateien: 28, zusammen 1173 MB
- Schiffe: 49 Karten (1024 px), Basen: 2621 (512 px)
- Stärke: Median 1.50, Spanne 0.50 bis 6.00; an der Untergrenze 0,5: 69, an der Obergrenze 6,0: 121
- p95 der Neigung: Median 28.0°, Spanne 8.0° bis 39.5°; unter 12° (flach): 13, über 40°: 0

## Roughness und Metallic

Aus der Diffuse-Textur abgeleitet (Helligkeit, Detail, Sättigung), als BC4. Schiffe 512 px, Basen 256 px.

| Gruppe | Karten | Roughness Mittel | Roughness Streuung | Metallic Mittel | Metallic Streuung | ohne Metallic-Karte (Mittel unter 0,05, Faktor 0) |
|---|---:|---:|---:|---:|---:|---:|
| ships | 49 | 0.45 | 0.12 | 0.32 | 0.11 | 3 |
| bases | 2621 | 0.60 | 0.10 | 0.10 | 0.11 | 1346 |

## Bibliotheken

| Datei | Größe |
|---|---:|
| `Material/fx/normalmaps_bases_backdrops_1.txm` | 7.4 MB |
| `Material/fx/normalmaps_bases_bretonia_1.txm` | 50.1 MB |
| `Material/fx/normalmaps_bases_bretonia_2.txm` | 50.0 MB |
| `Material/fx/normalmaps_bases_bretonia_3.txm` | 50.4 MB |
| `Material/fx/normalmaps_bases_bretonia_4.txm` | 50.1 MB |
| `Material/fx/normalmaps_bases_bretonia_5.txm` | 7.6 MB |
| `Material/fx/normalmaps_bases_generic_1.txm` | 50.0 MB |
| `Material/fx/normalmaps_bases_generic_2.txm` | 22.8 MB |
| `Material/fx/normalmaps_bases_kusari_1.txm` | 50.2 MB |
| `Material/fx/normalmaps_bases_kusari_2.txm` | 50.0 MB |
| `Material/fx/normalmaps_bases_kusari_3.txm` | 50.3 MB |
| `Material/fx/normalmaps_bases_kusari_4.txm` | 50.2 MB |
| `Material/fx/normalmaps_bases_kusari_5.txm` | 40.9 MB |
| `Material/fx/normalmaps_bases_liberty_1.txm` | 50.2 MB |
| `Material/fx/normalmaps_bases_liberty_2.txm` | 50.0 MB |
| `Material/fx/normalmaps_bases_liberty_3.txm` | 50.3 MB |
| `Material/fx/normalmaps_bases_liberty_4.txm` | 50.0 MB |
| `Material/fx/normalmaps_bases_liberty_5.txm` | 50.1 MB |
| `Material/fx/normalmaps_bases_liberty_6.txm` | 2.1 MB |
| `Material/fx/normalmaps_bases_pirate_1.txm` | 50.4 MB |
| `Material/fx/normalmaps_bases_pirate_2.txm` | 32.9 MB |
| `Material/fx/normalmaps_bases_rheinland_1.txm` | 50.1 MB |
| `Material/fx/normalmaps_bases_rheinland_2.txm` | 50.2 MB |
| `Material/fx/normalmaps_bases_rheinland_3.txm` | 50.4 MB |
| `Material/fx/normalmaps_bases_rheinland_4.txm` | 50.3 MB |
| `Material/fx/normalmaps_bases_rheinland_5.txm` | 21.2 MB |
| `Material/fx/normalmaps_ships_auto_1.txm` | 48.8 MB |
| `Material/fx/normalmaps_ships_auto_2.txm` | 36.4 MB |
