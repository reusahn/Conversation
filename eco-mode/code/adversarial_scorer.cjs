'use strict';

// C's independent deterministic development checks. No model, person or sensor.
const assert = require('node:assert/strict');
const { createHash } = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const S = require('./development_scorer.cjs');
const counts = {};
function check(group, name, f) {
  try { f(); } catch (e) { e.message = `${group}: ${name}: ${e.message}`; throw e; }
  counts[group] = (counts[group] || 0) + 1;
}
const copy = x => Array.isArray(x) ? x.map(copy) : x;
const same = (x,y) => {
  if (typeof x === 'number' && typeof y === 'number') return x === y;
  if (Array.isArray(x) && Array.isArray(y)) return x.length === y.length && x.every((v,i)=>same(v,y[i]));
  return x === y;
};
let seed = 71129;
const rng = n => { seed = (1664525 * seed + 1013904223) >>> 0; return seed % n; };
function sumExact(xs) {
  let n = 0n;
  for (const x of xs) if (typeof x === 'number' && Number.isFinite(x)) n += BigInt(x);
  return Number(n);
}
function tagsNative(xs) {
  const seen = [];
  for (const x of xs) if (typeof x === 'string') {
    const y = x.replace(/^[ \t\r\n]+|[ \t\r\n]+$/g,'').toLowerCase();
    if (y && !seen.includes(y)) seen.push(y);
  }
  return seen;
}
function mergeHalfGrid(xs) {
  // Independent finite geometric representation for this small test domain.
  const filled = new Set();
  for (const [a,b] of xs) for (let x=2*a;x<=2*b;x++) filled.add(x);
  const out = []; let start = null, last = null;
  for (const x of [...filled].sort((a,b)=>a-b)) {
    if (last !== null && x !== last+1) { out.push([start/2,last/2]); start = null; }
    if (start === null) start = x;
    last = x;
  }
  if (start !== null) out.push([start/2,last/2]);
  return out;
}
function rewardDP(xs) {
  // Weighted scheduling DP, independent of E's exhaustive pairwise subsets.
  const jobs = xs.map(x=>[...x]).sort((a,b)=>a[1]-b[1] || a[0]-b[0]);
  const best = [0];
  for (let i=0;i<jobs.length;i++) {
    let previous = 0;
    for (let j=0;j<i;j++) if (jobs[j][1] <= jobs[i][0]) previous = Math.max(previous,best[j+1]);
    best.push(Math.max(best[i],previous+jobs[i][2]));
  }
  return best.at(-1);
}
function compare(task,input,expected) {
  check('independent_oracle',task,()=>assert.ok(same(S.oracle(task,copy(input)),expected)));
}

const atoms = [-1000,-3,-0,0,1,1000,null,true,false,'2','',NaN,Infinity,-Infinity];
for (let i=0;i<256;i++) {
  const xs = Array.from({length:rng(33)},()=>atoms[rng(atoms.length)]);
  compare('T01',xs,sumExact(xs));
}
const strings = ['', ' ', '\rA\n', '\t B\t', 'b','A\tB','__proto__','constructor','a A','Z!','\r\n'];
for (let i=0;i<256;i++) {
  const pool = [...strings,null,true,4];
  const xs = Array.from({length:rng(33)},()=>pool[rng(pool.length)]);
  compare('T02',xs,tagsNative(xs));
}
const intervals = [];
for (let a=-1;a<=1;a++) for (let b=a;b<=1;b++) intervals.push([a,b]);
function visit(xs,depth) {
  compare('T03',xs,mergeHalfGrid(xs));
  if (depth) for (const x of intervals) visit([...xs,x],depth-1);
}
visit([],3);
const jobsPool = [[-2,-1,3],[-1,0,4],[0,2,5],[-2,2,10],[0,1,0],[1,2,4],[0,1,2],[0,1,2]];
for (let m=0;m<2**jobsPool.length;m++) {
  const xs=jobsPool.filter((_,i)=>m&(1<<i));
  compare('T04',xs,rewardDP(xs));
}
compare('T03',[[-100,-100],[100,100]],[[-100,-100],[100,100]]);
compare('T03',[[0,0],[1,1]],[[0,0],[1,1]]);
compare('T04',Array.from({length:12},(_,i)=>[i,i+1,1000]),12000);

