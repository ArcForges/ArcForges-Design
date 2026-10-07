# AIR09 public upstream source identity scanner support

Supporting amendment to P2-018, coordination reference 081.

## 1. Actual observed boundary

PLT65 source `e570ef1f8433107b63496ac9576ffbc311b37117` preserves its accepted implementation and scanner workflow. The ordinary full remote history scan observes five `generic-api-key` findings in the original AIR09 commit `d888bd42a83359a60097488a0309f530b152c7cf`. All five contain the same independently verified public upstream revision [`4e71bbe0c078468e00fefbf94b39849389f346e5`](https://github.com/openai/tiktoken/commit/4e71bbe0c078468e00fefbf94b39849389f346e5) of the public `openai/tiktoken` repository. The original declaration, source manifest, validator and genuine test inputs pin source identity; the value is not credential material.

The retained original hosted scan covers 722 commits and the isolated fetched all-current-remote-refs scan covers 723 commits, each with the same five observations. The accepted e570-only ancestry scan covers 642 commits with zero findings. These measured sets explain why accepted PLT65 ancestry alone does not settle the actual full-history gate. They do not authorize omitting AIR09 history or changing scanner scope. Actual source and line identities were independently read from the retained isolated Git objects, not inferred from a redacted hash substring.

## 2. Exact source witnesses

Every row belongs to original commit `d888bd42a83359a60097488a0309f530b152c7cf`. Line numbers describe that immutable witness, not a requirement to preserve mutable line positions. SHA256 is over the complete original UTF-8 line without its line-ending byte; complete normalized source blob identities are retained with the source facts. No body, key, quote or neighboring field may be widened.

| Exact path | Original line | Complete line SHA256 |
| --- | ---: | --- |
| `eng/model-input/acquire.py` | 17 | `1bd935f0c821fd47db2b4876d460a6584e0389c89d417e332b6af03b26368ff3` |
| `eng/model-input/original-source.v1.json` | 5 | `0c4767357942e41aa78b09f5a20d4987dfedabfc677857556e1dc25b075eda00` |
| `src/BuildingBlocks/ArcForges.AI.ModelInput/Engine/BundleValidator.cs` | 71 | `a8566da546f99c9ced7aff5bf8dd3be2d4263e866196bce4f34f8cfca0685b63` |
| `tests/ModelInputTests/BundleValidatorTests.cs` | 25 | `b9443cc8fc143803ec841887769a8a2431faf22420326b664c020b5635a18a9c` |
| `tests/ModelInputTests/OwnedMaterializerTests.cs` | 78 | `9d8fa813b387444fd2d82b17a4c22e716be1630df8ed5b6e6b0ec90fa08d26d5` |

The source-owned proposal is exactly the following five separate groups. Its original retained file bytes have SHA256 `96e9abbeb54ac04fe5b9d7c96b1dccac435fcecea3af6fd248f5d0b00deb13f1`; this formal document normalizes presentation line endings without changing any parsed group. The optional initial newline matches the actual scanner's captured line convention only; the remainder is anchored to the whole original source line. It does not permit a second line, suffix, prefix or different statement.

```toml
[[allowlists]]
description = "Exact AIR.09 public tiktoken upstream commit line: eng/model-input/acquire.py"
paths = ['''^eng/model\-input/acquire\.py$''']
regexTarget = "line"
targetRules = ["generic-api-key"]
condition = "AND"
regexes = ['''^\n?TIKTOKEN\ =\ "4e71bbe0c078468e00fefbf94b39849389f346e5"$''']

[[allowlists]]
description = "Exact AIR.09 public tiktoken upstream commit line: eng/model-input/original-source.v1.json"
paths = ['''^eng/model\-input/original\-source\.v1\.json$''']
regexTarget = "line"
targetRules = ["generic-api-key"]
condition = "AND"
regexes = ['''^\n?\ \ "tiktokenCommit":\ "4e71bbe0c078468e00fefbf94b39849389f346e5",$''']

[[allowlists]]
description = "Exact AIR.09 public tiktoken upstream commit line: src/BuildingBlocks/ArcForges.AI.ModelInput/Engine/BundleValidator.cs"
paths = ['''^src/BuildingBlocks/ArcForges\.AI\.ModelInput/Engine/BundleValidator\.cs$''']
regexTarget = "line"
targetRules = ["generic-api-key"]
condition = "AND"
regexes = ['''^\n?\ \ \ \ \ \ \ \ Exact\(source,\ "tiktokenCommit",\ "4e71bbe0c078468e00fefbf94b39849389f346e5"\);$''']

[[allowlists]]
description = "Exact AIR.09 public tiktoken upstream commit line: tests/ModelInputTests/BundleValidatorTests.cs"
paths = ['''^tests/ModelInputTests/BundleValidatorTests\.cs$''']
regexTarget = "line"
targetRules = ["generic-api-key"]
condition = "AND"
regexes = ['''^\n?\ \ \ \ \ \ \ \ "source":\{"tiktokenCommit":"4e71bbe0c078468e00fefbf94b39849389f346e5","gptOssCommit":"7b583341fe16729127f6d5b94a7b09ccae97e1a1",$''']

[[allowlists]]
description = "Exact AIR.09 public tiktoken upstream commit line: tests/ModelInputTests/OwnedMaterializerTests.cs"
paths = ['''^tests/ModelInputTests/OwnedMaterializerTests\.cs$''']
regexTarget = "line"
targetRules = ["generic-api-key"]
condition = "AND"
regexes = ['''^\n?\ \ \ \ \ \ \ \ \ \ \ \ \{"schemaVersion":"model\-tokenizer\-bundle\.v1","modelId":"model","provider":"workersAi","routes":\["@cf/openai/gpt\-oss\-120b"\],"algorithm":"o200k\-harmony\-bpe\.v1","pretokenizer":"o200k\-scalar\-pattern\.v1","renderer":"arcforges\.harmony\-json\.v1","unicodeVersion":"17\.0\.0","ranks":\{\{Binding\(rankBinding\)\}\},"unicode":\{\{Binding\(unicodeBinding\)\}\},"framing":\{\{Binding\(framingBinding\)\}\},"source":\{"tiktokenCommit":"4e71bbe0c078468e00fefbf94b39849389f346e5","gptOssCommit":"7b583341fe16729127f6d5b94a7b09ccae97e1a1","rankSha256":"446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d","unicodeVersion":"17\.0\.0","unicodeDataSha256":"2e1efc1dcb59c575eedf5ccae60f95229f706ee6d031835247d843c11d96470c","unicodePropertiesSha256":"130dcddcaadaf071008bdfce1e7743e04fdfbc910886f017d9f9ac931d8c64dd"\},"legal":\["controlled\-owner\-association"\]\}$''']
```

## 3. Minimum source scope and preserved scanner

Append these five groups only to DesktopPlatform `.gitleaks.toml`, under AIR09's sole source owner `w-codex-20261006-image`. Each group requires both its exact anchored repository path and its exact whole original line, with `regexTarget = "line"`, `condition = "AND"` and `targetRules = ["generic-api-key"]`. Do not apply a value-only, repository-wide, arbitrary public-digest, rule-wide or path-only exception. All default rules, existing accepted groups and their original bytes remain intact.

The actual e570 configuration has 4 existing allowlist groups; this candidate appends exactly five, yielding 9 against that measured prefix. If another admitted configuration change is actually accepted first, preserve its entire real incoming prefix and append these same five groups once; recompute the factual count instead of overwriting incoming groups or imposing the stale total. No scanner version, history/ref traversal, workflow trigger, command, output policy, secret rule or product code change is admitted. Preserve all earlier source and task publication facts; this supporting repair is not a retrospective claim that a failed full-history run passed.

## 4. Meaningful affected validation

Independently verify all five original Git paths, complete source blobs and source lines, and their exact public upstream source revision. Parse the actual configuration and require each new group to have the single exact path, single exact line, AND condition and sole generic-api-key target. Preserve the accepted prefix byte-for-byte. Validate the same pinned ordinary full-history scanner over the genuine retained history after the admitted source change.

Use bounded hostile source fixtures or equivalent direct scanner evidence to show that adjacent and foreign paths, a changed commit digit, wrong key or quotation, leading or trailing text, two-line composition and a different scanner rule remain unsuppressed. A public commit substring alone never suffices. No broad product test suite, dependency reinstall, duplicate passing compiler phase or post-publication package download is prescribed for this scanner-only edit. Current source-specific CI remains mandatory, and no unchanged failed scan is retried as proof.

## 5. Ownership and truthful delivery

Governance authors this paired planning repair; Policy is the sole independent full planning reviewer. Native/Image remains AIR09's sole implementation owner. Observer owns the retained PLT65 scanner facts and actual publication evidence; this amendment does not transfer that source or claim. Root remains the sole Design/Plan fence owner. Source edits require actual reviewed paired admission, then independent exact-head source review and applicable current CI.

Only AIR09 supporting writes and notes change. Preserve every existing task identity, start/completion prerequisite, obligation, outcome, validation, baseline, source/legal admission, package boundary and accepted record. A public source commit exception does not prove Unicode legal evidence, signed artifact materialization, current Config readiness, tokenizer correctness, OS behavior, serving permission or whole AIR09/PLT65 acceptance. Preserve exact provenance and active input maps; inspect real evaluated-input membership before any immutable receipt successor, and never fabricate an empty dependency receipt for a configuration-only edit outside the input closure.
