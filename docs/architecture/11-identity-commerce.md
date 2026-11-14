# Identity, entitlements and hosted commerce

Status: V2 target design. Existing Go identity/session/device/entitlement foundations are retained and adapted; production subscription sales and the V2 management product are not yet delivered. Owners: `AFV2-CENTER-01`, `AFV2-ID-01`, `AFV2-HOST-01`, `AFV2-HOST-02`, `AFV2-WEB-03`.

## 1. Product and hosting rule

ArcForges software is open source. Local CLI execution, resource management and Sandbox data management work without an account, official server or subscription. A user-operated Center and its Blazor management UI have the corresponding remote capabilities without an official subscription. Official hosted Node connectivity and remote management are subscription services.

| Operation | Local use | Self-hosted Center | Official-hosted Center |
|---|---|---|---|
| Create/start/attach/stop local Sandbox Runs | Free; no account or network prerequisite | Unaffected by server state | Unaffected by subscription or server state |
| Local resource and data management | Free | Free | Free |
| Remote Node connection | Not required | Enabled subject to operator configuration and authentication | Requires hosted service entitlement |
| Remote view/control | Not required | Enabled subject to owner grant and operator limits | Requires hosted entitlement **and** owner grant |
| Account sign-in, security remediation and device revocation | Local identity only where applicable | Available | Available even after hosted entitlement expires |
| Hosted billing/cancellation/history | Not applicable | Not an official billing prerequisite | Available to the account, including lapsed subscribers |

There is no artificial local feature lock, online license check or entitlement token in Sandbox Core's execution path. There is no official account federation requirement for a self-hosted Center. Resource/traffic limits imposed by a self-hosted operator are operational policy, not an official paid tier.

Prices, currencies, commercial quotas, trials, offers and tax/legal texts remain owner decisions. No example price or quota is a product commitment. An unconfigured official catalog keeps sales closed and gated hosted features unavailable; the UI states the missing service configuration without implying a local software limitation.

## 2. Identity assets and boundaries

Retain Go account identity, WebAuthn/passkey and email-code sign-in, explicit self-host bootstrap, cookie and native bearer sessions, refresh rotation/reuse detection, step-up proof, device/installation records, rate limiting and audit. These are real code in `Cloud/center/internal/identity`, `session`, `device`, `access` and `pages`, with PostgreSQL integration tests; [the audit](../research/cloud-audit.md) distinguishes the code from unperformed real provider/browser acceptance.

The current route inventory registers 22 identity/device methods. It explicitly leaves recovery, account deletion, account export and email change unregistered. Public proto declarations do not make those services implemented. `AFV2-ID-01`, dependent on `AFV2-CENTER-01` and owning `R-CTR-004`, completes the minimal recovery/deletion/export lifecycle required by this product; `AFV2-WEB-03` consumes it after acceptance. Other old identity promises do not automatically enter V2 scope.

The Node connects with its own installation key and Node-scoped credential. It cannot use that credential for account billing, credential administration or operator actions. The browser uses an account cookie bound to its exact origin. A Cloud operator is a service administrator, not an implicit owner of every enrolled computer.

| Identity | Authority | Revocation effect |
|---|---|---|
| Local OS owner | Local Core operations and local remote-grant creation/expansion | Ends local client authority; does not depend on Center |
| Account session | Own account, enrollment and explicitly permitted remote methods | Blocks new calls and ends that session's subscriptions |
| Node installation | Its enrollment/channel, report and credential refresh | Channel closed; local Runs continue |
| Hosted operator | Explicit service/billing/configuration actions, audited and step-up protected | Removes administrative authority; no local process action |
| Self-host operator | Own Center configuration/bootstrap and service limits | Operator-controlled; does not create unbounded Node authority |

Keep one-use proof semantics. A recent authentication timestamp is not interchangeable with operation-bound step-up evidence. High-risk enrollment revocation, destructive data operation and grant/security changes use the operation class and exact target binding defined by the API/security contract. Human and Node credentials are differentiated by scopes and cryptographic origin, without preserving the cancelled AI Agent/Harness product model.

