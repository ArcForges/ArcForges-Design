# Content and Extension Isolation

> Status: **Authoritative** — Phase 2; [P2-007](../decisions/phase-2-specification-decisions.md#rule-p2-007) exercises the controlled isolation exception under D-016.
> Companions: [native boundary](12-native-interop-and-media.md), [extension platform](15-extension-platform-architecture.md), [security](08-security-architecture.md).

## 1. Ownership and trust boundary

| # | Rule |
|---|---|
| IS-01 | `ArcForges.ContentSandbox` is a first-party C# Native AOT helper, on demand, bound to its parent session, without UI, model loop, network, credentials or persistent product state. It loads the minimum approved parser/codec C APIs or owned C ABI libraries. Product domain, editing decisions, jobs, scheduling and authority remain C# in the owning product. This is not a C++ business worker or installed service. |
| IS-02 | Hostile PDF, compressed images, supported document imports, media demux/decode and interchange parsing execute behind this boundary. It adds no unsupported format or full Office feature. The host receives validated bounded text/geometry/pixels/audio or a typed parsed representation, never executable markup or parser-owned pointers. |
| IS-03 | Parser crash, access violation, hang, memory exhaustion or malformed result terminates that helper invocation. The parent preserves its committed domain state and returns the named unavailable/corrupt-content result; Notes uses a metadata/placeholder view, Slate reports the affected asset/job. A C ABI status code cannot contain an access violation in the same process. |
| IS-04 | The parent brokers read-only input handles and explicitly sized output buffers. The helper has no product-database directory, home directory, token cache, ambient network endpoint or inherited secret. Original paths and arbitrary open-file requests are not capabilities. Validate dimensions, counts, lengths, ranges and checksums again on the parent side. |
| IS-05 | CPU/memory/wall-time/process-count limits are enforced before untrusted code runs. A parent liveness channel, OS containment and bounded supervisor timeout terminate the helper tree on parent death. Idle helpers exit; writable scratch is invocation-scoped and removed by the parent cleanup journal after any crash. |
| IS-06 | Content-helper control uses a private parent-bound channel with generated bounded DTOs. Large data uses brokered per-invocation file/shared-buffer handles; this is not product-to-product bulk RPC or a global shared-memory pool. The child cannot enumerate or mint handles. Supported GPU buffer transfer needs RID-specific validation; otherwise use bounded CPU buffers, never an unsafe in-process parsing fallback. |

## 2. Platform enforcement profiles

These are implementation designs, with release-blocking OS tests below; prose is not evidence that a sandbox already works.

| Platform | Content-parser baseline | Executable extension baseline |
|---|---|---|
| Windows | Launch suspended into an AppContainer with no network capabilities and narrowly ACL-scoped assets/handles; attach a non-breakaway Job Object with kill-on-close, memory and process limits before resume. Restrict inherited handles and environment. | A per-package AppContainer identity, private state directory and broker channel. No product-store ACL or ambient user credential. Resource/job limits apply to the complete child tree; network/file access is brokered per grant. |
| Linux | Enforce a supported Landlock filesystem profile **before threads or untrusted parsing**, `no_new_privs`, seccomp network/process/ptrace restrictions, and isolated namespace/resource profile. Deny direct socket creation/connect for content; pass only broker descriptors. Require the declared kernel ABI and namespace capabilities, close extraneous descriptors. | Same filesystem/process restrictions with per-package state; broker permitted network requests and file operations. JIT/process requirements are separately declared and do not remove filesystem/network restrictions. Unsupported kernel/profile is a typed refusal. |
| macOS | A separately signed App-Sandboxed XPC helper with its own restricted entitlements, not `inherit` from the full application. No network, app-group/product container or broad file entitlement. Broker input descriptors/data and terminate the session on connection loss; validate signed helper identity. | Executable packages require a signed sandbox-compatible runner/service profile with a separate container. Dynamic-runtime entitlements, if needed, are explicit and verified per package/RID. It never inherits the owning app's file/network privileges. A package lacking a proven profile cannot execute. |

AppContainer supplies resource isolation; the Job Object supplies lifecycle/resource limits ([Microsoft AppContainer](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation), [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)). Landlock restrictions depend on kernel ABI and pre-opened descriptors; this design combines them with other OS controls rather than assuming a pathname rule also denies networking ([Linux kernel](https://www.kernel.org/doc/html/latest/userspace-api/landlock.html)). macOS privilege separation uses distinct XPC/App Sandbox entitlements; inheritance is not a narrower helper sandbox ([Apple](https://developer.apple.com/library/archive/documentation/Miscellaneous/Reference/EntitlementKeyReference/Chapters/EnablingAppSandbox.html)).

The exact syscall/entitlement/handle allowlists are versioned packaging inputs and verified on every supported RID. Probe the actual enforced profile before execution. Missing enforcement returns `security.isolation_unavailable`; it never silently falls back to same-user full trust. A required first-party feature cannot claim release acceptance while its profile is unavailable.

## 3. Extensions and authorised machine tools

| # | Rule |
|---|---|
| IX-01 | Process separation alone contains some crashes, not authority. An executable extension's grants are enforced both at broker dispatch and by the OS profile that prevents bypass through direct file/network/process APIs. Product DB/credential reads are denied even when the package knows their paths. |
| IX-02 | One package installation has one process identity and private state boundary. Every broker request carries its installation/session, grant generation, capability, target and nonce. Revocation cancels/denies subsequent requests and terminates a process whose profile cannot be reduced. No shared Hub credential is handed out. |
| IX-03 | Network and file grants are scoped broker operations by default. A broker validates destinations, redirects, resource ownership, path/handle boundaries, byte/time limits and audit metadata. Passing a raw credential/direct-network capability is a separately declared sensitive permission, not a generic implementation convenience. |
| IX-04 | User-authorised stdio MCP or explicit machine tools can have broader machine authority. Their UI states that trust scope and approval; they are not advertised as capability-sandboxed extensions. Cloud still reaches them only through the durable authorised device bridge. No extension silently upgrades itself to that category. |
| IX-05 | Extension UI remains declarative native Avalonia controls; no third-party in-process assembly or browser renderer is added. Sandbox failure may quarantine a package; it cannot bypass package provenance or compatibility checks. |

## 4. Verification and ownership

| Deliverable | Required evidence | Work package |
|---|---|---|
| Common C# helper/broker and RID launch profiles | Real child attempts product DB/token reads, outbound TCP/UDP/loopback, sibling-process access, spawn escape and oversized output; deny at OS boundary, with bounded resource exhaustion and parent-death cleanup | [WP-11.09](../planning/work-packages/11-security-foundation.md#rule-wp-11.09) |
| PDF/image viewer path | Native access violation, malformed PDF/image, decompression bomb and stalled parser leave the parent running and its document unchanged; repeat after packaging/signing | [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) and [PG-12](../assurance/open-gates-register.md#rule-pg-12) |
| Media/interchange | Malformed demux/OTIO input, decode timeout and helper death fail the affected job, preserve committed edits, clean broker buffers and support restart; throughput measured with isolation active | [WP-36.02](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.02), [WP-37.01](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.01), [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) |
| Executable extension | Malicious real package cannot read another package/product store or call the network outside the broker; revoke during invocation, restart and uninstall preserve denial | [WP-41.00](../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.00) and [PG-22](../assurance/open-gates-register.md#rule-pg-22) |

Pure managed unit tests or a mocked launcher cannot satisfy OS isolation evidence. A first-party parser library's ABI, licence, package hashes and Native AOT publish remain separate required gates. GPU/device-driver calls that necessarily remain in the product process still have an acknowledged crash/recovery risk; that is not reused as a promise that an in-process hostile parser is contained.

## P2-009 packaged helper ownership

DesktopPlatform publishes the signed ContentSandbox/Broker/Contracts and per-RID parser assets through the [package registry](01-solution-and-project-layout.md#12-package-and-native-distribution-registry). Each product selects only its approved parser profile. The existing OS-enforced handle, filesystem, network, process and lifetime rules above are unchanged. Product parsing never moves into the UI process merely because a native dependency became a NuGet package. This private helper protocol (including XPC on macOS) is an explicit exception to business gRPC.
