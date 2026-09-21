# WP01.03 native reconciliation profile

Authority: [WP01.03](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.03), [native package registry](../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [isolation](../architecture/24-content-and-extension-isolation.md), and [functional ABI](../architecture/contracts/06-native-functional-abi.md).

## Current source and bounded correction

DesktopPlatform b7744f3ffdeae161d8a3e34243aad3b8e8b47978 already owns Media, Colour, Image and Otio managed packages and win-x64 runtime packages, with common Native.Abstractions, pinned vcpkg and official OTIO 0.18.1. MDF is absent/excluded. Metal is a retained macOS-only probe, not an admitted Windows runtime or functional Graphics implementation. Instruments/Pdf/Graphics functional production remains WP13. No alternative native engine is selected here.

The current BuildingBlocks.NativeInterop contains a second set of ABI probe bindings used by NativeAbiTests; it is not an admitted package. Move those unchanged independent oracle sources to NativeAbiTests, preserving their null-pointer/layout/error tests and native symbol compatibility. Keep the non-packable placeholder project identity to avoid unrelated project-map churn. It must contain no native bindings. Capability-specific production declarations remain exclusively in src/Native; their package bytes, APIs and native sources need no behavioral change. Record the original and destination source identities and update the first-party provenance inventory. A repository architecture check prevents these bindings from reappearing outside their capability owner. Independent direct ABI oracle bindings are test-only and cannot be imported by production projects.

Inspect all three product source trees for duplicate native bindings, native source imports or MDF adoption before recording no transfer required. Existing immutable package consumers and source/NOTICE history remain compatible. Product source is not built through an adjacent repository.

## Parser prerequisite and evidence classes

There is no implemented signed PlatformBroker in the current source. The ContentSandbox executable is a Hello scaffold. Architecture 24 already assigns generated helper contracts to WP03, transport to WP08, restricted launch/test containment to WP11, and functional parser composition to WP13. WP01 retains only ABI version/build-info/error probes: they accept no untrusted content. Do not add risky parser entry points or report containment as implemented. Any later parser use requires those actual signed helper and OS enforcement proofs first; the requirement is preserved, not waived.

## Verification and merge sequence

Before implementation, review and merge this documentation repair. Then move the independent oracle without changing its behavior, add the production-binding boundary check, update provenance and record native component dispositions. Run locked managed restore/build/architecture checks, actual managed/native ABI tests, provenance/runtime/reconciliation checks and applicable formatting/hooks. Review the complete implementation PR and wait for every applicable native, Windows/Linux, package-consumer and security gate before merging. Verify the merged candidate and actual public package bytes, including isolated Native AOT/C17 consumers and negative loader fixtures. Retain branches/worktrees and record remaining functional/RID/helper gates with their scheduled owners. Probe success cannot close WP13 or commercial product readiness.
