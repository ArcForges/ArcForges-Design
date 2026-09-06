# End-to-End Workflow Verification

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Produced: 2026-09-06, **recomputed against the P2-006 requirements revision**. The five workflows of the previous baseline are superseded; three of them changed materially under the revised scope.
> Method: each step is resolved against a named operation, schema, rule or gate. **A step that cannot be resolved is a finding**, not a narrative gap.

A specification set can satisfy every internal check and still be unimplementable, because implementability is a property of whole workflows rather than of individual documents. These eight traces cross the most boundaries in the system, and each is followed to a **terminal state on both the success and the failure path**.

**Result: eight workflows traced, 0 unresolved steps, 7 findings — all closed within this pass.**

---

## 1. How to read a trace

| Column | Meaning |
|---|---|
| Step | What happens |
| Resolves to | The operation, schema, or rule that specifies it. **Every cell must be resolvable** |
| Failure branch | Where the trace continues when this step fails |

A step resolving to a requirement alone is **not** sufficient — a requirement states what must be true, not how.

---

## 2. Workflow A — purchase to settled AI usage

> *A user subscribes, then immediately runs an agent turn.* Crosses commerce, entitlement, configuration, the Harness and the metering chain.

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| A-01 | Purchase intent, provider checkout, webhook persisted before processing | `purchase.createIntent`; `EI-01`; `commerce.provider_event` | Signature invalid → quarantined, never processed (`PE-05`) |
| A-02 | Order and payment written | `commerce.order`, `commerce.payment` | Unmatched payment → quarantined, **never granted** (`PE-09`) |
| A-03 | **A service term is created** — the only four sources are a subscription, a Pass, an audited compensation or a self-host grant | `entitlement.service_term`; `SV-02`; `UQ (kind, source_ref)` | Replayed event → **extends nothing twice**, by unique constraint |
| A-04 | Capacity bucket initialised **once**, idempotently | `entitlement.capacity_bucket.initialised_from`; `RF-07` | Duplicate activation → no second initialisation |
| A-05 | Client hinted, then re-reads authoritatively | `serviceTerm.changed` → `entitlement.getServiceTerm`; `entitlement.getCapacity` | Event lost → converges on next read (`RE-07`) |
| A-06 | User starts a turn | `StartAgentTurnAsync` → Cloud (`CH-01`) | No term → `entitlement.no_service_term` **before any provider call** (`CH-03`, `AD-01`) |
| A-07 | **Admission**: refill, then atomically reserve capacity and check ceilings and provider budget | `§7.3` of the commerce architecture; `entitlement.capacity_reservation` | Insufficient → `capacity_exhausted` with `recoveryAt`, or `extra_credits_required` (`AI-02`, `AI-03`) |
| A-08 | Supplier price resolved at dispatch; customer tariff **pinned to the Run** | `agent.supplier_price_version`, `agent.tariff_version`; `MT-06`, `PR-05` | Unpriced category → **not dispatchable** (`AD-04`, `MT-15`) |
| A-09 | Provider attempts recorded with request identity, tiers and completeness | `commerce.provider_attempt`; `MT-02` | Retry → **a distinct row with its own supplier cost** (`ST-03`) |
| A-10 | Usage normalised into non-overlapping categories | `commerce.attempt_usage`; `§7.4`; `UQ (attempt, usage_revision, category)` | Cumulative stream → **replaces, never sums** (`UN-03`, `I-492`) |
| A-11 | Settlement once per logical request, half-even after aggregation | `commerce.customer_settlement`; `ST-01` | Write fails → idempotent per attempt usage revision, re-runs (`AI-10`) |
| A-12 | Debit and release against **the same sources the reservation held** | `ST-05`, `CD-06` | Release → capped by the burst; **cannot mint capacity** (`RF-05`) |
| A-13 | Supplier cost and customer cost recorded separately, in different units | `commerce.supplier_cost_entry` (decimal money) vs micro-credits; `I-493` | — |
| A-14 | User sees capacity, purchased credits and the funding source separately | `entitlement.getCapacity`, `commerce.explainCharge`; `AC-10`, `EC-04` | — |

**Terminal states.** Success: paid, term active, capacity reserved and settled, balance explainable. Failure: every branch either grants through reconciliation or quarantines explicitly; **no branch admits inference without a verified service term**.

---

