# Producer and Local gRPC Closure Review

Review date:2026-09-14. Baseline: merged Design f85c5b76313e3fb7c337d1e4a8792e083d093bd5. Scope: independently adopt/correct AF01–AF18 and close the specifically requested local RPC migration, under P2-011. Work was serial; no subagents. Formal edits were made only after the collection/adoption checkpoint in Plan. The reference/archive reading exclusions were retained.

## 1. Correct source interpretation

DesktopPlatform remote main467d910c2daa641c8aa85ba37ff61030bd15c8b8 contains the ten-package whitelist and is one commit ahead of05ff04f with zero behind according to the GitHub compare API. Local main7bdbf6c was stale. The five original shims expose probe ABI; the Metal header is APPLE-only and has three probe exports. Full functional native behavior is still implementation work; the existence of a package is not evidence of those functions.

Contracts remote main1fb1dfaaaaa7a9f2f4c64a6e1c6a2b7de47d67b0 contains Kotlin-lite/coroutine generation, Maven tooling and a Kotlin consumer, alongside C#/TS. Its authored business proto remains Hello-only. The initial production contract inventory remains WP03 work. No implementation/reference checkout, package or deployment was modified by this documentation repair. Earlier dated review source rows are historical snapshots, not current remote status.

## 2. Finding closure map

| Finding | Adopted authority and concrete closure |
|---|---|
| AF01 | WP13.05–13.16 implement the seven native families and full wrapper/runtime closure; .90 independently consumes completed artifacts. Probe and production scope are separate. |
| AF02 | WP53 and build14 §8.1 own the updater, signed feed, migration interlock and crash recovery; WP50 verifies the production release. |
| AF03 | Registry04 push.v1, Notification delivery persistence, WP45.09 and PG24 close server sending and later physical Android acceptance. Stale invalid-token responses cannot delete rotated registrations; unresolved intents migrate to the new revision within original TTL. WP45→31 explicitly gates the real Android consumer. |
| AF04 | WP11 owns helper mechanisms/test-parser containment; WP13 publishes the next immutable version of that same helper with actual parser composition/containment; WP18 owns viewer integration. No upstream dependency on a future parser. |
| AF05 | Native06/WP13.14 preserve ArcGraphicsMetalNative probes and independently implement ArcGraphicsNative CPU/private acceleration. No fake functional API claim. |
| AF06 | Platform21 adds missing image/OTIO/audio slots, repairs owner/degradation coverage and distinguishes required feature failure from allowed optional acceleration. |
| AF07 | Scope SD09, native instruments, WP13.12/16, WP33 and PG08 consistently include generic USB and explicit interface/endpoint/permission behavior. |
| AF08 | Catalogue00 AZ04 exports all seven effective fields through closed identity/actor/egress profiles; human-only operations excluded from tool bindings. |
| AF09 | Cloud requirements/architecture, release L04/L05 and WP46 describe actual PostgreSQL dispatch, bounded hints and CF recovery. No extra realtime/broker dependency. |
| AF10 | Native arc_* prefix preserved consistently. |
| AF11 | WP03 publishes Slate contracts; WP39 consumes and implements them. |
| AF12 | Idempotency examples resolve to real operations; no alternate Notes body-write surface. |
| AF13 | Forward tables, headers, section9 and reverse index represent the same graph. The seven erroneous reverse rows omitted eight edges. |
| AF14 | Unique phase membership and explicit valid serial schedule; phase grouping is not claimed to concatenate into that schedule. |
| AF15 | WP42 records technical/test-mode evidence; real checkout/payout belongs WP48/50. |
| AF16 | Every active WP §7 names its .90 artifact/integration receipt and evidence class. |
| AF17 | Platform21 and simulator23 numbered sections/anchors are unambiguous. |
| AF18 | Current traceability/counts reflect52 WPs/161 edges and Kotlin Android; historical review counts remain unchanged. |
| IPC01–06 | Local09 and numbered04 close proto ownership, port-free OS streams, bootstrap/lease, restricted launch, helper operations/bulk grants, reverse roles, hints, SSO/connectors and real stage-specific tests. Old private-XPC/code-first business definitions are replaced. |

## 3. Verification scope

Mechanical checks cover active document links/anchors, section-number uniqueness, graph equality/topology/phases, .90 receipts, numbered record/field/type/method uniqueness and all newly added local bindings, native export/layout preservation, dependency/slot ownership and bounded residual-protocol scans. Targeted rereading checks each finding against the corrected authority and its producer/consumer gate. Document checks cannot prove the implementation, AOT linker, native libraries, Kestrel sandbox, actual Firebase/CF/R2, physical hardware or paid operation.

