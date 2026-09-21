# Contracts publication channels

This profile refines the [producer publication protocol](14-build-packaging-and-release.md#complete-producer-candidate-and-promotion-protocol). It changes development distribution, not contract scope or product readiness.

| Trigger | NuGet/npm version | Maven version and destination |
|---|---|---|
| Reviewed main push | `1.0.0-ci.<run>.<attempt>` | `1.0.0-SNAPSHOT`, Sonatype snapshots |
| Canonical `vX.Y.Z` tag on a commit reachable from main | `X.Y.Z` | `X.Y.Z`, Maven Central release |
| Pull request, merge group or manual validation | Tested candidate only | No registry credentials or publication |

The configured development base is initially 1.0.0. A later release series changes it through a reviewed producer change. Formal tags use canonical numeric SemVer without leading zeroes. Creating a formal tag is a release action; validation must not create production tags just to exercise CI.

Maven's development channel is the explicit exception to immutable package coordinates. Sonatype snapshots use `https://central.sonatype.com/repository/maven-snapshots/`, require namespace SNAPSHOT support to be enabled, and may be overwritten and periodically deleted (currently approximately 90 days). They do not undergo Central's formal release validation. See [Sonatype's snapshot documentation](https://central.sonatype.org/publish/publish-portal-snapshots/), verified 2026-09-20. Namespace enablement and successful authenticated publication require implementation evidence.

Allocate both the cross-language build version and Maven coordinate before building. The candidate manifest records both; each Maven JAR carries the build version, source commit and descriptor hash. The Maven POM, module metadata and internal dependencies use the Maven coordinate. Test the complete archives in isolated consumers before credentials are exposed. Publication only transports those tested bytes; it never rebuilds or rewrites a POM/JAR/module. Record resolved timestamp/build numbers and remote hashes for all four current Maven modules.

Existing production and cross-repository consumer locks remain on exact immutable releases. Development users explicitly opt into a group-filtered snapshot repository; a floating snapshot is not an immutable deployment manifest or proof of long-term reproducibility. Cross-language development comparisons use the recorded build identity and descriptor hash. Formal releases retain matching NuGet/npm/Maven versions and exact locks.

Serialize Maven publication and prevent delayed CI runs from replacing a newer development build. A retry of already matching snapshot bytes may succeed without another upload. Partial or mismatched module visibility must not be reported as complete. Formal Central retries preserve and resume the accepted deployment receipt without uploading duplicates. Bound each Maven publication attempt to ten minutes, retain diagnostics/receipts after failure, and retry a stalled attempt from the same tested candidate.

Only canonical repository push runs may publish. Release tags must pass the same candidate and isolated consumer gates, match the candidate version and resolve to a main commit. GitHub environment branch/tag restrictions remain enabled. Signing credentials are exposed only to the formal Maven release path. After the first stable npm release, development builds use the `ci` dist-tag and cannot replace stable `latest`; older stable releases cannot rewind `latest`.

Acceptance requires negative publication guards, real snapshot repository transport/metadata resolution, real isolated package consumers, all applicable PR checks, and a post-merge live snapshot receipt with matching bytes. A local repository test is not evidence of Sonatype namespace enablement. Tag selection and release candidate tests may run without publishing an unrequested formal release.

[Implementation and live publication evidence](../assurance/contracts-publication-channels-evidence.md) records the successful failed-job retry, all 20 public Maven files matching the tested candidate, and actual isolated registry consumption. The snapshot authorization and consumption gate is closed for that candidate.

## Publishing usage and commercial operation

External policy checked 2026-09-20: [Sonatype publishing limits](https://central.sonatype.org/publish/maven-central-publishing-limits/) measure current-calendar-month publishing activity, not cumulative retained storage; published Central releases cannot be deleted to reclaim an allowance. Snapshot retention does not establish a quota exemption, and no such exemption has been verified. The account Usage Center is authoritative for current thresholds and measured usage.

[Sonatype's 2026-09-08 commercial-use announcement](https://central.sonatype.org/news/20260908_publisher_tiers_commercial_use/) states that commercial-nature artifacts require Publisher Pro from 2026-10-01 independently of publishing volume. Commercial operation must resolve the applicable subscription or approved classification with Sonatype before relying on continued distribution. This account/commercial prerequisite is distinct from the passed technical snapshot gate; neither tag-only formal releases nor successful snapshot uploads prove free commercial eligibility. No subscription purchase or exemption is claimed by this evidence.