## 3. Workflow B — exhaustion, extra credits, cancellation, expiry mid-task

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| B-01 | Capacity runs out mid-turn | Admission on the next iteration; `AI-02` | → `WaitingForCapacity` with a **server-calculated** `recoveryAt` (`EC-03`) |
| B-02 | User has purchased credits but has not opted in | `AI-03` | → `entitlement.extra_credits_required`. **No automatic purchase or paid fallback** (`AC-06`) |
| B-03 | User opts in with a maximum budget | `commerce.authoriseExtraUsage` | Budget exhausted → hard stop; no overdraft (`CR-23`) |
| B-04 | Turn parks awaiting a device tool | `PL-02`, `PL-03` | **The included-capacity hold is released at the safe boundary** and re-reserved on resume (`AC-05`, `AI-15`) |
| B-05 | User cancels mid-stream | `§6.2` of the harness; `MT-09` | Verified consumption within the ceiling settles; the remainder releases. **Completed provider work is not presumed refundable** |
| B-06 | Paid term expires while the Task is running | Term evaluation at each dispatch; `SV-06`, `AI-14` | Further dispatch stops at a **durable boundary** with the eligibility reason. Settled work stays settled |
| B-07 | Renewal grace begins | `service_term.grace_ends_at`; `SV-05`, `C-07` | **Data readable and downloadable; no new inference admitted.** The two windows are configured separately |
| B-08 | User renews | New `service_term` row; `RF-07` | Contiguous renewal **extends eligibility without refilling to full** (`AC-03`) |
| B-09 | Retained purchased credits become spendable again | `CR-05` | **Re-enabled without reissue or transfer** |
| B-10 | Refund of a purchased lot | `RefundHold` → settlement; `AI-17` | Amount frozen then zeroed. **A refund must not mint capacity above the burst** (`AC-11`) |

**Terminal states.** Every exhaustion path reaches a stated reason with a recovery action. **No path silently spends, silently waits forever, or silently converts one pool into another.**

---

## 4. Workflow C — Cloud task, device tool, native product job

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| C-01 | Turn submitted from any surface; Task is Cloud-owned | `task.create`; `TO-01` | — |
| C-02 | Model proposes a tool; it resolves to a declared capability | `MR-01`; `INotesOperations`, `ISlateOperations` | Unknown tool → typed protocol error to the model (`RC-02`) |
| C-03 | Step declares `toolLocality = device` | `TO-02` | No eligible device → `WaitingForDevice`, **never a cloud approximation** (`PL-02`) |
| C-04 | Approval required; turn suspends durably | `§5` of the harness; `task.approval` | Process exits → durable by construction |
| C-05 | Cloud writes a `ToolRequest`; **does not connect to the device** | `RA-01`, `RA-02`; **D-010** | — |
| C-06 | Desktop pulls and **re-authorises locally** | `bridge.pullRequests`; `BR-01`–`BR-03` | Local policy refuses → refusal returned; the cloud approval **does not override** |
| C-07 | Tool starts a **native Product Job** — a render | `StartRenderAsync` → `TaskRef`; `SL-04` | — |
| C-08 | The render is **not** adopted as an agent Step | `CM-04`, `AU-03`, `XA-07`; `I-485` | It invokes no model, debits no AI capacity, and ArcSlate owns its progress and recovery |
| C-09 | Result submitted, idempotent on `(taskId, attemptId)` | `BI-01` | Lost response → re-submission has one effect; crash resolved by `command_log` (`BI-02`) |
| C-10 | Cloud records the attempt; the device keeps its own `command_log` | `TO-04` | Neither writes the other's rows (`BI-03`) |
| C-11 | Turn resumes with **revalidated** context | `SI-05` | Content changed → the model is told (`SI-03`) |

**Terminal states.** Success: Cloud-owned task, device-executed tool, product-owned job, durable result. Failure: every branch reaches a stated reason; the one `unknown` (C-09) is resolved by the command log rather than assumed.

---

