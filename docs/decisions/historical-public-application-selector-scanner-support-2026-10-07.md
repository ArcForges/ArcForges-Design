# Exact historical public Application selector scanner support

This minimum P2-075 support repairs two independently diagnosed historical false positives. It changes no product credential, current-session authority, generated contract, dependency, accepted history, full-history scanner rule or other exception. COM.18 is the sole Cloud implementation owner of this correction; DEV.01 owns its unchanged public DI selector. Policy is the sole independent paired planning reviewer, and the integration owner fences the reviewed exact source head after applicable CI.

## 1. Actual observations and classification

Cloud PR77 source `450df9e2de9536b325bf5445b3beccba0a01a0a8`, CI `37603587235`, audit job `112733588801`, reports two Gitleaks findings. A single equivalent default all-ref diagnostic using the retained official portable Gitleaks 8.30.1 scanned 469 commits / 17.88 MB and returned the same two observations. A separate source-ancestry-only diagnostic scanned 248 commits with zero observations; that narrower result is explicitly not full-history clearance. All retained reports use redaction=100 and contain no emitted secret values.

Both observations are `generic-api-key` at immutable DEV.01 commit `389039026a5daa15503ffdf792ba1ca942e7bc64`. The literal is the public 23-byte ASCII DI/provider selector `application.presence.v1`, SHA256 `7cf0693e77f170ec1ffc1bdba110939f674d30a62b35264a8e0a7e87f6643de5`. The actual source owner independently confirms its purpose: three published Application List/Heartbeat/Disconnect RpcPolicy entries select the separately keyed Bearer/browser-session verifier services. Genuine raw Bearer/cookie/Origin/CSRF values are separately resolved by the request-scoped current C13 owner. The test selector proves keyed-provider refusal and Foundation/null-selector isolation. P2-049's trusted server selection remains unchanged; this public name supplies no credential or caller-selected fallback.

| Immutable file | 1-based line | Exact complete line, excluding line terminator | UTF8 bytes / SHA256 | Entire original Git blob SHA256 |
|---|---:|---|---|---|
| `src/ArcForges.Cloud/Composition/ApplicationPresenceModule.cs` | 12 | `    internal const string CredentialKey = "application.presence.v1";` | 68 / `e21b5c465a2e80280395a1157f9baf6989d6f9c669e5f7a99ab8ea7f4e7df49b` | `b903a616e7450c168a55e40faa1b84f274484321383a5e2aebac5b817fdd2251` |
| `tests/ArcForges.Cloud.Tests/Presence/KeyedPresenceIngressTests.cs` | 13 | `    private const string Key = "application.presence.v1";` | 57 / `6c64ad9767c12a4452be6685253a7e23926c9df85006eb7dac714e92b455da28` | `5d6f7c9de7bdd2d49af1188412adacd0ee2ab420dac8a25c05545da1dfeaa633` |

## 2. Exactly two fingerprint exceptions

Create `Cloud:.gitleaksignore` with exactly the following two sorted, unique LF-terminated full fingerprints and no additional entries, comments, wildcards or partial commit/path/rule matching:

```text
389039026a5daa15503ffdf792ba1ca942e7bc64:src/ArcForges.Cloud/Composition/ApplicationPresenceModule.cs:generic-api-key:12
389039026a5daa15503ffdf792ba1ca942e7bc64:tests/ArcForges.Cloud.Tests/Presence/KeyedPresenceIngressTests.cs:generic-api-key:13
```

A real isolated Git fixture using pinned 8.30.1 confirms that `gitleaks git <target>` discovers `<target>/.gitleaksignore` from a different working directory, and an explicit ignore-path invocation produces the same exact result. Therefore preserve the hosted command unchanged: pinned OCI `c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f`, network-none/read-only repository mount, default all-ref history, redact=100 and no-banner. Do not add log-opts/ref narrowing, rewrite DEV.01 history or rename current source to pretend historical findings disappeared. Preserve `.gitleaks.toml` byte-for-byte, its existing single public session-vector exception, all accepted P2-053 four-line AND tuple groups/count/indexed/adversarial matrices, default rules and every unrelated or unknown finding.

## 3. Closed pre-scan classification validation

Add `Cloud:tooling/gitleaks-classification.ts` as a bounded offline validator. Its only admitted classification is the immutable commit / exact two paths / lines / rule / full fingerprints above. Require the ignore file to equal those two complete canonical rows; refuse missing, duplicate, reordered, extra, partial, malformed, changed commit/path/rule/line or broad entries. Read the actual original Git blobs at the full commit, with bounded subprocess time/output and fixed repository root. A missing historical object or shallow checkout refuses. Require the entire original blob hashes above, exact complete source lines including indentation/declaration/semicolon, line lengths/hashes and independently computed public literal digest. Do not log a failing source line, matched secret, credential or raw scanner report; failures use bounded classification identifiers/reasons only. No current mutable checkout line, self-declared digest or regex alone substitutes for the original immutable Git evidence.

Run this validator before the unchanged secret scanner in the existing quality job, using the existing pinned Node setup. Append `check:secret-classifications` to the ordinary `npm run check` chain and its exact test registration to `package.json`; no new workflow, tool, installation, dependency or scanner version is added. The ordinary test module is `Cloud:tooling/gitleaks-classification.test.ts`. Exercise both genuine original blobs plus missing object, altered whole blob, changed selector byte/hash, changed declaration/indentation/path/line/rule/commit, neighboring credential/trailing-token, extra ignore and duplicate/reordered row negatives. Fixed fingerprint suppression never establishes general safety of the same string elsewhere or a later commit. Preserve every unknown finding as a scan failure. One necessary corrected current-head all-ref scan and ordinary affected validator tests establish the actual handoff; no unchanged scanner retry or unrelated component/runtime suite is required.

## 4. Ownership and evidence boundaries

Only COM.18's supporting writes and notes gain this narrow scope. Original starts, completions, outcomes, evidence, validation, baseline, adoption, original note prefix and all other tasks remain exact; no new delivery task or readiness grant is introduced. Catalog writes the Cloud source after this pair is merged, obtains independent exact-head source review and runs applicable current CI. A passing scan is repository-secret classification evidence, not quota behavior, release signing, OS isolation or deployment acceptance. Preserve accepted input-bound dependency/provenance history; any changed candidate source inputs receive only the genuine new owned successor under existing COM.18 admission.
