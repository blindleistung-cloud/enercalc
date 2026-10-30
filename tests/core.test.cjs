'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const core=require('../core/engine.js');
const registry=JSON.parse(fs.readFileSync(path.join(root,'docs/normative/traceability.json'),'utf8'));
const fixtures=JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/core-cases.json'),'utf8'));
const close=(actual,expected,label)=>assert.ok(Math.abs(actual-expected)<=1e-9+Math.abs(expected)*1e-10,
 `${label}: expected ${expected}, actual ${actual}`);

test('saved Excel intermediate values and independent arithmetic match each implemented leaf',()=>{
 assert.ok(fixtures.length>=500);
 for(const c of fixtures){
  const result=core.runReference(c.rule,c.inputs).outputs;
  for(const [key,expected] of Object.entries(c.expected))close(result[key],expected,`${c.label}: ${key}`);
 }
 for(const id of core.implemented)assert.ok(fixtures.some(c=>c.rule===id),`No case for ${id}`);
});

test('source requirements, public factor checks and all implemented rules are traceable',()=>{
 const ids=new Set(registry.rules.map(r=>r.id));assert.equal(ids.size,registry.rules.length);
 for(const id of core.implemented){
  const rule=registry.rules.find(r=>r.id===id);assert.ok(rule);
  assert.ok(rule.expression&&rule.inputFields.length&&rule.outputs.length&&rule.scopeLimit);
  assert.equal(rule.normativeReview.status,'source-required');
  for(const ref of rule.requirements)assert.ok(registry.requirements.some(n=>n.id===ref));
 }
 const emissions=registry.publicSources.find(s=>s.id==='geg9');
 assert.equal(emissions.table.find(r=>r.number===12).value,560);
 assert.equal(emissions.table.find(r=>r.number===2).value,240);
 assert.equal(emissions.table.find(r=>r.number===1).value,310);
 for(const row of registry.factorComparisons){
  const source=registry.publicSources.find(s=>s.id===row.source);assert.ok(source);
  assert.ok(row.workbookCell&&row.item);
 }
});

test('a passed cache match, a supplied factor and a standalone verified flag never imply normative release',()=>{
 assert.equal(core.readiness(registry,core.implemented).ready,false);
 for(const r of registry.rules.filter(r=>r.executionMode!=='current-leaf'))assert.equal(core.reviewStatus(r).normativeVerified,false);
 assert.equal(core.reviewStatus({id:'apply-factor',normativeReview:{status:'verified'}}).normativeVerified,false);
 assert.equal(core.readiness(registry,['made-up-rule']).ready,false);
 assert.throws(()=>core.readiness(registry,[]));
 assert.throws(()=>core.runReference('monthly-balance',{}),/nicht implementiert/);
});

test('gain-utilization limits are stable at gamma=1, at zero gains and at large ratios',()=>{
 const run=(g,a,t=.01)=>core.runReference('heating-utilization',{gamma:g,a,limitThreshold:t}).outputs;
 close(run(1,4).raw,.8,'gamma=1');
 assert.equal(run(0,4).raw,1);
 close(run(1-1e-12,4).raw,.8,'gamma just below 1');
 close(run(1+1e-12,4).raw,.8,'gamma just above 1');
 close(run(1e200,4).raw,1e-200,'large ratio');
 for(const g of [.001,.1,.5,1,2,10,1e9])close(run(g,1).raw,1/(1+g),'independent a=1 identity');
 assert.equal(run(1,1000).limited,1,'legacy limit is explicit');
 assert.equal(run(1,1000,0).limited,1000/1001,'limiting can be inspected separately');
});

test('domains, zero denominators, booleans and invalid inputs fail visibly',()=>{
 assert.throws(()=>core.runReference('window-u',{glassArea:0,frameArea:0,ug:1,uf:1,edgeLength:0,psi:0}));
 assert.throws(()=>core.runReference('thermal-response',{capacity:1,transfer:0,a0:1,tau0:16}));
 assert.throws(()=>core.runReference('heating-part',{losses:1,gains:0,utilization:1,days:31,area:0}));
 assert.throws(()=>core.runReference('heated-area',{zones:[{area:10,heated:'false'}]}));
 assert.throws(()=>core.runReference('heated-area',{zones:Array.from({length:12},()=>({area:1,heated:true}))}));
 assert.throws(()=>core.runReference('apply-factor',{energy:NaN,factor:1}));
 assert.throws(()=>core.runReference('apply-factor',{energy:Infinity,factor:1}));
 assert.throws(()=>core.runReference('apply-factor',{energy:'10',factor:1}));
 assert.throws(()=>core.runReference('apply-factor',{energy:1e308,factor:1e308}));
 assert.throws(()=>core.runReference('heating-utilization',{gamma:-1,a:1,limitThreshold:.01}));
});

