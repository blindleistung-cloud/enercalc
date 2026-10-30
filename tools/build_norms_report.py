"""Render the current-source matrix as a readable review document."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
N=json.loads((ROOT/'docs/normative/traceability.json').read_text())
checks=json.loads((ROOT/'docs/normative/check-results.json').read_text())
clients=N['clientSources']
client_rows='\n'.join(f"| [{s['title']}]({s['url']}) | {s['edition']} | {s['relevance']} |" for s in clients)
requirements='\n\n'.join(f"### {r['id']} · {r['priority']} — {r['document']}\n\n{r['needed']}\n\nStatus: `{r['status']}`. Betroffene Rechenregeln: {', '.join(r['rules'])}." for r in N['requirements'])
comparisons='\n'.join(f"| {r['label']} | {r['workbook']:.10g} | {r['public']:.10g} | {r['unit']} | [{r['item']}]({next(s['url'] for s in N['publicSources'] if s['id']==r['source'])}) |" for r in N['factorComparisons'])
rows=[]
for r in N['rules']:
 if r['executionMode']=='reference-only':continue
 inputs='; '.join(r.get('inputContract') or [f"{i['label']} [{i['unit']}]" for i in r['inputFields']])
 outputs='; '.join(r.get('outputContract') or [f"{i['label']} [{i['unit']}]" for i in r['outputs']])
 evidence='; '.join(e['section'] for e in r['normativeReview']['evidence']) if r['executionMode']=='current-leaf' else ', '.join(r['requirements'])
 rows.append(f"| `{r['id']}` | {inputs} | {r['expression'] or 'Verfahren nach Quellenklärung implementieren'} | {outputs} | {evidence} | {'Einzelbaustein belegt, keine Gesamtfreigabe' if r['executionMode']=='current-leaf' else 'Offen / Anwendung gesperrt'} |")
text=f'''# Aktuelle Rechenverfahren und normative Nachweise

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
- Elf historische Auditbausteine sind mit **{checks['passed']} / {checks['total']}** gespeicherten Zwischenwert-/Arithmetikfällen verglichen. Sie gehören **nicht** zum aktuellen Anwendungspfad und werden nicht als Normnachweis gewertet. Leere Zonen, Fehlerwerte und nicht unterstützte Definitionsbereiche sind keine bestandenen Fälle.
- Zehn Node-Testgruppen prüfen diese Vergleiche, unabhängige Identitäten/Grenzfälle, Einheiten, Quellenzuordnung und Sperren. Acht Python-Integritätstests betreffen die ursprüngliche statische Analyse.
- Zwei eng begrenzte aktuelle Bausteine sind auf Basis öffentlich belegter Rechtsquellen implementiert: **Endenergie → Primärenergie** und **Endenergie → Treibhausgasmenge** für den explizit geprüften Teilkatalog netzbezogener Strom, Erdgas, Heizöl und Holz.
- Die vorgegebene Endenergie wird dabei **nicht** aus Gebäudeparametern bestimmt; sie ist ein externer Eingangswert, dessen methodengerechte Bestimmung eine Voraussetzung bleibt. Fernwärme, KWK, Biomethan-Sonderfälle und weitere Konstellationen sind kein impliziter Bestandteil dieses Teilkatalogs.
- Der aktuelle Pfad verweigert alte Auditregeln, unbekannte Energieträger, nicht geprüfte Stichtage und ungültige Eingaben. Eine positive Einzelregelprüfung führt nicht zur Freigabe der Gebäude-Gesamtberechnung.

## Nachweismatrix für den aktuellen Zielpfad

Die Matrix benennt auch die Verträge der noch nicht implementierten Module. Offene Rechenregeln werden nicht mit pauschalen Ersatzannahmen befüllt. Die vollständigen strukturierten Datensätze stehen in [traceability.json](normative/traceability.json).

| Rechenregel | Eingang | Rechnung | Ausgang | Normbeleg / Quellenbedarf | Status |
|---|---|---|---|---|---|
{chr(10).join(rows)}

### Öffentlich belegte Einzelregeln

Die Primärenergieumrechnung nutzt den nicht erneuerbaren Primärenergiefaktor nach [§ 22 Abs. 1](https://www.gesetze-im-internet.de/geg/__22.html) in Verbindung mit [Anlage 4](https://www.gesetze-im-internet.de/geg/anlage_4.html). Die Treibhausgasumrechnung nutzt [Anlage 9 Nr. 1a und Nr. 3](https://www.gesetze-im-internet.de/geg/anlage_9.html): Endenergie je Energieträger mal entsprechender Faktor; die Anwendung gibt Kilogramm statt Gramm aus. Der isolierte Teilkatalog und die Einheitenrechnung sind direkt gegen die abgerufenen Texte/Tabellen geprüft.

Das bestätigt weder eine vorgelagerte Bedarfsermittlung nach §§ 20/21 noch sämtliche Bedingungen eines Energieausweises, eine fachplanerische Gesamtfreigabe oder die Einhaltung zusätzlicher Bundeswehr-Anforderungen. Die Prüfstatuswerte sind entsprechend auf den Einzelbaustein begrenzt.

## Nachgewiesene Unterschiede zum Excelstand

| Größe | Excel | Öffentlicher Tabellenwert | Einheit | Quelle |
|---|---:|---:|---|---|
{comparisons}

Diese Werte werden nicht als Korrektur einer historischen EnEV-/LU-Bilanz interpretiert. Sie zeigen, weshalb die neue Anwendung einen eigenen aktuellen Energieträgerkatalog benötigt. Besonders Heizöl und Erdgas dürfen nicht aus dem gemeinsamen Excel-Sammelfaktor abgeleitet werden. Die Zulässigkeit einer Energiegutschrift ist zusätzlich zum Faktor selbst zu prüfen.

## AMEV / Bundesbau: auffindbare Originalquellen

Die fünf AMEV-PDFs und die RBBau wurden heruntergeladen, statisch nach relevanten Begriffen durchsucht und mit Hash und PDF-Seitenfundstellen erfasst. Das ist **keine vollständige fachliche Prüfung sämtlicher darin enthaltener Empfehlungen**. In das Repository werden eigene Zusammenfassungen, bibliografische Angaben und Fundstellen übernommen, keine Vollkopien der AMEV-Publikationen.

| Quelle | Auf der Originalseite angebotene Fassung | Bedeutung für die Migration |
|---|---|---|
{client_rows}

Die PDF-Seiten in [client-sources.json](normative/client-sources.json) sind physische PDF-Seitennummern ab 1, nicht zwingend die gedruckte Seitennummer. Beispiele: AMEV RLT nennt SFP auf PDF-Seiten 31/32; AMEV Beleuchtung verweist auf DIN 18599 auf PDF-Seiten 68/82; die RBBau nennt Standardsetzungen auf PDF-Seite 8 und militärische Regelungsmöglichkeiten auf PDF-Seite 31. Ein Suchtreffer ist ein Einstiegspunkt, noch keine normative Gleichung mit bestätigtem Anwendungsbereich.

Die öffentliche FIB verweist für Einführungserlasse und weitere Grundsatzdokumente auf **FIB intern**. Diese fachlich freigegebenen Unterlagen liegen hier nicht vor. Es wurden keine Zugangssperren umgangen und keine internen Bundeswehr-Unterlagen beschafft. Die RBBau allein ersetzt solche fachlichen Vorgaben nicht.

## Gezielt noch benötigte Quellen / Entscheidungen

Für den nächsten vollständigen Gebäuderechendurchstich haben **N01–N04 und N12–N14** Vorrang. Benötigt werden die aktuell anwendbaren Verfahrenstexte mit Definitionskontext, Tabellen, Anhängen und Bedingungen sowie die für den vorgesehenen Bundeswehr-Anwendungsfall fachlich freigegebenen Einführungen/Anforderungen. Zugangsdaten sind dafür nicht erforderlich und sollen nicht im Chat übermittelt werden.

{requirements}

## Wie eine Rechenregel freigegeben wird

Jede Regel erhält eine eindeutige ID, Eingaben samt Einheit/Definitionsbereich, Rechenweg, Ausgaben und verwendete Normausgabe/Fundstelle. Referenzwerte und normative Belege sind unterschiedliche Datenfelder. Eine Excel-Gleichungsbeschriftung, ein Suchtreffer oder ein bestandener Zahlenvergleich darf keinen normativen Prüfstatus automatisch setzen.

Für eine komplette fachliche Freigabe sind zusätzlich erforderlich: bestätigte Anwendbarkeit für Gebäudetyp/Bauaufgabe/Stichtag, vollständig geprüfte Verfahrenszweige, herkunftsgeprüfte aktuelle Kennwerte, unabhängige Beispiele, Einheiten-/Erhaltungstests und die dokumentierte fachliche Abnahme. Die Gesamtfreigabe steht derzeit auf **offen**.

Code: [core/engine.js](../core/engine.js). Prüfprotokoll: [check-results.json](normative/check-results.json). Öffentliche Text-/Tabellenquellen mit Hash: [sources.json](normative/sources.json). Historische Beispiele: [core-cases.json](../tests/fixtures/core-cases.json).
'''
(ROOT/'docs/NORMEN.md').write_text(text)
print('Wrote docs/NORMEN.md with',len(rows),'current-path contracts and',len(clients),'client-source entries.')
