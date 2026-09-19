# WP00.03 implementation evidence

> Status: Execution evidence for the inspected revisions, verified 2026-09-19 UTC.
> Owning substep: [WP-00.03 — Reuse and provenance process](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.03).

The nine current implementation owners satisfy this substep's process, admission,
source reconciliation, CI and affected-distribution obligations. Each final PR was
reviewed; code PRs merged after all applicable checks passed. Public packages and
deployed/installed consumers were verified after merge. The corresponding primary
checkouts were pulled and verified clean. Historical records, branches and worktrees
remain retained. This receipt completes WP00.03; it does not begin WP00.04 or close
later product and commercial-operation gates.

## Accepted source and publication identities

These are the final verification revisions, including earlier admissions and
repairs retained in their Git history. Each repository keeps exact source and
artifact receipts under its owning provenance/evidence conventions.

| Owner and final PR | Merged commit | Published version | Main CI/publication |
|---|---|---|---|
| [Contracts](https://github.com/ArcForges/Contracts/pull/22) | `aa2f187a4adae8ee4f79cee192c0d382cb7fec7f` | `1.0.0-ci.54.1` | [passed](https://github.com/ArcForges/Contracts/actions/runs/35423529896) |
| [DesktopPlatform](https://github.com/ArcForges/DesktopPlatform/pull/50) | `5cb1121dc2312a10fba4424005ec29b4ad5d0113` | `1.0.0-ci.13.1` | [passed](https://github.com/ArcForges/DesktopPlatform/actions/runs/35429555877) |
| [ArcNotes](https://github.com/ArcForges/ArcNotes/pull/4) | `e40423a1b14ce8341de35748cc2a093c7c9b77a7` | `0.1.0-ci.8.1` | [passed](https://github.com/ArcForges/ArcNotes/actions/runs/35425608146) |
| [ArcScope](https://github.com/ArcForges/ArcScope/pull/4) | `d247dcff36fd1123a70e5e59967a9b2294a2eeac` | `0.1.0-ci.8.1` | [passed](https://github.com/ArcForges/ArcScope/actions/runs/35426873548) |
| [ArcSlate](https://github.com/ArcForges/ArcSlate/pull/4) | `b0d255f54fb560a534cc493d5645ca4bc7b4bd0e` | `0.1.0-ci.8.1` | [passed](https://github.com/ArcForges/ArcSlate/actions/runs/35427484761) |
| [Cloud](https://github.com/ArcForges/Cloud/pull/4) | `3165c97cccd3ea1e0b230d66e22ab9c775ca19d8` | `0.1.0-ci.16.1` | [passed](https://github.com/ArcForges/Cloud/actions/runs/35431961965) |
| [AI](https://github.com/ArcForges/AI/pull/9) | `b26f05c73271693636d89a83a24f8cd66eac26b2` | `0.1.0-ci.24.1` | [passed](https://github.com/ArcForges/AI/actions/runs/35434201026) |
| [Web](https://github.com/ArcForges/Web/pull/7) | `84939ca1fde0f0653d2cb4d8b8f9e5dd1057abb5` | `0.1.0-ci.22.1` | [passed](https://github.com/ArcForges/Web/actions/runs/35437014881) |
| [Mobile](https://github.com/ArcForges/Mobile/pull/5) | `5031d837d2e7bf9dd1b681c837c942d2b74dc65e` | `0.1.0-ci.14.1` | [passed](https://github.com/ArcForges/Mobile/actions/runs/35444269638) |

## Process and source reconciliation

Every owner has the ten-subject record template, explicit inventory, closed licence
decision data, accountable approval and conflict handling, immutable revisions and
deterministic notices. Real wrappers, generator output, tooling ports, patches and
legal texts are bound to inspected upstream identities. Artifact records additionally
cover material introduced during packaging. Compiled dependencies and source/resource
reuse keep their distinct licensing obligations. Unknown, conflicting or unclassified
material fails before acceptance; historical records and profiles cannot be rewritten
to fit a later candidate. A retired initialization repository is not an implementation input.

Fresh source checks passed for these revisions. Naming checks covered all 1,319 files
with no findings; DesktopPlatform's single exact reference exception remains hash-bound.
The 286 count below includes preserved superseded records; it is not an active-record count.

| Owner | Inventoried files | Reused files | Retained records |
|---|---:|---:|---:|
| Contracts | 321 | 107 | 87 |
| DesktopPlatform | 353 | 10 | 115 |
| ArcNotes | 77 | 9 | 10 |
| ArcScope | 76 | 12 | 9 |
| ArcSlate | 76 | 12 | 9 |
| Cloud | 109 | 12 | 15 |
| AI | 88 | 10 | 10 |
| Web | 109 | 14 | 13 |
| Mobile | 110 | 19 | 18 |
| **Total** | **1,319** | **205** | **286** |

## Distribution and runtime verification

- **Contracts:** public NuGet contents match the candidate apart from the registry
  signature; both npm tarballs and all 20 Maven files match exactly. Four developer
  API-reference companions and provenance receipts bind the merged revision. Isolated
  Windows/Linux consumers passed all six protocol cases. The earlier twelve browser
  scenarios belong to generated developer reference documentation at ci.50.1; the
  final ci.54.1 authority-pin change was checked through its actual documentation
  closure and published bytes, without claiming a new browser/device run.
- **DesktopPlatform:** all ten public NuGet packages retain 599 byte-identical
  candidate members, with only the registry signature added. Isolated public-package
  consumers passed the policy rejection cases, all five native bindings under both
  JIT and Native AOT, an independent C17 caller over all four ABIs, and wrong-RID,
  missing-owned/transitive-DLL and changed-DLL failures. Native source recipes,
  corresponding-source delivery, full legal texts and the separately licensed
  Microsoft compiler runtime are bound to the inspected binary closure.
- **ArcNotes, ArcScope and ArcSlate:** each public release's eleven assets and five
  native candidates match main CI; the complete companion archives were verified.
  Each product passed real native UI/Cloud tests on Windows x64/Arm64, Linux x64 and
  macOS x64/Arm64. The UI uses Avalonia/Skia; these are native application tests.
- **Cloud:** seven public candidate members match CI. The actual deployed OCI image
  identity, eleven app members and six base legal members were inspected. Real
  published TypeScript and Kotlin clients exercised Worker-to-Native-AOT gRPC-Web.
  The observed live Cloud revision is `3165c97cccd3ea1e0b230d66e22ab9c775ca19d8`.
- **AI:** all twenty public candidate members match. The deployed Workflow used
  `@cf/openai/gpt-oss-20b`, made two real model calls and invoked `say_hello` with an
  accepted result. The separate local compiled-worker test uses explicitly mocked
  inference and is not substituted for that real-provider evidence.
- **Web:** all fifty public candidate members and deployment metadata match.
  Fifteen public static scenarios passed. Chromium, Firefox and WebKit each pressed
  the actual Cloud button, made one binary gRPC-Web request and received the real
  Native AOT response; startup made zero automatic API requests. These are browser
  product tests and do not establish desktop or Android behavior.
- **Mobile:** the [current Android receipt](open-gates-register.md#21-current-android-candidate-licence-evidence)
  covers all four Android archives, their 454 members, complete retained notices,
  both real API images, protected persistent signing, anonymous public downloads
  and real upgrades from version code 901. Every signed payload and companion
  matches the tested candidate. The client uses Kotlin/Jetpack Compose.

Mobile's initial ci.12.1 post-publication check exposed an API 36 verifier defect:
the package dump uses `appId` where API 26 uses `userId`. [The correction](https://github.com/ArcForges/Mobile/pull/5)
requires emulator user 0, accepts the two observed labels, rejects ambiguous fields
and exercises the reader on both PR images. The final revision and public upgrade
evidence in this receipt include that correction; ci.12.1's failed run remains retained.

Browser resources in developer API documentation are distribution material with
their own provenance; they are not a native client UI technology. Cloud and AI
currently compile their Worker sources with TypeScript 7.0.2. The historical 6.0.3
identity in an upstream generation record describes that producer's reproduction
toolchain; it does not select the current compiler or the Workers JavaScript runtime.

## Repairs, retained evidence and execution limits

The accepted [Android packaged-resource repair](reference-coverage-and-provenance.md#321-current-android-packaged-resources)
removed unused MPL suffix data, source-only annotations and legacy test-runner images.
No-cookie behavior and native authentication boundaries remain intact. Full required
notices remain, including instrumentation-only EPL terms and source availability.
The [native closure](reference-coverage-and-provenance.md#33-existing-native-distribution-closure)
and [compiler-runtime profile](reference-coverage-and-provenance.md#34-existing-windows-compiler-runtime-redistributable)
retain their particular source, permission and distribution evidence.

Task branches and `.worktree/wp00-03-*` checkouts remain in all owners. Their
`artifacts/evidence` directories retain review, source, archive, public-byte and
runtime receipts; DesktopPlatform's publication receipts are under
`artifacts/post-merge-ci13`. The final cross-owner index is retained in Mobile's
`wp00-03-provenance/artifacts/evidence/family-reconciliation` directory. Required
CI evidence is also linked from the final PRs and public release manifests.

Automatic local approval review rejected starting the owned Android emulators,
returning only "blocked by policy". Required API 26/36 and public upgrade tests
executed in CI. An additional local post-download desktop execution was also
rejected; the recorded basis remains completed local pre-merge native tests and
five-host main CI over byte-identical public candidates. No replacement local run
is claimed. No external prerequisite blocks WP00.03. Physical devices, store
submission, trusted desktop distribution and full commercial-product behavior
remain governed by their later work packages and are not established by this receipt.
