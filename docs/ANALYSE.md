# EnerCalC: statische Bestandsaufnahme

Stand: 30. Oktober 2026. Untersucht wurde die hochgeladene `EnerCalC.xlsm` mit 5.230.777 Bytes. Dateiinterne Versionsanzeige: **EnerCalC Version: 6.1.177**.

SHA-256: `d84dd1400ebbf5d604187ed44753fc439d6bcc08e1d19f98396421099c10306e`

## Ergebnis und Untersuchungsgrenze

Das Projekt ist technisch für eine lokale statische Webanwendung geeignet: die Rechenarbeit benötigt grundsätzlich keinen Server. Die Vorlage ist jedoch ein umfangreiches, zustandsbehaftetes Excelprogramm mit Gebäude-/Zonenberechnung, Anlagentechnik, mehreren Bilanzverfahren, Referenzanforderungen und Projektverwaltung.

**Vollständig erfasst wurden die statisch auslesbaren Zellinhalte, Formeln, gespeicherten Ergebnisse, globalen/lokalen Namen, extrahierten VBA-Quellen und die unten beschriebenen Objektinventare.** Das ist keine fachliche Zertifizierung aller Formeln und kein Nachweis des Verhaltens nach Ausführung sämtlicher Makros. Makros, Internetlinks und dokumentinterne Handlungsaufforderungen wurden nicht ausgeführt. Inhalte der Datei wurden ausschließlich als Untersuchungsgegenstand behandelt.

Die [interaktive index.html](../index.html) enthält alle belegten Zellen und VBA-Quellen als komprimierte Daten. Sie ist ein eigenständiges Analysewerkzeug und **noch kein nachgebauter Energie-Rechner**. Das [Migrationskonzept](MIGRATION.md) beschreibt den Übergang zur eigentlichen Anwendung.

## Umfang

| Gegenstand | Beobachtung |
|---|---:|
| Tabellenblätter | 29 |
| Sichtbare / ausgeblendete / sehr verborgene Blätter | 3 / 8 / 18 |
| Belegte Zellen, ohne reine Formatierungszellen | 179.048 |
| Formelzellen | 141.897 |
| Übrige belegte Zellen | 37.151 |
| Unterschiedliche erkannte Formelfunktionen | 58 |
| Globale Namensdefinitionen | 1.476 |
| Lokale Namensdefinitionen, inkl. Excel-Systemnamen | 195 |
| Alle Namensdefinitionen in workbook.xml | 1.671 |
| Extrahierte VBA-Module / Quelltextzeilen | 53 / 6.240 |
| Extrahierte Sub-Prozeduren / Function-Definitionen | 254 / 0 |
| Diagrammdefinitionen | 177 |
| ActiveX-XML-Definitionen | 9 |
| Mediendateien im OOXML-Paket | 30 |
| Erfasste Formular-/Zeichnungsbindungen | 746 |
| Datenvalidierungsdefinitionen / verbundene Bereiche | 126 / 81 |
| Externe Excel-Arbeitsmappenlinks | 0 |
| Gespeicherte Fehlerwerte | 1.668 |

Die ActiveX-Anzahl zählt XML-Definitionen im ZIP, nicht alle Schaltflächen, Comboboxen oder unterstützten Browserkontrollen. Die 746 Bindungen können mehrere Arten pro Objekt sowie Wiederholungen enthalten. Kein pauschaler Schluss „746 Controls“. Fehlende externe Excellinks bedeuten nicht, dass VBA keine externen Funktionen kennt: Onlinecheck verwendet beispielsweise einen historischen IE-/Downloadpfad; Einlesemakros adressieren weitere Blatt-/Arbeitsmappenstrukturen.

Der sehr verborgene Zustand `veryHidden` ist in Excel nicht über den normalen Dialog aufhebbar. Er ist ein Darstellungszustand, kein Grund, die enthaltene Fachlogik bei der Migration auszulassen.

## Blattinventar

Zeilen/Spalten sind die von openpyxl erkannten Blattdimensionen. Die Formelzahlen enthalten die aufgelösten geteilten Excel-Formeln. Neun in verbundenen Bereichen verborgene Rohdatenzellen wurden zusätzlich direkt aus OOXML wiederhergestellt: sechs Formeln in Tab.Wärme und drei Textwerte in Eingabe/Nutzungen. openpyxl blendet diese außerhalb der verbundenen Ankerzelle aus; deshalb ergab die erste Parserzählung nur 141.891 statt der tatsächlich gespeicherten 141.897 Formeln. Sichtbarkeit ist der gespeicherte Zustand.

