# Deployment and Release Execution

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: `§6` and `§6.1` of the cloud requirements, `§15` of the quality contract, `§11` of the build architecture
> Companions: [`14-build-packaging-and-release.md`](14-build-packaging-and-release.md), [`05-cloud-architecture.md`](05-cloud-architecture.md), [`20-cross-system-lifecycles.md`](20-cross-system-lifecycles.md)

The requirements say migration is a gated step, that schema change uses expand/contract, and that a production deployment is reversible. **What none of them gives is the sequence** — the order of the phases, the check that must pass between each, and what happens when one fails with a half-deployed fleet. A deployment procedure that exists only as a set of rules is a procedure that gets improvised at 2 a.m.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| DX-01 | **A deployment is a sequence of phases, each with an entry check, an exit check and a defined failure action.** A phase without all three is not deployable. |
| DX-02 | **Every phase is independently reversible, or it is not entered.** Where reversal is impossible — a contract phase that drops a column — the phase is deferred until the version that needs it is irreversibly established (`§2.4`). |
| DX-03 | **No phase depends on every replica being at the same version at the same instant.** Rolling deployment means mixed versions are the normal state, not an exception (`PS-10` of the cloud architecture). |
| DX-04 | **Production never rebuilds** (`EN-10`). The digest built once in CI is what runs, and deployment references the digest, never a tag (`EN-11`). |
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
| **0 Pre-flight** | Digest matches the CI-produced artifact; every release gate has resolvable evidence (`WP-50.00`); environment approval granted (`EN-13`) | All three pass | Stop. Nothing has changed |
| **1 Expand** | Migration is **additive only** — a machine check, not a reviewer's judgement; forward and backward rehearsal passed against a production-shaped copy (`RG-15`) | Schema applied; **the currently deployed version still passes its health checks** | Roll the migration back. It is additive, so rollback is safe by construction |
| **2 Backfill** | New structures exist; the backfill is resumable and idempotent | Backfill complete or provably converging; **no read path depends on it yet** | Stop and resume later. Old code is unaffected because it does not read the new structures |
| **3 Deploy** | Expand applied; the new version is **proven to run against the expanded schema** — this is the compatibility that makes rolling safe | Every replica healthy at the new version; error rate and latency within the release envelope | **Roll back the application** (`EN-14`, one action). The schema stays expanded, which is why this rollback is always available |
| **4 Soak** | Fleet at the new version | The soak window elapses with no new page-worthy condition and no error-budget burn | Roll back the application. The schema stays expanded |
| **5 Switch** | Soak clean; the new behaviour is behind a policy flag (`§4` of the policy architecture) | The behaviour is on and healthy | **Turn the flag off** — no deployment needed, which is the point of separating switch from deploy |
| **6 Contract** | The new version is **irreversibly established**: rollback to the pre-expand version is no longer a permitted action, and no read path touches the removed structure | Removal applied | Stop. A contract failure is the only phase whose reversal needs a restore, which is why `§2.4` gates entry so hard |

### 2.2 Why the phases are separate

| Separation | What it buys |
|---|---|
| Expand before deploy | The old version keeps working, so deploy is reversible |
| Backfill before switch | The new behaviour never reads a half-populated structure |
| Deploy before switch | A bad *deployment* and a bad *behaviour* fail independently and are diagnosed separately |
| Switch by flag, not by deploy | Reversal is seconds, not a deployment cycle |
| Contract as a **separate, later deployment** | The window in which rollback is possible is not shortened by tidying up |

| # | Rule |
|---|---|
| PH-01 | **Expand and contract are never in the same deployment.** Combining them removes the rollback path the expand phase exists to preserve. |
| PH-02 | **Contract runs only after the intervening version is established beyond the rollback horizon**, which is a stated duration, not a feeling. |
| PH-03 | **A migration that cannot be expressed as expand-then-contract is a design problem**, escalated rather than executed as a single destructive step (`MG-04`). |
| PH-04 | **"Migration down" is not the rollback strategy** (`MG-04`). Rollback is an application rollback or a forward fix. |
| PH-05 | **Migration never runs on application start-up, on any replica** (`MG-01`). It is a separate gated step with a single executor. |

