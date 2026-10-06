# Production supporting-scope repairs, 2026-10-07

This focused P2-018 amendment admits the minimum concrete supporting changes exposed by current implementation and CI. It changes only `writes` and explanatory `notes` for CON.26, CLOUD.07, PLT.11, CON.32 and PLT.62. All 464 task identities, dependencies, outcomes, obligations, baselines and completion requirements stay unchanged; the accepted security lifecycle/final-expiry producers remain intact. The original Final selection is unchanged, and `ArcForges - Final.md` is never edited.

## CON.26: exact public source hashes and actual private policy version

The completed pinned Gitleaks8.30.1 Security run37540778304/job112532979781 reports four occurrences of three public `eng/policy/contract-access.json` SHA256 receipt tuples. Preserve the accepted85 groups and the three previously reviewed CON26 groups byte-for-byte, giving88; append exactly two AND groups targeting only `generic-api-key` and a complete anchored JSON line:

| Exact anchored path | Exact key | Exact SHA256 |
| --- | --- | --- |
| `eng/policy/dependency-policy.json` or `eng/policy/dependency-reviews/con-26-r2.json` | `eng/policy/contract-access.json` | `9ca13f767b08d3d28cac9450f2cb7ccb540cb3928978ad9810d70156c04f8307` |
| `eng/policy/dependency-reviews/con-26-r1.json` | `eng/policy/contract-access.json` | `17549663c7fd55d44de7c75f2903c2c78e72442a38739bf9a8218a7c28cf53e5` |

The resulting90-group maintenance belongs in the existing `tests/tooling/test_dependency_admission.py`; verify actual positives and changed digest/key/path, adjacent credentials and other-rule negatives. The two exact proposed TOML groups are retained in `con26-exact-scan-repair.toml.txt` with factual tuple evidence in `con26-sourcehash-scan-proof.json`. No wildcard hash, whole-path exclusion, historical rewrite, generic scanner relaxation or disabled scan is authorized.

GOV24 was actually published by37536039554 at `1.0.0-ci.111.1`. CON26 already uses this producer. Admit only corresponding default/positive literal maintenance in `eng/check_licences.py` and `tests/tooling/test_licence_boundary.py`; preserve private build-host-only admission, wrong-version/runtime visibility and AGPL rejection rules. No runtime or third-party version or licence boundary changes.

## CLOUD.07: one deterministic public codec vector

The retained all-ref scan also encounters C13's public codec fixture. Admit a new `.gitleaks.toml` with `extend.useDefault=true` and exactly one AND group targeting only `generic-api-key`, the anchored path `tests/ArcForges.Cloud.Tests/Sessions/SessionTokenCodecTests.cs`, and the complete line `private const string Token = "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8";`. This is the canonical bytes0..31 test vector, never an issued credential. Leading/trailing whitespace may vary; adjacent declarations or tokens must not match.

Use the existing `tests/worker/capacity.test.ts` and already-admitted Python `tomllib` for a narrowly bounded profile guard and positive/changed-vector/wrong-path/adjacent-credential negatives. Register only its actual owned first-party row under the existing provenance append protocol. No new package, test workflow or input reseal of unchanged shipping source is implied. Preserve default scanner rules, all refs, routes/data and `workers.dev=false`.

## PLT.11: actual generated project-reference lock closure

CI37540970758 exposes two necessary Security consumer lock updates after the actual LocalRpc Platform324 reference is added. Isolated SDK10.0.400 diagnostics show LocalRpcBoundary needs Platform324, already-admitted PublicApi324 and Sdk.Contracts324 transitive nodes, and the LocalRpc Platform dependency edge. Security.Tests needs Platform324 and the same edge. Regenerate only these two locks and the five already-admitted helper locks; preserve every existing coordinate/version/contentHash. The helper wording identifies Platform324 correctly; Foundation324 was already present. No hand-invented hashes, unlocked restore waiver or unrelated version change. The existing PLT11 owner is the sole lock writer and coordinates the accepted native/helper prefix once.

## CON.32: real optional-message generation and ordinary fixtures

The actual C# protobuf optional message is nullable and has no `HasToolCallId`/`HasToolResultFor` scalar presence property. Admit only `eng/generate_shapes.py`'s `proto_cs` optional-message condition so scalars keep their actual Has property and messages use their actual nullable presence. Preserve nested Id validation, absent-field compatibility and field-specific bounds. Admit actual generated fixture export in `src/public/ts/contract-fixtures/src/index.ts` and the existing `src/public/kotlin/contracts-proto/build.gradle.kts` test-only wire fixture hook. No runtime dependency, shape-emitter fiction, operation/package addition or inferred tool-pair authority is introduced. Actual generated declarations, absence/value negatives and old serialization stay under the original source review and CI.

## PLT.62: production resource isolation

The actual shared Shell project already excludes test Compile/None items, but a new focused test `.resx` also requires `<EmbeddedResource Remove="Tests/**" />` in its existing project. Admit only that exclusion, its actual dependency input successor `eng/policy/dependency-reviews/plt-62-r1.json` and matching owned dependency/provenance rows. Actual reconciliation-policy run37544384688 also requires a corresponding immutable owned append in `eng/policy/reconciliation/project-updates.json` and the exact Shell blob pointer in `eng/policy/reconciliation/active-projects.json`; preserve every historical snapshot and unrelated active project. Preserve all actual62NuGet/10Python coordinates and accepted immutable receipt prefixes. No drift gate relaxation, copied-tool successor, NOTICE rewrite or production test-resource leakage is allowed. Real ResourceManager/formatter/audit components require independent source review and applicable CI; this supporting amendment is not deployment or OS/UI acceptance evidence.

## Delivery and review

Regenerate both documentation repositories and require a paired delivery check. Existing implementation claimants own their supporting changes, preserve all completed source/publication receipts, obtain exact-head independent review and pass applicable CI before fenced merges. Ordinary implementation delivery remains distinct from unavailable full-system acceptance. This repair adds no tasks, edge relaxation, acceptance waiver, production deployment or credential authorization.
