# Identity, Account, Device, Session and Workspace Requirements

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: `docs/decisions/phase-1-foundation-decisions.md`
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md), [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md), [`../architecture/08-security-architecture.md`](../architecture/08-security-architecture.md)

This document specifies who a principal is, what they own, which machine may act for them, and where they are currently signed in. It is the base layer that commerce, entitlement, sync, AI, remote execution and support all depend on.

**The founding separation** (`I-001`):

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

## 1. The no-account rule

| # | Requirement |
|---|---|
| ID-01 | Installing, launching and fully using any desktop product locally requires **no account**. No product may present a "Sign in to continue" gate on first run or on any local path. |
| ID-02 | The signed-out operator is a **Local Profile**: the local application identity of the current OS user on the current device. It has no server-side representation. |
| ID-03 | A Local Profile is **never** silently registered as a cloud "Anonymous User" or "Guest Account". No hidden server record is created on first launch. |
| ID-04 | A Local Profile owns local settings, local documents, local agent history, local BYOK keys and local indexes. |
| ID-05 | Sign-in is requested only when the user activates a cloud capability: Enable Sync, Back up to Cloud, Use Arc AI, Remote Access, Continue on Mobile, Continue on Web, Cloud BYOK, Cloud Search. |
| ID-06 | Signing in **never** implies upload. After sign-in the user makes an explicit, per-scope choice about what participates in sync. A user with 2,000 local notes and 300 GB of local media must not observe an automatic upload. |
| ID-07 | Signing out never deletes local data. Signing out stops cloud sync; local content remains. |
| ID-08 | Subscription expiry never disables local application functionality (`C-07`). |

---

## 2. Identity model

### 2.1 Realm

A **Realm** is an independent identity and data authority: the Official ArcForges Cloud, or any self-hosted deployment.

| # | Requirement |
|---|---|
| ID-10 | Identity is `Realm + UserId`. A bare `UserId` is never globally meaningful. |
| ID-11 | The same email address in two realms denotes two different identities. Email is never used to establish cross-realm identity (`I-465` analogue; Stage 7 §83). |
| ID-12 | No client may hard-code the official API host as the only possible realm. Clients support **Server Profiles**. V1 UI may present one Official realm plus one self-hosted realm; the model supports more. |
| ID-13 | Self-host owns its own user system entirely and must never require reachability of the official service to authenticate. Optional OIDC federation to the official realm may be offered later; it must remain optional. |
| ID-14 | Cross-realm objects are never the same authoritative object. Every cross-application and cross-device reference is realm-aware. |
| ID-15 | Cross-realm movement in V1 is **Export → Import**, not live bidirectional sync. |

### 2.2 User and Authentication Identity

| # | Requirement |
|---|---|
| ID-20 | **Authentication Identity is a separate entity from User.** `User.Email = Identity` is prohibited. A User owns a set of Authentication Identities. |
| ID-21 | Supported identity kinds: Email, Passkey, and — as later additions — Apple, Google and enterprise SSO. Adding or removing an identity never changes the User. |
| ID-22 | **Multiple Passkeys per User are mandatory.** `one Account = one Passkey` is prohibited. Each Passkey is renameable and shows created time and last-used time, and can be removed. |
| ID-23 | The official Cloud primary authentication method is **Email OTP + Passkey**. Email OTP performs first verification and recovery; Passkey performs daily sign-in. |
| ID-24 | The official Cloud V1 has **no password**. Password reset, credential-stuffing and breach-response flows therefore do not exist for it. |
| ID-25 | Self-host must be able to offer additional authentication providers: local password, Passkey, OIDC, enterprise identity provider. The identity domain must not assume email OTP is available to everyone. `AuthenticationProvider` is an extensible concept. |
| ID-26 | V1 does **not** implement Google, Apple or other social sign-in. The model supports adding them without a schema change. |
| ID-27 | Email verification uses a **verification code** as the primary mechanism. Magic links may be offered as a convenience but must never be the only route, because ArcForges spans desktop, mobile and web with deep-link complications. |
| ID-28 | No phone number or SMS in the first stage. No global username. No security questions. |
| ID-29 | Account merging is never automatic and never inferred from a matching email address. Both identities must be re-verified. V1 need not implement merge; the model must permit it, handling Identity, Personal Workspace, Subscription, AI Credits, Organization Membership and Devices separately. |

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
| WS-03 | Workspace is the boundary for data, storage quota, AI usage and budget, sync participation, membership and entitlement. |
| WS-04 | **Organization** is modelled from day one with roles Owner / Admin / Member / Guest, and is not opened in V1. An Organization owns Organization Workspaces. |
| WS-05 | Leaving an organization removes a **Membership**, never the User. The user's Personal Workspace is unaffected. |
| WS-06 | An Organization Owner cannot delete their account without first transferring ownership or deleting the Organization. |
| WS-07 | **Every cloud object belongs to a Workspace** — objects, tasks, search index entries, AI credits, secrets, artifacts, automations. Authorization is always `Actor → Membership → Workspace → Resource`. Knowledge of an `ObjectId` never grants access. |
| WS-08 | An agent session always has an explicit **Active Workspace**. Data is never searched across workspaces implicitly, even where the user is a member of both. Cross-workspace operations are explicit user acts. |
| WS-09 | Workspace carries a **DataRegion** attribute from day one, defaulting to `Automatic`. It exists so regional requirements can be met later without a data-model migration. No public claim of a specific storage jurisdiction may be made unless infrastructure that legally guarantees it is actually in use. |
| WS-10 | Workspace carries a **DataProtectionProfile**: `Standard` (V1) or `EndToEndEncrypted` (modelled now, released later). See [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md) §6. |

