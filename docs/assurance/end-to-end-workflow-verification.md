# End-to-End Workflow Verification

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Produced: 2026-09-06, as part of the design-completeness pass
> Method: each step of each workflow is resolved against a named operation, schema, rule or gate. **A step that cannot be resolved is a finding**, not a narrative gap.

A specification set can satisfy every internal check and still be unimplementable, because implementability is a property of whole workflows rather than of individual documents. These traces cross the most boundaries in the system, and each is followed to a **terminal state on both the success and the failure path** — a workflow that only works when nothing goes wrong is not verified.

**Result: five workflows traced, 0 unresolved steps, 3 findings — all closed within this pass.**

---

## 1. How to read a trace

| Column | Meaning |
|---|---|
| Step | What happens |
| Resolves to | The operation, schema, or rule that specifies it. **Every cell must be resolvable** |
| Failure branch | Where the trace continues when this step fails |

A step resolving to a requirement alone is **not** sufficient — a requirement states what must be true, not how. Each step below resolves to an operation signature, a schema, or an architecture rule that specifies a mechanism.

---

## 2. Workflow A — remote agent edit from mobile

> *On a phone, a user tells the ArcChat agent to add a summary section to an ArcNotes document that lives on their desktop.* Crosses mobile, cloud, the durable bridge, the desktop, ArcNotes' editing core and sync.

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| A-01 | Mobile appends the user's message | `chat.appendMessage` ([`01-public-api-operations.md`](../architecture/contracts/01-public-api-operations.md) `§8`) | Offline → mobile outbox (`§6` of the mobile architecture) |
| A-02 | A Task is created rather than a synchronous call | `CH-01`; `EX-02` of the AI requirements | — |
| A-03 | Placement decided once as `remoteViaBridge` | `TO-02`, `TO-06` ([`00-data-model-overview.md`](../architecture/data-model/00-data-model-overview.md) `§4.1`) | No eligible device → `PL-02` of the harness: fail with a stated reason, **never degrade silently** |
| A-04 | Context assembled, permission-filtered, revision-stamped | `§4` of the [harness](../architecture/17-agent-harness.md); `PK-01`–`PK-04` | Local-only source → excluded **and the exclusion stated in the pack** (`PK-04`) |
| A-05 | Budget reserved before the model call | `§7` of the runtime architecture; `credit_reservation` ([`01-cloud-data-model.md`](../architecture/data-model/01-cloud-data-model.md)) | Insufficient → hard stop at zero (**D-020**); turn ends with a stated reason |
| A-06 | Model proposes a tool call; it resolves to a real capability | `MR-01`; `INotesOperations.ApplyBlockEditsAsync` ([`02-local-rpc-operations.md`](../architecture/contracts/02-local-rpc-operations.md) `§4`) | Unknown tool → typed protocol error returned to the model (`RC-02`) |
| A-07 | Security pipeline requires approval for a write | `§5` of the harness; `AZ-02` of the operation catalogue | — |
| A-08 | Turn suspends durably; approval record created | `AP-01`; `approval` table | Process exits → **durable by construction** (`§6.3` of the harness) |
| A-09 | User approves on the phone | `approval.decide` | Expired → tool result "approval expired"; turn continues or finishes per profile |
| A-10 | Cloud writes a durable `ToolRequest`; **does not connect to the device** | `RA-01`, `RA-02`; **D-010** | — |
| A-11 | Desktop pulls | `bridge.pullRequests` | Desktop offline → queues visibly with expiry shown (`BI-05`) |
| A-12 | **Desktop re-authorises locally** | `BR-01`–`BR-03` ([`03-realtime-and-bridge.md`](../architecture/contracts/03-realtime-and-bridge.md) `§5.2`) | Local policy refuses → `bridge.submitResult { refused, reasonCode }`; the cloud approval **does not override** (`BR-02`) |
| A-13 | Context revalidated before the write | `SI-02`, `SI-05` of the harness | Document changed → model told the content changed (`SI-03`) |
| A-14 | Edit applies as one `EditTransaction`, origin `agent` | `AE-01`, `AE-05` ([`18-editing-and-rich-content.md`](../architecture/18-editing-and-rich-content.md) `§3.4`) | Stale `ExpectedRev` → `conflict.revision_mismatch` (`NO-02`, `AE-02`), surfaced as correctable |
| A-15 | Command logged in the same transaction as the effect | `BE-02`; `command_log` ([`02-desktop-data-model.md`](../architecture/data-model/02-desktop-data-model.md) `§1.2`) | — |
| A-16 | Result submitted, idempotent on `(taskId, attemptId)` | `BI-01` | Response lost → re-submission has one effect (`BI-01`); crash mid-execution resolved by the command log (`BI-02`, `CR-01`) |
| A-17 | Edit is visibly attributed to the agent | `AE-04` | — |
| A-18 | Change enters the sync outbox | `sync_outbox`; `§3` of the sync architecture | Push response lost → **`unknown`**, resolved by idempotent re-push (`SY-01`) |
| A-19 | Mobile re-reads the task authoritatively | `task.get`; `RE-01` of the realtime contract | Realtime event missed → recoverable by re-reading (`RE-06`) |
| A-20 | Budget settled at actual usage | `§7` of the runtime architecture | Settlement write fails → idempotent per attempt, re-runs (`CR-02` of the [lifecycles](../architecture/20-cross-system-lifecycles.md)) |

