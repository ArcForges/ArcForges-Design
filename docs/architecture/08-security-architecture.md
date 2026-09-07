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
| **Workspace / Organization** | Tenancy and resource boundary | Cloud Workspace module |
| **Device** | A registered machine | Cloud Devices module |
| **App Installation** | One installed product on one device | Cloud Devices module |
| **App Instance** | One running process | Local Hub |
| **Local OS User** | The local IPC security principal | The operating system |
| **Local Profile** | The signed-out local operator | The local machine only |
| **Agent Actor** | Acting on behalf of a user session | Never an independent principal |
| **Service Principal** | A workspace-scoped non-human identity | Cloud Identity module |
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
| DG-03 | **An automation runs as its creator with re-evaluated permissions, or as an explicit service principal** ([SP-05](../requirements/07-security-privacy-and-trust.md#rule-sp-05) there) — never on a frozen permission snapshot ([SP-06](../requirements/07-security-privacy-and-trust.md#rule-sp-06) there). |
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
| <a id="rule-ta-03"></a>TA-03 | **Marking capability is therefore designed into the native format and the artifact model**, and reaches execution artifacts and generated media output (`TA-03` there). |
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

| Source | Consumed as |
|---|---|
| `I4 §Stage 26` | Principals, actor chain, permission and authorization separation, risk, approval, secrets, egress, instruction provenance, leases, trust, the decision pipeline and audit |
| `I4 §Stage 11` | Privacy obligations and AI transparency |
| `I4 §Stage 10 §113–119` | Operator surface separation, break-glass, webhook ingress, SSRF protection |
| `I3 §20`, `§18.4` | Identity layering, local authentication, secret storage, web security |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | Licence boundary enforcement as a security-adjacent control |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Remote authority: cloud never reaches local; the desktop re-authorises |
| **[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)** | Web origin, cookie, CSP, CSRF and CORS boundaries |
| **[V-01](../assurance/phase-1-official-verification.md#rule-v-01)** | AI transparency obligations and the marking gate |
| **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** | Store-policy prohibitions relevant to mobile unlock paths |
