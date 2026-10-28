'use strict';

// Trusted, synchronous, local development fixtures only. This is NOT a sandbox,
// timeout runner, hidden study bank, participant evaluator or model benchmark.
const { isDeepStrictEqual, types } = require('node:util');
const CONTRACT_ID = 'dev-task-contract-v0.1';
const BANK_ID = 'dev-public-bank-v0.1';
const TASKS = ['T01', 'T02', 'T03', 'T04'];

function fail(message) { throw new Error(message); }
function denseArray(value, max, length, requireMutable = true) {
  if (!Array.isArray(value) || Object.getPrototypeOf(value) !== Array.prototype) fail('ordinary_array_required');
  const keys = Reflect.ownKeys(value);
  if (value.length > max || (length !== undefined && value.length !== length) || keys.length !== value.length + 1) fail('array_bounds_or_properties');
  for (let i = 0; i < value.length; i++) {
    const d = Object.getOwnPropertyDescriptor(value, String(i));
    if (!d || !Object.hasOwn(d, 'value') || (requireMutable && (!d.enumerable || !d.configurable || !d.writable))) fail('dense_data_array_required');
  }
  const d = Object.getOwnPropertyDescriptor(value, 'length');
  if (!d || (requireMutable && !d.writable)) fail('mutable_length_required');
}
const integer = (x, lo, hi) => typeof x === 'number' && Number.isInteger(x) && x >= lo && x <= hi;
const ascii = x => typeof x === 'string' && x.length <= 64 && /^[\x09\x0a\x0d\x20-\x7e]*$/.test(x);
function validateInput(taskId, input) {
  if (!TASKS.includes(taskId)) fail('unknown_task');
  denseArray(input, taskId === 'T01' || taskId === 'T02' ? 32 : 12);
  for (const item of input) {
    if (taskId === 'T01' || taskId === 'T02') {
      const ignored = item === null || typeof item === 'boolean' || ascii(item);
      const special = taskId === 'T01' && typeof item === 'number' && !Number.isFinite(item);
      if (!ignored && !special && !integer(item, -1000, 1000)) fail('invalid_mixed_item');
    } else {
      denseArray(item, taskId === 'T03' ? 2 : 3, taskId === 'T03' ? 2 : 3);
      if (!integer(item[0], -100, 100) || !integer(item[1], -100, 100)) fail('invalid_endpoint');
      if (taskId === 'T03' ? item[0] > item[1] : item[0] >= item[1]) fail('invalid_interval');
      if (taskId === 'T04' && !integer(item[2], 0, 1000)) fail('invalid_reward');
    }
  }
  return true;
}
const clone = x => Array.isArray(x) ? x.map(clone) : x;

function oracle(taskId, input) {
  validateInput(taskId, input);
  if (taskId === 'T01') {
    let total = 0;
    for (const item of input) if (typeof item === 'number' && Number.isFinite(item)) total += item;
    return total === 0 ? 0 : total;
  }
  if (taskId === 'T02') {
    const out = [], seen = new Set();
    for (const item of input) {
      if (typeof item !== 'string') continue;
      let begin = 0, end = item.length;
      const blank = c => c === ' ' || c === '\t' || c === '\n' || c === '\r';
      while (begin < end && blank(item[begin])) begin++;
      while (end > begin && blank(item[end - 1])) end--;
      let normalized = '';
      for (const c of item.slice(begin, end)) {
        const n = c.charCodeAt(0);
        normalized += n >= 65 && n <= 90 ? String.fromCharCode(n + 32) : c;
      }
      if (normalized && !seen.has(normalized)) { seen.add(normalized); out.push(normalized); }
    }
    return out;
  }
  if (taskId === 'T03') {
    // Independent interval-overlap graph components, rather than sorted merge.
    const visited = new Set(), out = [];
    for (let i = 0; i < input.length; i++) {
      if (visited.has(i)) continue;
      const queue = [i]; visited.add(i);
      let lo = input[i][0], hi = input[i][1];
      for (let q = 0; q < queue.length; q++) {
        const a = input[queue[q]];
        lo = Math.min(lo, a[0]); hi = Math.max(hi, a[1]);
        for (let j = 0; j < input.length; j++) {
          if (!visited.has(j) && a[0] <= input[j][1] && input[j][0] <= a[1]) {
            visited.add(j); queue.push(j);
          }
        }
      }
      out.push([lo === 0 ? 0 : lo, hi === 0 ? 0 : hi]);
    }
    return out.sort((a,b) => a[0] - b[0]);
  }
  // Independent exhaustive subsets with pairwise compatibility, at most 2^12.
  let best = 0;
  for (let mask = 0; mask < 2 ** input.length; mask++) {
    let reward = 0, valid = true;
    for (let i = 0; i < input.length && valid; i++) if (mask & (1 << i)) {
      reward += input[i][2];
      for (let j = i + 1; j < input.length; j++) if (mask & (1 << j)) {
        const a = input[i], b = input[j];
        if (!(a[1] <= b[0] || b[1] <= a[0])) { valid = false; break; }
      }
    }
    if (valid) best = Math.max(best, reward);
  }
  return best;
}