| Blatt | Zustand | Dimension | Formeln | Konstanten | Fehlercache |
|---|---|---:|---:|---:|---:|
| Language | veryHidden | 1044 × 6 | 1,420 | 2,105 | 0 |
| LOG | veryHidden | 311 × 10 | 19 | 1,160 | 0 |
| Start | visible | 43 × 23 | 35 | 21 | 0 |
| Eingabe | visible | 428 × 23 | 635 | 129 | 0 |
| Gesamtbilanz | visible | 698 × 54 | 6,626 | 318 | 3 |
| Gesamtbilanz_Referenz | veryHidden | 382 × 52 | 5,115 | 314 | 3 |
| nZEB-Bilanzen | hidden | 69 × 27 | 311 | 72 | 0 |
| Anforderungen | hidden | 119 × 39 | 155 | 49 | 0 |
| Faktoren | hidden | 15 × 10 | 30 | 14 | 0 |
| TEK | hidden | 46 × 25 | 225 | 13 | 0 |
| Wetterdaten | hidden | 301 × 18 | 639 | 2,447 | 0 |
| Nutzungen | hidden | 111 × 57 | 912 | 2,362 | 0 |
| Sankey | hidden | 46 × 23 | 2 | 0 | 0 |
| Tab.Sankey | veryHidden | 350 × 49 | 4,346 | 740 | 216 |
| CalC | hidden | 3962 × 31 | 47,551 | 3,900 | 13 |
| CalC_Referenz | veryHidden | 3962 × 26 | 47,615 | 3,844 | 18 |
| DATA | veryHidden | 1569 × 61 | 4,245 | 287 | 0 |
| Konst | veryHidden | 343 × 62 | 2,330 | 2,347 | 0 |
| Tab.Referenz | veryHidden | 447 × 65 | 4,234 | 727 | 1303 |
| Tab.Rating | veryHidden | 53 × 20 | 324 | 120 | 0 |
| Tab.Listen | veryHidden | 522 × 31 | 1,683 | 787 | 0 |
| Tab.Grafiken | veryHidden | 176 × 36 | 1,491 | 92 | 3 |
| Tab.Grafiken2 | veryHidden | 490 × 50 | 5,455 | 340 | 0 |
| Tab.Wärme | veryHidden | 100 × 60 | 969 | 573 | 104 |
| Tab.WW | veryHidden | 127 × 20 | 388 | 380 | 0 |
| Tab.Kälte | veryHidden | 987 × 33 | 2,386 | 12,944 | 0 |
| Tab.Solar | veryHidden | 102 × 33 | 771 | 589 | 2 |
| Tab.PV | veryHidden | 103 × 43 | 1,209 | 330 | 3 |
| Tab.WEA | veryHidden | 92 × 19 | 776 | 147 | 0 |

### Fachliche Gruppen

- **Bedienung:** Start und Eingabe sind die eigentliche Eingabeoberfläche; Gesamtbilanz ist das dritte sichtbare Blatt. Language liefert deutsche/englische Texte, LOG die Versionierung.
- **Stammdaten und Vermittlung:** Wetterdaten, Nutzungen, Faktoren, Konst, DATA und Tab.Listen. Viele Dropdowns schreiben zunächst Auswahlindizes nach Tab.Listen. DATA übersetzt/vermittelt und aggregiert; es ist keine reine Konstantentabelle.
- **Zonenberechnung:** CalC und CalC_Referenz enthalten zusammen 95.166 Formeln, also rund 67,1 % der Formelzellen. Zonen erscheinen insbesondere in F:P; Monate und Betriebszustände erzeugen wiederholte Blöcke.
- **Anlagentechnik:** Tab.Wärme, Tab.WW, Tab.Kälte, Tab.Solar, Tab.PV und Tab.WEA.
- **Bilanz und Regeln:** Gesamtbilanz, Gesamtbilanz_Referenz, nZEB-Bilanzen, Anforderungen, Tab.Referenz und Tab.Rating.
- **Auswertung:** TEK, Sankey, Tab.Sankey, Tab.Grafiken und Tab.Grafiken2. Diagrammdaten sind von Rechenwerten abhängig und sollen im Ziel aus Ergebnisobjekten entstehen.

