# Product Naming Policy

Authority: [P2-015](../decisions/phase-2-specification-decisions.md#rule-p2-015), implementing the [portfolio](../requirements/00-product-scope-and-portfolio.md), [glossary](../requirements/01-normative-glossary-and-invariants.md) and P2-012/P2-013. Owner: Contracts for policy data/tooling; each product retains its application and format ownership.

## Single machine-readable authority

`Contracts/eng/policy/product-names.json` is the only authored naming-data file. It is Apache-2.0 interoperable policy data, not business code, a new runtime API or a generated package prerequisite. Its versioned schema records the effective Design commit, closed wire ProductId set, display names, reserved namespaces, installed identities, file-association reservations, forbidden-name dispositions, retired wire IDs, provider roles and exact provenance exceptions. Unknown fields, duplicate JSON keys, duplicate identities and invalid mappings fail validation. A naming change requires a Design decision and compatibility review before updating this file.

| Identity | Kind / owner | Stable names and compatibility |
|---|---|---|
| `arcnotes` / ArcNotes | Desktop / ArcNotes | Managed namespaces `ArcNotes`, `ArcForges.ArcNotes`; installed bundle/auth scheme `com.arcforges.arcnotes`; existing assembly `ArcForges.ArcNotes` |
| `arcscope` / ArcScope | Desktop / ArcScope | Managed namespaces `ArcScope`, `ArcForges.ArcScope`; installed bundle/auth scheme `com.arcforges.arcscope`; existing assembly `ArcForges.ArcScope` |
| `arcslate` / ArcSlate | Desktop / ArcSlate | Managed namespaces `ArcSlate`, `ArcForges.ArcSlate`; installed bundle/auth scheme `com.arcforges.arcslate`; existing assembly `ArcForges.ArcSlate` |
| `companion` / ArcChat | Android and Web / Mobile and Web | Formal Android package `com.arcforges.mobile`; observed prerelease `io.github.arcforges.mobile` remains until WP30's explicit reinstall migration. Web output names remain `site`, `account`, `chat`, `operations`. |
| `assistant` / ArcChat | Embedded feature / DesktopPlatform | `ArcForges.Assistant` package/namespace family; retained ArcChat vocabulary identifies features only. No separate application, wire ProductId, installation, executable or file association. |

`arcchat`, `arcchat-mobile`, `mobile` and `web` are retired wire product values, not aliases. Historical compatibility vocabulary in types or documentation does not reactivate them. `cloud` names a service, not a client ProductId. Paddle is the sole customer-facing MoR; Payoneer is payout-only. The forbidden-name list and historical dispositions implement glossary section 8 without creating migration aliases. Existing NuGet/npm/Maven Hello identities remain unchanged; the naming file does not rename published packages.

## File-association reservations

| Owner / format | Extension | Windows ProgID | Apple type identifier | State |
|---|---|---|---|---|
| ArcScope native project | `.arcscope` | `ArcForges.ArcScope.Project` | `com.arcforges.arcscope.project` | Reserved; WP33/WP35 own format/open/import semantics, WP53 installs the handler |
| ArcSlate native project | `.arcslate` | `ArcForges.ArcSlate.Project` | `com.arcforges.arcslate.project` | Reserved; WP36/WP39 own format/open/import semantics, WP53 installs the handler |
| ArcNotes, companion, embedded assistant | None | None | None | No private native archive/association is added; existing export formats remain authoritative |

Reservations are names for the already required native formats, not evidence that a reader, writer, OS association or installer exists. Format versions remain separate. Common interchange formats, including Markdown, JSON, media and OTIO, use explicit Open/Import/Open with and never seize system defaults. No private association is registered until its owner can validate and open that format with the required recovery behavior. Authentication callback schemes retain their existing separate security semantics.

## Scan boundary and exceptions

WP00.00 scans all nine implementation repositories using their actual Git file inventory: tracked paths and contents, plus non-ignored untracked files for local pre-commit validation. There are no source-directory assumptions; root manifests, CI, generated source, tests, assets and implementation notes are included. Scan case-insensitively, including substrings in identifiers/paths and UTF-16 resource text. A missing/unreadable tracked file or unsupported symbolic entry fails rather than silently reducing coverage. Ignored build products and Git history are not current source inventory. Shipped-archive verification remains the owning release gate.

The one policy file is parsed with a closed schema and its designated forbidden/disposition fields validated as policy declarations. It is not a free-text bypass; any forbidden name outside those designated fields fails. Negative tests create temporary Git repositories and derive forbidden inputs from the validated policy; no checked-in fixture directory is broadly exempted.

The only permitted exception names are the two existing media reference repositories in WP00 BR-02. Each exception pins the scanned repository, an exact `docs/provenance/` or `eng/provenance/` file, its SHA-256, the exact permitted reference name(s), and a reason. The one pre-existing tracked provenance artifact, DesktopPlatform `artifacts/evidence/traceability/feature-trace-bridge.json`, is also eligible at SHA-256 `f4a8f47549a96e529af5af9582f07a81dd97af73f006ba3c4436c624210a0976`; all 50 matches are fixed-commit entries in `sourceBaselines` arrays. No other artifact path is admitted. Retaining this historical provenance does not accept its old step identifiers as current requirements. It admits those names in that provenance file's content only, never in a runtime/source file, identifier or path. Changed bytes, unused entries, other forbidden names and overly broad paths fail. An empty exception list is valid and preferred when no occurrence exists. Exceptions authorize naming only, never reuse or a licence determination.

Contracts CI runs policy validation, its own scan and adversarial tests. WP00.00 additionally records the nine-root scan with commit, dirty state, policy digest, file count, exceptions used and result per root; invoking a read-only inventory tool from outside a target is not a target build dependency. WP02/WP05 package and integrate continuing repository enforcement through their prescribed artifact process. No consumer imports sibling source, copies a second authored authority or requires a future published policy package at WP00.

## Verified external constraints

Checked 2026-09-18: [Microsoft ProgIDs](https://learn.microsoft.com/en-us/windows/win32/shell/fa-progids) bind application-specific file types; [Apple type declarations](https://developer.apple.com/documentation/uniformtypeidentifiers/defining-file-and-data-types-for-your-app) use unique reverse-DNS identifiers; [Android application IDs](https://developer.android.com/build/configure-app-module) must remain stable after publication. These constrain identifier syntax and installation continuity, not new product scope. The already adopted WP30 rename is explicitly before production/Play distribution and requires development-prerelease reinstall. No store registration, trademark availability, signed installer or live payment capability is inferred.
