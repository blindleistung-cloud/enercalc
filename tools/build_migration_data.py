"""Prepare traceability and independent Excel-cache fixtures from the audit.
No normative approval is inferred from an Excel label or cache comparison.
"""
import gzip,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
W=json.loads((ROOT/'docs/workbook-inventory.json').read_text())
C=json.loads(gzip.decompress((ROOT/'docs/cell-catalog.json.gz').read_bytes()))
D={s:{r[0]:r for r in rows} for s,rows in C.items()}

def value(s,a):return D[s][a][2]
def numeric(x):return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def binding(s,a):return {'sheet':s,'cell':a,'formula':D[s][a][1],'savedValue':value(s,a)}
def plain(s,a):return {'sheet':s,'cell':a}

requirements=[
 dict(id='N01',priority='P1',document='DIN V 18599-1:2018-09',needed='System-/Bilanzgrenzen, Flächenbezüge, Zonierung, Hüllflächenzuweisung und Anhang D; Abgleich mit der vom Excelverfahren verwendeten älteren Fassung.',rules=['heated-area','direct-envelope','zone-allocation','apply-factor']),
 dict(id='N02',priority='P1',document='DIN V 18599-2:2018-09',needed='Vollständige Regelkontexte für Transmission, Erdreich, Infiltration/Lüftung, Zeitkonstanten, Bilanztemperaturen, Ausnutzungsgrade und Heiz-/Kühlbilanz; Definitionen, Bedingungen und Tabellen einschließen. Excel-Gleichungsnummern sind noch keiner Ausgabe sicher zugeordnet.',rules=['transmission','air-transfer','heat-capacity','thermal-response','heating-utilization','heating-part','monthly-balance']),
 dict(id='N03',priority='P1',document='DIN V 18599-10:2018-09',needed='Nutzungsprofile einschließlich Teilbetriebszeiten/Sollwerte sowie Klima-/Strahlungsdaten und Zuordnung der Profilvarianten.',rules=['profiles-climate','air-transfer','monthly-balance']),
 dict(id='N04',priority='P1',document='DIN 4108-4:2017-03; DIN EN ISO 6946:2008-04; einschlägiges Fensterverfahren',needed='Vom öffentlich abgerufenen § 20 Abs. 6 ausdrücklich genannte U-Wert-Verfahren und Randbedingungen. Für den Fenster-Randverbund zusätzlich anzuwendende Ausgabe/Abschnitt von DIN EN ISO 10077-1 prüfen. Keine Normgleichheit aus dem pauschalen Excel-Faktor 3 m⁻¹ ableiten.',rules=['window-u','transmission']),
 dict(id='N05',priority='P2',document='DIN V 18599-4:2018-09',needed='Tageslichtbereiche, Transparenz-/Verbauungsindizes, Kontrollsysteme und Monats-/Jahresverfahren der Beleuchtung.',rules=['lighting-daylight']),
 dict(id='N06',priority='P2',document='DIN V 18599-3, -6 und -7:2018-09',needed='Je Gebäudetyp einschlägige Luftaufbereitung, WRG, Ventilatoren, Kälteerzeugung, Betriebszeiten und Anlagenkopplungen.',rules=['ventilation-system','cooling-system']),
 dict(id='N07',priority='P2',document='DIN V 18599-5 und -8:2018-09',needed='Wärmeerzeugung, Übergabe/Verteilung/Speicherung, TWW und Solarthermie samt Tabellen, Hilfsenergie und Kopplungen.',rules=['heat-dhw-system']),
 dict(id='N08',priority='P2',document='DIN V 18599-9:2018-09 und einschlägige gesetzliche Anrechnungsregeln',needed='PV, KWK, Erzeugungsanrechnung, Export-/Verdrängungsstrom und Speicher. Wind-/Speichermodell des Exceltools auf normative Grundlage oder Autorenvereinfachung prüfen.',rules=['renewable-balance']),
 dict(id='N09',priority='P2',document='DIN V 18599-11:2018-09',needed='Gebäudeautomation und betriebliche Korrekturen; Zuordnung zu den Blattparametern.',rules=['monthly-balance','ventilation-system']),
 dict(id='N10',priority='P1',document='Autoren-/Verfahrensdokumentation EnerCalC 6.1.177 und ältere verwendete DIN-Fassungen',needed='Hüllflächenvereinfachung, Faktor 3 m⁻¹ beim Fenster, gerundeter Glasanteil, Wärmebrücken-Flächenbezug, 1-%-Begrenzung des Ausnutzungsgrads, Wind/Speicher/KWK sowie Begründung gemischter Normstände.',rules=['window-u','transmission','heating-utilization','zone-allocation','renewable-balance']),
 dict(id='N11',priority='P1',document='Kontrollierter Excel-Neuberechnungsexport',needed='Exakte Eingabestände, aktive Regelwerk-/Profilindizes, erforderliche VBA-Schritte sowie Monats-/Zonen-/Jahres-Zwischenwerte. Der vorhandene Cache allein ist keine dynamische Excel-Referenz.',rules=['monthly-balance','zone-allocation','renewable-balance']),
]
for r in requirements:r['status']='source-required'

