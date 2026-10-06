# Focused security lifecycle and final expiry — 2026-10-06

The actual C75 realm/recovery producer and COM16 family infrastructure are available. Authentication/provider and full session integration remain unfinished, but cannot prevent complete independent StepUp/recovery/deletion core, real persistence and component implementation. Move only CLOUD15/17 implementation starts to those actual producers; retain actual CLOUD13 integration and original CLOUD12 credential source integration through the real CLOUD80 adapter at mandatory completion/activation. No delivered or commercial acceptance status changes.

## Persisted deletion authority and family ownership

Model01 now defines exactly one Identity-owned account_deletion lifecycle row with a captured immutable disclosed deadline/policy/duration/previous state. CLOUD79 owns required lazy policy, forward-only migration, physical manifest and actual Read/Prepare port. C13 integrates this independent producer; whole C17 integrates79 and actual13 sessions before final acceptance. Actual completion edges require upstream COMPLETE, so79 has no12/13edge and cannot create17↔13deadlock. Ordinary independently feasible source remains progressive and never substitutes a successful placeholder.

C13 is the sole family/union writer. Preserve create-user and append its actual native/browser issue/enroll plans, device-revocation, session-lifecycle and push-registration participants. Registered native/browser variants split absolute/access/idle expiry, refresh current/spent proof and installation possession, device-only targets and disjoint actor/target roles. Device revocation includes exact empty/present Notification cleanup and existing real zero/many races. Session writes stay Identity-owned; Device/Workspace authorization is read-only, Platform recovery remains Storage-issued and Notification security intent is a genuine protected durable owner contribution. Credential replacement/removal/recovery consume disjoint actual Session and C16 Token fanout; no fake notice, foreign SQL or extra global/user epoch.

CLOUD16 owns the actual TokenRevocationParticipant and real published PublicOperationCatalog/EventOperationCatalog host projection. Its own token-owner/revoke-user-api-tokens contribution binds actual user revision/recovery to the same issuer/family/plan/scope and revokes zero/many current or stale generation rows atomically. Host pins only actual published CON26 producers/mandatory evaluated closure, no local scope whitelist or hash-only receipt refresh.

## Actual final transaction time

CLOUD78 is the minimum ROOT-owned closed securityExpiry compiler/typed metadata producer, started from actual72/75. Model04 gives the exact integer SQLite UTC ceiling and captured lower-bound contract; existing captured fresh stays byte-identical. Delayed batch/write-lock/expiry boundaries run real generated SQL and migrated SQLite, including full rollback and reconciliation. This source/component evidence is separate from live D1 timing, authentication/provider deployment and whole acceptance. Identity/Pat consume the actual producer; no conservative preflight timestamp is promoted to final proof.

## Sensitive credential integration phasing

The real event graph also detects19→16→15→12→19 and19→17→12→19 if an old12artifact implementation prerequisite is naively promoted to whole12completion. CLOUD80 therefore owns the minimal actual sensitive-credential integration adapter, started only from real12/13source and15typed challenge artifacts. It freshly resolves current actor authority, delegates genuine method verification to the existing C12 owner, verifies exact realm/credential/revision/operation/target/expiry and one-use facts, and uses actual owned proof contributions. C15/17 completion consumes80 and real13; no whole12acceptance gate, empty port, caller-success proof or global tool weakening. C12 preserves full19account/browser acceptance and method ownership.


## Exact current owner family variant/role freeze

### CLOUD13 exact closed family variant and role handoff

Planning freeze for the current production implementation, not delivery evidence. Names below are exact server-selected plan IDs; callers cannot select a family, guard role, SQL predicate or time source. Native/browser actor variants keep separate exact expiry columns; no nullable/freshIfPresent weakening.

### Registrations

