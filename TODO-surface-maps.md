# TODO: Normal Maps und Cube Maps als Zusatzkarten

**Ablage:** Alle Zusatzkarten und ihre INIs liegen in der eigenen Klasse `NAP/Surface/` (Pfade im virtuellen Root unverändert `fx/…`). Die INIs `SDK/fx/SurfaceMaps*.ini` gehen über `sync_inis_to_nap.py` ebenfalls dorthin. Schutz vor `build_nap.py`: `tools/extra_maps.txt`, `tools/extra_maps_auto.txt`.

Ziel: Zu Texturen lassen sich zusätzliche Normal Maps und Cube Maps (Umgebungsspiegelung) per INI eintragen, für Schiffe, Stationen/Basen und Planeten/Solar-Objekte. Umfang bewusst klein: ein Satz Beispielkarten, kein Vollausbau.

## 1. Stand

| Teil | Ergebnis |
|---|---|
| Generator | `tools/make_surface_maps.py` (Pillow, numpy), reproduzierbar aus dem NAP |
| Normal Maps | 55 Karten in vier Bibliotheken `NAP/Surface/fx/normalmaps_<ships|bases|solar|planets>.txm` (22 / 12 / 6 / 15 Karten, zusammen 77 MB). Je 1024 × 1024, **BC5** (ATI2N, nur X und Y) mit Mips bis 4 × 4. Schiffe: Liberty, Kusari, Bretonia, Piraten, Zivil, Order, Nutzschiffe. Basen: Bretonia/Pygar und Liberty. Solar: Asteroiden, Geschütztürme, Torpedo, Nomaden. Planeten: 8 kachelnde Detailkarten und 7 Oberflächenkarten |
| Cube Maps | `NAP/Surface/fx/envcube_space.mat`, `envcube_sun.mat`, `envcube_nebula.mat` (je 256 px, DDS A8R8G8B8 mit Mips, 2,1 MB), Aufbau wie `envmapbasic.mat` (Knoten `CUBE`) |
| INI | `SDK/fx/SurfaceMaps.ini` mit `[Texture]`, `[NormalMap]`, `[CubeMap]`, vom Generator erzeugt |
| Bewertung | `surface-maps-bewertung.md` (Kennzahlen je Karte, vorher/nachher) |
| Schutz | `tools/extra_maps.txt` (`build_nap.py` überschreibt oder löscht die Dateien nicht) |

Die Normal Maps sind **aus der Helligkeit der Textur abgeleitet** (Höhenkarte → Sobel), keine echte Geometrie. Sie geben Rillen, Fugen und Nieten Tiefe, falsche Schatten im Bild können als Relief erscheinen. Die Cube Maps sind **prozedural** (Sterne, Sonne, Nebel), keine Abbildung echter Systeme.

Technische Beschreibung der Dateien, der INI-Syntax und der Engine-Anbindung mit Aufgabenliste für den Client: `Client/docs/surface-maps.md`.

## 1a. Bewertung und Anpassung (2026-10-12)

`make_surface_maps.py --evaluate` bewertet jede Karte, `--tune` passt Stärke und Glättung an. Bericht: `surface-maps-bewertung.md`.

| Kennzahl | Zielbereich |
|---|---|
| Neigung der Normalen p95 | 12° bis 40° (Ziel 28°) |
| Anteil über 60° | höchstens 1 % |
| Anteil unter 1° | höchstens 85 % |
| Körnung (Pixelrauschen zu Struktur) | höchstens 1,5 |
| Naht beim Kacheln (nur Planetenkarten) | höchstens 2,5 |

**Erster Lauf** (Stärken 2,0 bis 3,5, geschätzt): 14 von 17 Karten waren zu steil, 10 hatten mehr als 1 % Pixel über 60°. Die Planetenkarten kachelten sauber (Naht 0,8 bis 1,0), die Körnung war überall niedrig (0,3 bis 0,4).

