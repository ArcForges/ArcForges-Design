# Design Repair Verification

> **Historical evidence boundary.** Results and technology claims below belong to their recorded baseline. [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) amends current repository, protocol, Cloud and Mobile decisions; current implementation obligations are in the [gate register](open-gates-register.md). This amendment does not rewrite the earlier finding evidence or turn a design check into runtime proof.
> Scope: Stage 2 design evidence. These checks do not execute the product, database transactions, providers, native libraries or OS isolation profiles.

The [closure review](phase-2-design-closure-review.md) records the fourteen repaired groups and their future runtime evidence. This artifact makes the counterexamples and the complete document-integrity check reproducible with Python's standard library.

## Recorded execution

Both programs below were executed from a temporary directory outside the repositories. The counterexample suite passed all 20 cases, including 200 independently seeded read-partition schedules. The corpus check covers all Markdown files except immutable input contents as citation sources; input files remain valid link targets. It validates paths, section and rule anchors, unique document-scoped definitions, unqualified citations, the invariant mapping, all nine work-package fields, header/index dependency agreement, downstream symmetry and the complete serial dependency order.

Copy the two code blocks into a temporary directory as `design_counterexamples.py` and `check_design.py`, then run:

```text
python design_counterexamples.py
python check_design.py <absolute-path-to-phase-2-specifications-worktree>
```

The corpus checker writes `design_check.json` beside its temporary script and exits nonzero on a defect. No product, reference or input file is modified. Reserved identifier headroom and standard names are vocabulary/metadata, not waived normative citations. Retired work-package identifiers resolve to their explicit retirement records.

Passing arithmetic/state models establishes their bounded counterexample outcomes only; illustrative assertions have the narrower proof strength recorded below. Real concurrent SQL, provider reconciliation, packaged RID containment, physical restores and real OTIO/media processing remain the named implementation gates.

<a id="proof-strength"></a>
## Proof strength of the historical counterexamples

The recorded 20 passing tests are an execution fact, not 20 complete behavioral models. Classify the seven questioned tests by their actual bodies; an inline model needs no separate helper function, and a constant/assignment assertion proves less than a state transition.

| Test | What executes and what it establishes | Limit and required implementation evidence |
|---|---|---|
| `test_supplier_unknown_survives_customer_release` | Illustrative constants and arithmetic inequalities retain70 exposure while customer hold is set to0 | Does not execute reserve/release/period-rollover transitions; real supplier exposure/admission and reconciliation remain in commerce/provider packages |
| `test_storage_reservations_and_cleanup` | Bounded arithmetic model of committed/reserved conversion; cleanup branch is only an illustrative conditional | Does not execute database locking, object publication, crash cleanup or GC; real upload/promotion/concurrency evidence remains in API/sync packages |
| `test_conflict_lineage_does_not_ack_later_edits` | Inline receipt filtering/set subtraction models covered local sequences and preserves later edit7 | Assumes authenticated matching receipt/range and models no transaction race; real conflict lineage and delayed acknowledgements remain in sync |
| `test_stream_state_never_substitutes_task_state` | Enumerates the finite stream/task/final-reference product and checks the presentation action | Does not execute stream storage, transport or failover; real shared-stream recovery remains in Harness and client packages |
| `test_intent_nullable_and_invocation_not_turn` | Illustrates nullable dispatch intent and assigns settlement from a committed flag | No dispatch barrier, usage validation or settlement state machine is executed; provider/Harness transaction/crash evidence remains required |
| `test_audio_cut_mix_dissolve_gap` | Exact rational boundary rounding plus small mix/dissolve/silence arithmetic examples | Not an audio engine, buffer-coverage or multitrack interval enumerator; real timeline/audio/OTIO boundary fixtures remain required |
| `test_derived_publication_requires_matching_source` | Illustrates inequality of two source tokens | No publication function, CAS or concurrent writer is exercised; real stale-result refusal and rebuild evidence remain in product/index packages |

