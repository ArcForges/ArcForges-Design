# Deprecated Input Independence Review

> Status: **Completed focused dependency review**
> Date: 2026-09-07
> Baseline: `bb69010d27cf4ddb47b0877926f746020fc487ca`
> Scope: Current formal specifications and their implementation inputs; not a new extraction from the archived discovery material

The original inputs have completed their role. Current implementation must obtain its required behavior, mechanism and acceptance from the formal design, effective decisions and declared reference-source evidence. The [archive](../deprecated-inputs/README.md) remains historical provenance and supplies no missing normative answer.

## 1. Review method

1. Inventory source shorthands, original and renamed filenames, old input stage/section references, governing-authority lines, required-input tables and traceability tables across all current requirements, architecture, contracts, data models, work packages, decisions and assurance. Classify archive-exclusion notices, completed historical evidence and test/runtime input terminology separately from implementation dependencies.
2. Follow each active dependency to the actual definition it consumes. Retain an already complete rule while removing provenance-only citations; replace a source-only prerequisite with a current definition. Where acceptance was delegated to the archive, specify the scenario and its outcomes in the formal assurance layer.
3. Check indirect consumers through effective decision records and invariant evidence. Preserve original decision quotations and completed extraction history, while routing current work to the current catalogue, definitions, gates and sequence.
4. Compare existing rule entries, identifiers, dependency edges, code examples and archived file blobs with the baseline. Review all non-citation changes against the accepted scope. Run link/anchor/sequence checks and negative fixtures for the input-dependency guard.

The archived input bodies were not reread or re-extracted. Product and reference repositories were not modified or used to infer new scope.

## 2. Resolved dependencies and formal owners

| Dependency found | Resolution and current definition |
|---|---|
| Old sequencing notes presented as governing authority, mock policy and per-step format | [Implementation sequence](../planning/implementation-sequence.md) contains the binding order, mock boundary, replacement ownership and nine required fields. Effective decision notes route consumers there |
| Old input sections required by nine work packages | Probe, IPC, ArcChat, first workflow, property/view, Mobile, Scope, Slate and release packages now consume current definitions or explicitly state their own behavior and acceptance |
| Source-only inline provenance in otherwise complete rules | Existing constraints retained in requirements and architecture; removed the instruction-like shorthand instead of weakening the rule |
| Original input provenance tables used as design traceability | Replaced with explicit relationships among current requirements, mechanisms, data/contracts, assurance and implementation owners |
| First ArcChat–ArcNotes scenario delegated to a discovery-stage section | [Canonical workflow acceptance](end-to-end-workflow-verification.md#first-arcchat-arcnotes-workflow) now defines inputs, success observations and seven failure cases; distinguishes native capability proof from the real Cloud/provider/device workflow |
| Work-package failure acceptance required every case to become terminal | The [Cloud Harness workflow gate](../planning/work-packages/52-cloud-harness.md#rule-wp-52.05) accepts only the defined waiting, refusal or terminal outcome. Waiting for a device or admission is asserted explicitly, without pretending completion |
| Property/view prerequisites pointed to a retired canvas package and an unrelated editor section | [Bounded property/view package](../planning/work-packages/28-arcnotes-properties-and-views.md) consumes active foundations, current scalar requirements, property storage and typed mutation. The storage enum and delivery list include the already-required date-time and URL kinds |
| Installer choice and future-product contract could lead back through decision context | [Installer baseline](../decisions/phase-2-specification-decisions.md#rule-p2-001) names Velopack explicitly; [current portfolio acceptance](../requirements/00-product-scope-and-portfolio.md#24-adding-a-fifth-product) owns any future-product proposal |
| Commercial examples and historical invariant counts looked like ongoing input authority | Current commercial examples retain proposal/approval status; completed extraction statistics remain history. Current work consumes the [429-entry catalogue mapping](invariant-coverage.md), not a repeated raw-input extraction |
| Static-site rationale said only content was needed | The sequence now states the existing shared Node-toolchain prerequisite, consistent with the current Web design and existing dependency graph |
| No check prevented reintroducing an archived input dependency | [Input-independence rule](testing-and-verification-strategy.md#rule-sv-09) and the [runnable checker](design-repair-verification.md#complete-corpus-checker) cover active specification and assurance layers, including their code blocks, with sixteen guard fixtures |

No new product or excluded feature is introduced. The single Cloud Harness, subscription/credit policy, native Avalonia desktop, React/TypeScript Web and current Mobile boundaries remain governed by the accepted requirements and decisions. Existing runtime evidence obligations are retained.

## 3. Historical material that remains

The root and layer READMEs may link to the archive README solely to state its exclusion. The completed Phase 1 reading ledger, original decision quotations, dated verification context, original invariant extraction accounting and previously executed verification commands retain source labels or old paths as history. Current-consumption notes make their boundary explicit. These references are not required implementation inputs, governing mechanisms or instructions to repeat the old review. The checker explicitly lists the six historical assurance records it exempts; their current-consumption boundary was reviewed separately.

Reference-source coverage remains a separate obligation. Deprecating discovery inputs does not deprecate ArcVideo, ArcVideoFoundation, AionUi, AFFiNE, SiYuan, Serial-Studio or distribution reference evidence.

## 4. Verification evidence

The checker is reproducible by extracting the Python block under [Complete corpus checker](design-repair-verification.md#complete-corpus-checker) into a temporary file outside the repository, then running `python <checker.py> <design-worktree>`. It writes `design_check.json` beside that temporary script and exits nonzero on structural errors or unresolved rule citations. Its input-dependency fixtures execute before the document scan.

| Check | Result |
|---|---|
| Active specification references to source shorthands, old input stages or archived filenames | Zero active dependencies; remaining archive notices and explicitly historical records classified separately |
| Current local links and stable anchors | 144 Markdown files; 10,170 local links; 2,614 stable rule anchors; zero broken targets or unresolved rule citations |
| Active work-package graph and catalogue mapping | 51 active packages, 135 dependency edges and all 429 catalogue entries reconciled; no dependency-edge or invariant-ID removal |
| Guard fixtures | 16 passed: 10 forbidden references rejected, six valid current/history controls accepted |
| Existing ID-labelled table rows and code examples | 115 active-layer files compared with the baseline; 6,620 ID-labelled table rows reconciled, including the explicitly amended property-package prerequisite row; no unexplained removal. All existing active-layer code blocks unchanged |
| Four archived bodies | Byte-for-byte and SHA-256 equality with baseline Git blobs; original Phase 1 quotation blocks also unchanged |
| Whitespace | `git diff --check` passed |

## 5. Closure boundary

This review closes dependency on the deprecated input bodies in the current formal implementation chain. It does not certify that every product mechanism has passed the separate design-completeness audit, nor claim implemented behavior, successful builds, deployment, performance or production readiness. Those obligations retain their own methods and evidence gates.
