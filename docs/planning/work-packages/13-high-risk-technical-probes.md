<a id="rule-wp-13"></a>

# WP-13 — Four High-Risk Technical Probes

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Upstream: `06`, `07`, `08` · Downstream: `14`, `33`, `36`

> **Goal.** Retire the four technical risks that would be most expensive to discover late — one per product — with reproducible build, test and performance evidence. ArcScope and ArcSlate are built last precisely because their risks are ascertained now.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform and affected products. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Four isolated probes producing evidence: an agent running inside a real Native AOT release binary; a block editor over the local store with undo and crash recovery; high-throughput acquisition with a ring buffer and plot downsampling; and native decoding with audio/video synchronisation displaying a frame.

**Out of scope.** Product features. Probe code is not production code ([ND-05](../implementation-sequence.md#rule-nd-05) in the implementation sequence) — conclusions feed the formal steps, and the code is cleaned up or discarded.

**Why this package exists.** Each probe answers a question whose wrong answer invalidates a later package's design. Answering them in verification projects costs days; answering them in `36` costs the schedule.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [Quality and compatibility requirements](../../requirements/12-quality-and-compatibility-contract.md) | The acceptance constraints for the four probes defined in this package; native, editor and acquisition designs below supply their mechanisms |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§2` | The AOT resolution the agent probe must validate |
| [`../../architecture/12-native-interop-and-media.md`](../../architecture/12-native-interop-and-media.md) | The native boundary and safety obligations the media probe must respect |
| [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md) `§4`, `§18` | Acquisition, overrun and rolling-buffer semantics |
| [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06), [WP-07](07-local-persistence-foundation.md#rule-wp-07), [WP-08](08-local-ipc-and-registration.md#rule-wp-08) output | Proven AOT publish, the local store, and the real transport |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **A probe runs against a real published AOT binary**, not a debug host ([QI-01](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-01), [QI-02](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-02)). |
| BR-02 | **Probe evidence is reproducible**: a recorded environment, a recorded procedure and a recorded result. |
| BR-03 | **Probe code is not promoted to production without cleanup**. |
| BR-04 | **A probe that fails produces a decision, not a workaround.** A failed probe raises the conflict rather than being papered over (**[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**). |
| BR-05 | **Native probes obey the native safety obligations from the start** — validated input, sanitiser builds, sacrificial-process tests (`§6` of the native architecture). |
| BR-06 | **The acquisition probe uses a real transport**, not an in-memory generator, for at least one configuration. |
| BR-07 | **Every native dependency the probes introduce receives a licence position** before use ([PG-03](../../assurance/open-gates-register.md#rule-pg-03)). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `benchmarks/probes/agent-aot/` | Probe A workspace and evidence |
| `benchmarks/probes/editor-store/` | Probe B workspace and evidence |
| `benchmarks/probes/acquisition/` | Probe C workspace and evidence |
| `benchmarks/probes/media/` | Probe D workspace and evidence |
| `native/` | Any shim the media probe requires, with its licence position recorded |
| `eng/verification/probe-evidence/` | The recorded environments, procedures and results |
| `tests/HardwareLab/` | Created: the device inventory the later hardware families depend on |

**Major types introduced:** probe-local only; nothing promoted.

---

## 5. Required implementation work

<a id="rule-wp-13.00"></a>

### WP-13.00 — Probe A: device tool execution under Native AOT

**What must be fully done.** The **device side** of the Harness runs inside a published Native AOT desktop binary: it pulls a stub `ToolRequest`, re-authorises it locally, resolves a `CapabilityKey` through the **generated allowlist**, decodes structured arguments into a **typed** product request (`§3.1` of the local RPC contract), invokes it, and returns an idempotent result. **The model loop is not probed here — it is the CF Workflow** ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02), **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). What is at risk under AOT is the generated decode and static registration path, not the loop. No reflection, no dynamic assembly, no runtime code generation is involved. Static registration and out-of-process extensibility are both exercised.

**Testing requirements.** An AOT publish log with zero diagnostics; an end-to-end `ToolRequest` → decode → typed invocation → result run inside the published binary; a negative test confirming a reflection-based registration or decode path fails to compile or is absent; a containment test confirming the structured value type appears only in the boundary dispatch assembly ([DP-02](../../architecture/contracts/02-local-rpc-operations.md#rule-dp-02)).

**Completion gate.** A device tool request is decoded and executed through generated, typed, statically registered code inside a published AOT binary, with no reflection path present.

<a id="rule-wp-13.01"></a>

### WP-13.01 — Probe B: block editor, store, undo and recovery

**What must be fully done.** A minimal block editor over the local store: create, edit and reorder blocks; undo and redo across a composite operation; and recovery from a hard process kill mid-edit, returning to the last committed boundary with uncommitted work reported rather than silently lost. Undo, revision, checkpoint and journal are exercised as four distinct mechanisms.

**Testing requirements.** A kill-during-edit recovery run; an undo-across-composite-operation test; a test asserting undo history is not crash recovery ([QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)).

**Completion gate.** Recovery returns to a committed boundary with explicit loss reporting, and undo and recovery are demonstrably different mechanisms.

<a id="rule-wp-13.02"></a>

### WP-13.02 — Probe C: high-throughput acquisition

**What must be fully done.** Sustained acquisition from a real transport at a rate above the intended product target, through a ring buffer, with plot downsampling that keeps the display responsive. Overrun is surfaced with a count and a timestamp, never hidden. Pausing the view does not stop recording. A disconnect leaves an explicit gap.

**Testing requirements.** A sustained-throughput run with recorded rate, memory and drop counts; an induced overrun; an induced disconnect; a pause-view-while-recording test.

**Completion gate.** Sustained throughput above target with bounded memory, and every overrun, gap and disconnect explicitly reported.

<a id="rule-wp-13.03"></a>

### WP-13.03 — Probe D: native decode and synchronisation

**What must be fully done.** Native decode through a thin C ABI shim, displaying one frame in the desktop shell, with audio and video synchronised against a shared timeline clock. Handle lifetime uses safe handles; input is validated in managed code; the probe runs under a sanitiser build and in a sacrificial process for its integration tests. Hardware acceleration is discovered at runtime with a software fallback proven.

**Testing requirements.** A frame-display run; an audio/video synchronisation measurement; a sanitiser run; a sacrificial-process crash test; a forced-software-path run.

**Completion gate.** A frame displays with synchronised audio, the sanitiser run is clean, and the software fallback works when acceleration is disabled.

<a id="rule-wp-13.04"></a>

### WP-13.04 — Evidence, licence positions and conclusions

**What must be fully done.** Each probe produces a written conclusion: what was proven, what was not, what constraint it imposes on the owning product package, and what remains open. Every native dependency introduced receives a licence position. The hardware-lab device inventory is created with device, firmware and driver versions.

**Testing requirements.** A completeness check that each probe has a recorded environment, procedure, result and conclusion.

**Completion gate.** Four conclusions exist, every native dependency has a licence position, and the hardware inventory exists. **This satisfies [PG-08](../../assurance/open-gates-register.md#rule-pg-08)** and partially satisfies [PG-03](../../assurance/open-gates-register.md#rule-pg-03).

---

<a id="rule-wp-13.90"></a>
### WP-13.90 — Verify the owned artifact and real integration

**What must be fully done.** Retain the four accepted probes: AOT device execution, Notes editor/recovery, acquisition throughput and media decode/synchronization. Consume real package candidates and generated contracts; use current reference boundaries.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Probe results are tied to package/RID/native graph identities and existing independent behavioral oracles; no full new reference audit or reference execution is added.

**Completion gate.** Probe results are tied to package/RID/native graph identities and existing independent behavioral oracles; no full new reference audit or reference execution is added. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Probe B validates the store's recovery behaviour under real editing load |
| Protocol | Probe A validates capability invocation under AOT |
| UI | Probes B and D validate that the shell can host an editor and a video surface |
| Security | Probe D exercises the native safety obligations before any product depends on them |
| Platform | Probes C and D establish the hardware-lab requirement |
| Migration | None |
| Compatibility | Probe conclusions constrain the design of `33` and `36` |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| AOT publish log and an in-binary **device tool request** decoded and executed through generated, statically registered code — **no model loop is probed here**, it is the CF Workflow | [WP-13.00](#rule-wp-13.00) |
| Kill-during-edit recovery and undo distinction results | [WP-13.01](#rule-wp-13.01) |
| Sustained-throughput record with overrun, gap and pause results | [WP-13.02](#rule-wp-13.02) |
| Frame display, synchronisation measurement, sanitiser and sacrificial-process results | [WP-13.03](#rule-wp-13.03) |
| Four written conclusions, licence positions, hardware inventory | [WP-13.04](#rule-wp-13.04) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-13.90](#rule-wp-13.90) and all inherited domain-specific gates must pass on the same candidate closure. Probe results are tied to package/RID/native graph identities and existing independent behavioral oracles; no full new reference audit or reference execution is added.

**[PG-03](../../assurance/open-gates-register.md#rule-pg-03) evidence:** [WP-13](#rule-wp-13) — Licence/provenance approval for each native dependency admitted by the probes. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. A device tool request is decoded and executed through generated, typed, statically registered code inside a published Native AOT binary, with no reflection path present. **The model loop is not probed here** — it is the CF Workflow ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02), **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**).
2. A kill during editing recovers to a committed boundary with explicit loss reporting, and undo is demonstrably not crash recovery.
3. Sustained acquisition above the product target runs with bounded memory, and every overrun, gap and disconnect is explicitly reported.
4. A decoded frame displays with synchronised audio; the sanitiser run is clean; the software fallback works with acceleration disabled.
5. Each probe has a written conclusion stating what it proved, what it did not, and what constraint it imposes downstream.
6. Every native dependency introduced has a recorded licence position, and the hardware-lab inventory exists — satisfying [PG-08](../../assurance/open-gates-register.md#rule-pg-08).

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)
- [WP-07](07-local-persistence-foundation.md#rule-wp-07)
- [WP-08](08-local-ipc-and-registration.md#rule-wp-08)

**Downstream — consumers of these released outputs.**

- [WP-14](14-hub-and-minimal-provider-slice.md#rule-wp-14)
- [WP-33](33-arcscope-acquisition-and-session.md#rule-wp-33)
- [WP-36](36-arcslate-project-and-timeline.md#rule-wp-36)


---
