# CON31 public source-digest scanner support, 2026-10-07

This minimum P2-018 supporting amendment changes only CON.31 write scope and explanatory notes. All task identities, dependencies, outcomes, obligations, baselines, acceptance requirements, completed records and the original Final selection remain unchanged. `ArcForges - Final.md` is never edited.

## Actual public inputs and precise matching

Retained CON.31 diagnostics identify public source-receipt JSON lines matching `generic-api-key`. The twelve receipt input observations below were recomputed from actual public Git blobs at source `8a0f9a19aafefa23ead116922e8dd8c6d041fb13` for r1, `0015402d3f8e03d785adb3f698968f5989240966` for r2, and genuinely frozen source `ce865e6e1fbc450ade6055f73f95a24877497c49` for r3. The r3 source includes the actual owned JSON schema-version annotation and evaluated access successor. These digests identify published source inputs, not authentication credentials. The exact source observations and proposed TOML are retained in the claimant's `artifacts/con31-public-scanner-facts.json` and `artifacts/con31-scanner-groups-proposal.toml`. The new schema is an actual access/package-graph input; no separate global dependency-input map entry is asserted for it.

Actual Security run `37579875209`, job `112656845588`, at the r3 source reports 18 redacted `generic-api-key` observations: the previous twelve, the four r3 receipt input lines and two current dependency-policy access-input occurrences. Its retained redacted log is `artifacts/con31-secret-scan-112656845588.log`. Repeated containing lines are not additional distinct source inputs.

| Exact containing path | Exact JSON key | Exact SHA256 |
| --- | --- | --- |
| `eng/policy/dependency-policy.json` or `eng/policy/dependency-reviews/con-31-r1.json` | `eng/policy/contract-access.json` | `7f7006a49be969a4c8855f1f05f916117279cfe04076f7b6a10bc64e4dd83ae5` |
| `eng/policy/dependency-policy.json` or `eng/policy/dependency-reviews/con-31-r2.json` | `eng/policy/contract-access.json` | `bd3cd1d7e7fb8f7e06e48930607af469db4134e41a649d4b8251933936a6e686` |
| `eng/policy/dependency-policy.json` or `eng/policy/dependency-reviews/con-31-r3.json` | `eng/policy/contract-access.json` | `80e6402d69fee1913bfffbb0ebc8006c741d37f47f44a0b0536339881ce219dc` |
| `eng/policy/dependency-reviews/con-31-r1.json`, `eng/policy/dependency-reviews/con-31-r2.json` or `eng/policy/dependency-reviews/con-31-r3.json` | `eng/provenance/records/dokka-combokeys-licence-r1.json` | `75219d61672002f0bb242fed0fd93a0886f07d944e0b9e1b1f72132f59df1b41` |
| `eng/policy/dependency-reviews/con-31-r1.json`, `eng/policy/dependency-reviews/con-31-r2.json` or `eng/policy/dependency-reviews/con-31-r3.json` | `eng/provenance/records/dokka-object-keys-licence-r1.json` | `55621ecc7032745ca46e56d13133dc22a3bd808d80966d737427b5d6fc5bd096` |
| `eng/policy/dependency-reviews/con-31-r1.json`, `eng/policy/dependency-reviews/con-31-r2.json` or `eng/policy/dependency-reviews/con-31-r3.json` | `src/public/dotnet/ArcForges.Contracts.PublicApi/ArcForges.Contracts.PublicApi.csproj` | `986b7a97734cd5d0630e548da897869de322a112c087c2d0df6a0bfc98b8784c` |

Append precisely four AND groups to `.gitleaks.toml`: the dependency-policy group contains the three exact access-input digests, and each exact r1, r2 and r3 receipt group contains its four input tuples. Each group targets only `generic-api-key`, uses `regexTarget="line"`, anchors every containing path and matches a complete anchored JSON key/value line. Leading/trailing JSON whitespace and a final comma may vary. Preserve the accepted 85-group prefix byte-for-byte, all default rules, pins, history scope, workflow commands, permissions and required-success behavior. The resulting current total is 89 groups with the appended tuple-count vector `[3,4,4,4]`; preserve every indexed historical expectation. This is based on the actual accepted Contracts parent `8715f6e2462153fac44bccac2dd9e8b55adafc5f`, not on a planned future integration or receipt.

Only factual total-count maintenance and exact owned tuple coverage are admitted in `tests/tooling/test_dependency_admission.py`. Cover actual positives and changed digest, key and path, adjacent credentials, other rules and whole-file false matches. No wildcard digest, future receipt name, path-only exclusion, historical rewrite, scanner disablement or generic matcher change is admitted. Any genuinely new receipt tuple requires actual source facts and independent review before its exact replacement or append is included in the final decision. Unchanged shipping inputs are not resealed solely for scanner verification.

## Genuine strict-context fixture maintenance

Actual candidate run `37579875270` at the same frozen r3 source passed generation, SDK compilation and private package construction but failed one of 421 ordinary Python cases: `tests/tooling/test_serialization_policy.py:34` still asserts 97 strict JSON contexts. Accepted source `8715f6e2462153fac44bccac2dd9e8b55adafc5f` has 97; the r3 source has 98, with all original contexts preserved and the sole new `OperatorProviderPolicyJsonContext` in `src/internal/dotnet/ArcForges.Contracts.CloudInternal/Generated/Shapes/OperatorProviderPolicy.g.cs`.

Admit only that existing expected-count literal from 97 to 98 in the existing serialization-policy test. Preserve every strict JSON option, declaration check, input/output identity, public/private boundary and negative assertion. This is a factual assertion adjustment for the genuine new producer, with no serializer algorithm, package input, generated output or immutable receipt change. Run the affected ordinary test, require an independent exact-source delta review and fresh applicable CI; do not retry the unchanged failed candidate or reseal unchanged shipping inputs.

## Ownership and delivery

The existing CON.31 claimant is the sole source writer for this append. Governance alone coordinates Contracts integration and normal publication, preserving all accepted scanner groups when later independently reviewed producers compose. Root coordinates the paired planning fence. Generate and check the explicit Design and Plan worktrees, require independent exact-head planning and source reviews, and pass all applicable ordinary CI including the unchanged full-history scan.

These exact public input facts authorize the bounded supporting implementation. They are not proof of a clean scanner run, package publication, deployment, authenticated provider behavior or full-system acceptance.
