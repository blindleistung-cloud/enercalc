"""Integrity checks for the extracted workbook and the self-contained artifact."""
import base64
import collections
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
W = json.loads((ROOT/'docs/workbook-inventory.json').read_text())
C = json.loads(gzip.decompress((ROOT/'docs/cell-catalog.json.gz').read_bytes()))
SOURCE = os.environ.get('ENERCALC_SOURCE')


def cell(sheet, address):
    return next(r for r in C[sheet] if r[0] == address)


class InventoryIntegrity(unittest.TestCase):
    def test_all_sheets_and_cells_reconcile(self):
        self.assertEqual(set(C), {s['name'] for s in W['sheets']})
        self.assertEqual(sum(len(rows) for rows in C.values()), 179048)
        self.assertEqual(W['totalCells'], 179048)
        for sheet in W['sheets']:
            records = C[sheet['name']]
            self.assertEqual(len({r[0] for r in records}), len(records))
            self.assertEqual(sum(r[3]=='f' for r in records), sheet['formulas'])
            self.assertEqual(sum(r[3]!='f' for r in records), sheet['literals'])
        self.assertEqual(sum(s['formulas'] for s in W['sheets']), 141897)
        self.assertEqual(len(W['recoveredMergedCells']),9)
        self.assertEqual(cell('Tab.Wärme','Y4')[1],'=Y20')

    def test_errors_have_exact_locations_and_counts(self):
        errors = collections.Counter(r[2] for rows in C.values() for r in rows if r[2] in ['#N/A','#VALUE!','#DIV/0!'])
        self.assertEqual(dict(errors), W['cachedErrors'])
        self.assertEqual(sum(errors.values()), 1668)
        self.assertEqual(cell('Gesamtbilanz','Q182')[2], 0)
        self.assertEqual(cell('Gesamtbilanz','Q183')[2], 0)
        self.assertEqual(cell('Gesamtbilanz','U183')[2], '#DIV/0!')
        self.assertEqual(cell('CalC','E1987')[2], 'W')
        self.assertEqual(cell('CalC','S2081')[2], '#VALUE!')

    def test_scoped_names_not_lost(self):
        self.assertEqual(len(W['names']), 1671)
        self.assertEqual(sum(n['scope']=='workbook' for n in W['names']), 1476)
        self.assertEqual(sum(n['scope']!='workbook' for n in W['names']), 195)
        self.assertEqual(len({(n['scope'],n['name'].lower()) for n in W['names']}), 1671)
        self.assertTrue(any(n['builtin'] for n in W['names']))

    def test_profiles_keep_positional_identity(self):
        self.assertEqual(len(W['profiles']), 44)
        self.assertEqual(len({p['id'] for p in W['profiles']}), 44)
        park = next(p for p in W['profiles'] if p['id']=='34')
        self.assertEqual(park['name'], '32 Parkhaus')
        self.assertEqual(next(p for p in W['profiles'] if p['id']=='44')['name'], '34 Wohnen EFH')
        self.assertEqual(len(W['climates']), 18)
        for c in W['climates']:
            for key in ['temperature','horizontal','south','east','west','north']:
                self.assertEqual(len(c[key]), 12)
                self.assertTrue(all(isinstance(x,(int,float)) for x in c[key]))

    def test_saved_example_reconciles_without_formula_execution(self):
        self.assertEqual(sum(z['area'] for z in W['zones'] if z['heated']), 821)
        self.assertEqual(sum(z['area'] for z in W['zones']), 1079)
        self.assertEqual(sum(z['area'] for z in W['zones'] if z['cooled']), 722)
        self.assertAlmostEqual(sum(cell('Eingabe',f'D{r}')[2] for r in range(36,41)), W['snapshot']['envelope'])
        self.assertAlmostEqual(sum(cell('DATA',f'C{r}')[2] for r in range(6,12)), W['snapshot']['primary'])
        inputs={r[0]:r[2] for r in C['Eingabe']}
        weighted = sum((cell('DATA',f'{c}74')[2] or 0)*(inputs.get(f'{c}83',0) or 0) for c in 'EFGHIJKLMNO')/821
        self.assertAlmostEqual(weighted, W['snapshot']['heating'])

    def test_vba_sources_reconcile(self):
        self.assertEqual(len(W['modules']), 53)
        self.assertEqual(sum(m['lines'] for m in W['modules']), 6240)
        self.assertEqual(sum(len(m['procedures']) for m in W['modules']), 254)
        for m in W['modules']:
            procedures = re.findall(r'^\s*(?:(?:Public|Private|Friend|Static)\s+)?(?:Sub|Function)\s+(\w+)',m['source'],re.M|re.I)
            self.assertEqual(procedures, m['procedures'])
            self.assertFalse(m['hasFunction'])

    def test_single_file_contains_complete_identical_payload(self):
        html = (ROOT/'index.html').read_text()
        encoded = re.search(r'<script id="payload" type="application/octet-stream">([^<]+)</script>',html)[1]
        data = json.loads(gzip.decompress(base64.b64decode(encoded)))
        self.assertEqual(data['workbook'], W)
        self.assertEqual(data['cells'], C)
        self.assertNotRegex(html, r'<script[^>]+src\s*=')
        self.assertNotRegex(html, r'<link[^>]+(?:href|src)\s*=')
        self.assertNotRegex(html, r'<img[^>]+src\s*=')
        self.assertIn("connect-src 'none'", html)
        self.assertNotIn('/*__CSS__*/', html)
        self.assertNotIn('/*__JS__*/', html)

    @unittest.skipUnless(SOURCE, 'Set ENERCALC_SOURCE for independent original OOXML checks.')
    def test_original_ooxml_independently_matches_inventory(self):
        source = Path(SOURCE)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), W['sha256'])
        ns = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        with zipfile.ZipFile(source) as archive:
            count=0
            raw_cells=0
            errors=collections.Counter()
            for name in archive.namelist():
                if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',name):
                    xml=ET.fromstring(archive.read(name))
                    count += len(xml.findall('.//s:c/s:f',ns))
                    for c in xml.findall('.//s:c',ns):
                        if any(c.find('s:'+tag,ns) is not None for tag in ['f','v','is']):raw_cells+=1
                        if c.get('t')=='e':
                            errors[c.find('s:v',ns).text]+=1
            self.assertEqual(count, W['formulaCount'])
            self.assertEqual(raw_cells, W['totalCells'])
            self.assertEqual(dict(errors), W['cachedErrors'])
            workbook=ET.fromstring(archive.read('xl/workbook.xml'))
            names=workbook.findall('s:definedNames/s:definedName',ns)
            self.assertEqual(len(names), W['namedRangeCount'])
            expected={(n.get('name'),n.get('localSheetId'),n.text) for n in names}
            positions={s['name']:str(i) for i,s in enumerate(W['sheets'])}
            observed={(n['name'],None if n['scope']=='workbook' else positions[n['scope']],n['target']) for n in W['names']}
            self.assertEqual(expected,observed)


if __name__ == '__main__':
    unittest.main()
