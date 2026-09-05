# Distribution, Update, Support and Trust & Safety Requirements

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: **D-004** (mobile licensing boundary), **D-008** (runtime matrix), **D-022**/**V-09** (store posture)
> Companions: [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md), [`11-policy-and-configuration.md`](11-policy-and-configuration.md), [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md), [`../architecture/14-build-packaging-and-release.md`](../architecture/14-build-packaging-and-release.md)

Two halves of one lifecycle: how software reaches users, and what happens when something goes wrong afterwards.

---

# Part I — Distribution, release and update

## 1. Distribution posture

| # | Requirement |
|---|---|
| DS-01 | **Each product installs, versions, updates and releases independently** (`P-12`). |
| DS-02 | **The suite is an installation experience, not a packaging unit.** A "full suite" download may exist as a bootstrapper that installs the selected products; it must never become one giant monolithic installer. |
| DS-03 | **Open-source distribution and store distribution do not conflict.** The same signed artifact may be delivered through the official site and through a platform store. |
| DS-04 | **A source-hosting platform is a build and release automation platform, not the primary distribution channel.** Release artifacts and update feeds are served from ArcForges-controlled infrastructure. |
| DS-05 | **Release artifacts are immutable.** A published version's bytes never change. |
| DS-06 | **Clients never hard-code an object-storage URL.** They resolve through an ArcForges-owned update domain, so storage can move without breaking installed clients (**D-014**). |

### 1.1 Platform matrix

| Platform | Primary channel | Secondary | Notes |
|---|---|---|---|
| **Windows** | Signed installer from the official site, with a built-in update system | Platform store listing carrying the **same signed binary**; a package-manager manifest | Store distribution is distribution only, **never a commerce channel** (**D-022**) |
| **macOS** | Official site distribution, signed with a Developer ID, hardened runtime, notarised | — | A store route is deferred: it would force sandboxing that conflicts with professional local-file and device workflows |
| **Linux** | A single self-contained portable format as the first official format | Additional package formats later | **Do not maintain many packaging formats simultaneously in the first stage** |
| **Android** | The official app store, as an app bundle with platform app signing | A directly downloadable package may exist, and is not the primary channel | **D-022**: consumption-only, no in-app purchase |
| **iOS** | Architecture present, **build deferred** (**D-008**) | — | Release runtime re-verified against the then-current supported baseline before activation |

| # | Requirement |
|---|---|
| PL-01 | **All Windows executables and installers are signed and timestamped.** |
| PL-02 | **macOS artifacts are signed, hardened-runtime enabled and notarised**; Linux artifacts carry checksums and repository signing where a repository is used. |
| PL-03 | **A store listing must not become the update mechanism.** The product's own update system remains authoritative, so update behaviour is identical across channels. |
| PL-04 | **The signing identity and the brand identity are distinct concerns.** Where a signing certificate displays an individual name, the product surfaces and documentation must still present the product brand consistently, and the discrepancy must be anticipated rather than discovered at first release. |
| PL-05 | **Store developer accounts must be established under the intended long-term owning identity**, not casually under a personal account that later requires a brand transfer. |
| PL-06 | **Mobile provenance and the complete direct and transitive dependency closure are verified before the first mobile artifact is produced** — the **F-023** gate. *Owners: Release Engineering Owner and Licensing and Provenance Owner; Product Owner approves.* |
| PL-07 | **Store category fit and consumption-only conformance are confirmed before first submission** — the **V-09** gate. Apple's free-companion exemption is decided by review, not by reading the guideline. |

---

## 2. Release channels and versioning

Exactly three channels from day one:

| Channel | Audience | Distribution |
|---|---|---|
| **Stable** | Everyone | Site, store, package manager |
| **Beta** | Opt-in | Site only |
| **Nightly / Canary** | Internal and explicit opt-in | Build artifacts only; **never shipped to a platform store** |

| # | Requirement |
|---|---|
| RC-01 | **The channel is directly switchable by the user**, with the consequences stated — including that moving to a lower channel may require a data-compatibility check (`MG-09` in the data requirements). |
| RC-02 | **Versioning is semantic**, and version is not one number: the nine version axes in [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md) §14 apply. |
| RC-03 | **Every release produces a Release Record**: version, channel, build identity, commit, artifacts with hashes, signing and notarisation status, SBOM, compatibility manifest, minimum OS versions, minimum cloud version, release notes, and the quality report. |
| RC-04 | **Every release artifact is verifiable**: published hashes, signatures and attestations that a user or an auditor can check independently. |

---

## 3. Update

| # | Requirement |
|---|---|
| UP-01 | **An update never blocks launch.** The product starts; the update is discovered, downloaded and staged in the background, and applied at a safe moment. |
| UP-02 | **Delta updates are supported**, which matters most for large products such as ArcSlate. |
| UP-03 | **Before updating**, the product checks for running tasks and unsaved work, and defers rather than interrupting critical work (`LF-09`). |
| UP-04 | The update sequence is: download → verify signature and hash → stage → **switch atomically** → retain the previous launchable version. |
| UP-05 | **A failed update must never damage user data.** **An executable directory is never a user data directory.** |
| UP-06 | **Rollback is reserved and tested.** The previous version remains launchable, subject to data-compatibility rules. |
| UP-07 | **Uninstall does not delete user data by default**, and says so explicitly. |
| UP-08 | **Data migration is independent of the installer.** The sequence is installer update → application start → data compatibility check → migration, with its own recovery path (`SV-05` in the cloud requirements, `MG-05`–`MG-09` in the data requirements). Migration must consider rollback compatibility. |
| UP-09 | **A critical security update has an expedited path**, coordinated with the security advisory process (§14) and, where warranted, with a policy-level kill switch (`KS-05`) — noting that a kill switch reduces exposure but does not fix a local vulnerability. |
| UP-10 | **A bad version must be immediately haltable**: the update feed can stop offering it, and the compatibility policy can block it as a specific version range without blocking neighbouring versions (`CO-04`). |
| UP-11 | **A cloud minimum-version requirement must not be imposed before every channel has had a genuine opportunity to update**, with the grace period honoured (`CO-05`). |

---

## 4. Release domain model

```
ProductRelease · ReleaseVersion · ReleaseChannel · ReleaseStatus
Platform · Architecture · PackageFormat
ReleaseArtifact · DownloadArtifact · UpdateArtifact · PackageIdentity
SigningIdentity · SigningStatus · NotarizationStatus
ArtifactHash · ArtifactAttestation · SBOM
MinimumOSVersion · MinimumCloudVersion
UpdatePolicy · UpdateFeed
DistributionChannel · StoreSubmission · StoreSubmissionStatus
Rollout · ReleaseNote · CompatibilityRange
```

## 5. Release acceptance scenarios

Fresh install · install over an existing version · upgrade from the previous stable · upgrade across two versions · downgrade protection · rollback to the previous version · interrupted download · interrupted install · corrupted artifact rejected by hash or signature · update while a long task is running · update while documents are open · uninstall preserving user data · channel switch up and down · a blocked bad version refused by the feed and by policy · a store-delivered build updating through the product's own update system.

---

# Part II — Support, operations and Trust & Safety

## 6. Founding principles

| # | Principle |
|---|---|
| SP-01 | **Support is assistance, not impersonation** (`I-415`). |
| SP-02 | **An Operator is an Actor, not the User** (`I-416`). |
| SP-03 | **Recovery repairs data through product semantics, never through arbitrary database mutation** (`I-426`). |
| SP-04 | **Trust & Safety enforcement acts on distribution and access surfaces, never silently on a user's local canonical data** (`I-436`, `I-438`). |
| SP-05 | **Security emergency powers remain scoped, attributable and auditable.** |

---

## 7. Separating the operational objects

Nine distinct object types. **They must never all be called "ticket"** (`I-410`–`I-414`):

| Object | Definition |
|---|---|
| **Feedback** | An unsolicited comment or feature idea |
| **Bug Report** | A user's report that something is wrong |
| **Support Case** | A private, individual customer engagement |
| **Engineering Defect** | An internal, deduplicated engineering item |
| **Known Issue** | A published, acknowledged defect with a status |
| **Incident** | An operational event affecting multiple users or services |
| **Community Report** | A report about a public ecosystem object |
| **Security Report** | A private vulnerability disclosure |
| **Security Advisory** | A published, versioned security notice |

| # | Requirement |
|---|---|
| OB-01 | **Feedback ≠ Support Case** (`I-410`), **Bug Report ≠ Engineering Defect** (`I-411`), **Feature Request ≠ product commitment** (`I-412`), **Known Issue ≠ Incident** (`I-413`), **Incident ≠ Security Advisory** (`I-414`). |
| OB-02 | **One hundred bug reports may map to one engineering defect**, and closing the defect does not close the support cases — each user is answered. |
| OB-03 | **An internal engineering issue must not copy user-sensitive content.** It references, redacts and summarises. |
| OB-04 | **A bug fix status is bound to a real release.** "Fixed" is only user-visible once a release containing the fix exists on a channel the user can reach. |
| OB-05 | **A feature request never creates a false roadmap promise.** "Planned" may be shown only where it is true. |

### 7.1 In-product "Report a Problem"

| # | Requirement |
|---|---|
| RP-01 | One unified in-product entry point routes to the correct object type. |
| RP-02 | **A security issue is explicitly directed to the private security channel**, never to a public tracker. |
| RP-03 | **An in-product bug report is private by default.** Creating a public issue is an explicit, separate user choice. |
| RP-04 | **A diagnostic bundle is never uploaded automatically** (`I-424`). Each sensitive category — logs, configuration, redacted paths, content excerpts — is a separate explicit opt-in. |

---

## 8. Support case and support access

| # | Requirement |
|---|---|
| SC-01 | A support case is a **private customer object** with a unified state model, and its **history is never deleted**. |
| SC-02 | **A case must not be closed silently to improve a response-time metric.** |
| SC-03 | **Data existing in the cloud does not give support the right to browse it** (`I-447`). |
| SC-04 | Access requires an explicit **Support Access Grant** from the user, which is: minimal in scope by default, purpose-bound to a case, **time-limited and auto-expiring**, cancellable by the user at any time, and audited. |
| SC-05 | **Support Access ≠ User Session** (`I-418`) and **≠ permanent permission** (`I-419`). |
| SC-06 | **Silent impersonation is prohibited** (`I-415`, `I-420`). An operator can never become a user. |
| SC-07 | **Minting a user session for debugging is prohibited.** |
| SC-08 | **Every operator action uses the operator's own principal.** An action taken by support must never be recorded as if the user performed it. |
| SC-09 | **"View as user" is a Support Projection / Reproduction View**, not impersonation: a read-only rendering constructed under an explicit grant, clearly marked as such. |
| SC-10 | **Support must never ask a user for a secret**, and **never for a persistent remote-access credential**. Any remote support session is explicit, ephemeral, view-only by default, and separately authorised for any interaction. A remote support session must not expose secrets. |
| SC-11 | **Support attachments are support-domain data.** They never become ArcNotes, ArcChat or other product resources, they carry their own retention, and they are not copied into unrelated systems. |
| SC-12 | **Support data retention and product data retention are separate** (`BK-09` in the cloud requirements). |
| SC-13 | **Temporary access is revoked immediately when the case closes.** |
| SC-14 | **Sending a recovery package is data egress** and follows the egress authorization rules (`EG-02`), including workspace-administrator authorization where applicable. |
| SC-15 | **Support analytics use minimised data only.** |
| SC-16 | **Support priority may derive from a commercial plan; the privacy and permission model never does** (`I-417`). A higher plan buys faster attention, never broader access. |
| SC-17 | **Trust & Safety is not affected by payment level.** Paying does not exempt anyone from reporting; not paying does not warrant harsher enforcement. |

---

## 9. Break-glass

| # | Requirement |
|---|---|
| BG-01 | **Break-glass is not impersonation** (`I-420`) and **is not a global superuser** (`I-421`). It is a narrowly defined emergency operator action taken under the operator's own identity. |
| BG-02 | It requires: a declared reason, an incident or case reference, an explicit scope, **dual approval / four-eyes review**, a time limit, and an audit record. |
| BG-03 | **Break-glass must never accumulate into a general-purpose back office.** Each break-glass capability is individually defined and individually approved. |
| BG-04 | **The risk of a large-scale operator action automatically escalates**, requiring higher approval and dual control. |
| BG-05 | **An operator can never modify audit history** (`I-446`). |

---

## 10. Operator Console

**Operator Console = a controlled interface for support, operations, Trust & Safety and security management capabilities.**

| # | Requirement |
|---|---|
| OC-01 | **Operator Console ≠ Database Console** (`I-422`). **It provides no arbitrary SQL.** A production data problem is never solved by ad-hoc production SQL; where an exceptional data operation is unavoidable it is an individually defined, individually audited capability. |
| OC-02 | **Operator Console ≠ Domain Owner** (`I-423`). It does not own an ArcNotes document, an ArcScope session or an ArcSlate project. Changes go through the owning application's recovery capability. |
| OC-03 | **Roles are separated and least-privileged**: Customer Support Operator, Recovery Specialist, Operations Operator, Trust & Safety Operator, Security Operator. **No role holds all capabilities**, and an operations role does not become a customer-content role. |
| OC-04 | **Global content search is prohibited.** Access is purpose-bound. |
| OC-05 | **Every operator access requires a case or incident context.** Curiosity browsing is structurally impossible, not merely discouraged. |
| OC-06 | **Every high-value operator access is audited** with actor, purpose, scope, target and time. |
| OC-07 | **The operator dashboard shows only what operations requires** — never a general window into what users are creating. |
| OC-08 | **Trust & Safety operators do not gain access to all users' private cloud content** (`SC-03`). |

---

## 11. Data recovery

Four tiers, escalating only as far as necessary:

| Tier | Description |
|---|---|
| **0 — Self-service** | Version history, trash, local recovery, export — the user resolves it |
| **1 — Guided recovery** | Support guides the user through product capabilities; support touches nothing |
| **2 — Recovery Package** | The user generates and explicitly shares a package; ArcForges works on a copy |
| **3 — Cloud/product recovery operation** | An explicit recovery capability, under grant, through the owning application |

| # | Requirement |
|---|---|
| RV-01 | **A Recovery Package is not a Diagnostic Bundle** (`I-425`). It carries far more sensitive content, and therefore has stricter generation, sharing, handling and retention rules. |
| RV-02 | **Recovery preserves the original first.** The pattern is **preserve original → work on a copy → validate → produce a recovery result**. |
| RV-03 | **Recovered data must not silently overwrite normal data.** It arrives as an explicit, reviewable result. |
| RV-04 | **Every recovery operation retains provenance**, so "why did this data change?" is always answerable. |
| RV-05 | **Recovery is not guaranteed** (`I-428`). Support must never promise recovery of data that does not exist, and must say plainly when data cannot be recovered. |
| RV-06 | **Local-only data is not visible to cloud support.** There is no back-office route to read it. |
| RV-07 | **Self-hosted realm data is not accessible by default.** There is no secret backdoor; the self-host administrator provides diagnostics or a recovery package if they choose to. |
| RV-08 | **Projection repair ≠ canonical data repair** (`I-427`). Rebuilding a derived projection is lighter, and is still recorded. |
| RV-09 | **Staff must never quietly "fix" user data.** Every change carries recovery provenance. |
| RV-10 | **Recovery must not bypass user ownership.** It requires an explicit user recovery request or a proper legal or security process. |
| RV-11 | **Recovery-uploaded content has a defined lifecycle** and a shorter default retention after the case closes; security-incident evidence may require longer retention under a stated policy. |

---

## 12. Incidents

**Incident = an operational event affecting the normal operation of multiple users or services.**

| # | Requirement |
|---|---|
| IN-01 | **A single-user bug is not an incident** (`I-413`). |
| IN-02 | The incident lifecycle: detect → declare with severity → mitigate → resolve → post-incident review → published summary where users were affected. |
| IN-03 | **Support cases link to an incident**, so affected users are answered consistently and updated together. |
| IN-04 | **Incidents combine with the policy control plane**: an unavailable provider may be marked unavailable for new requests while the incident explains why and the product behaviour is legible (`PA-02`). |
| IN-05 | **A public status page is an operational surface** reporting per-capability state — Identity, Sync, Storage, Search, Remote, Tasks, Managed AI, Billing (`CL-03`) — and **never contains customer-specific private data**. |
| IN-06 | **A possible personal-data breach automatically escalates to the highest-severity legal and security incident class**, with the statutory notification clock treated as a hard operational deadline (§16.5 of the security requirements). |
| IN-07 | **SLO ≠ external SLA** (`I-403`). Internal objectives are not published commitments. |

---

## 13. Community reports and enforcement

| # | Requirement |
|---|---|
| CR-01 | **Community Report = a report about a public ecosystem object** — a package, a publisher, a public share. |
| CR-02 | **Every report has a specific target**, including a **version identity** where a package is concerned. |
| CR-03 | **Report ≠ Investigation ≠ Enforcement ≠ Appeal** (`I-429`). Four stages, four objects. |
| CR-04 | **Report count is not guilt** (`I-431`). A coordinated malicious report campaign must not be able to destroy a publisher. Permanent major enforcement requires controlled decision-making. |
| CR-05 | **Reporter identity is not disclosed to the reported party by default**, and enforcement notices must not leak it. |
| CR-06 | **An automated security scanner result is a signal, not a verdict.** |

### 13.1 Enforcement ladder

Escalating, always at **minimum necessary scope**:

```
Notice → Warning → Version-scoped delist → Package delist
      → Version-scoped revoke → Package revoke → Publisher suspension
```

| # | Requirement |
|---|---|
| EN-01 | **Enforcement scope is minimised.** A problem in one version is handled at that version, not across an entire publisher's catalogue. |
| EN-02 | **Delist ≠ Revoke** (`I-432`). Delist removes it from catalog discovery; revoke stops execution. |
| EN-03 | **Publisher Yank ≠ platform enforcement removal** (`I-433`). A publisher's own withdrawal is a different act with a different record. |
| EN-04 | **Package revocation prefers version scope** over destroying an entire package's history. |
| EN-05 | **A revoked package stops executing, including in the background.** |
| EN-06 | **Package revocation never deletes user project data** (`I-434`) and **never deletes resources created with it** (`I-435`). |
| EN-07 | **Extension private data is retained by default** — as evidence and as user property — with removal available as a separate, explicit act. |
| EN-08 | **A malicious package binary may be quarantined**; canonical product data is never deleted alongside it. |
| EN-09 | **Confirmed severe malware may be contained first and notified after**, with the investigation and notification continuing — an explicitly exceptional path with its own audit. |
| EN-10 | **A cryptographic compromise of a publisher account is an immediate containment case.** After recovery the publisher **may not reuse a contaminated version number**; a new version is required. |
| EN-11 | **The offline-device reality is stated honestly** (`DS-06` in the policy requirements): a revocation cannot reach a machine that never connects. The operating-system and update security perimeter remains necessary. |
| EN-12 | **Self-host revocation must never become an official hidden backdoor** (`I-443`). The official control plane cannot silently control an independent realm; it may publish information that the realm's administrator chooses to act on. |
| EN-13 | **Trust & Safety actions are as reversible as possible.** A false positive can be restored. |
| EN-14 | **Trust & Safety reason codes are stable and invariant.** The human-readable explanation is localised; **the enforcement semantics never differ by user language** (`I-770` analogue). |
| EN-15 | **A normal policy delisting must not create a security panic.** Delisting for a routine reason and delisting for a security reason are presented differently. |
| EN-16 | **Installed users receive a Needs Attention state** when a package they use is revoked (`CA-13`). |
| EN-17 | **The official catalog shows a package's security status.** |

### 13.2 Copyright and public content

| # | Requirement |
|---|---|
| CP-01 | **Copyright and intellectual-property reports follow an independent legal workflow**, separate from ordinary abuse. |
| CP-02 | **Copyright enforcement targets the distribution surface** — the catalog listing, the public share — **not a user's private local canonical data** (`I-436`). |
| CP-03 | **Public share removal does not delete the private source** (`I-437`). |
| CP-04 | **Private local data is not a community moderation surface** (`I-489` analogue). |
| CP-05 | **A community report does not expose private cloud data to a moderator** (`SC-03`, `OC-08`). |

### 13.3 Account enforcement

| # | Requirement |
|---|---|
| AE-01 | **Account enforcement is compatible with local-first.** Restricting or suspending a cloud account never locks local software or local data (`I-016`, §9 of the identity requirements). |
| AE-02 | **Cloud Account Restriction ≠ local data confiscation** (`I-438`). |

### 13.4 Appeal

| # | Requirement |
|---|---|
| AP-01 | **Appeal is a first-class object**: a request to re-examine a specific enforcement action. |
| AP-02 | **An appeal does not modify enforcement history** (`I-439`). The original action, the appeal and the outcome are all retained. |
| AP-03 | **Serious enforcement is reviewed as independently as practical**, by someone other than only the original decision-maker. |
| AP-04 | **A security revocation appeal is special**: a binary containing exploitable malware stays revoked permanently, regardless of who now controls the account. |
| AP-05 | **An enforcement notice is understandable** without revealing detection rules or the reporter's identity. |
| AP-06 | **An emergency security investigation may delay some notice**, under a formal security case with audit. |
| AP-07 | **Appeal must not become a harassment tool**, and a real review path must nonetheless exist. |

---

## 14. Security reports and advisories

| # | Requirement |
|---|---|
| SR-01 | **Security Report = a private vulnerability disclosure object**, with its own lifecycle: received → triaged → validated → fixed or contained → advisory published → credited. |
| SR-02 | **A security report is private by default** (`I-440`) and is never auto-published. |
| SR-03 | **Ordinary bugs and security reports convert both ways**: a bug found to be a vulnerability moves into the security case workflow, with its history preserved. |
| SR-04 | **Security Advisory = a versioned, published security notice**, exposed to users and administrators after validation. |
| SR-05 | **Security Advisory ≠ Incident** (`I-414`), **≠ Kill Switch** (`I-441`), **≠ Package Revocation** (`I-442`). An advisory communicates; a kill switch and a revocation enforce. |
| SR-06 | **An advisory has a stable identity and is versioned; history is never rewritten in place.** |
| SR-07 | **An advisory is connected to the update system**: it names the fixed versions and the upgrade path, so a user can act on it. |
| SR-08 | **A serious cloud vulnerability may be combined with a kill switch**, and an extension vulnerability with package revocation — as separate, coordinated acts. |
| SR-09 | **A security advisory must never prevent a user from accessing their own local data** in the name of security. |
| SR-10 | **A signed advisory feed is published**, so administrators and self-hosted realms can consume it. |
| SR-11 | **A self-hosted realm may subscribe to the official advisory feed. Subscribing must not hand control of self-host policy to the official cloud** (`I-443`). **Advisory is information, not remote policy authority.** |
| SR-12 | **A publisher-facing advisory path exists** for vulnerabilities in third-party packages. |

---

## 15. Operator security and audit

| # | Requirement |
|---|---|
| OA-01 | **Operator actions use the ordinary security model**: an operator is a human principal with capabilities, scope and risk, subject to approval and step-up like any other actor. |
| OA-02 | **Support audit and Trust & Safety audit are distinguished** by category, and both use the one unified audit vocabulary (`AU-02` in the security requirements). |
| OA-03 | **Users can see the important operator actions that relate to them**, in their own security activity. |
| OA-04 | **`Staff Access ≠ Secret Access`** (`I-444`). Operating access never implies access to secrets. |
| OA-05 | **`Support Attachment ≠ product resource authority`** (`I-445`). |
| OA-06 | **Feedback, diagnostics and recovery all respect workspace boundaries** (`WS-07` in the identity requirements). |

---

## 16. Operational identity

```
FeedbackId · BugReportId · SupportCaseId · EngineeringDefectId · KnownIssueId
IncidentId · DiagnosticBundleId
RecoveryCaseId · RecoveryActionId
CommunityReportId · SecurityReportId
EnforcementActionId · AppealId · SecurityAdvisoryId
```

Relationships:

```
Support Case ── Diagnostic Bundle · Recovery Case · Engineering Defect · Known Issue · Incident

Community Report → Investigation → Enforcement Action → Appeal

Security Report → Security Case / Investigation → Fix / Containment → Security Advisory
                                                                    ├─ Update
                                                                    ├─ Kill Switch
                                                                    └─ Package Revocation
```

---

## 17. Acceptance scenarios

**Ordinary bug report** — filed privately from the product; no automatic upload; the user sees the bundle before sending; a deduplicated engineering defect is created; the case remains open until the user is answered.

**Public issue** — creating one is an explicit, separate choice with a clear content warning.

**Bug dedupe** — many reports map to one defect; closing the defect does not close the cases.

**Support privacy** — support cannot read cloud content without an explicit, scoped, expiring grant; the grant is revocable and audited.

**Impersonation prohibited** — no route exists for an operator to obtain a user session; "view as user" is a marked read-only projection under a grant.

**Recovery** — the original is preserved; work happens on a copy; the result is explicit and reviewable and carries provenance.

**Unable to recover** — support states plainly that data cannot be recovered rather than implying a guarantee.

**Operator repair** — a change to a user's data goes through the owning product's recovery capability and is recorded; no ad-hoc SQL path exists.

**Canonical recovery** — canonical repair and projection repair are separately recorded and separately authorised.

**Remote support** — the session is explicit, ephemeral, view-only by default, exposes no secrets, and ends automatically.

**Community report** — a report names a package version; investigation precedes enforcement; report volume alone changes nothing.

**Confirmed malware** — containment first with notification following; execution stops; user projects and created resources survive.

**Fixed package** — a new version is required; the contaminated version number is never reused.

**False positive** — enforcement is reversed; the package returns; the history of both actions remains.

**Copyright** — enforcement targets the distribution surface; the private source is untouched.

**Public share removal** — the share stops; the underlying private resource remains.

**Cloud account restriction** — every local product continues to work at full capability.

**Appeal** — reviewed by someone other than only the original decision-maker; the original action is not erased.

**Security report** — private by default; converted from a public bug with history preserved; an advisory is published with fixed versions and an upgrade path.

**Self-host** — the official control plane cannot enforce inside an independent realm; the realm's administrator may act on the published advisory.

**Operator audit** — every high-value access carries actor, purpose, scope and target; no operator can edit the audit.

**Break glass** — requires reason, case reference, scope, dual approval, expiry and audit, and grants no general back office.

---

## 18. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 5` | Distribution matrix, signing, channels, versioning, release records, artifact verification, update behaviour, rollback, uninstall and the release domain model |
| `I4 §Stage 28` | Support, operator, recovery, incident, community report, enforcement, appeal, security report and advisory model, and operational identity |
| `I4 §Stage 10` | Incident runbook, status page and operational escalation |
| `I4 §Stage 11` | Breach-notification obligations feeding the incident runbook |
| `I3 §27` | Installation, update and rollback discipline; data compatibility on upgrade |
| **D-004**, **F-023** | Mobile licensing boundary and the pre-distribution provenance gate |
| **D-008** | Android production runtime; iOS build-deferred posture |
| **D-022**, **V-09** | Store distribution without commerce; the category-fit and consumption-only submission gates |