rules=[];fixtures=[]
def add(id,title,expression,inputs,outputs,refs,limits,fields,reqs,claim):
 sample=inputs
 rule=dict(id=id,title=title,expression=expression,sampleInput=sample,outputs=outputs,workbook=[binding(s,a) for s,a in refs],
           inputFields=fields,scopeLimit=limits,requirements=reqs,
           workbookReportedReference=claim,normativeReview=dict(status='source-required',edition=None,evidence=[],reviewer=None),
           technicalValidation=dict(kind='not-yet-run',caseCount=0))
 rules.append(rule);return rule

def field(path,label,unit='',s=None,a=None):return dict(path=path,label=label,unit=unit,source=plain(s,a) if s else None)
def output(key,label,unit):return dict(key=key,label=label,unit=unit)
def case(id,inputs,expected,label,source=None):
 fixtures.append(dict(rule=id,inputs=inputs,expected=expected,label=label,source=source,referenceKind='saved-excel-cache' if source else 'independent-arithmetic'))

zones=[dict(area=z['area'],heated=z['heated']) for z in W['zones']]
r=add('heated-area','Energiebezugsfläche beheizter Zonen','A_EBF = Σ A_zone für beheizte Zonen',dict(zones=zones),[output('area','Beheizte Bezugsfläche','m²'),output('totalArea','Gesamte Zonenfläche','m²')],[('Eingabe','D85')],
 'Reproduziert die Auswahl beheizter Zonen. Die normative Gleichsetzung mit anderen Flächenbezügen ist nicht freigegeben.',
 [field(f'zones.{i}.{k}',f'Zone {i+1}: '+('Fläche' if k=='area' else 'beheizt'),'m²' if k=='area' else '', 'Eingabe' if k=='area' else 'DATA',f'{chr(69+i)}'+('83' if k=='area' else '151')) for i in range(len(zones)) for k in ['area','heated']],['N01'],'Eingabe!D85 / SUMIF')
case(r['id'],r['sampleInput'],{'area':821,'totalArea':1079},'Beispiel EBF und Gesamtfläche',plain('Eingabe','D85'))

inputs=dict(facadeGross=value('Eingabe','D34'),facadeWindows=sum(value('Eingabe',f'{c}25') for c in 'EFGH'),groundWalls=value('Eingabe','D38'),roofGross=value('Eingabe','I28'),roofWindows=value('Eingabe','I36'),floor=value('Eingabe','I28'),volume=value('Eingabe','D42'))
fields=[field(k,l,u,'Eingabe',a) for k,l,u,a in [('facadeGross','Fassaden brutto','m²','D34'),('facadeWindows','Fassadenfenster gesamt','m²','D36'),('groundWalls','Wände gegen Erdreich/unbeheizt','m²','D38'),('roofGross','Dach brutto (Beispiel-Flachdach)','m²','I28'),('roofWindows','Dachfenster','m²','I36'),('floor','Boden','m²','I28'),('volume','Beheiztes Volumen','m³','D42')]]
add('direct-envelope','Direkte Hüllflächensummen','A = A_Fenster + A_Wand,opak + A_Wand,Erdreich + A_Dach,opak + A_Boden; A/V',inputs,[output('walls','Opake Außenwände','m²'),output('windows','Fenster gesamt','m²'),output('roof','Opakes Dach','m²'),output('area','Hüllfläche','m²'),output('compactness','Kompaktheit A/V','m⁻¹')],[('Eingabe','D41'),('Eingabe','D43')],
 'Direkte Flächensummen, kein Ersatz für das vereinfachte Fassadenverfahren, die Zonenzuweisung oder eine Prüfung der normativen Bilanzgrenze.',fields,['N01'],'Eingabe!D36:D43')
case('direct-envelope',inputs,dict(area=W['snapshot']['envelope'],compactness=value('Eingabe','D43'),walls=443.1,windows=250.9,roof=294),'Direkte Hülle des gespeicherten Beispiels',plain('Eingabe','D41'))