---

## 4. Device, Installation, Instance and Session

Four distinct concepts (`I-007`, `I-008`, `I-009`, Stage 1 §15–17):

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
| DV-06 | **Device SSO must not create an architecture dependency.** ArcNotes signing in must work with ArcChat absent. The unified account/session infrastructure is shared desktop foundation, never an ArcChat-private authentication service (Stage 13 §58). |
| DV-07 | Sign-out distinguishes four operations, each with different scope: **Sign out of this App** (other Arc apps stay signed in), **Sign out of this Device** (all Arc app cloud sessions revoked, local data retained), **Revoke Device** (performed from another device; stops sync, remote and cloud access), **Sign out everywhere** (all sessions cleared; the account remains). |

---

## 5. Trust and remote access

| # | Requirement |
|---|---|
| TR-01 | **Device Presence ≠ Device Trust** (`I-250`). Presence is ephemeral; trust is a durable, user-granted state. |
| TR-02 | **Device Online ≠ Remote Agent Enabled** (`I-251`). |
| TR-03 | **Registered Device ≠ Remote-authorized Device** (`I-252`). |
| TR-04 | Remote access defaults to **off**. The chain is `Account → Trusted Device → Remote Enabled → Allowed Capabilities`. |
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
- Add or replace Cloud BYOK credentials
- Reveal or replace any sensitive secret
- Enable Remote Agent
- Revoke trusted devices
- Create a high-privilege API token
- Transfer Organization ownership

**Step-up ≠ Approval** (`I-242`). Step-up proves identity; Approval authorises a specific pending operation.

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
| AC-02 | Audit records the true actor kind. An agent-performed action must never be recorded as if the human performed it directly. |
| AC-03 | **Identity ≠ Actor ≠ Executor ≠ Caller Process** (`I-230`). |
| AC-04 | An Agent Profile is configuration, never a security principal (`I-232`). |
| AC-05 | An Automation is not a principal (`I-234`); it carries a creator permission snapshot which is **not** permanent authority (`I-236`). |

---

## 9. Account lifecycle states

Account status is richer than Active/Deleted:

| State | Meaning | Local effect |
|---|---|---|
| `Pending` | Registered, first verification incomplete | None |
| `Active` | Normal | None |
| `Restricted` | e.g. AI abuse — cloud AI disabled; the user can still sign in and export | **None** |
| `Suspended` | Serious violation — official Cloud discontinued | **None. Local products must never be remotely locked.** |
| `DeletionPending` | Deletion requested, within the reversal window | None |
| `Deleted` | Cloud identity and data removed | **None. Local files remain.** |

`I-016`: **Cloud Account Restriction ≠ Local Data Confiscation.**

---

## 10. Account deletion

Deletion is a first-class, in-product flow, required both in-app and on the web (Apple and Google both mandate an in-app deletion entry point; Google additionally mandates a web entry point).

Required entry points:

- In every product: Settings → Account → Delete Account.
- On the web: the canonical account portal, at `account.arcforges.com` (**D-015**), with `arcforges.com/account` as a permanent redirect.

Flow: `Request → Step-up Authentication → Explain consequences → Offer data export → Confirm → DeletionPending`.

On entering `DeletionPending`, the system must: prohibit new cloud writes; cancel or stop renewal per billing rules; revoke sessions, devices, API tokens and remote access; delete workspace data, the vector index, cloud BYOK secrets and cloud resources; and process records that must legally be retained (accounting) under a stated retention policy.

| # | Requirement |
|---|---|
| DL-01 | **Local data is not part of account deletion** (`I-016`). `~/Documents/ArcNotes` and equivalents are never deleted automatically. A separate, explicit "delete local data too" choice exists. |
| DL-02 | **Subscription cancellation ≠ Account deletion ≠ Cloud data deletion ≠ Workspace deletion** (`I-002`). Four distinct flows. |
| DL-03 | A user may delete cloud data while retaining the account, AI credits and purchase history. |
| DL-04 | Deletion propagates to derived data: full-text index entries, vector entries, derived previews and caches. A deleted document must not remain findable through semantic search (`I-165`, Stage 7 §71). |

---

## 11. Security notifications and activity

| # | Requirement |
|---|---|
| SN-01 | The account portal exposes a **Security Activity** log the user can read: new device sign-in, passkey added or removed, email changed, recovery initiated, device revoked, Cloud BYOK changed, remote access enabled. |
| SN-02 | Security notifications are **not opt-out**: new sign-in, email changed, passkey removed, recovery used, remote access enabled, account deletion requested. |
| SN-03 | Marketing email is separately opt-in and opt-out and must never be bundled with security notification preferences. |

