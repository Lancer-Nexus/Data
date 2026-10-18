# Bewertung der Normal Maps

Die Kennzahlen werden mit den Bewertungsfunktionen aus `tools/make_surface_maps.py` berechnet und beschreiben die Karten, nicht allein ihre Wirkung im Spiel. Die beiden Pygar-Stärken wurden nach einem kontrollierten ModelViewer-Lauf visuell kalibriert; der zugehörige Laufzeitbefund steht am Ende dieses Dokuments.

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
| `li_freighter1` | `freighter1.tga` | 0.56 | 1 | 7.2° / 27.9° | 0.0 % | 9 % | 0.31 | – | gut |
| `li_fighter` | `l_fighter.tga` | 1.15 | 1 | 8.6° / 28.1° | 0.0 % | 3 % | 0.34 | – | gut |
| `ku_k_panel01` | `k_panel01_256.tga` | 0.50 | 1 | 7.1° / 28.9° | 0.0 % | 8 % | 0.31 | – | gut |
| `ku_k_wings` | `k_wings.tga` | 0.72 | 1 | 6.2° / 27.9° | 0.0 % | 6 % | 0.33 | – | gut |
| `ku_metal03` | `metal03.tga` | 2.23 | 1 | 13.9° / 28.0° | 0.0 % | 0 % | 0.41 | – | gut |
| `br_player01` | `b_player01_256.tga` | 1.16 | 1 | 6.9° / 28.1° | 0.1 % | 5 % | 0.32 | – | gut |
| `br_player02` | `b_player02_256.tga` | 0.96 | 1 | 7.5° / 28.0° | 0.0 % | 5 % | 0.33 | – | gut |
| `br_player03` | `b_player03_256.tga` | 0.68 | 1 | 7.4° / 28.1° | 0.0 % | 8 % | 0.33 | – | gut |
| `br_cap_dtl1` | `b-dtl1.tga` | 0.50 | 1 | 8.7° / 30.7° | 0.0 % | 13 % | 0.32 | – | gut |
| `br_cap_dtl2` | `b-dtl2.tga` | 0.50 | 1 | 12.6° / 36.8° | 0.0 % | 6 % | 0.33 | – | gut |
| `co_p_fighter01` | `p_fighter01.tga` | 0.75 | 1 | 8.1° / 28.1° | 0.0 % | 5 % | 0.31 | – | gut |
| `co_p_fighter02` | `p_fighter02.tga` | 0.84 | 1 | 9.1° / 28.1° | 0.0 % | 3 % | 0.33 | – | gut |
| `cv_g_fighter01` | `g_fighter01.tga` | 0.50 | 1 | 6.9° / 29.7° | 0.0 % | 13 % | 0.31 | – | gut |
| `cv_g_fighter02` | `g_fighter02.tga` | 0.80 | 1 | 6.0° / 28.1° | 0.2 % | 9 % | 0.32 | – | gut |
| `or_equip_mstr` | `equip_mstr.tga` | 0.94 | 1 | 8.8° / 28.0° | 0.0 % | 7 % | 0.32 | – | gut |
| `or_liberty1` | `liberty1_256.tga` | 0.63 | 1 | 7.1° / 28.1° | 0.0 % | 5 % | 0.32 | – | gut |
| `or_weaponplate2` | `weaponplate2.tga` | 0.59 | 1 | 6.6° / 28.0° | 0.0 % | 13 % | 0.31 | – | gut |
| `ut_panels01` | `utility_panels_01.tga` | 0.51 | 1 | 6.0° / 27.9° | 0.0 % | 17 % | 0.33 | – | gut |
| `ut_liner1` | `liner1_256.tga` | 0.50 | 1 | 5.7° / 29.2° | 0.0 % | 15 % | 0.32 | – | gut |
| `bw_dig_site_16` | `dig_site_16.tga` | 0.73 | 1 | 6.1° / 27.9° | 0.0 % | 31 % | 0.31 | – | gut |
| `bw_dig_site_18` | `dig_site_18.tga` | 0.50 | 1 | 3.2° / 13.7° | 0.0 % | 38 % | 0.31 | – | gut |
| `bw_dig_site_20` | `dig_site_20.tga` | 2.00 | 1 | 3.9° / 13.4° | 0.0 % | 20 % | 0.33 | – | gut |
| `li_ceiling_gen01` | `ceiling_gen01.tga021111195321` | 2.30 | 1 | 9.1° / 28.0° | 0.0 % | 3 % | 0.35 | – | gut |
| `bw_pygar_door` | `pygar_door.tga` | 2.39 | 1 | 12.0° / 28.0° | 0.4 % | 1 % | 0.38 | – | gut |
| `bw_pygar_generator` | `pygar_generator.tga` | 0.95 | 1 | 7.6° / 28.1° | 0.1 % | 8 % | 0.32 | – | gut |
| `bw_pygar_fan` | `bw_pygar_fan.tga` | 3.80 | 1 | 11.6° / 28.0° | 0.1 % | 1 % | 0.35 | – | gut |
| `bw_concrete_base` | `concrete base 2.tga` | 4.26 | 1 | 13.3° / 28.0° | 0.0 % | 1 % | 0.36 | – | gut |
| `bw_catwalk` | `catwalk siding.tga` | 0.88 | 1 | 6.5° / 28.1° | 0.2 % | 14 % | 0.31 | – | gut |
| `bw_grate` | `grate.tga` | 0.85 | 1 | 8.4° / 28.0° | 0.0 % | 10 % | 0.31 | – | gut |
| `bw_landing_pad` | `landing pad.tga` | 0.51 | 1 | 11.9° / 28.0° | 0.0 % | 12 % | 0.32 | – | gut |
| `bw_tunnel_panel` | `tunnel inside panel.tga` | 2.95 | 1 | 13.2° / 28.0° | 0.0 % | 1 % | 0.36 | – | gut |
| `ast_rock_4` | `asteroid_rock_4` | 6.00 | 1 | 4.0° / 16.1° | 0.0 % | 40 % | 0.26 | – | gut |
| `ast_rock_r04` | `rock4.psd` | 1.90 | 1 | 11.3° / 28.1° | 0.0 % | 1 % | 0.36 | – | gut |
| `eq_turret_mturret` | `stadtl2_256.tga` | 1.26 | 1 | 9.8° / 28.0° | 0.0 % | 8 % | 0.33 | – | gut |
| `eq_turret_wins` | `stawins_128.tga` | 0.50 | 1 | 7.3° / 29.8° | 0.0 % | 25 % | 0.30 | – | gut |
| `eq_torpedo` | `weapon_1.tga` | 0.82 | 1 | 7.0° / 27.9° | 0.0 % | 11 % | 0.32 | – | gut |
| `no_dtl2` | `n-dtl2-256.tga` | 0.87 | 1 | 8.8° / 28.0° | 0.0 % | 5 % | 0.34 | – | gut |
| `planet_rock01` | `detailmap_rock01` | 1.01 | 1 | 13.2° / 28.0° | 0.0 % | 1 % | 0.39 | 0.97 | gut |
| `planet_crater_hi` | `detailmap_crater_high` | 1.43 | 1 | 11.6° / 28.0° | 0.0 % | 1 % | 0.35 | 0.80 | gut |
| `planet_crater_mid` | `detailmap_crater_mid` | 1.90 | 1 | 11.6° / 28.0° | 0.0 % | 1 % | 0.35 | 0.80 | gut |
| `planet_crater_low` | `detailmap_crater_low` | 2.86 | 1 | 11.6° / 28.0° | 0.0 % | 1 % | 0.35 | 0.80 | gut |
| `planet_ground01` | `detailmap_ground01` | 0.93 | 1 | 11.0° / 28.0° | 0.0 % | 1 % | 0.41 | 0.99 | gut |
| `planet_ice` | `detailmap_ice` | 2.80 | 1 | 12.6° / 28.0° | 0.0 % | 1 % | 0.40 | 0.99 | gut |
| `planet_lava` | `detailmap_lava` | 1.28 | 1 | 12.6° / 27.9° | 0.0 % | 1 % | 0.37 | 0.98 | gut |
| `planet_ocean` | `detailmap_ocean` | 6.00 | 1 | 14.1° / 28.0° | 0.0 % | 1 % | 0.36 | 1.66 | gut |
| `pbody_mercury01` | `mercury01` | 1.02 | 1 | 9.2° / 28.1° | 0.0 % | 3 % | 0.36 | – | gut |
| `pbody_cratermoon` | `cratermoon` | 1.35 | 1 | 8.8° / 27.9° | 0.0 % | 4 % | 0.34 | – | gut |
| `pbody_desert01` | `desert01` | 6.00 | 1 | 6.7° / 21.2° | 0.0 % | 6 % | 0.36 | – | gut |
| `pbody_desert_rock` | `desert_rock_01` | 4.47 | 1 | 9.5° / 28.0° | 0.1 % | 3 % | 0.36 | – | gut |
| `pbody_icegrey01` | `icegrey01` | 1.47 | 1 | 11.1° / 28.1° | 0.0 % | 2 % | 0.34 | – | gut |
| `pbody_icewhiteblue` | `icewhiteblue01` | 1.56 | 1 | 10.1° / 28.0° | 0.0 % | 11 % | 0.31 | – | gut |
| `pbody_indust01` | `indust01` | 0.97 | 1 | 7.2° / 28.0° | 0.0 % | 17 % | 0.37 | – | gut |

