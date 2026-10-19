# 17 — Delegated execution with verified contracts

> **ROADMAP. Proposed.** This chapter records a proposed long-term direction. Nothing in it is release-1 behaviour, a delivered capability, a contract, a requirement, a state machine or a task. Release 1 is unchanged, and UNCONFINED stays every origin's default. The principles are accepted in [AD-0017](../decisions/AD-0017-delegated-execution-direction.md); everything else here is a **proposed** model, and each of its elements is accepted by an ADR amendment only when the first roadmap row that needs it is promoted.

- **Principles:** [AD-0017](../decisions/AD-0017-delegated-execution-direction.md).
- **Roadmap rows:** RM-15 (accepted) and EX-07 … EX-23 (exploratory), with changes to RM-02, RM-04, RM-05, RM-12, RM-13, EX-01 and EX-03 … EX-06, in [`roadmap.md` in ArcForges/Plan](https://github.com/ArcForges/Plan/blob/main/roadmap.md).
- **Evidence:** the [research record](../research/2026-10-18-delegated-execution/README.md) of 2026-10-18: facts by their ID `D-<file>-<n>`, labs by their ID and gate in its [lab register](../research/2026-10-18-delegated-execution/lab-register.md).

## 1. Status and conventions

### 1.1 What this chapter records

- **The proposed model** (§2–§12): the five concepts and their state sketches, the guarantee model (dimensions, strengths, `holds_against` rules, `api_status` promotion), the threat scope per tier with the future boundaries B7–B10 and threat rows T-28 … T-42, the platform strategies, lifecycle, policy and identity (with the inheritance rules R1–R7), channels, the technical strategy, privacy, compatibility and the illustrative contract sketch.
- **Validation** (§13): the labs, venues and the owner's lab decisions.
- **The fourteen fields per roadmap row** (§14), as the request asks for each validated capability: each capability's own internal stages and its own invest-or-reject conditions, linked to its row by ID. There is **no cross-row stage diagram**: cross-row order is stated only in the rows' Prerequisites cells, and "Revisit when" is each row's single trigger.
- **Amendment texts recorded here** (§15), with their effective clauses.
- **Rejected and deferred alternatives** (§16), so that later work does not repeat the investigation.
- **The owner decisions required** (§17), each with the date it was asked and, once given, the owner's words verbatim.
- **The mapping of the request's four categories** (§18).

**Not recorded here:** the study's review history, which stays in its working files; release-1 behaviour, which the other chapters state.

**Evidence rule.** No lab of the research record has run. Every value this chapter states for a capability that is not delivered is an **attainable**, pre-lab value with its gaps and the lab that decides it, never a realized ENFORCED; delivered values are marked as delivered. Every new ArcForges capability is at most **E4** until its lab has run, and a composite takes the weakest evidence among its parts. "Can enforce (probed)" is the only way an attainable value is shown to a user (§3.2). Limitations are stated at documentation level; no attack or escape technique is described.

### 1.2 Citation convention

- **Roadmap-level assumptions cite LAB IDs and the row ID, never A or F IDs, until promotion creates owner tasks.** A and F entries of the [verification register](../verification/platform-capabilities.md) need owner tasks, and roadmap rows have none until a row is promoted. When a row is promoted, the facts it then relies on enter the register under its own rules.
- **Facts of the research record** are cited by their ID, for example D-x-agents-1 (file `evidence/x-agents.md`). Where a record row carries a review correction, the corrected statement governs, and this chapter uses it.
- **Release-1 facts** keep their verification IDs (V, L, A, F).
- **No identifier is created for future work:** no requirement, state-machine, verification or task ID. The installation lifecycle is called "installation lifecycle (sketch)". Future work is named by roadmap row ID and lab ID only.
- **First-party code** is cited by repository path and commit, for example `src/ArcForges.Node.Platform/ExecutionPlatform.cs` in ArcForges/ArcForges at `b22d2ec`.

### 1.3 Evidence labels and vocabulary

| Term | Meaning |
|---|---|
| **E1 … E6** | Evidence labels: E1 demonstrated in ArcForges; E2 officially supported and documented by the OS vendor or specification owner; E3 demonstrated by a mature third-party project; E4 technically feasible, but needs a prototype or a lab run; E5 speculative, with significant unknowns; E6 impractical, unsafe, redundant or inappropriate. **E1-DP**: first-party code in DesktopPlatform, outside the node, that sets a precedent |
| **DELIVERED, SPECIFIED, PLANNED** | Status of an ArcForges part: merged and verified; designed in this Design but not built; scheduled as a release-1 task |
| **A1 … A6** | Adversary classes: A1 accidental damage; A2 an over-privileged honest tool; A3 a compromised tool or MCP server, hostile within its granted channels; A4 an untrusted AI-generated command; A5 deliberately evasive software that targets the isolation mechanism; A6 a privileged installer or system-level software |
| **P0 … P3** | Privilege levels: P0 standard user at run time; P1 a one-time administrator or root setup step; P2 elevation per operation; P3 a vendor entitlement, signing requirement or driver |
| **Capability classes** | LIFECYCLE, CONTAINMENT, SANDBOX, VIRTUALIZATION, STRONG, OBSERVATION, SUPPLY, POLICY, IDENTITY/IPC: design vocabulary only, never a runtime field (§3.1) |
| **OWNED, DELEGATED, OBSERVED, EXCLUDED** | Lifecycle levels: ArcForges placed it and can remove exactly what it wrote; another manager owns install, update and removal; installed outside ArcForges and only inventoried; not supported, with the reason. The **method** is a separate field inside the level (§6.1) |
| **Target classes 1 … 6** | Compatibility order: 1 stdio MCP servers; 2 headless developer CLIs and build steps; 3 AI-generated commands routed by agents; 4 AI agent CLIs as confined attempts; 5 background AI tools and inference servers; 6 portable GUI applications (§11.1) |
| **The 80/60 rule** | Per class and OS: at least 80 % running with adapter-derived grants may become a default; 60–80 % opt-in per installation; below 60 % reported available but not recommended (§11.2) |
| **D0 … D4** | Data classes of [01](01-system-overview.md) §4: D0 public; D1 operational summary; D2 sensitive execution detail (command lines, paths, destinations); D3 secrets; D4 workspace content |
| **Owner decisions D1 … D5** | The owner's lab decisions (§13.3). Where a sentence could be read either way, they are written "owner decision D1" |
| **LAB-WIN-nn, LAB-LNX-nn, LAB-MAC-nn, LAB-X-nn; G01 … G41** | Entries of the [lab register](../research/2026-10-18-delegated-execution/lab-register.md) and the decision gates they feed |

### 1.4 Terms

Existing ArcForges terms keep their Design meaning: task, attempt, container (Windows job or Linux transient unit), holder (`exec-wrap`), guard, capability report, policy document, approval, origin (HUMAN, AGENT, SCRIPT, PEER and the others of [11](11-security-privacy.md) §1), `ActorRef`, finding, two-phase cleanup, managed root, managed worktree, and the `SERVICE` and `COMMAND` task kinds. The terms below are proposed.

| Term | Meaning |
|---|---|
| **Concept** | A new persistent entity, a new state machine, or a new contract service or message family (AD-0017, principle 8). Roles of the one binary, enum values and record kinds inside an existing family are not concepts |
| **Dimension** | An access area a grant or a resource request can target on at least one OS: `fs.read`, `fs.write`, `config` (Windows only: registry key classes), `net.out`, `net.in`, `ipc`, `devices` (with `devices.gpu`), `creds`, `persist`, `exec` (with `exec.elevation` = REACHABLE or BLOCKED), `visibility` (reported, not grantable, on Windows), `res`. `res` is the one dimension targeted by resource requests (task limits, envelope budgets) rather than by a grant kind. On Linux and macOS configuration is files, so it is `fs` (§3.2) |
| **Strength** | ENFORCED, MEDIATED, PARTIAL, GUARDRAIL, OBSERVED, NONE (UNAVAILABLE is NONE with a reason), N/A, ordered for `meet` (§3.2) |
| **Attainable value** | Per host and backend, from the start-up probe, with a probe reference. Used at PLAN; shown as "can enforce (probed)"; never printed as ENFORCED |
| **Realized value** | Per attempt, from that attempt's read-back. Used at VERIFY and in records, approvals, exports and remote views |
| **Read-back** | Per backend, the mechanism's configuration verified for this attempt. On Windows a stated composite (§5.1) |
| **Basis** | The facts behind a value: backend, `api_status`, OS build, component version and fix status, ABI, probe reference and time, hardening, platform facts, `ui_isolation`, evidence label |
| **Gap; gap class** | A documented shortfall of a value, listed in `gaps[]`. Class *escape* means a reachable launcher of unconfined work: on Windows WMI, Task Scheduler, COM activation of launch-capable servers and WSL interop; on Linux the session bus, the systemd private socket, the user-wide node endpoint, a reachable display server or any abstract-addressed session service that can start work; on macOS an allowed launch- or write-brokering Mach service. **A launcher cell not measured on the host's build class counts as an escape gap until its lab denies it. An escape gap is a property of the realization**: it caps every dimension of that realization (§3.2). Class *partial* is every other gap |
| **`holds_against`** | The adversary classes a value holds against, computed by fixed rules (§3.2) |
| **Implicit grant** | Access a backend gives without an ArcForges grant: AppContainer profile storage, the probe-found ALL APPLICATION PACKAGES (AAP) and ALL RESTRICTED APPLICATION PACKAGES (ARAP) writable paths, the view's tmp, the private HOME |
| **AAP, ARAP** | The Windows group SIDs whose ACEs AppContainer and LPAC (Less Privileged AppContainer) processes match |
| **`api_status`** | DOCUMENTED, DEPRECATED, EXPERIMENTAL, UNDOCUMENTED, PREVIEW (§3.3) |
| **REQUIRED, PREFERRED, `min_strength`** | Per grant: a REQUIRED dimension that cannot be met refuses the task; a PREFERRED shortfall is recorded and shown. `min_strength` is the lowest strength that satisfies a REQUIRED dimension (§3.4) |
| **CONFINED, UNCONFINED profile** | A profile with an intent. CONFINED denies everything not granted; UNCONFINED carries no grants and is today's behaviour, every access dimension NONE (same-user tier) |
| **`meet`** | The effective requirement: the strongest of the requested, caller, HUMAN-set client, client-declared, origin, installation and envelope floors, requirement fields included (§3.4) |
| **Canonical summary** | The one node-computed projection of a realization that every surface renders (§3.5) |
| **Exposure statement** | A node-computed sentence across dimensions, for example "exfiltration possible to <scope>" when a `creds` or `fs.read` scope meets a `net.out` that is not ENFORCED-deny (§3.5) |
| **`ui_isolation`** | A reported basis fact of a realization, not a dimension: separate desktop measured, separate desktop not measured, shared, no display (§8.5) |
| **Policy filter; surface hardening** | A seccomp rule that implements a denied grant counts toward its dimension (policy filter). Syscall-surface reduction against kernel bugs is basis only (surface hardening) |
| **`identity_strength`** | How strongly the node knows which attempt called: ENFORCED, PARTIAL, GUARDRAIL, RACY, ASSERTED, with a basis like a strength (§7.2) |
| **`provenance_strength`** | How strongly the node knows who authored a policy revision or decided an approval: ASSERTED, GUARDRAIL or ATTESTED (§7.2) |
| **Helper role; helper-role profile** | A role of the one `arcforges` binary that parses hostile input or mediates a channel; the profile it must run under: deny-all except passed descriptors, network denied (egress only for the proxy), no bus. Where it cannot be realized ENFORCED for `fs`, `net` and `ipc`, the method is UNAVAILABLE (§4.3) |
| **Attempt endpoint** | The per-attempt bundle of node-served endpoints (node API S5', sccache server S2', cache store S3', brokers, relay), created at launch, recorded as owned objects, closed at the end (§2.2, §8.3) |
| **SR-1 … SR-5** | Service-reach rules: SR-1 isolation wins over cache; SR-2 one per-attempt bundle; SR-3 identity from the endpoint; SR-4 a token is a scope, not a boundary; SR-5 adapters configure only reachable services |
| **R1 … R7** | Inheritance rules: R1 identity only from OS-attested facts; R2 floor `meet(requested, profile(A))`, grants a subset of A's, charged to A; R3 unknown foreign confinement fails closed; R4 every node endpoint; R5 widening is human and recorded (local HUMAN only until EX-23); R6 never HUMAN from inside an attempt; R7 ENFORCED only where identity is ENFORCED (§7.2) |
| **TP-1 … TP-8** | Cache-trust rules: TP-1 write own only; TP-2 read own plus more trusted; TP-3 partitions orthogonal to compatibility keys; TP-4 the node the only writer of trusted stores; TP-5 per-partition quota; TP-6 guests never write back; TP-7 promotion only for content-verifiable entries; TP-8 read grants are `fs.read` and private (§8.6) |
| **Delegation envelope** | A policy record keyed by session: grants, expiry, workspace, action budgets and a resource budget (§7.3) |
| **Group container** | An optional third container level that realizes an envelope's resource budget where three-level containers are proven (§7.3) |
| **Action budget** | Per session: approvals requested per hour, grant widenings, distinct N1 destinations, acquisitions. Exhaustion pauses submission and notifies; it never auto-approves (§7.3) |
| **Shared-SERVICE rule** | A SERVICE launched for a session inherits that session's envelope as a floor and is revoked when it closes; a SERVICE shared by several sessions never gets more than the meet of its users' envelopes and is revoked for each user as that user's envelope closes (§2.3) |
| **Host-write journal** | One record of every host change ArcForges makes, with its prior state; writer kinds `INTEGRATION`, `SELF_INSTALL`, `INSTALLATION`, `CONFINEMENT_OBJECT`, `PERSISTENCE_HOLD` (§6.3) |
| **Owned object** | An OS object ArcForges created and must remove exactly: an AppContainer profile, an ACE, a desktop, a transient unit, a slice |
| **Protected control set** | `ValidatePolicy` rules: no profile may deny the node endpoint to HUMAN clients; and a profile for an AI client that ArcForges launches as a confined attempt may not deny that client the grants of its own configuration, state and credential that the always-forbidden set's grantee-relative exception allows, unless explicitly flagged (§7.1) |
| **Confirm-or-revert** | A policy revision that tightens running SERVICE workloads, or an AI client ArcForges launches, applies with a deadline; without HUMAN confirmation the previous revision is restored |
| **Safe start** | `node run --safe`: the node starts with no isolation profile applied, so the owner can restore a revision |
| **Lock-out rules** | The protected control set, confirm-or-revert and safe start together |
| **Always-forbidden set** | Paths no grant to any attempt may include, with one grantee-relative exception: an AI client's own configuration, state and credential, granted to that client's own confined attempt by a recorded HUMAN approval, never to its tools or MCP servers (§7.1) |
| **Workspace provenance** | The granted-directory diff recording which attempt and profile digest wrote each file (§7.1) |
| **HUMAN-only local surface** | A node surface whose values are returned only to local callers of HUMAN origin: never to AGENT or SCRIPT callers, never through the MCP adapter or the relay, and left out of support bundles unless the owner includes them. Origins are guardrails ([11](11-security-privacy.md) §1), so this keeps D2 host facts out of AI clients and model context; it does not stop same-user code that forges HUMAN |
| **Terminal-attached attempt mode** | A proposed attempt mode in which the holder or `exec-init` owns a pseudo-terminal relayed to the owner's terminal, with the terminal-injection filter kept; needed before an interactive AI client can run as a confined attempt (§7.2). A mode of the existing attempt, not a new concept |
| **Weakest-run rule** | An uninstall may say "nothing outside the recorded grants" only if every run of the installation was a verified confined attempt, under per-OS conditions; otherwise `ran_unconfined = true` (§6.6) |
| **Three-part uninstall result** | Removed; left in place; not known (§6.6) |
| **Ephemeral-state, persistent-state profile** | Linux view profiles without, or with, a workload-writable bind source that persists across attempts (§5.2) |
| **Acquisition attempt; O1 … O4** | The attempt that resolves, fetches and verifies software under its own profile; the acquisition stages O1 observe, O2 pin, O3 owned tool store, O4 split acquisition and run profiles (§6.2) |
| **`update_owner`** | The one recorded owner of updates per Installation: ARCFORGES, MANAGER or VENDOR (§6.4) |
| **Revocation classes** | IMMEDIATE, NEW_ACCESS_ONLY, RESTART_REQUIRED, UNREVOCABLE (§7.4) |
| **MOTW; quarantine** | Mark-of-the-Web, the Windows zone-of-origin mark; `com.apple.quarantine`, its macOS analogue (§6.2) |
| **Backends** | Windows W0 (today's jobs), W2 (a hand-built AppContainer brokered by the holder), W3 (LPAC); Linux L0 (today's transient unit), the view chain, the Landlock-only tier, N0 (no network), N1 (an `lo`-only network namespace plus a mediated proxy); macOS stage 1 (monitored) and Seatbelt; STRONG backends (VM-class, separate kernel or account), each accounted as one `GUEST_VM` consumer (§5) |
| **View chain** | unit → `exec-launch` → the distribution's `bwrap` (the only mount-namespace owner) → `exec-init` (PID 1) → `exec-final` (no-new-privileges, Landlock at the probed ABI, seccomp policy filters) → workload (§5.2) |
| **Lease invariant** | A Windows AppContainer SID is re-leased only after every ACE for it is removed, its storage is reset and no process with its token is alive; after a node crash it is quarantined (§5.1) |
| **Composite first-backend rule** | The six conditions under which Windows goes first; otherwise Linux goes first (§13.2; gate G40) |
| **Editions check** | No local default may require a remote decision; the local queue, the envelope and confirm-or-revert must on their own make every local default usable (§7.6) |
| **Never-remote list** | Decisions never made remotely: accepting a deprecated or experimental basis or a downgrade; editing profiles, templates or the protected control set; adding an external path; running `recover`; trusting a new backend; any macOS confined widening (§5.4) |
| **"Accepted as RM and promoted together with"** | The cross-row phrase of the roadmap's Prerequisites cells: each named row is first accepted as RM by a recorded product-owner decision, and the rows are then promoted in one change. An EX row is never promoted itself |
| **The pair-1 corrections** | The corrections of 2026-10-19 to today's Design (threat rows T-22 … T-27 and the amended T-11, boundaries B0 and B11, the release coverage statement's stated limits); they describe release 1 and are in force |

## 2. Concepts and state (proposed)

### 2.1 Design rules

The definition of "concept" and the design rules M1–M5 are accepted principles ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 8): one execution lifecycle (M1); a dimension only where a grant or a resource request can target it (M2); lifecycle and isolation as independent facts (M3); the node as the only writer (M4); no new concept, and no new theme, without two uses (M5).

**The couplings M3 allows** are one-directional and recorded:
- an Installation's default profile;
- the installation floor in the admission `meet` (§3.4);
- split acquisition and run profiles (O4, §6.2);
- the owned-state snapshot taken when a profile marks a state root owned (§6.5);
- the `state_root:<installation>` grant class (§7.1).

The only other link is the weakest-run rule (§6.6): isolation facts can let an uninstall say more, never raise a lifecycle level.

**The mission-level rule** ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 9) has a resource-side payoff: a read-confined attempt has a verified input set, which is what RM-04's restore needs (§11.2).

### 2.2 Five concepts, each with two uses

| Concept | What it is | Uses (at least two) | Enters with |
|---|---|---|---|
| **Realization** (message family) | Per backend and dimension the *attainable* value; per attempt and dimension the *realized* value: `(dimension, policy, strength, holds_against, basis, gaps, implicit grants, reason)`, plus exposure statements and the canonical summary (§3) | Capability report; attempt record; `ExplainTask`; `GetReleaseScope`; the remote D1 summary; the residue rule (§6.6) | EX-07 stage a (every access value NONE) |
| **Access profile with typed grants** (entity; includes the grant lifecycle on a running attempt) | A named, revisioned set of typed grants inside `PolicyDocument`, with REQUIRED or PREFERRED per grant and an intent, CONFINED; UNCONFINED profiles carry **no grants**. Grant kinds: `fs`, `config` (Windows registry key classes), `net`, `ipc`, `devices`, `creds`, `persist`, `exec`, `visibility` (where a backend can withhold it), each with expiry, source `ActorRef` and approval ID | Confined commands and services; acquisition attempts (O4); inheritance floors; credential delivery; cache read grants (TP-8); LAN placement feasibility | EX-07 stage b, with the first confined backend |
| **Installation** (entity; includes the installation lifecycle (sketch), `InstallationService` and the acquisition record) | Software ArcForges records: lifecycle level (OWNED, DELEGATED, OBSERVED, EXCLUDED), method, `update_owner`, versions with acquisition records, state roots, journal references. Generalizes `install_source` ([AD-0012](../decisions/AD-0012-distribution-and-updates.md) §4) | ArcForges' own install; OWNED tools; DELEGATED reporting; version rollback; residue statements; MCP digest pins | EX-13 stage b |
| **Delegation envelope** (entity; includes its lifecycle) | A policy record keyed by session: grants, expiry, workspace, action budgets, and a resource budget realized by admission or, where proven, by a group container (§7.3) | One-operation revocation; action budgets; session worktrees (EX-16); agent introspection; the AI client as a confined SERVICE attempt | EX-14 |
| **Attempt endpoint** (entity: an owned-object bundle) | The per-attempt bundle of node-served endpoints, created at launch, closed at the end; the confined attempt's only route to ArcForges and the source of its OS-attested identity (SR-2, SR-3) | Node API from a confined attempt; identity; cache reach; credential brokers; network relay | EX-09 |

**Extensions of existing primitives** (not concepts by the definition, each with two uses):
- **Host-write journal:** `integration_write` (AF-AI-02, SPECIFIED) with writer kinds `INTEGRATION`, `SELF_INSTALL`, `INSTALLATION`, `CONFINEMENT_OBJECT`, `PERSISTENCE_HOLD`. Uses: integrations, ArcForges' own uninstall, installations, confinement objects, holds, owner-prompted privileged steps (AD-0017, boundary 2).
- **`ActorRef` fields:** `calling_attempt_id`, `caller_profile_digest`, `os_principal`, `identity_strength` with its basis. Uses: inheritance (R1, R7); `ExplainPermission`.
- **`provenance_strength`** on policy revisions and approval decisions. Uses: the A4 rule (§3.2); approval review (§7.3).
- **A group container level** between root and attempt containers. Uses: envelope budgets; WSL guest grants.
- **Adoption kinds** (persistence holds, Flatpak scopes), **finding kinds** and **record kinds** (persistence diff, workspace provenance, granted-directory diff).

