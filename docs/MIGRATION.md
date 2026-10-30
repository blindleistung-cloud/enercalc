# EnerCalC: Migrationskonzept

> **Aktualisierte Zielvorgabe:** Dieses Dokument enthält das ursprüngliche Konzept. Seit der Freigabe zur Migration gilt ausschließlich die aktuell anwendbare Norm-/Rechtsbasis einschließlich AMEV und Bundesbau/Bundeswehr. Historische EnEV-/LU-Verfahren sind kein Anwendungspfad. Maßgeblich für den aktuellen Arbeitsstand ist [Aktuelle Verfahren und Normnachweise](NORMEN.md). Die ursprüngliche Analyse bleibt als Vergleichsquelle erhalten.

Stand: 30. Oktober 2026. Grundlage: die hochgeladene EnerCalC.xlsm, Version 6.1.177. Die [Bestandsaufnahme](ANALYSE.md) beschreibt die beobachtete Datei; dieses Dokument beschreibt die empfohlene zukünftige Implementierung.

## Ziel und Umfang

Ziel ist eine elegante, eigenständige Webanwendung, die als **einzelne index.html** lokal geöffnet wird. Sie benötigt weder Excel noch Backend, Installation, Internetzugriff oder einen lokalen Webserver. Gebäude-, Zonen- und Anlagenparameter führen zu nachvollziehbaren Monats-/Jahresbilanzen, einem Original-/Referenzvergleich und speicherbaren Varianten.

Die erste abgeschlossene Arbeit ist die statische Analyse und dieses Konzept. Ein nachgebildeter, fachlich validierter Energie-Rechenkern ist noch nicht implementiert. Die mitgelieferte index.html ist ein Analysewerkzeug und kein Energieberatungsprogramm.

**Empfehlung:** Fachlogik modular neu implementieren, Herkunft und Zwischenwerte erhalten, gegen kontrollierte Excel-Referenzfälle validieren. Kein pauschaler vereinfachter Wärmebedarfsrechner als vermeintlich gleichwertiger Ersatz.

## Architektur

```text
versionierte Stammdaten + Projektzustand
                 ↓
validieren → Geometrie → Zonenparameter → Monatsberechnung
                 ↓
Beleuchtung ↔ interne Gewinne → Heiz-/Kühl-Nutzenergie
                 ↓
Lüftung + Warmwasser + Anlagentechnik + Hilfsenergie
                 ↓
Erzeugung / Eigenstrom / Speicher / Bilanzstrategie
                 ↓
Endenergie + Primärenergie + CO₂ + Referenzvergleich
                 ↓
Ergebnisobjekt → Oberfläche / Diagramme / Datei / Druck
```

Die Pfeile sind die Zielstruktur, noch kein vollständig aufgelöster Ablauf des Originals. Kopplungen, vor allem Beleuchtung/Wärmequellen, Solarnutzung, KWK und Hilfsenergie, müssen aus den Excel-Referenzen und der tatsächlichen Berechnung abgeleitet werden.

### Vier getrennte Ebenen

1. **Datenmodell:** stabile fachliche IDs, Einheiten, Gültigkeitsbereiche und Quellversionen. Keine Zelladressen als primäre Anwendungsdaten.
2. **Rechenkern:** möglichst reine JavaScript-Funktionen. Keine DOM-Zugriffe, versteckten Steuerzellen oder veränderlichen globalen Auswahlzustände. Gleiche Eingaben erzeugen gleiche Ergebnisse.
3. **Ergebnisobjekt:** Monats- und Jahreswerte, Zonenwerte, Bilanzmethode, Warnungen sowie wichtige Zwischenwerte mit Excel-Herkunft.
4. **Oberfläche:** führt durch Eingaben, zeigt Diagnosen und visualisiert ein gemeinsames Ergebnisobjekt. Keine getrennte Berechnungslogik in Diagrammen oder Exporten.

Original- und Referenzgebäude nutzen dieselben Funktionen mit unterschiedlichen Parametern. Die duplizierten Blätter CalC und CalC_Referenz werden nicht als zwei dauerhaft unabhängig gepflegte Rechenprogramme nachgebaut.

### Datenvertrag