**Terminal states.** Success: document edited, attributed, synced, task complete, budget settled. Failure: every branch above reaches a stated reason, and **none reaches an ambiguous state** — the one `unknown` (A-16) is resolved by the command log rather than assumed either way.

---

## 3. Workflow B — purchase then immediate use

> *A user buys a paid plan and uses a paid capability seconds later.*

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| B-01 | Intent created | `purchase.createIntent`; `purchase_intent` | Abandoned → closed by policy (`PU-04`); a later event is **reconciled, not granted** (`PE-01`) |
| B-02 | Provider checkout | `§4` of the commerce architecture | — |
| B-03 | Webhook persisted **before** processing | `EI-01`; `provider_event` | Signature invalid → recorded and rejected, quarantined (`PE-05`) |
| B-04 | Verification chain, in fixed order | `EI-05` | No matching intent → quarantined, **never granted** (`PE-09`) |
| B-05 | Order and payment written | `order`, `payment` | — |
| B-06 | Grant issued **through Entitlement's interface** | `EO-03`; `IssueGrant` | Grant write fails → **partial success**; retried from the durable order, order never rolled back (`PE-06`) |
| B-07 | `entitlement_version` bumped | `entitlement.snapshot` | Not bumped → reconciliation invariant recomputes (`PE-07`) |
| B-08 | Client hinted, then re-reads authoritatively | `entitlement.changed` → `entitlement.getSnapshot` | Event lost → converges on next read (`PE-08`) |
| B-09 | Paid capability invoked; entitlement checked at the enforcement point | `MB-05`; `QA-05` | Snapshot stale → the client re-reads before an entitlement-sensitive action (`PE-08`) |
| B-10 | Capability runs | Product operation | Commerce unavailable → **Entitlement still works** (`EO-05`, `PE-R3`) |

**Terminal states.** Success: paid, granted, used. Failure: every branch reaches either a completed grant via reconciliation or an explicit quarantine — **no branch grants access without a verified event**, and no branch leaves a paid user without access.

---

## 4. Workflow C — offline edits on two devices

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| C-01 | Both devices edit offline | `EditTransaction`; journal + outbox in one transaction (`PC-01`, `PC-02`) | Crash mid-edit → at most the coalescing window is lost, and what survives is a valid document (`PC-02`) |
| C-02 | Device A reconnects and pushes | `sync.pushChanges` | Response lost → `unknown`; idempotent re-push (`SY-01`) |
| C-03 | Device B reconnects and pushes a conflicting revision | Revision comparison (`§4` of the sync architecture) | — |
| C-04 | Conflict raised, **both branches retained** | `sync.conflictRaised`; `conflict` table | — |
| C-05 | Resolution produces a **new revision** | `§4` there; `SY-05` | Edit-versus-delete → the delete does not silently win (`SY-06`); the user decides |
| C-06 | Derived stores rebuilt | `DS-01`–`DS-07`; `PC-05` | Stale index → detected by staleness key; **losing it costs compute, never content** (`SY-10`) |
| C-07 | Undo stack rebased around the remote change | `UN-05` | Target block gone → the entry is **dropped, never retargeted** (`UN-05`) |
| C-08 | Both devices converge | `GP-04`; `WP-24.03` | Gap → scoped reconciliation, convergence verified (`SY-04`) |

**Terminal states.** Success: converged, no content lost, both branches available. Failure: every branch preserves both users' work; the only unrecoverable action is one the user takes deliberately.

---

## 5. Workflow D — budget exhausted mid-turn

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| D-01 | Turn runs; iteration 3 reserves budget | `§2` of the harness step 2 | — |
| D-02 | Reservation refused — balance insufficient | Hard stop at zero (**D-020**) | — |
| D-03 | Turn pauses and asks rather than failing | `BudgetExceeded` → *pause and request an extension* (`§15` of the runtime architecture) | — |
| D-04 | Work already done is preserved | `§6.1` of the harness — every iteration persisted before the next begins | — |
| D-05 | Prior iterations already settled | Settlement per attempt | Settlement lost → idempotent re-run (`CR-02`) |
| D-06 | User adds credit; turn resumes | `credit_lot`; resume path (`§5` of the harness) | Never resumed → the task rests in a valid state with a reason facet (`CR-03` of the harness) |
| D-07 | Context revalidated on resume | `SI-05` | Content changed → the model is told (`SI-03`) |
| D-08 | Sub-agent work shares one pool | `BG-05` of the AI requirements; `MA-03` of the harness | Parallel sub-work → **cannot collectively overdraw** (`CS-02` of the commerce architecture) |

