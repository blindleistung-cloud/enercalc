# Prüfung der Analyseartefakte

Stand: 30. Oktober 2026.

## Bestand und Extraktion

Quelle: EnerCalC.xlsm, SHA-256 `d84dd1400ebbf5d604187ed44753fc439d6bcc08e1d19f98396421099c10306e`.

- 29 Blattkataloge; 179.048 belegte Rohdatenzellen.
- 141.897 Formeln einschließlich sechs sonst durch die Normalisierung verbundener Zellen verdeckter geteilter Formeln.
- 1.671 Namensdefinitionen einschließlich 195 blattlokaler Definitionen.
- 53 VBA-Quellen mit 254 Prozeduren.
- Die Originaldatei wurde nur gelesen und blieb unverändert. Kein Makro wurde ausgeführt.

Extraktionswerkzeuge: Python 3.12.14, openpyxl 3.1.5 und oletools 0.60.2. Für das HTML-Bündeln wird nur die Python-Standardbibliothek benötigt. Keine zusätzlichen Anwendungsabhängigkeiten zur Nutzung der HTML-Datei.

## Integritätstests

Ausgeführt:

```sh
ENERCALC_SOURCE=/pfad/zu/EnerCalC.xlsm python3 -m unittest discover -s tests -p 'test_*.py' -v
```

**Ergebnis: 8 Tests bestanden, 0 fehlgeschlagen, 0 übersprungen.**

1. Blatt-/Zellzahlen, eindeutige Adressen, Formeln und Konstanten passen zum Katalog; neun wiederhergestellte Rohdatenzellen sind enthalten.
2. Fehlerwerte stimmen in Anzahl und Fundstellen überein; dokumentierte 0/0- und Textarithmetikfälle sind belegt.
3. Alle 1.671 Namensdefinitionen besitzen die erwarteten globalen/lokalen Gültigkeitsbereiche und eindeutige Kombinationen aus Name und Gültigkeitsbereich.
4. Profil-IDs sind eindeutig; Parkhaus-/Wohnprofilindex und vollständige Monatsklimadatensätze werden geprüft.
5. Der gespeicherte Beispielstand stimmt arithmetisch in Flächen-, Primärenergie- und gewichteter Heizwärmeaggregation überein. Das ist eine Cache-Konsistenzprüfung, keine Neuberechnung aller Formeln.
6. VBA-Quelltext und Prozedur-/Zeilenzahlen stimmen überein.
7. Der HTML-Datenblock ist vollständig identisch zu Inventar und Zellkatalog. Keine externen Skript-, Stylesheet- oder Bildreferenzen; Netzwerk-CSP vorhanden.
8. Roh-OOXML unabhängig gelesen: Originalhash, vollständige Anzahl der Formel-/Wertzellen, Fehlerwerte und sämtliche globalen/lokalen Namensdefinitionen stimmen überein.

Der Originaldaten-Test wird ohne gesetzte Quellvariable ausdrücklich übersprungen; im dokumentierten abschließenden Lauf war die Quelle gesetzt und der Test lief mit.

## Browserprüfung

Ausgeführt: `python3 tests/browser_smoke.py` mit Playwright und dem vorhandenen System-Chromium.

**Bestanden:**

- Laden der Einzeldatei über einen temporären lokalen Testserver und Entpacken aller eingebetteten Daten;
- Desktopnavigation und mobile Ansicht mit 390 px Breite ohne Seitenüberlauf;
- Suche über alle Blätter, Fehlerfilter, 128 #VALUE!-Fundstellen und Ergebnisseiten;
- Suchtexte mit HTML-Zeichen bleiben Text, keine HTML-Interpretation;
- Quellverweise und Zelldetails einschließlich echter Formeln und Cachewerte;
- Namenskatalog, 18 Klimadatensätze, 44 Nutzungsprofile und sechs Faktorzeilen;
- VBA-Modul-/Prozedursuche und Anzeige der vollständigen Quelltexte;
- fünf Migrationsphasen und JSON-Download mit vollständigen Inventarzahlen;
- sämtliche Bedienprüfungen nach dem initialen Laden bei im Browser deaktiviertem Netzwerk;
- genau eine Dokumentanforderung, keine externen Anfragen und keine JavaScript-Ausnahmen.

Der lokale Testserver wird vom Test gestartet und anschließend beendet. Er ist keine Anwendungsabhängigkeit.

### Grenze des direkten Datei-Tests

Die verwaltete System-Chromium-Richtlinie dieser Cloud blockiert `file://` mit `ERR_BLOCKED_BY_ADMINISTRATOR`. Die Richtlinie wurde weder verändert noch umgangen. Deshalb ist ein direkter Doppelklickstart hier **nicht erfolgreich geprüft**. Das Artefakt ist vollständig eigenständig, verwendet keine fetch-/Modul-/Netzwerkressourcen und wurde nach dem initialen lokalen Dokumenttransport vollständig offline bedient. Ein direkter file://-Test in einem normalen Zielbrowser sowie Tests mit Firefox/Safari/Edge bleiben offen.

## Bewusst nicht nachgewiesen

- Excel-Neuberechnung und Ergebnisse nach Makroausführung;
- fachliche Gleichheit eines neuen Rechenkerns: ein solcher wurde in dieser Phase nicht implementiert;
- vollständige Laufzeitauflösung aller OFFSET-/INDIRECT-Ziele und Makro-Nebenwirkungen;
- visuelle Nachbildung der ursprünglichen Excel-Diagramme und ActiveX-Oberfläche;
- aktuelle Norm-/Verordnungskonformität und fachliche Zertifizierung.

Diese Grenzen sind im Analysewerkzeug und Migrationskonzept kenntlich gemacht. Die vorhandenen 1.668 Excel-Fehlercachewerte wurden inventarisiert und nicht als Fehler der Analyseansicht unterdrückt.