The other tests retain their stated arithmetic/state-model scope. No assertion here proves a product, provider, OS isolation profile, real SQL schedule or commercial deployment. Future completion gates require the actual producer named in the work packages; a green historical suite cannot replace that evidence.

## Executable counterexamples

```python
"""Executable design counterexamples; no product or provider code is exercised."""
from fractions import Fraction as Q
from dataclasses import dataclass
from itertools import product
import math, random, unittest

@dataclass
class Bucket:
    available: Q
    held: int = 0
    at: Q = Q(0)
    def advance(self, now, periods):
        end = max(self.at, Q(now))
        for lo, hi, burst, rate in periods:
            duration = max(Q(0), min(end, Q(hi)) - max(self.at, Q(lo)))
            ceiling = max(0, burst - self.held)
            self.available = min(self.available + duration * rate,
                                 max(self.available, Q(ceiling)))
        self.at = end
    def reserve(self, amount, now, periods):
        self.advance(now, periods)
        if self.available < amount: raise ValueError("insufficient")
        self.available -= amount
        self.held += amount
    def settle(self, amount, consumed, now, periods):
        self.advance(now, periods)  # OLD held applies to elapsed time.
        self.held -= amount
        self.available += amount - consumed

def publish(pending, committed, last_key=""):
    # Small model of workspace lock + one earliest revision per aggregate.
    keys = sorted(set(a for a, r, uid in pending))
    ordered = [a for a in keys if a > last_key] + [a for a in keys if a <= last_key]
    a = ordered[0]
    row = min((x for x in pending if x[0] == a), key=lambda x:x[1])
    pending.remove(row)
    committed.append((len(committed)+1, row))
    return a

def apply_revision(state, revision, body):
    return (revision, body) if revision > state[0] else state

def cas_capture(target, version, body):
    return (version, body) if version > target[0] else target

def service_runs(terms):
    # Effective service intervals, not provider webhook arrival order.
    intervals = sorted((max(start, authorised), end)
                       for start, end, authorised, priority in terms
                       if max(start, authorised) < end)
    result=[]
    for start,end in intervals:
        if result and start <= result[-1][1]:
            result[-1]=(result[-1][0],max(end,result[-1][1]))
        else: result.append((start,end))
    return result

def chosen_offer(terms, t):
    valid=[(priority,index) for index,(start,end,authorised,priority) in enumerate(terms)
           if max(start,authorised) <= t < end]
    return max(valid)[0] if valid else None

def project_source(value, rate, tick_rate=705600000):
    if not(math.isfinite(value) and math.isfinite(rate)) or rate <= 0:
        raise ValueError("invalid OTIO numeric boundary")
    exact_rate=Q.from_float(rate)
    for standard in (Q(24000,1001),Q(30000,1001),Q(60000,1001)):
        if abs(rate-float(standard)) <= math.ulp(float(standard)):
            exact_rate=standard
            break
    ticks=Q.from_float(value)/exact_rate*tick_rate
    result=round(ticks)  # Exact rational ties to even.
    if not -(2**63) <= result < 2**63:raise OverflowError
    return result,ticks-Q(result)

def otio_exact_export(ticks, tick_rate=705600000):
    seconds=Q(ticks,tick_rate)
    n,d=seconds.numerator,seconds.denominator
    if abs(n)>2**53 or d>2**53:raise ValueError("not exactly representable")
    return float(n),float(d)

class DesignCounterexamples(unittest.TestCase):
    def test_old_hold_time_is_not_retroactive(self):
        periods=[(0,100,10,1)]
        a=Bucket(Q(10));b=Bucket(Q(10))
        for x in (a,b):x.reserve(10,0,periods)
        a.advance(10,periods)
        for x in (a,b):
            x.settle(10,10,10,periods);x.advance(11,periods)
        self.assertEqual((a.available,b.available),(Q(1),Q(1)))
    def test_policy_history_not_last_policy(self):
        a=Bucket(Q(10));a.advance(11,[(0,10,10,1),(10,100,100,1)])
        self.assertEqual(a.available,11)
    def test_saturation_does_not_bank_fraction(self):
        p=[(0,100,10,1)];a=Bucket(Q(19,2));a.advance(1,p)
        self.assertEqual(a.available,10)
        a.reserve(1,1,p);a.settle(1,1,2,p);a.advance(Q(21,10),p)
        self.assertEqual(a.available,Q(91,10))
    def test_policy_reduction_preserves_balance(self):
        p=[(0,1,10,1),(1,100,3,1)];a=Bucket(Q(10));a.advance(10,p)
        self.assertEqual(a.available,10)
        a.reserve(8,10,p);a.settle(8,8,11,p);a.advance(12,p)
        self.assertEqual(a.available,3)
    def test_cancel_preserves_held_capacity_across_downgrade(self):
        p=[(0,1,10,1),(1,100,3,1)]
        a=Bucket(Q(10));a.reserve(10,0,p)
        a.settle(10,0,2,p);a.advance(10,p)
        self.assertEqual((a.available,a.held),(10,0))
    def test_read_partition_invariance_200_schedules(self):
        p=[(0,5,10,3),(5,8,6,1),(8,100,12,2)]
        events=[(Q(2),'r',2,0),(Q(6),'s',2,1),(Q(8),'r',2,0),(Q(9),'s',2,2)]
        def execute(reads):
            a=Bucket(Q(7))
            for t,kind,v,c in sorted(events+[(t,'q',0,0) for t in reads]):
                if kind=='r':a.reserve(v,t,p)
                elif kind=='s':a.settle(v,c,t,p)
                else:a.advance(t,p)
            a.advance(11,p);return a
        expected=execute([])
        for seed in range(200):
            randomizer=random.Random(seed)
            self.assertEqual(execute([Q(randomizer.randrange(0,11000),1000)
                                      for _ in range(30)]),expected)
    def test_contiguous_renewal_gap_and_offer_priority(self):
        a=[(0,10,0,1),(10,20,9,1)]
        self.assertEqual(service_runs(a),[(0,20)])
        self.assertEqual(service_runs([(0,10,0,1),(10,20,12,2)]),[(0,10),(12,20)])
        terms=a+[(5,15,5,3)]
        self.assertEqual(chosen_offer(terms,11),3)
        self.assertEqual(chosen_offer(list(reversed(terms)),11),3)
    def test_supplier_unknown_survives_customer_release(self):
        supplier_limit=100;unknown_supplier=70;customer_hold=20
        customer_hold=0
        self.assertEqual(customer_hold,0)
        self.assertGreater(unknown_supplier+40,supplier_limit)
        # New period/platform beneficiary do not erase outstanding exposure.
        new_period_spend=0
        self.assertGreater(new_period_spend+unknown_supplier+40,supplier_limit)
    def test_storage_reservations_and_cleanup(self):
        limit=100;committed=60;reserved=30
        self.assertGreater(committed+reserved+20,limit)
        verified_bytes=25
        committed+=verified_bytes;reserved-=30
        self.assertEqual((committed,reserved),(85,0))
        staged=10
        for deleted in (False,True):
            retained=0 if deleted else staged
            self.assertEqual(retained,0 if deleted else 10)
    def test_revision_order_not_uuid_order(self):
        pending=[('a',2,'0001'),('a',1,'ffff')];result=[];last=''
        self.assertEqual(sorted(pending,key=lambda r:r[2])[0][1],2)
        for _ in range(2):last=publish(pending,result,last)
        self.assertEqual([r[1][1] for r in result],[1,2])
        cursor=result[-1][0];pending.append(('a',3,'0000'));publish(pending,result,last)
        self.assertGreater(result[-1][0],cursor)
    def test_aggregate_fairness(self):
        pending=[('a',i,str(i)) for i in range(1,10)]+[('z',1,'0')]
        result=[];last=''
        for _ in range(3):last=publish(pending,result,last)
        self.assertEqual([r[1][0] for r in result],['a','z','a'])
    def test_bootstrap_echo_and_tombstone_never_regress(self):
        state=(2,'snapshot')
        self.assertEqual(apply_revision(state,1,'old'),state)
        state=apply_revision(state,3,None)
        self.assertEqual(apply_revision(state,2,'old'),(3,None))
        self.assertEqual(apply_revision((0,None),1,'own-device-body'),(1,'own-device-body'))
    def test_backfill_cas_and_cutover_fence(self):
        target=cas_capture((0,None),2,'v2')
        self.assertEqual(cas_capture(target,1,'stale'),(2,'v2'))
        target=cas_capture(target,3,None)
        self.assertEqual(cas_capture(target,2,'v2'),(3,None))
        def can_cutover(inflight,dirty,exclusive):return exclusive and not inflight and not dirty
        self.assertFalse(can_cutover(1,0,True))
        self.assertFalse(can_cutover(0,1,True))
        self.assertFalse(can_cutover(0,0,False))
        self.assertTrue(can_cutover(0,0,True))
    def test_conflict_lineage_does_not_ack_later_edits(self):
        rows={1,2,3,4,5,6,7};active='replacement';original='original'
        receipts=[(original,6),(active,6)]
        for batch,end in receipts:
            if batch==active:rows={n for n in rows if n>end}
            else:self.assertIn(1,rows)
        self.assertEqual(rows,{7})
        cloud_rev=8;keep_cloud_no_content_receipt_rev=8
        self.assertEqual(cloud_rev,keep_cloud_no_content_receipt_rev)
    def test_stream_state_never_substitutes_task_state(self):
        for stream,task,final in product(('open','completed','truncated','superseded','evicted'),
                                        ('running','waiting','completed','cancelled'),(None,'message')):
            action='fetch-reference' if final else 'poll' if task in ('running','waiting') else 'show-no-answer'
            if not final:self.assertNotEqual(action,'fetch-reference')
            if stream in ('completed','truncated','evicted') and task=='running' and not final:
                self.assertEqual(action,'poll')
    def test_intent_nullable_and_invocation_not_turn(self):
        attempt={'intent':True,'provider_ref':None,'outcome':None}
        self.assertTrue(attempt['intent'] and attempt['outcome'] is None)
        iteration={'committed':True,'tool_proposal':'bounded-tool','settled':False}
        iteration['settled']=iteration['committed']
        task_state='running';final_message=None
        self.assertTrue(iteration['settled'])
        self.assertEqual((task_state,final_message),('running',None))
    def test_audio_cut_mix_dissolve_gap(self):
        boundary=round(Q(1001,30000)*48000)
        self.assertEqual(boundary,1602)
        self.assertTrue(1601<boundary<=1602)
        output=[Q(1)+Q(2) for _ in range(4)] # Two tracks, one sample emitted each index.
        self.assertEqual(output,[Q(3)]*4)
        self.assertEqual(Q(1,4)*2+Q(3,4)*4,Q(7,2))
        self.assertEqual(sum([],Q(0)),0) # Gap is silence.
    def test_otio_standard_rate_and_plain_decimal_differ(self):
        nominal,_=project_source(1.0,float(Q(30000,1001)))
        decimal,_=project_source(1.0,29.97)
        self.assertEqual(nominal,23543520)
        self.assertNotEqual(decimal,nominal)
    def test_otio_exact_pair_and_invalid_boundary(self):
        for t in (0,1,23543520,705600000,-1,2**40):
            v,r=otio_exact_export(t)
            restored,_=project_source(v,r)
            self.assertEqual(restored,t)
        for v,r in ((float('nan'),1),(1,0),(1,-1),(float('inf'),1)):
            with self.assertRaises(ValueError):project_source(v,r)
        with self.assertRaises(ValueError):otio_exact_export(2**63-1)
    def test_derived_publication_requires_matching_source(self):
        analysed_token=(5,12);current_token=(5,13)
        self.assertFalse(analysed_token==current_token)
        current_token=(6,13)
        self.assertFalse(analysed_token==current_token)

if __name__=='__main__':
    unittest.main(verbosity=2)
```