### 3.1 Bounded final review and corrections

After the concentrated edit batches, structural checks and rereading of the affected producer/consumer paths identified specific closure defects. Repairs were restricted to those paths:

- The final dependency graph is **52 work packages and161 edges**. AF03's proposed160-edge target omitted the new actual push producer45→Android consumer31;32 inherits that prerequisite. Every graph representation and the serial order now includes it. Counts are measured, not acceptance quotas.
- WP13.05 proves common ABI/header/layout primitives; it cannot require the family implementations produced by13.06–13.14. WP11's real foundation helper and WP13's production parser composition are successive immutable versions of one owned runtime, not competing helpers or a future input to11.
- The former raw challenge-echo/x-af-peer paragraph was replaced by the exact SHA256/HMAC transcript and binary metadata profile. LocalCallContext closes actor/scope/evidence forwarding; it cannot turn actor claims or approval IDs into owner authority. Distinct compatible descriptor hashes are permitted through the compiled service compatibility manifest.
- Sandbox media IDs and buffer seals now agree; seek has explicit monotonic sequence/receipt semantics, and native scalar text positions map to bounded UTF16 wire pagination. Shared memory is copied privately and validated before use.
- Android token rotation recreates eligible delivery intents without extending TTL, deleting a replacement token or resolving durable attention. Remaining old realtime-backfill/broker-session wording was replaced.
- Mobile phase headers and added index rows were brought into the same graph. Numbered wire groups now render as tables. No historical dated review baseline/count was rewritten.

All AF01–AF18 and IPC01–06 closure conditions are addressed in the final authorities and work-package acceptance. No additional product-scope decision is pending. This states document/design closure for this bounded task, not absence of all future implementation defects.

### 3.2 Measured document checks

| Document check | Measured result |
|---|---|
| Effective Markdown documents (including this record, excluding archive) | 153 |
| Local links and fragments | 10,886 checked; no missing target/anchor or duplicate explicit anchor |
| Wire record declarations | 370; unique names and field numbers, defined referenced types |
| Operation/service bindings | 335; unique stable operation IDs and generated methods |
| Newly bound local methods | 34; complete bootstrap/hints/connector/helper set |
| Active work packages and graph | 52 nodes,161 directed edges; all projections agree, valid serial topology, unique phases |
| Artifact acceptance | All52 active section7 evidence lists reference the owned .90 step |
| Native ABI preserved | 58 export signatures and17 C record declarations unchanged from f85c5b7 |
| Gate register | 40 entries:5 design-closed,33 implementation-open/triggered,1 retired,1 merged |
| Final mechanical issues | 0; git diff --check also passes |

The33 open implementation obligations include30 plain OPEN rows, two conditional/recurring OPEN rows and one TRIGGERED row. None was closed by this review. Required external evidence includes AOT and packaged native behavior, restricted OS IPC/containment, actual CF/R2/FCM, physical devices, signing/accounts and real commercial operation. A proto inventory is not generated/compiled production proto; those released artifacts remain WP03 work.

### 3.3 Reproducible mechanical checker

Save the Python block to a temporary file outside the Design checkout and run it from the Design repository/worktree root with Python3. It uses only the standard library and read-only Git access to the pinned baseline. It excludes docs/deprecated-inputs and ignores code-fenced link fixtures. It checks document structure, declarations and graph projections; semantic review and runtime tests are separate evidence.

