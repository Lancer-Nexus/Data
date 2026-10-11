# TODO: Normal Maps und Cube Maps als Zusatzkarten

Ziel: Zu Texturen lassen sich zusätzliche Normal Maps und Cube Maps (Umgebungsspiegelung) per INI eintragen, für Schiffe, Stationen/Basen und Planeten/Solar-Objekte. Umfang bewusst klein: ein Satz Beispielkarten, kein Vollausbau.

## 1. Stand

| Teil | Ergebnis |
|---|---|
| Generator | `tools/make_surface_maps.py` (Pillow, numpy), reproduzierbar aus dem NAP |
| Normal Maps | 9 Karten in `NAP/Material/fx/normalmaps.txm` (je 1024 × 1024, DDS 24 Bit mit Mip-Kette, 37,8 MB): 3 Schiffe (Liberty), 3 Stationen/Basen, 3 Planeten-Detailkarten (kachelnd) |
| Cube Maps | `NAP/Material/fx/envcube_space.mat`, `envcube_sun.mat`, `envcube_nebula.mat` (je 256 px, DDS A8R8G8B8 mit Mips, 2,1 MB), Aufbau wie `envmapbasic.mat` (Knoten `CUBE`) |
| INI | `SDK/fx/SurfaceMaps.ini` mit `[Texture]`, `[NormalMap]`, `[CubeMap]` |
| Schutz | `tools/extra_maps.txt` (`build_nap.py` überschreibt oder löscht die Dateien nicht) |

Die Normal Maps sind **aus der Helligkeit der Textur abgeleitet** (Höhenkarte → Sobel), keine echte Geometrie. Sie geben Rillen, Fugen und Nieten Tiefe, falsche Schatten im Bild können als Relief erscheinen. Die Cube Maps sind **prozedural** (Sterne, Sonne, Nebel), keine Abbildung echter Systeme.

Technische Beschreibung der Dateien, der INI-Syntax und der Engine-Anbindung mit Aufgabenliste für den Client: `Client/docs/surface-maps.md`.

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

