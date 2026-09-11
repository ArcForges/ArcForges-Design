# Security Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** (remote authority model), **[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)** (web origin boundaries), **[V-01](../assurance/phase-1-official-verification.md#rule-v-01)** (AI transparency)
> Companions: [`../requirements/07-security-privacy-and-trust.md`](../requirements/07-security-privacy-and-trust.md), [`03-local-ipc-and-process-model.md`](03-local-ipc-and-process-model.md), [`05-cloud-architecture.md`](05-cloud-architecture.md)

The requirements define **what** must hold. This document defines **where** it is enforced and **how** the pieces fit.

---

## 1. Identity layering

| Layer | Scope | Authority |
|---|---|---|
| **Realm** | A deployment's identity and data authority | Itself |
| **Cloud User** | An account within a realm | Cloud Identity module |
| **Workspace** | Single-owner tenancy, data, device, billing and sync boundary | Cloud Workspace module |
| **Device** | A registered machine | Cloud Devices module |
| **App Installation** | One installed product on one device | Cloud Devices module |
| **App Instance** | One running process | Local Hub |
| **Local OS User** | The local IPC security principal | The operating system |
| **Local Profile** | The signed-out local operator | The local machine only |
| **Agent Actor** | Acting on behalf of a user session | Never an independent principal |
| **Deployment service identity** | Explicitly provisioned internal process identity; no independent customer authority | Deployment security boundary; product work still requires the Workspace owner chain |
| **Operator Principal** | Support, operations, trust & safety, security | **A separate identity system** |

