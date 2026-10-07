# Local product UI component-test support

<a id="rule-p2-074"></a>

Status: Authoritative supporting decision for APP.03 — P2-074.

The production ArcScope application already selects Avalonia.Desktop and Avalonia.Themes.Fluent 12.1.3. The genuine shared AST10 component suite selects Avalonia.Headless 12.1.3 in DesktopPlatform `Directory.Packages.props` for `AssistantAvaloniaTests`, and exercises actual controls with `HeadlessUnitTestSession`. ArcScope currently selects the existing xunit.v3.mtp-v2 runner. Its real application control source is owned by APP.03; the current annotation workspace already composes the real owner endpoint, durable SQLite journal, fresh security gate and explicit R2 approval coordinator.

The minimum supporting change adds Avalonia.Headless 12.1.3 as a private test-only reference in the existing `tests/ArcForges.ArcScope.Tests/ArcForges.ArcScope.Tests.csproj`, with a conditional central selector for that project. The same test project references the actual `src/ArcForges.ArcScope/ArcForges.ArcScope.csproj`; that actual app grants `InternalsVisibleTo` only to the existing `ArcForges.ArcScope.Tests` assembly for these owned internal controls. Preserve existing Core/test friend declarations. No new public API, application, test runner, source-reference substitute, production fake authority or hidden shared runtime is introduced.

Generate the affected test lock with the actual SDK and exact approved package source/version; preserve the existing production selectors, all native/runtime identities, immutable historical receipts and current licence/provenance/dependency/admission gates. Test helper source remains in the existing owned test tree and uses the actual owner fixture/store/gate. It may substitute only genuinely unavailable external ports and must identify those limits. Real protected custody, live Cloud registration/deployment, OS isolation, NativeAOT installed behavior and assistive/manual acceptance remain separate applicable gates.

Meaningful ordinary components exercise the actual user-owned complete Replay configuration and current ScopeSession response, actual R2 request/decision/execute and retained original request/command after lost replies, disabled/busy/toggled controls, cancellation and fresh actor refusal, privacy clearing before slow external drain, and shared concurrent Close/Dispose ownership and failure. Headless control behavior is not presented as physical OS acceptance. The complete ArcScope host, shared ShellSession/Lifecycle and full intended shared AI assistant remain required; this narrow support cannot close APP.03 implementation or whole acceptance by itself.

Only APP.03 write support and notes are extended. All incoming task identities, start/completion edges, outcome, obligations, baselines and unrelated fields remain unchanged.