| Objekt | Wesentliche Felder | Herkunft |
|---|---|---|
| Projekt | Formatversion, Name, Sprach-ID, Rechenkernversion, Regelwerk-ID | VBA-Projektverwaltung, Language |
| Gebäude | Hüllflächenverfahren, Orientierung, Flächen/Längen, Geschosse, beheiztes Volumen, Bauteilkennwerte | Eingabe 14–77 |
| Verglasung | Glasart, Ug, Uf, Randverbund ψ, Rahmenanteil, g, Sonnenschutz, Verschattung | Eingabe 54–71, Konst |
| Zonen[] | stabile ID, Profil-ID, Fläche, Höhe, beheizt/gekühlt, Lüftungs-/Lichtsteuerung, Hüllflächenzuweisung | Eingabe 80–118, DATA, Tab.Listen |
| Klima | ID, Herkunft, 12 Temperaturwerte, Strahlung nach Orientierung, Wind | Wetterdaten |
| Nutzung | ID und ursprünglicher Profilindex, Zeiten, Solltemperaturen, Außenluft, Personen-/Gerätegewinne, Beleuchtung | Nutzungen |
| Anlagen | Wärme-/Kälteerzeuger, Übergabe, Verteilung, Warmwasser, Solar, PV, WEA, KWK, Speicher | Eingabe 121–183, Anlagenblätter |
| Faktoren | Energieträger-ID, Primärenergie/CO₂, Version, erlaubte Nutzerüberschreibung | Faktoren, Tab.Referenz |
| Bilanz | explizite Methode, Zeitschritt, Bezug, Anrechnung und Exportbehandlung | Gesamtbilanz, nZEB-Bilanzen |
| Variante | Name, vollständiger unveränderlicher Eingabe-Snapshot, Version | bisherige Varianten-/Kopiermakros |

Profilindex, im Namen sichtbare Nutzungsnummer und stabile Web-ID müssen getrennt sein. Beispielsweise ist das Profil „32 Parkhaus“ die 34. Profilposition, da Nutzung 22 drei Untervarianten besitzt. Einfache Umwandlung der Textnummer in einen Arrayindex wäre falsch.

Zahlen intern als JavaScript Number; UI mit de-DE-Formatierung. Einheiten explizit, beispielsweise W, kW, Wh, kWh, m², m³, Stunden, Tage, Grad und Prozent. Umrechnungen und Rundung nur an definierten Stellen. Der Dezimaltrenner einer importierten Altdatei muss vor dem Zahlenparsen behandelt werden.

### Projektdateien

- Primärformat: versioniertes JSON mit Validierung und Whitelist der Felder. Import darf keine Formeln ausführen oder HTML interpretieren.
- Optionaler Legacy-Import: bisherige TXT-Projektdateien. Header, Version und Dezimaltrenner prüfen; `Wert[[Blatt]]Name/Zelle` in bekannte fachliche Felder übersetzen. Unbekannte Ziele nicht einfach übernehmen. Die VBA-Altversionskonvertierung als separaten Adapter behandeln.
- Speichern: Blob-Download; Laden: Dateiauswahl/FileReader. Keine erforderliche File System Access API, da diese unter file:// und in Browsern unterschiedlich verfügbar ist.
- Browser-Autosave optional, mit Fehlerbehandlung. localStorage-Verhalten unter file:// ist nicht browserübergreifend verlässlich; eine heruntergeladene Projektdatei bleibt der verlässliche Austauschweg.
- Varianten speichern Eingaben und Rechenkern-/Datenversionen. Ergebnisse dürfen als Cache beigefügt sein, müssen nach Import auf Versionskompatibilität geprüft werden.

## Umsetzungsreihenfolge und Abnahme

### 1. Referenzbasis sichern

Die vorhandene statische Analyse archiviert die belegten Zellen, Formeln, Cachewerte, Namen und VBA-Quellen. Für die nächste Phase ist eine kontrollierte Ausführung in der ursprünglichen Excelumgebung nötig:

- Exakte Originaldatei mit dokumentierter Excelversion verwenden; vor/nach dem Öffnen und nach erforderlichen Makros Werte exportieren.
- Aktuelle Auswahlparameter, versteckte Eingaben und den Hüllflächenmodus protokollieren.
- Makroabhängige Datenänderungen gesondert erfassen: Profilkopie, Referenzladen, Beispiel, Parameterstudien.
- Je Testfall vollständige Zonen-/Monats-/Jahreswerte und zentrale Zwischenwerte sichern.
- Fehlerwerte mitaktivierten und unbenutzten Rechenpfaden zuordnen. Keine pauschale Nullsetzung.

**Abnahme:** definierter Eingabezustand und reproduzierbare Ausgaben pro Referenzfall. Der gespeicherte Cache allein gilt noch nicht als bestätigtes Soll-Ergebnis.