**Anpassung:** Die Stärke wird so gesetzt, dass p95 bei 28° liegt und p99 höchstens 60° erreicht. Ergebnis: Stärken zwischen 0,5 und 2,8, 6,0 nur beim glatten Asteroidengestein. Alle 16 Karten liegen danach im Zielbereich. Zwei Karten haben die Untergrenze 0,5 erreicht (`li_engine_grill`, `ku_k_panel01`), dort ist die Textur selbst sehr kontrastreich.

**Sichtprüfung der Normalen und einer Beleuchtung von links oben:**
- Rumpf-, Gitter- und Paneelkarten: Fugen, Nieten und Lamellen lesbar, nach der Anpassung dezent.
- Kachelnde Planetenkarten: gleichmäßiges Relief ohne sichtbare Naht.
- **Ausgeschieden (erste Runde):** `asteroid_belt_04` (ein Billboard mit verstreuten Brocken) und die Stadtkulisse `background_city` (Bild mit beleuchteten Fenstern, daraus entstehen Punkte als Relief). Beide sind keine Oberflächen. Ersatz: `asteroid_rock_4`.

**Zweite Runde (55 Karten, BC5):** Mit denselben Einstellungen (Ziel p95 28°, p99 höchstens 60°) kamen 39 Karten dazu: 15 Schiffe, 9 Basen, 5 Solar/Ausrüstung, 10 Planeten. Alle 55 erfüllen die Kriterien (steil höchstens 0,4 %, p95 zwischen 16° und 37°, Körnung 0,26 bis 0,41). Sieben Karten liegen an der Untergrenze der Stärke 0,5 (`li_engine_grill`, `ku_k_panel01`, `br_cap_dtl1`, `br_cap_dtl2`, `cv_g_fighter01`, `ut_liner1`, `eq_turret_wins`, sehr kontrastreiche Texturen; bei `br_cap_dtl1` und `br_cap_dtl2` bleibt p95 mit 31° und 37° über dem Ziel), drei an der Obergrenze 6,0 (`ast_rock_4` mit p95 16°, `pbody_desert01` mit 21°, `planet_ocean` mit 28°; sehr flache Texturen).

**Format:** Von 24-Bit-RGB (230 MB) auf **BC5** umgestellt (77 MB). Die Engine liest `ATI2N` als `Rgtc2` (`DDS.cs`), der Shader nutzt nur X und Y und rekonstruiert Z. Rückprüfung: Dekodiert stimmen die Kanäle bis auf einen mittleren Fehler von unter 1/255; Z-Mittel 0,98.

**Planetenoberflächen (`pbody_*`):** Das sind keine kachelnden Detailkarten, sondern die Farbkarten der Planeten selbst. Die Normal Map daraus zeigt Relief aus Helligkeitsunterschieden (Krater, Gebirge, aber auch aufgemalte Farbwechsel). Gut für Gesteins- und Eiswelten, ungeeignet für Wasser- und Gaswelten (nicht erzeugt).

**Grenzen der Bewertung:**
- Die Zielwerte sind unsere Festlegung, nicht aus der Engine oder aus Messungen im Spiel abgeleitet. Die Kennzahlen belegen nur, dass die Karten in dieser Spanne liegen.
- Die Körnungskennzahl trennt kaum (alle 0,3 bis 0,4) und hat noch keine Aussagekraft.
- Die Wirkung hängt von Tangenten, Shaderpfad und Beleuchtung in der Engine ab und ist ungeprüft.
- Aus der Helligkeit abgeleitete Karten zeigen auch Farbwechsel als Relief (z. B. aufgemalte Linien).

## 1b. Massenlauf für alle Schiffe und Basen (2026-10-12)