| # | Rule |
|---|---|
| IL-01 | **Identity is `Realm + UserId`.** A bare user identifier is never globally meaningful ([ID-10](../requirements/02-identity-account-and-workspace.md#rule-id-10) in the identity requirements). |
| IL-02 | **Operator identity is not customer identity** ([SC-04](../requirements/products/arcforges-cloud.md#rule-sc-04) in the cloud product requirements). |
| IL-03 | **A local profile has no server representation** ([ID-02](../requirements/02-identity-account-and-workspace.md#rule-id-02)–[ID-03](../requirements/02-identity-account-and-workspace.md#rule-id-03) there). |

---

## 2. Enforcement points

Authorization is enforced at **four** points, and each is mandatory.

```
1. Caller-side pre-check         ArcChat / companion / client
      ↓                           user experience and early failure — never authority
2. Transport boundary            local IPC handshake, or cloud authentication
      ↓                           who is connected, at all
3. Service-side decision         Cloud module, or the Hub for local coordination
      ↓                           the substantive decision for cloud operations
4. Owner-side final validation   the product that owns the resource
                                  ALWAYS — the last word
```

| # | Rule |
|---|---|
| EP-01 | **Point 4 is never skipped** ([DP-02](../requirements/07-security-privacy-and-trust.md#rule-dp-02) in the security requirements). Points 1–3 may execute in ArcChat, the Hub or Cloud; the owner validates again at execution. |
| EP-02 | **A caller-side check is a user-experience optimisation only.** A client-asserted entitlement or permission is never trusted ([ES-06](../requirements/04-commerce-entitlement-and-credits.md#rule-es-06) in the commerce requirements, [RX-10](../requirements/03-cloud-services-and-sync.md#rule-rx-10) in the cloud requirements). |
| EP-03 | **Workspace scoping is enforced in the data access layer**, so a missing filter is structurally impossible rather than a review finding ([MT-03](05-cloud-architecture.md#rule-mt-03) in the cloud architecture). |
| EP-04 | **The security decision pipeline runs in the stated order** (`§11` of the security requirements), and each step's outcome is recorded for explanation and audit. |

---

## 3. Authentication

### 3.1 Cloud

| # | Rule |
|---|---|
| AU-01 | **Standard OIDC/OAuth 2.1 semantics** with the framework's authentication and authorization stack. |
| AU-02 | **Native/mobile bearer access tokens are short-lived with rotating revocable refresh tokens.** Browser authentication uses server-held opaque-cookie sessions with idle/absolute expiry and live revocation under [Web session architecture](10-web-architecture.md#5-browser-session-architecture--p2-003-resolved). |
| AU-03 | **Audience, issuer, tenant, device and scope are all validated.** |
| AU-04 | **Endpoints use policy-based authorization**; **resource-level authorization is re-validated in the application service**, never resting on a route or hub attribute alone. |
| AU-05 | **Realtime connections and hub methods use the same identity model and explicit authorization.** |
| AU-06 | **Administrative capabilities are entirely separate from ordinary user capabilities.** |
| AU-07 | **Authorization headers and query tokens never appear in logs.** |
| AU-08 | **Passkey is the primary daily method; email one-time codes perform first verification and recovery** (`§2.2` of the identity requirements). |
| AU-09 | **Step-up re-authentication is required for the enumerated sensitive operations** (`§6` there), and cannot be satisfied by an already-open session or by a biometric device unlock ([I-278](../requirements/01-normative-glossary-and-invariants.md#rule-i-278)). |

### 3.2 Local

| # | Rule |
|---|---|
| AL-01 | **Operating-system permissions restrict access first**: pipe ACLs, socket permissions, a private runtime directory. |
| AL-02 | **A session handshake completes immediately after connection**, issuing a short-lived token binding `AppId`, `InstanceId`, endpoint, build identity, contract set and expiry. |
| AL-03 | **The endpoint manifest carries no secret** ([EM-01](03-local-ipc-and-process-model.md#rule-em-01) in the local IPC architecture). |
| AL-04 | **Every call carries actor, scope and correlation.** |
| AL-05 | **Being local grants nothing automatically** ([SC-07](03-local-ipc-and-process-model.md#rule-sc-07) there). |

---

## 4. Authorization model

```
Principal
  └── Permission Grant  →  Capability + Resource Scope + Constraints + Lifetime
                                    ↓
                          Resource Authorization (owner)
                                    ↓
                          Effective Risk (baseline + modifiers)
                                    ↓
                          Approval / Step-up / Local Presence requirement
                                    ↓
                          Execute · record effect certainty · write audit
```

| # | Rule |
|---|---|
| AZ-01 | **Capability permission and resource authorization are separate decisions** ([I-238](../requirements/01-normative-glossary-and-invariants.md#rule-i-238)). |
| AZ-02 | **The Hub is not a universal ACL database** ([PM-05](../requirements/07-security-privacy-and-trust.md#rule-pm-05) in the security requirements). Professional resource rules stay with their owner. |
| AZ-03 | **Role is an assignment convenience, not the model** ([I-237](../requirements/01-normative-glossary-and-invariants.md#rule-i-237)). |
| AZ-04 | **Effective risk is computed per invocation** from the capability baseline plus runtime modifiers, and may only be raised by third-party metadata ([RK-02](../requirements/07-security-privacy-and-trust.md#rule-rk-02), [RK-03](../requirements/07-security-privacy-and-trust.md#rule-rk-03) there). |
| AZ-05 | **Permission cache is optimisation only**; revocation invalidates it ([PM-12](../requirements/07-security-privacy-and-trust.md#rule-pm-12) there). |
| AZ-06 | **Re-authorization occurs at every security boundary of a long task, and at every automation trigger** ([RA-01](../requirements/07-security-privacy-and-trust.md#rule-ra-01)–[RA-03](../requirements/07-security-privacy-and-trust.md#rule-ra-03) there). |
| AZ-07 | **An entitlement gate is evaluated separately and never deposited into permission** ([DP-01](../requirements/07-security-privacy-and-trust.md#rule-dp-01) there). |

---

## 5. Approval architecture

| # | Rule |
|---|---|
| AP-01 | **An approval is a durable object**, so it survives an application restart, a device change and a missed notification ([AD-04](../requirements/07-security-privacy-and-trust.md#rule-ad-04) in the security requirements). |
| <a id="rule-ap-02"></a>AP-02 | **The approval binds an action snapshot** including the target resource revision and a **parameter digest**, so a materially changed action requires a new approval ([AP-04](../requirements/07-security-privacy-and-trust.md#rule-ap-04) there). |
| AP-03 | **An approval may issue a transient, task-scoped grant** that expires with the task and never becomes durable ([AP-09](../requirements/07-security-privacy-and-trust.md#rule-ap-09) there). |
| AP-04 | **Approval state machine**: `Requested → Presented → Approved \| Denied \| Expired → Executed \| Failed`. |
| AP-05 | **Delivery is never authority** ([AD-01](../requirements/07-security-privacy-and-trust.md#rule-ad-01), [AD-02](../requirements/07-security-privacy-and-trust.md#rule-ad-02) there). A push action or a deep link opens the approval surface. |
| AP-06 | **Local presence is a device-verified attribute**, not a claim carried in a request ([LP-01](../requirements/07-security-privacy-and-trust.md#rule-lp-01)–[LP-04](../requirements/07-security-privacy-and-trust.md#rule-lp-04) there). |

---

## 6. Secret architecture

```
Business data           →  SecretRef only
                              │
                        Secret Broker
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  Perform the         Issue a short-lived     Reveal (rare,
  credentialed        scoped credential       step-up, audited)
  operation           to a scoped consumer
```

| # | Rule |
|---|---|
| SE-01 | **A secret value never appears in a DTO, a task payload, a settings blob, a log, a trace, an audit record, telemetry or an AI context** (`SE-01` there). |
| SE-02 | **`Use` and `Reveal` are separate permissions** ([I-257](../requirements/01-normative-glossary-and-invariants.md#rule-i-257)); most functionality needs use without reveal. |
| SE-03 | **Local secrets use platform secure storage** — the platform credential store, keychain or keystore. |
| SE-04 | **Cloud secrets use a managed vault** with secret-manager or Docker-secret injection ([DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15)). **There are no user provider secrets to store** — end-user BYOK is excluded in every form ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [I-015](../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired). Provider credentials belong to the deployment operator, never to a customer, and never appear in the policy file, the image, the logs or the public sample. Envelope encryption remains for per-workspace data keys wrapped by vault-held key-encryption keys ([SC-03](../requirements/products/arcforges-cloud.md#rule-sc-03) in the cloud product requirements). |
| SE-05 | **Workspace and personal secret scopes are a hard boundary** ([SE-08](../requirements/07-security-privacy-and-trust.md#rule-se-08) in the security requirements). |
| SE-06 | **Rotation does not change the business configuration identity** ([SE-09](../requirements/07-security-privacy-and-trust.md#rule-se-09) there). |
| SE-07 | **Revocation is immediate**: the credential becomes unobtainable at once, and dependents enter Needs Attention ([RA-06](../requirements/07-security-privacy-and-trust.md#rule-ra-06) there). |
| SE-08 | **An extension receives only its granted secret, brokered by default** ([SE-06](../requirements/07-security-privacy-and-trust.md#rule-se-06), [SE-07](../requirements/07-security-privacy-and-trust.md#rule-se-07) there). |
| SE-09 | **A model never sees secret plaintext** ([SE-03](../requirements/07-security-privacy-and-trust.md#rule-se-03) there). |

---

## 7. Data egress control

```
Read permission ──✗── does not imply ──✗── Egress permission

Egress decision inputs:
  content classification · knowledge policy (AI eligibility) · destination identity
  · destination class (cloud AI provider | connector | third-party | public)
  · workspace policy · actor permission · effective risk
```

| # | Rule |
|---|---|
| EG-01 | **Egress is a separate authorization** ([I-254](../requirements/01-normative-glossary-and-invariants.md#rule-i-254)), evaluated per destination identity, not per destination category ([EG-05](../requirements/07-security-privacy-and-trust.md#rule-eg-05) there). |
| EG-02 | **A cloud AI provider is a distinct egress destination class** with its own rules ([EG-04](../requirements/07-security-privacy-and-trust.md#rule-eg-04) there). There is no customer-provider destination, because no customer credential exists ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)). |
| EG-03 | **A package must not route user data to a publisher-controlled backend to evade network permission** ([EG-07](../requirements/07-security-privacy-and-trust.md#rule-eg-07) there). |
| EG-04 | **Every egress event is auditable and user-visible**: what content, to which destination, under which authorization, when ([UI-07](../requirements/07-security-privacy-and-trust.md#rule-ui-07) there). |
| EG-05 | **Knowledge retrieval policy does not replace permission** ([EG-03](../requirements/07-security-privacy-and-trust.md#rule-eg-03) there). Both must hold. |

---

## 8. Untrusted input boundaries

Every one of these is **data, never instruction**:

| Boundary | Content |
|---|---|
| Retrieved knowledge | Document text, capture data, media metadata |
| MCP | Tool descriptions, prompts, resource contents, server metadata |
| Connectors | Issue bodies, messages, documents, external records |
| Web | Page content, search results |
| Deep links | Externally originated navigation input |
| Imported packages | Manifests, format contents, embedded references |
| Extension output | Structured values returned across the extension boundary |
| Community packages | Skills, templates, workflows, metadata |

| # | Rule |
|---|---|
| UI-01 | **Instruction provenance is tracked for every item entering a model context** ([IN-01](../requirements/07-security-privacy-and-trust.md#rule-in-01) there). |
| UI-02 | **Instruction authority derives from provenance, never from text content** ([IN-04](../requirements/07-security-privacy-and-trust.md#rule-in-04) there). |
| UI-03 | **A parser treats its input as hostile**: bounded allocation, bounded decompression, rejected traversal, no contained code executed. |
| UI-04 | **Extension output is schema-validated before entering the product** ([EX-13](../requirements/08-extensions-and-developer-platform.md#rule-ex-13) in the extension requirements). |
| UI-05 | **A structured extension value cannot carry a CLR type, a runtime type name or a native pointer** ([DB-02](../requirements/08-extensions-and-developer-platform.md#rule-db-02) there). |

---

## 9. Delegation

```
Human Principal
   └── delegates to → Agent Actor          (never exceeds the delegator)
          └── invokes → Extension tool  under a bounded Capability Lease
                                              (task-scoped, time-bounded, non-amplifying)
```

| # | Rule |
|---|---|
| DG-01 | **Delegation narrows authority; it never amplifies it** ([I-266](../requirements/01-normative-glossary-and-invariants.md#rule-i-266)). |
| DG-02 | **A lease expires automatically with its task** ([CL-02](../requirements/07-security-privacy-and-trust.md#rule-cl-02) there). |
| DG-03 | **Automation acts for the single Workspace owner.** Current service eligibility, permissions and policy are re-evaluated at each trigger and protected invocation ([SP-05](../requirements/07-security-privacy-and-trust.md#rule-sp-05), [SP-06](../requirements/07-security-privacy-and-trust.md#rule-sp-06)). Internal deployment credentials authenticate the process and cannot bypass the owner chain; there is no customer-created service-principal alternative. |
| DG-04 | **The actor chain is carried end to end and never truncated at a process boundary** ([AC-02](../requirements/07-security-privacy-and-trust.md#rule-ac-02), [AC-03](../requirements/07-security-privacy-and-trust.md#rule-ac-03) there). |

---

## 10. Trust architecture

**Trust is typed, never a scalar** (`§9` of the security requirements).

| Type | Evaluated at |
|---|---|
| Publisher trust | Package installation and update |
| Package trust | Installation, update, and every start of an extension host |
| Software identity | Local RPC handshake and extension host handshake |
| Device trust | Cloud authentication and remote invocation |
| Extension trust state | Every extension invocation |

| # | Rule |
|---|---|
| TR-01 | **A signature proves origin and integrity, not safety** ([I-247](../requirements/01-normative-glossary-and-invariants.md#rule-i-247)). |
| TR-02 | **A trust upgrade never expands permission** ([TR-09](../requirements/07-security-privacy-and-trust.md#rule-tr-09) there). |
| TR-03 | **A permission-surface expansion in an update requires renewed consent** ([TR-08](../requirements/07-security-privacy-and-trust.md#rule-tr-08) there). |
| TR-04 | **Isolation is not authorization** ([I-259](../requirements/01-normative-glossary-and-invariants.md#rule-i-259)); **out-of-process is not automatically safe** ([I-260](../requirements/01-normative-glossary-and-invariants.md#rule-i-260)). |
| TR-05 | **A revoked package stops executing and deletes no user data** ([TR-06](../requirements/07-security-privacy-and-trust.md#rule-tr-06) there). |

---

## 11. Audit architecture

```
Security decision or high-value business effect
        ↓
Audit event  (append-only, owner-scoped)
        ↓
├── Product-local audit        product-owned security events
├── Cloud audit                cloud-side security events
└── Aggregated projection      a read model, never a second authority
```

| # | Rule |
|---|---|
| AD-01 | **Audit is not debug log, not telemetry, not domain revision history and not task operational trace** ([I-272](../requirements/01-normative-glossary-and-invariants.md#rule-i-272)–[I-275](../requirements/01-normative-glossary-and-invariants.md#rule-i-275)). |
| AD-02 | **Audit is append-oriented**; a revocation is a new event, never an edit ([AU-07](../requirements/07-security-privacy-and-trust.md#rule-au-07) there). |
| AD-03 | **Audit never stores secret plaintext or full sensitive content** ([AU-05](../requirements/07-security-privacy-and-trust.md#rule-au-05), [AU-06](../requirements/07-security-privacy-and-trust.md#rule-au-06) there). |
| AD-04 | **Local audit is not claimed tamper-proof** ([AU-08](../requirements/07-security-privacy-and-trust.md#rule-au-08) there). |
| AD-05 | **Audit ownership follows product ownership**; the aggregated view is a projection ([AU-09](../requirements/07-security-privacy-and-trust.md#rule-au-09) there). |
| AD-06 | **Audit has a stated retention policy** ([AU-11](../requirements/07-security-privacy-and-trust.md#rule-au-11) there). |
| AD-07 | **No operator can modify audit history** ([I-446](../requirements/01-normative-glossary-and-invariants.md#rule-i-446)). |

---

## 12. Web and browser security

| # | Rule |
|---|---|
| WB-01 | **HTTPS only, on every surface.** |
| <a id="rule-wb-02"></a>WB-02 | **Origins are isolated**: the account portal and the chat surface do not share authentication cookies, and **no broad parent-domain cookie exists** (**[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| WB-03 | **Per-origin host-only Secure/HttpOnly cookie sessions use the existing C# Cloud adapter**, with explicit Origin and antiforgery checks on every unsafe cookie operation including JSON/multipart and realtime negotiation; no parent-domain cookie. |
| <a id="rule-wb-04"></a>WB-04 | **No secret is compiled into the browser bundle.** |
| <a id="rule-wb-05"></a>WB-05 | **Browser JavaScript holds no access/refresh credential.** The HttpOnly opaque handle, server session state, exact-origin checks and CSRF rules are fixed by [P2-003](../decisions/phase-2-specification-decisions.md#rule-p2-003), now adopted; no token in Web Storage or URL. |
| <a id="rule-wb-06"></a>WB-06 | **Cross-origin policy is an explicit allowlist.** |
| <a id="rule-wb-07"></a>WB-07 | **Uploads are content-type-, size- and format-validated with a quarantine area, and are never executed server-side.** |
| <a id="rule-wb-08"></a>WB-08 | **Realtime transport logs redact tokens.** |
| WB-09 | **A web session is more conservative than a desktop session**, and a new browser does not immediately hold high-risk approval capability ([OF-07](../requirements/products/arcchat-mobile-and-web.md#rule-of-07), [OF-08](../requirements/products/arcchat-mobile-and-web.md#rule-of-08) in the companion requirements). |

---

## 13. Mobile security

| # | Rule |
|---|---|
| MB-01 | **Session material uses platform secure storage; sensitive tokens never enter ordinary preferences or logs.** |
| MB-02 | **App lock is UI access protection, not authentication** ([I-277](../requirements/01-normative-glossary-and-invariants.md#rule-i-277)), and biometric unlock never substitutes for step-up ([I-278](../requirements/01-normative-glossary-and-invariants.md#rule-i-278)). |
| MB-03 | **No provider credential exists on any client** ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)). There is no desktop-local secret to protect from mobile, because there is no desktop-local provider secret. |
| MB-04 | **A push action is not an authorization token** ([AD-01](../requirements/07-security-privacy-and-trust.md#rule-ad-01) in the security requirements). |
| MB-05 | **The Apache-2.0 boundary is enforced by dependency and architecture tests** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7). |

---

## 14. Network security

| # | Rule |
|---|---|
| NS-01 | **The API origin is not directly reachable from the public internet** ([NW-01](../requirements/products/arcforges-cloud.md#rule-nw-01) in the cloud product requirements). |
| NS-02 | **Edge WAF, targeted human verification and application rate limiting all exist**, and rate limiting is never IP-only ([NW-04](../requirements/products/arcforges-cloud.md#rule-nw-04)–[NW-06](../requirements/products/arcforges-cloud.md#rule-nw-06) there). |
| NS-03 | **A webhook endpoint verifies signatures, accepts fast, queues, and deduplicates**, and never treats the request as carrying authorization ([NW-09](../requirements/products/arcforges-cloud.md#rule-nw-09) there). |
| NS-04 | **Cloud task outbound traffic has SSRF protection**, including redirect re-validation and blocked internal and metadata addresses ([NW-10](../requirements/products/arcforges-cloud.md#rule-nw-10) there). |
| NS-05 | **The production database is never publicly reachable** ([NW-07](../requirements/products/arcforges-cloud.md#rule-nw-07) there). |

---

## 15. Native and process boundaries

The enforced mechanisms and RID-specific negative tests are in [Content and Extension Isolation](24-content-and-extension-isolation.md). Broker authorization and OS denial are both required; no same-user process is assumed capability-restricted merely because it uses RPC.

| # | Rule |
|---|---|
| NB-01 | **A native library never owns an ArcForges domain** (Technical Exception C in `§8.1` of the product scope). |
| NB-02 | **Managed code validates every input before it crosses into native code** (`§12` of the native interop architecture). |
| NB-03 | **Untrusted third-party native plug-ins never enter a product's main process** ([EX-02](../requirements/08-extensions-and-developer-platform.md#rule-ex-02) in the extension requirements). |
| NB-04 | **Extension processes hold no product identity beyond what their grants confer**, and their process identity is bound to their package installation ([EX-12](../requirements/08-extensions-and-developer-platform.md#rule-ex-12) there). |

---

## 16. AI transparency enforcement ([V-01](../assurance/phase-1-official-verification.md#rule-v-01))

| # | Rule |
|---|---|
| TA-01 | **Every AI-interaction surface carries an explicit disclosure** (`TA-01` in the security requirements). |
| <a id="rule-ta-02"></a>TA-02 | **Machine-readable marking is applied at the point of generation**, which makes it a property of the generation pipeline and the artifact format — not a user-interface concern (`TA-02` there). |
| <a id="rule-ta-03"></a>TA-03 | **The [content-origin profile](../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier contract](../requirements/13-data-formats-and-portability.md#content-origin-carriers) define applicability, propagation, durable representation and fail-closed publication in the native format and artifact model**, and reaches execution artifacts and generated media output (`TA-03` there). |
| TA-04 | **A gate before first EU market availability records the compliance route and the per-artifact-type marking mechanism.** *Owner: Security/Privacy Owner; Product Owner approves.* |

---

## 17. Threat model summary

| Threat | Primary control |
|---|---|
| Prompt injection through retrieved or connector content | Instruction provenance; retrieved content is never instruction (`§8`) |
| Capability escalation through an agent | Agents never exceed the delegator; owner-side final authorization; typed capabilities only |
| Escalation through an extension | Out-of-process, capability-scoped, schema-validated, brokered secrets, bound identity |
| Confused deputy across products | Actor chain carried end to end; owner re-authorises with the real actor, not the caller |
| Cross-tenant access | Workspace scoping in the data layer; index partitioning; identifier knowledge grants nothing |
| Credential exfiltration | `SecretRef` only in business data; brokered use; no plaintext to models, logs, traces or audit |
| Data exfiltration through AI | Egress as a separate authorization; destination identity; knowledge policy; egress audit |
| Stolen device | Device revocation; short-lived tokens; local presence for high-risk operations; honest statement that already-downloaded data is not remotely erasable (`§10` of the distribution requirements) |
| Replay and duplication | `CommandId` idempotency; provider event `eventId` deduplication; sync `ChangeId` deduplication |
| Malicious import package | Untrusted parsing; bounded decompression; rejected traversal; no execution |
| Malicious community package | Typed trust; declared permissions; consent on expansion; revocation; quarantine |
| Compromised publisher | Containment; version revocation; a contaminated version number never reused |
| Supply chain | Locked restore, SBOM, provenance attestation, signature verification, dependency and secret scanning |
| Operator abuse | Separate operator identity; purpose binding; no global search; no arbitrary SQL; dual approval for break-glass; immutable audit |
| Billing fraud | Signature-verified webhooks, idempotency, reconciliation, spend-velocity limits on new accounts, credit refund holds |
| Cost exhaustion | Reservation before execution, hard stop at zero, task and automation budgets, storm caps, autoscale caps |

---

## 18. Traceability

| Current document | Relationship |
|---|---|
| [Security, Permission, Privacy and Trust Requirements](../requirements/07-security-privacy-and-trust.md) | Owns the security, privacy, trust, permission and audit obligations |
| [Identity, Account, Device, Session and Workspace Requirements](../requirements/02-identity-account-and-workspace.md) | Owns identity, sessions, devices and realm isolation |
| [Content and Extension Isolation](24-content-and-extension-isolation.md) | Defines the process and OS enforcement profiles |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | Licence boundary enforcement as a security-adjacent control |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Remote authority: cloud never reaches local; the desktop re-authorises |
| **[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)** | Web origin, cookie, CSP, CSRF and CORS boundaries |
| **[V-01](../assurance/phase-1-official-verification.md#rule-v-01)** | AI transparency obligations and the marking gate |
| **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** | Store-policy prohibitions relevant to mobile unlock paths |

## P2-009 Cloud, CF and operator authentication composition

[The selected session profile](21-platform-and-dependency-matrix.md#7-selected-p2-009-runtime-and-dependency-closure) owns session shapes; [the CF contract](contracts/05-cloudflare-integration.md) owns HMAC service authentication, origin routing, per-frame/range authorization, fencing and revoke/cancel ordering. Browser Account/Chat origins are independent exact allowlist entries, /rpc and /session go C#, /ai/v1 and /objects/v1 go Worker under the same visible origin. No general token in JavaScript or URL. C# admission derives owner/actor/workspace from session, not CF/client assertions; every tool owner rechecks current grants and local presence. Service key IDs are direction-specific, rotate with15min overlap, signed timestamp skew60s and nonce120s, not ambient Cloudflare account tokens.

A frame/range already authorized before revocation is an in-flight read; subsequent delivery authorizes again and fails closed if C# is unreachable. This is the concrete interpretation of immediate revocation, not a ten-minute presigned URL authority leak. R2 tickets use a session-bound facade precisely because [RS-02](contracts/01-public-api-operations.md#rule-rs-02) requires consumption-time checks. Logs expose only operation/correlation/run/attempt IDs, receipt hashes and bounded reasons; no prompt/output/cookie/secret/absolute local path. Existing content-origin and source-authorization profile survives all protocol projections.

[Selected AOT session/WebAuthn implementation](21-platform-and-dependency-matrix.md#7-selected-p2-009-runtime-and-dependency-closure) fixes credential/hash/CSRF policy and operator identity. The [CF/private port contract](contracts/05-cloudflare-integration.md#2-http-framing-and-authentication) binds direction, audience, realm, timestamp, nonce, request hash, session and current permission. Enforce generated field bounds before domain dispatch. Operator identity/dual control remains separate from customer sessions, as specified in the [operator schema](contracts/04-protobuf-wire-registry.md#9-operator-control-and-separate-identity-boundary).

## Account and provider closure

**Profile and email.** Profile updates accept only the five required profile fields; avatar must be an owned verified image resource. Email change requires fresh step-up and a 10-minute code sent to the new address, at most five attempts. Completion atomically verifies the new unique address, switches the primary/email identity and schedules mandatory notifications to both old and new addresses. It never changes UserId/billing identity or merges another user. Last-credential and recovery-path checks apply before removal. Credential rename changes its label only.

**Recovery and sessions.** Store hashes of ten independent 128-bit recovery codes; consume a code atomically, invalidate the remaining set on successful account recovery and revoke all sessions/PAT/SSO grants. Issuing a replacement set invalidates its predecessor; plaintext is shown once. Native refresh uses single-flight rotation per installation. Move the old hash into spent_refresh before replacing it in the same transaction. A spent token identifies and revokes its family. Lost rotation acknowledgement requires fresh authentication; no transparent retry with the old token. Session listing is per-app/device; app logout affects one session, device sign-out affects all sessions and SSO grants of that device while retaining registration/trust/local data, device revocation also removes trust/remote access, and everywhere sign-out includes the caller. Current user/device/generation denial is checked on every PAT/session use.

**PAT.** Creation displays a 256-bit random secret once and stores its hash. Required expiry is no more than 365 days, scopes are an explicit registered capability subset and one owned workspace. A duplicate create command returns summary only. Default scopes are empty and unusable. PAT cannot manage authentication, mint other credentials, step up, expand remote authority or purchase/authorize extra usage. Normal capability, service-term, budget and owner checks still apply, and actor/audit records distinguish the token caller from a direct user action. Revocation is effective at the next authorization check.

**Device SSO.** Shared DesktopPlatform security infrastructure offers Continue as the account name only after the user selects it. Any installed Arc app can host the bootstrap; ArcChat is unnecessary. The requesting signed app is verified by OS peer identity, binds its installation/product to a server 60-second challenge and obtains a signature from the authorized device key through the source app's protected broker. Cloud atomically consumes that challenge, verifies current source session/device/generation and creates a distinct target-app session. Neither access nor refresh tokens are copied between apps. Source logout, device sign-out or revocation invalidates outstanding challenges. With no eligible source app, use ordinary login.

**Remote policy.** allowedCapabilities defaults empty. Effective permission is its intersection with registered capability scope, current owner grants, trust, remoteEnabled, application consent and required local approval. Removing scope cancels future delivery; an in-flight uncertain effect remains reconciled. No remote policy admits R4 by default.

**Deletion.** Fresh login with purpose=cancelDeletion for a pending-deletion account issues only a 15-minute restricted session, allowing getAccountDeletion/cancelAccountDeletion/logout. It never re-enables normal APIs, data download, device trust or paid execution. Purged/expired grace refuses. Workspace-only data deletion first previews current acknowledged content and pending exports; request binds the exact preview hash and revision. Preview returns bounded kind/count/byte totals and a 15-minute server manifest hash. Every content writer takes the workspace admission fence in shared mode; deletion takes it exclusively, drains in-flight commits, validates the full current root/revision set against the preview and refuses if changed before setting the durable purge fence. New writes then fail until reopening; no unbounded affected-root list crosses RPC. It disables sync/AI writes for that purge, fences jobs/grants, executes owner tombstones and purge/reference-release jobs, then reopens an empty workspace after completion. Identity, independent local content, subscriptions and retained commercial/security evidence remain. Old pending sync content is quarantined for explicit re-import, not silently restored.

**Self-host authentication.** A realm advertises only enabled configured providers; the official provider set remains email/passkey. Self-host additionally supports local password and generic OIDC (including an enterprise IdP speaking OIDC). Identity keys are realm/provider/subject, never matched by email. The operator configures enrollment: public email verification or issuer-allowlisted OIDC enrollment, or a single-use 15-minute local enrollment code created by the self-host administrator CLI for passkey/password setup. This is account provisioning, not a workspace invitation/membership feature. The CLI uses the same audited Identity application service. It prints a random code once, stores its hash and cannot read/change existing credentials without an audited recovery request.

Password setup/change requires a fresh enrollment/recovery or step-up flow; use .NET IdentityV3 PasswordHasher with explicitly configured 210000 PBKDF2-HMAC-SHA512 iterations, per-credential salt and rehash-on-login for increased policy. Accept 15–128 Unicode scalars, block known compromised values through a locally maintained hash list, no network password disclosure or composition rules. Limit verification to five failed attempts per account per 15 minutes plus source/global admission limits; reset does not bypass those limits. Non-email recovery uses a registered passkey, recovery code or separately audited administrator reset grant; no security questions. Official Cloud exposes no password endpoint/provider.

OIDC uses authorization code + PKCE S256, server-bound state/nonce, exact configured issuer/client/audience/redirect and signature/expiry verification. C# completes the IdP callback and issues a 60-second single-use providerReceipt bound to the original browser/native flow; never deliver IdP tokens in an app URL or reuse them as ArcForges sessions. Browser callback retains a bound HttpOnly flow cookie; native callback carries only the flow completion receipt to the registered app callback. Existing account linking requires authentication of both identities under step-up, never matching email. Tokens and provider secrets remain in the C# secret boundary. The selected callback schema adds GET /session/v1/providers/{providerId}/callback with standard code/state and POST /session/v1/enrollment/complete with enrollmentCode, method, installation and passkey/password proof; native response shaping remains NativeSession, browser Set-Cookie/SessionView. Both consume one-use proofs atomically.

These are selected design mechanisms, with real AOT/authentication proof in WP06/22. Primary references: [Microsoft Identity configuration](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity-configuration?view=aspnetcore-10.0), [PasswordHasher implementation](https://source.dot.net/Microsoft.Extensions.Identity.Core/PasswordHasher.cs.html), [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html).
