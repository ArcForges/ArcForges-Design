# Phase 1 Official Verification Record

> Status: Complete for the Phase 1 scope defined by **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)** (foundation-critical only), as amended by **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**
> Branch: `design/phase-1-foundation`
> Verification date: **2026-09-04**
> Companions: `docs/decisions/phase-1-foundation-decisions.md`, `docs/assurance/phase-1-input-review-ledger.md`

This record verifies the time-sensitive external claims that Phase 1 decisions depend on, against current official primary sources. It is evidence, not a specification.

**Historical claim boundary.** Input labels in the original claim and consequence descriptions identify what was verified at the date above. They create no requirement to reopen the deprecated inputs. Implementers consume the current formal requirements, contracts and architecture with their cited verification results; unresolved runtime or first-consumption proof follows the [current gate register](open-gates-register.md), not historical input stage numbers.

## Scope and exclusions

**In scope** ([D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003), foundation-critical): regulatory applicability, protocol specification status, runtime and AOT posture, dependency AOT evidence, payment-provider role and capability, payout relationship, and mobile-storefront commerce rules.

**Explicitly out of scope and not verified in this pass**, per [D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)'s first-consumption rule and [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020): current prices, fees, quotas, exchange rates, tax rates, provider rate cards, storage and egress rates, and AI model pricing. These remain `DEFERRED_WITH_OWNER_AND_TRIGGER`.

## Result vocabulary

`VERIFIED` — confirmed against an official primary source.
`PARTIALLY_VERIFIED` — the official source supports part of the claim but does not prove the whole; residual risk carried as a gate.
`SUPERSEDED` — the corpus claim was true when written and is no longer current.
`DEFERRED_WITH_OWNER_AND_TRIGGER` — not verifiable now, or deliberately deferred; owner and trigger recorded.

**Standing rule.** The absence of an official AOT guarantee is never treated as proof of AOT compatibility. Where documentation cannot prove a dependency's complete behaviour under an AOT deliverable, a real publish-and-test proof is recorded below as a deferred implementation gate.

---

<a id="rule-v-01"></a>

# V-01 — EU AI Act Article 50 transparency obligations

| Field | Value |
|---|---|
| **Claim affected** | `I4 §Stage 11.30` — Article 50 transparency obligations apply from 2026-08-02 |
| **Decision affected** | [D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003) (verification scope); T09 privacy/compliance; ArcChat AI-interaction surfaces |
| **Primary source** | European Commission, *Guidelines on transparency obligations for providers and deployers of certain AI systems*, Shaping Europe's Digital Future |
| **Source date** | Guidelines adopted **2026-07-20**; obligations apply from **2026-08-02** |
| **Verification date** | 2026-09-04 |
| **Result** | **VERIFIED** |

**Findings.** Article 50 of the AI Act applies from **2 August 2026** — the corpus date is correct and the date has now passed. The Commission adopted final guidelines on **20 July 2026**. The guidelines are **non-binding**; only the CJEU can give an authoritative interpretation. A **Code of Practice on Transparency of AI-generated Content** accompanies them: providers adhering to the Code can demonstrate compliance with the marking and labelling obligations, and non-adherents must use "alternative equivalently adequate means". Content generated **before 2 August 2026 does not require retroactive labelling**.

Four obligation categories:

1. **Provider** — individuals must be explicitly informed when they interact directly with an AI system.
2. **Provider** — machine-readable marks must enable detection of AI-generated or manipulated content.
3. **Deployer** — individuals must be informed when exposed to emotion recognition or biometric categorisation.
4. **Deployer** — people must be notified about deep fakes and about text publications on matters of public interest published without human review or editorial control.

**Architectural consequence.** Categories 1 and 2 bind ArcForges directly. ArcChat and every agent-facing surface must carry an explicit AI-interaction disclosure. Any ArcForges feature that emits generated or manipulated content must be capable of applying machine-readable marking at the point of generation — which means marking is a property of the generation pipeline and the artifact format, not a UI afterthought. This reaches `I4 §Stage 22` (native format), `§Stage 19` (execution artifacts) and `§Stage 20` (ArcSlate media output). Category 4 becomes relevant only if ArcForges itself publishes unreviewed AI text on public-interest matters; it does not currently.

**Required gate.** Before the first EU-available release: confirm whether ArcForges adheres to the Code of Practice on Transparency of AI-generated Content or relies on equivalently adequate alternative means, and record the marking mechanism per artifact type. **Owner:** Security/Privacy Owner, with Product Owner approval. **Trigger:** first EU market availability.

---

<a id="rule-v-02"></a>

# V-02 — Model Context Protocol specification 2026-07-28 and the official C# SDK