**Terminal states.** Success: resumed and completed. Failure: paused in a valid, reason-bearing state with no charge for work not done and no loss of work already done.

---

## 6. Workflow E — a PDF that will not render

| # | Step | Resolves to | Failure branch |
|---|---|---|---|
| E-01 | User inserts a PDF attachment | `attachment` block kind, `presentation = pdfViewer` (`§2.1` of the editing architecture) | — |
| E-02 | Attachment stored by reference, integrity verified | `AT-03`; managed resource store | — |
| E-03 | Viewer requests a page raster | `DR-01` (`§2.1` of the native interop architecture) | Dependency not adopted → **`AT-05` is not met**; the surface presents a metadata card and `PG-12` stays open (`DR-05`, `PD-07`) |
| E-04 | Start-up verification confirmed the library | `LD-03` | Verification failed → feature degraded explicitly with a named reason (`LD-04`); **never a partially verified library** (`DG-02`) |
| E-05 | Malformed or hostile PDF | `UT-01`; bounded input, recursion, time | → **Metadata card with a reason**; no process instability (`PD-04`) |
| E-06 | Extracted text carries untrusted provenance | `UT-03`; `I-262`, `I-263` | Instruction embedded in the text → **data, never instruction** (`WP-11.06`) |
| E-07 | Preview never fetches a remote resource | `PV-04` | An embedded remote reference → **not fetched**; it is an exfiltration channel if it were |
| E-08 | Annotation anchored to content hash and page | `PD-06` | Attachment content changes → the anchor is **invalidated honestly**, not silently moved |

**Terminal states.** Success: viewer works, annotations anchored. Failure: every branch degrades to a stated level with a reason (`PV-03`), and the unmet capability is carried as an open gate rather than concealed.

---

## 7. Findings

Three steps failed to resolve on the first pass. All three are closed.

| # | Finding | Resolution | State |
|---|---|---|---|
| **W-01** | **A-06 could not resolve.** The model's tool call had no specified path to a real product operation: no turn loop existed, and `09-ai-and-agent-runtime-architecture.md` gave a context-assembly sketch with no mechanism. A grep for a turn loop, tool call or model loop across the architecture layer returned nothing | [`17-agent-harness.md`](../architecture/17-agent-harness.md) written, connecting a tool call to `CapabilityDescriptor`-generated declarations and thence to the product interfaces in `02-local-rpc-operations.md` | **Closed** |
| **W-02** | **A-14 could not resolve.** No document specified how an edit is applied — no content model, no transaction, no undo, no concurrent-edit behaviour | [`18-editing-and-rich-content.md`](../architecture/18-editing-and-rich-content.md) written; `WP-18.00`, `.01`, `.04`, `.05` expanded to own it | **Closed** |
| **W-03** | **B-06 resolved to a contradiction.** The commerce architecture listed `Commerce.Entitlement` and `Commerce.Quota` as Commerce sub-modules, while `MD-05` of the cloud architecture says *Commerce depends on Entitlement's grant interface, never the reverse*. Two documents disagreed about who owns the most access-critical entity in the system | Both sub-modules removed; `§2.1` added with `EO-01`–`EO-07`. `EO-05` makes the boundary testable: **removing Commerce entirely must leave Entitlement working** | **Closed** |

| # | Rule |
|---|---|
| WF-01 | **A workflow trace is evidence only while its steps resolve.** These traces are re-run when an operation, schema or rule they cite changes. |
| WF-02 | **A step resolving to a requirement alone is a finding**, not a resolution. A requirement states what must be true; a workflow needs the mechanism. |
| WF-03 | **These five are representative, not exhaustive.** They were chosen for boundary crossings, not coverage, and passing them is not a claim that every workflow is verified. |

---

## 8. What this does and does not establish

| Establishes | Does not establish |
|---|---|
| Five boundary-crossing workflows resolve end to end, on success and failure paths | That every workflow in the product family does |
| Each traced failure path reaches a stated terminal state | That the implementation will behave as specified |
| Three real defects were found and closed | That no defects remain |
| The design layer is present where these workflows need it | That the design is complete in areas these workflows do not touch |

| # | Rule |
|---|---|
| WE-01 | **This is design-stage evidence.** It closes no implementation-stage gate, and `RS-02` of the open-gates register governs. |
| WE-02 | **Passing a trace is not passing a test.** The obligations these workflows imply are carried by the work packages each step cites, and they are verified there. |