```python
"""Run from the Design worktree root. Standard library only; never reads archived inputs."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib, json, re, subprocess, sys
from urllib.parse import unquote, urlsplit

root=Path.cwd().resolve()
assert (root/'docs/architecture/contracts/04-protobuf-wire-registry.md').is_file()
files=[root/'README.md']+[p for p in (root/'docs').rglob('*.md') if 'deprecated-inputs' not in p.parts]
texts={p.resolve():p.read_text(encoding='utf-8-sig') for p in files}
issues=[]
def fail(kind,where,detail):issues.append([kind,str(where),detail])
def visible(s):return re.sub(r'(?ms)^```.*?^```[^\n]*','',s)
def anchors(s):
    s=visible(s);result=set(re.findall(r'<a\s+id="([^"]+)"',s));seen=Counter()
    for h in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',s,re.M):
        h=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',h)
        h=re.sub(r'<[^>]+>','',h);h=re.sub(r'[^\w\s-]','',h.lower()).replace(' ','-')
        n=seen[h];seen[h]+=1;result.add(h+('-'+str(n) if n else ''))
    return result
ac={p:anchors(s) for p,s in texts.items()}
links=0
for p,s in texts.items():
    ids=re.findall(r'<a\s+id="([^"]+)"',visible(s))
    for k,v in Counter(ids).items():
        if v>1:fail('duplicate-anchor',p.relative_to(root),k)
    for target in re.findall(r'\]\(([^\n]*?)\)',visible(s)):
        target=target.strip().strip('<>')
        if not target or urlsplit(target).scheme or target.startswith('//'):continue
        path,_,frag=unquote(target).partition('#')
        if 'deprecated-inputs' in Path(path).parts:continue
        dest=(p.parent/path).resolve() if path else p
        links+=1
        if not dest.exists():fail('missing-link',p.relative_to(root),target);continue
        if frag and dest.suffix=='.md' and frag not in ac.get(dest,set()):fail('missing-anchor',p.relative_to(root),target)

wire=texts[(root/'docs/architecture/contracts/04-protobuf-wire-registry.md').resolve()]
aliases=set('string bytes bool sint32 sint64 uint64 int64 uint32 int32 double float Name Text Email SecretText Key ModelId CountryCode Cursor ReasonCode Hash Bytes Int32 Int64 UInt64 Bool'.split())
aliases.update(re.findall(r'(?:^|[.;] )([A-Z]\w*) = ',wire,re.M))
records={};refs=set();ops={};methods=set()
for line in wire.splitlines():
    if not line.startswith('| `'):continue
    cols=line.split('|')
    m=re.fullmatch(r' `([A-Z]\w*)` ',cols[1])
    if m:
        name=m[1]
        if name in records:fail('duplicate-record','wire',name)
        records[name]=cols[2]
    op=re.fullmatch(r' `([A-Za-z]\w*\.\w+)` ',cols[1])
    if op and len(cols)>4 and re.fullmatch(r' `\w+Service\.\w+` ',cols[2]):
        name=op[1]
        if name in ops:fail('duplicate-operation','wire',name)
        ops[name]=cols[2].strip(' `')
        if ops[name] in methods:fail('duplicate-method','wire',ops[name])
        methods.add(ops[name])
    for col in (cols[2:3] if m else cols[3:5] if op else []):
        fields=re.findall(r'`(\d+) (\w+):([A-Za-z]\w*)',col)
        nums=[n for n,_,_ in fields];names=[n for _,n,_ in fields]
        if len(nums)!=len(set(nums)) or len(names)!=len(set(names)):fail('duplicate-field','wire',cols[1])
        refs.update(t for _,_,t in fields)
for t in sorted(refs-set(records)-aliases):fail('undefined-type','wire',t)
for f in ['01-public-api-operations.md','02-local-rpc-operations.md']:
    counts=Counter()
    for line in texts[(root/'docs/architecture/contracts'/f).resolve()].splitlines():
        if line.startswith('| `'):counts.update(re.findall(r'`([a-z]\w*\.\w+)`',line.split('|')[1]))
    for op,n in counts.items():
        if n>1:fail('duplicate-classification',f,op)

ups={};downs={}
for p,s in texts.items():
    if p.parent.name!='work-packages' or not p.name[:2].isdigit() or p.name[:2] in ('27','29'):continue
    wp=p.name[:2];m=re.search(r'^> Upstream: (.*?) · Downstream: (.*)$',s,re.M)
    if not m:fail('wp-header',p.name,'missing');continue
    ups[wp]=set(re.findall(r'`(\d{2})`',m[1]));downs[wp]=set(re.findall(r'`(\d{2})`',m[2]))
    for label,expected in [('Upstream',ups[wp]),('Downstream',downs[wp])]:
        d=re.search(r'\*\*'+label+r':\*\* ([^\n]+)',s)
        if not d or set(re.findall(r'`(\d{2})`',d[1]))!=expected:fail('wp-body',wp,label)
    if 'producer-artifacts-and-integration.md' not in s:fail('wp-artifact-input',wp,'missing')
if len(ups)!=52:fail('wp-count','planning',str(len(ups)))
for wp,deps in ups.items():
    for d in deps:
        if d not in ups or wp not in downs[d]:fail('dependency',wp,d)
for wp,ds in downs.items():
    for d in ds:
        if d not in ups or wp not in ups[d]:fail('downstream',wp,d)