| Field | Value |
|---|---|
| **Claim affected** | `I4 §Stage 6.41` — MCP `2026-07-28` is a **Release Candidate** with breaking changes; Stage 6 forbids binding the ArcChat core architecture to it while it is an RC |
| **Decision affected** | T14 extensions/MCP; ArcChat platform direction |
| **Primary source** | Model Context Protocol Blog, *The 2026-07-28 Specification*; `modelcontextprotocol/csharp-sdk` release `v2.0.0`; MCP C# SDK documentation |
| **Source date** | Specification published **2026-07-28**; C# SDK v2.0.0 stable released on or before **2026-07-28** |
| **Verification date** | 2026-09-04 |
| **Result** | **SUPERSEDED** (the RC status is no longer current) |

**Findings.** The `2026-07-28` revision is a **stable release**, not a release candidate. All four Tier 1 SDKs — Python, TypeScript, Go and **C#** — speak `2026-07-28`. The official **C# SDK v2.0.0 is stable** and aligned with the specification. It is backward compatible in the sense that stable v1 code continues to compile and run, and it retains down-level interoperability with peers negotiating `2025-11-25` and earlier.

Breaking changes in the revision: the protocol core becomes **stateless**; the `initialize`/`initialized` exchange is removed; the `Mcp-Session-Id` header is eliminated; server-to-client requests are restructured through **Multi Round-Trip Requests (MRTR)**; capability negotiation moves to each request; header-based routing and cacheable list results are added; authorization is hardened. A **formal deprecation policy with a twelve-month minimum window** is established. Roots, Sampling, Logging and Dynamic Client Registration are deprecated but still functional.

**Architectural consequence.** `I4 §Stage 6.41`'s prohibition was conditioned on RC status and that condition no longer holds — the prohibition lapses on its own terms rather than being overruled. ArcChat may now target the stable `2026-07-28` revision. Two consequences matter structurally: the protocol is **stateless**, so ArcForges must not build session-identity assumptions on MCP transport state — this aligns with the corpus's own `Session ≠ Connection` treatment; and the **formal extensions framework** (Tasks, Skills over MCP, MCP Apps) overlaps materially with `I4 §Stage 19`'s `Task / Run / Step / Attempt` model and `§Stage 24`'s extension platform, so the ArcForges execution model and the MCP extension model must be explicitly reconciled rather than conflated. `Task` in MCP is not necessarily `Task` in ArcForges.

**Required gate.** Before the ArcChat extension/MCP work package is finalised: pin the exact C# SDK version, and record an explicit mapping between MCP extension concepts and the ArcForges execution vocabulary defined by the normative glossary ([D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)). **Owner:** Architecture Owner. **Trigger:** start of the MCP/extension work package.

---

<a id="rule-v-03"></a>

# V-03 — ASP.NET Core Native AOT support in .NET 10

