# TODO: Schwarze-Loch-Werte aus der HD-Edition prüfen

## Was übernommen wurde

`SDK/solar/blackhole/Bh.ini` und `Omega13.ini` stammen aus `DATA/SOLAR/BLACKHOLE/` der HD-Edition. `Bhshapes.ini` ist identisch.

Änderungen gegenüber der SDK:
- **Entfernt:** `[Sound]` (Ambient- und Flash-Töne), `[FadeChunks]` (600 Brocken, Lavaformen) und `[CloseChunks]` (100 Brocken in Nähe).
- **Nebelwolken:** `puff_shape` von `lava_wisp1–4` auf `rock_wisp1–4`.
- **Werte:** `opacity`, `spin` u. a. in gerundeter Schreibweise, sonst gleich.
- **Formen:** `solar/rings/Shapes.ini` ist ebenfalls aus der HD-Edition übernommen (1024-Pixel-Koordinaten). Die Textur `solar\rings\rings.txm` liegt in `NAP/` in der HD-Version (16,7 MB, auf der CD nur 0,7 MB), die Koordinaten passen dazu.

## Zu prüfen im Spiel

- [ ] Ob das Schwarze Loch ohne Ton und ohne Brocken korrekt wirkt, oder ob die Töne und Brocken fehlen.
- [ ] Ob die Nebelwolken mit `rock_wisp` richtig aussehen. Die Formen stammen aus der Textur `rock_wisps`.
- [ ] Ob die Ringe und Nebelwolken mit den HD-Formen und der HD-Textur richtig aussehen. Auch andere Ringsysteme nutzen `solar/rings/Shapes.ini`, die sind ebenfalls betroffen.
- [ ] Ob die Ring-Textur mit 1024 Pixeln in der Engine funktioniert (Speicher, Anzeige).

## Offen

- [ ] Die Entscheidung, ob `[Sound]`, `[FadeChunks]` und `[CloseChunks]` dauerhaft entfallen sollen.
- [ ] Die Änderungen sind noch nicht committet.
