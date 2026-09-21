# Contracts publication channels: implementation and live registry gate

## Verified implementation

[Design PR 36](https://github.com/ArcForges/ArcForges-Design/pull/36) defines the [publication channel profile](../architecture/contracts-publication-channels.md). [Contracts PR 26](https://github.com/ArcForges/Contracts/pull/26) implements it; [PR 27](https://github.com/ArcForges/Contracts/pull/27) corrects remote snapshot metadata transport. Both implementation PRs received full diff review and passed all applicable CI/security checks before merging. Final implementation commit: `24c05b7fc215896eeec91437ffe8846f2d4467a1`.

- Main uses Maven `1.0.0-SNAPSHOT`; NuGet/npm retain the exact CI build identity. Canonical `vX.Y.Z` tags on main ancestry use immutable formal versions.
- Candidate manifests record both versions. Maven JAR metadata retains the CI version, Git SHA and descriptor identity. Publication transports the same tested files.
- GitHub environments retain the `main` branch restriction and additionally admit `v*` tags; code rejects noncanonical tags, mismatched versions and unmerged tag commits. Main snapshot jobs receive no signing key.
- Maven publication steps have a ten-minute timeout and retained receipts. Central release polling shares one bounded attempt; accepted deployment IDs are reused on retry.
- Existing consumer versions and locks are unchanged. No formal production tag was created for testing.

## Validation and publication results

The local snapshot and formal `1.0.0` candidates passed actual isolated Windows C#, TypeScript, Kotlin, Connect Kotlin and Native AOT RPC success/error checks. Hosted PR and final main consumers passed on Linux and Windows with fresh caches and no producer source references. The suite contains 92 Python tooling tests and 10 compiled contract-access tests. Signing uses an ephemeral test key; the HTTP snapshot regression performs real metadata GET and artifact PUT requests and verifies all 20 candidate files. Reintroducing the previous offline flag makes that regression fail.

The first main attempt (`1.0.0-ci.63.1`, run `35545955979`) failed before upload because Gradle offline mode also blocks remote snapshot metadata reads. PR 27 removed that flag and replaced file-only transport coverage with HTTP coverage. Its receipt and the independently published NuGet/npm versions are retained; that producer set is not recorded as complete.

The final [main run 35546947568](https://github.com/ArcForges/Contracts/actions/runs/35546947568) built `1.0.0-ci.65.1` with Maven coordinate `1.0.0-SNAPSHOT`. Build, both consumers, Verify, NuGet and npm jobs passed. [Main security](https://github.com/ArcForges/Contracts/actions/runs/35546947604) passed. Independent public checks verified both npm tarballs byte for byte and all 13 original NuGet archive members, excluding only the registry-added signature.

## Recovered live publication

The first attempt received HTTP 403 on the first timestamped POM PUT. Its receipt and failure remain in the machine-readable history. After the namespace administrator supplied confirmation that SNAPSHOTs were enabled, only the failed Maven job was retried in run `35546947568`, attempt 2. It reused `1.0.0-ci.65.1` without rebuilding or republishing NuGet/npm. The publication step completed in 77 seconds and the complete CI run passed.

The successful receipt has phase `public-bytes-verified`. Independent public downloads matched all 20 Maven candidate files byte for byte, resolving timestamp `20260921.014054-1`. Both npm tarballs and all original NuGet members also matched. A fresh-cache Windows consumer run restored Maven packages directly from Sonatype and passed C# gRPC, TypeScript gRPC-Web, Kotlin gRPC, Kotlin Connect gRPC-Web, Kotlin Connect gRPC and Native AOT gRPC success/error checks. Its `registryRestore` is `maven-snapshot-passed`; live Maven bytes were checked before and after consumption. This closes the snapshot authorization and live-consumption gate.

## Limits of this evidence

No formal production tag was created. Existing immutable consumer locks remain unchanged. Successful snapshot publication does not prove exemption from publishing quotas or commercial subscription requirements. See the [publication policy](../architecture/contracts-publication-channels.md) for current external policy boundaries.

The [machine-readable evidence](contracts-publication-channels-evidence.json) retains reviews, exact heads, candidate hashes, local/hosted consumers, failed attempts, successful retry and public verification. Branches and worktrees are retained. Hello probes are not product readiness or Android/browser device acceptance.