inputs=dict(glassArea=.75,frameArea=.25,ug=1.1,uf=value('Eingabe','E56'),edgeLength=3,psi=value('Eingabe','E57'))
fields=[field(k,l,u,s,a) for k,l,u,s,a in [('glassArea','Glasfläche des Modellfensters','m²',None,None),('frameArea','Rahmenfläche des Modellfensters','m²',None,None),('ug','Ug','W/(m²K)','CalC','F1037'),('uf','Uf','W/(m²K)','Eingabe','E56'),('edgeLength','Glasrandlänge des Modellfensters','m',None,None),('psi','Randverbund ψ','W/(mK)','Eingabe','E57')]]
add('window-u','Fenster-U-Wert mit expliziter Geometrie','Uw = (Ag·Ug + Af·Uf + lg·ψ) / (Ag + Af)',inputs,[output('u','Fenster-U-Wert','W/(m²K)')],[('Eingabe','E58'),('Konst','D167')],
 'Der Beispielwert bildet FR=0,75 und den Excel-Zuschlag 3·ψ über ein Modellfenster von 1 m² ab. Die Randlänge 3 m ist eine ausdrücklich gesetzte Modellannahme, keine geprüfte normative Standardgeometrie.',fields,['N04','N10'],'Eingabe!E58: FR·Ug + (1−FR)·Uf + 3·ψ')
case('window-u',inputs,dict(u=value('Eingabe','E58')),'Legacy-Modellfenster mit FR=0,75 und l/A=3 m⁻¹',plain('Eingabe','E58'))

components=[dict(area=value('CalC',f'F{1017+i}'),u=value('CalC',f'F{1045+i}'),reduction=value('CalC',f'E{1017+i}')) for i in range(7)]
fields=[field(f'components.{i}.{k}',f'{value("CalC",f"B{1017+i}")}: {label}',unit,'CalC',f'{col}{(1017+i if k!="u" else 1045+i)}') for i in range(7) for k,label,unit,col in [('area','Fläche','m²','F'),('u','U-Wert','W/(m²K)','F'),('reduction','Reduktion','1','E')]]+[field('bridgeDeltaU','Wärmebrückenzuschlag','W/(m²K)','CalC','F1052')]
add('transmission','Transmissionsleitwert aus zugewiesenen Bauteilen','H_T = Σ(A_i·U_i·F_i) + ΔU_WB·Σ(A_i·F_i)',dict(components=components,bridgeDeltaU=value('CalC','F1052')),[output('coefficient','Transmissionsleitwert','W/K'),output('base','Bauteilanteil','W/K'),output('bridge','Wärmebrückenanteil','W/K'),output('weightedArea','Reduzierte Bezugsfläche','m²')],[('CalC','F1053')],
 'Übernimmt bereits zugewiesene CalC-Bauteile. Hüllflächenzuweisung und der reduzierte Flächenbezug des pauschalen Wärmebrückenzuschlags sind gesondert normativ zu prüfen. Die direkte Hülle wird hier nicht automatisch umverteilt.',fields,['N01','N02','N04','N10'],'CalC!F1053; DIN-Abschnitt aus Datei nicht editionssicher')

add('heat-capacity','Wirksame Wärmespeicherkapazität','C_wirk = c_wirk · A / 1000',dict(specificCapacity=value('CalC','F1059'),area=value('CalC','F327')),[output('capacity','Wirksame Kapazität','kWh/K')],[('CalC','F1060')],
 'Umrechnung mit vorgegebenem c_wirk. Die Einstufung leicht/mittel/schwer und die zulässige Bezugsfläche bleiben prüfpflichtig.',[field('specificCapacity','c_wirk','Wh/(m²K)','CalC','F1059'),field('area','Bezugsfläche','m²','CalC','F327')],['N02'],'CalC-Zeile 1056 nennt Kapitel 6.7.1')

add('air-transfer','Luftwechselbezogener Wärmeleitwert','H_v = n · V · ρc',dict(airChanges=value('CalC','F1282'),volume=value('CalC','F328'),airCapacity=value('Konst','D176')),[output('coefficient','Lüftungsleitwert','W/K')],[('CalC','F1283')],
 'Nur Multiplikation der expliziten Randbedingungen. Keine eigenständige Bestimmung von Infiltration, n₅₀-Umrechnung, Mindestaußenluft, WRG oder Anlagenbetrieb.',[field('airChanges','Wirksamer Luftwechsel','h⁻¹','CalC','F1282'),field('volume','Luftvolumen','m³','CalC','F328'),field('airCapacity','Volumetrische Wärmekapazität','Wh/(m³K)','Konst','D176')],['N02','N03'],'CalC!C1283 meldet H_v_inf (58), Ausgabe ungeprüft')

