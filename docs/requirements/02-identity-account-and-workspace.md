# Identity, Account, Device, Session and Workspace Requirements
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: `docs/decisions/phase-1-foundation-decisions.md`
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md), [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md), [`../architecture/08-security-architecture.md`](../architecture/08-security-architecture.md)

This document specifies who a principal is, what they own, which machine may act for them, and where they are currently signed in. It is the base layer that commerce, entitlement, sync, AI, remote execution and support all depend on.

**The founding separation** ([I-001](01-normative-glossary-and-invariants.md#rule-i-001)):

> **User ≠ Workspace ≠ Device ≠ Session ≠ Subscription ≠ Entitlement.**

Six responsibilities, never merged:

| Concept | Answers |
|---|---|
| **User** | Who you are |
| **Workspace** | Whose data this is |
| **Device** | Which machine may represent you |
| **Session** | Where you are signed in right now |
| **Entitlement** | Which official services you may use right now |
| **Billing Account** | Who pays for those services |

---

## 1. Native launch and Cloud account boundary

| # | Requirement |
|---|---|
| <a id="rule-id-01"></a>ID-01 | Installing and launching native applications requires no account. Cloud notebook enrolment, AI and continuity require sign-in; previously authorised hydrated content and pending edits follow the offline/cache rules. |
| <a id="rule-id-02"></a>ID-02 | The signed-out operator is a **Local Profile**: the local application identity of the current OS user on the current device. It has no server-side representation. |
| <a id="rule-id-03"></a>ID-03 | A Local Profile is **never** silently registered as a cloud "Anonymous User" or "Guest Account". No hidden server record is created on first launch. |
| ID-04 | A Local Profile owns device settings and ordinary native jobs/files. Authenticated workspace caches and pending edits remain scoped to their realm/owner; no local agent history or provider-key mode. |
| ID-05 | Sign-in identifies the selected Cloud realm/workspace for notes, sync, search, AI and remote tools. Service entitlement is checked separately; provider-key configuration is not an onboarding option. |
| ID-06 | Sign-in alone does not upload unrelated device files. Creating/importing into an enrolled Cloud notebook explicitly consents to storing those notes/managed attachments in that workspace; captures/original media require their own upload choice. |
| ID-07 | Sign-out stops Cloud access and clears active session credentials. Workspace views are locked until authentication; pending edits are retained safely and are never silently deleted or reassigned to a later account. |
| ID-08 | Service expiry blocks protected Cloud writes/AI according to the commerce lifecycle. Existing native work and pending edits remain recoverable; it does not enable an offline AI mode. |

---

## 2. Identity model

### 2.1 Realm

A **Realm** is an independent identity and data authority: the Official ArcForges Cloud, or any self-hosted deployment.

| # | Requirement |
|---|---|
| <a id="rule-id-10"></a>ID-10 | Identity is `Realm + UserId`. A bare `UserId` is never globally meaningful. |
| ID-11 | The same email address in two realms denotes two different identities. Email is never used to establish cross-realm identity ([I-465](01-normative-glossary-and-invariants.md#rule-i-465) analogue). |
| ID-12 | No client may hard-code the official API host as the only possible realm. Clients support **Server Profiles**. V1 UI may present one Official realm plus one self-hosted realm; the model supports more. |
| ID-13 | Self-host owns its own user system entirely and must never require reachability of the official service to authenticate. Optional OIDC federation to the official realm may be offered later; it must remain optional. |
| ID-14 | Cross-realm objects are never the same authoritative object. Every cross-application and cross-device reference is realm-aware. |
| ID-15 | Cross-realm movement in V1 is **Export → Import**, not live bidirectional sync. |

### 2.2 User and Authentication Identity

| # | Requirement |
|---|---|
| ID-20 | **Authentication Identity is a separate entity from User.** `User.Email = Identity` is prohibited. A User owns a set of Authentication Identities. |
| ID-21 | Official identity kinds: Email and Passkey; Apple, Google and enterprise sign-in products are later additions. Self-host configured generic OIDC/password providers follow ID-25 and are independent of official sign-in offerings. Adding or removing an identity never changes the User. |
| ID-22 | **Multiple Passkeys per User are mandatory.** `one Account = one Passkey` is prohibited. Each Passkey is renameable and shows created time and last-used time, and can be removed. |
| ID-23 | The official Cloud primary authentication method is **Email OTP + Passkey**. Email OTP performs first verification and recovery; Passkey performs daily sign-in. |
| ID-24 | The official Cloud V1 has **no password**. Password reset, credential-stuffing and breach-response flows therefore do not exist for it. |
| ID-25 | Self-host must be able to offer additional authentication providers: local password, Passkey, OIDC, enterprise identity provider. The identity domain must not assume email OTP is available to everyone. `AuthenticationProvider` is an extensible concept. |
| ID-26 | V1 does **not** implement Google, Apple or other social sign-in. The model supports adding them without a schema change. |
| ID-27 | Email verification uses a **verification code** as the primary mechanism. Magic links may be offered as a convenience but must never be the only route, because ArcForges spans desktop, mobile and web with deep-link complications. |
| ID-28 | No phone number or SMS in the first stage. No global username. No security questions. |
| ID-29 | V1 does not implement account merging. A matching email never merges realm/user identities or moves notes, devices, subscription sources or credits. |

### 2.3 Recovery

| # | Requirement |
|---|---|
| ID-30 | Recovery exists from the first release. Primary recovery is Email; secondary recovery is one-time **Recovery Codes** (a generated set, displayed once, individually consumable). |
| ID-31 | Recovery Code generation is a step-up-authenticated operation and produces a security notification. |

### 2.4 Profile

Account Profile is deliberately minimal: Display Name, Avatar, Primary Email, Locale, Timezone. Username, real name, phone, birthday, gender and address are **not** collected. Billing address is handled inside the payment flow and never stored on the User profile.

---

## 3. Workspace

| # | Requirement |
|---|---|
| WS-01 | **All cloud data belongs to a Workspace, never directly to a User.** `User.Notes`, `User.Storage`, `User.SubscriptionId` and equivalents are prohibited. |
| WS-02 | On registration a **Personal Workspace** is created automatically and owned by the User. |
| WS-03 | Workspace is the single-owner boundary for data, device access, storage, AI usage/budget, sync, authorisation and entitlement. |
| WS-04 | Organisations, team workspaces, membership roles and invitation models are excluded. V1 provisions one personal workspace per user in each realm. |
| WS-05 | Cross-user workspace access and shared credit pools are excluded. Device access belongs to the same owner and is independently revocable. |
| WS-06 | Account deletion applies to the owner personal workspace; no organisation ownership transfer or membership departure prerequisite exists. |
| <a id="rule-ws-07"></a>WS-07 | Every Cloud object belongs to a workspace. Authorisation checks authenticated realm/user → workspace OwnerUserId → resource permission, plus current service/device constraints. ObjectId knowledge is never permission. |
| WS-08 | An AI session has one explicit active realm/workspace. Another owner workspace or another realm is never searched or accessed implicitly. |
| <a id="rule-ws-09"></a>WS-09 | Workspace carries a **DataRegion** attribute from day one, defaulting to `Automatic`. It exists so regional requirements can be met later without a data-model migration. No public claim of a specific storage jurisdiction may be made unless infrastructure that legally guarantees it is actually in use. |
| WS-10 | Standard Cloud protection applies: authenticated access, workspace isolation, TLS and encryption at rest. No E2EE profile, encrypted-export mode or future encryption-profile field is required. |

---

## 4. Device, Installation, Instance and Session

Four distinct concepts ([I-007](01-normative-glossary-and-invariants.md#rule-i-007), [I-008](01-normative-glossary-and-invariants.md#rule-i-008), [I-009](01-normative-glossary-and-invariants.md#rule-i-009)):

```
User
 └── Device                 (a long-lived trusted installation environment)
      └── App Installation  (one product installed on that device)
           └── Runtime Instance  (one running process)

Session                     (one app's current authenticated login state)
```

| # | Requirement |
|---|---|
| DV-01 | **Device** carries: name, platform, created time, last-seen time, trust status, remote-enabled flag, and a revoke action. |
| DV-02 | Device identity is **created by user authorization**, not derived from a hardware fingerprint. CPU serial, motherboard ID and MAC address must not be used to identify a device — they break under virtualisation, reinstall, hardware replacement, and are privacy-hostile. A device may be renamed, revoked and re-registered. |
| DV-03 | **App Installation** is a distinct cloud-visible dimension. A process instance is never a device identity. |
| DV-04 | **Session** is per-application authenticated state. Sessions expire; the Device survives. One device may hold several concurrent sessions (`ArcChat`, `ArcNotes`, `ArcScope`, browser). |
| DV-05 | **Device SSO** — after a user signs in from one Arc product on a device, another Arc product on the same device offers "Continue as \<name\>" rather than re-entering an email. |
| DV-06 | **Device SSO must not create an architecture dependency.** ArcNotes signing in must work with ArcChat absent. The unified account/session infrastructure is shared desktop foundation, never an ArcChat-private authentication service. |
| DV-07 | Sign-out distinguishes four operations, each with different scope: **Sign out of this App** (other Arc apps stay signed in), **Sign out of this Device** (all Arc app cloud sessions revoked, local data retained), **Revoke Device** (performed from another device; stops sync, remote and cloud access), **Sign out everywhere** (all sessions cleared; the account remains). |

---

## 5. Trust and remote access

| # | Requirement |
|---|---|
| TR-01 | **Device Presence ≠ Device Trust** ([I-250](01-normative-glossary-and-invariants.md#rule-i-250)). Presence is ephemeral; trust is a durable, user-granted state. |
| TR-02 | **Device Online ≠ Remote Agent Enabled** ([I-251](01-normative-glossary-and-invariants.md#rule-i-251)). |
| TR-03 | **Registered Device ≠ Remote-authorized Device** ([I-252](01-normative-glossary-and-invariants.md#rule-i-252)). |
| <a id="rule-tr-04"></a>TR-04 | Remote access defaults to **off**. The chain is `Account → Trusted Device → Remote Enabled → Allowed Capabilities`. |
| TR-05 | Remote capability grants are per-product and per-capability-class, individually toggleable (for example ArcNotes and ArcScope enabled, ArcSlate export not). |
| TR-06 | High-risk capabilities may additionally require local confirmation on the desktop even when remote access is enabled. R4-class operations — credential changes, security settings, high-risk device operations — are **never remotely releasable by default**; cloud and mobile may only prompt the user to return to a trusted device. |
| TR-07 | Remote access is delivered by a desktop-initiated authenticated **outbound** connection to Cloud. **No inbound public port is opened on the user's machine.** |
| TR-08 | The user can revoke a device, disable remote access and revoke capability scope at any time, from any signed-in surface. |

---

## 6. Step-up authentication

Re-authentication is required for a sensitive operation even inside a valid session: `Normal Session → Sensitive Action → Passkey or fresh OTP → Continue`.

Operations requiring step-up:

- Change email
- Remove all Passkeys
- Generate Recovery Codes
- Delete Account
- Add or revoke an external connector authorisation
- Reveal or replace any sensitive secret
- Enable Remote Agent
- Revoke trusted devices
- Create a high-privilege API token
- Change the owner account’s security or recovery credentials

**Step-up ≠ Approval** ([I-242](01-normative-glossary-and-invariants.md#rule-i-242)). Step-up proves identity; Approval authorises a specific pending operation.

---

## 7. API tokens

| # | Requirement |
|---|---|
| AT-01 | Personal Access Tokens exist in the model from the first release, for CLI, automation, third-party agents and integrations. |
| AT-02 | Every token is **named**, **scoped**, **expirable**, **revocable**, and displays last-used time. |
| AT-03 | A permanent, unscoped master API key is prohibited. |
| AT-04 | Token scopes are drawn from the same capability/permission vocabulary as the rest of the system (for example `notes.read`, `notes.write`). |

---

## 8. Actor model

| # | Requirement |
|---|---|
| AC-01 | Human users and machine actors are never conflated. `Actor` has kinds: **User**, **Agent**, **Device**, **ServiceAccount**. |
| <a id="rule-ac-02"></a>AC-02 | Audit records the true actor kind. An agent-performed action must never be recorded as if the human performed it directly. |
| AC-03 | **Identity ≠ Actor ≠ Executor ≠ Caller Process** ([I-230](01-normative-glossary-and-invariants.md#rule-i-230)). |
| AC-04 | An Agent Profile is configuration, never a security principal ([I-232](01-normative-glossary-and-invariants.md#rule-i-232)). |
| AC-05 | An Automation is not a principal ([I-234](01-normative-glossary-and-invariants.md#rule-i-234)); it carries a creator permission snapshot which is **not** permanent authority ([I-236](01-normative-glossary-and-invariants.md#rule-i-236)). |

---

## 9. Account lifecycle states

Account status is richer than Active/Deleted:

| State | Meaning | Local effect |
|---|---|---|
| `Pending` | Registered, first verification incomplete | None |
| `Active` | Normal | None |
| `Restricted` | e.g. AI abuse — cloud AI disabled; the user can still sign in and export | **None** |
| `Suspended` | Serious violation — protected Cloud operations denied | Native capture/media and pending-work recovery remain; cached data follows its authorized access contract |
| `DeletionPending` | Deletion requested, within the reversal window | None |
| `Deleted` | Cloud identity and data removed subject to retention | Independent native files and pending work are not remotely wiped; cached Cloud views are no longer an active workspace |

[I-016](01-normative-glossary-and-invariants.md#rule-i-016): **Cloud Account Restriction ≠ Local Data Confiscation.**

---

## 10. Account deletion

Deletion is a first-class, in-product flow, required both in-app and on the web (Apple and Google both mandate an in-app deletion entry point; Google additionally mandates a web entry point).

Required entry points:

- In every product: Settings → Account → Delete Account.
- On the web: the canonical account portal, at `account.arcforges.com` (**[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)**), with `arcforges.com/account` as a permanent redirect.

Flow: `Request → Step-up Authentication → Explain consequences → Offer data export → Confirm → DeletionPending`.

On entering DeletionPending, prohibit new Cloud writes and AI dispatch, stop renewal, revoke ordinary sessions/devices/API tokens/remote access, and schedule data/credential purge after the disclosed reversal window. A narrowly scoped reauthentication/recovery path may cancel deletion within that window; ordinary revoked tokens cannot. Purge workspace content and derived data only at the irreversible deadline, subject to explicit retention duties; commercial/security records follow separate retention.

| # | Requirement |
|---|---|
| <a id="rule-dl-01"></a>DL-01 | Account deletion does not remotely erase independent native capture/media files or pending user edits/uploads. Preview their fate before confirmation and offer recovery. Explicit local cache deletion is a separate choice. A guarded recovery view for locally owned pending work must remain usable without paid Cloud access, even if the Cloud identity has been deleted; it is not a new standalone notebook mode. |
| DL-02 | **Subscription cancellation ≠ Account deletion ≠ Cloud data deletion ≠ Workspace deletion** ([I-002](01-normative-glossary-and-invariants.md#rule-i-002)). Four distinct flows. |
| DL-03 | A user may delete cloud data while retaining the account, AI credits and purchase history. |
| DL-04 | Deletion propagates to derived data: full-text index entries, vector entries, derived previews and caches. A deleted document must not remain findable through semantic search ([I-165](01-normative-glossary-and-invariants.md#rule-i-165)). |

---

## 11. Security notifications and activity

| # | Requirement |
|---|---|
| SN-01 | The account portal exposes security activity: device sign-in/revocation, passkey/email/recovery changes, connector authorisation and remote access enablement. No BYOK event class is required. |
| <a id="rule-sn-02"></a>SN-02 | Security notifications are **not opt-out**: new sign-in, email changed, passkey removed, recovery used, remote access enabled, account deletion requested. |
| SN-03 | Marketing email is separately opt-in and opt-out and must never be bundled with security notification preferences. |

---

## 12. Account portal

The **ArcForges Account Portal** is a first-class product surface, not a marketing page. It is canonically `account.arcforges.com` (**[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)**), served by the single `ArcForges.Web.App` codebase (**[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**).

Minimum V1 portal scope:

| Section | Contents |
|---|---|
| Account | Profile, Email, Locale, Timezone |
| Security | Passkeys, Recovery Codes, Sessions, Devices, Security Activity, API Tokens |
| Workspace | Personal Workspace, Storage usage by product, AI usage |
| Cloud | Sync state, Devices, Remote Access |
| Billing | Plan, Subscription, Storage add-ons, AI credits |
| Data | Export, Delete Account |

**In-product account UI stays lightweight.** A desktop product shows the signed-in identity, realm, storage summary and a "Manage Account →" link to the portal. Passkeys, billing, devices, recovery and deletion are managed centrally, not reimplemented per product.

---

## 13. Commerce separation

| # | Requirement |
|---|---|
| BI-01 | **Billing Account is a separate entity from User.** `User.SubscriptionId` is prohibited. The chain is `Billing Account → Subscription → Entitlement → Workspace`. |
| BI-02 | **Billing identity is never matched by email.** A payment email such as `finance@company.com` must never be used to decide which account a subscription belongs to. A stable internal billing identity is the buyer identity; email is contact information only. Changing the account email must never lose a subscription (**[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)** preserved principles). |
| BI-03 | Provider identifiers never enter client authority contracts (**[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**). |

---

## 14. Credential ownership

| # | Requirement |
|---|---|
| SC-01 | Client login/device credentials use OS secure storage. Operator model/payment/signing credentials live only in Cloud deployment secret storage; no end-user AI provider-key vault or reveal API exists. |
| SC-02 | External connector credentials, where an accepted integration needs them, are workspace-scoped and distinct from operator AI-provider credentials. Removing BYOK does not remove connector authentication or device identity. |
| SC-03 | Secret management exposes authorised replacement/revocation/status, never full secret retrieval. Operator deployment credentials are not editable through a customer settings screen. |
| SC-04 | **SecretRef ≠ Secret Value** ([I-256](01-normative-glossary-and-invariants.md#rule-i-256)) and **Secret Use ≠ Secret Reveal** ([I-257](01-normative-glossary-and-invariants.md#rule-i-257)). |

---

## 15. Domain model

The cloud identity domain must be able to express:

```
Identity Realm
├── User
│   ├── Profile
│   ├── Authentication Identity  (Email · Passkey · External Provider)
│   ├── Recovery                 (Email · Recovery Codes)
│   ├── Security Activity
│   └── OwnerUserId ────────────► Personal Workspace
│
├── Workspace   (single owner)
│   ├── DataRegion
│   └── OwnerUserId
│
├── Device
│   └── App Installation
│        └── Runtime Instance
│
├── Session
├── Trusted Device
├── Remote Access Grant
├── API Token
├── Actor            (User | Agent | Device | ServiceAccount)
├── Billing Account
├── Subscription
├── Entitlement
├── Storage Quota
├── AI Capacity and Credit Accounts
└── Secret Vault
```

This document settles **identity ownership relationships**; commercial rules for Billing Account, Subscription, Entitlement, Storage Quota and AI Capacity and Credit Accounts are specified in [`04-commerce-entitlement-and-credits.md`](04-commerce-entitlement-and-credits.md).

---

## 16. Acceptance criteria

| # | Scenario | Required outcome |
|---|---|---|
| A-01 | Fresh install, no network/account | Native UI starts within budget; local capture/media operations are usable; initial Cloud notebook enrolment and AI show their sign-in/network requirement |
| A-02 | Sign in with unrelated local files present | Nothing is automatically imported/uploaded; explicit notebook enrolment and file selection define participation |
| A-03 | Sign out of ArcNotes while ArcChat is signed in | ArcChat session unaffected; ArcNotes local data intact |
| A-04 | Revoke a device from another device | The revoked device loses sync, remote and cloud access; its local data is intact |
| A-05 | Enable remote access, then attempt an R4 operation from mobile | The operation is refused remotely and the user is directed to confirm on a trusted device |
| A-06 | Sign in to Official and to a self-hosted realm with the same email | Two distinct identities; no data or entitlement crosses between them |
| A-07 | Delete all Passkeys, then recover via Email | Recovery succeeds; a security notification is emitted; the user is prompted to add a Passkey |
| A-08 | Account moves to Suspended | Cloud/AI access is denied; native files and pending edits are preserved; the product accurately distinguishes available local operations |
| A-09 | Request account deletion | Step-up is required; export is offered; on confirmation, cloud identity, workspace data, index entries and vault entries are removed; local files remain |
| A-10 | Change account email while subscribed | Subscription and entitlement are unaffected |
| A-11 | Cross-owner workspace ObjectId probe | Access denied regardless of a known object ID or valid subscription on another workspace |
| A-12 | Switch realm/workspace while an AI task or local edit is pending | The original scope remains fixed; another account cannot read its cache, spend its credits or redirect its pending operation |

---

## 17. Traceability

| Current document | Relationship |
|---|---|
| [Security Architecture](../architecture/08-security-architecture.md) | Implements identity, authentication, authorization and realm isolation |
| [Cloud Data Model](../architecture/data-model/01-cloud-data-model.md) | Defines persisted identity, workspace, device and session records |
| [Public API Operations](../architecture/contracts/01-public-api-operations.md) | Defines the account and device operations consumed by clients |
| **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**, **[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)** | Surface inventory and the canonical account portal origin |
| **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)** | Billing identity separation and provider-abstraction principles |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** | Mobile account/security settings limited to non-commercial operations |
