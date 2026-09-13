# Family Design Completion Review

> Review date: 2026-09-13. Scope: current accepted product family, Android-only amendment, producer completeness and implementation-plan closure. This is documentation evidence, not a product implementation or release approval.
> Governing amendment: [P2-010](../decisions/phase-2-specification-decisions.md#rule-p2-010). Current producer sequence: [artifact and integration matrix](../planning/producer-artifacts-and-integration.md). Actual implementation obligations remain in the [gate register](open-gates-register.md).

## 1. Baseline and method

The formal baseline was clean Design main **f6e0cd267615a3cd00d6a3f6e9bb251fb53fb9b3**. Changes were made only on `codex/family-design-completion` in `C:/MyFile/Projects/ArcForges-Design/.worktree/family-design-completion`; the primary checkout was not edited. Earlier architecture-change commits are historical context, not an alternative file source for this revision.

One context performed the review serially. The separate local Plan repository first committed the portfolio and source map (`3dbb0b8`), then its review (`e46b49c`). Complete collection of35 grouped findings and the coverage record was committed as `51d55f0`; the unified repair plan and consequential choices as `831757d`; its review/corrections as `6a33235`. Only then was this Design worktree created and the nine repair sets executed. The Plan repository is an audit trail, not a build or validation dependency of Design. All needed current decisions and the validation program are contained here.

Collection covered requirements00–13 and every product requirement; architecture00–25; the six existing contract documents and four data-model documents; all51 active work packages and their entry points; decisions, assurance, provenance and acceptance. Retired27/29 stayed retired. Deprecated inputs were excluded before reading, and reference reading exclusions were preserved. Later closure checks corrected concrete affected statements, field bindings, dependency rows and examples under the same35 findings; they did not start another open-ended collection.

The convergence boundary is externally observable behavior, data meaning, authority, contract/layout compatibility, recovery and independent acceptance. Equivalent internal classes, control composition, query optimization and algorithms that preserve the specified profiles remain coding choices. Completing the initial producer surface does not promise APIs can never evolve: exact consumer pins, supported-version windows and incompatible-change gates remain required.

## 2. Source evidence and its limits

| Read-only source | Observed revision / role | What this establishes |
|---|---|---|
| DesktopPlatform | Local main7bdbf6c4656721088081cdf85c9f1ec8d78bc848; reviewed native-fix worktree05ff04f4; remote snapshot467d910c2daa641c8aa85ba37ff61030bd15c8b8 | Existing shared C ABI POD/status/probe signatures, wrappers, ten-package publication and consumer mechanisms. Existing media/image/colour/OTIO exports provide version/build/error queries; they do not implement the newly specified functional surface. |
| Contracts | Local main37ac517017e0072ab0058b1bcddecaac2ec9e1f8; Apache amendment6992789; remote snapshot4f6564a0fa15a18e92668efb995c25a88a9edf19 | Hello World C#/TS generation/publication and the authorized all-Apache boundary. No complete family schema or Kotlin package proof is inferred. |
| Mobile bootstrap | Local mainabfe0fb49faff5158615b254b9b00cb498fc7649; retained Android publication worktree64446af | Historical RN bootstrap, application identity and signing/release continuity inputs. Remote lookup was unavailable during collection; no current remote implementation or Kotlin device result is claimed. |
| Previous implementation | C:/MyFile/ArcForges-Old atede43db5b2237104dd0008b99398090c54a2cf94 | Historical166-project scaffold only. WP00/01/02/05 must inspect actual independent repository inventories. |
| AionUi |29c9271a59484e4696778cb80164f705245a6186 | Permitted chat/task/approval interaction reference. An in-memory approval map is not durable persistence evidence. |
| AFFiNE / SiYuan |81df4751a367f2795bc0d165586650dbe8db73d6 / eef10568384e2e7cf547adb029ae46a72e43c287 | Permitted Notes frontend/editor/knowledge behavior; excluded enterprise/backend/common-native expression was not used. No Notes canvas, slides, formulas or E2EE parity was added. |
| Serial-Studio |639daafb2fe7d324c3b2d5583d2514c8c470676f | Permitted acquisition/framing/replay behavior, preserving Pro/MQTT/XY/3D/vendor exclusions. Initial accepted analysis profiles are first-party definitions. |
| ArcVideo / ArcVideoFoundation |caf56513278703adec0c2933ec235bb864d72e31 /139eecaaa79dbad743a146f174a9c89a66ed594b | Permitted media/time/editor reference with Olive-origin provenance retained. No shader/translated-resource copying or relicensing. |
| StartArcForges | Local packaged-output layout | Names, layout and notices only; no binary execution, unpacking or reverse engineering. |

The source and package versions above are bounded observations, not assertions that every source branch still has that HEAD. No implementation/reference repository was edited. No reference function automatically became a requirement, and translating or rewriting copied GPL expression is not a licensing workaround.

## 3. Frozen finding closure

All rows below close the **documentation defect** against the specified authority and consumer acceptance. They do not mark the listed implementation work packages complete.

| Finding | Implementer blocker removed | Repaired authority and independent closure obligation |
|---|---|---|
| G-01 | Conflicting current runtime/protocol/generator text | [P2-010](../decisions/phase-2-specification-decisions.md#rule-p2-010), architecture00/01/02 and [wire registry](../architecture/contracts/04-protobuf-wire-registry.md) agree on authored proto and selected transports. Third-party extension-only schema generation remains its explicit exception. WP00–06 enforce this boundary. |
| G-02 | RN and retained-iOS instructions for the wrong client | [Mobile architecture](../architecture/11-mobile-architecture.md) and WP30–32 implement Kotlin/Compose Android only; requirements, platform matrix and gate register agree. No dormant iOS deliverable. |
| G-03 | Incomplete companion navigation/actions/recovery | Mobile section15 maps Home, conversations, tasks/approval, projects/search, simple automation, artifacts, trust/grants, account/support and credit consent to exact ports. WP31/32/49 require full denied/offline/recovery cases. |
| G-04 | Missing functional native producer | [Native ABI](../architecture/contracts/06-native-functional-abi.md) fixes seven capability families,58 new functions, typed wrappers, profiles and package dependencies. WP13 delivers actual libraries and isolated C17/C# AOT consumers before product WPs. |
| G-05 | Existing ABI broken by blanket new headers | Native ABI preserves original common PODs/statuses/probe names and specifies additive minor1 records. Actual C17/C++20 declaration/layout check is recorded below; runtime compatibility remains WP13. |
| G-06 | Wrong Contracts licence and absent Kotlin artifact | All authored Contracts schemas/tools/SDK/fixtures are Apache-2.0. [Package registry](../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry) adds the public Java/Kotlin-lite Maven artifacts with clean-consumer tests in WP03/06. Internal visibility stays restricted. |
| G-07 | Incomplete capability/context wire projection | Wire04 completes binding/effect/retry/preview/cancel/checkpoint/limits and typed source selections, ephemeral instance/generation/expiry. First-party capability rows resolve to exact ports; WP03/09 validate without side schemas. |
| G-08 | Task state/control mismatch | Wire TaskState and TaskSnapshot match the glossary, including Interrupted/PartiallySucceeded and separate control progress/unknown effect. WP16 handles local ProductJobs; WP52 owns actual AgentTask transitions and mixed-version clients. |
| G-09 | Missing device readiness/capability evidence | Device views and paged capability snapshots distinguish installed/running/offline/readiness/current grants. WP22/26/31/49 reject stale or substituted targets. |
| G-10 | Ambiguous candidate versions/promotion/pins | [Producer integration](../planning/producer-artifacts-and-integration.md) and build14 define run+attempt identity, pack once, full registry availability, partial-publication resume, complete manifest/latest promotion and exact consumer locks. |
| G-11 | Duplicate operation risks and obsolete local provider | Public/local catalogues have one classification per operation; newly enumerated wire-only support operations carry their explicit classification. Resource access uses the current bounded owner port. WP03/08/23 test the generated bindings. |
| G-12 | Impossible module isolation/transaction write sets | [Data overview](../architecture/data-model/00-data-model-overview.md) enumerates complete participants/order, including ordinary ChatTurn, provider intent, purchase and realm transfer. Entitlement logical IDs are provider-independent, with no required Commerce FK; WP21/42 rollback tests cover all participants. |
| G-13 | Obsolete partial-payment states and premature hold release | Purchase recognition is one local order/grant/version transaction; provider uncertainty stays outside it. Lifecycles20 and commerce16 preserve unknown liabilities/deadlines and remove mobile purchasing reconciliation. WP42/43 inject loss/replay at each actual boundary. |
| G-14 | Unsync deleting authority and refusing legal Cloud writes | Notes/Chat pause/cache eviction preserves acknowledged Cloud authority and pending local work. Authorized Cloud Notes tools use owner validation/publication. WP19/25/28 distinguish pause, detach and explicit Cloud deletion. |
| G-15 | Conflicting backup objectives/universal rollback | Requirements03, sync07, build14 and deployment22 agree on PG5minute/blob15minute RPO,30day immutable retention and4hour RTO. ModeC closes rollback; WP46/50 require actual independent restore and forward rescue. |
| G-16 | Ordinary/temporary chat forced into Task/history | [Journeys](../architecture/contracts/07-client-journeys-and-ports.md), Harness17, CF05 and Chat tables distinguish ChatTurn/AgentTask with one execution owner, explicit write promotion and bounded temporary body cleanup. WP52 replaces early fixtures. |
| G-17 | Blanket unsynced-input prohibition | One-use selected transient input is separate from knowledge/sync. Bytes/version/purpose/egress/expiry/origin and current permission are pinned. WP17/25/40/52 reject unauthorized or implicitly enrolled content. |
| G-18 | Protected-context loss and unspecified payer | Harness packs protected spans first; overflow refuses with an explicit handoff, no silent truncation. Compaction is operator-funded and idempotently reconciled; temporary summary is volatile. WP52 tests overflow/failure/restart. |
| G-19 | Unbound accepted Web-search capability | Journeys and CF05 select BraveWebV1, typed bounded results, egress consent, supplier budget and no automatic page fetching. WP43/52 require actual provider response/evidence before activation. |
| G-20 | Ambiguous Notes positions/undo/IME | [Product profiles](../architecture/26-product-behavior-profiles.md) and editing18 fix stable block/run/atom/cell addresses with UTF16 offsets, typed edits, explicit conflict preservation and recovery of invalid undo/composition. WP18/19/28 use independent edit vectors. |
| G-21 | Unspecified Scope framing/trigger/analysis | Product profiles and wire04 close accepted source/checksum/gap/trigger, spectrum/correlation/event/threshold/digital-decoder rules without altering measurements.v1. WP33–35/51 verify independent data/time vectors. |
| G-22 | Ambiguous Slate edits/retime/keyframe/colour | Product profiles close TL-06 edits, linked/locked/ripple semantics, point-list rational retime, explicit tangent interpolation, CPU colour/audio/analysis and render publication. WP36–39 retain exact time/OTIO/subtitle fidelity. |
| G-23 | Universal updater/full-local-function claims | Distribution10 and Mobile11 separate desktop updater from Android signing/versionCode and forward rescue. Account restriction preserves local recovery/export while accurately restricting Cloud-dependent work. WP32/50 verify old-install upgrade. |
| G-24 | Impossible all-traces/all-audit/no-duplicate-email promises | Observability13/WP12 use bounded trace buffering with overflow evidence; audit is immutable under ordinary roles with authorized retention purge. One email challenge remains authoritative despite uncertain physical duplicate delivery; WP11/22/45 test this distinction. |
| G-25 | Contradictory WP04/19/22 bodies | Storage-free04 asserts primitives, real persistence belongs07/21; Notes export reports format fidelity; official and self-host identity paths are explicit. Old conflicting steps and completion text were replaced. |
| G-26 | Producers depending on later full consumers | [Stage matrix](../planning/producer-artifacts-and-integration.md) names every fixture and real replacement. WP03 freezes all initial contracts;06 minimal actual transport probe;13 full native packages;25 real R2;52 full AI before31/49. Graph matches every WP header/body/index. |
| G-27 | Historical166-project inventory presented as current | Current source observations above and WP00/01/02/05 replace old inventory assumptions. Historical reconciliation is labelled and cannot override independent repository source/producer ownership. |
| G-28 | Missing enrollment/recovery/SSO closure | Journeys and wire04 fix purpose-bound enrollment, email/passkey/self-host/OIDC/recovery, limited proofs, device SSO and cookie/native shaping. WP22/23/30 test lost proof, revoked source and non-email realm recovery. |
| G-29 | Unspecified package/workflow/panel/update/connector rules | [Extension profiles](../architecture/contracts/08-extension-and-policy-profiles.md) close all six families, bounded manifest/DAG/panels, connection secrets and drain/migration/rollback. WP03/09/11/41 preserve typed boundaries and current grants. |
| G-30 | Unspecified policy/configuration/experiments | Extension/policy profiles define closed keys/private sections, deterministic targeting/priority/buckets/expiry and presentation-only experiments. WP03/44 reject invalid or incomplete activation; no guessed commercial fallback. |
| G-31 | Undefined Pass/subscription/proration behavior | Commerce16 fixes mutual exclusion, next-period plan change, renewal/refund and no capacity/credit reset. Existing three-ledger accounting and customer/supplier deadlines remain; WP42/48 test boundary races. |
| G-32 | Incomplete realm migration/irrecoverable outcome | Journeys and wire04 define realm-transfer.v1 inclusion/exclusion, preview/fidelity, new IDs, root receipts, bounded resume/cancel and source preservation. WP46/48 distinguish missing unrecoverable bytes from repaired data. |
| G-33 | Missing hostile-helper bulk transport | Native ABI and isolation24 fix three64MiB OS-owned slots, typed descriptor, lease/generation/hash/coverage/ack/cancel and separately admitted8K memory. WP13 tests actual containment and stale slot denial. |
| G-34 | Incorrect evidence/invariant/reference scheduling | [Implementation sequence](../planning/implementation-sequence.md), all51WPs, reference matrices and invariant map are aligned. WP42 test-mode is distinct from48/50 activation;45 follows47 tooling; this validator has no deleted-Plan dependency. |
| G-35 | Missing one-time policy-override receipt | Wire04 and Resource/Policy records bind explicit consent to actor/operation/source/version/policy/generation/expiry. Persistent policy is separate; WP17/25/40/52 recheck current authorization and preserve receipt idempotency. |

## 4. Final bounded rehearsal

| Rehearsed path | Documentary result and required runtime replacement |
|---|---|
| Login/enrollment/recovery → ordinary/temporary/agent turn → tool → approval → artifact | All steps resolve to a numbered operation or declared standard exception and one owner. Ordinary reads create no phantom Task; write promotion is explicit. Temporary text cannot enter PG/WAL/Workflow history/backup; metadata-only settlement survives. Invalid/lost proof, pending control, source revoke and unknown provider effects have explicit outcomes. Actual execution remains WP22/25/26/43/52/31/49. |
| Offline Notes edit → remote edit → conflict/undo/IME → export | Stable run/cell offsets prevent retargeting; pending journal acknowledgement uses the covered local watermark. Divergent whole-document branches and invalid inverse edits are retained for explicit resolution. Transfer is separate from lossy user formats; no cache operation deletes the Cloud authority. Actual owner-store proof remains WP18/19/25/28/46. |
| Scope source → framing/trigger → capture → analysis/report | Source identity/time, checksum/gap/overflow, trigger intervals, decoder assumptions and unavailable numeric outcomes are fixed. Simulator/replay is labelled, never hardware evidence. Actual native acquisition and finite-number vectors remain WP13/33–35/51. |
| Slate import → edit/retime → playback/render → transcription/OTIO | Typed edits freeze affected locked/linked roots;705600000Hz identity, sourcePTS and rational mapping remain distinct. Colour/audio rules, render output commit and OTIO fidelity are explicit. ProductJob owns rendering; only transcription/agent work uses Cloud AI. Actual packages/media/OS tests remain WP13/36–39/52. |
| Android/Web interrupted connection → revoke → reauthenticate | Pending work is partitioned by realm/user/generation; hints/push/live text are not authority. Unknown command acknowledgement is reconciled before replay, high-risk work needs foreground confirmation, and revoked data does not leak through cached projections. Android physical release evidence remains WP32; browser evidence WP49. |
| Purchase/renew/refund → quota and AI unknown usage | External payment success can precede local recognition; within ArcForges order/grant/version are atomic. No asynchronous half-grant state remains. Paid period, purchased credit stock, capacity refill and unresolved supplier liability have distinct identities and reset rules. Live provider/payout evidence remains48/50. |
| Publish one registry → another fails → consumer upgrade | Candidate bytes/version stay immutable, partial publication is recorded, latest/complete manifest waits for the full required set, and retry verifies already-published identities. Consumers pin a complete release and run without producer source. Actual NuGet/npm/Maven/OS execution remains producer WPs. |
| Migration/rollback → independent restore → recovered generation | ModeA/B compatible rollback and modeC forward rescue differ. Restore uses independent immutable objects/journal and rejects obsolete credentials/effect replays. Lost mandatory bytes are irrecoverable, not fabricated. Real4hour recovery, RPO and generation-fence proof remains WP46/50. |

Closure corrections stayed inside the frozen findings: stable AGP9.3.2 replaced a9.4 preview candidate; three obsolete RN/iOS bodies were removed; old purchase/Notes/Task worked examples were aligned with the selected transactions; realm transfer explicitly enlists Workspace receipts; stale gate totals and a native section number were corrected. None introduces a new product family or a new round of requirements.

## 5. Verification performed and open evidence

The documented command was executed from this Design worktree with exit code0 and no reported issues:

| Check | Observed result |
|---|---|
| Current Markdown corpus |150 files; archived inputs excluded |
| Local links and anchors |10,837 checked; no missing target/anchor or duplicate explicit anchor |
| Numbered wire registry |351 named records and301 stable operations; checked field numbers/names and referenced types resolve uniquely |
| Active implementation graph |51 work packages; headers, body dependencies, index, graph table and serial execution agree; acyclic; no retired package dependency |
| Functional native catalogue |58 unique new export declarations across all seven required families |
| Mathematical checks |Unsigned64/UTF8/UTF16/exact-time examples and periodic-Hann sine amplitude assertions passed |
| Whitespace |git diff --check passed |

The same validator is embedded below, rather than referring to local Plan scratch scripts. Link counts describe this snapshot and are not a permanent acceptance threshold.

The native declaration check extracted the17 C records and58 function signatures from the native annex, included the existing read-only `DesktopPlatform/native/shared/include/arc/arc_native_abi.h`, and compiled them with local MSVC in C17 and C++20 modes with warnings as errors. The Windows x64 size probe matched every frozen/common and new record size in the annex. This checks declaration compatibility and one ABI layout only: no new functional DLL was built or called, no C# AOT wrapper was executed, and no other RID layout was proven.

Manual closure additionally checked the table above, active runtime/licence/protocol residues, public/local bindings and producer-to-consumer replacement. Historical decisions and explicit negative exclusions retain their original names; rule IDs such as RN-01 in rendering are not React Native dependencies. The closed third-party extension schema generator is not first-party RPC code-first authority.

The32 current implementation-stage gates remain open/triggered or conditional under their existing rules. This task did not implement Mobile, Contracts or DesktopPlatform; publish packages; configure provider accounts; execute full native functionality; validate actual C# AOT/CF Workflow/R2/physical Android/Play; or process commercial payments/payouts/restore production data. Stable SDK patch compatibility, provider accounts/terms/prices, signing credentials, store approval and those actual execution receipts must be supplied at their named implementation gates. No unresolved consequential design choice remains among G-01–35; unknown runtime compatibility is an explicit gate, not invented evidence.

Primary-source checks informed mechanisms, not runtime conclusions: [stable AGP compatibility](https://developer.android.com/build/releases/agp-9-3-0-release-notes), [built-in Kotlin](https://developer.android.com/build/migrate-to-built-in-kotlin), [Compose compiler](https://developer.android.com/develop/ui/compose/setup-compose-dependencies-and-compiler), [gRPC Android Kotlin](https://grpc.io/docs/platforms/android/kotlin/) and [lite generator example](https://github.com/grpc/grpc-kotlin/blob/master/examples/stub-lite/build.gradle.kts), [Maven namespace verification](https://central.sonatype.org/register/namespace/) and [publication requirements](https://central.sonatype.org/publish/requirements/), [Brave search protocol](https://api-dashboard.search.brave.com/app/documentation/web-search), [Workers AI catalogue](https://developers.cloudflare.com/workers-ai/models/) and [FFmpeg send/receive state machine](https://ffmpeg.org/doxygen/trunk/group__lavc__encdec.html). Package pins are not claimed tested merely because an official page describes them.

## 6. Self-contained document validation

Requires Python3 standard library and the current Design checkout only. From the repository root run this PowerShell-compatible command, which extracts the single Python block below. It reads current Markdown, excludes archived inputs before reading, checks links/anchors, numbered wire fields/types/operations, duplicate catalogue classifications, every active WP dependency view and topological order, and declared native-family coverage. Independent exact-value/time/Hann arithmetic assertions are illustrative mathematical checks, not a substitute for producer/owner test vectors. The validator does not parse or compile generated proto, prove contract behavior or check external URLs/accounts.

```powershell
python -X utf8 -c 'from pathlib import Path; import re; s=Path("docs/assurance/family-design-completion-review.md").read_text(encoding="utf-8"); code=re.search(r"(?ms)^```python\n(.*?)^```\s*$",s).group(1); exec(compile(code,"<design-document-validator>","exec"))'
```

```python
"""Run from the Design worktree root. Standard library only; never reads archived inputs."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib, json, math, re, sys
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
if len(ups)!=51:fail('wp-count','planning',str(len(ups)))
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
if not serial or re.findall(r'\d{2}',serial[1])!=order:fail('sequence','planning','order differs from graph')

native=texts[(root/'docs/architecture/contracts/06-native-functional-abi.md').resolve()]
exports=re.findall(r'^\| `(arc_\w+)\(',native,re.M)
if len(exports)!=len(set(exports)):fail('native-exports','native','duplicate')
for family in ['media','color','image','otio','pdf','instruments','graphics']:
    if not any(x.startswith('arc_'+family+'_') for x in exports):fail('native-coverage','native',family)

# Independent mathematics/encoding counterexamples, not runtime implementations.
assert str(2**64-1)=='18446744073709551615'
assert bytes.fromhex('00112233445566778899aabbccddeeff').hex()=='00112233445566778899aabbccddeeff'
assert len('A中😀'.encode('utf-8'))==8 and len('😀'.encode('utf-16-le'))//2==2
assert Fraction(705600000*1001,30000)==23543520
assert Fraction(705600000,48000)==14700
assert Fraction(48000*1001,30000)==Fraction(8008,5)
assert Fraction(1,2)*(0+1)==Fraction(1,2)  # linear keyframe midpoint
n=64;k=7;w=[0.5-0.5*math.cos(2*math.pi*j/n) for j in range(n)]
x=[math.sin(2*math.pi*k*j/n) for j in range(n)]
real=sum(x[j]*w[j]*math.cos(2*math.pi*k*j/n) for j in range(n))
imag=-sum(x[j]*w[j]*math.sin(2*math.pi*k*j/n) for j in range(n))
assert abs(2*math.hypot(real,imag)/sum(w)-1)<1e-12
result={'markdownFiles':len(texts),'checkedLocalLinks':links,'wireRecords':len(records),'wireOperations':len(ops),'activeWorkPackages':len(ups),'nativeExports':len(exports),'topologicalOrder':order,'issues':issues}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(bool(issues))
```
