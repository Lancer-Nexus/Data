# TODO: HD-Pack im Spiel prüfen

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

- [ ] Phase 5: Texturmaße (256 gegenüber 1024) und richtige Textur prüfen.
- [ ] 42 Verweise lösen sich nicht auf (`missing.md`).