add('thermal-response','Zeitkonstante und numerischer Parameter','τ = C_wirk · 1000 / H; a = a₀ + τ/τ₀',dict(capacity=value('CalC','F1060'),transfer=value('CalC','F2004'),a0=value('Konst','D150'),tau0=value('Konst','D151')),[output('tau','Zeitkonstante','h'),output('a','Numerischer Parameter','1')],[('CalC','F2005'),('CalC','F2006')],
 'H, a₀ und τ₀ werden explizit übergeben. Bei H=0 wird ein Fehler gemeldet, statt wie Excel pauschal 0 zu setzen. Zugehörige Komponenten und Normbedingungen sind offen.',[field('capacity','Kapazität','kWh/K','CalC','F1060'),field('transfer','Gesamt-Wärmetransferkoeffizient','W/K','CalC','F2004'),field('a0','a₀','1','Konst','D150'),field('tau0','τ₀','h','Konst','D151')],['N02'],'CalC: τ (22,136), a (142) – aus Dateibeschriftung, nicht gegen Normtext geprüft')

add('heating-utilization','Ausnutzungsgrad im Heizfall','η = (1−γ^a)/(1−γ^(a+1)); bei γ=1: a/(a+1); Excel-Begrenzung separat',dict(gamma=value('CalC','F2033'),a=value('CalC','F2006'),limitThreshold=.01),[output('raw','Ausnutzungsgrad roh','1'),output('limited','Ausnutzungsgrad begrenzt','1')],[('CalC','F2034'),('CalC','F2035')],
 'Definierter numerisch stabiler Grenzfall γ=1. Die 1-%-Begrenzung und die Ermittlung von γ bei nichtpositiven Senken sind nicht normativ bestätigt.',[field('gamma','Gewinn-/Verlustverhältnis γ','1','CalC','F2033'),field('a','a','1','CalC','F2006'),field('limitThreshold','Excel-Begrenzungsschwelle','1',None,None)],['N02','N10'],'CalC: Gleichungen (140),(141),(144); Ausgabe nicht bestätigt')

add('heating-part','Heizwärme einer Nutzungs-Teilperiode','q_h = max(0, (Q_sink − η·Q_source) · d / A)',dict(losses=value('CalC','F2015'),gains=value('CalC','F2032'),utilization=value('CalC','F2035'),days=value('CalC','F1988'),area=value('CalC','F327')),[output('specificHeat','Heizwärme Teilperiode','kWh/m²')],[('CalC','F2036')],
 'Nur Nutzungs-Teilperiode mit übergebenen Senken, Quellen und Tagen. Nichtnutzungszeit, gespeicherte Wärme, Temperaturen, Kühlung und Gesamtmonatsbilanz fehlen ausdrücklich.',[field(k,l,u,'CalC',a) for k,l,u,a in [('losses','Senken','kWh/d','F2015'),('gains','Quellen','kWh/d','F2032'),('utilization','Ausnutzungsgrad','1','F2035'),('days','Gewichtete Nutzungstage','d','F1988'),('area','Zonenfläche','m²','F327')]],['N02','N03'],'CalC!F2036; Q_sink (11), Q_source (16) sind vorgelagerte Berechnungen')

add('apply-factor','Energetische Umrechnung mit explizitem Faktor','Q_result = Q_input · f',dict(energy=value('DATA','A7'),factor=value('DATA','F7')),[output('energy','Umgerechnete Energie','kWh/(m²a)')],[('DATA','C7')],
 'Der Beispiel-Gesamtfaktor enthält Anlagen- und Primärenergiewirkungen. Ein geprüfter Multiplikationskern bestätigt nicht die Herkunft oder Zulässigkeit des Faktors und keine Gesamtbilanz.',[field('energy','Nutzenergie Heizen','kWh/(m²a)','DATA','A7'),field('factor','Excel-Gesamtfaktor','1','DATA','F7')],['N01','N07'],'DATA!C7, Gesamtbilanz!P411')
case('apply-factor',rules[-1]['sampleInput'],dict(energy=value('DATA','C7')),'Heizen Nutzenergie zu Primärenergie mit vorgegebenem Gesamtfaktor',plain('DATA','C7'))

add('emissions','Endenergie in Treibhausgasmenge umrechnen','m_CO₂eq [kg] = Q_end [kWh] · f [g/kWh] / 1000',dict(energy=1000,factor=560),[output('emissions','Treibhausgasmenge','kg CO₂-Äq.')],[],
 'Öffentlich belegter Tabellenwert für netzbezogenen Strom und isolierte Multiplikation. Keine Prüfung des vorgelagerten Endenergiebedarfs, der Bilanzgrenze oder der gesetzlichen Gesamtanwendung.',[field('energy','Endenergie','kWh'),field('factor','Emissionsfaktor','g CO₂-Äq./kWh')],['N01'],'Öffentlich abgerufene Anlage 9 Nr. 1a / 3, Tabellenzeile 12')
case('emissions',rules[-1]['sampleInput'],dict(emissions=560),'Einheitenrechnung 1000 kWh × 560 g/kWh /1000; kein Excelfall')

