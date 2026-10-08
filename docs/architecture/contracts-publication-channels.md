# Contracts publication channels

This profile refines the [producer publication protocol](14-build-packaging-and-release.md#complete-producer-candidate-and-promotion-protocol). It changes development distribution, not contract scope or product readiness.

Under [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 4, the first-party business SDK is the generated C# NuGet package set. The npm and Maven SDK channels stop after their consumers migrate. The one npm package kept is `@arcforges/ai-internal`, the internal thin-adapter transport codec used by the Cloud Worker binding adapters.

| Trigger | NuGet version (C# SDK and Contracts packages) | npm version (`@arcforges/ai-internal` only) | Maven |
|---|---|---|---|
| Reviewed main push | `1.0.0-ci.<run>.<attempt>` | `1.0.0-ci.<run>.<attempt>` on the `ci` dist-tag | Stopped after consumer migration; no new coordinates |
| Canonical `vX.Y.Z` tag on a commit reachable from main | `X.Y.Z` | `X.Y.Z` | Stopped after consumer migration; no new coordinates |
| Pull request, merge group or manual validation | Tested candidate only | Tested candidate only | No registry credentials or publication |

The configured development base is initially 1.0.0. A later release series changes it through a reviewed producer change. Formal tags use canonical numeric SemVer without leading zeroes. Creating a formal tag is a release action; validation must not create production tags just to exercise CI.

**Stopped channels.** The npm identities `@arcforges/proto`, `@arcforges/api-client`, `@arcforges/contract-fixtures` and `@arcforges/operator-client`, and the Maven identities `contracts-proto`, `contracts-connect-client` and `contract-fixtures`, stop receiving new publication only after their consumers are migrated (the migration is [CON.40](../planning/delivery/lanes/contracts.md#task-con-40), after WEB.40, AND.40 and CLOUD.84 deliver). Stopping is a reviewed record. Published versions stay immutable and resolvable; nothing is unpublished, deleted or deprecated without explicit user approval. Existing production and cross-repository consumer locks remain on exact immutable releases.

**Immutability.** A published NuGet or npm version is never overwritten, and a retry of already matching bytes may succeed without another upload. A `-ci` version is a build identity, not a floating channel, and is not a deployment manifest or proof of long-term reproducibility. Development comparisons use the recorded build identity and the canonical semantic hash of [CON.17](../planning/delivery/lanes/contracts.md#task-con-17), whose authority is the C# implementation. Formal releases retain matching NuGet and npm versions and exact locks.

Allocate the cross-package build version before building. The candidate manifest records every package version and the source commit; each NuGet package carries its build version, source commit and descriptor hash. Test the complete packages in isolated consumers before credentials are exposed. Publication only transports those tested bytes; it never rebuilds or rewrites a package. Record resolved versions and remote hashes for every published package.

Serialize publication and prevent delayed CI runs from replacing a newer development build. Partial or mismatched package visibility must not be reported as complete. Bound each publication attempt to ten minutes, retain diagnostics and receipts after failure, and retry a stalled attempt from the same tested candidate.

Only canonical repository push runs may publish. Release tags must pass the same candidate and isolated consumer gates, match the candidate version and resolve to a main commit. GitHub environment branch/tag restrictions remain enabled. Signing credentials are exposed only to the formal release path. After the first stable npm release, development builds of `@arcforges/ai-internal` use the `ci` dist-tag and cannot replace stable `latest`; older stable releases cannot rewind `latest`.

Acceptance requires negative publication guards, real NuGet feed transport and metadata resolution, real isolated package consumers, all applicable PR checks, and a post-merge live feed receipt with matching bytes. A local feed test is not evidence of the live feed. Tag selection and release candidate tests may run without publishing an unrequested formal release.

[Implementation and live publication evidence](../assurance/contracts-publication-channels-evidence.md) records the earlier Maven snapshot publication (the successful failed-job retry, all 20 public Maven files matching the tested candidate, and actual isolated registry consumption). That record is historical for the Maven channel, which stops under P2-021; it is not a NuGet receipt.

## Publishing usage and commercial operation

These obligations apply to the Maven channel until its stop record is accepted (superseded in scope 2026-10-08 by P2-021 item 4); they are retained, not weakened.

External policy checked 2026-09-20: [Sonatype publishing limits](https://central.sonatype.org/publish/maven-central-publishing-limits/) measure current-calendar-month publishing activity, not cumulative retained storage; published Central releases cannot be deleted to reclaim an allowance. Snapshot retention does not establish a quota exemption, and no such exemption has been verified. The account Usage Center is authoritative for current thresholds and measured usage.

[Sonatype's 2026-09-08 commercial-use announcement](https://central.sonatype.org/news/20260908_publisher_tiers_commercial_use/) states that commercial-nature artifacts require Publisher Pro from 2026-10-01 independently of publishing volume. Commercial operation must resolve the applicable subscription or approved classification with Sonatype before relying on continued distribution of any remaining Maven artifact. This account/commercial prerequisite is distinct from any technical gate; neither tag-only formal releases nor successful snapshot uploads prove free commercial eligibility. No subscription purchase or exemption is claimed by this evidence.
