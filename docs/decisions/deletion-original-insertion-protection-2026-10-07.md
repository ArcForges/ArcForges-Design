# Account-deletion original insertion protection

This narrow supporting-scope repair preserves every original task outcome, dependency and acceptance obligation. CLOUD.79 remains the sole deletion lifecycle producer; CLOUD.17 composes the complete proof, revocation, notification and purge transaction. No CLOUD.79-to-CLOUD.83 dependency or authentication completion cycle is introduced. The original Final selection and all accepted migrations remain unchanged.

## Actual failure and owner repair

The unpublished Identity deletion migration0025 previously protected original disclosure only through BEFORE UPDATE and BEFORE DELETE. An actual migrated SQLite negative proved INSERT OR REPLACE can implicitly delete the existing row when recursive triggers are disabled, replacing the original grace deadline/policy while retaining revision1. Both primary-key replacement and replacement through the active User partial unique index must refuse. Connection settings, an application pre-read or a stronger UPDATE guard cannot substitute for this persisted invariant.

CLOUD.79 now owns the exact BEFORE INSERT trigger `tr_identity_account_deletion__original_insert`. It refuses either an existing `deletion_id`, or a new row with state Pending1/Purging3 when that same User already has a Pending1/Purging3 lifecycle. It raises the existing closed `af_immutable_identity_account_deletion` constraint refusal. The fixed predicate is:

```sql
EXISTS (SELECT 1 FROM "identity_account_deletion" WHERE "deletion_id" = NEW."deletion_id") OR (NEW."state" IN (1, 3) AND EXISTS (SELECT 1 FROM "identity_account_deletion" WHERE "user_id" = NEW."user_id" AND "state" IN (1, 3)))
```

This matches the actual still-unpublished migration0025 SHA256 `4a51237e996b1b45799ffe3c14f97e5d6145b9ae5f9c0951b8a8a3ea23c0e643`. The original `f19739b338cda9b9da8a85a1da9deaad35d70b4ffffd3aa55546ade84eb9c76a` fixture remains historical evidence; it is not rewritten or presented as final insertion protection. Accepted0000..0024 and their lock entries remain byte-identical. Further source corrections require their actual new hash and independent review, not an assertion that this document deployed a migration.

## Closed physical-shape support

The current strict physical generator compares exact trigger names and definitions, and currently understands only update/delete mutability. Admit only the optional closed `insertionInvariant: "deletionLifecycleOriginal"` marker in the owned Identity lifecycle table manifest and its resolved physical table. Only the exact Identity-owned `identity_account_deletion` table, canonical `deletion_id` primary key, actual User/state columns and actual active-user unique-index shape may select it. Unknown markers, a foreign owner/table, wrong columns/kinds, wrong primary key/index/state profile or mutable mismatched shape refuse.

The marker generates only the exact fixed trigger above. It permits no arbitrary trigger, table, SQL fragment or cross-owner predicate. Existing normalized tables omit the marker entirely when absent; preserve every old normalized table, baseline SQL, schema/hash formula and existing mutation/clock/scope behavior. Never accept undeclared extra triggers or relax `expectedShape`/`compareShapes`; include the genuine insertion invariant in their strict generated definition instead. Existing physical column maps and enums gain no new kind or wire field.

Only CLOUD.79's write scope expands: the exact `eng/verification/physical-schema.ts` marker resolution/closed validation/fixed trigger generation; its own `identity.json` lifecycle marker; and targeted `d1-physical-schema.test.ts` generator/shape/hostile tests alongside the already owned `deletion-lifecycle.test.ts` migrated SQLite tests. Root CLOUD.83's credential discipline remains separately owned; it does not gain a replacement-protection wildcard or require CLOUD.79 to wait for whole authentication acceptance.

## Required evidence and delivery

Require actual primary-key and active-user replacement refusal with recursive triggers both disabled and enabled, retained terminal-history refusal, unchanged original deadline/policy/revision after rejected inserts, legitimate cancellation and a new request with a genuinely new ID, and preserved foreign keys. The new negative must fail against the old migration and pass against the corrected one. Unknown/foreign/wrong-shape marker negatives and a modified or missing trigger must fail the unchanged strict shape gate. Actual old normalized tables and emitted SQL remain unchanged when the marker is absent.

Require independent exact-head source and immutable r53 admission review, applicable CI and serialized normal publication/deployment after the actually delivered CLOUD.82 predecessor. CLOUD.79 never commits an incomplete deletion family. CLOUD.17's complete security/provider cleanup, real authentication/session activation, deployed D1 contention and whole-series acceptance remain separately required. Local SQLite, a compiler fixture or this planning decision proves neither provider deployment nor OS isolation.