| Field | Value |
|---|---|
| **Claim affected** | `I3 §2.1`, `§16.2`, `§23.2` — Native AOT is the ArcForges Cloud production baseline; `I3 §2.1.3` on SignalR |
| **Decision affected** | **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime and AOT matrix); [F-007](../decisions/phase-1-foundation-decisions.md#rule-f-007) |
| **Primary source** | Microsoft Learn, *ASP.NET Core support for Native AOT*, `?view=aspnetcore-10.0` |
| **Source date** | `ms.date` **2026-06-02**; page updated **2026-07-31** |
| **Verification date** | 2026-09-04 |
| **Result** | **VERIFIED** — the expected conclusion holds |

**Findings.** The official .NET 10 compatibility table:

| Support level | Features |
|---|---|
| **Supported** | CORS · gRPC · HealthChecks · HttpLogging · JWT Authentication · Localization · OutputCaching · RateLimiting · RequestDecompression · ResponseCaching · ResponseCompression · Rewrite · StaticFiles · WebSockets |
| **Partial support** | **Minimal APIs** · **SignalR** |
| **Not supported** | **Blazor Server** · **MVC** · **OData** · **Other Authentication** · **Session** · **Spa** |

Stated constraints: reflection is not supported, so `System.Text.Json` source generation is mandatory and every type crossing the HTTP body must be registered on a `JsonSerializerContext`; `CreateSlimBuilder` omits HTTPS endpoints, HTTP/3, IIS integration, `UseStartup`, hosting startup assemblies, `UseStaticWebAssets`, several logging providers, and regex/alpha routing constraints. Features incompatible with Native AOT "are disabled and throw exceptions at run time."

From the general Native AOT overview (page updated **2026-07-27**): no dynamic loading (`Assembly.LoadFile`); no runtime code generation (`System.Reflection.Emit`); no C++/CLI; no built-in COM on Windows; trimming required; single-file compilation implied; `System.Linq.Expressions` always uses its slower interpreted form; generic instantiations are all pre-generated, with significant disk-size impact; "**Not all the runtime libraries are fully annotated to be Native AOT compatible**"; diagnostics support is limited.

**One correction to the corpus baseline.** `I3` was written against a baseline in which SignalR was **Not supported** under AOT (its .NET 8 status). Under .NET 10 SignalR has **Partial support**. This is an improvement, not a regression, and it does not alter [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008) — but the `I3 §2.1.3` statement is now stale and must not be carried into an authoritative document unamended.

**Architectural consequence.** This is the decisive evidence for **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**. A Cloud that needs anything beyond JWT bearer authentication is blocked outright: "Other Authentication" is **Not supported**. MVC is unavailable. `CreateSlimBuilder`'s omission of HTTPS endpoints and HTTP/3 pushes TLS to an ingress. Combined with the Azure SDK, durable agent loop, provider adapter and billing surfaces that `I4 §Stage 10` selects — none of which carry an AOT guarantee — a strict-AOT Cloud would be a permanent, compounding constraint on the server that changes most often. [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)'s move to an **ASP.NET Core JIT modular monolith** is confirmed by the official surface, not merely preferred.

**Required gate.** None for Cloud — the JIT decision removes the gate. Retained for desktop: AOT release gates apply only to projects actually consumed by an AOT deliverable ([D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)).

---

<a id="rule-v-04"></a>

# V-04 — .NET MAUI runtime and compilation status for Android and iOS

| Field | Value |
|---|---|
| **Claim affected** | `I3 §2.1`, `§29.6` — Android CoreCLR Native AOT is not a stable production baseline; Mono AOT is production |
| **Decision affected** | **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (mobile runtime); [D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)/[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022) mobile boundary |
| **Primary source** | Microsoft Learn, *Runtimes and compilation in .NET MAUI*, `?view=net-maui-10.0` |
| **Source date** | `ms.date` **2026-03-09**; page updated **2026-03-11** |
| **Verification date** | 2026-09-04 |
| **Result** | **VERIFIED** — the expected conclusion holds |

**Findings.** Defaults in .NET 10:

| Platform | Debug | Release |
|---|---|---|
| Android | Mono + JIT + interpreter | **Mono + Mono AOT** |
| iOS | Mono + JIT (x64) / Mono + AOT + interpreter (ARM64) | **Mono + Mono AOT** |
| Mac Catalyst | Mono + JIT (x64) / Mono + AOT + interpreter (ARM64) | **Mono + Mono AOT** |
| Windows | CoreCLR + JIT | CoreCLR + JIT + ReadyToRun |

Verbatim: "**In .NET 10, CoreCLR on Android is an experimental feature and isn't intended for production use.** In .NET 11, CoreCLR becomes the default runtime for Android `Release` builds, and is available as an experimental option for iOS."

`UseMonoRuntime` defaults to `true` for Android in .NET 10 and to `false` for Android in .NET 11. NativeAOT is "iOS and Mac Catalyst stable in .NET 9+, **Android experimental**". The platform/architecture table for .NET 9+ still marks Android Native AOT "**Experimental, no built-in Java interop**". iOS and Mac Catalyst ARM64 cannot use JIT at all, due to Apple's restrictions on dynamically generated code; Full AOT is the default for Mono release builds there.

**Architectural consequence.** Confirms **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** exactly: ArcChat Mobile Android uses the supported **.NET 10 Mono AOT** release path; Android CoreCLR and Android NativeAOT are excluded as production baselines. The .NET 11 default flip is a scheduled, known migration rather than a surprise — but it is a runtime change under the mobile app, so it must be treated as a deliberate upgrade with its own verification, not absorbed silently.

**Required gate.** (a) Before the first Android production build: confirm the runtime is Mono AOT and that `UseMonoRuntime` is explicit in the project file rather than relying on a default that changes in .NET 11. (b) Before any move to .NET 11: re-verify the Android runtime posture and re-run the mobile AOT/trim proof. (c) **iOS is architecture-present, build-deferred ([D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008))**; its eventual release runtime must be re-verified against the then-current supported MAUI/iOS baseline. **Owner:** Release Engineering Owner with Architecture Owner. **Trigger:** first Android production build; any framework major-version upgrade; iOS build activation.

---

<a id="rule-v-05"></a>

# V-05 — AOT evidence for dependencies consumed by AOT deliverables

Verified per dependency. Every entry below is a **desktop** concern only; per [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008), Cloud is JIT and Cloud-only dependencies need no AOT evidence.

<a id="rule-v-05a"></a>

### V-05a — Avalonia

| Field | Value |
|---|---|
| **Primary source** | Avalonia Docs, *Native AOT* |
| **Result** | **PARTIALLY_VERIFIED** |

Official requirements: `<PublishAot>true</PublishAot>` on the main executable only; `<IsAotCompatible>true</IsAotCompatible>` on **all** projects and libraries in use; `<BuiltInComInteropSupport>false</BuiltInComInteropSupport>` "necessary before Avalonia 12.0"; `x:CompileBindings="True"` in XAML; assets bundled as embedded resources with the `AvaloniaResource` build action; compile-time DI configuration and no reflection-based service location.

Documented limitations, verbatim in substance: "Dynamic control creation must be configured in trimmer settings", "Some third-party Avalonia controls may not be AOT-compatible", "Platform-specific features need explicit configuration". Platform support defers to Microsoft's platform/architecture restrictions rather than being independently enumerated.

**Consequence.** Avalonia supports Native AOT under conditions, and the conditions are structural — compiled bindings and compile-time DI are architecture, not build flags. The **third-party control** caveat is the real exposure: it is unbounded and cannot be discharged from documentation.

**Required gate.** A real `dotnet publish` AOT proof of the desktop shell plus every third-party control actually used, with zero IL2026/IL3050 warnings. **Owner:** owning platform work-package owner. **Trigger:** before accepting any third-party control into an AOT deliverable.

<a id="rule-v-05b"></a>

### V-05b — StreamJsonRpc with Nerdbank.MessagePack

| Field | Value |
|---|---|
| **Primary source** | StreamJsonRpc documentation (*Strongly typed proxies*, *Protocol extensibility*); Nerdbank.MessagePack documentation |
| **Result** | **PARTIALLY_VERIFIED** — the corpus design is confirmed as the correct one |

The `NerdbankMessagePackFormatter` is documented as **NativeAOT ready**, and Nerdbank.MessagePack claims "premium support for trimming and Native AOT". **Source-generated proxies** replace runtime-generated dynamic proxies and are the documented route to NativeAOT compatibility and faster startup. Interfaces carrying `[JsonRpcContract]` or `[RpcMarshalable]` **should also apply `[GenerateShape]` with `IncludeMethods` set to `PublicInstance`**. `[GenerateShape]` is "highly encouraged" because it "ensures NativeAOT and trim safety", and referenced types have their shapes source-generated transitively.

**Consequence.** This confirms `I3`'s local-IPC design precisely — `[JsonRpcContract]` + `GenerateShape` + `EnableStreamJsonRpcInterceptors` + Nerdbank.MessagePack is the AOT-viable combination, and it is the *only* documented one. It also means the shape-generation attributes are a **contract-authoring obligation**, not an optimisation: an interface added without them silently falls back to a path that is not AOT-safe. This belongs in the contract conventions under D-009.

**Required gate.** An AOT publish proof of the desktop host with the real LocalRpc contract set, plus a repository-policy test asserting that every `[JsonRpcContract]`/`[RpcMarshalable]` interface carries `[GenerateShape(IncludeMethods = PublicInstance)]`. **Owner:** Architecture Owner. **Trigger:** before the first AOT desktop deliverable.

<a id="rule-v-05c"></a>

### V-05c — Refit

| Field | Value |
|---|---|
| **Claim affected** | `I3 §2` pins **Refit 13.1.0** |
| **Primary source** | `reactiveui/refit` releases and breaking-changes documentation |
| **Result** | **PARTIALLY_VERIFIED** — with a material packaging change the corpus does not record |

Refit 12.0 rewrote request building so the **source generator constructs HTTP requests inline at compile time** rather than through the reflection pipeline, which is what makes generated clients trim- and Native-AOT-friendly. Two consequences are implementation-critical and are **not** in the corpus:

1. **The reflection request builder moved out of the main package.** Methods that cannot be generated inline report diagnostic **`RF006`** and require the separate **`Refit.Reflection`** package — which reintroduces exactly the reflection dependency an AOT deliverable must avoid. `RF006` is therefore an AOT design signal, not a nuisance warning.
2. **`RestService.ForGenerated<T>`** is the AOT-safe entry point; it constructs a client only where the source generator registered an implementation. Plain `RestService.For<T>` is not equivalent under AOT.

Some hot-path async members now return `ValueTask` instead of `Task`. Refit 14 is a later release line focused on request-generation correctness.

**Consequence.** The corpus's pinned version and its silence on `ForGenerated`/`Refit.Reflection` mean a naive implementation would compile and then fail or silently de-optimise under AOT. This is a genuine new finding, recorded as **[F-026](open-gates-register.md#rule-f-026)**.

**Required gate.** Pin the Refit version deliberately at first consumption; forbid `Refit.Reflection` in any AOT deliverable; require `RestService.ForGenerated<T>`; treat `RF006` as build-breaking in AOT projects. **Owner:** owning platform work-package owner. **Trigger:** before accepting Refit into an AOT deliverable.

<a id="rule-v-05d"></a>

### V-05d — SignalR

| Field | Value |
|---|---|
| **Result** | **VERIFIED** (see [V-03](#rule-v-03)) |

Server-side SignalR has **Partial support** under .NET 10 Native AOT — an improvement over the .NET 8 status `I3 §2.1.3` was written against. Immaterial to the runtime decision, because [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008) makes Cloud JIT. The **client** side is what desktop consumes, and it is exercised by the desktop AOT proof rather than by this table.

**Required gate.** Covered by the desktop AOT publish proof.

<a id="rule-v-05e"></a>

### V-05e — Azure SDKs, EF Core and the Cloud dependency set

| Field | Value |
|---|---|
| **Result** | **DEFERRED — and rendered moot for Cloud by [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** |

`I4 §Stage 10` selects Azure SignalR Service, Azure Service Bus, Azure Key Vault, Managed Identity and OpenTelemetry exporters; `I3 §2.1.4` and `§29.7` exclude EF Core from a strict-AOT production path. Microsoft's own guidance continues to advise against EF Core under Native AOT.

**Consequence.** [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008) explicitly instructs that Phase 1 must **not** be spent proving Azure SDK Native AOT compatibility for a server that is now JIT. That instruction is honoured: no Azure SDK AOT verification was attempted. The EF Core exclusion likewise no longer constrains Cloud. Both remain live only if a future decision moves a component into an AOT deliverable.

**Required gate.** If any Cloud component is ever moved into an AOT deliverable, its full dependency closure requires an AOT publish proof at that time. **Owner:** Architecture Owner. **Trigger:** any decision to AOT-publish a Cloud component.

---

<a id="rule-v-06"></a>

# V-06 — Paddle as Merchant of Record

| Field | Value |
|---|---|
| **Claim affected** | **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)** — Paddle is the sole customer-facing Merchant of Record for ArcForges web and cloud commerce |
| **Primary source** | Paddle Developer Docs, *Supported countries and locales*; Paddle Help Center |
| **Verification date** | 2026-09-04 |
| **Result** | **VERIFIED** |

**Findings.** Verbatim from Paddle's documentation: "As merchant of record, Paddle calculates, collects, and remits taxes for all supported countries — **you have zero sales tax liability for any Paddle transaction**." Paddle supports selling "in over 200 countries and territories" with no additional setup. Paddle blocks payments from certain countries "in compliance with international sanctions regulations, payments platforms policies, and anti-money laundering regulations."

The MoR role covers checkout, subscriptions, recurring billing, tax handling, invoices, refunds, chargebacks and webhooks — matching [D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)'s description of the role.

**Architectural consequence.** Confirms D-005. Critically for the Phase 1 brief's constraint that no payment provider may become the basis of the architecture: MoR status means Paddle is the **legal seller**, which is a commercial and tax fact, not an architectural one. The entitlement architecture stays provider-independent under [D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)'s preserved abstraction principles, and the MoR relationship does not propagate into domain contracts.

**Required gate.** Supplier onboarding and account approval before go-live. Sanctions and export screening for the intended market set. **Owner:** Commercial Operations Owner. **Trigger:** before first live transaction.

---

<a id="rule-v-07"></a>

# V-07 — The Paddle-to-Payoneer payout relationship

| Field | Value |
|---|---|
| **Claim affected** | **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)** — Payoneer is the payout and settlement destination for receiving Paddle payouts |
| **Primary source** | Paddle Help Center, *When and how do I get paid?*; *Is there a fee taken for payouts?* |
| **Verification date** | 2026-09-04 |
| **Result** | **VERIFIED** |

**Findings.** Verbatim: "You can receive your payment either via **wire transfer or Payoneer**." The payout cycle: if the balance meets the threshold, Paddle **creates the payout on the 1st and sends payment by the 15th**, then up to **3 working days** to arrive depending on method. The payout **threshold minimum is $100**, adjustable up to $100,000 (£100 / €100 equivalents). On fees: the seller is "subject to all Payoneer fees, depending on your Payoneer account type", and "Paddle will not add any fees beyond the Paddle fee on payouts made to you." A $15 SWIFT fee applies for certain countries on wire transfers.

**Architectural consequence.** Confirms [D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)'s role split exactly: Payoneer is a **payout destination**, not a second Merchant of Record and not a checkout provider. It never appears in a customer-facing flow, never issues an entitlement, and must never appear in a client authority contract. The monthly-cycle timing is a **finance-operations** fact, not a system-design fact — but it does bear on reconciliation design, because settlement lags transactions by up to six weeks, so the reconciliation model must not assume payout timing tracks transaction timing.

**Fees not verified.** Payoneer's own fee schedule and account-type differences are deferred under [D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003) and D-020.

**Required gate.** Payoneer account eligibility and receiving-currency confirmation for the chosen supplier jurisdiction, before go-live. **Owner:** Commercial Operations Owner. **Trigger:** first authoritative pricing specification, and again before launch.

---

<a id="rule-v-08"></a>

# V-08 — Paddle's current mainland-China support

| Field | Value |
|---|---|
| **Claim affected** | **[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)** — the intended China route; `I4 §Stage 3.4`, `§3.6`, `§3.50` (all built on the removed provider) |
| **Primary source** | Paddle Developer Docs, *Alipay*; Paddle Developer Docs, *WeChat Pay* |
| **Verification date** | 2026-09-04 |
| **Result** | **VERIFIED** — with two corrections to the corpus and one to a working assumption |

### Alipay

| Attribute | Paddle's documented position |
|---|---|
| One-time items | **Supported** |
| Subscriptions | **Supported** |
| Currency | **CNY only** |
| Country | China |
| Renewal/charge cap | **1,600 CNY** maximum for subscription renewals and charges; payments **fail** above it, then enter dunning recovery |
| Approval | **Separate Paddle approval required**; criteria include offering products in CNY and confirming renewals do not typically exceed the cap |
| Chargebacks | **Not supported** |
| Saved payment methods | **Not supported** |
| Platform | Desktop scans a QR code; mobile opens the Alipay app |
| Presentation rule | "Paddle Checkout only presents Alipay as a payment method for items priced in Chinese Yuan, where the customer address is China" |
| Entity requirement | No Chinese entity and no Alipay merchant account needed |

### WeChat Pay

| Attribute | Paddle's documented position |
|---|---|
| One-time items | **Supported** |
| Subscriptions | **Not supported** |
| Currencies | **CNY, USD** |
| Countries | CN |
| Platforms | **Desktop only** |
| Configuration | No configuration required; enabled in dashboard settings |
| Chargebacks | **Not supported** |
| Saved payment methods | **Not supported** |
| Capture | Deferred; usually immediate, up to ten minutes |
| Presentation rule | Presented only for one-time items priced in CNY or USD where the customer address is in China |
| Entity requirement | No WeChat Pay account and no entity in China needed |

**Three corrections.**

1. **CNY pricing inverts from forbidden to required.** `I4 §Stage 3.6` forbade inventing a fixed CNY price, because the removed provider offered no real CNY product pricing. Paddle's Alipay route **requires** CNY-priced products, and Paddle approval is conditioned on it. A CNY price list is now a prerequisite, not a hazard.
2. **The transaction cap changed shape.** The corpus recorded a single-transaction cap of roughly $140 / ¥1,000 belonging to the removed provider. Paddle's Alipay cap is **1,600 CNY on subscription renewals and charges**. Different number, different provider, different scope.
3. **WeChat Pay cannot carry subscriptions and cannot be used on mobile.** The corpus routed Chinese users to WeChat Pay for one-time USD products, which is directionally compatible; but the desktop-only restriction and the absence of subscription support are hard limits that any China plan must design around.

**Architectural consequence.** [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023) is confirmed as written and needs no amendment: its stated route — Alipay for CNY one-time and recurring subject to approval and limits, WeChat Pay for one-time desktop-web purchases, cards and other Paddle methods as available, Payoneer as payout only — matches the verified capability set item for item. Two of [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)'s structural instructions are now demonstrably load-bearing rather than precautionary: **do not hard-code caps, currencies, approval rules or platform limitations into domain contracts** (they differ per method and change per provider), and **Cloud Pass remains the non-recurring fixed-term product** (WeChat Pay users literally cannot subscribe, and Alipay users hit a renewal ceiling).

The absence of chargeback support on both methods is a further consequence for the commercial-evidence and dispute model: the dispute pathway for China differs from the card pathway, so refund and reconciliation behaviour cannot be modelled once and assumed universal.

**Required gate.** All of [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)'s listed pre-enablement gates stand, and [V-08](#rule-v-08) sharpens three of them: Alipay approval is a **separate application** with stated criteria; a **CNY product and tax configuration** must exist before approval can be sought; and the refund/dispute model must be validated against **no chargeback support** on either China method. **Owner:** Commercial Operations Owner, with Product Owner approval on the pricing catalogue. **Trigger:** before enabling mainland-China sales. **Failure consequence:** per [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023), disable mainland-China sales through explicit regional policy without blocking the global launch, and do not silently substitute another provider.

---

<a id="rule-v-09"></a>

# V-09 — Apple App Store and Google Play rules for a free consumption-only companion app

| Field | Value |
|---|---|
| **Claim affected** | **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** — ArcChat Mobile is a free companion/consumption-only application; `I4 §Stage 3.44` |
| **Primary source** | Apple, *App Review Guidelines* §3.1.1, §3.1.3, §3.1.3(f); Google Play Console Help, *Understanding Google Play's Payments policy* |
| **Verification date** | 2026-09-04 |
| **Result** | **VERIFIED** for Google Play; **PARTIALLY_VERIFIED** for Apple |

### Apple

Verbatim, **3.1.3(f) Free Stand-alone Apps**: "Free apps acting as a stand-alone companion to a paid web based tool (i.e. VoIP, Cloud Storage, Email Services, Web Hosting) do not need to use in-app purchase, provided there is no purchasing inside the app, or calls to action for purchase outside of the app."

Verbatim, **3.1.3 opening**: "The following apps may use purchase methods other than in-app purchase. Apps in this section cannot, within the app, encourage users to use a purchasing method other than in-app purchase, **except for apps on the United States storefront** and as set forth in 3.1.1(a) and 3.1.3(a). Developers can send communications outside of the app to their user base about purchasing methods other than in-app purchase."

Verbatim, **3.1.1**: "If you want to unlock features or functionality within your app … you must use in-app purchase. **Apps may not use their own mechanisms to unlock content or functionality, such as license keys**, augmented reality markers, QR codes, cryptocurrencies and cryptocurrency wallets, etc."

**Why this is `PARTIALLY_VERIFIED`.** The exemption's category list — VoIP, Cloud Storage, Email Services, Web Hosting — is illustrative ("i.e."), and ArcChat Mobile as a companion to a paid cloud and agent service fits the shape of the category without being literally enumerated. Category fit under 3.1.3(f) is decided by App Review, not by reading the guideline. No last-updated date is exposed on the guidelines page, so the text is current as fetched but not version-pinned.

### Google Play

Verbatim: "**Google Play allows any app to be consumption-only, even if it is part of a paid service. For example, a user could log in when the app opens and access content paid for somewhere else.**" And: "consumption-only means that any product(s) or service(s), whether digital or physical, cannot be purchased from within the app."

On steering: "developers may not lead users to a payment method other than Google Play's billing system unless Section 3, 8, or 9 of Payments policy applies." Outside the app, developers "are free to communicate with your users about alternative purchase options." Consumption-only apps may use informational language such as "You can purchase this book directly on our website" **without direct links**.

Google's 2026 policy changes expand billing choice — Google will not require Google Play Billing, nor prohibit other in-app payment methods, nor prohibit developers communicating about them — with a market-specific rate of 5% in the EEA, UK and US for developers using Play's billing system.

**Architectural consequence.** **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022) Option A is confirmed as viable on both storefronts, and is the only option that is viable on both without per-region variation.** Three of its prohibitions are now traceable to specific rule text rather than caution:

- No in-app purchase of subscriptions, Cloud access or AI credits, and no embedded Paddle checkout → Apple 3.1.3(f)'s "no purchasing inside the app"; Google's consumption-only definition.
- No external purchase button, link or call to action → Apple 3.1.3(f)'s "no calls to action for purchase outside of the app"; Google's in-app steering prohibition.
- **No unlocking via a locally entered licence key or purchase token** → Apple 3.1.1's explicit ban on licence keys. This is the prohibition most likely to be violated by accident, because a licence-key path is a natural engineering shortcut for offline entitlement.

[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)'s instruction to use the same conservative behaviour across storefronts even where a regional programme permits external links is well founded: Apple's US-storefront exception and Google's 2026 billing-choice changes both create region-specific permission that would otherwise force region-specific commercial builds and continuously tracked programme eligibility.

**Required gate.** Before the first App Store submission: confirm ArcChat Mobile's category fit under 3.1.3(f) with App Review, and confirm that no build path can display a purchase call to action or accept a licence key. Before the first Play submission: confirm consumption-only conformance. **Owner:** Release Engineering Owner with Product Owner approval. **Trigger:** first mobile store submission. Related: **[F-023](open-gates-register.md#rule-f-023)** (provenance and dependency closure) gates the same artifact.

---

# Summary

| ID | Subject | Result |
|---|---|---|
| [V-01](#rule-v-01) | EU AI Act Article 50 and Commission guidance | VERIFIED |
| [V-02](#rule-v-02) | MCP `2026-07-28` specification and C# SDK | SUPERSEDED (RC status no longer current; now stable) |
| [V-03](#rule-v-03) | ASP.NET Core Native AOT in .NET 10 | VERIFIED |
| [V-04](#rule-v-04) | .NET MAUI Android and iOS runtime status | VERIFIED |
| [V-05a](#rule-v-05a) | Avalonia AOT | PARTIALLY_VERIFIED |
| [V-05b](#rule-v-05b) | StreamJsonRpc + Nerdbank.MessagePack AOT | PARTIALLY_VERIFIED |
| [V-05c](#rule-v-05c) | Refit AOT | PARTIALLY_VERIFIED — new finding, see **[F-026](open-gates-register.md#rule-f-026)** |
| [V-05d](#rule-v-05d) | SignalR AOT | VERIFIED (corpus statement stale, decision unaffected) |
| [V-05e](#rule-v-05e) | Azure SDKs and EF Core | DEFERRED — moot for Cloud under [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008) |
| [V-06](#rule-v-06) | Paddle Merchant of Record | VERIFIED |
| [V-07](#rule-v-07) | Paddle-to-Payoneer payout | VERIFIED |
| [V-08](#rule-v-08) | Paddle mainland-China support | VERIFIED — three corpus corrections |
| [V-09](#rule-v-09) | Apple and Google consumption-only rules | Google VERIFIED; Apple PARTIALLY_VERIFIED |

**Every expected conclusion listed in the decision package was checked against official evidence and none was substituted for it.** All nine held. Two produced corrections the corpus does not contain ([V-05c](#rule-v-05c) Refit packaging; [V-08](#rule-v-08) CNY pricing inversion), and one lapsed a corpus prohibition on its own terms ([V-02](#rule-v-02)).

## Deferred gates registered by this verification

| Gate | Owner | Trigger |
|---|---|---|
| EU AI-content marking mechanism and Code of Practice position | Security/Privacy Owner (Product Owner approves) | First EU market availability |
| MCP SDK version pin and extension-vocabulary mapping | Architecture Owner | Start of the MCP/extension work package |
| Avalonia + third-party control AOT publish proof | Owning platform work-package owner | Before accepting a third-party control into an AOT deliverable |
| StreamJsonRpc contract-attribute policy test and AOT publish proof | Architecture Owner | Before the first AOT desktop deliverable |
| Refit version pin, `ForGenerated` policy, `Refit.Reflection` prohibition, `RF006` as build-breaking | Owning platform work-package owner | Before accepting Refit into an AOT deliverable |
| Android runtime confirmation; re-verification on any framework major upgrade; iOS baseline re-verification | Release Engineering Owner with Architecture Owner | First Android production build; framework upgrade; iOS build activation |
| Cloud component AOT proof, if any component is ever AOT-published | Architecture Owner | Any decision to AOT-publish a Cloud component |
| Paddle supplier onboarding, sanctions and export screening | Commercial Operations Owner | Before first live transaction |
| Payoneer eligibility and receiving-currency confirmation | Commercial Operations Owner | First authoritative pricing specification; again before launch |
| China enablement gates per [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023), sharpened by [V-08](#rule-v-08) | Commercial Operations Owner (Product Owner approves catalogue) | Before enabling mainland-China sales |
| Store category-fit and consumption-only conformance | Release Engineering Owner with Product Owner approval | First mobile store submission |
| All pricing, fees, quotas and rates | Commercial Operations Owner | First consumption by a specification; again before launch |

## Official sources consulted

- European Commission — [Guidelines on transparency obligations for providers and deployers of certain AI systems](https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations)
- Model Context Protocol — [The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- Model Context Protocol — [C# SDK releases](https://github.com/modelcontextprotocol/csharp-sdk/releases)
- Microsoft Learn — [ASP.NET Core support for Native AOT (aspnetcore-10.0)](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot?view=aspnetcore-10.0)
- Microsoft Learn — [Native AOT deployment overview](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/)
- Microsoft Learn — [Runtimes and compilation in .NET MAUI (net-maui-10.0)](https://learn.microsoft.com/en-us/dotnet/maui/deployment/runtimes-compilation?view=net-maui-10.0)
- Avalonia — [Native AOT](https://docs.avaloniaui.net/docs/deployment/native-aot)
- StreamJsonRpc — [Strongly typed proxies](https://microsoft.github.io/vs-streamjsonrpc/docs/proxies.html)
- Refit — [Releases](https://github.com/reactiveui/refit/releases) and [breaking changes](https://github.com/reactiveui/refit/blob/main/docs/breaking-changes.md)
- Paddle Developer Docs — [Supported countries and locales](https://developer.paddle.com/concepts/sell/supported-countries-locales/)
- Paddle Developer Docs — [Alipay](https://developer.paddle.com/concepts/payment-methods/alipay/)
- Paddle Developer Docs — [WeChat Pay](https://developer.paddle.com/concepts/payment-methods/wechat-pay/)
- Paddle Help Center — [When and how do I get paid?](https://www.paddle.com/help/manage/get-paid/when-and-how-do-i-get-paid)
- Apple Developer — [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- Google Play Console Help — [Understanding Google Play's Payments policy](https://support.google.com/googleplay/android-developer/answer/10281818)