## Erkannte Bedien- und Rechenabläufe

### 1. Projekt und Hüllfläche

Eingabe bietet direkte Hüllflächeneingabe und eine vereinfachte Erfassung über Fassadenlängen, Geschosse, Geschosshöhen und Fensteranteile. Orientierungen sind Süd, West, Nord, Ost und horizontal. Erfasst werden Fenster, opake Außenwände, erdberührte/unbeheizte Wände, Boden, Dach und beheiztes Gebäudevolumen.

`Eingabe!D41` summiert `D36:D40` zur thermischen Hülle; `D43` setzt diese ins Verhältnis zum beheizten Volumen. `Eingabe!E58` berechnet Uw aus Glas, Rahmen, Rahmenanteil und Randverbund. Wärmebrücken, g-Werte, Verschattung, Sonnenschutz und Luftdichtheit sind separate Parameter. Ein Webmodell nur mit vier pauschalen U-Werten würde Teile der vorhandenen Funktionen verlieren.

### 2. Zonen und Nutzung

Bis zu elf Zonen mit Fläche, Raumhöhe, Nutzungsprofil, Heiz-/Kühlzustand, Beleuchtung und Lüftung. Die EBF ist die Summe der beheizten Zonen (`Eingabe!D85`, benannt `G_EBF`), nicht automatisch die gesamte Nettogrundfläche.

Im gespeicherten Beispiel: 462 m² Büro, 66 m² Sitzung, 194 m² Verkehrsfläche, 66 m² WC/Sanitär und 33 m² Lager/Technik sind beheizt; 258 m² Parkhaus sind unbeheizt. Gesamtfläche 1.079 m², EBF 821 m². Gekühlt sind die ersten drei Zonen mit insgesamt 722 m².

44 numerisch befüllte Profilspalten wurden als vollständige Referenzdatensätze extrahiert. Weitere/partielle Zellen bleiben im vollständigen Zellkatalog. **Profilnummer und Auswahlindex sind nicht identisch:** Nutzung 22 hat drei Untervarianten; „32 Parkhaus“ steht an Position 34. „34 Wohnen EFH“ steht an Position 44. Die aktuelle Auswahl in DATA!J148 = 34 bezeichnet daher Parkhaus, nicht Wohnen.

### 3. Monatsklima und Zonenkern

18 numerisch vollständige Klimadatensätze: DIN-Referenzklima, 15 Regionen, Luxemburg und Referenzklima 2007. Zusätzlich sind eigene leere Datenplätze vorhanden. Temperatur, Strahlung nach Orientierung und Wind liegen monatlich vor. Es wurden keine aktuellen Wetterdaten nachgeladen.

CalC bereitet zunächst Geometrie, Fenster-/Raumparameter, Tageslichtbereiche und Beleuchtungsbedarf auf. Der thermische Teil beginnt laut Blattbeschriftung in Zeile 1009. Er umfasst Soll-/Bilanztemperaturen, Nutz-/Nichtnutzungszeiten, Absenkung, Lüftung, Infiltration, WRG, Wärmesenken/-quellen, solare/interne Gewinne, Zeitkonstanten, Ausnutzungsgrade und Heiz-/Kühlenergie.

Die Monatsblöcke haben unterschiedliche Betriebszustände. Eine globale Jahresgradtagszahl oder gleichmäßige Monatsaufteilung wäre kein gleichwertiger Ersatz. Beleuchtungsbedarf beeinflusst zugleich die internen Wärmequellen. CalC_Referenz bildet die Vergleichsberechnung ab.

### 4. Anlagentechnik und Erzeugung

Nutzenergie wird mit Übergabe-, Verteilungs-, Speicher- und Erzeugergrößen sowie Hilfsenergie zu End-/Primärenergie und Emissionen überführt. Heizsystem, Kühlung und TWW sind getrennte Stränge; Solarthermie und KWK koppeln Teile davon.

PV und WEA haben Monatsprofile. Gesamtbilanz behandelt zusätzlich Strom aus KWK, Anrechnung, Überschüsse, Speicher und verschiedene Bilanzvarianten. Primärenergiefaktoren und CO₂-Faktoren sind nicht austauschbar. Die Referenzdatei enthält u. a. Strombezug 1,8 und 617 gCO₂/kWh; diese Werte sind historische Dateiinhalte und werden hier nicht als aktuelle Standardwerte empfohlen.

