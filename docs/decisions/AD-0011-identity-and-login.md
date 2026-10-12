# AD-0011 — Identity, sign-in, pairing and credentials

- Status: Accepted (2026-10-12)
- Reuses: the Cloud Identity module (main `92ba1dc9`) and `arcforges.publicapi.v1` IdentityService/DeviceService/WorkspaceService (passkeys, email codes, sessions, step-up, recovery, deletion, devices). Also the native authorization tables `identity_native_authorization` and `identity_browser_auth_flow`, and the historical system-browser PKCE design (ArcForges-Design-Parallel `08-security-architecture.md`, main `64173614`).

## Decision

1. **Account authentication** is the existing identity service: passkeys first, email codes as fallback, recovery codes, account deletion. Account sessions are separate from node credentials.
2. **Desktop and CLI sign-in.**
   - **Default: system browser with PKCE (S256) and a loopback redirect** on `127.0.0.1:<ephemeral>` (RFC 8252 pattern). The node opens the browser, receives the one-use authorization code, and exchanges it for a session plus a device enrollment in one call (`NodeEnrollmentService.CompleteNodeSignIn`).
   - **Fallback: the device authorization grant** (RFC 8628 pattern). The node shows a code, a URL (`arcforges.com/activate`) and a QR. The user approves on any signed-in browser or phone, and the node polls with backoff at the advertised interval.
   - Both flows end with the node enrolled as a **device installation of kind `NODE`**. It receives a refresh-capable device credential (scope `node`) and an initial entitlement token.
3. **Android sign-in.** A Custom Tab with PKCE and a verified app link. Alternatively, **QR from a signed-in desktop node**:
   1. The desktop shows a short-lived (120 s), single-use pairing QR.
   2. The phone scans it and requests sign-in.
   3. The **desktop user confirms** "Allow <device> to sign in as <account>?".
   4. The phone receives its own session.

   Approval happens only on the already-authenticated device, never on the requesting one.
4. **Credentials at rest.**
   - **Windows:** Windows Credential Manager through DesktopPlatform `ArcForges.Security.Secrets` (reused).
   - **Android:** Keystore-wrapped storage (reused Mobile security module).
   - **Linux:** the Secret Service (libsecret over D-Bus) when available. Otherwise a 0600 file in the node data root, and the node reports the weaker `FILE_PERMISSIONS_ONLY` protection (R-AUTH-003).
5. **Scopes and revocation.**
   - Scopes: `account` (user session, interactive), `node` (node uplink, relay token issuance, entitlement refresh), `push` (push registration) and `automation` (personal access tokens for CI, never the normal path).
   - Any device, session or node can be revoked from web, Desktop or Android. Revocation stops token refresh, and relay sockets close within one token lifetime (≤15 min).
6. **OS privilege is separate.** No account action grants OS privileges. The optional privileged features (Windows service mode, Linux I/O control) are installed through explicit OS prompts (UAC, sudo), and the UI labels them as OS-level changes (R-AUTH-005).
7. **Abuse resistance.**
   - Sign-in, device-code and QR flows are rate-limited per IP prefix and per account.
   - Device codes are 8 characters from a 20-character alphabet, valid 10 minutes, with 5 attempts per code.
   - QR codes are bound to the issuing node session and expire after 120 s.
