# Bewertung der automatisch erzeugten Normal Maps (Schiffe und Basen)

Erzeugt von `tools/make_surface_maps_bulk.py`. Die Kennzahlen beschreiben die Karten, nicht ihre Wirkung im Spiel.

## Auswahl

| Schritt | Texturen |
|---|---:|
| gesamt | 4398 |
| Name aussortiert | 807 |
| Duplikat | 460 |
| Name nicht eindeutig | 144 |
| schon kuratiert | 110 |
| unter 256 px | 97 |
| **erzeugt** | **2751** |
| übersprungen: zu flach (p95 unter 8°) | 18 |
| übersprungen: kaum Relief | 11 |

## Ergebnis

- Dateien: 30, zusammen 1256 MB
- Gruppen: Schiffe 46, Basen 2620, Solar 85; 1024 px: 97, 512 px: 2654
- Stärke: Median 1.48, Spanne 0.50 bis 6.00; an der Untergrenze 0,5: 77, an der Obergrenze 6,0: 121
- p95 der Neigung: Median 28.0°, Spanne 8.0° bis 39.5°; unter 12° (flach): 13, über 40°: 0

## Roughness und Metallic

Aus der Diffuse-Textur abgeleitet (Helligkeit, Detail, Sättigung), als BC4. Schiffe 512 px, Basen und Solar 256 px.

| Gruppe | Karten | Roughness Mittel | Roughness Streuung | Metallic Mittel | Metallic Streuung | ohne Metallic-Karte (Mittel unter 0,05, Faktor 0) |
|---|---:|---:|---:|---:|---:|---:|
| ships | 46 | 0.45 | 0.12 | 0.32 | 0.11 | 3 |
| bases | 2620 | 0.60 | 0.10 | 0.10 | 0.11 | 1346 |
| solar | 85 | 0.67 | 0.11 | 0.17 | 0.07 | 36 |

## Bibliotheken

| Datei | Größe |
|---|---:|
| `Shader/fx/normalmaps_bases_backdrops_1.txm` | 7.4 MB |
| `Shader/fx/normalmaps_bases_bretonia_1.txm` | 50.1 MB |
| `Shader/fx/normalmaps_bases_bretonia_2.txm` | 50.0 MB |
| `Shader/fx/normalmaps_bases_bretonia_3.txm` | 50.4 MB |
| `Shader/fx/normalmaps_bases_bretonia_4.txm` | 50.1 MB |
| `Shader/fx/normalmaps_bases_bretonia_5.txm` | 7.6 MB |
| `Shader/fx/normalmaps_bases_generic_1.txm` | 50.0 MB |
| `Shader/fx/normalmaps_bases_generic_2.txm` | 22.3 MB |
| `Shader/fx/normalmaps_bases_kusari_1.txm` | 50.2 MB |
| `Shader/fx/normalmaps_bases_kusari_2.txm` | 50.0 MB |
| `Shader/fx/normalmaps_bases_kusari_3.txm` | 50.3 MB |
| `Shader/fx/normalmaps_bases_kusari_4.txm` | 50.2 MB |
| `Shader/fx/normalmaps_bases_kusari_5.txm` | 40.9 MB |
| `Shader/fx/normalmaps_bases_liberty_1.txm` | 50.2 MB |
| `Shader/fx/normalmaps_bases_liberty_2.txm` | 50.0 MB |
| `Shader/fx/normalmaps_bases_liberty_3.txm` | 50.3 MB |
| `Shader/fx/normalmaps_bases_liberty_4.txm` | 50.0 MB |
| `Shader/fx/normalmaps_bases_liberty_5.txm` | 50.1 MB |
| `Shader/fx/normalmaps_bases_liberty_6.txm` | 2.1 MB |
| `Shader/fx/normalmaps_bases_pirate_1.txm` | 50.4 MB |
| `Shader/fx/normalmaps_bases_pirate_2.txm` | 32.9 MB |
| `Shader/fx/normalmaps_bases_rheinland_1.txm` | 50.1 MB |
| `Shader/fx/normalmaps_bases_rheinland_2.txm` | 50.2 MB |
| `Shader/fx/normalmaps_bases_rheinland_3.txm` | 50.4 MB |
| `Shader/fx/normalmaps_bases_rheinland_4.txm` | 50.3 MB |
| `Shader/fx/normalmaps_bases_rheinland_5.txm` | 21.2 MB |
| `Shader/fx/normalmaps_ships_auto_1.txm` | 48.8 MB |
| `Shader/fx/normalmaps_ships_auto_2.txm` | 31.1 MB |
| `Shader/fx/normalmaps_solar_auto_1.txm` | 50.1 MB |
| `Shader/fx/normalmaps_solar_auto_2.txm` | 39.0 MB |
