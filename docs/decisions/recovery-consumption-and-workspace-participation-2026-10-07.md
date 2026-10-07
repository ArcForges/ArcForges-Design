# P2-050 — Recovery consumption and Workspace participation

Status: proposed paired implementation repair. This successor preserves the complete P2-041 recovery-clock/channel decision and P2-045 recovery-original decision; it does not rewrite their reviewed candidates, task outcomes or dependency edges.

## Actual producer gaps

The existing recovery-code table has only code_hash, set_id, user_id, issued_at, consumed_at and invalidated_at. Its nullable one-use timestamps cannot be safely represented by the generic family equality grammar, which generates nonnullable `=` parameters. A conditional consume record that silently updates zero rows would not prove one-use consumption. Do not add a generic nullable comparison, caller success flag or record-count substitute.

The actual C13-owned WorkspaceSessionFamilyParticipant already reads its own workspace.workspace-load, verifies canonical personal-workspace scope, persisted realm/user/Active1/positive revision and seals the exact scoped workspace-current role. Its closed allowlist does not yet include the final account-security recovery/deletion consumers. Identity cannot manufacture this foreign role or accept a preflight status as its capability.

## Fixed RecoveryCodeOriginal transition discipline

Root CLOUD83 retains sole implementation ownership of the P2-045 fixed identity_recovery_code profile. Clarify its permitted UPDATE: at least one original NULL timestamp must advance to an integer at or after issued_at. consumed_at and invalidated_at remain one-way; already nonnull values never change, including attempts to set the same consumed timestamp without a new legitimate invalidation. Pure timestamp no-op updates refuse. Invalidating an already consumed code is legitimate only when invalidated_at advances from NULL, with consumed_at unchanged. No fields, original identities, delete authority, lifetime profile or general trigger grammar are added.

C17 prepares a consume record over the already guarded exact code_hash/user_id/set_id/issued_at identity. It must not add `WHERE consumed_at IS NULL` or another condition that can turn already-used consumption into a successful zero-row update. The actual SQLite before-update invariant therefore rejects reused consumption, including equal sampled timestamps and concurrent distinct recovery flows. Subsequent successful recovery invalidates the remaining set; a previously consumed row may receive its first invalidation, preserving its original consumption. Own current User/flow/revision, original proof/target, real75 recovery capability, real78 transaction clock and all final participant guards remain mandatory. Physical transition discipline alone grants no recovery authority.

The production family guard establishes existence and immutable identity; the record executes inside that same atomic unit. Failed/foreign/stale guards refuse before effects. Tests must exercise real migrated SQLite with recursive_triggers both disabled and enabled, reused same/different timestamps, prior invalidation, concurrent flows, and late-tail rollback. Preserve actual constraints, strict schema verification, generated metadata and historical outputs.

## Five finite Workspace consumers

C13 alone extends its existing Workspace participant registration to these exact family/plan pairs:

| family | plan |
| --- | --- |
| account-security | families.account-security.request-deletion-native |
| account-security | families.account-security.request-deletion-browser |
| account-security | families.account-security.cancel-deletion-native |
| account-security | families.account-security.cancel-deletion-browser |
| account-security | families.account-security.complete-recovery |

No wildcard, unsuffixed request/cancel alias, recovery-prove or recovery-fail entry is added. Preserve every existing registration. Use the existing server-only target, real owned read and same injected factory issuer. Its exact scoped workspace-current bindings remain personal workspace ID, realm ID, persisted owner User ID, Active1 and captured positive revision. Foreign scope/realm/user, inactive/deleted workspace, changed revision, unknown plan and cross-issuer capability refuse before effects. Current User/lifecycle state remains Identity-owned, including limited purpose5 cancellation; Workspace must not invent an Active User requirement that would prevent that genuine original cancellation.

Anonymous recovery only reaches complete-recovery after C17 verifies the original known User and actual recovery proof. A caller ActorRef, account hint, generated recovery reference or an unbound nullable subject is never its owner identity. Recovery does not lift a suspension, issue a Session or grant ordinary workspace business access. Real scoped Workspace authority joins the complete atomic owner composition, not a separate partial commit.

## Scope, sequencing and evidence

Only CLOUD83 fixed physical transition enforcement, CLOUD13 existing Workspace participant/typed contract and its actual consumer fixtures, and CLOUD17 exact consume preparation/real joined components gain supporting writes/notes. Root83 owns physical generation/migration; C13 owns Workspace source and the shared family union; C17 owns final recovery/deletion orchestration. Coordinate those independent ownership ranges and preserve all accepted histories. There is no CLOUD83-to-CLOUD17 completion edge, new table/module/endpoint or dependency cycle.

Independent exact-head review and applicable ordinary component/CI gates remain required. Component substitution may represent unavailable provider/D1 dependencies but cannot establish deployed one-use behavior, provider purge, whole-account acceptance or OS isolation. Final activation waits genuine method/session/proof, clock, physical and complete participant producers; implementation continues independently while those integrations advance.
