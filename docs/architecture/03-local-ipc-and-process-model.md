# Application Process and Private Helper IPC

Authority: [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012). Professional applications host their own UI, domain, assistant service/store and Cloud client. There is no shared Hub, shared coordinator, product discovery, cross-product local listener or peer data relay. [Architecture 27](27-platform-projects-and-application-assistants.md) fixes process/project ownership; [annex 10](contracts/10-application-scope-and-streams.md) fixes Cloud targeting and public gRPC-Web.

## Current process topology

Product UI/assistant → typed in-process Application handlers → owned domain/store/native wrappers. Each app → Worker ingress → C# Container over gRPC-Web. A Cloud tool request targets exactly one application installation and is reauthorized in that application's process. Android/Web never connect to a desktop local endpoint.

Only parent-owned ContentSandbox and admitted extension/connector children use local RPC. Use authored proto/generated native gRPC, Kestrel HTTP/2 over owner-only Windows Named Pipe or Unix domain socket, and ConnectCallback clients. No TCP port is opened for this local boundary. The parent supplies a private endpoint/launch identity; no directory/LAN/global registry scan occurs. Child crash/parent exit revokes the launch grants and removes the endpoint.

Platform packages, managed services, SQLite repositories, assistant windows and ordinary P/Invoke wrappers run inside the host application. They must not create a service process or local RPC listener merely because they are separately packaged. The isolated parser/extension exceptions below are security boundaries, not application-to-application communication. No generic background local service is part of the product.

## Private boundary rules

OS identity/ACL and authenticated LocalBootstrap bind parent/child, build/protocol and fresh nonce/epoch. Names are not authentication. Helpers use restricted OS tokens/profiles and only brokered resource/buffer grants; unrestricted same-user children do not satisfy containment. Opposite-direction callbacks use explicitly parent-created bounded channels, never a peer application registry. Keep the 30s lease/10s renewal and 16 active/64 queued bounds for admitted helper connections, with deadlines and typed overload/cancel/effect results.

Large parser input/output uses bounded broker resource grants and verified transfer/buffer mechanisms in [annex 09](contracts/09-local-grpc-and-sandbox.md), not arbitrary filesystem paths or cross-product transfer tickets. Signed parser/helper runtime and native libraries come from tested Platform packages. Product UI remains responsive and canonical data remains recoverable if a helper fails. Ordinary in-process app handlers need no RPC bootstrap, heartbeat or network serialization.

## Required verification

WP06 proves two real AOT helper-probe processes over each exact OS transport; WP08 implements the parent-bound mechanics; WP11 proves hostile-child containment; WP13 composes actual parser libraries. Tests cover wrong OS user/nonce/build, stale epoch, malformed/truncated protobuf, queue saturation, cancellation, lost acknowledgement, parent death, orphan cleanup and repeated restricted relaunch. No first-party product-to-product fixture is a current requirement. WP26/52 separately prove Cloud-targeted same-app tools, and professional products remain locally usable when Cloud is unavailable.

## Stable rule and section references

The following legacy anchors are retained for existing links. Their current normative meaning is the helper-only topology, authentication, bounds, lifetime and verification above; none retains the retired application runtime/discovery behavior. Cross-product examples are [future only](../future/cross-product-collaboration/README.md).

<a id="1-generated-service-shape"></a>
<a id="10-bidirectional-communication"></a>
<a id="11-aot-checklist"></a>
<a id="12-fault-injection"></a>
<a id="13-the-remote-bridge"></a>
<a id="14-traceability"></a>
<a id="2-authenticated-local-transport"></a>
<a id="3-wire-and-flow-control-profile"></a>
<a id="4-hub-and-registration"></a>
<a id="41-endpoint-manifest"></a>
<a id="42-registration-lifecycle"></a>
<a id="43-health-and-backpressure"></a>
<a id="44-routing"></a>
<a id="5-connection-management"></a>
<a id="6-concurrency-and-ordering"></a>
<a id="7-disconnection-cancellation-and-retry"></a>
<a id="8-security-of-the-local-boundary"></a>
<a id="9-large-data-across-the-local-boundary"></a>
<a id="rule-cc-01"></a>
<a id="rule-cc-06"></a>
<a id="rule-em-01"></a>
<a id="rule-sc-07"></a>