Preserve existing families.account-enrollment.create-user SQL/participants/default ordering exactly. Append the existing account-enrollment family's task-owned issue-native-session / issue-browser-session / enroll-native-session / enroll-browser-session plans. They require Identity+Workspace and real Device+Notification completion contributions; configured grants use the later explicitly admitted Entitlement variant, never a second commit.

Register device-revocation: Identity +Device +Notification write participants, Platform privileged recovery authorization; current Workspace may authorize read-only. Exact variants:

- families.device-revocation.revoke-device-{empty|present}-{native|browser}
- families.device-revocation.sign-out-device-{empty|present}-{native|browser}
- families.device-revocation.revoke-installation-{empty|present}-{native|browser}
- families.device-revocation.rotate-installation-key-{empty|present}-{native|browser}

Register session-lifecycle: Identity writes, Device and Workspace read-only current authorization contributions, privileged Platform recovery. Exact variants:

- families.session-lifecycle.refresh-native
- families.session-lifecycle.refresh-reuse-native
- families.session-lifecycle.browser-activity
- families.session-lifecycle.revoke-session-{native|browser}
- families.session-lifecycle.logout-current-{native|browser}
- families.session-lifecycle.logout-others-{native|browser}
- families.session-lifecycle.revoke-all-{native|browser}

Register push-registration: Notification writes; Identity +Device +Workspace current authorization only; privileged Platform recovery. Exact variants:

- families.push-registration.create-{native|browser}
- families.push-registration.replace-{native|browser}
- families.push-registration.remove-empty-{native|browser}
- families.push-registration.remove-present-{native|browser}

Device rename/trust/remoteEnabled/remotePolicy changes use exact device-lifecycle variants with Device write+Identity actor/proof guards, current Workspace read-only and75 privileged recovery. If the architecture registry treats these as device-revocation variants, use those registered names consistently; no free-form sixth family. Exact names proposed: families.device-revocation.{rename-device|set-trust|set-remote-enabled|set-remote-policy}-{native|browser}, Notification conditional only when actual push cleanup is performed. Sign-out retains Device identity/registration/trust/local data while its bound sessions are revoked; revoke and key rotation cannot leave old-key sessions valid.

### Fixed role names and arrays

Platform authorization/recovery-current is the delivered75 sealed issuer: [realm, generation, state4, recoveryRevision] (command ID added only by executor).

Identity current actor guard key actor-current: [sessionId,userId,deviceId,installationId,productId,purpose,credentialKind,authEpoch,recoveryGeneration,sessionRevision,capturedServerMicros]. Native variants require actual transaction expiry on expires_at+access_expires_at; browser variants expires_at+idle_expires_at. Refresh-native/reuse use key refresh-current and absolute family expires_at only, with actual current/spent refresh proof plus owned installation possession; expired access never becomes a fake refresh authority.

Identity user authorization key actor-user: [realm,userId,currentState,userRevision]. The coordinator must enforce allowed operation/account state, and purpose5 only get/cancel/logout. Identity proof key action-proof binds actual persisted proved challenge actor/session/operation/target/epochs/revision/expiry and is consumed atomically in its record role; no legacy elevation flags.

Device current actor roles: actor-device-owner [deviceId,userId], actor-installation-binding [installationId,deviceId,productId,keyVersion], actor-device-revision [deviceId,rev], actor-installation-revision [installationId,rev]. Exact target roles retain frozen DeviceFamilyRoles: device-owner [targetDevice,userId], installation-binding [targetInstallation,targetDevice,productId,keyVersion], device-revision [targetDevice,rev], installation-revision [targetInstallation,rev]. Expected0 is only verified absence for a new insert, never a valid persisted current revision.

For issuance, target-only Device roles suffice; for a lifecycle target differing from the actor, both disjoint actor and target roles are required. Device-only rename/revoke/signout/trust/policy targets must not require an invented installation: owner participant supports device-only target result and omits installation roles on exactly those registered variants.