order=[];todo=set(ups)
while todo:
    ready=sorted(w for w in todo if ups[w]<=set(order))
    if not ready:fail('cycle','planning',','.join(sorted(todo)));break
    order.append(ready[0]);todo.remove(ready[0])
seq=texts[(root/'docs/planning/implementation-sequence.md').resolve()]
for wp,ds in ups.items():
    m=re.search(r'^\| '+wp+r' \| ([^|]+) \|$',seq,re.M)
    if not m or set(re.findall(r'\d{2}',m[1]))!=ds:fail('sequence-table',wp,'upstream mismatch')
index=texts[(root/'docs/planning/work-packages/README.md').resolve()]
for wp,ds in ups.items():
    m=re.search(r'^\| '+wp+r' \| [^\n]+? \| ([^|]+) \|$',index,re.M)
    if not m or set(re.findall(r'`(\d{2})`',m[1]))!=ds:fail('wp-index-table',wp,'upstream mismatch')

serial=re.search(r'^Serial execution: ([\d, ]+)\.',seq,re.M)
serial_order=re.findall(r'\d{2}',serial[1]) if serial else []
if len(serial_order)!=len(ups) or set(serial_order)!=set(ups):fail('sequence','planning','membership mismatch')
else:
    positions={w:i for i,w in enumerate(serial_order)}
    for wp,ds in ups.items():
        if any(positions[d]>=positions[wp] for d in ds):fail('sequence','planning','dependency follows '+wp)
    if not positions['45']<positions['53']<positions['46']:fail('sequence','planning','updater position')

native=texts[(root/'docs/architecture/contracts/06-native-functional-abi.md').resolve()]
exports=re.findall(r'^\| `(arc_\w+)\(',native,re.M)
if len(exports)!=len(set(exports)):fail('native-exports','native','duplicate')
for family in ['media','color','image','otio','pdf','instruments','graphics']:
    if not any(x.startswith('arc_'+family+'_') for x in exports):fail('native-coverage','native',family)


# Equality of every graph projection, including the independent reverse index.
edge_count=sum(map(len,ups.values()))
if edge_count!=161:fail('edge-count','planning',edge_count)
if '45' not in ups['31']:fail('push-producer','31','missing45')
reverse=index.split('## Downstream dependency index',1)[1]
for wp,ds in downs.items():
    m=re.search(r'^\| '+wp+r' \| ([^|]+) \|$',reverse,re.M)
    if not m or set(re.findall(r'\d{2}',m[1]))!=ds:fail('reverse-index',wp,'mismatch')

def expand_ids(s):
    result=[]
    for a,b,one in re.findall(r'(\d{2})\s*[–-]\s*(\d{2})|(\d{2})',s):
        result.extend(f'{i:02}' for i in range(int(a),int(b)+1)) if a else result.append(one)
    return result

phases={};phase_ids=[]
for phase,items in re.findall(r'^\| \*\*([A-K]) — [^|]+\| ([^|]+) \|',seq,re.M):
    for wp in expand_ids(items):
        phase_ids.append(wp);phases[wp]=phase
if Counter(phase_ids)!=Counter(ups.keys()):fail('phase-membership','sequence',phase_ids)
index_phase={};phase_ids=[]
for phase,body in re.findall(r'(?ms)^### Phase ([A-K]) —[^\n]+\n(.*?)(?=^### Phase |^## Downstream|\Z)',index):
    for wp in re.findall(r'^\| (\d{2}) \| [^\n]+? \| [^|]+ \|$',body,re.M):
        phase_ids.append(wp);index_phase[wp]=phase
if Counter(phase_ids)!=Counter(ups.keys()) or index_phase!=phases:fail('phase-membership','index',phase_ids)

for p,s in texts.items():
    # Only numbered top-level sections, not n.m sub-sections or dated prose.
    ns=re.findall(r'^## (\d+)\. ',visible(s),re.M)
    for n,count in Counter(ns).items():
        if count>1:fail('duplicate-section',p.relative_to(root),n)
    if p.parent.name!='work-packages' or p.name[:2] not in ups:continue
    wp=p.name[:2]
    if sorted(map(int,ns))!=list(range(1,10)):fail('wp-sections',wp,ns)
    m=re.search(r'^> Phase: ([A-K])',s,re.M)
    if not m or m[1]!=phases.get(wp):fail('wp-phase',wp,'mismatch')
    evidence=re.search(r'(?ms)^## 7\. .*?(?=^## 8\.)',s)
    if not evidence or ('WP-'+wp+'.90') not in evidence[0]:fail('artifact-receipt',wp,'missing from section7')
    if f'rule-wp-{wp}.90' not in ac[p]:fail('artifact-step',wp,'missing')