test('independent physical identities and unit conversions hold',()=>{
 assert.deepEqual(core.runReference('window-u',{glassArea:.8,frameArea:.2,ug:2,uf:2,edgeLength:0,psi:0}).outputs,{u:2});
 const t=core.runReference('transmission',{components:[{area:10,u:2,reduction:.5}],bridgeDeltaU:.1}).outputs;
 assert.equal(t.base,10);assert.equal(t.bridge,.5);assert.equal(t.coefficient,10.5);
 assert.equal(core.runReference('heat-capacity',{specificCapacity:100,area:100}).outputs.capacity,10);
 assert.equal(core.runReference('air-transfer',{airChanges:.5,volume:100,airCapacity:.34}).outputs.coefficient,17);
 assert.equal(core.runReference('thermal-response',{capacity:1,transfer:100,a0:1,tau0:10}).outputs.tau,10);
 assert.equal(core.runReference('heating-part',{losses:10,gains:100,utilization:1,days:31,area:10}).outputs.specificHeat,0);
 assert.equal(core.runReference('emissions',{energy:1000,factor:560}).outputs.emissions,560);
});

test('geometry does not double count roof windows or accept impossible facade windows',()=>{
 const input={facadeGross:100,facadeWindows:20,groundWalls:10,roofGross:50,roofWindows:5,floor:50,volume:500};
 const result=core.runReference('direct-envelope',input).outputs;
 assert.equal(result.area,210);assert.equal(result.windows,25);assert.equal(result.roof,45);
 const modified=core.runReference('direct-envelope',{...input,roofWindows:20}).outputs;
 assert.equal(result.area,modified.area);
 assert.throws(()=>core.runReference('direct-envelope',{...input,facadeWindows:101}));
 assert.throws(()=>core.runReference('direct-envelope',{...input,roofWindows:51}));
});

test('calculation leaves preserve inputs and return a detached evidence snapshot',()=>{
 const input={zones:[{area:100,heated:true},{area:50,heated:false}]};
 const before=JSON.stringify(input),run=core.runReference('heated-area',input);
 assert.equal(JSON.stringify(input),before);
 run.inputs.zones[0].area=1;
 assert.equal(input.zones[0].area,100);
 assert.equal(run.outputs.area,100);
});

test('current conversion leaves use separate source-backed carriers, not the historical combined factor',()=>{
 const input={energy:1000,asOf:'2026-10-30'};
 const expected=[['grid-electricity',1800,560],['natural-gas',1100,240],['heating-oil',1100,310],['wood',200,20]];
 for(const [carrier,primary,emissions] of expected){
  const p=core.runCurrent(registry,'current-primary',{...input,carrier});
  const c=core.runCurrent(registry,'current-emissions',{...input,carrier});
  assert.equal(p.outputs.primaryEnergy,primary);
  assert.equal(c.outputs.emissions,emissions);
  assert.equal(c.buildingReady,false);
  assert.equal(c.usedSource.id,'geg9');
 }
 assert.equal(core.runCurrent(registry,'current-emissions',{...input,energy:0,carrier:'grid-electricity'}).outputs.emissions,0);
 for(const id of core.implemented)assert.throws(()=>core.runCurrent(registry,id,input),/nicht freigegeben/);
 assert.throws(()=>core.runCurrent(registry,'current-emissions',{...input,carrier:'district-heat'}));
 assert.throws(()=>core.runCurrent(registry,'current-emissions',{...input,energy:-1,carrier:'grid-electricity'}));
});

test('unsupported legal dates including 2027 and omitted dates fail without legacy fallback',()=>{
 const x={energy:1000,carrier:'grid-electricity'};
 assert.throws(()=>core.runCurrent(registry,'current-primary',x),/Stichtag/);
 assert.throws(()=>core.runCurrent(registry,'current-primary',{...x,asOf:'2027-01-01'}),/2027/);
 assert.throws(()=>core.runCurrent(registry,'current-primary',{...x,asOf:'2026-10-29'}),/Stichtag/);
 assert.equal(registry.targetProfile.status,'current-only');
 assert.equal(registry.targetProfile.reviewRequiredFrom,'2027-01-01');
 assert.ok(registry.requirements.some(r=>r.id==='N14'&&r.status==='source-required'));
 assert.equal(core.readiness(registry,['current-primary','current-emissions']).ready,false);
});
