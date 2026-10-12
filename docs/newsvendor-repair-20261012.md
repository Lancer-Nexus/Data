# Reparatur der Newsvendor-Texturbibliothek

Die lokale HD-Datei `NAP/Material/interface/neuronet/newsvendor/newsvendor.txm`
war auf exakt 40 MiB abgeschnitten. 40 UTF-Blätter verwiesen auf Bytes hinter
dem Dateiende. Das verursachte beim Client-Start einen UTF-Ladefehler.

Die vollständige HD-Datei stammt aus dem festgelegten Commit
`7c6186efcb408207beafed7363650308abc34637` des
[HD-Repositories](https://github.com/FLHDE/freelancer-hd-edition/blob/7c6186efcb408207beafed7363650308abc34637/DATA/INTERFACE/NEURONET/NEWSVENDOR/newsvendor.txm).
Sie enthält 82.325.060 Bytes. Git-Blob-ID und Dateigröße wurden geprüft;
die alte lokale Datei ist bytegenau ihr Anfang. Damit bleiben die HD-Texturen
bei der Reparatur erhalten. Die alte Datei wurde lokal gesichert. Originale
und Paketarchive werden nicht in Git übernommen.

## Schutz vor unvollständiger Übernahme

- `utf_write.load` lehnt abgeschnittene Blätter, ungültige Namens-/Baumbereiche
  sowie zyklische oder mehrfach referenzierte Knoten ab. Die belegte Länge des
  Namensblocks wird geprüft, nicht seine reservierte Kapazität. Gültige UTFs
  mit Namen vor dem Baum bleiben kompatibel.
- Der HD-Importer prüft UTF-Quelldateien vor jeder Übernahme. Ein Fehler bei
  einer Quelle verhindert das Überschreiben der vorhandenen Dateien.
- Kopien und die HD-Ausnahmeliste werden erst nach vollständigem Schreiben
  atomar pro Datei ausgetauscht. Exportfehler von Git oder tar werden gemeldet,
  bevor der Export als aktuell markiert wird. Der gesamte Import ist weiterhin
  keine Transaktion über mehrere Dateien.

## Nachweise und Grenzen

Alle 3.327 Dateien mit UTF-Signatur im lokalen NAP-Quellbestand bestehen die
Prüfung ihrer Knoten- und Datenbereiche. Dies ist kein vollständiger
Texturdecoder- oder Gameplay-Test. Retail-ALEs mit Namen vor dem Baum und die
reparierte TXM bestehen zusätzlich den Lade-/Speicher-Rundlauf.

Das Material-Archiv wurde neu gebaut und seine 263 Einträge vollständig
verifiziert. Ein Probelauf mit dem echten Client-UTF-Loader liest alle 79
Newsvendor-Texturen aus dem aktiven Archiv. Der erneute Client-Lauf ohne loses DATA erreicht `Finished loading
game data` und `Interface loaded`. Der vorherige Newsvendor-Ladefehler tritt
nicht mehr auf. Der Lauf wurde zeitlich begrenzt beendet. Die Menü-Klicknavigation
und die NativeBuffer-Startdiagnose bleiben offen.

[Hashes und Messbefunde](evidence/newsvendor-repair-20261012.json).
