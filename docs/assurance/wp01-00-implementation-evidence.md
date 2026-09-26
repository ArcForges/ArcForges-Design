# WP01.00 implementation evidence

Scope: [verify nine independent current repositories](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.00), under the [inventory profile](wp01-00-inventory-policy.md). This receipt records inventory and policy acceptance, not completed product behavior.

## Authority and change

[Design PR32](https://github.com/ArcForges/ArcForges-Design/pull/32), merge `33bcddd9508ec60c0a2b0d7b53901ee7f50d0a70`, corrected historical licence/current-root and Cloud ownership wording before dependent implementation. It preserves the old 166-project evidence and forbids placeholder reconstruction.

[DesktopPlatform PR53](https://github.com/ArcForges/DesktopPlatform/pull/53), reviewed head `94d48e8b441d6d1cb9164b34eb543a25c10c1522`, merged as `b7744f3ffdeae161d8a3e34243aad3b8e8b47978`. The complete reviewed diff SHA256 is `1dcc43c994bbe6cad8e229f7f11d09c794d2680cc9ad57a4155a16eb42849f64`. All 20 checks passed in [PR CI](https://github.com/ArcForges/DesktopPlatform/actions/runs/35539555597).

The implementation owns `eng/policy/reconciliation/{source,current,historical,directories,native}.json`, `eng/reconciliation.py`, its tests and Windows/Linux CI gates. All new files are in the source provenance inventory. Other implementation repositories retain their source and published identities.

## Inventory and dispositions

| Inventory | Verified coverage |
|---|---|
| Current repositories | Nine independent origins, full commits and tree hashes, clean primary checkouts, retained worktree branch/commit observations |
| Current build projects | 75: DesktopPlatform 35, Contracts 15, ArcNotes 4, ArcScope 4, ArcSlate 4, Cloud 5, AI 1, Web 4, Mobile 3 |
| Historical C# projects | All 166 paths and blob identities from `ede43db5b2237104dd0008b99398090c54a2cf94`, each with current presence/change status, target owner, disposition, producer and reason |
| Planned/current directories | 359 explicit owner/path records, including all 21 Cloud module owners and their three layers, seven native managed families with six RID families each, and six helper runtime directories |
| Historical native entries | Six shims plus shared; retain five admitted foundations and shared support, exclude MDF. Full admission/surface work remains WP01.03/WP13 |

Keep may denote a required future directory under its producing step; it does not authorize an empty placeholder or assert implemented behavior. Old Notes Edgeless/Slides and standalone ArcChat/hub paths remain retired. Contract schema ownership is assigned to Contracts, while individual type visibility is WP01.01. Old .NET Mobile/Web projects are historical; current Kotlin/Compose and React/TypeScript bootstrap outputs remain intact. The actual generated C# directory is `src/public/dotnet`; the old `csharp` spelling is not recreated.

## Source and runtime evidence boundaries

The inventory pins the [WP00 stage receipt](wp00-stage-acceptance.json) by SHA256 `69e06cd1248f61b5da2509184430ffc8c1f96d5c8550dd790f87e432393cc340`. Fresh remote-main and CI queries confirmed all nine recorded pre-change commits still matched that receipt. The new DesktopPlatform merge is a policy-only successor; the other eight commits and candidate identities remain unchanged.

| Owner | Recorded source | Existing published candidate |
|---|---|---|
| DesktopPlatform | `08c46ab9fe955c60c28e7106df519eb55bd8e3ba` | `1.0.0-ci.15.1`; successor below |
| Contracts | `d716045854e2e401a1a536ba2ee5c62ad1c4e8ab` | `1.0.0-ci.58.1` |
| ArcNotes | `e40423a1b14ce8341de35748cc2a093c7c9b77a7` | `0.1.0-ci.8.1` |
| ArcScope | `d247dcff36fd1123a70e5e59967a9b2294a2eeac` | `0.1.0-ci.8.1` |
| ArcSlate | `b0d255f54fb560a534cc493d5645ca4bc7b4bd0e` | `0.1.0-ci.8.1` |
| Cloud | `4571ec8692235485712d4c4e3ef4886c162f2574` | `0.1.0-ci.18.1` |
| AI | `944edfe88718fc5f72a42ea0bed1c495307c22df` | `0.1.0-ci.26.1` |
| Web | `84939ca1fde0f0653d2cb4d8b8f9e5dd1057abb5` | `0.1.0-ci.22.1` |
| Mobile | `5031d837d2e7bf9dd1b681c837c942d2b74dc65e` | `0.1.0-ci.14.1` |

WP00's exact NuGet/npm/Maven/native, five-RID desktop, browser, signed Android, Container/Worker and AI Workflow receipts retain their original scenario and runtime/service revisions. This inventory did not rerun those unchanged applications or a paid model call. In particular, archived desktop UI/transport proofs still name their older observed Cloud revision; they are not recast as new end-to-end runs.

## Checks and review

- Fresh read-only nine-owner audit and independent pinned Git snapshot audit passed; no adjacent owner was compiled as a source dependency. The merged DesktopPlatform checkout also passed the fresh audit.
- All 103 Python policy/provenance test groups passed (62 policy, including six reconciliation fixture groups, plus 41 provenance). Real Git fixtures reject missing/extra projects, modified historical blobs, source symlinks, gitlinks, wrong owners/origins, incomplete targets, unsafe paths and escaped project references.
- SDK 10.0.400 locked restore, Release build and all four current .NET architecture tests passed, with zero build warnings/errors. Pre-commit and source provenance checks passed.
- Windows/Linux CI inventory reports were downloaded and matched all counts. The CI graph requires both before packing; existing native compilation/tests and isolated empty-cache consumers remained required.
- Full review corrected equivalent GitHub origin URL handling, historical assistant/Mobile test destinations, helper RID entries and a local UTF-8 editing issue. The corrected exact PR head passed all checks; no finding remains open.

## Main candidate and public verification

[Main CI](https://github.com/ArcForges/DesktopPlatform/actions/runs/35539950237) completed successfully on the merge. Candidate `1.0.0-ci.16.1` contains ten NuGet packages, with manifest SHA256 `54a8e94c8ce7d143446e118e67d8b5fa11051aede1961efc42988aed688c510a`. Every candidate package hash matched. Windows/Linux empty-cache package consumers and Windows Native AOT runtime consumers passed before publication.

All ten public NuGet packages were downloaded and all **599 original ZIP members** matched the tested candidate exactly. Only registry-added `.signature.p7s` was excluded from member comparison. Initial 404 responses cleared after registry processing; retries and cache-busting requests were used without republishing or overwriting any version. Exact public package hashes are in the [machine-readable receipt](wp01-00-implementation-evidence.json). The main CI and public-availability gates passed; no pending prerequisite remains for WP01.00.

## Retention and remaining scope

Retained branches/worktrees: Design `codex/wp01-00-inventory-policy` and `codex/wp01-00-completion-evidence`; DesktopPlatform `codex/wp01-00-reconciliation-inventory`, each under its repository's `.worktree/`. Primary checkouts were pulled after each merge. Existing branches/worktrees were preserved.

No external prerequisite blocked the inventory step. Contract type assignment, shared-foundation content review, native surface execution, test-family mapping and physical reconciliation remain the separate WP01.01 through WP01.05 obligations. Full commercial activation is not inferred from this policy receipt.