### 5. Referenz und Anforderungen

`Tab.Referenz!S17:S21` enthält EnEV 2014, EnEV 2016, LU 2010, LU 2016 und LU 2019 nZEB. S23 = 2 wählt im gespeicherten Stand EnEV 2016. Die Referenzberechnung benötigt damit neben Gebäude-/Nutzungsdaten ein explizites historisches Regelwerkprofil.

Die Vorlage beschreibt sich als Lernmodul für vereinfachte Bilanzen in Anlehnung an DIN V 18599:2011/2016/2018 und enthält den Hinweis, dass sie nicht für die Ausstellung von Energieausweisen geeignet ist. Das ist eine inhaltliche Produkteigenschaft, keine Arbeitsanweisung an den Agenten. Portierung und Aktualisierung auf heutige Regeln sind unterschiedliche Vorhaben.

## Zahlen und Ausgangsbelege

Alle folgenden Zahlen sind **gespeicherte Excel-Cachewerte**. Sie wurden nicht mit Excel neu berechnet und sind noch keine unabhängig bestätigten Referenzergebnisse.

| Größe | Cachewert | Herkunft |
|---|---:|---|
| Energiebezugsfläche | 821 m² | Eingabe!D85 |
| Thermische Hüllfläche | 1.336,6 m² | Eingabe!D41 |
| Beheiztes Volumen | 2.996 m³ | Eingabe!D42 |
| Transmissionsleitwert | 642,102 W/K | DATA!D99 |
| Nutzenergie Heizen | 52,8584553759 kWh/(m²a) | DATA!A7 |
| Nutzenergie Kühlen | 27,5859786826 kWh/(m²a) | DATA!A6 |
| Nutz-/Endenergie Beleuchten | 15,1537445361 kWh/(m²a) | DATA!A9 |
| Endenergie Lüften | 9,40288139464 kWh/(m²a) | DATA!A10 |
| Nutzenergie TWW | 4,82338611449 kWh/(m²a) | DATA!A8 |
| Primärenergie Original | 135,2603977384 kWh/(m²a) | DATA!C12 |
| Primärenergie Referenz | 126,4641289187 kWh/(m²a) | DATA!D12 |

Beispielhafter Pfad: `Eingabe!D85` bestimmt die Bezugsfläche; `DATA!A7` gewichtet Zonen-Heizwärmewerte mit den Zonenflächen und teilt durch G_EBF; `DATA!C7 = IF(ISNUMBER(A7*F7),A7*F7,0)` wendet den resultierenden Anlagen-/Primärenergiefaktor an; `DATA!C12 = SUM(C6:C11)` aggregiert die primärenergetischen Teilwerte.

## Formelsprache und Abhängigkeiten

Erfasst sind 58 Funktionsnamen. Die häufigsten Aufrufe sind IF 61.721, INDEX 26.911, OFFSET 24.634, SUM 14.657, ISNUMBER 11.619 und IFERROR 10.443. Daneben kommen unter anderem VLOOKUP/HLOOKUP/MATCH, SUMPRODUCT, COUNTIFS/SUMIFS, TREND/LINEST, Exponential-/Logarithmus-/Trigonometriefunktionen und TEXT vor.

231 INDIRECT-Aufrufe und die 24.634 OFFSET-Aufrufe sind besonders relevant: sie erzeugen Zellreferenzen aus Laufzeitwerten. Die exportierte Blatt-Abhängigkeitsliste erfasst direkte Blattverweise und statisch auflösbare benannte Bereiche. Sie ist **kein vollständiger Zell-Ausführungsgraph**; dynamische Zieladressen, implizite VBA-Aufrufe und indirekte Makroänderungen sind darin nicht vollständig enthalten. Quell- und Zielblatt einer Kante bedeuten „Quelle benötigt Ziel“. Ein Zyklus zwischen Blättern beweist keinen zirkulären Zellbezug.

Keine der 1.671 Namensdefinitionen enthält im untersuchten Stand einen wörtlichen `#REF!`-Zieltext. Das belegt nicht, dass alle daraus berechneten dynamischen Adressen gültig sind. Globale und blattlokale Namen müssen inklusive ihrer Gültigkeitsbereiche übertragen werden; lokale Namen können globale Definitionen überschreiben.

