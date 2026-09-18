# Independent Review Remediation Verification

Date: 2026-09-17. Design baseline: `8b60426a09e89b9006815206928419a60cec83b6`. Independent review input: local Plan commits `c873199` and `9771885`; execution plan: Plan `572dcba`, with the bounded corrections recorded below. This record belongs to the resulting Design revision, not to an implementation release.

The executing reviewer read the findings, consolidated decisions and closure criteria before changing formal Design. Repairs were applied in one isolated worktree, followed by checks against the same 37 findings and eight global conditions. Verification failures were corrected in their affected owners; they did not start another scope expansion. Deprecated input bodies and dated historical reviews were not rewritten.

## Evidence and limits

Evidence is E0–E2: document inspection, read-only committed-source inspection, structural checks and execution of the documented SQLite examples. No product repository was changed. No NuGet/npm/Maven package, native binary, AOT host, Cloudflare deployment, Android device, supplier account or real payment was exercised by this repair. A passing document fixture is not a passing production integration test.

The [open-gates register](open-gates-register.md) retains **35 current implementation obligations**, including the new self-host and capacity evidence. Capacity, playback and simulator numbers are proposed acceptance targets under D-020; neither a Product Owner signature nor a measured performance result is implied. There is no remaining user decision required to apply these document repairs.

The current local-process boundary is explicit: desktop products never discover, launch or call each other. Assistant windows, SQLite, ordinary Platform services and P/Invoke wrappers run in their own host process. Only separately specified hostile-parser containment and admitted extension/connector children have private parent-bound channels. Standard external MCP stdio remains an adapter exception. This does not add a generic local service or claim that Hello World implements these helpers.

## Bounded corrections to the reviewed plan

| Issue | Applied disposition |
|---|---|
| Commercial defaults | IRQ-1 A: no free official Cloud service tier. IRQ-2 A: the operator funds web-search provider requests; customer model processing remains metered. Existing local use, paid terms, credits, compensation and self-host grants remain intact. |
| Email verification | Postmark callbacks use its documented TLS/credential/IP verification, not a nonexistent signed-webhook feature. SES uses verified SNS envelopes. Missing provider search evidence is not proof of non-delivery and never authorizes blind failover. |
| CI authentication | Cloudflare deployment uses its documented scoped API-token path with protected custody/rotation. Provider-supported federation remains usable elsewhere; application scope is not workload identity. |
| Early producers | WP22 supplies real identity mail and the minimal browser ceremony before WP45 operations/WP48 account UI. WP03 defines signed formats and WP02/06 test trust before WP32/41 consumers. WP53 supplies production distribution trust before WP50. |
| History and streams | Typed role-preserving transcript windows, bounded transient objects and compaction hashes replace flattened history. Public progress preserves owner state, attempt state, cursor, output/final references and no-answer recovery in generated records. |
| D1 and alarms | Fixed guarded batches, stable-key bootstrap plus replay and durable publication fences replace PostgreSQL assumptions. DO pacing includes delayed/duplicate alarms, bounded provider retries and Cron rescue. SQLite tests establish example semantics only. |
| Scope and counts | The manifest distinguishes active operations from reserved future names. Negative rules, old quotations, technical identifiers and SQLite WAL are not false-positive current dependencies. |

