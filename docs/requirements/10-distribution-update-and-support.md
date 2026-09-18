# Distribution, Update, Support and Trust & Safety Requirements
> Effective scope: [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012) and [P2-013](../decisions/phase-2-specification-decisions.md#rule-p2-013) amend the technology and application ownership below. **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** (mobile licensing boundary), **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime matrix), **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**/**[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** (store posture)
> Companions: [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md), [`11-policy-and-configuration.md`](11-policy-and-configuration.md), [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md), [`../architecture/14-build-packaging-and-release.md`](../architecture/14-build-packaging-and-release.md)

Two halves of one lifecycle: how software reaches users, and what happens when something goes wrong afterwards.

---

# Part I — Distribution, release and update

## 1. Distribution posture

| # | Requirement |
|---|---|
| <a id="rule-ds-01"></a>DS-01 | **Each product installs, versions, updates and releases independently** ([P-12](00-product-scope-and-portfolio.md#rule-p-12)). |
| <a id="rule-ds-02"></a>DS-02 | **The suite is an installation experience, not a packaging unit.** A "full suite" download may exist as a bootstrapper that installs the selected products; it must never become one giant monolithic installer. |
| <a id="rule-ds-03"></a>DS-03 | **Open-source distribution and store distribution do not conflict.** The same signed artifact may be delivered through the official site and through a platform store. |
| <a id="rule-ds-04"></a>DS-04 | **A source-hosting platform is a build and release automation platform, not the primary distribution channel.** Release artifacts and update feeds are served from ArcForges-controlled infrastructure. |
| <a id="rule-ds-05"></a>DS-05 | **Release artifacts are immutable.** A published version's bytes never change. |
| <a id="rule-ds-06"></a>DS-06 | **Clients never hard-code an object-storage URL.** They resolve through an ArcForges-owned update domain, so storage can move without breaking installed clients (**[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**). |

### 1.1 Platform matrix

| Platform | Primary channel | Secondary | Notes |
|---|---|---|---|
| **Windows** | Signed installer from the official site, with a built-in update system | Platform store listing carrying the **same signed binary**; a package-manager manifest | Store distribution is distribution only, **never a commerce channel** (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**) |
| **macOS** | Official site distribution, signed with a Developer ID, hardened runtime, notarised | — | A store route is deferred: it would force sandboxing that conflicts with professional local-file and device workflows |
| **Linux** | A single self-contained portable format as the first official format | Additional package formats later | **Do not maintain many packaging formats simultaneously in the first stage** |
| **Android** | The official app store, as an app bundle with platform app signing | A directly downloadable package may exist, and is not the primary channel | **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**: consumption-only, no in-app purchase |

| # | Requirement |
|---|---|
| <a id="rule-pl-01"></a>PL-01 | **All Windows executables and installers are signed and timestamped.** |
| <a id="rule-pl-02"></a>PL-02 | **macOS artifacts are signed, hardened-runtime enabled and notarised**; Linux artifacts carry checksums and repository signing where a repository is used. |
| <a id="rule-pl-03"></a>PL-03 | Desktop product update authority remains the signed ArcForges updater across its channels. Android uses its declared direct-APK or Play channel and monotonically increasing versionCode/signing lineage; store delivery and policy gates are explicit. A higher-version rescue release, not downgrade installation, is the normal Android rollback path. |
| <a id="rule-pl-04"></a>PL-04 | **The signing identity and the brand identity are distinct concerns.** Where a signing certificate displays an individual name, the product surfaces and documentation must still present the product brand consistently, and the discrepancy must be anticipated rather than discovered at first release. |
| <a id="rule-pl-05"></a>PL-05 | **Store developer accounts must be established under the intended long-term owning identity**, not casually under a personal account that later requires a brand transfer. |
| <a id="rule-pl-06"></a>PL-06 | **Mobile provenance and the complete direct and transitive dependency closure are verified before the first mobile artifact is produced** — the **[F-023](../assurance/open-gates-register.md#rule-f-023)** gate. *Owners: Release Engineering Owner and Licensing and Provenance Owner; Product Owner approves.* |
| <a id="rule-pl-07"></a>PL-07 | **Store category fit and consumption-only conformance are confirmed before first submission** — the **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** gate. Apple's free-companion exemption is decided by review, not by reading the guideline. |

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
| <a id="rule-rc-01"></a>RC-01 | **The channel is directly switchable by the user**, with the consequences stated — including that moving to a lower channel may require a data-compatibility check ([MG-09](13-data-formats-and-portability.md#rule-mg-09) in the data requirements). |
| <a id="rule-rc-02"></a>RC-02 | **Versioning is semantic**, and version is not one number: the nine version axes in [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md) §14 apply. |
| <a id="rule-rc-03"></a>RC-03 | **Every release produces a Release Record**: version, channel, build identity, commit, artifacts with hashes, signing and notarisation status, SBOM, compatibility manifest, minimum OS versions, minimum cloud version, release notes, and the quality report. |
| <a id="rule-rc-04"></a>RC-04 | **Every release artifact is verifiable**: published hashes, signatures and attestations that a user or an auditor can check independently. |

---

## 3. Update

| # | Requirement |
|---|---|
| <a id="rule-up-01"></a>UP-01 | **An update never blocks launch.** The product starts; the update is discovered, downloaded and staged in the background, and applied at a safe moment. |
| <a id="rule-up-02"></a>UP-02 | **Delta updates are supported**, which matters most for large products such as ArcSlate. |
| <a id="rule-up-03"></a>UP-03 | **Before updating**, the product checks for running tasks and unsaved work, and defers rather than interrupting critical work ([LF-09](09-shared-desktop-experience.md#rule-lf-09)). |
| <a id="rule-up-04"></a>UP-04 | The update sequence is: download → verify signature and hash → stage → **switch atomically** → retain the previous launchable version. |
| <a id="rule-up-05"></a>UP-05 | **A failed update must never damage user data.** **An executable directory is never a user data directory.** |
| <a id="rule-up-06"></a>UP-06 | **Rollback is reserved and tested.** The previous version remains launchable, subject to data-compatibility rules. |
| <a id="rule-up-07"></a>UP-07 | **Uninstall does not delete user data by default**, and says so explicitly. |
| <a id="rule-up-08"></a>UP-08 | **Data migration is independent of the installer.** The sequence is installer update → application start → data compatibility check → migration, with its own recovery path ([SV-05](03-cloud-services-and-sync.md#rule-sv-05) in the cloud requirements, [MG-05](13-data-formats-and-portability.md#rule-mg-05)–[MG-09](13-data-formats-and-portability.md#rule-mg-09) in the data requirements). Migration must consider rollback compatibility. |
| <a id="rule-up-09"></a>UP-09 | **A critical security update has an expedited path**, coordinated with the security advisory process (§14) and, where warranted, with a policy-level kill switch ([KS-05](11-policy-and-configuration.md#rule-ks-05)) — noting that a kill switch reduces exposure but does not fix a local vulnerability. |
| <a id="rule-up-10"></a>UP-10 | **A bad version must be immediately haltable**: the update feed can stop offering it, and the compatibility policy can block it as a specific version range without blocking neighbouring versions ([CO-04](11-policy-and-configuration.md#rule-co-04)). |
| <a id="rule-up-11"></a>UP-11 | **A cloud minimum-version requirement must not be imposed before every channel has had a genuine opportunity to update**, with the grace period honoured ([CO-05](11-policy-and-configuration.md#rule-co-05)). |

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
| <a id="rule-sp-01"></a>SP-01 | **Support is assistance, not impersonation** ([I-415](01-normative-glossary-and-invariants.md#rule-i-415)). |
| <a id="rule-sp-02"></a>SP-02 | **An Operator is an Actor, not the User** ([I-416](01-normative-glossary-and-invariants.md#rule-i-416)). |
| <a id="rule-sp-03"></a>SP-03 | **Recovery repairs data through product semantics, never through arbitrary database mutation** ([I-426](01-normative-glossary-and-invariants.md#rule-i-426)). |
| <a id="rule-sp-04"></a>SP-04 | **Trust & Safety enforcement acts on distribution and access surfaces, never silently on a user's local canonical data** ([I-436](01-normative-glossary-and-invariants.md#rule-i-436), [I-438](01-normative-glossary-and-invariants.md#rule-i-438)). |
| <a id="rule-sp-05"></a>SP-05 | **Security emergency powers remain scoped, attributable and auditable.** |

---

## 7. Separating the operational objects

Nine distinct object types. **They must never all be called "ticket"** ([I-410](01-normative-glossary-and-invariants.md#rule-i-410)–[I-414](01-normative-glossary-and-invariants.md#rule-i-414)):

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
| <a id="rule-ob-01"></a>OB-01 | **Feedback ≠ Support Case** ([I-410](01-normative-glossary-and-invariants.md#rule-i-410)), **Bug Report ≠ Engineering Defect** ([I-411](01-normative-glossary-and-invariants.md#rule-i-411)), **Feature Request ≠ product commitment** ([I-412](01-normative-glossary-and-invariants.md#rule-i-412)), **Known Issue ≠ Incident** ([I-413](01-normative-glossary-and-invariants.md#rule-i-413)), **Incident ≠ Security Advisory** ([I-414](01-normative-glossary-and-invariants.md#rule-i-414)). |
| <a id="rule-ob-02"></a>OB-02 | **One hundred bug reports may map to one engineering defect**, and closing the defect does not close the support cases — each user is answered. |
| <a id="rule-ob-03"></a>OB-03 | **An internal engineering issue must not copy user-sensitive content.** It references, redacts and summarises. |
| <a id="rule-ob-04"></a>OB-04 | **A bug fix status is bound to a real release.** "Fixed" is only user-visible once a release containing the fix exists on a channel the user can reach. |
| <a id="rule-ob-05"></a>OB-05 | **A feature request never creates a false roadmap promise.** "Planned" may be shown only where it is true. |

### 7.1 In-product "Report a Problem"

| # | Requirement |
|---|---|
| <a id="rule-rp-01"></a>RP-01 | One unified in-product entry point routes to the correct object type. |
| <a id="rule-rp-02"></a>RP-02 | **A security issue is explicitly directed to the private security channel**, never to a public tracker. |
| <a id="rule-rp-03"></a>RP-03 | **An in-product bug report is private by default.** Creating a public issue is an explicit, separate user choice. |
| <a id="rule-rp-04"></a>RP-04 | **A diagnostic bundle is never uploaded automatically** ([I-424](01-normative-glossary-and-invariants.md#rule-i-424)). Each sensitive category — logs, configuration, redacted paths, content excerpts — is a separate explicit opt-in. |

---

## 8. Support case and support access

| # | Requirement |
|---|---|
| <a id="rule-sc-01"></a>SC-01 | A support case is a **private customer object** with a unified state model, and its **history is never deleted**. |
| <a id="rule-sc-02"></a>SC-02 | **A case must not be closed silently to improve a response-time metric.** |
| <a id="rule-sc-03"></a>SC-03 | **Data existing in the cloud does not give support the right to browse it** ([I-447](01-normative-glossary-and-invariants.md#rule-i-447)). |
| <a id="rule-sc-04"></a>SC-04 | Access requires an explicit **Support Access Grant** from the user, which is: minimal in scope by default, purpose-bound to a case, **time-limited and auto-expiring**, cancellable by the user at any time, and audited. |
| <a id="rule-sc-05"></a>SC-05 | **Support Access ≠ User Session** ([I-418](01-normative-glossary-and-invariants.md#rule-i-418)) and **≠ permanent permission** ([I-419](01-normative-glossary-and-invariants.md#rule-i-419)). |
| <a id="rule-sc-06"></a>SC-06 | **Silent impersonation is prohibited** ([I-415](01-normative-glossary-and-invariants.md#rule-i-415), [I-420](01-normative-glossary-and-invariants.md#rule-i-420)). An operator can never become a user. |
| <a id="rule-sc-07"></a>SC-07 | **Minting a user session for debugging is prohibited.** |
| <a id="rule-sc-08"></a>SC-08 | **Every operator action uses the operator's own principal.** An action taken by support must never be recorded as if the user performed it. |
| <a id="rule-sc-09"></a>SC-09 | **"View as user" is a Support Projection / Reproduction View**, not impersonation: a read-only rendering constructed under an explicit grant, clearly marked as such. |
| <a id="rule-sc-10"></a>SC-10 | **Support must never ask a user for a secret**, and **never for a persistent remote-access credential**. Any remote support session is explicit, ephemeral, view-only by default, and separately authorised for any interaction. A remote support session must not expose secrets. |
| <a id="rule-sc-11"></a>SC-11 | **Support attachments are support-domain data.** They never become ArcNotes, ArcChat or other product resources, they carry their own retention, and they are not copied into unrelated systems. |
| <a id="rule-sc-12"></a>SC-12 | **Support data retention and product data retention are separate** ([BK-09](03-cloud-services-and-sync.md#rule-bk-09) in the cloud requirements). |
| <a id="rule-sc-13"></a>SC-13 | **Temporary access is revoked immediately when the case closes.** |
| <a id="rule-sc-14"></a>SC-14 | **Sending a recovery package is data egress** and follows the egress authorization rules ([EG-02](07-security-privacy-and-trust.md#rule-eg-02)), including the owning user's authorization and current resource permissions. |
| <a id="rule-sc-15"></a>SC-15 | **Support analytics use minimised data only.** |
| <a id="rule-sc-16"></a>SC-16 | **Support priority may derive from a commercial plan; the privacy and permission model never does** ([I-417](01-normative-glossary-and-invariants.md#rule-i-417)). A higher plan buys faster attention, never broader access. |
| <a id="rule-sc-17"></a>SC-17 | **Trust & Safety is not affected by payment level.** Paying does not exempt anyone from reporting; not paying does not warrant harsher enforcement. |

---

## 9. Break-glass

| # | Requirement |
|---|---|
| <a id="rule-bg-01"></a>BG-01 | **Break-glass is not impersonation** ([I-420](01-normative-glossary-and-invariants.md#rule-i-420)) and **is not a global superuser** ([I-421](01-normative-glossary-and-invariants.md#rule-i-421)). It is a narrowly defined emergency operator action taken under the operator's own identity. |
| <a id="rule-bg-02"></a>BG-02 | It requires: a declared reason, an incident or case reference, an explicit scope, **dual approval / four-eyes review**, a time limit, and an audit record. |
| <a id="rule-bg-03"></a>BG-03 | **Break-glass must never accumulate into a general-purpose back office.** Each break-glass capability is individually defined and individually approved. |
| <a id="rule-bg-04"></a>BG-04 | **The risk of a large-scale operator action automatically escalates**, requiring higher approval and dual control. |
| <a id="rule-bg-05"></a>BG-05 | **An operator can never modify audit history** ([I-446](01-normative-glossary-and-invariants.md#rule-i-446)). |

---

## 10. Operator Console

**Operator Console = a controlled interface for support, operations, Trust & Safety and security management capabilities.**

| # | Requirement |
|---|---|
| <a id="rule-oc-01"></a>OC-01 | **Operator Console ≠ Database Console** ([I-422](01-normative-glossary-and-invariants.md#rule-i-422)). **It provides no arbitrary SQL.** A production data problem is never solved by ad-hoc production SQL; where an exceptional data operation is unavoidable it is an individually defined, individually audited capability. |
| <a id="rule-oc-02"></a>OC-02 | **Operator Console ≠ Domain Owner** ([I-423](01-normative-glossary-and-invariants.md#rule-i-423)). It does not own an ArcNotes document, an ArcScope session or an ArcSlate project. Changes go through the owning application's recovery capability. |
| <a id="rule-oc-03"></a>OC-03 | **Roles are separated and least-privileged**: Customer Support Operator, Recovery Specialist, Operations Operator, Trust & Safety Operator, Security Operator. **No role holds all capabilities**, and an operations role does not become a customer-content role. Their exact directory keys are customerSupport, recoverySpecialist, operations, trustSafety and security; [registry04 §9.1](../architecture/contracts/04-protobuf-wire-registry.md#91-complete-operator-authorization-and-call-context) binds every method to this vocabulary. |
| <a id="rule-oc-04"></a>OC-04 | **Global content search is prohibited.** Access is purpose-bound. |
| <a id="rule-oc-05"></a>OC-05 | **Every operator access requires a case or incident context.** Curiosity browsing is structurally impossible, not merely discouraged. |
| <a id="rule-oc-06"></a>OC-06 | **Every high-value operator access is audited** with actor, purpose, scope, target and time. |
| <a id="rule-oc-07"></a>OC-07 | **The operator dashboard shows only what operations requires** — never a general window into what users are creating. |
| <a id="rule-oc-08"></a>OC-08 | **Trust & Safety operators do not gain access to all users' private cloud content** ([SC-03](#rule-sc-03)). |

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
| <a id="rule-rv-01"></a>RV-01 | **A Recovery Package is not a Diagnostic Bundle** ([I-425](01-normative-glossary-and-invariants.md#rule-i-425)). It carries far more sensitive content, and therefore has stricter generation, sharing, handling and retention rules. |
| <a id="rule-rv-02"></a>RV-02 | **Recovery preserves the original first.** The pattern is **preserve original → work on a copy → validate → produce a recovery result**. |
| <a id="rule-rv-03"></a>RV-03 | **Recovered data must not silently overwrite normal data.** It arrives as an explicit, reviewable result. |
| <a id="rule-rv-04"></a>RV-04 | **Every recovery operation retains provenance**, so "why did this data change?" is always answerable. |
| <a id="rule-rv-05"></a>RV-05 | **Recovery is not guaranteed** ([I-428](01-normative-glossary-and-invariants.md#rule-i-428)). Support must never promise recovery of data that does not exist, and must say plainly when data cannot be recovered. |
| <a id="rule-rv-06"></a>RV-06 | **Local-only data is not visible to cloud support.** There is no back-office route to read it. |
| <a id="rule-rv-07"></a>RV-07 | **Self-hosted realm data is not accessible by default.** There is no secret backdoor; the self-host administrator provides diagnostics or a recovery package if they choose to. |
| <a id="rule-rv-08"></a>RV-08 | **Projection repair ≠ canonical data repair** ([I-427](01-normative-glossary-and-invariants.md#rule-i-427)). Rebuilding a derived projection is lighter, and is still recorded. |
| <a id="rule-rv-09"></a>RV-09 | **Staff must never quietly "fix" user data.** Every change carries recovery provenance. |
| <a id="rule-rv-10"></a>RV-10 | **Recovery must not bypass user ownership.** It requires an explicit user recovery request or a proper legal or security process. |
| <a id="rule-rv-11"></a>RV-11 | **Recovery-uploaded content has a defined lifecycle** and a shorter default retention after the case closes; security-incident evidence may require longer retention under a stated policy. |

---

## 12. Incidents

**Incident = an operational event affecting the normal operation of multiple users or services.**

| # | Requirement |
|---|---|
| <a id="rule-in-01"></a>IN-01 | **A single-user bug is not an incident** ([I-413](01-normative-glossary-and-invariants.md#rule-i-413)). |
| <a id="rule-in-02"></a>IN-02 | The incident lifecycle: detect → declare with severity → mitigate → resolve → post-incident review → published summary where users were affected. |
| <a id="rule-in-03"></a>IN-03 | **Support cases link to an incident**, so affected users are answered consistently and updated together. |
| <a id="rule-in-04"></a>IN-04 | **Incidents combine with the policy control plane**: an unavailable provider may be marked unavailable for new requests while the incident explains why and the product behaviour is legible ([PA-02](11-policy-and-configuration.md#rule-pa-02)). |
| <a id="rule-in-05"></a>IN-05 | **A public status page is an operational surface** reporting per-capability state — Identity, Sync, Storage, Search, Remote, Tasks, Managed AI, Billing ([CL-03](03-cloud-services-and-sync.md#rule-cl-03)) — and **never contains customer-specific private data**. |
| <a id="rule-in-06"></a>IN-06 | **A possible personal-data breach automatically escalates to the highest-severity legal and security incident class**, with the statutory notification clock treated as a hard operational deadline (§16.5 of the security requirements). |
| <a id="rule-in-07"></a>IN-07 | **SLO ≠ external SLA** ([I-403](01-normative-glossary-and-invariants.md#rule-i-403)). Internal objectives are not published commitments. |

---

## 13. Community reports and enforcement

| # | Requirement |
|---|---|
| <a id="rule-cr-01"></a>CR-01 | **Community Report = a report about a public ecosystem object** — a package, a publisher, a public share. |
| <a id="rule-cr-02"></a>CR-02 | **Every report has a specific target**, including a **version identity** where a package is concerned. |
| <a id="rule-cr-03"></a>CR-03 | **Report ≠ Investigation ≠ Enforcement ≠ Appeal** ([I-429](01-normative-glossary-and-invariants.md#rule-i-429)). Four stages, four objects. |
| <a id="rule-cr-04"></a>CR-04 | **Report count is not guilt** ([I-431](01-normative-glossary-and-invariants.md#rule-i-431)). A coordinated malicious report campaign must not be able to destroy a publisher. Permanent major enforcement requires controlled decision-making. |
| <a id="rule-cr-05"></a>CR-05 | **Reporter identity is not disclosed to the reported party by default**, and enforcement notices must not leak it. |
| <a id="rule-cr-06"></a>CR-06 | **An automated security scanner result is a signal, not a verdict.** |

### 13.1 Enforcement ladder

Escalating, always at **minimum necessary scope**:

```
Notice → Warning → Version-scoped delist → Package delist
      → Version-scoped revoke → Package revoke → Publisher suspension
```

| # | Requirement |
|---|---|
| <a id="rule-en-01"></a>EN-01 | **Enforcement scope is minimised.** A problem in one version is handled at that version, not across an entire publisher's catalogue. |
| <a id="rule-en-02"></a>EN-02 | **Delist ≠ Revoke** ([I-432](01-normative-glossary-and-invariants.md#rule-i-432)). Delist removes it from catalog discovery; revoke stops execution. |
| <a id="rule-en-03"></a>EN-03 | **Publisher Yank ≠ platform enforcement removal** ([I-433](01-normative-glossary-and-invariants.md#rule-i-433)). A publisher's own withdrawal is a different act with a different record. |
| <a id="rule-en-04"></a>EN-04 | **Package revocation prefers version scope** over destroying an entire package's history. |
| <a id="rule-en-05"></a>EN-05 | **A revoked package stops executing, including in the background.** |
| <a id="rule-en-06"></a>EN-06 | **Package revocation never deletes user project data** ([I-434](01-normative-glossary-and-invariants.md#rule-i-434)) and **never deletes resources created with it** ([I-435](01-normative-glossary-and-invariants.md#rule-i-435)). |
| <a id="rule-en-07"></a>EN-07 | **Extension private data is retained by default** — as evidence and as user property — with removal available as a separate, explicit act. |
| <a id="rule-en-08"></a>EN-08 | **A malicious package binary may be quarantined**; canonical product data is never deleted alongside it. |
| <a id="rule-en-09"></a>EN-09 | **Confirmed severe malware may be contained first and notified after**, with the investigation and notification continuing — an explicitly exceptional path with its own audit. |
| <a id="rule-en-10"></a>EN-10 | **A cryptographic compromise of a publisher account is an immediate containment case.** After recovery the publisher **may not reuse a contaminated version number**; a new version is required. |
| <a id="rule-en-11"></a>EN-11 | **The offline-device reality is stated honestly** ([DS-06](11-policy-and-configuration.md#rule-ds-06) in the policy requirements): a revocation cannot reach a machine that never connects. The operating-system and update security perimeter remains necessary. |
| <a id="rule-en-12"></a>EN-12 | **Self-host revocation must never become an official hidden backdoor** ([I-443](01-normative-glossary-and-invariants.md#rule-i-443)). The official control plane cannot silently control an independent realm; it may publish information that the realm's administrator chooses to act on. |
| <a id="rule-en-13"></a>EN-13 | **Trust & Safety actions are as reversible as possible.** A false positive can be restored. |
| <a id="rule-en-14"></a>EN-14 | **Trust & Safety reason codes are stable and invariant.** The human-readable explanation is localised; **the enforcement semantics never differ by user language**. |
| <a id="rule-en-15"></a>EN-15 | **A normal policy delisting must not create a security panic.** Delisting for a routine reason and delisting for a security reason are presented differently. |
| <a id="rule-en-16"></a>EN-16 | **Installed users receive a Needs Attention state** when a package they use is revoked ([CA-13](08-extensions-and-developer-platform.md#rule-ca-13)). |
| <a id="rule-en-17"></a>EN-17 | **The official catalog shows a package's security status.** |

### 13.2 Copyright and public content

| # | Requirement |
|---|---|
| <a id="rule-cp-01"></a>CP-01 | **Copyright and intellectual-property reports follow an independent legal workflow**, separate from ordinary abuse. |
| <a id="rule-cp-02"></a>CP-02 | **Copyright enforcement targets the distribution surface** — the catalog listing, the public share — **not a user's private local canonical data** ([I-436](01-normative-glossary-and-invariants.md#rule-i-436)). |
| <a id="rule-cp-03"></a>CP-03 | **Public share removal does not delete the private source** ([I-437](01-normative-glossary-and-invariants.md#rule-i-437)). |
| <a id="rule-cp-04"></a>CP-04 | **Private local data is not a community moderation surface** ([I-489](01-normative-glossary-and-invariants.md#rule-i-489) analogue). |
| <a id="rule-cp-05"></a>CP-05 | **A community report does not expose private cloud data to a moderator** ([SC-03](#rule-sc-03), [OC-08](#rule-oc-08)). |

### 13.3 Account enforcement

| # | Requirement |
|---|---|
| <a id="rule-ae-01"></a>AE-01 | Cloud account restrictions stop authorized Cloud service access as specified; they do not confiscate independent native capture/media data or discard unsynced work. Cached Notes/Chat access, service expiry and deletion follow the identity and Cloud lifecycle contracts; local AI is not a fallback. |
| <a id="rule-ae-02"></a>AE-02 | **Cloud Account Restriction ≠ local data confiscation** ([I-438](01-normative-glossary-and-invariants.md#rule-i-438)). |

### 13.4 Appeal

| # | Requirement |
|---|---|
| <a id="rule-ap-01"></a>AP-01 | **Appeal is a first-class object**: a request to re-examine a specific enforcement action. |
| <a id="rule-ap-02"></a>AP-02 | **An appeal does not modify enforcement history** ([I-439](01-normative-glossary-and-invariants.md#rule-i-439)). The original action, the appeal and the outcome are all retained. |
| <a id="rule-ap-03"></a>AP-03 | **Serious enforcement is reviewed as independently as practical**, by someone other than only the original decision-maker. |
| <a id="rule-ap-04"></a>AP-04 | **A security revocation appeal is special**: a binary containing exploitable malware stays revoked permanently, regardless of who now controls the account. |
| <a id="rule-ap-05"></a>AP-05 | **An enforcement notice is understandable** without revealing detection rules or the reporter's identity. |
| <a id="rule-ap-06"></a>AP-06 | **An emergency security investigation may delay some notice**, under a formal security case with audit. |
| <a id="rule-ap-07"></a>AP-07 | **Appeal must not become a harassment tool**, and a real review path must nonetheless exist. |

---

## 14. Security reports and advisories

| # | Requirement |
|---|---|
| <a id="rule-sr-01"></a>SR-01 | **Security Report = a private vulnerability disclosure object**, with its own lifecycle: received → triaged → validated → fixed or contained → advisory published → credited. |
| <a id="rule-sr-02"></a>SR-02 | **A security report is private by default** ([I-440](01-normative-glossary-and-invariants.md#rule-i-440)) and is never auto-published. |
| <a id="rule-sr-03"></a>SR-03 | **Ordinary bugs and security reports convert both ways**: a bug found to be a vulnerability moves into the security case workflow, with its history preserved. |
| <a id="rule-sr-04"></a>SR-04 | **Security Advisory = a versioned, published security notice**, exposed to users and administrators after validation. |
| <a id="rule-sr-05"></a>SR-05 | **Security Advisory ≠ Incident** ([I-414](01-normative-glossary-and-invariants.md#rule-i-414)), **≠ Kill Switch** ([I-441](01-normative-glossary-and-invariants.md#rule-i-441)), **≠ Package Revocation** ([I-442](01-normative-glossary-and-invariants.md#rule-i-442)). An advisory communicates; a kill switch and a revocation enforce. |
| <a id="rule-sr-06"></a>SR-06 | **An advisory has a stable identity and is versioned; history is never rewritten in place.** |
| <a id="rule-sr-07"></a>SR-07 | **An advisory is connected to the update system**: it names the fixed versions and the upgrade path, so a user can act on it. |
| <a id="rule-sr-08"></a>SR-08 | **A serious cloud vulnerability may be combined with a kill switch**, and an extension vulnerability with package revocation — as separate, coordinated acts. |
| <a id="rule-sr-09"></a>SR-09 | **A security advisory must never prevent a user from accessing their own local data** in the name of security. |
| <a id="rule-sr-10"></a>SR-10 | **A signed advisory feed is published**, so administrators and self-hosted realms can consume it. |
| <a id="rule-sr-11"></a>SR-11 | **A self-hosted realm may subscribe to the official advisory feed. Subscribing must not hand control of self-host policy to the official cloud** ([I-443](01-normative-glossary-and-invariants.md#rule-i-443)). **Advisory is information, not remote policy authority.** |
| <a id="rule-sr-12"></a>SR-12 | **A publisher-facing advisory path exists** for vulnerabilities in third-party packages. |

---

## 15. Operator security and audit

| # | Requirement |
|---|---|
| <a id="rule-oa-01"></a>OA-01 | **Operator actions use the ordinary security model**: an operator is a human principal with capabilities, scope and risk, subject to approval and step-up like any other actor. |
| <a id="rule-oa-02"></a>OA-02 | **Support audit and Trust & Safety audit are distinguished** by category, and both use the one unified audit vocabulary ([AU-02](07-security-privacy-and-trust.md#rule-au-02) in the security requirements). |
| <a id="rule-oa-03"></a>OA-03 | **Users can see the important operator actions that relate to them**, in their own security activity. |
| <a id="rule-oa-04"></a>OA-04 | **`Staff Access ≠ Secret Access`** ([I-444](01-normative-glossary-and-invariants.md#rule-i-444)). Operating access never implies access to secrets. |
| <a id="rule-oa-05"></a>OA-05 | **`Support Attachment ≠ product resource authority`** ([I-445](01-normative-glossary-and-invariants.md#rule-i-445)). |
| <a id="rule-oa-06"></a>OA-06 | **Feedback, diagnostics and recovery all respect workspace boundaries** ([WS-07](02-identity-account-and-workspace.md#rule-ws-07) in the identity requirements). |

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

| Current document | Relationship |
|---|---|
| [Build, Packaging and Release Architecture](../architecture/14-build-packaging-and-release.md) | Implements packaging, signing, release records and updates |
| [Deployment and Release Execution](../architecture/22-deployment-and-release-execution.md) | Defines promotion, rollback and mixed-version release procedures |
| [Observability and Operations Architecture](../architecture/13-observability-and-operations.md) | Implements support, incident, status and operator mechanisms |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[F-023](../assurance/open-gates-register.md#rule-f-023)** | Mobile licensing boundary and the pre-distribution provenance gate |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Android production runtime; Android-only delivery posture |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** | Store distribution without commerce; the category-fit and consumption-only submission gates |