## VBA: Aufgaben und Zustand

In 53 extrahierten Modulen stehen 254 Sub-Prozeduren und keine eigenen Function-Definitionen. Diese Aussage bezieht sich auf die extrahierten Quellen, nicht auf eine Laufzeitanalyse oder eine Prüfung des kompilierten VBA-P-Codes.

| Gruppe | Wichtige Module | Wirkung / Web-Ersatz |
|---|---|---|
| Projektverwaltung | Z_Data_Projektverwaltung | TXT lesen/schreiben, Backup, Dezimaltrenner, Altversionen → versioniertes JSON + optionaler Legacy-Adapter |
| Beispiel/Referenz | Z_Data_Beispiel, Z_Data_Referenz_laden | Eingaben und teils Formeln ändern → explizite Zustandsänderungen mit getrenntem Referenzzustand |
| Klassifizierung/Studien | Copy_Paste, Einstellungen_Gebäude | Profilsteuerung, Parameter setzen, Resultate kopieren → reine Variantenberechnung |
| Datenzuordnung | Einlesen, Einlesen_Bagatell | Flächen/Zonen aus anderen Strukturen übertragen → geprüfter Importadapter |
| Eigene Profile | Z_Nutzungsprofil_kopieren, Nutzungsprofil.frm | Profile kopieren/löschen → Profilverwaltung |
| Bedienung | Z_Ein_Ausblenden, Z_dropdownlisten, Tabelle3 | Hüllverfahren, Sichtbarkeit, Dropdowns → direkte UI-Logik |
| Rücksetzen | Z_Data_delete, Z_Zonendaten_delete | Eingaben/Zonen löschen → definierte Modellaktionen |
| Export | Z_Grafiken_Export, Diagramme | Excel-Chart-/Clipboardfunktionen → SVG/Browserdruck/Dateiexport |
| Excel-Lifecycle | DieseArbeitsmappe, Z_Hilfemakros | Ribbon, Berechnungsmodus, Save/Close, Blattschutz → nicht wortgleich portieren |
| Sprache/Online | Z_sprache, Onlinecheck | Sprache trennen; historische IE-/EXE-Updatefunktion entfällt offline |

**Wichtig:** `Z_Data_Referenz_laden` setzt sowohl Werte als auch `.FormulaR1C1`. Es enthält explizit den Kommentar, bei einer Lüftungszuordnung nur den Wert zu übernehmen, um einen Zirkelbezug zu vermeiden. Ein bloßer Import der gespeicherten Formeln ignoriert diese Zustandsübergänge.

`Copy_Paste.Energieen_für_Klassifizierung` verändert `Nutzungseinsteller` (CalC!F141), liest Ergebnisse aus CalC und kopiert Werte in Zielbereiche. Diese Abläufe sind keine zusätzlichen mathematischen UDFs, aber für Studienergebnisse erforderlich.

`DieseArbeitsmappe` greift in Save/Close/Print/Open ein; normale Arbeitsmappenspeicherung ist nicht der vorgesehene Projektworkflow. Der Browser sollte stattdessen explizite Projektdateien verwenden und nicht versuchen, Excel-Lifecycle-Effekte zu reproduzieren.

### Vorhandenes Projektformat

`PROJEKT_SPEICHERN` und `SpeicherProzedur` schreiben eine TXT-Datei mit EnerCalC-Versionskopf, Dezimaltrennzeichen und Datensätzen im Muster `Wert[[Blatt]]Name/Zelle`. `PROJEKT_LADEN` liest diese Informationen, konvertiert Dezimaltrennzeichen und behandelt alte Wetterdatenpositionen; Versionen vor Hauptversion 5 werden abgelehnt.

Ein Web-Legacy-Importer sollte nur bekannte Ziele auf fachliche Felder abbilden. Die aus der Exceldatei übernommene Möglichkeit, beliebige Worksheets/Range-Adressen zu beschreiben, ist kein geeigneter Datenvertrag für eine neue Webanwendung.

## Gespeicherte Fehler und Auffälligkeiten

| Blatt | #N/A | #VALUE! | #DIV/0! |
|---|---:|---:|---:|
| Gesamtbilanz | 0 | 0 | 3 |
| Gesamtbilanz_Referenz | 0 | 0 | 3 |
| Tab.Sankey | 216 | 0 | 0 |
| CalC | 0 | 12 | 1 |
| CalC_Referenz | 5 | 12 | 1 |
| Tab.Referenz | 1303 | 0 | 0 |
| Tab.Grafiken | 0 | 0 | 3 |
| Tab.Wärme | 0 | 104 | 0 |
| Tab.Solar | 0 | 0 | 2 |
| Tab.PV | 0 | 0 | 3 |