### 2.3 Mixed-version behaviour during phases 3 and 4

| Situation | Required behaviour |
|---|---|
| Old replica reads a row written by a new replica | Unknown fields preserved on round trip; no loss (`SY-09` of the lifecycle document) |
| New replica reads a row written by an old replica | New columns absent or default; the new code must tolerate this, and a test asserts it |
| An outbox message enqueued by one version, consumed by the other | Message contracts are additive-only within a major; a consumer ignores unknown fields |
| A background lease taken by an old replica, expiring during deploy | Lease expiry is version-independent; another replica takes it (`BG-02`, `BG-03`) |
| A long-running task started before the deploy | **Task authority is in the database, not the worker** (`BG-03`). It continues on any replica |
| A realtime connection to a replica being drained | The client reconnects and **reconciles unconditionally** (`GP-03`) |

| # | Rule |
|---|---|
| MX-01 | **Both orderings are tested**, not just old-then-new (`CM-07` of the quality contract) — a client or replica newer than its peer is as normal as the reverse. |
| MX-02 | **A message or row written by either version is readable by the other**, for the whole rolling window. |
| MX-03 | **Draining a replica completes or releases its in-flight work**; it never abandons a lease silently. |

### 2.4 The rollback horizon

| # | Rule |
|---|---|
| RH-01 | **The rollback horizon is the period during which the previous version can be restored by an application rollback alone.** It begins at deploy and ends at contract. |
| RH-02 | **Contract closes the horizon**, which is why `§2.1` phase 6 requires that closing it be an explicit, recorded decision rather than a consequence of routine tidying. |
| RH-03 | **Beyond the horizon, recovery is a restore**, with its own drill evidence (`WP-46.03`) — a materially more expensive operation, and the reason the horizon is generous by default. |
| RH-04 | **A security fix may close the horizon early**, and that is a decision with its own record, not an exception taken quietly. |

---

### 2.5 Backfill catch-up and rollback data safety

> **Added 2026-09-07.** The phase table said backfill populates new structures while old code still *reads* old ones. Old code also **writes** them. A row backfilled at T and updated by old code at T+1 leaves the new representation **stale**, and the switch then reads it. Separately, "the migration was additive" makes the *schema* rollback-safe; it says nothing about **data** written only in the new representation after the switch. Both gaps are closed here.

#### The write-compatibility ladder

Every expand/contract migration declares one of three modes **before** the expand phase, and the mode determines the backfill and rollback procedure.

| Mode | When it applies | Backfill | Rollback safety |
|---|---|---|---|
| **A — Derived** | The new structure is computable from the old at any time (an index, a denormalisation, a projection) | Backfill, then a **catch-up pass** to convergence | **Free.** Old code never needed the new structure; rolling back loses nothing |
| **B — Dual-write** | Both representations must carry the same fact during the window | New code writes **both**; old code writes the old one, and a **converter** maintains the new one for those writes | **Free while dual-write holds.** The old representation is never behind |
| **C — Exclusive** | The new representation carries facts the old one cannot express | Backfill, then a **bounded write pause** at cutover | **Not free.** Rollback loses post-cutover facts, so it is gated by `§2.6` |

