# Original browser logout command producer

Supporting amendment to P2-018, coordination reference 059.

## 1. Actual missing input

The current authored browser exception schema declares `browser.logout` as POST `/session/v1/logout`, with session-cookie credential, exact configured Origin, required CSRF, cookie clearing and no-store. Its request root list is empty. Its actual `BrowserReceipt` requires a nonzero UUID commandId. No original command header is defined. Identity's actual `IIdentitySessionLogoutPort.LogoutAsync(SessionCredentialReference credential, Guid commandId, CancellationToken)` already accepts the original command; another public RPC or facade signature is unnecessary. A random server UUID cannot reconcile the client's indeterminate original command.

## 2. One strict request and unchanged route

Add only `BrowserLogoutRequest` with one required commandId string: exactly 36 characters, lowercase canonical nonzero UUID-D. The closed JSON object rejects extra, missing, duplicate, differently cased or malformed properties and has maximum UTF8 body size 4096. The existing logout route acquires exactly this JSON request root. Its path/method/credential/Origin/CSRF/setCookie/cache/response fields stay unchanged, and every other browser/native operation and the complete 49 Identity operation inventory stay unchanged. Do not infer command identity from trace IDs, a cookie, receipt identity, a newly allocated UUID or a token-only RevokeSession call.

## 3. Genuine SDK implementation and original intent

Use the existing authored JSON schema compiler for real C# DTO/strict AOT-safe reader and TS model/strict reader, and the actual BrowserSessionRoutes catalogs. The existing Kotlin code generator emits protobuf/Connect and has no general browser JSON emitter. Publish a new explicitly closed Kotlin browser logout wire/helper via its real generated staging hook, with the same bounded request and canonical compact JSON bytes; do not claim a nonexistent general Kotlin HTTP adapter or add a JSON library dependency.

Each SDK's closed original-intent helper captures the validated command once, owns its canonical UTF8 body, exposes the fixed existing method/path, and compares any parsed receipt command to that exact original command. Mutable caller bytes cannot alter its retained intent. An indeterminate retry uses the same captured command and byte body; no helper allocates a replacement command, reruns randomness or performs a hidden automatic request. Caller authentication/cookie/CSRF secrets never enter the body/helper/fixture/diagnostics. Existing real transport owners send this request through their ordinary HTTP adapters and current cookie/Origin/CSRF protocol.

## 4. Current authority and host integration

CLOUD.13 consumes the normally published producer as a completion artifact, keeping all current ordinary source starts and existing completion requirements. The genuine public host maps the validated original body command directly to existing LogoutAsync after current cookie/Origin/CSRF authentication and owner checks. Existing internal original-intent fingerprint remains bound to resolved realm/User/Workspace/Session and purpose domain. The body does not grant session authority. Invalid or absent input refuses before effects; exact AlreadyEnded clears a cookie only after the existing ended credential, Origin and CSRF verification, and does not fabricate a receipt. Lost response/replay continues using the durable original command and actual receipt owner semantics. P54's existing RPC host progress remains independent; browser logout full composition requires this real producer.

## 5. Production validation

Independently authored C#/TS/Kotlin vectors cover canonical command/body bytes, genuine encode/read/replay, mutation of borrowed buffers, original-command preservation through repeated and indeterminate intent use, and mismatched receipt refusal. Reject zero/uppercase/truncated/noncanonical UUID, missing/duplicate/unknown/case fields, invalid UTF8/control data and oversized bodies. Keep exact route security assertions and all 49 Identity operation identities; only the actual logout request-root fixture changes. All other existing CON.07 vectors remain intact. No interface-only implementation, parser success stub, synthetic authentication grant, route count waiver or unrelated dependency upgrade is admitted.

## 6. Ownership and delivery

Governance owns CON.39. All admitted write entries use complete repository-qualified physical paths. The existing RES-contracts-generated-baseline regenerate protocol applies: regenerate actual schema/descriptor/SDK outputs with pinned generators after rebase, never hand-edit or hand-merge their source. Contracts integration serializes shared generation, access/source inventory and immutable receipt/NOTICE/package successors from the actual accepted prefix. Preserve every completed producer and accepted history; source-only reviews do not replace final independent exact-head review, applicable current CI and normal immutable publication. Existing package identities are retained. Actual production host authentication, atomic revoke/receipt, receipt retrieval and cookie transport remain separate owner implementation and acceptance; SDK vectors do not prove deployed logout or session revocation.