`tools/make_surface_maps_bulk.py` erzeugt Normal Maps für alle geeigneten Texturen aus `Material/ships`, `Models/ships` und `Models/bases`. Bericht: `surface-maps-auto-bewertung.md`, Parameter: `tools/surface_maps_auto.json`, INI: `SDK/fx/SurfaceMapsShips.ini` (49 Karten) und `SDK/fx/SurfaceMapsBases.ini` (2621 Karten).

| Schritt | Texturen |
|---|---:|
| gelesen (alle Container) | 4057 |
| Name aussortiert (Lichter, Fenster, Schilder, Kulissen, Schäden u. ä.) | 730 |
| unter 256 px | 76 |
| schon als kuratierte Karte vorhanden | 91 |
| gleicher Inhalt (MD5) | 364 |
| Name mit verschiedenem Inhalt (über die INI nicht zuordenbar) | 98 |
| kaum Relief (über 90 % unter 1°) | 10 |
| zu flach (p95 unter 8° selbst bei größter Stärke) | 18 |
| **erzeugt** | **2670** |

- **Schiffe:** 49 Karten (1024 px) in `normalmaps_ships_auto_1/2.txm`. Zusammen mit den 22 kuratierten sind es 71 Schiffskarten. Schiffstexturen liegen in `Material/ships/*.mat` (etwa 80 Texturen), nicht in den Modellen.
- **Basen:** 2621 Karten (512 px) in 23 Bibliotheken nach Gruppe: `normalmaps_bases_<generic|liberty|bretonia|kusari|rheinland|pirate|backdrops>_<n>.txm`, je höchstens 50 MB.
- **Größe:** 946 MB im NAP (BC5), nichts davon im Git. Im Git liegen nur die Skripte, die INI (370 KB) und die Parameterdatei (650 KB).
- **Auflösung:** Basen 512 px, weil die Texturen großteils KI-hochskaliert sind (`TODO-texturen-upscale.md`) und die Karten aus der Helligkeit abgeleitet werden. Mehr Auflösung brächte kein zusätzliches Detail.
- **Zuordnung:** Eine Karte gilt für eine Textur gleichen Namens. Namen, hinter denen verschiedene Bilder liegen, wurden ausgelassen (98), damit keine falsche Karte zugeordnet wird.
- **Stärke:** Median 1,5, Spanne 0,5 bis 6,0; p95 der Neigung durchgehend 15° bis 40°.

**Nicht geprüft:**
- Die Namensfilter sind eine Heuristik. Im Lauf stecken vermutlich einzelne ungeeignete Texturen (Stadtkulissen, Schilder), die nicht im Namen erkennbar sind. Eine Stichprobe von acht Karten sah plausibel aus.
- Ob die Engine Bibliotheken dieser Größe (bis 50 MB je Datei, insgesamt viele) zügig lädt, ist offen. Eine Bibliothek wird in der Engine möglicherweise erst beim Zugriff geladen; das ist nicht geprüft.
- Die Wirkung im Spiel hängt weiter von Tangenten und Shaderpfad ab.

**Lade-Profile (nur INIs, keine doppelten Daten):** Die Karten stehen in vier INIs, die die Engine je nach Bedarf liest.

| Profil | INIs | Karten | Größe der Bibliotheken |
|---|---|---:|---:|
| minimal | `SurfaceMaps.ini` | 55 (Beispielsatz: Schiffe, Basen, Solar, Planeten) | 77 MB |
| Standard | + `SurfaceMapsShips.ini`, `SurfaceMapsSolar.ini` | + 46 (Schiffstexturen) + 85 (Tore, Trade Lanes, Docks, Asteroiden, Trümmer) | + 0,2 GB |
| voll | + `SurfaceMapsBases.ini` | + 2621 (alle Basistexturen) | + 0,88 GB |

Die Engine liest nur die INIs des gewählten Profils und lädt eine Bibliothek erst, wenn eine passende Diffuse-Textur gebunden wird. Die Textur-zu-Bibliothek-Zuordnung steht in den INIs.

