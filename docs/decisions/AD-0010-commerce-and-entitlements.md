# AD-0010 — Commerce and entitlements: Paddle on the web, Google Play on Android

- Status: Accepted (2026-10-12; revised 2026-10-13 after the findings review: LAN gating stated as a launch decision; revised 2026-10-13 by the product owner's decisions (AD-0015): local and LAN free; entitlement tokens describe cloud features only)
- Reuses: ArcForges-Design-Parallel BC-01 (Paddle as sole Merchant of Record, main `64173614`); the existing Cloud Entitlement module (2,439 lines at main `92ba1dc9`) and the commerce/entitlement D1 tables.
- Supersedes for the active product: the historical Mobile position that "the Play channel is out of scope" (Mobile README, main `6702e281`). Android distribution and in-app subscription now use Google Play, as the product owner requires; direct APK prereleases remain a development channel.

## Decision

1. **Plan catalogue as data.** It lives in the Entitlement module's configuration revision. Launch plans:
   - `free` (no charge);
   - `pro_monthly` and `pro_annual`, each with web (Paddle) and Play (`arcforges.pro`, with base plans `monthly` and `annual`) offers.

   **Feature gating** ([AD-0015](AD-0015-direction-editions-roadmap.md) §2). Only cloud-backed features are gated: remote status and control through the relay (`remote.view`, `remote.control`) and push (`push`). Local and LAN functionality is free, including future local and LAN capabilities, and is never a plan feature. The gating is catalogue data, so changing it needs no code change ([product definition](../product/product-definition.md) §5).

   A feature flag set per plan drives gating (product definition §5).
2. **Web purchases** use Paddle hosted checkout as Merchant of Record. Verified webhooks (raw-body HMAC, per the historical adapter design) drive subscription state through the existing commerce tables.
3. **Android purchases** use Google Play Billing. The app launches the purchase with `obfuscatedAccountId` set to an opaque, server-issued account reference. Then:
   1. The app sends the purchase token to `StoreBillingService.SubmitPlayPurchase` (`arcforges.fleet.v1`).
   2. C# verifies it with `purchases.subscriptionsv2.get` and links it to the account. The link is refused if `obfuscatedAccountId` mismatches, or if the token is already linked elsewhere.
   3. C# grants the entitlement and acknowledges server-side with `purchases.subscriptions.acknowledge`, well within the 3-day window (V-C05). A retry job (platform job lease) guarantees acknowledgement within 24 h or raises an operator alert.
   4. RTDN (Cloud Pub/Sub push to a Worker route, verified as an authenticated push to C#) drives all later state changes. On each notification C# re-reads `subscriptionsv2`. States handled: active, grace period, account hold, paused, canceled (until expiry), expired, revoked and refunded.
   5. **Restore:** the app queries existing purchases and resubmits their tokens. Purchases made outside the app (no account identifier) are linked to the signed-in account only after explicit confirmation.
4. **One entitlement snapshot per account** combines all sources with source precedence. A user holding both web and Play subscriptions is warned about the duplicate. Entitlement is the union, with no double grant of quantity-based features.
5. **Offline enforcement on nodes.**
   - The cloud issues a signed **entitlement token** to each enrolled node: ES256 (ECDSA P-256; .NET has no built-in Ed25519, V-N05), the account's plan features, `not_after` = now + 14 days, and refresh at least every 24 h while online.
   - Nodes verify it with the embedded public key set, which is rotated through releases and the relay.
   - The token describes cloud features only. On expiry, only cloud features stop: the node stops opening relay connections and shows remote access as unavailable. Local and LAN features never check it, and running tasks are never interrupted (R-COM-004).
6. **Failure states shown to users:** payment failed (dunning), on hold, grace period, pending (Play `PENDING` purchases are not granted), refunded (revoked immediately) and region-restricted.
