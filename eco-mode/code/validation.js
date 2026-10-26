
function runValidation() {
  const checks = [];
  const check = (name, condition) => { checks.push({name, pass:!!condition}); };
  const eq = (a,b) => Object.is(a,b) || (a && b && typeof a==="object" && typeof b==="object" && Array.isArray(a)===Array.isArray(b) && Object.keys(a).length===Object.keys(b).length && Object.keys(a).every(k=>Object.hasOwn(b,k) && eq(a[k],b[k])));
  const clone = x => Array.isArray(x)?x.map(clone):(x && typeof x==="object"?Object.fromEntries(Object.entries(x).map(([k,v])=>[k,clone(v)])):x);
  const tasks = [
    {
      id:"T01", name:"sumFiniteNumbers",
      requirement:"Sum only finite JavaScript numbers; ignore strings, null, NaN and infinities. Do not mutate the array.",
      reference:xs=>xs.reduce((s,x)=>s+(typeof x==="number" && Number.isFinite(x)?x:0),0),
      buggy:xs=>xs.reduce((s,x)=>s+x,0),
      cases:[
        {input:[1,2,3],expected:6},{input:[],expected:0},
        {input:[1,"2",null,-1],expected:0},{input:[NaN,3],expected:3},
        {input:[Infinity,-Infinity,4],expected:4},{input:[-.5,1.25],expected:.75}
      ]
    },
    {
      id:"T02",name:"normalizeTags",
      requirement:"Keep string items only. Trim, lowercase, remove empty strings, remove duplicates preserving first appearance. Do not mutate input.",
      reference:xs=>[...new Set(xs.filter(x=>typeof x==="string").map(x=>x.trim().toLowerCase()).filter(Boolean))],
      buggy:xs=>xs.map(x=>x.toLowerCase()),
      cases:[
        {input:[" A ","a","B"," "],expected:["a","b"]},
        {input:[],expected:[]},{input:[null,"X",12," x "],expected:["x"]},
        {input:["b","A","B","a"],expected:["b","a"]},
        {input:["\t Blue\n","RED"],expected:["blue","red"]},
        {input:["  ","\n"],expected:[]}
      ]
    },
    {
      id:"T03",name:"mergeIntervals",
      requirement:"Input contains valid closed numeric [start,end] intervals with start<=end. Sort and merge overlapping or touching intervals. Do not mutate any input array.",
      reference:xs=>{
        const out=[];
        for(const [a,b] of xs.map(x=>[...x]).sort((x,y)=>x[0]-y[0] || x[1]-y[1])) {
          const last=out.at(-1);
          if(last && a<=last[1]) last[1]=Math.max(last[1],b); else out.push([a,b]);
        }
        return out;
      },
      buggy:xs=>{
        const out=[];
        for(const [a,b] of xs.sort()) {
          const last=out.at(-1);
          if(last && a<last[1]) last[1]=Math.max(last[1],b); else out.push([a,b]);
        }
        return out;
      },
      cases:[
        {input:[[1,3],[2,5]],expected:[[1,5]]},
        {input:[[1,2],[2,3]],expected:[[1,3]]},
        {input:[[10,12],[2,4]],expected:[[2,4],[10,12]]},
        {input:[[-4,-2],[-3,0],[2,2]],expected:[[-4,0],[2,2]]},
        {input:[],expected:[]},
        {input:[[5,8],[1,6],[2,3]],expected:[[1,8]]}
      ]
    },
    {
      id:"T04",name:"maxReward",
      requirement:"Each job is [start,end,reward], with finite numeric start<end and nonnegative reward. Return maximum total reward from non-overlapping jobs. Jobs touching at endpoints are compatible. Do not mutate input.",
      reference:jobs=>{
        const a=jobs.map(x=>[...x]).sort((x,y)=>x[1]-y[1] || x[0]-y[0]);
        const dp=[0];
        for(let i=0;i<a.length;i++){
          let j=i-1;
          while(j>=0 && a[j][1]>a[i][0]) j--;
          dp.push(Math.max(dp[i],a[i][2]+dp[j+1]));
        }
        return dp.at(-1);
      },
      buggy:jobs=>{
        let end=-Infinity,total=0;
        for(const [s,e,r] of jobs.sort((a,b)=>a[1]-b[1])) if(s>=end){total+=r;end=e;}
        return total;
      },
      cases:[
        {input:[],expected:0},
        {input:[[0,2,2],[2,4,3]],expected:5},
        {input:[[0,1,1],[0,3,10],[1,3,1]],expected:10},
        {input:[[0,2,5],[1,3,6],[2,4,5]],expected:10},
        {input:[[-3,-1,2],[-1,0,4],[-3,0,5]],expected:6},
        {input:[[0,1,0],[1,2,0]],expected:0}
      ]
    }
  ];
  const taskResults=tasks.map(t=>{
    let referencePassed=0, buggyRejected=0;
    t.cases.forEach((c,i)=>{
      const input=clone(c.input),before=clone(input);
      const value=t.reference(input);
      const ok=eq(value,c.expected) && eq(input,before);
      check(t.id+" reference case "+(i+1),ok);
      if(ok) referencePassed++;
      let bad=false;
      try {
        const badInput=clone(c.input),snap=clone(badInput);
        bad=!eq(t.buggy(badInput),c.expected) || !eq(badInput,snap);
      } catch { bad=true; }
      if(bad) buggyRejected++;
    });
    check(t.id+" rejects supplied faulty solution",buggyRejected>0);
    return {id:t.id,name:t.name,cases:t.cases.length,referencePassed,buggyRejected,
      note:"Engineering fixture only; no LLM output or participant performance was measured."};
  });
  function summarize(attempts) {
    const unique=new Map();
    for(const a of attempts) {
      if(unique.has(a.id)) {
        if(!eq(unique.get(a.id),a)) throw Error("conflicting_duplicate");
      } else unique.set(a.id,a);
    }
    const a=[...unique.values()].sort((x,y)=>x.start_ms-y.start_ms);
    const issues=[];
    let known=0, input=0, output=0, energyComplete=true;
    const scopes=new Set();
    const sources=new Set();
    for(let i=0;i<a.length;i++){
      const x=a[i];
      if(x.stop_ms<x.start_ms) issues.push("invalid_time");
      if(i && x.start_ms<a[i-1].stop_ms) issues.push("overlap");
      input+=x.input_tokens; output+=x.output_tokens;
      sources.add(x.source);scopes.add(x.scope);
      if(!Number.isFinite(x.before_mj) || !Number.isFinite(x.after_mj)) {
        energyComplete=false;issues.push("missing_energy");continue;
      }
      if(x.after_mj<x.before_mj){
        energyComplete=false;issues.push("counter_reset");continue;
      }
      known+=(x.after_mj-x.before_mj)/1000;
    }
    if(scopes.size>1) issues.push("mixed_scope");
    if(sources.size>1) issues.push("mixed_source");
    const invalid=["overlap","invalid_time","mixed_scope","mixed_source"];
    if(issues.some(x=>invalid.includes(x))) energyComplete=false;
    const measured=a.length>0 && energyComplete && [...sources].every(x=>x==="measured_fixture");
    return {attempts:a.length,input_tokens:input,output_tokens:output,known_energy_j:known,
      total_energy_j:energyComplete?known:null,measurement_valid:measured,issues:[...new Set(issues)],
      final_status:a.at(-1)?.status ?? "not_started",
      notice:"All energy values in this validation are synthetic fixture values, never device measurements."};
  }
  const attempt=(id,start,stop,before,after,status="success",extra={})=>({
    id,start_ms:start,stop_ms:stop,before_mj:before,after_mj:after,
    input_tokens:10,output_tokens:5,status,source:"measured_fixture",scope:"gpu_fixture",...extra
  });
  const basic=attempt("a1",0,1000,1000,13000);
  const retry1=attempt("r1",0,1000,0,4000,"failed");
  const retry2=attempt("r2",1100,2000,5000,13000);
  const normal=summarize([basic]);
  check("normal energy 12J",normal.total_energy_j===12);
  const retry=summarize([retry1,retry2]);
  check("failed attempt included in retry total",retry.total_energy_j===12 && retry.attempts===2);
  const duplicate=summarize([basic,clone(basic)]);
  check("identical telemetry duplicate counted once",duplicate.total_energy_j===12 && duplicate.attempts===1);
  let conflict=false;try{summarize([basic,{...basic,after_mj:14000}]);}catch(e){conflict=e.message==="conflicting_duplicate";}
  check("conflicting duplicate rejected",conflict);
  const cancel=summarize([attempt("c1",0,3000,0,9000,"cancelled",{cancel_requested_ms:1000})]);
  check("cancellation charged through actual stop",cancel.total_energy_j===9);
  const missing=summarize([attempt("m1",0,1000,null,null,"failed")]);
  check("missing energy not replaced with zero",missing.total_energy_j===null && missing.issues.includes("missing_energy"));
  const reset=summarize([attempt("x1",0,1000,4000,1000,"failed")]);
  check("counter reset invalidates total",reset.total_energy_j===null && reset.issues.includes("counter_reset"));
  const overlap=summarize([basic,attempt("o1",500,1500,13000,17000)]);
  check("overlap blocks attribution",overlap.total_energy_j===null && overlap.issues.includes("overlap"));
  const scope=summarize([basic,attempt("s2",1100,2000,13000,17000,"success",{scope:"wall_fixture"})]);
  check("incompatible scopes never summed as valid total",scope.total_energy_j===null);
  const estimate=summarize([attempt("est",0,1000,0,3000,"success",{source:"estimated_fixture"})]);
  check("estimate never marked measured",estimate.total_energy_j===3 && !estimate.measurement_valid);
  const failed=summarize([attempt("f1",0,1000,0,2000,"abandoned")]);
  check("abandoned task consumption retained",failed.total_energy_j===2 && failed.final_status==="abandoned");
  const empty=summarize([]);
  check("unattempted task classified separately",empty.final_status==="not_started" && empty.attempts===0 && !empty.measurement_valid);
  const config=(label,mode)=>({model:"CANDIDATE_NOT_LOADED",runtime:"CANDIDATE_NOT_INSTALLED",mode,
    thinking_token_budget:mode==="low"?256:2048,max_tokens:8192,temperature:.6,top_p:.95});
  check("low configuration identical across all labels",eq(config("Low","low"),config("Fast","low")) && eq(config("Fast","low"),config("Eco","low")));
  check("two budgets differ",config("Eco","low").thinking_token_budget!==config("Eco","high").thinking_token_budget);
  return {validation_kind:"synthetic_engineering_only",checks:checks.length,passed:checks.filter(x=>x.pass).length,
    failed:checks.filter(x=>!x.pass),tasks:taskResults,
    retry_fixture_summary:retry,
    implementation_limits:[
      "No UI/browser, model inference, GPU sensor, wall meter, participant, or environmental reduction was tested.",
      "These four tasks are candidates. They are not empirically validated easy/hard strata.",
      "Production configuration hashing, clock alignment, final event state machine and user-code sandboxing are not implemented by this proof-of-concept."
    ]};
}

const report = runValidation();
console.log(JSON.stringify(report, null, 2));
if (report.failed.length) process.exitCode = 1;
