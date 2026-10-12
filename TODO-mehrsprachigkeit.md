# Mehrsprachige Texte und Sounds in NAP

Dieser Plan umfasst den Datenimport, die NAP-Ablage und die Zusammenarbeit
mit dem Client. Client-Ladepfad und Laufzeitprüfungen stehen in
[`Client/docs/data-client-todo.md`](../Client/docs/data-client-todo.md).
Originaldateien und daraus extrahierte Inhalte bleiben lokale Testeingaben;
keine Spieldateien werden hier eingecheckt.

## Ressourcen-DLLs als NAP-JSON

- [ ] Lokal bereitgestellte `InfoCards.dll`, `MiscText.dll` und
  `NameResources.dll` mit einem reproduzierbaren Offline-Konverter auslesen.
  Die Dateien sind aktuell nicht in `Data/SDK` vorhanden.
- [ ] Ein versioniertes UTF-8-JSON-Schema für Stringtabellen und Infocards
  festlegen. Numerische IDs, Ressourcentyp, Sprache/Region und RDL-Markup der
  Infocards erhalten; keine Texte anhand ihres Inhalts deduplizieren.
- [ ] DLL-Quellreihenfolge aus `Freelancer.ini` im Ressourcenmanifest erhalten,
  da der Client daraus zusammengesetzte IDs bildet. Sprachspezifische Daten
  getrennt ablegen und einen expliziten Standarddatensatz vorsehen.
- [ ] JSON-Ressourcen in den NAP-Generator integrieren. Der Build muss fehlende
  Quellen, doppelte IDs, ungültige UTF-8-/JSON-Daten und unvollständige
  Sprachsätze melden; die ursprünglichen DLLs nicht als Laufzeitabhängigkeit
  voraussetzen.
- [ ] Konvertierte Einträge gegen den bestehenden Client-DLL-Parser abgleichen:
  IDs, Textbytes nach UTF-16-Decodierung, Ressourcentyp und RDL-Markup müssen
  übereinstimmen. Test-DLLs und synthetische Fixtures verwenden, keine
  Originalressourcen in Git ablegen.

## Sprachvarianten für Audio

- [ ] BCP-47-Sprach-/Regionskennungen und eine feste Fallback-Reihenfolge
  vereinbaren: `Sprache-Region → Sprache → Standard`.
- [ ] Sprachabhängige Dialog- und Sprachaufnahmen als Varianten in NAP
  organisieren. Gemeinsame, sprachneutrale SFX und Musik nicht unnötig pro
  Sprache duplizieren; lokalisierte Musik bleibt bei Bedarf möglich.
- [ ] Verfügbare Sprachen, fehlende Varianten und den verwendeten Fallback im
  Datenmanifest beziehungsweise in einem Prüfbericht ausweisen.
- [ ] Den Generator mit synthetischen Audiofixtures für mindestens zwei
  Sprachen prüfen. Pfadzuordnung und Fallback müssen stimmen; Audio bleibt in
  einem vom Client unterstützten Format und wird durch die vorhandene
  Audio-Pipeline validiert.

## Abnahme

- [ ] Zwei Sprachsätze sind aus denselben Quellressourcen reproduzierbar
  konvertiert und in NAP auffindbar.
- [ ] Der Client kann Texte und lokalisierte Dialog-/Sprachaufnahmen pro
  Sprache laden, auf Standardressourcen zurückfallen und fehlende IDs oder
  Varianten nachvollziehbar melden.
- [ ] Ein NAP-only-Clientstart ohne lose `DATA` und ohne Laufzeitabhängigkeit
  von den drei Original-DLLs zeigt Hauptmenütexte in zwei Sprachen; ein
  lokalisierter Sound wird jeweils abgespielt.