| # | Rule |
|---|---|
| BF-01 | **The mode is declared in the migration, not chosen at execution time**, and the deployment gate refuses a migration that declares none. |
| BF-02 | **Mode A is the default and is preferred.** Most schema evolution can be made derived by keeping the old column authoritative until contract. |
| BF-03 | **Mode B's converter is part of the migration, not of application code.** It is a database trigger or an outbox-driven applier that runs regardless of which application version wrote the row, because the whole point is that old code does not know about the new structure. |
| BF-04 | **Mode C requires an explicit, bounded, announced write pause** on the affected aggregates. It is the only mode that may block writes, its duration is measured in the rehearsal, and exceeding the measured bound aborts the cutover. |
| BF-05 | **Backfill is not complete when the pass ends.** It is complete when a **catch-up pass finds nothing** — no row whose old representation changed after its backfill. Convergence, not completion, is the exit check. |
| BF-06 | **The catch-up pass is driven by change detection, not by re-scanning**: the affected rows carry an update watermark, and the pass reprocesses only rows updated since their backfill. A full re-scan is the fallback, and its cost is measured. |
| BF-07 | **Equivalence is asserted before the switch, on live data**: a sampled comparison of old and new representations must find zero divergence, and a divergence stops the sequence (`DX-05`). A backfill that "looks done" is not evidence. |

#### 2.6 The rollback window and its data semantics

`RH-01` defines the rollback horizon in terms of *schema*. This defines it in terms of **data**.

| # | Rule |
|---|---|
| RW-01 | **Rollback is data-safe only while the old representation is still authoritative or still maintained.** In mode A that is always; in mode B it is until dual-write stops; in mode C it ends at cutover. |
| RW-02 | **The switch is what ends mode B's dual-write, and it is a separate decision from the flag that enables the behaviour.** Turning the behaviour off does not restart dual-write, so the two are ordered: stop the behaviour, confirm, then stop dual-write. |
| RW-03 | **A mode C cutover closes the data-rollback window immediately**, even though the schema window stays open until contract. The deployment record states both, because assuming they are the same is how a "safe" rollback silently discards a day of writes. |
| RW-04 | **Beyond the data-rollback window, recovery is a forward fix or a restore** (`RH-03`), never an application rollback presented as safe. |
| RW-05 | **The pre-rollback check is mechanical**: the operator tooling refuses an application rollback whose target version cannot read the current authoritative representation, and states which mode and which cutover closed the window. |

#### 2.7 Additions to the phase table

| Phase | Additional entry check | Additional exit check |
|---|---|---|
| **1 Expand** | The migration declares mode A, B or C (`BF-01`); a mode B converter exists and is itself tested | — |
| **2 Backfill** | — | **Catch-up converges** (`BF-05`) and the live equivalence sample finds zero divergence (`BF-07`) |
| **5 Switch** | For mode C, the announced write pause has been rehearsed and its measured bound is within budget (`BF-04`) | The data-rollback window's state is **recorded** (`RW-03`) |
| **6 Contract** | Dual-write, where used, has been stopped and confirmed (`RW-02`) | — |

---

## 3. Configuration and secrets at deploy time

| # | Rule |
|---|---|
| CF-01 | **Environments are configuration, not builds** (`EP-01`). The same digest runs in staging and production. |
| CF-02 | **Configuration files hold references, never long-lived plaintext secrets** (`CS-01` of the cloud architecture); production secrets live in a managed vault in RBAC mode with purge protection (`CS-02` there). |
| CF-03 | **CI authenticates with federated identity only** (`EN-08`); no long-lived deployment credential exists to leak. |
| CF-04 | **Staging and production use different deployment identities**, neither holding subscription-owner rights (`EN-09`). |
| CF-05 | **A missing or malformed required configuration value fails start-up with a named key**, never a default that silently changes behaviour. |
| CF-06 | **A secret rotation is a configuration change, not a deployment.** The application re-reads on a defined schedule or on a signal, so rotating does not require a release. |
| CF-07 | **IaC state is a secret** (`EN-06`), stored in a secured backend, never in version control, and separated per environment. |
| CF-08 | **Portal-driven production change is prohibited** (`EN-07`); an emergency manual change is reconciled back into IaC promptly, and drift detection runs regularly. |

---

## 3.1 Configuration activation — a separate lifecycle from deployment

