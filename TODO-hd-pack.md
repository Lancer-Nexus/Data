# TODO: HD-Pack im Spiel prüfen

Phase 2 (Daten nach `NAP/`) und Phase 3 (INIs nach `SDK/`) des Plans `PLAN-hd-pack.md` sind ausgeführt.

## Was übernommen wurde

- **Daten (`NAP/`):** 1001 Dateien überschrieben, 249 neu (`.3db`, `.cmp`, `.dfm`, `.thn`, `.mat`, `.txm`, `.ale`, `.tga` …). Liste: `tools/hd_overrides.txt`.
- **INIs (`SDK/`):** 254 geändert, 10 neu (siehe `SDK/changelog.md`, Abschnitt „HD-Pack: INIs“).
- **`exe/Freelancer.ini`:** aus `EXE/freelancer.ini` des HD-Packs übernommen, mit unseren Dateinamen.

## Zu prüfen im Spiel

- [ ] Ob das Spiel mit der HD-`Freelancer.ini` startet (Ladereihenfolge, neue Einträge).
- [ ] Ob die neuen HD-Modelle und Texturen (1024 Pixel) von der Engine der Version 1.3 geladen werden.
- [ ] Ob die HD-Spiellogik (Missionen, Gerüchte, Encounter, Fraktionsgewichte) stimmig ist: Das HD-Pack entfernt viele `faction_weight`-Einträge und ändert Skripte. Entscheidung war: HD-Werte gelten.
- [ ] Ob die zehn neuen INIs geladen werden und referenziert sind (`Storyfactions.ini`, `Territory.ini`, `Ranks.ini` u. a.). Ohne Verweis in `Freelancer.ini` oder einer anderen INI werden sie nicht verwendet.
- [ ] Ob die neun INIs, die nur in der SDK liegen, noch gebraucht werden (`Concave.ini`, `FuseLiBattleship.ini`, `HudTarget.ini`, `FactionSets.ini`, `MShipProps.ini`, `NewEncounterExample.ini` …).

## Offen

- [ ] Phase 5: Texturmaße (256 gegenüber 1024) und richtige Textur prüfen.
- [ ] 42 Verweise lösen sich nicht auf (`missing.md`).
