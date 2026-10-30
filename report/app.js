'use strict';
let W, CELLS, N, CHECKS;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const nf=new Intl.NumberFormat('de-DE'), dec=new Intl.NumberFormat('de-DE',{maximumFractionDigits:2});
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=x=>typeof x==='number'?dec.format(x):String(x??'∅');
const cacheError=x=>typeof x==='string'&&/^#(?:DIV\/0!|N\/A|VALUE!|REF!|NUM!|NAME\?|NULL!)/.test(x);
const sum=xs=>xs.reduce((a,b)=>a+b,0);
const labels={overview:'Überblick',workbook:'Arbeitsmappe',logic:'Excel-Rechenwege',vba:'VBA & Abläufe',migration:'Migrationskonzept',calculate:'Rechenbausteine',norms:'Normnachweise'};
const roles={Language:'Sprachkatalog DE / EN',LOG:'Versionshistorie',Start:'Startseite und Quellen',Eingabe:'Gebäude, Zonen und Anlagen',Gesamtbilanz:'Monats-, Jahres- und CO₂-Bilanzen',Gesamtbilanz_Referenz:'Referenzbilanz',
 'nZEB-Bilanzen':'Vergleich mehrerer Bilanzmethoden',Anforderungen:'Grenzwerte und Referenzanforderungen',Faktoren:'Primärenergie- und Umweltfaktoren',TEK:'Teilenergiekennwerte',Wetterdaten:'Monatliche Klimadaten',Nutzungen:'Nutzungsprofile und Zeitpläne',Sankey:'Darstellung von Energieflüssen',
 'Tab.Sankey':'Datenaufbereitung für Energieflüsse',CalC:'Zonenbezogener Rechenkern',CalC_Referenz:'Referenz-Rechenkern',DATA:'Vermittlung, Auswahlwerte und Aggregation',Konst:'Konstanten und Kennwerttabellen','Tab.Referenz':'Regelwerkabhängige Referenzparameter','Tab.Rating':'Klassifizierung',
 'Tab.Listen':'Auswahllisten und Steuerzellen','Tab.Grafiken':'Diagrammdaten','Tab.Grafiken2':'Weitere Diagrammdaten','Tab.Wärme':'Wärmeerzeugung und Übergabe','Tab.WW':'Trinkwarmwasser','Tab.Kälte':'Kälteerzeugung und Hilfsenergie','Tab.Solar':'Solarthermische Erzeugung','Tab.PV':'Photovoltaik und Eigenstrom','Tab.WEA':'Windenergie'};
