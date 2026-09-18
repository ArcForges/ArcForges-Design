# Future Cross-Product Collaboration

Status: **FUTURE — not part of current implementation or release acceptance**. P2-012 explicitly defers collaboration between Notes, Scope and Slate. WP20 is reserved, has no active dependency edges, and is not a release prerequisite. Current one-application Android/Web control is separate and remains required.

No current app-to-app RPC, Hub, discovery, peer transfer, multi-product agent capability or mandatory collaboration package is produced. The following examples describe intended future behavior only. They do not assign active proto field numbers, public APIs, databases, producer deadlines or customer commitments. Existing history/resource/product IDs are reused conceptually; a future adopted plan must freeze the detailed contracts before implementation.

| Example | Future user journey | Decisions to close when activated |
|---|---|---|
| Slate summary → Notes | user selects an immutable sequence/range; Slate assistant produces a cited summary; user selects an authorized notebook; explicit Cloud transfer stages a versioned artifact; Notes shows an import preview and commits through its own document command path | recipient selection/acceptance, exact source citation/revision, raw media exclusion, permissions and egress, conflict/duplicate import, transfer expiry, cancellation and independently retained source/recipient copies |
| Scope report → Notes | user selects a capture/range/measurement profile; Scope produces a reproducible report; Cloud stages it for a chosen notebook; Notes previews table/plots/provenance and commits an owned document | units/non-finite/gaps/source hash and synthetic labels, target property mapping, bounded attachments, retention, permission revocation and missing source behavior |

Example-level common sequence: select/freeze source → review destination and data egress → upload verified artifact to Cloud → recipient preview → explicit recipient-authorized import → independent source/export and destination/import receipts. A disconnected recipient sees a pending transfer with expiry; retries reuse a transfer ID/hash; permission loss denies import; destination conflicts never overwrite silently. Each product remains usable without the collaboration service. No universal shared conversation/database is introduced by these examples.

Activation requires a new accepted scope decision, full protocol/state/privacy/failure plan, source/recipient producer packages, a reviewed dependency graph and actual two-product acceptance. Until then, current search and agent execution remain within one application plus explicitly authorized web/upload sources.


## Examples retained from the pre-P2-012 requirements

These examples are inactive, with no current operation, plan edge or acceptance claim:

- “ArcScope → ArcNotes” report copy/import creates a new ArcNotes-owned document with retained ArcScope provenance; two products never share one writable object.
- An ArcSlate rendered output could be referenced from an ArcNotes document, or a report could be materialized there through explicit future Cloud-mediated consent and source/destination contracts.
- A future assistant could federate search across products only after defining server-mediated scope, ownership, retention, conflict and permission rules. Current search never launches a closed product.
- Cross-application Device SSO and independent local peer discovery remain retired. Any future sign-in reuse must have its own accepted security design; current system-browser login reuses only the browser session with consent.

Historical names IHubRegistry/IHubRouting/DeviceSsoBroker and Handoff are reserved here. They are absent from active service registration and release gates. Shared UI conventions, copy/import provenance and Pearson cross-products are unrelated to enabling this future feature.
