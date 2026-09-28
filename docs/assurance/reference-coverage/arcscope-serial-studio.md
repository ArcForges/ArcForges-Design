# Reference Coverage Matrix — ArcScope / Serial-Studio

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete**
> Governing authority: **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**, **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**, **[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)** (ArcScope is independently defined, not a rename of a superseded product)
> Scope note: Sections 1–7 are the historical review bound to commit 639daafb. Section 8 is a separate current-drift check and does not rewrite those baseline observations or expand ArcScope requirements. In particular, “the most restrictive in the programme” in §2 describes the licence at that pinned baseline, not the current upstream model.
> Consuming product: **ArcScope** — [`../../requirements/products/arcscope.md`](../../requirements/products/arcscope.md)

---

## 1. Source identity

| Field | Value |
|---|---|
| Repository | `github.com/Serial-Studio/Serial-Studio` |
| Local path | `C:\MyFile\ArcForges\Serial-Studio` |
| Commit | `639daafb` |
| Commit date | 2026-07-13 |
| Reviewed on | 2026-09-05 |
| Reviewer | Architecture Owner (design stage) |

---

## 2. Licence and provenance position — the most restrictive in the programme

`LICENSE.md` is a **custom dual-licence agreement**, not a standard grant. Read in full:

| Element | Evidence | Finding |
|---|---|---|
| Model | `LICENSE.md` §1 | **Dual**: GPL-3.0-only for source, **Serial Studio Commercial License** for official binaries and any build including gated features |
| GPL scope | `LICENSE.md` §1, §2 | GPLv3 applies **only** to components explicitly marked as such and **excludes** the Pro modules |
| GPL conditions | `LICENSE.md` §2.1 | Must compile from source; must use a GPL-compliant Qt; **must not enable, link, replicate, simulate or include any Pro module** |
| Pro modules (commercial-only, excluded from GPL) | `LICENSE.md` §4 | Qt MQTT and Qt SerialBus modules; **MQTT support**; **XY plotting**; **3D visualization**; **activation/licensing systems** |
| Pro module status | `LICENSE.md` §4 | *"defined as separate works and not covered by GPLv3. Their source code, even if visible, does not confer any right to use, modify, compile, or distribute them"* |
| Binary trial | `LICENSE.md` §1.1 | Official binary is a 14-day single-use trial, then requires a paid licence |
| Licence file set | `LICENSES/GPL-3.0-only.txt`, `LICENSES/LicenseRef-SerialStudio-Commercial.txt` | Confirms the two-licence structure |

| # | Finding |
|---|---|
| <a id="rule-lp-01"></a>LP-01 | **The GPL portion is GPL-3.0-only.** Under **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**, GPL-only material **must not be copied, translated or ported**. It may be used only as controlled behavioural reference. |
| <a id="rule-lp-02"></a>LP-02 | **The Pro modules are commercial-only and are not open source at all.** Source visibility confers no rights. They are treated as an **authorship boundary**: their source was not read, and no ArcForges capability may be derived from their expression. |
| <a id="rule-lp-03"></a>LP-03 | **The packaged binary in `StartArcForges/Serial-Studio` is trial-limited commercial software.** It was **not executed** — consistent with the instruction not to execute packaged-product binaries, and independently required here because execution would consume a licensed trial. |
| <a id="rule-lp-04"></a>LP-04 | **Every row in this matrix is `Reference Only` or an accepted exclusion.** No reuse is possible from either portion. |

---

## 3. Reviewed scope

| Area read | Evidence location |
|---|---|
| Licence agreement in full | `LICENSE.md`, `LICENSES/` |
| Acquisition and transport | `app/src/IO/**`, `app/src/IO/Drivers/**` |
| Frame and data model | `app/src/DataModel/**` |
| Session, recording, replay, export, reporting | `app/src/Sessions/**`, `app/src/CSV/**`, `app/src/MDF4/**` |
| Visualisation surface | `app/qml/Widgets/Dashboard/**`, `app/src/UI/**` |
| Console | `app/src/Console/**` |
| API surface | `app/src/API/**` |
| Miscellaneous services | `app/src/Misc/**` |
| Platform integration | `app/src/Platform/**` |
| Test approach | `tests/{integration,unit,performance,security,benchmarks,manual}/**` |
| Packaged release shape | `StartArcForges/Serial-Studio` — directory listing only, **not executed** |

**Not read, and why:** `app/src/MQTT/**`, `app/src/Licensing/**`, and the 3D/XY plotting implementations — **Pro modules under `LICENSE.md` §4**. Their expression is deliberately not read; their existence and stated purpose are recorded from the licence text and directory names alone. `app/src/ThirdParty/**` — vendored dependencies under their own licences, out of scope.

---

## 4. Item-level matrix