The initial V2 authorization model is account ownership plus explicit local Node/Sandbox grants. Do not add organization/team sharing, arbitrary custom roles or an enterprise policy engine to this delivery. Shared independent products can continue to consume their existing contracts without becoming ArcForges V2 prerequisites.

### 2.1 Minimal account lifecycle

Recovery starts with a bounded, non-enumerating request and a one-use challenge delivered only to an already verified recovery channel. Reuse the existing email delivery/proof primitives where applicable, with per-account and source rate limits, bounded attempts and an explicit expiry. An unavailable sender produces a service-state error without inventing an alternate proof path. An existing valid passkey can use normal sign-in/step-up. Recovery completion verifies the bound proof, increments recovery generation, revokes affected session/refresh families and enrolled remote credentials, and records audit/outbox effects in one transaction. A replacement passkey is registered only through a ceremony bound to the verified recovery operation; any recovered session is newly issued at the current generation, never an old session reactivated. Recovery creates no implicit local grant and issues no Run stop or local data delete. A user who controls neither an accepted credential nor the registered recovery channel cannot claim the account through an operator bypass introduced by this task.

Deletion is prepare then confirm. An authenticated request obtains an operation-bound step-up challenge and an expiring deletion plan identifying the account, active subscriptions, unresolved remote commands and retained-record categories. Confirmation binds the plan revision, proof and stable command identity. Its transaction marks deletion pending, denies new account/remote work, revokes sessions/enrollments and schedules idempotent service cleanup. Provider cancellation/reconciliation and unresolved command evidence are settled through bounded retryable jobs before final deletion status. A timeout is reconciled with the same command identity. No account deletion sends Sandbox deletion or Run stop: local data and existing processes remain with their local owner. Financial/audit retention follows the configured approved policy; durable non-executable command identities are retained or privacy-preservingly transformed so deletion cannot reopen replay.

Export is authenticated and operation-bound, with recent step-up for the exact account. It includes account profile, public credential/device metadata, relevant security/entitlement and billing facts; it excludes private keys, session/refresh tokens, recovery secrets, Node logs and local Sandbox files. Use bounded page/byte limits and a short-lived account-bound export receipt. Each download rechecks current authorization and receipt expiry; a signed URL alone cannot grant a different account access. Background materialization, if required, uses temporary protected storage with expiry and content deletion. The database stores the receipt/digest/status, not an unlimited export blob. Requests and completion are idempotent; revocation cancels undisclosed exports. The implementation must test challenge reuse, race with revoke, duplicate confirmation, provider outage and export expiry, alongside ordinary success.

## 3. Local remote grants

Local remote authority is a separate durable Node record bound to Center audience, enrollment, account identity, permitted Sandbox IDs/actions and a local policy revision. Default is disabled. The local owner can enable view/logs, Run control, permitted configuration/resource edits, regular-file transfer or Sandbox deletion individually. The effective authority is the intersection of the request's authenticated scope, Center policy, local grant, Sandbox policy and backend capability.

Only the local owner may edit a grant, authorize a new host path, change the data root or increase the local resource ceiling. A remote caller may revoke its grant through the fixed typed revocation action. Grant narrowing/re-enablement uses local `SetRemoteGrant`; remote configuration/resource edits remain inside the already granted envelope. Revocation is enforced before the next operation and closes affected reads; it need not wait for the Center to acknowledge. Disconnecting from a Center does not delete local data or kill local Runs.

Enrollment does not by itself grant host-shell execution. A remote Run start targets an existing Sandbox and uses Core's ordinary checks. A remote request never authorizes unconfined execution as a fallback when MXC or the requested backend combination is unavailable.

Remote Sandbox creation requires a separate locally issued provisioning grant. Its `scope_kind=provision` has no Sandbox ID and binds an immutable complete creation template and revision; the request names `provision_grant_id` and can only preserve or narrow that template. Core creates the child Sandbox and its Sandbox-scoped grant within the same authority boundary. Ordinary `scope_kind=sandbox` grants require a Sandbox ID. Only local `SetRemoteGrant` creates or expands either kind; the Center's account/session/subscription can never mint local creation authority.

## 4. Entitlement model

Retain the deterministic Go resolver, immutable grant/revocation/service-term records, revision fence, derived snapshot and current-definition version. The existing resolver's C# parity vectors are historical regression evidence and useful inputs; they do not require shipping the C# Center. The V2 resolver retains only business branches needed by hosted management and historical record decoding.

