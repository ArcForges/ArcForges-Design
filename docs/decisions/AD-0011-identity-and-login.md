# AD-0011 — Identity, sign-in, pairing and credentials

- Status: Accepted (2026-10-12; revised after the independent review the same day: honest reuse statement, scoped phone sessions)
- Reuses: the `arcforges.publicapi.v1` IdentityService and DeviceService contracts, the D1 identity and device schema, and the Cloud Identity domain store (main `92ba1dc9`). The endpoints are new work (AF-ID-01, AF-ID-02), because the baseline serves only `HelloService` (10 §2). Also reuses the native authorization tables `identity_native_authorization` and `identity_browser_auth_flow`, and the historical system-browser PKCE design (ArcForges-Design-Parallel `08-security-architecture.md`, main `64173614`).

## Decision

1. **Account authentication** follows the existing identity contracts (implemented by AF-ID-01): passkeys first, email codes as fallback, recovery codes, account deletion. Account sessions are separate from node credentials.
2. **Desktop and CLI sign-in.**
   - **Default: system browser with PKCE (S256) and a loopback redirect** on `127.0.0.1:<ephemeral>` (RFC 8252 pattern). The node opens the browser, receives the one-use authorization code, and exchanges it for a session plus a device enrollment in one call (`NodeEnrollmentService.CompleteNodeSignIn`).
   - **Fallback: the device authorization grant** (RFC 8628 pattern). The node shows a code, a URL (`arcforges.com/activate`) and a QR. The user approves on any signed-in browser or phone, and the node polls with backoff at the advertised interval.
   - Both flows end with the node enrolled as a **device installation with product `arcforges-node`**. Each node, including each WSL guest node, is its own device record. The node receives a refresh-capable device credential (scope `node`) and an initial entitlement token.
3. **Android sign-in.** A Custom Tab with PKCE and a verified app link. Alternatively, **QR from a signed-in desktop node**:
   1. The desktop shows a short-lived (120 s), single-use pairing QR.
   2. The phone scans it and requests sign-in.
   3. The **desktop user confirms** "Allow <device> to sign in as <account>?".
   4. The phone receives its own session with scope **`mobile.limited`**: fleet view, push registration and low-risk commands only.
   5. Anything more needs a step-up **on the phone itself** (passkey through Android Credential Manager, or an e-mail code), which upgrades the session to `account`. This covers medium- and high-risk commands, billing, device management and account settings.

   Approval happens only on the already-authenticated device, never on the requesting one.
   - **Bounding a stolen node credential.** A node credential can confirm a pairing, but a stolen one (for example from the Linux file fallback) yields at most a limited phone session. It never yields account control (T-19).
4. **Credentials at rest.**
   - **Windows:** Windows Credential Manager through DesktopPlatform `ArcForges.Security.Secrets` (reused).
   - **Android:** Keystore-wrapped storage (reused Mobile security module).
   - **Linux:** the Secret Service (libsecret over D-Bus) when available. Otherwise a 0600 file in the node data root, and the node reports the weaker `FILE_PERMISSIONS_ONLY` protection (R-AUTH-003).
5. **Scopes and revocation.**
   - Scopes: `account` (user session, interactive), `mobile.limited` (QR-paired phone before step-up), `node` (node uplink, relay token issuance, entitlement refresh, phone-pairing creation and confirmation), `push` (push registration) and `automation` (personal access tokens for CI, never the normal path).
   - Any device, session or node can be revoked from web, Desktop or Android. Revocation stops token refresh, and relay sockets close within one token lifetime (≤15 min).
6. **OS privilege is separate.** No account action grants OS privileges. The optional privileged features are out of the current scope (AR-16). When built, they install through explicit OS prompts (UAC, sudo), and the UI labels them as OS-level changes (R-AUTH-005).
7. **Abuse resistance.**
   - Sign-in, device-code and QR flows are rate-limited per IP prefix and per account.
   - Device codes are 8 characters from a 20-character alphabet, valid 10 minutes, with 5 attempts per code.
   - QR codes are bound to the issuing node session and expire after 120 s.