# Independent saved intermediate cases across both cores, all populated zones/months.
for sn in ['CalC','CalC_Referenz']:
 for col in 'FGHIJKLMNOP':
  area=value(sn,f'{col}327')
  def v(row):return value(sn,f'{col}{row}')
  comp=[dict(area=v(1017+i),u=v(1045+i),reduction=value(sn,f'E{1017+i}')) for i in range(7)]
  if all(numeric(x) for item in comp for x in item.values()) and numeric(v(1053)):
   case('transmission',dict(components=comp,bridgeDeltaU=v(1052)),dict(coefficient=v(1053)),sn+' '+col+' H_T',plain(sn,f'{col}1053'))
  if all(numeric(v(r)) for r in [1059,1060,327]):case('heat-capacity',dict(specificCapacity=v(1059),area=area),dict(capacity=v(1060)),sn+' '+col+' C',plain(sn,f'{col}1060'))
  if all(numeric(v(r)) for r in [1282,328,1283]):case('air-transfer',dict(airChanges=v(1282),volume=v(328),airCapacity=value('Konst','D176')),dict(coefficient=v(1283)),sn+' '+col+' H_v',plain(sn,f'{col}1283'))
  for month in range(12):
   base=1984+month*165
   if numeric(v(base+20)) and v(base+20)>0 and all(numeric(v(r)) for r in [1060,base+21,base+22]):
    case('thermal-response',dict(capacity=v(1060),transfer=v(base+20),a0=value('Konst','D150'),tau0=value('Konst','D151')),dict(tau=v(base+21),a=v(base+22)),f'{sn} {col} Monat {month+1} τ/a',plain(sn,f'{col}{base+21}'))
   if all(numeric(v(r)) for r in [base+22,base+49,base+50,base+51]) and v(base+22)>0 and v(base+49)>=0:
    # Excel's Q_sink=0 branch is a different rule, so do not feed it to eta(gamma,a).
    if v(base+31)!=0:
     case('heating-utilization',dict(gamma=v(base+49),a=v(base+22),limitThreshold=.01),dict(raw=v(base+50),limited=v(base+51)),f'{sn} {col} Monat {month+1} η',plain(sn,f'{col}{base+50}'))
   if numeric(area) and area>0 and all(numeric(v(r)) for r in [base+31,base+48,base+51,base+4,base+52]) and 0<=v(base+51)<=1 and v(base+48)>=0:
    case('heating-part',dict(losses=v(base+31),gains=v(base+48),utilization=v(base+51),days=v(base+4),area=area),dict(specificHeat=v(base+52)),f'{sn} {col} Monat {month+1} Nutzungs-Teilbilanz',plain(sn,f'{col}{base+52}'))

blocked=[
 ('zone-allocation','Hüllflächen und Bilanzgrenzen der Zonen',['N01','N10','N11'],'DATA!E104:O115; CalC!F299:P345'),
 ('profiles-climate','Nutzungs- und Klimarandbedingungen',['N03'],'Nutzungen, Wetterdaten, Tab.Listen'),
 ('monthly-balance','Vollständige Heiz-/Kühl-Monatsbilanz',['N02','N03','N09','N11'],'CalC!F1984:P3960 und Monatsaggregation'),
 ('lighting-daylight','Tageslicht und Beleuchtung',['N05'],'CalC bis Zeile 1008'),
 ('ventilation-system','Lüftungsanlage, WRG und Hilfsenergie',['N06','N09'],'CalC, Tab.Listen, Gesamtbilanz'),
 ('cooling-system','Kälteerzeugung und Verteilung',['N06'],'Tab.Kälte'),
 ('heat-dhw-system','Heizung, Warmwasser und Solarthermie',['N07'],'Tab.Wärme, Tab.WW, Tab.Solar'),
 ('renewable-balance','PV, WEA, KWK, Speicher und Stromanrechnung',['N08','N10','N11'],'Tab.PV, Tab.WEA, Gesamtbilanz, nZEB-Bilanzen'),
]
for id,title,reqs,ref in blocked:
 rules.append(dict(id=id,title=title,expression=None,sampleInput=None,inputFields=[],outputs=[],workbook=[],scopeLimit='Noch nicht migriert. Benötigte Verfahrens-/Normbelege müssen vor der Freigabe geklärt werden.',requirements=reqs,workbookReportedReference=ref,normativeReview=dict(status='source-required',edition=None,evidence=[],reviewer=None),technicalValidation=dict(kind='not-implemented',caseCount=0)))

