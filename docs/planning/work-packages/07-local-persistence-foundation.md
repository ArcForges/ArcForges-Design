<a id="rule-wp-07"></a>

# WP-07 — Local Persistence Foundation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `04`, `06` · Downstream: `08`, `13`, `18`, `33`, `36`

> **Goal.** Build the local storage foundation every desktop product shares: the canonical commit unit, the journal, snapshots, the migration runner, the managed resource store and the derived-store separation — with crash recovery proven, not assumed.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform managed mechanisms; product owners. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The seven-part store composition of the persistence architecture, implemented as reusable mechanism: the working store, the write path, the journal, snapshots, the managed resource store, the large append store and the derived store, plus the migration runner and the storage-pressure model.

**Out of scope.** Any product's schema — those land with their products. Cloud persistence (`21`). Sync (`25`). The portable package format, whose *mechanism* is here but whose per-product content is in each product package.

**Why this package exists.** [QI-08](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-08) states that crash-free is not recoverable and [QI-10](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-10) that cache recovery is not canonical data recovery. Both are only true if the journal and snapshot mechanism exists once, correctly, rather than four times approximately.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../architecture/06-data-persistence-and-formats.md`](../../architecture/06-data-persistence-and-formats.md) | Store composition, canonical commit unit, journal, snapshot, migration mechanics, storage pressure |
| [`../../requirements/13-data-formats-and-portability.md`](../../requirements/13-data-formats-and-portability.md) | The five layers, save semantics, and the undo/revision/checkpoint/journal separation |
| [`../../architecture/04-desktop-application-architecture.md`](../../architecture/04-desktop-application-architecture.md) `§5` | Recovery, native crash handling and safe start |
| [WP-04](04-identity-error-and-versioning-primitives.md#rule-wp-04) output | Revision, sequence, time and reason-code primitives |
| [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) output | A proven AOT host to run the store inside |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **There is exactly one write path.** Every mutation — UI, RPC, agent, import, sync — goes through the same eight steps (`§4` of the architecture overview). |
| BR-02 | **The canonical commit unit is atomic**: a commit either applies fully or not at all, with its revision advanced exactly once. |
| BR-03 | **Undo, revision, checkpoint and journal are four different things** and never substitute for one another ([QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)). |
| BR-04 | **A derived store is fully reconstructable**, and deleting every derived store leaves the product intact ([QI-10](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-10)). |
| BR-05 | **The executable directory is never a user data directory** ([UP-05](../../requirements/10-distribution-update-and-support.md#rule-up-05) in the distribution requirements). |
| BR-06 | **Storage schema version equals the highest applied migration** (`§4` of the build architecture). |
| BR-07 | **Migration is independent of the installer** and has its own recovery path ([UP-08](../../requirements/10-distribution-update-and-support.md#rule-up-08) there). |
| BR-08 | **A resource identity is never a file path** ([I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)), and the managed resource store resolves identity to location. |
| BR-09 | **Large append data does not live in the working store** — captures and similar streams use the chunked verifiable store. |
| BR-10 | **Persistence types never cross an application boundary.** Repositories expose domain types only. |
| BR-11 | **Writes are serialised per store; reads are concurrent.** Single-writer discipline is structural, not conventional. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.Persistence/` | Created or reconciled: store abstraction, write path, journal, snapshot, migration runner |
| `src/BuildingBlocks/ArcForges.Persistence.Sqlite/` | The local working store provider |
| `src/BuildingBlocks/ArcForges.Persistence.Resources/` | The managed resource store and the large append store |
| `src/BuildingBlocks/ArcForges.Persistence.Derived/` | The derived-store abstraction with rebuild semantics |
| `fixtures/formats/` | Seeded with the first schema version fixture |
| `tests/PersistenceRecoveryTests/` | Extended to the full crash and recovery matrix |
| `tests/MigrationTests/` | Created: forward and backward migration with golden fixtures |

