# Actual GOV25 consumer public-digest support, 2026-10-07

This narrow P2-018 supporting amendment changes only CON.26 write scope and explanatory notes. Task identities, dependency edges, obligations, outcomes, acceptance gates and completed ledgers remain unchanged. The original selection and `ArcForges - Final.md` are unchanged.

## Actual failure and bounded scope

GOV.25 was normally published at `1.0.0-ci.119.1` by DesktopPlatform run37556762692 at actual source0ac0fbf368f3e15d78008834219321acd4ad1390. Contracts consumed that exact private policy producer at b32193784f17b3c6c3689fbb4651b60a732703bd. Its pinned Gitleaks8.30.1 full337-commit-history scan returned six `generic-api-key` findings, all four exact public SHA256 source-receipt tuples below. The complete redacted report and source proof are retained in the CON.26 worktree artifacts; each source digest was independently recomputed at that commit using the existing normalized-source convention.

| Exact anchored containing path | Exact JSON key | Exact SHA256 |
| --- | --- | --- |
| `eng/policy/dependency-policy.json` or `eng/policy/dependency-reviews/con-26-r3.json` | `eng/policy/contract-access.json` | `e8c200306c928f898871194663910ec244caafe4baf9fc9e1c1ce30e2becd346` |
| `eng/policy/dependency-reviews/con-26-r3.json` | `eng/provenance/records/dokka-combokeys-licence-r1.json` | `75219d61672002f0bb242fed0fd93a0886f07d944e0b9e1b1f72132f59df1b41` |
| `eng/policy/dependency-reviews/con-26-r3.json` | `eng/provenance/records/dokka-object-keys-licence-r1.json` | `55621ecc7032745ca46e56d13133dc22a3bd808d80966d737427b5d6fc5bd096` |
| `eng/policy/dependency-reviews/con-26-r3.json` | `src/public/dotnet/ArcForges.Contracts.PublicApi/ArcForges.Contracts.PublicApi.csproj` | `986b7a97734cd5d0630e548da897869de322a112c087c2d0df6a0bfc98b8784c` |

Append precisely two AND groups to `.gitleaks.toml`, each targeting only `generic-api-key` with `regexTarget="line"` and an anchored whole JSON key/value line. The first group has one exact permitted tuple and only the two containing paths in its table row; the second has the three exact immutable tuples and only `con-26-r3.json`. Leading/trailing JSON whitespace and a final comma may vary. A neighboring declaration, credential or other content must not match. Preserve the accepted90-group prefix byte-for-byte and all scanner defaults, existing rules, history scope, workflow commands, pins, permissions and required-success behavior.

Update only the nine current total-count assertions in `tests/tooling/test_dependency_admission.py` from90 to92, preserving every indexed historical expectation and appending the vector `[1,3]`. Add actual six-observation/four-tuple source verification and changed key, path, digest, adjacent credential and other-rule negatives. No wildcard digest/path exclusion, source-wide exemption, generic matcher change, historical receipt rewrite or dependency reseal of unchanged shipping inputs is admitted. If later source changes alter a tuple, gather fresh exact evidence and independent review before admitting its replacement.

The actual GOV25 producer119.1 supersedes the previously admitted GOV24 default111.1 for this private architecture host. The existing CON26 candidate b321 already has `eng/check_licences.py`'s exact119.1 default; preserve that literal and admit only exact119.1 default maintenance. The actual pending edits are the three existing default/positive/privateAssets111.1 literals in `tests/tooling/test_licence_boundary.py`, moved to119.1. Preserve the wrong94.2 rejection and all private build-host isolation, runtime visibility and AGPL negatives; no algorithm or licence-boundary relaxation. Run the actual affected licence suite, whose positive still used111.1 during the real119.1 consumer review.

## Delivery

The existing CON.26 claimant is the sole source writer; the Contracts integration owner serializes its shared input/publication changes. Require independent exact-head review and passing applicable CI, including the unchanged full-history scan. Generate and check the paired Design/Plan views. This support decision is neither a scanner pass nor publication, deployment or full-system acceptance evidence.
