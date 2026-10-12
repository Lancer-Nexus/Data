# Native Menü-Navigation im NAP-Client

Der Test vom 12.10.2026 verwendet den verifizierten NAP-Snapshot nach der
Newsvendor-Reparatur. Er läuft in einer Wayland-Sitzung mit dem SDL3-Treiber
`x11`. Ein temporärer Testtreiber delegiert an den unveränderten `LuaMenu`,
beobachtet Mausereignisse und den aktiven UI-Root und prüft den Prozessabschluss.
Die folgende Abfolge wurde durch echte SDL-Maus-/Tastaturereignisse ausgeführt:

1. Hauptmenü → Optionsseite über einen linken Mausklick.
2. Optionsseite → Hauptmenü über Escape.
3. Hauptmenü → reguläres Beenden über den Exit-Button, Prozess-Exit-Code **0**.

Die Ereignisse zeigen `MouseDown` und `MouseUp`, den linken Button, die passenden
Pixel-/UI-Koordinaten und `CaptureMouse=False`. Die Roots wechseln von `mainmenu`
zu `options` und zurück. Der Testtreiber bestätigt die Exit-Anforderung; seine
Zeitbegrenzung löst nicht aus. Die beiden Screenshots wurden lokal geprüft.
Es wurden weder UI-Aktionen direkt aufgerufen noch Änderungen am Client-Code
vorgenommen.

## Automatisierung

Der Controller aktiviert ausschließlich das Fenster des eigenen Testprozesses.
Er bewegt zuerst den Zeiger, sendet `mousedown`, wartet 300 ms und sendet danach
`mouseup`. Tastendrücken und Loslassen von Escape werden ebenfalls getrennt
gesendet. Vor jedem Eingriff prüft er PID und aktives Fenster. Der Testtreiber
meldet neue Roots an den Controller, der vor dem nächsten Schritt darauf wartet.

Frühere kurze oder gezielt an ein Fenster gesendete synthetische Klicks hatten
keine ausreichende Evidenz für den Seitenwechsel geliefert. Die erfolgreiche
Abfolge belegt die oben genannten Eingabepfade. Daraus folgt keine allgemeine
Aussage über alle synthetischen Klicks oder andere SDL-Backends.

## Grenzen

- New Game, Load Game und Multiplayer wurden in diesem Lauf nicht ausgeführt.
- Anmeldung, Gameplay, Cluster-Transfer sowie Normalmap-/Vulkan-Wirkung sind
  weiterhin eigenständige Prüfungen.
- Die NativeBuffer-Startdiagnose bleibt offen.
- Testtreiber, Originaldaten, Archive und Screenshots liegen nur lokal außerhalb
  von Git. Der aktive Snapshot ist kein signiertes Produktionsrelease.

[Hashes, Prüfbedingungen und Ergebnis](evidence/native-menu-navigation-20261012.json).