## 1c. Roughness und Metallic (2026-10-12)

Die Karten-Pipeline erzeugt zusätzlich zu jeder Normal Map (außer bei Planeten) eine **Roughness-** und eine **Metallic-Karte**, abgeleitet aus der Diffuse-Textur. Beide liegen in derselben Bibliothek wie die Normal Map (`rt_<name>`, `mt_<name>`).

| Teil | Wert |
|---|---|
| Format | BC4 (ATI1N), ein Kanal; die Engine liest den R-Kanal (`PBR.frag.hlsl`) und kennt `ATI1N` als `Rgtc1` |
| Größe | Schiffe 512 px, Basen und Solar 256 px (die Karten sind niederfrequent) |
| Karten | 40 kuratierte Sätze (Schiffe, Basen, Solar), 2670 automatische (49 Schiffe, 2621 Basen) |
| Speicher | Bibliotheken jetzt zusammen 1,2 GB (vorher 1,0 GB) |

**Ableitung** (`derive_rm` in `make_surface_maps.py`):
- *Roughness:* dunkle und detailreiche Bereiche rauer, helle glatte Flächen glatter. Mittel je Gruppe (Schiffe 0,45, Basen 0,60, Solar 0,55), Streuung mindestens 0,10.
- *Metallic:* wenig gesättigte Flächen mittlerer Helligkeit gelten als Metall, bunte Farbflächen und sehr dunkle Bereiche (Glas, Öffnungen) nicht. Obergrenze für das Mittel je Gruppe (Schiffe 0,35, Basen 0,25, Solar 0,30), damit Flächen im Spiel nicht zu dunkel werden (siehe unten).
- Ohne Metallic-Karte (Mittel unter 0,05; bei Basen 1346 von 2621, 3 von 49 Schiffskarten) steht in der INI `metallic = 0`, denn der Standardwert der Engine ohne Karte ist 1 (`Metallic ?? 1.0f`).

**INI:** In `[NormalMap]` kommen die optionalen Schlüssel `roughness_map`, `roughness` (Faktor), `metallic_map`, `metallic` (Faktor) hinzu. Sobald eine der Karten gesetzt ist, benutzt die Engine den PBR-Pfad (`BasicMaterial`: `pbr = (Rt || Mt || Roughness || Metallic) && lights.Enabled`).

**Ergebnis (Mittel über die Karten):**

| Gruppe | Karten | Roughness Mittel | Roughness Streuung | Metallic Mittel | Metallic Streuung |
|---|---:|---:|---:|---:|---:|
| Schiffe (automatisch) | 49 | 0,45 | 0,12 | 0,32 | 0,11 |
| Basen (automatisch) | 2621 | 0,60 | 0,10 | 0,10 | 0,11 |
| kuratiert | 40 | 0,51 | – | 0,29 | – |

**Einschränkungen (wichtig):**
- Die Karten sind **Schätzungen aus dem Bild**, keine Materialdaten. Metall und Rauheit werden aus Helligkeit, Sättigung und Detail erraten. Die Metallic-Karten sind oft nahezu einheitlich (Streuung 0,06 bis 0,11), der Unterschied ergibt sich vor allem aus dem Faktor.
- Metallische Flächen haben im PBR-Pfad **kein Diffuslicht** (`diffuseColor *= 1 - metallic`), sie spiegeln nur. Ohne Umgebungsreflexion (Image-Based Lighting, siehe `renderer-roadmap.md`) wirken sie dunkel. Deshalb sind die Mittelwerte niedrig gehalten; mit den Cube Maps `envcube_*` als `envmap_material` wird es besser, ist aber nicht geprüft.
- Der PBR-Pfad ändert die gesamte Beleuchtung des Materials, nicht nur die Karten. Ob das für Freelancer-Materialien gewünscht ist, ist eine Entscheidung der Engine-Seite.
- Planetenkarten haben weder Roughness noch Metallic.

