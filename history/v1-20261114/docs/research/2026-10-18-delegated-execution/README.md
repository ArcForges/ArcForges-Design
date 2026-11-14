# Delegated-execution study: research evidence and lab plans

- **Study date:** 2026-10-18. **Curated for publication:** 2026-10-19.
- **What this folder is:** the research evidence and the lab plans behind the proposed delegated-execution direction, recorded in AD-0017 and Design chapter 17 (`docs/architecture/17-delegated-execution.md`). Its rows support roadmap rows of the EX class (and RM-15), not release-1 work.
- **What it is not:**
  - It holds no release-1 facts. Release-1 behaviour is stated by the Design chapters, the contracts and the delivered code.
  - It is not the verification register. Verification facts are cited by verification ID from [platform-capabilities.md](https://github.com/ArcForges/ArcForges-Design/blob/main/docs/verification/platform-capabilities.md); nothing in this folder adds, changes or proves a verification entry.
  - Nothing here has been run as a lab experiment, and nothing here is a decision. Values are attainable values under stated conditions, never realized guarantees.
- **Privacy:** no file describes the owner's own machines, accounts or WSL distributions. Facts the study read from them were removed or restated host-neutrally before publication.

## Files

| File | Topic |
|---|---|
| `lab-register.md` | The 74 lab entries (`LAB-WIN-nn`, `LAB-LNX-nn`, `LAB-MAC-nn`, `LAB-X-nn`), their venues and rules, the decision gates G01 … G41, the first-backend rule and the minimum lab set |
| `evidence/win-primitives-completion.md` | Windows primitives below the account boundary: jobs, tokens, integrity levels, AppContainer and LPAC |
| `evidence/win-strong.md` | Windows strong isolation, execution control and network control |
| `evidence/win-install.md` | Windows installation lifecycle |
| `evidence/lnx-kernel.md` | Linux kernel and systemd mechanisms |
| `evidence/lnx-projects.md` | Linux sandboxing projects, network control, desktop and IPC exposure, portable formats |
| `evidence/linux-chain-install.md` | The Linux launch chain and managed installation |
| `evidence/macos.md` | macOS mechanisms |
| `evidence/x-agents.md` | Agent, tool and MCP-server sandboxes; WASI |
| `evidence/x-lifecycle.md` | Application lifecycle, supply-chain trust, snapshots, policy model and Native AOT |
| `evidence/acquisition-runtimes.md` | Acquisition runtimes, extension hosts, updaters and GPU |
| `evidence/persistence-observation-recovery.md` | Persistence, privileged-change observation, revocation and recovery |
| `evidence/identity-ipc-completion.md` | Caller identity, IPC reach and cache trust |
| `evidence/credentials-completion.md` | Group budgets and credential mediation |

## Evidence labels

| Label | Meaning |
|---|---|
| **E1** | Demonstrated in ArcForges: delivered code, a Design section or a verification ID, cited by an https link to `main` of [ArcForges/ArcForges](https://github.com/ArcForges/ArcForges) or [ArcForges/ArcForges-Design](https://github.com/ArcForges/ArcForges-Design) |
| **E1-DP** | First-party code in [ArcForges/DesktopPlatform](https://github.com/ArcForges/DesktopPlatform), outside the node, that the node consumes or that sets a precedent |
| **E2** | Officially supported and documented by the OS vendor or the specification owner |
| **E3** | Demonstrated by a mature third-party project (its source code, documentation or release notes) |
| **E4** | Technically feasible, but needs a prototype or a lab run; the row says what must be shown |
| **E5** | Speculative, with significant unknowns |
| **E6** | Impractical, unsafe, redundant or inappropriate for ArcForges |

Further terms:
- **SPECIFIED** means the ArcForges Design specifies the mechanism, but it is not delivered.
- **"E4 → E2 (lab)"** and **"E4 → E3 (lab)"** in the lab register are what a passing run would establish, for the tested build only. **"E1 (venue-scoped)"** is a run of ArcForges code on a lab venue; it counts as Design evidence only after the AD-0002 venue amendment the register describes.
- **"Analysis, no primary source"** marks a claim that rests on the study's own reasoning. It is never stronger than E4.
- An E4 or E5 claim is never promoted to a guarantee by argument, only by the lab run or delivery that the row names.

## How to read the files

**Evidence files.** Each file has a header, a fact table and a closing "Review corrections" section.
- **ID** is `D-<file>-<n>`, stable within its file. Rows elsewhere cite facts by this ID.
- **Claim** states the mechanism, its strength per access dimension and the privilege it needs. Strength words are ENFORCED (the OS enforces it and ArcForges can read it back or probe it), MEDIATED (a proposed strength: access passes only through an ArcForges broker that enforces it), PARTIAL (enforced with documented gaps), GUARDRAIL (enforced by ArcForges, or bypassable by the same user), OBSERVED (detected and reported only) and NONE. Privileges: P0 standard user; P1 a one-time administrator or root step; P2 elevation for each operation; P3 a vendor entitlement, a signing requirement or a driver.
- **Adversary classes:** A1 accidental damage; A2 an over-privileged but honest tool; A3 a compromised tool or MCP server; A4 an untrusted AI-generated command; A5 malicious software that targets the isolation mechanism itself; A6 a privileged installer or system-level software. `holds_against` names the classes a value holds against.
- **Evidence** is the label of the row (see above); where several apply, each names the aspect it covers.
- **Primary source(s)** is the citable evidence: an https URL to vendor documentation, project source or an ArcForges repository at `main`.
- **Report section** names the section of the study report the fact was drawn from. The study's reports, digests and reconciliation are working files and are not published, so this column is provenance only.
- **Review corrections.** The study's review round of 2026-10-18 ruled some values overstated or incomplete. Rulings named C-nn and N-nn are from its consolidated review, and M-n from its re-review; neither review is published, so each corrected statement is given in full. **Where a claim and its correction differ, the corrected statement governs.** Claim text is left unedited so its provenance stays visible.

**Lab register.** Each entry states its question, the evidence record it draws on, its venue, hardware and privileges, a plan-level procedure, its pass and fail criteria, the evidence label a run would establish, and the gates and roadmap rows it feeds. Escape and denial suites record only reachable or denied, with the error; the register holds no bypass procedure. §0 gives the venue rules, §0.1 the operation, channel, budget and stop rule, §0.2 the first-backend rule, §2 the venue classes and owner decisions D1–D5, and §3 the gates and the minimum set.

## Citation rule

Roadmap-level assumptions cite **LAB IDs and the roadmap row ID**, for example "LAB-WIN-04, EX-10", **never A or F IDs** of the verification register. A and F items need owner tasks, and roadmap rows have none until a row is promoted. When a row is promoted, its promotion creates the owner tasks, and the facts it then relies on enter the verification register under its own rules. Facts in this folder are cited by their `D-<file>-<n>` ID and file name, and lab plans by their LAB ID and gate.
