# Platform and Dependency Matrix

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (publish matrix), **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** (provenance), **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** (owned distribution surfaces), [PM-02](../requirements/12-quality-and-compatibility-contract.md#rule-pm-02) and `§20` of the quality contract
> Companions: [`12-native-interop-and-media.md`](12-native-interop-and-media.md), [`14-build-packaging-and-release.md`](14-build-packaging-and-release.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

The publish matrix says which runtime each target uses. The native interop architecture says how a native call must be made. **Neither says which native capabilities the product family actually needs, which platform and architecture each is available on, what happens where it is absent, or how a dependency reaches the signed artifact.** A product with a real media pipeline and a real acquisition pipeline cannot be planned without that.

This document is a **capability inventory and a platform commitment structure**, not a list of chosen libraries. Choosing a library is an adoption decision with obligations (`§3.3`), and this document states those obligations rather than pre-empting them.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| <a id="rule-pd-01"></a>PD-01 | **A platform is supported only if it enters every matrix** — build, AOT publish, install, UI, recovery, compatibility, performance and release ([PM-01](../requirements/12-quality-and-compatibility-contract.md#rule-pm-01) of the quality contract). **A platform that only compiles is not supported** ([PM-11](../requirements/12-quality-and-compatibility-contract.md#rule-pm-11) there, [I-398](../requirements/01-normative-glossary-and-invariants.md#rule-i-398)). |
| PD-02 | **The supported OS range is versioned release metadata**, published with the release and verified at that release ([PM-02](../requirements/12-quality-and-compatibility-contract.md#rule-pm-02) there). It is **not fixed here**, because a range asserted in a design document ages into folklore. |
| PD-03 | **Every native capability in `§3` is a slot with a stated responsibility, not a named library.** A slot is filled by an adoption decision carrying [NP-01](12-native-interop-and-media.md#rule-np-01)'s substitute analysis, [PG-03](../assurance/open-gates-register.md#rule-pg-03)'s licence review and **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**'s provenance record. |
| <a id="rule-pd-04"></a>PD-04 | **A capability absent on a platform degrades explicitly with a named reason** ([LD-04](12-native-interop-and-media.md#rule-ld-04) of the native interop architecture) and never silently disappears. `§5` gives the degradation for every slot. |
| PD-05 | **Every native asset ships published and signed with the application** ([LD-01](12-native-interop-and-media.md#rule-ld-01) there). Nothing is downloaded at runtime, and nothing resolves from a user-writable path ([LD-02](12-native-interop-and-media.md#rule-ld-02) there). |
| <a id="rule-pd-06"></a>PD-06 | **A dependency that cannot meet the AOT constraint cannot enter a desktop deliverable** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**), whatever else recommends it. |

---

## 2. Platform and architecture matrix

### 2.1 Tiers

| Tier | Commitment |
|---|---|
| **Tier 1** | Full matrix participation ([PD-01](#rule-pd-01)); a release is blocked by its failure |
| **Tier 2** | Build and automated test participation; a failure is recorded and may be waived per `§21` of the quality contract |
| **Not supported** | Not built, not tested, not claimed. **Absence is stated, never implied** |

### 2.2 The matrix

| Target | Windows x64 | Windows arm64 | macOS arm64 | macOS x64 | Linux x64 | Linux arm64 |
|---|---|---|---|---|---|---|
| **ArcChat Desktop** | Tier 1 | Tier 2 | Tier 1 | Tier 2 | Tier 1 | Tier 2 |
| **ArcNotes** | Tier 1 | Tier 2 | Tier 1 | Tier 2 | Tier 1 | Tier 2 |
| **ArcScope** | Tier 1 | Tier 2 | Tier 1 | Tier 2 | Tier 1 | Tier 2 |
| **ArcSlate** | Tier 1 | Tier 2 | Tier 1 | Tier 2 | Tier 1 | Tier 2 |

| Target | Runtime | Architecture posture |
|---|---|---|
| **ArcForges Cloud** | ASP.NET Core Native AOT container | Linux x64 Native AOT container; identical replicas, one process per instance |
| **ArcForges.Web.App** | React/TypeScript browser assets; Node.js/npm build tooling | Supported browser matrix; no .NET WASM host. win.slnx/esproj on Windows; npm directory workflow elsewhere ([P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008)) |
| **ArcChat Mobile — Android** | React Native/Hermes | arm64 Tier 1; x64 for emulator use only, never a release claim |
| **ArcChat Mobile — iOS** | **Architecture present, build deferred** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | **Never claimed as compiled or tested** |

| # | Rule |
|---|---|
| PT-01 | **Every desktop product ships the same platform set.** A product supported on fewer platforms than its siblings would break the cross-product workflows the family is built on. |
| PT-02 | **A Tier-2 platform is a real build, not a promise.** It publishes AOT in CI; what it does not carry is release-blocking authority. |
| PT-03 | **Tier promotion is a decision with evidence** — full matrix participation demonstrated — not a marketing choice. |
| PT-04 | **The mobile emulator architecture is never a release claim** ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) there). |
| PT-05 | **A native capability unavailable on a Tier-2 architecture does not demote the platform**; it degrades the capability per `§5`, and the degradation is part of that platform's release metadata. |

---

## 3. Native capability inventory

### 3.1 How to read a slot

| Field | Meaning |
|---|---|
| **Slot** | The capability the product needs |
| **Owner** | The project holding the managed wrapper — a DesktopPlatform capability package; products consume it through their C# infrastructure adapters ([CP-02](19-product-implementation-maps.md#rule-cp-02) of the implementation maps) |
| **ABI** | Whether ArcForges owns the C ABI shim (`af_*`) or consumes a library's own C API directly |
| **Required by** | What breaks without it |
| **Gate** | The open gate that governs its adoption |

### 3.2 The slots

| Slot | Owner | ABI | Required by | Gate |
|---|---|---|---|---|
| **Media demux and decode** | `ArcForges.Native.Media` / DesktopPlatform | **ArcForges-owned `af_media_*` shim** over the chosen foundation | ArcSlate playback, proxy generation, thumbnails, waveforms | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **Media encode and mux** | `ArcForges.Native.Media` / DesktopPlatform | Same shim | ArcSlate export and render | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **Colour conversion, scale, resample** | `ArcForges.Native.Media` / DesktopPlatform | Same shim | Playback and render correctness; **preview and render share semantics** ([MP-03](12-native-interop-and-media.md#rule-mp-03)) | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **Colour management transforms** | `ArcForges.Native.Colour` / DesktopPlatform | ArcForges-owned shim | ArcSlate colour pipeline ([WP-38](../planning/work-packages/38-arcslate-render-and-colour.md#rule-wp-38)) | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **GPU device and surface access** | `ArcForges.Native.Media` / DesktopPlatform | Platform-specific rendering bridge ([BF-06](12-native-interop-and-media.md#rule-bf-06)) | Accelerated preview; **optional at every stage** ([GP-04](12-native-interop-and-media.md#rule-gp-04)) | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **Serial and device transports** | `ArcForges.Native.Instruments` / DesktopPlatform | Platform APIs and vendor SDKs, each behind its own wrapper | ArcScope acquisition ([WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33)) | [PG-03](../assurance/open-gates-register.md#rule-pg-03), [PG-08](../assurance/open-gates-register.md#rule-pg-08) |
| **High-rate acquisition and signal primitives** | `ArcForges.Native.Instruments` / DesktopPlatform | ArcForges-owned shim where a managed path cannot meet the rate | ArcScope hot path | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **Document rendering and text extraction** | `ArcForges.ContentSandbox` with the desktop broker in `ArcNotes.Infrastructure` | Native library loaded only in the isolated helper; **two operations only** ([DR-01](12-native-interop-and-media.md#rule-dr-01)) | ArcNotes PDF viewing ([AT-05](../requirements/products/arcnotes.md#rule-at-05)) | **[PG-12](../assurance/open-gates-register.md#rule-pg-12)** |
| **Secure storage** | Per-product `*.Infrastructure` | Platform APIs | Secret broker backing (`§6` of the security architecture) | — |
| **Shell integration, global hotkey, notification** | Per-product `*.Infrastructure` | Platform APIs | Desktop shell behaviours | — |
| **Text shaping, font fallback, glyph rasterisation** | **Not ArcForges'** — Avalonia's platform backends | — | All text rendering ([RN-02](18-editing-and-rich-content.md#rule-rn-02) of the editing architecture) | — |

| # | Rule |
|---|---|
| NS-01 | **There is no first-party C++ worker process.** Native code runs in-process behind the ABI (`§1` of the native interop architecture), which is why `§6` there carries the safety obligations that make a worker-free design acceptable. |
| NS-02 | **Cloud has no desktop native slot** (`§2` there). Cloud is a Native AOT executable using platform crypto/SQL/HTTP without the desktop media stack. |
| NS-03 | **Mobile and Web have no first-party native ABI** (`§2` there). A capability that needs one is a desktop capability. |
| NS-04 | **A slot filled for one product is not thereby available to another.** A native library used by two products is still loaded per process with no shared global state ([NP-02](12-native-interop-and-media.md#rule-np-02) there), and the second product's use is its own adoption decision. |
| NS-05 | **Every ArcForges-owned shim carries a fixed prefix and an ABI version** ([AB-02](12-native-interop-and-media.md#rule-ab-02) there), negotiated at load rather than assumed ([AB-12](12-native-interop-and-media.md#rule-ab-12) there). |

### 3.3 What an adoption decision must produce

Filling a slot is not a code change. Before a dependency enters a deliverable:

| # | Obligation | Authority |
|---|---|---|
| <a id="rule-ad-01"></a>AD-01 | A **named owner** for the dependency | [NP-01](12-native-interop-and-media.md#rule-np-01) |
| AD-02 | A **substitute analysis** — which managed option was evaluated and why it was insufficient | [NP-01](12-native-interop-and-media.md#rule-np-01) |
| AD-03 | A **licence review against that product's licence boundary**, with the file-level position established rather than inferred from a repository root | [PG-03](../assurance/open-gates-register.md#rule-pg-03), **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** |
| AD-04 | A **provenance record** carrying **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**'s ten fields | **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** |
| AD-05 | An **ABI decision**: an ArcForges-owned `af_*` shim, or direct consumption of a stable C API — with the reason | `§3.2` of the native interop architecture |
| AD-06 | A **per-platform availability statement** and the degradation for every platform where it is absent | [PD-04](#rule-pd-04), `§5` |
| AD-07 | A **supply-chain position**: how the binary is obtained, verified, signed and reproduced | `§5` of the build architecture |
| <a id="rule-ad-08"></a>AD-08 | An **AOT compatibility statement** for any dependency in a desktop deliverable | [PD-06](#rule-pd-06), **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** |

| # | Rule |
|---|---|
| AD-R1 | **A dependency present in the repository is not thereby adopted.** Adoption is [AD-01](#rule-ad-01)–[AD-08](#rule-ad-08) completed and recorded. |
| AD-R2 | **A missing obligation blocks the dependent work rather than becoming a warning** ([OG-02](../assurance/open-gates-register.md#rule-og-02) of the open-gates register). |
| AD-R3 | **A GPL-only or unclear-licence library cannot be adopted into an AGPL-boundary product without the licence position being established first**, and never into the Apache-2.0 interoperability boundary (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |

---

## 4. Managed dependency classes

| Class | Constraint | Examples of the class |
|---|---|---|
| **In a desktop AOT deliverable** | Must publish AOT with zero trim/AOT warnings (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-05](../assurance/phase-1-official-verification.md#rule-v-05)**); no reflection-driven runtime construction | UI, contracts, persistence, HTTP, realtime |
| **In Cloud only** | Native AOT required; explicit generated serializers/registration and zero-warning publish (**[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**) | Explicit hosting, Npgsql SQL, typed provider HTTP and telemetry |
| **In the Apache-2.0 boundary** | Licence-compatible with Apache-2.0 redistribution (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**) | Contracts, SDK, mobile core |
| **Build-time only** | Never shipped; may be more permissive about runtime constraints | Generators, analyzers, test tooling |

| # | Rule |
|---|---|
| MD-01 | **A dependency's class is declared where it is introduced**, and a class change is a review, not an edit. |
| MD-02 | **A Cloud-class dependency never enters a desktop project**, enforced by a repository policy test rather than by convention. |
| MD-03 | **An AGPL-boundary dependency never enters an Apache-2.0 project** ([PV-03](19-product-implementation-maps.md#rule-pv-03) of the implementation maps). |
| MD-04 | **A dependency upgrade re-runs its class's gate** (`§22` of the quality contract), so an upgrade cannot quietly break the AOT proof. |

---

## 5. Degradation matrix

What the user sees when a slot is unavailable — absent library, unsupported platform, failed verification, missing hardware.

| Slot | Degradation | Never |
|---|---|---|
| Media decode | The affected format is reported unsupported with its name; the project opens, media shows as **offline** ([MP-12](12-native-interop-and-media.md#rule-mp-12)) | The project fails to open |
| Media encode | Export to that format is unavailable with a reason; other formats remain | Export appears to succeed and produces an unusable file |
| GPU acceleration | **Software path, with a visible reason** ([GP-04](12-native-interop-and-media.md#rule-gp-04), [MP-08](12-native-interop-and-media.md#rule-mp-08)) | A feature disappears |
| Colour transforms | Render is refused with a named reason rather than produced with wrong colour | Silently wrong colour |
| Serial or device transport | That transport is listed unavailable with its reason; others remain usable ([PM-06](../requirements/12-quality-and-compatibility-contract.md#rule-pm-06) of the quality contract) | The device list is silently short |
| High-rate acquisition | Rate ceiling reduced and **stated before capture starts**, not discovered afterwards | A capture that silently drops samples |
| Document rendering | **Metadata card** with open-in-system-application (`§8.2` of the editing architecture); [AT-05](../requirements/products/arcnotes.md#rule-at-05) is **not met** and [PG-12](../assurance/open-gates-register.md#rule-pg-12) stays open | A blank viewer, or the gap concealed by calling it a preview |
| Secure storage | Start-up fails with an actionable message | A secret stored unprotected |
| Shell integration | That integration is unavailable; the product runs | Start-up failure |

| # | Rule |
|---|---|
| DG-01 | **A degradation is discovered at start-up verification, not at first use** ([LD-03](12-native-interop-and-media.md#rule-ld-03) there), so a user learns what is unavailable before committing work to it. |
| DG-02 | **A failed verification never proceeds with a partially verified library** ([LD-04](12-native-interop-and-media.md#rule-ld-04) there). |
| DG-03 | **A degradation is recorded in diagnostics as well as shown**, so a support case does not depend on the user remembering the message. |
| DG-04 | **Secure storage is the one slot whose absence is fatal.** Everything else degrades; a product that cannot protect a secret does not start. |

---

## 6. Build and packaging linkage

```
dependency adopted (§3.3)
   ↓ pinned to an exact version, with hash and provenance record
   ↓ restored deterministically (lock files committed)
   ↓ per-RID native assets selected at publish
   ↓ signed with the application (PD-05)
   ↓ recorded in the SBOM with its licence and provenance
   ↓ verified at start-up: ABI version, build id, hash, entry points, features (LD-03)
```

| # | Rule |
|---|---|
| BL-01 | **Every dependency is pinned to an exact version**, and lock files are committed — the implementation repository already carries 165 of them (`§3` of the implementation-state reconciliation). |
| BL-02 | **Native assets are per-RID and are published with the application**, resolved through `NativeLibrary.SetDllImportResolver` ([LD-01](12-native-interop-and-media.md#rule-ld-01) there). |
| BL-03 | **Every shipped native binary is signed as part of the application's signing**, and an unsigned native asset fails the release gate (`§5` of the build architecture). |
| BL-04 | **The SBOM lists every dependency with its licence and provenance**, and the licence audit is a release gate ([WP-50.01](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.01)). |
| BL-05 | **Start-up verification is the runtime half of the build-time guarantee** ([LD-03](12-native-interop-and-media.md#rule-ld-03) there): what CI signed is what loads, or the feature degrades. |
| BL-06 | **A per-RID asset missing for a supported platform fails that platform's publish**, rather than producing an artifact that fails at first use. |

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| PV-01 | Every Tier-1 platform completes build, AOT publish, install, UI, recovery, compatibility and performance matrices | [WP-06.00](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00), [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) |
| PV-02 | Every Tier-2 platform completes build and AOT publish in CI | [WP-06.00](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) |
| PV-03 | The supported OS range is published as release metadata and matches what was tested | [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02), [WP-50.08](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.08) |
| PV-04 | Every native slot in use has its [AD-01](#rule-ad-01)–[AD-08](#rule-ad-08) obligations recorded before the dependent work completes | [PG-03](../assurance/open-gates-register.md#rule-pg-03), [PG-12](../assurance/open-gates-register.md#rule-pg-12), [WP-50.01](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.01) |
| PV-05 | Every degradation row is exercised: absent library, failed verification, missing hardware, unsupported format | [WP-13.03](../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.03), [WP-37](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37), [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33), [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) |
| PV-06 | Start-up verification rejects an ABI-version mismatch with an actionable message rather than crashing later | [WP-13.03](../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.03) |
| PV-07 | No native asset resolves from a user-writable path, and no dependency is downloaded at runtime | Repository policy test; [WP-11.05](../planning/work-packages/11-security-foundation.md#rule-wp-11.05) |
| PV-08 | A Cloud-class dependency cannot be referenced from a desktop project | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) |
| PV-09 | An AGPL-boundary assembly cannot be referenced from an Apache-2.0 project | [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) |
| PV-10 | The SBOM resolves for every shipped artifact, with a licence position for every entry | [WP-50.01](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.01) |

## 7. Selected P2-009 runtime and dependency closure

Cloud uses .NET SDK 10.0.400, .NET10 runtime10.0.12, Grpc.AspNetCore/Web2.83.0 and Npgsql 10.0.3, PostgreSQL 18.6. One Linux-x64 Native AOT executable, chiseled Ubuntu runtime-deps image with ICU/tzdata/CA certificates, non-root, read-only root and declared scratch, no dynamic plugin assemblies, EF/dynamic ORM, ASP.NET Session or CookieAuthenticationHandler. ASP.NET Core Minimal API endpoints and explicit generated metadata handle only allowed HTTP exceptions. NpgsqlDataSource with fixed SQL and explicit parameter/reader mapping; SQL migrations shipped as one-shot bundle. DB pool max 32, max 128 active RPCs, bounded queue 256, drain 30s; liveness process-only, readiness DB/config/private-port binding, degraded CF/R2 reported separately.

Authentication is first-party explicit session/challenge state over .NET cryptography and System.Formats.Cbor, avoiding a reflection/native dependency closure from a full Identity/FIDO framework. WebAuthn RP offers ES256 only, resident/discoverable credentials, UV required, attestation none; verify type/challenge/exact origin/RP hash/UP+UV/credential ownership/signature per W3C, bounded CBOR/JSON, reject duplicates/trailing malformed structures. Parse only COSE EC2 NIST P256 keys; ECDsa verifies signature, no ad-hoc cryptographic algorithm. Non-backup counter rollback rejects; synced credential backup flags/counter changes follow explicit suspicious-auth step-up and audit, never count as proof of compromise by themselves. Email/recovery remain existing one-use challenge/rate-limit flow, no enumeration. WP06 tests real passkey ceremony and negative vectors under AOT; failed chosen-path proof requires a focused design correction, not automatic JIT.

Native access handles are random256-bit opaque bearer values (PG access_token_hash + expiry), fifteen-minute expiry; native refresh token family thirty-day max with existing rotation/reuse revocation. Browser session random256-bit handle, host-only Secure/HttpOnly/SameSite=Lax, twelve-hour absolute/thirty-minute idle; CSRF token random256-bit bound to session/preauth flow hash, Origin+header checks on unsafe routes. C# validates current user/device/workspace/expiry on every command. No JavaScript-accessible browser credential. Secret handling never depends on ASP.NET Data Protection automatic cookie auth; same PG/hash-based session works on identical replicas. Browser login challenge state and session creation retain the existing Identity→Device shared transaction.

Other adapters: Paddle raw-body HMAC and typed source-generated HttpClient, no provider SDK reflection; R2/backup S3 uses typed HTTP and .NET crypto/SigV4; CF HMAC ports use source-generated STJ from the JSON schema; compression through framework streams; crypto through .NET platform primitives; telemetry through ActivitySource/Meter plus explicitly registered OTLP exporters; simulator pure deterministic C# under current AST. Domain store authority and all 20 modules stay unchanged. Early WP06 proves complete selected host dependency publish+auth/gRPC/SQL/CF/R2 path with zero trim/AOT diagnostics; product functions follow their later WPs.

Operator access uses the separate Entra OIDC/operator opaque-session scheme and typed internal operator methods fixed in [the internal operator schema](contracts/04-protobuf-wire-registry.md#9-operator-control-and-separate-identity-boundary). The same AOT host enforces both schemes with disjoint audiences/origins; no customer token can authorize administration. Public status remains independently hosted static output with an alternate provider URL under the existing operations rule.


Native dependency selection and resolved OTIO/MDF dispositions are in [package registry](01-solution-and-project-layout.md#12-package-and-native-distribution-registry). RN native OS modules are Mobile dependencies, not desktop ABI packages. All actual candidate/RID/admission proofs remain required; the selected route is fixed before coding.
