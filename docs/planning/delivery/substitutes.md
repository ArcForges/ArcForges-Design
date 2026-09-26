# Substitutes and Real Replacement

> Generated from [the delivery graph](delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](README.md).

A substitute implements an authoritative contract so that a consumer can start before its real producer exists. Its checks prove only what is stated here. The replacing task removes runtime registration of the substitute and records the real evidence; retained regression fixtures stay test-only.

A **value** substitute supplies contract-shaped data (vectors, documents, recorded responses) that only the consumer's own logic interprets; a **behavior** substitute emulates a producer's decisions or effects. Neither kind closes a service, authorization, transaction, hardware, provider, AI or commercial gate ([DLV-18](README.md#rule-dlv-18)).

| Substitute | Class | Stands in for | Real producer | Replaced by | Used by |
|---|---|---|---|---|---|
| [SUB-assistant-history-fixture](#sub-assistant-history-fixture) | value | [WP-25](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) real Cloud Notes/Chat snapshot and export job | [CLOUD.45](lanes/cloud.md#task-cloud-45) | [AST.21](lanes/assistant.md#task-ast-21) | [AST.07](lanes/assistant.md#task-ast-07) |
| [SUB-automation-fixture](#sub-automation-fixture) | behavior | the durable Cloud trigger scheduler and occurrence execution engine | [HAR.06](lanes/harness.md#task-har-06) | [HAR.06](lanes/harness.md#task-har-06) | [AST.14](lanes/assistant.md#task-ast-14), [HAR.06](lanes/harness.md#task-har-06), [AND.10](lanes/android.md#task-and-10) |
| [SUB-commercial-figure-proposal](#sub-commercial-figure-proposal) | value | final approved production commercial figures (storage/window/grace/retention amounts) | [REL.08](lanes/release.md#task-rel-08) | [REL.08](lanes/release.md#task-rel-08) | [COM.02](lanes/commerce.md#task-com-02) |
| [SUB-desktop-candidate-feed](#sub-desktop-candidate-feed) | value | the production update feed publication pointer (the real WP50.02 cutover) | [UPD.07](lanes/updater.md#task-upd-07) | [REL.10](lanes/release.md#task-rel-10) | [REL.01](lanes/release.md#task-rel-01), [REL.02](lanes/release.md#task-rel-02), [REL.03](lanes/release.md#task-rel-03) |
| [SUB-device-runtime-loopback](#sub-device-runtime-loopback) | behavior | [WP-26](../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) real Cloud-connected durable target queue and application presence | [DEV.01](lanes/device-bridge.md#task-dev-01), [DEV.02](lanes/device-bridge.md#task-dev-02) | [DEV.14](lanes/device-bridge.md#task-dev-14) | [AST.11](lanes/assistant.md#task-ast-11) |
| [SUB-embedding-rerank-fixture](#sub-embedding-rerank-fixture) | value | [WP-43.00](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00) real Workers AI embed/rerank calls | [AIR.00](lanes/ai-routing.md#task-air-00) | [SRCH.06](lanes/search.md#task-srch-06) | [SRCH.01](lanes/search.md#task-srch-01), [SRCH.02](lanes/search.md#task-srch-02) |
| [SUB-fcm-recorded-responses](#sub-fcm-recorded-responses) | value | live Firebase Cloud Messaging sender responses | [OPS.10](lanes/operations.md#task-ops-10) | [AND.26](lanes/android.md#task-and-26) | [OPS.10](lanes/operations.md#task-ops-10) |
| [SUB-fixture-turn-endpoint](#sub-fixture-turn-endpoint) | behavior | the Cloud Harness real turn/task loop (model, planner, admission, metering) | [HAR.00](lanes/harness.md#task-har-00), [HAR.02](lanes/harness.md#task-har-02), [HAR.03](lanes/harness.md#task-har-03) | [HAR.05](lanes/harness.md#task-har-05) | [AST.11](lanes/assistant.md#task-ast-11), [AND.09](lanes/android.md#task-and-09), [WEB.20](lanes/web.md#task-web-20) |
| [SUB-guarded-batch-capacity-fixtures](#sub-guarded-batch-capacity-fixtures) | behavior | real per-module business plans not yet built when capacity is first measured | [CLOUD.47](lanes/cloud.md#task-cloud-47), [COM.15](lanes/commerce.md#task-com-15) | [REL.06](lanes/release.md#task-rel-06) | [CLOUD.07](lanes/cloud.md#task-cloud-07) |
| [SUB-history-admission-fixture](#sub-history-admission-fixture) | behavior | [WP-25.09](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.09) real Cloud application-history restartable import receiver | [CLOUD.46](lanes/cloud.md#task-cloud-46) | [AST.22](lanes/assistant.md#task-ast-22) | [AST.15](lanes/assistant.md#task-ast-15) |
| [SUB-hosted-checkout-sandbox](#sub-hosted-checkout-sandbox) | behavior | real Paddle hosted checkout page and redirect | [COM.14](lanes/commerce.md#task-com-14) | [REL.08](lanes/release.md#task-rel-08) | [COM.03](lanes/commerce.md#task-com-03) |
| [SUB-hostile-test-parser](#sub-hostile-test-parser) | behavior | [WP-13.13](../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) production native parser composition (PDF/image/media/OTIO) | [NAT.14](lanes/native.md#task-nat-14) | [PLT.54](lanes/platform.md#task-plt-54) | [PLT.45](lanes/platform.md#task-plt-45), [NAT.14](lanes/native.md#task-nat-14) |
| [SUB-lkg-compiled-defaults-seed](#sub-lkg-compiled-defaults-seed) | value | a real prior published bundle to fall back to | [POL.08](lanes/policy.md#task-pol-08) | [POL.11](lanes/policy.md#task-pol-11) | [POL.09](lanes/policy.md#task-pol-09) |
| [SUB-media-probe-fixture](#sub-media-probe-fixture) | value | [WP-13.06](../work-packages/13-high-risk-technical-probes.md#rule-wp-13.06) real arc_media_probe output | [NAT.07](lanes/native.md#task-nat-07) | [SLATE.15](lanes/arcslate.md#task-slate-15) | [SLATE.04](lanes/arcslate.md#task-slate-04) |
| [SUB-no-op-media-adapter](#sub-no-op-media-adapter) | behavior | real codec integration (existing named scaffolding, implementation-sequence.md §3.1) | [NAT.07](lanes/native.md#task-nat-07), [NAT.08](lanes/native.md#task-nat-08) | [SLATE.23](lanes/arcslate.md#task-slate-23) | [SLATE.15](lanes/arcslate.md#task-slate-15) |
| [SUB-notes-cloud-export](#sub-notes-cloud-export) | behavior | [WP-25.00](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00)..25.08 real Cloud Notes export authority | [CLOUD.45](lanes/cloud.md#task-cloud-45) | [NOTES.33](lanes/arcnotes.md#task-notes-33) | [NOTES.20](lanes/arcnotes.md#task-notes-20) |
| [SUB-notes-pdf-fixture-parser](#sub-notes-pdf-fixture-parser) | behavior | [WP-13](../work-packages/13-high-risk-technical-probes.md#rule-wp-13)'s production ArcForges.Native.Pdf/PDFium wrapper (does not exist yet, not even as a declared placeholder project) | [NAT.14](lanes/native.md#task-nat-14) | [NOTES.37](lanes/arcnotes.md#task-notes-37) | [NOTES.09](lanes/arcnotes.md#task-notes-09) |
| [SUB-postmark-ses-test-recordings](#sub-postmark-ses-test-recordings) | value | live Postmark primary / SES secondary email delivery | [CLOUD.12](lanes/cloud.md#task-cloud-12) | [CLOUD.12](lanes/cloud.md#task-cloud-12) | [CLOUD.12](lanes/cloud.md#task-cloud-12) |
| [SUB-provider-adapter-fixture](#sub-provider-adapter-fixture) | behavior | real Paddle/Payoneer API calls behind the adapter | [COM.14](lanes/commerce.md#task-com-14) | [COM.14](lanes/commerce.md#task-com-14) | [COM.01](lanes/commerce.md#task-com-01) |
| [SUB-provider-event-fixtures](#sub-provider-event-fixtures) | value | live Paddle/Payoneer webhook traffic | [COM.14](lanes/commerce.md#task-com-14) | [COM.14](lanes/commerce.md#task-com-14) | [COM.04](lanes/commerce.md#task-com-04) |
| [SUB-provider-response-fixture](#sub-provider-response-fixture) | value | [WP-43.00](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00)/43.07 real provider text/tool/image dispatch responses | [AIR.00](lanes/ai-routing.md#task-air-00) | [HAR.05](lanes/harness.md#task-har-05) | [HAR.00](lanes/harness.md#task-har-00) |
| [SUB-resource-transport-schema-fixtures](#sub-resource-transport-schema-fixtures) | value | [WP-25.05](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.05)'s real R2 multipart upload/verify/commit and full Resource/Entitlement/sync owner tables | [CLOUD.42](lanes/cloud.md#task-cloud-42) | [CLOUD.42](lanes/cloud.md#task-cloud-42) | [CLOUD.25](lanes/cloud.md#task-cloud-25) |
| [SUB-same-app-fixture-tool](#sub-same-app-fixture-tool) | behavior | [WP-17](../work-packages/17-arcchat-independent-core.md#rule-wp-17) real device-side tool executor | [AST.11](lanes/assistant.md#task-ast-11) | [HAR.05](lanes/harness.md#task-har-05) | [HAR.00](lanes/harness.md#task-har-00) |
| [SUB-scope-instruments-fixture](#sub-scope-instruments-fixture) | behavior | [WP-13.12](../work-packages/13-high-risk-technical-probes.md#rule-wp-13.12) real hardware-backed ArcInstruments build | [NAT.13](lanes/native.md#task-nat-13), [NAT.24](lanes/native.md#task-nat-24) | [SCOPE.11](lanes/arcscope.md#task-scope-11) | [SCOPE.04](lanes/arcscope.md#task-scope-04) |
| [SUB-scope-sync-fixture](#sub-scope-sync-fixture) | value | [WP-25.00](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00) real deployed Cloud sync engine | [CLOUD.39](lanes/cloud.md#task-cloud-39) | [SCOPE.27](lanes/arcscope.md#task-scope-27) | [SCOPE.22](lanes/arcscope.md#task-scope-22) |
| [SUB-signed-format-fixture-keys](#sub-signed-format-fixture-keys) | value | [WP-53](../work-packages/53-desktop-distribution-and-update.md#rule-wp-53)'s production signing keys | [UPD.07](lanes/updater.md#task-upd-07) | [REL.11](lanes/release.md#task-rel-11) | [CON.16](lanes/contracts.md#task-con-16), [PRF.07](lanes/runtime-proofs.md#task-prf-07), [EXT.04](lanes/extensions.md#task-ext-04) |
| [SUB-slate-asr-fixture](#sub-slate-asr-fixture) | value | real Cloud Workers AI whisper-large-v3-turbo transcription output | [AIR.09](lanes/ai-routing.md#task-air-09) | [HAR.91](lanes/harness.md#task-har-91) | [SLATE.30](lanes/arcslate.md#task-slate-30) |
| [SUB-stubbed-provider-path](#sub-stubbed-provider-path) | behavior | [WP-43](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43) real provider routing and metering (already-named [WP-17.05](../work-packages/17-arcchat-independent-core.md#rule-wp-17.05) scaffolding) | [AIR.00](lanes/ai-routing.md#task-air-00) | [AIR.08](lanes/ai-routing.md#task-air-08) | [AST.15](lanes/assistant.md#task-ast-15), [AIR.08](lanes/ai-routing.md#task-air-08) |
| [SUB-test-signed-update-feed](#sub-test-signed-update-feed) | value | the production feed and real product signing key custody | [UPD.07](lanes/updater.md#task-upd-07) | [REL.10](lanes/release.md#task-rel-10) | [UPD.01](lanes/updater.md#task-upd-01) |
| [SUB-updater-policy-fixture](#sub-updater-policy-fixture) | value | [WP-44](../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) real activated policy distribution and [WP-45](../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) real security-advisory process | [POL.09](lanes/policy.md#task-pol-09) | [UPD.08](lanes/updater.md#task-upd-08) | [UPD.05](lanes/updater.md#task-upd-05) |
| [SUB-web-msw-fixtures](#sub-web-msw-fixtures) | value | real API/session conformance | [CLOUD.19](lanes/cloud.md#task-cloud-19), [CLOUD.21](lanes/cloud.md#task-cloud-21) | [WEB.30](lanes/web.md#task-web-30) | [PRF.08](lanes/runtime-proofs.md#task-prf-08) |
| [SUB-web-search-fixture](#sub-web-search-fixture) | value | [WP-43.05](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.05) real Brave web-search dispatch | [AIR.06](lanes/ai-routing.md#task-air-06) | [SRCH.06](lanes/search.md#task-srch-06) | [SRCH.00](lanes/search.md#task-srch-00) |

### SUB-assistant-history-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-25](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) real Cloud Notes/Chat snapshot and export job |
| Authoritative contract | assistant-history.v1 archive format (Contracts) |
| What its checks prove | local offline export/import round-trip, malformed/hash/foreign-reference handling, branch-cycle and cancel-import handling only -- no Cloud upload |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.45](lanes/cloud.md#task-cloud-45) |
| Removes runtime substitution | [AST.21](lanes/assistant.md#task-ast-21) |
| Real evidence still required | real Cloud Notes/Chat export producer accepts and round-trips the same archive against a deployed environment |

### SUB-automation-fixture

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | the durable Cloud trigger scheduler and occurrence execution engine |
| Authoritative contract | Cloud-owned rule/occurrence records (wire registry) |
| What its checks prove | client rendering of schedule/timezone/target/budget and action availability, offline-draft handling only |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [HAR.06](lanes/harness.md#task-har-06) |
| Removes runtime substitution | [HAR.06](lanes/harness.md#task-har-06) |
| Real evidence still required | a live scheduled occurrence executes and cascades with storm protection, observed from this client |
| Origin | Named scaffolding introduced by [WP-17.04](../work-packages/17-arcchat-independent-core.md#rule-wp-17.04); HAR.06 completes only after the desktop and Android consumers switch (AST.20, AND.24). |

### SUB-commercial-figure-proposal

| Field | Value |
|---|---|
| Class | value |
| Stands in for | final approved production commercial figures (storage/window/grace/retention amounts) |
| Authoritative contract | PolicyVersion/PriceVersion row shape |
| What its checks prove | Proposed figures exercise the configured paths only; approval under [D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020) and commercial activation are release evidence. |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [REL.08](lanes/release.md#task-rel-08) |
| Removes runtime substitution | [REL.08](lanes/release.md#task-rel-08) |
| Real evidence still required | approved commercial-figure-status sign-off per docs/assurance/commercial-figure-status.md; none of the 7 proposal figures is a production default yet |

### SUB-desktop-candidate-feed

| Field | Value |
|---|---|
| Class | value |
| Stands in for | the production update feed publication pointer (the real WP50.02 cutover) |
| Authoritative contract | the same feed schema/hash/compatibility-range format WP53 defines for the real feed |
| What its checks prove | the update matrix (fresh install/upgrade/rollback/etc.) works against a correctly-shaped feed |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [UPD.07](lanes/updater.md#task-upd-07) |
| Removes runtime substitution | [REL.10](lanes/release.md#task-rel-10) |
| Real evidence still required | the same update-matrix results re-observed once REL.10 points the production feed/signing keys at the proven candidate; per [BR-01](../../architecture/14-build-packaging-and-release.md#rule-br-01) (build once, promote the same artifact) this does not require a fresh test run against new bits, only confirmation that the production pointer now serves the exact already-proven candidate |

### SUB-device-runtime-loopback

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-26](../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) real Cloud-connected durable target queue and application presence |
| Authoritative contract | Device.Runtime pull/claim/result typed interface (contracts/03 ToolRequest shape) |
| What its checks prove | in-process typed dispatch/decode/local-reauthorization mechanics only, no real cross-device delivery |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [DEV.01](lanes/device-bridge.md#task-dev-01), [DEV.02](lanes/device-bridge.md#task-dev-02) |
| Removes runtime substitution | [DEV.14](lanes/device-bridge.md#task-dev-14) |
| Real evidence still required | [RV-05](../../architecture/contracts/03-realtime-and-bridge.md#rule-rv-05) 'no cloud-initiated connection to device' structural test plus a live queued tool request surviving a restart |

### SUB-embedding-rerank-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-43.00](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00) real Workers AI embed/rerank calls |
| Authoritative contract | Contracts published fixture embedding/rerank vectors (deterministic decimal vectors) |
| What its checks prove | index-write correctness (namespace scoping, filters, tombstones, dimension-change isolation) independent of real model variance |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [AIR.00](lanes/ai-routing.md#task-air-00) |
| Removes runtime substitution | [SRCH.06](lanes/search.md#task-srch-06) |
| Real evidence still required | real compatible client/owner/index versions confirmed against the deployed Vectorize/D1 in SRCH.06/90 |

### SUB-fcm-recorded-responses

| Field | Value |
|---|---|
| Class | value |
| Stands in for | live Firebase Cloud Messaging sender responses |
| Authoritative contract | FCM HTTP v1 send responses recorded for the push sender adapter |
| What its checks prove | Sender error, retry and token-invalidation handling only; live sending is proven by the same task and physical receipt by the Android integration task. |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [OPS.10](lanes/operations.md#task-ops-10) |
| Removes runtime substitution | [AND.26](lanes/android.md#task-and-26) |
| Real evidence still required | Live FCM sending with a project-bound credential and physical Android receipt, fallback and permission evidence ([PG-24](../../assurance/open-gates-register.md#rule-pg-24)). |
| Origin | Named scaffolding: recorded FCM sender responses introduced by [WP-45.09](../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.09). |

### SUB-fixture-turn-endpoint

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | the Cloud Harness real turn/task loop (model, planner, admission, metering) |
| Authoritative contract | IChatOperations.StartAgentTurnAsync / TaskRef + streaming output contracts (wire registry) |
| What its checks prove | client-side session/event/output/upload handling, typed state transitions, reconnection -- runs no model/planner/admission/metering itself |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [HAR.00](lanes/harness.md#task-har-00), [HAR.02](lanes/harness.md#task-har-02), [HAR.03](lanes/harness.md#task-har-03) |
| Removes runtime substitution | [HAR.05](lanes/harness.md#task-har-05) |
| Real evidence still required | [HV-09](../../architecture/17-agent-harness.md#rule-hv-09) structural test 'no client runs a model loop' plus a live turn against the deployed Harness |
| Origin | Named scaffolding introduced by [WP-17.01](../work-packages/17-arcchat-independent-core.md#rule-wp-17.01); consumers switch in AST.19, AND.24 and WEB.27; [WP-52.05](../work-packages/52-cloud-harness.md#rule-wp-52.05) deletes it structurally. |

### SUB-guarded-batch-capacity-fixtures

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | real per-module business plans not yet built when capacity is first measured |
| Authoritative contract | model-04 D1 execution profile generic plan envelope shape |
| What its checks prove | capacity/latency/contention envelope under synthetic load only, never business correctness |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.47](lanes/cloud.md#task-cloud-47), [COM.15](lanes/commerce.md#task-com-15) |
| Removes runtime substitution | [REL.06](lanes/release.md#task-rel-06) |
| Real evidence still required | [WP-50](../work-packages/50-full-platform-production-release.md#rule-wp-50) load evidence with real modules |

### SUB-history-admission-fixture

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-25.09](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.09) real Cloud application-history restartable import receiver |
| Authoritative contract | history.beginImport/finalizeImport/getImport/cancelImport operations (contracts/10) |
| What its checks prove | local mode selection/disclosure/promotion UI and denied-admission/credit-consent gating only, no real upload |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.46](lanes/cloud.md#task-cloud-46) |
| Removes runtime substitution | [AST.22](lanes/assistant.md#task-ast-22) |
| Real evidence still required | a real promoted history survives a restartable import against deployed Cloud, including lost-finalize-ack and account-switch cases |

### SUB-hosted-checkout-sandbox

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | real Paddle hosted checkout page and redirect |
| Authoritative contract | adapter checkout port (COM.01) |
| What its checks prove | internal metadata completeness and redirect-forgery rejection against a scripted/sandbox redirect |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [COM.14](lanes/commerce.md#task-com-14) |
| Removes runtime substitution | [REL.08](lanes/release.md#task-rel-08) |
| Real evidence still required | Paddle sandbox checkout session evidence |

### SUB-hostile-test-parser

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-13.13](../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) production native parser composition (PDF/image/media/OTIO) |
| Authoritative contract | ArcForges.Contracts.LocalRpc.Sandbox ContentSandboxService |
| What its checks prove | OS-level containment mechanics only (AppContainer/Job Object, Landlock/seccomp, App-Sandbox/XPC denial, resource bounds, crash/hang/parent-death cleanup) against a deliberately hostile FIRST-PARTY test parser, not real format-parsing correctness |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [NAT.14](lanes/native.md#task-nat-14) |
| Removes runtime substitution | [PLT.54](lanes/platform.md#task-plt-54) |
| Real evidence still required | packaged RID containment matrix re-run against the real parser libraries plus product-level malformed-input/crash tests in [WP-18.04](../work-packages/18-arcnotes-document-core.md#rule-wp-18.04)/[WP-37.01](../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.01) |
| Origin | Named scaffolding introduced by [WP-11.09](../work-packages/11-security-foundation.md#rule-wp-11.09); [WP-13.13](../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) replaces production fixture registration; the malicious regression fixture stays test-only. |

### SUB-lkg-compiled-defaults-seed

| Field | Value |
|---|---|
| Class | value |
| Stands in for | a real prior published bundle to fall back to |
| Authoritative contract | LastKnownGood/compiled-defaults shape (this task's own output) |
| What its checks prove | the fallback chain mechanics in isolation before any bundle has ever been published in a live environment |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [POL.08](lanes/policy.md#task-pol-08) |
| Removes runtime substitution | [POL.11](lanes/policy.md#task-pol-11) |
| Real evidence still required | a genuinely stale client falling back through a real prior bundle, observed against the deployed Cloud policy service |

### SUB-media-probe-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-13.06](../work-packages/13-high-risk-technical-probes.md#rule-wp-13.06) real arc_media_probe output |
| Authoritative contract | native.metadata.v1 closed JSON projection (contracts/06-native-functional-abi.md §3: {version,streams:[...],warnings:[...]}) |
| What its checks prove | domain/library/editing/timeline logic against synthetic but schema-conformant metadata only; never hostile-input containment or real decode fidelity |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [NAT.07](lanes/native.md#task-nat-07) |
| Removes runtime substitution | [SLATE.15](lanes/arcslate.md#task-slate-15) |
| Real evidence still required | Real file probe against packaged ArcForges.Native.Media on every admitted RID, including malformed/oversized/fuzzed input and a forced child-crash recovery run |

### SUB-no-op-media-adapter

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | real codec integration (existing named scaffolding, implementation-sequence.md §3.1) |
| Authoritative contract | n/a - unit-test-local no-op |
| What its checks prove | wiring/composition only, never decode/codec correctness |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [NAT.07](lanes/native.md#task-nat-07), [NAT.08](lanes/native.md#task-nat-08) |
| Removes runtime substitution | [SLATE.23](lanes/arcslate.md#task-slate-23) |
| Real evidence still required | SLATE.16's decode results and SLATE.31's golden-corpus results |

### SUB-notes-cloud-export

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-25.00](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00)..25.08 real Cloud Notes export authority |
| Authoritative contract | ArtifactRef/export-manifest shape in ArcForges.Contracts.PublicApi |
| What its checks prove | client-side export request construction, fidelity-report rendering, attachment-hash verification, offline-refusal behaviour against a scripted endpoint |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.45](lanes/cloud.md#task-cloud-45) |
| Removes runtime substitution | [NOTES.33](lanes/arcnotes.md#task-notes-33) |
| Real evidence still required | real host/database/object-store export across concurrent edits, notebook moves, deleted attachments, quota, expiry, restart, cancellation, paid-term end, per [WP-25.08](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) testing requirements |

### SUB-notes-pdf-fixture-parser

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-13](../work-packages/13-high-risk-technical-probes.md#rule-wp-13)'s production ArcForges.Native.Pdf/PDFium wrapper (does not exist yet, not even as a declared placeholder project) |
| Authoritative contract | [WP-11.09](../work-packages/11-security-foundation.md#rule-wp-11.09)'s restricted fixture-parser ContentSandbox ABI |
| What its checks prove | viewer UI, page-anchor model, preview-degradation logic and sandbox call plumbing only - not real PDFium behaviour |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [NAT.14](lanes/native.md#task-nat-14) |
| Removes runtime substitution | [NOTES.37](lanes/arcnotes.md#task-notes-37) |
| Real evidence still required | real packaged PDFium build, licence inventory and hostile-input containment evidence per [PG-12](../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../assurance/open-gates-register.md#rule-pg-22) |

### SUB-postmark-ses-test-recordings

| Field | Value |
|---|---|
| Class | value |
| Stands in for | live Postmark primary / SES secondary email delivery |
| Authoritative contract | notification.delivery / delivery_attempt / provider_event / suppression schema (data-model/01) |
| What its checks prove | Deterministic refusal, unknown-outcome and callback regression cases only; runtime registration is forbidden and live delivery is proven by the same task. |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.12](lanes/cloud.md#task-cloud-12) |
| Removes runtime substitution | [CLOUD.12](lanes/cloud.md#task-cloud-12) |
| Real evidence still required | live send to a controlled recipient inbox through the real Postmark account plus a prepared SES secondary before this task's completion gate closes |

### SUB-provider-adapter-fixture

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | real Paddle/Payoneer API calls behind the adapter |
| Authoritative contract | the adapter's own typed capability/port interface (this task's output) |
| What its checks prove | containment (no provider type leaks) and capability-driven branching in isolation |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [COM.14](lanes/commerce.md#task-com-14) |
| Removes runtime substitution | [COM.14](lanes/commerce.md#task-com-14) |
| Real evidence still required | Paddle/Payoneer sandbox environment calls recorded at [WP-42.10](../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10); production evidence only at WP50/[L-30](../../assurance/release-gates.md#rule-l-30) |

### SUB-provider-event-fixtures

| Field | Value |
|---|---|
| Class | value |
| Stands in for | live Paddle/Payoneer webhook traffic |
| Authoritative contract | adapter's typed ProviderEvent shape (COM.01) |
| What its checks prove | Recorded provider events drive inbox, idempotency and reconciliation tests; recorded cases remain regression inputs after live ingestion replaces runtime registration. |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [COM.14](lanes/commerce.md#task-com-14) |
| Removes runtime substitution | [COM.14](lanes/commerce.md#task-com-14) |
| Real evidence still required | sandbox webhook delivery and reconciliation logs; production evidence only at WP50 |

### SUB-provider-response-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-43.00](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00)/43.07 real provider text/tool/image dispatch responses |
| Authoritative contract | Contracts published normalized fixture response shapes (from AIR.08) |
| What its checks prove | turn-loop/dispatch-intent/budget/conflict-set state-machine correctness under scripted responses |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [AIR.00](lanes/ai-routing.md#task-air-00) |
| Removes runtime substitution | [HAR.05](lanes/harness.md#task-har-05) |
| Real evidence still required | the two HAR.05 end-to-end oracles running against the real deployed provider |

### SUB-resource-transport-schema-fixtures

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-25.05](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.05)'s real R2 multipart upload/verify/commit and full Resource/Entitlement/sync owner tables |
| Authoritative contract | generated upload/status/ticket/verification/owner-promotion schema in ArcForges.Contracts.PublicApi |
| What its checks prove | protocol/schema/permission/error envelope only, via declared fixtures -- release excludes the fixture handlers |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.42](lanes/cloud.md#task-cloud-42) |
| Removes runtime substitution | [CLOUD.42](lanes/cloud.md#task-cloud-42) |
| Real evidence still required | interrupted-upload resumption, verification-failure, orphan-cleanup, accounting-vs-committed-storage against real R2 (CLOUD.42/CLOUD.47) |

### SUB-same-app-fixture-tool

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-17](../work-packages/17-arcchat-independent-core.md#rule-wp-17) real device-side tool executor |
| Authoritative contract | a minimal same-application tool contract (per producer-artifacts-and-integration.md's 'complete same-app tools' [WP-52](../work-packages/52-cloud-harness.md#rule-wp-52) standing substitute) |
| What its checks prove | tool-batching, conflict-set enforcement and parallel-limit mechanics |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [AST.11](lanes/assistant.md#task-ast-11) |
| Removes runtime substitution | [HAR.05](lanes/harness.md#task-har-05) |
| Real evidence still required | the two HAR.05 oracles exercising the real device tool path in an AOT release binary |

### SUB-scope-instruments-fixture

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-13.12](../work-packages/13-high-risk-technical-probes.md#rule-wp-13.12) real hardware-backed ArcInstruments build |
| Authoritative contract | arc_instruments_* ABI shape (contracts/06-native-functional-abi.md) |
| What its checks prove | adapter enumerate/open/transfer/cancel/error-path logic against a simulated-hardware build only |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [NAT.13](lanes/native.md#task-nat-13), [NAT.24](lanes/native.md#task-nat-24) |
| Removes runtime substitution | [SCOPE.11](lanes/arcscope.md#task-scope-11) |
| Real evidence still required | per-RID real device connect/transfer/disconnect run against the maintained lab inventory |

### SUB-scope-sync-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-25.00](../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00) real deployed Cloud sync engine |
| Authoritative contract | Contracts SyncService records |
| What its checks prove | client-side scope-mapping/exclusion logic only |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.39](lanes/cloud.md#task-cloud-39) |
| Removes runtime substitution | [SCOPE.27](lanes/arcscope.md#task-scope-27) |
| Real evidence still required | multi-device convergence against deployed Cloud with zero raw-capture bytes transferred |

### SUB-signed-format-fixture-keys

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-53](../work-packages/53-desktop-distribution-and-update.md#rule-wp-53)'s production signing keys |
| Authoritative contract | this task's Ed25519 fixture trust root |
| What its checks prove | signature/hash verification mechanics, expired/revoked/unknown-key refusal, malformed/rollback/mixed-shard handling |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [UPD.07](lanes/updater.md#task-upd-07) |
| Removes runtime substitution | [REL.11](lanes/release.md#task-rel-11) |
| Real evidence still required | production-signed manifest verified against the real distribution trust root, checked at release |
| Origin | Fixture trust roots from [WP-03.07](../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.07) and the [WP-02](../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02)/[WP-06](../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) test identities; production keys come from [WP-53](../work-packages/53-desktop-distribution-and-update.md#rule-wp-53) and replace fixture roots in release configuration at REL.10; the family release audit asserts no fixture root remains in any release configuration. |

### SUB-slate-asr-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | real Cloud Workers AI whisper-large-v3-turbo transcription output |
| Authoritative contract | slate.transcribe.v1 TranscriptRecord/segment schema (23-simulator-and-interchange.md §5) |
| What its checks prove | chunking, extraction-artifact hashing, adoption preview/undo/content-origin logic only -- never real ASR accuracy, real budget/metering or real provider failure modes |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [AIR.09](lanes/ai-routing.md#task-air-09) |
| Removes runtime substitution | [HAR.91](lanes/harness.md#task-har-91) |
| Real evidence still required | A real paid transcription dispatch reconciled through [WP-42](../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42)/43's real metering path, end to end through [WP-52](../work-packages/52-cloud-harness.md#rule-wp-52)'s Harness |

### SUB-stubbed-provider-path

| Field | Value |
|---|---|
| Class | behavior |
| Stands in for | [WP-43](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43) real provider routing and metering (already-named [WP-17.05](../work-packages/17-arcchat-independent-core.md#rule-wp-17.05) scaffolding) |
| Authoritative contract | [WP-17.05](../work-packages/17-arcchat-independent-core.md#rule-wp-17.05) stubbed managed provider path |
| What its checks prove | early client/UI development against a scripted AI response only |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [AIR.00](lanes/ai-routing.md#task-air-00) |
| Removes runtime substitution | [AIR.08](lanes/ai-routing.md#task-air-08) |
| Real evidence still required | a controlled real-provider run plus [PG-13](../../assurance/open-gates-register.md#rule-pg-13)'s exact worked-fixture evidence |
| Origin | Named scaffolding introduced by [WP-17.05](../work-packages/17-arcchat-independent-core.md#rule-wp-17.05) in the assistant admission path; replaced by [WP-43.00](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00) and [WP-43.07](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07). |

### SUB-test-signed-update-feed

| Field | Value |
|---|---|
| Class | value |
| Stands in for | the production feed and real product signing key custody |
| Authoritative contract | update.feed.v1 signed envelope schema (architecture 14 SS8.1) |
| What its checks prove | feed parsing, trust-chain verification, product/RID/channel/version selection and anti-replay mechanics only |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [UPD.07](lanes/updater.md#task-upd-07) |
| Removes runtime substitution | [REL.10](lanes/release.md#task-rel-10) |
| Real evidence still required | [WP-50](../work-packages/50-full-platform-production-release.md#rule-wp-50)'s full release matrix against production-signed feeds |

### SUB-updater-policy-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-44](../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) real activated policy distribution and [WP-45](../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) real security-advisory process |
| Authoritative contract | the policy.rollout_assignment shape (data-model/03-derived-stores.md SS5) and the update.feed.v1 blockedVersions/rolloutBasisPoints fields already fixed by architecture 14 SS8.1 |
| What its checks prove | deterministic per-installation rollout assignment stability and channel-switch mechanics against a locally authored fixture policy document |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [POL.09](lanes/policy.md#task-pol-09) |
| Removes runtime substitution | [UPD.08](lanes/updater.md#task-upd-08) |
| Real evidence still required | expedited security-update rehearsal against a real [WP-45](../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) advisory and a real [WP-44](../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) policy push |

### SUB-web-msw-fixtures

| Field | Value |
|---|---|
| Class | value |
| Stands in for | real API/session conformance |
| Authoritative contract | generated TS client types |
| What its checks prove | Generated-contract request and response shapes in the browser only; MSW handlers stay test-only and are excluded from release bundles. |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [CLOUD.19](lanes/cloud.md#task-cloud-19), [CLOUD.21](lanes/cloud.md#task-cloud-21) |
| Removes runtime substitution | [WEB.30](lanes/web.md#task-web-30) |
| Real evidence still required | [WP-23](../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) real API/session conformance; MSW handlers remain test-only forever, never a release-gate substitute |

### SUB-web-search-fixture

| Field | Value |
|---|---|
| Class | value |
| Stands in for | [WP-43.05](../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.05) real Brave web-search dispatch |
| Authoritative contract | Contracts fixture web-search response shape |
| What its checks prove | source admission's origin/consent/rejection logic for web sources without a funded external call |
| What it does not prove | Any real runtime, provider, device, integration or commercial behavior. |
| Real producer | [AIR.06](lanes/ai-routing.md#task-air-06) |
| Removes runtime substitution | [SRCH.06](lanes/search.md#task-srch-06) |
| Real evidence still required | a real authorized web source admitted and indexed through the funded Brave dispatch with consent/egress recorded |