Fresh primary-source checks informing these corrections are linked at their normative owners and in the Plan execution record: [Postmark webhooks](https://postmarkapp.com/developer/webhooks/webhooks-overview), [SES events](https://docs.aws.amazon.com/ses/latest/dg/event-publishing-send-email.html), [Cloudflare CI authentication](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/), [D1 limits](https://developers.cloudflare.com/d1/platform/limits/), [DO alarms](https://developers.cloudflare.com/durable-objects/api/alarms/), [Container outbound controls](https://developers.cloudflare.com/containers/guides/outbound-traffic/) and [native authorization RFC 8252](https://www.rfc-editor.org/rfc/rfc8252). These checks establish documented capabilities, not deployed evidence.

## Per-finding closure

“Closed” below means the document defect and its implementation/acceptance instructions are resolved. Fixtures named in a WP remain mandatory future implementation work unless explicitly listed as executed in the mechanical-results section.

| Check | Result and authoritative repair | Verification / remaining runtime producer |
|---|---|---|
| IRC-01 | Closed. Three desktop hosts, independent embedded assistants, history modes and one per-host residence rule replace standalone ArcChat/federation. | Requirements00/09, assistant requirements and experience01 agree; LF-03/SI-20/BL-01 cite BR-01. WP15/17/52 retain the accepted assistant behaviors. |
| IRC-02 | Closed. Current-effective cells and inline supersession identify every changed old decision; P2-013 records all 26 resolutions and nine repositories. | Read [decisions](../decisions/README.md); historical quotations are not active instructions. |
| IRC-03 | Closed. All 65 replacement occurrences are classified; Pearson and the D-018 quotation are restored. | [Occurrence ledger](review-remediation-term-ledger.md), case-insensitive baseline comparison, exact quotation comparison to `e974df5`, independent Pearson vectors. |
| IRC-04 | Closed. Four ProductId keys and application-installation presence have one authority; device live-presence fields are retired/reserved. | Registry04, annex10, model01; 17 hint IDs including application.presenceChanged; WP22/26 test actual presence. |
| IRC-05 | Closed. Public AI output uses gRPC-Web with an explicit former-field mapping, typed progress, unary recovery and streams. | [Harness §7.2](../architecture/17-agent-harness.md#72-client-read-contract), registry exception table and annex10; WP24/52 supply real framing/recovery proof. |
| IRC-06 | Closed. One numbered TaskState/TaskReasonFacet registry separates waiting causes from state and unknown effect. | Registry04 number convention and WP03 facet/unknown-response vectors; model01 and requirements use the same values. |
| IRC-07 | Closed. One ToolRequest authority; result key is toolRequestId + attemptId + commandId for both Task and ChatTurn owners. | Contracts03/04 and model01; WP26 tests lost acknowledgements and Chat-owned results. |
| IRC-08 | Closed. Per-installation browser PKCE, passkey origins and the closed 12-operation PAT allowlist replace cross-app SSO. | Contracts07, security08, model01 and WP22 negative cases; allowlist IDs resolve mechanically. |
| IRC-09 | Closed. Closed ContentSandbox/extension/connector child roles replace discovery and peer leases. | [Process model](../architecture/03-local-ipc-and-process-model.md), annex09 and manifest11; WP06/08/11 must prove the real restricted no-TCP boundary. |
| IRC-10 | Closed. Public gRPC-Web, private child controls and in-process product handlers are distinguished at their original owners. | Architecture02/03/05/08/10 and owner revision rules; no current dependency relies on retired arch03 anchor content. |
| IRC-11 | Closed. Producer manifests/locks own exact toolchain patches; generated proto artifacts have one authoring rule and the Kotlin Maven producer. | Registry04, architecture11/25/27, WP02/03; obsolete contracts-client generation is retired. |
| IRC-12 | Closed. D1 plan registry, guarded publisher/bootstrap algorithms and paired export/replay backup replace PostgreSQL transaction/restore assumptions. | [Model04](../architecture/data-model/04-d1-execution-profile.md), deployment22 and WP21/46; example SQL rollback/receipt vectors executed. Real D1/restore remains open. |
| IRC-13 | Closed. Missing columns and prose-only owned records are integrated at model01 owners, including identity, execution, terms, prices, payment/credit movement and delivery. | 125 extracted UQ/IX column checks pass; no duplicate field declaration; child concurrency remains on the root. This is not a compiled production DDL proof. |
| IRC-14 | Closed. One [model05](../architecture/data-model/05-application-history.md) assistant schema replaces the competing store. | All 16 tables create with foreign_keys enabled; positive inserts and four negative constraints pass. Temporary history cannot be persisted as a local conversation. |
| IRC-15 | Closed. Typed windows/compaction have one protected-set/refusal rule and bounded branch-aware recovery. | Annex10 tags retained/appended; model05 four worked cases; WP52.01/.03 consume those cases. |
| IRC-16 | Closed. Capacity envelope, 16 KiB body placement, metadata retention, growth trigger and L-16/PG-26 are explicit. | Model04, WP21/40/50 and gate register agree. Owner approval and measured capacity remain open. |
| IRC-17 | Closed. One edge route/binding/egress graph governs Worker, Container, AI and supplier calls. | Architecture05 and contracts05; WP21 tests public access to an internal route and denied egress. |
| IRC-18 | Closed. Search namespaces partition owner/workspace/product without conflating prefix filtering with authorization. | Requirements06 PM-05, model04 and WP40 forged-scope vector. Real index behavior remains required. |
| IRC-19 | Closed. Cloudflare deployment, rollback, restore, credentials and runbooks replace old host/provider operations. | Cloud requirements, architecture22, L-02/L-07/L-10 and WP50; source verification does not close deployment gates. |
| IRC-20 | Closed. Real mail adapters, DNS ownership, push/operator/service/origin/observability/status configuration and fixture removal have owners. | Architecture13, annex08, producer matrix and WP22/45; provider accounts and live acceptance remain open. |
| IRC-21 | Closed. selfhost.v1 has a realm descriptor, feature differences, custody and recovery sequence. | Architecture22, contracts07, PG-25 and WP21.08/46/50; a real operator account is still needed. |
| IRC-22 | Closed. Simulator pacing has states, cursor/checkpoint rules, alarm rescue and explicit service targets. | Architecture23, SIM-10 and WP51 alarm/cold-start/pause/resume/24-hour-cost cases. |
| IRC-23 | Closed. Plan changes take effect at the next term; unknown post-dispatch holds follow existing reconciliation/deadlines. | Requirements04 CT-06, lifecycle SU-05/LV-07, billing16 and model01; no immediate/provider-default proration. |
| IRC-24 | Closed. No free official tier; one source/kind/subscription vocabulary and no grant on enrollment. | Requirements03/04, registry04, model01, billing16 and WP42 enrollment fixture. |
| IRC-25 | Closed. Web-search request cost is operator-funded and model processing remains customer-metered. | Requirements05/06, architecture09/16 and WP43 funding vector; no hidden double debit. |
| IRC-26 | Closed. Workers AI has no hidden provider/model fallback or required AI Gateway path. | Harness recovery, selected routes, L-06 and WP43 separate synthetic normalization from actual supplier proof. |
| IRC-27 | Closed. Product export fidelity and assistant-history.v1 apply consistently by history mode. | Requirements13, product requirements, model05 and WP15/19 round-trip/closure criteria. |
| IRC-28 | Closed. PackageCatalog is the twenty-first business module with nine operations, signed index/revocation formats and custody. | Registry04/manifest11/model01, architecture05/15 and WP03/41/45/53; revocation/offline tests have producers. |
| IRC-29 | Closed. C# extension authoring convenience generates parameter schemas only; proto owns service envelopes. MCP placement is explicit. | Architecture15 and annex08; WP41.07 covers admitted local/Cloud placements without a second Harness. |
| IRC-30 | Closed. Android identity is com.arcforges.mobile; one module map and F-1 stable toolchain reconciliation replace the old preserve premise. | Architecture11/27, WP30.00 and producer pins; no new iOS target. |
| IRC-31 | Closed. Android store/direct channels have signed metadata, notify-only behavior and tamper rejection. | Architecture11/14, registry04 signed formats and WP32; GitHub Releases remain archive/mirror. |
| IRC-32 | Closed. Product Domain/Application/Infrastructure/Desktop/AssistantIntegration matches architecture27; no product LocalRpc project remains. | Architecture19 original layer table and capability maps; only Platform/Contracts child transport names remain. |
| IRC-33 | Closed. Web outputs are site, account, chat and operations. | Architecture10/25/27 and WP45; status is independently hosted, not an extra application profile. |
| IRC-34 | Closed. Playback/helper memory targets, undo semantics, math profile, selected PDFium and own-app previews agree. | Requirements12, product rules, architecture18/24/26 and WP18/37. Actual performance/parser containment remains open. |
| IRC-35 | Closed. WPs consume current artifacts and stages, and the real payout gate belongs to WP50 L-30. | Header/forward/reverse/topological comparison; original WP42 completion gate repaired, not merely overridden by an appendix. |
| IRC-36 | Closed. Own-application Notes/Slate acceptance scenarios replace the federated scenario; current trace and invariant rows use actual owners. | [End-to-end verification](end-to-end-workflow-verification.md), 429 exact invariant statements and [traceability](traceability-matrix.md); NC-10 re-dated. |
| IRC-37 | Closed. Broken table fragments, columns, links, reverse edges and prose number joins are repaired. | Link/anchor/table check, graph transpose check and bounded prose inspection; identifiers, technical terms, versions and literal schema tags are preserved. |

## Global verification results

The reproducible standard-library Python checks and JSON outputs are retained in the local Plan repository under `remediation/verification/`. They read this worktree without editing it. Git history containing `8b60426` and `e974df5` is required for baseline checks.

| Check | Result |
|---|---|
| IRC-G1 Decisions | P2-013, IRQ dispositions, 26 IRDs, supersession and preserved scope checked against the current body. |
| IRC-G2 Links/tables | Relative Markdown files/anchors resolve; no duplicate explicit anchor, inconsistent table width or orphan table fragment. Code-fenced fixture text and deprecated input bodies are excluded. |
| IRC-G3 Plan graph | 51 active WPs, 158 dependency edges; headers, forward table, phase index and reverse transpose agree; serial order has no violation. WP20/27/29 have no active graph edges. Amended .90 steps are mapped to completion. |
| IRC-G4 Operations | 351 manifest entries = 344 active catalogue methods + 7 reserved future Hub names. No missing active method or duplicate ID. All 13 annex10 additions and nine catalog operations are included. Authorization is the eight-field effective profile, including patEligible, not the former incomplete seven-field description. |
| IRC-G5 Vocabulary | Shared closed ProductId keys, Task state/facet, subscription, grant source/kind and 17 event IDs inspected at the owners. Retained record fields keep their tags; removed DeviceView presence tags/names are reserved; five retired SSO/peer-transfer/presence records have no active registration. |
| IRC-G6 Configuration | Provider/reference inventory below resolves to closed schema owners; production activation still validates secret references and operator choices. |
| IRC-G7 Gates | Current PG/VG/L identifiers resolve. L-16/PG-26 and PG-25 retain owner, trigger, evidence and failure consequence; no implementation gate is marked complete here. |
| IRC-G8 Residues | Contextual scans of active requirements, architecture, experience and planning pass after the affected-body corrections. Allowed matches are explicit negative/retirement statements, future-only examples, dated historical evidence, standard third-party/OS boundaries and SQLite-specific terms. |

| Configuration use | Closed authority and validation |
|---|---|
| Identity/passkeys/OIDC/native callback | configuration.v1 identity/origins; contracts07 ceremony and exact RP/origin/redirect values; official and self-host modes are distinct. |
| Postmark/SES and FCM | email/push sections; verified sender domains, per-environment credentials, callback correlation and exact Android package. |
| Operator login and private service calls | operatorIdentity/serviceKeys/origins; disjoint issuer/roles, bound directions, expiry and limited overlap. |
| Workers AI/Brave and monetary admission | models/search/customerTariffs/supplierPrices/funding/offers/entitlementProfiles; closed model/price references, exact amounts and operator budgets. |
| R2 and independent backup | objects/backup; purpose-bound grants, immutable inventory, independent account and COMPLIANCE retention. |
| Deployment and self-host identity | release configuration plus signed deployment/realm/selfhost.v1 manifests in architecture22/contracts07; registry hash, compatibility date, schema/plan hashes and realm trust checked together. |
| OTLP, analytics, incident routing, status | observability/status; provider admission, redaction/consent, independent status origin and operator-selected references. |
| Android/catalog/update signing | registry04 signed formats and architecture14/15 trust stores; keys are custody references, never customer configuration values or mobile secrets. |

Executed SQLite evidence: 16 assistant tables; clean foreign-key inspection; valid branch/message insertion; rejection of a missing conversation FK, duplicate branch ordinal, temporary durable conversation and invalid attachment. The D1 example was executed in SQLite to verify stale-guard rollback and duplicate-command rollback even after an attempted owner update; one outbox effect remains. This does not establish D1 runtime limits, sessions, batching behavior over the deployed bridge or recovery across Cloudflare services.

Other executed checks: 125 extracted model UQ/IX references name declared columns; 12 PAT IDs resolve; all 65 baseline term occurrences are represented; the D-018 quotation matches its pre-amendment version; Pearson gives 1, -1 and unavailable for the defined three vectors; all 429 invariant statements match the canonical glossary; the existing functional native ABI specification is unchanged.

## Handoff

Implement from [the planning entry](../planning/README.md), [serial order](../planning/implementation-sequence.md) and [producer matrix](../planning/producer-artifacts-and-integration.md). Generated packages and mocks remain distinct from real consumer integration. Every release still needs the complete applicable native/AOT/Cloudflare/browser/Android/provider/restore/commercial evidence. This record closes the reviewed document defects, not those product gates.