Die Verteilung allein zeigt keine vollständige Fehlerursache und auch nicht, welche Fehler aktive Endergebnisse beeinflussen. Insbesondere liegen viele Fehler außerhalb des sichtbaren Beispielpfads.

### Direkt nachvollziehbare Fundstellen

1. **Nullerzeugung:** Gesamtbilanz!Q182 = 0 und Q183 = 0; `U183 = Q183/Q$182` hat #DIV/0!. Ein Verhältnis bei Nullbedarf/Nullproduktion benötigt im Web ein definiertes Anzeige-/Fehlerverhalten. Ähnliche Quotienten treten in Grafiken und PV auf.
2. **Leere Zone:** CalC!P1060, P1053, P1283 und P1396 sind im Cache jeweils 0. `R1665 = P$1060*1000/(P$1053+P$1283+P$1396)` ergibt #DIV/0!. Das ist im untersuchten Zustand direkt eine 0/0-Situation für die betreffende Zone; daraus folgt noch kein Fehler in der aktiven Gesamtkennzahl.
3. **Leere Profilzuordnung:** Tab.Referenz!R81 ist leer; `R82 = MATCH(R81,Nutzungen!$E$78:$AW$78)` hat #N/A. Viele Referenztabellenfehler sind damit zumindest im unmittelbaren Ausdruck verständlich; die gesamte Fehlerfortpflanzung ist noch nicht dynamisch geprüft.
4. **Text in Rechenpfad:** CalC!E1987 hat den Cachewert `W`. S2081 enthält `E2077-E1987` und hat #VALUE!. Vor Übernahme muss geklärt werden, ob dies ein ungenutzter Hilfspfad oder eine tatsächlich benötigte Berechnung ist.
5. **Weitergereichte Anlagenfehler:** Tab.Wärme!D12 verweist auf AO62, das wiederum AO60 verwendet; diese Cachewerte enthalten #VALUE!. Den betroffenen Erzeugerpfad in den Vergleichstests gesondert aktivieren.
6. **Auffällige Bereichsgröße:** Eingabe!I4 prüft SUMIF mit `CalC!F1699:P1699`, verwendet im Ergebniszweig aber `CalC!F1699:P16704`. Der gespeicherte Text ist `38 kW`. Das ist eine belegte Bereichsabweichung, noch kein bewiesener falscher Leistungswert: Excel-SUMIF kann den tatsächlich ausgewerteten Summenbereich anhand des Kriterienbereichs dimensionieren. Ein Port muss diese Semantik klären, statt stillschweigend andere Dimensionen auszuwerten.

1.937 Formelzellen haben über openpyxl keinen numerischen/textuellen Cachewert (`None`). Das umfasst auch beabsichtigte Leertexte oder leere Ergebnisfelder und ist **nicht** als Zahl von 1.937 defekten Formeln zu verstehen.

Die Arbeitsmappe setzt `fullCalcOnLoad=True`; ein definierter Berechnungsabschluss ist nicht gespeichert. `calcMode` und Iterationseinstellungen sind nicht explizit gesetzt. Deshalb Cachewerte nicht als Nachweis einer vollständigen aktuellen Neuberechnung interpretieren.

## Technische Extraktion und Reproduzierbarkeit