### 2. Stammdaten, Geometrie und eine Zone

Klimakatalog und Profilkatalog mit stabilen IDs übernehmen. Geometrie, beide Hüllflächenverfahren, EBF und Bauteil-U-Werte implementieren. Einen Original-/Referenzfall für eine Zone und einen Monat vollständig durch die Nutzenergieberechnung führen. Danach Monate/Zonen parametrisieren.

**Abnahme:** Flächen-, Temperatur- und Energiezwischenwerte stimmen mit dem kontrollierten Excelfall überein. Beide Flächenverfahren und Prozent-/Einheitenkonversion sind getestet.

### 3. Rechenkern vollständig erweitern

Tageslicht und Beleuchtung, interne Gewinne, Nutzung/Nichtnutzung, Lüftung/Infiltration, Wärme-/Kältesenken, Zeitkonstanten und Ausnutzungsgrade modulweise übertragen. Anschließend Warmwasser, Übergabe/Verteilung, Erzeuger und Hilfsenergie. Original und Referenz parallel prüfen.

**Abnahme:** jeder Modulabschluss besitzt Vergleichstests für Eingaben, Zwischenwerte und Ausgaben. Dynamische Exceladressen wurden entweder fachlich ersetzt oder ihre Semantik nachweislich abgebildet. Keine unbemerkte Vereinfachung.

### 4. Erzeugung und Bilanzverfahren

Solarthermie, PV, WEA, KWK und Batterie getrennt implementieren. Eigenverbrauch, Einspeisung, Anrechnungsbegrenzung, Monats-/Jahressaldierung und CO₂-/Primärenergiebehandlung als explizite Bilanzstrategien modellieren. Welche Strommengen anrechenbar sind, ist keine pauschale `min(Jahresbedarf, Jahresertrag)`-Regel.

**Abnahme:** Energiebilanzen schließen pro Monat und Jahr. Gleichzeitige Erzeugung, Nullbedarf, Überschuss, Speicherverluste und die einzelnen Bilanzmethoden sind durch Vergleichsfälle gedeckt.

### 5. Oberfläche und Auslieferung

Schritte: Projekt → Gebäudehülle → Zonen → Anlagen → Bilanz → Varianten. Eingabefehler direkt an Feldern; Ergebnisse kennzeichnen Bezug, Einheit und Methode. Herkunftsdetails optional ausklappbar. Diagramme aus Ergebnisobjekten; Druck-/PDF-Ansicht über Browserdruck.

**Abnahme:** die einzelne index.html funktioniert per Doppelklick bei deaktiviertem Netzwerk. Keine externen Fonts, Skripte, Bilder, Modulimporte oder fetch-Zugriffe. Projekt-Import/Export, Tastaturbedienung, schmale Bildschirme und Druck sind in den Zielbrowsern geprüft.

## Funktionsmatrix

| Bereich | Übertragung | Priorität / Besonderheit |
|---|---|---|
| Projektverwaltung | JSON-Import/Export; Legacy-TXT-Adapter | Früher Datenvertrag |
| Hülle direkt / vereinfacht | Geometriemodul | Früher Durchstich |
| Zonen / Nutzung | bis 11 Zonen, volle Profilparameter | Keine Nummer/Index-Verwechslung |
| Tageslicht / Beleuchtung | Detailmodul aus CalC | Stark mit Gewinnen gekoppelt |
| Thermische Monatsbilanz | parametrisierte Zonen-/Monatsfunktionen | Kritischer Kern |
| Lüftung | Luftmengen, Steuerung, WRG, Fan-/Hilfsenergie | Nutzungszeiten erhalten |
| Wärme / Kälte / TWW | eigene Anlagenmodule | Aufwandszahlen und Hilfsenergie |
| Solar / PV / WEA / KWK / Speicher | modulare Erzeugung und Anrechnung | Eigene Testmatrix |
| Primärenergie / CO₂ / nZEB | getrennte Bilanzstrategien | Keine Methoden vermischen |
| Referenz / Anforderungen | versionierte historische Parameterprofile | DE und LU getrennt |
| Varianten / Studien | immutable Eingabesnapshots | Nach Rechenkernvalidierung |
| Sankey / Diagramme | SVG aus Ergebnisdaten | Excel-Chartkopien entfallen |
| DE / EN | Sprachkatalog vom Modell trennen | DE zuerst; EN vorbereitet |
| Excel-Blattschutz / Ribbon / Clipboard | normale Browserbedienung | Nicht wortgleich portieren |
| IE-Updateprüfung / EXE-Download | entfällt im Offlinebetrieb | Kein Netz nötig |