`DC-01`–`DC-17` make deployment configuration the production policy source. **Replacing it is not a deployment**, and conflating the two is how a price change ends up requiring an image rebuild — which `DC-02` exists to prevent.

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
| CA-01 | **Changing prices must not require rebuilding the image** (`DC-02`). The bundle is mounted read-only; the deployment points at the file. |
| CA-02 | **A revision identity cannot be reused with different content** (`DC-04`), enforced by a unique constraint on the identity together with the content hash. |
| CA-03 | **Activation is atomic, and all replicas converge on one coherent revision** (`DC-11`, `DC-12`). A replica that cannot load it **admits no affected work** — it does not fall back to a previous revision, and never to the public sample. |
| CA-04 | **Missing prices disable that route; missing official commercial policy disables new paid work without disabling data recovery** (`DC-10`). Degradation is scoped to what the gap actually affects. |
| CA-05 | **Rollback publishes a new revision restoring prior values** (`DC-12`). A superseded revision is never reactivated, so the history stays append-only. |
| CA-06 | **Replacement never resets usage, replenishes an issued allowance, reissues purchased credits or releases unresolved reservations** (`DC-13`, `RP-03`). Clock skew and process restart cannot increase entitlement. |
| CA-07 | **A started Run keeps its pinned customer tariff** (`AC-09`, `DC-12`). A new revision cannot retroactively lower a Run's budget or silently raise its rate. |
| CA-08 | **Emergency suspension is a bounded, authenticated, operator-triggered runtime reload** enforced server-side before further dispatch (`DC-11`). It does not wait for desktop updates and does not restart all tasks. **There is no unauthenticated upload or reload endpoint.** |
| CA-09 | **Secrets are provisioned separately from the bundle** (`DC-15`, `CG-06`) — secret manager or Docker secret, least privilege, absent from the file, the image, the logs and the public sample. |
| CA-10 | **A self-host realm may disable payment collection and apply operator grants within its own realm** (`DC-16`), while identity, authorisation, real usage measurement, budget limits and accounting correctness remain enforced. It cannot assert official-service entitlement. |

### 3.2 Configuration failure matrix

| # | Failure | Detected by | Owner | Action |
|---|---|---|---|---|
| CF-01 | Malformed, partial or duplicate-version bundle | Validation, step 1 | Operations | Rejected before persistence; the active revision is untouched |
| CF-02 | Unknown billable model dimension | Validation | Operations | Rejected — an unpriced route would admit an unbounded charge (`AD-04`) |
| CF-03 | Currency or payment-mapping mismatch | Validation | Operations | Rejected (`DC-10`, `MT-16`) |
| CF-04 | A replica cannot load the activated revision | Startup and reload check | Operations | **That replica admits no affected work** (`CA-03`); it does not serve from a stale revision |
| CF-05 | Production accidentally pointed at the public sample | Environment and realm field mismatch (`DC-04`) | Operations | Rejected. **A sample is labelled non-production and never silently selected** (`§8.6` of the commerce requirements) |
| CF-06 | Activation succeeds but a rate is wrong | Post-activation review | Operations | Publish a **new** revision restoring prior values (`CA-05`). History is not edited |

---

## 4. Client release execution

Client and cloud releases are decoupled (`EP-04`), so this sequence runs independently of `§2`.

### 4.1 Desktop

```
build once (per RID) → sign → publish to the artifact store
   → update feed entry: version, hashes, compatibility range, minimum versions
   → channel promotion: nightly → beta → stable
   → client discovers, verifies hash and signature, stages, applies
```

| # | Rule |
|---|---|
| CD-01 | **The product's own feed is authoritative; storage is replaceable** (`§7` of the build architecture, confirmed independently by `AC-17` of the AionUI matrix). |
| CD-02 | **A client verifies hash and signature before applying**, and a corrupted artifact is rejected rather than installed (`WP-50.02`). |
| CD-03 | **An update never interrupts a long-running task.** It stages and applies at a safe point, and the update matrix tests exactly this case. |
| CD-04 | **Downgrade protection is enforced by the feed and by compatibility policy**, so a blocked bad version is refused twice. |
| CD-05 | **An interrupted download or install leaves a working previous installation.** Partial state is never the resting state. |
| CD-06 | **The four desktop products version independently** (`CM-02` of the quality contract), and **mixed-version combinations are actually tested** — nominal independence with de facto lockstep is a failed contract. |