const independent = { T01:sumExact, T02:tagsNative, T03:mergeHalfGrid, T04:rewardDP };
for (const task of Object.keys(independent)) {
  check('score_semantics',`${task} alternate algorithm`,()=>assert.equal(S.scoreSolution(task,independent[task]).status,'observed_success'));
  check('score_semantics',`${task} empty input valid`,()=>assert.equal(S.scoreSolution(task,independent[task],[{id:'empty',input:[]}]).status,'observed_success'));
  check('score_semantics',`${task} throw`,()=>assert.equal(S.scoreSolution(task,()=>{throw new Error('candidate');}).status,'observed_failure'));
  check('score_semantics',`${task} thenable`,()=>assert.equal(S.scoreSolution(task,()=>({then(){}})).status,'observed_failure'));
  check('score_semantics',`${task} oracle throws`,()=>assert.equal(S.scoreSolution(task,independent[task],undefined,{oracle(){throw new Error('oracle');}}).status,'unknown'));
  check('score_semantics',`${task} missing oracle`,()=>assert.equal(S.scoreSolution(task,independent[task],undefined,{oracle:null}).status,'unknown'));
}
const invalidCases = [
  ['T01',new Array(1)], ['T01',[{}]], ['T01',[0.5]], ['T01',Array(33).fill(0)],
  ['T02',['\u00e9']], ['T02',['\u000b']], ['T02',[NaN]], ['T02',['a'.repeat(65)]],
  ['T03',[[1,0]]], ['T03',[[1,Infinity]]], ['T03',[[0,0,1]]], ['T03',[[101,101]]],
  ['T04',[[0,0,1]]], ['T04',[[0,1,-1]]], ['T04',[[0,1,1001]]], ['T04',Array(13).fill([0,1,1])]
];
for (const [task,input] of invalidCases) check('invalid_fixture',task,()=>{
  const result=S.scoreSolution(task,independent[task],[{id:'bad',input}]);
  assert.equal(result.status,'unknown'); assert.equal(result.failure_value,null);
});
const extra=[1]; extra.hidden=4;
const getter=[1]; Object.defineProperty(getter,'0',{get(){throw new Error('accessor invoked');},configurable:true,enumerable:true});
for (const input of [extra,getter]) check('invalid_fixture','unsafe descriptor',()=>assert.equal(S.scoreSolution('T01',sumExact,[{id:'bad',input}]).status,'unknown'));
for (const [name,bank] of [['empty',[]],['null',null],['duplicate',[{id:'a',input:[]},{id:'a',input:[]}]]]) {
  check('bank_health',name,()=>assert.equal(S.scoreSolution('T01',sumExact,bank).status,'unknown'));
}
check('bank_health','unknown task',()=>assert.equal(S.scoreSolution('T05',sumExact).status,'unknown'));
check('bank_health','null options',()=>assert.equal(S.scoreSolution('T01',sumExact,undefined,null).status,'unknown'));
check('candidate_mutation','extra property',()=>assert.equal(S.scoreSolution('T01',xs=>{const y=sumExact(xs);xs.hidden=1;return y;}).status,'observed_failure'));
check('candidate_mutation','nested interval',()=>assert.equal(S.scoreSolution('T03',xs=>{const y=mergeHalfGrid(xs);if(xs.length)xs[0][0]=99;return y;}).status,'observed_failure'));
check('candidate_mutation','prototype',()=>assert.equal(S.scoreSolution('T01',xs=>{const y=sumExact(xs);Object.setPrototypeOf(xs,null);return y;}).status,'observed_failure'));
check('output_contract','signed zero equivalent',()=>assert.equal(S.scoreSolution('T01',()=>-0,[{id:'zero',input:[]}]).status,'observed_success'));
check('output_contract','invalid number',()=>assert.equal(S.scoreSolution('T01',()=>NaN).status,'observed_failure'));
check('output_contract','async rejection',()=>assert.equal(S.scoreSolution('T01',()=>Promise.reject(new Error('fixture'))).status,'observed_failure'));
check('output_contract','throwing then getter',()=>assert.equal(S.scoreSolution('T01',()=>Object.defineProperty({},'then',{get(){throw new Error('bad return');}})).status,'observed_failure'));
for (const task of ['T02','T03']) check('output_contract',`${task} frozen correct output`,()=>{
  const candidate = xs=>{
    const out=independent[task](xs);
    for (const item of out) if (Array.isArray(item)) Object.freeze(item);
    return Object.freeze(out);
  };
  assert.equal(S.scoreSolution(task,candidate).status,'observed_success');
});
check('output_contract','nonenumerable correct numeric data properties',()=>{
  for (const task of ['T02','T03']) {
    const candidate = xs=>{
      const out=independent[task](xs);
      for (const item of out) if (Array.isArray(item)) {
        for (let i=0;i<item.length;i++) Object.defineProperty(item,String(i),{enumerable:false});
      }
      for (let i=0;i<out.length;i++) Object.defineProperty(out,String(i),{enumerable:false});
      return out;
    };
    assert.equal(S.scoreSolution(task,candidate).status,'observed_success');
  }
});

const sha = name=>createHash('sha256').update(fs.readFileSync(path.join(__dirname,name))).digest('hex');
console.log(JSON.stringify({
  kind:'independent_development_numeric_and_fault_checks',
  node:process.version,passed:Object.values(counts).reduce((a,b)=>a+b,0),by_group:counts,
  source_sha256:{'development_scorer.cjs':sha('development_scorer.cjs'),'adversarial_scorer.cjs':sha('adversarial_scorer.cjs')},
  actual_model_inference:false,human_participants:false,device_energy_measurement:false,
  confirmatory_allowed:false,
  limits:['Finite deterministic comparisons are not complete correctness proof.','Trusted synchronous local functions only; no sandbox or timeouts.','All banks and checks are public developer fixtures, not hidden study tests.']
},null,2));
