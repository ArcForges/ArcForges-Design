# WP01.00 current inventory profile

Authority: [WP01.00](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.00), [project and package ownership](../architecture/27-platform-projects-and-application-assistants.md), [package registry](../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), and [WP00 stage receipt](wp00-stage-acceptance.md).

## Scope and decision

DesktopPlatform owns `eng/policy/reconciliation/` and its portable read-only drift checker. This is policy data, not a shared source repository or a build dependency of another owner. Each of the nine independent repositories retains its own source, license, runtime, CI and published candidate. CI may fetch exact Git snapshots to audit their trees; it must not compile adjacent source as a consumer dependency.

The inventory records every current build project recognized by the existing licence inventory, every historical C# project in `ede43db5b2237104dd0008b99398090c54a2cf94`, and the planned directory families in architecture 27 and the package registry. Preserve the historical measurements; do not reinterpret 166 old projects as 166 missing current projects. Include native shim dispositions separately from managed project rows. Current projects carry an explicit disposition and producing step; retained bootstrap projects do not claim full product behavior.

Each planned directory has exactly one repository owner, an explicit Keep, Move or Retire disposition, current presence, and a named implementation producer. Keep includes a required future directory whose creation belongs to that producer; absence is not permission to create placeholders. Move describes a target migration, not proof that it has occurred. Retire means the old directory is excluded from the current graph; retain its history and provenance. Historical item detail may refine these classes using the existing Rename/Split/Merge/Rewrite/Fence/Delete vocabulary, with an explicit reason and target owner. Assign shared historical test mechanisms to DesktopPlatform and product/provider tests to their actual owner; WP01.04 supplies test-family coverage, not this inventory.

## Immutable observations and drift

Record all nine origin URLs, full source commits, tree identities, clean primary states and worktree branches/commits. Bind the observation to the exact WP00 published-candidate receipt and its file hash. Existing Hello, native probes and signed Android identity remain compatible. Archived real-runtime evidence retains its original service revision and date; a new inventory does not turn it into a new runtime run.

The checker compares the 166 historical paths and Git blob identities to the bound historical tree, the current project sets to each owner's Git tree and licence inventory, and all planned directory presence to those same snapshots. Reject unknown/duplicate owners, incomplete/duplicate paths, unsafe paths, missing targets or producing steps, changed pinned identities, source links and submodules. Reuse the existing licence/reference/runtime checks instead of introducing another build system. The checked DesktopPlatform worktree may add this inventory and its checks; its project graph must still match the observed snapshot. A fresh family audit accepts nine explicitly supplied roots and reports their actual commits and cleanliness; snapshot verification must never label stale pins as current heads.

## Validation and follow-through

Exercise actual Git fixtures for missing/extra projects, changed historical blobs, linked source/submodule entries and incomplete directory ownership. Windows and Linux CI run the drift checker before package publication. Record source checks separately from candidate/runtime evidence. Compare the published source commits and candidate identities to the WP00 receipt; unchanged public artifacts need not be republished by their owners solely to restate their inventory. Any new DesktopPlatform main candidate still follows its existing full CI, publication and public-byte verification.

This step neither assigns individual contract types (WP01.01), finishes shared mechanism review (WP01.02), implements native capabilities (WP01.03/WP13), maps all test families (WP01.04), nor executes later source moves (WP01.05). Those obligations remain explicit. The current nine roots replace the retired monorepo as the integration unit; Cloud's 21 module owners and AI's sole Harness replace historical in-host AI/AppHost assumptions without changing accepted product scope.
