"""Build the single-file offline report. Uses Python's standard library only."""
import base64
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
workbook = json.loads((ROOT/'docs/workbook-inventory.json').read_text())
cells = json.loads(gzip.decompress((ROOT/'docs/cell-catalog.json.gz').read_bytes()))
payload = json.dumps(dict(workbook=workbook, cells=cells), ensure_ascii=False, separators=(',', ':')).encode()
encoded = base64.b64encode(gzip.compress(payload, mtime=0)).decode()
css = (ROOT/'report/style.css').read_text()
js = (ROOT/'report/app.js').read_text().replace('</script', '<\\/script')
html = (ROOT/'report/template.html').read_text().replace('/*__CSS__*/', css).replace('/*__JS__*/', js).replace('__PAYLOAD__', encoded)
(ROOT/'index.html').write_text(html)
print(f'Built index.html: {len(html.encode()):,} bytes; {len(cells)} sheets; all data embedded.')
