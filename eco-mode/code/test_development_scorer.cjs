'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { oracle, scoreSolution, DEVELOPMENT_BANK, REFERENCE_SOLUTIONS, FAULTY_SOLUTIONS,
  validateInput, CONTRACT_ID, BANK_ID } = require('./development_scorer.cjs');

for (const id of ['T01','T02','T03','T04']) {
  test(`${id}: reference passes the public development bank`, () => {
    const result = scoreSolution(id, REFERENCE_SOLUTIONS[id]);
    assert.equal(result.status, 'observed_success');
    assert.equal(result.cases.length, DEVELOPMENT_BANK[id].length);
    assert.equal(result.contract_id, CONTRACT_ID); assert.equal(result.bank_id, BANK_ID);
    assert.equal(result.real_model_inference, false); assert.equal(result.confirmatory_allowed, false);
    assert.equal(result.failure_value, 0);
  });
  for (const [name, fn] of Object.entries(FAULTY_SOLUTIONS[id])) {
    test(`${id}: bank rejects ${name}`, () => {
      const r = scoreSolution(id, fn);
      assert.equal(r.status, 'observed_failure'); assert.equal(r.failure_value, 1);
      assert.ok(r.cases.some(c => c.status === 'observed_failure'));
    });
  }
}

test('invalid or empty banks remain unknown, never vacuous success', () => {
  for (const bank of [[], null, undefined, new Array(2), [{id:'bad',input:[{}]}], [{id:'x',input:[]},{id:'x',input:[]}]]) {
    // undefined intentionally selects the default; all other invalids are unknown.
    if (bank === undefined) continue;
    const r = scoreSolution('T01', REFERENCE_SOLUTIONS.T01, bank);
    assert.equal(r.status, 'unknown'); assert.equal(r.failure_value, null); assert.deepEqual(r.cases, []);
  }
});
test('validate entire bank before running any candidate', () => {
  let calls=0;
  const r=scoreSolution('T01', () => {calls++;return 0;}, [{id:'ok',input:[]},{id:'bad',input:[{}]}]);
  assert.equal(r.status,'unknown'); assert.equal(calls,0);
});
test('unknown task and absent callable are infrastructure unknown', () => {
  assert.equal(scoreSolution('unknown',()=>0).status,'unknown');
  assert.equal(scoreSolution('T01',null).status,'unknown');
});
test('oracle throw, mutation, invalid shape and asynchronous oracle stay unknown', async () => {
  const bank = [{id:'one',input:[1]}];
  for (const calculate of [()=>{throw Error('oracle outage');},(_id,x)=>{x.push(1);return 1;},()=>NaN,()=>undefined,async()=>{throw Error('async oracle');}]) {
    const r=scoreSolution('T01',REFERENCE_SOLUTIONS.T01,bank,{oracle:calculate});
    assert.equal(r.status,'unknown'); assert.equal(r.failure_value,null);
  }
  await new Promise(resolve=>setImmediate(resolve));
});
test('bad options cannot invoke an accessor or escape classification', () => {
  assert.equal(scoreSolution('T01',()=>0,[],null).status,'unknown');
  let accessed=false;
  const options={get oracle(){accessed=true;throw Error('accessor');}};
  assert.equal(scoreSolution('T01',()=>0,[],options).status,'unknown');
  assert.equal(accessed,false);
});
test('candidate throw, wrong primitive and invalid shape are observed failures', () => {
  for (const fn of [()=>{throw Error('candidate');},()=>NaN,()=>Infinity,()=>undefined,()=>({}),()=>0]) {
    const r=scoreSolution('T01',fn,[{id:'one',input:[1]}]);
    assert.equal(r.status,'observed_failure'); assert.equal(r.failure_value,1);
  }
});
test('candidate Promise rejection, thenables and throwing then getter do not crash the suite', async () => {
  for (const fn of [async()=>{throw Error('candidate rejected');},()=>Promise.resolve(1),()=>({then(){}}),()=>({get then(){throw Error('getter');}})]) {
    assert.equal(scoreSolution('T01',fn,[{id:'one',input:[1]}]).status,'observed_failure');
  }
  await new Promise(resolve=>setImmediate(resolve));
});
test('candidate input mutation that returns correct output is still failure', () => {
  const r=scoreSolution('T03',x=>{const v=REFERENCE_SOLUTIONS.T03(x);x[0][0]=99;return v;},[{id:'one',input:[[1,2]]}]);
  assert.equal(r.status,'observed_failure'); assert.equal(r.cases[0].reason,'input_mutated');
});
test('input accessor/prototype/property changes are mutation without getter execution', () => {
  let called=false;
  const r=scoreSolution('T01',x=>{Object.defineProperty(x,'0',{get(){called=true;throw Error('getter');}});return 1;},[{id:'one',input:[1]}]);
  assert.equal(r.status,'observed_failure'); assert.equal(called,false);
  assert.equal(scoreSolution('T01',x=>{x.extra=1;return 1;},[{id:'one',input:[1]}]).status,'observed_failure');
});
test('candidate receives clones, preserving source fixtures between runs', () => {
  const bank=[{id:'one',input:[[1,2],[3,4]]}];
  scoreSolution('T03',x=>{x.reverse();x[0][0]=99;return [];},bank);
  assert.deepEqual(bank,[{id:'one',input:[[1,2],[3,4]]}]);
  assert.equal(scoreSolution('T03',REFERENCE_SOLUTIONS.T03,bank).status,'observed_success');
});
test('zero output treats signed zero as equivalent, while input signed-zero mutation is observable', () => {
  assert.equal(scoreSolution('T01',()=>-0,[{id:'zero',input:[]}]).status,'observed_success');
  assert.equal(scoreSolution('T01',x=>{x[0]=0;return 0;},[{id:'zero',input:[-0]}]).status,'observed_failure');
});
test('bounds, sparse arrays, accessors, symbols and exotic inputs reject before scoring', () => {
  const getter=[];Object.defineProperty(getter,'0',{get(){throw Error('not invoked');},enumerable:true});
  const extra=[1];extra.a=1;
  const sym=[1];sym[Symbol('x')]=1;
  const custom=[1];Object.setPrototypeOf(custom,null);
  for (const input of [new Array(1),getter,extra,sym,custom,[undefined],[1.5],[1001],['é'],[{}],Array(33).fill(0),Object.freeze([1])]) {
    assert.equal(scoreSolution('T01',()=>0,[{id:'bad',input}]).status,'unknown');
  }
  for (const [id,input] of [['T03',[[1,0]]],['T03',[[0,101]]],['T04',[[0,0,1]]],['T04',[[0,1,-1]]],['T04',Array(13).fill([0,1,1])],['T02',['\v']]]) {
    assert.equal(scoreSolution(id,()=>0,[{id:'bad',input}]).status,'unknown');
  }
});
test('ASCII normalization preserves interior whitespace and first appearance', () => {
  assert.deepEqual(oracle('T02',['\t A\r','a','B',' b ','A B','a\tb',false,99]),['a','b','a b','a\tb']);
});
test('closed interval graph agrees with sorted merge on all 1000 ordered triples over small domain', () => {
  const intervals=[];for(let a=-1;a<=2;a++)for(let b=a;b<=2;b++)intervals.push([a,b]);
  let checks=0;
  // All ordered triples: 10^3. This is a finite grid check, not all valid inputs.
  for(const a of intervals)for(const b of intervals)for(const c of intervals){
    assert.deepEqual(oracle('T03',[a,b,c]),REFERENCE_SOLUTIONS.T03([a,b,c]));checks++;
  }
  assert.equal(checks,1000);
});
test('exhaustive scheduler agrees with dynamic programming on 1728 ordered triples', () => {
  const jobs=[];for(let s=0;s<3;s++)for(let e=s+1;e<=3;e++)for(const r of [0,2])jobs.push([s,e,r]);
  let checks=0;
  for(const a of jobs)for(const b of jobs)for(const c of jobs){
    assert.equal(oracle('T04',[a,b,c]),REFERENCE_SOLUTIONS.T04([a,b,c]));checks++;
  }
  assert.equal(checks,1728);
});
test('endpoint contact, duplicate jobs, empty and maximum-length values have explicit semantics', () => {
  assert.equal(oracle('T04',[[0,1,5],[0,1,5],[1,2,6]]),11);
  assert.equal(oracle('T04',[]),0);
  assert.equal(oracle('T04',Array.from({length:12},(_,i)=>[i,i+1,1000])),12000);
  assert.deepEqual(oracle('T03',[[2,2],[1,2],[2,3],[-0,0]]),[[0,0],[1,3]]);
  assert.equal(oracle('T01',[NaN,Infinity,-Infinity,'3',true,null,-1000,1000,-0]),0);
});
test('development cases are not claims about humans, model performance or measured energy', () => {
  const r=scoreSolution('T01',REFERENCE_SOLUTIONS.T01);
  assert.equal(r.measurement_kind,'development_fixture'); assert.equal(r.stage,'development_only');
  assert.equal(r.human_participants,false); assert.equal(r.device_energy_measurement,false);
  assert.equal(r.confirmatory_allowed,false);
});

test('correct read-only outputs pass: output writability is not part of task correctness', () => {
  const tags = xs => Object.freeze(REFERENCE_SOLUTIONS.T02(xs));
  const intervals = xs => Object.freeze(REFERENCE_SOLUTIONS.T03(xs).map(x => Object.freeze(x)));
  assert.equal(scoreSolution('T02',tags).status,'observed_success');
  assert.equal(scoreSolution('T03',intervals).status,'observed_success');
});

test('correct output data does not require enumerable index properties', () => {
  const readonlyData = xs => {
    xs.forEach((x,i) => Object.defineProperty(xs, String(i), {
      value: Array.isArray(x) ? readonlyData(x) : x,
      enumerable: false, writable: false, configurable: false
    }));
    return Object.freeze(xs);
  };
  assert.equal(scoreSolution('T02',xs=>readonlyData(REFERENCE_SOLUTIONS.T02(xs))).status,'observed_success');
  assert.equal(scoreSolution('T03',xs=>readonlyData(REFERENCE_SOLUTIONS.T03(xs))).status,'observed_success');
});
