# WP02.00 toolchain pin and restore profile

Authority: [WP02.00](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.00), [build model](../architecture/14-build-packaging-and-release.md#2-repository-build-model), [current roots](wp01-stage-acceptance.md) and the explicit local dependency reuse instruction of 2026-09-20.

## Current inputs and bounded repairs

The current nine repositories contain 43 managed projects and their 43 per-project NuGet locks, four independently owned npm root locks (Contracts, Cloud, AI and Web), and the existing Contracts/Mobile/Cloud-test Gradle wrapper, catalog, strict locks and checksum metadata. The historical 165 NuGet locks describe the retired monorepo. Mobile is Kotlin/Gradle and has no npm build dependency. Keep the current independent SDK/package versions and published compatibility identities; no family-wide version upgrade is required.

DesktopPlatform and Contracts already enable NuGet central transitive pinning. Enable it in ArcNotes, ArcScope, ArcSlate and Cloud, refresh locks only through the owning restore, and review any resulting dependency change before admission. Existing managed projects have no inline PackageReference version override.

The existing Node patch and bundled npm version remain authoritative through .node-version and packageManager. Contracts and Web already check both. Add equivalent executable checks to AI and Cloud. Web's pinned JavaScript SDK adapter keeps ShouldRunNpmInstall=false and delegates to its own npm commands; explicit npm restore precedes IDE build. Do not introduce a second lock or a .NET Web runtime.

Contracts and the Cloud Kotlin fixture use Java 17, while Mobile compiles JVM 21. Replace CI major-only selectors with the already observed successful producer patch releases, Temurin 17.0.20 and 21.0.12 respectively, recorded in owner-local version inputs. Preserve bytecode targets and the separate JetBrains preview runtime. Retain actual vendor build/OS identities in execution evidence: the existing Contracts run observed 17.0.20+1 on Linux and 17.0.20+101 on Windows. Local compatible JDK checks must identify their actual version and are not substituted for the exact pinned hosted producer proof. No new JDK patch upgrade is inferred from a newer remote default.

DesktopPlatform's Python tooling currently follows runner state and installs pre-commit without a version. Pin its Python release, pre-commit and complete dependency closure with verified archive hashes; use the pin in Python-running jobs. Preserve the existing native baseline, overlays, toolsets and package admission. Contracts and Mobile already carry .python-version. This does not introduce a Python runtime dependency into desktop applications or TS-only owners.

## Local native reuse and published candidates

Normal local development first uses the already installed vcpkg executable and suitable installed dependency tree. Do not reinstall vcpkg or rebuild dependencies merely to match a local patch/version difference when the required package names are present and compilation succeeds. Supply the existing installed-root explicitly or through ignored local configuration; never rewrite the user's global installation. A successful local build records what actually ran.

The committed CI/native producer baseline and admitted candidate provenance remain reproducible and unchanged. A locally compatible build is useful development evidence; it does not falsely attest that arbitrary local binaries are the reviewed publishable candidate. Candidate distribution still uses the tested, admitted CI dependency closure and matching notices. No local reinstall is a prerequisite to this step's validation. Ordinary application consumers never run CMake/vcpkg.

## Ordered execution and verification

1. Review and merge this authority clarification before dependent implementation.
2. Apply the bounded owner-local repairs above in isolated worktrees; register new first-party tooling/configuration in each owner's provenance inventory. Preserve package identities, generation sources, native choices and application signing continuity.
3. Restore each actual dependency graph in clean source worktrees using committed locks. Exercise offline repeats from fetched caches; use package-manager offline/source-isolation modes, not an assumption that an up-to-date build performed no network resolution. Keep online vulnerability scanning as a separate required gate. Reuse installed native dependencies without a new vcpkg installation.
4. Prove altered locks/baselines or floating selections fail at their relevant existing/toolchain policy boundary. Run generated-source comparison and actual changed owner builds/consumers. NuGet central pin changes require lock-diff review; no manual hash editing or suppression of restore failures.
5. Review each complete PR. Merge code only after all applicable checks pass, in producer-before-consumer order. Pull primaries, verify new main candidates and public bytes/runtime evidence where publication occurs, and retain branches/worktrees. Formal Central releases still require explicit version tags; a validation retry reuses its candidate.
6. Record a final evidence receipt with exact commits, pins/locks, actual local/CI tools, online/offline and negative results, and genuine unavailable external prerequisites. This profile is a decision and plan, not completion evidence.

## Primary facts checked

On 2026-09-20, the [NuGet central management documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) confirms transitive pinning is opt-in; [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/) rejects manifest/lock disagreement; [Gradle locking](https://docs.gradle.org/current/userguide/dependency_locking.html), [dependency verification](https://docs.gradle.org/current/userguide/dependency_verification.html) and [offline caching](https://docs.gradle.org/current/userguide/dependency_caching.html) distinguish version locking, integrity and offline resolution. [setup-java](https://github.com/actions/setup-java) supports version files. The selected Java producer patches come from the recorded successful CI runs, not an unverified latest-release claim. Adoptium API requests returned HTTP 403 on the recorded attempts; exact hosted setup and build results must establish availability before merging any Java pin change.