- Zellinhalte mit openpyxl im Formelmodus und Datenmodus gelesen; VBA nicht geöffnet/ausgeführt.
- Neun durch die Normalisierung verbundener Zellen verdeckte Inhalte zusätzlich aus den Roh-XML-Zellen rekonstruiert; geteilte Formeln adressrichtig übersetzt. Das Inventar führt alle neun Fundstellen auf.
- Alle 1.671 Namensdefinitionen direkt aus workbook.xml gelesen, damit lokale Namen und Excel-Systemnamen nicht verloren gehen.
- VBA mit oletools statisch dekomprimiert; Quellen als Text gespeichert, nicht evaluiert.
- Bindungen aus Zeichnungs-/Formular-OOXML/VML ausgelesen. Zwei VML-Dateien sind für ElementTree nicht wohlgeformt: `vmlDrawing15.vml` und `vmlDrawing3.vml`. Ihre Bindungselemente wurden zusätzlich textuell extrahiert; die Ausnahmen sind im Inventar vermerkt.
- Die HTML-Datei enthält Daten als gzip/Base64, entpackt sie lokal über DecompressionStream und setzt Quelltexte als Text ein. Keine Netzabfrage, kein VBA-Interpreter und keine Formel-Ausführung.
- Zellkatalogschema: `[Adresse, Rohinhalt/Formel, Cachewert, Zelltyp, Zahlenformat, Kommentar, nicht_gesperrt]`. Reine Formatierungs-/Leerzellen sind bewusst nicht als belegte Zellen inventarisiert. Originale Grafik-/ActiveX-Binärdaten werden nicht visuell emuliert; Objektanzahlen/Bindungen sind erfasst.
- Bestandteile: `workbook-inventory.json` mit allen Metadaten/VBA-Quellen; `cell-catalog.json.gz` mit allen Zellrecords; `index.html` mit beiden vollständig eingebettet.

Analyse und Migrationskonzept legen damit die Grundlage für einen exakten Port, ersetzen aber noch nicht kontrollierte Excel-Referenzfälle, fachliche Abnahme und Browserfreigabe der späteren Rechenanwendung.

## Vollständige VBA-Modulliste

| Modul | Quelltextzeilen | Prozeduren |
|---|---:|---:|
| Tabelle6.cls | 8 | 0 |
| DieseArbeitsmappe.cls | 90 | 4 |
| Tabelle4.cls | 8 | 0 |
| Tabelle2.cls | 8 | 0 |
| Tabelle18.cls | 8 | 0 |
| Tabelle12.cls | 8 | 0 |
| Tabelle22.cls | 8 | 0 |
| Tabelle10.cls | 8 | 0 |
| Tabelle8.cls | 8 | 0 |
| Tabelle16.cls | 8 | 0 |
| Tabelle17.cls | 8 | 0 |
| Tabelle3.cls | 94 | 10 |
| Tabelle5.cls | 8 | 0 |
| Tabelle13.cls | 8 | 0 |
| Tabelle7.cls | 8 | 0 |
| Tabelle19.cls | 8 | 0 |
| Tabelle14.cls | 8 | 0 |
| Tabelle21.cls | 8 | 0 |
| Tabelle11.cls | 8 | 0 |
| Tabelle20.cls | 8 | 0 |
| Tabelle15.cls | 8 | 0 |
| Tabelle9.cls | 8 | 0 |
| Z_dropdownlisten.bas | 145 | 5 |
| Nutzungsprofil.frm | 56 | 3 |
| Onlinecheck.frm | 48 | 4 |
| Copy_Paste.bas | 441 | 10 |
| Diagramme.bas | 173 | 5 |
| Einlesen.bas | 220 | 4 |
| Einlesen_Bagatell.bas | 586 | 17 |
| Einstellungen_Gebäude.bas | 344 | 11 |
| Z_Ein_Ausblenden.bas | 606 | 36 |
| Z_Grafiken_Export.bas | 204 | 66 |
| Z_Hilfemakros.bas | 172 | 11 |
| Z_Data_Projektverwaltung.bas | 928 | 6 |
| Z_Texte.bas | 12 | 2 |
| Z_Data_Beispiel.bas | 352 | 1 |
| Ein_und_Ausblenden.frm | 44 | 6 |
| Z_Nutzungsprofil_kopieren.bas | 366 | 10 |
| Tabelle1.cls | 8 | 0 |
| Z_sprache.bas | 22 | 3 |
| Tabelle24.cls | 8 | 0 |
| Tabelle23.cls | 11 | 1 |
| Z_Data_Zielwerte.bas | 166 | 1 |
| Z_Zonendaten_delete.bas | 379 | 33 |
| Z_Variablen.bas | 30 | 0 |
| Tabelle25.cls | 8 | 0 |
| Tabelle26.cls | 8 | 0 |
| Anforderungen.bas | 8 | 1 |
| Tabelle27.cls | 13 | 0 |
| Tabelle28.cls | 12 | 1 |
| Z_Data_Referenz_laden.bas | 307 | 2 |
| Tabelle29.cls | 8 | 0 |
| Z_Data_delete.bas | 211 | 1 |