| # | Capability / behaviour | Evidence location | ArcForges requirement or exclusion | Disposition | Rationale | Licence position | Verification oracle | Owner | State |
|---|---|---|---|---|---|---|---|---|---|
| <a id="rule-as-01"></a>AS-01 | Connection and device management separation | `app/src/IO/{ConnectionManager,DeviceManager}.{h,cpp}` | `products/arcscope.md` [SD-01](../../requirements/products/arcscope.md#rule-sd-01) (`Device ≠ DataSource`); [WP-33.00](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) | Reference Only | **Independent confirmation of [I-466](../../requirements/01-normative-glossary-and-invariants.md#rule-i-466)**: the reference separates connection management from device identity | GPL-3.0-only — no reuse permitted | First-party test: `Device ≠ DataSource` structurally | Product Owner | Evidence established |
| <a id="rule-as-02"></a>AS-02 | Transport drivers — serial, network, Bluetooth LE, HID, audio, process, CAN, Modbus | `app/src/IO/Drivers/{Network,BluetoothLE,HID,Audio,Process,CANBus,CanBackends,GsUsbCanBackend,Modbus}.{h,cpp}` | `products/arcscope.md` [SD-09](../../requirements/products/arcscope.md#rule-sd-09) (V1 generic transports; device SDKs later); [WP-33.00](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) | Reference Only | Establishes the transport family a product in this category is expected to cover, and confirms ArcForges' V1 subset is a deliberate reduction rather than an omission | GPL-3.0-only — no reuse permitted | Per-adapter real-transport test ([WP-33.00](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00)) | Product Owner | Evidence established |
| <a id="rule-as-03"></a>AS-03 | MQTT transport | `app/src/IO/Drivers/MQTT.{h,cpp}`, `app/src/MQTT/**` | **Accepted exclusion** — Pro module, and not in accepted V1 transports | Drop | `LICENSE.md` §4 lists MQTT as commercial-only; **its source was not read** | Commercial-only; no rights conferred | — | Licensing and Provenance Owner | Accepted exclusion |
| <a id="rule-as-04"></a>AS-04 | Circular / rolling buffer | `app/src/IO/CircularBuffer.h` | `products/arcscope.md` [SE-04](../../requirements/products/arcscope.md#rule-se-04) (live view vs capture); [WP-33.02](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.02) | Reference Only | Confirms the rolling-buffer/live-view separation and its role in pre-trigger windows | GPL-3.0-only — no reuse permitted | First-party test: pausing the view never stops recording | Product Owner | Evidence established |
| <a id="rule-as-05"></a>AS-05 | Frame reader, frame builder, frame config, checksum | `app/src/IO/{FrameReader,FrameBuilder,FrameConfig,Checksum}.*` | `products/arcscope.md` §decoders; [WP-34.03](../../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.03) | Reference Only | Evidence that framing and checksum validation are first-class and their failures must be visible | GPL-3.0-only — no reuse permitted | First-party test: checksum failures surfaced with counts and locations | Product Owner | Evidence established |
| <a id="rule-as-06"></a>AS-06 | Data table and frame consumer | `app/src/DataModel/{DataTable,Frame,FrameConsumer}.*` | `products/arcscope.md` §channel/signal/event model; [WP-33.03](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.03) | Reference Only | Evidence on the decoded-data model shape | GPL-3.0-only — no reuse permitted | First-party precision and alignment tests | Product Owner | Evidence established |
| <a id="rule-as-07"></a>AS-07 | Hot-path optimisation | `app/src/DataModel/HotpathOptimization.h`, `app/src/DSP.h` | `products/arcscope.md` §18 (throughput); [WP-13.02](../../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.02), [WP-33.01](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.01) | Reference Only | **Performance evidence**: confirms that a dedicated hot path is required to sustain acquisition rates — supporting the probe in [WP-13.02](../../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.02) | GPL-3.0-only — no reuse permitted | Sustained-throughput measurement with bounded memory | Product Owner | Evidence established |
| <a id="rule-as-08"></a>AS-08 | Importers — DBC, Modbus map, Protobuf | `app/src/DataModel/Importers/{DBCImporter,ModbusMapImporter,ProtoImporter}.*` | **Accepted exclusion** for V1; retained as later-adapter evidence | Drop | Protocol-description import is beyond the accepted V1 decoder scope; recorded so it is a deliberate choice | GPL-3.0-only — no reuse permitted | — | Product Owner | Accepted exclusion |
| <a id="rule-as-09"></a>AS-09 | Session database and worker | `app/src/Sessions/{DatabaseManager,DatabaseWorker}.*` | `products/arcscope.md` [SE-14](../../requirements/products/arcscope.md#rule-se-14) (chunked verifiable store, not database blobs); [WP-33.04](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.04) | Reference Only | **Divergence recorded**: the reference stores session data in a database. ArcForges requires raw capture in a chunked verifiable store instead, because capture is evidence and must be independently verifiable | GPL-3.0-only — no reuse permitted | First-party test: crash yields a verifiable prefix with recorded loss | Architecture Owner | Evidence established |
| <a id="rule-as-10"></a>AS-10 | Player / replay | `app/src/Sessions/{Player,PlayerLoaderWorker}.*`, `app/src/CSV/Player.*`, `app/src/MDF4/Player.*` | `products/arcscope.md` [SD-10](../../requirements/products/arcscope.md#rule-sd-10) (replay never impersonates a device); [WP-33.05](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.05) | Reference Only | Evidence that replay is a first-class source; ArcForges adds the labelling requirement the reference does not have | GPL-3.0-only — no reuse permitted | First-party test: replay always labelled, device-only fields absent | Product Owner | Evidence established |
| <a id="rule-as-11"></a>AS-11 | Export — CSV, MDF4, console, session | `app/src/{CSV,MDF4,Console}/Export.*`, `app/src/Sessions/Export.*` | `products/arcscope.md` §16 (export with precision warnings); [WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04) | Reference Only | **Migration evidence**: names the interchange formats expected in this category, and confirms tabular export needs precision handling | GPL-3.0-only — no reuse permitted | Format fixture per claimed export version ([PG-07](../open-gates-register.md#rule-pg-07)) | Product Owner | Evidence established |
| <a id="rule-as-12"></a>AS-12 | HTML report and report data | `app/src/Sessions/{HtmlReport,ReportData}.*` | `products/arcscope.md` §12 (reports with source traceability); [WP-34.06](../../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.06) | Reference Only | Evidence on report composition; ArcForges additionally requires every element to trace to session, capture, configuration snapshot and analysis version | GPL-3.0-only — no reuse permitted | First-party test: report regeneration produces equivalent results | Product Owner | Evidence established |
| <a id="rule-as-13"></a>AS-13 | Dashboard widgets — plot, multi-plot, FFT, waterfall, bar, gauge, meter, compass, accelerometer, gyroscope, GPS, LED panel, data grid, terminal, clock, stopwatch | `app/qml/Widgets/Dashboard/*.qml` (24 files) | `products/arcscope.md` §5 visualisation; [WP-34.00](../../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.00) | Reference Only | **Establishes the expected visualisation vocabulary.** ArcForges' V1 set is a deliberate subset; this row is what makes that a choice rather than an oversight | GPL-3.0-only — no reuse permitted | First-party scope reference-signal tests | Product Owner | Evidence established |
| <a id="rule-as-14"></a>AS-14 | 3D plot and XY plot widgets | `app/qml/Widgets/Dashboard/Plot3D.qml` and the XY plotting implementation | **Accepted exclusion** — Pro modules | Drop | `LICENSE.md` §4 lists XY plotting and 3D visualization as commercial-only; **their implementations were not read** | Commercial-only; no rights conferred | — | Licensing and Provenance Owner | Accepted exclusion |
| <a id="rule-as-15"></a>AS-15 | Web engine / web view widgets | `app/qml/Widgets/Dashboard/{WebEngineSurface,WebView}.qml` | **Accepted exclusion** — no ArcForges requirement | Drop | An embedded browser surface in a professional acquisition product is outside the accepted scope and is a large security surface | GPL-3.0-only — no reuse | — | Security and Privacy Owner | Accepted exclusion |
| <a id="rule-as-16"></a>AS-16 | Alarm monitor | `app/src/UI/AlarmMonitor.*` | `products/arcscope.md` §7 triggers; [WP-34.01](../../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.01) | Reference Only | Evidence that threshold alarms are a distinct concept from capture triggers | GPL-3.0-only — no reuse permitted | First-party trigger window tests | Product Owner | Evidence established |
| <a id="rule-as-17"></a>AS-17 | Notification centre | `app/src/DataModel/NotificationCenter.*`, `app/qml/Widgets/Dashboard/NotificationLog.qml` | `09-shared-desktop-experience.md` §attention; [WP-10.04](../../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.04) | Reference Only | Evidence that acquisition products need a durable event log distinct from transient notifications | GPL-3.0-only — no reuse permitted | First-party durability test | Product Owner | Evidence established |
| <a id="rule-as-18"></a>AS-18 | Project editor | `app/qml/ProjectEditor/**` | `products/arcscope.md` §2 project model; [WP-33.00](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) | Reference Only | Evidence on configuring a data schema before acquisition; ArcForges records this as the effective configuration snapshot | GPL-3.0-only — no reuse permitted | First-party test: profile edit never rewrites a historical session | Product Owner | Evidence established |
| <a id="rule-as-19"></a>AS-19 | MCP handler and command protocol | `app/src/API/{MCPHandler,MCPProtocol,CommandHandler,CommandProtocol,CommandRegistry}.*` | `08-extensions-and-developer-platform.md` §MCP; **[V-02](../phase-1-official-verification.md#rule-v-02)**; [WP-35.00](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.00) | Reference Only | **Third independent confirmation** that MCP appears as an integration adapter in this product category | GPL-3.0-only — no reuse permitted | Vocabulary mapping record ([VG-02](../open-gates-register.md#rule-vg-02)) | Architecture Owner | Evidence established |
| <a id="rule-as-20"></a>AS-20 | gRPC API | `app/src/API/GRPC/**` | **Accepted source exclusion** — reference API implementation is not adopted | Drop | ArcForges uses its own authored proto/native gRPC under [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009)/010. The GPL reference implementation is not reused; this row does not prohibit gRPC or remove the accepted first-party protocol | GPL-3.0-only — no reuse | — | Architecture Owner | Accepted exclusion |
| <a id="rule-as-21"></a>AS-21 | Path policy | `app/src/API/PathPolicy.*` | `products/arcscope.md` §14 ([AI-08](../../requirements/products/arcscope.md#rule-ai-08)); `07-security-privacy-and-trust.md` | Reference Only | **Security evidence**: confirms an API that can touch files needs an explicit path policy — supporting ArcForges' resource-identity-not-path rule | GPL-3.0-only — no reuse permitted | First-party test: a reference cannot carry a path | Security and Privacy Owner | Evidence established |
| <a id="rule-as-22"></a>AS-22 | AI assistant with file sandbox and doc search | `app/src/AI/{Assistant,ChatStore,ContextBuilder,Conversation,DocSearch,FileSandbox,CommandRegistry}.*` | `products/arcscope.md` §14 (bounded structured context); [WP-35.01](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.01) | Reference Only | **Directly supports [I-182](../../requirements/01-normative-glossary-and-invariants.md#rule-i-182) and [AI-02](../../requirements/products/arcscope.md#rule-ai-02)**: the reference sandboxes file access and builds bounded context rather than handing over raw data | GPL-3.0-only — no reuse permitted | First-party test: raw capture structurally cannot enter an AI context payload | Security and Privacy Owner | Evidence established |
| <a id="rule-as-23"></a>AS-23 | Extension manager | `app/src/Misc/ExtensionManager.*` | `08-extensions-and-developer-platform.md`; [WP-41](../../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41) | Reference Only | Evidence of an extension surface in this category; ArcForges' out-of-process model diverges deliberately | GPL-3.0-only — no reuse permitted | First-party isolation tests | Architecture Owner | Evidence established |
| <a id="rule-as-24"></a>AS-24 | Crash tracker | `app/src/Misc/CrashTracker.*` | `12-native-interop-and-media.md` §6; [WP-12.05](../../planning/work-packages/12-observability-foundation.md#rule-wp-12.05) | Reference Only | Evidence that native-heavy acquisition products need crash capture; ArcForges requires user approval before upload | GPL-3.0-only — no reuse permitted | First-party test: no report sent without approval | Security and Privacy Owner | Evidence established |
| <a id="rule-as-25"></a>AS-25 | Backup manager | `app/src/Misc/BackupManager.*` | `13-data-formats-and-portability.md`; [WP-46](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) | Reference Only | Evidence on local backup expectations | GPL-3.0-only — no reuse permitted | First-party restore proof | Operations Owner | Evidence established |
| <a id="rule-as-26"></a>AS-26 | CLI and console-only mode | `app/src/Misc/CLI.*`, `tests/integration/test_console_only_mode.py` | **Accepted exclusion** for V1 | Drop | A headless acquisition CLI is beyond the accepted V1 scope; recorded as a choice | GPL-3.0-only — no reuse | — | Product Owner | Accepted exclusion |
| <a id="rule-as-27"></a>AS-27 | Licensing / activation system | `app/src/Licensing/**` (CommercialToken, LemonSqueezy, MachineID, MonotonicClock, OfflineCertificate, OfflineLicense, GuardSelfTest) | **Accepted exclusion** — Pro module, and **directly contrary to [D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)** | Drop | `LICENSE.md` §4 lists activation/licensing as commercial-only; **source not read**. Independently, a machine-bound offline licence key is exactly the unlock path **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)** prohibits in ArcForges Mobile | Commercial-only; no rights conferred | Mobile commerce-prohibition check ([WP-32.03](../../planning/work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.03)) | Licensing and Provenance Owner | Accepted exclusion |
| <a id="rule-as-28"></a>AS-28 | Platform integration — client-side decorations, native window | `app/src/Platform/{AppPlatform,CSD,NativeWindow*}.*` | `09-shared-desktop-experience.md` §windows; [WP-10.01](../../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.01) | Reference Only | Evidence on per-platform window integration expectations | GPL-3.0-only — no reuse permitted | First-party per-platform window tests | Product Owner | Evidence established |
| <a id="rule-as-29"></a>AS-29 | Test approach — integration suite | `tests/integration/**` (~20+ named scenarios incl. `test_csv_player`, `test_device_write`, `test_audio_loopback`, `test_dataset_transforms`, `test_console_ansi_vt100`, `test_data_tables`) | `../testing-and-verification-strategy.md` [F-05](../testing-and-verification-strategy.md#rule-f-05), [F-11](../testing-and-verification-strategy.md#rule-f-11), [F-18](../testing-and-verification-strategy.md#rule-f-18) | Reference Only | **Test evidence**: names the acquisition scenarios worth covering — device write, loopback, transforms, player — which ArcScope's suites must also cover | GPL-3.0-only — no reuse permitted | [WP-33](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33), [WP-34](../../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34) scenario coverage | Quality Owner | Evidence established |
| <a id="rule-as-30"></a>AS-30 | Test approach — performance, security and benchmark suites | `tests/{performance,security,benchmarks,manual}/**` | `12-quality-and-compatibility-contract.md` §§7, 9, 15; [WP-13.02](../../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.02) | Reference Only | Confirms that this product category needs performance, security and manual hardware suites as separate families — matching the eighteen-family split | GPL-3.0-only — no reuse permitted | Hardware-lab inventory ([PG-08](../open-gates-register.md#rule-pg-08)) | Quality Owner | Evidence established |
| <a id="rule-as-31"></a>AS-31 | Packaged release shape | `StartArcForges/Serial-Studio`: `bin/`, `plugins/`, `qml/`, `resources/`, `translations/`, `run.cmd` — **no installer** | `10-distribution-update-and-support.md` §1.1; `14-build-packaging-and-release.md` §5 | Reference Only | **Packaging evidence**: the native Qt reference ships as a loose directory with a launcher script and no installer — the opposite of ArcForges' signed per-user installer requirement | Commercial binary; **not executed** | Update matrix ([WP-50.02](../../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02)) | Release Engineering Owner | Evidence established |

---

## 5. Completeness check

| Check | Result |
|---|---|
| Every reviewed area in `§3` produces at least one row | **Pass** — 31 rows across all 11 areas |
| Every row carries all nine required fields | **Pass** |
| Every row has exactly one completeness state | **Pass** — 31 rows: 24 evidence established, 7 accepted exclusions, 0 unresolved |
| Every non-`Drop` row maps to an existing ArcForges requirement | **Pass** |
| Pro-module boundary respected | **Pass** — 3 rows ([AS-03](#rule-as-03), [AS-14](#rule-as-14), [AS-27](#rule-as-27)) are excluded on licence grounds with their source deliberately unread |
| Packaged binary not executed | **Pass** — directory listing only |
| Any row proposing reuse carries a provenance obligation | **Not applicable** — no row proposes reuse |

**Unresolved determinations: none.**

---

## 6. Findings that affect ArcForges design

| # | Finding | Effect |
|---|---|---|
| <a id="rule-f-as-1"></a>F-AS-1 | **Serial-Studio's licence excludes named features from GPL and reserves them commercially**, and states that source visibility confers no rights. | This is the strictest position in the programme. It creates an **authorship boundary**, not merely a reuse prohibition: three capability areas were deliberately not read. Recorded so a later reader does not mistake the gap for incomplete review. |
| <a id="rule-f-as-2"></a>F-AS-2 | **The reference's activation system is a machine-bound offline licence key** ([AS-27](#rule-as-27)). | Independent confirmation that **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**'s prohibition on a licence-key unlock path targets a real, common pattern — and that [MC-05](../../architecture/11-mobile-architecture.md#rule-mc-05) is correctly identified as the prohibition most likely to be violated by accident. **No design change**; the build check in [WP-32.03](../../planning/work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.03) already covers it. |
| <a id="rule-f-as-3"></a>F-AS-3 | **The reference stores session data in a database** ([AS-09](#rule-as-09)). | ArcForges diverges deliberately: raw capture goes to a chunked verifiable store because it is evidence. Recorded so the divergence is visible as a decision. |
| <a id="rule-f-as-4"></a>F-AS-4 | **The reference sandboxes AI file access and builds bounded context** ([AS-22](#rule-as-22)). | Independent support for [I-182](../../requirements/01-normative-glossary-and-invariants.md#rule-i-182) and [AI-02](../../requirements/products/arcscope.md#rule-ai-02). No change needed. |
| <a id="rule-f-as-5"></a>F-AS-5 | **The native Qt reference ships with no installer** ([AS-31](#rule-as-31)). | Contrast evidence for [P2-001](../../decisions/phase-2-specification-decisions.md#rule-p2-001): ArcForges' signed per-user installer requirement is a deliberate improvement over the category norm for native products. No change needed. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| <a id="rule-mt-01"></a>MT-01 | Bound to commit `639daafb`. [WP-33](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) re-checks for drift and newly introduced material; it does not re-create this matrix. |
| <a id="rule-mt-02"></a>MT-02 | **The Pro-module list in `LICENSE.md` §4 is re-read on every drift check.** A feature moving into or out of that list changes the authorship boundary. |
| <a id="rule-mt-03"></a>MT-03 | The packaged binary is never executed, at any stage. |

---

## 8. Current upstream drift check — 2026-09-28

### 8.1 Identity and review method

| Field | Value |
|---|---|
| Historical comparison point | 639daafb2fe7d324c3b2d5583d2514c8c470676f (Branch_v4.0.3, 2026-07-13) |
| Current upstream point | master at 2e6ee11350c1ab619ff41e758c1861864325cf3f (2026-09-28 13:07:29Z), a direct child of 44c9452acfbf0ca31f1c5764d225bccdd53549c1 |
| Change locator | Pinned-to-current repository tree comparison with rename detection disabled: 5,270 changed path records across additions, modifications and removals. Paths locate drift; they do not establish implementation behaviour. The incremental commit changes REUSE.toml plus alarm, audio, API, consent, test, translation and public-help material. |
| Current material read | Public README.md, DISCOVER.md, focused doc/help/** pages, current licence instruments and REUSE.toml; names and locations of changed source, test and packaging paths. |
| Binary handling | No packaged binary was opened or executed. |

The focused public help-page set reviewed under doc/help/ was Command-Palette.md, Console-Annotations.md, Drivers-EtherNet-IP.md, Drivers-IEC-104.md, Drivers-OPC-UA.md, Drivers-S7.md, Extensions.md, InfluxDB.md, Macros.md, Problem-Center.md, Remote-Dashboard.md, Session-Database.md, Session-Reports.md, Widget-Extension-Development.md, Aural-Alerts.md, API-Reference.md, Control-Script.md, JavaScript-API.md, Notifications.md and Widget-Reference.md. Internal developer/agent specification material was not treated as product authority.

The original 31 rows remain the evidence record for the pinned commit. This check updates only their current path/capability disposition. The reference-source authorship boundary is preserved: no implementation under the baseline Pro exclusions was read. Current publicly documented commercial-only material, including direct industrial drivers, MQTT/Sparkplug, the AI Assistant and Pro visualisation surfaces, is treated as excluded; its source implementation was not read. No code is proposed for reuse.

The table below accounts for every existing row family with path-level drift. It deliberately separates historical evidence from current claims: where a behaviour or product claim comes only from current documentation, it is not presented as source-verified.

| Row | Current path or documented drift | Existing ArcForges target or accepted exclusion | Current disposition |
|---|---|---|---|
| AS-01 | Connection/device code is reorganised under core/Devices/IO/, including ConnectionManager and DeviceManager families. | I-466, SD-01, WP-33.00 | Reference Only; the historical separation remains a category cue, not a source-use proposal. |
| AS-02 | Transport code is reorganised under core/Devices/ and core/Protocols/. Current public docs add WebSocket/HTTP to the GPL network list and document Pro OPC UA, S7comm, EtherNet/IP and IEC 60870-5-104 clients. | SD-09, WP-33.00; the accepted V1 transport subset is intentionally narrower. | Reference Only for generic transport coverage. The additional Pro industrial clients are Drop for this scope; no implementation was read. |
| AS-03 | Current docs identify MQTT with Sparkplug B support as Pro; current MQTT implementation paths remain outside review. | Accepted exclusion: Pro/commercial MQTT; no accepted V1 requirement. | Drop. |
| AS-04 | The rolling buffer is now located at core/Core/CircularBuffer.h. | SE-04, WP-33.02 | Reference Only; no source reuse. |
| AS-05 | Framing and checksum paths are split across core/Pipeline/IO/, core/Pipeline/DataModel/ and core/Core/{IO,Checksum}/. Current docs also describe built-in, JavaScript and Lua parsers and parser templates. | Decoder/checksum requirements and WP-34.03 | Reference Only for framing and failure visibility; parser implementations and templates are not adopted. |
| AS-06 | Frame, table and consumer code is split across core/Pipeline/DataModel/ and core/Core/DataModel/; current docs describe dataset transforms and computed variables. | Existing channel/signal/event model and WP-33.03 | Reference Only. |
| AS-07 | DSP and hot-path paths are split between core/Pipeline/ and core/Core/, including SIMD and hot-path helper families. | Throughput requirement, WP-13.02 and WP-33.01 | Reference Only; the path change alone is not performance evidence for ArcForges. |
| AS-08 | Importer paths are reorganised under core/Pipeline/DataModel/Importers/; current docs describe DBC multiplexing/J1939/ISO-TP and Modbus register-map import. | Accepted V1 importer exclusion; later-adapter evidence only. | Drop for the importers and extended protocol integrations; they do not enlarge V1. |
| AS-09 | Session storage is reorganised under core/Storage/Sessions/; the current help centre uses the “Historian” name for the SQLite session feature. | SE-14, WP-33.04; deliberate divergence to the chunked verifiable capture store remains. | Reference Only. The current database implementation does not replace the ArcForges storage decision. |
| AS-10 | Player/replay code is reorganised under core/Storage/{CSV,MDF4,Sessions}/; current docs retain replay and describe database-backed session replay. | SD-10, WP-33.05 | Reference Only; ArcForges' replay-label and device-identity constraints remain authoritative. |
| AS-11 | Export paths are reorganised under core/Storage/; current docs add a Pro InfluxDB 2.x live sink alongside CSV/MDF4/session exports. | Existing export/precision requirements and WP-35.04; no ArcScope requirement authorises a live InfluxDB sink. | Reference Only for established export evidence. The new InfluxDB sink is Drop. |
| AS-12 | Session-report paths are reorganised under core/Storage/Sessions/; current docs describe richer self-contained HTML/PDF reports. | Report traceability and WP-34.06 | Reference Only; source/session/configuration traceability remains the ArcForges requirement. |
| AS-13 | Dashboard widget paths remain documented as a broad and changing vocabulary; current README distinguishes GPL widgets from additional Pro visualisation/output surfaces. | Existing visualisation scope and WP-34.00 | Reference Only for category vocabulary. Pro 3D/XY/Waterfall/Image/Canvas and output implementations remain excluded. |
| AS-14 | Pro 3D/XY visualisation paths are reorganised; the current docs use “Canvas” for the surface called “Painter” at the baseline. | Accepted Pro-module exclusion. | Drop; no Pro visualisation implementation was read. |
| AS-15 | The web-view widget paths remain present; web surfaces also appear in other product areas. | Accepted exclusion: no ArcScope requirement and a large security surface. | Drop. |
| AS-16 | Alarm monitor paths move under core/Ui/UI/; the current tree adds core/Ui/UI/Alarms/ annunciator/audio path names, and new Aural-Alerts help describes a master alarm panel available in every build. | Existing trigger/alarm distinction and WP-34.01 | Reference Only for alarm-state/annunciation category evidence; no sound implementation is reused or newly required. |
| AS-17 | Notification code moves under core/Pipeline/DataModel/; current help adds console byte annotations, Problem Center/Connection Diagnostics and Warning/Caution/Advisory points feeding the annunciator. | Durable event-log/attention requirements and WP-10.04; decoder evidence also maps to WP-34.03. | Reference Only for event/diagnostic concepts; no new ArcScope requirement is inferred. |
| AS-18 | Project Editor paths are reorganised and expanded in current public help with workspaces and project configuration flows. | Existing ArcScope project/configuration model and WP-33.00 | Reference Only; current workflow is not a requirement to reproduce. |
| AS-19 | Command/API code is reorganised under core/Api/ and core/Core/Api/; current docs add a command palette, in-process Macros and explicit remote consent prompts for device writes and project-script changes, plus a per-project prompt before any script launches a process. | Existing API/integration vocabulary and WP-35.00; shared approval principles in AD-05 and R3. | Reference Only for explicit approval as a security pattern. The exact consent persistence, dispatch model and blanket headless override are not adopted. |
| AS-20 | The gRPC implementation remains under app/src/API/GRPC/ and has changed. | Accepted source exclusion; ArcForges uses its own first-party protocol. | Drop; no reference implementation reuse. |
| AS-21 | Path-policy code is reorganised under core/Api/API/. | Existing resource-identity/path policy and AI-08 | Reference Only. |
| AS-22 | AI paths are reorganised/expanded; current README classifies the AI Assistant as Pro. | Existing bounded-context requirements in I-182 and AI-02; current Pro implementation is outside the authorship boundary. | The pinned evidence remains historical Reference Only; current Pro AI additions are Drop and their implementation was not read. |
| AS-23 | The extension surface is expanded in current docs to include in-process QML widget extensions as well as external API-connected plugins. | WP-41; ArcForges' accepted out-of-process extension model deliberately diverges. | Reference Only for external-plugin category evidence. In-process widget extensions are Drop. |
| AS-24 | Crash tracking moves under core/Ui/Misc/. | Crash-report consent and WP-12.05 | Reference Only. |
| AS-25 | Backup management moves under core/Ui/Misc/. | Existing portability/recovery requirements and WP-46 | Reference Only. |
| AS-26 | CLI code remains in the product tree and is expanded/documented for additional driver configuration. | Accepted exclusion: headless acquisition CLI is outside accepted V1 scope. | Drop. |
| AS-27 | Current licensing adds EULA.md, TRADEMARKS.md, REUSE.toml, new SPDX texts and updated commercial terms; licensing/activation implementation remains unreviewed. | Accepted exclusion: commercial-only activation/licensing and D-022. | Drop for current activation/licensing implementation; see the current licence re-verification below. |
| AS-28 | Platform code is split between core/Pipeline/Platform/ and core/Ui/Platform/, including CSD/native-window families. | Existing window/platform integration requirements and WP-10.01 | Reference Only. |
| AS-29 | Integration/unit test families are reorganised and substantially expanded under app/tests/ and tests/. | Existing verification strategy F-05, F-11, F-18, WP-33 and WP-34 | Reference Only; path/test names are not ArcForges test evidence. |
| AS-30 | Performance, security, benchmark and manual test materials change alongside the test-tree refactor. | Existing quality families, WP-13.02 and PG-08 | Reference Only; no upstream result is substituted for a first-party gate. |
| AS-31 | Packaging/build material now includes current app/deploy/ platform assets and release/build paths; the pinned loose-directory observation is not evidence of the current release artifact shape. | WP-50.02; signed per-user distribution requirements remain authoritative. | Reference Only. Current release artifacts were not executed or exhaustively inspected; the historical “no installer” claim is baseline-only. |

### 8.2 Current licence and provenance re-verification

The current upstream root LICENSE.md (dated 2026-08-29) now states that per-file SPDX declarations or REUSE.toml are authoritative. It says files declared GPL-3.0-or-later OR LicenseRef-SerialStudio-Commercial may use either arm; the GPL option carries the GPL's own terms with no extra commercial-use restriction. Files marked only LicenseRef-SerialStudio-Commercial are proprietary Pro modules. This differs materially from the baseline's GPL-3.0-only description and must not be conflated with it.

The current commercial-source instrument still says visibility grants no right to compile, use or distribute Pro source without an active commercial term, and bars distribution of Pro modules/builds. Official precompiled binaries now route to a separate 2026-08-29 EULA with a 14-day trial; TRADEMARKS.md states a separate trademark policy. The EULA and commercial terms contain [COUNSEL: ...] annotations. This report records those documents as published and makes no legal-validity determination.

REUSE.toml adds explicit file-scoped declarations for first-party material and third parties. Its current entries identify, among others, open62541 as MPL-2.0, Mbed TLS as Apache-2.0 for this project, HIDAPI's alternative expressions, and the existing MIT/BSD families; it states that libplctag is fetched at configure time rather than vendored. The current license inventory includes Apache, BSD, GPL-3.0-or-later, MIT, MPL, OFL, Zlib and other SPDX texts. The latest drift commit adds app/rcc/sounds/** to the existing first-party asset annotation, so current bundled sound assets are declared GPL-3.0-or-later OR LicenseRef-SerialStudio-Commercial. LICENSE.md, EULA.md, TRADEMARKS.md and the SPDX text files are unchanged by that commit. These declarations are provenance evidence only and do not grant ArcForges rights to reuse upstream expression. Under D-013, no reference source is copied, translated or ported; current Pro-source visibility is not treated as permission.

The baseline LP-01 through LP-04 findings remain accurate only for the pinned baseline. For the current point, the governing disposition is: GPL-classified content remains Reference Only under D-013; current commercial-only and insufficiently classified surfaces are Drop; vendor content is not reused. The current README's Pro classification was used as a conservative no-read boundary for new Pro capabilities. Aural alerts are publicly stated to exist in every build, while current REUSE metadata assigns the bundled sound assets the dual-license expression; the sound files themselves were not opened or played. No packaged binary or Pro implementation was inspected.

### 8.3 Newly documented capability and material disposition

| Newly documented or materially expanded material | Existing ArcForges mapping or accepted exclusion | Disposition |
|---|---|---|
| WebSocket and HTTP network transports in the GPL edition. | Generic transport coverage in SD-09 and WP-33.00. | Reference Only; category evidence, no implementation reuse. |
| OPC UA tag browsing, direct S7comm/EtherNet/IP/IEC 60870-5-104 PLC clients and MQTT Sparkplug B. | SD-09 deliberately accepts a narrower V1 subset; MQTT is the accepted AS-03 Pro exclusion. | Drop for these additional Pro integrations; do not read their implementation or expand V1. |
| Built-in/JavaScript/Lua parser choices and script-template catalogue. | Existing framing/decoder requirements and WP-34.03 (AS-05). | Reference Only for generic decoding needs; no source or template reuse. |
| Modbus register-map and DBC import, including extended multiplexing/J1939/ISO-TP claims. | Accepted V1 importer exclusion (AS-08); later-adapter evidence only. | Drop; no importer or protocol expansion. |
| InfluxDB live time-series sink. | No accepted ArcScope requirement for this destination; distinct from existing export evidence (AS-11). | Drop; no new requirement is inferred. |
| Command palette, workspace navigation, project editor workflows and in-process Macros. | Existing project/configuration and command/API evidence (AS-18, AS-19; WP-33.00, WP-35.00). | Reference Only as product-category observations; do not add a workflow requirement. |
| Console byte annotations, Problem Center and connection diagnostics. | Existing decoder-failure and durable attention evidence (AS-05, AS-17; WP-34.03, WP-10.04). | Reference Only; ArcForges requirements remain unchanged. |
| QML widget extensions running inside the host process. | WP-41 explicitly chooses an out-of-process extension boundary (AS-23). | Drop; directly divergent trust model. |
| Remote read-only dashboard mirroring over the API server. | No accepted ArcScope remote-mirroring requirement; existing API evidence is limited to AS-19. | Drop; no new remote-access requirement is inferred. |
| Current Pro AI Assistant additions. | Existing bounded-context requirement vocabulary (I-182, AI-02); current README classifies the feature as Pro. | Drop for current implementation and additions; historical AS-22 remains pinned evidence only. |
| Current commercial-source, binary-EULA, trademark and per-file third-party licensing model. | Existing authorship boundary and licence exclusion (AS-27, D-013, D-022). | Reference Only as licensing/provenance evidence; no code rights or licence conclusion inferred. |
| Current platform packaging/build tree and release documentation. | Existing signed distribution requirement (AS-31, WP-50.02). | Reference Only; do not infer the current artifact shape from the pinned directory or execute a binary. |
| Newly added internal developer/agent specifications and planning notes under doc/claude/specs/. | Not product requirements or accepted ArcScope evidence. | Drop from product-evidence scope; not mined for requirements. |
| Expanded upstream unit, integration, performance, security, benchmark and fixture materials under app/tests/, tests/ and scripts/. | Existing test-family rows AS-29 and AS-30; first-party acceptance evidence remains governed by the ArcForges test strategy. | Reference Only for test-family names; no upstream test result is evidence of ArcForges conformance. |
| Added/updated third-party component trees and notices, including Mbed TLS, open62541 and configure-time libplctag metadata. | Existing provenance boundary (AS-02, AS-27) and D-013; no third-party source reuse is proposed. | Drop as source material; retain license identity only as provenance evidence. |
| Public Aural Alerts help describes ISA-18.1 alarm sequences, IEC 60601-1-8 sound signatures, priority points, master annunciator actions and application event sounds, available in every build. | Alarm/trigger distinction and notification evidence (AS-16, AS-17; WP-34.01, WP-10.04). | Reference Only for alarm-state and operator-attention vocabulary. Sound behaviour and source remain unadopted; no ArcScope audio-alert requirement is added. |
| User-selected WAV sounds and per-band/per-channel project sound mappings. | No accepted ArcScope requirement for custom sound assets; existing path/resource security principles remain authoritative. | Drop as an ArcScope feature; no sound asset or path-handling implementation is reused. |
| Remote API/MCP/gRPC device-write and project-script consent prompts, plus a per-project process-launch prompt for scripts. | Shared explicit-approval principles AD-05/R3 and existing API integration evidence AS-19/WP-35.00. | Reference Only for an operator-confirmation pattern. Exact grants, storage lifetime, first-party script privileges and the environment-variable headless override are not adopted. |
| Unrestricted in-process project-script API access described alongside remote consent controls. | ArcForges' least-privilege/security and out-of-process integration boundaries (SE-06, WP-41); accepted reference divergence. | Drop as an access-control model; it does not establish ArcForges permission or script-sandbox policy. |
| New annunciator, audio, consent-gate, API and test files in the latest upstream commit. | Existing alarm, API-security and test-family rows AS-16, AS-19, AS-29 and AS-30. | Path names and upstream tests are Reference Only; no current implementation behaviour was source-reviewed or treated as ArcForges evidence. |

### 8.4 Drift-check completeness

| Check | Result |
|---|---|
| All historical row families AS-01 through AS-31 checked for current path/document drift | **Pass** — every row family is dispositioned in §8.1; path observations are not presented as behaviour verification. |
| Every current public capability/material group identified in the reviewed README/help material has a requirement mapping or explicit exclusion | **Pass** — §8.3 maps each group to an existing row/authority or records an accepted Drop. |
| Current upstream licence instruments and REUSE/SPDX inventory re-verified, including identity of accompanying texts | **Pass** — §8.2; no vendor-source reuse or legal-validity opinion made. |
| Original baseline facts remain distinguishable from current drift | **Pass** — §§1–7 stay bound to 639daafb; current claims are separately dated and bound to 2e6ee11350c1ab619ff41e758c1861864325cf3f. |
| Pro-module authorship boundary and packaged-binary restriction respected | **Pass** — current Pro implementations were not read; no packaged binary was opened or executed. |
| Any source reuse or new ArcScope requirement proposed | **No** — all current material is Reference Only or Drop; existing ArcForges requirements are unchanged. |

**Current drift determinations:** none require changing ArcScope requirements or this matrix's 31 baseline dispositions. The current source's commercial/licensing and product surface is materially different from the pinned baseline; subsequent drift checks must compare against a newly authorised source identity rather than silently rolling this report forward.
