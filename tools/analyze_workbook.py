"""Read the workbook without executing VBA. Generates offline browser reference data.

Usage: python tools/analyze_workbook.py /path/to/EnerCalC.xlsm
Analysis dependencies: openpyxl; optional oletools for the VBA inventory.
"""
import collections
import gzip
import hashlib
import html
import json
import pathlib
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

import openpyxl
from openpyxl.cell.cell import Cell
from openpyxl.formula.translate import Translator

ROOT = pathlib.Path(__file__).resolve().parents[1]


def analyze(path):
    formulas = openpyxl.load_workbook(path, data_only=False, keep_vba=True)
    values = openpyxl.load_workbook(path, data_only=True)
    with zipfile.ZipFile(path) as archive:
        workbook_xml=ET.fromstring(archive.read('xl/workbook.xml'))
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    names=[]
    for defined in workbook_xml.findall('s:definedNames/s:definedName',ns):
        index=defined.get('localSheetId')
        names.append(dict(name=defined.get('name'),target=defined.text or '',
                          scope=formulas.sheetnames[int(index)] if index is not None else 'workbook',
                          builtin=defined.get('name','').startswith('_xlnm.')))
    sheets, functions, errors = [], collections.Counter(), collections.Counter()
    catalog, edges = {}, collections.Counter()
    name_targets = {}
    for name, defined in formulas.defined_names.items():
        try:
            name_targets[name.lower()] = [s for s, _ in defined.destinations]
        except (TypeError, AttributeError):
            name_targets[name.lower()] = []
    ref_pattern = re.compile(r"(?:'((?:[^']|'')+)'|([\w.]+))!")
    token_pattern = re.compile(r'[^\W\d][\w.]*', re.UNICODE)
    scoped_targets={s:{} for s in formulas.sheetnames}
    for n in names:
        if n['scope']!='workbook':
            scoped_targets[n['scope']][n['name'].lower()]=[m[1] or m[2] for m in ref_pattern.finditer(n['target'])]
    for sheet in formulas:
        count, literals, missing, unlocked = 0, 0, 0, 0
        local_errors, records = collections.Counter(), []
        for row in sheet:
            for cell in row:
                if cell.value is None:
                    continue
                cached = values[sheet.title][cell.coordinate]
                raw = cell.value
                if cell.data_type == 'f':
                    count += 1
                    functions.update(re.findall(r'\b([A-Z][A-Z0-9_.]*)\(', str(cell.value)))
                    if cached.value is None:
                        missing += 1
                    expression = re.sub(r'"(?:[^"]|"")*"', '', str(raw))
                    for match in ref_pattern.finditer(expression):
                        target = (match[1] or match[2]).replace("''", "'")
                        if target != sheet.title and target in formulas.sheetnames:
                            edges[(sheet.title, target, 'direct')] += 1
                    for token in set(token_pattern.findall(expression)):
                        for target in scoped_targets[sheet.title].get(token.lower(),name_targets.get(token.lower(), [])):
                            if target != sheet.title and target in formulas.sheetnames:
                                edges[(sheet.title, target, 'named')] += 1
                else:
                    literals += 1
                if not cell.protection.locked:
                    unlocked += 1
                if cached.data_type == 'e':
                    errors[cached.value] += 1
                    local_errors[cached.value] += 1
                records.append([cell.coordinate, raw, cached.value, cell.data_type,
                                cell.number_format, cell.comment.text if cell.comment else None,
                                not cell.protection.locked])
        catalog[sheet.title] = records
        sheets.append(dict(name=sheet.title, state=sheet.sheet_state,
                           rows=sheet.max_row, columns=sheet.max_column, formulas=count,
                           literals=literals, missingCache=missing, unlocked=unlocked, errors=dict(local_errors),
                           protected=bool(sheet.protection.sheet), merged=[str(r) for r in sheet.merged_cells.ranges],
                           validations=[dict(range=str(d.sqref),type=d.type,formula1=d.formula1,formula2=d.formula2)
                                        for d in sheet.data_validations.dataValidation]))

    # openpyxl intentionally discards non-anchor values in merged ranges. Keep
    # those original OOXML records too: they matter for a complete static audit.
    recovered=[]
    with zipfile.ZipFile(path) as archive:
        strings_xml=ET.fromstring(archive.read('xl/sharedStrings.xml'))
        strings=[''.join(t.text or '' for t in si.findall('.//s:t',ns)) for si in strings_xml]
        for index, sheet in enumerate(formulas,1):
            tree=ET.fromstring(archive.read(f'xl/worksheets/sheet{index}.xml'))
            nodes=tree.findall('.//s:c',ns)
            anchors={}
            for node in nodes:
                f=node.find('s:f',ns)
                if f is not None and f.get('t')=='shared' and f.text:
                    anchors[f.get('si')]=(node.get('r'),'='+f.text)
            existing={r[0] for r in catalog[sheet.title]}
            meta=next(s for s in sheets if s['name']==sheet.title)
            for node in nodes:
                address=node.get('r')
                if address in existing:
                    continue
                f=node.find('s:f',ns)
                v=node.find('s:v',ns)
                text=v.text if v is not None else None
                typ=node.get('t','n')
                if typ=='s': cached=strings[int(text)] if text is not None else None
                elif typ in ['str','e']: cached=text
                elif typ=='b': cached=text=='1'
                elif typ=='inlineStr': cached=''.join(t.text or '' for t in node.findall('.//s:t',ns))
                else:
                    cached=float(text) if text is not None else None
                    if isinstance(cached,float) and cached.is_integer():cached=int(cached)
                if f is not None:
                    if f.text:
                        raw='='+f.text
                    else:
                        origin, expression=anchors[f.get('si')]
                        raw=Translator(expression,origin=origin).translate_formula(address)
                    typ='f'
                    meta['formulas']+=1
                    functions.update(re.findall(r'\b([A-Z][A-Z0-9_.]*)\(',raw))
                    if cached is None:meta['missingCache']+=1
                else:
                    raw=cached
                    if raw is None:continue
                    typ='s' if typ in ['s','str','inlineStr'] else typ
                    meta['literals']+=1
                row,col=openpyxl.utils.cell.coordinate_to_tuple(address)
                style_cell=Cell(sheet,row,col)
                style_cell._style=formulas._cell_styles[int(node.get('s','0'))]
                unlocked=not style_cell.protection.locked
                if unlocked:meta['unlocked']+=1
                catalog[sheet.title].append([address,raw,cached,typ,style_cell.number_format,None,unlocked])
                if node.get('t')=='e':
                    errors[cached]+=1
                    meta['errors'][cached]=meta['errors'].get(cached,0)+1
                recovered.append(dict(sheet=sheet.title,cell=address,reason='Raw OOXML content hidden by merged-cell normalization'))
            catalog[sheet.title].sort(key=lambda r:openpyxl.utils.cell.coordinate_to_tuple(r[0]))

    def val(sheet, address):
        return values[sheet][address].value

    def nums(sheet, row, start=4, end=15):
        return [values[sheet].cell(row, c).value for c in range(start, end + 1)]

    climates = []
    for row in range(17, 301, 13):
        name = val('Wetterdaten', f'C{row}')
        temp = nums('Wetterdaten', row + 1)
        if name and all(isinstance(x, (int, float)) for x in temp):
            climates.append(dict(id=str(row), name=str(name), source=f'Wetterdaten!B{row}:O{row+11}',
                                 temperature=temp, horizontal=nums('Wetterdaten', row+2),
                                 south=nums('Wetterdaten', row+3), east=nums('Wetterdaten', row+6),
                                 west=nums('Wetterdaten', row+7), north=nums('Wetterdaten', row+10)))
    profiles = []
    fields = dict(hours=6, days=7, operationHours=10, operationDays=11, lux=14,
                  absence=17, lightingFactor=19, air=26, people=29, equipment=30,
                  heating=36, setback=37, cooling=38, height=53)
    for col in range(5, 58):
        name = values['Nutzungen'].cell(2, col).value
        number = values['Nutzungen'].cell(78, col).value
        if not isinstance(name, str) or not isinstance(number, (int, float)):
            continue
        data = {key: values['Nutzungen'].cell(row, col).value for key, row in fields.items()}
        if not all(isinstance(x, (int, float)) for x in data.values()):
            continue
        profiles.append(dict(id=str(col-4), code=str(number), name=name,
                             source=f'Nutzungen!{openpyxl.utils.get_column_letter(col)}2', **data))
    modules = []
    try:
        from oletools.olevba import VBA_Parser
        parser = VBA_Parser(str(path))
        for _, _, name, code in parser.extract_macros():
            procedures = re.findall(r'^\s*(?:(?:Public|Private|Friend|Static)\s+)?(?:Sub|Function)\s+(\w+)', code, re.M | re.I)
            modules.append(dict(name=name, lines=len(code.splitlines()), procedures=procedures,
                                calls=sorted(set(re.findall(r'\bCall\s+([\w]+)',code,re.I))),
                                source=code.replace('\r\n','\n'),
                                hasFunction=bool(re.search(r'^\s*(?:(?:Public|Private)\s+)?Function\s+',code,re.M|re.I))))
        parser.close()
    except ImportError:
        raise RuntimeError('Install oletools to retain the complete VBA inventory.')
    examples = []
    addresses = {'Eingabe': ['E26', 'D36', 'D37', 'D41', 'D43', 'E58', 'D85', 'E149'],
                 'DATA': ['A7', 'C7', 'C9', 'C12', 'D99'],
                 'Tab.PV': ['N29', 'N40', 'N28'],
                 'CalC': ['F1699', 'F1076', 'F1082'],
                 'Gesamtbilanz': ['Q183', 'Q187', 'Q347'], 'Faktoren': ['I7', 'J7', 'I10', 'J10']}
    for sheet, cells in addresses.items():
        for address in cells:
            examples.append(dict(sheet=sheet, cell=address,
                                 formula=str(formulas[sheet][address].value), value=val(sheet, address)))
    factors = [dict(name=val('Faktoren', f'B{r}'), primary=val('Faktoren', f'I{r}'),
                    co2=val('Faktoren', f'J{r}'), source=f'Faktoren!I{r}:J{r}') for r in range(7, 13)]
    pv = [dict(id=str(c), name=val('Tab.PV', f'{openpyxl.utils.get_column_letter(c)}5'),
               yieldAnnual=values['Tab.PV'].cell(19,c).value,
               weights=[values['Tab.PV'].cell(r,c).value for r in range(6,18)],
               source=f'Tab.PV!{openpyxl.utils.get_column_letter(c)}6:{openpyxl.utils.get_column_letter(c)}19') for c in range(17,24)]
    zones = []
    for c in range(5,16):
        area = values['Eingabe'].cell(83,c).value
        if not isinstance(area,(int,float)) or area <= 0:
            continue
        col = openpyxl.utils.get_column_letter(c)
        zones.append(dict(name=values['DATA'].cell(118,c).value, area=area,
                          profile=str(values['DATA'].cell(148,c).value),
                          height=values['Eingabe'].cell(84,c).value,
                          heated=values['DATA'].cell(151,c).value=='ja',
                          cooled=values['DATA'].cell(149,c).value=='ja',
                          mechanical=values['DATA'].cell(158,c).value!='Fensterlüftung',
                          lighting=round(values['CalC'].cell(802,c+1).value or 0,3),
                          source=f'Eingabe!{col}83:{col}85'))
    result = dict(filename=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  version=val('Start', 'L30'), sheets=sheets, formulaCount=sum(s['formulas'] for s in sheets),
                  namedRangeCount=len(names), functions=dict(functions.most_common()), cachedErrors=dict(errors),
                  globalNameCount=sum(n['scope']=='workbook' for n in names),
                  localNameCount=sum(n['scope']!='workbook' for n in names),
                  modules=modules, names=names, climates=climates, profiles=profiles,
                  factors=factors, pv=pv, zones=zones, examples=examples,
                  snapshot=dict(area=val('Eingabe','D85'), envelope=val('Eingabe','D41'),
                                heatTransfer=val('DATA','D99'), primary=val('DATA','C12'),
                                primaryReference=val('DATA','D12'), heating=val('DATA','A7'),
                                cooling=val('DATA','A6'), lighting=val('DATA','A9'),
                                ventilation=val('DATA','A10'), dhw=val('DATA','A8')))
    with zipfile.ZipFile(path) as archive:
        members = archive.namelist()
        result['package'] = dict(charts=sum(bool(re.fullmatch(r'xl/charts/chart\d+\.xml', n)) for n in members),
                                 activeX=sum(bool(re.fullmatch(r'xl/activeX/activeX\d+\.xml',n)) for n in members),
                                 media=sum(n.startswith('xl/media/') for n in members),
                                 externalLinks=len(formulas._external_links))
        bindings=[]
        parse_warnings=[]
        for n in members:
            if n.endswith(('.xml','.vml')) and ('drawing' in n or 'ctrlProp' in n):
                source=archive.read(n)
                try:
                    tree=ET.fromstring(source)
                except ET.ParseError:
                    parse_warnings.append(n)
                    text=source.decode('utf-8', errors='replace')
                    for kind, text_value in re.findall(r'<(?:\w+:)?(FmlaMacro|FmlaLink|FmlaRange)>(.*?)</(?:\w+:)?\1>', text, re.S):
                        bindings.append(dict(part=n,kind=kind,value=html.unescape(text_value)))
                    continue
                for el in tree.iter():
                    tag=el.tag.split('}')[-1]
                    if tag in ['FmlaMacro','FmlaLink','FmlaRange'] and el.text:
                        bindings.append(dict(part=n,kind=tag,value=el.text))
                    if el.get('macro'):
                        bindings.append(dict(part=n,kind='macro',value=el.get('macro')))
        result['controlBindings']=bindings
        result['package']['xmlFallbacks']=parse_warnings
    result['dependencies']=[dict(source=a,target=b,kind=k,count=v) for (a,b,k),v in edges.most_common()]
    result['calculation']={k:getattr(formulas.calculation,k) for k in ['calcId','calcMode','fullCalcOnLoad','iterate','iterateCount','iterateDelta','calcCompleted']}
    result['totalCells']=sum(len(v) for v in catalog.values())
    result['recoveredMergedCells']=recovered
    result['sourceNotice']='Extracted values are saved Excel caches, not recalculated or validated results.'
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/'docs/workbook-inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n')
    packed=json.dumps(catalog,ensure_ascii=False,separators=(',',':'),default=str).encode()
    (ROOT/'docs/cell-catalog.json.gz').write_bytes(gzip.compress(packed,mtime=0))
    print(json.dumps({k:result[k] for k in ['formulaCount','namedRangeCount','cachedErrors','snapshot']},indent=2))
    print(f'{len(climates)} climates, {len(profiles)} profiles, {len(modules)} VBA modules; no macros executed.')


if __name__ == '__main__':
    analyze(pathlib.Path(sys.argv[1]))