function outputShape(taskId, value) {
  if (taskId === 'T01') return integer(value, -32000, 32000);
  if (taskId === 'T04') return integer(value, 0, 12000);
  try {
    // Return values need not be writable: a correct frozen result is valid.
    denseArray(value, taskId === 'T02' ? 32 : 12, undefined, false);
    if (taskId === 'T02') return value.every(ascii);
    return value.every(v => { denseArray(v, 2, 2, false); return v.every(x => integer(x, -100, 100)); });
  } catch { return false; }
}
function equivalent(a, b) {
  if (typeof a === 'number' && typeof b === 'number') return a === b || (Number.isNaN(a) && Number.isNaN(b));
  if (Array.isArray(a) && Array.isArray(b)) return a.length === b.length && a.every((x,i) => equivalent(x, b[i]));
  return a === b;
}
function inputUnchanged(input, before) {
  // Accessor/prototype/sparse changes are rejected without invoking accessors.
  try { validateInput(before.taskId, input); } catch { return false; }
  return isDeepStrictEqual(input, before.value);
}
function scoreSolution(taskId, candidate, bank = DEVELOPMENT_BANK[taskId], options = {}) {
  const base = { contract_id: CONTRACT_ID, bank_id: BANK_ID, task_id: taskId,
    measurement_kind: 'development_fixture', stage: 'development_only', real_model_inference: false,
    human_participants: false, device_energy_measurement: false,
    confirmatory_allowed: false, cases: [] };
  const unknown = reason => ({ ...base, status: 'unknown', failure_value: null, reason });
  if (!options || Object.getPrototypeOf(options) !== Object.prototype) return unknown('invalid_options');
  const optionDescriptors = Object.getOwnPropertyDescriptors(options);
  if (Reflect.ownKeys(optionDescriptors).some(k => k !== 'oracle') ||
      (optionDescriptors.oracle && !Object.hasOwn(optionDescriptors.oracle, 'value'))) return unknown('invalid_options');
  const calculate = options.oracle === undefined ? oracle : options.oracle;
  if (!TASKS.includes(taskId)) return unknown('unknown_task');
  if (typeof candidate !== 'function') return unknown('candidate_function_missing');
  if (typeof calculate !== 'function') return unknown('oracle_unavailable');
  const prepared = [];
  try {
    denseArray(bank, 10000);
    if (!bank.length) return unknown('empty_bank');
    const ids = new Set();
    for (const item of bank) {
      if (!item || Object.getPrototypeOf(item) !== Object.prototype) fail('invalid_case');
      const ds = Object.getOwnPropertyDescriptors(item);
      if (Reflect.ownKeys(ds).length !== 2 || !ds.id || !ds.input || !Object.hasOwn(ds.id,'value') || !Object.hasOwn(ds.input,'value')) fail('invalid_case_shape');
      if (typeof item.id !== 'string' || !item.id || ids.has(item.id)) fail('invalid_or_duplicate_case_id');
      ids.add(item.id);
      validateInput(taskId, item.input);
      const forOracle = clone(item.input), snapshot = clone(forOracle);
      const expected = calculate(taskId, forOracle);
      if (types.isPromise(expected)) { expected.catch(() => {}); fail('async_oracle'); }
      if (!inputUnchanged(forOracle, { taskId, value: snapshot })) fail('oracle_mutated_input');
      if (!outputShape(taskId, expected)) fail('invalid_oracle_output');
      prepared.push({ id: item.id, input: clone(item.input), expected: clone(expected) });
    }
  } catch (e) { return unknown('bank_or_oracle_invalid:' + (e?.message || 'error')); }
  for (const item of prepared) {
    const input = clone(item.input), before = { taskId, value: clone(input) };
    let actual, reason = null;
    try {
      actual = candidate(input);
      if (types.isPromise(actual)) { actual.catch(() => {}); reason = 'async_return'; }
      else if (actual && (typeof actual === 'object' || typeof actual === 'function') && typeof actual.then === 'function') reason = 'thenable_return';
      else if (!outputShape(taskId, actual)) reason = 'invalid_return';
    } catch { reason = 'candidate_threw'; }
    if (!inputUnchanged(input, before)) reason = 'input_mutated';
    if (!reason && !equivalent(actual, item.expected)) reason = 'wrong_output';
    base.cases.push({ id: item.id, status: reason ? 'observed_failure' : 'observed_success', reason });
  }
  const failed = base.cases.some(x => x.status === 'observed_failure');
  return { ...base, status: failed ? 'observed_failure' : 'observed_success', failure_value: failed ? 1 : 0,
    reason: failed ? 'required_case_failed' : null };
}