const visible=s=>s==='visible'?'sichtbar':s==='hidden'?'ausgeblendet':'sehr verborgen';
const errCount=s=>sum(Object.values(s.errors));
let view='overview',tab='cells',sheet='Eingabe',query='',scope='sheet',kind='all',page=0,moduleIndex=0,vbaQuery='',detail=null;
const perPage=80;
const source=(s,a)=>`<button class="source-link" data-source="${esc(s)}" data-address="${esc(a)}">${esc(s)}!${esc(a)}</button>`;
const intro=(k,title,text)=>`<div class="page-intro"><div class="eyebrow">${k}</div><h1>${title}</h1><p>${text}</p></div>`;
function heroArt(){return `<svg viewBox="0 0 440 270" fill="none" aria-hidden="true"><defs><pattern id="dots" x="0" y="0" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#a7b399" opacity=".5"/></pattern></defs><rect x="20" y="12" width="400" height="240" fill="url(#dots)"/><path d="M104 112C160 112 134 177 208 177M111 172C155 172 157 177 208 177M229 127L229 156M246 178C300 178 275 105 326 105M246 178C305 178 281 225 329 225" stroke="#95ad80" stroke-width="1.5" stroke-dasharray="4 4"/><g transform="translate(42 58) rotate(-7 50 75)"><rect width="100" height="127" rx="6" fill="#fdfef8" stroke="#becbad"/><path d="M0 25H100M25 25V127M50 25V127M75 25V127M0 46H100M0 67H100M0 88H100M0 109H100" stroke="#dce5d0"/><rect width="100" height="25" rx="6" fill="#b3c5a0"/><text x="12" y="17" font-family="sans-serif" font-size="9" fill="#3f5b32">EnerCalC.xlsm</text><rect x="26" y="47" width="23" height="19" fill="#dfe8ce"/><rect x="51" y="68" width="23" height="19" fill="#e9ddbf"/></g><g transform="translate(175 75)"><rect width="107" height="52" rx="7" fill="#fff" stroke="#c0d1b1"/><text x="15" y="21" font-family="monospace" font-size="10" fill="#577344">ƒ(x)</text><text x="15" y="38" font-family="sans-serif" font-size="9" fill="#7d9071">Formeln & Daten</text></g><g transform="translate(182 156)"><rect width="90" height="44" rx="6" fill="#3c6047"/><text x="14" y="27" font-family="monospace" font-size="10" fill="#e7efd9">{ Modell }</text></g><g transform="translate(307 66) rotate(5 50 65)"><rect width="106" height="137" rx="6" fill="#fff" stroke="#c3d0b5"/><path d="M0 22H106" stroke="#d8e1cf"/><circle cx="10" cy="11" r="2" fill="#aabd95"/><circle cx="18" cy="11" r="2" fill="#ced9bf"/><circle cx="26" cy="11" r="2" fill="#e1e8d6"/><rect x="12" y="34" width="81" height="32" rx="3" fill="#e9efdc"/><rect x="12" y="76" width="36" height="46" rx="3" fill="#f2f5eb"/><path d="M58 119H95M61 112V98M73 112V86M85 112V94" stroke="#8ba479" stroke-width="6"/><path d="M21 45H62M21 53H45" stroke="#b1c397" stroke-width="3"/></g><rect x="309" y="216" width="92" height="27" rx="13" fill="#dce7cf"/><text x="323" y="233" font-family="monospace" font-size="9" fill="#5f7c49">index.html →</text></svg>`;}
function overview(){
 const hidden=W.sheets.filter(s=>s.state!=='visible').length;
 const calc=W.sheets.filter(s=>s.name==='CalC'||s.name==='CalC_Referenz').reduce((a,s)=>a+s.formulas,0);
 const groups=[['Zonen-Rechenkerne',calc],['Gesamtbilanzen',11741],['Diagrammaufbereitung',11292],['Übrige Tabellen',W.formulaCount-calc-11741-11292]];
 return `<section class="hero"><div class="hero-copy"><div class="eyebrow">REVERSE ENGINEERING · MIGRATION</div><h1>Von der Zelle<br>zum System.</h1><p>Excel verstehen und aktuelle Verfahren nachvollziehbar migrieren. Mit Quellenbezug, offenem Prüfstatus und eigenen Offline-Rechenbausteinen.</p><div class="hero-buttons"><a class="button primary" href="#workbook">Arbeitsmappe erkunden <span>→</span></a><a class="button" href="#migration">Migrationskonzept →</a></div></div><div class="hero-art">${heroArt()}</div></section>
 <section class="stats" aria-label="Bestandsaufnahme">
 ${[[W.sheets.length,'Tabellenblätter',`3 sichtbar · ${hidden} verborgen`,'▦'],[W.formulaCount,'Zellformeln',`${nf.format(W.totalCells)} belegte Zellen`,'ƒ'],[W.modules.length,'VBA-Module','254 Prozeduren · keine Function','⌘'],[sum(Object.values(W.cachedErrors)),'Gespeicherte Fehlerwerte','Prüfbedarf für Vergleichstests','→']].map((x,i)=>`<div class="stat ${i===3?'warn':''}"><span class="stat-icon">${x[3]}</span><div class="stat-label">${x[1]}</div><strong>${nf.format(x[0])}</strong><small>${x[2]}</small></div>`).join('')}</section>
 <div class="grid-two"><section class="card"><div class="section-top"><h2>Wo die Berechnung lebt</h2><a class="mini-link" href="#logic">Rechenwege →</a></div><p>Verteilung der Zellformeln nach Funktionsbereich.</p>
 ${groups.map(x=>`<div class="bar-row"><span>${x[0]}</span><div class="bar-track"><div class="bar-fill" style="width:${x[1]/W.formulaCount*100}%"></div></div><strong>${nf.format(x[1])}</strong></div>`).join('')}
 <div class="notice green">${dec.format(calc/W.formulaCount*100)} % aller Formeln liegen in den beiden Zonen-Rechenkernen. Wiederholte Monats- und Zonenblöcke bestimmen den Umfang.</div></section>
 <section class="card"><div class="section-top"><h2>Der gespeicherte Beispielstand</h2><span class="tag">Excel-Cache</span></div><p>Ausgangswerte der Datei, noch nicht neu berechnet.</p>
 ${[['Energiebezugsfläche',fmt(W.snapshot.area)+' m²'],['Gebäudehülle',fmt(W.snapshot.envelope)+' m²'],['Nutzwärme Heizen',fmt(W.snapshot.heating)+' kWh/(m²a)'],['Primärenergie',fmt(W.snapshot.primary)+' kWh/(m²a)'],['Referenz-Primärenergie',fmt(W.snapshot.primaryReference)+' kWh/(m²a)']].map(x=>`<div class="text-row"><span>${x[0]}</span><strong>${x[1]}</strong></div>`).join('')}
 <div class="row-note">Belege: ${source('Eingabe','D85')} · ${source('DATA','C12')} · ${source('DATA','D12')}</div></section></div>
 <div class="grid-two"><section class="card"><div class="section-top"><h2>Die entscheidenden Befunde</h2><a class="mini-link" href="#migration">Einordnung →</a></div><div class="findings">
 <div class="finding"><span>01</span><div><h3>Die Datei enthält bereits Fehlerwerte.</h3><p>1.524 × #N/A, 128 × #VALUE! und 16 × #DIV/0!. Verteilung und einzelne Fundstellen sind durchsuchbar.</p></div></div>
 <div class="finding"><span>02</span><div><h3>VBA ist Teil des Zustandsmodells.</h3><p>Makros laden Profile, kopieren Daten und setzen Formeln. Eine reine Formelkonvertierung greift zu kurz.</p></div></div>
 <div class="finding"><span>03</span><div><h3>Dynamische Adressen sind häufig.</h3><p>24.634 OFFSET- und 231 INDIRECT-Aufrufe erfordern eine gezielte Auflösung der Datenabhängigkeiten.</p></div></div></div></section>
 <section class="card"><h2>Was diese Analyse abdeckt</h2><p>Vollständige statische Bestandsaufnahme der hochgeladenen Datei.</p><ul class="check-list"><li>Alle belegten Zellen mit Formel und gespeichertem Wert</li><li>1.671 Namensdefinitionen und vollständige VBA-Quellen</li><li>Klimadaten, Profile, Faktoren und Steuerelementbindungen</li><li>Architektur, Umsetzungsschritte und Abnahmekriterien</li></ul><p class="quiet">Die Makros wurden nicht ausgeführt. Excel-Rechengleichheit und die fachliche Richtigkeit jeder einzelnen Formel sind noch nicht nachgewiesen.</p></section></div>
 <section class="card"><div class="section-top"><h2>Der Weg zur lokalen Webanwendung</h2><span class="tag">Zielarchitektur</span></div><div class="flow"><div class="flow-node">01 · Datenmodell<small>Gebäude, Zonen, Anlagen</small></div><span class="flow-arrow">→</span><div class="flow-node">02 · Rechenkern<small>Deterministisch, mit Herkunftsbelegen</small></div><span class="flow-arrow">→</span><div class="flow-node">03 · Oberfläche<small>Eingabe, Auswertung, Varianten</small></div><span class="flow-arrow">→</span><div class="flow-node">04 · index.html<small>Alle Ressourcen eingebettet</small></div></div></section>
 <div class="section-gap"><div class="eyebrow">DATEI-IDENTITÄT</div><p class="hash">SHA-256 · ${esc(W.sha256)}</p></div>`;
}
function workbook(){
 return intro('DATEI ERKUNDEN','Eine Mappe. Alle Zusammenhänge.','Belegte Zellen, Formeln und Referenzdaten der Originaldatei. Auch neun Rohdatenzellen unter verbundenen Bereichen sind erfasst. Cachewerte werden hier nicht neu berechnet.')+
 `<div class="tabs" role="tablist" aria-label="Datenansicht">${[['cells','Zellen & Formeln'],['names','Benannte Bereiche'],['climate','Klima'],['profiles','Nutzungsprofile'],['factors','Faktoren']].map(([id,label])=>`<button role="tab" aria-selected="${tab===id}" class="${tab===id?'active':''}" data-tab="${id}">${label}</button>`).join('')}</div><div id="work-panel"></div>`;
}
function sheetWorkspace(){
 const s=W.sheets.find(x=>x.name===sheet);
 $('#work-panel').innerHTML=`<div class="workspace"><aside class="sheet-list" aria-label="Tabellenblätter">${W.sheets.map(x=>`<button data-sheet="${esc(x.name)}" class="${x.name===sheet?'active':''}" aria-pressed="${x.name===sheet}"><span>${esc(x.name)}</span><small>${nf.format(x.formulas)}</small></button>`).join('')}</aside><section class="panel"><div class="panel-head"><div><h2>${esc(sheet)}</h2><span class="quiet">${esc(roles[sheet])}</span></div><span class="tag">${visible(s.state)}</span></div><div class="legend"><span>${nf.format(s.formulas)} Formeln</span><span>${nf.format(s.literals)} Konstanten</span><span>${nf.format(errCount(s))} Fehlerwerte</span></div><div class="toolbar"><input id="cell-search" class="search" type="search" aria-label="Zellen durchsuchen" placeholder="Zelle, Formel, Text oder Fehler suchen …" value="${esc(query)}"><select id="scope" aria-label="Suchbereich"><option value="sheet" ${scope==='sheet'?'selected':''}>Dieses Blatt</option><option value="all" ${scope==='all'?'selected':''}>Alle 29 Blätter</option></select><select id="kind" aria-label="Zelltyp"><option value="all">Alle Inhalte</option><option value="formula" ${kind==='formula'?'selected':''}>Nur Formeln</option><option value="error" ${kind==='error'?'selected':''}>Nur Fehlerwerte</option><option value="unlocked" ${kind==='unlocked'?'selected':''}>Nicht gesperrte Zellen</option></select></div><div id="cell-detail"></div><div id="cell-results"></div></section></div>`;
 renderCells(); renderDetail();
 $('#cell-search').addEventListener('input',e=>{query=e.target.value;page=0;renderCells();});
 $('#scope').addEventListener('change',e=>{scope=e.target.value;page=0;renderCells();});
 $('#kind').addEventListener('change',e=>{kind=e.target.value;page=0;renderCells();});
}
function matchCell(r,q){return !q||r[0].toLowerCase()===q||String(r[1]??'').toLowerCase().includes(q)||String(r[2]??'').toLowerCase().includes(q)||String(r[5]??'').toLowerCase().includes(q);}
function filteredCells(){
 const q=query.toLowerCase().trim(),out=[];
 for(const sn of scope==='all'?W.sheets.map(x=>x.name):[sheet]){
  for(const r of CELLS[sn]){
   if(kind==='formula'&&r[3]!=='f'||kind==='error'&&!cacheError(r[2])||kind==='unlocked'&&!r[6])continue;
   if(matchCell(r,q))out.push({s:sn,r});
  }
 }
 return out;
}
function renderCells(){
 const rows=filteredCells(),pages=Math.max(1,Math.ceil(rows.length/perPage));page=Math.min(page,pages-1);
 const subset=rows.slice(page*perPage,(page+1)*perPage);
 $('#cell-results').innerHTML=`<div class="table-scroll"><table><thead><tr><th>Zelle</th><th>Inhalt / Formel</th><th>Gespeicherter Wert</th></tr></thead><tbody>${subset.map(({s,r})=>`<tr><td><button class="cell-link" data-cell="${esc(r[0])}" data-cell-sheet="${esc(s)}">${scope==='all'?esc(s)+'!':''}${esc(r[0])}</button></td><td><div class="${r[3]==='f'?'formula-text':'value-text'}" title="${esc(r[1])}">${esc(fmt(r[1]))}</div></td><td><div class="value-text">${cacheError(r[2])?`<span class="error-tag">${esc(r[2])}</span>`:esc(fmt(r[2]))}</div></td></tr>`).join('')||'<tr><td colspan="3" class="empty">Keine passenden Zellen gefunden.</td></tr>'}</tbody></table></div><div class="pagination"><span>${nf.format(rows.length)} Treffer · ${rows.length?nf.format(page*perPage+1):0}–${nf.format(Math.min(rows.length,(page+1)*perPage))}</span><div><button class="button small" data-page="prev" ${page===0?'disabled':''}>← Zurück</button><span> ${page+1} / ${nf.format(pages)} </span><button class="button small" data-page="next" ${page>=pages-1?'disabled':''}>Weiter →</button></div></div>${kind==='unlocked'?'<div class="row-note">Nicht gesperrt bedeutet nicht automatisch Benutzereingabe. ActiveX-/Formular-Steuerzellen liegen auch in Tab.Listen.</div>':''}`;
}
function renderDetail(){
 const el=$('#cell-detail');if(!el)return;if(!detail){el.innerHTML='';return;}
 const r=CELLS[detail.sheet].find(x=>x[0]===detail.address);
 if(!r){el.innerHTML=`<div class="notice">${esc(detail.sheet)}!${esc(detail.address)} ist keine belegte Zelle im Katalog.</div>`;return;}
 const related=W.names.filter(n=>(n.scope==='workbook'||n.scope===detail.sheet)&&n.target.replace(/\$/g,'').replace(/'/g,'').toLowerCase()===`${detail.sheet}!${detail.address}`.toLowerCase());
 el.innerHTML=`<section class="cell-detail" aria-label="Zelldetails"><h3><span>${esc(detail.sheet)}!${esc(r[0])}</span><button class="close" data-close="detail" aria-label="Zelldetails schließen">×</button></h3><pre>${esc(fmt(r[1]))}</pre><dl><dt>Gespeicherter Wert</dt><dd>${esc(fmt(r[2]))}</dd><dt>Zelltyp</dt><dd>${r[3]==='f'?'Formel':r[3]==='e'?'Fehlerkonstante':'Konstante'}</dd><dt>Zahlenformat</dt><dd class="mono">${esc(r[4])}</dd><dt>Gesperrt</dt><dd>${r[6]?'Nein':'Ja'}</dd><dt>Benannte Referenz</dt><dd>${esc(related.map(n=>n.name).join(', ')||'Keine direkte Einzelzellreferenz')}</dd>${r[5]?`<dt>Kommentar</dt><dd>${esc(r[5])}</dd>`:''}</dl><p class="row-note">∅ bezeichnet einen leeren oder nicht vorhandenen Cachewert. Eine Formel kann absichtlich einen leeren Text zurückgeben.</p></section>`;
}
function tablePanel(headers,rows,note=''){
 $('#work-panel').innerHTML=`<div class="toolbar"><input id="data-search" type="search" class="search" placeholder="Einträge durchsuchen …" aria-label="Referenzdaten durchsuchen"></div><div id="data-table"></div><p class="row-note">${note}</p>`;
 const render=q=>{const filtered=rows.filter(r=>r.text.toLowerCase().includes(q.toLowerCase()));$('#data-table').innerHTML=`<p class="quiet">${nf.format(filtered.length)} Einträge</p><div class="table-scroll"><table><thead><tr>${headers.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${filtered.map(r=>`<tr>${r.cells.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')||`<tr><td class="empty" colspan="${headers.length}">Keine Einträge gefunden.</td></tr>`}</tbody></table></div>`;};render('');$('#data-search').oninput=e=>render(e.target.value);
}
function renderTab(){
 if(tab==='cells'){sheetWorkspace();return;}
 if(tab==='names')tablePanel(['Name','Gültigkeitsbereich','Referenz / Bereich'],W.names.map(n=>({text:n.name+' '+n.target+' '+n.scope,cells:[`<span class="mono">${esc(n.name)}</span>`,esc(n.scope==='workbook'?'Arbeitsmappe':n.scope),namedSource(n.target)]})),'1.476 globale und 195 lokale Namensdefinitionen, einschließlich Excel-Druck-/Filterdefinitionen. Verweise auf ganze Zeilen oder mehrzellige Bereiche sind im Originalformat erhalten.');
 if(tab==='climate'){
 const headers=['Datensatz','Temperaturmittel °C','Januar °C','Juli °C','Herkunft'];
 tablePanel(headers,W.climates.map(c=>({text:c.name+' '+c.source,cells:[esc(c.name),fmt(sum(c.temperature)/12),fmt(c.temperature[0]),fmt(c.temperature[6]),source('Wetterdaten',c.source.match(/B\d+/)[0])]})),'18 numerisch befüllte Datensätze: Referenzklima, 15 Regionen sowie Luxemburg und Referenzklima 2007. Leere eigene Datensätze bleiben im Zellkatalog zugänglich. Die Werte sind historische Dateiinhalte.');
 }
 if(tab==='profiles')tablePanel(['Profilindex','Nutzung','h/Tag','Tage/Jahr','Heizen °C','Kühlen °C','Luft m³/(h·m²)','Herkunft'],W.profiles.map(p=>({text:p.name+' '+p.id+' '+p.source,cells:[esc(p.id),esc(p.name),fmt(p.hours),fmt(p.days),fmt(p.heating),fmt(p.cooling),fmt(p.air),source('Nutzungen',p.source.split('!')[1])]})),'44 befüllte Profilspalten. Der Profilindex ist die Spaltenposition, nicht die Profilnummer im Namen. Die Nutzung 22 hat drei Varianten.');
 if(tab==='factors')tablePanel(['Energieträger','Primärenergiefaktor','CO₂-Äquivalent g/kWh','Herkunft'],W.factors.map(f=>({text:f.name+' '+f.source,cells:[esc(f.name),fmt(f.primary),fmt(f.co2),source('Faktoren',f.source.split('!')[1].split(':')[0])]})),'Die Faktoren stammen aus dieser Excelversion und stellen keine Zusage aktueller Norm- oder Gesetzeskonformität dar.');
}
function namedSource(target){const match=/^'?([^'!]+)'?!\$?([A-Z]+)\$?(\d+)$/.exec(target);return match&&CELLS[match[1]]?source(match[1],match[2]+match[3]):`<span class="mono">${esc(target)}</span>`;}
function logic(){
 const blocks=[['Gebäudehülle','Eingabe','D41','Fenster, opake Wände, erdberührte Flächen, Boden und Dach werden zusammengeführt. Zwei Eingabeverfahren: direkte Flächen oder Fassadenlängen mit Geschossen.'],['Energiebezugsfläche','Eingabe','D85','Nur beheizte Zonen fließen in die EBF ein. Die Nettogrundfläche inklusive unbeheiztem Parkhaus beträgt dagegen 1.079 m².'],['Fenster-U-Wert','Eingabe','E58','Uw wird aus Glas, Rahmenanteil, Rahmen-U-Wert und Randverbund berechnet. Die einzelnen Bauteilparameter müssen im Webmodell erhalten bleiben.'],['Nutzwärme Heizen','DATA','A7','Zonenwerte werden flächengewichtet und auf die EBF bezogen. Der Rechenkern unterscheidet Nutzungszeit, Nichtnutzungszeit und monatliche Randbedingungen.'],['Primärenergie Heizen','DATA','C7','Nutzenergie wird über Verteilungs-/Übergabe-, Erzeuger- und Primärenergiefaktoren in die Bilanz überführt.'],['Gesamte Primärenergie','DATA','C12','Die gespeicherte Summe enthält Heizen, Kühlen, Warmwasser, Beleuchten, Lüften und den RES-Beitrag. Die Bilanzvariante ist explizit zu führen.']];
 return intro('HISTORISCHE EXCEL-ANALYSE','Die Logik hinter den Excelkennwerten.','Repräsentative, direkt belegte Rechenwege und die Struktur des Gesamtsystems. Die Abhängigkeitsauswertung ergänzt die Formelprüfung, ersetzt aber keine vollständige dynamische Ausführung.')+
 `<div class="architecture"><div class="arch-row"><div class="arch-box">Eingabe + Tab.Listen<small>Geometrie, Parameter und Auswahlindizes</small></div><div class="arch-box">Nutzungen + Wetterdaten<small>Zeiten, Sollwerte und Monatsklima</small></div></div><div class="arch-arrow">↓</div><div class="arch-row"><div class="arch-box">DATA + Konst + Tab.Referenz<small>Vermittlung, Kennwerte, Referenzparameter</small></div></div><div class="arch-arrow">↓</div><div class="arch-row"><div class="arch-box">CalC<small>Originalgebäude · 47.551 Formeln</small></div><div class="arch-box">CalC_Referenz<small>Referenzgebäude · 47.615 Formeln</small></div></div><div class="arch-arrow">↓</div><div class="arch-row"><div class="arch-box">Gesamtbilanzen + Anlagenblätter<small>Nutzenergie → Endenergie → Primärenergie / CO₂</small></div></div><div class="arch-arrow">↓</div><div class="arch-row"><div class="arch-box">TEK · nZEB · Anforderungen · Sankey<small>Auswertung, Vergleich und Visualisierung</small></div></div></div>
 <div class="notice">Dies ist eine fachlich vereinfachte Darstellung. Die tatsächlichen Zellbeziehungen sind wechselseitig; Auswahlwerte und Rückkopplungen laufen insbesondere über DATA und Tab.Listen.</div>
 <div class="grid-two"><section class="card"><h2>Nachvollziehbare Rechenbeispiele</h2>${blocks.map(([title,s,a,text])=>{const r=CELLS[s].find(x=>x[0]===a);return `<div class="formula-card"><h3>${title}</h3><p>${text}</p><pre>${esc(r[1])}</pre><div class="source">${source(s,a)} · gespeicherter Wert: ${esc(fmt(r[2]))}</div></div>`;}).join('')}</section>
 <div><section class="card"><h2>58 verschiedene Formelfunktionen</h2><p>Anzahl der Aufrufe, nicht Anzahl unterschiedlicher Formeln.</p>${Object.entries(W.functions).slice(0,12).map(([k,v])=>`<div class="bar-row"><span class="mono">${k}</span><div class="bar-track"><div class="bar-fill" style="width:${v/W.functions.IF*100}%"></div></div><strong>${nf.format(v)}</strong></div>`).join('')}<details><summary>Alle Funktionsaufrufe anzeigen</summary>${Object.entries(W.functions).map(([k,v])=>`<div class="text-row"><span class="mono">${k}</span><strong>${nf.format(v)}</strong></div>`).join('')}</details></section>
 <section class="card section-gap"><h2>Wiederholung statt 142.000 Einzelregeln</h2><p>CalC enthält bis zu elf Zonen in Spalten F:P und wiederholte Monatsblöcke. Die Referenzberechnung spiegelt große Teile davon.</p><ul class="check-list"><li>Geometrie und Tageslicht: vorderer Rechenkern</li><li>Thermische Bilanz: ab Zeile 1009</li><li>Ausnutzungsgrade, Gewinne und Verluste: Monatsblöcke</li><li>Ausgabegrößen und Diagramme: aggregierte Daten</li></ul><p>Die Migration sollte diese Blöcke in parametrisierte Funktionen überführen. Excel-spezifische Adressarithmetik wird durch benannte Datenstrukturen ersetzt.</p></section></div></div>
 <section class="card"><div class="section-top"><h2>Statisch erkennbare Blattabhängigkeiten</h2><span class="tag">${W.dependencies.length} Beziehungen inkl. Typ</span></div><p>„Quelle“ verwendet Werte aus „Ziel“. Direktverweise und Verweise über benannte Bereiche werden getrennt gezählt. Dynamisch gebildete Adressen sind nicht vollständig aufgelöst.</p><div class="table-scroll"><table><thead><tr><th>Quelle</th><th>Benötigtes Ziel</th><th>Referenzart</th><th>Fundstellen</th></tr></thead><tbody>${W.dependencies.slice(0,20).map(d=>`<tr><td>${esc(d.source)}</td><td>${esc(d.target)}</td><td>${d.kind==='direct'?'Direkter Blattverweis':'Benannter Bereich'}</td><td>${nf.format(d.count)}</td></tr>`).join('')}</tbody></table></div><p class="row-note">Die vollständige Liste ist im exportierbaren Inventar enthalten. Zählung: direkte Fundstellen bzw. eindeutige Namen je Formel und Zielblatt.</p></section>`;
}
const moduleRoles={
 'Copy_Paste.bas':'Parameterstudien und Klassifizierung; Umschalten des Profils und Übertragen von Berechnungsergebnissen.',
 'Z_Data_Projektverwaltung.bas':'Eigene TXT-Projektdateien lesen und schreiben; Dezimaltrennzeichen und alte Versionen behandeln.',
 'Z_Data_Referenz_laden.bas':'Referenzparameter in Eingaben kopieren; teils Werte, teils dynamische Formelverknüpfungen.',
 'Z_Data_Beispiel.bas':'Vollständige Eingabeparameter des Beispielgebäudes setzen.',
 'Z_Ein_Ausblenden.bas':'Benutzerführung, Auswahl des Hüllflächenverfahrens, Sichtbarkeit von Zonen und Grafiken.',
 'Einlesen.bas':'Daten aus anderen Arbeitsblättern/Arbeitsmappen in Zielstrukturen übertragen.',
 'Einlesen_Bagatell.bas':'Alternative Flächenzuordnung, Bagatellfälle und Auswahlverfahren.',
 'Z_Nutzungsprofil_kopieren.bas':'Eigene Nutzungsprofile kopieren und löschen.',
 'Z_Grafiken_Export.bas':'Diagramme über Excel-Funktionen kopieren/exportieren.',
 'Onlinecheck.frm':'Historische Online-Updateprüfung über Internet Explorer und EXE-Download; für die Offline-Webanwendung entbehrlich.',
 'DieseArbeitsmappe.cls':'Ereignisse beim Öffnen, Drucken, Speichern und Schließen; eigener Projekt-Speicherablauf.',
 'Z_Hilfemakros.bas':'Excel-Oberfläche, Blattschutz, Berechnungsmodus und Hilfsaktionen.',
 'Z_sprache.bas':'Sprachumschaltung und Textbezeichnungen.',
 'Z_Data_delete.bas':'Eingaben zurücksetzen.', 'Z_Zonendaten_delete.bas':'Einzelne Zonen, Beleuchtungs- und Lüftungsparameter zurücksetzen.'};
function vba(){
 return intro('ZUSTÄNDE & INTERAKTION','Mehr als Formeln.','Der vollständige extrahierte VBA-Quelltext ist hier lesbar, wird aber niemals ausgeführt. Die Makros beschreiben wichtige Datenänderungen und den bisherigen Bedienablauf.')+
 `<div class="notice green">53 Module · 6.240 Quelltextzeilen · 254 Sub-Prozeduren · keine Function-Definitionen in den extrahierten Quellen. ${nf.format(W.controlBindings.length)} Bindungen aus Formular-/Zeichnungsdateien erfasst.</div><div class="toolbar"><input class="search" id="vba-search" type="search" placeholder="Modul oder Prozedur suchen …" aria-label="VBA durchsuchen" value="${esc(vbaQuery)}"></div><div class="workspace"><aside id="module-list" class="sheet-list" aria-label="VBA-Module"></aside><section id="module-detail" class="panel"></section></div>
 <details class="section-gap"><summary>Steuerelemente und Bindungen (${nf.format(W.controlBindings.length)})</summary><p>Verknüpfungen zu Makros, Steuerzellen und Listenbereichen. Die vollständigen OOXML-Teilpfade stehen im JSON-Inventar. Zwei VML-Dateien sind nicht XML-konform; ihre Bindungen wurden ergänzend textuell erfasst.</p><div class="table-scroll"><table><thead><tr><th>Typ</th><th>Bindung</th></tr></thead><tbody>${W.controlBindings.map(b=>`<tr><td>${esc(b.kind)}</td><td class="mono">${esc(b.value)}</td></tr>`).join('')}</tbody></table></div></details>`;
}
function renderModules(){
 const q=vbaQuery.toLowerCase();const filtered=W.modules.map((m,i)=>({m,i})).filter(({m})=>(m.name+' '+m.procedures.join(' ')).toLowerCase().includes(q));
 $('#module-list').innerHTML=filtered.map(({m,i})=>`<button data-module="${i}" class="${i===moduleIndex?'active':''}"><span>${esc(m.name)}</span><small>${m.procedures.length}</small></button>`).join('')||'<p class="quiet">Kein Modul gefunden.</p>';
 if(filtered.length&&!filtered.some(x=>x.i===moduleIndex))moduleIndex=filtered[0].i;
 $$('#module-list button').forEach(b=>b.classList.toggle('active',+b.dataset.module===moduleIndex));
 const m=W.modules[moduleIndex];
 $('#module-detail').innerHTML=`<div class="panel-head"><h2>${esc(m.name)}</h2><span class="tag">Quelltext</span></div><div class="macro-meta"><span>${nf.format(m.lines)} Zeilen</span><span>${m.procedures.length} Prozeduren</span></div><p class="quiet">${esc(moduleRoles[m.name]||(m.procedures.length?'Excel-Ereignisse, Einstellungen oder Hilfsaktionen; siehe Quelltext.':'Blatt-/Klassenmodul ohne extrahierte Prozeduren.'))}</p><div class="procedure-chips">${m.procedures.map(p=>`<span class="chip">${esc(p)}</span>`).join('')}</div>${m.calls.length?`<p class="quiet">Explizite Call-Aufrufe</p><div class="procedure-chips">${m.calls.map(p=>`<button class="chip button" data-procedure="${esc(p)}">${esc(p)}</button>`).join('')}</div>`:''}<pre id="vba-code" class="code-block" tabindex="0" aria-label="VBA Quelltext"></pre>`;
 $('#vba-code').textContent=m.source;
}
const currentPhases=[
 ['Quellen und Anwendbarkeit','Nur aktuell anwendbare Verfahren bilden die Zielbasis. Gesetzlicher Rechenweg, Normausgabe, Übergangsregelung und zusätzliche Auftraggebervorgaben werden je Stichtag dokumentiert.','Abnahme: Fundstelle, Ausgabe, Geltungsbereich und Verbindlichkeit sind belegt; offene Quellen sind benannt.'],
 ['Projekt- und Datenmodell','Gebäudetyp, Neubau/Bestand, Flächenbezug, Nutzung, Energieversorgung und Bundeswehr-spezifische Randbedingungen werden explizite Eingaben. Historische Excel-Auswahlindizes werden nicht zu aktuellen Normprofilen umetikettiert.','Abnahme: Alle für die Verfahrenswahl nötigen Projektmerkmale und aktuellen Stammdaten sind definiert.'],
 ['Grundlegende Rechenmodule','Geometrie, Wärmetransport, Lüftung, Tageslicht, Bilanztemperaturen, Nutzenergie und Anlagentechnik werden gegen die aktuelle Anforderungsmatrix implementiert. Excel dient ergänzend zur Ursachenanalyse.','Abnahme: Jeder verwendete Algorithmus hat Eingabevertrag, Einheiten, Normbeleg und unabhängige Vergleichsfälle.'],
 ['AMEV und Bundesbau/Bundeswehr','Zusätzliche Planungs-, Betriebs-, Automations- und Effizienzvorgaben erhalten eigene Regeln samt Einführung und Anwendungsbereich. Planungsrichtwerte ersetzen keine Jahres-Energiebilanz.','Abnahme: Keine ungeprüfte Pauschalannahme zu Bundeswehr-Vorgaben oder zur universellen Geltung einer AMEV-Empfehlung.'],
 ['Gesamtprüfung und Offline-Auslieferung','Erst nach geprüften Vorstufen entstehen Gebäude-Gesamtbilanzen, Varianten und eine fachlich freigegebene Eingabeoberfläche. Alle Rechen- und Quellenstände bleiben im Ergebnisprotokoll sichtbar.','Abnahme: Rechenfälle, Energieerhaltung, Grenzfälle, Einheiten, Übergänge, file://, Import/Export und Zielbrowser sind geprüft.']
];
let currentRule='current-primary',currentResult=null;
function calculate(){
 const rules=N.rules.filter(r=>r.executionMode==='current-leaf');
 return intro('MIGRATION · AKTUELLER QUELLENSTAND','Rechnen mit offenem Nachweis.','Erste isolierte Umrechnungsbausteine auf öffentlich belegter gesetzlicher Grundlage. Die Gebäudeenergiebedarfsberechnung und Bundesbau-/Bundeswehr-Gesamtfreigabe sind noch offen.')+
 `<div class="notice">Quellenstichtag: <strong>${esc(N.targetProfile.asOf)}</strong>. Die Bundesbau-Quelle kündigt Änderungen des Berechnungsregelwerks ab <strong>01.01.2027</strong> an. Andere Stichtage werden bis zur erneuten Quellenprüfung gesperrt.</div><div class="toolbar"><label for="current-rule" class="quiet">Rechenbaustein</label><select id="current-rule">${rules.map(r=>`<option value="${esc(r.id)}" ${r.id===currentRule?'selected':''}>${esc(r.title)}</option>`).join('')}</select></div><div id="current-panel"></div>`;
}
function renderCurrent(){
 const rule=N.rules.find(r=>r.id===currentRule);
 const sample=rule.sampleInput;
 $('#current-panel').innerHTML=`<div class="grid-two"><section class="card"><div class="eyebrow">01 · EINGABEN</div><h2>${esc(rule.title)}</h2><p>Der Endenergiebedarf wird hier als bereits fachlich bestimmter Eingangswert vorausgesetzt.</p><div class="input-stack"><label>Endenergiebedarf <span>kWh</span><input id="energy-input" type="number" step="any" min="0" value="${sample.energy}"></label><label>Energieträger<select id="carrier-input">${N.currentFactors.map(c=>`<option value="${esc(c.id)}">${esc(c.label)}</option>`).join('')}</select></label><label>Quellenstichtag<input id="asof-input" type="date" value="${sample.asOf}"></label></div><div class="formula-card"><h3>02 · Rechenregel</h3><pre>${esc(rule.expression)}</pre><div id="current-factor" class="quiet"></div></div></section><section class="card"><div class="eyebrow">03 · ERGEBNIS & HERKUNFT</div><div id="current-output" aria-live="polite"></div><div class="notice green">Belegt ist nur die angegebene energieträgerbezogene Umrechnung. Eine Gebäude-Gesamtbilanz oder Bundeswehr-Konformität wird damit nicht bestätigt.</div><p class="quiet">${esc(rule.scopeLimit)}</p><button class="button" id="export-calculation">Rechenprotokoll als JSON speichern</button></section></div><section class="card"><div class="section-top"><h2>Weitere Rechenmodule</h2><a href="#norms" class="mini-link">Fehlende Nachweise →</a></div><p>Die übrigen aktuellen Verfahren sind noch nicht freigegeben. Die Anwendung fällt nicht auf das alte Excelverfahren zurück.</p><div class="dependency-grid">${N.rules.filter(r=>r.executionMode==='current-blocked').map(r=>`<div class="dependency-card"><h3>${esc(r.title)}</h3><span class="error-tag">Norm-/Verfahrensprüfung offen</span><p style="margin-top:8px">Benötigte Belege: ${esc(r.requirements.join(', '))}</p></div>`).join('')}</div></section>`;
 $('#carrier-input').value=sample.carrier;
 ['#energy-input','#carrier-input','#asof-input'].forEach(s=>$(s).addEventListener('input',updateCurrent));
 $('#export-calculation').onclick=()=>{
  if(!currentResult)return;
  const record={engineVersion:CHECKS.engineVersion,checkedAtSourceDate:N.targetProfile.asOf,...currentResult,
   normativeReview:rule.normativeReview,sourceLinks:N.publicSources.filter(s=>s.id===currentResult.usedSource.id||rule.normativeReview.evidence.some(e=>e.source===s.id)).map(s=>({url:s.url,htmlSha256:s.htmlSha256})),
   unresolvedProjectRequirements:N.requirements.filter(r=>['N12','N13','N14'].includes(r.id))};
  download('EnerCalC-Rechenprotokoll.json',JSON.stringify(record,null,2));notify('Rechenprotokoll mit Quellenbezug gespeichert.');
 };
 updateCurrent();
}
function updateCurrent(){
 const rule=N.rules.find(r=>r.id===currentRule);
 try{
  currentResult=EnerCore.runCurrent(N,currentRule,{energy:$('#energy-input').valueAsNumber,carrier:$('#carrier-input').value,asOf:$('#asof-input').value});
  const out=rule.outputs[0],source=N.publicSources.find(s=>s.id===currentResult.usedSource.id);
  $('#current-output').innerHTML=`<div class="result-number">${esc(fmt(currentResult.outputs[out.key]))}<small>${esc(out.unit)}</small></div><div class="text-row"><span>Faktor</span><strong>${esc(fmt(currentResult.usedFactor))} ${currentRule==='current-primary'?'kWh_prim/kWh_end':'g CO₂-Äq./kWh_end'}</strong></div><div class="text-row"><span>Quellenstand</span><strong>${esc(N.targetProfile.asOf)}</strong></div><div class="source-panel"><h3>04 · Öffentlicher Beleg</h3><a href="${esc(source.url)}" target="_blank" rel="noopener">${esc(source.title)}</a><p>Tabellenzeile ${currentResult.usedSource.tableNumber}. ${esc(rule.normativeReview.evidence[0].section)}</p><span class="tag">Einzelbaustein belegt · Gesamtverfahren offen</span></div>`;
  $('#current-factor').textContent=`Tabellenwert wird aus dem getrennten aktuellen Energieträgerkatalog bezogen: ${fmt(currentResult.usedFactor)}.`;
  $('#export-calculation').disabled=false;
 }catch(e){
  currentResult=null;$('#current-output').innerHTML=`<div class="notice" role="alert">${esc(e.message)}</div>`;
  $('#current-factor').textContent='Keine Ausgabe bei ungültiger Eingabe oder unbestätigtem Stichtag.';
  $('#export-calculation').disabled=true;
 }
}
function norms(){
 const references=N.rules.filter(r=>r.executionMode==='reference-only');
 return intro('NORMATIVE RÜCKVERFOLGBARKEIT','Vom Eingang bis zum Beleg.','Aktuell anwendbare gesetzliche Verfahren, technische Normen und zusätzliche Anforderungen für öffentliche Gebäude werden getrennt geführt. Historische Excelwerte bleiben ausschließlich Vergleichsmaterial.')+
 `<section class="stats"><div class="stat"><div class="stat-label">Aktuelle Einzelbausteine</div><strong>2</strong><small>Öffentliche Umrechnungsregeln belegt</small></div><div class="stat"><div class="stat-label">Cache-/Arithmetikvergleiche</div><strong>${CHECKS.passed}</strong><small>${references.length} Referenzbausteine · keine Sollvorgabe</small></div><div class="stat warn"><div class="stat-label">Gebäude-Gesamtverfahren</div><strong>Offen</strong><small>DIN-Verfahrenstexte und Detailprüfung fehlen</small></div><div class="stat warn"><div class="stat-label">Bundeswehr-Anwendung</div><strong>Offen</strong><small>Einführung und Projektvorgaben erforderlich</small></div></section>
 <div class="notice">${esc(N.targetProfile.statutoryReference)} Ab 01.01.2027 meldet die FIB Änderungen des Berechnungsregelwerks. Ein Fund im Quellenregister allein bedeutet noch keine Verfahrensfreigabe.</div>
 <section class="card"><div class="section-top"><h2>Quellenhierarchie</h2><button class="button small" data-norm-export="true">Nachweismatrix exportieren</button></div><div class="flow"><div class="flow-node">Gesetz und Übergang<small>Rechenweg, Stichtag, Bilanzgrenze</small></div><span class="flow-arrow">→</span><div class="flow-node">In Bezug genommene Norm<small>Konkrete Ausgabe und Bedingungen</small></div><span class="flow-arrow">→</span><div class="flow-node">Einführung / Auftraggeber<small>Bundesbau und Bundeswehr</small></div><span class="flow-arrow">→</span><div class="flow-node">Planungsempfehlungen<small>AMEV mit geklärter Anwendbarkeit</small></div></div><p class="quiet">Zusätzliche Projektanforderungen können einen strengeren Maßstab verlangen. Widersprüche, Ausnahmen und Rangfolgen müssen ausdrücklich geklärt werden; kein Dokument ersetzt automatisch alle anderen.</p></section>
 <section class="card section-gap"><h2>Konkrete Unterschiede zur alten Exceldatei</h2><div class="table-scroll"><table><thead><tr><th>Größe</th><th>Excel</th><th>Öffentlicher Tabellenwert</th><th>Quelle / Einordnung</th></tr></thead><tbody>${N.factorComparisons.map(c=>{const s=N.publicSources.find(s=>s.id===c.source);return `<tr><td>${esc(c.label)}<div class="row-note">${esc(c.unit)}</div></td><td>${fmt(c.workbook)}<div>${source(c.workbookCell.sheet,c.workbookCell.cell)}</div></td><td>${fmt(c.public)}</td><td><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(c.item)}</a><div class="row-note">${esc(c.finding)}</div></td></tr>`;}).join('')}</tbody></table></div></section>
 <section class="card section-gap"><h2>AMEV und Bundesbau: gefundene Originalquellen</h2><p>Ausgabe, Dokumentidentität und relevante Anknüpfungspunkte wurden recherchiert. Die vollständige Zuordnung aller Regeln und ihre Einführung für den konkreten Bundeswehr-Anwendungsfall ist noch offen.</p><div class="table-scroll"><table><thead><tr><th>Dokument / Ausgabe</th><th>Bedeutung</th><th>Stand der Prüfung</th></tr></thead><tbody>${(N.clientSources||[]).map(s=>`<tr><td><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title)}</a><div class="row-note">${esc(s.edition)}</div></td><td>${esc(s.relevance)}</td><td>${esc(s.status)}</td></tr>`).join('')}</tbody></table></div></section>
 <section class="card section-gap"><h2>Welche Unterlagen noch benötigt werden</h2><p>Die Kennungen führen in den Rechenmodulen zur jeweils fehlenden Grundlage. P1 bezeichnet den nächsten Durchstich; P3 ist ergänzende historische Analyse und kein aktueller Sollmaßstab.</p>${N.requirements.map(r=>`<details><summary><strong>${esc(r.id)} · ${esc(r.priority)}</strong> — ${esc(r.document)}</summary><p>${esc(r.needed)}</p><p class="mono">Betroffene Regeln: ${esc(r.rules.join(', '))}</p></details>`).join('')}</section>
 <section class="card section-gap"><h2>Zuordnung Eingang → Rechnung → Ausgang → Normbeleg</h2>${N.rules.filter(r=>r.executionMode!=='reference-only').map(r=>`<details><summary>${esc(r.title)} <span class="tag">${r.executionMode==='current-leaf'?'Einzelregel belegt':'offen'}</span></summary><p><strong>Eingang:</strong> ${esc(r.inputContract?r.inputContract.join(' · '):r.inputFields.map(i=>i.label+' '+i.unit).join(' · ')||'Vertrag nach Klärung des Verfahrens festzulegen')}</p><div class="formula-card"><pre>${esc(r.expression||'Kein unbestätigtes Ersatzverfahren implementiert.')}</pre></div><p><strong>Ausgang:</strong> ${esc(r.outputContract?r.outputContract.join(' · '):r.outputs.map(o=>o.label+' ['+o.unit+']').join(' · ')||'Noch nicht freigegeben')}</p><p><strong>Normbeleg / Bedarf:</strong> ${r.executionMode==='current-leaf'?esc(r.normativeReview.evidence.map(e=>e.section).join(' · ')):esc(r.requirements.join(', '))}</p><p>${esc(r.scopeLimit)}</p></details>`).join('')}</section>
 <details class="section-gap"><summary>Historische Vergleichsbausteine: ${references.length} · ${CHECKS.total} Prüfwerte</summary><p>Diese Funktionen sind ausschließlich im Referenzaudit verwendet. Eine Gleichheit mit gespeicherten Excel-Zwischenwerten gilt nicht als aktueller Normnachweis. Sie sind über den aktuellen Anwendungspfad gesperrt.</p>${references.map(r=>`<div class="text-row"><span>${esc(r.title)}</span><strong>${CHECKS.results[r.id]?.passed||0} Vergleiche</strong></div>`).join('')}<p>${esc(CHECKS.scope)}</p></details>`;
}
function migration(){
 return intro('MIGRATION · FREIGEGEBENER ZIELUMFANG','Aktuell anwendbar.<br>Mit belegten Rechenwegen.','Die Zielvorgabe lautet: aktuelle Verfahren und Normbasis, ergänzt um AMEV sowie Bundesbau/Bundeswehr. Das frühere Konzept eines historischen EnEV-/LU-Nachbaus ist damit als Anwendungspfad abgelöst.')+
 `<div class="notice green">Kein Rückgriff auf unbestätigte Altverfahren. Noch fehlende Quellen und Anwendbarkeitsentscheidungen sind im <a href="#norms">Normnachweisregister</a> benannt. Zwei isolierte gesetzliche Umrechnungsbausteine sind bereits ausführbar; die Gesamtberechnung ist noch nicht freigegeben.</div>`+
 currentPhases.map(([title,text,acceptance],i)=>`<section class="phase"><div class="phase-num">0${i+1}</div><div class="card"><h3>${title}</h3><p>${text}</p><div class="acceptance">${acceptance}</div></div></section>`).join('')+
 `<section class="card"><h2>Nächster fachlicher Durchstich</h2><p>Gebäude-/Zonenmodell und vollständiger Heiz-/Kühl-Monatsrechengang auf der aktuell anzuwendenden Normbasis. Dafür werden zunächst die vollständigen relevanten Verfahrenstexte und die fachlich geltenden Bundeswehr-/Bundesbau-Einführungen benötigt.</p><div class="export-area"><a href="#calculate" class="button primary">Erste Rechenbausteine öffnen</a><a href="#norms" class="button">Normen und Quellen prüfen</a><button class="button" data-action="print">Konzept drucken</button></div></section>`;
}

