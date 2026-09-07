<a id="rule-wp-22"></a>

# WP-22 — Identity, Workspace, Device and Session

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `11`, `21` · Downstream: `23`, `42`

> **Goal.** Build the account layer: realms, users and authentication identities separated; workspaces from day one; devices, installations, instances and sessions distinguished; device trust and remote gating; step-up; recovery; and the account lifecycle through to deletion — with no product ever requiring an account to work locally.

---

## 1. Scope and purpose

**In scope.** The identity domain and its cloud implementation: realm, user, authentication identity, **single-owner** workspace, device, installation, instance, session, device trust, API tokens, actor kinds, account states, recovery, and deletion. Authentication methods, step-up, and the session contention behaviour that must be real early (`I2 §V`).

**Out of scope.** The account portal UI (`48`). Entitlement (`42`). **Organisations, membership, invitations, roles, seats and shared editing are excluded outright by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** — not deferred, and with no dormant schema hook ([WO-01](../../architecture/data-model/01-cloud-data-model.md#rule-wo-01)–[WO-05](../../architecture/data-model/01-cloud-data-model.md#rule-wo-05)). Historical note: the earlier baseline placed team capability beyond the first launch.

**Why this package exists.** Everything cloud-side attaches to identity, and `I2 §V` marks identity, refresh and session contention as things that must be real early. Getting the separation of user from authentication identity wrong is close to unrecoverable once accounts exist.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/02-identity-account-and-workspace.md`](../../requirements/02-identity-account-and-workspace.md) | The complete identity model, step-up list, account states, deletion and portal scope |
| [`../../architecture/08-security-architecture.md`](../../architecture/08-security-architecture.md) | Identity layering, authentication, delegation and trust evaluation |
| **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** | The canonical account origin and per-origin boundary policy |
| [WP-11](11-security-foundation.md#rule-wp-11), [WP-21](21-cloud-host-and-persistence.md#rule-wp-21) output | The local security foundation and the cloud substrate |

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

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Changing an authentication identity never affects user identity, workspace ownership or attached data, and no membership, role, invitation or seat concept exists.
2. Concurrent refresh never storms; revocation is immediate; multiple passkeys work per user.
3. Device, installation, instance and session are distinguishable everywhere; device revocation cascades correctly; device identity is not a hardware fingerprint.
4. Remote access is off by default; a valid session alone never grants it.
5. Every enumerated sensitive operation demands step-up; the window expires; app unlock never substitutes.
6. Token scope is enforced; tokens cannot perform step-up operations; revocation is immediate.
7. Recovery resists the modelled abuse cases; every account state has defined capability; deletion never touches local data.
8. **No product requires an account to work locally, and no sign-out variant or account deletion removes local data.**

---

## 9. Dependencies

**Upstream — all must be complete.**

- [11 — Security Foundation](11-security-foundation.md)
- [21 — Cloud Host, Modules, Persistence and Migrations](21-cloud-host-and-persistence.md)

**Downstream — these consume this package’s completed output.**

- [23 — Public API Surface and Generated Clients](23-public-api-and-generated-clients.md)
- [42 — Commerce, Entitlement and Credits](42-commerce-entitlement-and-credits.md)
