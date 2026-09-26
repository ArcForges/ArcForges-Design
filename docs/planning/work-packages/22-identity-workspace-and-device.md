<a id="rule-wp-22"></a>

# WP-22 — Identity, Workspace, Device and Session

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

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

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../requirements/02-identity-account-and-workspace.md`](../../requirements/02-identity-account-and-workspace.md) | The complete identity model, step-up list, account states, deletion and portal scope |
| [`../../architecture/08-security-architecture.md`](../../architecture/08-security-architecture.md) | Identity layering, authentication, delegation and trust evaluation |
| **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** | The canonical account origin and per-origin boundary policy |
| [WP-11](11-security-foundation.md#rule-wp-11), [WP-21](21-cloud-host-and-persistence.md#rule-wp-21) output | The local security foundation and the cloud substrate |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

**Real mail prerequisites (owned by Operations before WP22 completion).** An isolated Postmark account/server and verified sending subdomain, SPF/DKIM/DMARC records, protected CI SecretRefs, controlled recipient inbox and prepared SES secondary identity/configuration must exist. Provider credentials never enter source or fixtures. Recorded provider responses are permitted only in regression tests; the real delivery/recovery gate cannot close on a fake sender. Missing external access keeps the gate open, not the adapter design undecided.

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **No product requires an account to work locally.** Sign-in is never a launch gate. |
| <a id="rule-br-02"></a>BR-02 | **Account and user data are not tied together.** Local data survives sign-out and account deletion. |
| <a id="rule-br-03"></a>BR-03 | **A local user is not a cloud guest account.** The two concepts never merge. |
| <a id="rule-br-04"></a>BR-04 | **Authentication identity is separate from user.** One user may hold several authentication identities; changing one never changes the user. |
| <a id="rule-br-05"></a>BR-05 | **Workspace exists from the first day** and is the scope entitlement and data attach to. |
| <a id="rule-br-06"></a>BR-06 | **Account, workspace and billing are completely separated.** |
| <a id="rule-br-07"></a>BR-07 | **`Device ≠ Session`** and **`Installation ≠ Device`**. Four distinct concepts: device, installation, instance, session. |
| <a id="rule-br-08"></a>BR-08 | **Device identity is not a hardware fingerprint.** |
| <a id="rule-br-09"></a>BR-09 | **Sign-out distinguishes four actions** and never silently deletes local data. |
| <a id="rule-br-10"></a>BR-10 | **Remote access is gated by device trust**, defaulting to off. |
| <a id="rule-br-11"></a>BR-11 | **Passkey is the primary method**, with email one-time codes for first verification and recovery; the official realm uses no password; self-host password/OIDC remains supported. |
| <a id="rule-br-12"></a>BR-12 | **Step-up is required for the enumerated sensitive operations**, and an app unlock never substitutes for it ([I-278](../../requirements/01-normative-glossary-and-invariants.md#rule-i-278)). |
| <a id="rule-br-13"></a>BR-13 | **Recovery is designed from the first version**, not retrofitted. |

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

### WP-22.01 — Native and browser authentication with real mail

**What must be fully done.** Implement contracts 07 native authorize/token PKCE ceremony and minimal browser login UI, passkey/email and configured self-host OIDC/password. Produce Postmark/SES delivery/outcome adapters and provider/DNS setup checklist now; WP45 later adds operational drills. Account full UI in WP48 is not a prerequisite.

**Testing requirements.** Actual email delivery/recovery and prepared secondary; timeout remains unknown; PKCE/state/redirect/code replay, Credential Manager/RP origin fixtures, refresh contention and revocation.

**Completion gate.** Real provider identity flows work on the foundation client; required accounts/DNS are recorded external inputs, never replaced by a stub acceptance.

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

### WP-22.05 — PAT and actor authorization

**What must be fully done.** Implement the exact patEligible/scopes metadata, hash-only token storage, expiry/revocation and one-time display after step-up. Preserve actor chain and deny customer tokens on operator/internal/local boundaries.

**Testing requirements.** All eligible/denied methods enumerated from the generated manifest; cookie+bearer conflict, scope escalation and agent substitution negative vectors.

**Completion gate.** No missing/default PAT metadata or generic token bypass remains.

<a id="rule-wp-22.06"></a>

### WP-22.06 — Recovery, account states and deletion

**What must be fully done.** Recovery flows designed from the start, with anti-abuse protections and clear communication. Account states — active, restricted, suspended, pending deletion — with defined capability in each. Deletion with a grace period, an explicit statement of what is and is not deleted, and no effect on local data.

**Testing requirements.** Recovery flow tests including abuse attempts; state-transition capability matrix; deletion tests asserting local data is untouched and the grace period behaves correctly.

**Completion gate.** Recovery resists the modelled abuse cases, every account state has defined capability, and deletion never touches local data.

<a id="rule-wp-22.07"></a>

### WP-22.07 — Independent native session integration

**What must be fully done.** Integrate system browser, per-product redirects, secure storage and installation-bound tokens into Platform client primitives. Android package/links follow arch 11; no token-sharing/device SSO.

**Testing requirements.** Separate product sign-in/sign-out, canceled/lost callback, wrong state/realm, expired code, device revoke and local history preservation.

**Completion gate.** Each client owns its session; browser login reuse is not shared application authority.

---

<a id="rule-wp-22.08"></a>

### WP-22.08 — Browser cookie-session adapter


**What must be fully done.** Implement the same-origin browser adapter in the AOT host using the selected random hashed session/preauth/CSRF records. Preserve the browser/native exclusive schema, exact Origin, idle/absolute expiry, lowest-trust browser installation and one-use auth flow. Map the declared /session bootstrap/auth/logout endpoints to existing application services. Use explicit cookie parsing/writing and X-AF-CSRF validation; no ASP.NET Data Protection/cookie-auth middleware dependency.

**Testing requirements.** Real D1 one-use challenge, lost login response, idle-versus-revoke race, expiry and replica failover; browser exact Origin/CSRF on unsafe RPC/session/stream/object operations, native-token route refusal and gRPC-Web stream authorization. Install two products under one OS user: neither enumerates the other account, reads its credentials, exposes a peer listener or signs a sibling challenge. Browser session convenience still produces distinct installation-bound sessions; revocation follows the selected explicit sign-out scope.

**Completion gate.** One server-owned session authority, no JS bearer, no cross-origin reuse or session resurrection; actual AOT closure feeds WP23 and full portal acceptance.

**Required implementation and closure from the final review.** Implement and independently verify [08-security-architecture](../../architecture/08-security-architecture.md#account-and-provider-closure). Implement the complete typed account surface: profile/email, recovery-code set, scoped PAT, credential rename, session listing, four sign-out scopes, independent per-installation browser authorization, remote capability policy and restricted deletion-cancel reauthentication. Exercise official email/passkey and self-host password/passkey/OIDC enrollment/recovery, no email-based merging, old refresh reuse/lost response, one-use proofs and secret-free browser session replies. Wire UI consumers through the same owner ports. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-22.90"></a>
### WP-22.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement native/Android bearer sessions, same-origin Web opaque sessions, passkeys/recovery, workspace/device rules and authenticated CF authorization ports using selected AOT-compatible components.

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

Acceptance includes every amended §5 producer/consumer and [WP-22.90](#rule-wp-22.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

| Evidence | Produced by |
|---|---|
| Identity continuity and structural separation results | [WP-22.00](#rule-wp-22.00) |
| Concurrent-refresh contention and revocation results | [WP-22.01](#rule-wp-22.01) |
| Four-concept distinction matrix and revocation cascade | [WP-22.02](#rule-wp-22.02) |
| Default-off and session-insufficiency results | [WP-22.03](#rule-wp-22.03) |
| Step-up coverage, expiry and non-substitution results | [WP-22.04](#rule-wp-22.04) |
| Token scope and revocation results | [WP-22.05](#rule-wp-22.05) |
| Recovery abuse-resistance, state matrix and deletion results | [WP-22.06](#rule-wp-22.06) |
| same-application sign-in and local-data-survival results | [WP-22.07](#rule-wp-22.07) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-22.90](#rule-wp-22.90) |

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

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [CLOUD.11](../delivery/lanes/cloud.md#task-cloud-11) | [WP-22.00](22-identity-workspace-and-device.md#rule-wp-22.00) (all work except the parts mapped to CLOUD.20) | [CLOUD.02](../delivery/lanes/cloud.md#task-cloud-02) (artifact), [CLOUD.03](../delivery/lanes/cloud.md#task-cloud-03) (artifact), [CLOUD.06](../delivery/lanes/cloud.md#task-cloud-06) (artifact) |
| [CLOUD.12](../delivery/lanes/cloud.md#task-cloud-12) | [WP-22.01](22-identity-workspace-and-device.md#rule-wp-22.01) (full) | none |
| [CLOUD.13](../delivery/lanes/cloud.md#task-cloud-13) | [WP-22.02](22-identity-workspace-and-device.md#rule-wp-22.02) (full) | [CLOUD.06](../delivery/lanes/cloud.md#task-cloud-06) (artifact) |
| [CLOUD.14](../delivery/lanes/cloud.md#task-cloud-14) | [WP-22.03](22-identity-workspace-and-device.md#rule-wp-22.03) (full) | none |
| [CLOUD.15](../delivery/lanes/cloud.md#task-cloud-15) | [WP-22.04](22-identity-workspace-and-device.md#rule-wp-22.04) (the step-up mechanism itself and coverage for Cloud/Identity-owned sensitive operations (credential change, recovery, deletion, trust elevation); full coverage across every enumerated operation in every module is completed as each owning module wires it in -- see IM.step-up-cross-product-coverage) | none |
| [CLOUD.16](../delivery/lanes/cloud.md#task-cloud-16) | [WP-22.05](22-identity-workspace-and-device.md#rule-wp-22.05) (full) | none |
| [CLOUD.17](../delivery/lanes/cloud.md#task-cloud-17) | [WP-22.06](22-identity-workspace-and-device.md#rule-wp-22.06) (full) | none |
| [CLOUD.18](../delivery/lanes/cloud.md#task-cloud-18) | [WP-22.07](22-identity-workspace-and-device.md#rule-wp-22.07) (full) | [PLT.40](../delivery/lanes/platform.md#task-plt-40) (artifact) |
| [CLOUD.19](../delivery/lanes/cloud.md#task-cloud-19) | [WP-22.08](22-identity-workspace-and-device.md#rule-wp-22.08) (full, including the 'Required implementation and closure from the final review' paragraph (complete typed account surface: profile/email, recovery-code set, scoped PAT, credential rename, session listing, four sign-out scopes, per-installation browser authorization, remote capability policy, restricted deletion-cancel reauthentication))<br>[WP-22](22-identity-workspace-and-device.md#rule-wp-22) Browser-session evidence note ([WP-22.08](22-identity-workspace-and-device.md#rule-wp-22.08) must pass before [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) consumes its contract; a written [P2-003](../../decisions/phase-2-specification-decisions.md#rule-p2-003) decision alone is insufficient) (package-level obligation contribution) | [CLOUD.01](../delivery/lanes/cloud.md#task-cloud-01) (artifact) |
| [CLOUD.20](../delivery/lanes/cloud.md#task-cloud-20) | [WP-22.90](22-identity-workspace-and-device.md#rule-wp-22.90) (full)<br>[WP-22](22-identity-workspace-and-device.md#rule-wp-22) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure appendix (initial enrollment/recovery/provider/account/SSO methods wired end-to-end in client journeys) ([P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure appendix (initial enrollment/recovery/provider/account/SSO methods wired end-to-end in client journeys))<br>[WP-22.00](22-identity-workspace-and-device.md#rule-wp-22.00) (real identity/session implementation) | [CON.07](../delivery/lanes/contracts.md#task-con-07) (artifact) |
| [CLOUD.21](../delivery/lanes/cloud.md#task-cloud-21) | [WP-22](22-identity-workspace-and-device.md#rule-wp-22) Browser-session evidence note ([WP-22.08](22-identity-workspace-and-device.md#rule-wp-22.08) must pass before [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) consumes its contract; a written [P2-003](../../decisions/phase-2-specification-decisions.md#rule-p2-003) decision alone is insufficient) (package-level obligation contribution) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [CLOUD.66](../delivery/lanes/cloud.md#task-cloud-66) | [WP-22.04](22-identity-workspace-and-device.md#rule-wp-22.04) (cross-product operation coverage beyond Identity's own operations) | [COM.10](../delivery/lanes/commerce.md#task-com-10) (artifact), [CLOUD.22](../delivery/lanes/cloud.md#task-cloud-22) (artifact) |

**Consumers outside this package:** [AND.04](../delivery/lanes/android.md#task-and-04), [AND.07](../delivery/lanes/android.md#task-and-07), [CLOUD.22](../delivery/lanes/cloud.md#task-cloud-22), [CLOUD.23](../delivery/lanes/cloud.md#task-cloud-23), [CLOUD.24](../delivery/lanes/cloud.md#task-cloud-24), [CLOUD.25](../delivery/lanes/cloud.md#task-cloud-25), [CLOUD.26](../delivery/lanes/cloud.md#task-cloud-26), [CLOUD.28](../delivery/lanes/cloud.md#task-cloud-28), [CLOUD.29](../delivery/lanes/cloud.md#task-cloud-29), [CLOUD.50](../delivery/lanes/cloud.md#task-cloud-50), [CLOUD.63](../delivery/lanes/cloud.md#task-cloud-63), [CLOUD.64](../delivery/lanes/cloud.md#task-cloud-64), [COM.13](../delivery/lanes/commerce.md#task-com-13), [DEV.01](../delivery/lanes/device-bridge.md#task-dev-01), [EXT.06](../delivery/lanes/extensions.md#task-ext-06), [EXT.08](../delivery/lanes/extensions.md#task-ext-08), [GOV.16](../delivery/lanes/governance.md#task-gov-16), [OPS.09](../delivery/lanes/operations.md#task-ops-09), [PLT.40](../delivery/lanes/platform.md#task-plt-40), [REL.06](../delivery/lanes/release.md#task-rel-06), [SIM.05](../delivery/lanes/simulator.md#task-sim-05), [SRCH.03](../delivery/lanes/search.md#task-srch-03), [WEB.10](../delivery/lanes/web.md#task-web-10), [WEB.11](../delivery/lanes/web.md#task-web-11), [WEB.30](../delivery/lanes/web.md#task-web-30).

<!-- delivery-graph:end -->

## [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure

Complete all initial enrollment/recovery/provider/account/SSO methods in client journeys and wire 04. Official passwordless and self-host configured password/OIDC are distinct; account-free startup is not account-free creation of Cloud-authoritative content. The referenced normative profile and producer stage matrix are binding inputs. Record independent positive/negative vectors and actual owner integration at this WP's assigned stage; a mock cannot close a real-provider/device requirement.
