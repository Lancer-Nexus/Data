# Referenz: Freelancer-Plugins (Quellcode)

Quellcode der Client-Plugins aus dem HD-Pack, als Referenz für die Portierung in den neuen Quellcode. **Nur Referenz, nichts davon wird gebaut oder geladen.** Die kompilierten DLLs sind nicht enthalten.

## adoxa/ (Jason Hood)

| | |
|---|---|
| Autor | Jason Hood (adoxa) |
| Quelle | `https://adoxa.altervista.org/freelancer/plugins.html`, Archive über `dlp.php?f=<name>` |
| Abgerufen | 2026-10-11 (das Zertifikat der Seite war abgelaufen, die Archive wurden ohne Zertifikatsprüfung geladen) |
| Lizenz | Laut Seite: „These plugins may be freely used by any mod.“ Eine formale Lizenzdatei gibt es nicht. |
| Inhalt | Quellen, `makefile`, `.rc`, `.def`, Beispiel-INI und Readme je Plugin. Keine DLLs. |

| Ordner | Plugin | Version | Sprache | Zweck |
|---|---|---:|---|---|
| `storyfactions/` | Story Factions | 1.01 | C++ | Fraktionen, die in der Reputationsliste fehlen |
| `territory/` | Territory | 1.03 | C++ | Systemeintrittsmeldung, Häuser auf der Nav-Map |
| `ranks/` | Ranks | 1.00 | C++ | Rangnamen für das Level |
| `hudshift/` | HUD Shift | 2.12.1 | C++ | HUD-Elemente verschieben (Breitbild) |
| `zone/` | Zone | 1.20 | C++ | Meldung beim Betreten/Verlassen benannter Zonen |
| `wheelscroll/` | Wheel Scroll | 1.12 | C++ | Mausrad in Fenstern |
| `mprep/` | MP Rep | 1.03 | C++ | politische Zonen/Patrouillen im Multiplayer |
| `turretzoom/` | Turret Zoom | 1.41 | C | Kamera der Turmansicht per Mausrad |
| `hail/` | Hail | 1.01 | C | Taste für Hail |
| `hudless/` | HUDless | 1.02 | C | HUD per Taste ausblenden |
| `mp3codec/` | MP3 Codec Fix | 1.12 | C | Fraunhofer-MP3-Codec finden |
| `numeric/` | Numeric Damage | 1.00 | C/NASM | Trefferpunkte numerisch anzeigen |
| `console/` | Console | 1.24 | C++ | Konsole im Einzelspielermodus |

Technische Details und Hinweise zur Portierung: `TODO-plugins.md` im Wurzelverzeichnis.

## github/ (Quellcode aus GitHub-Repos)

Jedes Plugin ist ein eigenes Repo mit eigener Lizenz. Die Lizenzdatei liegt im jeweiligen Ordner. Der Code steht **nicht** unter der Lizenz dieses Repos.

| Ordner | Repo | Stand | Lizenz | Zweck |
|---|---|---|---|---|
| `flplusplus/` | `github.com/FLHDE/flplusplus` | e7a8593 (2026-07-24) | BSD-3-Clause | Fehlerkorrekturen und Erweiterungen |
| `FLSharp/` | `github.com/BC46/FLSharp` | 0575fc3 (2026-09-21) | MIT | Hook-basierte Korrekturen und Verbesserungen |
| `MultiIntro-Updated/` | `github.com/FLHDE/MultiIntro-Updated` | dc9333e (2023-05-19) | GPL-3.0 | mehr als drei Intro-Bildschirme |
| `DynamicTargetScreen/` | `github.com/FLHDE/DynamicTargetScreen` | 13003d9 (2025-09-24) | MIT | dynamischer Zielbildschirm |
| `cyrillic_chat/` | `github.com/FLHDE/cyrillic_chat` | b73d6a4 (2026-07-15) | MIT | kyrillischer Chat (im Pack deaktiviert) |
| `fl-lighting-bug-fix/` | `github.com/FLHDE/fl-lighting-bug-fix` | 2cb3ace (2025-11-11) | MIT | Beleuchtungsfehler (im Pack deaktiviert) |
| `FLHook/` | `github.com/TheStarport/FLHook` | a7b177e (2026-07-17) | GPL-3.0 | Server-Erweiterung (Hook-Framework) |
| `DelayDisplay/` | `github.com/FLHDE/DelayDisplay` | 938f068 (2026-05-05) | **keine** | Abklingzeit der Waffen in der Kontaktliste |

Hinweis: `MultiIntro-Updated` und `FLHook` stehen unter **GPL-3.0**. Wer Code daraus übernimmt, muss die GPL beachten.

## adoxa/jflp/

| Datei | Herkunft |
|---|---|
| `jflp.c`, `jflp.rc` | Quellcode von JFLP.DLL v1.27, `https://adoxa.altervista.org/freelancer/dl.php?f=jflpsrc` |
| `jflpmod.c` | Quelle des Werkzeugs `jflpmod.exe` aus dem HD-Pack (`JFLP/`) |
| `jflp_readme.txt` | `JFLP/jflp.txt` aus dem HD-Pack |

## Hinweis zu DelayDisplay (keine Lizenz)

`github/DelayDisplay/` ist eine **Dekompilation** des Plugins von M0tah. Dessen Quellcode wurde nie veröffentlicht, das Repo enthält keine Lizenzdatei. Die Rechte liegen daher beim ursprünglichen Autor und beim Autor der Rekonstruktion (FLHDE). Der Code liegt hier ausschließlich als technische Referenz. **Vor einer Weitergabe oder Übernahme in den neuen Quellcode ist die Lizenz zu klären.**

Eine Variante mit ausdrücklicher Lizenz gibt es in `github.com/TheStarport/FLUF` (`modules/delay_display`, AGPL-3.0). Sie ist hier nicht kopiert.

## Nicht kopiert

| Plugin | Grund |
|---|---|
| VersionText | Das in der README des HD-Packs verlinkte Repo existiert nicht (404). |