## Validierungsstrategie

### Vergleichsregeln

Pro Ergebnis werden Eingabeversion, erwarteter Excelwert, tatsächlicher Webwert, absoluter/relativer Unterschied und Fehlerstatus protokolliert. Exakte Gleichheit für Auswahl-, Zustands- und Fallunterscheidungen. Für numerische Werte zunächst strenge technische Toleranzen vereinbaren und anhand ungerundeter Excelwerte kalibrieren; keine nachträgliche Toleranzerhöhung, um eine unbekannte Abweichung zu verdecken. Gerundete Anzeigen und Rohwerte getrennt vergleichen.

Excel-Semantik ausdrücklich testen: Leerzelle vs. `""`, Null, Textzahl, boolescher Wert, Fehlerwert, Suchmodus von MATCH/VLOOKUP/HLOOKUP, IFERROR/ISNUMBER, Rundung, übergroße SUMIF-Summenbereiche, Matrizen/Regressionen in TREND und LINEST sowie volatile/dynamische Verweise. Ein Formelauswerter darf keine unkontrollierten eval-Aufrufe verwenden.

### Referenzfallmatrix

| Dimension | Mindestfälle |
|---|---|
| Geometrie | direkt, vereinfacht, ohne Fenster, Dachfenster, erdberührte Flächen |
| Zonen | eine, mehrere, elf; leer/unbenutzt; unbeheizt; teilgekühlt; Wohn-/Nichtwohnen |
| Nutzung | Büro, Sitzung, Verkehrsfläche, WC, Lager, Wohnen; Indexuntervarianten |
| Klima | Referenz, warme/kalte Region, eigener vollständiger Satz |
| Betrieb | Nutz-/Nichtnutzungszeit, Wochenende, Absenkung, Nachtlüftung |
| Anlagen | Kessel, Wärmepumpe, Fernwärme, elektrische TWW, Kühlung, WRG |
| Erzeugung | alles aus, PV allein, WEA allein, KWK, Solar, Speicher und Kombinationen |
| Bilanz | jede übernommene nZEB-/Anrechnungsmethode, DE-/LU-Referenz |
| Grenzfälle | Nullbedarf, Nullerzeugung, 0/100-%-Anteile, nicht gefundene Auswahlwerte |
| Dateien/UI | JSON-Roundtrip, Legacy-Dezimaltrenner, ungültige Daten, file://, offline, Druck |

Zusätzlich physikalische Invarianten prüfen: Flächensummen stimmen; nach außen ausgewiesene Energieströme schließen; Erzeugung wird nicht doppelt gutgeschrieben; Speicherverlust ist kein Energiegewinn. Diese Tests ergänzen Excel-Vergleiche und helfen, bestehende Altfehler nicht blind zu reproduzieren.

## Entscheidungen und offene Nachweise

- Die Datei enthält historische EnEV-/LU-Verfahren und bezeichnet sich als Lernmodul. Eine Portierung ist keine Aktualisierung auf heutiges GEG oder aktuelle DIN-Ausgaben.
- Der Hinweis, dass die Berechnungen nicht für Energieausweise geeignet sind, ist Produktinhalt der Vorlage und muss bei der fachlichen Einordnung erhalten bleiben.
- Ein bestätigter Altfehler wird entweder kompatibel abgebildet oder bewusst korrigiert. Entscheidung, Auswirkungen und Testfall dokumentieren; keine stille Änderung.
- Vollständige dynamische Abhängigkeiten und Makroergebnisse bleiben bis zur kontrollierten Excelausführung offen. Aus statischen Blattzyklen folgt nicht automatisch ein zirkulärer Zellbezug.
- Bezeichnungen, Tabellen und Originalquellen haben Urheber-/Nutzungsrechte. Vor öffentlicher Verteilung übernommener Inhalte die verfügbaren Rechte klären; die technische Analyse allein belegt keine Lizenz.
- Eine seriöse Aufwandsschätzung folgt nach dem ersten validierten vertikalen Rechendurchstich. Die reine Formelanzahl ist wegen Wiederholungen kein brauchbarer Multiplikator.

Der nächste fachlich sinnvolle Schritt ist die Gewinnung kontrollierter Excel-Referenzfälle. Die Oberfläche kann parallel gestaltet werden; freigegebene Zahlen sollten erst nach der zugehörigen Kernvalidierung angezeigt werden.
