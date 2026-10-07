# CON26 GOV26 consumer public-source digest support

Supporting amendment to P2-018, 2026-10-07 (coordination reference 053). This is a narrow CON.26 supporting-scope repair. It preserves the completed GOV.26 producer, generated operation catalogue, qualified metadata bindings, and the original selected delivery scope. Governance remains the Contracts source/integration owner; Native Image is the independent planning and final source-delta reviewer.

## Actual observation and public-source proof

The current consumer uses the genuinely normally published Build.Policy `1.0.0-ci.124.1` from DesktopPlatform `6e7b92097228c2b73c6156625b156fa240a2c81b`. Its clean Contracts checkpoint is `b5e8842ed2d4af596622f21d9a63ead49b65661f`. Hosted Security run `37585952828`, job `112675991497`, failed only the pinned full-history generic-api-key scan before the architecture stages ran. The redacted log contains six observations: `eng/policy/dependency-policy.json` lines19/2516 and `eng/policy/dependency-reviews/con-26-r4.json` lines22/85/154/211. Each is a public dependency-input digest. The exact frozen Git source bytes, with the repository's LF normalization, independently recompute all four values below; no credential material is involved.

| Input key | Exact SHA256 | Permitted containing files |
| --- | --- | --- |
| `eng/policy/contract-access.json` | `165e911588b1f9e07fa12b94ea43e70544415b4cd85ab6656e241e727d01972d` | `eng/policy/dependency-policy.json`, `eng/policy/dependency-reviews/con-26-r4.json` |
| `eng/provenance/records/dokka-combokeys-licence-r1.json` | `75219d61672002f0bb242fed0fd93a0886f07d944e0b9e1b1f72132f59df1b41` | `eng/policy/dependency-reviews/con-26-r4.json` |
| `eng/provenance/records/dokka-object-keys-licence-r1.json` | `55621ecc7032745ca46e56d13133dc22a3bd808d80966d737427b5d6fc5bd096` | `eng/policy/dependency-reviews/con-26-r4.json` |
| `src/public/dotnet/ArcForges.Contracts.PublicApi/ArcForges.Contracts.PublicApi.csproj` | `986b7a97734cd5d0630e548da897869de322a112c087c2d0df6a0bfc98b8784c` | `eng/policy/dependency-reviews/con-26-r4.json` |

## Minimum repair and immutable-prefix coordination

Append exactly two `condition="AND"` allowlist groups targeting only `generic-api-key` and `regexTarget="line"`. One has exactly the current contract-access key/digest and the two exact containing paths; the other has exactly the three historical source key/digest lines and only the exact r4 receipt path. Each regex is anchored to the complete JSON key/value line, with only ordinary surrounding whitespace and optional trailing comma. There is no digest, key, path, credential, rule or line-content wildcard.

The frozen consumer configuration has93 groups: accepted main8715's85 followed by eight already reviewed CON26 historical groups. Adding the two groups in isolation gives95. CON31 was actually accepted as `c990df25dbe721b0df2d8e7aedc28e02468ae3e1` with its four reviewed groups, making the accepted prefix89. The natural CON26 union therefore has **99** groups: the byte-preserved accepted89, the same eight CON26 historical groups, then only the new `[1,3]` groups. The test cardinality/vector must reflect that real union. Never discard incoming accepted groups, replace historical receipts, or fabricate an orphan receipt fork merely to retain95. Any later accepted-prefix change needs factual coordinated maintenance and independent exact-head review.

The existing `test_dependency_admission.py` may derive these expected values from the exact frozen b5 Git JSON and rehash the corresponding source blobs. That avoids adding a new digest-literal exception for Python test source. Add meaningful checks for all six original observations, four unique source tuples, exact allowed paths/rule/whole-line boundaries, and refusal of changed keys/digests, wrong receipts/paths, adjacent credential text, multiple lines and arbitrary credential payload. Maintain all prior group/tuple/count checks and append only the owned vector. Preserve every default rule, existing scan invocation, source output, dependency closure/input mirror and accepted immutable record.

## Delivery and acceptance

This repairs a measured source-classification false positive; it does not waive scanning or the architecture gate. Run the affected admission regression, real pinned full-history scanner and all applicable latest-head CI. Require independent exact-head source review, fenced merge, normal source-bound publication and factual ledger delivery. Actual current contract access/provenance and published124 private-host component evidence remain distinct from whole-series deployment, operating-system isolation and commercial end-to-end acceptance. No repeated old failing CI, history rewrite, success stub or copied policy source is admitted.
