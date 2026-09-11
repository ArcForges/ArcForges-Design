<a id="rule-wp-22"></a>

# WP-22 — Identity, Workspace, Device and Session

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `11`, `21` · Downstream: `23`, `42`

> **Goal.** Build the account layer: realms, users and authentication identities separated; workspaces from day one; devices, installations, instances and sessions distinguished; device trust and remote gating; step-up; recovery; and the account lifecycle through to deletion — with no product ever requiring an account to work locally.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud; client/AI adapters. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The identity domain and its cloud implementation: realm, user, authentication identity, **single-owner** workspace, device, installation, instance, session, device trust, API tokens, actor kinds, account states, recovery, and deletion. Authentication methods, step-up, and the session contention behaviour that must be real early.

**Out of scope.** The account portal UI (`48`). Entitlement (`42`). **Organisations, membership, invitations, roles, seats and shared editing are excluded outright by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — not deferred, and with no dormant schema hook ([WO-01](../../architecture/data-model/01-cloud-data-model.md#rule-wo-01)–[WO-05](../../architecture/data-model/01-cloud-data-model.md#rule-wo-05)). Historical note: the earlier baseline placed team capability beyond the first launch.

**Why this package exists.** Everything cloud-side attaches to identity, and [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) marks identity, refresh and session contention as things that must be real early. Getting the separation of user from authentication identity wrong is close to unrecoverable once accounts exist.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../requirements/02-identity-account-and-workspace.md`](../../requirements/02-identity-account-and-workspace.md) | The complete identity model, step-up list, account states, deletion and portal scope |
| [`../../architecture/08-security-architecture.md`](../../architecture/08-security-architecture.md) | Identity layering, authentication, delegation and trust evaluation |
| **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** | The canonical account origin and per-origin boundary policy |
| [WP-11](11-security-foundation.md#rule-wp-11), [WP-21](21-cloud-host-and-persistence.md#rule-wp-21) output | The local security foundation and the cloud substrate |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **No product requires an account to work locally.** Sign-in is never a launch gate. |
| BR-02 | **Account and user data are not tied together.** Local data survives sign-out and account deletion. |
| BR-03 | **A local user is not a cloud guest account.** The two concepts never merge. |
| BR-04 | **Authentication identity is separate from user.** One user may hold several authentication identities; changing one never changes the user. |
| BR-05 | **Workspace exists from the first day** and is the scope entitlement and data attach to. |
| BR-06 | **Account, workspace and billing are completely separated.** |
| BR-07 | **`Device ≠ Session`** and **`Installation ≠ Device`**. Four distinct concepts: device, installation, instance, session. |
| <a id="rule-br-08"></a>BR-08 | **Device identity is not a hardware fingerprint.** |
| BR-09 | **Sign-out distinguishes four actions** and never silently deletes local data. |
| BR-10 | **Remote access is gated by device trust**, defaulting to off. |
| BR-11 | **Passkey is the primary method**, with email one-time codes for first verification and recovery; the first version requires no password. |
| BR-12 | **Step-up is required for the enumerated sensitive operations**, and an app unlock never substitutes for it ([I-278](../../requirements/01-normative-glossary-and-invariants.md#rule-i-278)). |
| BR-13 | **Recovery is designed from the first version**, not retrofitted. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Identity/` | The identity module: realm, user, authentication identity, single-owner workspace, device, session, trust, tokens, recovery, deletion |
| `src/Cloud/ArcForges.Cloud.Host/` | Authentication and tenancy resolution wired into the fixed pipeline |
| `src/BuildingBlocks/ArcForges.Security/` | Client-side session handling, refresh serialisation, device registration |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.Identity/` | Identity DTOs on the Apache boundary |
| `tests/CloudIntegrationTests/Identity/` | Authentication, contention, trust, recovery and deletion suites |

**Major types introduced.** `Realm`, `User`, `AuthIdentity`, `AuthMethod`, `Workspace`, `ServiceTerm`, `Device`, `DeviceTrustLevel`, `Installation`, `Instance`, `Session`, `RefreshToken`, `ApiToken`, `StepUpChallenge`, `RecoveryFlow`, `AccountState`, `DeletionRequest`.

---

## 5. Required implementation work

<a id="rule-wp-22.00"></a>

### WP-22.00 — Core identity model

**What must be fully done.** Realm, user, authentication identity and **single-owner** workspace with their relationships. Ownership is `workspace.owner_user_id`; **there is no membership table, join, role or seat** ([WO-01](../../architecture/data-model/01-cloud-data-model.md#rule-wo-01)–[WO-05](../../architecture/data-model/01-cloud-data-model.md#rule-wo-05)), and authorization is a direct ownership check ([WO-02](../../architecture/data-model/01-cloud-data-model.md#rule-wo-02)). A user may hold several authentication identities. Adding, removing or changing an authentication identity never changes user identity or workspace membership. Workspace is the scope everything else attaches to.

**Testing requirements.** Identity-change tests asserting user continuity; **a structural test asserting no schema, contract or operation carries a membership, role, invitation, seat or shared-editor concept** ([WO-05](../../architecture/data-model/01-cloud-data-model.md#rule-wo-05)); a structural test asserting no capability treats an authentication identity as a user.

**Completion gate.** Changing an authentication identity never affects user identity, workspace ownership or attached data, and **no membership, role, invitation or seat concept exists anywhere in the schema, contracts or operations**.

<a id="rule-wp-22.01"></a>

### WP-22.01 — Authentication

**What must be fully done.** Passkey registration and authentication with multiple passkeys per user; email one-time codes for first verification and recovery; no password in the first version. Session issue, refresh with rotation, and revocation. Refresh is serialised so concurrent requests never trigger a storm.

**Testing requirements.** Multi-passkey registration and authentication; concurrent-refresh contention under load; revocation taking effect immediately; a rate-limit test on code delivery.

**Completion gate.** Concurrent refresh never storms, revocation is immediate, and multiple passkeys work per user.

<a id="rule-wp-22.02"></a>

### WP-22.02 — Device, installation, instance and session

**What must be fully done.** Four distinct concepts with four lifecycles. Device identity is stable but not a hardware fingerprint. A device lists its installations; an installation may have several instances; sessions belong to a device and installation. Device revocation revokes its sessions and push registrations.

**Testing requirements.** A distinction matrix; device revocation cascading correctly; a test asserting device identity survives ordinary hardware change.

**Completion gate.** The four concepts are distinguishable everywhere, and device revocation cascades to sessions and registrations.

<a id="rule-wp-22.03"></a>

### WP-22.03 — Device trust and remote gating

**What must be fully done.** Trust levels per device with remote access defaulting to off. Raising trust requires an explicit act with step-up. Remote capability availability is derived from trust, not from possession of a session.

**Testing requirements.** A default-off assertion; a trust-elevation test requiring step-up; a test asserting a valid session alone does not grant remote capability.

**Completion gate.** Remote access is off by default and a valid session alone never grants it.

<a id="rule-wp-22.04"></a>

### WP-22.04 — Step-up and sensitive operations

**What must be fully done.** Step-up challenges for the enumerated sensitive operations, with a bounded validity window and no substitution by an app unlock. Step-up state is per session and per operation class, never a global elevated mode.

**Testing requirements.** Coverage that every enumerated operation demands step-up; a window-expiry test; a negative test asserting app unlock does not satisfy step-up.

**Completion gate.** Every enumerated sensitive operation demands step-up, the window expires, and app unlock never substitutes.

<a id="rule-wp-22.05"></a>

### WP-22.05 — API tokens and actor kinds

**What must be fully done.** Scoped API tokens with expiry, revocation and last-use visibility. Actor kinds — human, agent, automation, extension, operator, service — are modelled explicitly and carried in the actor chain. A token never grants more than its scope, and never grants step-up-requiring operations.

**Testing requirements.** Scope-enforcement tests; a negative test asserting a token cannot perform a step-up operation; revocation immediacy.

**Completion gate.** Token scope is enforced, tokens cannot perform step-up operations, and revocation is immediate.

<a id="rule-wp-22.06"></a>

### WP-22.06 — Recovery, account states and deletion

**What must be fully done.** Recovery flows designed from the start, with anti-abuse protections and clear communication. Account states — active, restricted, suspended, pending deletion — with defined capability in each. Deletion with a grace period, an explicit statement of what is and is not deleted, and no effect on local data.

**Testing requirements.** Recovery flow tests including abuse attempts; state-transition capability matrix; deletion tests asserting local data is untouched and the grace period behaves correctly.

**Completion gate.** Recovery resists the modelled abuse cases, every account state has defined capability, and deletion never touches local data.

<a id="rule-wp-22.07"></a>

### WP-22.07 — Local integration

**What must be fully done.** Desktop sign-in with device registration, secure session storage through the broker, and a unified sign-in experience across the four products on one device. Sign-out distinguishes its four actions and never deletes local data.

**Testing requirements.** Cross-product sign-in on one device; sign-out variants; a test asserting local data survives every sign-out variant and account deletion.

**Completion gate.** Sign-in is unified per device, and no sign-out variant nor account deletion removes local data.

---

<a id="rule-wp-22.08"></a>

### WP-22.08 — Browser cookie-session adapter


**What must be fully done.** Implement the same-origin browser adapter in the AOT host using the selected random hashed session/preauth/CSRF records. Preserve the browser/native exclusive schema, exact Origin, idle/absolute expiry, lowest-trust browser installation and one-use auth flow. Map the declared /session bootstrap/auth/logout endpoints to existing application services. Use explicit cookie parsing/writing and X-AF-CSRF validation; no ASP.NET Data Protection/cookie-auth middleware dependency.

**Testing requirements.** Real PostgreSQL one-use challenge, lost login response, idle-versus-revoke race, expiry and replica failover; browser exact Origin/CSRF on unsafe RPC/session/CF-connect/object operations, native-token route refusal and WebSocket first-frame auth.

**Completion gate.** One server-owned session authority, no JS bearer, no cross-origin reuse or session resurrection; actual AOT closure feeds WP23 and full portal acceptance.

**Required implementation and closure from the final review.** Implement and independently verify [08-security-architecture](../../architecture/08-security-architecture.md#account-and-provider-closure). Implement the complete typed account surface: profile/email, recovery-code set, scoped PAT, credential rename, session listing, four sign-out scopes, Device SSO, remote capability policy and restricted deletion-cancel reauthentication. Exercise official email/passkey and self-host password/passkey/OIDC enrollment/recovery, no email-based merging, old refresh reuse/lost response, one-use proofs and secret-free browser session replies. Wire UI consumers through the same owner ports. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-22.90"></a>
### WP-22.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement native/RN bearer sessions, same-origin Web opaque sessions, passkeys/recovery, workspace/device rules and authenticated CF authorization ports using selected AOT-compatible components.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Real publish-mode auth/session/CSRF/origin/rotation/revocation tests, including stale CF requests and browser credential secrecy.

**Completion gate.** Real publish-mode auth/session/CSRF/origin/rotation/revocation tests, including stale CF requests and browser credential secrecy. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The identity schema, the most privacy-sensitive in the system |
| Protocol | Identity DTOs, session and step-up contracts |
| UI | Sign-in, device list, trust, step-up and account state surfaces |
| Security | This package is where authentication and trust become real |
| Platform | Passkey support and secure session storage per platform |
| Migration | Identity schema changes are the highest-risk migrations |
| Compatibility | Session and token contracts enter the supported window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Identity continuity and structural separation results | [WP-22.00](#rule-wp-22.00) |
| Concurrent-refresh contention and revocation results | [WP-22.01](#rule-wp-22.01) |
| Four-concept distinction matrix and revocation cascade | [WP-22.02](#rule-wp-22.02) |
| Default-off and session-insufficiency results | [WP-22.03](#rule-wp-22.03) |
| Step-up coverage, expiry and non-substitution results | [WP-22.04](#rule-wp-22.04) |
| Token scope and revocation results | [WP-22.05](#rule-wp-22.05) |
| Recovery abuse-resistance, state matrix and deletion results | [WP-22.06](#rule-wp-22.06) |
| Cross-product sign-in and local-data-survival results | [WP-22.07](#rule-wp-22.07) |

---

**Browser-session evidence.** [WP-22.08](#rule-wp-22.08) contributes real database/concurrency, origin/CSRF/expiry and multi-replica results. The browser adapter must pass these before [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) consumes its contract; a written [P2-003](../../decisions/phase-2-specification-decisions.md#rule-p2-003) decision alone is insufficient.

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-22.90](#rule-wp-22.90) and all inherited domain-specific gates must pass on the same candidate closure. Real publish-mode auth/session/CSRF/origin/rotation/revocation tests, including stale CF requests and browser credential secrecy.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-22.08](#rule-wp-22.08) — Real cookie-only browser identity/session/CSRF/expiry/revocation conformance. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Identity boundary evidence.** Apply the [owner/deployment identity chain](../../architecture/08-security-architecture.md#1-identity-layering). Automation loses authorization when its owner loses permission/service eligibility even with a valid process credential; no customer service-principal or Organization authority is introduced.

**All of the following, with recorded evidence:**

1. Changing an authentication identity never affects user identity, workspace ownership or attached data, and no customer workspace membership, role, invitation or seat concept exists; separate operator roles and self-host account enrollment retain their specified boundary.
2. Concurrent refresh never storms; revocation is immediate; multiple passkeys work per user.
3. Device, installation, instance and session are distinguishable everywhere; device revocation cascades correctly; device identity is not a hardware fingerprint.
4. Remote access is off by default; a valid session alone never grants it.
5. Every enumerated sensitive operation demands step-up; the window expires; app unlock never substitutes.
6. Token scope is enforced; tokens cannot perform step-up operations; revocation is immediate.
7. Recovery resists the modelled abuse cases; every account state has defined capability; deletion never touches local data.
8. Shell launch and native Scope/Slate work require no account; Notes and Chat content behavior passes the [offline initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix). Signout/deletion preserves native projects and pending recovery material while blocking normal signed-out Cloud content views.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-11](11-security-foundation.md#rule-wp-11)
- [WP-21](21-cloud-host-and-persistence.md#rule-wp-21)

**Downstream — consumers of these released outputs.**

- [WP-23](23-public-api-and-generated-clients.md#rule-wp-23)
- [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42)


---