## 5. Workflow D — offline edit, pending journal, acknowledgement

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| D-01 | User edits a hydrated note offline | `EditTransaction`; journal + `sync_outbox` in one transaction (`PC-01`) | Crash → at most the coalescing window is lost; what survives is a valid document |
| D-02 | The edit is durable **on this device**, and is **not** presented as saved to Cloud | `PE-04`, `NO-04`; `§3.1` of the product scope | — |
| D-03 | Cache pressure occurs while the edit is pending | `PE-02` eviction gate | **Refused** — a row with an unacknowledged change is not evictable (`I-498`) |
| D-04 | Reconnect; outbox pushes with its `command_id` | `sync.pushChange` | Response lost → `unknown`; idempotent re-push (`SY-01`) |
| D-05 | Cloud acknowledges; the revision becomes authoritative | `AU-01` | — |
| D-06 | Outbox row clears **only on a confirmed ack** | `PE-02` | Crash before clearing → duplicate push recognised by revision (`SY-02`) |
| D-07 | Concurrent edit on another device raises a conflict | `sync.conflictRaised`; both branches retained | Edit-versus-delete → the delete does not silently win (`SY-06`) |
| D-08 | Resolution produces a **new revision** | `§4` of the sync architecture | — |
| D-09 | The second device converges | `GP-04` | Gap → scoped reconciliation, convergence verified (`SY-04`) |
| D-10 | The agent's context uses acknowledged revisions only | `PK-04`, `CH-04`; `I-498` | A pending edit is visible to the user, **not** to the model |

**Terminal states.** Success: converged, acknowledged, nothing lost. Failure: **no branch discards an unacknowledged change**, and the local-versus-cloud distinction is never blurred.

---

## 6. Workflow E — restriction, deletion, retention

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| E-01 | Subscription lapses; workspace enters restriction | `SV-05`; `QU-03` | Data readable and downloadable; **no data deleted to enforce a downgrade** (`SU-06`) |
| E-02 | Pending edits at the moment of restriction | `PE-03`, `C-06` | **Preserved and recoverable.** Restriction runs the same eviction gate as cache pressure |
| E-03 | User signs out or switches account | `PE-03` | Same gate. Unacknowledged work is offered for recovery or export before anything is cleared |
| E-04 | User requests account deletion | `identity.requestAccountDeletion`; grace period | In-flight commercial operations block completion until resolved (`DE-05`) |
| E-05 | Deletion runs across every store | `DE-01`, `DE-04` | Partial → retried; **confirmed only when every store reports done** |
| E-06 | Search and vector entries removed | `DE-01` | Content unreadable but findable → invariant detects and retries |
| E-07 | Financial records survive | `DL-08`, `DE-05` | **Never deleted**; retained under their own policy with identity minimised |
| E-08 | Audit records survive | `DL-07` | **Refused** by constraint |
| E-09 | Local files remain | `DL-01` of the identity requirements; `I-016` | **Correct behaviour, not a failure.** A separate explicit choice deletes local data |
| E-10 | Simulator output follows retained-data rules | `SC-07`, `SIM-19` | Retention effects on historical runs are exposed, not silent |

**Terminal states.** Success: restricted or deleted with every store confirmed. Failure: **no subsystem silently reverses another's decision** — deletion cannot remove audit or financial records, and restriction cannot discard pending work.

---

## 7. Workflow F — simulator start, host failure, native consumption

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| F-01 | User publishes an immutable scenario version | `simulation.publishScenarioVersion`; `SIM-02` | Invalid AST → **rejected before any lease, object or quota debit** (`SB-01`, `SO-09`) |
| F-02 | Run started with seed and execution profile | `simulation.startRun`; `scope.simulation_run` | No service term → refused (`SIM-17`); quota exhausted → refused before side effects |
| F-03 | A replica claims the run by lease with a fence token | `scope.simulation_lease`; `SX-03` | Two replicas contend → one wins; the other does not publish |
| F-04 | Bounded batches generate canonical data | `RT-05`, `SIM-10` | Preview overload → **preview decimates; canonical generation does not** (`SF-03`) |
| F-05 | Object written, verified, **then** the manifest row commits | `SX-01` | Crash between → object invisible, swept (`SX-06`) |
| F-06 | Checkpoint advances in the same transaction | `SX-02` | Reversed order would let a takeover skip an invisible range — which is why it is one transaction |
| F-07 | **The host is killed mid-run** | Lease expiry; `SX-04` | Another replica takes over with a higher fence token |
| F-08 | The old host attempts a late publish | `SX-03` | **Rejected on the stale token** |
| F-09 | Generation resumes from the checkpoint | `SIM-12` | **Same remaining canonical data; no duplicate, no missing range** |
| F-10 | Client lists the manifest and fetches segments | `simulation.listSegments`, `getSegmentTicket` | Hash mismatch → segment rejected (`SN-02`) |
| F-11 | Realtime is disabled entirely | `SO-05`, `RE-07`, `SIM-13` | **Polling plus manifest is a complete authoritative fallback**, not a degraded one |
| F-12 | ArcScope ingests through the normal pipeline | `SN-01` | Session, capture, decoder, measurement, report all unchanged |
| F-13 | Output is labelled synthetic through export and copy | `SC-06`; `I-496` | **Never enters a hardware-evidence path** |
| F-14 | Term expires mid-run | `SC-04`, `SIM-17` | Stops at a **durable boundary** as `canceled` with the reason; committed output follows retention rules |

