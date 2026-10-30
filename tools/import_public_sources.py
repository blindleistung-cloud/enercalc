"""Import already fetched public legislative HTML. Does not fetch or execute it.
Usage: python tools/import_public_sources.py /path/to/snapshots
"""
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
URLS={
 'geg20':'https://www.gesetze-im-internet.de/geg/__20.html',
 'geg21':'https://www.gesetze-im-internet.de/geg/__21.html',
 'geg22':'https://www.gesetze-im-internet.de/geg/__22.html',
 'geg4':'https://www.gesetze-im-internet.de/geg/anlage_4.html',
 'geg9':'https://www.gesetze-im-internet.de/geg/anlage_9.html',
 'gegFull':'https://www.gesetze-im-internet.de/geg/BJNR172810020.html',
}
class PublicText(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.rows=[];self.row=None;self.cell=None;self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t=='tr':self.row=[]
  if t in ['td','th']:self.cell=[]
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t in ['td','th'] and self.cell is not None:
   if self.row is not None:self.row.append(' '.join(self.cell))
   self.cell=None
  if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
 def handle_data(self,d):
  if not self.skip and d.strip():
   self.parts.append(d.strip())
   if self.cell is not None:self.cell.append(d.strip())


def main(folder):
 out=[]
 dest=ROOT/'docs/normative/public';dest.mkdir(parents=True,exist_ok=True)
 for id,url in URLS.items():
  raw=(folder/(id+'.html')).read_bytes();p=PublicText();p.feed(raw.decode('utf-8',errors='replace'))
  text='\n'.join(p.parts)
  # Only the title / change-history of the full consolidated document is needed.
  if id=='gegFull':text=text[:text.index('Nichtamtliches Inhaltsverzeichnis\nInhaltsübersicht')]
  (dest/(id+'.txt')).write_text(text.rstrip()+'\n')
  rows=[]
  for row in p.rows:
   if len(row)>=3 and row[0].isdigit():
    try:value=float(row[-1].replace(',','.'))
    except ValueError:continue
    rows.append(dict(number=int(row[0]),carrier=row[-2],value=value))
  out.append(dict(id=id,url=url,retrievedAt=datetime.now(timezone.utc).isoformat(),
                  kind='public-legislation',title=p.parts[0],htmlSha256=hashlib.sha256(raw).hexdigest(),
                  snapshot='public/'+id+'.txt',table=rows if id in ['geg4','geg9'] else []))
 # Record the identity actually returned by the official source, not the old URL name.
 head=next(s for s in out if s['id']=='gegFull')
 head['observedLawName']='Gebäudemodernisierungsgesetz (GModG)'
 head['observedAmendment']='Art. 4 G v. 23.7.2026 I Nr. 226 (Angabe des abgerufenen Texts)'
 assert 'GModG' in (dest/'gegFull.txt').read_text()
 primary=next(s for s in out if s['id']=='geg4')['table']
 co2=next(s for s in out if s['id']=='geg9')['table']
 assert next(r for r in primary if r['number']==9)['value']==1.8
 assert next(r for r in co2 if r['number']==12)['value']==560
 (ROOT/'docs/normative/sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('Saved',len(out),'public sources; parsed',len(primary),'primary-energy rows and',len(co2),'emissions rows.')

if __name__=='__main__':main(Path(sys.argv[1]))