## 1d. Tore, Trümmer und Solar-Objekte (2026-10-12)

Der Massenlauf deckt jetzt auch `Material/solar/*.mat` (nicht die Unterordner Planeten, Nebel, Ringe, Schwarzes Loch) und `Models/solar/{dockable,misc,asteroids}` ab. Ergebnis: `SDK/fx/SurfaceMapsSolar.ini` mit **85 Karten** in `normalmaps_solar_auto_1/2.txm` (85 MB).

| Gruppe | Beispiele |
|---|---|
| Sprungtore, Tunnelringe, Docks (`solar_mat_ring`, `solar_mat_dockable01…03`, `solar_mat_misc02`) | `gtdtl_128`, `stadtl1_256`, `stadtl3_256`, `stadtls2_128`, `et`, `arch_tile1`, `lib_pal_02`, `track_tube_128` |
| Trade Lanes (`solar_mat_tlr`) | `tlr_map_green`, `tlr_map_vents` |
| Weltraumstationen und Träger | `space_cap`, `space_girder`, `space_tank`, `sanctum_interior_wall01/02`, `stawin2_128` |
| Asteroiden, Gestein, Eis (`ast_*.mat`) | `rock3b`, `rock3c`, `rock3d128`, `rock_detail`, `ice_block`, `ice_carbon`, `lavastroid`, `lair_rock01/02` |
| Trümmer | `debris_detail2` |

**Anpassungen gegenüber Schiffen und Basen:**
- Das Wort `debris` im Namen wird bei Solar-Objekten zugelassen. Bei Schiffen bleibt es gesperrt, dort sind es Trümmerstücke und Schadensflächen.
- Billboard-Gürtel (`*belt*`, `*dust*`, `*_cap`: `asteroid_belt_04`, `asteroid_icebelt_04`, `debris_field`) bleiben ausgeschlossen. Das sind Bildflächen mit verstreuten Brocken, keine Oberflächen.
- Schadens- und Lichtvarianten (`tlr_damage`, `tlr_map_grndmg`, `tlr_map_ventdmg`, `stawinillum`) bleiben gesperrt.
- Asteroiden, Trümmer und Gestein (`ast_*.mat`, `Models/solar/asteroids`) sind als `rock` eingestuft: Normal Map 512 px, Roughness hoch (Mittel 0,85), **kein Metallic** (`metallic = 0`).

**Nicht abgedeckt, weil der Name nicht eindeutig ist:** Texturen gleichen Namens mit verschiedenem Inhalt in Schiffen, Basen und Solar-Objekten (z. B. `stadtls1_128`, `x_pnl_a`, `debris-1`, `lib_pal_05`). Die INI ordnet Karten über den Texturnamen zu, also werden sie weggelassen (144 Namen insgesamt). Dadurch hat der Massenlauf für Schiffe jetzt 46 statt 49 Karten. Eine Lösung wäre die Zuordnung zusätzlich nach Material (`Dt_name` plus Materialname). Das ist eine Engine-Entscheidung.

**Ergebnis gesamt:** 2751 automatische Karten (46 Schiffe, 2620 Basen, 85 Solar) in 30 Bibliotheken, 1,25 GB.

## 2. Was die Engine heute schon kann (Client, geprüft im Quelltext)

- `BasicMaterial` kennt `Nm_name` (Normal Map), `Mt_name`, `Rt_name`, `Bt_name` im `.mat`. Der PBR-Pfad wertet sie aus; der Shader liest nur die Kanäle R und G und braucht eine dritte UV-Menge/Tangenten (Original-Modelle haben diese vermutlich nicht, nicht geprüft).
- Cube Maps liegen als `.mat` mit einem Knoten `CUBE` vor und werden über `material_library` und `envmap_material` in `ships/Shiparch.ini` und `solar/SolarArch.ini` gebunden (z. B. `envmap_material = envmapbasic`). Ein neuer Cube braucht also **keine neue INI-Syntax**, nur eine Zeile dort.
- Neu ist nur: Normal Maps **per INI** statt im binären `.mat`. Dafür muss die Engine `SurfaceMaps.ini` einlesen und `Nm_name` bei der Materialauflösung ergänzen.