**Deliberately not concepts:**
- helper roles: roles of the one binary ([AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §1);
- the vocabularies of strengths, `api_status`, revocation classes, `update_owner` and writer kinds: enum fields inside the families above;
- the protected control set: `ValidatePolicy` rules;
- "application": an Installation plus its default profile and state root (the APPLICATION group kind is dropped until it has a second use);
- "execution environment": a derived view (§2.4);
- "sandbox": a realized profile;
- "tier": a backend name, which is a basis attribute.

### 2.3 Relationships and state sketches

```
PolicyDocument (revisioned; DELIVERED store)
  ├─ AccessProfile* ── Grant*            (provenance_strength per revision)
  └─ DelegationEnvelope* (keyed by session: grants, expiry, workspace, action budgets, resource budget)
Installation* ── default_profile; versions* (acquisition record, digest, provenance)
   └─ launches as ─► Task (COMMAND | SERVICE) ─► Attempt ─► container (job / transient unit)
                         │ profile_ref, envelope_ref        ├─ group container (optional, where proven)
                         │                                  ├─ AttemptEndpoint (node API, cache, brokers, relay)
                         │                                  └─ Realization (attainable at PLAN; realized at VERIFY)
Records / findings / audit ◄── host-write journal ──► two-phase cleanup (quarantine)
```

**Attempt (SM-ATTEMPT, DELIVERED; a proposed amendment, recorded in this chapter only).** PLAN happens once, **at admission**, against attainable values. APPLY and VERIFY:
- **Windows:** inside STARTING, before the suspended process is resumed. A VERIFY mismatch ends the attempt `SPAWN_FAILED` before any workload instruction runs.
- **Linux view chain:** today STARTING → RUNNING happens at "unit job done", before bwrap, `exec-init` and `exec-final` run. Proposed: for view attempts RUNNING begins at the workload line, reported by `exec-final` through the durable realization record, as launch-step failures are today; a VERIFY mismatch ends the attempt `SPAWN_FAILED` before the workload's `execve`. The alternative, a sub-state, is decided at EX-11's promotion. No `machines.json` change is made before promotion.
- **macOS (EX-22 only):** `sandbox-exec -p <profile> arcforges exec-final -- <workload>`; the in-profile self-check gives PARTIAL ("self-check passed"), never ENFORCED.

**Installation lifecycle (sketch).** For OWNED installations: REQUESTED → ACQUIRING (an acquisition attempt) → VERIFIED → STAGED (a read-only version directory) → ACTIVE. An update stages a new version, then switch, health check, and either ACTIVE or ROLLED_BACK. Removal goes REMOVING (two-phase plan and approval) → QUARANTINED (24 h; D3 material excluded, §10) → REMOVED. Any state can go to FAILED with a residue statement. DELEGATED installations run RECORDED → ACTIVE → REMOVED_BY_MANAGER; OBSERVED ones SEEN → GONE.

**Access profile.** Profiles are `PolicyDocument` revisions; no new state machine. Confirm-or-revert is a revision plus an approval TTL whose expiry runs `RestorePolicyRevision` (D-persistence-observation-recovery-26).

**Grant on a running attempt.** ACTIVE → REVOKED_PENDING(class) → GONE, with the revocation class of §7.4. After a RESTART_REQUIRED revocation the attempt is marked `grant_stale`, never "revoked".

**Delegation envelope.** OPEN → DRAINING → CLOSED. Closing revokes the envelope's grants and brokered channels, closes its attempt endpoints, and releases its group container where one was realized. **Shared-SERVICE rule:** a SERVICE launched for a session inherits that session's envelope as a floor and is revoked when the envelope closes; a SERVICE shared by several sessions never gets more than the meet of its users' envelopes, and is revoked for each user as that user's envelope closes.

### 2.4 What is deliberately not unified

The request asks for the relationships between four things that look alike (request §6). They have different success criteria, so they stay separate:

| | Managed installer run | Sandboxed process | Resource-controlled task | Isolated execution environment |
|---|---|---|---|---|
| **Is** | An acquisition attempt of an Installation | An attempt with a CONFINED profile, realized and verified | An attempt with the UNCONFINED profile (today's behaviour) | **Not an entity.** A derived view: profile digest + pinned installation versions + workspace + environment snapshot |
| **Lifecycle owner** | Installation lifecycle (outcome) + SM-ATTEMPT (run) | SM-ATTEMPT | SM-ATTEMPT | None; its parts have owners |
| **Produces** | Staged files, an acquisition record, journal entries | Output, records, realization | Output, records | A reproducibility key: the result-cache action key extended with installation versions and the grant-set digest |
| **Security claim** | The acquisition profile's realization only; the installed artifact gets **no** claim | Per dimension, as realized | `res` only; every access dimension NONE | None of its own |
| **Rollback** | Version pointer (OWNED) | n/a | n/a | Re-run with the same key; data only from owned snapshots (EX-16 stage b) |

STRONG backends (Windows Sandbox, rootless Podman, Apple `container`) are **backends of an attempt**, each accounted as one `GUEST_VM` consumer as with WSL ([AD-0005](../decisions/AD-0005-resource-enforcement.md), WSL2 model). Their guarantees follow each backend's own row (§4.1). They are not persistent environments ArcForges manages.

### 2.5 Mapping onto existing primitives

| Existing primitive (status) | Role | Change (proposed) |
|---|---|---|
| Task and attempt (DELIVERED) | The only execution unit | `TaskSpec.profile_ref`, `envelope_ref`, `installation_ref`; attempt realization |
| Execution-platform seam `IExecutionPlatform` + `IAttemptHandle` (DELIVERED) | Backend selection, realization and read-back | §2.5.1 |
| Container: job or transient unit (DELIVERED) | Resources and lifetime; the parent of every confinement | An optional group level between root and attempt (LAB-WIN-02, with the two-to-three-level runtime transition; LAB-LNX-13) |
| Holder `exec-wrap` (DELIVERED) | Windows broker: creates the AppContainer child suspended, holds the handle list, reads back | A new launch mode, no new binary. `kill_with_node` tasks have no holder, so CONFINED with `kill_with_node` is refused until defined |
| Transient unit + `exec-launch` (DELIVERED) | Linux owner of ordering and descriptors | Two new roles of the one binary, `exec-init` and `exec-final`, plus the delivered-behaviour changes of §2.5.1 |
| Capability report + `require_enforcement` (DELIVERED) | Per backend and dimension, attainable values with basis; refusal generalized | Additive entries and codes. **Isolation, observation and lifecycle entries never change SM-NODE**, as `io` does not today (`NodeCapabilities.FullyEnforced`) |
| Policy document + revisions (store DELIVERED) | Profiles, envelopes, `provenance_strength` | Additive messages |
| Permission matrix (PLANNED, AF-SEC-01) | "Who may change grants" | New operation rows only; stays separate from grants |
| Approvals (PLANNED) | Widening, install, uninstall, hold | New approval kinds; widening and install decisions local-only until EX-23 (§7.5) |
| Audit log (schema DELIVERED) | Grant changes, installs, holds | New operation names |
| Records, findings, doctor (PLANNED) | Realizations in timelines; new findings; the probe as a self-test | Additive kinds |
| Managed roots, two-phase cleanup (PLANNED, AF-STOR-01) | Installation versions, state roots, cache partitions, owned OS objects | New owner kinds |
| Worktrees with archive and restore (SPECIFIED, AF-WS-01; L-19) | Session worktrees and reviewable writes | EX-16, no new concept |
| Update switch, SM-UPDATE (PLANNED, AF-DIST-02); signed release manifest ([AD-0012](../decisions/AD-0012-distribution-and-updates.md) §3) | OWNED version switch and rollback; probe reference data such as bwrap fix lists, carried as signed data | Reused |
| `integration_write` (PLANNED, AF-AI-02) | The host-write journal | Generalized writer kinds |
| Adoption (PLANNED) | Persistence holds; Flatpak scopes | New adoption kinds, HUMAN only |
| `SERVICE` tasks (PLANNED) | MCP servers, inference servers, background AI tools, later the AI client | — |
| `ActorRef`, origins (interim DELIVERED) | Calling attempt, profile digest, identity strength | Additive |
| Sealed task secrets (DELIVERED) | The first credential delivery mode | A `delivery` field |
| CAS, compatibility keys (PLANNED) | Acquired artifacts by digest; cache partition key | — |
| LocalRpc resolver (DesktopPlatform, DELIVERED) | Token facts from the process handle; the pidfd ladder; the macOS audit token; **dynamic per-attempt listeners with per-listener access rules** | Changes in DesktopPlatform, consumed by the node: a cross-repository prerequisite of EX-09 ([AD-0013](../decisions/AD-0013-reuse-and-supersession.md)) |

#### 2.5.1 The execution-platform seam

The delivered code (`src/ArcForges.Node.Platform/ExecutionPlatform.cs` in ArcForges/ArcForges at `b22d2ec`) shows what must change:
- `IExecutionPlatform.Evaluate()` returns one `CapabilityReport` per node (line 324). It would return per-backend entries with attainable values.
- `AttemptLaunch` has no isolation plan. It would gain an `IsolationPlan`: backend, manifest, required fields, implicit grants.
- `IAttemptHandle` exposes `TryReadExit()` and `TryReadLaunchFailure()` (lines 258, 261) and nothing for a realization. It would gain `TryReadRealization()`, backed by a durable realization record that the holder (Windows) or `exec-init` and `exec-final` (Linux) write.
- `Reopen()` (line 340) does not know a backend. The backend an attempt used would be recorded and read back on reopen.

**Delivered Linux behaviour that the view chain changes** (AF-EXEC-02's area):
- `exec-launch` gains memfd argv, `CLOSE_RANGE_CLOEXEC` and `SIG_IGN` for stop signals;
- end steps move from `ExecStop=` (`ExecStopRole`) into the view, before the main PID exits;
- the `exit-record` precedence gains `view.jsonl`;
- the cancel grace counts from the workload line;
- the view binds `tmp/<attempt>/` and never mounts a tmpfs at `/tmp`, so the disk-monitored tmp limit does not become a memory charge against `MemoryMax` (L-25).

The E1 tests to re-run under the chain are L-13, L-24 and L-25. macOS would be the seam's third implementation (RM-15). The eight-interface list of [AD-0002](../decisions/AD-0002-platform-scope.md) is not what the code implements; AD-0002's dated revision of 2026-10-19 replaces it with the delivered seam.

#### 2.5.2 Where attempt-resident roles run, and node restart

Restart survival is delivered ([AD-0006](../decisions/AD-0006-execution-semantics.md) §2; L-13, L-14). **Constraint:** a mediated channel either survives a node restart, or the attempt's realization degrades visibly (the channel moves to `unenforced_dimensions` and the canonical summary changes). The topology below is a candidate, decided at promotion:

| Role | Candidate host process | Its sandbox | Owner of record | Across a node restart |
|---|---|---|---|---|
| `exec-init` (Linux) | Inside the view, PID 1 of the attempt | The attempt's view | The attempt's unit | Survives with the unit |
| `exec-final` (Linux; macOS in EX-22) | Inside the view, replaced by the workload | The attempt's profile | — | n/a |
| Holder `exec-wrap` (Windows) | The delivered holder in the attempt job | An unconfined broker that parses no hostile input | The attempt | Survives (L-14) |
| sccache server S2' | Inside the attempt, same profile (compile-time code runs in it) | The attempt's | The attempt | Survives with the attempt |
| Linux TCP-to-UDS relay | Inside the attempt's network namespace | The attempt's | The attempt | Survives with the attempt |
| Node API S5', cache store S3' | The node, one dynamic listener per attempt | — | The node | Does not survive. Linux endpoints are **bound by directory**, so the restarted node re-creates the socket; Windows pipes are re-created by name; the realization shows the gap until the endpoint is back |
| N1 proxy; credential brokers | A separate helper process per attempt or per profile, in its own transient unit or job | The helper-role profile: egress only for the proxy, no network for brokers, no workspace, no `creds` beyond the brokered item | The attempt | Survives in its own unit or job, or degrades visibly |
| Extractor; installer inspection | An acquisition attempt | The helper-role profile | The acquisition attempt | n/a |

**Candidate:** one cross-OS attempt-holder contract (`exec-wrap` on Windows, `exec-init` on Linux) behind RM-14's narrow command-line contract, hosting the attempt-resident roles. It is one concept rather than two, and it gives RM-14 one measured trigger. **Prerequisites:** DesktopPlatform dynamic per-attempt listeners ([AD-0013](../decisions/AD-0013-reuse-and-supersession.md)); the node-restart legs of LAB-LNX-21 and LAB-WIN-09.

## 3. The guarantee model (proposed)

The no-silent-fallback rule (require → refuse) is an accepted principle ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 4). The vocabulary below (dimensions, strengths, `holds_against` rules, `api_status` promotion) is the proposed model.

### 3.1 Classes are design vocabulary only

The nine capability classes (§1.3) describe mechanisms in decisions and tables. **They are never a runtime field.** At run time a surface shows dimensions and strengths through the canonical summary, never a class bit or a tier number.
- VIRTUALIZATION is never reported as a strength. Redirection such as MSIX write virtualization or an overlay upper is a lifecycle fact of an Installation: "redirected writes removable at uninstall: yes / no / unknown".
- CONTAINMENT carries its adversary qualifier (§3.2).

### 3.2 The reported value

**Two quantities, never confused.**
- **Attainable:** per host and backend, from the probe, with `probe_ref`. It is used at PLAN and shown in the capability report and `GetReleaseScope` as "can enforce (probed)". **No surface prints an attainable value as ENFORCED.**
- **Realized:** per attempt, from that attempt's read-back. It is used at VERIFY and in records, approvals, exports and remote views. "Never relabel" applies to realized values.

Every value has the shape **`(dimension, policy, strength, holds_against[], basis, gaps[], implicit_grants[], reason)`**.

**Dimensions:**
- `fs.read`, `fs.write`. On Linux and macOS configuration is files, so configuration stores (dconf files, defaults plists) are `fs` grants there.
- `config`: **Windows only**, with a `config` grant kind for registry key classes.
- `net.out`, `net.in`.
- `ipc`. On Linux it is a function of the `net` policy and the Landlock ABI: abstract UNIX sockets are scoped by the network namespace, or by Landlock's abstract-socket scope from ABI 6, not by the mount view.
- `devices`, with the sub-dimension `devices.gpu`.
- `creds`.
- `persist`.
- `exec`, with the sub-value `exec.elevation` = REACHABLE or BLOCKED (whether a privileged path such as a polkit-authorized system-bus request or a UAC request is reachable).
- `visibility`: whether other processes, their environments and windows can be enumerated. Grantable where a backend can withhold it (the Linux view's PID namespace); **reported, not grantable, on Windows**, where no backend can grant or withhold it.
- `res`: the existing resource entries, targeted by resource requests (task limits, envelope budgets), not by a grant kind.

`ui` is not a dimension: nothing can grant it. It is the basis fact **`ui_isolation`** of a realization (§8.5). **`ui_isolation = shared` with a reachable display server, or any reachable abstract-addressed session service that can start work, is an *escape*-class gap of the realization**: input into the owner's own windows is a launcher of unconfined work.

**Policy.** The requested rule, for example `deny_all` or `allow registry.npmjs.org:443`, kept separate from the strength.

**Strengths, and when they satisfy a REQUIRED dimension:**

| Strength | Definition | Satisfies REQUIRED? |
|---|---|---|
| **ENFORCED** | The OS enforces the stated policy for the whole dimension, outside the explicit **and implicit** grants; the API is DOCUMENTED; and the mechanism's configuration was **read back for this attempt** (per backend: the Windows composite, §5.1; Linux per-field read-back and the in-view self-check, §5.2). An attainable value is never ENFORCED | Yes (realized only) |
| **MEDIATED** | Every route except the mediator is ENFORCED-denied and read back. The mediator runs under the helper-role profile, one per attempt or per profile, and the workload cannot write, signal or replace it. It decides each request; its precision is stated (`per_host`, `per_ip_port`, `per_service`). It holds **outside the allowlist** only: inside it, the exposure statements apply | Only when the requested policy is mediated (an allowlist, a broker). Never when a deny was requested |
| **PARTIAL** | Enforced with documented gaps, each in `gaps[]` with its class | Only with an explicit `min_strength=PARTIAL` in the effective requirement (§3.4), and never for a tier that is a guardrail by design |
| **GUARDRAIL** | Enforced by ArcForges, or bypassable by any same-user process | Never |
| **OBSERVED** | Detected and reported only | Never |
| **NONE** | Not restricted. `UNAVAILABLE` is NONE with a reason | Never |
| **N/A** | The platform has no such dimension | — |

Strengths are ordered ENFORCED > MEDIATED > PARTIAL > GUARDRAIL > OBSERVED > NONE for `meet`.

**`holds_against[]`** is computed by fixed rules, never written by hand:
- **The escape rule comes first.** *An escape-class gap is a property of the realization: if any dimension carries one, every dimension of that realization, ENFORCED and MEDIATED included, has `holds_against` capped at {A1, A2}, and the canonical summary's headline states the escape.* **A launcher cell not measured on the host's build class counts as an escape gap until its lab denies it.** The launcher cells are listed per OS in the term "Gap; gap class" (§1.4) and marked escape-class in the tables of §5. A refusal such as "`wsl.exe` is refused inside CONFINED profiles" is a guardrail and never changes the value.
- **GUARDRAIL** holds against {A1, A2}.
- **PARTIAL** holds against {A1, A2, A3}, unless the realization carries an escape gap.
- **ENFORCED or MEDIATED in a confined tier** holds against {A1, A2, A3}, unless the realization carries an escape gap, and against A4 only where **both** hold:
  - every policy revision on the profile's path is ATTESTED, or the agent client itself runs as a confined attempt (EX-09, later stage); and
  - the writable roots were node-assigned.

  Otherwise the value reads A1–A3 with the gap "profile authorship not attested". Today no `provenance_strength` above GUARDRAIL exists, so no value would carry A4.
- **A5** never appears for a same-kernel tier. A STRONG backend shows it only where that backend's own row lists it, and then as "the vendor's boundary" (§4.1).
- **A6** never appears for the host.
- **`res`** today reads `ENFORCED holds_against [A1, A2]`, `GUARDRAIL against workloads that target ArcForges' objects` (T-22). For a confined attempt it would read **ENFORCED against A1/A2 (as delivered) and "can enforce (probed)" against A3/A4, for processes in the attempt's job or unit**. The A3/A4 credit is conditional: on Windows on LAB-WIN-04's WMI, Task Scheduler and COM-activation cells all denying and on the escape scan tagging sandboxed children; on Linux on the cgroupfs view being read-only and read back; and everywhere on the realization carrying no escape gap. **Work that shared OS services perform on the attempt's behalf is not charged to it** (E4).

**Implicit grants.** Every realization lists the access the backend gives without an ArcForges grant: AppContainer profile storage, the AAP and ARAP writable locations the per-build probe found, the view's tmp, the private HOME. "ENFORCED outside grants" means outside explicit plus implicit grants.

**Basis** (mandatory on every value, attainable and realized): backend; `api_status`; OS build; component version and **fix status read from the installed package**; ABI; probe reference and time; hardening facts; platform facts (for example `wsl_interop_reachable`, the firewall product and service state, `tcc_attribution`); `ui_isolation`; evidence label.

**Hardening and policy filters.**
- A **policy filter** is a seccomp rule that implements a denied grant: socket address families, ptrace, `TIOCSTI` and `TIOCLINUX`, `io_uring_setup` when sockets are denied. It counts toward its dimension and is read back by filter count and policy digest. The address-family allowlist is a required, read-back element of N0 and N1.
- **Surface hardening** (no-new-privileges, syscall-surface reduction against kernel bugs, Win32k lockdown, mitigation masks) is `basis.hardening` only. It may be required (`require_hardening`) and refused if absent; it is never shown as protection and gives no adversary credit.

**Observation** has its own namespace, `observe.*` (for example `observe.etw`, `observe.sandbox_denials`, `observe.landlock_denials`). Its values are limited to OBSERVED, PARTIAL (sampled or lossy) and NONE, with any group-membership dependence stated. It never satisfies REQUIRED.

**Invariants, not fields:**
- **`creds.internal`.** ArcForges' own secrets (the data key, the node credential, link tokens, the LAN key, the data root's `store` and `run`) are never granted to any profile. This is a fixed release-scope sentence.
- **`ipc.arcforges`** (whether ArcForges' user-wide endpoint is reachable) is a basis fact decided by the endpoint rule of §8.3, including its Landlock-only exception.

### 3.3 `api_status` and promotion

`api_status` keeps five values: DOCUMENTED, DEPRECATED, EXPERIMENTAL, UNDOCUMENTED and PREVIEW.
- **Only DOCUMENTED values satisfy REQUIRED.**
- **DEPRECATED** values satisfy REQUIRED only when **all** of these hold, and they are always shown with the label:
  - a local HUMAN set `accept_deprecated` for that backend;
  - the host's probe for that OS version passed;
  - the effective requirement carries `min_strength=PARTIAL` wherever the value is PARTIAL.

  This exists for macOS Seatbelt, the only standard-user macOS route (EX-22).
- **One rule covers the three non-documented values:** EXPERIMENTAL, UNDOCUMENTED and PREVIEW never satisfy REQUIRED. They may realize a PREFERRED dimension, shown as "active, <status>". This covers `Experimental_CreateProcessInSandbox`, PSEC, MXC Tier 1, agent workspaces and the macOS responsibility-disclaim SPI (D-win-primitives-completion-23, -24; D-x-agents-2; D-macos-7).
- **Why five values and not three.** The three non-documented values share one satisfaction rule, but they differ in what the owner is told and in their path to promotion: EXPERIMENTAL names a vendor API on a stated path to documentation; PREVIEW a product preview channel tied to particular builds; UNDOCUMENTED a private interface with no vendor path. Folding them would lose information the owner needs to judge "active, <status>", at no safety gain.

**Promotion to DOCUMENTED-equivalent** is a **Design decision per backend and build class, never a node flag**. It requires all of:
1. vendor documentation that supports the use;
2. a register lab on that build class;
3. a venue-scoped E1 test;
4. the escape-suite row passed;
5. one servicing cycle after general availability;
6. one ArcForges release that shipped it as PREFERRED without a regression finding.

**Identity strength has a basis too.** `identity_strength` carries a basis and an `api_status` like a strength. ENFORCED needs a DOCUMENTED mechanism; a DEPRECATED basis (a Seatbelt `literal` path) is capped at PARTIAL (§7.2).

### 3.4 Require → plan → realize → verify → report

1. **Require.** A task names a profile, or inherits one from its submitter, envelope, installation or origin default. Each grant is REQUIRED or PREFERRED. In a CONFINED profile everything not granted is denied, and **implicit denials are REQUIRED by default**, with a profile-level `min_strength` override. `allow_unenforced` (`policy.proto`) applies to `res` only.
2. **Plan, at admission, against attainable values.** The node computes `effective = meet(requested, caller floor, HUMAN-set client floor, client-declared floor, origin floor, installation floor, envelope)`.
   - **`meet` covers the requirement fields too:** the stronger wins. REQUIRED beats PREFERRED, the higher `min_strength` wins, and any `require_*` wins. Lowering any of them below a floor is a widening and takes the path of §7.3.
   - The node then picks the strongest available backend whose attainable values satisfy every REQUIRED dimension under §3.2–§3.3.
   - If none does, it refuses with `ISOLATION/unavailable:<dimension>` and an `ExplainTask` answer.
   - **It never falls back to UNCONFINED.** Refuse; do not merely warn. MXC refuses unsupported fields per field and per backend (D-x-agents-1); Claude Code's sandbox falls back to unsandboxed execution unless `failIfUnavailable` is set (D-x-agents-18), the counter-example this rule avoids.
3. **Realize.** Confinement is applied before the workload's first instruction: on Windows through a suspended AppContainer process; on Linux before the workload's `execve`.
4. **Verify.** Per-backend read-back produces the realized values.
   - A REQUIRED mismatch gives `SPAWN_FAILED` with the reason; no workload code has run (§2.3 for the SM-ATTEMPT mapping).
   - A PREFERRED mismatch is recorded in `unenforced_dimensions` and shown on every surface.
5. **Report.** The realization becomes part of the attempt record, `ExplainTask`, `SessionCoverage` and the remote D1 summary, always through the canonical summary (§3.5). Approvals, remote views and exports show the *realization*, never the request.

**Defaults.** Every origin's default profile is UNCONFINED, today's behaviour, reported truthfully: every access dimension shows `NONE (reason: same-user tier)`. UNCONFINED profiles carry no grants at all. Making a CONFINED profile the default for an origin, starting with AGENT, is a later, separate owner decision, gated by:
- compatibility (G19, at least 80 % for the class and OS);
- overhead (G20, within the X % ceiling of [AD-0017](../decisions/AD-0017-delegated-execution-direction.md) principle 9, with cache-hit-rate loss and start latency measured);
- the editions check (§7.6);
- the lock-out rules (protected control set, confirm-or-revert, `--safe`) in force (EX-07 stage b).

### 3.5 Reporting surfaces

**The canonical summary.** One node-computed projection, in the contract, never computed by clients:
- **protected against / not protected against**, by adversary class from `holds_against`, in plain language;
- **the headline:** the realization's escape gap where one exists, otherwise the weakest REQUIRED dimension;
- **exposure statements**, computed across dimensions: `creds` delivered or an `fs.read` scope, together with a `net.out` that is not ENFORCED-deny, gives "exfiltration possible to <scope>"; a MEDIATED allowlist gives "exfiltration possible to <allowed hosts>"; `ui_isolation = shared` gives "can read the screen and inject input into the desktop";
- a fixed link to the full table.

The remote D1 summary is exactly this projection. **No surface renders a realization except through the canonical summary or the full table** (an acceptance criterion of EX-07 stage a).

| Surface | Today | Gains (proposed) |
|---|---|---|
| `CapabilityReport` | Per-resource enforcement with reasons (DELIVERED) | Per backend and dimension the **attainable** value with basis ("can enforce (probed)"). The probe runs at node start, and again on a package, kernel or sysctl change. `observe.*` is listed separately. It never changes SM-NODE |
| `ExplainTask` | Feasibility, keys, holders (SPECIFIED) | The realization plan or result; the floors; why a backend was chosen or the task refused; cooldown or provenance reasons; a **dry-run mode** over a draft `TaskSpec` with a profile, which also states each grant's revocation class |
| `ExplainPermission` | Matrix decision and its source (SPECIFIED) | The caller's `identity_strength` with basis; the `provenance_strength` of the policy revision |
| `GetReleaseScope` | Managed operations and gaps (SPECIFIED), with the stated limits of the [product definition](../product/product-definition.md) §9 | One row per access dimension, stated per platform, not per host. Lifecycle rows. The credential sentence (§8.2). The per-client routing statement and "the client's own process keeps the user's full access". The generic UAC sentence. **Never a host-posture fact or a D2 path**: `GetReleaseScope` is callable by AGENT callers (`HUMAN=A SCRIPT=A AGENT=A`) and the MCP `session_coverage` tool returns it to the AI client, so anything in it can reach a prompt-injected agent and the model provider's context |
| Doctor | Health, enforcement self-test (SPECIFIED); the HUMAN-only host-posture check of the account type and the Administrator protection state ([07](07-records-diagnosis-memory.md) §2.4; AF-DIAG-01) | The probe as an isolation self-test. The **HUMAN-only host-posture check** (§10) gains the AppArmor userns restriction, the bwrap fix status, `wsl_interop_reachable`, the firewall service state, `AlwaysInstallElevated`, Smart App Control, SIP, the TCC categories the node holds, Performance Log Users membership, and on Windows every user directory whose ACL ArcForges changed (EX-10). `RunDoctor` is AGENT-callable and the MCP `doctor` tool returns it, so these values go to HUMAN callers only: AGENT and SCRIPT callers and the MCP tool see only that a HUMAN-only check exists, with neither its status nor its values (a status alone would disclose the posture). Host-posture facts are D2 and left out of support bundles unless the owner includes them |
| Findings | 24+ kinds (SPECIFIED) | `ISOLATION_DEGRADED`, `ISOLATION_FIX_UNKNOWN`, `SANDBOX_DENIED` (where denial evidence is readable), `PERSISTENCE_ADDED`, `PRIVILEGED_CHANGE_OBSERVED` (attempt windows only), `TOOL_DEFINITION_CHANGED`, `UPDATE_OWNER_CONFLICT`, `RESIDUE_FOUND`, `CACHE_UNAVAILABLE_IN_PROFILE` |
| MCP adapter | The tools of [experience/mcp.md](../experience/mcp.md) | Agent-facing envelope introspection: the agent's own realized profile, remaining budget and dry-run answers (EX-09), the access analogue of the accepted roadmap row on real-time resource requests from AI clients |
| Desktop, phone, Web | — | The canonical summary; **never a single "sandboxed" bit** |

## 4. Threat model and trust boundaries (direction)

Release 1's threat model is [11](11-security-privacy.md) §1–§4, with the pair-1 rows T-22 … T-27, the amended T-11, and the boundaries B0 and B11 of [01](01-system-overview.md) §4. Everything in this section beyond the unconfined row is direction.

### 4.1 The tiered threat scope

Today [11](11-security-privacy.md) §2 says that any same-user process can reach the node and that malware running as the user is out of scope. That stays true for the unconfined tier and is **not weakened there**. The tiered scope has one row per workload state. The unconfined row is in force now; the other rows are direction until their rows are promoted ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 5). Its invariant has a part that is true of release 1 and a part that is direction (principles 6 and 7):

> **In force now:** the node never extends the privileges of any caller.
>
> **Direction, effective at EX-09's promotion:** when confined attempts exist, the node never relaxes the confinement of a caller it confined. Today it cannot see a client's own sandbox, and commands routed through it run outside that sandbox (T-24, B11).

| Workload state | In scope | Out of scope (stated) |
|---|---|---|
| **Unconfined** (today, and the default; in force) | A1, A2 for resources. Records and guardrails (approvals, origins, cleanup re-validation). Tampering with ArcForges' own objects is a **documented bypass** (T-22) | A3–A6. Any same-user code can do what the user can: read every credential the user can read, change ArcForges' containers, escape detection. **HUMAN is an origin, not an identity; local widening is GUARDRAIL against unconfined same-user code.** On an administrator account without Administrator protection, UAC is not a security boundary, and an unconfined workload may obtain administrator rights silently |
| **Confined, per realized dimension** (direction) | A1–A3 for each dimension realized ENFORCED or MEDIATED and read back. A4 only where every revision on the profile's path is ATTESTED (or the agent client itself runs confined) **and** the writable roots were node-assigned (§3.2). ArcForges' objects (jobs, cgroupfs, node endpoint, store, secrets) unreachable from the attempt | Dimensions realized PARTIAL, GUARDRAIL or NONE; a realization with an escape gap holds only A1, A2 in every dimension (§3.2). A5 beyond the vendor-serviced boundary. A6 always. Writes to granted roots that unconfined processes execute later (§7.1) |
| **STRONG backend** (direction; EX-18) | **Per backend row:** VM-class backends A1–A5 within the vendor boundary as configured; same-kernel backends (rootless Podman) A1–A4; account backends A1–A4, A5 only for a non-admin account; microVMs A5 only if the VMM is confined; `net` and `ui_isolation` per backend | Channels the backend's defaults open: networking, clipboard, mapped folders (D-win-strong-2) |
| **Privileged installers and system software (A6)** (direction) | Structural prevention: ArcForges never elevates at run time, and an elevation prompt is the owner's decision **where a prompt appears**. Detection: standard-user detectors raise `PRIVILEGED_CHANGE_OBSERVED` only inside an attempt window, labelled "seen during attempt <id>, cause unknown" | Containment of machine-wide changes on the host; only a VM backend can contain them. Writes of an elevated run land in another account's profile (the administrator's, or Administrator protection's shadow profile) and are `Not known` (D-win-install-19). Silent elevation without Administrator protection |

**The A5 sentence**, shown in realizations of STRONG backends: *"This attempt ran inside <vendor boundary>, which <vendor> services as a security boundary. ArcForges does not independently guarantee it against software designed to escape it."*

**The permission matrix.** The existing sentence of [11](11-security-privacy.md) §1 stays: the matrix "protects against accidental and casual misuse by AI clients". Its future companion: **for confined attempts the matrix becomes OS-backed where the identity is ENFORCED: W2/W3 and the Linux view chain.** On macOS `identity_strength` is capped at PARTIAL, and below Landlock ABI 9 without a view it rests on the node's peer-cgroup clamp.

**Identity qualifier.** `identity_strength = ENFORCED` means that a sandboxed caller cannot present another identity. **It does not exclude calls from unsandboxed same-user processes.** A leased AppContainer identity is GUARDRAIL against unsandboxed same-user code (D-identity-ipc-completion-4).

### 4.2 Future trust boundaries B7–B10

[01](01-system-overview.md) §4 keeps B1–B6 and the now-rows B0 and B11. The boundaries below apply only when their rows are promoted:

| ID | Boundary | Protection (proposed) | When |
|---|---|---|---|
| B7 | The node and a confined attempt, across the attempt endpoint | OS-enforced reach (a pipe DACL with the leased AppContainer SID; a socket bound into the view by directory; a Seatbelt `literal` path, PARTIAL) plus R1–R7 | EX-09 |
| B8 | Sibling attempts: environments, process objects, caches, workspaces | A leased per-attempt AppContainer identity, **ENFORCED only under the lease invariant** (§5.1), otherwise GUARDRAIL across leases; a PID namespace; cache trust partitions; per-session worktrees | EX-09, EX-10, EX-11 |
| B9 | The node and acquired content being parsed: archives, OCI layers, manager outputs, installers, proxied traffic | **Untrusted formats are parsed only under the helper-role profile; where no backend realizes it, the method is UNAVAILABLE.** Vendor code never runs at extraction | EX-12, EX-13 stage b |
| B10 | The artifact and the node: what an acquisition installs and later runs | Digest pins; recorded signatures and OS gate verdicts; cooldown; MOTW and quarantine kept; split acquisition and run profiles | EX-13 |

**What does not change:** there is still **no boundary between the node and an unconfined workload**, and the Design keeps saying so ([01](01-system-overview.md) §4).

### 4.3 ArcForges as a high-value target

Confinement would turn the node into the mediator for confined attempts, and that makes it a target.

**Self-protection principles:**
1. The node is never inside a sandbox it creates. No profile ever applies to the node or to the owner's shell.
2. **Hostile input is never parsed in the node process.** Extraction, installer inspection, proxy parsing and TLS termination run in helper roles under the **helper-role profile**: deny-all except the passed descriptors, network denied (egress only for the proxy), no bus. Its realized strength per OS: on Linux the view chain, or a socket-family policy filter on the Landlock-only tier; on Windows LPAC; on macOS only an App-Sandboxed helper executable, which is a second signed binary that RM-14 does not cover today: it would need RM-14's Item widened, or its own row (§9.1). **Where the profile cannot be realized ENFORCED for `fs`, `net` and `ipc`, the method is UNAVAILABLE and refused, never parsed in the node.**
3. No ArcForges object is reachable from a confined workload.
4. Every widening is decided by HUMAN, which is GUARDRAIL against unconfined same-user code until attested presence exists (EX-23).

**ArcForges' own privileges stay minimal** ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), boundary 10). The new attack surface is managed code: the profile compiler, the attempt endpoint, the mediators and the journal. That is why the host-write journal precedes the first backend that creates host objects (EX-08 in EX-10's Prerequisites), and why property-based tests (CsCheck, [AD-0016](../decisions/AD-0016-local-first-verification.md) §5) are part of every promotion.

### 4.4 Future threat rows T-28 … T-42

The rows that apply now, T-22 … T-27 and the amended T-11, are in [11](11-security-privacy.md) §4. The rows below are proposed; none enters chapter 11 before its row is promoted.

| Row | Threat | Mitigation (proposed) | Applies when |
|---|---|---|---|
| T-28 | Confinement laundering: a confined attempt asks the node for an unconfined task | R1–R7; unknown foreign confinement fails closed; widening only by HUMAN; never HUMAN from inside | EX-09 |
| T-29 | Policy-input injection and link substitution: writable roots from caller input (`cwd`, MCP Roots); a bind or ACE that lands on a link target | Writable roots only from registered workspaces and managed roots; the compiler's link-safety rule (§7.1) | EX-07 stage b |
| T-30 | Mediator or parser compromise | Closed grant types; the helper-role profile; metadata-only records; one mediator per attempt or per profile | EX-12, EX-13 stage b |
| T-31 | Remote widening or downgrade | Local-only until end-to-end approval signatures exist; the never-remote list | EX-23 |
| T-32 | Managed-artifact substitution, re-resolution and tool-definition change | Digest pin; cooldown; publisher continuity; `tools/list` digests; the wrapper fails closed | EX-13 |
| T-33 | Host-state residue: AppContainer profiles, ACEs, desktops, MXC-style host ACLs | Every object a journal entry and an owned object; the lease invariant | EX-08, EX-10 |
| T-34 | Cache poisoning across trust levels | TP-1 … TP-8 | EX-09 |
| T-35 | Install- and launch-time code | Split acquisition and run profiles (O4); MOTW and quarantine | EX-13 stage b |
| T-36 | Credential exfiltration through granted egress | Exposure statements; brokers instead of values; inject hosts only (a later research stage) | EX-12 |
| T-37 | Approval fatigue and misleading approval content | The exact grant delta at D2 to the approver; widening TTLs; action budgets; local-only where the remote privacy toggle forbids D2 | EX-07 stage b, EX-14 |
| T-38 | Lock-out by a strict profile | The protected control set; confirm-or-revert; `--safe` | EX-07 stage b |
| T-39 | Direct edits of policy or grants by same-user code | Tamper finding; `provenance_strength`; no A4 credit without ATTESTED revisions | EX-07 stage b |
| T-40 | Journal or `recover` misuse | Journal entries name exact objects; `recover` replays only recorded entries, HUMAN only | EX-08 |
| T-41 | Re-creation of a held persistence entry | Re-check at the OS mechanism; a finding; "held", never "blocked" | EX-15, holds stage |
| T-42 | Delayed execution of confined writes by unconfined processes | The extended always-forbidden set; workspace provenance; a finding or the writer's profile as a floor (decided at EX-09) | EX-09 |

## 5. Platform strategies (attainable, pre-lab)

The three implementations are deliberately asymmetric. **The contract is shared (§2, §3); the mechanisms are not.** Each ladder lists only backends this direction proposes to build; rejected rungs are in §16. **Every per-dimension value below is an attainable, pre-lab value with its gaps and its lab, never a realized ENFORCED.**

### 5.1 Windows (EX-10; EX-17 … EX-21 for research backends)

| Backend | Status | Privilege |
|---|---|---|
| **W0**: root and attempt jobs (today) | Kept. `res` ENFORCED against A1/A2, GUARDRAIL against hostile code (T-22); every access dimension NONE (D-win-primitives-completion-1) | P0 |
| **W2**: a hand-built AppContainer, brokered by the `exec-wrap` holder: suspended creation inside today's root and attempt jobs, the existing handle list, read-back before resume, a leased identity per running attempt, no job UI limits, the profile recorded as an owned object | **The one Windows confined backend** (EX-10) | P0 |
| **W3**: LPAC | The same backend, chosen per profile where the tool tolerates it | P0 |
| W1: write-restricted token, Low IL, alternate desktop | **Not offered**: "a guardrail that looks like a sandbox" (D-win-primitives-completion-14) | P0 |
| SBOX, PSEC, MXC | EX-17. Capped at "active, experimental". PSEC returned access denied for a standard user in a public report | P0, unverified |
| Windows Sandbox; Hyper-V/HCS (reference only); OS agent accounts (tracked only) | EX-18 | P1 (the owner enables); HCS needs Hyper-V Administrators |

**W2 and W3, attainable values before any lab** (D-win-primitives-completion-16, -17, -20):

| Dimension | W2 | W3 (LPAC) difference | Deciding lab |
|---|---|---|---|
| `fs.write` | PARTIAL ("probed, not read back") until the composite read-back below is accepted; then ENFORCED outside explicit and implicit grants. AAP-writable locations are gaps. Conditional on the WSL leg | As W2 | LAB-WIN-04, LAB-WIN-18 |
| `fs.read` | PARTIAL: system and AAP locations stay readable | PARTIAL, with the ARAP gap: core system binaries stay readable through ARAP; whether LPAC honours such ACEs is unverified | LAB-WIN-04, LAB-WIN-18 |
| `config` | Reads PARTIAL (HKCU and HKLM keys readable by AAP). Writes: the container's own registry location is an implicit grant; elsewhere PARTIAL until the composite read-back | Reads need the `registryRead` capability | LAB-WIN-04 |
| `net.out` | "Deny (own sockets); service-mediated egress unmeasured", until the DNS and redirector cells of LAB-WIN-04 and LAB-WIN-09 deny. The value comes from a **live canary probe** at node start, and the basis records the firewall product and service state. `internetClient` is PARTIAL: "no network or full network" | As W2 | LAB-WIN-04, LAB-WIN-09 |
| `net.in` | Deny without server capabilities, loopback included; the same canary basis | As W2 | LAB-WIN-09 |
| `ipc` | PARTIAL: gaps `system_brokers`, `com_per_server_permissions`. Pipes without a DACL grant are denied | COM needs `lpacCom` | LAB-WIN-04, LAB-WIN-05 |
| `devices` | PARTIAL: gaps `input_always_available`, `gpu_unverified`. `devices.gpu`: no deny mechanism is proven on Windows, so it is a basis fact "GPU reachable (unverified)", not a grant | As W2 | LAB-WIN-04 |
| `creds` | PARTIAL until the Credential Manager, DPAPI and WSL legs pass | As W2 | LAB-WIN-04 |
| `persist` | PARTIAL: Run keys and the Startup folder closed by DACL (no redirection); the Task Scheduler and WMI cells are launcher cells (row below) | As W2 | LAB-WIN-04 |
| `exec` | PARTIAL: System32 binaries stay executable. `exec.elevation` is measured by a LAB-WIN-04 leg. `wsl.exe` is refused inside CONFINED profiles if WSL interop is reachable | As W2 | LAB-WIN-04 |
| `visibility` | Reported, not grantable; PARTIAL or NONE until measured | As W2 | LAB-WIN-04 |
| `res` | ENFORCED against A1/A2 (delivered); can enforce (probed) against A3/A4 for processes in the attempt's job, conditional on LAB-WIN-04's WMI, Task Scheduler and COM cells (§3.2) | As W2 | LAB-WIN-01, LAB-WIN-04 |
| **Launcher cells (escape class)** | WMI, Task Scheduler, COM activation of launch-capable servers, and WSL interop (`wsl.exe`, `\\wsl$`, `\\wsl.localhost`, `LxssManager` activation): all unmeasured. **Each counts as an escape gap of the realization until LAB-WIN-04 denies it from W2 and W3**, so until then every row above holds against {A1, A2} only (§3.2) | As W2 | LAB-WIN-04 (with its WSL leg) |
| `ui_isolation` (basis fact) | The first backend is headless: GUARDRAIL (a holder-owned window station and desktop; a reopen of `WinSta0\Default` not shown denied). "Separate desktop measured" only if LAB-WIN-04 shows the reopen denied, expected for LPAC at most | As W2 | LAB-WIN-04 |

**The Windows read-back is a stated composite.** A token read-back proves which SIDs and capabilities the process has, not what it can write. Windows read-back is therefore:
1. the token read-back before resume (AppContainer flag, package SID, capabilities, LPAC flag);
2. a journal check that the only ACEs naming this SID are this attempt's, with none left from an earlier lease;
3. a per-build probe of AAP- and ARAP-writable locations, listed in `gaps[]`.

Until this composite is accepted as Windows read-back (a Design decision at EX-10's promotion), Windows `fs.*` is PARTIAL ("probed, not read back").

**The lease invariant.** A SID is re-leased only after the journal shows every ACE for it removed, its profile storage and private registry location reset, and no process with that token alive (checked through the holder's job). After a node crash a SID is quarantined, not reused. B8 is ENFORCED only under this invariant. `TEMP` and `TMP`, which an AppContainer launch reroutes to the container profile, are pointed at `tmp/<attempt>` and verified, or profile storage counts against the tmp limit (AF-STOR-01). G20 measures "one fresh profile per attempt" as the alternative. Residue test: a re-leased SID has no access to the prior lessee's grants (§14.1).

**WSL interop.** `wsl.exe` sits in System32 and reaches `/mnt/c` with the Windows user's permissions. W2/W3 `fs.*` and `creds` are ENFORCED only if LAB-WIN-04's WSL leg (`wsl.exe`, `\\wsl$`, `\\wsl.localhost`, `LxssManager` activation, from W2 and W3, with WSL installed in the guest) denies. The basis carries `wsl_interop_reachable`. If it is reachable, or not yet measured, those dimensions are PARTIAL with the gap stated (class *escape*), and **because the gap is escape-class, every dimension of the realization (`net.*`, `ipc`, `persist`, `exec` and `res` included) holds against {A1, A2} only** (§3.2). `wsl.exe` is also refused inside CONFINED profiles; **that refusal is a guardrail and never changes the value**, because it does not cover a workload's own children, the `\\wsl$` paths or service activation.

**Grant compilation is an open design choice with a cost leg.** A registered workspace and user-installed toolchains (`.cargo`, `.nuget\packages`, `%APPDATA%\npm`) are the user's files without AppContainer ACEs. The options, evaluated together in LAB-WIN-18 and G20:
1. **Per-root custom capability SIDs:** one journaled, HUMAN-approved inheritable ACE per root; a per-attempt grant is then the capability in the token, with RESTART_REQUIRED revocation. A capability ACE admits every attempt holding that capability.
2. **Managed worktrees as the default writable workspace** (AF-WS-01; EX-16); an ACE on the registered checkout only by explicit HUMAN choice.
3. **Per-attempt ACEs** only if LAB-WIN-18 and G20 show the propagation cost acceptable at 10³–10⁵ files; a crash mid-propagation leaves altered ACLs, which the journal must repair.
4. **An Installation-scoped stable AppContainer identity** for an always-confined OWNED installation: its profile becomes the state root, uninstall is `DeleteAppContainerProfile` plus the journal, and its Credential Locker holds its own secrets. The trade-off is one identity shared by that installation's attempts.

`user_path` grants on Windows are copy-in, copy-out, or refused. The "no ACE" rule is narrowed to credential files. Every user directory whose ACL ArcForges changed is listed on HUMAN-only local surfaces (the doctor's host-posture check and ArcForges' own uninstall plan) and removed by ArcForges' own uninstall. These are D2 paths, so they never appear in `GetReleaseScope` or any other AGENT-readable or MCP-returned surface.

**Endpoint reach.** A passed handle reaches only the direct child; descendants (`arcforges run`, the MCP adapter, tools started by `node` or Python) must open the endpoint **by name** from inside the AppContainer, which is E4 (LAB-WIN-05). If that fails, the stated fallback is "only the attempt's direct child can reach the node; descendants are refused".

**Further W2 facts.** The holder's private station and desktop must grant the leased SID access: one more owned object. Each alternate desktop costs about 4 MB of desktop heap; G20 measures desktops at N parallel attempts. `graceful_stop` (`CTRL_BREAK`, `WM_CLOSE`) to a child on another desktop is unmeasured (LAB-WIN-01) and reported per backend. CONFINED with `kill_with_node` is refused until defined.

**Today's W0 compatibility note.** Chromium-family workloads set job UI limits on their own children, which may not nest inside ArcForges' attempt job (D-win-primitives-completion-4, E4). Browser-automation MCP servers are target class 1, so this is a release-1 compatibility note ([AD-0005](../decisions/AD-0005-resource-enforcement.md), Windows §3) and a W0 headless-Chromium leg of LAB-WIN-01.

**Delegated to the OS:** elevation (UAC, Administrator protection), execution allow-listing (App Control, Smart App Control; reported only, and kept effective for OWNED content by MOTW, §6.2), device consent, Credential Locker for packaged apps, vendor MSIX deployment (EX-21).

**Reported as unavailable:**
- GUI isolation on the shared desktop;
- per-destination network control: there is no documented OS-forced proxy path for unpackaged processes (D-win-strong-23);
- loopback caches for confined attempts, **conditionally (E4)**: if LAB-WIN-09 leg (a) shows that loopback between two processes inside the same AppContainer is blocked, a cache service reached over loopback is `UNAVAILABLE(loopback_blocked)` and the run proceeds uncached (sccache is TCP-only on Windows). With the sccache server S2' inside the attempt's own AppContainer, the connection is intra-container, so the cached path may remain. **Never a loopback exemption** (SR-1);
- WMI, broker and spoofed-launch escape detection (T-23);
- physical memory caps (V-W05).

**Minimum viable step.** W2/W3 for headless COMMAND and SERVICE attempts: `fs` grants on managed roots and managed worktrees only; `net{none}` or `net{open}`; `ui_isolation` GUARDRAIL.

**Gates.** The composite first-backend rule (§13.2; G40): LAB-WIN-01 (G01), LAB-WIN-05 by-name reach (G07), the Windows class-1 corpus at 60 % or more (LAB-X-01), LAB-WIN-18 with at least one class-2 toolchain under root-scoped grants, the owner's acceptance of uncached builds where LAB-WIN-09 (a) fails, and LAB-WIN-04's launcher cells and WSL leg denying from W2 and W3 (condition 6); then the rest of LAB-WIN-04 (G02) and LAB-WIN-09 (G08).

**Reject condition.** If no combination nests with limits, accounting and termination intact, Windows confinement goes only to the STRONG backends (EX-18), and the Design says so plainly. **Never trade E1 containment for E4 isolation.**

**Positive compatibility ladder** (request §3), each rung with its own residue statement:
1. the portable OWNED layout (D-win-install-32);
2. environment and flag redirection, labelled `HONORED` or `BEST_EFFORT` (D-win-install-25);
3. owned app hives for ArcForges tooling (D-win-install-27);
4. COM-registration capture under the helper-role profile, which also keeps COM registration off the host (D-win-install-28);
5. later, per-user dual-purpose MSI as DELEGATED, with static pre-checks (D-win-install-15).

Rejected: repackaging, PSF, UAC virtualization, bind links, minifilters.

### 5.2 Linux (EX-11; EX-18 for STRONG backends)

| Backend | Status | Attainable values (pre-lab) | Privilege |
|---|---|---|---|
| **L0**: transient unit (today) | Kept | `res` ENFORCED against A1/A2, GUARDRAIL against hostile code (D-lnx-kernel-1) | P0 |
| **View chain**: unit → `exec-launch` → the distribution's `bwrap` (the only mount-namespace owner) → `exec-init` (PID 1: reaping, exact exit status, in-view end steps) → `exec-final` (no-new-privileges, Landlock reduced to the probed ABI, seccomp policy filters; no TSYNC) → workload | **The Linux confined backend** (EX-11) | `fs.*` "can enforce (probed)" outside explicit and implicit grants, read back per field and by the in-view self-check before the workload's `execve`. `net{none}` N0 with the address-family allowlist read back. `ipc` and `ui_isolation` per the table below. `visibility` by PID namespace. ptrace and `TIOCSTI` denied by policy filters. `res` against the confined workload with a **read-only view of the attempt's own cgroup** under a cgroup namespace by default; "hidden" is a profile option. Persistent-state profiles only where the **installed** bwrap package is on the exact fixed-revision list (CVE-2026-87766; Debian 13 `0.12.0-1~deb13u1` or later; D-linux-chain-install-14) | P0 (Ubuntu 24.04: a P1 profile step) |
| **Landlock-only tier** | A separate tier with backend `landlock`, never under the view's field names; a mandatory node clamp by peer cgroup identity | `fs.*` PARTIAL with an **escape** gap below ABI 9 (the session bus, `$XDG_RUNTIME_DIR/systemd/private` and the node's pathname socket reachable). Because the gap belongs to the realization, **every dimension of the tier holds against {A1, A2} only below ABI 9** (§3.2). `ipc` **NONE below ABI 6**; PARTIAL with the escape gap at ABI 6–8. `net.out` PARTIAL (TCP ports) from ABI 4, NONE below. The other cells are in the table below | P0 |
| N1 egress: an `lo`-only network namespace plus the proxy under the helper-role profile, on a socket bound by directory | EX-12 | `net.out` MEDIATED (`per_host`), holding outside the allowlist; destinations measured. **It needs a network namespace: unavailable on Ubuntu 24.04 by default and without user namespaces** | P0 |
| L1 hardening profile | Optional, on every target | Basis facts; `exec` PARTIAL only (no setuid gain) | P0 |
| systemd unit sandboxing | **Only** for the optional hardening of ArcForges' own units (F-L04) | — | P0 + userns |
| Rootless Podman `--cgroups=split`, gVisor | EX-18 | Per their own rows | P0 (a one-time P1 for subuid) |

**View chain and Landlock-only tier, attainable values per dimension before any lab.** Every cell is pre-lab (E4) and is shown as "can enforce (probed)" at most; none is a realized ENFORCED.

| Dimension | View chain | Landlock-only tier | Deciding lab |
|---|---|---|---|
| `fs.read`, `fs.write` | Can enforce (probed) outside explicit and implicit grants; per-field read-back and in-view self-check before `execve`. Persistent-state profiles only with a fixed bwrap package | PARTIAL, escape gap below ABI 9 | LAB-LNX-01, LAB-LNX-02 |
| `config` | N/A: configuration is files on Linux, folded into `fs` | N/A, as the view chain | — |
| `net.out`, `net.in` | `net{none}`: N0 with the address-family allowlist read back; `net{open}`: NONE, reported "unrestricted" | `net.out` PARTIAL (TCP ports) from ABI 4, NONE below; `net.in` PARTIAL (TCP bind by port) from ABI 4, NONE below | LAB-LNX-01, LAB-LNX-03 |
| `ipc` | Per the `net` and ABI table below | NONE below ABI 6; PARTIAL with the escape gap at ABI 6–8 | LAB-LNX-02 |
| `devices` | Can enforce (probed) for device nodes withheld from the view; `devices.gpu` only by an explicit grant. Gap: devices reachable through a granted socket or service | PARTIAL: device files are paths under Landlock's rules; unmeasured | LAB-LNX-01; LAB-X-06 for `devices.gpu` |
| `creds` | Can enforce (probed) by inclusion for credential files and agent sockets outside grants (a private HOME). On WSL PARTIAL until LAB-LNX-05 (the `/mnt/*` and interop bridge) | PARTIAL, escape gap: the session bus and its secret service stay reachable below ABI 9 | LAB-LNX-01, LAB-LNX-05 |
| `persist` | PARTIAL: user units, autostart entries and shell profiles outside grants are absent from the view; writes to granted persistent roots may be run later by unconfined processes (§7.1); the user manager is unreachable only while its sockets are hidden and read back (D-lnx-kernel-20) | PARTIAL, escape gap: the user manager is reachable below ABI 9 | LAB-LNX-02, LAB-LNX-17 |
| `exec`, `exec.elevation` | `exec` PARTIAL: no-new-privileges closes setuid gain; system binaries stay executable. `exec.elevation` BLOCKED only where the view hides the system bus and is read back, otherwise REACHABLE (D-persistence-observation-recovery-14) | `exec` PARTIAL (no-new-privileges); `exec.elevation` REACHABLE, because the system bus stays reachable below ABI 9 | LAB-LNX-01, LAB-LNX-02 |
| `visibility` | Can enforce (probed) through the PID namespace; gap: the host network namespace and its abstract sockets under `net{open}` | NONE: no PID namespace | LAB-LNX-01 |
| `res` | ENFORCED against A1/A2 (delivered, L0); can enforce (probed) against A3/A4 with the read-only own-cgroup view read back (§3.2) | As L0: ENFORCED against A1/A2, GUARDRAIL against workloads that target ArcForges' objects | LAB-LNX-01, LAB-LNX-19 |
| **Launcher cells (escape class)** | The session bus, the systemd private socket and the user-wide node endpoint: hidden from the view, read back. A display server reachable under `net{open}` below ABI 6: an escape gap (table below). Any cell not yet measured counts as an escape gap until LAB-LNX-02 denies it | The session bus, the systemd private socket and the node's pathname socket are reachable below ABI 9: escape gaps, so the whole tier holds against {A1, A2} | LAB-LNX-02 |

**`ipc` and `ui_isolation` depend on `net` and the Landlock ABI** (D-lnx-projects-14, -28; D-lnx-kernel-10). Under `net{open}` the attempt keeps the host network namespace, so host abstract sockets such as X11's `@/tmp/.X11-unix/X0` are reachable unless Landlock's abstract-socket scope (ABI 6 or later) applies. The probe and the in-view self-check both run an abstract-connect check.

| Host (Landlock ABI) | `net{none}` or N1 | `net{open}` |
|---|---|---|
| Debian 13 (6), current WSL2 kernels (7) | `ipc` can enforce; `ui_isolation` no display | `ipc` can enforce with the abstract-socket scope; no display socket in the view |
| Debian 12 (2), Ubuntu 22.04 (1; HWE 4), Ubuntu 24.04 with the profile (4) | `ipc` can enforce; no display | `ipc` PARTIAL; `ui_isolation` shared; **an escape gap where a display server is reachable** (the X11 abstract socket), so on a desktop host every dimension of the realization holds against {A1, A2} only |

**The Ubuntu 24.04 statement, made plainly:** *Ubuntu 24.04 by default gives no boundary against compromised tools or AI-generated commands; it gives resource control plus guardrails.*
- The default is the Landlock-only tier, because of the AppArmor userns restriction (D-lnx-kernel-9), and that tier has a complete escape to an unconfined unit below ABI 9 (D-lnx-kernel-10). Ubuntu 24.04 GA has ABI 4.
- The full view needs the AppArmor `bwrap-userns-restrict` profile, a P1 step. Whether ArcForges offers it as an OS-prompted, journaled step under boundary 2 is an owner question (§17).
- Even then the view stays **ephemeral-state only** while Ubuntu's fix stays reverted (USN-8779-2).
- A remedy to evaluate before the tier is promoted: a socket-family policy filter in `exec-final` (deny `AF_INET`, `AF_INET6`, `AF_NETLINK`, `AF_VSOCK` for `net{none}`; deny `AF_UNIX` creation, `socketpair` allowed, for `ipc{none}`). For profiles without IPC needs, such as many stdio MCP servers, it could make `net{none}` a real deny and close the session-socket escape at P0 (E4; LAB-LNX-01, LAB-LNX-02).
- Debian 13 with the fixed package is the reference. **The Linux story must not be marketed from the Debian reference alone.**
- WSL2 evidence counts for WSL2 on that kernel only. The WSL bridge (`/mnt/*` and interop) keeps `creds` PARTIAL until LAB-LNX-05.

**Ephemeral-state and persistent-state profiles.**
- A **persistent-state profile** has at least one workload-writable bind source that persists across attempts: the workspace, a cache, HOME, a state root. The hazard of the 2026 view-setup escape class (CVE-2026-87766) is a link planted in such a source that a later setup follows.
- An **ephemeral-state profile** has none: every writable mount is a per-attempt directory deleted at the end, and results leave only through a reviewed copy-out (EX-16).
- The exact trigger is confirmed in LAB-LNX-01. **A compiler rule to test:** no mount destination at or beneath a persistent workload-writable source, and caches and HOME at disjoint paths. If the class loses its precondition under that rule, "ephemeral-state only" would lift on three distributions.

**What works today, per target class and distribution (all E4; nothing measured):**

| | Debian 13, fixed package | Debian 13 with an unfixed package (an unfixed revision such as `0.11.0-2+deb13u1` exists in the field) | Debian 12; Ubuntu 22.04; Ubuntu 24.04 with the profile | Ubuntu 24.04 default |
|---|---|---|---|---|
| Class 1: stdio MCP servers (`net{none}`, small state) | View, persistent state | View, ephemeral state; state roots only under the compiler rule | As the unfixed Debian 13 column | Resource control plus guardrails (the Landlock-only tier); the socket-family filter may lift it for IPC-free servers |
| Class 2: CLIs and builds (workspace, caches) | View, persistent state | Ephemeral: the workspace through a session-worktree copy-out, unless the compiler rule holds | As the unfixed Debian 13 column | Resource control plus guardrails |
| Class 3: AI-generated commands (workspace) | View, persistent state | As class 2 | As class 2 | Resource control plus guardrails |

**Probe reference data is a standing security-data duty.** Ubuntu's revert compares as *newer*, so a version comparison wrongly accepts unfixed packages. The fix-revision lists, ABI tables and other probe reference data would travel as signed data in the release manifest of [AD-0012](../decisions/AD-0012-distribution-and-updates.md) (no new outbound lookup). An unknown revision is unfixed, with the finding `ISOLATION_FIX_UNKNOWN`. The owner of the data is named at EX-11's promotion. LAB-LNX-01 asks whether a harmless behavioural self-test can back the list.

**`exec-init` memory.** The Linux guard role of the same binary measured 8.18 MB private ([15](15-performance-targets.md) §2), so a fixed 8 MiB gate would probably fail. The target is **measured in LAB-LNX-19, with headroom, and recorded in [15](15-performance-targets.md)** as the Linux per-confined-attempt overhead (today "Linux 0 per execution"; §15.4). Decision order: keep `exec-init` at the measured target; otherwise RM-14 (a separate small executable, still C#); the bwrap-init fallback (`exit_fidelity = SHELL_ENCODED`, with the loss of signal identity and in-view end steps) only if neither is acceptable. `exec-init` memory counts in `accounted_mem_bytes` and admission.

**Delivered as delegation:** the view is the distribution's bwrap, never embedded or installed ([05](05-toolchains-caches.md) §1 stays true for it); Flatpak is DELEGATED, its sandbox reported, never claimed; distribution packages are OBSERVED; SELinux and AppArmor are host facts.

**Reported as unavailable:** BPF unit options in user units (ignored with a warning, D-lnx-kernel-8); per-destination IP filtering without root; X11 GUI isolation; Landlock denial evidence for an unprivileged node (D-lnx-kernel-12); namespaced tiers on default Ubuntu 24.04.

**Minimum viable step.** The view chain with N0 and no bus, for headless COMMAND and SERVICE attempts on hosts whose probe passes; ephemeral-state profiles elsewhere; the Landlock-only tier, labelled with its escape gap, on Ubuntu 24.04 without the profile.

**Gates:** LAB-LNX-01, LAB-LNX-19 (`exec-init` at its measured target; exact exit and signal posture), LAB-LNX-02 and LAB-LNX-21.

**Delivery venue.** The owner-updated WSL Debian distribution (WSL2 evidence only), or a VM venue that [AD-0002](../decisions/AD-0002-platform-scope.md) admits and the verification lanes can reach. `ArcForgesTest` is reserved for installation and Secret Service tests and is not a development venue. Ubuntu rows are acceptance-register items.

**Further prerequisites:** AF-SEC-01 (peer identity for the clamp) and AF-TOOL-01 (adapter cache and tool-home knowledge for grant allowlists) delivered; a test-residue rule for transient units and slices in the style of [AD-0016](../decisions/AD-0016-local-first-verification.md) §5 (bounded churn, exact-name cleanup, never at scale); the .NET facts the chain relies on (no default SIGTERM handler; `SIG_IGN` surviving `execve`) recorded as version-tracked facts in the AOT verification table.

### 5.3 macOS (RM-15; EX-22 for Seatbelt)

The product owner asked for a deliberately lightweight macOS strategy. The evidence supports going lighter still.

**RM-15: the monitored local node (stage 1, accepted on request §3).**

| Element | Reported as | Privilege |
|---|---|---|
| The node as a user LaunchAgent: Developer-ID signed, notarized, at a stable bundle path (D-macos-32) | — | P3, ArcForges' own signing |
| One session per attempt; a holder; rlimits (CPU, FSIZE, NOFILE); QoS and I/O tier; node-monitored memory and process counts | `cpu`, `memory`, `pids`, `io` **OBSERVE_ONLY**; per-process `RLIMIT_CPU` and `RLIMIT_FSIZE` PARTIAL; **no aggregate or rate enforcement** (D-macos-15); `pause=UNSUPPORTED`; `kill_tree=BEST_EFFORT`; `restart_survival=false` until LAB-MAC-04. `R-RES-008` refuses aggregate CPU and memory requirements | P0 |
| App Sandbox, TCC, Gatekeeper and SIP of vendor apps | Reported, never claimed (D-macos-1, D-macos-4, D-macos-5, D-macos-6) | P0 |
| **TCC attribution** | **`tcc_attribution = NODE (aggregating)` by default.** Without responsibility disclaim, the LaunchAgent node is the responsible process, so grants the owner gives at prompts raised by one managed tool (Documents, Desktop, Downloads, volumes, camera, microphone, Local Network) apply to every later tool. The node never holds Full Disk Access or App Management, and its data root stays outside protected folders. Disclaim (a private SPI, UNDOCUMENTED) is PREFERRED only, and the word "non-aggregation" is used only when disclaim is active and probed | P0 |
| First screen and `GetReleaseScope` | "macOS is the weakest of the three nodes." "TCC grants given to prompts raised by managed tools are held by ArcForges and apply to every later tool; decline such prompts unless you intend that." The doctor reports the TCC categories the node holds, where detectable. A stage-1 switch refuses, or asks for the owner's acknowledgement for, workspaces in protected folders | P0 |
| Apple `container` for Linux workloads | EX-18 (and weighed in EX-22) | The owner installs (P1) |

- **LAN:** server-side TLS 1.3 in .NET is "not before .NET 12, and not committed then" (D-macos-31). An outbound-only LAN client is an alternative in G35's question (LAB-MAC-12). The macOS LAN stage also depends on the disclaim decision and on Local Network inheritance.
- **Open question for RM-15:** disclaim by default (UNDOCUMENTED, never satisfying REQUIRED) or no disclaim with the aggregation disclosed (§17).
- **Prerequisites:** owner decision D4 (an Apple-silicon lab Mac and the Apple Developer Program); the AD-0002, AD-0012 and AD-0016 amendments of 2026-10-19; a third `IExecutionPlatform` implementation.
- **Gate:** G25, which holds no Seatbelt leg, so that the accepted node never waits on Seatbelt labs: LAB-MAC-02 (its TCC-attribution and Local Network legs), LAB-MAC-03 (headless TCC prompts), LAB-MAC-04, LAB-MAC-06 to LAB-MAC-09 and LAB-MAC-15's audit-token leg. LAB-MAC-01, LAB-MAC-02's Seatbelt leg and LAB-MAC-15's Seatbelt legs belong to G41 (EX-22) only. **Narrowing question** for G25: does a monitored node add enough over "macOS as a control client plus Linux workloads in Apple `container`"? That is a question for the owner if G25 shows little value, never a design consequence: request §3 makes macOS an execution target.
- **Hostile input on macOS:** with one signed binary, no role can be App-Sandboxed while the node is not, so acquisitions that need extraction are UNAVAILABLE on macOS until an App-Sandboxed helper executable exists. That is a second signed binary, which RM-14 does not cover today: it would need RM-14's Item widened, or its own row ([AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §1).

**EX-22: Seatbelt profiles (exploratory).**
- **Question:** do deny-default profiles, run by the owner's choice through the absolute `/usr/bin/sandbox-exec`, add measurable value for MCP servers and hooks over the clients' own Seatbelt sandboxes, at an acceptable per-release cost? Apple `container` for cross-platform class-1 servers (Node, Python) is weighed as the alternative.
- **Values** (attainable, pre-lab): `api_status=DEPRECATED` on every cell; REQUIRED satisfied only with a local `accept_deprecated`, a passing host probe **and** `min_strength=PARTIAL`. No wildcard `mach-lookup` unless HUMAN policy sets it.

| Dimension | EX-22 value | Deciding lab |
|---|---|---|
| `fs.read`, `fs.write` | PARTIAL ("self-check passed") | LAB-MAC-01 |
| `config` | N/A: preferences are files on macOS, folded into `fs` | — |
| `net.out` | PARTIAL; a localhost proxy matches every local address | LAB-MAC-01 |
| `net.in` | Unmeasured (E5) until LAB-MAC-01's TCP and UDP listen leg | LAB-MAC-01 |
| `ipc` | PARTIAL: the per-version Mach allowlist; every allowed service not shown to enforce the caller's profile is a gap | LAB-MAC-15 |
| `devices` | Unmeasured; no device claim until a lab measures it | LAB-MAC-01 |
| `creds` | PARTIAL: credential files by `fs` rules; the Keychain through an allowed Mach service is a gap unless denied | LAB-MAC-01, LAB-MAC-11, LAB-MAC-15 |
| `persist` | PARTIAL at best (brokered services below) | LAB-MAC-15 |
| `exec`, `exec.elevation` | `exec` PARTIAL by process-exec rules; `exec.elevation` unmeasured | LAB-MAC-15 |
| `visibility` | NONE: no process namespace | — |
| `res` | As RM-15: OBSERVE_ONLY, per-process rlimits PARTIAL | LAB-MAC-04 |
| **Launcher cells (escape class)** | Any allowed launch- or write-brokering Mach service (Launch Services, launchd job submission, Apple Events), and any allowed service not yet measured: escape gaps of the realization, so every dimension then holds against {A1, A2} only (§3.2) | LAB-MAC-15 (broker leg) |

- **Verification:** the chain `sandbox-exec -p <profile> arcforges exec-final -- <workload>`, whose in-profile self-check probes canary denials (a write outside the root, a protected read, an external connect); PARTIAL ("self-check passed"), never ENFORCED. `identity_strength` is capped at PARTIAL.
- **Brokered Mach services:** anything allowed through `mach-lookup` runs outside the sandbox (D-macos-10). The macOS weakest-run rule also requires a per-version allowlist with no launch- or write-brokering service (Launch Services, launchd job submission, Apple Events); every allowed service not shown to enforce the caller's profile is a gap; macOS `persist` is PARTIAL at best.
- **Gates:** G41: LAB-MAC-01 (with the TCP and UDP listen leg), LAB-MAC-02's Seatbelt leg, LAB-MAC-11, LAB-MAC-15's Seatbelt legs (with a broker leg) and the macOS Seatbelt corpus of LAB-X-01; LAB-MAC-10 for the Apple `container` alternative.
- **Prerequisites:** RM-15 delivered; EX-07 stage b, promoted together if EX-22 is the first confined backend; EX-09 for node reach.
- macOS confined widenings are local-only.

### 5.4 Android, iOS and the Web: control clients only

**Why clients:**
- The request makes it final (request §3).
- None of the three can host the mechanisms this direction rests on (user-scoped transient units, job objects, AppContainer, bwrap).
- Their value is that they sit *outside* the managed machine, which is exactly where an approver belongs, once its decisions are signed end to end (EX-23).

**What they do:**
- **View** canonical summaries (D1), inventory counts and findings. Destinations, paths and command lines are D2 and appear only on explicit request where the node's privacy policy allows; destinations, inventories and denials need a **separate toggle** (§10).
- **Narrow** at MEDIUM risk: revoke a grant, close an envelope, freeze, stop.
- **Decide captured approvals that are not widenings or installs**, under today's rules ([11](11-security-privacy.md) §1).
- **Access-profile widenings and installs will be decided locally only until end-to-end approval signatures exist** (a device-bound phone key enrolled with and pinned by the node, verified over the approval digest; EX-23). After that, a widening is remote-eligible only if no element of its delta is on the never-remote list. **Release 1 is unchanged:** its opt-in remote approval path (`remote.allow_approvals`, default false) stays as designed and is covered by T-11 as amended; widening-class approvals do not exist before EX-07 stage b, and the future refusal of REMOTE for them is a contract change of `DecideApproval`, recorded with EX-07 stage b.
- **Never remote:** accepting a deprecated or experimental basis; accepting a downgrade; editing profiles, templates or the protected control set; adding an external path; running `recover`; trusting a new backend; any macOS confined widening.

**Editions.** Remote decisions are Pro (cloud) by the existing rule. Every local capability, confinement included, stays free, and no local default may depend on a remote decision (§7.6). Whether a LAN-only approval path from the phone would be free under [AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2 is an owner question (EX-23; §17).

## 6. Lifecycle (proposed)

All of this section is proposed model (EX-13, EX-15, EX-16). ArcForges' own uninstall, corrected on 2026-10-19 ([AD-0012](../decisions/AD-0012-distribution-and-updates.md) §2), is release-1 design and is not restated here.

### 6.1 Levels and methods

The **level** is OWNED, DELEGATED, OBSERVED or EXCLUDED. The **method** is a separate field inside the level.

| Level | Meaning | Methods | What ArcForges states |
|---|---|---|---|
| **OWNED** | ArcForges placed the software in managed roots and can remove exactly what it wrote. **Relocatable software only** | Portable archives and single binaries; digest-pinned MCPB and direct binaries; ecosystem tools in an owned, versioned prefix (`dnx`/NuGet first, then npm/pnpm with a prefix, uv/pipx, `cargo --root`); AppImage through trusted extraction; later, portable applications including a macOS portable `.app` (EX-13, later stage) | Exact removal of journal entries and owned roots; residue per the weakest-run rule; version rollback by pointer |
| **DELEGATED** | Another manager owns install, update and uninstall | winget installer packages; Flatpak `--user`; Homebrew; possibly mise or aqua inside an acquisition attempt (an EX-13 stage b alternative); later, vendor MSIX (EX-21) | The manager's own guarantees, quoted, never restated as ArcForges' own. Rollback is the manager's, or NONE. ArcForges **reports** the `update_owner`; it does not run installs on the owner's behalf by default |
| **OBSERVED** | Installed outside ArcForges; inventoried only when the owner enables it | ARP entries, distribution packages, Snap, `.pkg` receipts, vendor self-updaters | Presence only |
| **EXCLUDED** | Not supported, with the reason stated | Machine-wide installers and services, drivers, root maintainer scripts, repackaging, portable services, sysext/confext | The reason |

**Excluded software is not banned.** It still runs as an ordinary task with containment and records, labelled `UNMANAGED` for lifecycle and NONE for access.

### 6.2 Acquisition events

**Launching is installing.** For `npx -y`, `uvx`, `pnpm dlx`, `bunx`, `dnx` and `docker run`, the client configuration (an argv, usually unversioned) is the only manifest.

The model is: spec → resolve → fetch → verify → materialize → cache → bind → run (D-acquisition-runtimes-1), realized with existing parts:
- **resolve, fetch and verify** run as an **acquisition attempt** under its own profile: writes only to staging and, where N1 exists, registry-only egress;
- **materialize** writes a read-only version directory (the layout of [AD-0012](../decisions/AD-0012-distribution-and-updates.md), generalized);
- **cache** uses the CAS, by digest;
- **bind** is a journal entry, for example the MCP configuration rewritten to `arcforges mcp-wrap --acq <id>` with an exact diff;
- **run** is a `SERVICE` or `COMMAND` task that references the Installation.

**The OS gates stay effective** (D-win-install-34). ArcForges sets Mark-of-the-Web (the zone of origin) on Windows and `com.apple.quarantine` on macOS on every executable it fetches or extracts, or records an equivalent reputation or signature check as provenance. It never strips either mark. A Smart App Control or Gatekeeper block is a reported refusal (`blocked by OS policy`), never retried without the mark. The OS verdicts become recorded supply inputs. The compatibility cost (Smart App Control blocks unsigned tools; Gatekeeper prompts for or translocates un-notarized CLIs) is stated in §11 and measured in LAB-X-04 and LAB-MAC-14.

**Stages:**
- **Stage a (EX-13): O1 observe** (parse client configurations and launcher caches) and **O2 pin** (a consented rewrite: `pkg@x.y.z`, `@sha256:`, `uvx --no-build --exclude-newer`) (D-acquisition-runtimes-2, -3). They need no amendment, give an honest OBSERVED or GUARDRAIL statement at P0, and use the existing IntegrationService.
- **Stage b (EX-13): O3 the tool store, and O4 split acquisition and run profiles.** They need the no-install amendment of [05](05-toolchains-caches.md) §1 (§15.1), effective at stage b's promotion; `requirements.md` stays unchanged. Stage b also needs a helper-role profile that realizes ENFORCED for `fs`, `net` and `ipc` on that OS. **Alternatives for stage b**, weighed at promotion, each with its maintenance burden:
  1. an OWNED store across `dnx`/NuGet, npm/pnpm, uv/pipx and `cargo --root`: per-ecosystem launcher drift, rated M–H;
  2. DELEGATED to mise or aqua, run inside an ArcForges acquisition attempt under O4: mise covers these backends, verifies checksums, cosign, minisign, SLSA and GitHub attestations, and applies a default release-age cooldown (D-x-lifecycle-7); ArcForges tracks one manager's behaviour instead of several ecosystems;
  3. a hybrid: delegated resolution, OWNED materialization by digest.
- O4 becomes a **default** only when LAB-X-04 reaches at least **80 %**; between 60 and 80 % it stays opt-in; below 60 % it is not recommended (D-acquisition-runtimes-5).
- **Later stage: OWNED portable applications** (lifecycle only; their residue is "Not known" while they run unconfined). This is a lifecycle stage, not GUI confinement.

**The acquisition record** holds the version, digests, the scripts that ran, the interpreter, the provenance inputs, the OS gate verdicts, the cooldown decision, the hosts contacted (where N1 measured them) and the acquisition attempt ID.
- Provenance (npm provenance, PEP 740, crates.io trusted publishing, NuGet signatures, cosign), OS verdicts and cooldown are **recorded inputs, never safety claims**.
- No online provenance lookups by default, for privacy (§10).

### 6.3 One host-write journal

One journal (EX-08) records every host change ArcForges makes, generalized from `integration_write`. Each entry has:
- a writer kind: `INTEGRATION`, `SELF_INSTALL`, `INSTALLATION`, `CONFINEMENT_OBJECT`, `PERSISTENCE_HOLD`;
- a target, named exactly;
- the prior state, or "absent";
- the new state's digest;
- the owner and the actor, with `provenance_strength`.

Rules:
- Uninstall, recovery and reconciliation replay it backwards.
- An offline `arcforges recover` role can replay it with the node down. It replays only recorded entries, and only for a HUMAN caller (T-40).
- It never records secret values.
- An owner-prompted privileged step ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), boundary 2) is a journal entry with its exact removal.
- ArcForges' own setup becomes a `SELF_INSTALL` writer.

### 6.4 One update owner

`install_source` ([AD-0012](../decisions/AD-0012-distribution-and-updates.md) §4) would become `update_owner` at EX-13 stage b, with **exactly one recorded owner** per Installation:
- **ARCFORGES:** OWNED; the AD-0012 switch, health check and rollback apply.
- **MANAGER:** winget, Flatpak, Homebrew, or a delegated tool manager; ArcForges reports and records.
- **VENDOR:** Squirrel, Velopack, Sparkle, the Electron updater; ArcForges reports.

Classification happens before installation. **A self-updating application cannot be OWNED**: its updater replaces the install root, which is incompatible with read-only version directories (D-acquisition-runtimes-20). The choice is DELEGATE, with rollback NONE, or REFUSE. ArcForges never forcibly disables a vendor updater.

### 6.5 Rollback: versions versus data

| What | Possible when | Mechanism | Stated as |
|---|---|---|---|
| **Version** of an OWNED installation | While the previous version is kept (the last two, as in AD-0012) | A pointer switch (junction retarget, L-16; symlink rename), health check, automatic rollback | "Program rolled back" |
| **Version** of a DELEGATED installation | Only if the manager supports it (Flatpak `--commit`, Podman by digest; not Homebrew) | The manager | Quoted |
| **Data** in an owned state root | Only from a snapshot taken while the workload was STOPPED or FROZEN (Linux freeze, E1; Windows has no freeze, so STOPPED only) | The clone primitive (reflink, block clone, `clonefile`, else copy) into quarantine-managed storage (EX-16 stage b) | `consistency` STOPPED or FROZEN; `LIVE_UNSAFE` only on the owner's explicit acceptance |
| **Data** outside owned roots, OS credential stores, app-migrated schemas without a prior snapshot | Never | — | "Not restorable" |

**A version rollback never implies a data rollback.** When the profile marks a state root owned, the update switch takes a STOPPED snapshot first. Snapshots are opt-in and size-bounded, never a default.

### 6.6 Honest uninstall: a three-part result

An uninstall is a two-phase cleanup plan ([06](06-storage-workspaces.md) §7, SPECIFIED) over the Installation's journal entries (reversed), its owned version directories and state roots, and its owned OS objects (for example `DeleteAppContainerProfile`). It also lists **observed residue candidates** from the per-attempt persistence diff and the view's granted-directory diff, removable only by a HUMAN choice. Execution moves files to a 24-hour, restorable quarantine, an "undo uninstall"; **D3 material (derived credential copies) never enters it**, and a purge-now path exists.

The result always has three parts:
- **Removed:** everything ArcForges wrote, listed.
- **Left in place:** what the owner chose to keep, for example the state root.
- **Not known:** what the application may have written elsewhere, **including any writes of an elevated run, which land in another account's profile**.

**The weakest-run rule** decides whether "Not known" may say "none outside the recorded grants". It may only if **every** run of the installation was a verified confined attempt, under per-OS conditions:

| OS | Condition for "none outside recorded grants" |
|---|---|
| Linux | Every run was a view-chain attempt with `view.fs` read back and a private HOME |
| Windows | Every run was W2/W3 with the composite read-back accepted (§5.1), the WSL leg denying, and the AppContainer profile storage recorded and removed as an owned object. AAP-writable locations are listed as a gap |
| macOS | Only read-narrow Seatbelt runs (EX-22) with a broker-free Mach allowlist for that macOS version; never read-broad. The RM-15 node has no confined tier, so the statement is always "Not known" |

Otherwise the installation carries `ran_unconfined = true` and the statement is "ArcForges removed everything it wrote; the application may have written elsewhere; observed candidates: …". **`ran_unconfined` is a durable installation summary that `PurgeTaskRecord` cannot delete; a missing history counts as unconfined.**

DELEGATED uninstall quotes the manager. OBSERVED software has no uninstall through ArcForges.

### 6.7 Privileged installers

- **ArcForges never elevates an installer on the host.**
- **Signals before the run:** error 740 (partial: self-elevating installers never return it, D-win-install-17); static inspection (D-win-install-21); winget's `ElevationRequirement`, which is under-declared.
- **During the run:** a UAC prompt, where one appears, is the owner's decision. On an administrator account without Administrator protection, elevation may happen silently. Resulting changes are seen by standard-user detectors inside the attempt window, attributed "cause unknown" unless the attempt's elevation was observed. The elevated run's per-user writes land in another account's profile, which a P0 node cannot read.
- **Administrator protection** is reported as a host fact. Microsoft advises against it on devices that need Hyper-V (D-win-strong-14), which bears on owner decision D1 and on EX-18.
- **Assessment** in Windows Sandbox (`VM_CAPTURED`) is EX-18; Windows Sandbox is not available on Home (D-win-strong-2).
- **Linux:** distribution packages and Snap are OBSERVED, and DELEGATED only with administrator approval per transaction.
- **macOS:** root `.pkg` installs are OBSERVED only.
- **Confined profiles close one route.** They hide the system bus, so polkit-authorized installs are not reachable from a confined attempt; otherwise the realization reports `exec.elevation = REACHABLE`.

## 7. Policy, identity and agent autonomy (proposed)

All of this section is proposed model (EX-07 stage b, EX-09, EX-14, EX-23). The release-1 statements are those of the [product definition](../product/product-definition.md) §9 and [11](11-security-privacy.md) §1.

### 7.1 Two planes

- **The permission matrix** (AF-SEC-01, PLANNED) decides **who may change** grants, profiles and approvals. It is keyed by origin, and origins are guardrails.
- **Grants** decide **what a workload may access**. They are typed and closed, node-held in `PolicyDocument`, and evaluated in node C#.
  - They borrow Cedar's semantics, not its engine: default deny in confined profiles, forbid wins, a closed schema, templates and decidable subset checks (D-x-lifecycle-37). **There is no policy language or engine.**
- **Grants name things, not raw paths.** The path classes are `workspace:<id>`, `state_root:<installation>`, `managed:<root>`, `cache_partition:<p>`, `toolchain:<id>` (from adapter knowledge) and `user_path:<path>` (HUMAN only; on Windows copy-in, copy-out or refused). Credentials are catalogue names, never paths. The node compiles names into OS rules per backend: capability SIDs or ACEs (§5.1), bwrap binds, Landlock rules, SBPL `literal`/`subpath`.
- **The compiler's link-safety rule.**
  - Linux: resolve with `openat2(RESOLVE_BENEATH | RESOLVE_NO_SYMLINKS)` and bind by descriptor (D-lnx-projects-26).
  - Windows: open with `FILE_FLAG_OPEN_REPARSE_POINT`, refuse reparse points and files with a link count above 1, and apply ACEs through the handle (`SetSecurityInfo`), never by name.
  - Re-validate at apply time. T-29 covers policy-input injection and link substitution.
- **The always-forbidden set** is at least the union of today's set and the `srt` and Codex protected-path lists (D-x-agents-15). **It is relative to the grantee:** no grant to any attempt may include these paths, **except** that an AI client's own configuration, state and credential may be granted to **that client's own confined attempt** (its Installation or session envelope) by a recorded HUMAN approval, and never to its tools or MCP servers. The set:
  - `creds.internal`; the data root's `store` and `run`: **forbidden to every attempt, the client's own included**;
  - the AI client's own configuration and state, and project-scoped client configuration: `.claude/` (commands and agents), `.codex/`, `.agents/`, `.mcp.json`: forbidden except to that client's own confined attempt, as above;
  - `.git/` metadata, in particular `.git/hooks` and `.git/config`, and `.gitconfig`: `.git/hooks` **forbidden to every attempt, the client's own included**;
  - shell rc files and profiles (`.bashrc`, `.zshrc`, `.profile`, PowerShell profiles): **forbidden to every attempt, the client's own included**;
  - IDE project configuration: `.vscode/`, `.idea/`;
  - cloud CLI configuration such as `.aws/`.
- **The client's own credential** (an API key or sign-in token, in its configuration or an OS store) is a `creds` grant to that client's own confined attempt only, by recorded HUMAN approval, and it carries its exposure statement: with the model service reachable through `net.out`, "exfiltration possible to <the client's model service>" (§3.5). A disclosed credential is UNREVOCABLE (§7.4).
- **Delayed execution of confined writes.** A confined attempt can still write files in granted roots that unconfined processes run later: build and test scripts, CI workflows, `.envrc`, instruction files for later agent sessions. Every realization with a writable grant carries the gap "writes to granted roots may be executed later by unconfined processes". The granted-directory diff records **workspace provenance** (attempt and profile digest). At EX-09's promotion the Design decides between a finding and the writer's profile as a floor for an UNCONFINED task over unreviewed confined writes (T-42). Session worktrees with review before landing (EX-16) are the practical answer.
- **The protected control set** (lock-out rules) is a set of `ValidatePolicy` rules of EX-07 stage b: no profile may deny the node endpoint to HUMAN clients; and **a profile for an AI client that ArcForges launches as a confined attempt** may not deny that client the grants of its own configuration, state and credential that the grantee-relative exception above allows, unless explicitly flagged. With the two rules consistent, a valid profile for a confined AI client exists: the client's own items granted to the client's attempt, nothing of the set granted to its tools or MCP servers, and the entries forbidden to every attempt never granted.

### 7.2 Identity and inheritance

Each attempt has one identity, attested at the strongest available level:
1. **the attempt endpoint:** a pipe DACL with the leased AppContainer SID; a socket bound into the view by directory; a Seatbelt `literal` path (a DEPRECATED basis, capped at PARTIAL);
2. **token facts** read from the process handle the LocalRpc resolver already holds (Windows); `SO_PEERPIDFD` → `GetUnitByPIDFD` (Linux); `LOCAL_PEERTOKEN` (macOS);
3. job or cgroup membership, for attribution only;
4. the PID and the client hello, which are ASSERTED.

**No sandbox decision rests on a PID.** `ActorRef.identity_strength` records which level held, with its basis and the qualifier of §4.1.

**Policy authorship has a strength too.** Every policy revision and approval decision records `provenance_strength`: ASSERTED, GUARDRAIL (a HUMAN-classified local client: forgeable by same-user code, [11](11-security-privacy.md) §1) or ATTESTED (a mechanism same-user code cannot satisfy; none exists yet, and EX-23 researches OS-attested presence). It feeds the A4 rule of §3.2.

**Per-agent and per-application OS identities exist only where the OS supplies them:** a leased AppContainer identity per running attempt; a bwrap view's user namespace; possibly later OS agent accounts (EX-18, tracked only). ArcForges does **not** create OS accounts with held passwords (D-win-strong-1).

**The inheritance invariant R1–R7** (D-identity-ipc-completion-10; §1.4):
- A task submitted from attempt A runs with `meet(requested, profile(A))`, including the requirement fields; its grants are a subset of A's, and it is charged to A's envelope.
- A caller whose foreign confinement the node cannot map is refused or routed to a local HUMAN.
- Calls from inside any attempt are **never HUMAN**.
- R5 is changed for remote: widening is decided by a **local** HUMAN only, until end-to-end approval signatures exist (§7.5).
- The rule is ENFORCED only where the identity is ENFORCED.

**The floor per client and route.**
- **Primary:** a **HUMAN-set floor per client and route**, chosen at integration time in the IntegrationService consent step (for example "commands from Claude Code's MCP route run at least under profile `agent-default`").
- **Refinement:** a client-declared floor, such as Codex's experimental `sandbox-state` (cooperating servers only, D-x-agents-14), is honoured as a minimum on top.
- **Clients that declare nothing** (Claude Code today, D-x-agents-18): the HUMAN-set floor applies. If the owner set none, the route is UNCONFINED, the consent text and the realization say so ("client sandbox unknown"), and nothing is inferred as confined.
- **PEER origin:** a PEER-origin profile floor for placed work, once a confined backend exists.
- **Later stage:** the AI client itself runs as a confined `SERVICE` attempt in its session envelope. Its file tools, hooks and MCP servers then run inside a boundary; its calls are never HUMAN (R6), which removes most of the HUMAN-forgery path for that client; and the routing gap closes without client cooperation. Until then the agent story stays "commands routed through ArcForges run without …".
  - **Prerequisite:** a **terminal-attached attempt mode**, or an equivalent. The clients are interactive terminal programs; M1 offers only the `COMMAND` and `SERVICE` kinds, [08](08-ai-integration.md) §4.1 passes "interactive programs that need a terminal" through unrouted, and the view chain's `--new-session` detaches the controlling terminal. The mode keeps a pseudo-terminal owned by the holder or `exec-init`, relayed to the owner's terminal, with the terminal-injection filter kept. It is checked against M1 (a mode of the existing attempt, not a new runtime) and M5 (no new concept).
  - **Grants:** the client's own configuration, state and credential under the grantee-relative exception of §7.1; model-service egress per `net` option; its MCP servers and hooks inside the same envelope.
  - **Gate:** LAB-X-03 (the clients' own sandboxes nested inside an ArcForges tier) **and** a dedicated leg, "the AI client itself as a confined attempt" (LAB-X-19), on W2/W3, the Linux view chain and macOS. It measures interactive use, model-service egress per `net` option, the client's credential and configuration grants, its MCP servers and hooks inside the same envelope, and nested client sandboxes.
  - **Until LAB-X-19 has run, this stage's feasibility is unexamined (E5).**

This keeps `arcforges run` and the MCP adapter usable from inside a confined agent without a confused-deputy hole, and it is the fix for the routing gap: **isolation-preserving routing** (EX-09). Agent-facing envelope introspection through the MCP adapter lets an agent read its own realized profile, remaining budget and dry-run answers, and request a widening before failing.

### 7.3 Delegation, approvals and the envelope

- **Delegation is attenuation only:** path-prefix containment, a port-set subset, an earlier expiry, decided by the node.
- **Widening** is a separate operation:
  1. an AGENT requests it;
  2. the request returns `AUTHORIZATION/approval_required`;
  3. the approval captures the profile delta;
  4. a **local** HUMAN decides (§7.5);
  5. the task runs under the original `command_id`.
- **Approval integrity:**
  - the digest covers the effective profile, floors, requirement fields, grants and acquisition digests;
  - the view shows the realization this host will produce, and **the exact grant delta at D2** to the approver; where a privacy toggle would hide D2 from a surface, the approval is decided locally;
  - widening approvals have a short TTL;
  - a decision that arrives later is re-validated against the current probe.
- **The delegation envelope** is a policy record in `PolicyDocument`, keyed by session: grants, expiry, workspace and action budgets, plus a resource budget.
  - The resource budget is realized by admission (`max_running_per_session` maps additively, AF-SCHED-01), and by a **group container** only where three-level containers are proven (LAB-WIN-02 with the two-to-three-level runtime transition; LAB-LNX-13). On macOS it is monitored only. The envelope's grants, expiry and revocation need no container.
  - Inside the envelope the agent acts freely; at its edge it requests.
  - **Action budgets are a later stage of EX-14:** approvals requested per hour, grant widenings, distinct N1 destinations, acquisitions. Exhausting one pauses submission with `AUTHORIZATION/budget_exhausted` and notifies the owner. **It never auto-approves.**
  - The SESSION kind only; the APPLICATION kind is dropped until it has a second use. The shared-SERVICE rule is in §2.3.
  - **Question:** should owner-scoped profile templates replicate across the owner's paired machines over the existing LAN pairing, with each node still realizing and refusing locally? It is free under [AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2 and is not team policy (team administration stays its own accepted roadmap row).

### 7.4 Revocation classes

| Class | Mechanisms |
|---|---|
| IMMEDIATE | Mediated channels (proxy, brokers, attempt endpoint), resource limits, freeze, holds |
| NEW_ACCESS_ONLY | ACE removal: handles already open survive |
| RESTART_REQUIRED | AppContainer capabilities (including per-root capability SIDs), Landlock, seccomp, bwrap views, Seatbelt |
| UNREVOCABLE | A disclosed secret: rotate it at the issuer |

**Design consequence.** `SERVICE` tasks receive sensitive access **only** through IMMEDIATE-revocable mediated channels, subject to the restart constraint of §2.5.2. `COMMAND` attempts may use RESTART_REQUIRED mechanisms. The `ExplainTask` dry run states the class of each grant.

### 7.5 Remote and LAN

- Remote **narrows** at MEDIUM risk.
- Remote **widening and install decisions will be local-only** until end-to-end approval signatures exist (EX-23): today a remote command is signed by the cloud's command key ([AD-0009](../decisions/AD-0009-cloud-relay-and-cost-controls.md) §5), so a compromised key could issue any command the node's local policy permits (T-11 as amended). `allow_lifecycle_approvals` is not in the contract sketch. Release 1's opt-in remote approval path is unchanged; the refusal of REMOTE for widening-class approvals is a `DecideApproval` contract change of EX-07 stage b (§5.4).
- Once EX-23 exists, a widening is remote-eligible only if no element of its delta is on the never-remote list (§5.4).
- Remote **never originates** a widening, an install or a profile change.
- **LAN peers are never approvers.** A placement to a peer re-realizes the profile under the **target's** policy and capability report, and is refused if a REQUIRED dimension cannot be met there. Isolation-aware placement is a new feasibility input to [AD-0008](../decisions/AD-0008-lan-trust-and-placement.md) §5 (EX-04). Peers receive only the D1 realization summaries of attempts they placed and capability summaries for placement (§10, principle 5).

### 7.6 The editions check

**Rule:** the local approval queue (Desktop, CLI), the envelope and confirm-or-revert must on their own make every local default usable. **No local default may require a remote decision.** Unattended widening requests wait in the local queue; a push notification of a pending request and remote decisions of other approvals are the Pro convenience on top; nothing is ever auto-approved. Because remote widening decisions do not exist at all before EX-23 (§7.5), this rule holds by construction. It is an acceptance criterion for any CONFINED default (§14.1).

## 8. Channels (proposed)

Three principles hold throughout: **deny by inclusion** in CONFINED profiles; **mediation only through the attempt endpoint**; **report the minimum** of the mediation strength and the tier strength. All values are attainable and pre-lab.

### 8.1 Network

| Grant | Windows (W2/W3) | Linux | macOS (EX-22) |
|---|---|---|---|
| `net{none}` | Deny of own sockets, loopback included; service-mediated egress unmeasured (LAB-WIN-04, LAB-WIN-09); live canary probe | N0: bwrap `--unshare-net` plus the read-back address-family allowlist. Landlock-only tier: PARTIAL (TCP ports, ABI ≥ 4), or a real deny if the socket-family policy filter of §5.2 holds | PARTIAL: Seatbelt `(deny network*)`, DEPRECATED |
| `net{proxy, destinations}` | **Not offered.** No documented OS-forced egress path; PSEC is EX-17 | MEDIATED: N1 (EX-12). Needs a network namespace: unavailable on Ubuntu 24.04 by default and without user namespaces | PARTIAL: a localhost proxy, where `localhost` matches every local address |
| `net{open}` | PARTIAL (`internetClient`: no network or full network) | NONE: the shared network namespace, reported "unrestricted"; it also opens host abstract sockets below ABI 6 (§5.2) | NONE |
| `net.in` | Deny without server capabilities | Deny under a network namespace | Unmeasured (E5) until LAB-MAC-01's listen leg |

**Observation at P0:** Windows `GetExtendedTcpTable` samples (they miss short-lived connections and carry no bytes); Linux N1 destinations measured; on every platform, listeners opened by an attempt are detected. The product definition §9 gap "Network use per process (inferred only)" would become **per tier** when EX-12 is promoted (§15.2).

**Not built:** firewall rules, WFP filters, callouts, Network Extension, BPF unit options, seccomp notification on `connect`, a filtering MITM.

### 8.2 Credentials

**The release-scope sentence, true today and already stated** ([product definition](../product/product-definition.md) §9): *"Unsandboxed managed processes can read every credential the signed-in user can read. ArcForges does not read or record them."* The future clause "and offers confined profiles that hide them" is added only when a confined backend is promoted.

- **Confined tiers would build their view by inclusion.** The user's home, OS secret stores, agent sockets and browser profiles are absent unless granted.
  - On W2/W3, Credential Manager and DPAPI are PARTIAL until LAB-WIN-04, and conditional on the WSL leg.
  - On WSL, the bridge keeps the view PARTIAL until LAB-LNX-05.
- **Internal secrets are never granted** (§3.2).
- **Delivery, staged** (EX-12):
  1. sealed task secrets (DELIVERED) by environment, with per-adapter hook labels `HONORED`/`BEST_EFFORT`;
  2. read-only derived-file grants: a per-attempt copy, never an ACE on the user's file. **Derived copies are D3 at rest: never quarantined, snapshotted, exported, archived or transferred; deleted at attempt end with a journal entry**;
  3. agent and helper-protocol brokers (an ssh-agent filter; git, Docker and AWS `credential_process`; Cargo helpers) on the attempt endpoint, under the helper-role profile (MEDIATED);
  4. a later research stage: proxy header injection with a per-attempt, memory-only, name-constrained CA for inject hosts only, and hardware-bound keys (LAB-X-17; the key-class leg of LAB-WIN-04).
- **Every delivered credential carries an exposure statement:** with a `net.out` that is not ENFORCED-deny, "exfiltration possible to <scope>", and a disclosed value is UNREVOCABLE.
- **Never granted:** browser profiles, the user's whole OS store, the login keychain.
- **Policy names credentials, not paths.** AGENT-origin tasks get none unless one is named.

### 8.3 IPC and service reachability

- **The user-wide node endpoint stays closed to every confined tier that can hide it:** the view chain (by mount), W2/W3 (by DACL), and Landlock at ABI 9 or later. A confined attempt reaches ArcForges only through its attempt endpoint: S5' (the node API, under inheritance), S3' (the cache store), S2' (the sccache server, **inside the same profile**, because compile-time code runs in it), brokers, and on Linux the TCP-to-UDS relay for attempts in a network namespace.
- **Exception, stated:** in the **Landlock-only tier below ABI 9**, the node's pathname socket, the session bus and the systemd private socket stay reachable. The node then identifies the caller by peer cgroup identity and applies the **mandatory inheritance clamp** (`node_endpoint_hidden=false`; D-identity-ipc-completion-7), and the realization carries the escape gap.
- **SR-1: isolation wins over cache.** An unreachable service is `UNAVAILABLE(reason)`, and the run proceeds uncached.
- **Service discovery between managed workloads** uses node-injected endpoints only. A workload granted `ipc{service: X}` receives X's endpoint by environment or by a passed handle. No broadcast; DNS-SD stays for node discovery only. A loopback HTTP listener for MCP (RM-05) would be labelled "token-authenticated, not peer-identified".
- **Controlled application-to-application interaction** is exactly the set of `ipc` grants between workloads ArcForges launched. Interaction with software ArcForges did not launch is denied or allowed by the tier, never "controlled".

### 8.4 Devices

- Denied by default in confined profiles, where the backend can deny. On Windows input devices are always available and GPU denial is unverified (§5.1), so `devices` is PARTIAL there.
- `devices.gpu` is a wholesale grant, off by default, and reported as a widening of driver attack surface. On Windows it is a basis fact until LAB-WIN-04 proves a deny mechanism.
- GPU budgets are reported only where `dmem` or MPS is probed, and never promised on Windows or macOS (EX-03).
- Camera, microphone and location: the AppContainer capability model on Windows; TCC on macOS (aggregating on the node by default, §5.3); withheld device nodes and portals on Linux.

### 8.5 UI

**No GUI confinement in any stage proposed here** (EX-19 holds the question). `ui` is not a dimension; each realization reports the basis fact **`ui_isolation`**, which feeds an exposure statement:
- **Windows** headless confined attempts get a holder-owned window station and desktop: `ui_isolation` GUARDRAIL, and "separate desktop measured" only where LAB-WIN-04 shows the token cannot reopen `WinSta0\Default` (expected for LPAC at most).
- **Linux** confined attempts get no display socket in the view; **the X11 abstract socket stays reachable under `net{open}` unless ABI ≥ 6.** X11 is labelled "not isolated", and **a reachable display server is an escape-class gap of the realization** (§3.2). Terminal injection is denied by `--new-session` plus a `TIOCSTI`/`TIOCLINUX` policy filter.
- **macOS:** no confined `ui` claim at any stage.

This is the largest deliberate scale-down: compatible GUI applications get LIFECYCLE and CONTAINMENT, not SANDBOX.

### 8.6 Cache trust

The partition rules TP-1 … TP-8 (D-identity-ipc-completion-16, -17; §1.4) are adopted for the stage that introduces confined tiers (EX-09):
- the storage key is `(kind, compat_key, partition)`;
- the node is the only writer of trusted stores;
- promotion to `shared` covers content-verifiable entries only;
- action-keyed results are never promoted;
- read grants on `user` are `fs.read` grants and reported as such; the default read grants (TP-8) are an owner decision (§17).

**No foundation is needed now.** The partition column can be added by an expand-only migration when EX-09 is promoted, so AF-CACHE-01 is unchanged. The wording of [05](05-toolchains-caches.md) §6 item 4 already reads "integrity checks detect corruption, not a less-trusted producer" (corrected 2026-10-19).

## 9. Technical strategy: C# first and Native AOT

### 9.1 Where each element lives

**The security boundary is the operating system's; C# orchestrates it.** Every element of the core is reachable from the one multi-role Native AOT binary on plain `net10.0`. Evidence is labelled per call:

| Kind | Elements | Evidence |
|---|---|---|
| Direct .NET | Profile compiler, `meet` and subset checks, inheritance, journal, installation lifecycle, SHA-256/CAS, STJ source-generated parsing; mediators (proxy, brokers, relay) and extraction as helper roles of the same binary | E1 patterns; the proxy under AOT E4 |
| `LibraryImport`, Windows | Job objects and `PROC_THREAD_ATTRIBUTE_*` | E1 (the 43 delivered `Native.cs` declarations, AOT-clean; D-x-lifecycle-40) |
| | AppContainer profiles and tokens, LPAC | E1-DP for a zero-capability launch with a JIT broker (ContentSandbox); in the node's AOT holder, nested, with capabilities: E4 |
| | Security descriptors and ACEs through handles | E1 (`System.Security.AccessControl`); handle-based application E4 |
| | Window stations and desktops | E4 |
| `LibraryImport`, Linux | Signals, rlimits, `waitpid`, `execve`, `posix_spawn`, file actions | E1 (the 28 delivered `Libc.cs` declarations, AOT-clean) |
| | Landlock and seccomp through `syscall` | E1-DP code in DesktopPlatform's ContentSandbox (containment unproven on Linux); in the node E4 |
| | `openat2`, pidfd, `close_range`, `memfd_create` | E2 (kernel documentation); E4 in the node |
| `LibraryImport`, macOS | `posix_spawn`, rlimits, QoS, libproc, `LOCAL_PEERTOKEN`, `clonefile`, `SecStaticCode*` | E4 |
| Existing managed libraries | Tmds.DBus.Protocol | E1 |
| Orchestrated OS-provided or user-installed tools | §9.2 | — |
| Native helpers | **None** in the core | — |

**Where Native AOT limits matter:**
- `wasmtime-dotnet` fails the zero-warning rule, so in-process WASM is rejected (D-x-agents-28).
- CsWinRT `PackageManager` and winget COM need a Windows TFM, and their AOT status is E4. MSIX stays in EX-21. Windows Hello's `UserConsentVerifier` (EX-23) is WinRT too.
- CsWin32's default output uses the runtime marshaller and is avoided.
- The Sigstore and TUF .NET libraries are E4 (LAB-X-13).
- MXC declares AOT compatibility but ships a Rust native unit (`mxc_ffi`) plus possible sidecars (unverified; D-x-agents-1). The deciding issue is [AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §6, not AOT.
- ASP.NET Core minimal APIs are partial for AOT; this matters only for RM-05.
- **Version-tracked runtime facts:** `exec-init` relies on .NET 10 and later installing no default SIGTERM handler and on `SIG_IGN` dispositions surviving `execve`. Both enter the AOT verification table, re-checked per runtime update.

**Where C# alone is genuinely insufficient:**
- Linux namespace setup needs a single-threaded caller for `unshare(CLONE_NEWUSER)`. A .NET process is not one, so the distribution's bwrap owns the view, and no C helper is written.
- **macOS App Sandbox for ArcForges' own helpers** needs signed entitlements, which belong to an executable's code signature. A role of the one signed binary cannot be App-Sandboxed while the node is not. The language is not the issue; the **binary count** is: macOS helper isolation needs a second signed executable, which [AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §1 does not allow today and which RM-14 does not cover today (RM-14's Item is the Windows attempt holder and the Linux disk guard): it would need RM-14's Item widened, or its own row. Until then, macOS methods that parse hostile input are UNAVAILABLE.

**RM-14 is a lab question, not a settled one.** Helper roles stay roles of the one binary if `exec-init` fits its measured target in LAB-LNX-19 and the G20 cost legs hold. Otherwise RM-14's trigger is met, before any bwrap-init fallback is considered. [AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) records this as a future-tense note.

### 9.2 Inventory: native components and orchestrated tools

This is the Design inventory that [AD-0003](../decisions/AD-0003-architecture-and-runtimes.md)'s direction (b) refers to.

| Item | Kind | Shipped by ArcForges? | Required for | Reported when absent |
|---|---|---|---|---|
| `arcforges` roles: `exec-init`, `exec-final`, `recover`, `mcp-wrap`, proxy, relay, broker and extractor roles | C# AOT roles | Yes | Per row | — |
| `bwrap` (distribution package; the exact fixed-revision list carried as signed data) | Orchestrated OS tool | **No** | The Linux view backend (EX-11) | `view.* = NONE (bwrap_absent or bwrap_unfixed)`, then the Landlock-only tier |
| `xdg-dbus-proxy`, `pasta` | Orchestrated | No | Optional (EX rows) | `UNAVAILABLE` |
| `/usr/bin/sandbox-exec` | Orchestrated OS binary, DEPRECATED | No | EX-22 | `isolation.seatbelt = UNAVAILABLE` |
| npm/pnpm, uv/pipx, `dnx`, `cargo`, `winget.exe`, `flatpak`, `brew`, possibly `mise` or `aqua` | Orchestrated user tools | No | Per installation method | Method unavailable |
| `wsb.exe`, `podman`, `runsc`, Apple `container` | Orchestrated STRONG backends | No | EX-18 | Backend absent |
| MXC (`mxc_ffi` plus possible sidecars, unverified) | Third-party native Rust unit | Would be | EX-17 only | **Not adopted** |
| Cedar engine, OPA, Wasmtime | Third-party native | Would be | — | **Not adopted** |

**Other technical consequences.**
- **[AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §6** stays unchanged until the first backend row is promoted; its direction (a)–(c) is recorded there. Under (b), depending on the distribution's bwrap fits §6.
- **[AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §1 (one binary)** stays. New stages are roles, subject to the RM-14 note above and to the macOS binary-count consequence.
- **Windows TFM: no change now.** Multi-targeting the Windows platform projects to `net10.0-windows10.0.x` is a separate build ADR. It needs LAB-WIN-17 and LAB-X-14 to show zero AOT and trim warnings on win-x64 and win-arm64, with Linux RIDs unaffected. Its only consumers (MSIX, Credential Locker, winget COM, `UserConsentVerifier`) are outside the core.

### 9.3 Licensing and redistribution

**ArcForges itself is AGPL-3.0-only** (the ArcForges repository's `LICENSE` and SPDX headers). The licences below are as the study recorded them from each project's published licence; any unit ArcForges would ship gets its own licence review first.

| Component | Licence | How ArcForges would use it | Obligation |
|---|---|---|---|
| bubblewrap | LGPL-2.0+ to 0.11, **LGPL-2.1+ from 0.12.0** | Orchestrated distribution binary | None for ArcForges' code. Never link or embed it |
| xdg-dbus-proxy, Flatpak, xdg-desktop-portal | LGPL-2.1+ | Orchestrated, or D-Bus protocol use | None |
| systemd (D-Bus API) | LGPL-2.1+ | Protocol use (E1 today) | None |
| pasta (passt) | GPL-2.0+ | Orchestrated (optional) | None if not shipped |
| Podman / crun | Apache-2.0 / GPL-2.0 | Orchestrated (EX-18) | None if not shipped; GPL-2.0-only units are never linked |
| gVisor; Firecracker, Kata, libkrun | Apache-2.0 | Orchestrated (EX-18) | None |
| Snap, Firejail, distrobox | GPL-3.0 / GPL-2.0 / GPL-3.0 | Reference only | — |
| Nix / Guix | LGPL-2.1 / GPL-3.0+ | Optional orchestration | None |
| mise / aqua | MIT | A possible delegate (EX-13 stage b) | None if orchestrated |
| MXC | MIT; `wslcsdk.dll` licence **unverified** | EX-17 only | An ADR and a licence review before any shipping |
| Wasmtime | Apache-2.0 (with the LLVM exception per upstream; not re-verified) | Not adopted | — |
| Cedar | Apache-2.0 | Semantics borrowed, no engine | None |
| Sigstore (specification), the Sigstore .NET library, BouncyCastle | Apache-2.0 / MIT / MIT | Optional verification (LAB-X-13) | Notice files if shipped |
| winget-cli | MIT | Orchestrated `winget.exe` | None |
| winget-pkgs manifest data | Repository MIT; **reuse of the manifest data not reviewed** | Assessment input | A review before programmatic reuse |
| Scoop and its kiennq shim | MIT or Unlicense | Reference | None |
| Homebrew | BSD-2-Clause | Orchestrated `brew` | None |
| pm2 | AGPL-3.0 | **Not used**, on fitness: a Node.js process manager that duplicates ArcForges' supervision | — |
| CRIU | GPL-2.0 | Not used (live migration rejected) | — |
| Docker MCP Gateway; Docker Sandboxes `sbx` | MIT; proprietary | Interoperate only | — |
| Codex CLI, Claude `sandbox-runtime`, Gemini CLI | Apache-2.0 | Reference only | — |

**Rule:** no third-party native component is shipped in the core; anything ArcForges ships must be AGPL-3.0-compatible, with its notices. Orchestrated tools are the user's or the distribution's.

## 10. Privacy (proposed)

**Principles.** All extend existing rules ([11](11-security-privacy.md) §5, R-OPS-003, R-REC-002, data classes D0–D4):
1. **Purpose limitation at ingestion.** No new evidence kind is collected for workloads ArcForges did not launch, except standard-user inventories that are **off until the owner enables them**. Machine-wide sources keep only rows inside a managed attempt's window, labelled "seen during attempt <id>, cause unknown".
2. **Metadata, never content.** Host and port, never URLs or payloads. Paths in granted directories, never file contents. Credential names, never values.
3. **No new outbound lookups.** No online Rekor or GitHub attestation fetch by default: verification is bundle-only. Probe reference data arrives in the signed release manifest the update check already fetches.
4. **Local by default.** New evidence never goes into telemetry. It reaches the relay only as the canonical D1 summary, or on explicit request where the node privacy policy allows. **A separate remote toggle** governs destinations, inventories and denial paths, even when D2 viewing is otherwise allowed.
5. **LAN peers receive only the D1 realization summaries of attempts they placed and capability summaries for placement**; never inventories, denials or destinations.
6. **Isolation reduces collection.** A confined attempt's record holds what it was granted, not everything it could have touched.
7. **Retention is shorter than audit.** Detail is reduced to counts after a short window.
8. **D3 material never enters quarantine, snapshots, archives, exports, LAN transfer or support bundles**, and the 24-hour quarantine has a purge-now path.

| Evidence | Class | Default | Retention (proposal) | Remote |
|---|---|---|---|---|
| Realization (dimension, strength, basis) | D1 (basis detail D2) | On | With the attempt record | The canonical summary |
| Capability probe results (host facts) | D2 | On | Latest plus changes | On request |
| **Doctor host-security posture** (unfixed bwrap, account type, Administrator protection, Smart App Control, `wsl_interop_reachable`, TCC categories held, user directories whose ACL ArcForges changed): effectively a vulnerability inventory | D2 | On, local, **HUMAN-only**: never returned to AGENT or SCRIPT callers, through the MCP adapter or in `GetReleaseScope` | Latest only | No; **redacted from support bundles unless the owner includes it** |
| OWNED and DELEGATED installation inventory | D2 | On | Installation lifetime + 30 days | Counts only |
| `ran_unconfined` installation summary | D1 | On | **Installation lifetime; `PurgeTaskRecord` cannot delete it** | No |
| OBSERVED inventory (all software) | D2 | **Off until enabled** | Latest snapshot only | No |
| Acquisition records, including OS gate verdicts | D2 | On for ArcForges' acquisitions | With the installation | No |
| **`tools/list` digests and `TOOL_DEFINITION_CHANGED` content** | D2 (tool descriptions may contain private names) | On for wrapped servers | Latest digest plus the last change | Finding title only |
| Per-attempt persistence diff and `PERSISTENCE_ADDED` | D2 | On | 90 days of findings | Finding titles only |
| Machine-wide persistence inventory | D2 | **Off until enabled** (EX-15, later stage) | Latest snapshot | No |
| `PRIVILEGED_CHANGE_OBSERVED` | D2 | On, **attempt windows only** | 90 days | Finding titles |
| Network destinations (N1) | D2 | On when N1 is realized | 7 days in detail, then per-domain counts | Separate toggle |
| Credential-use events | D2, never values | On when a broker is granted | 1 year (audit-like) | No |
| **Derived credential copies** (per-attempt files) | **D3** | Only while the attempt runs | **Deleted at attempt end with a journal entry**; never quarantined, snapshotted, exported or transferred | No |
| Denial evidence | D2 | On | 7 days in detail (path class plus the first segment under home), then counts | Separate toggle |
| Granted-directory diffs and workspace provenance | D2, paths only | On for confined attempts | With the attempt; provenance with the worktree | No |
| **`ActorRef` identity facts** (`calling_attempt_id`, profile digests, OS principals) | D2 | On | With the record they annotate | No |
| **Delegation receipts** (export) | D2 | Produced only on request | Not retained beyond the export | Only if the owner sends it |
| Host-write journal | D2; secret-shaped values as presence only | On | Until reversed + 30 days | No |
| Approval records for widenings and installs, with the D2 grant delta | D2 | On | 1 year (audit) | Shown to a local approver; remote only after EX-23 |

Every new kind is covered by AF-REC-01's export and purge. `PurgeTaskRecord` removes realizations and diffs with the task, but not the `ran_unconfined` summary.

## 11. Compatibility (proposed)

### 11.1 Target classes, in order

| Order | Class | Why | Expected realization | Lifecycle |
|---|---|---|---|---|
| 1 | **Stdio MCP servers** (npm, uvx, `dnx`, single binaries, MCPB) | Third-party code with the agent's reach; the highest risk per unit of trust; today unmanaged (RM-12) | Confined, `net{none}` by default, declared needs granted. **Open question:** no source of per-server grants exists; adapters cover toolchains, not MCP servers. Where the grants come from is measured in LAB-X-01 | OWNED through the tool store, or a delegate (EX-13) |
| 2 | **Headless developer CLIs and build steps** | ArcForges' existing workload; adapters already know their caches and homes | Confined where the corpus passes; otherwise UNCONFINED, labelled. Limit-aware runtimes (.NET, JVM, Go) need the read-only own-cgroup view | OWNED prefixes or OBSERVED |
| 3 | **AI-generated commands routed by agents** | The request's aim of safer execution of AI-generated code (request §5) | The AGENT default profile, once G19, G20 (within X %) and the editions check pass | — |
| 4 | **AI agent CLIs themselves, as confined `SERVICE` attempts in their session envelope** | The client's own file tools, hooks and MCP servers are otherwise outside every boundary | A later stage of EX-09, E5 (unexamined): it needs a terminal-attached attempt mode and the grantee-relative grants of §7.1; gated on LAB-X-03 (the clients' own sandboxes nested inside ArcForges tiers) and on the dedicated leg "the AI client itself as a confined attempt" (LAB-X-19) | DELEGATED (vendor updaters) |
| 5 | **Background AI tools and inference servers** as `SERVICE` tasks | Containment and lifecycle value today | CONTAINMENT first; confinement with `devices.gpu` after LAB-X-06 | DELEGATED (vendor updaters) |
| 6 | **Portable GUI applications** | Lifecycle value without isolation claims | UNCONFINED only | OWNED where not self-updating (EX-13, later stage) |

### 11.2 Measurement before defaults

**LAB-X-01**, the compatibility corpus, runs 30–50 real tools from classes 1–4 under each tier on each OS, with a Windows class-1 subset in the minimum lab set (§13.4). It records failure classes: loopback blocked; reads outside grants; registry or configuration writes; named objects; nested sandboxes; devices; network; OS gate blocks after MOTW or quarantine; heap sizing under a hidden or read-only cgroup. It also measures where class-1 grants come from, and runs a read-denial leg for action-key soundness: a read-confined attempt has a verified input set, so its result-cache action key is proven, which is what RM-04's restore needs.

Supporting entries: LAB-X-02 and LAB-X-03 (MCP wrapping; nested client sandboxes), LAB-X-04 and LAB-X-05 (install-time code with MOTW and quarantine legs; re-resolution), LAB-WIN-18 (toolchains under AppContainer and LPAC, with the ACE-propagation cost leg).

**Decision rule, per class and per OS (the 80/60 rule):**
- **at least 80 %** running with adapter-derived grants and no per-tool tuning: may become the default;
- **60–80 %**: opt-in per installation;
- **below 60 %**: the backend is reported available but not recommended for the class.

Measured numbers replace every estimate in the Design. Until then, compatibility is stated as "unmeasured".

**The cost of keeping the OS gates.** Setting MOTW and quarantine means Smart App Control may block unsigned tools and Gatekeeper may prompt for or translocate un-notarized CLIs. Each such block is a reported refusal. LAB-X-04 and LAB-MAC-14 measure how often.

### 11.3 Excluded classes

| Class | Why |
|---|---|
| GUI applications from confined profiles (all OSes) | A shared desktop or display server; no standard-user boundary |
| Browsers and Electron apps with their own sandboxes, from confined profiles | Nested sandboxes break; job UI limits conflict (D-win-primitives-completion-4). Even unconfined (W0, today) Chromium-family workloads may conflict with ArcForges' attempt job (E4; [AD-0005](../decisions/AD-0005-resource-enforcement.md), Windows §3) |
| Machine-wide installers, services, drivers | A6; privilege |
| Self-updating apps from OWNED | The updater replaces the install root |
| Per-extension isolation inside IDE extension hosts | Extensions share one host process; only the whole host or its children can be bounded |
| Docker-based MCP servers counted as "contained" | Where the container engine runs in WSL2 or another VM, the attempt job holds only the front-end process (for example `wsl.exe`); it is labelled `GUEST_VM` |
| `wsl.exe` inside CONFINED Windows profiles while WSL interop is reachable | It would reach `/mnt/c` with the user's permissions |
| Windows 10, 32-bit | Existing floors ([AD-0002](../decisions/AD-0002-platform-scope.md)) |
| macOS on Intel | A study proposal, not an existing floor: AD-0002 defines no macOS floor. Apple silicon only is proposed because the lab hardware of owner decision D4 and Apple `container` are Apple-silicon-only; the owner decides (§17, decision 21) |

### 11.4 Expanding without compromising

Every compatibility expansion must be one of two things:
- a **named, reported grant**, for example `fs.read` on a toolchain root, or a per-root capability SID on Windows;
- a **mediated channel**, for example a broker or the cache relay.

**Forbidden:**
- a loopback exemption;
- a read-broad profile reported as narrow;
- a deny list reported as ENFORCED;
- a learning-mode "allow" or `--audit` on real work;
- a silent fallback to a weaker tier;
- stripping MOTW or quarantine to get past an OS gate.

## 12. Additive `v1` contract sketch (illustrative)

Reviewed only when each row is promoted; additive within `arcforges.node.v1`, with a `validate:` rule per request field and catalogued codes ([contracts](../contracts/README.md)). **No reserved names now:** names reserved within `v1` cannot be withdrawn.
- `common.proto`
  - `AccessDimension`; `Strength`; `ApiStatus`.
  - `DimensionStatus { dimension, policy, attainable | realized, strength, holds_against[], basis, gaps[] (each with a class), implicit_grants[], reason }`.
  - `StrengthBasis { backend, api_status, os_build, component_version, fix_status, abi, probe_ref, probed_at, hardening[], platform_facts[], ui_isolation, evidence_label }`.
  - `ExposureStatement`; `RealizationSummary` (the canonical summary).
  - `ActorRef` gains `calling_attempt_id`, `caller_profile_digest`, `os_principal`, `identity_strength` and an identity basis.
- `policy.proto`
  - `AccessProfile`, `Grant` (oneof by kind), `Requirement` (REQUIRED or PREFERRED, `min_strength`, `require_hardening`).
  - `DelegationEnvelope { session, grants, expiry, workspace, action_budgets, resource_budget }`.
  - `provenance_strength` on policy revisions.
  - Isolation settings: `accept_deprecated` per backend; the default profile per origin; the per-client HUMAN floor.
  - **No `allow_lifecycle_approvals`:** remote widening and install decisions stay local-only until end-to-end approval signatures exist (EX-23).
- `approvals.proto`: `provenance_strength` on decisions; the grant delta at D2.
- `tasks.proto`
  - `TaskSpec.profile_ref`, `envelope_ref`, `installation_ref`.
  - `Attempt.realized[]`, `unenforced_dimensions[]`, `exposure[]`.
  - The `ExplainTask` realization section, and **a dry-run mode of `ExplainTask` over a draft `TaskSpec` with a profile**, in place of a separate `ExplainGrant` RPC.
- `installations.proto`, a new file: one new service, `InstallationService` (Plan, Apply, Remove, Get, List, SetUpdateOwner), mirroring `IntegrationService`'s plan, apply and remove with exact diffs.
- Codes: `ISOLATION/unavailable` (with dimension, backend and reason), `ISOLATION/experimental_only`, `LIFECYCLE/owner_conflict`, `LIFECYCLE/not_owned`, `AUTHORIZATION/widening_requires_human`, `AUTHORIZATION/budget_exhausted`.

**One new service, no new package.** None of these names exists in the protos, and none is reserved.

## 13. Validation: labs, venues and the owner's lab decisions

The entries, venues, procedures at plan level, pass and fail criteria, evidence labels and gates are in the [lab register](../research/2026-10-18-delegated-execution/lab-register.md). This section states what the roadmap relies on.

### 13.1 No lab can run today, and the timing is the owner's choice

[AD-0002](../decisions/AD-0002-platform-scope.md) admits only the developer workstation and its WSL Debian 13 distribution as validation venues, and the owner's request rules out invasive experiments on the personal environment (request §11). So no admitted venue exists for the confinement labs until the owner's decisions D1 and D5 (§13.3). No fact about the owner's own workstation enters this chapter; whether any should be recorded is an owner question (§17, decision 20).

The decisive evidence for the Windows strategy would otherwise arrive late: the release-1 tasks from AF-RES-01 onward still shape the job code that LAB-WIN-01 copies, and they all stand before AF-ACC-01. **The owner chooses (§17, decision 2):**
- **(a) early research spikes:** run the decisive spikes (LAB-WIN-01, LAB-WIN-05, LAB-WIN-18, the Windows class-1 subset of LAB-X-01, and LAB-LNX-19) as research as soon as D1 and D5 exist, independent of release-1 acceptance and without touching the delivery sequence; or
- **(b) accept the late-learning risk:** labs run only after AF-ACC-01 is delivered, and a late Windows result may mean rework in delivered job code or a Windows story learned late.

Either way, the labs sit in the rows' Prerequisites and "Revisit when" cells, not in a stage diagram.

### 13.2 The composite first-backend rule

**Windows goes first only if all of these hold:**
1. LAB-WIN-01 passes in at least one combination (nesting with limits, accounting, stdio, termination and graceful stop intact);
2. LAB-WIN-05 shows **by-name** endpoint reach from inside the AppContainer;
3. the Windows class-1 subset of LAB-X-01 reaches at least 60 %;
4. LAB-WIN-18 runs at least one class-2 toolchain with root-scoped grants (per-root capability SIDs or managed worktrees);
5. the owner accepts the stated cost of uncached confined builds on Windows (SR-1: sccache is TCP-only there). **This condition applies only if LAB-WIN-09 leg (a) shows that loopback between two processes inside the same AppContainer is blocked**; with the sccache server S2' inside the attempt's own AppContainer, the cached path may remain (E4; §5.1);
6. **LAB-WIN-04's launcher cells (WMI, Task Scheduler, COM activation) and its WSL leg deny from W2 and W3, or the owner accepts a Windows backend that holds against {A1, A2} only on hosts where they are reachable.** Under the escape rule of §3.2 these cells decide the Windows value; refusing `wsl.exe` inside CONFINED profiles is a guardrail and never satisfies this condition.

**Otherwise Linux goes first**, and the Windows statement becomes "containment plus guardrails; isolation only through STRONG backends", said plainly. Gate G40 records the decision. The rule is in EX-10's and EX-11's "Revisit when" cells.

**Stage order.** Conditions 1–4 are decided by the stage-1 spikes; LAB-WIN-04 and LAB-WIN-09 run in stage 2. G40 is therefore decided **provisionally** at the end of stage 1: **a Windows-first choice made then stays provisional until conditions 5 and 6 are known.** LAB-WIN-04's launcher cells and WSL leg and LAB-WIN-09's legs (a) and (e) run first in stage 2, and the owner then states whether the measured costs are accepted. Moving those legs into stage 1 would need D1 to provide a WSL-capable guest; they stay in stage 2, and the choice is marked provisional.

### 13.3 The owner's lab decisions, the operator, the channel, the budget and the stop rule

| ID | Decision | Unblocks |
|---|---|---|
| D1 | Provide a second x64 host (**preferred**, so L-01 stays unchanged during release 1), **or** enable Hyper-V on the workstation (an administrator step plus a restart; its effect on L-01 must be checked, and so must Administrator protection, which Microsoft advises against on Hyper-V devices) | Most Windows and Linux labs, including the minimum set |
| D2 | A guest image of the 26300 servicing series (26H2 ≥ .9550) or an Insider image | The PSEC and SBOX legs; agent-account experiments |
| D3 | Test accounts and licences (Claude Code, Codex, JetBrains) | The client-integration labs, LAB-X-03 |
| D4 | An Apple-silicon lab Mac (wipeable, or a cloud Mac) and the Apple Developer Program | Every macOS lab; RM-15 |
| D5 | Prototype code inside disposable VMs | LAB-LNX-19 (the `exec-init` gate) and other prototype legs |
| — | A `bubblewrap` package on the fixed-revision list on the Linux delivery venue (an install by the owner where the venue's package is not on the list; the probe reads the installed revision) | The Linux delivery venue for persistent-state views |

**Who operates the labs, and through which channel.** D1 and D5 also decide this. Under the repositories' standing rules, agents use no SSH, never leave their own process job (no WMI, scheduled tasks or new consoles), and never change a security setting (Hyper-V management needs Hyper-V Administrators membership). **Proposal:** the owner, or a person the owner names, operates the lab VMs; agents prepare scripts and read results only through a channel the owner sets up that needs none of those, for example result files the owner copies to them.

**Budget and stop rule: one proposal**, in the lab register (§0.1); the owner is asked to accept or change it (§17, decision 3). In short: stage 1, the decisive spikes, about 10 operator-days and about 70 GiB of guest disk (estimated), at most two re-runs per leg; stage 2, the rest of the minimum set, about 15 operator-days; later stages budgeted by the owner when they open. A run or stage stops at the first of five rules: its result decides its gate; a fail already selects the reject path; the budget is spent (the gate is then "undecided at budget" and counts as a fail for the first-backend rule); any sign of contact with a real credential store, a real account, the workstation's validation venues or data outside the guest; an unplanned host-state change on the lab host. A stopped stage is a recorded result in the register, never a silent drop.

### 13.4 The minimum lab set

Fifteen entries:
- Windows: LAB-WIN-01, LAB-WIN-02, LAB-WIN-04, LAB-WIN-05, LAB-WIN-06, LAB-WIN-09, LAB-WIN-18;
- Linux: LAB-LNX-01, LAB-LNX-02, LAB-LNX-03, LAB-LNX-13, LAB-LNX-14, LAB-LNX-19, LAB-LNX-21;
- cross-platform: the Windows class-1 subset of LAB-X-01.

It needs **D1 and D5**, not D1 alone.

### 13.5 Venue amendment

Lab results count as Design evidence only on a venue that [AD-0002](../decisions/AD-0002-platform-scope.md) admits. Its amendment of 2026-10-19 admits "a disposable lab VM or wipeable lab hardware: research evidence for roadmap rows, for that build only; not a validation venue for release-1 tasks".

## 14. Capabilities per theme: the fourteen fields

The request asks that each validated capability record fourteen details (request §10). Each roadmap row below has one table of those fields. The rows themselves, in [`roadmap.md` in ArcForges/Plan](https://github.com/ArcForges/Plan/blob/main/roadmap.md), carry only the cells the roadmap defines; this section carries everything else.

| # | Field | What the field holds here |
|---|---|---|
| 1 | Purpose and user value | The user's job the row serves, in the owner's terms |
| 2 | Fit with the conceptual model | Which concept of §2.2 it introduces or uses, which extension of an existing primitive, and why it passes M5 |
| 3 | Existing capabilities it builds on | Delivered, specified or planned ArcForges parts, by Design area or task |
| 4 | Platform scope and differences | Windows, Linux, macOS; the three are deliberately asymmetric (§5) |
| 5 | Expected guarantees | **Attainable** values only, each with its gaps and the lab that decides it. No value here is a realized ENFORCED |
| 6 | Candidate mechanisms | Mechanisms named at documentation level |
| 7 | Compatibility strategy and exclusions | What is expected to work, what is excluded and why |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell is the binding cross-row order and is not restated: this field names that cell and adds only intra-row needs |
| 9 | Risks and unresolved questions | Including the threat rows of §4.4 that apply when the row is promoted |
| 10 | Research and prototypes needed | LAB IDs and gates of the lab register |
| 11 | Internal delivery stages | The row's own stages only; no cross-row stage diagram exists |
| 12 | Acceptance criteria appropriate to maturity | Specific to the capability, at the maturity the row would reach when promoted (§14.1) |
| 13 | Relationships | To other rows and to release-1 tasks, by ID |
| 14 | Conditions to invest or reject | The row's own conditions; a gated row's reject condition also sits in its own "Revisit when" cell |

### 14.1 Rules that apply to every row

**Tier and the owner question.**
- **Every new row is exploratory (EX-07 … EX-23).** Request §10 authorizes recording validated, non-implementation proposals; the roadmap defines accepted future work as work for which a product decision exists, and admits an idea to RM only through a recorded product-owner decision.
- **One tier change: EX-05 becomes `accepted as RM-15`, for macOS stage 1 only** (the monitored local node). The recorded decision is request §3 ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 10; [AD-0002](../decisions/AD-0002-platform-scope.md) amendment (1)). Seatbelt confinement is not part of RM-15; it is EX-22.
- **The owner is asked which rows to accept as RM** (§17, decision 1). The recommended set: **EX-07 stage a, EX-08, EX-13 stage a, EX-15 stage 1**, each feasible at P0 on delivered or specified patterns. A row the owner confirms moves to RM in a later Plan change that records the answer verbatim; a feasibility-gated row the owner confirms anyway carries its reject condition in its own "Revisit when" cell.
- **Nothing is promoted before AF-ACC-01 is delivered** (every new row names it, directly or through a row it depends on). No row of the delivery sequence changes position or dependencies.

**The completion-time rule** ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 9). G20 measures the cost legs against X: per-attempt memory (holder, `exec-init`), leased identities or fresh profiles, Windows desktops at N parallel attempts, ACE propagation, probe and read-back latency, **start latency and cache-hit-rate loss**. The rule binds every confinement row (EX-09 … EX-12, EX-14's defaults, EX-22) and appears in their field 14 as "cost above X %".

**The acceptance maturity ladder.** Field 12 states criteria at the maturity the row would reach:

| Maturity | Criterion |
|---|---|
| Research (EX) | The question is answered by a registered lab, with a recorded pass or fail and an evidence label, and no claim beyond the tested build |
| Accepted (RM) | Every guarantee the row would state has a per-backend table: every dimension, attainable strength, gaps with classes, `holds_against`, privilege, evidence. Every E4 item names its lab |
| Design-promoted | The ADR amendment for the model elements it needs is accepted. Contract additions are reviewed as additive `v1`. Threat and privacy rows are written. Compatibility is "unmeasured" or measured |
| Delivered (future tasks) | Per backend and dimension, a venue-scoped real test that out-of-grant access is denied. A test that a REQUIRED dimension the host lacks refuses before any workload code runs. A test that a PREFERRED shortfall is labelled on every surface. A re-probe test after a package change. Residue tests for every owned OS object, including "a re-leased SID has no access to the prior lessee's grants". Inheritance tests: a confined caller cannot obtain a weaker task, and "an AGENT request with `min_strength=PARTIAL` under an ENFORCED floor is refused". **No silent fallback anywhere**; no surface renders a realization except through the canonical summary or the full table |
| Defaults (any CONFINED default) | G19 at least 80 % for the class and OS; G20 within the X % median completion-time ceiling, with cache-hit loss and start latency measured; the editions check (§7.6); the lock-out rules in force |
| Real-world | Acceptance-register entries per OS and distribution; never reported as proven by lab VMs alone |

**Boundaries every row keeps:** [AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 3.

**Remote:** remote narrowing stays available at MEDIUM risk; remote widening and install decisions will be local-only until EX-23; release 1's opt-in remote approval path is unchanged (§5.4, §7.5).

### 14.2 Theme 1: truthful contract and recovery (EX-07, EX-08)

Theme purpose: make ArcForges truthful about what its workloads can reach, and able to undo exactly what it changed on the host, before any confinement exists. Both rows are valuable with zero confined backends.

#### EX-07 Truthful access contract

Status: exploratory. Recommended to the owner for RM: **stage a**.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | For any command, MCP server or agent session, the owner sees what it may do and what is actually enforced, from any surface (CLI, Desktop, MCP, Web, phone), through one summary. On day one the honest answer for every access dimension is "not restricted (same-user tier)", which tells owners exactly where they stand. The one-time **"what can my agents reach right now?"** report runs locally against the owner's real setup: installed AI clients and their declared sandboxes, credential files present, configured MCP servers. It never enumerates or queries an OS secret store; store reachability is stated from the tier, not probed. Stage a makes ArcForges truthful; it does not make any access rule enforceable |
| 2 | Fit with the conceptual model | Introduces the **Realization** message family (concept 1, §2.2); its two uses are the capability report and every attempt record, with `ExplainTask`, `GetReleaseScope`, the remote D1 summary and the residue rule as further uses. Stage b introduces the **access profile with typed grants** (concept 2), whose uses are confined commands and services, acquisition attempts, inheritance floors, credential delivery and cache read grants. M2 decides the dimension list; UNCONFINED profiles carry no grants. The always-forbidden set is relative to the grantee: an AI client's own configuration, state and credential are grantable only to that client's own confined attempt (§7.1). No policy language or engine: grants borrow default-deny, forbid-wins and decidable subset semantics, evaluated in node C# |
| 3 | Existing capabilities | The `R-RES-008` pattern (require enforcement, report OBSERVE_ONLY or PARTIAL per resource, refuse when required; `NodeCapabilities`, DELIVERED, E1); `CapabilityReport` (DELIVERED); `ExplainTask` and `ExplainPermission` (SPECIFIED); `SessionService.GetReleaseScope` and `SessionCoverage` (AF-AI-01, PLANNED); records and exports (AF-REC-01); the doctor (AF-DIAG-01), with the HUMAN-only host-posture check of the account type and the Administrator protection state; `PolicyDocument` with revisions (store DELIVERED); `ValidatePolicy`; the release coverage statement's stated limits (routing, the credential sentence, the same-user qualifier, the generic UAC sentence) |
| 4 | Platform scope | Windows, Linux and macOS (macOS through RM-15). Stage a is identical in form on all three: every access dimension `NONE (same-user tier)`. Per-OS differences appear only in the dimension list (`config` exists on Windows only; `visibility` is reported, not grantable, on Windows) and in host facts. Every surface, the phone and Web included, renders the canonical summary; Android, iOS and the Web only display it |
| 5 | Expected guarantees | Stage a claims nothing beyond truthful reporting: each access dimension reads `NONE` with the reason "same-user tier"; `res` keeps today's values with the same-user qualifier (ENFORCED against A1/A2, GUARDRAIL against workloads that target ArcForges' objects; T-22). The reporting itself is node-computed and consistent across surfaces; it is GUARDRAIL against same-user code that edits the node's store (T-39). Stage b: per backend, as realized by EX-10, EX-11 or EX-22, never stronger than the backend's attainable value |
| 6 | Candidate mechanisms | `DimensionStatus` per dimension with policy, strength, `holds_against`, basis, gaps, implicit grants and reason; attainable entries in the capability report ("can enforce (probed)"), realized entries per attempt; `ExposureStatement` and `RealizationSummary` computed only by the node; `GetReleaseScope` rows per access dimension, stated per platform, not per host, and the per-client routing statement ("commands routed through ArcForges run outside <client>'s own sandbox; the client's own process keeps the user's full access"); the local reach report built from IntegrationService probes, `SessionCoverage` and catalogue names of credential files (presence only, never contents); **it never enumerates or queries an OS secret store** (Credential Manager, Secret Service, Keychain): store reachability is stated from the tier, not probed. **Host-posture facts** (the account type and Administrator protection state already in the doctor; in stage a also the AppArmor userns restriction, the bwrap fix status, `wsl_interop_reachable`, the firewall service state, Smart App Control, SIP and the TCC categories the node holds) live only in the doctor's **HUMAN-only host-posture check** (AF-DIAG-01), never in `GetReleaseScope`, `ExplainTask` for AGENT callers or any MCP result, because they are D2 (§3.5, §10). **Later stage, delegation receipts:** a per-session export of grants, realizations, acquisitions, destinations, persistence and worktree changes. **Stage b:** `AccessProfile` and `Grant` (oneof by kind) inside `PolicyDocument`; `Requirement` with REQUIRED or PREFERRED, `min_strength`, `require_hardening`; a **dry-run mode of `ExplainTask`** over a draft `TaskSpec` with a profile, stating each grant's revocation class (no separate `ExplainGrant`); the lock-out rules as `ValidatePolicy` rules (the protected control set), a policy revision plus an approval TTL whose expiry runs `RestorePolicyRevision` (confirm-or-revert) and `node run --safe`. The refusal of REMOTE for widening-class approvals in `DecideApproval` is a contract change recorded with stage b; release 1's opt-in remote approval path is unchanged. **Question in stage b:** proposing grants from denial evidence (`SANDBOX_DENIED` turned into an approval-class remedy), never through a learning mode |
| 7 | Compatibility and exclusions | Stage a changes no workload behaviour; nothing can break. Excluded at every stage: a single "sandboxed" bit, a tier number or a class name on any surface; client-side computation of summaries; reporting an attainable value as ENFORCED. Stage b inherits its backend's compatibility; a CONFINED default stays gated by the completion-time rule (§14.1) and the 80/60 rule |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the Contracts package release follows the dependency-admission rules; stage a may ship node, CLI and MCP first, with clients second; stage a extends the doctor's existing HUMAN-only host-posture check (AF-DIAG-01) instead of adding a second one. Cross-repository: Contracts, Cloud, Mobile, Web, Desktop |
| 9 | Risks and open questions | Surfaces condensing a realization differently (mitigated by the one node-computed summary); owners reading NONE as a product failure rather than a truthful baseline; T-39 (same-user edits of policy, mitigated by tamper findings and `provenance_strength`); T-37 (approval fatigue and misleading approval content, stage b); T-38 (lock-out by a strict profile, stage b); T-29 (policy-input injection and link substitution, stage b). Open: whether the denial evidence readable at P0 is rich enough for grant proposals (largely unreadable at standard-user privilege; D-lnx-kernel-12) |
| 10 | Research and prototypes | Stage a: none; it is managed code over a delivered pattern. Stage b: the chosen backend's labs; LAB-LNX-18 and LAB-WIN-07 for denial evidence (G32) before the grant-proposal question can be answered |
| 11 | Internal delivery stages | **a:** node, CLI and MCP surfaces (per-dimension status, release-scope rows, the routing statement, the canonical summary, exposure statements, the local reach report), and the further host-posture facts in the doctor's HUMAN-only check. **a′:** Desktop, Web and Android render the canonical summary; the relay carries it as the D1 summary. **Later:** delegation receipts. **b** (with the first backend): profiles and typed grants, the `ExplainTask` dry run, the lock-out rules; grant proposals from denials as a question |
| 12 | Acceptance criteria | **a:** every access dimension appears in `GetReleaseScope` and `ExplainTask` on each supported OS; an UNCONFINED attempt reads `NONE (same-user tier)` for every access dimension; **no surface renders a realization except through the canonical summary or the full table**; a test over every surface finds no single "sandboxed" bit, tier number or class name; the per-client routing statement is present for each supported client; the local reach report runs against ArcForges' own delegated development and states truthfully that its delegates' access to OS stores was not restricted, **without enumerating or querying any OS secret store**; **no host-posture value and no D2 path appears in `GetReleaseScope` or any MCP tool result, and the doctor's host-posture values are returned to local HUMAN callers only.** **b:** a profile that would deny the node endpoint to HUMAN clients, or that would deny an AI client ArcForges launches as a confined attempt the grants of its own configuration, state and credential that the grantee-relative exception allows, is refused by `ValidatePolicy` unless flagged; a profile that grants an always-forbidden entry to any attempt other than the client's own, or `creds.internal`, `.git/hooks` or shell profiles to any attempt, the client's own included, is refused; a deliberately locking revision is reverted by confirm-or-revert within its TTL; `--safe` starts the node with no isolation profile applied; the dry run states each grant's revocation class; an UNCONFINED profile with a grant is rejected |
| 13 | Relationships | Gates every confined row (EX-09 … EX-12, EX-22): no confined value is shown except through this contract. Feeds EX-14 (envelope grants), EX-23 (the approval digest covers the effective profile), the three-part uninstall of EX-13 (the weakest-run rule) and EX-15's findings. Its foundation in release 1 is AF-AI-01's `GetReleaseScope` with the release coverage statement's stated limits ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §7) |
| 14 | Invest or reject | **Invest:** always for stage a; it is cheap, true on day one and the gate for every later claim. **Narrow:** stage a′ may follow stage a if the Contracts and client releases are not ready together. **Reject:** never as a whole; stage b is never built without a confined backend, so that no unenforceable grant schema ships |

#### EX-08 Host-write journal and offline recovery

Status: exploratory. Recommended to the owner for RM.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Every host change ArcForges made can be undone exactly, even when the node is impaired or will not start: integrations in AI-client configuration, ArcForges' own setup, installations, confinement objects, persistence holds and owner-prompted privileged steps. ArcForges' own uninstall becomes exact. The lock-out rules are not part of this row; they are EX-07 stage b |
| 2 | Fit with the conceptual model | **Not a concept**: an extension of `integration_write` (AF-AI-02, SPECIFIED) with writer kinds `INTEGRATION`, `SELF_INSTALL`, `INSTALLATION`, `CONFINEMENT_OBJECT`, `PERSISTENCE_HOLD`. Its uses (six): integrations, ArcForges' own uninstall, managed installs, confinement objects, holds, owner-prompted privileged steps. M4: only the node writes it; `recover` replays only what it recorded |
| 3 | Existing capabilities | `integration_write` and the IntegrationService plan, apply and remove with exact diffs (AF-AI-02); managed roots with ownership records and two-phase cleanup with quarantine (AF-STOR-01; `R-STOR-002`, `R-STOR-006`); policy revisions; the per-user setup program and its uninstall (AF-DIST-01, with the uninstall correction of 2026-10-19) |
| 4 | Platform scope | All three OSes. Windows has the most host objects (AppContainer profiles, ACEs, desktops, registry values); Linux mostly transient units and slices, which systemd removes, plus user files; macOS LaunchAgent plists and owned files |
| 5 | Expected guarantees | **Exact removal of recorded entries only; nothing unrecorded is touched.** Restoring a prior state is as good as the recorded prior state (absent, or a digest plus stored content for small non-secret values). The journal is GUARDRAIL against same-user tampering (T-40): it detects but cannot prevent edits by unconfined same-user code. It never records secret values; secret-shaped values appear as presence only |
| 6 | Candidate mechanisms | Write-ahead entries (target named exactly, prior state, new-state digest, owner and actor with `provenance_strength`) committed before the host write; reconciliation at node start that compares recorded owned objects with the host and removes orphans by exact name; an offline `arcforges recover` role of the one binary, HUMAN only, that replays recorded entries backwards with the node down; uninstall, reconciliation and recovery all replay the same journal |
| 7 | Compatibility and exclusions | Transparent to workloads. Excluded: anything ArcForges did not write (vendor installers, the application's own writes); machine-wide changes; wildcard or unbounded removal (`R-STOR-008`) |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell; no intra-row needs beyond it. The row is itself a prerequisite of EX-10, EX-13 stage b, EX-15's holds stage and EX-20, and not of EX-11, because the view leaves no host state, unless the Ubuntu AppArmor profile is offered as a prompted step; those orders sit in those rows' cells |
| 9 | Risks and open questions | A crash between a host write and its entry (write-ahead order needed); an interrupted reversal; T-40 journal or `recover` misuse (entries name exact objects; HUMAN only); T-33 host-state residue of backends (every object an entry and an owned object). Open: the retention of reversed entries (proposal: until reversed + 30 days, §10) |
| 10 | Research and prototypes | LAB-X-10 (does open access survive revocation, per mechanism); LAB-WIN-13 (break-glass removal); LAB-WIN-08 (what persistence a standard user can hold); gate G23 |
| 11 | Internal delivery stages | One stage: the journal, reconciliation and `recover` for the existing writers (integrations, own setup). Further writer kinds join when their rows are promoted (installations with EX-13 stage b, confinement objects with EX-10, holds with EX-15, privileged steps with EX-20) |
| 12 | Acceptance criteria | `recover` replays the journal with the node down and restores every recorded prior state; reconciliation after a killed node removes an orphaned owned object it recorded, and nothing else; an injected crash between a host write and its entry leaves either both or a detectable, repairable entry; ArcForges' own uninstall leaves no recorded object behind; no entry contains a secret value; `recover` refuses a non-HUMAN caller |
| 13 | Relationships | Precedes the first host-object backend (EX-10); records EX-13's installations and EX-15's holds; makes EX-20's privileged steps exactly removable (AD-0017, boundary 2); serves AF-DIST-01's uninstall |
| 14 | Invest or reject | **Invest:** before the first backend that creates host objects, or when the owner confirms the row. **Narrow:** to Windows-only writer kinds if Linux and macOS create none beyond integrations. **Reject:** never as a whole |

### 14.3 Theme 2: confinement (EX-09, EX-10, EX-11, EX-12)

Theme purpose: let ArcForges deny out-of-grant access to headless work at standard-user privilege, one backend at a time, without creating a confused deputy and without falling back silently. Every value in this theme is attainable and pre-lab (E4); no lab can run before the owner's decisions D1 and D5. The rows are accepted as RM and promoted together: the endpoint (EX-09), one backend (EX-10, EX-11, or EX-22 on macOS) and EX-07 stage b. Every value below obeys the escape rule of §3.2: an escape-class gap caps the whole realization at {A1, A2}.

#### EX-09 Attempt endpoint, inheritance and isolation-preserving routing

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | A confined command can still submit tasks, use caches and see its output through ArcForges, without obtaining more than it has (no confused deputy). Routing a client's commands through ArcForges keeps a floor the owner set for that client, instead of removing the client's own sandbox. Later, the AI client itself runs inside a boundary, and an agent can see its own limits before it fails |
| 2 | Fit with the conceptual model | Introduces the **attempt endpoint** (concept 5, an owned-object bundle); its uses are the node API from a confined attempt, OS-attested identity, cache reach, credential brokers and the network relay. Uses the access profile (EX-07 stage b) for floors and the delegation envelope (EX-14) in its later stages. Extensions, not concepts: `ActorRef` gains `calling_attempt_id`, `caller_profile_digest`, `os_principal`, `identity_strength` with its basis; cache partitions are a column of the existing cache registry. Applies R1–R7, SR-1 … SR-5 and TP-1 … TP-8 |
| 3 | Existing capabilities | The DesktopPlatform LocalRpc resolver (token facts from the process handle on Windows, peer credentials on Linux; DELIVERED, [AD-0013](../decisions/AD-0013-reuse-and-supersession.md)); the MCP adapter and its `run` tool (AF-MCP-01); hooks, sessions and `SessionCoverage` (AF-AI-01); the IntegrationService consent step (AF-AI-02); per-attempt sccache servers and tokens (AF-TOOL-02); the cache registry and CAS (AF-CACHE-01); origins and the permission matrix (AF-SEC-01) |
| 4 | Platform scope | **Windows:** a pipe per attempt with a DACL naming the leased AppContainer SID; descendants must open it by name from inside the AppContainer (E4). **Linux:** a socket bound into the view by directory, so the restarted node can re-create it; identity through `SO_PEERPIDFD` and the unit; in the Landlock-only tier below ABI 9 the user-wide endpoint stays reachable and the node applies the mandatory inheritance clamp by peer cgroup identity. **macOS (only with EX-22):** a Seatbelt `literal` path, a DEPRECATED basis capped at PARTIAL |
| 5 | Expected guarantees | Inheritance is **ENFORCED only where `identity_strength` is ENFORCED** (W2/W3 and the view chain, attainable, pending LAB-WIN-05 and LAB-LNX-14); otherwise GUARDRAIL. B7 (node ↔ confined attempt) is OS-enforced reach plus R1–R7 when promoted. `identity_strength = ENFORCED` means a sandboxed caller cannot present another identity; **it does not exclude calls from unsandboxed same-user processes**. B11 (AI-client routes) stays GUARDRAIL until identity is ENFORCED for that client, which holds only in the later stage where the client runs confined. **That stage's own feasibility is unexamined (E5) until LAB-X-19 has run.** Caches: an unreachable service is `UNAVAILABLE(reason)` and the run proceeds uncached (SR-1) |
| 6 | Candidate mechanisms | The per-attempt bundle (node API S5', cache store S3', sccache S2' inside the attempt's own profile, brokers, the Linux TCP-to-UDS relay), created at launch, journaled as owned objects, closed at the end; identity from the endpoint (SR-3); the **HUMAN-set floor per client and route**, chosen in the IntegrationService consent step (for example "commands from Claude Code's MCP route run at least under profile `agent-default`"); client-declared floors honoured as a refinement on top; "client sandbox unknown" for clients that declare nothing and have no HUMAN floor; a PEER-origin floor for placed work; cache trust partitions keyed `(kind, compat_key, partition)` with the node the only writer of trusted stores; workspace provenance from the granted-directory diff. **Later stage: the AI client as a confined `SERVICE` attempt in its session envelope.** It needs a **terminal-attached attempt mode** (a pseudo-terminal owned by the holder or `exec-init`, relayed to the owner's terminal, with the terminal-injection filter kept), or an equivalent, because the clients are interactive terminal programs, M1 offers only the `COMMAND` and `SERVICE` kinds, and the view chain detaches the controlling terminal. The client's own configuration, state and credential are granted to its own attempt only, by recorded HUMAN approval, under the grantee-relative always-forbidden set, and the credential carries its exposure statement; model-service egress follows the `net` option; its MCP servers and hooks run inside the same envelope; its calls are then never HUMAN (R6). **Later stage: agent-facing envelope introspection** through the MCP adapter: the agent's own realized profile, remaining budget and `ExplainTask` dry-run answers, so it can request a widening before failing (the access analogue of the accepted roadmap row on real-time resource requests from AI clients) |
| 7 | Compatibility and exclusions | Transparent to tools that use `arcforges run` or MCP. Clients that declare nothing get the HUMAN floor or are labelled "client sandbox unknown"; nothing is inferred as confined. Confined builds whose cache service is unreachable run uncached; a loopback exemption is never used. If by-name reach fails on Windows, only the direct child reaches the node and descendants are refused (the stated fallback) |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the DesktopPlatform dynamic per-attempt listeners come with per-listener access rules and the resolver changes, as a DesktopPlatform task before the node task ([AD-0013](../decisions/AD-0013-reuse-and-supersession.md)); the AI-client stage's terminal-attached attempt mode is checked against M1 (a mode of the existing attempt, not a new runtime) and M5 (no new concept) |
| 9 | Risks and open questions | A node restart cuts per-attempt listeners (the realization must degrade visibly until the endpoint is back); PID reuse in peer identity (LAB-LNX-14); T-28 confinement laundering; T-34 cache poisoning across trust levels; T-42 delayed execution of confined writes by unconfined processes, with the decision at promotion between a finding and the writer's profile as a floor for an UNCONFINED task over unreviewed confined writes. Open: whether the HUMAN-set floor closes the routing gap for clients that declare nothing; whether the clients' own sandboxes run nested inside an ArcForges tier (LAB-X-03); whether the AI client itself runs usefully as one confined attempt, interactively, with its grants and its MCP servers and hooks in the same envelope (LAB-X-19); the default cache read grants (TP-8: `shared` only, or `user` too, an owner question) |
| 10 | Research and prototypes | LAB-WIN-05 (by-name open of a DACL-granted pipe from inside W2/W3); LAB-LNX-14 (the PID-reuse residual); LAB-LNX-21 and LAB-WIN-09 with their node-restart legs; LAB-X-03 (nested client sandboxes) and LAB-X-19 (the AI client itself as a confined attempt), both for the AI-client stage; LAB-X-15 (read-only cache tiers); gates G07, G17, G36, G37 |
| 11 | Internal delivery stages | **1** (with the first backend): the endpoint bundle, R1–R7 with `identity_strength`, the HUMAN-set and client-declared floors, the PEER floor, cache partitions, workspace provenance. **Later:** the AI client as a confined SERVICE attempt in its session envelope (after LAB-X-03 and LAB-X-19, with a terminal-attached attempt mode). **Later:** agent-facing envelope introspection through MCP |
| 12 | Acceptance criteria | A confined attempt cannot obtain a weaker task through `arcforges run` or MCP; an AGENT request with `min_strength=PARTIAL` under an ENFORCED floor is refused; a caller with unmappable foreign confinement is refused or routed to a local HUMAN; no call from inside an attempt is classified HUMAN; descendants reach the endpoint by name on Windows, or are refused with the stated fallback; a node restart shows the endpoint gap in the realization until the endpoint is back; a cache write into another partition is refused; a route whose client declares nothing and has no HUMAN floor reads "client sandbox unknown" in the consent text and the realization. **AI-client stage:** the client runs interactively through the relayed terminal inside its envelope; its own configuration, state and credential are reachable by it and by none of its tools or MCP servers that run as separate attempts; `creds.internal`, `.git/hooks` and shell profiles are denied to it |
| 13 | Relationships | Promoted with EX-10 or EX-11 and EX-07 stage b; carries EX-12's brokers and relay; uses EX-14's envelope for its later stages; the access analogue of the accepted row on real-time resource requests from AI clients; gives RM-02 and RM-04 their trust preconditions (the TP rules); raises B11 above GUARDRAIL only through its later stage |
| 14 | Invest or reject | **Invest:** with the first confined backend; without it a confined attempt would be cut off from ArcForges. **Narrow:** if by-name reach fails on Windows, direct children only; if LAB-X-03 or LAB-X-19 fails for a client and OS, the AI-client stage is dropped there and the agent story stays "commands routed through ArcForges run without …". **Reject:** cost of the bundle above X % (§14.1) |

#### EX-10 Windows confined backend (W2/W3)

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | On the request's priority platform, out-of-grant file, network and IPC access is denied to headless tools, MCP servers and agent commands at standard-user privilege, while today's resource containment stays intact |
| 2 | Fit with the conceptual model | A backend of the access profile; no new concept. Its host objects (AppContainer profiles, ACEs, the holder's station and desktop) are owned objects in the journal (EX-08) |
| 3 | Existing capabilities | The `exec-wrap` holder (DELIVERED, AF-EXEC-01: suspended creation, handle list, root and attempt jobs, restart survival through named jobs, [AD-0006](../decisions/AD-0006-execution-semantics.md) §2 and L-14); managed worktrees (AF-WS-01); per-attempt temporary directories (`R-STOR-004`); the journal (EX-08). Precedent: ContentSandbox in DesktopPlatform is E1-DP for a zero-capability launch with a JIT broker in a standalone job; the AOT broker, nesting, capabilities, LPAC and ACE grants are E4 |
| 4 | Platform scope | Windows 11 x64 and arm64; headless COMMAND and SERVICE attempts only. W1 (restricted token, Low IL, alternate desktop) is not offered: a guardrail that looks like a sandbox |
| 5 | Expected guarantees | Attainable, pre-lab (§5.1): `fs.write` PARTIAL ("probed, not read back") until the composite read-back is accepted, AAP-writable locations as gaps, conditional on the WSL leg; `fs.read` PARTIAL (system and AAP locations readable; W3 with the ARAP gap); `config` reads PARTIAL, writes outside the container's own location PARTIAL; `net.out` "deny (own sockets); service-mediated egress unmeasured", from a live canary probe with the firewall product and service state in the basis, `internetClient` PARTIAL ("no network or full network"); `net.in` deny without server capabilities; `ipc` PARTIAL (system brokers, COM per-server permissions); `devices` PARTIAL, `devices.gpu` a basis fact "GPU reachable (unverified)"; `creds` PARTIAL until the Credential Manager, DPAPI and WSL legs pass; `persist` PARTIAL; `exec` PARTIAL, `exec.elevation` measured; `visibility` reported, not grantable; `res` ENFORCED against A1/A2 (delivered) and can enforce (probed) against A3/A4 for processes in the attempt's job, conditional on LAB-WIN-04's WMI, Task Scheduler and COM cells; work by shared OS services is not charged to the attempt; `ui_isolation` GUARDRAIL. **Launcher cells** (WMI, Task Scheduler, COM activation of launch-capable servers, WSL interop) are unmeasured, and each counts as an escape gap of the realization until LAB-WIN-04 denies it from W2 and W3; an escape gap caps every dimension of the realization, ENFORCED and MEDIATED included, at {A1, A2}. If WSL interop is reachable, `fs.*` and `creds` are PARTIAL with that escape gap; `wsl.exe` is also refused inside CONFINED profiles, a guardrail that never changes the value. B8 (siblings) is ENFORCED only under the lease invariant |
| 6 | Candidate mechanisms | A hand-built AppContainer (W2) or LPAC (W3, per profile) created suspended by the holder inside today's root and attempt jobs, with no job UI limits; the composite read-back before resume; a leased identity per running attempt under the lease invariant (G20 measures "one fresh profile per attempt" as the alternative); `TEMP` and `TMP` pointed at `tmp/<attempt>` and verified; the holder's private window station and desktop granted to the leased SID as one more owned object. **Grant compilation, an open choice with a cost leg:** per-root custom capability SIDs (one journaled, HUMAN-approved inheritable ACE per root; per-attempt grants are capabilities in the token, RESTART_REQUIRED); managed worktrees as the default writable workspace; per-attempt ACEs only if LAB-WIN-18 and G20 show the cost acceptable; an Installation-scoped stable identity for an always-confined OWNED installation. Link safety: open with `FILE_FLAG_OPEN_REPARSE_POINT`, refuse reparse points and multi-link files, apply ACEs through the handle; `user_path` grants copy-in, copy-out or refused; never an ACE on credential files |
| 7 | Compatibility and exclusions | Medium to low (E5 until LAB-X-01 and LAB-WIN-18). Confined builds may run uncached: if LAB-WIN-09 leg (a) shows loopback between two processes inside one AppContainer blocked, a cache service reached over loopback is `UNAVAILABLE(loopback_blocked)` (sccache is TCP-only on Windows), while with the sccache server inside the attempt's own AppContainer the cached path may remain (E4); never a loopback exemption. Further risks: named objects; the registry; reads outside system locations; user-installed toolchains without AppContainer ACEs. Excluded: GUI applications; Chromium-family workloads that set job UI limits; `wsl.exe` while interop is reachable; CONFINED with `kill_with_node` (refused until defined); per-destination network control (no documented OS-forced egress path) |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the lab venues need D1 and D5; the composite read-back is accepted as Windows read-back by a Design decision at promotion |
| 9 | Risks and open questions | Nesting inside ArcForges' jobs; toolchain compatibility; ACL propagation cost at 10³–10⁵ files and crash repair; lease residue; WSL interop; service-mediated egress; desktop heap (about 4 MB per alternate desktop); `graceful_stop` to a child on another desktop; T-33 host-state residue. Venue risk: Administrator protection is advised against on Hyper-V devices, which bears on owner decision D1 |
| 10 | Research and prototypes | LAB-WIN-01 (with the W0 headless-Chromium leg), LAB-WIN-04 (with the WSL, `exec.elevation`, DNS and redirector, config, persist and exec cells), LAB-WIN-05, LAB-WIN-09 (with the restart leg), LAB-WIN-18 (with the ACE-propagation, capability-SID and Installation-identity legs); the Windows class-1 subset of LAB-X-01; the G20 cost legs; gates G01, G02, G07, G08 and G40 (the composite first-backend rule, with its sixth condition on LAB-WIN-04's launcher cells and WSL leg) |
| 11 | Internal delivery stages | **1:** headless W2/W3 with `fs` grants on managed roots and managed worktrees only, `net{none}` or `net{open}`, `ui_isolation` GUARDRAIL. **Later:** `ui_isolation` measured where LAB-WIN-04 shows the reopen denied. **Later:** the Installation-scoped identity for always-confined OWNED installations |
| 12 | Acceptance criteria | An out-of-grant write, read, connect and pipe open is denied per dimension on the venue build; the composite read-back runs before resume and a mismatch ends the attempt `SPAWN_FAILED` before any workload instruction; a re-leased SID has no access to the prior lessee's grants; the launcher cells and the WSL leg deny, or the realization carries the escape gap and every dimension holds against {A1, A2} only; a REQUIRED dimension the host cannot meet refuses before any instruction runs; every user directory whose ACL ArcForges changed is listed on HUMAN-only local surfaces (the doctor's host-posture check and the uninstall plan), never in `GetReleaseScope` or an MCP result, and is removed by ArcForges' uninstall; limits, accounting, termination and restart survival are unchanged (L-14 re-run); one negative in-profile probe per confined attempt runs at the probe cadence |
| 13 | Relationships | Promoted with EX-09; makes EX-12's credential stage possible on Windows; competes with EX-11 under the composite first-backend rule; its failure moves Windows confinement to EX-18; its read-confined attempts give RM-04 verified input sets; EX-16's worktrees are its default writable workspace |
| 14 | Invest or reject | **Invest:** the composite first-backend rule holds, all six conditions (G40); a Windows-first choice made at the end of lab stage 1 stays provisional until LAB-WIN-04's launcher cells and WSL leg and LAB-WIN-09 have run. **Narrow:** a class-1 subset between 60 and 80 % keeps confinement opt-in per installation. **Reject:** no combination nests with limits, accounting and termination intact (Windows confinement then goes to EX-18 only, and the Design says "containment plus guardrails; isolation only through STRONG backends"); a class-1 subset below 60 %; cost above X %. **Never trade E1 containment for E4 isolation** |

#### EX-11 Linux confined backend (view chain)

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Out-of-grant access denied to headless work at standard-user privilege on Linux, building incrementally on the delivered transient-unit execution instead of replacing it (request §3) |
| 2 | Fit with the conceptual model | A backend of the access profile; no new concept. Two new roles of the one binary (`exec-init`, `exec-final`). The view leaves no host state, so the journal is not its prerequisite |
| 3 | Existing capabilities | The transient user unit and `exec-launch` (DELIVERED, AF-EXEC-02), with exact exit, signal, freeze (`R-EXE-011`), OOM and restart semantics (`R-EXE-008`; L-13, L-24, L-25); the distribution's `bwrap` (orchestrated, never installed or embedded); Landlock and seccomp code in DesktopPlatform's ContentSandbox (E1-DP, containment unproven on Linux); the signed release manifest ([AD-0012](../decisions/AD-0012-distribution-and-updates.md)) as the channel for probe reference data |
| 4 | Platform scope | AD-0002's Linux targets, per distribution (§5.2): Debian 13 with the fixed bwrap package is the reference; Debian 13 with an unfixed package (an unfixed revision such as `0.11.0-2+deb13u1` exists in the field), Debian 12, Ubuntu 22.04 and Ubuntu 24.04 with the AppArmor profile are ephemeral-state only; **Ubuntu 24.04 by default gives no boundary against compromised tools or AI-generated commands; it gives resource control plus guardrails**. WSL2 evidence counts for WSL2 on that kernel only. The Linux story is never marketed from the Debian reference alone |
| 5 | Expected guarantees | Attainable, pre-lab (§5.2); every cell is at most "can enforce (probed)". **View chain:** `fs.*` can enforce (probed) outside explicit and implicit grants, read back per field and by the in-view self-check before the workload's `execve`; `config` N/A (configuration is files, folded into `fs`); `net{none}` (N0) with the address-family allowlist read back, `net{open}` NONE; `ipc` and `ui_isolation` as functions of `net` and the Landlock ABI; `devices` can enforce (probed) for device nodes withheld from the view, `devices.gpu` only by an explicit grant, with the gap of devices reachable through a granted socket or service; `creds` can enforce (probed) by inclusion for credential files and agent sockets outside grants (a private HOME), PARTIAL on WSL until LAB-LNX-05; `persist` PARTIAL (user units, autostart entries and shell profiles outside grants are absent from the view; writes to granted persistent roots may be run later by unconfined processes; the user manager is unreachable only while its sockets are hidden and read back); `exec` PARTIAL (no-new-privileges closes setuid gain; system binaries stay executable), `exec.elevation` BLOCKED only where the view hides the system bus and is read back, otherwise REACHABLE; `visibility` can enforce (probed) through the PID namespace, with the host network namespace's abstract sockets as a gap under `net{open}`; ptrace and `TIOCSTI` denied by policy filters; `res` against the confined workload with a read-only view of the attempt's own cgroup under a cgroup namespace; persistent-state profiles only where the **installed** bwrap package is on the exact fixed-revision list. **Launcher cells (escape class):** the session bus, the systemd private socket and the user-wide node endpoint are hidden from the view and read back; under `net{open}` below ABI 6 a reachable display server (the X11 abstract socket) is an escape gap, so on a desktop host every dimension then holds against {A1, A2} only; any launcher cell not yet measured counts as an escape gap until LAB-LNX-02 denies it. **Landlock-only tier** (a separate backend, never under the view's field names): `fs.*` PARTIAL; `config` N/A; `ipc` NONE below ABI 6, PARTIAL with the escape gap at ABI 6–8; `net.out` PARTIAL (TCP ports) and `net.in` PARTIAL (TCP bind by port) from ABI 4, NONE below; `devices` PARTIAL (device files as Landlock paths; unmeasured); `creds` PARTIAL (the session bus and its secret service stay reachable below ABI 9); `persist` PARTIAL (the user manager is reachable below ABI 9); `exec` PARTIAL, `exec.elevation` REACHABLE; `visibility` NONE; `res` as L0. The session bus, the systemd private socket and the node's pathname socket are reachable below ABI 9: an escape gap of the realization, so **every dimension of the tier holds against {A1, A2} only below ABI 9**. **The escape rule:** an escape-class gap is a property of the realization and caps every dimension, ENFORCED and MEDIATED included, at {A1, A2}; the canonical summary's headline states it. The bridge to Windows (`/mnt/*`, interop) keeps `creds` PARTIAL on WSL until LAB-LNX-05 |
| 6 | Candidate mechanisms | The five-stage chain: unit → `exec-launch` (memfd argv, `CLOSE_RANGE_CLOEXEC`, `SIG_IGN` for stop signals) → the distribution's `bwrap` (the only mount-namespace owner) → `exec-init` (PID 1: reaping, exact exit status, in-view end steps) → `exec-final` (no-new-privileges, Landlock at the probed ABI, seccomp policy filters, no TSYNC) → workload. End steps move from `ExecStop=` into the view; the `exit-record` precedence gains `view.jsonl`; the cancel grace counts from the workload line; the view binds `tmp/<attempt>/` and never mounts a tmpfs at `/tmp`. The proposed SM-ATTEMPT mapping: for view attempts RUNNING begins at the workload line (decided at promotion; no `machines.json` change before). Linking: `openat2(RESOLVE_BENEATH, RESOLVE_NO_SYMLINKS)` and bind by descriptor. Probe reference data (fix-revision lists, ABI tables) as signed release-manifest data; an unknown revision is unfixed, with `ISOLATION_FIX_UNKNOWN`. **Questions:** a socket-family policy filter in `exec-final` for the tier without namespaces; a compiler rule placing no mount destination at or beneath a persistent workload-writable source (§5.2) |
| 7 | Compatibility and exclusions | 70–90 % for CLIs is an estimate (E5) until LAB-X-01. Limit-aware runtimes (.NET, JVM, Go) need the read-only own-cgroup view. Excluded: X11 GUI isolation; BPF unit options in user units; per-destination IP filtering without root; namespaced tiers on default Ubuntu 24.04; systemd unit sandboxing as a workload mechanism (it serves only the optional hardening of ArcForges' own units, which is read back and reported, F-L04) |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the venue is the owner-updated WSL Debian (WSL2 evidence only) or a VM that AD-0002 admits; AF-SEC-01 supplies peer identity for the clamp, and AF-TOOL-01 the adapter cache and tool-home knowledge for grants; the .NET facts the chain relies on (no default SIGTERM handler; `SIG_IGN` surviving `execve`) are version-tracked in the AOT verification table |
| 9 | Risks and open questions | `exec-init` memory (the Linux guard role measured 8.18 MB private, [15](15-performance-targets.md) §2, so a fixed 8 MiB gate would probably fail); fix-list upkeep as a standing security-data duty (Ubuntu's reverted fix compares as newer, so version comparison is rejected); the exact trigger of the 2026 view-setup escape class (CVE-2026-87766) on persistent-state profiles; .NET runtime behaviour per update; the venue. Open: whether the socket-family filter or the compiler rule lifts the Ubuntu 24.04 and ephemeral-state limits; who owns the probe reference data (named at promotion) |
| 10 | Research and prototypes | LAB-LNX-01 (with the abstract-connect check, the socket-family policy filter, the compiler rule, a behavioural self-test of the fixed bwrap property, the exact trigger, and leg (d) for the Ubuntu AppArmor profile); LAB-LNX-02 (escape channels per tier, with the display-server leg, recorded only as reachable or denied); LAB-LNX-17 (`persist`, `exec.elevation`); LAB-LNX-19 (`exec-init` at a measured target with headroom; exit and signal fidelity); LAB-LNX-21 (service reach and the restart leg); LAB-LNX-04 and LAB-LNX-05 for WSL (with the AF_VSOCK leg); gates G14, G15, G36 and G40 (the composite first-backend rule) |
| 11 | Internal delivery stages | **1:** the view chain with N0 and no bus, for headless COMMAND and SERVICE attempts on hosts whose probe passes, persistent-state only on the fixed package. **1′:** ephemeral-state profiles elsewhere, with workspace results leaving through a session-worktree copy-out (EX-16). **1″:** the Landlock-only tier, labelled with its escape gap, on Ubuntu 24.04 without the profile |
| 12 | Acceptance criteria | Per field, the view's read-back matches the manifest before `execve`, and a mismatch ends the attempt `SPAWN_FAILED` before the workload runs; today's exit, signal, freeze, OOM and restart semantics hold under the chain (L-13, L-24, L-25 re-run); `exec-init` stays within its measured target recorded in the Design's performance targets, and counts in `accounted_mem_bytes` and admission; an unknown bwrap revision gives `ISOLATION_FIX_UNKNOWN` and ephemeral-state profiles only; an abstract-socket connect is denied where the `net` and ABI table says so; the Landlock-only tier never reports under view field names and always shows its escape gap; the probe battery runs in the pre-push WSL lane as a regression test (and in a hosted Ubuntu image once AD-0002 admits it), and one negative in-profile probe per confined attempt runs at the probe cadence |
| 13 | Relationships | Promoted with EX-09; provides N1's network namespace to EX-12; competes with EX-10 under the composite first-backend rule; may meet RM-14's trigger if `exec-init` misses its target; gives RM-04's action keys verified input sets; hosts EX-04's question of placing cross-platform tools on the local WSL guest (never presented as Windows confinement) |
| 14 | Invest or reject | **Invest:** LAB-LNX-01, LAB-LNX-02, LAB-LNX-19 and LAB-LNX-21 pass on Debian 13 and the venue exists. **Narrow:** Ubuntu stays "resource control plus guardrails" unless the socket-family filter or the compiler rule holds; ephemeral-state only while the fix is missing. **Reject:** kill or restart fidelity regresses under the chain with no RM-14 path (the decision order is: `exec-init` at its measured target, then RM-14, then the bwrap-init fallback with `exit_fidelity = SHELL_ENCODED` only if neither is acceptable); cost above X % |

#### EX-12 Mediated channels

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Confined commands reach only the destinations and credentials the owner named: "only the npm registry", "this one deploy key". Destinations are measured, brokers can be revoked at once, and commands routed through ArcForges run without SSH keys, cloud tokens or browser stores unless a named credential is delivered. The client's own process is not covered until it runs confined (EX-09, later stage) |
| 2 | Fit with the conceptual model | No new concept: mediators are helper roles on the attempt endpoint (EX-09); credentials are `creds` grants of the access profile; the MEDIATED strength of the model |
| 3 | Existing capabilities | Sealed task secrets delivered by environment (DELIVERED); secret redaction (`R-SEC-003`, `R-EXE-017`); the endpoint bundle (EX-09); the helper-role profile realized by the backend |
| 4 | Platform scope | **Linux:** N1 egress (an `lo`-only network namespace plus the proxy on a socket bound by directory); **unavailable on Ubuntu 24.04 by default and without user namespaces**. **Windows:** no documented OS-forced egress path for unpackaged processes, so egress stays "no network or full network"; credentials by inclusion and brokers only. **macOS (EX-22):** a localhost proxy at PARTIAL, where `localhost` matches every local address |
| 5 | Expected guarantees | Attainable: `net.out` MEDIATED (`per_host`) on N1, holding **outside the allowlist only**; inside it, exposure statements apply ("exfiltration possible to <allowed hosts>"). Brokers MEDIATED for the granted item. On W2/W3, Credential Manager and DPAPI stay PARTIAL until LAB-WIN-04, conditional on the WSL leg. Every delivered credential carries an exposure statement; a disclosed value is UNREVOCABLE. Derived per-attempt credential copies are **D3 at rest**: never quarantined, snapshotted, exported, archived or transferred, and deleted at attempt end with a journal entry. ArcForges' own secrets are never granted |
| 6 | Candidate mechanisms | The N1 proxy and the brokers as separate helper processes per attempt or per profile, in their own transient unit or job, under the helper-role profile (egress only for the proxy; no network for brokers; no workspace; no `creds` beyond the brokered item); the restart constraint: a channel survives a node restart or the realization degrades visibly. **Credential delivery stages:** sealed secrets by environment, with per-adapter hook labels `HONORED` or `BEST_EFFORT`; read-only derived per-attempt copies, never an ACE on the user's file; agent and helper-protocol brokers (an ssh-agent filter; git, Docker and AWS `credential_process`; Cargo helpers). **Later research stage:** proxy header injection with a per-attempt, memory-only, name-constrained CA for inject hosts only, and hardware-bound keys |
| 7 | Compatibility and exclusions | Proxy-ignoring clients fail under N1 (reported, never bypassed). Excluded: firewall rules, WFP filters and callouts, Network Extension, BPF unit options, seccomp notification on `connect`, a filtering MITM, browser profiles, the user's whole OS store, the login keychain |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: where the helper-role profile cannot be realized ENFORCED for `fs`, `net` and `ipc` on an OS, the method is UNAVAILABLE there |
| 9 | Risks and open questions | T-30 mediator or parser compromise (closed grant types, the helper-role profile, metadata-only records); T-36 credential exfiltration through granted egress; protocol drift (SigV4, the ssh-agent protocol); the restart topology. Open: do N1 and brokers work with unchanged tools; can inject-host-only termination keep values off every other host |
| 10 | Research and prototypes | LAB-LNX-03 (network tiers and the egress proxy; G16); LAB-WIN-04 with its key-class leg; LAB-X-16 (sibling secret isolation); LAB-X-18 (brokers on the endpoint); LAB-X-17 (injection, for the later stage); gate G38 |
| 11 | Internal delivery stages | **1:** credential non-exposure by inclusion and the sealed-secret and derived-copy stages. **2:** brokers on the endpoint. **3 (Linux):** N1 egress with measured destinations. **Later research:** proxy injection and hardware-bound keys |
| 12 | Acceptance criteria | Under N1 a connect outside the allowlist fails while an allowed one succeeds, and the destination is recorded as host and port only; a broker serves only the granted key, and the value appears in no view, record, export or bundle; a derived copy is deleted at attempt end with a journal entry and never enters quarantine; a node restart either keeps the channel or the realization shows the gap; every surface shows the exposure statement for a delivered credential |
| 13 | Relationships | Uses EX-09's endpoint; feeds EX-13's registry-only acquisition egress; the product definition §9 network gap becomes per tier when promoted (§15.2); EX-14's action budgets count distinct N1 destinations |
| 14 | Invest or reject | **Invest:** N1 passes on the reference distribution and brokers work with unchanged tools. **Reject:** clients ignore proxies widely, or protocol drift costs more than the value; cost above X % |

### 14.4 Theme 3: lifecycle (EX-13, EX-16)

Theme purpose: make what runs the thing the owner approved, keep the owner's work reviewable, and state honestly what removal and rollback can and cannot restore. Lifecycle facts never raise an isolation strength (M3).

#### EX-13 Governed acquisition and OWNED lifecycle

Status: exploratory. Recommended to the owner for RM: **stage a**.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | "The MCP server or tool I approved is the one that runs, by digest": launchers such as `npx -y`, `uvx`, `pnpm dlx`, `bunx`, `dnx` and `docker run` make launching an install, with the client configuration as the only manifest. The owner sees what clients launch, pins it with consent, is told when a tool's definitions change, and later gets owned versions with rollback and an honest three-part removal statement |
| 2 | Fit with the conceptual model | Stage b introduces the **Installation** entity (concept 3), generalizing `install_source` ([AD-0012](../decisions/AD-0012-distribution-and-updates.md) §4); its uses are ArcForges' own install, OWNED tools, DELEGATED reporting, version rollback, residue statements and MCP digest pins. M3 couplings are one-directional and recorded: an Installation's default profile, the installation floor in `meet`, split acquisition and run profiles (O4), the owned-state snapshot before an update switch, `state_root:<installation>` grants. Stage a needs no new concept |
| 3 | Existing capabilities | IntegrationService plan, apply and remove with exact diffs and consent (AF-AI-02); the MCP adapter (AF-MCP-01); records; CAS by digest (AF-CACHE-01); managed roots and two-phase cleanup (AF-STOR-01); the update switch, health check and rollback (AF-DIST-02, `R-DIST-003`); toolchain detection (`R-TOOL-001`); bypass detection (`R-AI-006`); the journal (EX-08) |
| 4 | Platform scope | All three OSes. Windows sets Mark-of-the-Web on every executable ArcForges fetches or extracts; macOS sets `com.apple.quarantine`; Linux records signature checks as provenance. macOS extraction is UNAVAILABLE until an App-Sandboxed helper executable exists (a second signed binary, which RM-14 does not cover today; it would need RM-14's Item widened, or its own row), because no role of the one signed binary can be App-Sandboxed |
| 5 | Expected guarantees | Stage a: OBSERVED statements for observed launches; GUARDRAIL for consented pins (same-user code can edit client configuration; a changed definition is detected). Stage b: **the acquisition profile's realization only; the installed artifact gets no security claim.** Provenance (npm provenance, PEP 740, crates.io trusted publishing, NuGet signatures, cosign), OS gate verdicts and cooldown are **recorded inputs, never safety claims**. Removal: exact for journal entries and owned roots; "Not known" for the rest unless the weakest-run rule holds; version rollback by pointer, never data rollback |
| 6 | Candidate mechanisms | **Stage a:** O1 observe (parse client configurations and launcher caches), O2 pin (a consented rewrite to `pkg@x.y.z`, `@sha256:`, `uvx --no-build --exclude-newer`), `tools/list` digests with `TOOL_DEFINITION_CHANGED`, and the wrapper `arcforges mcp-wrap --acq <id>`, which fails closed. **Stage b:** the acquisition attempt (resolve, fetch and verify under its own profile, writes to staging only, registry-only egress where N1 exists); materialize into a read-only version directory; cache by digest; bind as a journal entry; run as a SERVICE or COMMAND task referencing the Installation; O4 split acquisition and run profiles; MOTW and quarantine kept on every fetched or extracted executable, never stripped, and an OS block a reported refusal (`blocked by OS policy`), never retried without the mark; **OS verdicts (SmartScreen, Smart App Control, Gatekeeper) as recorded supply inputs**; cooldown and publisher continuity; `update_owner` with exactly one owner per Installation; the three-part uninstall with the weakest-run rule and the durable `ran_unconfined` summary. Untrusted formats are parsed only under the helper-role profile. **Later stage:** OWNED portable applications (lifecycle only; residue "Not known" while they run unconfined; not GUI confinement) |
| 7 | Compatibility and exclusions | Stage a is transparent except for the consented rewrite. Stage b: O4 becomes a default only when LAB-X-04 reaches at least 80 %; between 60 and 80 % opt-in; below 60 % not recommended. The cost of keeping OS gates is stated: Smart App Control may block unsigned tools and Gatekeeper may prompt for or translocate un-notarized CLIs (measured in LAB-X-04 and LAB-MAC-14). Excluded: self-updating applications from OWNED (their updater replaces the install root; DELEGATE with rollback NONE, or refuse); forcibly disabling vendor updaters; machine-wide installers, services and drivers; repackaging; an apt or rpm frontend; a registry proxy; an application launcher |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the no-install amendment of [05](05-toolchains-caches.md) §1, whose text is in §15.1 (`requirements.md` unchanged) |
| 9 | Risks and open questions | Becoming a package manager (weighed against delegation below); per-ecosystem launcher drift; T-32 managed-artifact substitution, re-resolution and tool-definition change; T-35 install- and launch-time code; T-30 parser compromise; owners declining rewrites. Open: can pinning stop re-resolution across launchers (LAB-X-05); do split acquisition profiles run a real corpus at 80 %; is delegation cheaper to maintain than an owned store |
| 10 | Research and prototypes | LAB-X-02 (MCP wrapping, `tools/list` digests, definition-change simulation); LAB-X-04 (split acquisition profiles, with MOTW and quarantine legs); LAB-X-05 (re-resolution); LAB-X-13 (the Sigstore and TUF .NET libraries, AOT); LAB-LNX-20 (residue, rollback and uninstall statements, `ran_unconfined`); LAB-MAC-14 (with the quarantine leg); LAB-WIN-16 (vendor updaters); gates G21, G22, G30, G39 |
| 11 | Internal delivery stages | **a:** O1 observe and O2 pin; definition-change findings. **b:** one of the alternatives below, O4, MOTW and quarantine, OS verdicts, `update_owner`, the three-part uninstall. **Later:** OWNED portable applications |
| 12 | Acceptance criteria | **a:** an unpinned launcher entry in a supported client's configuration is reported with its client and route; a consented pin survives a client restart and the next launch resolves to the pinned version or digest; a changed `tools/list` digest raises `TOOL_DEFINITION_CHANGED` and the wrapper fails closed until the owner accepts. **b:** every executable ArcForges extracted carries MOTW or quarantine, and an OS block is a reported refusal; an uninstall gives the three-part result and removes every journal entry and owned root of the Installation; a self-updating application is refused as OWNED; `ran_unconfined` survives `PurgeTaskRecord`; O4 runs the corpus at its measured rate before any default |
| 13 | Relationships | Gives RM-12 its alternative trigger (the consented rewrite as a launch hook); uses EX-12's registry-only egress; takes EX-15's persistence diff as residue candidates; its owned versions feed EX-16's environment digest and RM-04; EX-21 is the DELEGATED MSIX path; EX-18's Windows Sandbox is the installer-assessment path |
| 14 | Invest or reject | **Invest:** stage a when unmanaged MCP load is visible in bypass evidence or the owner confirms; stage b when split acquisition works. **Reject:** pinning cannot stop re-resolution; owners decline the rewrites; delegation is clearly cheaper than an owned store (then alternative 2 below) |

**Alternatives for stage b**, weighed at promotion, each with its maintenance burden:

| Alternative | What ArcForges owns | Maintenance burden | Trade-off |
|---|---|---|---|
| 1. An OWNED store across `dnx`/NuGet, npm/pnpm, uv/pipx and `cargo --root` | Resolution, fetch, verification, materialization and removal per ecosystem | **M–H**: per-ecosystem launcher drift, flags and cache layouts | Exact removal and pinning per ecosystem; the most code to keep current |
| 2. DELEGATED to mise or aqua, run inside an ArcForges acquisition attempt under O4 | The acquisition attempt, its profile and records; the manager owns resolution | **L–M**: one manager's behaviour to track; mise verifies checksums, cosign, minisign, SLSA and GitHub attestations and applies a default release-age cooldown (D-x-lifecycle-7) | Fewer ecosystems to track; ArcForges quotes the manager's guarantees and reports `update_owner = MANAGER`; it does not run installs on the owner's behalf by default |
| 3. A hybrid: delegated resolution, OWNED materialization by digest | Materialization, version directories and removal | **M** | Keeps exact removal and pointer rollback while leaving resolution semantics to the manager |

None is chosen now. Under boundary 4 of [AD-0017](../decisions/AD-0017-delegated-execution-direction.md), a small store of tool versions acquired on explicit request is the most ArcForges would own, and even that is weighed against delegation first.

#### EX-16 Session worktrees, reviewable delegated writes and owned-state snapshots

Status: exploratory. A priority, P0 on specified patterns, but not an RM recommendation: its trigger is observed demand, which the owner can judge after release 1.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | The most frequent agent harm is damage inside the granted workspace (A1), which no sandbox prevents. Each agent session gets its own managed worktree; its writes stay there until the owner reviews a diff and lands them; a discarded session restores the base exactly; archive and restore round-trip. This works at day-one strength, with no confinement |
| 2 | Fit with the conceptual model | **No new concept.** It binds a managed worktree (AF-WS-01) to a session, and later to the delegation envelope's workspace (EX-14). Stage b's snapshots use the clone primitive and quarantine-managed storage; versioned environments are a derived view (§2.4), not an entity |
| 3 | Existing capabilities | Workspaces and managed worktrees with branch, base and owner recorded, and archive-before-remove of dirty worktrees (`R-STOR-003`; AF-WS-01, SPECIFIED, L-19); two-phase cleanup and quarantine (`R-STOR-006`; AF-STOR-01); sessions (AF-AI-01) |
| 4 | Platform scope | All three OSes for stage a. Stage b: clone primitives differ per filesystem (reflink, block clone on ReFS or Dev Drive, `clonefile` on APFS, else copy); Linux can freeze (E1), Windows cannot, so Windows snapshots are STOPPED only |
| 5 | Expected guarantees | Stage a: protection by review against A1 inside the workspace; **`.git` protection is NONE or GUARDRAIL for unconfined sessions, PARTIAL at most for confined ones**; the worktree is not a boundary against A3–A5. Stage b: data restored only from snapshots taken while the workload was STOPPED or FROZEN, with `consistency` recorded; `LIVE_UNSAFE` only on explicit owner acceptance; snapshots opt-in and size-bounded |
| 6 | Candidate mechanisms | **Stage a:** one managed worktree per agent session on AF-WS-01; diff review before landing; archive and restore; workspace provenance where confined (EX-09). **Stage b, research:** clone or overlay try-then-apply runs (try in a copy, review, apply or discard); owned-state snapshots into quarantine-managed storage; the environment digest (profile digest + pinned installation versions + workspace + environment snapshot) as the key for versioned environments, a relationship to RM-04 |
| 7 | Compatibility and exclusions | Tools that need the original checkout path, or that write outside the repository, are not helped. Excluded: privileged snapshots (VSS, LVM, ZFS, APFS); data rollback outside owned roots; OS credential stores; app-migrated schemas without a prior snapshot |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell; no intra-row needs beyond it |
| 9 | Risks and open questions | Merge conflicts on landing; the disk use of many worktrees (bounded by quotas and cleanup); snapshot consistency. Open: does a per-session worktree with review cover the common agent harms; are clone or overlay runs cheaper or safer than worktrees; is the environment digest stable enough for versioned environments |
| 10 | Research and prototypes | Stage a: none beyond AF-WS-01's own verification. Stage b: LAB-X-12 (clone and copy cost on 1k–100k files), LAB-LNX-15 (a delegated ZFS snapshot), LAB-LNX-16 (an unprivileged overlay upper); gate G24 |
| 11 | Internal delivery stages | **a:** session worktrees with review, archive and restore. **b (research):** try-then-apply and owned-state snapshots. Versioned environments stay a relationship to RM-04, not a stage of their own |
| 12 | Acceptance criteria | **a:** an agent session's writes stay in its worktree until the owner lands them; discarding a session restores the base commit exactly; archive and restore round-trip a dirty worktree; two sessions on one repository never write the same worktree; `.git` protection is reported with its true strength. **b:** a snapshot taken while stopped restores owned state bit-exactly, and a live snapshot is refused without explicit acceptance |
| 13 | Relationships | The envelope's workspace (EX-14); the default writable workspace for Windows confinement (EX-10); the copy-out path for Linux ephemeral-state profiles (EX-11); RM-04 for versioned environments |
| 14 | Invest or reject | **Invest:** stage a when owners run several agent sessions on one repository. **Reject stage b:** clone costs exceed worktrees, or snapshots cannot be made consistent without privilege |

### 14.5 Theme 4: coordination and ownership (EX-14, EX-15)

Theme purpose: bound whole delegations rather than single commands, and show the owner what managed work left behind in startup and background mechanisms. Control stays limited to what ArcForges launched or the owner explicitly adopted or held.

#### EX-14 Delegation envelopes and workload groups

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | "This agent session may use these grants until 18:00, and 8 GiB and 6 cores in total"; closing the session revokes everything it holds in one operation. Inside the envelope the agent acts freely; at its edge it requests |
| 2 | Fit with the conceptual model | Introduces the **delegation envelope** (concept 4): **a policy record in `PolicyDocument`, keyed by session**, with grants, expiry, workspace, action budgets and a resource budget, and the lifecycle OPEN → DRAINING → CLOSED. Its uses: one-operation revocation; action budgets; session worktrees (EX-16); agent introspection; the AI client as a confined SERVICE attempt. The **group container** is an extension, an optional realization of the resource budget, not the envelope itself. **The SESSION kind only; the APPLICATION kind is dropped until it has a second use** |
| 3 | Existing capabilities | Admission with `max_running_per_session`, pools and fair share (AF-SCHED-01; `R-EXE-013`, `R-EXE-014`); sessions and hooks (AF-AI-01); policy revisions; approvals (AF-SEC-01); the root and attempt container levels (DELIVERED) |
| 4 | Platform scope | **Windows:** a group job level between root and attempt jobs, gated on LAB-WIN-02 and the two-to-three-level runtime transition while attempts recovered by name are running. **Linux:** nested slices under `arcforges.slice` (LAB-LNX-13). **macOS:** monitored only, no aggregate enforcement. The envelope's grants, expiry and revocation need no container on any OS |
| 5 | Expected guarantees | Resource budgets: CONTAINMENT, at admission everywhere, and ENFORCED against A1/A2 for the group only where the group container is proven (E4), with the same-user qualifier (T-22). Grants: as their backend realizes them; an envelope never raises a strength. Revocation on close: IMMEDIATE for mediated channels and limits, other classes as stated (§7.4). Action budgets are guardrails on the agent's rate of asking, never a security boundary |
| 6 | Candidate mechanisms | The envelope record keyed by session; admission budgets mapped additively from `max_running_per_session`; an optional group container where proven; the **shared-SERVICE rule** (§2.3). **Later stage: action budgets** (approvals requested per hour, grant widenings, distinct N1 destinations, acquisitions); exhausting one pauses submission with `AUTHORIZATION/budget_exhausted` and notifies the owner, and **never auto-approves**. **Question:** should owner-scoped profile templates replicate across the owner's paired machines over the existing LAN pairing, each node still realizing and refusing locally? It would be free under [AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2 and is not team policy, which stays its own accepted roadmap row (team administration) |
| 7 | Compatibility and exclusions | Transparent to workloads. Excluded: the group container as the envelope (rejected); an APPLICATION group kind; team-wide policy (the team-administration row) |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the group container (stage 2) needs LAB-WIN-02 and LAB-LNX-13 |
| 9 | Risks and open questions | The two-to-three-level runtime transition on Windows; T-37 approval fatigue and misleading approval content (the exact grant delta at D2 to the approver, short widening TTLs, action budgets); unattended widening requests waiting in the local queue (push and remote decisions of other approvals are the Pro convenience; the editions check). Open: is admission alone enough for session budgets; the profile-template question |
| 10 | Research and prototypes | LAB-WIN-02 (with the runtime-transition leg), LAB-LNX-13, LAB-MAC-05 (monitored groups); gate G13 |
| 11 | Internal delivery stages | **1:** the envelope record with grants, expiry, workspace and admission budgets; one-operation close. **2:** the group container where proven. **Later:** action budgets |
| 12 | Acceptance criteria | Closing an envelope revokes its grants, closes its attempt endpoints and releases its group container, with each grant's revocation class recorded and IMMEDIATE ones effective at once; a shared SERVICE never holds more than the meet of its users' envelopes and is revoked for each user on that user's close; an exhausted action budget pauses submission, notifies the owner and never approves anything; with the group container, a budget overshoot is enforced for the group on Windows and Linux and only reported on macOS |
| 13 | Relationships | Hosts EX-09's later stages (the AI client runs inside its envelope; agent introspection reads it); EX-16's worktree is its workspace; EX-12's destinations count toward action budgets; team-wide policy stays the team-administration row; the profile-template question relates to the LAN pairing of [AD-0008](../decisions/AD-0008-lan-trust-and-placement.md) |
| 14 | Invest or reject | **Invest:** owners run several heavy agent sessions and ask for per-session totals, or the first CONFINED default for an origin nears. **Reject:** admission-only session tags suffice; the group container is dropped if three-level containers cannot be proven |

#### EX-15 Persistence diff, inventory and holds

Status: exploratory. Recommended to the owner for RM: **stage 1**.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | "What did this attempt add to startup, services and scheduled tasks, and who added it?" OS startup views show entries without attribution; ArcForges can attribute what appears during a managed attempt by construction. Later, an opt-in view of every autostart entry, and reversible per-user holds |
| 2 | Fit with the conceptual model | **No new concept.** A record kind (the per-attempt persistence diff), a finding kind (`PERSISTENCE_ADDED`), an adoption kind (persistence holds, HUMAN only) and a journal writer kind (`PERSISTENCE_HOLD`) |
| 3 | Existing capabilities | Records and timelines (AF-REC-01); findings, remedies and the doctor (AF-DIAG-01; `R-DIAG-002`); adoption, same-user only and recorded (AF-SEC-01; `R-RES-013`); bypass detection (`R-AI-006`); the journal (EX-08) for holds |
| 4 | Platform scope | All three OSes, per-user entries: Windows Run keys, Startup folders, per-user scheduled tasks; Linux user units, autostart files, shell profiles; macOS LaunchAgents and Login Items. Machine-wide entries: observe only, never controlled (D-persistence-observation-recovery-2) |
| 5 | Expected guarantees | Stage 1: OBSERVED, attributed to an attempt only within its window. Inventory: OBSERVED, off by default. Holds: **GUARDRAIL by nature** (same-user code can re-create a held entry), labelled "held", never "blocked". Elevated writes of an attempt land in another account's profile and are not visible (`Not known`) |
| 6 | Candidate mechanisms | **Stage 1:** a bounded before-and-after diff of per-user persistence locations around each managed attempt, raising `PERSISTENCE_ADDED` with the attempt ID. **Later:** a machine-wide inventory at P0, **opt-in and off by default**, with machine-wide sources kept only as rows inside a managed attempt's window, labelled "seen during attempt <id>, cause unknown". **Later:** per-user holds through the OS's own mechanisms (disable rather than delete), each a journal entry with exact release, re-checked at the OS mechanism; these **need the product definition §7 amendment (§15.2) and an owner decision** |
| 7 | Compatibility and exclusions | No workload is changed by stage 1 or the inventory. Excluded: machine-wide persistence control; an inventory on by default; EDR-style continuous monitoring outside attempt windows |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell; no intra-row needs beyond it |
| 9 | Risks and open questions | False positives from background activity; drift toward an EDR (mitigated by attempt windows and the opt-in inventory); T-41 re-creation of a held entry. Open: can standard-user detectors attribute persistence with few false positives; can a standard user hold and release per-user entries exactly through the OS's own mechanisms |
| 10 | Research and prototypes | LAB-WIN-07 (privileged-change signals at P0), LAB-WIN-08 (what a standard user can enumerate, disable or hold), LAB-WIN-12 (false positives of the bounded diff), LAB-LNX-17, LAB-MAC-13; gates G31, G32 |
| 11 | Internal delivery stages | **1:** the per-attempt persistence diff. **Later:** the machine-wide inventory, opt-in. **Later:** holds, after the owner's §7 decision |
| 12 | Acceptance criteria | **1:** a Run key, per-user scheduled task or user unit added during an attempt raises `PERSISTENCE_ADDED` naming that attempt; an entry added outside any attempt is not recorded by default; findings carry D2 detail locally and only their titles remotely; false positives on the lab background corpus stay within the bound LAB-WIN-12 sets. **Holds:** a held entry is reported "held" on every surface, re-creation raises a finding, and release restores the exact prior state from the journal |
| 13 | Relationships | Gives EX-13's uninstall its observed residue candidates; uses EX-08 for holds; complements the three-part uninstall; `PRIVILEGED_CHANGE_OBSERVED` stays limited to attempt windows (§10) |
| 14 | Invest or reject | **Invest:** stage 1 when detectors pass at P0 or the owner confirms. **Reject:** false positives make the findings noise; holds are never built without the owner's §7 decision |

### 14.6 Theme 5: platform (RM-15, EX-22)

Theme purpose: make macOS an execution target as request §3 decides, deliberately lightweight, delegating to the OS wherever it already provides guarantees, and stating plainly that the macOS node is the weakest of the three.

#### RM-15 macOS node, stage 1 (from EX-05)

Status: **accepted** (from EX-05, which becomes `accepted as RM-15`). The recorded decision is request §3 ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 10). It reverses the scope position recorded in [AD-0002](../decisions/AD-0002-platform-scope.md) ("macOS is outside the current implementation and acceptance scope"), which followed the product owner's 2026-10-08 decision that macOS was not required for that delivery. Only stage 1, the monitored local node, is accepted; Seatbelt confinement is EX-22. Accepted work is never implemented before promotion (the roadmap's §4).

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Developers on macOS get the same task, attempt, record, admission and remote-monitoring model as on Windows and Linux, honestly weaker: the node monitors resources, kills trees, records evidence and says on its first screen that it is the weakest node |
| 2 | Fit with the conceptual model | The third implementation of the delivered execution-platform seam (`IExecutionPlatform`, `IAttemptHandle`); **no new concept**. Every access dimension reads NONE through EX-07's contract |
| 3 | Existing capabilities | The seam (DELIVERED; AD-0002's dated revision of 2026-10-19 replaces its eight-interface list with the delivered seam); records; admission; the `R-RES-008` refusal; the update switch and signed manifests ([AD-0012](../decisions/AD-0012-distribution-and-updates.md)); the per-user install model |
| 4 | Platform scope | macOS on Apple silicon only, **as a study proposal**: AD-0002 defines no macOS floor, and the proposal rests on owner decision D4's lab hardware and Apple `container` being Apple-silicon-only; the owner decides (§17, decision 21). Local only first; the LAN stage later. Execution only: no mobile-local execution on iOS (request §3) |
| 5 | Expected guarantees | `cpu`, `memory`, `pids`, `io` **OBSERVE_ONLY**; per-process `RLIMIT_CPU` and `RLIMIT_FSIZE` PARTIAL; **no aggregate or rate enforcement**, so `R-RES-008` refuses aggregate CPU and memory requirements; `pause = UNSUPPORTED`; `kill_tree = BEST_EFFORT`; `restart_survival = false` until LAB-MAC-04; every access dimension NONE. App Sandbox, TCC, Gatekeeper and SIP of vendor apps are reported, never claimed. **`tcc_attribution = NODE (aggregating)` by default:** the LaunchAgent node is the responsible process, so a TCC grant the owner gives at a prompt raised by one managed tool applies to every later tool |
| 6 | Candidate mechanisms | The node as a Developer-ID-signed, notarized user LaunchAgent at a stable bundle path; one session per attempt with a holder; rlimits (CPU, FSIZE, NOFILE); QoS and I/O tier; node-monitored memory and process counts via libproc; `LOCAL_PEERTOKEN` for local callers; the node never holds Full Disk Access or App Management, and its data root stays outside protected folders; the first screen and `GetReleaseScope` state "macOS is the weakest of the three nodes" and the TCC aggregation sentence; the doctor reports the TCC categories the node holds, where detectable; a stage-1 switch refuses, or asks the owner to acknowledge, workspaces in protected folders. Responsibility disclaim (a private SPI, UNDOCUMENTED) is PREFERRED only, and "non-aggregation" is said only when disclaim is active and probed |
| 7 | Compatibility and exclusions | High for a monitored node: tools run unchanged as the user. Excluded: a confined tier (EX-22); Endpoint Security, Network Extension, kexts, the jetsam SPI, `TCC.db` edits, stripping quarantine; `RLIMIT_AS` and `RLIMIT_NPROC` as defaults; extraction of hostile archives (UNAVAILABLE without an App-Sandboxed helper executable, a second signed binary that RM-14 does not cover today); LAN server-side TLS 1.3 (not before .NET 12, and not committed then) |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the LAN stage (stage 2) also needs G35, the TCC disclaim decision and Local Network inheritance |
| 9 | Risks and open questions | Maintenance per macOS release (TCC behaviour, Background Task Management); TCC aggregation; the disclaim decision (an owner question: disclaim by default, UNDOCUMENTED and never satisfying REQUIRED, or no disclaim with the aggregation disclosed); LAN TLS; Keychain behaviour in tests (throwaway guests only, never the owner's store). **Narrowing question for G25:** does a monitored node add enough over macOS as a control client plus Linux workloads in Apple `container`? That is for the owner, never a design consequence, because request §3 makes macOS an execution target |
| 10 | Research and prototypes | LAB-MAC-02 (its TCC-attribution and Local Network legs), LAB-MAC-03 (headless TCC prompts), LAB-MAC-04, LAB-MAC-06 to LAB-MAC-09 and LAB-MAC-15's audit-token leg (gate G25, which holds no Seatbelt leg; LAB-MAC-01, LAB-MAC-02's Seatbelt leg and LAB-MAC-15's Seatbelt legs belong to G41 only); LAB-MAC-12 (gate G35, with the outbound-only LAN client option); LAB-MAC-11 for Keychain behaviour on throwaway guests |
| 11 | Internal delivery stages | **1:** the monitored local node. **2:** LAN, after G35 and the disclaim and Local Network decisions |
| 12 | Acceptance criteria | `R-RES-008` refuses an aggregate CPU or memory requirement on macOS with a reason; the first screen and `GetReleaseScope` carry the weakest-node and TCC-aggregation statements; every access dimension reads `NONE (same-user tier)`; a process tree either survives a node restart or `restart_survival = false` is reported; kill-tree is reported `BEST_EFFORT`, and a daemonizing child that escapes is reported, never claimed killed; the node holds no Full Disk Access; the signed, notarized bundle keeps its TCC grants across an update (LAB-MAC-07) |
| 13 | Relationships | EX-22 builds on it; EX-18 weighs Apple `container`; EX-05 is its source row; RM-14's second-binary question (macOS helper isolation); EX-07's contract reports its values |
| 14 | Invest or reject | **Invest:** the hardware and membership exist (D4) and G25 shows value. **Narrow:** the owner decides if G25 shows little value. **Reject:** not as a design consequence (request §3); only by a new owner decision |

#### EX-22 macOS Seatbelt profiles

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Narrow what MCP servers and hooks can reach on a macOS node, where no documented standard-user sandbox for ordinary CLI processes exists |
| 2 | Fit with the conceptual model | A backend of the access profile with a DEPRECATED `api_status`; no new concept; uses the `exec-final` role on macOS |
| 3 | Existing capabilities | RM-15 (the node); EX-07 stage b (profiles); the `exec-final` role (EX-11) |
| 4 | Platform scope | macOS 15, 26 and 27 on Apple silicon |
| 5 | Expected guarantees | Attainable, pre-lab (§5.3); every cell carries `api_status = DEPRECATED`. `fs.*` PARTIAL ("self-check passed"); `config` N/A (preferences are files, folded into `fs`); `net.out` PARTIAL (a localhost proxy matches every local address); `net.in` unmeasured (E5) until LAB-MAC-01's listen leg; `ipc` PARTIAL (the per-version Mach allowlist; every allowed service not shown to enforce the caller's profile is a gap); `devices` unmeasured, with no device claim until a lab measures it; `creds` PARTIAL (credential files by `fs` rules; the Keychain through an allowed Mach service is a gap unless denied); `persist` PARTIAL at best; `exec` PARTIAL by process-exec rules, `exec.elevation` unmeasured; `visibility` NONE (no process namespace); `res` as RM-15; `identity_strength` capped at PARTIAL; no `ui` claim. **Launcher cells (escape class):** any allowed launch- or write-brokering Mach service (Launch Services, launchd job submission, Apple Events), and any allowed service not yet measured, is an escape gap of the realization, so every dimension then holds against {A1, A2} only. REQUIRED is satisfied only with a local HUMAN `accept_deprecated`, a passing host probe **and** `min_strength = PARTIAL`. Anything allowed through `mach-lookup` runs outside the sandbox |
| 6 | Candidate mechanisms | Deny-default SBPL profiles chosen by HUMAN policy (allow-default profiles rejected); the chain `sandbox-exec -p <profile> arcforges exec-final -- <workload>` through the absolute `/usr/bin/sandbox-exec`; an in-profile self-check that probes canary denials (a write outside the root, a protected read, an external connect) and reports PARTIAL ("self-check passed"), never ENFORCED; a per-version Mach allowlist with no launch- or write-brokering service (Launch Services, launchd job submission, Apple Events); no wildcard `mach-lookup` unless HUMAN policy sets it. **Alternative weighed:** Apple `container` for cross-platform class-1 servers (Node, Python), a VM boundary that is orchestrated, never installed, and accounted as one `GUEST_VM` consumer |
| 7 | Compatibility and exclusions | GUI, Apple Events and XPC-heavy tools break. Excluded: read-broad profiles counting for the weakest-run rule; any macOS confined widening from a remote surface |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the `exec-final` role on macOS, and a local HUMAN `accept_deprecated` before any REQUIRED use |
| 9 | Risks and open questions | Deprecation without a replacement for unpackaged processes; brokered Mach services; per-release maintenance (rated H). Open: does it add measurable value over the clients' own Seatbelt sandboxes at an acceptable per-release cost; does Apple `container` serve cross-platform servers better |
| 10 | Research and prototypes | LAB-MAC-01 (with the TCP and UDP listen leg), LAB-MAC-02's Seatbelt-deny leg, LAB-MAC-11, LAB-MAC-15's Seatbelt and broker legs, the macOS Seatbelt corpus of LAB-X-01; LAB-MAC-10 for the `container` alternative; gate G41 |
| 11 | Internal delivery stages | One stage, opt-in per profile |
| 12 | Acceptance criteria | The self-check denies a canary write outside the root, a protected read and an external connect before the workload starts, and the value is reported PARTIAL with the DEPRECATED label; REQUIRED is never satisfied without `accept_deprecated`, a passing probe and `min_strength = PARTIAL`; a profile whose Mach allowlist contains a launch- or write-brokering service never qualifies for the weakest-run rule; no macOS confined widening is accepted from a remote surface |
| 13 | Relationships | Builds on RM-15; promoted with EX-07 stage b if it is the first confined backend, and uses EX-09 for node reach; weighed against EX-18's Apple `container`; uses EX-07's contract and EX-11's `exec-final` role |
| 14 | Invest or reject | **Invest:** only if value over the clients' own sandboxes is measured. **Reject:** Seatbelt is removed or broken in a macOS release, Apple `container` serves class 1 better, or the per-release cost exceeds the value; cost above X % |

### 14.7 Theme 6: research backends and integrations (EX-17 … EX-21, EX-23)

Theme purpose: keep research-only options visible with their triggers, so that future work does not repeat the investigation. Every row is research only; none is a commitment, and several depend on a privilege the core never takes.

#### EX-17 Windows OS sandbox APIs (SBOX, PSEC) and MXC

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Use a documented Windows path to egress control or broader grants, if one appears, instead of the hand-built AppContainer's "no network or full network" |
| 2 | Fit with the conceptual model | A gated backend of the access profile; no new concept |
| 3 | Existing capabilities | EX-10's holder launch mode, journal objects and composite read-back |
| 4 | Platform scope | Windows only; builds of the 26300 servicing series or Insider images for the newest APIs (owner decision D2) |
| 5 | Expected guarantees | Capped at "active, experimental" (or "active, undocumented", "active, preview"): EXPERIMENTAL, UNDOCUMENTED and PREVIEW never satisfy REQUIRED and may realize only PREFERRED dimensions. Promotion to DOCUMENTED-equivalent is a Design decision per backend and build class, never a node flag, and needs the six conditions of §3.3. PSEC returned access denied for a standard user in a public report (E4 until LAB-WIN-03) |
| 6 | Candidate mechanisms | The OS sandbox APIs (SBOX, PSEC, `Experimental_CreateProcessInSandbox`; D-x-agents-3); MXC (Microsoft Execution Containers, generally available since 2026-10-07, the closest prior art for the access-contract half; D-x-agents-1, -2) as a backend engine. MXC ships a Rust native unit (`mxc_ffi`) plus possible sidecars (unverified) |
| 7 | Compatibility and exclusions | Unknown; nesting in ArcForges' jobs is unproven. Excluded: direct PSEC or `Experimental_` APIs as a guarantee; MXC now |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the ADR follows [AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §6 direction (c), recorded with the first EX row that would ship a native unit; the licence review covers `wslcsdk.dll`, whose licence is unverified |
| 9 | Risks and open questions | Young, undocumented or experimental interfaces; host residue (MXC-style host ACLs, T-33); AOT cleanliness; a native unit against AD-0003 §6 |
| 10 | Research and prototypes | LAB-WIN-01 (in-job composition), LAB-WIN-03 (MXC residue, tier selection, PSEC and SBOX admissibility outside a job); gate G09 |
| 11 | Internal delivery stages | One research stage |
| 12 | Acceptance criteria | Research maturity: LAB-WIN-03 records, on a named build, whether a launch nests in ArcForges' jobs with limits, accounting and termination intact and leaves no untracked host residue; any value it would add is shown "active, <status>" and never satisfies REQUIRED |
| 13 | Relationships | An alternative engine for EX-10; would change EX-12's Windows egress statement only after promotion to DOCUMENTED-equivalent |
| 14 | Invest or reject | **Invest:** the API is documented, or its `Experimental_` prefix is removed, and LAB-WIN-01 and LAB-WIN-03 pass. **Reject:** it stays undocumented, needs a shipped native unit that fails review, or leaves untracked residue |

#### EX-18 STRONG backends

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | VM-class or kernel-separated execution for untrusted work, and installer assessment in a disposable environment, where same-kernel confinement is not enough or not available |
| 2 | Fit with the conceptual model | Backends of an attempt, each accounted as one `GUEST_VM` consumer exactly as the WSL VM is today (`R-RES-010`, `R-RES-011`); **not persistent environments ArcForges manages**; no new concept |
| 3 | Existing capabilities | The WSL accounting model (AF-WSL-01); the attempt and its records; EX-09's endpoint for node reach from a guest |
| 4 | Platform scope | Windows Sandbox (not available on Windows Home), with Hyper-V and HCS as reference only (HCS needs Hyper-V Administrators); rootless Podman with `--cgroups=split` and gVisor on Linux; Apple `container` on macOS (bare-metal Apple silicon); OS agent accounts on Windows tracked only, with no backend work until documented |
| 5 | Expected guarantees | **Per backend row**, never generically: VM-class backends A1–A5 within the vendor boundary as configured, with the A5 sentence (§4.1); same-kernel backends (rootless Podman) A1–A4; account backends A1–A4, A5 only for a non-admin account; microVMs A5 only if the VMM is confined; `net` and `ui_isolation` per backend. Channels the backend's defaults open (networking, clipboard, mapped folders) are stated |
| 6 | Candidate mechanisms | `wsb.exe` for Windows Sandbox, including installer assessment recorded as `VM_CAPTURED`; `podman` rootless with split cgroups; `runsc`; Apple `container`; each orchestrated by absolute, probed path, reported and **never installed** by ArcForges |
| 7 | Compatibility and exclusions | Each needs an owner-enabled feature (P1). **The container-platform drift guard:** ArcForges never manages images, registries, volumes or networks; a backend that needs it is rejected. Excluded: Windows containers, MDAG, Windows 365 for Agents, bundled Sandboxie; Hyper-V or HCS as a backend; Docker-based MCP servers counted as "contained" |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: each backend needs the owner's one-time enablement of its OS feature (P1) |
| 9 | Risks and open questions | Container-platform drift; Administrator protection is advised against on Hyper-V devices; per-backend residue and stop semantics; licence obligations stay the user's for orchestrated tools |
| 10 | Research and prototypes | LAB-WIN-10 (Windows Sandbox driven by a standard user), LAB-WIN-14 (HCS from AOT C#, reference), LAB-WIN-15 (agent accounts, tracked), LAB-LNX-11 (gVisor cost), LAB-LNX-12 (Podman split, OCI unpacker refusal), LAB-MAC-10 (Apple `container`); gates G10, G29, G33, and G41 for LAB-MAC-10 |
| 11 | Internal delivery stages | Per backend, one at a time, each its own decision |
| 12 | Acceptance criteria | Research maturity, per backend: a standard user (after the owner's one-time enablement) drives it with exact `GUEST_VM` accounting, stop and residue; ArcForges manages no image, registry, volume or network; the per-backend `holds_against` row is written before any value is shown |
| 13 | Relationships | EX-10's reject path (Windows confinement only through STRONG backends); EX-13's installer assessment; EX-22's alternative for cross-platform MCP servers on macOS |
| 14 | Invest or reject | **Invest:** a backend passes its lab with exact accounting and no image management. **Reject:** it needs image, registry, volume or network management, or a privilege beyond a one-time owner step |

#### EX-19 GUI application confinement

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Isolate compatible GUI applications' input, screen and clipboard: the largest deliberate scale-down of this direction (no stage elsewhere sandboxes GUI applications) |
| 2 | Fit with the conceptual model | Would raise the `ui_isolation` basis fact; no new concept. `ui` stays a basis fact, not a dimension, unless a grant can target it on some OS (M2) |
| 3 | Existing capabilities | EX-10's holder-owned window station and desktop; EX-11's view without a display socket |
| 4 | Platform scope | Linux (Wayland security contexts, portals) and Windows (separate desktops). macOS: no confined `ui` claim at any stage |
| 5 | Expected guarantees | Unknown. Today: GUI isolation NONE on X11 and on the shared Windows desktop (D-lnx-projects-28; D-win-primitives-completion-13); compatible GUI applications get LIFECYCLE and CONTAINMENT, never SANDBOX |
| 6 | Candidate mechanisms | Wayland security contexts; separate desktops for GUI workloads; xdg-desktop-portal mediation |
| 7 | Compatibility and exclusions | Most GUI applications break under separation. Excluded: browsers and Electron apps with their own sandboxes from confined profiles; X11 isolation claims |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell; no intra-row needs beyond it |
| 9 | Risks and open questions | No standard-user GUI boundary exists on X11 or the shared Windows desktop; per-compositor variation |
| 10 | Research and prototypes | LAB-LNX-06 (portal classification), LAB-LNX-07 (GUI isolation per compositor), the GUI legs of LAB-WIN-04; gate G28 |
| 11 | Internal delivery stages | One research stage |
| 12 | Acceptance criteria | Research maturity: a lab measures `ui_isolation` at P0 for named real GUI applications per compositor or desktop, and records the result as a basis fact only |
| 13 | Relationships | EX-10, EX-11; EX-13's later OWNED portable applications stay unconfined regardless |
| 14 | Invest or reject | **Invest:** a P0 mechanism isolates real GUI applications. **Reject:** no P0 mechanism exists |

#### EX-20 Optional privileged integrations

Status: exploratory. The AD-0011 §6 alignment question applies here (§17, decision 4).

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | An owner who chooses to grant privilege gets allow-listing of what they installed, richer observation, or the full Linux view on Ubuntu 24.04, without ArcForges taking that privilege itself |
| 2 | Fit with the conceptual model | Journal entries for owner-prompted privileged steps (EX-08); `observe.*` entries; no new concept |
| 3 | Existing capabilities | The journal (EX-08); OWNED install records (EX-13); the designed optional privileged features AR-16 (machine-wide service mode) and A-L02 (Linux I/O control), which stay as [AD-0005](../decisions/AD-0005-resource-enforcement.md) designs them |
| 4 | Platform scope | Windows: App Control supplemental policies built from install records; ETW through an opt-in Performance Log Users membership of the owner's account. Linux: a documented AppArmor profile for bwrap on Ubuntu 24.04 |
| 5 | Expected guarantees | Per integration, stated as the OS mechanism's own; each is a privilege increase of the owner's account, reported as such; observation values limited to OBSERVED, PARTIAL (sampled or lossy) and NONE |
| 6 | Candidate mechanisms | Under [AD-0017](../decisions/AD-0017-delegated-execution-direction.md) boundary 2: *ArcForges never performs an OS-level change silently; an optional privileged step is either the owner's own action or, where AD-0011 §6 applies, an explicit OS prompt with a journal entry and exact removal.* [AD-0011](../decisions/AD-0011-identity-and-login.md) §6 says the optional privileged features, "when built, … install through explicit OS prompts (UAC, sudo)", labelled as OS-level changes. Break-glass removal for allow-listing |
| 7 | Compatibility and exclusions | Excluded: kernel ETW sessions, minifilters, WFP callouts, SELinux module installs, AppLocker or managed installer as a guarantee, any silent elevation |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the owner's AD-0011 §6 alignment decision (§17, decision 4) before any integration is offered |
| 9 | Risks and open questions | Break-glass failure for allow-listing; privilege creep. **Owner questions (§17, decision 4):** (1) keep boundary 2 aligned with the accepted AD-0011 §6, or adopt the stricter rule (ArcForges never performs such a step) by an amendment of AD-0011 §6 and AD-0005 that names AR-16 and A-L02; (2) should the Ubuntu AppArmor profile for bwrap be offered as such a prompted, journaled step? **The study's recommendation (a recommendation, not a decision):** alignment, and the AppArmor profile only after LAB-LNX-01 leg (d) |
| 10 | Research and prototypes | LAB-WIN-13 (App Control supplementals and break-glass), LAB-WIN-07 (ETW with the opt-in membership), LAB-LNX-01 leg (d) (the Ubuntu AppArmor userns profile) |
| 11 | Internal delivery stages | Per integration, each its own decision |
| 12 | Acceptance criteria | Each integration is applied only through the OS prompt AD-0011 §6 names, recorded as a journal entry, removed exactly by `recover` or uninstall, and reported as a privilege increase of the owner's account; break-glass restores the prior policy |
| 13 | Relationships | EX-11 (Ubuntu's full view); EX-13 (install records as allow-list input); EX-08 (exact removal); EX-15 (richer observation of persistence) |
| 14 | Invest or reject | **Invest:** the owner wants the integration and exact removal is shown. **Reject:** no exact removal or break-glass; the owner adopts the stricter rule |

#### EX-21 DELEGATED MSIX and the Desktop identity package

Status: exploratory.

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Install and update vendor MSIX packages through the OS's own deployment, and give the Desktop app package identity where that helps (toasts, Credential Locker) |
| 2 | Fit with the conceptual model | The DELEGATED lifecycle level of an Installation (EX-13 stage b); no new concept |
| 3 | Existing capabilities | IntegrationService; EX-13's Installation; AF-DIST-01's installers; package-manager routes (`R-DIST-005`) |
| 4 | Platform scope | Windows only |
| 5 | Expected guarantees | The OS's own: MSIX write virtualization is a lifecycle fact ("redirected writes removable at uninstall: yes / no / unknown"), never an isolation strength; a package is not a permission boundary |
| 6 | Candidate mechanisms | `PackageManager` and the winget COM API through CsWinRT |
| 7 | Compatibility and exclusions | Needs a Windows TFM (`net10.0-windows10.0.x`) whose AOT status is unverified. Excluded: repackaging, PSF, ArcForges-held trusted keys, Developer Mode, `.appinstaller` auto-update |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: the Windows TFM build ADR needs LAB-WIN-17 and LAB-X-14 to show zero AOT and trim warnings on win-x64 and win-arm64, with Linux RIDs unaffected |
| 9 | Risks and open questions | AOT and trim compatibility; which packages are virtualized; the one-binary-per-platform rule ([AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §1) |
| 10 | Research and prototypes | LAB-WIN-11 (MSIX redirection and removal), LAB-WIN-17 (`PackageManager` and winget COM under AOT), LAB-X-14 (a build spike); gates G11, G12 |
| 11 | Internal delivery stages | One stage |
| 12 | Acceptance criteria | Research maturity: `PackageManager` and winget COM publish AOT-clean in the one binary per platform; for each tested package type, which writes are redirected and removed is recorded |
| 13 | Relationships | EX-13 (the DELEGATED level, `update_owner = MANAGER`); EX-23 (Windows Hello's `UserConsentVerifier` is WinRT too) |
| 14 | Invest or reject | **Invest:** AOT-clean with one binary per platform. **Reject:** AOT or trim failures, or a second binary would be needed |

#### EX-23 End-to-end approval signatures and attested presence

Status: exploratory (the phone as an approver; attested presence).

| # | Field | Content |
|---|---|---|
| 1 | Purpose and user value | Widening and install decisions made away from the machine, from the phone, without trusting the cloud's command key; and local approvals that unconfined same-user code cannot forge. Until this row exists, access-profile widenings and installs will be decided locally only; release 1's opt-in remote approval path (`remote.allow_approvals`, default false) is unchanged and covered by T-11 as amended |
| 2 | Fit with the conceptual model | Approvals and `provenance_strength` (ATTESTED); no new concept |
| 3 | Existing capabilities | Remote commands signed by the cloud's command key and re-checked by the node's local remote-control policy (AF-CLD-05; `R-CLOUD-004`; [AD-0009](../decisions/AD-0009-cloud-relay-and-cost-controls.md) §5); Android actions and approvals (AF-AND-02); LAN pairing ([AD-0008](../decisions/AD-0008-lan-trust-and-placement.md)) |
| 4 | Platform scope | Android first as approver (iOS only if EX-06 is promoted); Windows Hello, macOS LocalAuthentication and a polkit agent for presence on the nodes |
| 5 | Expected guarantees | Signatures: the node verifies a device-bound key it pinned at enrollment over the approval digest, so the cloud becomes a relay only (E4). Presence: **E5; never a boundary until a lab shows same-user code cannot satisfy it**; until then local HUMAN decisions stay GUARDRAIL against unconfined same-user code |
| 6 | Candidate mechanisms | A device-bound phone key enrolled with and pinned by the node, verified over the approval digest (effective profile, floors, requirement fields, grants, acquisition digests); OS-attested user presence for the few decisions that dissolve confinement; after signatures exist, a widening is remote-eligible only if no element of its delta is on the never-remote list |
| 7 | Compatibility and exclusions | Excluded: remote widening or install decisions signed only by the cloud's key; `allow_lifecycle_approvals` in the contract; remote origination of a widening, an install or a profile change |
| 8 | Dependencies and prerequisites | The row's Prerequisites cell, plus intra-row needs: stage 2 (attested presence) needs LAB-X-20's result |
| 9 | Risks and open questions | Presence spoofing by same-user code; key loss and re-enrollment; T-31 remote widening or downgrade. **Owner questions (§17, decision 7):** should remote widening and install decisions exist at all (recommendation: local-only until this row); **the editions question:** should a LAN-only approval path from the phone be free under [AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2? |
| 10 | Research and prototypes | LAB-X-20 (whether an OS presence check can be completed only by a person at the device, not by unconfined same-user code); a signature leg in the remote-command closed loop |
| 11 | Internal delivery stages | **1:** end-to-end approval signatures. **2:** attested presence |
| 12 | Acceptance criteria | The node rejects an approval whose phone signature fails or whose key is not pinned; a valid signature over a different digest is rejected; an item on the never-remote list is refused remotely even with a valid signature; presence is never reported as ATTESTED without the lab result |
| 13 | Relationships | Lifts the remote rule of §7.5; feeds `provenance_strength` and the A4 credit rule of §3.2; T-31; EX-06 (iOS) |
| 14 | Invest or reject | **Invest:** the owner decides that remote widening approvals should exist, and the signature design passes review. **Reject:** presence is forgeable by same-user code (signatures may still proceed alone) |

### 14.8 Existing roadmap rows that change

The exact new cell text is in the roadmap. In summary:

| Row | Change | Home in this chapter |
|---|---|---|
| EX-05 macOS node | `accepted as RM-15`, stage 1 only; request §3 quoted; the reversal of AD-0002's scope position named; the staging named as the study's, not the owner's words; the row is kept | §14.6 (RM-15) |
| EX-06 iOS app | "a remote control client only; no local execution, sandboxing or process supervision" (request §3) | §5.4 |
| RM-12 client-started operations | Inference servers and plugins also launch MCP servers; plugin-provided servers need client support; an alternative trigger in "Revisit when": EX-13 stage a's consented rewrite delivered as a launch hook. The owner is asked about it first among the RM-row changes (§17, decision 1) | §14.4 (EX-13 field 13) |
| EX-01 plugins | Out-of-process plugins as SERVICE attempts under an access profile, WASI only as an inner layer; in-process WASM rejected | §9.1 |
| EX-04 sessions on other nodes | Declarative re-placement with grants re-realized on the target; live migration rejected; placement of cross-platform tools on the local WSL guest as a question | §7.5; §14.3 (EX-11 field 13) |
| EX-03 GPU | `devices.gpu`; no proven GPU deny mechanism on Windows | §8.4; §14.3 (EX-10 field 5) |
| RM-02, RM-04, RM-13 | Cache-trust preconditions, phrased conditionally ("if … is promoted"), so that no accepted row is conditioned on the exploratory model; verified input sets for RM-04's action keys; a shared compiler server at most per profile, if confinement is promoted; each change asked of the owner (§17, decision 1) | §8.6; §14.3 (EX-09 field 13) |
| RM-05 | A loopback listener would be token-authenticated, not peer-identified | §8.3 |
| RM-14 | Unchanged by decision; whether its trigger is met depends on LAB-LNX-19, the G20 cost legs and the macOS helper-executable question | §9.1 |

## 15. Amendment texts recorded in this chapter

[AD-0017](../decisions/AD-0017-delegated-execution-direction.md) lists every amendment of 2026-10-19 with its effective clause. The texts below are recorded here only; the chapters they concern carry a pointer or nothing, and each stays unchanged until its clause takes effect.

### 15.1 The no-install amendment of chapter 05 §1

Today [05](05-toolchains-caches.md) §1 says: "Missing tools are reported, never installed by the node". That stays in force for release 1. The amendment text, recorded now and **effective when EX-13 stage b is promoted**:

> The node never installs tools implicitly. Managed installation happens only on an explicit HUMAN-initiated or approved acquisition into managed roots (OWNED), or through a recorded DELEGATED manager. Optional OS tools that backends use (bwrap, sandbox-exec) are reported, never installed.

`requirements.md` is unchanged: R-TOOL-001 is about detection, and the no-install rule is chapter 05's.

### 15.2 Product definition §7 and §9

The product definition's §2 gains its direction paragraph now ([product definition](../product/product-definition.md) §2). Two further changes are recorded here only:
- **§7 (holds).** The non-goal "Taking control of unrelated applications" would gain one exception, **only by the owner's decision at EX-15's holds stage** (§17, decision 17): *persistence entries the owner explicitly holds: per-user only, recorded, reversible, done through the operating system's own mechanism, and labelled "held", never "blocked".* Until that decision, §7 is unchanged.
- **§9 (network per tier).** The evidence row's gap "Network use per process (inferred only)" would become per tier **when EX-12 is promoted**: measured under N1, sampled on Windows, inferred elsewhere (§8.1). Until then, §9 is unchanged.

### 15.3 SM-ATTEMPT

No `machines.json` change now. The proposed mapping of PLAN, APPLY and VERIFY onto the delivered states is in §2.3; it is decided **at EX-11's promotion**, together with the choice between "RUNNING begins at the workload line" and a sub-state.

### 15.4 The Linux per-confined-attempt overhead (chapter 15)

**When EX-11 is promoted**, [15](15-performance-targets.md) §2's per-execution helper row will record the Linux per-confined-attempt overhead of `exec-init`, measured in LAB-LNX-19 with headroom, in place of today's "Linux 0 per execution". Until then, chapter 15 is unchanged.

### 15.5 Chapters 11 and 01

[11](11-security-privacy.md) §2 and §4 and [01](01-system-overview.md) §4 carry pointers to the tiered threat scope (§4.1), the future boundaries B7–B10 (§4.2) and the future threat rows T-28 … T-42 (§4.4). Each row and boundary enters those chapters only when its roadmap row is promoted.

## 16. Rejected and deferred alternatives

Recorded so that later work does not repeat the investigation.

**Governance and concept:**
- **Reading the request as the product decision for the new rows, confirmed by a reviewer:** rejected. Every new row is EX; the owner is asked.
- **AD-0017 accepting the concepts and the strength ladder now:** rejected; principles only, the model proposed.
- **A cross-row stage diagram, and a second invest-or-reject table:** rejected; Prerequisites cells and "Revisit when" only.
- **A unified environment, sandbox or application entity:** rejected (§2.4). Reopen only if a STRONG backend makes persistent environments enforceable.
- **A separate application runtime beside tasks:** rejected (M1).
- **The APPLICATION group kind:** deferred until a second use exists.
- **The group container as the delegation envelope:** rejected; the envelope is a policy record.
- **Grants inside UNCONFINED profiles, and a grant schema before any backend:** rejected.
- **A separate `ExplainGrant` RPC:** rejected; a dry-run mode of `ExplainTask` instead.
- **A policy language or engine** (Cedar, OPA/Rego, Biscuit): deferred or rejected. Enforceability must be decidable per backend, there is no AOT-clean .NET engine, and a native engine conflicts with [AD-0003](../decisions/AD-0003-architecture-and-runtimes.md) §6. Reopen with team policy (the team-administration row).
- **The permission matrix or `allowed_command_patterns` as the access model:** rejected. They are origin-keyed guardrails, and a regular expression over argv is no boundary.
- **Reporting classes, tiers or a single "sandboxed" bit at run time:** rejected.
- **Hardening as a dimension:** rejected; it is a basis attribute. Policy filters that implement a denied grant are not hardening.
- **`ui` and a non-Windows `config` as dimensions:** rejected.
- **Three runtime `api_status` values:** declined; five values with one rule for the three non-documented ones (§3.3).
- **A confinement default from day one:** deferred to G19, G20, the editions check and the lock-out rules.
- **"Reference monitor" as the public framing; "authority" alone on a surface:** rejected. A reference monitor is always invoked and tamper-proof, and for unconfined workloads neither holds.
- **Machine-checked honesty (a banned-phrase check; a chapter-to-roadmap cross-check):** declined for now as a tooling change outside documentation scope; a candidate for the next Design or Plan maintenance change.
- **A Plan register of owner decisions:** not now; the owner decisions table of §17 instead.

**Framings considered for the direction:**

| Framing | Verdict | Reason |
|---|---|---|
| Application sandbox | Rejected | Overclaims. Most Win32 GUI applications cannot run in an AppContainer, and GUI isolation is NONE on X11 and on a shared Windows desktop (D-lnx-projects-28; D-win-primitives-completion-13). It names one mechanism class and omits resources, lifecycle and evidence |
| Managed native execution environment | Rejected as the framing | Implies an environment entity with its own boundary. ArcForges cannot enforce one in the unconfined tier, and only VM-class tiers meet the expectation (§2.4) |
| Local workload control infrastructure | Accurate only with the qualifier "launched or adopted" | "Control" over workloads ArcForges did not launch contradicts the product definition §7 and needs privilege (D-persistence-observation-recovery-2) |
| Control plane | Rejected | Implies reconciliation over host state the node does not own |
| Endpoint security or allow-listing | Rejected for the core | Needs administrator rights or an Apple entitlement (D-win-strong-17; D-macos-12). At most an optional integration (EX-20) |
| Reference monitor | Internal term only | A reference monitor is always invoked and tamper-proof; for unconfined workloads neither holds (T-22) |
| **Local authority for delegated execution, with verified contracts** | **Recommended, as a Design description** ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 1) | "Authority" in the sense of [AD-0004](../decisions/AD-0004-contracts-and-state.md): the only writer of execution state. "Delegated execution" scopes the claim to work that passes through ArcForges. "Verified contracts" names the checkable property: require, realize, read back, refuse. It makes the weakest honest state (unconfined, every access dimension NONE) a valid state of the product |

**Windows:**
- WSL as the sandbox for native apps: rejected by the request.
- W1 as a second backend: not offered.
- Job UI limits on ArcForges jobs, and ContentSandbox wired in unchanged (it would fail closed inside an attempt job): rejected.
- MXC now: EX-17, because of an undocumented Tier 1 API and a native Rust unit with possible sidecars.
- Direct PSEC or the `Experimental_` API as a guarantee: rejected.
- Repackaging, PSF, ArcForges-held trusted keys, Developer Mode, `.appinstaller` auto-update: rejected.
- Kernel ETW, minifilters, WFP callouts and filters, bind links: rejected. ProjFS: deferred.
- AppLocker or managed installer as a guarantee: rejected.
- ArcForges-created accounts with held passwords: rejected.
- Windows containers, MDAG, Windows 365 for Agents, bundled Sandboxie: rejected.
- Hyper-V/HCS as a backend: reference only. OS agent accounts: tracked only.
- A loopback exemption to keep caches warm: rejected.
- Any per-attempt firewall rule: rejected.
- A token-only read-back presented as file-policy read-back: rejected.
- Per-attempt ACEs on the user's trees by default, and ACEs on credential files: rejected unless LAB-WIN-18 and G20 show the cost acceptable; credential files never.
- `wsl.exe` inside CONFINED profiles while interop is reachable: rejected.

**Linux:**
- systemd unit sandboxing as a workload mechanism or a separately reported fallback: rejected; it serves only the optional hardening of ArcForges' own units (F-L04).
- BPF unit options in user units; seccomp user notification as enforcement: rejected.
- Embedding bwrap or libseccomp; a C namespace helper; TSYNC as a dependency: rejected.
- Firejail, Snap or distrobox as substrate or isolation: rejected.
- `--appimage-extract` and FUSE AppImages: rejected.
- Installing SELinux modules: rejected. An AppArmor profile only as an owner-chosen, OS-prompted, journaled step (EX-20; an owner question).
- A version comparison for the bwrap fix: rejected; exact fixed revisions.
- A fixed 8 MiB `exec-init` gate, and the bwrap-init fallback before RM-14: rejected.
- A fully hidden cgroupfs as the default: replaced by a read-only view of the attempt's own cgroup.
- A tmpfs at `/tmp` charged to `MemoryMax`: rejected; the view binds `tmp/<attempt>/`.
- Calling the Landlock-only tier on Ubuntu 24.04 a boundary: rejected.

**macOS:**
- Endpoint Security, Network Extension, kexts, the jetsam SPI, VM hosting, re-signing, `TCC.db` edits, stripping quarantine: rejected.
- Full Disk Access or App Management for the node: rejected.
- Allow-default Seatbelt profiles: rejected.
- `RLIMIT_AS` and `RLIMIT_NPROC` as defaults: rejected.
- Seatbelt as accepted roadmap work: moved to EX-22.
- "TCC non-aggregation" as a default property: rejected.
- App-Sandboxed roles of the one signed binary: impossible; a second signed executable would be needed.

**Cross-platform:**
- A package manager, registry proxy, apt/rpm frontend or application launcher: rejected.
- Forcibly disabling vendor updaters: rejected.
- Machine-wide persistence control, and a machine-wide inventory on by default: rejected.
- Live process or VM migration: rejected (EX-04 is re-placement).
- Privileged snapshots (VSS, LVM, ZFS, APFS): rejected.
- Online provenance lookups: rejected, for privacy.
- WASM in the node process: rejected.
- DNS-SD for local workloads: rejected.
- A shared read-write cache across trust classes: rejected.
- Proxy-only network control without OS-forced egress, sold as enforcement: rejected.
- Learning modes that allow access, or disable security: rejected.
- Parsing hostile input in the node where no helper-role profile can be realized: rejected; the method is UNAVAILABLE.
- Remote widening and install decisions signed only by the cloud's key; `allow_lifecycle_approvals` in the contract: deferred to EX-23.
- Stripping MOTW or quarantine: rejected.
- Silent fallback anywhere: rejected.

## 17. Owner decisions required

None of these is pre-decided in this chapter; where the text adopts a position, it is the existing accepted position or a labelled proposal. Each decision was asked on the date shown. When the owner answers, the answer is recorded here verbatim, and a decision that changes a principle or a roadmap row is recorded by amendment of [AD-0017](../decisions/AD-0017-delegated-execution-direction.md) or by a Plan change.

| # | Decision | Recommendation (labelled as such) | When | Asked | Owner's answer (verbatim) |
|---|---|---|---|---|---|
| 1 | **RM confirmations:** which new rows should become accepted future work? **And the changes to accepted rows**, listed because the roadmap's §4 records accepted-row changes with a product decision: first, **RM-12's new alternative trigger** ("or the consented configuration rewrite of EX-13 stage a is delivered and serves as a launch hook"); then RM-12's Purpose and Why deferred; RM-02's and RM-04's conditional cache-trust sentences; RM-05's and RM-13's Why deferred; and the References gains of RM-02, RM-04, RM-05 and RM-13 (§14.8). RM-15 needs no question: request §3 decides it | Recommended: EX-07 stage a, EX-08, EX-13 stage a, EX-15 stage 1, each feasible at P0 on delivered or specified patterns. A gated row confirmed as RM carries its reject condition in "Revisit when". **EX-16 stage a is a priority but not an RM recommendation:** its trigger is observed demand, owners running several agent sessions on one repository, which the owner can judge after release 1; the owner may confirm it anyway. The accepted-row changes are recommended as drafted | With the study's final report | 2026-10-19 | |
| 2 | **Lab timing:** (a) run the decisive spikes (LAB-WIN-01, LAB-WIN-05, LAB-WIN-18, the Windows class-1 subset of LAB-X-01, LAB-LNX-19) as research as soon as D1 and D5 exist, independent of release-1 acceptance; or (b) accept the late-learning risk (§13.1) | (a), because the release-1 tasks from AF-RES-01 onward still shape the job code the Windows labs copy | Before any lab | 2026-10-19 | |
| 3 | **Lab operator, channel, budget and stop rule:** who operates the lab VMs, and through which channel, given no SSH, no leaving the agent's process job and no security-setting change by agents? Accept or change the budget and stop rules (§13.3) | The owner (or a named person) operates; agents read result files the owner provides; the lab register's single budget and stop-rule proposal | With D1 and D5 | 2026-10-19 | |
| 4 | **AD-0011 alignment:** keep boundary 2 aligned with the accepted [AD-0011](../decisions/AD-0011-identity-and-login.md) §6 (an optional privileged step only through an explicit OS prompt, journaled, with exact removal), or adopt the stricter rule (ArcForges never performs it) by an amendment that names AR-16 and A-L02. And: should the Ubuntu AppArmor profile for bwrap be offered as such a prompted step? | Alignment, and the AppArmor profile only after LAB-LNX-01 leg (d) | Before EX-11 or EX-20 is promoted | 2026-10-19 | |
| 5 | **The completion-time ceiling X** for any CONFINED default ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), principle 9) | X = 10 % median completion-time increase on the adapters' reference workloads | Before any CONFINED default | 2026-10-19 | |
| 6 | **macOS TCC disclaim default:** disclaim by default (a private SPI, UNDOCUMENTED, never satisfying REQUIRED) or no disclaim, with the aggregation disclosed | None; the trade-off is a private SPI against disclosed aggregation | At RM-15's promotion; it gates the macOS LAN stage | 2026-10-19 | |
| 7 | **Remote widening approvals:** should remote widening and install decisions exist at all? If so, only with end-to-end signatures (EX-23). Should a LAN-only approval path from the phone be free under [AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2? | Local-only until EX-23 | Before EX-23 | 2026-10-19 | |
| 8 | **D1:** a second x64 host, or Hyper-V on the workstation (check L-01 and Administrator protection first) | A second host | Before any confinement lab | 2026-10-19 | |
| 9 | **D2:** a guest image of the 26300 servicing series or an Insider guest image | — | Before the PSEC and SBOX legs | 2026-10-19 | |
| 10 | **D3:** test accounts and licences for the client labs | — | Before LAB-X-03 | 2026-10-19 | |
| 11 | **D4:** an Apple-silicon lab Mac and the Apple Developer Program | — | Before RM-15 | 2026-10-19 | |
| 12 | **D5:** prototype code inside disposable VMs | — | Before LAB-LNX-19 | 2026-10-19 | |
| 13 | **A fixed `bubblewrap` revision on the Linux delivery venue** (an install by the owner where the venue's package is not on the fixed-revision list) | — | Before Linux delivery | 2026-10-19 | |
| 14 | **Two costs of a Windows-first choice** (conditions 5 and 6 of §13.2): (a) the uncached-build cost, asked only if LAB-WIN-09 leg (a) shows that loopback inside one AppContainer is blocked; (b) if LAB-WIN-04's launcher cells or WSL leg do not deny, whether to accept a Windows backend that holds against {A1, A2} only on hosts where they are reachable | None for (b): it is the owner's trade-off between going Windows first and the Linux-first fallback | After the stage-2 runs of LAB-WIN-04 and LAB-WIN-09, before EX-10 is promoted first | 2026-10-19 | |
| 15 | **The default profile per origin** after the corpus (for example AGENT CONFINED) | — | After G19, G20 and the editions check | 2026-10-19 | |
| 16 | **Default cache read grants** (TP-8): `shared` only, or `user` too | `shared` only; `user` by explicit, recorded grant | At EX-09's promotion | 2026-10-19 | |
| 17 | **Holds:** the product definition §7 amendment (§15.2) | — | Before EX-15's holds stage | 2026-10-19 | |
| 18 | **Fedora** as a supported Linux target (the only one with Landlock ABI ≥ 9) | — | An [AD-0002](../decisions/AD-0002-platform-scope.md) amendment, when wanted | 2026-10-19 | |
| 19 | **macOS narrowing** if G25 shows little value | — | After G25 | 2026-10-19 | |
| 20 | **Workstation facts:** should any fact about the owner's own workstation or its WSL distributions (hardware figures, hypervisor, Hyper-V or Windows Sandbox state, installed package revisions) be recorded in the public Design or Plan repositories? | No: they are restated host-neutrally or kept out of the repositories, as the research record's publication rule says | Before the pair-2 Design PR | 2026-10-19 | |
| 21 | **Apple silicon only for the macOS node:** AD-0002 defines no macOS floor, so "Apple silicon only" is a study proposal, not an existing floor | Apple silicon only, because owner decision D4's lab hardware and Apple `container` are Apple-silicon-only; Intel Macs would need their own lab venue | Before RM-15 is promoted | 2026-10-19 | |
| 22 | **AD-0017's study-derived principles:** "AD-0017's study-derived principles are recorded as accepted design rules; object to any you do not want." Each principle's basis and effective clause are in [AD-0017](../decisions/AD-0017-delegated-execution-direction.md) | Record them as drafted | Before the pair-2 Design PR | 2026-10-19 | |

## 18. The request's four categories

Request §10 asks to distinguish confirmed architectural decisions, proposed directions, research spikes and speculative possibilities. The mapping:

| Request §10 category | What belongs to it | Where it is recorded |
|---|---|---|
| **Confirmed architectural decisions** | AD-0017's principles, each with its basis and effective clause; the pair-1 corrections of today's Design; RM-15 (request §3) | [AD-0017](../decisions/AD-0017-delegated-execution-direction.md); the corrections of 2026-10-19 in the chapters they concern; the roadmap's §2 (RM-15) and EX-05 (`accepted as RM-15`) |
| **Proposed directions** | EX-07 … EX-16 and the parts of EX-17 … EX-23 that are not E5, EX-20 included (its mechanisms are E2 and its integration E4), with this chapter's proposed model (§2–§12); any row the owner later confirms as RM. Recommended for RM: EX-07 stage a, EX-08, EX-13 stage a, EX-15 stage 1 | The roadmap's §3 theme subsections; this chapter, §14 |
| **Research spikes** | The LAB entries of the lab register; the minimum lab set (15 entries, needing D1 and D5); the owner's choice between early spikes and accepting late learning | The [research record](../research/2026-10-18-delegated-execution/README.md); field 10 of each row in §14 |
| **Speculative possibilities (E5)** | EX-16 stage b (try-then-apply, owned-state snapshots); EX-19 (GUI confinement); EX-23's attested-presence part (until LAB-X-20 has run); EX-01's WASI part; EX-07 stage b's grant proposals from denials; EX-09's AI-client stage (until LAB-X-19 has run) | The rows' stages in §14; §16 for what is declined |
