# AD-0011 — Identity, sign-in, pairing and credentials

- Status: Accepted (2026-10-12; revised after the independent review the same day: honest reuse statement, scoped phone sessions; amended 2026-10-19 by the current-design corrections: the same-user qualifier for credentials at rest, §4; amended 2026-10-21 by AD-0018: no WSL guest nodes; amended 2026-10-28 by [AD-0021](AD-0021-central-access-go-center.md): endpoints implemented in the Go center; a third credential kind, the agent grant (AD-0021 §7); amended 2026-11-05 by the AF-CTR-04 Plan decisions Q19 (no terminal QR, §2) and Q8 (lookups and budgets instead of attempts per code, §7), as the merged code implements them)
- Reuses: the `arcforges.publicapi.v1` IdentityService and DeviceService contracts, the D1 identity and device schema, and the Cloud Identity domain store (main `92ba1dc9`). The endpoints are new work (AF-ID-01, AF-ID-02), because the baseline serves only `HelloService` (10 §2). Also reuses the native authorization tables `identity_native_authorization` and `identity_browser_auth_flow`, and the historical system-browser PKCE design (ArcForges-Design-Parallel `08-security-architecture.md`, main `64173614`).

## Decision

1. **Account authentication** follows the existing identity contracts (implemented by AF-ID-01): passkeys first, email codes as fallback, recovery codes, account deletion. Account sessions are separate from node credentials.
2. **Desktop and CLI sign-in.**
   - **Default: system browser with PKCE (S256) and a loopback redirect** on `127.0.0.1:<ephemeral>` (RFC 8252 pattern). The node opens the browser, receives the one-use authorization code, and exchanges it for a session plus a device enrollment in one call (`NodeEnrollmentService.CompleteNodeSignIn`).
   - **Fallback: the device authorization grant** (RFC 8628 pattern). The node shows a code, a URL (`arcforges.com/activate`) and a QR. The user approves on any signed-in browser or phone, and the node polls with backoff at the advertised interval.
     *Amended 2026-11-05 (AF-CTR-04 Plan decision Q19; ArcForges #63 and #69):* the CLI shows no terminal QR and takes no QR dependency. It prints the code, the URL `<center>/activate` and the complete URL `<center>/activate#code=XXXX-XXXX`, and the node's `SignInFlow.qr_payload` carries that derived complete URL ([cli](../experience/cli.md) C-09, [10](../architecture/10-cloud.md) §3.2). The sentence above ("and a QR") stays as history.
   - Both flows end with the node enrolled as a **device installation with product `arcforges-node`**. Each node is its own device record (a Linux node a user runs in WSL2 is an ordinary node; *superseded 2026-10-21 by [AD-0018](AD-0018-native-platforms-without-wsl-integration.md):* "including each WSL guest node"). The node receives a refresh-capable device credential (scope `node`) and an initial entitlement token.
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
   - **Same-user qualifier** (amended 2026-10-19). The Windows and Linux stores protect the node's credentials and data key from other users, not from processes of the signed-in user. Unsandboxed managed processes can read every credential the signed-in user can read, the node's own included; the 0600 file is no exception ([11](../architecture/11-security-privacy.md) §3, T-25). The decision is unchanged; only the protection it claims is stated exactly.
5. **Scopes and revocation.**
   - Scopes: `account` (user session, interactive), `mobile.limited` (QR-paired phone before step-up), `node` (node uplink, relay token issuance, entitlement refresh, phone-pairing creation and confirmation), `push` (push registration) and `automation` (personal access tokens for CI, never the normal path).
   - Any device, session or node can be revoked from web, Desktop or Android. Revocation stops token refresh, and relay sockets close within one token lifetime (≤15 min).
6. **OS privilege is separate.** No account action grants OS privileges. The optional privileged features are out of the current scope (AR-16). When built, they install through explicit OS prompts (UAC, sudo), and the UI labels them as OS-level changes (R-AUTH-005).
7. **Abuse resistance.**
   - Sign-in, device-code and QR flows are rate-limited per IP prefix and per account.
   - Device codes are 8 characters from a 20-character alphabet, valid 10 minutes, with 5 attempts per code.
     *Amended 2026-11-05 (AF-CTR-04 Plan decision Q8; Cloud #134):* there is no attempt counter per code. A live code admits 5 lookups, and the sixth and later are refused `VALIDATION/code_invalid` while the authorization stays pending. Besides, each entry that does not name a live code the account may act on spends one unit of the account's budget (5 per 15 minutes) and of the network's (20 per 15 minutes), and once either budget is spent every entry, a right one too, is refused `RESOURCE/rate_limited` until its window ends ([10](../architecture/10-cloud.md) §3.2). "5 attempts per code" above stays as history.
   - QR codes are bound to the issuing node session and expire after 120 s.