function render(){
 document.title=`EnerCalC — ${labels[view]}`;$('#crumb').textContent=labels[view];$$('nav a').forEach(a=>{a.classList.toggle('active',a.dataset.view===view);if(a.dataset.view===view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 $('#content').innerHTML=({overview,workbook,logic,vba,migration,calculate,norms}[view])();
 if(view==='workbook')renderTab();
 if(view==='calculate'){renderCurrent();$('#current-rule').onchange=e=>{currentRule=e.target.value;renderCurrent();};}
 if(view==='vba'){renderModules();$('#vba-search').oninput=e=>{vbaQuery=e.target.value;renderModules();};}
}
function navigate(){const requested=location.hash.slice(1);view=Object.hasOwn(labels,requested)?requested:'overview';render();window.scrollTo(0,0);}
function download(name,data,type='application/json'){
 const url=URL.createObjectURL(new Blob([data],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);
}
function notify(t){$('#toast').textContent=t;$('#toast').hidden=false;setTimeout(()=>$('#toast').hidden=true,3500);}
function openSource(sn,address){sheet=sn;tab='cells';scope='sheet';kind='all';query=address;page=0;detail={sheet:sn,address};if(view!=='workbook')location.hash='workbook';else{render();$('#cell-detail').scrollIntoView({behavior:'smooth',block:'nearest'});}}
function exportInventory(){download('EnerCalC-Inventar.json',JSON.stringify(W,null,2));notify('Inventar lokal als JSON exportiert.');}
document.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 if(b.dataset.normExport){download('EnerCalC-Normnachweise.json',JSON.stringify({registry:N,checks:CHECKS},null,2));return;}
 if(b.dataset.source){openSource(b.dataset.source,b.dataset.address);return;}
 if(b.dataset.tab){tab=b.dataset.tab;render();return;}
 if(b.dataset.sheet){sheet=b.dataset.sheet;scope='sheet';query='';page=0;detail=null;render();return;}
 if(b.dataset.page){page+=b.dataset.page==='next'?1:-1;renderCells();return;}
 if(b.dataset.cell){detail={sheet:b.dataset.cellSheet,address:b.dataset.cell};renderDetail();$('#cell-detail').scrollIntoView({behavior:'smooth',block:'nearest'});return;}
 if(b.dataset.close){detail=null;renderDetail();return;}
 if(b.dataset.module!==undefined){moduleIndex=+b.dataset.module;renderModules();return;}
 if(b.dataset.procedure){const i=W.modules.findIndex(m=>m.procedures.some(p=>p.toLowerCase()===b.dataset.procedure.toLowerCase()));if(i>=0){moduleIndex=i;vbaQuery='';$('#vba-search').value='';renderModules();}else notify('Der Aufruf wurde in den extrahierten Prozeduren nicht aufgelöst.');return;}
 if(b.dataset.action==='print')window.print();
 if(b.dataset.action==='inventory')exportInventory();
});
$('#export').onclick=()=>exportInventory();
window.addEventListener('hashchange',()=>{if(W)navigate();});
(async()=>{
 try{
  if(typeof DecompressionStream==='undefined')throw new Error('Bitte einen aktuellen Browser mit DecompressionStream-Unterstützung verwenden (Chrome, Edge, Firefox oder Safari).');
  const bytes=Uint8Array.from(atob($('#payload').textContent.trim()),c=>c.charCodeAt(0));
  const data=await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).json();
  W=data.workbook;CELLS=data.cells;N=data.normative;CHECKS=data.checks;$('#payload').remove();navigate();
  // Read-only reference to support independent integrity checks of the embedded dataset.
  window.ENER_AUDIT={workbook:W,cells:CELLS};
  window.ENER_NORM_AUDIT={registry:N,checks:CHECKS};
 }catch(error){$('#loading').innerHTML='<h1>Analyse konnte nicht geöffnet werden.</h1><p id="load-error"></p>';$('#load-error').textContent=error.message;}
})();
