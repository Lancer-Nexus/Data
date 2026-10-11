# Bewertung der Normal Maps

Erzeugt von `tools/make_surface_maps.py --evaluate` bzw. `--tune`. Die Kennzahlen beschreiben die erzeugten Karten, nicht ihre Wirkung im Spiel.

| Kennzahl | Bedeutung | Zielbereich |
|---|---|---|
| Neigung Mittel / p95 | Winkel der Normalen gegen die Fläche (Grad); p95 = 95 % der Pixel neigen höchstens so | p95 12 bis 40 (Ziel 28) |
| steil | Anteil der Pixel mit mehr als 60° | höchstens 1 % |
| flach | Anteil der Pixel mit weniger als 1° | höchstens 85 % |
| Körnung | Energie des Pixelrauschens im Verhältnis zur mittleren Struktur | höchstens 1,5 |
| Naht | Kantenunterschied beim Kacheln im Verhältnis zum Nachbarpixel; nur für die kachelnden Planetenkarten bewertet | höchstens 2,5 |

| Karte | Quelle | Stärke | Glättung | Neigung Mittel / p95 | steil | flach | Körnung | Naht | Urteil |
|---|---|---:|---:|---|---:|---:|---:|---:|---|
| `li_elite_hull` | `elite_256.tga` | 0.62 | 1 | 7.2° / 28.2° | 0.0 % | 6 % | 0.33 | – | gut |
| `li_engine_grill` | `engine_grill01.tga` | 0.50 | 1 | 5.9° / 28.3° | 0.0 % | 36 % | 0.32 | – | gut |
| `li_equip_gen` | `equip_gen.tga` | 0.62 | 1 | 8.5° / 28.1° | 0.0 % | 7 % | 0.31 | – | gut |
| `bw_dig_site_16` | `dig_site_16.tga` | 0.73 | 1 | 6.1° / 27.9° | 0.0 % | 31 % | 0.31 | – | gut |
| `bw_dig_site_18` | `dig_site_18.tga` | 1.09 | 1 | 6.7° / 27.9° | 0.2 % | 15 % | 0.31 | – | gut |
| `li_ceiling_gen01` | `ceiling_gen01.tga021111195321` | 2.30 | 1 | 9.1° / 28.0° | 0.0 % | 3 % | 0.35 | – | gut |
| `ku_k_panel01` | `k_panel01_256.tga` | 0.50 | 1 | 7.1° / 28.9° | 0.0 % | 8 % | 0.31 | – | gut |
| `ku_k_wings` | `k_wings.tga` | 0.72 | 1 | 6.2° / 27.9° | 0.0 % | 6 % | 0.33 | – | gut |
| `ku_metal03` | `metal03.tga` | 2.23 | 1 | 13.9° / 28.0° | 0.0 % | 0 % | 0.41 | – | gut |
| `br_player01` | `b_player01_256.tga` | 1.16 | 1 | 6.9° / 28.1° | 0.1 % | 5 % | 0.32 | – | gut |
| `ast_rock_4` | `asteroid_rock_4` | 6.00 | 1 | 4.0° / 16.1° | 0.0 % | 40 % | 0.26 | – | gut |
| `planet_ice` | `detailmap_ice` | 2.80 | 1 | 12.6° / 28.0° | 0.0 % | 1 % | 0.40 | 0.99 | gut |
| `planet_lava` | `detailmap_lava` | 1.28 | 1 | 12.6° / 27.9° | 0.0 % | 1 % | 0.37 | 0.98 | gut |
| `planet_rock01` | `detailmap_rock01` | 1.01 | 1 | 13.2° / 28.0° | 0.0 % | 1 % | 0.39 | 0.97 | gut |
| `planet_crater_hi` | `detailmap_crater_high` | 1.43 | 1 | 11.6° / 28.0° | 0.0 % | 1 % | 0.35 | 0.80 | gut |
| `planet_ground01` | `detailmap_ground01` | 0.93 | 1 | 11.0° / 28.0° | 0.0 % | 1 % | 0.41 | 0.99 | gut |

## Vor der Anpassung

| Karte | Stärke → | Glättung → | p95 vorher → nachher | Urteil vorher |
|---|---|---|---|---|
| `li_elite_hull` | 0.62 → 0.62 | 1 → 1 | 28.2° → 28.2° | gut |
| `li_engine_grill` | 0.50 → 0.50 | 1 → 1 | 28.3° → 28.3° | gut |
| `li_equip_gen` | 0.62 → 0.62 | 1 → 1 | 28.1° → 28.1° | gut |
| `bw_dig_site_16` | 0.73 → 0.73 | 1 → 1 | 27.9° → 27.9° | gut |
| `bw_dig_site_18` | 1.09 → 1.09 | 1 → 1 | 27.9° → 27.9° | gut |
| `li_ceiling_gen01` | 2.30 → 2.30 | 1 → 1 | 28.0° → 28.0° | gut |
| `ku_k_panel01` | 0.50 → 0.50 | 1 → 1 | 28.9° → 28.9° | gut |
| `ku_k_wings` | 0.72 → 0.72 | 1 → 1 | 27.9° → 27.9° | gut |
| `ku_metal03` | 2.23 → 2.23 | 1 → 1 | 28.0° → 28.0° | gut |
| `br_player01` | 1.16 → 1.16 | 1 → 1 | 28.1° → 28.1° | gut |
| `ast_rock_4` | 3.00 → 6.00 | 1 → 1 | 8.2° → 16.1° | zu flach |
| `planet_ice` | 2.80 → 2.80 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_lava` | 1.28 → 1.28 | 1 → 1 | 27.9° → 27.9° | gut |
| `planet_rock01` | 1.01 → 1.01 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_crater_hi` | 1.43 → 1.43 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_ground01` | 0.93 → 0.93 | 1 → 1 | 28.0° → 28.0° | gut |