### 4.2 Mobile

| # | Rule |
|---|---|
| MR-01 | **Store review latency is part of the release plan**, not a surprise. A fix that must reach users quickly cannot depend on a store round trip. |
| MR-02 | **Android release is verified on real devices** (`PM-03` of the quality contract), against the release AOT artifact. |
| MR-03 | **iOS is architecture-present, build-deferred** (**D-008**) and is **never claimed as released**. |

### 4.3 Web

| # | Rule |
|---|---|
| CW-01 | **Static output regenerates byte-identically**, so a deployment that changes nothing produces no diff. |
| CW-02 | **A cached WebAssembly bundle must not strand a client on an incompatible version.** Version identity is part of the bundle's cache key. |
| CW-03 | **A web deployment is reversible by redeploying the previous artifact**, which is why the artifact is retained rather than regenerated. |

---

## 5. The compatibility window

| Axis | Window | Rule |
|---|---|---|
| Desktop ↔ desktop, locally | Current stable **and** the immediately previous supported stable line, **both directions** (`CM-03` of the quality contract) | A floor, not a ceiling (`CM-05` there) |
| Client ↔ Cloud | Cloud's declared **Supported Client Set** (`CM-06` there) | Removal is planned and communicated, **never discovered by users** |
| Extension protocol | Current major **and** previous major (`CM-08` there) | Earlier revocation only for a security reason |
| Native formats | Every format in the Supported Native Format set (`CM-09` there) | **Format compatibility outlives application interoperability** |

| # | Rule |
|---|---|
| CO-01 | **A cloud release must not require a client release on the same day** (`EP-04`). If it would, it is not shippable as designed. |
| CO-02 | **A minimum-cloud-version requirement is imposed only after every channel has had a genuine opportunity to update** (`EP-05`), with the grace period honoured. |
| CO-03 | **Every release produces a Compatibility Manifest as a release artifact** (`CM-01` there), so the window is a published fact rather than an assumption. |
| CO-04 | **Read compatibility is not write compatibility** (`CM-10` there, `I-385`). Each is declared and tested separately, so "we can open it" never becomes an implied "we can save it". |

---

## 6. Deployment failure matrix

