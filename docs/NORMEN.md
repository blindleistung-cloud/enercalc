# Aktuelle Rechenverfahren und normative Nachweise

Quellen- und Bearbeitungsstand: **30. Oktober 2026**. Dies ist die aktuelle Zielvorgabe für die Migration; das frühere Konzept eines historischen EnEV-/LU-Nachbaus ist als Anwendungspfad abgelöst.

## Verbindlicher Arbeitsauftrag

Nur aktuell **anwendbare** Verfahren und Normfassungen verwenden. AMEV und die einschlägigen Anforderungen für Bundesbau/Bundeswehr berücksichtigen. Die ursprüngliche EnerCalC-Datei dient ausschließlich als historische Analyse-/Vergleichsquelle. Ihre Formeln, Auswahlwerte und Fehlerbehandlungen sind kein normativer Sollmaßstab.

„Aktuell anwendbar“ bedeutet nicht automatisch „zuletzt erschienene DIN-Ausgabe“: maßgeblich sind Rechtsverweis, Übergangsregelung, Einführung und der vereinbarte Projektkontext. Die abgerufenen öffentlichen §§ 20/21 nennen ausdrücklich **DIN V 18599:2018-09**. Damit wird diese Ausgabe nicht durch eine unbekannte neuere Veröffentlichung ersetzt und auch nicht eine alte Excel-Gleichungsnummer ungeprüft dieser Ausgabe zugeordnet.

## Wichtiger Quellenbefund: Rechtsstand und Übergang

Die unter dem historischen URL-Pfad `/geg/` öffentlich abgerufenen Texte heißen inzwischen **Gebäudemodernisierungsgesetz (GModG)**. Die Gesamtausgabe nennt als Änderungsstand Art. 4 des Gesetzes vom 23.07.2026 (BGBl. 2026 I Nr. 226). Die offizielle FIB-Fachseite bestätigt die Bezeichnung und nennt die Geltung seit 29.07.2026.

