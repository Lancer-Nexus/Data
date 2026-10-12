# NAP-Client-Test vom 12.10.2026

Die zwölf Datenklassen aus `NAP/` wurden mit `nexus-pack` archiviert und jedes
Archiv vollständig verifiziert. Ein dreizehntes lokales Paket enthält die
Original-Textressourcen aus der vorhandenen Retail-Installation und die
Engine-Skriptüberlagerungen. Zusammen: 4.602.034.098 Bytes.
Die Originaldateien und Screenshots bleiben außerhalb von Git.

Der aktive Testsnapshot lädt ohne loses `DATA` und ohne lose Engine-Daten im
Anwendungsverzeichnis. Der Client erreicht `Finished loading game data` und
`Interface loaded`. Das Hauptmenü rendert seine Texte sichtbar und die animierte
Szene verändert sich zwischen den aufgenommenen Bildern. Ein zusätzlicher
VFS-Probelauf bestätigt die IDs 1268–1273 und die Surface-Dateien im Snapshot.
Der zeitlich begrenzte Client-Lauf endet mit Timeout-Code 124; Menü-Klickpfade,
Gameplay und Clusterbetrieb sind damit nicht abgenommen.

## Konfiguration reproduzieren

```bash
python3 tools/make_librelancer_config.py --output /pfad/zum/testspiel/librelancer.ini --skip-movies
```

`librelancer.ini` benötigt `resources.dll` ausdrücklich als erste Resource-DLL.
Die anschließende Reihenfolge aus dem SDK bleibt erhalten, weil die DLL-Position
den oberen Teil der Text-ID bestimmt. Der virtuelle Datenpfad ist `DATA`;
`data path = .` erzeugt Dot-Komponenten, die der NAP-Provider ablehnt. Ein
physisches DATA-Verzeichnis wird für diesen virtuellen Pfad nicht benötigt.

Im lokalen Test fehlte `HDEResources.dll`. Ausschließlich für diesen begrenzten
Test wurde `--omit-hde-resources` verwendet. Die ausgelassene DLL steht am Ende;
die Retail-Textindizes bleiben dadurch erhalten. Das ist kein Nachweis für die
Vollständigkeit der HD-Edition-Texte. Die Retail-DLLs müssen selbst bereitgestellt
werden; das Werkzeug verteilt oder kopiert sie nicht.

Der Client lädt `missions/faction_prop.ini` fest. Im Mission-Testpaket wurde
zusätzlich zum SDK-Namen `missions/FactionProp.ini` ein Alias angelegt. Die
Engine-Skriptüberlagerungen deklarieren `mission` und `script` als überschrieben.
Der lokale `active.json`-Snapshot ist kein signiertes Produktionsrelease.

## Offen

- `interface/neuronet/newsvendor/newsvendor.txm` erzeugt einen UTF-Ladefehler.
  Ursache und Auswirkungen auf Nachrichten-Anzeigen sind noch zu prüfen.
- Das Startprotokoll enthält eine NativeBuffer-Leak-Diagnose; sie ist noch
  nicht untersucht.
- Materialzuordnung und sichtbare Wirkung der Normalmaps/Cubemaps, feste
  Referenzszenen und Leistungswerte aus Grafikplan P0/P1 stehen noch aus.

Dateihashes, Paketgrößen, Testanpassungen und Grenzen:
[evidence/nap-client-smoke-20261012.json](evidence/nap-client-smoke-20261012.json).
