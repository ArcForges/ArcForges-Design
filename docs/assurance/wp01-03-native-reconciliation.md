# WP01.03 native reconciliation evidence

Authority: [WP01.03](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.03) and the merged [native reconciliation policy](wp01-03-native-reconciliation-policy.md). This receipt covers current native ownership and the independent test-oracle relocation; functional native capability admission remains separately scheduled.

## Source disposition

[DesktopPlatform PR 54](https://github.com/ArcForges/DesktopPlatform/pull/54) moves the three legacy NativeInterop ABI oracle files into NativeAbiTests. Two files are byte-identical after line-ending normalization; NativeSmoke changes only two public declarations to internal because the destination is a test executable. The test project owns its unsafe declarations and no longer references NativeInterop. The original and destination source hashes are retained in the [machine-readable receipt](wp01-03-native-reconciliation.json).

NativeInterop remains a non-packable name scaffold with no native bindings. Production imports remain in the Media, Colour, Image and Otio capability projects. The bounded source guard rejects unowned or duplicate declarations in the current LibraryImport source format, DllImport declarations and explicit production project references into tests. An actual injected duplicate production binding was rejected before being removed. This is not a general semantic C# or evaluated MSBuild analyzer.

| Native family | Verified disposition |
|---|---|
| Media | Keep in DesktopPlatform; existing ABI version/build-info/error probes and matching managed/runtime package. |
| Colour | Keep in DesktopPlatform; existing ABI probes and matching managed/runtime package. |
| Image | Keep in DesktopPlatform; existing ABI probes and matching managed/runtime package. |
| OTIO | Keep in DesktopPlatform at the selected official v0.18.1 overlay; no alternate implementation or version upgrade. |
| Metal | Retain macOS-only probe source; not a Windows runtime package or functional graphics acceptance. |
| MDF | Retired ABI remains absent and excluded; no replacement placeholder created. |
| Shared native ABI | Keep common owned C ABI support in DesktopPlatform. |

No native exports, package allowlist, upstream recipes or provenance component profiles changed. Read-only source scans of clean ArcNotes, ArcScope and ArcSlate commits found no native import/loader/oracle/PlatformBroker declarations matching the recorded scan. There was no matching product copy to migrate. The scan scope and exact commits are recorded, not extrapolated to future product behavior.

## Review and verification

The local Windows solution built Release|x64 with zero warnings and errors, and its freshly built native DLLs passed the managed ABI test. Five architecture tests, 63 engineering policy tests and 41 tooling tests passed. Locked restore, managed Release build, formatting, source/native provenance and the nine-owner snapshot reconciliation passed.

CI review found that the existing reconciliation checker rejected every project-file content change as snapshot drift. The fix preserves the original observation and admits only the exact reviewed NativeAbiTests replacement blob, bound to the WP01.03 producer and merged Design authority. Other content drift, missing/extra projects, historical identity changes and source escapes remain rejected. Negative fixtures cover the reviewed-update boundary. The fixed source was reviewed again before merge.

The [PR gate](https://github.com/ArcForges/DesktopPlatform/actions/runs/35554487715) passed all 20 checks on 152d2682105d005d88b46893f930dffccb2da4df, including actual Windows native compilation/tests, Linux/Windows package consumers, Native AOT, C17 and negative loader fixtures. The merge is 6cb08997bb35299df86a6434606d8e24cf5a4d97. The [main publication run](https://github.com/ArcForges/DesktopPlatform/actions/runs/35554989640) passed on attempt 2 and published all ten packages as `1.0.0-ci.17.1`. Attempt 1 passed native compilation and four CTests but received HTTP 403 while fetching Microsoft legal files; retrying failed jobs preserved the allocated version. Both original URLs also downloaded locally with matching reviewed hashes.

The merged candidate passed local package identity verification and a second independent run of all five JIT/Native AOT consumer cases, the packaged C17 caller and four negative loader fixtures. All ten public NuGet packages were then downloaded and compared with the CI candidate: every ZIP payload entry matched by SHA256, excluding only NuGet's added repository signature. The public receipt records actual URLs, candidate/public archive hashes and verification time. Public indexing delay was observed and resolved without republishing. The DesktopPlatform primary was fast-forwarded to the merge; its tree matches the reviewed PR tree. No external prerequisite blocks this substep.

## Remaining functional boundaries

ContentSandbox is still a scaffold, with no signed PlatformBroker or hostile-input containment claim. Generated helper contracts belong to WP03, transport to WP08, restricted helper enforcement to WP11 and parser composition/functional Instruments, Pdf and Graphics to WP13. The current probes accept no hostile media content. macOS Metal execution and additional RIDs are outside this Windows admission. Branches and worktrees are retained.