**Terminal states.** Success: deterministic data, recoverable across host loss, consumable natively, labelled synthetic. Failure: every branch either fails before a side effect or commits a partial outcome honestly — **never `succeeded` for an incomplete range** (`SC-05`).

---

## 8. Workflow G — OTIO import, edit, export, independent verification

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| G-01 | User previews an import | `PreviewOtioImportAsync`; `SL-05` | **Nothing mutates.** The fidelity report is produced first |
| G-02 | Report gives item-level dispositions | `OS-01`, `OT-07` | Retained, approximated or omitted — **never a silent flatten** |
| G-03 | User accepts; import commits | `ImportOtioAsync`; `SL-06` | Malformed or oversized → rejected before commit (`OY-01`) |
| G-04 | Import creates ArcSlate-owned objects with provenance | `OA-02`; `I-497` | OTIO is **not** the working store |
| G-05 | Media references resolve under an approved base | `OY-04`, `OT-08` | Missing → relinkable Offline Media (`RelinkMediaAsync`); a path outside the roots is denied |
| G-06 | No adapter, plug-in or executable content loads | `OY-02` | The upstream adapter mechanism is exactly the path this rule closes |
| G-07 | User edits natively; rates stay exact | `OS-03`; `frame_rate_num`/`frame_rate_den` | No float column exists to drift |
| G-08 | Export binds a **committed** revision | `SL-07`, `OA-02` | Live editor state cannot be exported |
| G-09 | Temporary destination, atomic publish | `OY-05` | Failure or cancellation leaves project **and** existing destination untouched |
| G-10 | Semantic round-trip verified independently | `OR-01`, `OT-06`, `OT-12` | Compared on **timeline meaning and media references**, not bytes or internal identifiers |
| G-11 | External tooling drops private ArcSlate metadata | `OR-03` | **Core supported edits still survive** |

**Terminal states.** Success: imported, edited, exported, semantically verified by an independent library. Failure: every unsupported construct is reported at item level, and no path shifts a frame silently (`OS-04`).

---

## 9. Workflow H — configuration replacement and upgrade under load

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| H-01 | Operator edits the bundle outside the repository and image | `DC-02`, `CA-01` | Changing a price **does not rebuild the image** |
| H-02 | Validation: schema, identity, cross-references, units, currency, bounds | `DC-10`, `CF-01`–`CF-03` | Rejected **before persistence**; the active revision is untouched |
| H-03 | Environment and realm checked | `DC-04`, `CF-05` | **Production pointed at the public sample is rejected** — a sample is never silently selected |
| H-04 | Validated snapshot persisted, then activated atomically | `config.revision`; `CG-03`, `CA-03` | Exactly one active revision per realm, by unique constraint |
| H-05 | Replicas converge | `DC-11` | A replica that cannot load it **admits no affected work** — no fallback to a previous revision or a sample (`CF-04`) |
| H-06 | Requests in flight keep their pinned tariff | `CA-07`, `AC-09`; `I-494` | A new revision **cannot** lower a started Run's budget or raise its rate |
| H-07 | Usage, capacity, credits and holds are untouched | `DC-13`, `CA-06`, `AI-16` | No reset, no reissue, no release |
| H-08 | Historical charge replayed after replacing every rate | `RP-02`, `MT-14` | **Reproduces exactly** — snapshots are persisted facts, not lookups |
| H-09 | Application upgrade: expand, backfill, deploy, soak, switch | `§2.1` of the deployment architecture | Each phase has an entry check, exit check and failure action |
| H-10 | Long-running tasks survive the fleet roll | `BG-03`, `MX-03` | Task authority is in the database; a drained replica releases its lease |
| H-11 | Older clients keep working | `CM-06`, `CO-02` | Support removal is planned and communicated, **never discovered by users** |
| H-12 | Emergency suspension | `CA-08`, `DC-11` | Bounded, **authenticated**, operator-triggered; server-enforced before dispatch; **no unauthenticated reload endpoint** |

