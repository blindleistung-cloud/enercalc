# EnerCalC · Workbook Atlas

Statische Analyse und Migrationskonzept für die hochgeladene **EnerCalC.xlsm (6.1.177)**. Der gewünschte erste Schritt ist die vollständige Analyse, noch kein nachgebauter Energierechner.

## Herunterladen über GitHub

- **[Gesamtpaket als ZIP](https://github.com/blindleistung-cloud/enercalc/raw/refs/heads/main/downloads/EnerCalC-Analyse.zip)** – entpacken und die enthaltene `index.html` öffnen.
- [Einzelne index.html](https://github.com/blindleistung-cloud/enercalc/blob/main/index.html)
- [Analyse](https://github.com/blindleistung-cloud/enercalc/blob/main/docs/ANALYSE.md)
- [Migrationskonzept](https://github.com/blindleistung-cloud/enercalc/blob/main/docs/MIGRATION.md)
- [Prüfbericht](https://github.com/blindleistung-cloud/enercalc/blob/main/docs/VALIDIERUNG.md)

Einzeldateien lassen sich auf ihrer GitHub-Dateiseite über **Download raw file** (Pfeil nach unten) speichern. Für ein privates Repository ist die Anmeldung mit deinem berechtigten GitHub-Konto erforderlich. Alternativ lädt **Code → Download ZIP** das gesamte Repository herunter.

**[index.html](index.html) herunterladen und in einem aktuellen Browser öffnen.** Die einzelne Datei enthält Oberfläche, alle 179.048 belegten Zellen und die extrahierten VBA-Quellen. Sie benötigt keine Installation, keinen Server, kein Excel und kein Internet. Chrome, Edge, Firefox oder Safari mit `DecompressionStream`-Unterstützung sind erforderlich.

Die Ansicht bietet:

- Überblick, Blattinventar und gespeicherten Beispielstand;
- Suche über alle Zellinhalte, Formeln, Cachewerte und Kommentare, Filter und Zelldetails;
- 1.671 Namensdefinitionen mit globalen/lokalen Gültigkeitsbereichen;
- Klima-, Nutzungs- und Faktorkatalog;
- vollständigen extrahierten VBA-Quelltext mit Prozedur-/Modulsuche;
- belegte Rechenbeispiele und Migrationsfahrplan mit Abnahmekriterien.

Alle Ergebnisse sind gespeicherte Excel-Caches. Weder Formeln noch Makros werden im Analysewerkzeug berechnet oder ausgeführt. 1.668 gespeicherte Fehlerwerte sind im Inventar dokumentiert. Die Seite baut keine Netzwerkverbindung auf; eine CSP unterbindet Netzwerkzugriffe und fremde Ressourcen.

## Schriftliche Unterlagen

- [Statische Bestandsaufnahme](docs/ANALYSE.md)
- [Migrationskonzept](docs/MIGRATION.md)
- [Maschinenlesbares Inventar einschließlich VBA-Quellen](docs/workbook-inventory.json)
- [Vollständiger komprimierter Zellkatalog](docs/cell-catalog.json.gz)
- [Prüfbericht](docs/VALIDIERUNG.md)

Die ursprüngliche XLSM wird nicht verändert und nicht in die HTML-Datei eingebettet. Für eine erneute Extraktion ist dieselbe Quelldatei nötig; ihr Hash steht im Inventar.

## Entwicklung und Reproduktion

Das vorhandene Checkout in `/workspace/enercalc` verwenden. Cloud-Tasks sind bereits isoliert; kein zusätzliches Git-Worktree erforderlich.

Die Analyseansicht und ihr Build benötigen keine npm-Abhängigkeiten. Zum erneuten Bündeln reichen Python 3 und die bereits extrahierten Daten:

```sh
cd /workspace/enercalc
python3 tools/build_report.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Eine neue Extraktion benötigt Python-Pakete `openpyxl==3.1.5` und `oletools==0.60.2` (Version der vorliegenden Extraktion siehe Prüfbericht). Installation in eine eigene virtuelle Umgebung, danach:

```sh
python tools/analyze_workbook.py /pfad/zu/EnerCalC.xlsm
python tools/build_report.py
```

Der Browser-Smoke-Test benötigt zusätzlich Playwright und System-Chromium:

```sh
python tests/browser_smoke.py
```

Der verwaltete System-Chromium dieser Cloud blockiert direkte `file://`-Navigation per Richtlinie. Der automatisierte Test nutzt deshalb ausschließlich einen lokalen temporären HTTP-Server; nach dem ersten Laden werden alle Interaktionen bei deaktiviertem Browsernetz geprüft. Die Richtlinie wird nicht verändert. Ein direkter Doppelklicktest in einem normalen lokalen Zielbrowser bleibt separat erforderlich.

Die Struktur `report/` enthält den wartbaren Quellcode. `tools/build_report.py` erzeugt die fertige Einzeldatei mit eingebettetem Datenbestand; sie darf unabhängig vom Rest des Verzeichnisses weitergegeben werden, sofern die Rechte an den übernommenen Inhalten das erlauben.