# ABI declarations and export signatures must not drift in a scheduling/IPC repair.
BASE='f85c5b76313e3fb7c337d1e4a8792e083d093bd5'
def baseline(path):
    return subprocess.run(['git','show',BASE+':'+path],check=True,capture_output=True,encoding='utf-8').stdout
old_native=baseline('docs/architecture/contracts/06-native-functional-abi.md')
c_blocks=lambda s:re.findall(r'(?ms)^```c\n(.*?)^```',s)
if c_blocks(native)!=c_blocks(old_native):fail('native-layout','native','declaration changed')
signatures=lambda s:re.findall(r'^\| `(arc_\w+\([^`]+)`',s,re.M)
if signatures(native)!=signatures(old_native):fail('native-export','native','signature changed')
structs=len(re.findall(r'typedef struct arc_\w+', '\n'.join(c_blocks(native))))
if len(exports)!=58 or structs!=17:fail('native-count','native',[len(exports),structs])
gates=texts[(root/'docs/assurance/open-gates-register.md').resolve()]
open_gates=lambda s:re.findall(r'^\| <a id="rule-[^"]+".*\| `(?:OPEN|TRIGGERED)[^|]*\|$',s,re.M)
if len(open_gates(gates))!=33 or len(open_gates(gates))!=len(open_gates(baseline('docs/assurance/open-gates-register.md')))+1:
    fail('open-gates','register',len(open_gates(gates)))
gate_ids=re.findall(r'^\| <a id="rule-((?:f|vg|pg)-[^"]+)"',gates,re.M)
if len(gate_ids)!=40 or len(set(gate_ids))!=40:fail('gate-count','register',gate_ids)
if '| **Open implementation-stage gates** | **33** |' not in gates or '| Gates created by Phase 2 | 24 |' not in gates:fail('gate-summary','register','stale')
assurance_index=texts[(root/'docs/assurance/README.md').resolve()]
if '40 entries, five design closures, 33 open implementation obligations' not in assurance_index:fail('gate-summary','assurance-index','stale')

# Closed local additions: each operation has exactly one numbered service binding.
helper='OpenSession RenewSession GrantSlot AckBuffer ProbeMedia OpenMediaReader ReadMediaFrame SeekMedia CopyVideoFrame CopyAudioFrame CloseFrame CloseReader OpenImage GetImageInfo ReadImageTile CloseImage OpenPdf GetPdfPage ExtractPdfText RenderPdfTile ClosePdf ReadOtio WriteOtio OtioReadChunk CancelSession CloseSession'.split()
connector='ListDefinitions ListConnections BeginConnection CompleteConnection GetConnection RevokeConnection'.split()
local_ops=['ILocalBootstrap.Renew','ILocalEvents.Poll']+['IContentSandbox.'+x for x in helper]+['IConnectorBroker.'+x for x in connector]
for op in local_ops:
    if op not in ops:fail('local-binding','wire',op)
if len(records)!=370 or len(ops)!=335:fail('wire-count','wire',[len(records),len(ops)])

# Current link and table edits may not introduce a single unheaded Markdown row.
for p,s in texts.items():
    if p.name=='producer-and-local-grpc-closure-review.md':continue
    def orphans(t):
        return [b for b in re.findall(r'(?m)(?:^\|[^\n]*\n)+',visible(t)+'\n') if not re.search(r'^\|[- :|]+\|\s*$',b,re.M)]
    old=baseline(str(p.relative_to(root)).replace('\\','/')) if p.name!='53-desktop-distribution-and-update.md' and p.name!='09-local-grpc-and-sandbox.md' else ''
    if len(orphans(s))>len(orphans(old)):fail('new-unheaded-table',p.relative_to(root),orphans(s))

result={'markdownFiles':len(texts),'checkedLocalLinks':links,'wireRecords':len(records),'wireOperations':len(ops),'newLocalOperations':len(local_ops),'activeWorkPackages':len(ups),'dependencyEdges':edge_count,'openImplementationGates':len(open_gates(gates)),'nativeExports':len(exports),'unchangedNativeStructs':structs,'serialOrder':serial_order,'issues':issues}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(bool(issues))
```