**Terminal states.** Success: new policy active, history intact, tasks and holds preserved. Failure: every branch either rejects before persistence or degrades scoped to what the gap affects (`CA-04`).

---

## 10. Findings

Seven steps failed to resolve on the first pass. All seven are closed by work in this pass.

| # | Finding | Resolution | State |
|---|---|---|---|
| **W-04** | **A-03 could not resolve.** No schema, operation or rule expressed "an active paid service term", so `C-03` — *credits alone cannot authorise AI* — was unenforceable. Nothing distinguished a credit grant from a paid term | `entitlement.service_term` added with `UQ (kind, source_ref)`; `§5.3` of the commerce architecture; `entitlement.getServiceTerm`; `entitlement.no_service_term`; `SV-01`–`SV-07` | **Closed** |
| **W-05** | **A-07 resolved to the wrong model.** The credit architecture described an allowance reissued per period and voided at period end — not a replenishing bucket. The refill arithmetic, the watermark, the fractional remainder and the burst ceiling had no design at all | `§7.2` of the commerce architecture with the algorithm; `entitlement.capacity_bucket` with the monotonic watermark and the `available ≤ max(0, burst − held)` constraint; `WP-42.11` | **Closed** |
| **W-06** | **A-10 could not resolve.** No schema recorded normalised usage, so `MT-03`'s non-overlapping categories and `MT-05`'s cumulative-stream rule had nowhere to live. Double-charging reasoning or cached tokens was not structurally prevented | The five-table metering chain; `UQ (provider_attempt_id, usage_revision, category)` as the idempotency key; `§7.4`, `§7.5`; `WP-43.07` | **Closed** |
| **W-07** | **C-08 resolved to a contradiction.** A render was reachable as an agent Step, which would have put a native job under AI metering and Cloud recovery | `CM-04` of the runtime architecture; `AU-03`; `XA-07`; `TO-05`; `I-121` and `I-485` restated | **Closed** |
| **W-08** | **D-03 could not resolve.** Nothing distinguished an evictable cache row from a durable pending edit, so cache pressure, sign-out and restriction could each have discarded unacknowledged work | `PE-01`–`PE-06` in the desktop data model as a schema constraint, not a convention; `I-498` | **Closed** |
| **W-09** | **F-06 had no specified ordering.** The simulator existed only as requirements; nothing said whether the manifest or the checkpoint commits first, which is the difference between a recoverable takeover and a silently skipped range | `§1.2` of the simulator architecture; `SX-01`, `SX-02`; the six simulator tables; `WP-51` | **Closed** |
| **W-10** | **H-04 could not resolve.** Configuration was a requirement with no owner. No module, schema or activation sequence existed, so `DC-12`'s "requests record which revision they used" was unimplementable | `§2.2` of the commerce architecture makes Configuration a top-level module; `config.revision`; `§3.1` of the deployment architecture; `CG-01`–`CG-06` | **Closed** |

| # | Rule |
|---|---|
| WF-01 | **A workflow trace is evidence only while its steps resolve.** These traces are re-run when an operation, schema or rule they cite changes. |
| WF-02 | **A step resolving to a requirement alone is a finding**, not a resolution. |
| WF-03 | **These eight are representative, not exhaustive.** They were chosen for boundary crossings, not coverage. |
| WF-04 | **The previous baseline's traces are superseded, not carried forward.** Workflows A, B and D of the earlier pass rested on a credit balance, a local harness and local-first authority — all three changed under P2-006, so re-using their results would have been false evidence. |

---

## 11. What this does and does not establish

| Establishes | Does not establish |
|---|---|
| Eight boundary-crossing workflows resolve end to end, on success and failure paths, **against the revised requirements** | That every workflow in the product family does |
| Each traced failure path reaches a stated terminal state | That the implementation will behave as specified |
| Seven real defects were found and closed | That no defects remain |
| The design layer is present where these workflows need it | That the design is complete in areas these workflows do not touch |

| # | Rule |
|---|---|
| WE-01 | **This is design-stage evidence.** It closes no implementation-stage gate, and `RS-02` of the open-gates register governs. |
| WE-02 | **Passing a trace is not passing a test.** The obligations these workflows imply are carried by the work packages each step cites — including `PG-13`, `PG-14b`, `PG-15` and `PG-16`, which require **real provider, real host and real library evidence** that no design pass can supply. |