## Complete corpus checker

The runnable checker follows the current repository layout: it checks formal-document structure and the archive README, excluding the four deprecated input bodies before reading files or building coverage counts. Earlier results in this record describe their recorded baseline; running this updated checker does not reopen input review.

```python
import sys,re,json,collections,posixpath
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(sys.argv[1]).resolve()
sys.stdout.reconfigure(encoding='utf-8')
T=Path(__file__).parent
LINK=re.compile(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)')
ID=re.compile(r'(?<![\w-])(?:WP-\d{2}(?:\.\d{2})?|P2-\d{3}|[A-Z][A-Z0-9]{0,5}-(?:[A-Z]\d{1,3}|\d{2,3}[a-z]?))(?![\w.-])')
ACTIVE_LAYERS=('docs/requirements/','docs/architecture/','docs/planning/')
HISTORICAL_ASSURANCE={
 'docs/assurance/phase-1-input-review-ledger.md',
 'docs/assurance/phase-1-official-verification.md',
 'docs/assurance/invariant-coverage.md',
 'docs/assurance/design-repair-verification.md',
 'docs/assurance/phase-2-design-closure-review.md',
 'docs/assurance/web-typescript-redesign-review.md',
}
LEGACY_INPUT=re.compile(r'\bI[1-4]\b|\bStage\s+\d+\s*(?:§|Invariant|\.\d)|\bdocs[/\\]inputs\b|FutureAllCSharp\.md|(?:platform-architecture-concept|product-discovery-record|product-discovery-overview|implementation-sequencing-notes)(?:-deprecated)?\.md',re.I)
def input_dependency_problem(path,line):
 current=path.startswith(ACTIVE_LAYERS) or (path.startswith('docs/assurance/') and path not in HISTORICAL_ASSURANCE)
 if current and LEGACY_INPUT.search(unquote(line)):
  return 'deprecated input reference in active specification'
 return None
def verify_input_dependency_guard():
 bad=(
  ('docs/requirements/test.md','> Governing authority: I1'),
  ('docs/planning/work-packages/test.md','| Required input | I2 section III |'),
  ('docs/architecture/test.md','Implement the I3 runtime rule.'),
  ('docs/architecture/contracts/test.md','Acceptance: Stage 13 §49'),
  ('docs/architecture/data-model/test.md','[source](../../deprecated-inputs/product-discovery-record-deprecated.md)'),
  ('docs/requirements/test.md','[source](../inputs/platform-architecture-concept.md)'),
  ('docs/planning/test.md','[source](../deprecated-inputs/%70roduct-discovery-overview-deprecated.md)'),
  ('docs/requirements/test.md','Read FutureAllCSharp.md for the required types.'),
  ('docs/assurance/open-gates-register.md','Required evidence: I4 section 19.'),
  ('docs/assurance/release-gates.md','[acceptance](../deprecated-inputs/implementation-sequencing-notes-deprecated.md)'),
 )
 good=(
  ('docs/requirements/test.md','[I-001](01-normative-glossary-and-invariants.md#rule-i-001)'),
  ('docs/planning/README.md','The [deprecated archive](../deprecated-inputs/README.md) is excluded.'),
  ('docs/planning/test.md','The Stage 2 repair produced this mapping.'),
  ('docs/architecture/test.md','Validate untrusted input before committing a resource.'),
  ('docs/planning/test.md','[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)'),
  ('docs/decisions/history.md','Historical quotation: I2 §III; not a current input.'),
 )
 for p,l in bad:
  if not input_dependency_problem(p,l):raise RuntimeError(('missed deprecated input',p,l))
 for p,l in good:
  if input_dependency_problem(p,l):raise RuntimeError(('rejected valid formal reference',p,l))
 return len(bad)+len(good)
input_guard_fixtures=verify_input_dependency_guard()
def visible(s):
 s=re.sub(r'<[^>]+>','',s)
 s=LINK.sub(lambda m:m[1],s)
 return re.sub(r'[\x60*~]','',s)
def slug(s):
 s=visible(s).lower()
 return re.sub(r'[^\w\- ]','',s,flags=re.UNICODE).replace(' ','-')
files={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig').splitlines() for p in ROOT.rglob('*.md') if '.git' not in p.relative_to(ROOT).parts and '.worktree' not in p.relative_to(ROOT).parts and (not p.relative_to(ROOT).as_posix().startswith('docs/deprecated-inputs/') or p.relative_to(ROOT).as_posix()=='docs/deprecated-inputs/README.md')}
anchors={};definitions={};errors=[];ruledefs=0
for p,ls in files.items():
 an=set();counter=collections.Counter();dd={}
 code=False
 for i,l in enumerate(ls,1):
  if l.lstrip().startswith(chr(96)*3):code=not code;continue
  if code:continue
  for k in re.findall(r'<a id="([^"]+)"></a>',l):
   if k in an:errors.append((p,i,'duplicate anchor',k))
   an.add(k)
  m=re.match(r'^#{1,6} (.*)$',l)
  if m:
   ss=slug(m[1]);n=counter[ss];counter[ss]+=1
   an.add(ss+('-'+str(n) if n else ''))
   for k in ID.findall(visible(m[1])):
    if k.startswith(('WP-','D-','P2-','V-','F-','R-')):dd.setdefault(k,i)
  if l.startswith('|'):
   cell=visible(l.split('|')[1]).strip()
   if ID.fullmatch(cell):dd.setdefault(cell,i)
   elif p.endswith('01-normative-glossary-and-invariants.md'):
    for k in ID.findall(cell):dd.setdefault(k,i)
  bm=re.match(r'^- ([A-Z][A-Z0-9]{0,5}-[0-9]{2,3}):',visible(l))
  if bm:dd.setdefault(bm[1],i)
 anchors[p]=an;definitions[p]=dd;ruledefs+=len([k for k in an if k.startswith('rule-')])
links=0;rulelinks=0;rawrefs=[];literals=0
for p,ls in files.items():
 code=False
 for i,l in enumerate(ls,1):
  problem=input_dependency_problem(p,l)
  if problem:errors.append((p,i,problem,l))
  if l.lstrip().startswith(chr(96)*3):code=not code;continue
  if code:continue
  matches=list(LINK.finditer(l))
  for m in matches:
   uri=m[2].strip('<>')
   if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',uri):continue
   name,_,frag=uri.partition('#')
   q=posixpath.normpath(posixpath.join(posixpath.dirname(p),unquote(name))) if name else p
   links+=1
   if not(ROOT/q).exists():errors.append((p,i,'missing file',uri));continue
   if frag:
    if unquote(frag) not in anchors.get(q,set()):errors.append((p,i,'missing fragment',uri))
    if frag.startswith('rule-'):rulelinks+=1
  if not p.startswith('docs/'):continue
  for mm in ID.finditer(l):
   k=mm[0]
   if any(m.start()<=mm.start()<m.end() for m in matches):continue
   if k in ('SHA-256','UTF-16','IEEE-754'):literals+=1;continue
   if definitions[p].get(k)==i:continue
   if p.endswith('invariant-coverage.md') and re.match(r'^\| 7\.\d+ \|',l) and mm.start()>l.rfind('|',0,l.rfind('|')) and k.startswith('I-'):literals+=1;continue
   if '<a id="rule-'+k.lower()+'"' in l:continue
   if re.match(r'^#{1,6} ',l):continue
   rawrefs.append((p,i,k,l[:180]))
wp={int(Path(p).name[:2]):p for p in files if p.startswith('docs/planning/work-packages/') and re.match(r'\d{2}-',Path(p).name)}
active=set(wp)-{27,29};deps={};down={}
for n in active:
 p=wp[n];ls=files[p]
 sections=[int(m[1]) for l in ls if (m:=re.match(r'^## ([1-9])\.',l))]
 if sections!=list(range(1,10)):errors.append((p,0,'mandatory sections',sections))
 sec='\n'.join(ls).split('## 9. Dependencies',1)[1]
 us,ds=sec.split('**Downstream',1)
 deps[n]={int(z) for z in re.findall(r'^- \[(\d{2}) ',us,re.M)}
 down[n]={int(z) for z in re.findall(r'^- \[(\d{2}) ',ds,re.M)}
 header=next(l for l in ls if l.startswith('> Upstream:'))
 hu,hdn=header.split('Downstream:',1)
 hd={int(z) for z in re.findall(r'\b(\d{2})\b',visible(hu))}
 dh={int(z) for z in re.findall(r'\b(\d{2})\b',visible(hdn))}
 if hd!=deps[n] or dh!=down[n]:errors.append((p,0,'header/dependencies mismatch',[sorted(hd),sorted(deps[n]),sorted(dh),sorted(down[n])]))
for n in active:
 if not deps[n]<=active:errors.append((wp[n],0,'inactive dependency',sorted(deps[n]-active)))
 expected={m for m in active if n in deps[m]}
 if expected!=down[n]:errors.append((wp[n],0,'asymmetric downstream',[sorted(expected),sorted(down[n])]))
idx=files['docs/planning/work-packages/README.md'];order=[];indexdeps={}
for l in idx:
 m=re.match(r'^\| (\d{2}) \| \[',l)
 if m:
  n=int(m[1]);order.append(n);indexdeps[n]={int(z) for z in re.findall(r'\b\d{2}\b',l.split('|')[-2])}
if len(order)!=51 or set(order)!=active:errors.append(('work-package index',0,'active count/order',len(order)))
pos={n:i for i,n in enumerate(order)}
for n in active:
 if deps[n]!=indexdeps.get(n):errors.append((wp[n],0,'index dependency mismatch',sorted(deps[n])))
 for d in deps[n]:
  if pos.get(d,999)>=pos.get(n,-1):errors.append((wp[n],0,'forward dependency',d))
for p,ls in files.items():
 if not (p.startswith('docs/architecture/') or p.startswith('docs/requirements/')):continue
 seen={}
 for i,l in enumerate(ls,1):
  if l.startswith('|'):
   k=visible(l.split('|')[1]).strip()
   if ID.fullmatch(k):
    if k in seen:errors.append((p,i,'duplicate document-scoped rule',k))
    seen[k]=i
cat='docs/requirements/01-normative-glossary-and-invariants.md'
coverage='docs/assurance/invariant-coverage.md'
expected={k for k in definitions[cat] if k.startswith('I-')}
actual=set()
for l in files[coverage]:
 if l.startswith('|'):
  first=visible(l.split('|')[1]).strip()
  if re.fullmatch(r'I-\d{3}',first):actual.add(first)
if expected!=actual:errors.append((coverage,0,'invariant mapping mismatch',[sorted(expected-actual),sorted(actual-expected)]))
result=dict(markdown_files=len(files),local_links=links,rule_links=rulelinks,stable_rule_anchors=ruledefs,invariant_catalogue_entries=len(expected),active_work_packages=len(active),dependency_edges=sum(map(len,deps.values())),input_guard_fixtures=input_guard_fixtures,raw_citations=rawrefs,literal_allocations_and_standards=literals,errors=errors)
(T/'design_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('errors','raw_citations')},ensure_ascii=False))
print('ERRORS',len(errors),'RAW CITATIONS',len(rawrefs))
for v in errors[:65]:print(v)
for v in rawrefs[:35]:print('RAW',v)
sys.exit(1 if errors or rawrefs else 0)

```