---

## 12. Account portal

The **ArcForges Account Portal** is a first-class product surface, not a marketing page (Stage 1 §44). It is canonically `account.arcforges.com` (**D-015**), served by the single `ArcForges.Web.App` codebase (**D-014**).

Minimum V1 portal scope:

| Section | Contents |
|---|---|
| Account | Profile, Email, Locale, Timezone |
| Security | Passkeys, Recovery Codes, Sessions, Devices, Security Activity, API Tokens |
| Workspace | Personal Workspace, Storage usage by product, AI usage |
| Cloud | Sync state, Devices, Remote Access |
| Billing | Plan, Subscription, Storage add-ons, AI credits |
| Data | Export, Delete Account |

**In-product account UI stays lightweight.** A desktop product shows the signed-in identity, realm, storage summary and a "Manage Account →" link to the portal. Passkeys, billing, devices, recovery and deletion are managed centrally, not reimplemented per product (Stage 1 §43).

---

## 13. Commerce separation

| # | Requirement |
|---|---|
| BI-01 | **Billing Account is a separate entity from User.** `User.SubscriptionId` is prohibited. The chain is `Billing Account → Subscription → Entitlement → Workspace`. |
| BI-02 | **Billing identity is never matched by email.** A payment email such as `finance@company.com` must never be used to decide which account a subscription belongs to. A stable internal billing identity is the buyer identity; email is contact information only. Changing the account email must never lose a subscription (**D-005** preserved principles). |
| BI-03 | Provider identifiers never enter client authority contracts (**D-005**). |

---

## 14. Secrets and BYOK ownership

| # | Requirement |
|---|---|
| SC-01 | **Local BYOK belongs to the Device**, stored in platform secure storage. **Cloud BYOK belongs to the Workspace**, stored in a Workspace Secret Vault. `User.Profile.ApiKey` is prohibited. |
| SC-02 | This split is what allows an Organization to hold a shared provider key without a member's personal BYOK leaking into the Organization. |
| SC-03 | A stored secret is never re-displayable in full. The vault exposes: replace, revoke, test, fingerprint/last-4, last-used, and audit. `GET /apikey` returning plaintext is prohibited. |
| SC-04 | **SecretRef ≠ Secret Value** (`I-256`) and **Secret Use ≠ Secret Reveal** (`I-257`). |

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
│   └── Membership ──────────────► Workspace
│
├── Workspace   (Personal | Organization)
│   ├── DataRegion
│   ├── DataProtectionProfile
│   └── Members
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
├── AI Wallet
└── Secret Vault
```

Stage 1 settles **identity ownership relationships** only. Commercial rules for Billing Account, Subscription, Entitlement, Storage Quota and AI Wallet are specified in [`04-commerce-entitlement-and-credits.md`](04-commerce-entitlement-and-credits.md).

---

## 16. Acceptance criteria

| # | Scenario | Required outcome |
|---|---|---|
| A-01 | Fresh install, no network, no account | Product reaches an editable state within its startup budget; no sign-in gate appears |
| A-02 | Sign in with 2,000 local notes present | No automatic upload; an explicit per-scope sync choice is presented |
| A-03 | Sign out of ArcNotes while ArcChat is signed in | ArcChat session unaffected; ArcNotes local data intact |
| A-04 | Revoke a device from another device | The revoked device loses sync, remote and cloud access; its local data is intact |
| A-05 | Enable remote access, then attempt an R4 operation from mobile | The operation is refused remotely and the user is directed to confirm on a trusted device |
| A-06 | Sign in to Official and to a self-hosted realm with the same email | Two distinct identities; no data or entitlement crosses between them |
| A-07 | Delete all Passkeys, then recover via Email | Recovery succeeds; a security notification is emitted; the user is prompted to add a Passkey |
| A-08 | Account moves to `Suspended` | Cloud services stop; every desktop product continues to function locally with full capability |
| A-09 | Request account deletion | Step-up is required; export is offered; on confirmation, cloud identity, workspace data, index entries and vault entries are removed; local files remain |
| A-10 | Change account email while subscribed | Subscription and entitlement are unaffected |
| A-11 | Cross-workspace object-id probe | Access is denied by workspace scoping, regardless of membership in another workspace |
| A-12 | Agent session with two workspace memberships | Search and retrieval are confined to the Active Workspace; no implicit cross-workspace access |

---

## 17. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 1` | The entire identity, device, session, workspace and portal model |
| `I4 §Stage 7 §74–75, §80–85` | Workspace-scoped authorization, realm separation, self-host boundaries |
| `I4 §Stage 13 §56–60` | Account-independence and realm invariants at the product-topology level |
| `I3 §20` | Identity layering, local IPC authentication, secret storage |
| **D-014**, **D-015** | Surface inventory and the canonical account portal origin |
| **D-005** | Billing identity separation and provider-abstraction principles |
| **D-022** | Mobile account/security settings limited to non-commercial operations |