sources=json.loads((ROOT/'docs/normative/sources.json').read_text())
pub={s['id']:s for s in sources}
def table(id,n):return next(r for r in pub[id]['table'] if r['number']==n)
comparisons=[
 dict(label='Primärenergie netzbezogener Strom',workbook=value('Faktoren','I10'),public=table('geg4',9)['value'],unit='kWh_prim/kWh_end',source='geg4',item='Tabelle Nr. 9',workbookCell=plain('Faktoren','I10'),finding='Einzelner Tabellenwert stimmt überein; keine Freigabe des gesamten Bilanzverfahrens.'),
 dict(label='Treibhausgase netzbezogener Strom',workbook=value('Faktoren','J10'),public=table('geg9',12)['value'],unit='g CO₂-Äq./kWh_end',source='geg9',item='Nr. 3, Tabelle Nr. 12',workbookCell=plain('Faktoren','J10'),finding='Abweichung: historischer Dateifaktor darf nicht in das aktuelle Rechtsprofil kopiert werden.'),
 dict(label='Treibhausgase Erdgas',workbook=value('Faktoren','J7'),public=table('geg9',2)['value'],unit='g CO₂-Äq./kWh_end',source='geg9',item='Nr. 3, Tabelle Nr. 2',workbookCell=plain('Faktoren','J7'),finding='Excel gruppiert Heizöl/Erdgas; diese gesetzliche Tabellenzeile gilt nur für Erdgas.'),
 dict(label='Treibhausgase Heizöl',workbook=value('Faktoren','J7'),public=table('geg9',1)['value'],unit='g CO₂-Äq./kWh_end',source='geg9',item='Nr. 3, Tabelle Nr. 1',workbookCell=plain('Faktoren','J7'),finding='Gleicher Excel-Sammelfaktor, anderer gesetzlicher Energieträger; getrennte IDs erforderlich.'),
 dict(label='Treibhausgase Holz',workbook=value('Faktoren','J8'),public=table('geg9',11)['value'],unit='g CO₂-Äq./kWh_end',source='geg9',item='Nr. 3, Tabelle Nr. 11',workbookCell=plain('Faktoren','J8'),finding='Historische Gruppierung Holz/Pellets und Rechtsprofil getrennt führen.'),
 dict(label='Treibhausgase Verdrängungsstrom',workbook=value('Faktoren','J12'),public=table('geg9',14)['value'],unit='g CO₂-Äq./kWh_end',source='geg9',item='Nr. 3, Tabelle Nr. 14',workbookCell=plain('Faktoren','J12'),finding='Anrechnungsverfahren und Zulässigkeit des Verdrängungsfaktors zusätzlich prüfen.'),
]
registry=dict(schemaVersion=1,title='Rechenkern und normative Nachweise',sourceWorkbookSha256=W['sha256'],
 targetProfile=dict(status='selection-pending',workbook='EnerCalC 6.1.177, gespeicherte Auswahl EnEV 2016; Formelquellen editionsgemischt',candidate='Deutsches Rechtsprofil mit ausdrücklich in Bezug genommener DIN V 18599:2018-09; noch nicht freigegeben',publicLawName='GModG laut abgerufener konsolidierter Fassung; URL-Pfad weiterhin /geg/'),
 rules=rules,requirements=requirements,publicSources=sources,factorComparisons=comparisons,
 overall=dict(normativeReady=False,note='Cachegleichheit, rechnerische Plausibilität und normative Freigabe sind voneinander unabhängig. Kein Gesamtenergiebedarfs- oder Energieausweisnachweis.'))
for rule in rules:
 count=sum(f['rule']==rule['id'] for f in fixtures)
 if count:
  rule['technicalValidation']=dict(kind='fixtures-prepared',caseCount=count)
  first=next(f for f in fixtures if f['rule']==rule['id'])
  rule['sampleExpected']=first['expected']
  rule['sampleReferenceKind']=first['referenceKind']