## Visuelle Laufzeitkalibrierung (2026-10-18)

Ein Same-Session-A/B des Modells `bw_pygar_airlock.cmp` zeigte bei den ursprünglichen Werten auffällige Streifen und flimmernde Highlights. Einzelkartenläufe ordneten den größten sichtbaren Beitrag `dig_site_18.tga` (Stärke 1,09) zu; `dig_site_20.tga` (4,48) wirkte auf der Decke, `dig_site_16.tga` (0,73) veränderte in der getesteten Ansicht keine Pixel. Ein gemeinsamer Kandidat mit den Stärken **0,73 / 0,50 / 2,00** erhielt reliefartige Details mit deutlich weniger Flimmern als der ursprüngliche Satz. Im Viewport-Crop 500×505 betrug das Normalmap-Ein/Aus-RMSE `0.0242191` gegenüber `0.0441831` mit den Originalwerten. Die aktiven Stärken stehen nun in `SDK/fx/SurfaceMaps.ini`, der gleichlautenden Kopie `NAP/Surface/fx/SurfaceMaps.ini` und `tools/surface_maps_params.json`.

Die Kandidatenarchive bestanden `nexus-pack verify`; alle 14 Einträge des aktiven Testmanifests stimmten bei Größe und SHA-256. Das Testarchiv enthielt ausschließlich die geänderte `SurfaceMaps.ini` und wurde aus einem QA-Verzeichnis unter `Data/NAP/` gebaut. Der A/B isoliert Normalmaps (roughness/metallic und Reflexionen aus, diffuse IBL an) in LancerEdit unter Mesa llvmpipe. Er ersetzt keine Abnahme im Spiel oder an weiteren Bretonia-Basen. Screenshots und vollständige Laufbedingungen stehen im Client-Bericht `docs/evidence/renderer/bw-pygar-map-isolation-ab-20261018/README.md`.