Canonical service keys:

| Key | Meaning | Checked by |
|---|---|---|
| `center.nodes` | Official hosted Node connectivity | Channel admission and periodic session/entitlement recheck |
| `remote.view` | Official hosted Sandbox/Run/resource/log view | Each remote read and bounded long-poll admission |
| `remote.control` | Official hosted Sandbox/Run/data/resource control | Each remote mutation after authorization and resource limits |

These are service availability keys, not permissions or preset prices. A subscription catalog can include all three as one hosted service; the local remote grant remains decisive for every action. Remove `center.mcp`, push/mobile products, task-submission `center.execute` and AI/storage-credit products from active V2 offers and route groups. Preserve their historical immutable records until their migration/retention policy permits compaction; never reinterpret an old key or enum value in place.

In self-hosted mode, the built-in feature configuration enables V2 self-hostable service keys minus explicit operator limits. It does not read or refresh an official entitlement store, require an official token, or call an official endpoint. Unknown mode or feature configuration is rejected. In official mode a missing/invalid catalog grants nothing; failures to read the entitlement store are reported as service unavailable, not “subscription expired.”

The Center checks entitlement at operation admission and at bounded channel/subscription rechecks. A loss of hosted entitlement denies future remote service and closes the channel/streams as specified, while Sandbox Core continues local work. No remote response is allowed to contain a local “license enforcement” stop command.

## 5. Hosted commerce scope

The earlier design selected Paddle for web sales. Retain that provider choice for the first official web subscription adapter; verify and pin the official provider API/webhook version during `AFV2-HOST-02`. Google Play and mobile purchase flows exit the V2 plan. Do not port AI credits, consumption settlement, storage add-ons or the large legacy commerce model simply because contract/schema placeholders exist.

The current C# `CommerceModule` is a 15-line module boundary, and there is no Go commerce package at the audited baseline. What can be reused is contract vocabulary, entitlement rules, persistence/idempotency/audit machinery and deployment controls. Billing provider behavior must be implemented and tested, not described as an existing completed service.

The minimal official module owns:

- Versioned catalog references and a `sales_open` gate; no hardcoded price amounts in application code.
- Provider customer/subscription associations scoped to one account.
- Purchase intent and checkout attempt with stable idempotency; redirect allowlist; checkout expiration.
- Signed provider webhook admission, bounded raw-body verification, unique event receipt, processing result and retryable recovery.
- Canonical subscription state, paid-through/service-term boundaries, cancellation/renewal state, failed-payment and refund adjustment facts.
- Billing history and provider-hosted management links; no raw payment-card storage.
- Entitlement transition/outbox/audit in a transaction; reconciliation against provider state after an uncertain/out-of-order notification.

Keep the provider adapter thin and explicit. No generic payment plugin marketplace is introduced. Provider secrets stay in deployment secret storage; browsers receive only short-lived approved checkout/portal URLs. An unsigned webhook, wrong environment/product/customer, duplicate event with changed payload or unverifiable account binding changes no entitlement.

## 6. Subscription and purchase state

| Canonical state | Availability decision | UI and recovery |
|---|---|---|
| `NOT_CONFIGURED` | No hosted sale or entitlement derived from a placeholder catalog | Explain service setup; local/self-host use stays available |
| `PENDING` | No entitlement merely because checkout was opened or returned | Show pending; query server; verified provider completion settles it |
| `ACTIVE` | Grant catalog keys during the verified service term | Show valid-until and renewal state |
| `CANCEL_AT_TERM_END` | Keep keys through verified paid-through time | Show cancellation date; provider-confirmed reactivation only |
| `PAYMENT_GRACE` | Follow the versioned catalog's explicit grace policy; never invent a trial/grace duration | Show payment remediation and exact service deadline |
| `EXPIRED` / `REVOKED` | Deny hosted keys after effective boundary | Keep billing/security remediation available; local Runs remain active |
| `PROVIDER_UNKNOWN` | Preserve the last verified service facts until their actual end; do not create a new paid term | Show verification pending; bounded server reconciliation |

