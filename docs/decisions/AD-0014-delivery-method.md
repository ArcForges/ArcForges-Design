# AD-0014 — Delivery method: serial development, distinct evidence, honest acceptance

- Status: Accepted (2026-10-12; revised the same day after the independent review: `blocked` state and real dependencies, so one blocked task cannot stall the plan; revised 2026-10-13 after the findings review: production activation separate from delivery; continuous serial execution once authorized; amended 2026-10-16 by [AD-0016](AD-0016-local-first-verification.md): the hosted-CI merge gate applies to external PRs; amended 2026-10-17 by AD-0016: the isolated secret-store backend in §6; amended 2026-10-21 by AD-0018: real Linux tests run on a native Linux host, not WSL2; amended 2026-10-22 by [AD-0020](AD-0020-post-push-verification-and-required-checks.md): the owner's verification runs after the push and the required host statuses gate the merge; amended 2026-10-27 by the user: provider-neutral delegation and accurate attribution)
- Supersedes for active development:
  - the parallel delivery model of ArcForges-Design-Parallel (P2-018, DLV-25, DLV-31 build slot, DLV-42 coordinator capacity) and of Plan-Parallel `execution-policy.md`, `single-task-command.md` and `arcforges-implementation.md`;
  - the launcher instruction to "use up to 10 concurrent subagents";
  - the "Reviewer coverage" (2026-10-08) and "Pre-push coverage" (2026-10-09) practices that had authors and reviewers each reproduce every hosted CI step locally on the same head.
- Evidence: the 2026-10-11 waiting audit. A third of build-slot time was gates-vs-review or hosted-CI duplicates at an unchanged head, and short runs paid 6–8 queue minutes per minute of work.

## Decision

1. **Development is strictly serial.** One implementation task is active at a time. Delegation is allowed to one worker or reviewer at a time, without a required provider or model. This governs how the product is built. The product itself supports and tests parallel execution.

   > **Amendment (2026-10-27).** The user removed the model-specific delegation and attribution requirements. Use available agents without requiring a separate client login. Independent exact-head review, serial delivery and the required verification checks remain. Any commit co-author trailer or PR footer must identify the actual contributors and tools used.

2. **No build slot.** With serial development there is no competing local build, so the workstation lock (`delivery.py build-slot`) and every retry-for-a-slot instruction are retired. Once the ArcForges node delivers its execution increment (Plan milestone M2), the development workflow may run its own heavy commands through ArcForges as dogfooding. This is recorded evidence, not a precondition.
3. **Vertical increments.** Every milestone connects a real user action to working behaviour end to end (contract, node, CLI or GUI, persistence, tests). No milestone delivers disconnected interface shells awaiting a final integration.
4. **Verification responsibilities (distinct evidence only):**

| Role | Runs | Never |
|---|---|---|
| Author | Targeted unit and integration tests for the change, the affected real Windows and Linux tests, build and AOT publish of the affected components, format and analyzers. It records exact commands and results in the PR. | Skips tests it changed or that cover changed code |
| Independent reviewer (one session, after the author) | Reads the complete diff at the exact head and checks it against the task's design references and acceptance criteria. Re-runs locally only what gives **distinct** evidence: a test the reviewer doubts, a check whose script or workflow the PR changed, or a real-environment test the author could not run. | Re-runs the author's identical full suite on the same unchanged head |
| Hosted CI | Full build, unit and contract tests, AOT publish per RID, packaging, security scans | GUI, device, browser-E2E, live-service and inference jobs (local opt-in only) |
| Coordinator | Push, PR, review record, CI watch, merge at the reviewed head, publication or deployment check, ledger | Duplicates any of the above |

   Re-review after changes covers the delta only, unless the delta changes build or test infrastructure.
5. **Fast local feedback.** Authors run real Windows tests on the workstation and real Linux tests on a native Linux host ([AD-0018](AD-0018-native-platforms-without-wsl-integration.md) §5) for everyday feedback and do not wait on hosted CI for it. Hosted CI is the merge gate for the platform-independent gates.

   > **Amendment (2026-10-16, [AD-0016](AD-0016-local-first-verification.md)).** The "Hosted CI" row of §4 and "hosted CI is the merge gate" now apply to external PRs (any author other than `deku2026`, Dependabot included). The owner's PRs are gated by the repository-managed pre-push verification at the pushed head plus the independent review, and run no hosted validation. *Amended 2026-10-22 by [AD-0020](AD-0020-post-push-verification-and-required-checks.md): the owner's verification runs after the push on each host and is enforced by the required commit statuses `arcforges/windows` and `arcforges/linux` on `main`.*
6. **Fakes only at unavailable boundaries.** Closed-loop automated tests may fake:
   - other machines;
   - Cloudflare, Paddle, Google Play, FCM and app stores;
   - AI clients' internals;
   - controlled failure scenarios.

   They never fake the behaviour under test. Real OS enforcement, deployment and full product acceptance are never claimed from fakes (R-TEST-001).

   > **Amendment (2026-10-17, [AD-0016](AD-0016-local-first-verification.md) §5, amendment).** By the user's decision of that day, routine tests also replace the OS secret store with the isolated secret-store backend, for behaviour above the secret-store adapter. The adapters' own OS integration tests use the real store, in the separate tier of [16](../architecture/16-testing-strategy.md) §1.
7. **Task states (Plan ledger):** `planned`, `active`, `blocked` (waiting on named human prerequisites or register entries; not counted as the active task), `delivered` (merged and published or deployed, own acceptance met at development stage), `complete` (also all completion prerequisites and recorded real-environment evidence that is possible now) and `superseded`.

   Deferred real-world validation (acceptance register) does not block `complete` for development-stage scope. It is tracked to its own register entry with prerequisites, trigger and owner.
8. **Blockers.** A task needing an unavailable human action (credentials, purchases, signing custody, a physical device, approval to publish) completes everything else and records the exact pending step in the acceptance register.
   - If the step prevents delivery, the task becomes `blocked` with the register IDs, and the plan continues with the next task that does not depend on it.
   - The Plan graph's `depends_on` lists only real dependencies (the serial order is separate), so independent tasks are never held back by a blocked one.
9. **Implementation delivery, production activation and real-world acceptance are separate.**
   - **Delivery** means merged, with the task's development-stage acceptance met: real implementations, verified on the workstation and the local cloud stack with approved external fakes. Cloud and Web merges deploy dark: flagship surfaces stay disabled in production ([10](../architecture/10-cloud.md) §8). No implementation merge waits for production key material, domains, provisioning or publication approval.
   - **Production activation** is its own task (AF-PROD-01), after the release candidate. It needs the user's approval and the production prerequisites, and enables the surfaces step by step. The approvals it needs are never bypassed: publication of the public site and enabling production surfaces stay explicit user decisions.
   - **Real-world acceptance** is the acceptance register: real payments, devices, physical LANs, production signing.
10. **Continuous serial execution once authorized.** A run gate holds until the user authorizes implementation by giving a session the Plan's execution prompt (`execution-prompt.md`) with a range of `sequence.md` steps; that range is the authorized scope. The authorization is recorded as a Plan ledger note, so every later session can see it; without an unfinished authorized range a coordinator only reports status. Within the range, the coordinator works through eligible tasks one at a time without asking for "continue" after each delivery, and it never starts a task outside the range. It reports each delivery, skips `blocked` tasks, and stops only when:
    - an outward-facing approval is needed;
    - the authorized range is complete;
    - no eligible task remains;
    - a decision only the user can make is required;
    - the user says stop.