## Frühere automatische Tune-Prüfung

Die folgende Tabelle dokumentiert den Generatorlauf vor der visuellen Laufzeitkalibrierung; sie ist nicht der aktuelle Parametersatz.

| Karte | Stärke → | Glättung → | p95 vorher → nachher | Urteil vorher |
|---|---|---|---|---|
| `li_elite_hull` | 0.62 → 0.62 | 1 → 1 | 28.2° → 28.2° | gut |
| `li_engine_grill` | 0.50 → 0.50 | 1 → 1 | 28.3° → 28.3° | gut |
| `li_equip_gen` | 0.62 → 0.62 | 1 → 1 | 28.1° → 28.1° | gut |
| `li_freighter1` | 0.56 → 0.56 | 1 → 1 | 27.9° → 27.9° | gut |
| `li_fighter` | 1.15 → 1.15 | 1 → 1 | 28.1° → 28.1° | gut |
| `ku_k_panel01` | 0.50 → 0.50 | 1 → 1 | 28.9° → 28.9° | gut |
| `ku_k_wings` | 0.72 → 0.72 | 1 → 1 | 27.9° → 27.9° | gut |
| `ku_metal03` | 2.23 → 2.23 | 1 → 1 | 28.0° → 28.0° | gut |
| `br_player01` | 1.16 → 1.16 | 1 → 1 | 28.1° → 28.1° | gut |
| `br_player02` | 0.96 → 0.96 | 1 → 1 | 28.0° → 28.0° | gut |
| `br_player03` | 0.68 → 0.68 | 1 → 1 | 28.1° → 28.1° | gut |
| `br_cap_dtl1` | 0.50 → 0.50 | 1 → 1 | 30.7° → 30.7° | gut |
| `br_cap_dtl2` | 0.50 → 0.50 | 1 → 1 | 36.8° → 36.8° | gut |
| `co_p_fighter01` | 0.75 → 0.75 | 1 → 1 | 28.1° → 28.1° | gut |
| `co_p_fighter02` | 0.84 → 0.84 | 1 → 1 | 28.1° → 28.1° | gut |
| `cv_g_fighter01` | 0.50 → 0.50 | 1 → 1 | 29.7° → 29.7° | gut |
| `cv_g_fighter02` | 0.80 → 0.80 | 1 → 1 | 28.1° → 28.1° | gut |
| `or_equip_mstr` | 0.94 → 0.94 | 1 → 1 | 28.0° → 28.0° | gut |
| `or_liberty1` | 0.63 → 0.63 | 1 → 1 | 28.1° → 28.1° | gut |
| `or_weaponplate2` | 0.59 → 0.59 | 1 → 1 | 28.0° → 28.0° | gut |
| `ut_panels01` | 0.51 → 0.51 | 1 → 1 | 27.9° → 27.9° | gut |
| `ut_liner1` | 0.50 → 0.50 | 1 → 1 | 29.2° → 29.2° | gut |
| `bw_dig_site_16` | 0.73 → 0.73 | 1 → 1 | 27.9° → 27.9° | gut |
| `bw_dig_site_18` | 1.09 → 1.09 | 1 → 1 | 27.9° → 27.9° | gut |
| `bw_dig_site_20` | 4.48 → 4.48 | 1 → 1 | 28.0° → 28.0° | gut |
| `li_ceiling_gen01` | 2.30 → 2.30 | 1 → 1 | 28.0° → 28.0° | gut |
| `bw_pygar_door` | 2.39 → 2.39 | 1 → 1 | 28.0° → 28.0° | gut |
| `bw_pygar_generator` | 0.95 → 0.95 | 1 → 1 | 28.1° → 28.1° | gut |
| `bw_pygar_fan` | 3.80 → 3.80 | 1 → 1 | 28.0° → 28.0° | gut |
| `bw_concrete_base` | 4.26 → 4.26 | 1 → 1 | 28.0° → 28.0° | gut |
| `bw_catwalk` | 0.88 → 0.88 | 1 → 1 | 28.1° → 28.1° | gut |
| `bw_grate` | 0.85 → 0.85 | 1 → 1 | 28.0° → 28.0° | gut |
| `bw_landing_pad` | 0.51 → 0.51 | 1 → 1 | 28.0° → 28.0° | gut |
| `bw_tunnel_panel` | 2.95 → 2.95 | 1 → 1 | 28.0° → 28.0° | gut |
| `ast_rock_4` | 6.00 → 6.00 | 1 → 1 | 16.1° → 16.1° | gut |
| `ast_rock_r04` | 1.90 → 1.90 | 1 → 1 | 28.1° → 28.1° | gut |
| `eq_turret_mturret` | 1.26 → 1.26 | 1 → 1 | 28.0° → 28.0° | gut |
| `eq_turret_wins` | 0.50 → 0.50 | 1 → 1 | 29.8° → 29.8° | gut |
| `eq_torpedo` | 0.82 → 0.82 | 1 → 1 | 27.9° → 27.9° | gut |
| `no_dtl2` | 0.87 → 0.87 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_rock01` | 1.01 → 1.01 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_crater_hi` | 1.43 → 1.43 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_crater_mid` | 1.90 → 1.90 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_crater_low` | 2.86 → 2.86 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_ground01` | 0.93 → 0.93 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_ice` | 2.80 → 2.80 | 1 → 1 | 28.0° → 28.0° | gut |
| `planet_lava` | 1.28 → 1.28 | 1 → 1 | 27.9° → 27.9° | gut |
| `planet_ocean` | 6.00 → 6.00 | 1 → 1 | 28.0° → 28.0° | gut |
| `pbody_mercury01` | 1.02 → 1.02 | 1 → 1 | 28.1° → 28.1° | gut |
| `pbody_cratermoon` | 1.35 → 1.35 | 1 → 1 | 27.9° → 27.9° | gut |
| `pbody_desert01` | 6.00 → 6.00 | 1 → 1 | 21.2° → 21.2° | gut |
| `pbody_desert_rock` | 4.47 → 4.47 | 1 → 1 | 28.0° → 28.0° | gut |
| `pbody_icegrey01` | 1.47 → 1.47 | 1 → 1 | 28.1° → 28.1° | gut |
| `pbody_icewhiteblue` | 1.56 → 1.56 | 1 → 1 | 28.0° → 28.0° | gut |
| `pbody_indust01` | 0.97 → 0.97 | 1 → 1 | 28.0° → 28.0° | gut |