Device record arrays: device [deviceId,userId,name,platform,firstSeen,lastSeen] for new insert (untrusted/defaultremoteoff/rev1); installation [installationId,deviceId,productId,appVersion,contractSetVersion,installedAt,lastActiveAt,platformText,canonicalPublicKey,keyVersion] for new insert/rev1. Mutations use exact own current revision and explicit SQL SET fields; no dynamic supplied SQL/column names. Key validation is actual admitted P256 canonical DER-SPKI, not possession; rotation requires current operation proof plus same-family session fanout.

Workspace authorization workspace-current [workspaceId,realmId,ownerUserId,stateActive,currentRevision], owner scope equals actual personal workspace. No Identity foreign Workspace SQL/exception expansion.

Notification empty registration guard registration-empty: exact owned by device_id or device_id,installation_id and closed absence=not-exists, no match/fresh. Present guard registration-current binds bounded real first registration_id/device_id/installation_id/registration_revision/recovery_generation, then actual cleanup deletes ALL exact target rows including old generation rows. Registration itself uses current actor/Device/Installation/recovery plus actual configured token protector, never a fabricated absence or success writer.

Identity record sessions-revoke fanout arrays omit command ID: [serverSampledRevokedAtMicros,userId] plus exactly one predicate identifier (session/device/installation/family), or exceptSessionId for logout-others. AllSessions [now,user]; CurrentSession [now,user,session]; OtherSessions [now,user,exceptSession]; Device [now,user,device]; Installation [now,user,installation]; RefreshFamily [now,user,family]. UPDATE only currently unrevoked rows, rev=rev+1 atomically. Predicate field set is closed per variant; no caller flags/count/success assertion. Existing session lifetime and refresh family IDs remain unchanged. Credential replace/remove/recovery use the actual account-security family and combine this own Session fanout with the disjoint C16 Identity token-revocation participant; no global realm epoch bump or extra user epoch.

Platform commit tail stays last, release remains last, guard and lock order remain unchanged. Closed per-plan record-only mutationRoleOrder enables User/Credential ->Workspace ->Device ->Installation ->Session ->Notification delivery ->attempt only where immediate FK requires it. Existing absent override remains byte-identical. FamilyBinding/ModuleFamilyPort.cs must deep-freeze/copy new metadata; its exact admission is necessary.
## Verified operation identifier refinement
Actual merged public metadata uses notification.registerPush/notification.unregisterPush and identity.revokeSession/identity.cancelAccountDeletion. Installation-specific internal revoke shares the registered device.revoke proof operation class with its exact installation-bearing target hash, rather than inventing a public device.revokeInstallation RPC. identity.logout and identity.browserActivity are owned native/browser exception lifecycle transport keys only, never advertised as new public operation registry entries or accepted C15 proof classes.

## Exact Devices mutation contribution arrays (frozen)

All record roles omit executor command ID; all current revisions are owner-reread and guards capture them. Target.AtMicros is ignored for authority/stamps. The owner uses its own server TimeProvider sample, and the shared final action-proof/expiry guard must still pass. Own contribution does not claim possession or perform a write.

