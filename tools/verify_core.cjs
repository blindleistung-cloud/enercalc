/* Re-run all stored comparisons and write an auditable result summary. */
'use strict';
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const core=require('../core/engine.js');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const fixtures=read('tests/fixtures/core-cases.json'),registry=read('docs/normative/traceability.json');
const results={};
for(const c of fixtures){
 const stats=results[c.rule]||={passed:0,failed:0,cases:0,referenceKinds:{}};
 stats.cases++;stats.referenceKinds[c.referenceKind]=(stats.referenceKinds[c.referenceKind]||0)+1;
 try{
  const outputs=core.runReference(c.rule,c.inputs).outputs;
  for(const [key,expected] of Object.entries(c.expected)){
   if(Math.abs(outputs[key]-expected)>1e-9+Math.abs(expected)*1e-10)throw new Error(`${key}: ${outputs[key]} / ${expected}`);
  }
  stats.passed++;
 }catch(e){stats.failed++;console.error(c.label,e.message);}
}
const failed=Object.values(results).reduce((a,r)=>a+r.failed,0);
const report={schemaVersion:1,engineVersion:'0.1.0',workbookSha256:registry.sourceWorkbookSha256,
  tolerance:{absolute:1e-9,relative:1e-10},total:fixtures.length,passed:fixtures.length-failed,failed,
  scope:'Vergleich gespeicherter Zwischenwerte; keine Excel-Neuberechnung. Nichtnumerische Cachewerte, nicht unterstützte Definitionsbereiche und leere Zonen werden nicht als bestandene Fälle gewertet.',
  normativeReady:false,results};
fs.writeFileSync(path.join(root,'docs/normative/check-results.json'),JSON.stringify(report,null,2)+'\n');
console.log(`${report.passed}/${report.total} comparisons passed; ${failed} failed. Normative release: NOT established.`);
if(failed)process.exitCode=1;