Die [FIB-Fachseite Energieausweise](https://www.fib-bund.de/Inhalt/Leitfaden/Energieausweise/) weist außerdem auf Änderungen am anzuwendenden Berechnungsregelwerk und an Energieausweisen **ab 01.01.2027** hin. Sie bezeichnet den alten Leitfaden GEG 2023 nur als teilweise weiter anwendbar. Deshalb wird weder dieser Leitfaden noch ein PDF mit älterem Titel pauschal zur aktuellen vollständigen Sollvorgabe.

Der derzeitige ausführbare Teilpfad ist nur dem geprüften Quellenstichtag **2026-10-30** zugeordnet. Abweichende Stichtage, insbesondere 2027, lösen eine sichtbare Sperre aus. Damit wird keine Aussage getroffen, dass alle Tabellenwerte am 01.01.2027 geändert werden; eine erneute Verfahrens-/Übergangsprüfung ist erforderlich.

## Quellenhierarchie und Anwendungsentscheidung

1. Gesetzliche Anforderungen und Übergangsvorschriften bestimmen Rechenweg und Bilanzgrenzen.
2. Die konkret in Bezug genommenen Normausgaben liefern die detaillierten Verfahren, Tabellen und Randbedingungen.
3. Einführungserlasse, aktuelle Bundesbau-/Bundeswehr-Festlegungen und Projektanforderungen legen ihre zusätzliche Verbindlichkeit, Zielwerte, Ausnahmen und Zuständigkeiten fest.
4. AMEV-Empfehlungen werden mit Titel, Ausgabe, Fundstelle und bestätigter Anwendbarkeit zugeordnet. Sie sind weder automatisch Gesetz noch automatisch für jede Bundeswehr-Bauaufgabe unverändert verbindlich.

Zusätzliche Auftraggeberanforderungen können strenger sein; Widersprüche oder Ausnahmen sind zu klären. Ein AMEV-Richtwert ersetzt keine vollständige Jahres-Energiebilanz. Eine Heiz-/Kühllast zur Anlagendimensionierung ist ein anderer Nachweis als ein monatlicher bzw. jährlicher Energiebedarf. Die Lebenszyklusbetrachtung im BNB ist ebenfalls von der Betriebsenergiebilanz zu unterscheiden.

## Bereits ausgeführt und technisch geprüft

- Ein modularer, DOM-unabhängiger JavaScript-Kern mit expliziten Einheiten und Definitionsbereichen liegt vor.
- Elf historische Auditbausteine sind mit **503 / 503** gespeicherten Zwischenwert-/Arithmetikfällen verglichen. Sie gehören **nicht** zum aktuellen Anwendungspfad und werden nicht als Normnachweis gewertet. Leere Zonen, Fehlerwerte und nicht unterstützte Definitionsbereiche sind keine bestandenen Fälle.
- Zehn Node-Testgruppen prüfen diese Vergleiche, unabhängige Identitäten/Grenzfälle, Einheiten, Quellenzuordnung und Sperren. Acht Python-Integritätstests betreffen die ursprüngliche statische Analyse.
- Zwei eng begrenzte aktuelle Bausteine sind auf Basis öffentlich belegter Rechtsquellen implementiert: **Endenergie → Primärenergie** und **Endenergie → Treibhausgasmenge** für den explizit geprüften Teilkatalog netzbezogener Strom, Erdgas, Heizöl und Holz.
- Die vorgegebene Endenergie wird dabei **nicht** aus Gebäudeparametern bestimmt; sie ist ein externer Eingangswert, dessen methodengerechte Bestimmung eine Voraussetzung bleibt. Fernwärme, KWK, Biomethan-Sonderfälle und weitere Konstellationen sind kein impliziter Bestandteil dieses Teilkatalogs.
- Der aktuelle Pfad verweigert alte Auditregeln, unbekannte Energieträger, nicht geprüfte Stichtage und ungültige Eingaben. Eine positive Einzelregelprüfung führt nicht zur Freigabe der Gebäude-Gesamtberechnung.

## Nachweismatrix für den aktuellen Zielpfad

Die Matrix benennt auch die Verträge der noch nicht implementierten Module. Offene Rechenregeln werden nicht mit pauschalen Ersatzannahmen befüllt. Die vollständigen strukturierten Datensätze stehen in [traceability.json](normative/traceability.json).

| Rechenregel | Eingang | Rechnung | Ausgang | Normbeleg / Quellenbedarf | Status |
|---|---|---|---|---|---|
| `zone-allocation` | Bauteilflächen je Orientierung und Randbedingung [m²]; Zonenflächen [m²], Gebäudetyp und zulässiges Zuweisungsverfahren | Verfahren nach Quellenklärung implementieren | Bauteilflächen je Zone und Randbedingung [m²]; Geprüfte Flächen-/Bilanzgrenzen | N01, N14 | Offen / Anwendung gesperrt |
| `profiles-climate` | Nutzungs-ID, Standort und Rechts-/Normstichtag; Aktueller freigegebener Profil-/Klima-Datensatz | Verfahren nach Quellenklärung implementieren | Nutzungs-/Betriebszeiten [h,d] und Solltemperaturen [°C]; Monatstemperaturen [°C], Strahlung [W/m²] und Luftmengenrandbedingungen | N03, N13, N14 | Offen / Anwendung gesperrt |
| `monthly-balance` | Geometrie und geprüfte Bauteil-/Lüftungsdaten; Aktuelle Nutzungs-/Klima-/Regelungsdaten, Quellen und Senken | Verfahren nach Quellenklärung implementieren | Nutzenergie Heizen/Kühlen je Zone/Monat [kWh]; Jahreswerte und eindeutig definierte spezifische Kennwerte [kWh/(m²a)] | N02, N03, N09, N12, N13, N14 | Offen / Anwendung gesperrt |
| `lighting-daylight` | Raum-/Fenstergeometrie, Verglasung, Verschattung und Nutzungszeiten; Aktuelle Leuchten-/Steuerungsdaten und Anforderungen an die Beleuchtung | Verfahren nach Quellenklärung implementieren | Beleuchtungs-Endenergie je Zone/Monat [kWh]; Zuordnung interner Wärmequellen zur thermischen Bilanz | N05, N12 | Offen / Anwendung gesperrt |
| `ventilation-system` | Nutzungsabhängige Luftmengen [m³/h], Betrieb [h], WRG und Druck-/Ventilatorparameter; Einführung der AMEV-Anforderungen und projektspezifische Bundeswehr-Randbedingungen | Verfahren nach Quellenklärung implementieren | Hilfs-/Ventilatorenergie [kWh]; Wärme-/Kältebeiträge mit definierter Bilanzgrenze | N06, N09, N12, N14 | Offen / Anwendung gesperrt |
| `cooling-system` | Nutzkältebedarf [kWh], System, Temperaturen und Betriebsweise; Aktuelle Effizienz-/Verteilungs-/Hilfsenergiekennwerte sowie eingeführte AMEV-Anforderungen | Verfahren nach Quellenklärung implementieren | Endenergie nach Energieträger [kWh]; Rückkühl-/Hilfsenergie und nachvollziehbare Anlagenverluste | N06, N12 | Offen / Anwendung gesperrt |
| `heat-dhw-system` | Heiz-/TWW-Nutzenergie [kWh], Speicher/Verteilung/Übergabe und Erzeuger; Betrieb, Temperaturniveau, Solarthermie und aktuelle Randbedingungen | Verfahren nach Quellenklärung implementieren | Endenergie nach Energieträger [kWh]; Hilfsenergie, Verluste und zu berücksichtigende Gewinne | N07, N12, N14 | Offen / Anwendung gesperrt |
| `renewable-balance` | Monats-/Zeitreihen der Erzeugung [kWh], Bedarf [kWh] und Speicherzustände; Aktuell zulässiges Anrechnungsverfahren und projektspezifische Versorgungskonfiguration | Verfahren nach Quellenklärung implementieren | Erzeugung, Eigenverbrauch, Bezug, Einspeisung und Verluste [kWh]; Methodengerechte Anrechnung; keine doppelte Energiegutschrift | N08, N13 | Offen / Anwendung gesperrt |
| `current-primary` | Bereits bestimmter Endenergiebedarf [kWh]; Energieträger []; Geprüfter Quellenstichtag [] | Qp = Qend · fp,nren | Umgerechnete Menge [kWh] | § 22 Abs. 1 in Verbindung mit Anlage 4; geprüfter Teilkatalog; Tabellenzeilen im explizit geprüften Teilkatalog | Einzelbaustein belegt, keine Gesamtfreigabe |
| `current-emissions` | Bereits bestimmter Endenergiebedarf [kWh]; Energieträger []; Geprüfter Quellenstichtag [] | m_CO₂eq [kg] = Qend [kWh] · f [g/kWh] / 1000 | Umgerechnete Menge [kg CO₂-Äq.] | Anlage 9 Nr. 1a und Nr. 3; geprüfter Teilkatalog; Tabellenzeilen im explizit geprüften Teilkatalog | Einzelbaustein belegt, keine Gesamtfreigabe |

### Öffentlich belegte Einzelregeln

Die Primärenergieumrechnung nutzt den nicht erneuerbaren Primärenergiefaktor nach [§ 22 Abs. 1](https://www.gesetze-im-internet.de/geg/__22.html) in Verbindung mit [Anlage 4](https://www.gesetze-im-internet.de/geg/anlage_4.html). Die Treibhausgasumrechnung nutzt [Anlage 9 Nr. 1a und Nr. 3](https://www.gesetze-im-internet.de/geg/anlage_9.html): Endenergie je Energieträger mal entsprechender Faktor; die Anwendung gibt Kilogramm statt Gramm aus. Der isolierte Teilkatalog und die Einheitenrechnung sind direkt gegen die abgerufenen Texte/Tabellen geprüft.

Das bestätigt weder eine vorgelagerte Bedarfsermittlung nach §§ 20/21 noch sämtliche Bedingungen eines Energieausweises, eine fachplanerische Gesamtfreigabe oder die Einhaltung zusätzlicher Bundeswehr-Anforderungen. Die Prüfstatuswerte sind entsprechend auf den Einzelbaustein begrenzt.

## Nachgewiesene Unterschiede zum Excelstand

| Größe | Excel | Öffentlicher Tabellenwert | Einheit | Quelle |
|---|---:|---:|---|---|
| Primärenergie netzbezogener Strom | 1.8 | 1.8 | kWh_prim/kWh_end | [Tabelle Nr. 9](https://www.gesetze-im-internet.de/geg/anlage_4.html) |
| Treibhausgase netzbezogener Strom | 617 | 560 | g CO₂-Äq./kWh_end | [Nr. 3, Tabelle Nr. 12](https://www.gesetze-im-internet.de/geg/anlage_9.html) |
| Treibhausgase Erdgas | 277 | 240 | g CO₂-Äq./kWh_end | [Nr. 3, Tabelle Nr. 2](https://www.gesetze-im-internet.de/geg/anlage_9.html) |
| Treibhausgase Heizöl | 277 | 310 | g CO₂-Äq./kWh_end | [Nr. 3, Tabelle Nr. 1](https://www.gesetze-im-internet.de/geg/anlage_9.html) |
| Treibhausgase Holz | 14.33333333 | 20 | g CO₂-Äq./kWh_end | [Nr. 3, Tabelle Nr. 11](https://www.gesetze-im-internet.de/geg/anlage_9.html) |
| Treibhausgase Verdrängungsstrom | 617 | 860 | g CO₂-Äq./kWh_end | [Nr. 3, Tabelle Nr. 14](https://www.gesetze-im-internet.de/geg/anlage_9.html) |

Diese Werte werden nicht als Korrektur einer historischen EnEV-/LU-Bilanz interpretiert. Sie zeigen, weshalb die neue Anwendung einen eigenen aktuellen Energieträgerkatalog benötigt. Besonders Heizöl und Erdgas dürfen nicht aus dem gemeinsamen Excel-Sammelfaktor abgeleitet werden. Die Zulässigkeit einer Energiegutschrift ist zusätzlich zum Faktor selbst zu prüfen.

## AMEV / Bundesbau: auffindbare Originalquellen

Die fünf AMEV-PDFs und die RBBau wurden heruntergeladen, statisch nach relevanten Begriffen durchsucht und mit Hash und PDF-Seitenfundstellen erfasst. Das ist **keine vollständige fachliche Prüfung sämtlicher darin enthaltener Empfehlungen**. In das Repository werden eigene Zusammenfassungen, bibliografische Angaben und Fundstellen übernommen, keine Vollkopien der AMEV-Publikationen.

| Quelle | Auf der Originalseite angebotene Fassung | Bedeutung für die Migration |
|---|---|---|
| [AMEV Wärmeversorgungsanlagen – Teil 1](https://www.amev-online.de/AMEVInhalt/Planen/Maschinenbau-und-Versorgungstechnik/Waermeversorgungsanlagen/WVA-Teil1_2021.pdf) | 2021 | Planung/Auslegung von Wärmeversorgung; Jahresbedarf und Auslegungs-Heizlast getrennt prüfen. |
| [AMEV RLT-Anlagen](https://www.amev-online.de/AMEVInhalt/Planen/Maschinenbau-und-Versorgungstechnik/RLT-Anlagen/RLT-Anlagen_Stand_01.07.2023.pdf) | Stand 01.07.2023 | Außenluft, Betrieb, Ventilatorleistung, WRG und Auslegungsdaten; konkrete Nutzungsfälle und Einführung fehlen. |
| [AMEV Kälte](https://www.amev-online.de/AMEVInhalt/Planen/Maschinenbau-und-Versorgungstechnik/Kaelte_2026/Kaelte_2026.pdf) | 2026 (ersetzt Kälte 2017 laut Fachseite) | Kühllastreduktion, Systemwahl, Erzeugung und Betrieb; keine pauschale Gleichsetzung mit der energetischen Monatsbilanz. |
| [AMEV Beleuchtung](https://www.amev-online.de/AMEVInhalt/Planen/Elektrotechnik/Beleuchtung/Beleuchtung_2023_Stand_03-25.pdf) | Ausgabe 2023, Stand 03/2025 | LED, Beleuchtungsplanung und energetische Betriebsführung; Projektanforderungen und DIN-Rechenverfahren getrennt führen. |
| [AMEV Gebäudeautomation](https://www.amev-online.de/AMEVInhalt/Planen/Gebaeudeautomation/GA/2023-09-11_AMEV_GA2023.pdf) | 2023 | Automation und Betriebsanforderungen einschließlich Einfluss auf energetische Randbedingungen; projektbezogene Festlegungen nötig. |
| [RBBau](https://www.fib-bund.de/Inhalt/Richtlinien/RBBau/RBBau_Onlinefassung_Stand_15.07.2026.pdf) | Stand 15.07.2026 | Bundesbau-Verfahren und Zuständigkeiten; zusätzliche bzw. abweichende Regelungen im militärischen Bau können erforderlich sein. |
| [FIB: Ausstellen von Energieausweisen](https://www.fib-bund.de/Inhalt/Leitfaden/Energieausweise/) | Öffentliche Fachseite, Abruf 30.10.2026 | Nennt GModG seit 29.07.2026, Änderungen des Berechnungsregelwerks zum 01.01.2027 sowie nur teilweise weiter anwendbaren Leitfaden GEG 2023. Einführungserlasse werden im Bereich FIB intern verortet. |
| [FIB: Leitfaden Nachhaltiges Bauen / BNB](https://www.fib-bund.de/Inhalt/Leitfaden/NachhaltigesBauen/) | Öffentliche Fachseite, Abruf 30.10.2026 | Nachhaltigkeitsbewertung, Lebenszyklus und Zielvereinbarung sind von der Gebäude-Betriebsenergiebilanz zu trennen. Je Nutzung/Bauaufgabe einschlägige BNB-Version und Einführung bestimmen. |
| [FIB intern – Einführungserlasse und Grundsatzdokumente](https://www.fachinfoboerse.de/) | Zugriff / projektspezifische Freigabe fehlt | Die öffentliche FIB verweist für Einführungserlasse und weitere Grundsatzdokumente auf diesen zugangsbeschränkten Bereich. Keine Anmeldung, keine Umgehung und keine Beschaffung interner Bundeswehr-Dokumente vorgenommen. |

Die PDF-Seiten in [client-sources.json](normative/client-sources.json) sind physische PDF-Seitennummern ab 1, nicht zwingend die gedruckte Seitennummer. Beispiele: AMEV RLT nennt SFP auf PDF-Seiten 31/32; AMEV Beleuchtung verweist auf DIN 18599 auf PDF-Seiten 68/82; die RBBau nennt Standardsetzungen auf PDF-Seite 8 und militärische Regelungsmöglichkeiten auf PDF-Seite 31. Ein Suchtreffer ist ein Einstiegspunkt, noch keine normative Gleichung mit bestätigtem Anwendungsbereich.

Die öffentliche FIB verweist für Einführungserlasse und weitere Grundsatzdokumente auf **FIB intern**. Diese fachlich freigegebenen Unterlagen liegen hier nicht vor. Es wurden keine Zugangssperren umgangen und keine internen Bundeswehr-Unterlagen beschafft. Die RBBau allein ersetzt solche fachlichen Vorgaben nicht.

## Gezielt noch benötigte Quellen / Entscheidungen

Für den nächsten vollständigen Gebäuderechendurchstich haben **N01–N04 und N12–N14** Vorrang. Benötigt werden die aktuell anwendbaren Verfahrenstexte mit Definitionskontext, Tabellen, Anhängen und Bedingungen sowie die für den vorgesehenen Bundeswehr-Anwendungsfall fachlich freigegebenen Einführungen/Anforderungen. Zugangsdaten sind dafür nicht erforderlich und sollen nicht im Chat übermittelt werden.

### N01 · P1 — DIN V 18599-1:2018-09

System-/Bilanzgrenzen, Flächenbezüge, Zonierung, Hüllflächenzuweisung und Anhang D; Abgleich mit der vom Excelverfahren verwendeten älteren Fassung.

Status: `source-required`. Betroffene Rechenregeln: heated-area, direct-envelope, zone-allocation, apply-factor.

### N02 · P1 — DIN V 18599-2:2018-09

Vollständige Regelkontexte für Transmission, Erdreich, Infiltration/Lüftung, Zeitkonstanten, Bilanztemperaturen, Ausnutzungsgrade und Heiz-/Kühlbilanz; Definitionen, Bedingungen und Tabellen einschließen. Excel-Gleichungsnummern sind noch keiner Ausgabe sicher zugeordnet.

Status: `source-required`. Betroffene Rechenregeln: transmission, air-transfer, heat-capacity, thermal-response, heating-utilization, heating-part, monthly-balance.

### N03 · P1 — DIN V 18599-10:2018-09

Nutzungsprofile einschließlich Teilbetriebszeiten/Sollwerte sowie Klima-/Strahlungsdaten und Zuordnung der Profilvarianten.

Status: `source-required`. Betroffene Rechenregeln: profiles-climate, air-transfer, monthly-balance.

### N04 · P1 — DIN 4108-4:2017-03; DIN EN ISO 6946:2008-04; einschlägiges Fensterverfahren

Vom öffentlich abgerufenen § 20 Abs. 6 ausdrücklich genannte U-Wert-Verfahren und Randbedingungen. Für den Fenster-Randverbund zusätzlich anzuwendende Ausgabe/Abschnitt von DIN EN ISO 10077-1 prüfen. Keine Normgleichheit aus dem pauschalen Excel-Faktor 3 m⁻¹ ableiten.

Status: `source-required`. Betroffene Rechenregeln: window-u, transmission.

### N05 · P2 — DIN V 18599-4:2018-09

Tageslichtbereiche, Transparenz-/Verbauungsindizes, Kontrollsysteme und Monats-/Jahresverfahren der Beleuchtung.

Status: `source-required`. Betroffene Rechenregeln: lighting-daylight.

### N06 · P2 — DIN V 18599-3, -6 und -7:2018-09

Je Gebäudetyp einschlägige Luftaufbereitung, WRG, Ventilatoren, Kälteerzeugung, Betriebszeiten und Anlagenkopplungen.

Status: `source-required`. Betroffene Rechenregeln: ventilation-system, cooling-system.

### N07 · P2 — DIN V 18599-5 und -8:2018-09

Wärmeerzeugung, Übergabe/Verteilung/Speicherung, TWW und Solarthermie samt Tabellen, Hilfsenergie und Kopplungen.

Status: `source-required`. Betroffene Rechenregeln: heat-dhw-system.

### N08 · P2 — DIN V 18599-9:2018-09 und einschlägige gesetzliche Anrechnungsregeln

PV, KWK, Erzeugungsanrechnung, Export-/Verdrängungsstrom und Speicher. Wind-/Speichermodell des Exceltools auf normative Grundlage oder Autorenvereinfachung prüfen.

Status: `source-required`. Betroffene Rechenregeln: renewable-balance.

### N09 · P2 — DIN V 18599-11:2018-09

Gebäudeautomation und betriebliche Korrekturen; Zuordnung zu den Blattparametern.

Status: `source-required`. Betroffene Rechenregeln: monthly-balance, ventilation-system.

### N10 · P3 — Autoren-/Verfahrensdokumentation EnerCalC 6.1.177 und ältere verwendete DIN-Fassungen

Nur für die historische Vergleichsanalyse, keine Sollvorgabe und keine Voraussetzung zur Übernahme aktueller Verfahren. Hüllflächenvereinfachung, Faktor 3 m⁻¹ beim Fenster, gerundeter Glasanteil, Wärmebrücken-Flächenbezug, 1-%-Begrenzung des Ausnutzungsgrads, Wind/Speicher/KWK sowie Begründung gemischter Normstände.

Status: `reference-only`. Betroffene Rechenregeln: window-u, transmission, heating-utilization, zone-allocation, renewable-balance.

### N11 · P3 — Kontrollierter Excel-Neuberechnungsexport

Nur für die historische Vergleichsanalyse, keine Sollvorgabe und keine Voraussetzung zur Übernahme aktueller Verfahren. Exakte Eingabestände, aktive Regelwerk-/Profilindizes, erforderliche VBA-Schritte sowie Monats-/Zonen-/Jahres-Zwischenwerte. Der vorhandene Cache allein ist keine dynamische Excel-Referenz.

Status: `reference-only`. Betroffene Rechenregeln: monthly-balance, zone-allocation, renewable-balance.

### N12 · P1 — AMEV – aktuell einschlägige Ausgaben und Einführung

Ausgaben und projektspezifische Verbindlichkeit für Heizung, RLT, Kälte, Beleuchtung, Gebäudeautomation und Energie-/Betriebsführung dokumentieren; konkrete Rechenregeln, Planungswerte und Abweichungen einzeln zuordnen.

Status: `applicability-open`. Betroffene Rechenregeln: monthly-balance, ventilation-system, cooling-system, heat-dhw-system, lighting-daylight.

### N13 · P1 — Bundesbau – RBBau, aktuelle Energie-/Nachhaltigkeitsvorgaben und Einführungserlasse

Öffentlich verfügbare Fassungen mit Stichtag prüfen; Anwendbarkeit für Neubau, Erweiterung, Sanierung und jeweilige Gebäudenutzung sowie verbindliche energetische Zielwerte/Methoden bestätigen.

Status: `applicability-open`. Betroffene Rechenregeln: profiles-climate, monthly-balance, renewable-balance.

### N14 · P1 — Bundeswehr – aktuelle baufachliche/projektspezifische Vorgaben

Für den vorgesehenen Anwendungsfall freigegebene fachliche Vorgaben einschließlich Ausgabe, Geltungsbereich, Betriebs-/Nutzungsprofilen, Abweichungen und Vorrangregeln bereitstellen. Nicht aus allgemeinen Bundesbau-Seiten oder dem Excel-Beispiel ableiten.

Status: `source-required`. Betroffene Rechenregeln: profiles-climate, zone-allocation, monthly-balance, ventilation-system, heat-dhw-system.

## Wie eine Rechenregel freigegeben wird

Jede Regel erhält eine eindeutige ID, Eingaben samt Einheit/Definitionsbereich, Rechenweg, Ausgaben und verwendete Normausgabe/Fundstelle. Referenzwerte und normative Belege sind unterschiedliche Datenfelder. Eine Excel-Gleichungsbeschriftung, ein Suchtreffer oder ein bestandener Zahlenvergleich darf keinen normativen Prüfstatus automatisch setzen.

Für eine komplette fachliche Freigabe sind zusätzlich erforderlich: bestätigte Anwendbarkeit für Gebäudetyp/Bauaufgabe/Stichtag, vollständig geprüfte Verfahrenszweige, herkunftsgeprüfte aktuelle Kennwerte, unabhängige Beispiele, Einheiten-/Erhaltungstests und die dokumentierte fachliche Abnahme. Die Gesamtfreigabe steht derzeit auf **offen**.

Code: [core/engine.js](../core/engine.js). Prüfprotokoll: [check-results.json](normative/check-results.json). Öffentliche Text-/Tabellenquellen mit Hash: [sources.json](normative/sources.json). Historische Beispiele: [core-cases.json](../tests/fixtures/core-cases.json).