| # | Failure | Effect | Detected by | Owner | Action |
|---|---|---|---|---|---|
| DF-01 | Expand migration fails part-way | Schema partially expanded | Migration step exit check | Operations | Roll back the additive change; the deployed version is unaffected |
| DF-02 | Backfill stalls | New structures partly populated | Backfill progress metric | Operations | Resume; **nothing reads them yet**, so there is no user impact |
| DF-03 | Deploy fails on some replicas | Mixed fleet | Health checks per replica | Operations | Roll back the application; mixed-version tolerance (`§2.3`) makes this safe |
| DF-04 | New version healthy but error rate rises in soak | Working but degraded | Release envelope | Operations | Roll back; investigate before re-attempting |
| DF-05 | Switch flag causes a regression | New behaviour bad | Alerting, error budget | Operations | **Turn the flag off** — seconds, no deployment |
| DF-06 | Contract removes something still read | Errors on a live path | Immediate errors | Operations | **Restore** (`RH-03`). This is why `§2.1` gates contract entry on "no read path touches it" |
| DF-07 | Rollback attempted after the horizon closed | Rollback unavailable | Pre-rollback check | Operations | Forward fix, or restore with drill-proven procedure |
| DF-08 | Configuration missing at start-up | Replica does not start | Start-up validation (`CF-05`) | Operations | Fix configuration; **no replica ever starts with a silent default** |
| DF-09 | Client update interrupted mid-install | Previous installation intact | Client update matrix | Client | Retry; **partial state is never the resting state** (`CD-05`) |
| DF-10 | Client on a version outside the Supported Client Set | Refused with a named reason and an update path | Version check | Cloud | The user is told what to do, never given an opaque failure |
| DF-11 | Backfill catch-up never converges — the write rate exceeds the pass rate | New representation permanently stale | Convergence check (`BF-05`) | Operations | **Do not switch.** Either raise the pass rate, or change the migration to mode B so old writes maintain the new structure |
| DF-12 | Live equivalence sample finds divergence | Old and new disagree | Equivalence check (`BF-07`) | Operations | Stop the sequence. A divergence before the switch is a converter or backfill defect, and switching would make it user-visible |
| DF-13 | Mode C write pause exceeds its measured bound | Writes blocked longer than announced | Pause timer | Operations | **Abort the cutover** and release the pause. The old representation is still authoritative, so aborting is safe |
| DF-14 | Application rollback attempted after a mode C cutover | Post-cutover facts unreadable by the old version | Pre-rollback check (`RW-05`) | Operations | **Refused by tooling**, with the mode and cutover named. Forward fix or restore (`RW-04`) |
| DF-15 | Dual-write stopped before the behaviour flag was turned off | New writes reach only the new representation while the old is presumed maintained | Ordering check (`RW-02`) | Operations | Restart dual-write, then re-order the shutdown correctly |

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| DV-01 | Migration forward and backward rehearsal passes against a production-shaped copy before every schema deployment | `RG-15`, `WP-21.03` |
| DV-02 | Expand-only enforcement is a machine check, and a non-additive migration in an expand phase fails the gate | `WP-21.03` |
| DV-03 | A rolling deployment is exercised with both version orderings, and rows and messages written by either are readable by the other | `WP-21.03`, `WP-50.04` |
| DV-04 | A long-running task survives a full fleet roll, and no lease is silently abandoned | `WP-21.05`, `WP-16.00` |
| DV-05 | An application rollback restores service without a schema change, at every point in the sequence before contract | `WP-21.03`, `WP-50.04` |
| DV-06 | A switch flag disables the new behaviour without a deployment | `WP-44.03` |
| DV-07 | A missing required configuration value fails start-up naming the key, and no default is silently substituted | `WP-44.01`, `WP-21.06` |
| DV-13 | Two example policies with different rates, prices, recovery rates and grants change future decisions and leave historical charges identical | `WP-44.01`, `WP-43.07` |
| DV-14 | Replacement during concurrent requests produces no mixed-version evaluation, quota reset or duplicate grant | `WP-44.01`, `WP-42.11` |
| DV-15 | All replicas restart preserving balances, holds and refill state | `WP-42.11`, `WP-21.06` |
| DV-16 | A replica that cannot load the active revision admits no affected work and never falls back to a sample | `WP-44.01` |
| DV-08 | The full client update matrix passes on all three desktop platforms, including interrupted download, interrupted install, corrupted artifact and update during a long task | `WP-50.02` |
| DV-09 | Mixed-version desktop combinations are tested in both directions, per `CM-03` of the quality contract | `WP-50.02`, `WP-23.06` |
| DV-10 | A Compatibility Manifest is produced for every release and matches what was tested | `WP-50.00`, `WP-50.08` |
| DV-11 | A client outside the Supported Client Set receives a named reason and an update path, never an opaque failure | `WP-23.06` |
| DV-12 | Every deployment phase records its checks, operator and time, and an incident can reconstruct the sequence | `WP-45.04` |
| DV-17 | A row updated by old code after its backfill is caught by the catch-up pass, and the switch never reads a stale new representation | `WP-21.03` |
| DV-18 | A mode B converter maintains the new representation for writes made by a version that does not know it exists | `WP-21.03` |
| DV-19 | The live equivalence sample detects an injected divergence and stops the sequence | `WP-21.03`, `WP-50.04` |
| DV-20 | A mode C write pause is rehearsed, measured, and aborts cleanly when it exceeds its bound | `WP-21.03` |
| DV-21 | The pre-rollback check refuses an unsafe application rollback and names the mode and cutover that closed the window | `WP-50.04` |