(ROOT/'tests/fixtures/core-cases.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
print(len(rules),'rules;',len(fixtures),'saved/arithmetic cases;',len(requirements),'source requirements.')

# Current-only target: historical leaves remain reference-audit code and can
# never be called as an operational fallback by runCurrent.
for r in rules:
 r['executionMode']='reference-only' if r['sampleInput'] is not None else 'current-blocked'
for n in requirements:
 if n['id'] in ['N10','N11']:
  n['priority']='P3';n['status']='reference-only';n['needed']='Nur für die historische Vergleichsanalyse, keine Sollvorgabe und keine Voraussetzung zur Übernahme aktueller Verfahren. '+n['needed']
requirements.extend([
 dict(id='N12',priority='P1',document='AMEV – aktuell einschlägige Ausgaben und Einführung',needed='Ausgaben und projektspezifische Verbindlichkeit für Heizung, RLT, Kälte, Beleuchtung, Gebäudeautomation und Energie-/Betriebsführung dokumentieren; konkrete Rechenregeln, Planungswerte und Abweichungen einzeln zuordnen.',status='applicability-open',rules=['monthly-balance','ventilation-system','cooling-system','heat-dhw-system','lighting-daylight']),
 dict(id='N13',priority='P1',document='Bundesbau – RBBau, aktuelle Energie-/Nachhaltigkeitsvorgaben und Einführungserlasse',needed='Öffentlich verfügbare Fassungen mit Stichtag prüfen; Anwendbarkeit für Neubau, Erweiterung, Sanierung und jeweilige Gebäudenutzung sowie verbindliche energetische Zielwerte/Methoden bestätigen.',status='applicability-open',rules=['profiles-climate','monthly-balance','renewable-balance']),
 dict(id='N14',priority='P1',document='Bundeswehr – aktuelle baufachliche/projektspezifische Vorgaben',needed='Für den vorgesehenen Anwendungsfall freigegebene fachliche Vorgaben einschließlich Ausgabe, Geltungsbereich, Betriebs-/Nutzungsprofilen, Abweichungen und Vorrangregeln bereitstellen. Nicht aus allgemeinen Bundesbau-Seiten oder dem Excel-Beispiel ableiten.',status='source-required',rules=['profiles-climate','zone-allocation','monthly-balance','ventilation-system','heat-dhw-system']),
])
registry['targetProfile']=dict(status='current-only',deploymentReady=False,asOf='2026-10-30',
 mandate='Nur aktuell anwendbare Verfahren, AMEV und Bundesbau/Bundeswehr berücksichtigen. Keine historischen EnEV-/LU-Rechenprofile als Anwendungspfad.',
 workbook='Nur historische Vergleichsquelle: EnerCalC 6.1.177; keine fachliche Sollvorgabe.',
 statutoryReference='Öffentlich abgerufene §§ 20/21 nennen ausdrücklich DIN V 18599:2018-09. Gesetzlich referenzierte Ausgabe und neueste Normveröffentlichung sind getrennt zu prüfen.',
 publicLawName='GModG laut abgerufener konsolidierter Fassung, Änderungsstand 23.07.2026; URL-Pfad weiterhin /geg/.')
registry['currentFactors']=[dict(id=id,label=label,primary=table('geg4',pn)['value'],co2=table('geg9',cn)['value'],primarySource=dict(id='geg4',tableNumber=pn),co2Source=dict(id='geg9',tableNumber=cn))
 for id,label,pn,cn in [('grid-electricity','Netzbezogener Strom',9,12),('natural-gas','Erdgas',2,2),('heating-oil','Heizöl',1,1),('wood','Holz',8,11)]]
for id,title,expr,key,unit,sourceId,section in [
 ('current-primary','Primärenergie: aktueller Einzelenergieträger','Qp = Qend · fp,nren','primaryEnergy','kWh','geg22','§ 22 Abs. 1 in Verbindung mit Anlage 4; geprüfter Teilkatalog'),
 ('current-emissions','Treibhausgase: aktueller Einzelenergieträger','m_CO₂eq [kg] = Qend [kWh] · f [g/kWh] / 1000','emissions','kg CO₂-Äq.','geg9','Anlage 9 Nr. 1a und Nr. 3; geprüfter Teilkatalog')]:
 rules.append(dict(id=id,title=title,executionMode='current-leaf',expression=expr,
  sampleInput=dict(energy=1000,carrier='grid-electricity',asOf='2026-10-30'),
  inputFields=[field('energy','Bereits bestimmter Endenergiebedarf','kWh'),dict(path='carrier',label='Energieträger',unit='',type='carrier',source=None)],
  outputs=[output(key,'Umgerechnete Menge',unit)],workbook=[],requirements=[],
  scopeLimit='Isolierte gesetzliche Umrechnung mit öffentlich belegten Faktoren. Der Endenergiebedarf muss bereits nach dem einschlägigen Verfahren bestimmt sein; dessen Ermittlung, weitere Energieträger/Sonderfälle und die Gebäude-/Bundeswehr-Gesamtprüfung sind nicht freigegeben.',
  workbookReportedReference='Kein Übernehmen des alten Excel-Sammelfaktors. Aktuelle Energieträger-IDs und öffentliche Originalquelle.',
  normativeReview=dict(status='verified',scope='leaf-only',edition='Öffentlich abgerufene konsolidierte Fassung, Stand 23.07.2026 / Abruf 30.10.2026',
   evidence=[dict(source=sourceId,section=section),dict(source='geg4' if id=='current-primary' else 'geg9',section='Tabellenzeilen im explizit geprüften Teilkatalog')],
   reviewer='Codex – direkter Text-/Tabellenabgleich, nur angegebener Einzelbaustein'),
  technicalValidation=dict(kind='public-source-and-unit-tests',caseCount=4)))
registry['overall']['note']='Nur aktuell anwendbare Verfahren als Ziel. Öffentlich belegte Umrechnungsbausteine sind eng begrenzt geprüft; die Gebäude-Gesamtberechnung und projektspezifische AMEV-/Bundesbau-/Bundeswehr-Anwendung bleiben offen.'

print('Current-only target applied: 2 narrow current leaves, 11 historical audit leaves, 8 blocked current modules.')

registry['targetProfile']['reviewRequiredFrom']='2027-01-01'
registry['targetProfile']['editionPolicy']='Nur aktuell anwendbar, nicht pauschal neueste DIN-Ausgabe: Rechtsverweis, Übergang, Einführung und Auftraggeberanforderungen bestimmen die verwendbare Fassung.'
for r in rules:
 if r['executionMode']=='current-leaf':
  r['inputFields'].append(dict(path='asOf',label='Geprüfter Quellenstichtag',unit='',type='date',source=None))
client_path=ROOT/'docs/normative/client-sources.json'
if client_path.exists():registry['clientSources']=json.loads(client_path.read_text())
else:registry['clientSources']=[]


registry['requiredCurrentRules']=[r['id'] for r in rules if r['executionMode']!='reference-only']

contracts={'zone-allocation': (['Bauteilflächen je Orientierung und Randbedingung [m²]', 'Zonenflächen [m²], Gebäudetyp und zulässiges Zuweisungsverfahren'], ['Bauteilflächen je Zone und Randbedingung [m²]', 'Geprüfte Flächen-/Bilanzgrenzen']), 'profiles-climate': (['Nutzungs-ID, Standort und Rechts-/Normstichtag', 'Aktueller freigegebener Profil-/Klima-Datensatz'], ['Nutzungs-/Betriebszeiten [h,d] und Solltemperaturen [°C]', 'Monatstemperaturen [°C], Strahlung [W/m²] und Luftmengenrandbedingungen']), 'monthly-balance': (['Geometrie und geprüfte Bauteil-/Lüftungsdaten', 'Aktuelle Nutzungs-/Klima-/Regelungsdaten, Quellen und Senken'], ['Nutzenergie Heizen/Kühlen je Zone/Monat [kWh]', 'Jahreswerte und eindeutig definierte spezifische Kennwerte [kWh/(m²a)]']), 'lighting-daylight': (['Raum-/Fenstergeometrie, Verglasung, Verschattung und Nutzungszeiten', 'Aktuelle Leuchten-/Steuerungsdaten und Anforderungen an die Beleuchtung'], ['Beleuchtungs-Endenergie je Zone/Monat [kWh]', 'Zuordnung interner Wärmequellen zur thermischen Bilanz']), 'ventilation-system': (['Nutzungsabhängige Luftmengen [m³/h], Betrieb [h], WRG und Druck-/Ventilatorparameter', 'Einführung der AMEV-Anforderungen und projektspezifische Bundeswehr-Randbedingungen'], ['Hilfs-/Ventilatorenergie [kWh]', 'Wärme-/Kältebeiträge mit definierter Bilanzgrenze']), 'cooling-system': (['Nutzkältebedarf [kWh], System, Temperaturen und Betriebsweise', 'Aktuelle Effizienz-/Verteilungs-/Hilfsenergiekennwerte sowie eingeführte AMEV-Anforderungen'], ['Endenergie nach Energieträger [kWh]', 'Rückkühl-/Hilfsenergie und nachvollziehbare Anlagenverluste']), 'heat-dhw-system': (['Heiz-/TWW-Nutzenergie [kWh], Speicher/Verteilung/Übergabe und Erzeuger', 'Betrieb, Temperaturniveau, Solarthermie und aktuelle Randbedingungen'], ['Endenergie nach Energieträger [kWh]', 'Hilfsenergie, Verluste und zu berücksichtigende Gewinne']), 'renewable-balance': (['Monats-/Zeitreihen der Erzeugung [kWh], Bedarf [kWh] und Speicherzustände', 'Aktuell zulässiges Anrechnungsverfahren und projektspezifische Versorgungskonfiguration'], ['Erzeugung, Eigenverbrauch, Bezug, Einspeisung und Verluste [kWh]', 'Methodengerechte Anrechnung; keine doppelte Energiegutschrift'])}
for rule in rules:
 if rule['id'] in contracts:
  rule['inputContract'],rule['outputContract']=contracts[rule['id']]
for rule in rules:
 if rule['executionMode']=='current-blocked':
  rule['requirements']=sorted({r['id'] for r in requirements if rule['id'] in r['rules'] and r['status']!='reference-only'},key=lambda x:int(x[1:]))
registry['requirementsHierarchy']=['Gesetz und Übergang','In Bezug genommene Normausgabe','Einführung/Auftraggeber und Projektfestlegungen','AMEV/weitere Planungsempfehlungen mit geklärter Verbindlichkeit']
(ROOT/'docs/normative/traceability.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