const DEVELOPMENT_BANK = {
  T01: [[], [1,2,3], [1,'2',null,-1], [NaN,3,Infinity,-Infinity], [-1000,1000,-0], [true,false,'',4], Array(32).fill(1000)].map((input,i) => ({id:`sum-${i}`,input})),
  T02: [[], [' A ','a','B',' '], [null,'X',12,true,' x '], ['b','A','B','a'], ['\t Blue\n','RED\r'], ['  ','\n'], ['A\tB','a\tb'], ['__proto__','constructor','__PROTO__']].map((input,i) => ({id:`tags-${i}`,input})),
  T03: [[], [[1,3],[2,5]], [[1,2],[2,3]], [[10,12],[2,4]], [[-4,-2],[-3,0],[2,2]], [[5,8],[1,6],[2,3]], [[0,0],[0,0]], [[-100,100],[0,0]], [[0,1],[2,3]]].map((input,i) => ({id:`merge-${i}`,input})),
  T04: [[], [[0,2,2],[2,4,3]], [[0,1,1],[0,3,10],[1,3,1]], [[0,2,5],[1,3,6],[2,4,5]], [[-3,-1,2],[-1,0,4],[-3,0,5]], [[0,1,0],[1,2,0]], [[0,1,5],[0,1,5]], Array.from({length:12},(_,i)=>[i,i+1,1000])].map((input,i) => ({id:`reward-${i}`,input}))
};
const REFERENCE_SOLUTIONS = {
  T01: xs => xs.reduce((s,x) => s + (typeof x === 'number' && Number.isFinite(x) ? x : 0),0),
  T02: xs => [...new Set(xs.filter(x=>typeof x==='string').map(x=>x.trim().toLowerCase()).filter(Boolean))],
  T03: xs => {
    const out = [];
    for (const [a,b] of xs.map(x=>[...x]).sort((x,y)=>x[0]-y[0] || x[1]-y[1])) {
      const last = out.at(-1);
      if (last && a <= last[1]) last[1] = Math.max(last[1], b); else out.push([a,b]);
    }
    return out;
  },
  T04: xs => {
    const a = xs.map(x=>[...x]).sort((x,y)=>x[1]-y[1] || x[0]-y[0]), dp = [0];
    for (let i=0;i<a.length;i++) {
      let j=i-1; while (j>=0 && a[j][1]>a[i][0]) j--;
      dp.push(Math.max(dp[i],a[i][2]+dp[j+1]));
    }
    return dp.at(-1);
  }
};
const FAULTY_SOLUTIONS = {
  T01: {
    coerce: xs => xs.reduce((s,x)=>s+x,0),
    truthy_only: xs => xs.reduce((s,x)=>s+(typeof x==='number' ? x : 0),0),
    nonnegative: xs => xs.filter(x=>typeof x==='number' && Number.isFinite(x) && x>0).reduce((s,x)=>s+x,0),
    mutates: xs => { xs.reverse(); return REFERENCE_SOLUTIONS.T01(xs); }
  },
  T02: {
    no_dedup: xs => xs.filter(x=>typeof x==='string').map(x=>x.trim().toLowerCase()).filter(Boolean),
    sort_order: xs => REFERENCE_SOLUTIONS.T02(xs).sort(),
    trim_interior: xs => REFERENCE_SOLUTIONS.T02(xs).map(x=>x.replace(/\s/g,'')),
    object_dictionary: xs => {const seen={}; return REFERENCE_SOLUTIONS.T02(xs).filter(x=>!seen[x] && (seen[x]=true));}
  },
  T03: {
    strict_touch: xs => {const out=[];for(const [a,b] of xs.map(x=>[...x]).sort((x,y)=>x[0]-y[0])){const p=out.at(-1);if(p && a<p[1])p[1]=Math.max(p[1],b);else out.push([a,b]);}return out;},
    lexicographic: xs => {const out=[];for(const [a,b] of xs.map(x=>[...x]).sort()){const p=out.at(-1);if(p && a<=p[1])p[1]=Math.max(p[1],b);else out.push([a,b]);}return out;},
    adjacent_integers: xs => {const out=[];for(const [a,b] of xs.map(x=>[...x]).sort((x,y)=>x[0]-y[0])){const p=out.at(-1);if(p && a<=p[1]+1)p[1]=Math.max(p[1],b);else out.push([a,b]);}return out;},
    mutates: xs => {xs.sort((x,y)=>x[0]-y[0]);return REFERENCE_SOLUTIONS.T03(xs);}
  },
  T04: {
    greedy: xs => {let end=-Infinity,total=0;for(const [s,e,r] of xs.map(x=>[...x]).sort((a,b)=>a[1]-b[1]))if(s>=end){total+=r;end=e;}return total;},
    strict_touch: xs => {let best=0;for(let m=0;m<2**xs.length;m++){let sum=0,ok=true;for(let i=0;i<xs.length;i++)if(m&(1<<i)){sum+=xs[i][2];for(let j=i+1;j<xs.length;j++)if(m&(1<<j))if(!(xs[i][1]<xs[j][0]||xs[j][1]<xs[i][0]))ok=false;}if(ok)best=Math.max(best,sum);}return best;},
    sum_all: xs => xs.reduce((s,x)=>s+x[2],0),
    mutates: xs => {xs.reverse();return REFERENCE_SOLUTIONS.T04(xs);}
  }
};
module.exports = { CONTRACT_ID, BANK_ID, DEVELOPMENT_BANK, REFERENCE_SOLUTIONS, FAULTY_SOLUTIONS,
  validateInput, oracle, scoreSolution };
