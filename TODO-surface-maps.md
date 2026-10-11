# TODO: Normal Maps und Cube Maps als Zusatzkarten

Ziel: Zu Texturen lassen sich zusätzliche Normal Maps und Cube Maps (Umgebungsspiegelung) per INI eintragen, für Schiffe, Stationen/Basen und Planeten/Solar-Objekte. Umfang bewusst klein: ein Satz Beispielkarten, kein Vollausbau.

## 1. Stand

| Teil | Ergebnis |
|---|---|
| Generator | `tools/make_surface_maps.py` (Pillow, numpy), reproduzierbar aus dem NAP |
| Normal Maps | 55 Karten in vier Bibliotheken `NAP/Material/fx/normalmaps_<ships|bases|solar|planets>.txm` (22 / 12 / 6 / 15 Karten, zusammen 77 MB). Je 1024 × 1024, **BC5** (ATI2N, nur X und Y) mit Mips bis 4 × 4. Schiffe: Liberty, Kusari, Bretonia, Piraten, Zivil, Order, Nutzschiffe. Basen: Bretonia/Pygar und Liberty. Solar: Asteroiden, Geschütztürme, Torpedo, Nomaden. Planeten: 8 kachelnde Detailkarten und 7 Oberflächenkarten |
| Cube Maps | `NAP/Material/fx/envcube_space.mat`, `envcube_sun.mat`, `envcube_nebula.mat` (je 256 px, DDS A8R8G8B8 mit Mips, 2,1 MB), Aufbau wie `envmapbasic.mat` (Knoten `CUBE`) |
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