## 3. Aufgaben

Engine (Client, patch-only):

- [ ] `fx/SurfaceMaps.ini` einlesen; Aufnahme in die Ladeliste, z. B. neuer Schlüssel in `[Data]` der `Freelancer.ini` (nicht gesetzt, der Original-Client würde ihn ignorieren).
- [ ] `[NormalMap]`: zur Diffuse-Textur (`Dt_name`, Groß-/Kleinschreibung egal) `Nm_name` aus der Bibliothek ergänzen, `strength` als Faktor auf die Abweichung anwenden. Fehlende Karte: still ohne Normal Map.
- [ ] Tangentenraum der Karten (+Y oben, Z nach außen) gegen den Shader prüfen; bei umgekehrtem Grün das Vorzeichen in der Engine, nicht in den Daten ändern.
- [ ] `[CubeMap]` nur als Katalog. Zuweisung weiter in `Shiparch.ini`/`SolarArch.ini`.
- [ ] Sichtprüfung: Schiff (`li_fighter`) mit `envcube_space`, eine Station, ein Planet.
- [ ] Beurteilen, ob der PBR-Pfad für Freelancer-Texturen ohne `Mt_name`/`Rt_name` passt oder ein eigener Pfad nur für Normal Maps nötig ist.

Daten:

- [ ] Karten in der Engine prüfen, dann weitere Texturen aufnehmen (Liste `NORMALS` in `make_surface_maps.py`).
- [ ] Entscheiden, ob einzelne Schiffsarchetypen auf die neuen Cube Maps umgestellt werden. Das ändert `Shiparch.ini` (nicht geschehen).
- [ ] Optional DXT-Kompression der Normal Maps (DXT5, Swizzle) und 2048 für Planeten, falls Speicher zählt (jetzt 37,8 MB).

## 4. Generatoren: was sich dem Projekt beilegen lässt

Eingeordnet nach Aufwand und Ergebnis. Lizenzen und Versionen bei den Fremdwerkzeugen sind **nicht geprüft**, vor der Aufnahme ins Repo klären.

**a) Regelbasiert (liegt bereits bei)**

- `tools/make_surface_maps.py`: Normal Map aus Helligkeit, Cube Maps prozedural. Läuft offline, reproduzierbar, keine Fremdlizenz.
- Erweiterbar: Höhenkarte aus Kanälen statt Helligkeit, Stärke und Glättung je Textur, Ambient-Occlusion aus der Höhenkarte, Roughness/Metallic aus Diffuse-Farbe (PBR-Pfad).

**b) KI-Modelle für Material aus Bild (lokal, GPU)**

- Modelle, die Normal Map oder Höhenkarte aus einem Farbbild schätzen (z. B. DeepBump, ein Modell für Blender/CLI; PBRify-Normalmodelle der Hochskalierer-Familie, die wir schon nutzen). Besser als reine Helligkeit bei bemalten Texturen, brauchen aber eigene Modelldateien (nicht im Repo, wie bei der Hochskalierung unter `~/Dokumente/Freelancer-Textures/models`).
- Werkzeuge mit GUI wie Materialize oder AwesomeBump (Normal/Höhen/AO aus Bild). Gut zum Nachbessern einzelner Karten, nicht als Teil der Pipeline.

**c) Cube Maps und Panoramen per Bildmodell**

- Diffusionsmodelle mit Panorama-Unterstützung (equirektangular, anschließend in sechs Flächen umrechnen) über ComfyUI oder AUTOMATIC1111. Das Ergebnis ist ein Bild, das ein Skript in `CUBE` schreibt. Brauchbar für Nebel und Sonnen, bei Sternenfeldern prozedural meist sauberer.
- Online-Dienste für Skyboxen: nur mit Rechteklärung, hier nicht vorgesehen.

