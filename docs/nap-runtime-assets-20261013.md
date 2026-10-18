# NAP Runtime-Vorlagen und Ressourcen-DLLs, 13.10.2026

Der NAP-Clientlauf lud Daten und Oberfläche, konnte einen neuen Einzelspieler
aber zunächst nicht starten: `newplayer.fl` fehlte im virtuellen Dateisystem.
Zusätzlich braucht `Freelancer.ini` sieben Standard-Resource-DLLs und in der
HD-Edition eine achte DLL namens `HDEResources.dll`.

`tools/import_nap_runtime.py` importiert diese Dateien nach `NAP/Runtime/`.
Für jede Datei wird zuerst `--hd-install-root/EXE` geprüft, danach
`--cd-install-root/EXE`. Beide Charaktervorlagen und die sieben Retail-DLLs
sind erforderlich; `HDEResources.dll` wird importiert, wenn sie im HD-Pfad
vorhanden ist. Alle erforderlichen Quellen werden geprüft, bevor das Werkzeug
atomar schreibt. `tools/runtime_assets.txt` schützt sie vor dem Entfernen beim
CD-Neuaufbau. Binärdateien bleiben per `.gitignore` außerhalb des Git-Repos.

## Importquellen

Die lokal verfügbare CD/Retail-Installation liegt unter
`/home/masterbee/Dokumente/FL/EXE/`. Sie lieferte beide `.fl`-Vorlagen und die
sieben Standard-DLLs. Das HD-Repository wurde für diesen Import auf
`7c6186efcb408207beafed7363650308abc34637` geprüft; darin liegt
`EXE/hderesources.dll`, die keine Retail/CD-Entsprechung hat. Das Repo enthält
zusätzlich anders benannte `*_tsr.dll`-Varianten. Sie werden nicht automatisch
anstelle der Standardnamen aus `Freelancer.ini` eingesetzt.

Der lokale Import wurde so ausgeführt:

```bash
python3 tools/import_nap_runtime.py \
  --hd-install-root /tmp/lancer-hd-repo-audit \
  --cd-install-root /home/masterbee/Dokumente/FL
```

Damit kamen `hderesources.dll` aus dem HD-Repo und die fehlenden Standarddateien
aus der CD-Installation. Ein echter installierter HD-Ordner wurde nicht
gefunden; der Importer unterstützt ihn als höher priorisierte Quelle.

| Datei | Quelle | Bytes | SHA-256 |
|---|---|---:|---|
| `newplayer.fl` | CD | 11672 | `3a35a25e4d3ab40b9875b36e7758d0f1f518d63fdcacd7ff3056c9d3e0c21e6d` |
| `mpnewcharacter.fl` | CD | 2311 | `ac6be33d53df2d1377869e367c996751b0f3c397c7e9cc943ddeda0db8e8d619` |
| `resources.dll` | CD | 750148 | `1f96be6eeac18e822bca0cbf29c8ff7999efbb8eb42614823c6397516e4e4a9b` |
| `infocards.dll` | CD | 913408 | `d0a61bd6e5f73b6c1d4e0dd7af5228e8e0ac6386f879d940461747c569809fb4` |
| `misctext.dll` | CD | 2323012 | `dc02c5871367c1c84a1c1308e49432b9a5aa7da09244095af0d5b8568f8d9107` |
| `nameresources.dll` | CD | 307784 | `328a52467db7e4aec26a3db145fd7f875d6927d5ba2ac9e6118391923e42da41` |
| `equipresources.dll` | CD | 787016 | `a99f28e11fb39def1551432177ee56c0bc6ec2d222423fc2067dd1f053a490f9` |
| `offerbriberesources.dll` | CD | 139852 | `c6a1dd8f1f54287c91394e909e22403baba9ab0a626bf3956e35a950a2632a00` |
| `misctextinfo2.dll` | CD | 356352 | `259eda2ff9ade3b5518d534ada22b6f8ea50630a284066f50dec3218450118bd` |
| `hderesources.dll` | HD-Repo | 23040 | `bc438c775f9d1bf970eb4702f5acd0c321090a82679779d5d63b6de58bc97ec4` |

## Client-Lauf

Das isolierte Debug-Testprofil mit aktivierten Normalmap-Optionen enthielt zehn
Runtime-Einträge im NAP-Archiv. `nexus-pack verify` bestätigte alle Einträge;
danach meldete der Client `Finished loading game data` und `Interface loaded`.
Beim Szenenstart wurden zwei unabhängige Clientfehler behoben: Der OpenGL-
Backend-Samplerzustand bekam dieselben `LinearRepeat`-Defaults wie die
öffentliche Sampler-Verwaltung; `Engine.OnUpdate` behandelt nun Objekte ohne
`ShipPhysicsComponent` sicher. Danach lief der Client mit `--new-game` über
60 Sekunden, meldete `Client: Spawning self`, mehrere `Client: Spawned`-Objekte
und `Found thorn mainObject`. Der Lauf wurde anschließend manuell beendet.

Damit sind NAP-Daten, Ressourcen, UI und der Szenenstart nachgewiesen. Die
damals protokollierten Nomad-Materialwarnungen ließen sich im folgenden
frischen Build mit verifiziertem aktivem Snapshot nicht reproduzieren; der
spätere Loglauf enthält keinen DcDtBtOcOtTwo-Materialfehler. Der frühere
Rohlog ist nicht erhalten, daher bleibt die Ursache ungeklärt. Eine sichtbare
Normalmap-Wirkung wurde damit noch nicht abgenommen.

## Wiederholter NAP-Paketlauf

Am 13.10.2026 wurde ein frischer BuildEngine mit Version
03bfd87-git (20261013) über einen vollständig aktiven NAP-Snapshot gegen
eine Testinstallation ohne loses DATA gestartet. Die lokalen Pakete
core.nap (8.368 Einträge aus Retail DATA), surface.nap (42 Einträge
aus Data/NAP/Surface) und runtime-exe.nap (10 Einträge aus
Data/NAP/Runtime unter dem virtuellen Präfix EXE/) wurden verifiziert;
der Snapshot prüft außerdem Größe und SHA-256. Das EXE-Präfix ist nötig,
weil der Client Ressourcen-DLLs und Charaktervorlagen unter EXE/... öffnet.
EXE/freelancer.ini, dacom.ini und dacomsrv.ini blieben in der Testinstallation,
ein DATA-Ordner war nicht vorhanden.

Der Client erreichte Daten- und UI-Load, FP7_system, mehrere erfolgreiche
THN-Hauptobjekt-Auflösungen und lief 79 Sekunden bis zum Übergang in die
Basis. Das Log hat 102 Warnungen, keine Error-Zeile und keinen
DcDtBtOcOtTwo-Materialfehler. Ein zweiter Lauf mit ausgeschalteten
Surface-Normalmaps betrat ebenfalls das System. Screenshots und Rohlog liegen
nur lokal unter /tmp/lancer-renderer-nap-20261013/evidence/ und
/tmp/lancer-renderer-nap-20261013/state/; sie enthalten Retail-Spielgrafik
und werden nicht ins Data-Repository übernommen. Die beiden Kamerawinkel
sind verschieden und erlauben keinen belastbaren Bildvergleich.
