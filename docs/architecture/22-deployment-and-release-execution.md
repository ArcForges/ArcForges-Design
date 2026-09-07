# Deployment and Release Execution

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: `§6` and `§6.1` of the cloud requirements, `§15` of the quality contract, `§11` of the build architecture
> Companions: [`14-build-packaging-and-release.md`](14-build-packaging-and-release.md), [`05-cloud-architecture.md`](05-cloud-architecture.md), [`20-cross-system-lifecycles.md`](20-cross-system-lifecycles.md)

The requirements say migration is a gated step, that schema change uses expand/contract, and that a production deployment is reversible. **What none of them gives is the sequence** — the order of the phases, the check that must pass between each, and what happens when one fails with a half-deployed fleet. A deployment procedure that exists only as a set of rules is a procedure that gets improvised at 2 a.m.

---

### Web deployment boundary

[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) uses Node-built Site/Account/Chat assets and the existing C# Cloud host. For each browser origin route /api, /session and /realtime only to the allowlisted Cloud service, preserving the validated external origin and permitting WebSocket upgrade. API/auth failures must never enter SPA fallback. Session/CSRF/config/API responses use no-store; hashed assets use immutable caching; old chunks survive the compatibility window. Each release manifest binds asset and generated-schema fingerprints, public runtime-config schema and compatible security headers. Promotion/rollback reuses those bytes and honors the current/previous API window. All replicas share the Identity session store and protected Data Protection key ring; restored data invalidates browser sessions. No Node production process, esproj evaluation or npm install occurs in the running Cloud image.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| DX-01 | **A deployment is a sequence of phases, each with an entry check, an exit check and a defined failure action.** A phase without all three is not deployable. |
| DX-02 | **Every phase is independently reversible, or it is not entered.** Where reversal is impossible — a contract phase that drops a column — the phase is deferred until the version that needs it is irreversibly established (`§2.4`). |
| DX-03 | **No phase depends on every replica being at the same version at the same instant.** Rolling deployment means mixed versions are the normal state, not an exception ([PS-10](05-cloud-architecture.md#rule-ps-10) of the cloud architecture). |
| DX-04 | **Production never rebuilds** ([EN-10](../requirements/products/arcforges-cloud.md#rule-en-10)). The digest built once in CI is what runs, and deployment references the digest, never a tag ([EN-11](../requirements/products/arcforges-cloud.md#rule-en-11)). |
| DX-05 | **A failed phase stops the sequence.** It never proceeds "to get to a consistent state", because the consistent state is the one before the failure. |
| DX-06 | **Every phase's outcome is recorded** with its checks, its operator and its time, so a later incident can reconstruct what ran. |

---

## 2. The cloud deployment sequence

### 2.1 Phases

```
 0  PRE-FLIGHT      artifact identity · gate evidence · approval
 1  EXPAND          additive schema only — new columns, new tables, new indexes
 2  BACKFILL        populate new structures; old code still reads old structures
 3  DEPLOY          roll the new application version across replicas
 4  SOAK            observe at the new version under real traffic
 5  SWITCH          enable behaviour that depends on the new structures (policy flag)
 6  CONTRACT        remove what nothing reads any more — a SEPARATE, LATER deployment
```

| Phase | Entry check | Exit check | On failure |
|---|---|---|---|
| **0 Pre-flight** | Digest matches the CI-produced artifact; every release gate has resolvable evidence ([WP-50.00](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.00)); environment approval granted ([EN-13](../requirements/products/arcforges-cloud.md#rule-en-13)) | All three pass | Stop. Nothing has changed |
| **1 Expand** | Migration is **additive only** — a machine check, not a reviewer's judgement; forward and backward rehearsal passed against a production-shaped copy ([RG-15](14-build-packaging-and-release.md#rule-rg-15)) | Schema applied; **the currently deployed version still passes its health checks** | Stop and retain the expanded schema while diagnosing; remove only proven-unused additions through a separate reviewed repair. Additive does not make arbitrary DDL reversal data-safe |
| **2 Backfill** | New structures exist; the backfill is resumable and idempotent | Backfill range coverage complete; **no read path depends on it yet** | Stop and resume later. Old code is unaffected because it does not read the new structures |
| **3 Deploy** | Expand applied; the new version is **proven to run against the expanded schema** — this is the compatibility that makes rolling safe | Every replica healthy at the new version; error rate and latency within the release envelope | **Roll back the application** ([EN-14](../requirements/products/arcforges-cloud.md#rule-en-14), one action). The schema stays expanded. Application rollback is allowed only while the declared data/reader compatibility horizon in §2.7 remains open; after closure, use the rehearsed forward-repair or full recovery procedure |
| **4 Soak** | Fleet at the new version | The soak window elapses with no new page-worthy condition and no error-budget burn | Roll back the application. The schema stays expanded |
| **5 Switch** | Soak clean; the new behaviour is behind a policy flag (`§4` of the policy architecture) | The behaviour is on and healthy | A/B: turn the reader flag off while old authority remains current. C: use forward fix or the rehearsed restore; flag-off cannot recover incompatible new facts |
| **6 Contract** | The new version is **irreversibly established**: rollback to the pre-expand version is no longer a permitted action, and no read path touches the removed structure | Removal applied | Stop. A contract failure is the only phase whose reversal needs a restore, which is why `§2.4` gates entry so hard |

### 2.2 Why the phases are separate

| Separation | What it buys |
|---|---|
| Expand before deploy | The old version keeps working, so deploy is reversible |
| Backfill before switch | The new behaviour never reads a half-populated structure |
| Deploy before switch | A bad *deployment* and a bad *behaviour* fail independently and are diagnosed separately |
| Reader switch separate from deploy | A/B can reverse readers within the valid data horizon; C requires an explicit authority cutover |
| Contract as a **separate, later deployment** | The window in which rollback is possible is not shortened by tidying up |

| # | Rule |
|---|---|
| PH-01 | **Expand and contract are never in the same deployment.** Combining them removes the rollback path the expand phase exists to preserve. |
| PH-02 | **Contract runs only after the intervening version is established beyond the rollback horizon**, which is a stated duration, not a feeling. |
| PH-03 | **A migration that cannot be expressed as expand-then-contract is a design problem**, escalated rather than executed as a single destructive step ([MG-04](../requirements/products/arcforges-cloud.md#rule-mg-04)). |
| PH-04 | **"Migration down" is not the rollback strategy** ([MG-04](../requirements/products/arcforges-cloud.md#rule-mg-04)). Rollback is an application rollback or a forward fix. |
| PH-05 | **Migration never runs on application start-up, on any replica** ([MG-01](../requirements/products/arcforges-cloud.md#rule-mg-01)). It is a separate gated step with a single executor. |

### 2.3 Mixed-version behaviour during phases 3 and 4

| Situation | Required behaviour |
|---|---|
| Old replica reads a row written by a new replica | Unknown fields preserved on round trip; no loss ([SY-09](20-cross-system-lifecycles.md#rule-sy-09) of the lifecycle document) |
| New replica reads a row written by an old replica | New columns absent or default; the new code must tolerate this, and a test asserts it |
| An outbox message enqueued by one version, consumed by the other | Message contracts are additive-only within a major; a consumer ignores unknown fields |
| A background lease taken by an old replica, expiring during deploy | Lease expiry is version-independent; another replica takes it ([BG-02](05-cloud-architecture.md#rule-bg-02), [BG-03](05-cloud-architecture.md#rule-bg-03)) |
| A long-running task started before the deploy | **Task authority is in the database, not the worker** ([BG-03](05-cloud-architecture.md#rule-bg-03)). It continues on any replica |
| A realtime connection to a replica being drained | The client reconnects and **reconciles unconditionally** ([GP-03](contracts/03-realtime-and-bridge.md#rule-gp-03)) |

| # | Rule |
|---|---|
| MX-01 | **Both orderings are tested**, not just old-then-new ([CM-07](../requirements/12-quality-and-compatibility-contract.md#rule-cm-07) of the quality contract) — a client or replica newer than its peer is as normal as the reverse. |
| MX-02 | **A message or row written by either version is readable by the other**, for the whole rolling window. |
| MX-03 | **Draining a replica completes or releases its in-flight work**; it never abandons a lease silently. |

### 2.4 The rollback horizon

| # | Rule |
|---|---|
| RH-01 | The rollback horizon permits application-only reversal while old data remains authoritative/representable. A/B normally retain it to contract; C closes its data horizon at cutover. The durable migration epoch is the authority. |
| RH-02 | Contract closes any remaining horizon. A mode-C cutover may already have closed the data horizon; the two are recorded independently. |
| <a id="rule-rh-03"></a>RH-03 | **Beyond the horizon, recovery is a restore**, with its own drill evidence ([WP-46.03](../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.03)) — a materially more expensive operation, and the reason the horizon is generous by default. |
| RH-04 | **A security fix may close the horizon early**, and that is a decision with its own record, not an exception taken quietly. |

---

### 2.5 Versioned capture, backfill and cutover

Starting capture before backfill is necessary but insufficient. **Counterexample:** backfill reads row v1; capture applies v2; delayed backfill overwrites the target with v1. Both timestamps satisfy the previous check, yet the target is stale. The mechanism must prevent regression and close the writer/cutover race.

| Mode | Authority until contract | Required conversion and rollback |
|---|---|---|
| A — derived (default) | Old representation | Every new reader's value is a deterministic derivation of old data. New-version writes still write the old authority; a synchronous database capture applies the derivation. Application rollback remains safe through the horizon. |
| B — lossless conversion | Old representation during the mixed-version horizon | New-version writers convert their inputs losslessly to the old authority; capture derives the new structure. The converter must round-trip every permitted write. New-only facts remain disabled until contract; if they cannot be represented, choose C. No bidirectional trigger loop or last-writer-wins pair of authorities. |
| C — incompatible new facts | Old until the recorded cutover; new afterwards | A bounded, announced write pause fences all old writers, validates conversion and changes authority. Old-version traffic remains blocked after switching. Data rollback closes at that point; a flag-off alone is not recovery. |

```
EXPAND: install database-enforced capture and migration epoch fence
        under a brief writer gate; wait for prior writers before enabling it
BACKFILL: bounded key ranges; read (key, source_revision, payload/deleted) atomically
          apply only if source_revision > target.source_revision
CAPTURE: same version predicate, same converter, durable delete tombstones
DEPLOY/SOAK: capture continues for writers from every deployed version
CUTOVER: hold exclusive writer fence, drain pre-fence writers/capture,
         verify range coverage and target equivalence at the barrier,
         change reader epoch (and authority only in C), then release fence
CONTRACT: after recorded rollback horizon, fence, disable old writers,
          verify converter/capture no longer needed, remove old structure separately
```

| # | Rule |
|---|---|
| BF-01 | Migration declares mode, converters, supported old/new versions, row version/tombstone scheme, range manifest, capture mode and maximum fence duration before execution. |
| BF-02 | A database trigger on every affected source write takes the migration epoch's shared transaction lock and assigns/increments the key's source revision in the same transaction. Expand installs it under the exclusive gate after pre-existing writers drain. New code alone cannot cover old replicas. |
| <a id="rule-bf-03"></a>BF-03 | Backfill reads payload and source revision in one snapshot. Both capture and backfill use `INSERT ... ON CONFLICT ... DO UPDATE ... WHERE incoming.source_revision > target.source_revision`. Equal revision requires equal canonical hash; disagreement fails migration. The per-key version and delete tombstone survive physical source deletion until the migration horizon. |
| BF-04 | Convergence requires **all** range-manifest entries complete with resumable receipts; version-preserving capture from before the snapshot; no conversion error/dead letter; and a fenced cutover comparison of keys, source revisions, tombstones and canonical hashes. A pair of timestamps or an empty queue read without the writer fence proves none of these. |
| <a id="rule-bf-05"></a>BF-05 | Capture and the epoch fence cover every old/new write throughout deploy, soak and switch. Mode A/B retains old authority and conversion until contract. |
| BF-06 | Synchronous capture is the default. An optional asynchronous variant uses a transactional capture outbox for **every** source write, keyed by entity revision. At cutover the exclusive gate blocks new source writers and waits for existing writers; the applier drains **all committed unapplied rows** before comparison. A sequence-number maximum or an unfenced momentary queue depth is not a drain proof. |
| <a id="rule-bf-07"></a>BF-07 | Full key/revision/hash comparison is partitioned and rehearsed at production scale. A bounded fence finalises changed-key verification against the completed range manifest; any unverified dirty range blocks switching. Samples are additional diagnostics. If the proven fence bound cannot be met, schedule an explicit maintenance window rather than claim an online cutover. |
| BF-08 | Readers switch to a durable migration epoch under the exclusive gate after convergence. Writers/adapters must support that epoch. A/B keep synchronous capture or transactionally validated read-through while readers use the new structure; an asynchronous stale target cannot silently serve acknowledged values. |
| BF-09 | Exceeding the cutover budget aborts **before** changing authority, leaves old authority/capture active and releases the pause. After a successful C cutover, old writers are rejected; restart cannot reopen them. |

`platform.migration_epoch(migration_id PK, mode, epoch, authority, capture_state, fence_state, rollback_open, changed_at)` is the durable control record. `migration_range(migration_id, range_id PK, lower_key, upper_key, snapshot_id, resume_key, state, verification_hash)` records coverage. `migration_capture` uses unique `(migration_id, entity_key, source_revision)` with payload/tombstone/hash and applied receipt. Capture/install, applier and migration executors have separate least-privilege roles; application replicas never run DDL. All fences are transaction-scoped and released on crash; durable epoch/authority determines safe recovery before writes resume.

### 2.6 Rollback data semantics

| # | Rule |
|---|---|
| RW-01 | A/B application rollback is safe only while every allowed write remains representable in and committed to old authority. C closes data rollback at its authority switch, even if the old tables still exist. |
| <a id="rule-rw-02"></a>RW-02 | A/B capture remains active after reader switch until the explicit contract event; no new-only behaviour starts before the recorded rollback horizon closes. |
| RW-03 | Deployment evidence records schema horizon and data horizon independently, with mode, epoch and the event that closes each. |
| <a id="rule-rw-04"></a>RW-04 | Beyond the data horizon use forward repair or a rehearsed restore with declared data-loss window. Do not present an application rollback or flag toggle as lossless. |
| <a id="rule-rw-05"></a>RW-05 | Pre-rollback tooling checks current epoch, writer compatibility, converter liveness and representability; it refuses an unsafe target. |
| <a id="rule-rw-06"></a>RW-06 | A interrupted capture/backfill replays versioned receipts and cannot overwrite a newer target. After capture failure, switching/rollback is blocked until complete convergence is re-established. |

### 2.7 Phase-entry and exit evidence

| Phase | Required evidence |
|---|---|
| Expand | Old writer fixture passes under the installed capture/fence; source update/delete increments the per-key version transactionally. |
| Backfill | All bounded ranges covered; forced delayed v1 backfill cannot replace captured v2 or a v3 tombstone. Crash resumes from durable range receipts. |
| Deploy/soak | Both versions write through the declared converter; no permitted fact is lost by conversion or rollback. |
| Switch | New source writer blocked at fence, in-flight writer drained, every committed capture applied, all dirty ranges verified, epoch transition atomic; mode-C rollback closure recorded. |
| Contract | Horizon explicitly closed; old writers denied before capture/table removal; post-contract restore/forward-fix path rehearsed. |

---

## 3. Configuration and secrets at deploy time

| # | Rule |
|---|---|
| CF-01 | **Environments are configuration, not builds** ([EP-01](14-build-packaging-and-release.md#rule-ep-01)). The same digest runs in staging and production. |
| CF-02 | **Configuration files hold references, never long-lived plaintext secrets** ([CS-01](05-cloud-architecture.md#rule-cs-01) of the cloud architecture); production secrets live in a managed vault in RBAC mode with purge protection ([CS-02](05-cloud-architecture.md#rule-cs-02) there). |
| CF-03 | **CI authenticates with federated identity only** ([EN-08](../requirements/products/arcforges-cloud.md#rule-en-08)); no long-lived deployment credential exists to leak. |
| CF-04 | **Staging and production use different deployment identities**, neither holding subscription-owner rights ([EN-09](../requirements/products/arcforges-cloud.md#rule-en-09)). |
| <a id="rule-cf-05"></a>CF-05 | **A missing or malformed required configuration value fails start-up with a named key**, never a default that silently changes behaviour. |
| CF-06 | **A secret rotation is a configuration change, not a deployment.** The application re-reads on a defined schedule or on a signal, so rotating does not require a release. |
| CF-07 | **IaC state is a secret** ([EN-06](../requirements/products/arcforges-cloud.md#rule-en-06)), stored in a secured backend, never in version control, and separated per environment. |
| CF-08 | **Portal-driven production change is prohibited** ([EN-07](../requirements/products/arcforges-cloud.md#rule-en-07)); an emergency manual change is reconciled back into IaC promptly, and drift detection runs regularly. |

---

## 3.1 Configuration activation — a separate lifecycle from deployment

[DC-01](../requirements/11-policy-and-configuration.md#rule-dc-01)–[DC-17](../requirements/11-policy-and-configuration.md#rule-dc-17) make deployment configuration the production policy source. **Replacing it is not a deployment**, and conflating the two is how a price change ends up requiring an image rebuild — which [DC-02](../requirements/11-policy-and-configuration.md#rule-dc-02) exists to prevent.

```
 0  AUTHOR      operator edits the bundle outside the repository and the image
 1  VALIDATE    schema, identity, cross-references, units, currency, non-negative
                rates, finite capacity and bounds, payment mapping, model categories,
                term transitions, compiled safety ceilings                     -- DC-10
 2  PERSIST     store the validated immutable snapshot with its revision identity
                and content hash                                               -- DC-04, DC-09
 3  ACTIVATE    atomically; exactly one active revision per realm               -- CG-03, DC-12
 4  CONVERGE    every replica loads it; one that cannot admits no affected work -- DC-11
 5  RECORD      each subsequent request records which revision it used          -- CG-02, DC-12
```

| # | Rule |
|---|---|
| CA-01 | **Changing prices must not require rebuilding the image** ([DC-02](../requirements/11-policy-and-configuration.md#rule-dc-02)). The bundle is mounted read-only; the deployment points at the file. |
| CA-02 | **A revision identity cannot be reused with different content** ([DC-04](../requirements/11-policy-and-configuration.md#rule-dc-04)), enforced by a unique constraint on the identity together with the content hash. |
| <a id="rule-ca-03"></a>CA-03 | **Activation is atomic, and all replicas converge on one coherent revision** ([DC-11](../requirements/11-policy-and-configuration.md#rule-dc-11), [DC-12](../requirements/11-policy-and-configuration.md#rule-dc-12)). A replica that cannot load it **admits no affected work** — it does not fall back to a previous revision, and never to the public sample. |
| CA-04 | **Missing prices disable that route; missing official commercial policy disables new paid work without disabling data recovery** ([DC-10](../requirements/11-policy-and-configuration.md#rule-dc-10)). Degradation is scoped to what the gap actually affects. |
| <a id="rule-ca-05"></a>CA-05 | **Rollback publishes a new revision restoring prior values** ([DC-12](../requirements/11-policy-and-configuration.md#rule-dc-12)). A superseded revision is never reactivated, so the history stays append-only. |
| CA-06 | **Replacement never resets usage, replenishes an issued allowance, reissues purchased credits or releases unresolved reservations** ([DC-13](../requirements/11-policy-and-configuration.md#rule-dc-13), [RP-03](16-billing-and-commerce-architecture.md#rule-rp-03)). Clock skew and process restart cannot increase entitlement. |
| CA-07 | **A started Run keeps its pinned customer tariff** ([AC-09](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-09), [DC-12](../requirements/11-policy-and-configuration.md#rule-dc-12)). A new revision cannot retroactively lower a Run's budget or silently raise its rate. |
| CA-08 | **Emergency suspension is a bounded, authenticated, operator-triggered runtime reload** enforced server-side before further dispatch ([DC-11](../requirements/11-policy-and-configuration.md#rule-dc-11)). It does not wait for desktop updates and does not restart all tasks. **There is no unauthenticated upload or reload endpoint.** |
| CA-09 | **Secrets are provisioned separately from the bundle** ([DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15), [CG-06](16-billing-and-commerce-architecture.md#rule-cg-06)) — secret manager or Docker secret, least privilege, absent from the file, the image, the logs and the public sample. |
| CA-10 | **A self-host realm may disable payment collection and apply operator grants within its own realm** ([DC-16](../requirements/11-policy-and-configuration.md#rule-dc-16)), while identity, authorisation, real usage measurement, budget limits and accounting correctness remain enforced. It cannot assert official-service entitlement. |

### 3.2 Configuration failure matrix

| # | Failure | Detected by | Owner | Action |
|---|---|---|---|---|
| CFV-01 | Malformed, partial or duplicate-version bundle | Validation, step 1 | Operations | Rejected before persistence; the active revision is untouched |
| CFV-02 | Unknown billable model dimension | Validation | Operations | Rejected — an unpriced route would admit an unbounded charge ([AD-04](16-billing-and-commerce-architecture.md#rule-ad-04)) |
| CFV-03 | Currency or payment-mapping mismatch | Validation | Operations | Rejected ([DC-10](../requirements/11-policy-and-configuration.md#rule-dc-10), [MT-16](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-16)) |
| CFV-04 | A replica cannot load the activated revision | Startup and reload check | Operations | **That replica admits no affected work** ([CA-03](#rule-ca-03)); it does not serve from a stale revision |
| CFV-05 | Production accidentally pointed at the public sample | Environment and realm field mismatch ([DC-04](../requirements/11-policy-and-configuration.md#rule-dc-04)) | Operations | Rejected. **A sample is labelled non-production and never silently selected** (`§8.6` of the commerce requirements) |
| CFV-06 | Activation succeeds but a rate is wrong | Post-activation review | Operations | Publish a **new** revision restoring prior values ([CA-05](#rule-ca-05)). History is not edited |

---

## 4. Client release execution

Client and cloud releases are decoupled ([EP-04](14-build-packaging-and-release.md#rule-ep-04)), so this sequence runs independently of `§2`.

### 4.1 Desktop

```
build once (per RID) → sign → publish to the artifact store
   → update feed entry: version, hashes, compatibility range, minimum versions
   → channel promotion: nightly → beta → stable
   → client discovers, verifies hash and signature, stages, applies
```

| # | Rule |
|---|---|
| CD-01 | **The product's own feed is authoritative; storage is replaceable** (`§7` of the build architecture, confirmed independently by [AC-17](19-product-implementation-maps.md#rule-ac-17) of the AionUI matrix). |
| CD-02 | **A client verifies hash and signature before applying**, and a corrupted artifact is rejected rather than installed ([WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02)). |
| CD-03 | **An update never interrupts a long-running task.** It stages and applies at a safe point, and the update matrix tests exactly this case. |
| CD-04 | **Downgrade protection is enforced by the feed and by compatibility policy**, so a blocked bad version is refused twice. |
| <a id="rule-cd-05"></a>CD-05 | **An interrupted download or install leaves a working previous installation.** Partial state is never the resting state. |
| <a id="rule-cd-06"></a>CD-06 | **The four desktop products version independently** ([CM-02](../requirements/12-quality-and-compatibility-contract.md#rule-cm-02) of the quality contract), and **mixed-version combinations are actually tested** — nominal independence with de facto lockstep is a failed contract. |

### 4.2 Mobile

| # | Rule |
|---|---|
| MR-01 | **Store review latency is part of the release plan**, not a surprise. A fix that must reach users quickly cannot depend on a store round trip. |
| MR-02 | **Android release is verified on real devices** ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) of the quality contract), against the release AOT artifact. |
| MR-03 | **iOS is architecture-present, build-deferred** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) and is **never claimed as released**. |

### 4.3 Web

| # | Rule |
|---|---|
| CW-01 | **Static output regenerates byte-identically**, so a deployment that changes nothing produces no diff. |
| CW-02 | **A cached browser bundle must not strand a client on an incompatible version.** Version identity is part of the bundle's cache key. |
| CW-03 | **A web deployment is reversible by redeploying the previous artifact**, which is why the artifact is retained rather than regenerated. |

---

## 5. The compatibility window

| Axis | Window | Rule |
|---|---|---|
| Desktop ↔ desktop, locally | Current stable **and** the immediately previous supported stable line, **both directions** ([CM-03](../requirements/12-quality-and-compatibility-contract.md#rule-cm-03) of the quality contract) | A floor, not a ceiling ([CM-05](../requirements/12-quality-and-compatibility-contract.md#rule-cm-05) there) |
| Client ↔ Cloud | Cloud's declared **Supported Client Set** ([CM-06](../requirements/12-quality-and-compatibility-contract.md#rule-cm-06) there) | Removal is planned and communicated, **never discovered by users** |
| Extension protocol | Current major **and** previous major ([CM-08](../requirements/12-quality-and-compatibility-contract.md#rule-cm-08) there) | Earlier revocation only for a security reason |
| Native formats | Every format in the Supported Native Format set ([CM-09](../requirements/12-quality-and-compatibility-contract.md#rule-cm-09) there) | **Format compatibility outlives application interoperability** |

| # | Rule |
|---|---|
| CO-01 | **A cloud release must not require a client release on the same day** ([EP-04](14-build-packaging-and-release.md#rule-ep-04)). If it would, it is not shippable as designed. |
| CO-02 | **A minimum-cloud-version requirement is imposed only after every channel has had a genuine opportunity to update** ([EP-05](14-build-packaging-and-release.md#rule-ep-05)), with the grace period honoured. |
| CO-03 | **Every release produces a Compatibility Manifest as a release artifact** ([CM-01](../requirements/12-quality-and-compatibility-contract.md#rule-cm-01) there), so the window is a published fact rather than an assumption. |
| CO-04 | **Read compatibility is not write compatibility** ([CM-10](../requirements/12-quality-and-compatibility-contract.md#rule-cm-10) there, [I-385](../requirements/01-normative-glossary-and-invariants.md#rule-i-385)). Each is declared and tested separately, so "we can open it" never becomes an implied "we can save it". |

---

## 6. Deployment failure matrix

| # | Failure | Effect | Detected by | Owner | Action |
|---|---|---|---|---|---|
| DF-01 | Expand migration fails part-way | Schema partially expanded | Migration step exit check | Operations | Roll back the additive change; the deployed version is unaffected |
| DF-02 | Backfill stalls | New structures partly populated | Backfill progress metric | Operations | Resume; **nothing reads them yet**, so there is no user impact |
| DF-03 | Deploy fails on some replicas | Mixed fleet | Health checks per replica | Operations | Roll back the application; mixed-version tolerance (`§2.3`) makes this safe |
| DF-04 | New version healthy but error rate rises in soak | Working but degraded | Release envelope | Operations | Roll back; investigate before re-attempting |
| DF-05 | Switch flag causes a regression | New behaviour bad | Alerting, error budget | Operations | **Turn the flag off** — seconds, no deployment |
| DF-06 | Contract removes something still read | Errors on a live path | Immediate errors | Operations | **Restore** ([RH-03](#rule-rh-03)). This is why `§2.1` gates contract entry on "no read path touches it" |
| DF-07 | Rollback attempted after the horizon closed | Rollback unavailable | Pre-rollback check | Operations | Forward fix, or restore with drill-proven procedure |
| DF-08 | Configuration missing at start-up | Replica does not start | Start-up validation ([CF-05](#rule-cf-05)) | Operations | Fix configuration; **no replica ever starts with a silent default** |
| DF-09 | Client update interrupted mid-install | Previous installation intact | Client update matrix | Client | Retry; **partial state is never the resting state** ([CD-05](#rule-cd-05)) |
| DF-10 | Client on a version outside the Supported Client Set | Refused with a named reason and an update path | Version check | Cloud | The user is told what to do, never given an opaque failure |
| DF-11 | Capture installation did not fence prior writers or started after the snapshot | Coverage cannot be established | Range/capture provenance check | Operations | Re-establish capture under the gate and rebuild affected ranges with the version predicate; do not switch until full convergence |
| DF-12 | Live equivalence sample finds divergence | Old and new disagree | Equivalence check ([BF-07](#rule-bf-07)) | Operations | Stop the sequence. A divergence before the switch is a converter or backfill defect, and switching would make it user-visible |
| DF-13 | Mode C write pause exceeds its measured bound | Writes blocked longer than announced | Pause timer | Operations | **Abort the cutover** and release the pause. The old representation is still authoritative, so aborting is safe |
| DF-14 | Application rollback attempted after a mode C cutover | Post-cutover facts unreadable by the old version | Pre-rollback check ([RW-05](#rule-rw-05)) | Operations | **Refused by tooling**, with the mode and cutover named. Forward fix or restore ([RW-04](#rule-rw-04)) |
| DF-15 | Capture stopped before contract | The old representation goes stale, silently closing the data-rollback window while the schema window still looks open | Capture liveness check ([RW-02](#rule-rw-02), [BF-05](#rule-bf-05)) | Operations | **Restart capture and re-backfill the gap**, then treat the window as closed until convergence is re-established |
| DF-16 | An unfenced empty backlog was mistaken for convergence | A writer can commit between check and switch | Exclusive epoch-fence test | Operations | Block source writes, drain in-flight writers and committed capture, verify dirty ranges, then switch or abort |

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| DV-01 | Migration forward and backward rehearsal passes against a production-shaped copy before every schema deployment | [RG-15](14-build-packaging-and-release.md#rule-rg-15), [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| DV-02 | Expand-only enforcement is a machine check, and a non-additive migration in an expand phase fails the gate | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| DV-03 | A rolling deployment is exercised with both version orderings, and rows and messages written by either are readable by the other | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03), [WP-50.04](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.04) |
| DV-04 | A long-running task survives a full fleet roll, and no lease is silently abandoned | [WP-21.05](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05), [WP-16.00](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.00) |
| DV-05 | An application rollback restores service without a schema change, at every point in the sequence before contract | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03), [WP-50.04](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.04) |
| DV-06 | A switch flag disables the new behaviour without a deployment | [WP-44.03](../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.03) |
| DV-07 | A missing required configuration value fails start-up naming the key, and no default is silently substituted | [WP-44.01](../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01), [WP-21.06](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) |
| DV-13 | Two example policies with different rates, prices, recovery rates and grants change future decisions and leave historical charges identical | [WP-44.01](../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01), [WP-43.07](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07) |
| DV-14 | Replacement during concurrent requests produces no mixed-version evaluation, quota reset or duplicate grant | [WP-44.01](../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01), [WP-42.11](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) |
| DV-15 | All replicas restart preserving balances, holds and refill state | [WP-42.11](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11), [WP-21.06](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) |
| DV-16 | A replica that cannot load the active revision admits no affected work and never falls back to a sample | [WP-44.01](../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01) |
| DV-08 | The full client update matrix passes on all three desktop platforms, including interrupted download, interrupted install, corrupted artifact and update during a long task | [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) |
| DV-09 | Mixed-version desktop combinations are tested in both directions, per [CM-03](../requirements/12-quality-and-compatibility-contract.md#rule-cm-03) of the quality contract | [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02), [WP-23.06](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.06) |
| DV-10 | A Compatibility Manifest is produced for every release and matches what was tested | [WP-50.00](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.00), [WP-50.08](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.08) |
| DV-11 | A client outside the Supported Client Set receives a named reason and an update path, never an opaque failure | [WP-23.06](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.06) |
| DV-12 | Every deployment phase records its checks, operator and time, and an incident can reconstruct the sequence | [WP-45.04](../planning/work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.04) |
| DV-17 | A row updated by an old replica after its backfill reaches the new representation **through capture**, and the switch never reads a stale representation ([BF-03](#rule-bf-03), [BF-05](#rule-bf-05)) | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| DV-18 | A mode B converter maintains the new representation for writes made by a version that does not know it exists | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| DV-19 | The live equivalence sample detects an injected divergence and stops the sequence | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03), [WP-50.04](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.04) |
| DV-20 | A mode C write pause is rehearsed, measured, and aborts cleanly when it exceeds its bound | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| DV-21 | The pre-rollback check refuses an unsafe application rollback and names the mode and cutover that closed the window | [WP-50.04](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.04) |
| DV-22 | Capture installation fences old writers, and delayed v1 backfill cannot overwrite captured v2 or a delete tombstone | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| DV-23 | A write made by an **old** replica during deploy and soak reaches the new representation through capture, with no application code in that path ([BF-03](#rule-bf-03)) | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03), [WP-50.04](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.04) |
| DV-24 | A writer racing cutover is either drained before the barrier or admitted under the new epoch; an asynchronous backlog is drained under the exclusive fence | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| DV-25 | An application rollback **after** the switch and within the horizon reads correct data, because capture never stopped ([RW-06](#rule-rw-06)) | [WP-50.04](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.04) |

**Browser realtime topology.** Configure the production edge for the browser WebSocket upgrade path. Browser SignalR uses WebSockets-only/skip-negotiation; a blocked upgrade falls back to generated ordinary HTTP operations, not SignalR long polling. Verify cross-replica catch-up with no affinity and no required backplane. This is the explicit transport companion to the shared session store in [Web architecture](10-web-architecture.md#5-browser-session-architecture--p2-003-resolved).