**d) LLM über LM Studio (OpenAI-kompatible API)**

LM Studio stellt unter `http://localhost:1234/v1` eine OpenAI-kompatible Schnittstelle (Chat, Embeddings) bereit; zum Zeitpunkt der Prüfung lief der Dienst nicht (`/v1/models` ohne Antwort). Ein Sprachmodell **erzeugt keine Bilder**. Sinnvoll ist es als Steuerung:

- **Parameter wählen:** Je Textur schickt ein Skript Name, Container, Größe und Statistik (mittlere Helligkeit, Kontrast) an das Modell, das `strength`, Glättung und Zuordnung als JSON zurückgibt (z. B. „Triebwerksgitter: 3,5“, „Kachel: wrap“). Mit Vision-Modell (VLM) kann zusätzlich das Bild beschrieben werden.
- **Cube-Beschreibung:** Das Modell setzt eine Beschreibung („violetter Nebel, kalte Sonne links“) in Parameter des prozeduralen Cube-Generators um (Farben, Sonnenrichtung, Sterndichte).
- **Strikt validiert:** Die Antwort wird gegen ein festes Schema geprüft, außerhalb des Bereichs gilt der Standardwert. Ohne laufenden Server arbeitet das Skript unverändert regelbasiert.
- Bilder selbst kämen aus einem Diffusionsserver (c), nicht aus LM Studio. Ein OpenAI-kompatibler Bildendpunkt (`/v1/images/generations`) wäre dann nur das Transportformat, falls ein Server ihn anbietet.

Empfehlung: a) beibehalten, die LLM-Stufe aus d) optional nutzen, b) nur bei Bedarf an bemalten Texturen.

### Umgesetzt: optionale LLM-Stufe im Generator

```bash
python3 tools/make_surface_maps.py --llm http://localhost:1234/v1 [--llm-model NAME] [--vision] \
    [--cube-desc envcube_nebula="roter Nebel, heiße Sonne links"] [--preview <Ordner>]
```

- **Ablauf:** Je Normal Map schickt das Skript Textur, Beschreibung und Bildstatistik (Helligkeit, Kontrast, Kantendichte) an `POST /chat/completions` (Temperatur 0), bei `--vision` zusätzlich ein 256-px-Bild. Antwort: `strength` (0,5 bis 6) und `smooth` (0 bis 3). Je Cube Map kommt eine Textbeschreibung, Antwort: Art (`space`, `sun`, `nebula`), Sternzahl, Sonnenrichtung und -farbe, Umgebungslicht, Nebelfarben und -anteil.
- **Absicherung:** Die Antwort wird aus Text oder Codeblock herausgelöst, jeder Wert auf feste Grenzen gekürzt, eine Nullrichtung oder ein fehlender Wert fällt auf den Standard zurück, eine nicht lesbare Antwort wird verworfen. Ohne Server läuft das Skript mit den gespeicherten Werten weiter.
- **Reproduzierbar:** Die gewählten Werte stehen in `tools/surface_maps_params.json` (mit Modellname). Spätere Läufe ohne `--llm` verwenden sie; `--no-params` setzt auf die Standardwerte im Skript zurück.
- **Geprüft:** Gegen einen lokalen Testserver (kein LM Studio): Standardlauf, Kürzen von Werten (`strength` 9 → 6, `star_count` 99999 → 8000), verworfene Antwort, Codeblock-Antwort und nicht erreichbarer Server. Mit einem echten Modell nicht ausprobiert; ob ein Modell brauchbare Werte liefert und `response_format` verträgt, ist offen.
- **Grenze:** Das Modell wählt nur Parameter. Die Pixel entstehen weiter im Skript.