**Major types introduced.** `IStore`, `CommitUnit`, `WriteCommand`, `JournalEntry`, `SnapshotDescriptor`, `MigrationStep`, `StorageSchemaVersion`, `ManagedResourceRef`, `AppendStream`, `DerivedStore`, `StoragePressureState`, `RecoveryOutcome`.

---

## 5. Required implementation work

<a id="rule-wp-07.00"></a>

### WP-07.00 — Store abstraction and the single write path

**Required design implementation and verification.** Commit payload and origin in the same owner transaction/journal boundary, with history pins and bounded GC. Kill between staging and commit: neither an origin-less completed payload nor a marker referencing absent bytes becomes visible. Migration records unknown for legacy input; unsupported writers refuse destructive round trips.

**What must be fully done.** Use typed LocalNotesVersion(acked_rev, head_local_seq), NativeContentRevision and CloudRevision separately; the materialised body/journal/index token must agree.  The store abstraction with the transactional write path implemented once: validate → authorize → begin commit unit → apply → journal → advance revision → enqueue publication/outbox → commit → notify from committed state. Every caller uses it. Persistence types do not leak past the repository boundary. Writes are serialised; reads are concurrent.

**Testing requirements.** Replay pending edits and remote-shadow advances, then verify query/index stale-work CAS rejects the old composite token.  A test asserting no alternative write path exists (policy test); concurrency tests for serialised writes and concurrent reads; a boundary test that no storage type appears in an application signature.

**Completion gate.** A local body cannot change without a new materialised version token.  One write path, enforced by a policy test; concurrency semantics correct.

<a id="rule-wp-07.01"></a>

### WP-07.01 — Journal

**What must be fully done.** An append-only journal recording every commit with enough information to replay. Journal writes are durable before a commit is acknowledged. Journal growth is bounded by snapshotting, and truncation is safe under concurrent read.

**Testing requirements.** A durability test using a simulated process kill between journal write and commit acknowledgement; a replay test; a truncation-under-read test.

**Completion gate.** A kill at any point in the write path leaves the store recoverable to a committed boundary with no torn state.

<a id="rule-wp-07.02"></a>

### WP-07.02 — Snapshot and recovery

**What must be fully done.** Snapshots are taken on a policy, are self-describing, and are verifiable. Recovery selects the latest verifiable snapshot and replays the journal forward. Recovery outcomes are typed: clean, recovered-with-loss-of-uncommitted-work, or unrecoverable-with-preserved-evidence. A native crash and a safe-start path are handled (`§5` of the desktop architecture).

**Testing requirements.** A recovery matrix: clean shutdown, hard kill, kill during snapshot, kill during migration, corrupted snapshot, corrupted journal tail, and disk-full during write.

**Completion gate.** Every case in the recovery matrix produces a named, correct outcome, and no case produces silent data loss.

<a id="rule-wp-07.03"></a>

### WP-07.03 — Migration runner

**What must be fully done.** Numbered migrations with a runner that is transactional per step, idempotent, and resumable after interruption. The storage schema version equals the highest applied migration. A downgrade path is defined: either supported with an explicit reverse migration, or refused with a clear message and no partial change.

**Testing requirements.** Forward migration from every historical version fixture; interruption and resume; a refusal test for an unsupported downgrade; a golden-fixture semantic comparison proving migration preserves meaning, not merely structure ([QI-07](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-07)).

**Completion gate.** Every historical fixture migrates forward correctly, interruption is resumable, and an unsupported downgrade refuses cleanly without partial change.

<a id="rule-wp-07.04"></a>

### WP-07.04 — Managed resource store

**What must be fully done.** Content-addressed storage for managed resources with identity-to-location resolution, integrity verification, reference counting, and a garbage-collection path that never deletes a referenced object. Resource identity is never a path.

**Testing requirements.** Integrity verification on read; a reference-counting test including crash between reference and store; a garbage-collection safety test.

**Completion gate.** Integrity is verified on every read, and garbage collection never removes a referenced object even after a crash mid-operation.

<a id="rule-wp-07.05"></a>

### WP-07.05 — Large append store

