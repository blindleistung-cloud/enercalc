/* Reusable calculation leaves. No DOM, Excel evaluator or implicit norm defaults. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.EnerCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function number(v, name, min=-Infinity, max=Infinity) {
    if(typeof v!=='number'||!Number.isFinite(v)||v<min||v>max)throw new RangeError(`${name}: ungültiger Zahlenwert.`);
    return v;
  }
  function positive(v,name){number(v,name,0);if(v===0)throw new RangeError(`${name}: muss größer als null sein.`);return v;}
  function array(xs,name){if(!Array.isArray(xs)||!xs.length)throw new TypeError(`${name}: nichtleere Liste erforderlich.`);return xs;}
  const sum=xs=>xs.reduce((a,b)=>a+b,0);
  const kernels={
    'heated-area': p => {
      array(p.zones,'Zonen');if(p.zones.length>11)throw new RangeError('Höchstens elf Zonen.');
      p.zones.forEach(z=>{number(z.area,'Zonenfläche',0);if(typeof z.heated!=='boolean')throw new TypeError('Beheizt muss ein boolescher Wert sein.');});
      return {area:sum(p.zones.filter(z=>z.heated).map(z=>z.area)),totalArea:sum(p.zones.map(z=>z.area))};
    },
    'direct-envelope': p => {
      for(const k of ['facadeGross','facadeWindows','groundWalls','roofGross','roofWindows','floor'])number(p[k],k,0);
      positive(p.volume,'Volumen');
      if(p.facadeWindows>p.facadeGross||p.roofWindows>p.roofGross)throw new RangeError('Fensterfläche überschreitet die zugehörige Bruttofläche.');
      const walls=p.facadeGross-p.facadeWindows,roof=p.roofGross-p.roofWindows;
      const windows=p.facadeWindows+p.roofWindows;
      const area=walls+roof+windows+p.groundWalls+p.floor;
      return {walls,roof,windows,area,compactness:area/p.volume};
    },
    'window-u': p => {
      for(const k of ['glassArea','frameArea','ug','uf','edgeLength','psi'])number(p[k],k,0);
      const windowArea=positive(p.glassArea+p.frameArea,'Fensterfläche');
      return {u:(p.glassArea*p.ug+p.frameArea*p.uf+p.edgeLength*p.psi)/windowArea};
    },
    'transmission': p => {
      array(p.components,'Bauteile');number(p.bridgeDeltaU,'Wärmebrückenzuschlag',0);
      for(const c of p.components){number(c.area,'Bauteilfläche',0);number(c.u,'U-Wert',0);number(c.reduction,'Reduktionsfaktor',0,1);}
      const base=sum(p.components.map(c=>c.area*c.u*c.reduction));
      const weightedArea=sum(p.components.map(c=>c.area*c.reduction));
      const bridge=p.bridgeDeltaU*weightedArea;
      return {base,bridge,coefficient:base+bridge,weightedArea};
    },
    'heat-capacity': p => ({capacity:number(p.specificCapacity,'Wirksame Speicherkapazität',0)*number(p.area,'Fläche',0)/1000}),
    'air-transfer': p => ({coefficient:number(p.airChanges,'Luftwechsel',0)*number(p.volume,'Luftvolumen',0)*number(p.airCapacity,'Volumetrische Wärmekapazität',0)}),
    'thermal-response': p => {
      const tau=number(p.capacity,'Speicherkapazität',0)*1000/positive(p.transfer,'Gesamt-Wärmetransferkoeffizient');
      return {tau,a:number(p.a0,'a₀',0)+tau/positive(p.tau0,'τ₀')};
    },
    'heating-utilization': p => {
      const g=number(p.gamma,'Gewinn-/Verlustverhältnis',0),a=positive(p.a,'Numerischer Parameter');
      const limit=number(p.limitThreshold,'Excel-Begrenzung',0,1);
      // Algebraically equivalent form avoids overflow for gamma > 1 and
      // cancellation near gamma = 1. The threshold is a supplied legacy input.
      let raw;
      if(g===0)raw=1;
      else if(g===1)raw=a/(a+1);
      else if(g<1)raw=Math.expm1(a*Math.log(g))/Math.expm1((a+1)*Math.log(g));
      else {const x=Math.log(g);
        // (1-g^-a)/(g-g^-a), arranged without large positive powers.
        raw=(-Math.expm1(-a*x))/(Math.expm1(x)-Math.expm1(-a*x));}
      const limited=1-raw*g<limit?1/g:raw;
      return {raw,limited};
    },
    'heating-part': p => {
      const loss=number(p.losses,'Senken'),gain=number(p.gains,'Quellen',0);
      const eta=number(p.utilization,'Ausnutzungsgrad',0,1);
      return {specificHeat:Math.max(0,(loss-eta*gain)*number(p.days,'Tage',0,31)/positive(p.area,'Zonenfläche'))};
    },
    'apply-factor': p => ({energy:number(p.energy,'Energiemenge',0)*number(p.factor,'Faktor',0)}),
    'emissions': p => ({emissions:number(p.energy,'Endenergie',0)*number(p.factor,'Emissionsfaktor',0)/1000})
  };
  function runReference(id,inputs){
    if(!Object.hasOwn(kernels,id))throw new Error(`Rechenregel nicht implementiert: ${id}`);
    const snapshot=JSON.parse(JSON.stringify(inputs));
    // Validate original inputs, so NaN/Infinity are not silently converted to null.
    const result=kernels[id](inputs);
    for(const [key,value] of Object.entries(result))number(value,key);
    return {rule:id,inputs:snapshot,outputs:result};
  }
  function reviewStatus(rule){
    const review=rule.normativeReview||{};
    const verified=review.status==='verified'&&typeof review.edition==='string'&&review.edition.length>0&&
      Array.isArray(review.evidence)&&review.evidence.length>0&&typeof review.reviewer==='string'&&review.reviewer.length>0;
    return {implemented:Object.hasOwn(kernels,rule.id)||rule.executionMode==='current-leaf',normativeVerified:verified&&review.scope==='leaf-only',
      label:verified&&review.scope==='leaf-only'?'Normbeleg für diesen Einzelbaustein geprüft':'Normprüfung offen'};
  }
  function readiness(registry,ids){
    array(ids,'Rechenregeln');
    const unique=[...new Set([...ids,...(registry.requiredCurrentRules||[])])];
    const issues=unique.flatMap(id=>{
      const rule=registry.rules.find(r=>r.id===id);
      if(!rule)return [{rule:id,reason:'Rechenregel nicht registriert'}];
      const status=reviewStatus(rule);
      return [...(rule.executionMode==='reference-only'?[{rule:id,reason:'Historischer Auditbaustein ist kein aktuelles Zielverfahren'}]:[]),...(!status.implemented?[{rule:id,reason:'Implementierung fehlt'}]:[]),
        ...(!status.normativeVerified?[{rule:id,reason:'Normativer Verfahrensnachweis fehlt'}]:[])];
    });
    if(registry.targetProfile?.deploymentReady!==true)issues.push({rule:'project-profile',reason:'Aktuelles Gesamtverfahren und Bundesbau-/Bundeswehr-Anforderungen sind nicht vollständig freigegeben'});
    return {ready:issues.length===0,issues};
  }
  function runCurrent(registry,id,inputs){
    const rule=registry.rules.find(r=>r.id===id);
    if(!rule||rule.executionMode!=='current-leaf'||!reviewStatus(rule).normativeVerified)throw new Error('Für das aktuelle Zielprofil nicht freigegeben. Kein Rückgriff auf das Excel-Altverfahren.');
    if(inputs.asOf!==registry.targetProfile.asOf)throw new Error(`Quellen nur für den geprüften Stichtag ${registry.targetProfile.asOf} zugeordnet. Für andere Stichtage einschließlich 2027 ist eine neue Rechts-/Normprüfung erforderlich.`);
    const quantity=number(inputs.energy,'Bereits bestimmter Endenergiebedarf [kWh]',0);
    const carrier=registry.currentFactors.find(c=>c.id===inputs.carrier);
    if(!carrier)throw new Error('Energieträger nicht im geprüften aktuellen Teilkatalog.');
    let outputs,usedSource;
    if(id==='current-primary'){
      outputs={primaryEnergy:quantity*number(carrier.primary,'Primärenergiefaktor',0)};usedSource=carrier.primarySource;
    }else if(id==='current-emissions'){
      outputs={emissions:quantity*number(carrier.co2,'Emissionsfaktor',0)/1000};usedSource=carrier.co2Source;
    }else throw new Error('Aktuelles Verfahren nicht implementiert.');
    for(const [k,v] of Object.entries(outputs))number(v,k);
    return {rule:id,inputs:{energy:quantity,carrier:carrier.id,asOf:inputs.asOf},outputs,usedFactor:id==='current-primary'?carrier.primary:carrier.co2,
      usedSource,scope:'Energieträgerbezogene Umrechnung eines extern bestimmten Endenergiebedarfs; keine Gebäude-Gesamtbilanz.',
      buildingReady:false};
  }
  return {runReference,runCurrent,readiness,reviewStatus,implemented:Object.keys(kernels)};
});
