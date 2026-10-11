# Changelog – Freelancer SDK Daten

Änderungen der INI-Dateien im SDK-Ordner gegenüber der Original-CD (Version 1.0).

| Version | Basis | Beschreibung | Dateien |
|---|---|---|---|
| [1.3.1](#131) | 1.3 | Korrekturen am SDK (diese Sammlung) | 6 + 3 neu (`EXE/`) |
| [1.3](#13-gegenüber-10) | 1.0 | Offizieller Patch 1.0 → 1.3 | 129 |

> Die Diffs stammen aus dem Textvergleich der jeweiligen Dateien. `-` ist der Zustand der Basisversion, `+` der neue Zustand. Zeilennummern beziehen sich auf die jeweilige Datei.

## 1.3.1

Korrekturen gegenüber 1.3. Alle Änderungen betreffen Formatfehler, keine Spielinhalte. Neu aufgenommen sind die drei INI-Dateien aus `EXE/`.

### Fixes gegenüber 1.3

| Datei | Änderung |
|---|---|
| `initialworld.ini` | Geschützte Leerzeichen (`0xA0`) in 53 Zeilen durch normale Leerzeichen ersetzt; Datei ist jetzt reines ASCII/UTF-8 |
| `Universe/Systems/Li02/Bases/Rooms/Li02_01_cityscape.ini` | Tippfehler `:gap` → `gap` in `[FlashlightSet]` (Wert wurde nie gelesen) |

### Angleichung an die Original-CD

Abweichungen zwischen dem 1.3-SDK und den BINI-Daten der CD, die im 1.3-Changelog nicht enthalten waren (kosmetisch, ohne Wirkung):

| Datei | Änderung |
|---|---|
| `Equipment/select_equip.ini` | `hit_pts_scale` gerundet |
| `Interface/Baseside/navbar.ini` | Leere Schlüssel ohne ` =` (`behavior`, `mesh`, `hardpoint`, `event`) |
| `Solar/asteroids/br02_birmingham_ice_asteroid_field.ini` | `-0.000000` → `0.000000` |
| `Universe/Systems/intro/intro.ini` | `difficulty =` → `difficulty` |

### Neu: `EXE/` (Konfiguration aus dem Spielverzeichnis)

Die drei INI-Dateien aus `exe\` der Original-CD (`CAB1.CAB`) gehören nicht zu `data/`, wurden aber ins SDK aufgenommen. Sie liegen im Unterordner `EXE/`.

| Datei | Größe | Inhalt |
|---|---:|---|
| `EXE/Freelancer.ini` | 12379 B | Hauptkonfiguration: Datenpfad, `initial_world`, Startfilme, DLLs, alle `[Data]`-Dateien |
| `EXE/DACOM.ini` | 5622 B | Engine-Bibliotheken, Render- und Material-Konfiguration |
| `EXE/dacomsrv.ini` | 339 B | Server-Variante der DACOM-Konfiguration |

Prüfung gegen CD und SDK:

- Alle 97 `[Data]`-INIs aus `Freelancer.ini` sind im SDK vorhanden.
- Alle referenzierten DLLs und Startfilme sind auf der CD vorhanden.
- `@include FL_Dev.ini` und `@include FL_DevOnlyLibs.ini` (Entwicklerdateien) existieren auch auf der CD nicht, sie sind optional.
- `FX/fuse_li_battleship.ini` ist in `Freelancer.ini` nicht eingetragen (wie im Original), die enthaltenen Fuses werden nirgends verwendet.

`DACOM.ini` und `dacomsrv.ini` sind unverändert gegenüber der CD.

#### `EXE/Freelancer.ini`

Änderung gegenüber der CD: Dateipfade im Abschnitt `[Data]` an die exakte Groß-/Kleinschreibung der SDK-Dateinamen angepasst (nötig für case-sensitive Dateisysteme, z. B. Linux/Wine). Unter Windows ohne Wirkung.

94 Hunks, +94 / −94 Zeilen · Tue Feb 04 00:00:00 2003 → Sun Oct 11 14:14:04 2026

<details><summary>Diff anzeigen (282 Zeilen)</summary>

```diff
@@ -84 +84 @@
-       solar = solar\solararch.ini
+       solar = Solar\SolarArch.ini
@@ -85 +85 @@
-    universe = universe\universe.ini
+    universe = Universe\universe.ini
@@ -86 +86 @@
-   constants = constants.ini				;constant variables
+   constants = Constants.ini				;constant variables
@@ -87 +87 @@
-       fonts = fonts\fonts.ini
+       fonts = Fonts\fonts.ini
@@ -89 +89 @@
-  rich_fonts = fonts\rich_fonts.ini
+  rich_fonts = Fonts\rich_fonts.ini
@@ -90 +90 @@
-      sounds = audio\ambience_sounds.ini                ;sound-effects (NOT music) for exterior map locations, regions, areas and solar objects
+      sounds = Audio\ambience_sounds.ini                ;sound-effects (NOT music) for exterior map locations, regions, areas and solar objects
@@ -91 +91 @@
-      sounds = audio\sounds.ini				;all sfx not falling into some other category
+      sounds = Audio\sounds.ini				;all sfx not falling into some other category
@@ -92 +92 @@
-      sounds = audio\engine_sounds.ini			;engine sounds only
+      sounds = Audio\engine_sounds.ini			;engine sounds only
@@ -93 +93 @@
-      sounds = audio\interface_sounds.ini
+      sounds = Audio\interface_sounds.ini
@@ -94 +94 @@
-      sounds = audio\music.ini
+      sounds = Audio\music.ini
@@ -95 +95 @@
-      sounds = audio\story_sounds.ini			;dialogue for the story (except for news broadcasts)
+      sounds = Audio\story_sounds.ini			;dialogue for the story (except for news broadcasts)
@@ -96 +96 @@
-      sounds = audio\gf_sounds.ini			;sound-effects for gameflow - bases, rooms etc.
+      sounds = Audio\gf_sounds.ini			;sound-effects for gameflow - bases, rooms etc.
@@ -98 +98 @@
-	voices = audio\voices_space_male.ini		;dialogue for male NPCs in space (all re-usable)
+	voices = Audio\voices_space_male.ini		;dialogue for male NPCs in space (all re-usable)
@@ -99 +99 @@
-	voices = audio\voices_space_female.ini		;dialogue for female NPCs in space (all re-usable)
+	voices = Audio\voices_space_female.ini		;dialogue for female NPCs in space (all re-usable)
@@ -100 +100 @@
-	voices = audio\voices_base_male.ini		;dialogue for male NPCs on bases (all re-usable)
+	voices = Audio\voices_base_male.ini		;dialogue for male NPCs on bases (all re-usable)
@@ -101 +101 @@
-	voices = audio\voices_base_female.ini		;dialogue for female NPCs on bases (all re-usable)
+	voices = Audio\voices_base_female.ini		;dialogue for female NPCs on bases (all re-usable)
@@ -102 +102 @@
-      voices = audio\voices_recognizable.ini		;all the main characters’ voice profiles (re-usable dialogue only) (must be read in before mission-specific lines)
+      voices = Audio\voices_recognizable.ini		;all the main characters’ voice profiles (re-usable dialogue only) (must be read in before mission-specific lines)
@@ -103 +103 @@
-      voices = audio\voices_mission01.ini		;dialogue specific to mission 01 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission01.ini		;dialogue specific to mission 01 (story & special supporting characters only - no reusable dialogue)
@@ -104 +104 @@
-      voices = audio\voices_mission02.ini		;dialogue specific to mission 02 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission02.ini		;dialogue specific to mission 02 (story & special supporting characters only - no reusable dialogue)
@@ -105 +105 @@
-      voices = audio\voices_mission03.ini		;dialogue specific to mission 03 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission03.ini		;dialogue specific to mission 03 (story & special supporting characters only - no reusable dialogue)
@@ -106 +106 @@
-      voices = audio\voices_mission04.ini		;dialogue specific to mission 04 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission04.ini		;dialogue specific to mission 04 (story & special supporting characters only - no reusable dialogue)
@@ -107 +107 @@
-      voices = audio\voices_mission05.ini		;dialogue specific to mission 05 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission05.ini		;dialogue specific to mission 05 (story & special supporting characters only - no reusable dialogue)
@@ -108 +108 @@
-      voices = audio\voices_mission06.ini		;dialogue specific to mission 06 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission06.ini		;dialogue specific to mission 06 (story & special supporting characters only - no reusable dialogue)
@@ -109 +109 @@
-      voices = audio\voices_mission07.ini		;dialogue specific to mission 07 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission07.ini		;dialogue specific to mission 07 (story & special supporting characters only - no reusable dialogue)
@@ -110 +110 @@
-      voices = audio\voices_mission08.ini		;dialogue specific to mission 08 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission08.ini		;dialogue specific to mission 08 (story & special supporting characters only - no reusable dialogue)
@@ -111 +111 @@
-      voices = audio\voices_mission09.ini		;dialogue specific to mission 09 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission09.ini		;dialogue specific to mission 09 (story & special supporting characters only - no reusable dialogue)
@@ -112 +112 @@
-      voices = audio\voices_mission10.ini		;dialogue specific to mission 10 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission10.ini		;dialogue specific to mission 10 (story & special supporting characters only - no reusable dialogue)
@@ -113 +113 @@
-      voices = audio\voices_mission11.ini		;dialogue specific to mission 11 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission11.ini		;dialogue specific to mission 11 (story & special supporting characters only - no reusable dialogue)
@@ -114 +114 @@
-      voices = audio\voices_mission12.ini		;dialogue specific to mission 12 (story & special supporting characters only - no reusable dialogue)
+      voices = Audio\voices_mission12.ini		;dialogue specific to mission 12 (story & special supporting characters only - no reusable dialogue)
@@ -115 +115 @@
-      voices = audio\voices_mission13.ini		;dialogue specific to mission 13 (story & special supporting characters only - no reusable dialogue)	
+      voices = Audio\voices_mission13.ini		;dialogue specific to mission 13 (story & special supporting characters only - no reusable dialogue)	
@@ -118 +118 @@
-  explosions = fx\explosions.ini
+  explosions = FX\explosions.ini
@@ -119 +119 @@
-      debris = fx\explosions.ini
+      debris = FX\explosions.ini
@@ -120 +120 @@
-   asteroids = solar\asteroidarch.ini
+   asteroids = Solar\asteroidarch.ini
@@ -122 +122 @@
-   equipment = equipment\light_equip.ini
+   equipment = Equipment\light_equip.ini
@@ -123 +123 @@
-   equipment = equipment\select_equip.ini
+   equipment = Equipment\select_equip.ini
@@ -124 +124 @@
-   equipment = equipment\misc_equip.ini
+   equipment = Equipment\misc_equip.ini
@@ -125 +125 @@
-   equipment = equipment\engine_equip.ini
+   equipment = Equipment\engine_equip.ini
@@ -126 +126 @@
-   equipment = equipment\ST_equip.ini
+   equipment = Equipment\st_equip.ini
@@ -127 +127 @@
-   equipment = equipment\weapon_equip.ini
+   equipment = Equipment\weapon_equip.ini
@@ -132 +132 @@
-   equipment = equipment\prop_equip.ini		
+   equipment = Equipment\prop_equip.ini		
@@ -137 +137 @@
-       ships = ships\shiparch.ini
+       ships = Ships\shiparch.ini
@@ -138 +138 @@
-       ships = ships\rtc_shiparch.ini
+       ships = Ships\rtc_shiparch.ini
@@ -140 +140 @@
-       goods = equipment\goods.ini
+       goods = Equipment\Goods.ini
@@ -141 +141 @@
-       goods = equipment\engine_good.ini
+       goods = Equipment\engine_good.ini
@@ -142 +142 @@
-       goods = equipment\misc_good.ini
+       goods = Equipment\misc_good.ini
@@ -143 +143 @@
-       goods = equipment\st_good.ini
+       goods = Equipment\ST_good.ini
@@ -144 +144 @@
-       goods = equipment\weapon_good.ini
+       goods = Equipment\weapon_good.ini
@@ -148 +148 @@
-    loadouts = ships\loadouts.ini
+    loadouts = Ships\loadouts.ini
@@ -149 +149 @@
-    loadouts = ships\loadouts_special.ini
+    loadouts = Ships\loadouts_special.ini
@@ -150 +150 @@
-    loadouts = ships\loadouts_utility.ini
+    loadouts = Ships\loadouts_utility.ini
@@ -151 +151 @@
-    loadouts = solar\loadouts.ini 
+    loadouts = Solar\loadouts.ini 
@@ -152 +152 @@
-   bodyparts = characters\bodyparts.ini
+   bodyparts = Characters\bodyparts.ini
@@ -153 +153 @@
-    costumes = characters\costumes.ini
+    costumes = Characters\costumes.ini
@@ -155 +155 @@
-     effects = fx\effect_types.ini			; needs to be before effects.ini
+     effects = FX\effect_types.ini			; needs to be before effects.ini
@@ -156 +156 @@
-     effects = fx\beam_effects.ini			; also needs to be before effects.ini
+     effects = FX\beam_effects.ini			; also needs to be before effects.ini
@@ -157 +157 @@
-     effects = fx\engines\engines_ale.ini
+     effects = FX\engines\engines_ale.ini
@@ -158 +158 @@
-     effects = fx\equipment\equipment_ale.ini
+     effects = FX\equipment\equipment_ale.ini
@@ -159 +159 @@
-     effects = fx\explosions\explosions_ale.ini
+     effects = FX\explosions\explosions_ale.ini
@@ -160 +160 @@
-     effects = fx\hull_hits\hull_hits_ale.ini
+     effects = FX\hull_hits\hull_hits_ale.ini
@@ -161 +161 @@
-     effects = fx\misc\misc_ale.ini
+     effects = FX\misc\misc_ale.ini
@@ -162 +162 @@
-     effects = fx\shields\shields_ale.ini
+     effects = FX\shields\shields_ale.ini
@@ -163 +163 @@
-     effects = fx\space\space_ale.ini
+     effects = FX\space\space_ale.ini
@@ -164 +164 @@
-     effects = fx\weapons\weapons_ale.ini
+     effects = FX\weapons\weapons_ale.ini
@@ -165 +165 @@
-     effects = fx\effects.ini
+     effects = FX\effects.ini
@@ -166 +166 @@
-     effects = fx\effects_explosion.ini
+     effects = FX\effects_explosion.ini
@@ -167 +167 @@
-effect_shapes = fx\effect_shapes.ini
+effect_shapes = FX\effect_shapes.ini
@@ -168 +168 @@
-       fuses = fx\fuse.ini
+       fuses = FX\fuse.ini
@@ -169 +169 @@
-       fuses = fx\fuse_br_battleship.ini
+       fuses = FX\fuse_br_battleship.ini
@@ -170 +170 @@
-       fuses = fx\fuse_br_destroyer.ini
+       fuses = FX\fuse_br_destroyer.ini
@@ -171 +171 @@
-       fuses = fx\fuse_br_gunship.ini
+       fuses = FX\fuse_br_gunship.ini
@@ -172 +172 @@
-       fuses = fx\fuse_ku_battleship.ini
+       fuses = FX\fuse_ku_battleship.ini
@@ -173 +173 @@
-       fuses = fx\fuse_ku_destroyer.ini
+       fuses = FX\fuse_ku_destroyer.ini
@@ -174 +174 @@
-       fuses = fx\fuse_ku_gunship.ini
+       fuses = FX\fuse_ku_gunship.ini
@@ -175 +175 @@
-       fuses = fx\fuse_li_cruiser.ini
+       fuses = FX\fuse_li_cruiser.ini
@@ -176 +176 @@
-       fuses = fx\fuse_li_dreadnought.ini
+       fuses = FX\fuse_li_dreadnought.ini
@@ -177 +177 @@
-       fuses = fx\fuse_rh_battleship.ini
+       fuses = FX\fuse_rh_battleship.ini
@@ -178 +178 @@
-       fuses = fx\fuse_rh_cruiser.ini
+       fuses = FX\fuse_rh_cruiser.ini
@@ -179 +179 @@
-       fuses = fx\fuse_rh_gunship.ini
+       fuses = FX\fuse_rh_gunship.ini
@@ -180 +180 @@
-       fuses = fx\fuse_or_osiris.ini
+       fuses = FX\fuse_or_osiris.ini
@@ -181 +181 @@
-       fuses = fx\fuse_transport.ini
+       fuses = FX\fuse_transport.ini
@@ -182 +182 @@
-       fuses = fx\fuse_suprise_solar.ini
+       fuses = FX\fuse_suprise_solar.ini
@@ -183 +183 @@
-       fuses = fx\fuse_freeport7.ini
+       fuses = FX\fuse_freeport7.ini
@@ -185 +185 @@
-       intro = interface\intro.ini
+       intro = Interface\intro.ini
@@ -186 +186 @@
-gate_tunnels = fx\gate_tunnel.ini
+gate_tunnels = FX\gate_tunnel.ini
@@ -187 +187 @@
-      groups = InitialWorld.ini
+      groups = initialworld.ini
@@ -188 +188 @@
-         HUD = interface\hud.ini
+         HUD = Interface\hud.ini
@@ -189 +189 @@
- jump_effect = fx\jumpeffect.ini
+ jump_effect = FX\jumpeffect.ini
@@ -190 +190 @@
-       stars = solar\StarArch.ini
+       stars = Solar\StarArch.ini
@@ -194 +194 @@
-     markets = equipment\market_misc.ini
+     markets = Equipment\market_misc.ini
@@ -195 +195 @@
-     markets = equipment\market_ships.ini
+     markets = Equipment\market_ships.ini
@@ -196 +196 @@
-     markets = equipment\market_commodities.ini
+     markets = Equipment\market_commodities.ini
@@ -197 +197 @@
-   NewCharDB = characters\NewCharacter.ini
+   NewCharDB = Characters\NewCharacter.ini
@@ -198 +198 @@
-   WeaponModDB = equipment\WeaponModDB.ini
+   WeaponModDB = Equipment\WeaponModDB.ini
@@ -199 +199 @@
-   rtcslider = scripts\rtcslider.ini
+   rtcslider = Scripts\rtcslider.ini
```

</details>

### Diffs 1.3 → 1.3.1

#### `initialworld.ini`

53 Hunks, +53 / −53 Zeilen · Thu Oct 30 00:00:00 2003 → Sun Oct 11 00:00:00 2026

_Die `-`-Zeilen enthalten geschützte Leerzeichen (U+00A0), die `+`-Zeilen normale Leerzeichen; sie sehen daher gleich aus._

<details><summary>Diff anzeigen (159 Zeilen)</summary>

```diff
@@ -4 +4 @@
-locked_gate = 2926089285         ;St01_to_St02_hole   ;St01_to_St02_hole
+locked_gate = 2926089285         ;St01_to_St02_hole   ;St01_to_St02_hole
@@ -5 +5 @@
-locked_gate = 2926433351         ;St01_to_St03_hole   ;St01_to_St03_hole
+locked_gate = 2926433351         ;St01_to_St03_hole   ;St01_to_St03_hole
@@ -6 +6 @@
-locked_gate = 2460445762         ;St02_to_St01_hole   ;St02_to_St01_hole
+locked_gate = 2460445762         ;St02_to_St01_hole   ;St02_to_St01_hole
@@ -7 +7 @@
-locked_gate = 2263303234         ;St03_to_St01_hole   ;St03_to_St01_hole
+locked_gate = 2263303234         ;St03_to_St01_hole   ;St03_to_St01_hole
@@ -8 +8 @@
-locked_gate = 2284213505         ;Li05_to_Li01   ;Li05_to_Li01
+locked_gate = 2284213505         ;Li05_to_Li01   ;Li05_to_Li01
@@ -9 +9 @@
-locked_gate = 2293678337         ;Li01_to_Li05   ;Li01_to_Li05
+locked_gate = 2293678337         ;Li01_to_Li05   ;Li01_to_Li05
@@ -10 +10 @@
-locked_gate = 2711806985         ;Ku06_to_Ku07_hole   ;Ku06_to_Ku07_hole
+locked_gate = 2711806985         ;Ku06_to_Ku07_hole   ;Ku06_to_Ku07_hole
@@ -11 +11 @@
-locked_gate = 3051899916         ;Ku07_to_Ku05_hole   ;Ku07_to_Ku05_hole
+locked_gate = 3051899916         ;Ku07_to_Ku05_hole   ;Ku07_to_Ku05_hole
@@ -12 +12 @@
-locked_gate = 2640501769         ;Ku05_to_Ku07_hole   ;Ku05_to_Ku07_hole
+locked_gate = 2640501769         ;Ku05_to_Ku07_hole   ;Ku05_to_Ku07_hole
@@ -14 +14 @@
-locked_gate = 2541540999         ;Iw03_to_Li01   ;Iw03_to_Li01
+locked_gate = 2541540999         ;Iw03_to_Li01   ;Iw03_to_Li01
@@ -15 +15 @@
-locked_gate = 2963174661         ;Li01_to_Iw03   ;Li01_to_Iw03
+locked_gate = 2963174661         ;Li01_to_Iw03   ;Li01_to_Iw03
@@ -19 +19 @@
-locked_gate = 2350144385         ;Bw01_to_br03_hole   ;Bw01_to_br03_hole
+locked_gate = 2350144385         ;Bw01_to_br03_hole   ;Bw01_to_br03_hole
@@ -20 +20 @@
-locked_gate = 2384076422         ;Br03_to_br04_hole   ;Br03_to_br04_hole
+locked_gate = 2384076422         ;Br03_to_br04_hole   ;Br03_to_br04_hole
@@ -21 +21 @@
-locked_gate = 2919942795         ;Br03_to_bw01_hole   ;Br03_to_bw01_hole
+locked_gate = 2919942795         ;Br03_to_bw01_hole   ;Br03_to_bw01_hole
@@ -22 +22 @@
-locked_gate = 2747303563         ;Br04_to_br03_hole   ;Br04_to_br03_hole
+locked_gate = 2747303563         ;Br04_to_br03_hole   ;Br04_to_br03_hole
@@ -24 +24 @@
-locked_gate = 2749302404         ;Br04_to_br05_hole   ;Br04_to_br05_hole
+locked_gate = 2749302404         ;Br04_to_br05_hole   ;Br04_to_br05_hole
@@ -25 +25 @@
-locked_gate = 3080351366         ;Br05_to_br04_hole   ;Br05_to_br04_hole
+locked_gate = 3080351366         ;Br05_to_br04_hole   ;Br05_to_br04_hole
@@ -29 +29 @@
-locked_gate = 3157307012         ;Bw05_to_Ku06_hole   ;Bw05_to_Ku06_hole
+locked_gate = 3157307012         ;Bw05_to_Ku06_hole   ;Bw05_to_Ku06_hole
@@ -30 +30 @@
-locked_gate = 2675819466         ;Bw05_to_rh01_hole   ;Bw05_to_rh01_hole
+locked_gate = 2675819466         ;Bw05_to_rh01_hole   ;Bw05_to_rh01_hole
@@ -31 +31 @@
-locked_gate = 2694587652         ;Ku06_to_bw05_hole   ;Ku06_to_bw05_hole
+locked_gate = 2694587652         ;Ku06_to_bw05_hole   ;Ku06_to_bw05_hole
@@ -32 +32 @@
-locked_gate = 3015759243         ;Rh01_to_Bw05_hole   ;Rh01_to_Bw05_hole
+locked_gate = 3015759243         ;Rh01_to_Bw05_hole   ;Rh01_to_Bw05_hole
@@ -33 +33 @@
-locked_gate = 2254122510         ;Rh02_to_Rh04_holeb   ;Rh02_to_Rh04_holeb
+locked_gate = 2254122510         ;Rh02_to_Rh04_holeb   ;Rh02_to_Rh04_holeb
@@ -34 +34 @@
-locked_gate = 2578962883         ;Rh04_to_Rh02_holeb   ;Rh04_to_Rh02_holeb
+locked_gate = 2578962883         ;Rh04_to_Rh02_holeb   ;Rh04_to_Rh02_holeb
@@ -36 +36 @@
-locked_gate = 2444625543         ;Li01a_to_Li01b_hole   ;Li01a_to_Li01b_hole
+locked_gate = 2444625543         ;Li01a_to_Li01b_hole   ;Li01a_to_Li01b_hole
@@ -37 +37 @@
-locked_gate = 2980035276         ;Li01b_to_Li01a_hole   ;Li01b_to_Li01a_hole
+locked_gate = 2980035276         ;Li01b_to_Li01a_hole   ;Li01b_to_Li01a_hole
@@ -38 +38 @@
-npc_locked_gate = 3080351366  ;Br05_to_br04_hole
+npc_locked_gate = 3080351366  ;Br05_to_br04_hole
@@ -39 +39 @@
-npc_locked_gate = 2749302404  ;Br04_to_br05_hole
+npc_locked_gate = 2749302404  ;Br04_to_br05_hole
@@ -40 +40 @@
-npc_locked_gate = 2384076422  ;Br03_to_br04_hole
+npc_locked_gate = 2384076422  ;Br03_to_br04_hole
@@ -41 +41 @@
-npc_locked_gate = 2747303563  ;Br04_to_br03_hole
+npc_locked_gate = 2747303563  ;Br04_to_br03_hole
@@ -42 +42 @@
-npc_locked_gate = 2350144385  ;Bw01_to_br03_hole
+npc_locked_gate = 2350144385  ;Bw01_to_br03_hole
@@ -43 +43 @@
-npc_locked_gate = 2919942795  ;Br03_to_bw01_hole
+npc_locked_gate = 2919942795  ;Br03_to_bw01_hole
@@ -44 +44 @@
-npc_locked_gate = 2694587652  ;Ku06_to_bw05_hole
+npc_locked_gate = 2694587652  ;Ku06_to_bw05_hole
@@ -45 +45 @@
-npc_locked_gate = 3157307012  ;Bw05_to_Ku06_hole
+npc_locked_gate = 3157307012  ;Bw05_to_Ku06_hole
@@ -46 +46 @@
-npc_locked_gate = 2675819466  ;Bw05_to_rh01_hole
+npc_locked_gate = 2675819466  ;Bw05_to_rh01_hole
@@ -47 +47 @@
-npc_locked_gate = 3015759243  ;Rh01_to_Bw05_hole
+npc_locked_gate = 3015759243  ;Rh01_to_Bw05_hole
@@ -48 +48 @@
-npc_locked_gate = 2578962883  ;Rh04_to_Rh02_holeb
+npc_locked_gate = 2578962883  ;Rh04_to_Rh02_holeb
@@ -49 +49 @@
-npc_locked_gate = 2254122510  ;Rh02_to_Rh04_holeb
+npc_locked_gate = 2254122510  ;Rh02_to_Rh04_holeb
@@ -50 +50 @@
-npc_locked_gate = 2293678337  ;Li01_to_Li05
+npc_locked_gate = 2293678337  ;Li01_to_Li05
@@ -51 +51 @@
-npc_locked_gate = 2284213505  ;Li05_to_Li01
+npc_locked_gate = 2284213505  ;Li05_to_Li01
@@ -52 +52 @@
-npc_locked_gate = 2444625543  ;Li01a_to_Li01b_hole
+npc_locked_gate = 2444625543  ;Li01a_to_Li01b_hole
@@ -53 +53 @@
-npc_locked_gate = 2980035276  ;Li01b_to_Li01a_hole
+npc_locked_gate = 2980035276  ;Li01b_to_Li01a_hole
@@ -54 +54 @@
-npc_locked_gate = 2640501769  ;Ku05_to_Ku07_hole
+npc_locked_gate = 2640501769  ;Ku05_to_Ku07_hole
@@ -55 +55 @@
-npc_locked_gate = 3051899916  ;Ku07_to_Ku05_hole
+npc_locked_gate = 3051899916  ;Ku07_to_Ku05_hole
@@ -56 +56 @@
-npc_locked_gate = 2711806985  ;Ku06_to_Ku07_hole
+npc_locked_gate = 2711806985  ;Ku06_to_Ku07_hole
@@ -57 +57 @@
-npc_locked_gate = 3051850763  ;Ku07_to_Ku06_hole
+npc_locked_gate = 3051850763  ;Ku07_to_Ku06_hole
@@ -58 +58 @@
-npc_locked_gate = 2926089285  ;St01_to_St02_hole
+npc_locked_gate = 2926089285  ;St01_to_St02_hole
@@ -59 +59 @@
-npc_locked_gate = 2460445762  ;St02_to_St01_hole
+npc_locked_gate = 2460445762  ;St02_to_St01_hole
@@ -60 +60 @@
-npc_locked_gate = 2926433351  ;St01_to_St03_hole
+npc_locked_gate = 2926433351  ;St01_to_St03_hole
@@ -61 +61 @@
-npc_locked_gate = 2263303234  ;St03_to_St01_hole
+npc_locked_gate = 2263303234  ;St03_to_St01_hole
@@ -62 +62 @@
-npc_locked_gate = 2382233355  ; ???
+npc_locked_gate = 2382233355  ; ???
@@ -63 +63 @@
-npc_locked_gate = 2569281742  ; ???
+npc_locked_gate = 2569281742  ; ???
@@ -64 +64 @@
-npc_locked_gate = 2963174661  ;Li01_to_Iw03
+npc_locked_gate = 2963174661  ;Li01_to_Iw03
@@ -65 +65 @@
-npc_locked_gate = 2541540999  ;Iw03_to_Li01
+npc_locked_gate = 2541540999  ;Iw03_to_Li01
```

</details>

#### `Universe/Systems/Li02/Bases/Rooms/Li02_01_cityscape.ini`

1 Hunk, +1 / −1 Zeilen · Thu Oct 30 00:00:00 2003 → Sun Oct 11 14:05:08 2026

```diff
@@ -81 +81 @@
-:gap = 0.200000
+gap = 0.200000
}
 
```

### Diffs 1.0 → 1.3.1 (kosmetisch)

#### `Equipment/select_equip.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Mon Sep 01 00:00:00 2003

```diff
@@ -11 +11 @@
-hit_pts_scale = 1000000015047466219876688855040.000000
+hit_pts_scale = 1000000015047466200000000000000.000000
```

#### `Interface/Baseside/navbar.ini`

25 Hunks, +26 / −26 Zeilen · Mon Sep 01 00:00:00 2003 → Mon Sep 01 00:00:00 2003

<details><summary>Diff anzeigen (77 Zeilen)</summary>

```diff
@@ -2,2 +2,2 @@
-behavior = 
-mesh = 
+behavior
+mesh
@@ -55 +55 @@
-hardpoint = 
+hardpoint
@@ -61 +61 @@
-event = 
+event
@@ -68 +68 @@
-hardpoint = 
+hardpoint
@@ -74 +74 @@
-event = 
+event
@@ -81 +81 @@
-hardpoint = 
+hardpoint
@@ -87 +87 @@
-event = 
+event
@@ -94 +94 @@
-hardpoint = 
+hardpoint
@@ -100 +100 @@
-event = 
+event
@@ -107 +107 @@
-hardpoint = 
+hardpoint
@@ -113 +113 @@
-event = 
+event
@@ -120 +120 @@
-hardpoint = 
+hardpoint
@@ -126 +126 @@
-event = 
+event
@@ -133 +133 @@
-hardpoint = 
+hardpoint
@@ -139 +139 @@
-event = 
+event
@@ -146 +146 @@
-hardpoint = 
+hardpoint
@@ -152 +152 @@
-event = 
+event
@@ -159 +159 @@
-hardpoint = 
+hardpoint
@@ -165 +165 @@
-event = 
+event
@@ -172 +172 @@
-hardpoint = 
+hardpoint
@@ -178 +178 @@
-event = 
+event
@@ -185 +185 @@
-hardpoint = 
+hardpoint
@@ -191 +191 @@
-event = 
+event
@@ -198 +198 @@
-hardpoint = 
+hardpoint
@@ -204 +204 @@
-event = 
+event
```

</details>

#### `Solar/asteroids/Br02_Birmingham_ice_asteroid_field.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Mon Sep 01 00:00:00 2003

```diff
@@ -28 +28 @@
-asteroid = ice_carbon_asteroid60, -0.000000, -0.100000, 0.200000, 105, 160, 25
+asteroid = ice_carbon_asteroid60, 0.000000, -0.100000, 0.200000, 105, 160, 25
```

#### `Universe/Systems/Intro/Intro.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Mon Sep 01 00:00:00 2003

```diff
@@ -1421 +1421 @@
-difficulty = 
+difficulty
```

---

## 1.3 (gegenüber 1.0)

Offizieller Patch: 129 Dateien, 1323 neue und 1411 entfernte Zeilen.

### Überblick nach Bereich

| Bereich | Dateien | + | − |
|---|---:|---:|---:|
| [Missions](#missions) | 78 | 749 | 756 |
| [Universe](#universe) | 33 | 57 | 67 |
| [FX](#fx) | 8 | 6 | 9 |
| [Ships](#ships) | 3 | 245 | 293 |
| [Equipment](#equipment) | 2 | 55 | 59 |
| [Solar](#solar) | 2 | 210 | 224 |
| [(Wurzelverzeichnis)](#wurzelverzeichnis) | 1 | 1 | 1 |
| [Audio](#audio) | 1 | 0 | 1 |
| [Characters](#characters) | 1 | 0 | 1 |

### Fehlerklassen

| Fehlerklasse in 1.0 | Korrektur in 1.3 |
|---|---|
| Schlüssel ohne Wert (`autoplay`, `separable`, `offers_missions`, `audio`, `autoselect`) | `= true` ergänzt |
| Doppelte Backslashes in Pfaden (`Act_AddRTC`, `Act_CallThorn`, `Act_RemoveRTC`, …) | einfache `\` |
| `MarketGood = x, , 0` (leeres Feld) | `0` eingesetzt |
| `zone_creation_distance = false` | `0` |
| Tippfehler in Schlüsseln (`info_ids`, `pacedust`, `spacedust_maxdust`, `spacedust_masparticles`, `system St02 =`) | `ids_info`, `spacedust`, `spacedust_maxparticles`, `system = St02` |
| Fehlende Werte (`BreakFormation`, `system`, `[start_effect]`, `name`) | ergänzt |
| Überzählige Zeilen (`cargo`, `equip`, `ids_info`, `force_gun_ori`, `loadout`, `head`) | entfernt |

### Hinweise

- Nur in 1.3 vorhanden: `sdk1.3.zip` (kein INI, nicht Teil des SDK-Ordners)
- Nur in 1.0 vorhanden: `Ships/loadouts_special.zip` (kein INI, nicht Teil des SDK-Ordners)

### Missions

#### `Missions/M01a/M000_s002xe_Li01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M01a/M001a_s003x_Li01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M01a/M001a_s005a_Li01_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -7 +7 @@
-autoplay
+autoplay = true
```

#### `Missions/M01a/M001a_s005d_Li01_01_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -9 +9 @@
-autoplay
+autoplay = true
```

#### `Missions/M01a/M001a_s006x_Li01_02_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M01a/m01a.ini`

19 Hunks, +27 / −27 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (73 Zeilen)</summary>

```diff
@@ -465 +465 @@
-Act_CallThorn = missions\\m01a\\m01a_fp7_01.thn, fp7base
+Act_CallThorn = missions\m01a\m01a_fp7_01.thn, fp7base
@@ -588 +588 @@
-Act_CallThorn = missions\\m01a\\m01a_fp7_02.thn, fp7base
+Act_CallThorn = missions\m01a\m01a_fp7_02.thn, fp7base
@@ -656 +656 @@
-Act_CallThorn = missions\\m01a\\m01a_fp7_02b.thn, fp7base
+Act_CallThorn = missions\m01a\m01a_fp7_02b.thn, fp7base
@@ -684 +684 @@
-Act_CallThorn = missions\\m01a\\m01a_fp7_03.thn
+Act_CallThorn = missions\m01a\m01a_fp7_03.thn
@@ -770 +770 @@
-Act_AddAmbient = Scripts\\Bases\\Li_01_Cityscape_gamestart_01.thn, Cityscape, Li01_01_Base
+Act_AddAmbient = Scripts\Bases\Li_01_Cityscape_gamestart_01.thn, Cityscape, Li01_01_Base
@@ -776 +776 @@
-Act_AddRTC = missions\\m01a\\M000_s002xe_Li01_01_nrml.ini
+Act_AddRTC = missions\m01a\M000_s002xe_Li01_01_nrml.ini
@@ -783 +783 @@
-Cnd_RTCDone = missions\\m01a\\M000_s002xe_Li01_01_nrml.ini
+Cnd_RTCDone = missions\m01a\M000_s002xe_Li01_01_nrml.ini
@@ -796,2 +796,2 @@
-Act_AddRTC = missions\\m01a\\M001a_s003x_Li01_01_nrml.ini
-Act_AddRTC = missions\\m01a\\M001a_s004x_Li01_01_nrml.ini
+Act_AddRTC = missions\m01a\M001a_s003x_Li01_01_nrml.ini
+Act_AddRTC = missions\m01a\M001a_s004x_Li01_01_nrml.ini
@@ -803 +803 @@
-Cnd_RTCDone = missions\\m01a\\M001a_s003x_Li01_01_nrml.ini
+Cnd_RTCDone = missions\m01a\M001a_s003x_Li01_01_nrml.ini
@@ -817,3 +817,3 @@
-Act_AddRTC = missions\\m01a\\M001a_s005a_Li01_01_offer.ini, repeatable
-Act_AddAmbient = scripts\\Bases\\Li_01_Equipment_ambi_s005_music.thn, Equipment, Li01_01_Base
-Act_AddAmbient = scripts\\story\\Li_01_Equipment_ambi_s005_ship_01.thn, Equipment, Li01_01_Base
+Act_AddRTC = missions\m01a\M001a_s005a_Li01_01_offer.ini, repeatable
+Act_AddAmbient = scripts\Bases\Li_01_Equipment_ambi_s005_music.thn, Equipment, Li01_01_Base
+Act_AddAmbient = scripts\story\Li_01_Equipment_ambi_s005_ship_01.thn, Equipment, Li01_01_Base
@@ -828,2 +828,2 @@
-Act_RemoveRTC = missions\\m01a\\M001a_s005a_Li01_01_offer.ini
-Act_AddRTC = missions\\m01a\\M001a_s005d_Li01_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m01a\M001a_s005a_Li01_01_offer.ini
+Act_AddRTC = missions\m01a\M001a_s005d_Li01_01_reoffer.ini, repeatable
@@ -841,5 +841,5 @@
-Act_RemoveRTC = missions\\m01a\\M001a_s005a_Li01_01_offer.ini
-Act_RemoveRTC = missions\\m01a\\M001a_s005d_Li01_01_reoffer.ini
-Act_RemoveAmbient = scripts\\story\\Li_01_Equipment_ambi_s005_ship_01.thn
-Act_RemoveAmbient = Scripts\\Bases\\Li_01_Cityscape_gamestart_01.thn
-Act_RemoveAmbient = scripts\\Bases\\Li_01_Equipment_ambi_s005_music.thn
+Act_RemoveRTC = missions\m01a\M001a_s005a_Li01_01_offer.ini
+Act_RemoveRTC = missions\m01a\M001a_s005d_Li01_01_reoffer.ini
+Act_RemoveAmbient = scripts\story\Li_01_Equipment_ambi_s005_ship_01.thn
+Act_RemoveAmbient = Scripts\Bases\Li_01_Cityscape_gamestart_01.thn
+Act_RemoveAmbient = scripts\Bases\Li_01_Equipment_ambi_s005_music.thn
@@ -905 +905 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_01.thn, fauxP1
+Act_CallThorn = missions\m01a\m01a_rev2_01.thn, fauxP1
@@ -1125 +1125 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_02.thn, r_cruiser_two
+Act_CallThorn = missions\m01a\m01a_rev2_02.thn, r_cruiser_two
@@ -1168 +1168 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_03.thn, r_cruiser
+Act_CallThorn = missions\m01a\m01a_rev2_03.thn, r_cruiser
@@ -1234 +1234 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_04.thn, o_hostile1_two
+Act_CallThorn = missions\m01a\m01a_rev2_04.thn, o_hostile1_two
@@ -1255 +1255 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_05.thn, r_cruiser
+Act_CallThorn = missions\m01a\m01a_rev2_05.thn, r_cruiser
@@ -1408 +1408 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_06.thn, o_hostile1
+Act_CallThorn = missions\m01a\m01a_rev2_06.thn, o_hostile1
@@ -1530 +1530 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_08.thn, r_cruiser
+Act_CallThorn = missions\m01a\m01a_rev2_08.thn, r_cruiser
```

</details>

#### `Missions/M01b/M01b.ini`

3 Hunks, +3 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -996 +996 @@
-Act_CallThorn = missions\\m01b\\M01_space_enter.thn
+Act_CallThorn = missions\m01b\M01_space_enter.thn
@@ -1011 +1011 @@
-Act_CallThorn = missions\\m01b\\m01b_king_01.thn
+Act_CallThorn = missions\m01b\m01b_king_01.thn
@@ -2442 +2442 @@
-Act_CallThorn = missions\\m01b\\m01b_11.thn, Player
+Act_CallThorn = missions\m01b\m01b_11.thn, Player
```

#### `Missions/M02/M002_s010x_Li01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M02/M002_s011x_Li01_03_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M02/m02.ini`

13 Hunks, +14 / −15 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (42 Zeilen)</summary>

```diff
@@ -599 +599 @@
-Act_AddRTC = missions\\m02\\M002_s009a_Li01_01_offer.ini
+Act_AddRTC = missions\m02\M002_s009a_Li01_01_offer.ini
@@ -610,2 +610,2 @@
-Act_RemoveRTC = missions\\m02\\M002_s009a_Li01_01_offer.ini
-Act_AddRTC = missions\\m02\\M002_s009d_Li01_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m02\M002_s009a_Li01_01_offer.ini
+Act_AddRTC = missions\m02\M002_s009d_Li01_01_reoffer.ini, repeatable
@@ -621,2 +621,2 @@
-Act_RemoveRTC = missions\\m02\\M002_s009d_Li01_01_reoffer.ini
-Act_AddRTC = missions\\m02\\M002_s010x_Li01_01_nrml.ini
+Act_RemoveRTC = missions\m02\M002_s009d_Li01_01_reoffer.ini
+Act_AddRTC = missions\m02\M002_s010x_Li01_01_nrml.ini
@@ -685 +685 @@
-Act_CallThorn = missions\\m02\\m02_space_enter.thn, Player
+Act_CallThorn = missions\m02\m02_space_enter.thn, Player
@@ -708 +708 @@
-Act_CallThorn = missions\\m02\\m02_king_01.thn, Player
+Act_CallThorn = missions\m02\m02_king_01.thn, Player
@@ -793 +793 @@
-BreakFormation
+BreakFormation = no_params
@@ -1052 +1052 @@
-BreakFormation
+BreakFormation = no_params
@@ -1156 +1155,0 @@
-Act_RandomPop = false
@@ -1242 +1241 @@
-Act_CallThorn = missions\\m02\\m02_cosmo_01.thn, PEscort1
+Act_CallThorn = missions\m02\m02_cosmo_01.thn, PEscort1
@@ -1743 +1742 @@
-BreakFormation
+BreakFormation = no_params
@@ -1748 +1747 @@
-BreakFormation
+BreakFormation = no_params
@@ -2187 +2186 @@
-BreakFormation
+BreakFormation = no_params
@@ -2421 +2420 @@
-Act_AddRTC = missions\\m02\\M002_s011x_Li01_03_nrml.ini
+Act_AddRTC = missions\m02\M002_s011x_Li01_03_nrml.ini
```

</details>

#### `Missions/M03/M003_s012xa_Li01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M03/M003_s012xb_Li01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M03/M003_s014a_Li02_02_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -9 +9 @@
-autoplay
+autoplay = true
```

#### `Missions/M03/M003_s015x_Li02_02_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M03/m03.ini`

13 Hunks, +14 / −14 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (41 Zeilen)</summary>

```diff
@@ -1007 +1007 @@
-Act_AddRTC = //missions//m03//M003_s012xa_Li01_01_nrml.ini
+Act_AddRTC = missions\m03\M003_s012xa_Li01_01_nrml.ini
@@ -1015 +1015 @@
-Act_AddRTC = //missions//m03//M003_s012xb_Li01_01_nrml.ini
+Act_AddRTC = missions\m03\M003_s012xb_Li01_01_nrml.ini
@@ -1131 +1131 @@
-Act_CallThorn = missions\\m03\\m03_Survivor1.thn, Player
+Act_CallThorn = missions\m03\m03_Survivor1.thn, Player
@@ -1156 +1156 @@
-Act_CallThorn = missions\\m03\\m03_Survivor1.thn, Player
+Act_CallThorn = missions\m03\m03_Survivor1.thn, Player
@@ -1281 +1281 @@
-Act_CallThorn = missions\\m03\\m03_Survivor2.thn, navy_patrol1
+Act_CallThorn = missions\m03\m03_Survivor2.thn, navy_patrol1
@@ -1324 +1324 @@
-Act_CallThorn = missions\\m03\\m03_Survivor3.thn, navy_patrol1
+Act_CallThorn = missions\m03\m03_Survivor3.thn, navy_patrol1
@@ -1374 +1374 @@
-Act_AddRTC = missions\\m03\\M003_s014a_Li02_02_offer.ini
+Act_AddRTC = missions\m03\M003_s014a_Li02_02_offer.ini
@@ -1380,2 +1380,2 @@
-Act_RemoveRTC = missions\\m03\\M003_s014a_Li02_02_offer.ini
-Act_AddRTC = missions\\m03\\M003_s014d_Li02_02_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m03\M003_s014a_Li02_02_offer.ini
+Act_AddRTC = missions\m03\M003_s014d_Li02_02_reoffer.ini, repeatable
@@ -1388 +1388 @@
-Act_RemoveRTC = missions\\m03\\M003_s014d_Li02_02_reoffer.ini
+Act_RemoveRTC = missions\m03\M003_s014d_Li02_02_reoffer.ini
@@ -2264 +2264 @@
-Act_CallThorn = missions\\M03\\M03_Rfighter_Encounter.thn, Player
+Act_CallThorn = missions\M03\M03_Rfighter_Encounter.thn, Player
@@ -2297 +2297 @@
-Act_CallThorn = missions\\M03\\M03_Rfighter_Response.thn, rfighter1
+Act_CallThorn = missions\M03\M03_Rfighter_Response.thn, rfighter1
@@ -2309 +2309 @@
-Act_CallThorn = missions\\M03\\M03_Rfighter_End.thn, Player
+Act_CallThorn = missions\M03\M03_Rfighter_End.thn, Player
@@ -2404 +2404 @@
-Act_AddRTC = missions//m03//M003_s015x_Li02_02_nrml.ini
+Act_AddRTC = missions\m03\M003_s015x_Li02_02_nrml.ini
```

</details>

#### `Missions/M04/M004_s019a_Li01_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -9 +9 @@
-autoplay
+autoplay = true
```

#### `Missions/M04/M004_s019d_Li01_01_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -9 +9 @@
-autoplay
+autoplay = true
```

#### `Missions/M04/M004_s020x_Li01_04_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M04/M004_s021x_Br04_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M04/m04.ini`

14 Hunks, +13 / −16 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (43 Zeilen)</summary>

```diff
@@ -4,2 +3,0 @@
-[Constants]
-
@@ -1096 +1093,0 @@
-label = station_attack_wing
@@ -1550 +1547 @@
-Act_AddRTC = missions\\m04\\M004_s019a_Li01_01_offer.ini
+Act_AddRTC = missions\m04\M004_s019a_Li01_01_offer.ini
@@ -1559 +1556 @@
-Act_RemoveRTC = missions\\m04\\M004_s019d_Li01_01_reoffer.ini
+Act_RemoveRTC = missions\m04\M004_s019d_Li01_01_reoffer.ini
@@ -1581 +1578 @@
-Act_CallThorn = missions\\m04\\M04_space_enter.thn, Player
+Act_CallThorn = missions\m04\M04_space_enter.thn, Player
@@ -1592,2 +1589,2 @@
-Act_RemoveRTC = missions\\m04\\M004_s019a_Li01_01_offer.ini
-Act_AddRTC = missions\\m04\\M004_s019d_Li01_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m04\M004_s019a_Li01_01_offer.ini
+Act_AddRTC = missions\m04\M004_s019d_Li01_01_reoffer.ini, repeatable
@@ -1897 +1894 @@
-Act_CallThorn = missions\\m04\\M04_space_enter.thn, Player
+Act_CallThorn = missions\m04\M04_space_enter.thn, Player
@@ -2155 +2152 @@
-Act_CallThorn = missions\\m04\\M04_LSF_Flyby.thn, rogue1
+Act_CallThorn = missions\m04\M04_LSF_Flyby.thn, rogue1
@@ -3103 +3100 @@
-Act_AddRTC = missions\\m04\\M004_s020x_Li01_04_nrml.ini
+Act_AddRTC = missions\m04\M004_s020x_Li01_04_nrml.ini
@@ -3406 +3403 @@
-Act_CallThorn = missions\\m04\\m04_02.thn, Player
+Act_CallThorn = missions\m04\m04_02.thn, Player
@@ -3544 +3541 @@
-Act_CallThorn = missions\\m04\\M04_VanPelt_Final.thn, station_cruiser1
+Act_CallThorn = missions\m04\M04_VanPelt_Final.thn, station_cruiser1
@@ -3653 +3650 @@
-Act_CallThorn = missions\\m04\\m04_01.thn, Player
+Act_CallThorn = missions\m04\m04_01.thn, Player
@@ -3660 +3657 @@
-Act_CallThorn = missions\\m04\\M04_Vanpelt_talks.thn, Player
+Act_CallThorn = missions\m04\M04_Vanpelt_talks.thn, Player
@@ -5351 +5348 @@
-Act_AddRTC = missions\\m04\\M004_s021x_Br04_01_nrml.ini
+Act_AddRTC = missions\m04\M004_s021x_Br04_01_nrml.ini
```

</details>

#### `Missions/M05/M005_s026a_Br03_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -9 +9 @@
-autoplay
+autoplay = true
```

#### `Missions/M05/M005_s026d_Br03_01_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -9 +9 @@
-autoplay
+autoplay = true
```

#### `Missions/M05/M005_s027xa_Bw01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M05/M005_s027xb_Bw01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M05/M005_s027xc_Bw01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M05/M005_s028x_Bw01_05_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M05/M005_s029x_Br04_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M05/m05.ini`

18 Hunks, +22 / −23 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (63 Zeilen)</summary>

```diff
@@ -714 +714 @@
-Act_AddRTC = missions\\m05\\M005_s026a_Br03_01_offer.ini
+Act_AddRTC = missions\m05\M005_s026a_Br03_01_offer.ini
@@ -722,2 +722,2 @@
-Act_RemoveRTC = missions\\m05\\M005_s026a_Br03_01_offer.ini
-Act_AddRTC = missions\\m05\\M005_s026d_Br03_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m05\M005_s026a_Br03_01_offer.ini
+Act_AddRTC = missions\m05\M005_s026d_Br03_01_reoffer.ini, repeatable
@@ -736 +736 @@
-Act_RemoveRTC = missions\\m05\\M005_s026d_Br03_01_reoffer.ini
+Act_RemoveRTC = missions\m05\M005_s026d_Br03_01_reoffer.ini
@@ -1069 +1069 @@
-Act_CallThorn = missions\\m05\\M05_Sprague_Decloak.thn, cloaked_rf2
+Act_CallThorn = missions\m05\M05_Sprague_Decloak.thn, cloaked_rf2
@@ -1176 +1176 @@
-Act_AddRTC = missions\\m05\\M005_s027xa_Bw01_01_nrml.ini, repeatable
+Act_AddRTC = missions\m05\M005_s027xa_Bw01_01_nrml.ini, repeatable
@@ -1186 +1186 @@
-Act_AddRTC = missions\\m05\\M005_s027xb_Bw01_01_nrml.ini, repeatable
+Act_AddRTC = missions\m05\M005_s027xb_Bw01_01_nrml.ini, repeatable
@@ -1192 +1192 @@
-Act_AddRTC = missions\\m05\\M005_s027xc_Bw01_01_nrml.ini, repeatable
+Act_AddRTC = missions\m05\M005_s027xc_Bw01_01_nrml.ini, repeatable
@@ -1217 +1217 @@
-Act_CallThorn = missions\\m05\\M05_Dock_Explodes.thn
+Act_CallThorn = missions\m05\M05_Dock_Explodes.thn
@@ -1226,4 +1226,4 @@
-Act_RemoveRTC = missions\\m05\\M005_s027xa_Bw01_01_nrml.ini
-Act_RemoveRTC = missions\\m05\\M005_s027xb_Bw01_01_nrml.ini
-Act_RemoveRTC = missions\\m05\\M005_s027xc_Bw01_01_nrml.ini
-Act_CallThorn = missions\\m05\\M05_Dock_Explodes.thn
+Act_RemoveRTC = missions\m05\M005_s027xa_Bw01_01_nrml.ini
+Act_RemoveRTC = missions\m05\M005_s027xb_Bw01_01_nrml.ini
+Act_RemoveRTC = missions\m05\M005_s027xc_Bw01_01_nrml.ini
+Act_CallThorn = missions\m05\M05_Dock_Explodes.thn
@@ -1564 +1564 @@
-Act_AddRTC = missions\\m05\\M005_s028x_Bw01_05_nrml.ini
+Act_AddRTC = missions\m05\M005_s028x_Bw01_05_nrml.ini
@@ -1573,2 +1573,2 @@
-Act_RemoveRTC = missions\\m05\\M005_s028x_Bw01_05_nrml.ini
-Act_CallThorn = missions\\m05\\M05_Baxter_Explodes.thn
+Act_RemoveRTC = missions\m05\M005_s028x_Bw01_05_nrml.ini
+Act_CallThorn = missions\m05\M05_Baxter_Explodes.thn
@@ -1828 +1828 @@
-Act_CallThorn = missions\\m05\\m05_traitor_01.thn, rh_traitor1
+Act_CallThorn = missions\m05\m05_traitor_01.thn, rh_traitor1
@@ -1845 +1844,0 @@
-Act_NagOff = to_br03_23_ring
@@ -1859 +1858 @@
-Act_CallThorn = missions\\m05\\m05_traitor_02.thn, Player
+Act_CallThorn = missions\m05\m05_traitor_02.thn, Player
@@ -2052 +2051 @@
-Act_CallThorn = missions\\m05\\M05_Chase.thn, rh_traitor2
+Act_CallThorn = missions\m05\M05_Chase.thn, rh_traitor2
@@ -2140 +2139 @@
-Act_CallThorn = missions\\m05\\M05_Battleship_Death.thn, rh_battleship
+Act_CallThorn = missions\m05\M05_Battleship_Death.thn, rh_battleship
@@ -2399 +2398 @@
-Act_AddRTC = missions\\m05\\M005_s029x_Br04_01_nrml.ini
+Act_AddRTC = missions\m05\M005_s029x_Br04_01_nrml.ini
@@ -2413 +2412 @@
-Act_AddRTC = missions\\m05\\M005_s029x_Br04_01_nrml.ini
+Act_AddRTC = missions\m05\M005_s029x_Br04_01_nrml.ini
```

</details>

#### `Missions/M06/M006_s032a_Br05_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M06/M006_s033x_Br05_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M06/M006_s034x_Br05_02_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M06/m06.ini`

21 Hunks, +22 / −22 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (65 Zeilen)</summary>

```diff
@@ -490 +490 @@
-Act_AddRTC = //missions//m06//M006_s032a_Br05_01_offer.ini
+Act_AddRTC = missions\m06\M006_s032a_Br05_01_offer.ini
@@ -498,2 +498,2 @@
-Act_RemoveRTC = //missions//m06//M006_s032a_Br05_01_offer.ini
-Act_AddRTC = missions\\m06\\M006_s032d_Br05_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m06\M006_s032a_Br05_01_offer.ini
+Act_AddRTC = missions\m06\M006_s032d_Br05_01_reoffer.ini, repeatable
@@ -522 +522 @@
-Act_RemoveRTC = missions\\m06\\M006_s032d_Br05_01_reoffer.ini
+Act_RemoveRTC = missions\m06\M006_s032d_Br05_01_reoffer.ini
@@ -622 +622 @@
-Act_CallThorn = missions\\m06\\M06_Race_Hood1.thn, Player
+Act_CallThorn = missions\m06\M06_Race_Hood1.thn, Player
@@ -647 +647 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood2.thn, Player
+Act_CallThorn = missions\m06\m06_Race_Hood2.thn, Player
@@ -755 +755 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood4_buoy.thn, Br05_telescope_1
+Act_CallThorn = missions\m06\m06_Race_Hood4_buoy.thn, Br05_telescope_1
@@ -774 +774 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood5.thn, dexter
+Act_CallThorn = missions\m06\m06_Race_Hood5.thn, dexter
@@ -863 +863 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood3Alt.thn, dexter
+Act_CallThorn = missions\m06\m06_Race_Hood3Alt.thn, dexter
@@ -914 +914 @@
-Act_CallThorn = missions\\m06\\M06_Hovis_Wins1.thn, dexter
+Act_CallThorn = missions\m06\M06_Hovis_Wins1.thn, dexter
@@ -933 +933 @@
-Act_CallThorn = missions\\m01a\\m01a_rev2_01.thn, Player
+Act_CallThorn = missions\m01a\m01a_rev2_01.thn, Player
@@ -940 +940 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood6.thn, Player
+Act_CallThorn = missions\m06\m06_Race_Hood6.thn, Player
@@ -1914 +1914 @@
-Act_CallThorn = missions\\m06\\M06_finish_line.thn, Player
+Act_CallThorn = missions\m06\M06_finish_line.thn, Player
@@ -1973 +1973 @@
-Act_CallThorn = missions\\m06\\M06_finish_line.thn, Player
+Act_CallThorn = missions\m06\M06_finish_line.thn, Player
@@ -2001 +2001 @@
-system
+system = Br05
@@ -2008 +2008 @@
-system
+system = Br05
@@ -2215 +2215 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood2.thn, Player
+Act_CallThorn = missions\m06\m06_Race_Hood2.thn, Player
@@ -2312 +2312 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood2.thn, dexter
+Act_CallThorn = missions\m06\m06_Race_Hood2.thn, dexter
@@ -2335 +2335 @@
-Act_CallThorn = missions\\m06\\m06_Race_Hood2.thn, Player
+Act_CallThorn = missions\m06\m06_Race_Hood2.thn, Player
@@ -2557 +2557 @@
-Act_AddRTC = //missions//m06//M006_s033x_Br05_01_nrml.ini
+Act_AddRTC = missions\m06\M006_s033x_Br05_01_nrml.ini
@@ -2936 +2936 @@
-Act_AddRTC = //missions//m06//M006_s034x_Br05_02_nrml.ini
+Act_AddRTC = missions\m06\M006_s034x_Br05_02_nrml.ini
@@ -3761 +3761 @@
-Act_CallThorn = missions\\m06\\M06_finish_line.thn, dexter
+Act_CallThorn = missions\m06\M06_finish_line.thn, dexter
```

</details>

#### `Missions/M07/M007_s037a_Br04_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -9 +9 @@
-autoplay
+autoplay = true
```

#### `Missions/M07/M007_s037d_Br04_01_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M07/M007_s038xa_Bw08_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M07/M007_s038xb_Bw08_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M07/M007_s039x_Ku03_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M07/m07.ini`

16 Hunks, +17 / −17 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (50 Zeilen)</summary>

```diff
@@ -974 +974 @@
-Act_AddRTC = missions\\m07\\M007_s037a_Br04_01_offer.ini
+Act_AddRTC = missions\m07\M007_s037a_Br04_01_offer.ini
@@ -988,2 +988,2 @@
-Act_RemoveRTC = missions\\m07\\M007_s037a_Br04_01_offer.ini
-Act_AddRTC = missions\\m07\\M007_s037d_Br04_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m07\M007_s037a_Br04_01_offer.ini
+Act_AddRTC = missions\m07\M007_s037d_Br04_01_reoffer.ini, repeatable
@@ -995 +995 @@
-Act_RemoveRTC = missions\\m07\\M007_s037d_Br04_01_reoffer.ini
+Act_RemoveRTC = missions\m07\M007_s037d_Br04_01_reoffer.ini
@@ -1041 +1041 @@
-Act_CallThorn = missions\\m07\\M07_Intro.thn, Player
+Act_CallThorn = missions\m07\M07_Intro.thn, Player
@@ -1053 +1053 @@
-Act_CallThorn = missions\\m07\\M07_Intro2.thn, juni
+Act_CallThorn = missions\m07\M07_Intro2.thn, juni
@@ -1065 +1065 @@
-Act_CallThorn = missions\\m07\\M07_Intro2b.thn, Player
+Act_CallThorn = missions\m07\M07_Intro2b.thn, Player
@@ -1100 +1100 @@
-Act_CallThorn = missions\\m07\\M07_Intro3.thn, Player
+Act_CallThorn = missions\m07\M07_Intro3.thn, Player
@@ -2488 +2488 @@
-Act_CallThorn = missions\\m07\\M07_Fleet1.thn, sluthammer1
+Act_CallThorn = missions\m07\M07_Fleet1.thn, sluthammer1
@@ -2578 +2578 @@
-Act_CallThorn = missions\\m07\\M07_Fleet2.thn, Player
+Act_CallThorn = missions\m07\M07_Fleet2.thn, Player
@@ -2608 +2608 @@
-Act_CallThorn = missions\\m07\\M07_Fleet3.thn, order_wing1_1
+Act_CallThorn = missions\m07\M07_Fleet3.thn, order_wing1_1
@@ -2626 +2626 @@
-Act_CallThorn = missions\\m07\\M07_Fleet4.thn, sluthammer1
+Act_CallThorn = missions\m07\M07_Fleet4.thn, sluthammer1
@@ -2658 +2658 @@
-Act_CallThorn = missions\\m07\\M07_Fleet6_chasecam.thn, order_wing1_1
+Act_CallThorn = missions\m07\M07_Fleet6_chasecam.thn, order_wing1_1
@@ -2684 +2684 @@
-Act_CallThorn = missions\\m07\\M07_Fleet7_bship.thn, sluthammer1
+Act_CallThorn = missions\m07\M07_Fleet7_bship.thn, sluthammer1
@@ -3042 +3042 @@
-Act_AddRTC = //missions//m07//M007_s038xa_Bw08_01_nrml.ini
+Act_AddRTC = missions\m07\M007_s038xa_Bw08_01_nrml.ini
@@ -3049 +3049 @@
-Act_AddRTC = //missions//m07//M007_s038xb_Bw08_01_nrml.ini
+Act_AddRTC = missions\m07\M007_s038xb_Bw08_01_nrml.ini
@@ -3236 +3236 @@
-Act_AddRTC = missions\\m07\\M007_s039x_Ku03_01_nrml.ini
+Act_AddRTC = missions\m07\M007_s039x_Ku03_01_nrml.ini
```

</details>

#### `Missions/M08/M008_s045a_Ku01_05_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -7 +7 @@
-autoplay
+autoplay = true
```

#### `Missions/M08/M008_s046x_Ku06_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M08/m08.ini`

5 Hunks, +7 / −7 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -456 +456 @@
-Act_AddRTC = missions\\m08\\M008_s045a_ku01_05_offer.ini
+Act_AddRTC = missions\m08\M008_s045a_ku01_05_offer.ini
@@ -464,2 +464,2 @@
-Act_RemoveRTC = missions\\m08\\M008_s045a_ku01_05_offer.ini
-Act_AddRTC = missions\\m08\\M008_s045d_ku01_05_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m08\M008_s045a_ku01_05_offer.ini
+Act_AddRTC = missions\m08\M008_s045d_ku01_05_reoffer.ini, repeatable
@@ -475,2 +475,2 @@
-Act_RemoveRTC = missions\\m08\\M008_s045d_ku01_05_reoffer.ini
-Act_AddRTC = missions\\m08\\M008_s046x_ku06_01_nrml.ini
+Act_RemoveRTC = missions\m08\M008_s045d_ku01_05_reoffer.ini
+Act_AddRTC = missions\m08\M008_s046x_ku06_01_nrml.ini
@@ -861 +861 @@
-BreakFormation
+BreakFormation = no_params
@@ -1135 +1135 @@
-Act_AddRTC = missions\\m08\\M008_s046x_ku06_01_nrml.ini
+Act_AddRTC = missions\m08\M008_s046x_ku06_01_nrml.ini
```

#### `Missions/M09/M009_s050a_Ku06_01_bar_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M09/M009_s050d_Ku06_01_bar_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M09/M009_s051xa_Ku07_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M09/M009_s051xb_Ku07_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M09/M009_s051xc_Ku07_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M09/M009_s052x_Ku06_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M09/m09.ini`

7 Hunks, +8 / −8 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1016 +1016 @@
-Act_AddRTC = missions\\m09\\M009_s050a_Ku06_01_bar_offer.ini
+Act_AddRTC = missions\m09\M009_s050a_Ku06_01_bar_offer.ini
@@ -1024,2 +1024,2 @@
-Act_RemoveRTC = missions\\m09\\M009_s050a_Ku06_01_bar_offer.ini
-Act_AddRTC = missions\\m09\\M009_s050d_Ku06_01_bar_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m09\M009_s050a_Ku06_01_bar_offer.ini
+Act_AddRTC = missions\m09\M009_s050d_Ku06_01_bar_reoffer.ini, repeatable
@@ -1031 +1031 @@
-Act_RemoveRTC = missions\\m09\\M009_s050d_Ku06_01_bar_reoffer.ini
+Act_RemoveRTC = missions\m09\M009_s050d_Ku06_01_bar_reoffer.ini
@@ -1815 +1815 @@
-Act_AddRTC = //missions//m09//M009_s051xa_Ku07_01_nrml.ini
+Act_AddRTC = missions\m09\M009_s051xa_Ku07_01_nrml.ini
@@ -1822 +1822 @@
-Act_AddRTC = //missions//m09//M009_s051xb_Ku07_01_nrml.ini
+Act_AddRTC = missions\m09\M009_s051xb_Ku07_01_nrml.ini
@@ -1836 +1836 @@
-Act_AddRTC = //missions//m09//M009_s051xc_Ku07_01_nrml.ini
+Act_AddRTC = missions\m09\M009_s051xc_Ku07_01_nrml.ini
@@ -2163 +2163 @@
-Act_AddRTC = missions\\m09\\M009_s052x_Ku06_01_nrml.ini
+Act_AddRTC = missions\m09\M009_s052x_Ku06_01_nrml.ini
```

#### `Missions/M10/dummy_test.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M10/M010_s055a_Ku06_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M10/M010_s059x_Rh01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M10/M010_s062x_Rh04_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M10/M010_s063x_Rh04_05_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M10/m010_s064x_rh02_07_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M10/m10.ini`

11 Hunks, +12 / −12 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -3577 +3577 @@
-Act_AddRTC = //missions//m10//M010_s055a_Ku06_01_offer.ini
+Act_AddRTC = missions\m10\M010_s055a_Ku06_01_offer.ini
@@ -3586,2 +3586,2 @@
-Act_RemoveRTC = //missions//m10//M010_s055a_Ku06_01_offer.ini
-Act_AddRTC = missions//m10//M010_s055d_Ku06_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m10\M010_s055a_Ku06_01_offer.ini
+Act_AddRTC = missions\m10\M010_s055d_Ku06_01_reoffer.ini, repeatable
@@ -3594 +3594 @@
-Act_RemoveRTC = missions//m10//M010_s055a_Ku06_01_offer.ini
+Act_RemoveRTC = missions\m10\M010_s055a_Ku06_01_offer.ini
@@ -4484 +4484 @@
-Act_AddRTC = //missions//m10//dummy_test.ini
+Act_AddRTC = missions\m10\dummy_test.ini
@@ -4499 +4499 @@
-Act_AddRTC = //missions//m10//M010_s059x_Rh01_01_nrml.ini
+Act_AddRTC = missions\m10\M010_s059x_Rh01_01_nrml.ini
@@ -4872 +4872 @@
-Act_AddRTC = //missions//m10//M010_s062x_Rh04_01_nrml.ini
+Act_AddRTC = missions\m10\M010_s062x_Rh04_01_nrml.ini
@@ -5166 +5166 @@
-Act_AddRTC = missions//m10//M010_s063x_Rh04_05_nrml.ini
+Act_AddRTC = missions\m10\M010_s063x_Rh04_05_nrml.ini
@@ -5184 +5184 @@
-Act_CallThorn = missions\\m10\\M10_Bund_Launch.thn, Von_Claussen
+Act_CallThorn = missions\m10\M10_Bund_Launch.thn, Von_Claussen
@@ -5209 +5209 @@
-Act_CallThorn = missions\\m10\\M10_Bund_Launch.thn, Von_Claussen
+Act_CallThorn = missions\m10\M10_Bund_Launch.thn, Von_Claussen
@@ -6526 +6526 @@
-Act_CallThorn = missions\\m10\\m10_Minefield.thn, Von_Claussen
+Act_CallThorn = missions\m10\m10_Minefield.thn, Von_Claussen
@@ -7648 +7648 @@
-Act_AddRTC = //missions//m10//m010_s064x_rh02_07_nrml.ini
+Act_AddRTC = missions\m10\m010_s064x_rh02_07_nrml.ini
```

#### `Missions/M11/M011_s067a_Iw02_03_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -7 +7 @@
-autoplay
+autoplay = true
```

#### `Missions/M11/M011_s067d_Iw02_03_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M11/M011_s068x_Li01_12_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M11/M011_s069x_Li05_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M11/M011_s070x_Li01_15_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M11/m11.ini`

7 Hunks, +7 / −7 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1411 +1411 @@
-Act_AddRTC = //missions//m11//M011_s067a_Iw02_03_offer.ini
+Act_AddRTC = missions\m11\M011_s067a_Iw02_03_offer.ini
@@ -1413 +1413 @@
-Act_AddAmbient = Scripts\\Bases\\Li_05_Deck_Ambi_s067_music.thn, Deck, Li04_06_base
+Act_AddAmbient = Scripts\Bases\Li_05_Deck_Ambi_s067_music.thn, Deck, Li04_06_base
@@ -1420 +1420 @@
-Act_RemoveRTC = //missions//m11//M011_s067a_Iw02_03_offer.ini
+Act_RemoveRTC = missions\m11\M011_s067a_Iw02_03_offer.ini
@@ -1432 +1432 @@
-Act_RemoveAmbient = Scripts\\Bases\\Li_05_Deck_Ambi_s067_music.thn
+Act_RemoveAmbient = Scripts\Bases\Li_05_Deck_Ambi_s067_music.thn
@@ -1731 +1731 @@
-Act_AddRTC = //missions//m11//M011_s068x_Li01_12_nrml.ini
+Act_AddRTC = missions\m11\M011_s068x_Li01_12_nrml.ini
@@ -2893 +2893 @@
-Act_AddRTC = //missions//m11//M011_s069x_Li05_01_nrml.ini, repeatable
+Act_AddRTC = missions\m11\M011_s069x_Li05_01_nrml.ini, repeatable
@@ -2912 +2912 @@
-Act_RemoveRTC = //missions//m11//M011_s069x_Li05_01_nrml.ini
+Act_RemoveRTC = missions\m11\M011_s069x_Li05_01_nrml.ini
```

#### `Missions/M12/dummy_test.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M12/M012_s071a_St02_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -7 +7 @@
-autoplay
+autoplay = true
```

#### `Missions/M12/M012_s071d_St02_01_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M12/m12.ini`

9 Hunks, +8 / −10 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -2092 +2092 @@
-Act_AddRTC = missions\\m12\\dummy_test.ini
+Act_AddRTC = missions\m12\dummy_test.ini
@@ -2105 +2105 @@
-Act_AddRTC = missions\\m11\\M011_s070x_Li01_15_nrml.ini
+Act_AddRTC = missions\m11\M011_s070x_Li01_15_nrml.ini
@@ -2115 +2115 @@
-Act_AddRTC = missions\\m12\\M012_s071a_St02_01_offer.ini
+Act_AddRTC = missions\m12\M012_s071a_St02_01_offer.ini
@@ -2125,2 +2125,2 @@
-Act_RemoveRTC = missions\\m12\\M012_s071a_St02_01_offer.ini
-Act_AddRTC = missions\\m12\\M012_s071d_St02_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m12\M012_s071a_St02_01_offer.ini
+Act_AddRTC = missions\m12\M012_s071d_St02_01_reoffer.ini, repeatable
@@ -2132 +2132 @@
-Act_RemoveRTC = missions\\m12\\M012_s071d_St02_01_reoffer.ini
+Act_RemoveRTC = missions\m12\M012_s071d_St02_01_reoffer.ini
@@ -2391 +2391 @@
-Act_CallThorn = missions\\m12\\M12_Osiris.thn, osiris
+Act_CallThorn = missions\m12\M12_Osiris.thn, osiris
@@ -3227 +3227 @@
-system St02
+system = St02
@@ -3311 +3310,0 @@
-system = St02
@@ -3430 +3428,0 @@
-Idle = no_params
```

#### `Missions/M13/M013_Endgame_St03b_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s072aa_St01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s072ab_St01_01_offer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -7 +7 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s072bb_St01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s072d_St01_01_reoffer.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -8 +8 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s074x_St01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s075x_St01_02_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -5 +5 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s076xa_Li01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/M013_s076xb_Li01_01_nrml.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Dec 02 00:00:00 2003

```diff
@@ -4 +4 @@
-autoplay
+autoplay = true
```

#### `Missions/M13/m13.ini`

10 Hunks, +11 / −11 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1211 +1211 @@
-Act_AddRTC = missions\\m13\\M013_s072aa_St01_01_nrml.ini
+Act_AddRTC = missions\m13\M013_s072aa_St01_01_nrml.ini
@@ -1217 +1217 @@
-Act_AddRTC = missions\\m13\\M013_s072ab_St01_01_offer.ini
+Act_AddRTC = missions\m13\M013_s072ab_St01_01_offer.ini
@@ -1224,2 +1224,2 @@
-Act_RemoveRTC = missions\\m13\\M013_s072ab_St01_01_offer.ini
-Act_AddRTC = missions\\m13\\M013_s072d_St01_01_reoffer.ini, repeatable
+Act_RemoveRTC = missions\m13\M013_s072ab_St01_01_offer.ini
+Act_AddRTC = missions\m13\M013_s072d_St01_01_reoffer.ini, repeatable
@@ -1233 +1233 @@
-Act_RemoveRTC = missions\\m13\\M013_s072d_St01_01_reoffer.ini
+Act_RemoveRTC = missions\m13\M013_s072d_St01_01_reoffer.ini
@@ -1248 +1248 @@
-Act_AddRTC = missions\\m13\\M013_s072bb_St01_01_nrml.ini
+Act_AddRTC = missions\m13\M013_s072bb_St01_01_nrml.ini
@@ -1593 +1593 @@
-Act_AddRTC = missions\\m13\\M013_s074x_St01_01_nrml.ini
+Act_AddRTC = missions\m13\M013_s074x_St01_01_nrml.ini
@@ -1841 +1841 @@
-Act_AddRTC = missions\\m13\\M013_s075x_St01_02_nrml.ini
+Act_AddRTC = missions\m13\M013_s075x_St01_02_nrml.ini
@@ -2568 +2568 @@
-Act_AddRTC = missions\\m13\\M013_Endgame_St03b_nrml.ini
+Act_AddRTC = missions\m13\M013_Endgame_St03b_nrml.ini
@@ -2573 +2573 @@
-Act_AddRTC = missions\\m13\\M013_s076xa_Li01_01_nrml.ini
+Act_AddRTC = missions\m13\M013_s076xa_Li01_01_nrml.ini
@@ -2578 +2578 @@
-Act_AddRTC = missions\\m13\\M013_s076xb_Li01_01_nrml.ini
+Act_AddRTC = missions\m13\M013_s076xb_Li01_01_nrml.ini
```

#### `Missions/mBases.ini`

241 Hunks, +241 / −241 Zeilen · Mon Sep 01 00:00:00 2003 → Sat Sep 13 00:00:00 2003

<details><summary>Diff anzeigen (723 Zeilen)</summary>

```diff
@@ -13 +13 @@
-offers_missions
+offers_missions = true
@@ -22 +22 @@
-offers_missions
+offers_missions = true
@@ -31 +31 @@
-offers_missions
+offers_missions = true
@@ -1319 +1319 @@
-offers_missions
+offers_missions = true
@@ -1326 +1326 @@
-offers_missions
+offers_missions = true
@@ -1351 +1351 @@
-offers_missions
+offers_missions = true
@@ -1968 +1968 @@
-offers_missions
+offers_missions = true
@@ -1987 +1987 @@
-offers_missions
+offers_missions = true
@@ -2454 +2454 @@
-offers_missions
+offers_missions = true
@@ -2881 +2881 @@
-offers_missions
+offers_missions = true
@@ -2931 +2931 @@
-offers_missions
+offers_missions = true
@@ -3653 +3653 @@
-offers_missions
+offers_missions = true
@@ -3673 +3673 @@
-offers_missions
+offers_missions = true
@@ -4375 +4375 @@
-offers_missions
+offers_missions = true
@@ -4390 +4390 @@
-offers_missions
+offers_missions = true
@@ -4828 +4828 @@
-offers_missions
+offers_missions = true
@@ -4835 +4835 @@
-offers_missions
+offers_missions = true
@@ -4850 +4850 @@
-offers_missions
+offers_missions = true
@@ -5326 +5326 @@
-offers_missions
+offers_missions = true
@@ -5376 +5376 @@
-offers_missions
+offers_missions = true
@@ -6110 +6110 @@
-offers_missions
+offers_missions = true
@@ -6118 +6118 @@
-offers_missions
+offers_missions = true
@@ -6530 +6530 @@
-offers_missions
+offers_missions = true
@@ -6540 +6540 @@
-offers_missions
+offers_missions = true
@@ -6946 +6946 @@
-offers_missions
+offers_missions = true
@@ -6963 +6963 @@
-offers_missions
+offers_missions = true
@@ -6998 +6998 @@
-offers_missions
+offers_missions = true
@@ -7751 +7751 @@
-offers_missions
+offers_missions = true
@@ -8002 +8002 @@
-offers_missions
+offers_missions = true
@@ -8009 +8009 @@
-offers_missions
+offers_missions = true
@@ -8054 +8054 @@
-offers_missions
+offers_missions = true
@@ -8609 +8609 @@
-offers_missions
+offers_missions = true
@@ -8616 +8616 @@
-offers_missions
+offers_missions = true
@@ -8630 +8630 @@
-offers_missions
+offers_missions = true
@@ -8977 +8977 @@
-offers_missions
+offers_missions = true
@@ -8996 +8996 @@
-offers_missions
+offers_missions = true
@@ -9291 +9291 @@
-offers_missions
+offers_missions = true
@@ -9306 +9306 @@
-offers_missions
+offers_missions = true
@@ -9634 +9634 @@
-offers_missions
+offers_missions = true
@@ -9647 +9647 @@
-offers_missions
+offers_missions = true
@@ -9855 +9855 @@
-offers_missions
+offers_missions = true
@@ -9862 +9862 @@
-offers_missions
+offers_missions = true
@@ -10139 +10139 @@
-offers_missions
+offers_missions = true
@@ -10178 +10178 @@
-offers_missions
+offers_missions = true
@@ -10646 +10646 @@
-offers_missions
+offers_missions = true
@@ -10665 +10665 @@
-offers_missions
+offers_missions = true
@@ -10960 +10960 @@
-offers_missions
+offers_missions = true
@@ -11146 +11146 @@
-offers_missions
+offers_missions = true
@@ -11557 +11557 @@
-offers_missions
+offers_missions = true
@@ -11600 +11600 @@
-offers_missions
+offers_missions = true
@@ -12053 +12053 @@
-offers_missions
+offers_missions = true
@@ -12067 +12067 @@
-offers_missions
+offers_missions = true
@@ -12329 +12329 @@
-offers_missions
+offers_missions = true
@@ -12348 +12348 @@
-offers_missions
+offers_missions = true
@@ -12654 +12654 @@
-offers_missions
+offers_missions = true
@@ -12663 +12663 @@
-offers_missions
+offers_missions = true
@@ -13034 +13034 @@
-offers_missions
+offers_missions = true
@@ -13063 +13063 @@
-offers_missions
+offers_missions = true
@@ -13699 +13699 @@
-offers_missions
+offers_missions = true
@@ -13762 +13762 @@
-offers_missions
+offers_missions = true
@@ -14294 +14294 @@
-offers_missions
+offers_missions = true
@@ -14312 +14312 @@
-offers_missions
+offers_missions = true
@@ -14341 +14341 @@
-offers_missions
+offers_missions = true
@@ -14799 +14799 @@
-offers_missions
+offers_missions = true
@@ -14812 +14812 @@
-offers_missions
+offers_missions = true
@@ -15055 +15055 @@
-offers_missions
+offers_missions = true
@@ -15069 +15069 @@
-offers_missions
+offers_missions = true
@@ -15351 +15351 @@
-offers_missions
+offers_missions = true
@@ -15359 +15359 @@
-offers_missions
+offers_missions = true
@@ -15368 +15368 @@
-offers_missions
+offers_missions = true
@@ -15666 +15666 @@
-offers_missions
+offers_missions = true
@@ -15848 +15848 @@
-offers_missions
+offers_missions = true
@@ -15861 +15861 @@
-offers_missions
+offers_missions = true
@@ -16154 +16154 @@
-offers_missions
+offers_missions = true
@@ -16162 +16162 @@
-offers_missions
+offers_missions = true
@@ -16170 +16170 @@
-offers_missions
+offers_missions = true
@@ -16179 +16179 @@
-offers_missions
+offers_missions = true
@@ -16186 +16186 @@
-offers_missions
+offers_missions = true
@@ -16620 +16620 @@
-offers_missions
+offers_missions = true
@@ -16634 +16634 @@
-offers_missions
+offers_missions = true
@@ -16904 +16904 @@
-offers_missions
+offers_missions = true
@@ -16923 +16923 @@
-offers_missions
+offers_missions = true
@@ -17210 +17210 @@
-offers_missions
+offers_missions = true
@@ -17233 +17233 @@
-offers_missions
+offers_missions = true
@@ -17577 +17577 @@
-offers_missions
+offers_missions = true
@@ -17774 +17774 @@
-offers_missions
+offers_missions = true
@@ -17971 +17971 @@
-offers_missions
+offers_missions = true
@@ -18291 +18291 @@
-offers_missions
+offers_missions = true
@@ -18478 +18478 @@
-offers_missions
+offers_missions = true
@@ -18491 +18491 @@
-offers_missions
+offers_missions = true
@@ -18742 +18742 @@
-offers_missions
+offers_missions = true
@@ -18934 +18934 @@
-offers_missions
+offers_missions = true
@@ -19404 +19404 @@
-offers_missions
+offers_missions = true
@@ -19762 +19762 @@
-offers_missions
+offers_missions = true
@@ -19775 +19775 @@
-offers_missions
+offers_missions = true
@@ -20006 +20006 @@
-offers_missions
+offers_missions = true
@@ -20217 +20217 @@
-offers_missions
+offers_missions = true
@@ -20225 +20225 @@
-offers_missions
+offers_missions = true
@@ -20489 +20489 @@
-offers_missions
+offers_missions = true
@@ -20503 +20503 @@
-offers_missions
+offers_missions = true
@@ -20777 +20777 @@
-offers_missions
+offers_missions = true
@@ -20786 +20786 @@
-offers_missions
+offers_missions = true
@@ -21094 +21094 @@
-offers_missions
+offers_missions = true
@@ -21109 +21109 @@
-offers_missions
+offers_missions = true
@@ -21271 +21271 @@
-offers_missions
+offers_missions = true
@@ -21284 +21284 @@
-offers_missions
+offers_missions = true
@@ -21518 +21518 @@
-offers_missions
+offers_missions = true
@@ -21737 +21737 @@
-offers_missions
+offers_missions = true
@@ -21751 +21751 @@
-offers_missions
+offers_missions = true
@@ -22131 +22131 @@
-offers_missions
+offers_missions = true
@@ -22145 +22145 @@
-offers_missions
+offers_missions = true
@@ -22413 +22413 @@
-offers_missions
+offers_missions = true
@@ -22591 +22591 @@
-offers_missions
+offers_missions = true
@@ -22774 +22774 @@
-offers_missions
+offers_missions = true
@@ -23130 +23130 @@
-offers_missions
+offers_missions = true
@@ -23395 +23395 @@
-offers_missions
+offers_missions = true
@@ -23403 +23403 @@
-offers_missions
+offers_missions = true
@@ -23621 +23621 @@
-offers_missions
+offers_missions = true
@@ -23848 +23848 @@
-offers_missions
+offers_missions = true
@@ -24022 +24022 @@
-offers_missions
+offers_missions = true
@@ -24186 +24186 @@
-offers_missions
+offers_missions = true
@@ -24368 +24368 @@
-offers_missions
+offers_missions = true
@@ -24536 +24536 @@
-offers_missions
+offers_missions = true
@@ -24732 +24732 @@
-offers_missions
+offers_missions = true
@@ -25000 +25000 @@
-offers_missions
+offers_missions = true
@@ -25008 +25008 @@
-offers_missions
+offers_missions = true
@@ -25242 +25242 @@
-offers_missions
+offers_missions = true
@@ -25422 +25422 @@
-offers_missions
+offers_missions = true
@@ -25642 +25642 @@
-offers_missions
+offers_missions = true
@@ -25822 +25822 @@
-offers_missions
+offers_missions = true
@@ -26019 +26019 @@
-offers_missions
+offers_missions = true
@@ -26197 +26197 @@
-offers_missions
+offers_missions = true
@@ -26337 +26337 @@
-offers_missions
+offers_missions = true
@@ -26647 +26647 @@
-offers_missions
+offers_missions = true
@@ -26832 +26832 @@
-offers_missions
+offers_missions = true
@@ -26995 +26995 @@
-offers_missions
+offers_missions = true
@@ -27182 +27182 @@
-offers_missions
+offers_missions = true
@@ -27328 +27328 @@
-offers_missions
+offers_missions = true
@@ -27510 +27510 @@
-offers_missions
+offers_missions = true
@@ -27676 +27676 @@
-offers_missions
+offers_missions = true
@@ -27683 +27683 @@
-offers_missions
+offers_missions = true
@@ -27867 +27867 @@
-offers_missions
+offers_missions = true
@@ -28031 +28031 @@
-offers_missions
+offers_missions = true
@@ -28203 +28203 @@
-offers_missions
+offers_missions = true
@@ -28477 +28477 @@
-offers_missions
+offers_missions = true
@@ -28814 +28814 @@
-offers_missions
+offers_missions = true
@@ -29037 +29037 @@
-offers_missions
+offers_missions = true
@@ -29238 +29238 @@
-offers_missions
+offers_missions = true
@@ -29257 +29257 @@
-offers_missions
+offers_missions = true
@@ -29507 +29507 @@
-offers_missions
+offers_missions = true
@@ -29675 +29675 @@
-offers_missions
+offers_missions = true
@@ -29852 +29852 @@
-offers_missions
+offers_missions = true
@@ -30024 +30024 @@
-offers_missions
+offers_missions = true
@@ -30032 +30032 @@
-offers_missions
+offers_missions = true
@@ -30051 +30051 @@
-offers_missions
+offers_missions = true
@@ -30345 +30345 @@
-offers_missions
+offers_missions = true
@@ -30369 +30369 @@
-offers_missions
+offers_missions = true
@@ -30632 +30632 @@
-offers_missions
+offers_missions = true
@@ -30651 +30651 @@
-offers_missions
+offers_missions = true
@@ -30876 +30876 @@
-offers_missions
+offers_missions = true
@@ -31055 +31055 @@
-offers_missions
+offers_missions = true
@@ -31063 +31063 @@
-offers_missions
+offers_missions = true
@@ -31255 +31255 @@
-offers_missions
+offers_missions = true
@@ -31431 +31431 @@
-offers_missions
+offers_missions = true
@@ -31854 +31854 @@
-offers_missions
+offers_missions = true
@@ -31888 +31888 @@
-offers_missions
+offers_missions = true
@@ -32224 +32224 @@
-offers_missions
+offers_missions = true
@@ -32483 +32483 @@
-offers_missions
+offers_missions = true
@@ -32502 +32502 @@
-offers_missions
+offers_missions = true
@@ -32773 +32773 @@
-offers_missions
+offers_missions = true
@@ -32955 +32955 @@
-offers_missions
+offers_missions = true
@@ -33139 +33139 @@
-offers_missions
+offers_missions = true
@@ -33147 +33147 @@
-offers_missions
+offers_missions = true
@@ -33346 +33346 @@
-offers_missions
+offers_missions = true
@@ -33538 +33538 @@
-offers_missions
+offers_missions = true
@@ -33775 +33775 @@
-offers_missions
+offers_missions = true
@@ -33909 +33909 @@
-offers_missions
+offers_missions = true
@@ -34075 +34075 @@
-offers_missions
+offers_missions = true
@@ -34232 +34232 @@
-offers_missions
+offers_missions = true
@@ -34241 +34241 @@
-offers_missions
+offers_missions = true
@@ -34433 +34433 @@
-offers_missions
+offers_missions = true
@@ -34622 +34622 @@
-offers_missions
+offers_missions = true
@@ -34786 +34786 @@
-offers_missions
+offers_missions = true
@@ -35015 +35015 @@
-offers_missions
+offers_missions = true
@@ -35180 +35180 @@
-offers_missions
+offers_missions = true
@@ -35427 +35427 @@
-offers_missions
+offers_missions = true
@@ -35573 +35573 @@
-offers_missions
+offers_missions = true
@@ -35862 +35862 @@
-offers_missions
+offers_missions = true
@@ -35870 +35870 @@
-offers_missions
+offers_missions = true
@@ -35879 +35879 @@
-offers_missions
+offers_missions = true
@@ -36178 +36178 @@
-offers_missions
+offers_missions = true
@@ -36186 +36186 @@
-offers_missions
+offers_missions = true
@@ -36453 +36453 @@
-offers_missions
+offers_missions = true
@@ -36466 +36466 @@
-offers_missions
+offers_missions = true
@@ -36762 +36762 @@
-offers_missions
+offers_missions = true
@@ -36769 +36769 @@
-offers_missions
+offers_missions = true
@@ -36776 +36776 @@
-offers_missions
+offers_missions = true
@@ -37015 +37015 @@
-offers_missions
+offers_missions = true
@@ -37283 +37283 @@
-offers_missions
+offers_missions = true
@@ -37425 +37425 @@
-offers_missions
+offers_missions = true
@@ -37646 +37646 @@
-offers_missions
+offers_missions = true
@@ -37797 +37797 @@
-offers_missions
+offers_missions = true
@@ -37842 +37842 @@
-offers_missions
+offers_missions = true
@@ -38109 +38109 @@
-offers_missions
+offers_missions = true
@@ -38241 +38241 @@
-offers_missions
+offers_missions = true
@@ -38250 +38250 @@
-offers_missions
+offers_missions = true
@@ -38430 +38430 @@
-offers_missions
+offers_missions = true
@@ -38666 +38666 @@
-offers_missions
+offers_missions = true
@@ -38823 +38823 @@
-offers_missions
+offers_missions = true
@@ -38832 +38832 @@
-offers_missions
+offers_missions = true
@@ -39077 +39077 @@
-offers_missions
+offers_missions = true
@@ -39204 +39204 @@
-offers_missions
+offers_missions = true
@@ -39338 +39338 @@
-offers_missions
+offers_missions = true
@@ -39347 +39347 @@
-offers_missions
+offers_missions = true
@@ -39530 +39530 @@
-offers_missions
+offers_missions = true
@@ -39677 +39677 @@
-offers_missions
+offers_missions = true
@@ -39885 +39885 @@
-offers_missions
+offers_missions = true
@@ -40071 +40071 @@
-offers_missions
+offers_missions = true
@@ -40083 +40083 @@
-offers_missions
+offers_missions = true
@@ -40306 +40306 @@
-offers_missions
+offers_missions = true
@@ -40485 +40485 @@
-offers_missions
+offers_missions = true
@@ -40656 +40656 @@
-offers_missions
+offers_missions = true
@@ -40680 +40680 @@
-offers_missions
+offers_missions = true
@@ -40905 +40905 @@
-offers_missions
+offers_missions = true
@@ -41067 +41067 @@
-offers_missions
+offers_missions = true
@@ -41246 +41246 @@
-offers_missions
+offers_missions = true
@@ -41405 +41405 @@
-offers_missions
+offers_missions = true
@@ -41546 +41546 @@
-offers_missions
+offers_missions = true
@@ -41674 +41674 @@
-offers_missions
+offers_missions = true
@@ -41847 +41847 @@
-offers_missions
+offers_missions = true
@@ -42112 +42112 @@
-offers_missions
+offers_missions = true
@@ -42267 +42267 @@
-offers_missions
+offers_missions = true
@@ -42475 +42475 @@
-offers_missions
+offers_missions = true
@@ -42689 +42689 @@
-offers_missions
+offers_missions = true
@@ -42816 +42816 @@
-offers_missions
+offers_missions = true
@@ -42960 +42960 @@
-offers_missions
+offers_missions = true
@@ -43128 +43128 @@
-offers_missions
+offers_missions = true
@@ -43354 +43354 @@
-offers_missions
+offers_missions = true
@@ -43597 +43597 @@
-offers_missions
+offers_missions = true
@@ -43816 +43816 @@
-offers_missions
+offers_missions = true
@@ -44008 +44008 @@
-offers_missions
+offers_missions = true
```

</details>

#### `Missions/news.ini`

259 Hunks, +259 / −259 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (777 Zeilen)</summary>

```diff
@@ -3 +3 @@
-autoselect
+autoselect = true
@@ -31 +31 @@
-autoselect
+autoselect = true
@@ -137 +137 @@
-autoselect
+autoselect = true
@@ -274 +274 @@
-autoselect
+autoselect = true
@@ -344 +344 @@
-autoselect
+autoselect = true
@@ -670 +670 @@
-autoselect
+autoselect = true
@@ -827 +827 @@
-autoselect
+autoselect = true
@@ -906 +906 @@
-autoselect
+autoselect = true
@@ -1204 +1204 @@
-autoselect
+autoselect = true
@@ -1568 +1568 @@
-autoselect
+autoselect = true
@@ -1689 +1689 @@
-autoselect
+autoselect = true
@@ -1890 +1890 @@
-autoselect
+autoselect = true
@@ -2091 +2091 @@
-autoselect
+autoselect = true
@@ -2412 +2412 @@
-autoselect
+autoselect = true
@@ -2653 +2653 @@
-autoselect
+autoselect = true
@@ -2838 +2838 @@
-autoselect
+autoselect = true
@@ -2935 +2935 @@
-autoselect
+autoselect = true
@@ -3176 +3176 @@
-autoselect
+autoselect = true
@@ -3709 +3709 @@
-autoselect
+autoselect = true
@@ -3824 +3824 @@
-autoselect
+autoselect = true
@@ -4015 +4015 @@
-autoselect
+autoselect = true
@@ -4130 +4130 @@
-autoselect
+autoselect = true
@@ -4283 +4283 @@
-autoselect
+autoselect = true
@@ -4474 +4474 @@
-autoselect
+autoselect = true
@@ -4627 +4627 @@
-autoselect
+autoselect = true
@@ -4932 +4932 @@
-autoselect
+autoselect = true
@@ -4959 +4959 @@
-autoselect
+autoselect = true
@@ -5025 +5025 @@
-autoselect
+autoselect = true
@@ -5222 +5222 @@
-audio
+audio = true
@@ -5232 +5232 @@
-audio
+audio = true
@@ -5242 +5242 @@
-audio
+audio = true
@@ -5252 +5252 @@
-audio
+audio = true
@@ -5264 +5264 @@
-audio
+audio = true
@@ -5274 +5274 @@
-audio
+audio = true
@@ -5286 +5286 @@
-audio
+audio = true
@@ -5297 +5297 @@
-audio
+audio = true
@@ -5309 +5309 @@
-audio
+audio = true
@@ -5321 +5321 @@
-audio
+audio = true
@@ -5331 +5331 @@
-audio
+audio = true
@@ -5341 +5341 @@
-audio
+audio = true
@@ -5351 +5351 @@
-audio
+audio = true
@@ -5363 +5363 @@
-audio
+audio = true
@@ -5373 +5373 @@
-audio
+audio = true
@@ -5385 +5385 @@
-audio
+audio = true
@@ -5397 +5397 @@
-audio
+audio = true
@@ -5409 +5409 @@
-audio
+audio = true
@@ -5420 +5420 @@
-audio
+audio = true
@@ -5431 +5431 @@
-audio
+audio = true
@@ -5442 +5442 @@
-audio
+audio = true
@@ -5456 +5456 @@
-audio
+audio = true
@@ -5467 +5467 @@
-audio
+audio = true
@@ -5478 +5478 @@
-audio
+audio = true
@@ -5488 +5488 @@
-audio
+audio = true
@@ -5499 +5499 @@
-audio
+audio = true
@@ -5510 +5510 @@
-audio
+audio = true
@@ -5520 +5520 @@
-audio
+audio = true
@@ -5532 +5532 @@
-audio
+audio = true
@@ -5543 +5543 @@
-audio
+audio = true
@@ -5554 +5554 @@
-audio
+audio = true
@@ -5566 +5566 @@
-audio
+audio = true
@@ -5582 +5582 @@
-audio
+audio = true
@@ -5594 +5594 @@
-audio
+audio = true
@@ -5607 +5607 @@
-audio
+audio = true
@@ -5619 +5619 @@
-audio
+audio = true
@@ -5633 +5633 @@
-audio
+audio = true
@@ -5647 +5647 @@
-audio
+audio = true
@@ -5665 +5665 @@
-audio
+audio = true
@@ -5678 +5678 @@
-audio
+audio = true
@@ -5693 +5693 @@
-audio
+audio = true
@@ -5705 +5705 @@
-audio
+audio = true
@@ -5715 +5715 @@
-audio
+audio = true
@@ -5725 +5725 @@
-audio
+audio = true
@@ -5739 +5739 @@
-audio
+audio = true
@@ -5749 +5749 @@
-audio
+audio = true
@@ -5762 +5762 @@
-audio
+audio = true
@@ -5774 +5774 @@
-audio
+audio = true
@@ -5790 +5790 @@
-audio
+audio = true
@@ -5804 +5804 @@
-audio
+audio = true
@@ -5816 +5816 @@
-audio
+audio = true
@@ -5827 +5827 @@
-audio
+audio = true
@@ -5840 +5840 @@
-audio
+audio = true
@@ -5852 +5852 @@
-audio
+audio = true
@@ -5865 +5865 @@
-audio
+audio = true
@@ -5876 +5876 @@
-audio
+audio = true
@@ -5888 +5888 @@
-audio
+audio = true
@@ -5900 +5900 @@
-audio
+audio = true
@@ -5914 +5914 @@
-audio
+audio = true
@@ -5927 +5927 @@
-audio
+audio = true
@@ -5937 +5937 @@
-audio
+audio = true
@@ -5947 +5947 @@
-audio
+audio = true
@@ -5960 +5960 @@
-audio
+audio = true
@@ -5977 +5977 @@
-audio
+audio = true
@@ -5991 +5991 @@
-audio
+audio = true
@@ -6005 +6005 @@
-audio
+audio = true
@@ -6017 +6017 @@
-audio
+audio = true
@@ -6030 +6030 @@
-audio
+audio = true
@@ -6046 +6046 @@
-audio
+audio = true
@@ -6060 +6060 @@
-audio
+audio = true
@@ -6074 +6074 @@
-audio
+audio = true
@@ -6090 +6090 @@
-audio
+audio = true
@@ -6103 +6103 @@
-audio
+audio = true
@@ -6113 +6113 @@
-audio
+audio = true
@@ -6126 +6126 @@
-audio
+audio = true
@@ -6142 +6142 @@
-audio
+audio = true
@@ -6155 +6155 @@
-audio
+audio = true
@@ -6170 +6170 @@
-audio
+audio = true
@@ -6183 +6183 @@
-audio
+audio = true
@@ -6200 +6200 @@
-audio
+audio = true
@@ -6214 +6214 @@
-audio
+audio = true
@@ -6227 +6227 @@
-audio
+audio = true
@@ -6240 +6240 @@
-audio
+audio = true
@@ -6256 +6256 @@
-audio
+audio = true
@@ -6272 +6272 @@
-audio
+audio = true
@@ -6288 +6288 @@
-audio
+audio = true
@@ -6303 +6303 @@
-audio
+audio = true
@@ -6319 +6319 @@
-audio
+audio = true
@@ -6338 +6338 @@
-audio
+audio = true
@@ -6350 +6350 @@
-audio
+audio = true
@@ -6363 +6363 @@
-audio
+audio = true
@@ -6375 +6375 @@
-audio
+audio = true
@@ -6391 +6391 @@
-audio
+audio = true
@@ -6404 +6404 @@
-audio
+audio = true
@@ -6421 +6421 @@
-audio
+audio = true
@@ -6436 +6436 @@
-audio
+audio = true
@@ -6455 +6455 @@
-audio
+audio = true
@@ -6470 +6470 @@
-audio
+audio = true
@@ -6483 +6483 @@
-audio
+audio = true
@@ -6509 +6509 @@
-audio
+audio = true
@@ -6525 +6525 @@
-audio
+audio = true
@@ -6542 +6542 @@
-audio
+audio = true
@@ -6558 +6558 @@
-audio
+audio = true
@@ -6571 +6571 @@
-audio
+audio = true
@@ -6586 +6586 @@
-audio
+audio = true
@@ -6599 +6599 @@
-audio
+audio = true
@@ -6612 +6612 @@
-audio
+audio = true
@@ -6625 +6625 @@
-audio
+audio = true
@@ -6643 +6643 @@
-audio
+audio = true
@@ -6657 +6657 @@
-audio
+audio = true
@@ -6670 +6670 @@
-audio
+audio = true
@@ -6683 +6683 @@
-audio
+audio = true
@@ -6697 +6697 @@
-audio
+audio = true
@@ -6712 +6712 @@
-audio
+audio = true
@@ -6727 +6727 @@
-audio
+audio = true
@@ -6741 +6741 @@
-audio
+audio = true
@@ -6755 +6755 @@
-audio
+audio = true
@@ -6772 +6772 @@
-audio
+audio = true
@@ -6790 +6790 @@
-audio
+audio = true
@@ -6803 +6803 @@
-audio
+audio = true
@@ -6821 +6821 @@
-audio
+audio = true
@@ -6837 +6837 @@
-audio
+audio = true
@@ -6852 +6852 @@
-audio
+audio = true
@@ -6867 +6867 @@
-audio
+audio = true
@@ -6882 +6882 @@
-audio
+audio = true
@@ -6897 +6897 @@
-audio
+audio = true
@@ -6913 +6913 @@
-audio
+audio = true
@@ -6928 +6928 @@
-audio
+audio = true
@@ -6942 +6942 @@
-audio
+audio = true
@@ -6961 +6961 @@
-audio
+audio = true
@@ -6980 +6980 @@
-audio
+audio = true
@@ -7001 +7001 @@
-audio
+audio = true
@@ -7024 +7024 @@
-audio
+audio = true
@@ -7042 +7042 @@
-audio
+audio = true
@@ -7059 +7059 @@
-audio
+audio = true
@@ -7077 +7077 @@
-audio
+audio = true
@@ -7092 +7092 @@
-audio
+audio = true
@@ -7112 +7112 @@
-audio
+audio = true
@@ -7133 +7133 @@
-audio
+audio = true
@@ -7151 +7151 @@
-audio
+audio = true
@@ -7166 +7166 @@
-audio
+audio = true
@@ -7178 +7178 @@
-audio
+audio = true
@@ -7190 +7190 @@
-audio
+audio = true
@@ -7202 +7202 @@
-audio
+audio = true
@@ -7212 +7212 @@
-audio
+audio = true
@@ -7245 +7245 @@
-audio
+audio = true
@@ -7278 +7278 @@
-audio
+audio = true
@@ -7311 +7311 @@
-audio
+audio = true
@@ -7344 +7344 @@
-audio
+audio = true
@@ -7377 +7377 @@
-audio
+audio = true
@@ -7410 +7410 @@
-audio
+audio = true
@@ -7443 +7443 @@
-audio
+audio = true
@@ -7476 +7476 @@
-audio
+audio = true
@@ -7509 +7509 @@
-audio
+audio = true
@@ -7542 +7542 @@
-audio
+audio = true
@@ -7671 +7671 @@
-audio
+audio = true
@@ -7704 +7704 @@
-audio
+audio = true
@@ -7716 +7716 @@
-audio
+audio = true
@@ -7728 +7728 @@
-audio
+audio = true
@@ -7740 +7740 @@
-audio
+audio = true
@@ -7752 +7752 @@
-audio
+audio = true
@@ -7762 +7762 @@
-audio
+audio = true
@@ -7772 +7772 @@
-audio
+audio = true
@@ -7782 +7782 @@
-audio
+audio = true
@@ -7792 +7792 @@
-audio
+audio = true
@@ -7802 +7802 @@
-audio
+audio = true
@@ -7812 +7812 @@
-audio
+audio = true
@@ -7822 +7822 @@
-audio
+audio = true
@@ -7832 +7832 @@
-audio
+audio = true
@@ -7842 +7842 @@
-audio
+audio = true
@@ -7852 +7852 @@
-audio
+audio = true
@@ -7862 +7862 @@
-audio
+audio = true
@@ -7871 +7871 @@
-audio
+audio = true
@@ -7880 +7880 @@
-audio
+audio = true
@@ -7890 +7890 @@
-audio
+audio = true
@@ -7900 +7900 @@
-audio
+audio = true
@@ -7910 +7910 @@
-audio
+audio = true
@@ -7920 +7920 @@
-audio
+audio = true
@@ -7930 +7930 @@
-audio
+audio = true
@@ -7940 +7940 @@
-audio
+audio = true
@@ -7950 +7950 @@
-audio
+audio = true
@@ -7960 +7960 @@
-audio
+audio = true
@@ -7970 +7970 @@
-audio
+audio = true
@@ -7980 +7980 @@
-audio
+audio = true
@@ -7990 +7990 @@
-audio
+audio = true
@@ -8000 +8000 @@
-audio
+audio = true
@@ -8010 +8010 @@
-audio
+audio = true
@@ -8020 +8020 @@
-audio
+audio = true
@@ -8030 +8030 @@
-audio
+audio = true
@@ -8040 +8040 @@
-audio
+audio = true
@@ -8050 +8050 @@
-audio
+audio = true
@@ -8060 +8060 @@
-audio
+audio = true
@@ -8070 +8070 @@
-audio
+audio = true
@@ -8080 +8080 @@
-audio
+audio = true
@@ -8090 +8090 @@
-audio
+audio = true
@@ -8100 +8100 @@
-audio
+audio = true
@@ -8110 +8110 @@
-audio
+audio = true
@@ -8120 +8120 @@
-audio
+audio = true
@@ -8130 +8130 @@
-audio
+audio = true
@@ -8140 +8140 @@
-audio
+audio = true
@@ -8150 +8150 @@
-audio
+audio = true
@@ -8160 +8160 @@
-audio
+audio = true
@@ -8170 +8170 @@
-audio
+audio = true
@@ -8180 +8180 @@
-audio
+audio = true
@@ -8190 +8190 @@
-audio
+audio = true
@@ -8200 +8200 @@
-audio
+audio = true
@@ -8210 +8210 @@
-audio
+audio = true
@@ -8220 +8220 @@
-audio
+audio = true
@@ -8230 +8230 @@
-audio
+audio = true
@@ -8240 +8240 @@
-audio
+audio = true
@@ -8250 +8250 @@
-audio
+audio = true
@@ -8260 +8260 @@
-audio
+audio = true
@@ -8270 +8270 @@
-audio
+audio = true
@@ -8316 +8316 @@
-audio
+audio = true
@@ -8328 +8328 @@
-audio
+audio = true
@@ -8340 +8340 @@
-audio
+audio = true
@@ -8352 +8352 @@
-audio
+audio = true
@@ -8364 +8364 @@
-audio
+audio = true
@@ -8376 +8376 @@
-audio
+audio = true
@@ -8388 +8388 @@
-audio
+audio = true
@@ -8400 +8400 @@
-audio
+audio = true
@@ -8412 +8412 @@
-audio
+audio = true
@@ -8424 +8424 @@
-audio
+audio = true
@@ -8436 +8436 @@
-audio
+audio = true
@@ -8448 +8448 @@
-audio
+audio = true
@@ -8460 +8460 @@
-audio
+audio = true
@@ -8472 +8472 @@
-audio
+audio = true
@@ -8484 +8484 @@
-audio
+audio = true
@@ -8496 +8496 @@
-audio
+audio = true
@@ -8508 +8508 @@
-audio
+audio = true
@@ -8520 +8520 @@
-audio
+audio = true
```

</details>

#### `Missions/npcships.ini`

3 Hunks, +3 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Oct 21 00:00:00 2003

```diff
@@ -241 +241 @@
-npc_class = lawful, class_armored, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19
+npc_class = lawful, class_armored, d4
@@ -1249 +1249 @@
-npc_class = unlawful, class_fighter, d1, d2, d3, d4, d5, d6, d7, d8, d9
+npc_class = unlawful, class_fighter, d9
@@ -2761 +2761 @@
-npc_class = unlawful, FIGHTER, d13, d14, d15, d16, d17, d18, d19
+npc_class = unlawful, FIGHTER, d19
```

### Universe

#### `Universe/Systems/Br01/Br01.ini`

9 Hunks, +1 / −8 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Br01
@@ -2244 +2244,0 @@
-ids_info = 66170
@@ -2261 +2260,0 @@
-ids_info = 66170
@@ -2277 +2275,0 @@
-ids_info = 66170
@@ -2293 +2290,0 @@
-ids_info = 66170
@@ -2309 +2305,0 @@
-ids_info = 66170
@@ -2325 +2320,0 @@
-ids_info = 66170
@@ -2341 +2335,0 @@
-ids_info = 66170
@@ -2356 +2349,0 @@
-ids_info = 66170
```

#### `Universe/Systems/Br02/Br02.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 11 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Br02
```

#### `Universe/Systems/Br03/Br03.ini`

4 Hunks, +2 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Br03
@@ -203 +204 @@
-info_card_ids = 66145
+ids_info = 66145
@@ -3858 +3858,0 @@
-behavior = NOTHING
@@ -4201 +4200,0 @@
-ids_info = 66403
```

#### `Universe/Systems/Br04/Br04.ini`

4 Hunks, +3 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Br04
@@ -3 +4 @@
-local_faction = li_p_grp
+local_faction = br_p_grp
@@ -4930 +4931 @@
-spacedusr_maxparticles = 125
+spacedust_maxparticles = 125
@@ -5017 +5017,0 @@
-ids_info = 66405
```

#### `Universe/Systems/Br05/Br05.ini`

3 Hunks, +2 / −2 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Br05
@@ -3 +4 @@
-local_faction = li_p_grp
+local_faction = br_p_grp
@@ -667 +667,0 @@
-ids_info = 66147
```

#### `Universe/Systems/Br06/Br06.ini`

2 Hunks, +2 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 11 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Br06
@@ -3 +4 @@
-local_faction = li_p_grp
+local_faction = br_p_grp
```

#### `Universe/Systems/Bw01/Bw01.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw01
```

#### `Universe/Systems/Bw02/Bw02.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 11 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw02
```

#### `Universe/Systems/Bw03/Bw03.ini`

3 Hunks, +3 / −2 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw03
@@ -180 +181 @@
-info_ids = 66145
+ids_info = 66145
@@ -196 +197 @@
-info_ids = 66145
+ids_info = 66145
```

#### `Universe/Systems/Bw04/Bw04.ini`

4 Hunks, +4 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw04
@@ -219 +220 @@
-pacedust = leedsdust
+spacedust = leedsdust
@@ -248 +249 @@
-pacedust = leedsdust
+spacedust = leedsdust
@@ -276 +277 @@
-pacedust = leedsdust
+spacedust = leedsdust
```

#### `Universe/Systems/Bw05/Bw05.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 11 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw05
```

#### `Universe/Systems/Bw06/Bw06.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 11 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw06
```

#### `Universe/Systems/Bw07/Bw07.ini`

2 Hunks, +2 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw07
@@ -156 +157 @@
-info_ids = 66145
+ids_info = 66145
```

#### `Universe/Systems/Bw08/Bw08.ini`

3 Hunks, +1 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw08
@@ -181 +181,0 @@
-size = 20000, 0, 0
@@ -312,2 +311,0 @@
-power_modifier = 0.050000
-drag_modifier = 1.050000
```

#### `Universe/Systems/Bw09/Bw09.ini`

2 Hunks, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw09
@@ -492 +492,0 @@
-behavior = NOTHING
```

#### `Universe/Systems/Bw10/Bw10.ini`

3 Hunks, +1 / −2 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Bw10
@@ -127 +127,0 @@
-nebulae = solar\starsphere\starsphere_Bw10.cmp
@@ -530 +529,0 @@
-behavior = NOTHING
```

#### `Universe/Systems/Iw01/Iw01.ini`

6 Hunks, +0 / −6 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -271 +270,0 @@
-260800
@@ -288 +286,0 @@
-260800
@@ -304 +301,0 @@
-260800
@@ -320 +316,0 @@
-260800
@@ -336 +331,0 @@
-260800
@@ -351 +345,0 @@
-260800
```

#### `Universe/Systems/Iw05/Iw05.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1895 +1894,0 @@
-mission_type = unlawful
```

#### `Universe/Systems/Ku01/Ku01.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -152 +151,0 @@
-size = 0, 10, 0
```

#### `Universe/Systems/Ku03/Ku03.ini`

3 Hunks, +2 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1196 +1195,0 @@
-info_card = 60252
@@ -3061 +3060 @@
-spacedust_masparticles = 50
+spacedust_maxparticles = 50
@@ -3074 +3073 @@
-spacedust_masparticles = 50
+spacedust_maxparticles = 50
```

#### `Universe/Systems/Ku05/Ku05.ini`

4 Hunks, +4 / −4 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -352 +352 @@
-zone_creation_distance = False
+zone_creation_distance = 0
@@ -2884 +2884 @@
-spacedust_maxdust = 50
+spacedust_maxparticles = 50
@@ -2897 +2897 @@
-spacedust_maxdust = 100
+spacedust_maxparticles = 100
@@ -2910 +2910 @@
-spacedust_maxdust = 150
+spacedust_maxparticles = 150
```

#### `Universe/Systems/Ku07/Ku07.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -265 +265 @@
-zone_creation_distance = false
+zone_creation_distance = 0
```

#### `Universe/Systems/Li01/li01.ini`

2 Hunks, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Li01
@@ -809 +809,0 @@
-behavior = NOTHING
```

#### `Universe/Systems/Li02/Li02.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Li02
```

#### `Universe/Systems/Li03/Li03.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Li03
```

#### `Universe/Systems/Li04/Li04.ini`

3 Hunks, +1 / −2 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Li04
@@ -1053 +1053,0 @@
-ids_info = 66051
@@ -1071 +1070,0 @@
-ids_info = 66050
```

#### `Universe/Systems/Li05/Li05.ini`

1 Hunk, +1 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1,0 +2 @@
+name = Li05
```

#### `Universe/Systems/Rh01/Rh01.ini`

3 Hunks, +3 / −3 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -2087 +2087 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -2098 +2098 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -2109 +2109 @@
-zone_creation_distance = false
+zone_creation_distance = 0
```

#### `Universe/Systems/Rh02/Rh02.ini`

4 Hunks, +4 / −4 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1377 +1377 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1465 +1465 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1476 +1476 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1487 +1487 @@
-zone_creation_distance = false
+zone_creation_distance = 0
```

#### `Universe/Systems/Rh03/Rh03.ini`

5 Hunks, +5 / −5 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -1420 +1420 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1431 +1431 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1442 +1442 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1453 +1453 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1464 +1464 @@
-zone_creation_distance = false
+zone_creation_distance = 0
```

#### `Universe/Systems/Rh04/Rh04.ini`

5 Hunks, +5 / −5 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -193 +193 @@
-info_ids = 66145
+ids_info = 66145
@@ -984 +984 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -995 +995 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1006 +1006 @@
-zone_creation_distance = false
+zone_creation_distance = 0
@@ -1017 +1017 @@
-zone_creation_distance = false
+zone_creation_distance = 0
```

#### `Universe/Systems/Rh05/Rh05.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -812 +812 @@
-zone_creation_distance = false
+zone_creation_distance = 0
```

#### `Universe/Systems/St03/St03.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

```diff
@@ -5 +4,0 @@
-rpop_solar_detection = false
```

### FX

#### `FX/effects_explosion.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -431 +430,0 @@
-: = ==================================
```

#### `FX/explosions.ini`

2 Hunks, +0 / −2 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -750 +749,0 @@
-effect = gf_piratestationexplode#3
@@ -877 +875,0 @@
-effect = gf_piratestationexplode#3
```

#### `FX/fuse_br_battleship.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -79 +78,0 @@
-ONLY
```

#### `FX/fuse_ku_battleship.ini`

1 Hunk, +2 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -383,0 +384,2 @@
+
+[start_effect]
```

#### `FX/fuse_ku_gunship.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -48 +47,0 @@
-age_fire
```

#### `FX/fuse_li_dreadnought.ini`

1 Hunk, +2 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -357,0 +358,2 @@
+
+[start_effect]
```

#### `FX/fuse_or_osiris.ini`

1 Hunk, +2 / −0 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -356,0 +357,2 @@
+
+[start_effect]
```

#### `FX/fuse_suprise_solar.ini`

3 Hunks, +0 / −4 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -245 +244,0 @@
-separable
@@ -326 +324,0 @@
-LODranges = 0, 60, 150, 1000
@@ -665,2 +662,0 @@
-dmg_hp = dpeng01
-dmg_obj = ew_dmg_engine01_cap
```

### Ships

#### `Ships/loadouts.ini`

40 Hunks, +0 / −40 Zeilen · Mon Sep 01 00:00:00 2003 → Mon Oct 06 00:00:00 2003

<details><summary>Diff anzeigen (80 Zeilen)</summary>

```diff
@@ -2009 +2008,0 @@
-cargo = missile02_mark02_ammo, 20
@@ -2041 +2039,0 @@
-cargo = missile02_mark02_ammo, 20
@@ -2202 +2199,0 @@
-cargo = missile01_mark03_ammo, 20
@@ -2234 +2230,0 @@
-cargo = missile01_mark03_ammo, 20
@@ -2749 +2744,0 @@
-cargo = missile02_mark03_ammo, 20
@@ -2751 +2745,0 @@
-cargo = missile02_mark03_ammo, 20
@@ -2781 +2774,0 @@
-cargo = missile01_mark01_ammo, 5
@@ -3639 +3631,0 @@
-cargo = missile01_mark01_ammo, 4
@@ -3913 +3904,0 @@
-cargo = missile01_mark01_ammo, 4
@@ -4501 +4491,0 @@
-cargo = missile01_mark04_ammo, 10
@@ -4535 +4524,0 @@
-cargo = missile01_mark04_ammo, 10
@@ -4569 +4557,0 @@
-cargo = missile01_mark04_ammo, 10
@@ -4604 +4591,0 @@
-cargo = missile01_mark04_ammo, 8
@@ -4639 +4625,0 @@
-cargo = missile01_mark04_ammo, 8
@@ -4832 +4817,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -4868 +4852,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5104 +5087,0 @@
-cargo = missile01_mark01_ammo, 8
@@ -5228 +5210,0 @@
-cargo = missile01_mark01_ammo, 8
@@ -5266 +5247,0 @@
-cargo = missile01_mark01_ammo, 8
@@ -5345 +5325,0 @@
-cargo = missile01_mark04_ammo, 2
@@ -5588 +5567,0 @@
-cargo = missile01_mark01_rtc_ammo, 2
@@ -5620 +5598,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5655 +5632,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5690 +5666,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5725 +5700,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5760 +5734,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5795 +5768,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5830 +5802,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5866 +5837,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5904 +5874,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5942 +5911,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -5979 +5947,0 @@
-cargo = missile01_mark05_ammo, 20
@@ -7461 +7428,0 @@
-cargo = missile01_mark01_ammo, 4
@@ -7569 +7535,0 @@
-cargo = missile01_mark03_ammo, 10
@@ -7844 +7809,0 @@
-cargo = missile01_mark01_ammo, 4
@@ -8071 +8035,0 @@
-cargo = missile01_mark04_ammo, 5
@@ -8111 +8074,0 @@
-cargo = missile01_mark04_ammo, 5
@@ -8153 +8115,0 @@
-cargo = missile01_mark04_ammo, 20
@@ -9392 +9353,0 @@
-cargo = missile02_mark04_ammo, 4
@@ -9412 +9372,0 @@
-
```

</details>

#### `Ships/loadouts_special.ini`

6 Hunks, +0 / −6 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 02 00:00:00 2003

```diff
@@ -1549 +1548,0 @@
-equip = ge_bb_engine_01
@@ -1577 +1575,0 @@
-equip = ge_bb_engine_01
@@ -1606 +1603,0 @@
-equip = ge_kb_engine_01
@@ -1639 +1635,0 @@
-equip = ge_lbd_engine_01
@@ -1663 +1658,0 @@
-equip = ge_lbd_engine_01
@@ -1708 +1702,0 @@
-equip = ge_rb_engine_01
```

#### `Ships/shiparch.ini`

247 Hunks, +245 / −247 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

<details><summary>Diff anzeigen (739 Zeilen)</summary>

```diff
@@ -74 +74 @@
-separable
+separable = true
@@ -88 +88 @@
-separable
+separable = true
@@ -193 +193 @@
-separable
+separable = true
@@ -207 +207 @@
-separable
+separable = true
@@ -221 +221 @@
-separable
+separable = true
@@ -348 +348 @@
-separable
+separable = true
@@ -362 +362 @@
-separable
+separable = true
@@ -376 +376 @@
-separable
+separable = true
@@ -455 +455 @@
-separable
+separable = true
@@ -469 +469 @@
-separable
+separable = true
@@ -529 +529 @@
-separable
+separable = true
@@ -542 +542 @@
-separable
+separable = true
@@ -555 +555 @@
-separable
+separable = true
@@ -570 +570 @@
-separable
+separable = true
@@ -585 +585 @@
-separable
+separable = true
@@ -600 +600 @@
-separable
+separable = true
@@ -697 +697 @@
-separable
+separable = true
@@ -708 +708 @@
-separable
+separable = true
@@ -719 +719 @@
-separable
+separable = true
@@ -730 +730 @@
-separable
+separable = true
@@ -741 +741 @@
-separable
+separable = true
@@ -752 +752 @@
-separable
+separable = true
@@ -763 +763 @@
-separable
+separable = true
@@ -774 +774 @@
-separable
+separable = true
@@ -785 +785 @@
-separable
+separable = true
@@ -798 +798 @@
-separable
+separable = true
@@ -811 +811 @@
-separable
+separable = true
@@ -825 +825 @@
-separable
+separable = true
@@ -839 +839 @@
-separable
+separable = true
@@ -853 +853 @@
-separable
+separable = true
@@ -866 +866 @@
-separable
+separable = true
@@ -879 +879 @@
-separable
+separable = true
@@ -890 +890 @@
-separable
+separable = true
@@ -901 +901 @@
-separable
+separable = true
@@ -1044 +1044 @@
-separable
+separable = true
@@ -1133 +1133 @@
-separable
+separable = true
@@ -1147 +1147 @@
-separable
+separable = true
@@ -1161 +1161 @@
-separable
+separable = true
@@ -1264 +1264 @@
-separable
+separable = true
@@ -1278 +1278 @@
-separable
+separable = true
@@ -1338 +1338 @@
-separable
+separable = true
@@ -1351 +1351 @@
-separable
+separable = true
@@ -1364 +1364 @@
-separable
+separable = true
@@ -1377 +1377 @@
-separable
+separable = true
@@ -1390 +1390 @@
-separable
+separable = true
@@ -1403 +1403 @@
-separable
+separable = true
@@ -1413 +1412,0 @@
-------------------------------------------
@@ -1497 +1496 @@
-separable
+separable = true
@@ -1510 +1509 @@
-separable
+separable = true
@@ -1525 +1524 @@
-separable
+separable = true
@@ -1540 +1539 @@
-separable
+separable = true
@@ -1553 +1552 @@
-separable
+separable = true
@@ -1566 +1565 @@
-separable
+separable = true
@@ -1653 +1652 @@
-separable
+separable = true
@@ -1666 +1665 @@
-separable
+separable = true
@@ -1680 +1679 @@
-separable
+separable = true
@@ -1694 +1693 @@
-separable
+separable = true
@@ -1707 +1706 @@
-separable
+separable = true
@@ -1720 +1719 @@
-separable
+separable = true
@@ -1734 +1733 @@
-separable
+separable = true
@@ -1748 +1747 @@
-separable
+separable = true
@@ -1891 +1890 @@
-separable
+separable = true
@@ -1905 +1904 @@
-separable
+separable = true
@@ -2003 +2002 @@
-separable
+separable = true
@@ -2017 +2016 @@
-separable
+separable = true
@@ -2031 +2030 @@
-separable
+separable = true
@@ -2045 +2044 @@
-separable
+separable = true
@@ -2059 +2058 @@
-separable
+separable = true
@@ -2182 +2181 @@
-separable
+separable = true
@@ -2196 +2195 @@
-separable
+separable = true
@@ -2210 +2209 @@
-separable
+separable = true
@@ -2319 +2318 @@
-separable
+separable = true
@@ -2333 +2332 @@
-separable
+separable = true
@@ -2393 +2392 @@
-separable
+separable = true
@@ -2406 +2405 @@
-separable
+separable = true
@@ -2419 +2418 @@
-separable
+separable = true
@@ -2432 +2431 @@
-separable
+separable = true
@@ -2445 +2444 @@
-separable
+separable = true
@@ -2458 +2457 @@
-separable
+separable = true
@@ -2471 +2470 @@
-separable
+separable = true
@@ -2484 +2483 @@
-separable
+separable = true
@@ -2586 +2585 @@
-separable
+separable = true
@@ -2600 +2599 @@
-separable
+separable = true
@@ -2613 +2612 @@
-separable
+separable = true
@@ -2626 +2625 @@
-separable
+separable = true
@@ -2639 +2638 @@
-separable
+separable = true
@@ -2726 +2725 @@
-separable
+separable = true
@@ -2739 +2738 @@
-separable
+separable = true
@@ -2753 +2752 @@
-separable
+separable = true
@@ -2767 +2766 @@
-separable
+separable = true
@@ -2781 +2780 @@
-separable
+separable = true
@@ -2791 +2790 @@
-separable
+separable = true
@@ -2807 +2806 @@
-separable
+separable = true
@@ -2817 +2816 @@
-separable
+separable = true
@@ -2828 +2827 @@
-separable
+separable = true
@@ -2839 +2838 @@
-separable
+separable = true
@@ -2852 +2851 @@
-separable
+separable = true
@@ -2865 +2864 @@
-separable
+separable = true
@@ -2876 +2875 @@
-separable
+separable = true
@@ -3013 +3012 @@
-separable
+separable = true
@@ -3027 +3026 @@
-separable
+separable = true
@@ -3137 +3136 @@
-separable
+separable = true
@@ -3151 +3150 @@
-separable
+separable = true
@@ -3165 +3164 @@
-separable
+separable = true
@@ -3277 +3276 @@
-separable
+separable = true
@@ -3291 +3290 @@
-separable
+separable = true
@@ -3351 +3350 @@
-separable
+separable = true
@@ -3364 +3363 @@
-separable
+separable = true
@@ -3377 +3376 @@
-separable
+separable = true
@@ -3443 +3442 @@
-separable
+separable = true
@@ -3457 +3456 @@
-separable
+separable = true
@@ -3469 +3468 @@
-separable
+separable = true
@@ -3482 +3481 @@
-separable
+separable = true
@@ -3494 +3493 @@
-separable
+separable = true
@@ -3574 +3573 @@
-separable
+separable = true
@@ -3588 +3587 @@
-separable
+separable = true
@@ -3601 +3600 @@
-separable
+separable = true
@@ -3615 +3614 @@
-separable
+separable = true
@@ -3628 +3627 @@
-separable
+separable = true
@@ -3642 +3641 @@
-separable
+separable = true
@@ -3655 +3654 @@
-separable
+separable = true
@@ -3669 +3668 @@
-separable
+separable = true
@@ -3804 +3803 @@
-separable
+separable = true
@@ -3818 +3817 @@
-separable
+separable = true
@@ -3930 +3929 @@
-separable
+separable = true
@@ -3944 +3943 @@
-separable
+separable = true
@@ -3958 +3957 @@
-separable
+separable = true
@@ -3972 +3971 @@
-separable
+separable = true
@@ -4071 +4070 @@
-separable
+separable = true
@@ -4085 +4084 @@
-separable
+separable = true
@@ -4099 +4098 @@
-separable
+separable = true
@@ -4113 +4112 @@
-separable
+separable = true
@@ -4196 +4195 @@
-separable
+separable = true
@@ -4208 +4207 @@
-separable
+separable = true
@@ -4296 +4295 @@
-separable
+separable = true
@@ -4308 +4307 @@
-separable
+separable = true
@@ -4320 +4319 @@
-separable
+separable = true
@@ -4332 +4331 @@
-separable
+separable = true
@@ -4412 +4411 @@
-separable
+separable = true
@@ -4424 +4423 @@
-separable
+separable = true
@@ -4436 +4435 @@
-separable
+separable = true
@@ -4515 +4514 @@
-separable
+separable = true
@@ -4529 +4528 @@
-separable
+separable = true
@@ -4619 +4617,0 @@
-camera_angular_slerp_multiplier = 0.040000
@@ -4676 +4674 @@
-separable
+separable = true
@@ -4690 +4688 @@
-separable
+separable = true
@@ -4704 +4702 @@
-separable
+separable = true
@@ -4718 +4716 @@
-separable
+separable = true
@@ -4820 +4818 @@
-separable
+separable = true
@@ -4834 +4832 @@
-separable
+separable = true
@@ -4848 +4846 @@
-separable
+separable = true
@@ -4862 +4860 @@
-separable
+separable = true
@@ -4958 +4956 @@
-separable
+separable = true
@@ -4972 +4970 @@
-separable
+separable = true
@@ -5050 +5048 @@
-separable
+separable = true
@@ -5064 +5062 @@
-separable
+separable = true
@@ -5160 +5158 @@
-separable
+separable = true
@@ -5174 +5172 @@
-separable
+separable = true
@@ -5298 +5296 @@
-separable
+separable = true
@@ -5312 +5310 @@
-separable
+separable = true
@@ -5326 +5324 @@
-separable
+separable = true
@@ -5428 +5426 @@
-separable
+separable = true
@@ -5442 +5440 @@
-separable
+separable = true
@@ -5456 +5454 @@
-separable
+separable = true
@@ -5470 +5468 @@
-separable
+separable = true
@@ -5552 +5550 @@
-separable
+separable = true
@@ -5566 +5564 @@
-separable
+separable = true
@@ -5652 +5650 @@
-separable
+separable = true
@@ -5666 +5664 @@
-separable
+separable = true
@@ -5680 +5678 @@
-separable
+separable = true
@@ -5694 +5692 @@
-separable
+separable = true
@@ -5838 +5836 @@
-separable
+separable = true
@@ -5852 +5850 @@
-separable
+separable = true
@@ -5866 +5864 @@
-separable
+separable = true
@@ -5880 +5878 @@
-separable
+separable = true
@@ -5968 +5966 @@
-separable
+separable = true
@@ -5982 +5980 @@
-separable
+separable = true
@@ -6086 +6084 @@
-separable
+separable = true
@@ -6100 +6098 @@
-separable
+separable = true
@@ -6210 +6208 @@
-separable
+separable = true
@@ -6224 +6222 @@
-separable
+separable = true
@@ -6274 +6272 @@
-separable
+separable = true
@@ -6283 +6281 @@
-separable
+separable = true
@@ -6294 +6292 @@
-separable
+separable = true
@@ -6305 +6303 @@
-separable
+separable = true
@@ -6316 +6314 @@
-separable
+separable = true
@@ -6327 +6325 @@
-separable
+separable = true
@@ -6338 +6336 @@
-separable
+separable = true
@@ -6349 +6347 @@
-separable
+separable = true
@@ -6360 +6358 @@
-separable
+separable = true
@@ -6374 +6372 @@
-separable
+separable = true
@@ -6388 +6386 @@
-separable
+separable = true
@@ -6402 +6400 @@
-separable
+separable = true
@@ -6416 +6414 @@
-separable
+separable = true
@@ -6430 +6428 @@
-separable
+separable = true
@@ -6444 +6442 @@
-separable
+separable = true
@@ -6456 +6454 @@
-separable
+separable = true
@@ -6470 +6468 @@
-separable
+separable = true
@@ -6638 +6636 @@
-separable
+separable = true
@@ -6651 +6649 @@
-separable
+separable = true
@@ -6664 +6662 @@
-separable
+separable = true
@@ -6677 +6675 @@
-separable
+separable = true
@@ -6753 +6751 @@
-separable
+separable = true
@@ -6766 +6764 @@
-separable
+separable = true
@@ -6779 +6777 @@
-separable
+separable = true
@@ -6792 +6790 @@
-separable
+separable = true
@@ -6920 +6918 @@
-separable
+separable = true
@@ -7000 +6998 @@
-separable
+separable = true
@@ -7012 +7010 @@
-separable
+separable = true
@@ -7024 +7022 @@
-separable
+separable = true
@@ -7036 +7034 @@
-separable
+separable = true
@@ -7048 +7046 @@
-separable
+separable = true
@@ -7060 +7058 @@
-separable
+separable = true
@@ -7073 +7071 @@
-separable
+separable = true
@@ -7169 +7167 @@
-separable
+separable = true
@@ -7181 +7179 @@
-separable
+separable = true
@@ -7193 +7191 @@
-separable
+separable = true
@@ -7205 +7203 @@
-separable
+separable = true
@@ -7216 +7214 @@
-separable
+separable = true
@@ -7228 +7226 @@
-separable
+separable = true
@@ -7241 +7239 @@
-separable
+separable = true
@@ -7404 +7402 @@
-separable
+separable = true
@@ -7418 +7416 @@
-separable
+separable = true
@@ -7473 +7471 @@
-separable
+separable = true
@@ -7486 +7484 @@
-separable
+separable = true
@@ -7541 +7539 @@
-separable
+separable = true
@@ -7555 +7553 @@
-separable
+separable = true
@@ -7602 +7600 @@
-separable
+separable = true
@@ -7611 +7609 @@
-separable
+separable = true
@@ -7620 +7618 @@
-separable
+separable = true
@@ -7629 +7627 @@
-separable
+separable = true
@@ -7638 +7636 @@
-separable
+separable = true
@@ -7647 +7645 @@
-separable
+separable = true
@@ -7656 +7654 @@
-separable
+separable = true
@@ -7699 +7697 @@
-separable
+separable = true
@@ -7711 +7709 @@
-separable
+separable = true
@@ -7723 +7721 @@
-separable
+separable = true
@@ -7735 +7733 @@
-separable
+separable = true
@@ -7747 +7745 @@
-separable
+separable = true
@@ -7787 +7785 @@
-separable
+separable = true
@@ -7797 +7795 @@
-separable
+separable = true
@@ -7807 +7805 @@
-separable
+separable = true
@@ -7817 +7815 @@
-separable
+separable = true
@@ -7827 +7825 @@
-separable
+separable = true
@@ -7837 +7835 @@
-separable
+separable = true
@@ -7847 +7845 @@
-separable
+separable = true
@@ -7891 +7889 @@
-separable
+separable = true
```

</details>

### Equipment

#### `Equipment/commodities_per_faction.ini`

33 Hunks, +55 / −55 Zeilen · Mon Sep 01 00:00:00 2003 → Tue Nov 18 00:00:00 2003

<details><summary>Diff anzeigen (143 Zeilen)</summary>

```diff
@@ -53 +53 @@
-MarketGood = commodity_scrap_metal, , 0
+MarketGood = commodity_scrap_metal, 0, 0
@@ -58 +58 @@
-MarketGood = commodity_toxic_waste, , 0
+MarketGood = commodity_toxic_waste, 0, 0
@@ -104 +104 @@
-MarketGood = commodity_scrap_metal, , 0
+MarketGood = commodity_scrap_metal, 0, 0
@@ -127 +127 @@
-MarketGood = commodity_superconductors, , 0
+MarketGood = commodity_superconductors, 0, 0
@@ -159 +159 @@
-MarketGood = commodity_high_temp_alloys, , 0
+MarketGood = commodity_high_temp_alloys, 0, 0
@@ -202 +202 @@
-MarketGood = commodity_scrap_metal, , 0
+MarketGood = commodity_scrap_metal, 0, 0
@@ -217 +217 @@
-MarketGood = commodity_pharm, , 0
+MarketGood = commodity_pharm, 0, 0
@@ -226 +226 @@
-MarketGood = commodity_engine_components, , 0
+MarketGood = commodity_engine_components, 0, 0
@@ -229,14 +229,14 @@
-MarketGood = commodity_H_fuel, , 0
-MarketGood = commodity_hydrocarbons, , 0
-MarketGood = commodity_luxury_consumer_goods, , 0
-MarketGood = commodity_luxury_food, 0, 0
-MarketGood = commodity_mining_machinery, , 0
-MarketGood = commodity_niobium, , 0
-MarketGood = commodity_optronics, , 0
-MarketGood = commodity_oxygen, , 0
-MarketGood = commodity_pharm, , 0
-MarketGood = commodity_polymers, , 0
-MarketGood = commodity_scrap_metal, , 0
-MarketGood = commodity_super_alloys, , 0
-MarketGood = commodity_superconductors, , 0
-MarketGood = commodity_water, , 0
+MarketGood = commodity_H_fuel, 0, 0
+MarketGood = commodity_hydrocarbons, 0, 0
+MarketGood = commodity_luxury_consumer_goods, 0, 0
+MarketGood = commodity_luxury_food, 0, 0
+MarketGood = commodity_mining_machinery, 0, 0
+MarketGood = commodity_niobium, 0, 0
+MarketGood = commodity_optronics, 0, 0
+MarketGood = commodity_oxygen, 0, 0
+MarketGood = commodity_pharm, 0, 0
+MarketGood = commodity_polymers, 0, 0
+MarketGood = commodity_scrap_metal, 0, 0
+MarketGood = commodity_super_alloys, 0, 0
+MarketGood = commodity_superconductors, 0, 0
+MarketGood = commodity_water, 0, 0
@@ -297 +297 @@
-MarketGood = commodity_scrap_metal, , 0
+MarketGood = commodity_scrap_metal, 0, 0
@@ -307 +307 @@
-MarketGood = commodity_engine_components, , 0
+MarketGood = commodity_engine_components, 0, 0
@@ -311,3 +311,3 @@
-MarketGood = commodity_mining_machinery, , 0
-MarketGood = commodity_niobium, , 0
-MarketGood = commodity_optronics, , 0
+MarketGood = commodity_mining_machinery, 0, 0
+MarketGood = commodity_niobium, 0, 0
+MarketGood = commodity_optronics, 0, 0
@@ -317,3 +317,3 @@
-MarketGood = commodity_scrap_metal, , 0
-MarketGood = commodity_super_alloys, , 0
-MarketGood = commodity_superconductors, , 0
+MarketGood = commodity_scrap_metal, 0, 0
+MarketGood = commodity_super_alloys, 0, 0
+MarketGood = commodity_superconductors, 0, 0
@@ -370 +370 @@
-MarketGood = commodity_scrap_metal, , 0
+MarketGood = commodity_scrap_metal, 0, 0
@@ -372,2 +372,2 @@
-MarketGood = commodity_super_alloys, , 0
-MarketGood = commodity_superconductors, , 0
+MarketGood = commodity_super_alloys, 0, 0
+MarketGood = commodity_superconductors, 0, 0
@@ -401 +401 @@
-MarketGood = commodity_gold, , 0
+MarketGood = commodity_gold, 0, 0
@@ -477,2 +477,2 @@
-MarketGood = commodity_cardamine, , 0
-MarketGood = commodity_cobalt, , 0
+MarketGood = commodity_cardamine, 0, 0
+MarketGood = commodity_cobalt, 0, 0
@@ -481 +481 @@
-MarketGood = commodity_copper, , 0
+MarketGood = commodity_copper, 0, 0
@@ -484 +484 @@
-MarketGood = commodity_fertilizers, , 0
+MarketGood = commodity_fertilizers, 0, 0
@@ -489 +489 @@
-MarketGood = commodity_hydrocarbons, , 0
+MarketGood = commodity_hydrocarbons, 0, 0
@@ -492 +492 @@
-MarketGood = commodity_mining_machinery, , 0
+MarketGood = commodity_mining_machinery, 0, 0
@@ -500 +500 @@
-MarketGood = commodity_scrap_metal, , 0
+MarketGood = commodity_scrap_metal, 0, 0
@@ -506,2 +506,2 @@
-MarketGood = commodity_terraforming_gases, , 0
-MarketGood = commodity_toxic_waste, , 0
+MarketGood = commodity_terraforming_gases, 0, 0
+MarketGood = commodity_toxic_waste, 0, 0
@@ -528 +528 @@
-MarketGood = commodity_silver, , 0
+MarketGood = commodity_silver, 0, 0
@@ -552 +552 @@
-MarketGood = commodity_tradelane_parts, , 0
+MarketGood = commodity_tradelane_parts, 0, 0
@@ -575 +575 @@
-MarketGood = commodity_sidearms, , 0
+MarketGood = commodity_sidearms, 0, 0
@@ -580 +580 @@
-MarketGood = commodity_cardamine, , 0
+MarketGood = commodity_cardamine, 0, 0
@@ -582 +582 @@
-MarketGood = commodity_diamonds, , 0
+MarketGood = commodity_diamonds, 0, 0
@@ -595 +595 @@
-MarketGood = commodity_silver, , 0
+MarketGood = commodity_silver, 0, 0
@@ -667 +667 @@
-MarketGood = commodity_polymers, , 0
+MarketGood = commodity_polymers, 0, 0
@@ -712,2 +712,2 @@
-MarketGood = commodity_toxic_waste, , 0
-MarketGood = commodity_tradelane_parts, , 0
+MarketGood = commodity_toxic_waste, 0, 0
+MarketGood = commodity_tradelane_parts, 0, 0
@@ -728 +728 @@
-MarketGood = commodity_ship_hull_panels, , 0
+MarketGood = commodity_ship_hull_panels, 0, 0
@@ -760,2 +760,2 @@
-MarketGood = commodity_optical_chips, , 0
-MarketGood = commodity_optronics, , 0
+MarketGood = commodity_optical_chips, 0, 0
+MarketGood = commodity_optronics, 0, 0
```

</details>

#### `Equipment/misc_equip.ini`

4 Hunks, +0 / −4 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -515 +514,0 @@
-force_gun_ori = false
@@ -570 +568,0 @@
-force_gun_ori = false
@@ -625 +622,0 @@
-force_gun_ori = false
@@ -684 +680,0 @@
-
```

### Solar

#### `Solar/loadouts.ini`

5 Hunks, +0 / −9 Zeilen · Mon Sep 01 00:00:00 2003 → Mon Oct 06 00:00:00 2003

```diff
@@ -31 +30,0 @@
-equip = infinite_power
@@ -703 +701,0 @@
-equip = infinite_power
@@ -1128,4 +1125,0 @@
-equip = Small_station_turret, HpTurret_S1_01
-equip = Small_station_turret, HpTurret_S1_02
-equip = Small_station_turret, HpTurret_S1_03
-equip = Small_station_turret, HpTurret_S1_04
@@ -1283,2 +1276,0 @@
-equip = infinite_power
-equip = ge_s_scanner_02
@@ -7470 +7461,0 @@
-
```

#### `Solar/SolarArch.ini`

215 Hunks, +210 / −215 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

<details><summary>Diff anzeigen (640 Zeilen)</summary>

```diff
@@ -839 +839 @@
-separable
+separable = true
@@ -849 +849 @@
-separable
+separable = true
@@ -859 +859 @@
-separable
+separable = true
@@ -869 +869 @@
-separable
+separable = true
@@ -1995 +1994,0 @@
-loadout = li_dreadnought
@@ -2014 +2012,0 @@
-loadout = li_dreadnought
@@ -2445 +2442,0 @@
-ids_info = 66170
@@ -4230 +4226,0 @@
-destructible = true
@@ -4321 +4317 @@
-separable
+separable = true
@@ -4334 +4330 @@
-separable
+separable = true
@@ -4347 +4343 @@
-separable
+separable = true
@@ -4360 +4356 @@
-separable
+separable = true
@@ -4373 +4369 @@
-separable
+separable = true
@@ -4386 +4382 @@
-separable
+separable = true
@@ -4399 +4395 @@
-separable
+separable = true
@@ -4412 +4408 @@
-separable
+separable = true
@@ -4444 +4440 @@
-separable
+separable = true
@@ -4455 +4451 @@
-separable
+separable = true
@@ -4466 +4462 @@
-separable
+separable = true
@@ -4477 +4473 @@
-separable
+separable = true
@@ -4488 +4484 @@
-separable
+separable = true
@@ -4499 +4495 @@
-separable
+separable = true
@@ -4510 +4506 @@
-separable
+separable = true
@@ -4521 +4517 @@
-separable
+separable = true
@@ -4532 +4528 @@
-separable
+separable = true
@@ -4545 +4541 @@
-separable
+separable = true
@@ -4558 +4554 @@
-separable
+separable = true
@@ -4571 +4567 @@
-separable
+separable = true
@@ -4584 +4580 @@
-separable
+separable = true
@@ -4597 +4593 @@
-separable
+separable = true
@@ -4610 +4606 @@
-separable
+separable = true
@@ -4623 +4619 @@
-separable
+separable = true
@@ -4634 +4630 @@
-separable
+separable = true
@@ -4645 +4641 @@
-separable
+separable = true
@@ -4681 +4677 @@
-separable
+separable = true
@@ -4694 +4690 @@
-separable
+separable = true
@@ -4707 +4703 @@
-separable
+separable = true
@@ -4720 +4716 @@
-separable
+separable = true
@@ -4733 +4729 @@
-separable
+separable = true
@@ -4742 +4738 @@
-separable
+separable = true
@@ -4758 +4754 @@
-separable
+separable = true
@@ -4768 +4764 @@
-separable
+separable = true
@@ -4779 +4775 @@
-separable
+separable = true
@@ -4790 +4786 @@
-separable
+separable = true
@@ -4803 +4799 @@
-separable
+separable = true
@@ -4816 +4812 @@
-separable
+separable = true
@@ -4827 +4823 @@
-separable
+separable = true
@@ -4859 +4855 @@
-separable
+separable = true
@@ -4872 +4868 @@
-separable
+separable = true
@@ -4885 +4881 @@
-separable
+separable = true
@@ -4898 +4894 @@
-separable
+separable = true
@@ -4911 +4907 @@
-separable
+separable = true
@@ -4923 +4919 @@
-separable
+separable = true
@@ -4935 +4931 @@
-separable
+separable = true
@@ -4947 +4943 @@
-separable
+separable = true
@@ -4982 +4978 @@
-separable
+separable = true
@@ -4995 +4991 @@
-separable
+separable = true
@@ -5008 +5004 @@
-separable
+separable = true
@@ -5021 +5017 @@
-separable
+separable = true
@@ -5034 +5030 @@
-separable
+separable = true
@@ -5043 +5039 @@
-separable
+separable = true
@@ -5059 +5055 @@
-separable
+separable = true
@@ -5069 +5065 @@
-separable
+separable = true
@@ -5080 +5076 @@
-separable
+separable = true
@@ -5091 +5087 @@
-separable
+separable = true
@@ -5104 +5100 @@
-separable
+separable = true
@@ -5117 +5113 @@
-separable
+separable = true
@@ -5128 +5124 @@
-separable
+separable = true
@@ -5157 +5153 @@
-separable
+separable = true
@@ -5167 +5163 @@
-separable
+separable = true
@@ -5177 +5173 @@
-separable
+separable = true
@@ -5187 +5183 @@
-separable
+separable = true
@@ -5195 +5191 @@
-separable
+separable = true
@@ -5219 +5215 @@
-separable
+separable = true
@@ -5229 +5225 @@
-separable
+separable = true
@@ -5239 +5235 @@
-separable
+separable = true
@@ -5249 +5245 @@
-separable
+separable = true
@@ -5275 +5271 @@
-separable
+separable = true
@@ -5285 +5281 @@
-separable
+separable = true
@@ -5295 +5291 @@
-separable
+separable = true
@@ -5305 +5301 @@
-separable
+separable = true
@@ -5333 +5329 @@
-separable
+separable = true
@@ -5343 +5339 @@
-separable
+separable = true
@@ -5369 +5365 @@
-separable
+separable = true
@@ -5379 +5375 @@
-separable
+separable = true
@@ -5405 +5401 @@
-separable
+separable = true
@@ -5431 +5427 @@
-separable
+separable = true
@@ -5441 +5437 @@
-separable
+separable = true
@@ -5451 +5447 @@
-separable
+separable = true
@@ -5475 +5470,0 @@
-separable
@@ -5478 +5473 @@
-separable
+separable = true
@@ -5488 +5483 @@
-separable
+separable = true
@@ -5514 +5509 @@
-separable
+separable = true
@@ -5524 +5519 @@
-separable
+separable = true
@@ -5550 +5545 @@
-separable
+separable = true
@@ -5560 +5555 @@
-separable
+separable = true
@@ -5570 +5565 @@
-separable
+separable = true
@@ -5580 +5575 @@
-separable
+separable = true
@@ -5590 +5585 @@
-separable
+separable = true
@@ -5616 +5611 @@
-separable
+separable = true
@@ -5626 +5621 @@
-separable
+separable = true
@@ -5652 +5647 @@
-separable
+separable = true
@@ -5662 +5657 @@
-separable
+separable = true
@@ -5688 +5683 @@
-separable
+separable = true
@@ -5698 +5693 @@
-separable
+separable = true
@@ -5708 +5703 @@
-separable
+separable = true
@@ -5734 +5729 @@
-separable
+separable = true
@@ -5744 +5739 @@
-separable
+separable = true
@@ -5770 +5765 @@
-separable
+separable = true
@@ -5780 +5775 @@
-separable
+separable = true
@@ -5806 +5801 @@
-separable
+separable = true
@@ -5816 +5811 @@
-separable
+separable = true
@@ -5826 +5821 @@
-separable
+separable = true
@@ -5836 +5831 @@
-separable
+separable = true
@@ -5862 +5857 @@
-separable
+separable = true
@@ -5872 +5867 @@
-separable
+separable = true
@@ -5882 +5877 @@
-separable
+separable = true
@@ -5892 +5887 @@
-separable
+separable = true
@@ -5916 +5911 @@
-separable
+separable = true
@@ -5924 +5919 @@
-separable
+separable = true
@@ -5948 +5943 @@
-separable
+separable = true
@@ -5956 +5951 @@
-separable
+separable = true
@@ -5964 +5959 @@
-separable
+separable = true
@@ -5972 +5967 @@
-separable
+separable = true
@@ -5996 +5991 @@
-separable
+separable = true
@@ -6004 +5999 @@
-separable
+separable = true
@@ -6012 +6007 @@
-separable
+separable = true
@@ -6038 +6033 @@
-separable
+separable = true
@@ -6048 +6043 @@
-separable
+separable = true
@@ -6074 +6069 @@
-separable
+separable = true
@@ -6084 +6079 @@
-separable
+separable = true
@@ -6094 +6089 @@
-separable
+separable = true
@@ -6104 +6099 @@
-separable
+separable = true
@@ -6130 +6125 @@
-separable
+separable = true
@@ -6140 +6135 @@
-separable
+separable = true
@@ -6150 +6145 @@
-separable
+separable = true
@@ -6160 +6155 @@
-separable
+separable = true
@@ -6186 +6181 @@
-separable
+separable = true
@@ -6196 +6191 @@
-separable
+separable = true
@@ -6222 +6217 @@
-separable
+separable = true
@@ -6232 +6227 @@
-separable
+separable = true
@@ -6242 +6237 @@
-separable
+separable = true
@@ -6268 +6263 @@
-separable
+separable = true
@@ -6278 +6273 @@
-separable
+separable = true
@@ -6303 +6298 @@
-separable
+separable = true
@@ -6313 +6308 @@
-separable
+separable = true
@@ -6323 +6318 @@
-separable
+separable = true
@@ -6349 +6344 @@
-separable
+separable = true
@@ -6359 +6354 @@
-separable
+separable = true
@@ -6369 +6364 @@
-separable
+separable = true
@@ -6395 +6390 @@
-separable
+separable = true
@@ -6405 +6400 @@
-separable
+separable = true
@@ -6431 +6426 @@
-separable
+separable = true
@@ -6441 +6436 @@
-separable
+separable = true
@@ -6451 +6446 @@
-separable
+separable = true
@@ -6461 +6456 @@
-separable
+separable = true
@@ -6471 +6466 @@
-separable
+separable = true
@@ -6481 +6476 @@
-separable
+separable = true
@@ -6507 +6502 @@
-separable
+separable = true
@@ -6517 +6512 @@
-separable
+separable = true
@@ -6527 +6522 @@
-separable
+separable = true
@@ -6537 +6532 @@
-separable
+separable = true
@@ -6563 +6558 @@
-separable
+separable = true
@@ -6573 +6568 @@
-separable
+separable = true
@@ -6839 +6834 @@
-separable
+separable = true
@@ -6852 +6847 @@
-separable
+separable = true
@@ -6865 +6860 @@
-separable
+separable = true
@@ -6878 +6873 @@
-separable
+separable = true
@@ -6890 +6885 @@
-separable
+separable = true
@@ -6903 +6898 @@
-separable
+separable = true
@@ -6915 +6910 @@
-separable
+separable = true
@@ -6928 +6923 @@
-separable
+separable = true
@@ -6960 +6955 @@
-separable
+separable = true
@@ -6971 +6966 @@
-separable
+separable = true
@@ -6982 +6977 @@
-separable
+separable = true
@@ -6993 +6988 @@
-separable
+separable = true
@@ -7004 +6999 @@
-separable
+separable = true
@@ -7015 +7010 @@
-separable
+separable = true
@@ -7026 +7021 @@
-separable
+separable = true
@@ -7037 +7032 @@
-separable
+separable = true
@@ -7048 +7043 @@
-separable
+separable = true
@@ -7061 +7056 @@
-separable
+separable = true
@@ -7074 +7069 @@
-separable
+separable = true
@@ -7087 +7082 @@
-separable
+separable = true
@@ -7100 +7095 @@
-separable
+separable = true
@@ -7113 +7108 @@
-separable
+separable = true
@@ -7126 +7121 @@
-separable
+separable = true
@@ -7139 +7134 @@
-separable
+separable = true
@@ -7150 +7145 @@
-separable
+separable = true
@@ -7161 +7156 @@
-separable
+separable = true
@@ -7193 +7188 @@
-separable
+separable = true
@@ -7206 +7201 @@
-separable
+separable = true
@@ -7219 +7214 @@
-separable
+separable = true
@@ -7232 +7227 @@
-separable
+separable = true
@@ -7245 +7240 @@
-separable
+separable = true
@@ -7258 +7253 @@
-separable
+separable = true
@@ -7271 +7266 @@
-separable
+separable = true
@@ -7284 +7279 @@
-separable
+separable = true
@@ -7320 +7315 @@
-separable
+separable = true
@@ -7333 +7328 @@
-separable
+separable = true
@@ -7346 +7341 @@
-separable
+separable = true
@@ -7359 +7354 @@
-separable
+separable = true
@@ -7372 +7367 @@
-separable
+separable = true
@@ -7381 +7376 @@
-separable
+separable = true
@@ -7397 +7392 @@
-separable
+separable = true
@@ -7407 +7402 @@
-separable
+separable = true
@@ -7418 +7413 @@
-separable
+separable = true
@@ -7429 +7424 @@
-separable
+separable = true
@@ -7442 +7437 @@
-separable
+separable = true
@@ -7455 +7450 @@
-separable
+separable = true
@@ -7466 +7461 @@
-separable
+separable = true
@@ -7515 +7510 @@
-separable
+separable = true
@@ -7525 +7520 @@
-separable
+separable = true
@@ -7535 +7530 @@
-separable
+separable = true
@@ -7545 +7540 @@
-separable
+separable = true
```

</details>

### (Wurzelverzeichnis)

#### `PetalDB.ini`

1 Hunk, +1 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -327 +327 @@
-prop = solar_badlands_dynamic, solar\asteroids\models\badlands_dynamic.3db, solar\ast_badlands.mat
+prop = solar_badlands_dynamic, solar\asteroids\models\badlands_dynamic.3db
```

### Audio

#### `Audio/story_sounds.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -5308 +5307,0 @@
-type = voice
```

### Characters

#### `Characters/costumes.ini`

1 Hunk, +0 / −1 Zeilen · Mon Sep 01 00:00:00 2003 → Thu Oct 30 00:00:00 2003

```diff
@@ -616 +615,0 @@
-head = rh_wilham_head
```