- rename-device: record device = [name,deviceId,currentDeviceRevision]; SET display_name, rev=rev+1. Authored alias max256 Unicode scalars.
- sign-out-device: record device = [deviceId,currentDeviceRevision]; SET rev=rev+1 only. Stable registration/trust/data remain; this fence also invalidates pending old Device-bound completion proofs. Same-family Identity sessions-revoke [sampled,user,device] plus Notification cleanup required.
- revoke-device: record device = [sampledRevokedAtMicros,deviceId,currentDeviceRevision]; SET revoked_at, remote_enabled=0, rev=rev+1. No delete. Same-family session and push cleanup.
- revoke-installation: record installation = [sampledRevokedAtMicros,installationId,currentInstallationRevision]; SET revoked_at, rev=rev+1. Same-family exact installation session/push cleanup.
- set-trust: record device = [trustEnum,proofStampedAtOrMinusOne,trustEnum,deviceId,currentDeviceRevision]. SET trust_level from first arg; trust_raised_at NULLIF(second,-1); remote_enabled remains only when thirdarg=2, otherwise0; rev=rev+1. Raising trust requires real current action-proof in full family; owner stamp samples now. Lowering trust stamps NULL and disables remote. No legacy read requires a nonnull trust stamp.
- set-remote-enabled: record device = [enabledBool,deviceId,currentDeviceRevision]; SET remote_enabled, rev=rev+1. Enabling additionally requires current owned trust2 and real action proof; mere session possession never grants remote access.
- set-remote-policy: guard revision/remote-policy-revision [deviceId,currentPolicyRevisionOrVerifiedAbsent0]; record remote-policy = [deviceId,canonicalAllowedKeysJson,canonicalConfirmationKeysJson]. INSERT rev1 or ON CONFLICT update arrays+rev=rev+1. Key collections are defensively captured before await, valid canonical Key arrays; effective operation gating remains the actual registered capability/remote-policy producer, no new invented capabilities.
- rotate-installation-key: record installation = [canonicalBase64DerSpki,newKeyVersion,installationId,currentInstallationRevision]; SET public_key,key_version,rev=rev+1. newVersion checked currentVersion+1 (binding unbound0 produces1), no change of Device/Installation IDs or activity timestamps. Real current device.register conditional action proof and same-family session fanout required; parsing the supplied canonical P256 key never implies possession. Already revoked installation is refused.

PrepareCurrent allowed family mapping: account-enrollment exact four issue/enroll native/browser variants use TargetCurrent role set; session-lifecycle exact listed actor variants, push-registration exact listed variants and device-revocation exact listed lifecycle variants use ActorCurrent role set. device-revocation TargetCurrent is reserved for real target own-state guards distinct from actor keys. Unknown family/plan/purpose combinations fail closed before sealing. Device-only lifecycle targets use only device owner/revision and record roles; do not invent an installation for Device rename/signout/revoke/trust/policy. Issuance new/existing row modes are determined by actual own reads and exact registered variant, never caller assertions of newness.
## Issuance mode refinement (exact, no silent UPSERT key changes)

issue-native-session/issue-browser-session require existing live Device+Installation, Device current guards only; no key or metadata overwrite. enroll-native-session/enroll-browser-session is new User plus verified-absent Device+Installation.

Append four exact account-enrollment variants: register-native-session/register-browser-session for an existing user plus verified-absent Device+Installation; add-installation-native-session/add-installation-browser-session for existing live Device plus verified-absent Installation (also exact device/product uniqueness read). Mixed existing installation/new Device refuses. An existing bound key never changes through issuance; only explicit rotation+real proof+atomic session fanout can change it. Mode derives from actual owner reads and exact registered plan, never a caller boolean. Device records exist only on new Device variants; Installation records only on new Installation variants. All variants keep existing account-enrollment defaults and required Workspace ownership authorization.

C16 TokenRevocationTarget follows the actual SessionRevocationPort shape: exact family/plan/ownerScope plus RealmId/UserId; the owner samples time and re-reads UserRevision. Result returns the actual captured UserRevision and its opaque contribution, and the coordinator compares the real actor/proof capture. No callerAt/authentication flag or token-id list. DeletionLifecyclePort uses the common ArcForges.Cloud.Modules namespace and exact named path, retaining immutable source facts and owner-only contribution semantics.


The actual common contribution API also supplies a closed ModuleFamilyContributionException with only Rejected/Unavailable and no plan/SQL/subject/secret details. Identity owns this primitive seam, Storage maps only exact known private validation failures toRejected, and C21 maps unavailable configuration toUnavailable after actual shared producer publication. Unexpected implementation failures are not swallowed; opaque authority, interface/signatures and all issuer/family/scope checks remain unchanged.
