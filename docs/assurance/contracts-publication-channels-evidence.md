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

**Live Maven publication remains blocked.** The first timestamped `contract-fixtures` POM PUT returned HTTP 403 Forbidden. The Maven job ran from `2026-09-21T00:20:28Z` to `00:21:01Z`; this was an immediate access denial, not a Central validation timeout. Snapshot metadata is unavailable, so live Sonatype package restoration and a complete cross-registry release are not claimed.

## External prerequisite and exact recovery

The Sonatype namespace administrator must confirm or enable **Enable SNAPSHOTs** for `io.github.arcforges` in [Portal namespace settings](https://central.sonatype.com/publishing/namespaces). If already enabled, verify that the existing publishing-token account has snapshot write permission for this namespace. The Portal setting has not been observed in this execution; HTTP 403 alone does not prove which permission is missing. [Sonatype documents namespace enablement as a prerequisite](https://central.sonatype.org/publish/publish-portal-snapshots/).

After correcting that account setting, re-run **only the failed Maven job** in run `35546947568`. It reuses candidate `1.0.0-ci.65.1`; do not rebuild all jobs or republish NuGet/npm. Acceptance still requires all 20 remote timestamped files to match the candidate and `python eng/contracts.py consume --directory <downloaded-candidate> --aot --snapshot-registry` to pass. Its verifier checks live bytes before and after actual Kotlin/Connect restoration and RPC execution.

The [machine-readable evidence](contracts-publication-channels-evidence.json) records reviews, exact heads, candidate hashes, local/hosted consumers, public package checks, environment policies, both failed Maven attempts and the open external gate. Branches and worktrees are retained. Hello probes are not product readiness or Android/browser device acceptance.
