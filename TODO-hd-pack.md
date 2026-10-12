# TODO: HD-Pack im Spiel prüfen

Stand: Phasen 0 bis 6 abgeschlossen. Offen ist nur die Prüfung im Spiel.

Phase 2 (Daten nach `NAP/`) und Phase 3 (INIs nach `SDK/`) des Plans `PLAN-hd-pack.md` sind ausgeführt.

## Was übernommen wurde

- **Daten (`NAP/`):** 1001 Dateien überschrieben, 249 neu (`.3db`, `.cmp`, `.dfm`, `.thn`, `.mat`, `.txm`, `.ale`, `.tga` …). Liste: `tools/hd_overrides.txt`.
- **INIs (`SDK/`):** 254 geändert, 10 neu (siehe `SDK/changelog.md`, Abschnitt „HD-Pack: INIs“).
- **`exe/Freelancer.ini`:** Der Abgleich mit der HD-Datei ergibt keine inhaltlichen Unterschiede (96 Einträge im Abschnitt `[Data]`, gleiche Reihenfolge). Alle 95 INI-Pfade existieren exakt.

## Zu prüfen im Spiel

- [ ] Ob das Spiel mit der HD-`Freelancer.ini` startet (Ladereihenfolge, neue Einträge).
- [ ] Ob die neuen HD-Modelle und Texturen (1024 Pixel) von der Engine der Version 1.3 geladen werden.
- [ ] Ob die HD-Spiellogik (Missionen, Gerüchte, Encounter, Fraktionsgewichte) stimmig ist: Das HD-Pack entfernt viele `faction_weight`-Einträge und ändert Skripte. Entscheidung war: HD-Werte gelten.
- [ ] Die zehn neuen INIs: Vier gehören zu Plugin-DLLs des HD-Packs, die in `EXE/` liegen und über `EXE/dacom.ini` geladen werden (`storyfactions.dll`, `Territory.dll`, `ranks.dll`, `HudShift.dll`). Ohne diese DLLs (nicht im Umfang, es wurden nur `DATA/` und die `Freelancer.ini` übernommen) sind `Storyfactions.ini`, `Territory.ini`, `Ranks.ini` und `HudShift.ini` wirkungslos. `LoadoutsRegen.ini`, `EffectsExplosionNew.ini` und `M13OpenspNormal/Pirate.ini` werden von keiner INI und keiner Datei im HD-Pack referenziert. Die Plugins sind untersucht, der Quellcode liegt als Referenz in `reference/freelancer-plugins/`, die technischen Informationen und Hinweise zur Portierung stehen in `TODO-plugins.md`. Entscheidung offen: Funktionen im neuen Quellcode umsetzen oder die INIs ungenutzt lassen.
- [ ] Ob die neun INIs, die nur in der SDK liegen, noch gebraucht werden (`Concave.ini`, `FuseLiBattleship.ini`, `HudTarget.ini`, `FactionSets.ini`, `MShipProps.ini`, `NewEncounterExample.ini` …).

## Offen

- [x] Phase 5 (Texturmaße und Texturen) ist geprüft, Bericht in `textur-pruefung.md`, Werkzeuge `tools/utf_textures.py` und `tools/check_textures.py`:
  - 394 Texturen in 112 Bibliotheken. 302 haben eine andere Größe als im CD-Original (vor allem 256 → 2048: 106, 128 → 512: 102, 64 → 256: 45, 256 → 1024: 33).
  - 81 Formen (`[Shape]` mit `x`, `y`, `w`, `h`) geprüft: keine liegt außerhalb ihrer Textur, keine deckt nur die Hälfte ab. Die INIs passen also zu den vorhandenen Texturen.
  - Alle 825 Texturnamen in Materialien lösen sich auf (Bibliotheken, eingebettete Texturen, `.tga`).
  - Offen: `solar/asteroids/roids.txm` und `interface/hud/hudtarget.txm` fehlen (siehe `missing.md`), deshalb sind die Formen in `solar/asteroids/Shapes.ini` und `interface/hud/HudTarget.ini` ohne Textur.
- [ ] Im Spiel prüfen, ob die Engine 2048×2048-Texturen (DXT5) verträgt, besonders bei Planeten.
- [x] Verweise geprüft (`tools/check_refs.py`): 32 Ziele fehlen wirklich, 10 Verweise ohne Ordner finden ihre Datei (`missing.md`).
