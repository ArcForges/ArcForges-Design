# 08 — Security and trust boundaries

## Principals and trust

Local actions require authenticated OS owner identity over the existing protected LocalRpc transport (Windows pipe ACL and verified token; Linux Unix socket ownership/mode and peer credentials). Node is per-user by default; elevation belongs only to a narrow separately reviewed installation/prerequisite operation. No internet listener is enabled for Node management. Loopback and possession of a SandboxId are not authorization.

A sandbox payload is untrusted relative to host files, Node metadata, IPC endpoints, secrets and other sandbox roots. Grant only explicitly requested paths and the minimal system/runtime read set proven by the backend profile. Reject unapproved writes, host IPC and forbidden network paths according to actual backend capability. A generic CLI that needs more rights receives a specific error and an inspectable grant request; no silent host fallback or learning-mode grant escalation.

The Center is a remote management principal, never an ambient host administrator. Enrollment binds a node instance and local owner to one configured Center origin and issuer. TLS plus short-lived node channel credentials, key rotation, session epoch and revocation prevent replay of old enrollment. A server message must match the active enrollment, command freshness, grant version, declared method and bounded body. Host-level path grants and privileged capabilities cannot be broadened remotely. New remote access grants are created locally and default off.

## Permissions

| Action | Local requirement | Remote requirement |
|---|---|---|
| Read Sandbox/Run/resource status | Owner principal | Device association plus scoped read grant |
| Start/stop run | Owner plus valid Sandbox policy | Explicit run-control grant; same Core admission; no host launch |
| Configure Sandbox | Owner; revision check; stopped runs for access changes | Only locally permitted narrowing/policy fields; no host-path/network expansion |
| Read output/export | Owner plus data scope | Explicit output/data grant; bounded proxy, no arbitrary host path |
| Import a regular file | Owner and owned-path and managed-use checks | Scoped data-write grant through the admitted regular-file transfer routes |
| Preview, execute or resume Sandbox deletion | Owner-local plan or original journal with revision, identity and managed-use checks | Owner-local on the shipped cohort |
| Create/expand remote grant | Local owner only | Forbidden |
| Revoke own remote access | Local owner | Revoke only; grant edits use local SetRemoteGrant; invalidate future commands |
| Resource policy | Local owner within node safety envelope | Within preauthorized bounds; cannot remove host reserve or raise local ceilings |
| Terminal input/resize | Local owner and exclusive terminal lease | Not exposed in the V2 remote surface |

## Files and secrets

All Node metadata, manifests and supervisor endpoints are outside payload-writable areas. Private roots use restrictive permissions and stable directory identities. Resolve file operations relative to an opened owned root, reject absolute/drive/UNC/device/alternate-stream paths, `..`, unsafe symlinks/reparse points, mount crossings and collisions under native case rules. Check identity at the moment of mutation, not just when making a UI preview. Never follow links when recursively enumerating/deleting owned data.

Do not inherit the host's full environment, SSH agents, credential sockets, cloud keys or Node signing material. A sandbox user's intentionally provided application credentials may persist inside that sandbox and are within its data/export scope; warn in the export preview and never silently upload them. Raw terminal output is treated as untrusted bytes. CLI handles terminal escape behavior without creating host-side command actions; Web renders escaped text, never HTML. Output may contain secrets, so retention and remote output grants are explicit.

### Trusted local process inspection

Under the [2026-11-17 owner decision](../decisions/AD-0022-cli-sandbox-platform-pivot.md#local-process-visibility--2026-11-17-amendment), the owning host user, local administrators and their trusted host inspection tools may observe explicitly supplied Run inputs in official MXC/helper process arguments. That observation alone is not an admission failure. This does not authorize an untrusted payload, a neighboring Sandbox or another unauthorized principal to inspect host/control data; sharing an OS UID does not grant a payload those rights. Host credential inheritance remains prohibited unless a credential is an explicitly authorized input. Record synthetic visibility observations truthfully, with observer authority, without exporting raw secrets, argv or environment values to ordinary logs, public Plan/GitHub records or evidence bundles.

## Failure and audit

Authenticate and authorize before existence-sensitive reads. The same operation ID/payload hash and actor chain persist across Center and Node; audit state changes, denials, grant changes, policy application/readback, deletes and migrations. Redact secrets and avoid recording command environments. Audits include a correlation ID, timestamp, local/remote origin, resource revision and effect certainty. `UNKNOWN` never has a blind retry recommendation.

The Dashboard displays security facts available to the current account, such as session and device status and the selected Node grant. Server audit storage and account-export data do not create a general security activity feed in the browser. Account and subscription ceremonies use the Center's exact operation class, target and single-use proof when required. [Center account scope](https://github.com/ArcForges/Cloud/blob/9b8796eac760982d9814f371b820b736ddd945c4/docs/center-identity.md), [Center operation policy](https://github.com/ArcForges/Cloud/blob/9b8796eac760982d9814f371b820b736ddd945c4/center/internal/access/access.go)

Revocation prevents further remote commands immediately when locally observed; the Node rejects stale epochs/grants on reconnect. A command already accepted by Core may finish and is reconciled; revocation does not erase effects or masquerade as rollback. Server outage, subscription expiry, account deletion or remote device revocation do not delete local sandbox data or stop local runs.

No isolation claim covers kernel exploits or an administrator deliberately changing host security. Native negative tests nevertheless cover the promised host/path/network/descendant boundaries. A detected boundary failure disables that backend profile and blocks release until repaired or supported by a newly admitted official version. See [acceptance](../verification/acceptance.md).