**What must be fully done.** A chunked, verifiable append store for high-rate data with per-chunk checksums, an explicit end marker, and honest truncation semantics — a crash leaves a verifiable prefix plus a recorded loss, never a silently short file.

**Testing requirements.** Append-under-kill tests at chunk boundaries and mid-chunk; verification of the recovered prefix; a loss-record assertion.

**Completion gate.** A crash mid-append yields a verifiable prefix with the loss explicitly recorded.

<a id="rule-wp-07.06"></a>

### WP-07.06 — Derived stores and storage pressure

**What must be fully done.** The derived-store abstraction with declared rebuild semantics: every derived store can be deleted and rebuilt from canonical data. Storage pressure is modelled with visible states and an eviction policy that only ever evicts derived data.

**Testing requirements.** A delete-and-rebuild test per derived store kind; an eviction test asserting canonical data is never evicted.

**Completion gate.** Deleting every derived store leaves the product fully intact, and eviction cannot touch canonical data.

---

<a id="rule-wp-07.90"></a>
### WP-07.90 — Verify the owned artifact and real integration

**What must be fully done.** Package desktop persistence mechanisms; retain product-owned canonical schemas, journal/snapshot/pending-edit distinctions and corruption/recovery rules. RN storage follows the same public semantics through Mobile's implementation.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Package consumption does not centralize product data ownership; pending edits, interrupted commits and unknown-schema behavior retain their current profile results.

**Completion gate.** Package consumption does not centralize product data ownership; pending edits, interrupted commits and unknown-schema behavior retain their current profile results. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | This package defines the local database contract every product schema plugs into |
| Protocol | Revision semantics from `04` become observable through the change publication step |
| UI | Save semantics, recovery prompts and storage pressure states become available to the shell |
| Security | The write path is where owner-side final validation is enforced for local stores |
| Platform | Per-platform data directory resolution and file-locking behaviour |
| Migration | This package *is* the migration mechanism |
| Compatibility | Storage schema version and the fixture corpus start here |

---

## 7. Tests and verification evidence

**Required evidence addition.** [WP-07.00](#rule-wp-07.00) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Single-write-path policy test result | [WP-07.00](#rule-wp-07.00) |
| Durability and replay results | [WP-07.01](#rule-wp-07.01) |
| The full recovery matrix with a named outcome per case | [WP-07.02](#rule-wp-07.02) |
| Migration results against every historical fixture, plus semantic comparison | [WP-07.03](#rule-wp-07.03) |
| Integrity, reference-counting and garbage-collection safety results | [WP-07.04](#rule-wp-07.04) |
| Append-under-kill results with loss records | [WP-07.05](#rule-wp-07.05) |
| Rebuild and eviction results | [WP-07.06](#rule-wp-07.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-07.90](#rule-wp-07.90) and all inherited domain-specific gates must pass on the same candidate closure. Package consumption does not centralize product data ownership; pending edits, interrupted commits and unknown-schema behavior retain their current profile results.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Exactly one write path exists and is enforced by a policy test; write serialisation and read concurrency are correct.
2. A process kill at any point in the write path leaves the store recoverable to a committed boundary with no torn state.
3. Every case in the recovery matrix produces a named, correct outcome with no silent loss.
4. Every historical fixture migrates forward with semantics preserved; interruption resumes; unsupported downgrade refuses without partial change.
5. Managed resource integrity is verified on read and garbage collection never removes a referenced object.
6. A crash mid-append yields a verifiable prefix with the loss explicitly recorded.
7. Deleting every derived store leaves the product fully intact, and eviction never touches canonical data.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-04](04-identity-error-and-versioning-primitives.md#rule-wp-04)
- [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)

**Downstream — consumers of these released outputs.**

- [WP-08](08-local-ipc-and-registration.md#rule-wp-08)
- [WP-13](13-high-risk-technical-probes.md#rule-wp-13)
- [WP-18](18-arcnotes-document-core.md#rule-wp-18)
- [WP-33](33-arcscope-acquisition-and-session.md#rule-wp-33)
- [WP-36](36-arcslate-project-and-timeline.md#rule-wp-36)


---
