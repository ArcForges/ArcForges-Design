# Platform and Dependency Matrix

[P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012) current implementation authorities: [Exact package/project producers](27-platform-projects-and-application-assistants.md); [Container/D1 binding dependency closure](data-model/04-d1-execution-profile.md).

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (publish matrix), **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** (provenance), **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** (owned distribution surfaces), [PM-02](../requirements/12-quality-and-compatibility-contract.md#rule-pm-02) and `§20` of the quality contract
> Companions: [`12-native-interop-and-media.md`](12-native-interop-and-media.md), [`14-build-packaging-and-release.md`](14-build-packaging-and-release.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

The publish matrix says which runtime each target uses. The native interop architecture says how a native call must be made. **Neither says which native capabilities the product family actually needs, which platform and architecture each is available on, what happens where it is absent, or how a dependency reaches the signed artifact.** A product with a real acquisition pipeline and a real preview pipeline cannot be planned without that.

This inventory states capability and degradation obligations. The package registry and functional ABI fix the selected initial libraries; WP13 records their adoption evidence under §3.3. Implementation cannot postpone those selections.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| <a id="rule-pd-01"></a>PD-01 | **A platform is supported only if it enters every matrix** — build, AOT publish, install, UI, recovery, compatibility, performance and release ([PM-01](../requirements/12-quality-and-compatibility-contract.md#rule-pm-01) of the quality contract). **A platform that only compiles is not supported** ([PM-11](../requirements/12-quality-and-compatibility-contract.md#rule-pm-11) there, [I-398](../requirements/01-normative-glossary-and-invariants.md#rule-i-398)). |
| <a id="rule-pd-02"></a>PD-02 | **The supported OS range is versioned release metadata**, published with the release and verified at that release ([PM-02](../requirements/12-quality-and-compatibility-contract.md#rule-pm-02) there). It is **not fixed here**, because a range asserted in a design document ages into folklore. |
| <a id="rule-pd-03"></a>PD-03 | **Every native capability in `§3` is a slot with a stated responsibility, not a named library.** A slot is filled by an adoption decision carrying [NP-01](12-native-interop-and-media.md#rule-np-01)'s substitute analysis, [PG-03](../assurance/open-gates-register.md#rule-pg-03)'s licence review and **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**'s provenance record. |
| <a id="rule-pd-04"></a>PD-04 | **A capability absent on a platform degrades explicitly with a named reason** ([LD-04](12-native-interop-and-media.md#rule-ld-04) of the native interop architecture) and never silently disappears. `§5` gives the degradation for every slot. |
| <a id="rule-pd-05"></a>PD-05 | **Every native asset ships published and signed with the application** ([LD-01](12-native-interop-and-media.md#rule-ld-01) there). Nothing is downloaded at runtime, and nothing resolves from a user-writable path ([LD-02](12-native-interop-and-media.md#rule-ld-02) there). |
| <a id="rule-pd-06"></a>PD-06 | **A dependency that cannot meet the AOT constraint cannot enter a desktop deliverable** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**), whatever else recommends it. |

---

## 2. Platform and architecture matrix

### 2.1 Tiers

| Tier | Commitment |
|---|---|
| **Tier 1** | Full matrix participation ([PD-01](#rule-pd-01)); a release is blocked by its failure |
| **Tier 2** | Produced Windows/Linux build and permitted automated-check participation under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017); a failure is recorded and may be waived per `§21` of the quality contract |
| **Not supported** | Not built, not tested, not claimed. **Absence is stated, never implied** |

### 2.2 The matrix

Embedded assistant packages are verified inside each host below; they are not a second desktop deliverable. The table records source-support design intent, not an assertion that every RID is produced or tested. Under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017), CI/publication inventories include only actually produced Windows/Linux artifacts. macOS is out of scope under [P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023): it is not a supported platform, has no source-support row, artifact, RID (`osx-*`), CI job, signing or notarisation, and no macOS support or validation is claimed. Shared code that Linux uses (for example Unix socket paths) stays.

| Target | Windows x64 | Windows arm64 | Linux x64 | Linux arm64 |
|---|---|---|---|---|
| **ArcScope** | Tier 1 | Tier 2 | Tier 1 | Tier 2 |

| Target | Runtime | Architecture posture |
|---|---|---|
| **ArcForges Cloud** | ASP.NET Core Native AOT container | Linux x64 Native AOT container; identical replicas, one process per instance |
| **ArcForges.Web.App** | Blazor WebAssembly (standalone) static assets on Cloudflare Workers Static Assets for the interactive account, chat, ArcScope library/reports/simulator console and operations profiles ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2), and the C# static Site generator; Node.js is wrangler tooling only | [browser-support.v1](../requirements/12-quality-and-compatibility-contract.md#202-browser-supportv1); no server-side WASM host; `RunAOTCompilation=false` unless a measured benchmark adopts WASM AOT. C# solution build on Windows and Linux ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021); supersedes the React/TypeScript form of [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008)) |
| **ArcChat Mobile — Android** | .NET MAUI (`net10.0-android` only, Mono runtime with AOT for release) | arm64 Tier 1; x64 for emulator use only, never a release claim ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021); supersedes the Kotlin/Jetpack Compose form of [P2-010](../decisions/phase-2-specification-decisions.md#rule-p2-010)) |

| # | Rule |
|---|---|
| <a id="rule-pt-01"></a>PT-01 | Every professional desktop retains the accepted Windows/Linux source-support design (macOS is out of scope under [P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)); a release ships only its actually produced RID set under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017) and records missing or untested coverage explicitly. Shared native/UI mechanisms require per-product integration evidence; platform parity does not imply cross-product execution. |
| <a id="rule-pt-02"></a>PT-02 | **A claimed Tier-2 release platform is a real build, not a promise.** Produced Windows/Linux RIDs publish AOT in permitted CI; source-only targets are not counted as released Tier-2 artifacts. Tier 2 does not carry release-blocking authority. |
| <a id="rule-pt-03"></a>PT-03 | **Tier promotion is a decision with evidence** — full matrix participation demonstrated — not a marketing choice. |
| <a id="rule-pt-04"></a>PT-04 | **The mobile emulator architecture is never a release claim** ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) there). |
| <a id="rule-pt-05"></a>PT-05 | **A native capability unavailable on a Tier-2 architecture does not demote the platform**; it degrades the capability per `§5`, and the degradation is part of that platform's release metadata. |

---

## 3. Native capability inventory

### 3.1 How to read a slot

| Field | Meaning |
|---|---|
| **Slot** | The capability the product needs |
| **Owner** | The project holding the managed wrapper — a DesktopPlatform capability package; products consume it through their C# infrastructure adapters ([CP-02](19-product-implementation-maps.md#rule-cp-02) of the implementation maps) |
| **ABI** | Whether ArcForges owns the C ABI shim (`arc_*`) or consumes a library's own C API directly |
| **Required by** | What breaks without it |
| **Gate** | The open gate that governs its adoption |

### 3.2 The slots

| Slot | Owner | ABI | Required by | Gate |
|---|---|---|---|---|
| **Serial and device transports** | `ArcForges.Native.Instruments` / DesktopPlatform | arc_instruments_* over OS serial and libusb; no vendor SDK in V1 | ArcScope generic serial and explicit-interface USB acquisition | [PG-03](../assurance/open-gates-register.md#rule-pg-03), [PG-08](../assurance/open-gates-register.md#rule-pg-08) |
| **High-rate acquisition and signal primitives** | `ArcForges.Native.Instruments` / DesktopPlatform | ArcForges-owned shim where a managed path cannot meet the rate | ArcScope hot path | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **Document rendering and text extraction** | **Retired** ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)): `ArcForges.Native.Pdf`, the arc_pdf_* native ABI and the ContentSandbox PDF parser path are removed by [NAT.32](../planning/delivery/lanes/native.md#task-nat-32). This removes code, not wire: the five ContentSandbox PDF RPCs and their PDF-named messages in `arcforges.local.sandbox.v1` stay in the published schema unchanged, are marked retired, and are answered with the closed `UNIMPLEMENTED` refusal; no new consumer may call them ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) item 3). Still-image parsers are composed into ContentSandbox by [NAT.31](../planning/delivery/lanes/native.md#task-nat-31) | Image parsers only; PDF is never parsed (the report-export PDF writer under SCOPE.18 is a writer, not a parser) | No PDF preview or text extraction on any surface. PDFium and [PG-12](../assurance/open-gates-register.md#rule-pg-12) are retired, not completed. | [PG-03](../assurance/open-gates-register.md#rule-pg-03) is re-scoped, not dropped: its licence and provenance review covers the report-export PDF writer chosen by SCOPE.18 and its transitive closure ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) item 2), alongside the still-image and instruments families |
| **Still-image codecs** | `ArcForges.Native.Image` (logical library `ArcImageNative`) | arc_image_* over OIIO/OpenEXR/Imath | Assistant image thin previews | [PG-03](../assurance/open-gates-register.md#rule-pg-03) |
| **Secure storage** | Per-product `*.Infrastructure` | Platform APIs | Secret broker backing (`§6` of the security architecture) | — |
| **Shell integration, global hotkey, notification** | Per-product `*.Infrastructure` | Platform APIs | Desktop shell behaviours | — |
| **Text shaping, font fallback, glyph rasterisation** | **Not ArcForges'** — Avalonia's platform backends | — | All text rendering ([RN-02](18-editing-and-rich-content.md#rule-rn-02) of the editing architecture) | — |

| # | Rule |
|---|---|
| <a id="rule-ns-01"></a>NS-01 | **There is no first-party C++ worker process.** Native code runs in-process behind the ABI (`§1` of the native interop architecture), which is why `§6` there carries the safety obligations that make a worker-free design acceptable. |
| <a id="rule-ns-02"></a>NS-02 | **Cloud has no desktop native slot** (`§2` there). Cloud is a Native AOT executable using platform crypto/SQL/HTTP without the desktop native stack. |
| <a id="rule-ns-03"></a>NS-03 | **Mobile and Web have no first-party native ABI** (`§2` there). A capability that needs one is a desktop capability. |
| <a id="rule-ns-04"></a>NS-04 | **A slot filled for one product is not thereby available to another.** A native library used by two products is still loaded per process with no shared global state ([NP-02](12-native-interop-and-media.md#rule-np-02) there), and the second product's use is its own adoption decision. |
| <a id="rule-ns-05"></a>NS-05 | **Every ArcForges-owned shim carries a fixed prefix and an ABI version** ([AB-02](12-native-interop-and-media.md#rule-ab-02) there), negotiated at load rather than assumed ([AB-12](12-native-interop-and-media.md#rule-ab-12) there). |

### 3.3 What an adoption decision must produce

Filling a slot is not a code change. Before a dependency enters a deliverable:

| # | Obligation | Authority |
|---|---|---|
| <a id="rule-ad-01"></a>AD-01 | A **named owner** for the dependency | [NP-01](12-native-interop-and-media.md#rule-np-01) |
| <a id="rule-ad-02"></a>AD-02 | A **substitute analysis** — which managed option was evaluated and why it was insufficient | [NP-01](12-native-interop-and-media.md#rule-np-01) |
| <a id="rule-ad-03"></a>AD-03 | A **licence review against that product's licence boundary**, with the file-level position established rather than inferred from a repository root | [PG-03](../assurance/open-gates-register.md#rule-pg-03), **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** |
| <a id="rule-ad-04"></a>AD-04 | A **provenance record** carrying **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**'s ten fields | **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** |
| <a id="rule-ad-05"></a>AD-05 | An **ABI decision**: an ArcForges-owned `arc_*` shim, or direct consumption of a stable C API — with the reason | `§3.2` of the native interop architecture |
| <a id="rule-ad-06"></a>AD-06 | A **per-platform availability statement** and the degradation for every platform where it is absent | [PD-04](#rule-pd-04), `§5` |
| <a id="rule-ad-07"></a>AD-07 | A **supply-chain position**: how the binary is obtained, verified, signed and reproduced | `§5` of the build architecture |
| <a id="rule-ad-08"></a>AD-08 | An **AOT compatibility statement** for any dependency in a desktop deliverable | [PD-06](#rule-pd-06), **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** |

| # | Rule |
|---|---|
| <a id="rule-ad-r1"></a>AD-R1 | **A dependency present in the repository is not thereby adopted.** Adoption is [AD-01](#rule-ad-01)–[AD-08](#rule-ad-08) completed and recorded. |
| <a id="rule-ad-r2"></a>AD-R2 | **A missing obligation blocks the dependent work rather than becoming a warning** ([OG-02](../assurance/open-gates-register.md#rule-og-02) of the open-gates register). |
| <a id="rule-ad-r3"></a>AD-R3 | **A GPL-only or unclear-licence library cannot be adopted into an AGPL-boundary product without the licence position being established first**, and never into the Apache-2.0 interoperability boundary (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |

---

## 4. Managed dependency classes

| Class | Constraint | Examples of the class |
|---|---|---|
| **In a desktop AOT deliverable** | Must publish AOT with zero trim/AOT warnings (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-05](../assurance/phase-1-official-verification.md#rule-v-05)**); no reflection-driven runtime construction | UI, contracts, persistence, HTTP, realtime |
| **In Cloud only** | Native AOT required; explicit generated serializers/registration and zero-warning publish (**[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**) | Explicit hosting, D1 binding adapter SQL, typed provider HTTP and telemetry |
| **In the Apache-2.0 boundary** | Licence-compatible with Apache-2.0 redistribution (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**) | Contracts, SDK, mobile core |
| **Build-time only** | Never shipped; may be more permissive about runtime constraints | Generators, analyzers, test tooling |

| # | Rule |
|---|---|
| <a id="rule-md-01"></a>MD-01 | **A dependency's class is declared where it is introduced**, and a class change is a review, not an edit. |
| <a id="rule-md-02"></a>MD-02 | **A Cloud-class dependency never enters a desktop project**, enforced by a repository policy test rather than by convention. |
| <a id="rule-md-03"></a>MD-03 | **An AGPL-boundary dependency never enters an Apache-2.0 project** ([PV-03](19-product-implementation-maps.md#rule-pv-03) of the implementation maps). |
| <a id="rule-md-04"></a>MD-04 | **A dependency upgrade re-runs its class's gate** (`§22` of the quality contract), so an upgrade cannot quietly break the AOT proof. |

---

## 5. Degradation matrix

What the user sees when a slot is unavailable — absent library, unsupported platform, failed verification, missing hardware.

| Slot | Degradation | Never |
|---|---|---|
| Serial or device transport | That transport is listed unavailable with its reason; others remain usable ([PM-06](../requirements/12-quality-and-compatibility-contract.md#rule-pm-06) of the quality contract) | The device list is silently short |
| High-rate acquisition | Rate ceiling reduced and **stated before capture starts**, not discovered afterwards | A capture that silently drops samples |
| Document rendering | PDF preview and parsing are retired ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)); a PDF attachment is a generic attachment shown as a **metadata card** (`§8.1`–`§8.2` of the rich content architecture) with download or share | A blank preview, or the gap concealed by calling it complete |
| Still-image codecs | Affected formats are named unavailable; the assistant's thin image preview falls back to the **metadata card** | A silently missing image presented as available |
| USB instrument transport | Device remains listed with driver/permission/interface-busy reason; other transports remain usable | Silently short enumeration or automatic kernel-driver detach |
| Text shaping, font fallback, glyph rasterisation | Use verified bundled fallback fonts, mark unsupported glyphs explicitly; broken rendering backend blocks that platform release | Silent text omission or corrupted layout |
| Secure storage | Start-up fails with an actionable message | A secret stored unprotected |
| Shell integration | That integration is unavailable; the product runs | Start-up failure |

| # | Rule |
|---|---|
| <a id="rule-dg-01"></a>DG-01 | **Library/profile degradation is discovered at startup; hotplug, device loss and later corruption are detected again at use** ([LD-03](12-native-interop-and-media.md#rule-ld-03) there), so a user learns what is unavailable before committing work to it. |
| <a id="rule-dg-02"></a>DG-02 | **A failed verification never proceeds with a partially verified library** ([LD-04](12-native-interop-and-media.md#rule-ld-04) there). |
| <a id="rule-dg-03"></a>DG-03 | **A degradation is recorded in diagnostics as well as shown**, so a support case does not depend on the user remembering the message. |
| <a id="rule-dg-04"></a>DG-04 | **Secure storage is the one slot whose absence is fatal.** Everything else degrades; a product that cannot protect a secret does not start. |

---

The slot-to-degradation mapping is explicit: serial/device→Serial or device transport plus USB instrument transport; high-rate→High-rate acquisition; document rendering→Document rendering; still-image, secure storage, shell integration and text shaping→their named rows. Native.Abstractions is common ownership infrastructure, not a physical slot. Every stated degradation preserves local data; a required Tier 1 feature that is unavailable still fails its release gate.

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
| <a id="rule-bl-01"></a>BL-01 | **Every dependency is pinned to an exact version**, and lock files are committed — the implementation repository already carries 165 of them (`§3` of the implementation-state reconciliation). |
| <a id="rule-bl-02"></a>BL-02 | **Native assets are per-RID and are published with the application**, resolved through `NativeLibrary.SetDllImportResolver` ([LD-01](12-native-interop-and-media.md#rule-ld-01) there). |
| <a id="rule-bl-03"></a>BL-03 | **Every shipped native binary is signed as part of the application's signing**, and an unsigned native asset fails the release gate (`§5` of the build architecture). |
| <a id="rule-bl-04"></a>BL-04 | **The SBOM lists every dependency with its licence and provenance**, and the licence audit is a release gate ([WP-50.01](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.01)). |
| <a id="rule-bl-05"></a>BL-05 | **Start-up verification is the runtime half of the build-time guarantee** ([LD-03](12-native-interop-and-media.md#rule-ld-03) there): what CI signed is what loads, or the feature degrades. |
| <a id="rule-bl-06"></a>BL-06 | **A per-RID asset missing for a supported platform fails that platform's publish**, rather than producing an artifact that fails at first use. |

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| <a id="rule-pv-01"></a>PV-01 | Claimed Tier-1 coverage records build/AOT and relevant local install, UI, recovery, compatibility and performance evidence under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017); unavailable environments are reported, never fabricated or provisioned solely for validation | [WP-06.00](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00), [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) |
| <a id="rule-pv-02"></a>PV-02 | Every produced Windows/Linux Tier-2 release RID completes build and AOT publish in permitted CI; macOS is out of scope under [P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023) and has no inventory entry | [WP-06.00](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.00) |
| <a id="rule-pv-03"></a>PV-03 | The supported OS range is published as release metadata and matches what was tested | [WP-50.02](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02), [WP-50.08](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.08) |
| <a id="rule-pv-04"></a>PV-04 | Every native slot in use has its [AD-01](#rule-ad-01)–[AD-08](#rule-ad-08) obligations recorded before the dependent work completes | [PG-03](../assurance/open-gates-register.md#rule-pg-03), [PG-12](../assurance/open-gates-register.md#rule-pg-12) (retired under [P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022); not a gate for any native slot), [WP-50.01](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.01) |
| <a id="rule-pv-05"></a>PV-05 | Every degradation row is exercised: absent library, failed verification, missing hardware, unsupported format | [WP-13.05](../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.05), [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) |
| <a id="rule-pv-06"></a>PV-06 | Start-up verification rejects an ABI-version mismatch with an actionable message rather than crashing later | [WP-13.05](../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.05) |
| <a id="rule-pv-07"></a>PV-07 | No native asset resolves from a user-writable path, and no dependency is downloaded at runtime | Repository policy test; [WP-11.05](../planning/work-packages/11-security-foundation.md#rule-wp-11.05) |
| <a id="rule-pv-08"></a>PV-08 | A Cloud-class dependency cannot be referenced from a desktop project | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) |
| <a id="rule-pv-09"></a>PV-09 | An AGPL-boundary assembly cannot be referenced from an Apache-2.0 project | [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) |
| <a id="rule-pv-10"></a>PV-10 | The SBOM resolves for every shipped artifact, with a licence position for every entry | [WP-50.01](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.01) |

## 8. Selected [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) runtime and dependency closure

Cloud uses .NET SDK 10.0.400, .NET10 runtime 10.0.12, Grpc.AspNetCore/Web2.83.0 and the private Worker D1 binding adapter. One Linux-x64 Native AOT executable in Cloudflare Containers, chiseled Ubuntu runtime-deps image with ICU/tzdata/CA certificates, non-root, read-only root and declared scratch, no dynamic plugin assemblies, EF/dynamic ORM, ASP.NET Session or CookieAuthenticationHandler. ASP.NET Core Minimal API endpoints and explicit generated metadata handle only allowed HTTP exceptions. The private Worker binding bridge with versioned named SQL plans and exact typed results; SQL migrations shipped as one-shot bundle. Private binding requests max 6 per Worker invocation, max 128 active RPCs per Container, bounded queue 256, drain30s; liveness process-only, readiness DB/config/private-port binding, degraded CF/R2 reported separately.

Authentication is first-party explicit session/challenge state over .NET cryptography and System.Formats.Cbor, avoiding a reflection/native dependency closure from a full Identity/FIDO framework. WebAuthn RP offers ES256 only, resident/discoverable credentials, UV required, attestation none; verify type/challenge/exact origin/RP hash/UP+UV/credential ownership/signature per W3C, bounded CBOR/JSON, reject duplicates/trailing malformed structures. Parse only COSE EC2 NIST P256 keys; ECDsa verifies signature, no ad-hoc cryptographic algorithm. Non-backup counter rollback rejects; synced credential backup flags/counter changes follow explicit suspicious-auth step-up and audit, never count as proof of compromise by themselves. Email/recovery remain existing one-use challenge/rate-limit flow, no enumeration. WP06 tests real passkey ceremony and negative vectors under AOT; failed chosen-path proof requires a focused design correction, not automatic JIT.

Native access handles are random 256-bit opaque bearer values (D1 identity.session access_token_hash + expiry), fifteen-minute expiry; native refresh token family thirty-day max with existing rotation/reuse revocation. Browser session random 256-bit handle, host-only Secure/HttpOnly/SameSite=Lax, twelve-hour absolute/thirty-minute idle; CSRF token random 256-bit bound to session/preauth flow hash, Origin+header checks on unsafe routes. C# validates current user/device/workspace/expiry on every command. No JavaScript-accessible browser credential. Secret handling never depends on ASP.NET Data Protection automatic cookie auth; each identical Container validates the same current hashed D1 session on primary reads, with guarded rotation/revocation. Browser login challenge state and session creation retain the existing Identity→Device shared transaction.

Other adapters: Paddle raw-body HMAC and typed source-generated HttpClient, no provider SDK reflection; R2/backup S3 uses typed HTTP and .NET crypto/SigV4; CF HMAC ports use source-generated STJ from the JSON schema; compression through framework streams; crypto through .NET platform primitives; telemetry through ActivitySource/Meter plus explicitly registered OTLP exporters; simulator pure deterministic C# under current AST. Domain store authority and all 20 modules stay unchanged. Early WP06 proves complete selected host dependency publish+auth/gRPC/SQL/CF/R2 path with zero trim/AOT diagnostics; product functions follow their later WPs.

Operator access uses the separate Entra OIDC/operator opaque-session scheme and typed internal operator methods fixed in [the internal operator schema](contracts/04-protobuf-wire-registry.md#9-operator-control-and-separate-identity-boundary). The same AOT host enforces both schemes with disjoint audiences/origins; no customer token can authorize administration. Public status remains independently hosted static output with an alternate provider URL under the existing operations rule.


Native dependency selection and resolved native dispositions are in [package registry](01-solution-and-project-layout.md#12-package-and-native-distribution-registry). Android OS adapters are Mobile dependencies, not desktop ABI packages. All actual candidate/RID/admission proofs remain required; the selected route is fixed before coding.

## 9. [P2-010](../decisions/phase-2-specification-decisions.md#rule-p2-010) producer and Android closure

Android .NET MAUI toolchain (`net10.0-android`, Mono runtime with AOT and trimming plus R8 for release), API/RID and OS adapter decisions are in [Mobile architecture](11-mobile-architecture.md#3-runtime-libraries-and-lifecycle-baseline) ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021); the Kotlin/Gradle baseline is superseded). Under [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3, `UseMonoRuntime=true` is explicit; NativeAOT and CoreCLR for Android stay experimental and unused until a later decision; MAUI consumes only Apache-licensed packages (Contracts NuGet, Microsoft and AndroidX bindings) and never AGPL DesktopPlatform packages. The client layer the companion needs, `Communication/ArcForges.Cloud.Client`, is AGPL: an Apache-2.0 replacement or a re-homed layer, with a licence-boundary test, is a **blocking AND.40 gate**, and no MAUI build may reference that layer until the gate passes ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3); platform APIs (Keystore, Credential Manager, WorkManager, SAF, FCM) are reached through .NET for Android/AndroidX bindings, each admitted when its task needs it. All versions are candidate pins until [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) proves actual tool availability and release-device behavior; failed compatibility is a focused gate failure, never permission to silently switch runtime. Central NuGet package management, lock files and verification checksums cover MAUI, AndroidX bindings and the first-party Contracts package. iOS and macOS are outside this delivery. The Kotlin release checks are re-proven for the MAUI closure under [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) (P2-021 item 3): minified (trimmed and R8) release, 16 KB page-size alignment, signed APK or AAB, licence and provenance closure, and F-023-class closure checks. None of these is claimed until that proof passes. C# is the Mobile implementation language; Node and TypeScript are not Mobile runtimes.

Every native slot in section 3 has fixed functions, C# wrapper ownership, error/lifetime/bulk-buffer and package closure in [functional ABI](contracts/06-native-functional-abi.md). Current probe-only DLLs do not satisfy functional producer completion. WP13 proves each required RID or retains the existing explicitly conditional tier status; mandatory portable functionality cannot be hidden behind an optional acceleration gate. [Producer stage matrix](../planning/producer-artifacts-and-integration.md) governs publication and isolated consumer evidence.
