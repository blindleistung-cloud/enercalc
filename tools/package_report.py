"""Package the report and its documentation for download from GitHub."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'downloads' / 'EnerCalC-Analyse.zip'
files = [ROOT / name for name in ['index.html', 'README.md', 'requirements-analysis.txt']]
for folder in ['docs', 'report', 'tools', 'tests']:
    files.extend(p for p in (ROOT / folder).rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
DESTINATION.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(DESTINATION, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(files):
        archive.write(path, str(path.relative_to(ROOT)))
with zipfile.ZipFile(DESTINATION) as archive:
    assert archive.testzip() is None
    assert archive.read('index.html') == (ROOT / 'index.html').read_bytes()
print(f'{DESTINATION}: {len(files)} files, {DESTINATION.stat().st_size} bytes; verified.')