The catalog and provider adapter define how provider statuses map into these states. Canonical state is derived from verified facts and effective times. Event arrival order alone does not decide the latest subscription state. An older event must not re-enable a canceled/refunded service or shorten a newer verified paid term incorrectly; where provider event/version data cannot establish order, query authoritative provider state and record the reconciled version.

A checkout redirect is never payment proof. Repeated purchase intent uses the same idempotency key. A timeout after provider submission remains pending/unknown until reconciliation, rather than creating a second subscription. Provider callbacks are at-least-once; each event identity is bound to its digest before applying a transaction. Duplicate processing returns the recorded effect. Canonical entitlement grants name provider period/event identity so duplicate events cannot issue a second term.

Cancellation changes renewal, not local process state. Full or partial refunds and chargebacks use documented provider facts and the versioned product policy; monetary policy and customer-facing promises require owner-approved texts before sales open. Implement the receipt and reconciliation paths with fixture commercial data while those production parameters are absent.

## 7. Historical entitlements and account data

Do not update historical grant rows to change their meaning. A legacy-to-V2 entitlement migration appends explicit migration facts naming original grant/term, new catalog definition, validity interval and migration version. It must not increase the paid-through date, grant value or local remote authority silently. Unknown legacy product/credit/storage records are preserved for review, not converted into a new local restriction or silently discarded.

Enrollment and account IDs retain their identity where the qualified migration permits it. V1 keys/credentials are rotated or fenced at the protocol cutover; an already connected V1 Node cannot exercise V2 routes. A new Center enrollment receives a new grant and protocol epoch, so old signed operations cannot be replayed across the boundary.

Account deletion/recovery must handle sessions, Node enrollments, provider subscription associations, unresolved mutations and retained audit/financial records explicitly. Revocation severs remote authority immediately; local Sandbox data belongs to its local owner and is not remotely wiped by deleting a cloud account. Required financial retention and legal erasure exceptions are production policy inputs. Missing legal text blocks activation of the relevant user-facing operation, not completion of unrelated local or self-host features.

## 8. Operating controls and self-host package

`AFV2-HOST-01` provides the Go binary/container, static Blazor bundle, PostgreSQL migration/backup/restore procedures, TLS reverse-proxy example, explicit mode/base URL, owner bootstrap, signing-key generation and documented upgrade/cutover. Self-host configuration has no official plan, checkout, issuer or payment-provider prerequisite. Administrators supply their own email provider if email sign-in is enabled; passkey/bootstrap flows state their prerequisites honestly.

`AFV2-HOST-02` adds official catalog/provider configuration, hosted service-key enforcement, meterable connection/traffic/storage budgets, minimal health/alert/runbooks, billing audit and dark-to-live release gates. Retain existing sealed-candidate promotion: build once, verify exact bytes, migrate with a separate role, promote through repository scripts. A continuously connected Node keeps its official Container active; capacity/cost acceptance must account for that rather than assuming idle sleep always bounds cost.

The current singleton hub, bounded queues and PostgreSQL connection pool remain structural limits. Operational degradation can reject new connections/calls and close hosted channels under an explicit reason; it never reaches local Run control. No price or commercial allowance is inferred from technical queue/frame bounds.

Production-only inputs include seller configuration, product/price references, legal texts, domain/TLS, sending provider, signing-key custody, database backup retention and approved operating budget. Record each missing item with its owner and activation gate. The V2 delivery plan must still implement and verify all behavior that can be exercised with isolated real stores and clearly labeled test provider boundaries.

## 9. Verification

Preserve native host verification and independent review. Test identity and role boundaries, real PostgreSQL concurrent receipt/grant writes, deterministic snapshot rebuild, expired terms, clock boundaries, out-of-order and duplicate provider notifications, repeated checkout/cancel commands, revocation, key rotation, subscription lapse during remote reads, and official catalog failure. Explicitly prove that local CLI operation succeeds without login/Center and after official subscription lapse, and that self-hosted remote use never contacts or depends on official billing.

Provider sandbox tests and browser/device tests are explicit local acceptance or recorded external prerequisites, not silently substituted by unit mocks. Test credential verification and business persistence with their real code. No live purchase, refund, production migration or public activation is performed by this Design/Plan migration.
