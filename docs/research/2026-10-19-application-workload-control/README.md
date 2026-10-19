# Vision-correction study: research evidence and lab plans

- **Study date:** 2026-10-19. **Curated for publication:** 2026-10-19.
- **What this folder is:** the research evidence and the lab plans behind the corrected long-term direction recorded in AD-0017 as amended on 2026-10-19 and in Design chapters 17 (`docs/architecture/17-delegated-execution.md`) and 18 (`docs/architecture/18-application-workload-control.md`). Its rows support roadmap rows: the exploratory rows, the widened RM-09 and RM-16 … RM-18, not release-1 work.
- **What it is not:**
  - It holds no release-1 facts. Release-1 behaviour is stated by the Design chapters, the contracts and the delivered code. Observations the study made about delivered or planned release-1 tasks are recorded outside this record, for the product owner and the owning tasks' reviewers, and are not published here.
  - It is not the verification register. Verification facts are cited by verification ID from [platform-capabilities.md](https://github.com/ArcForges/ArcForges-Design/blob/main/docs/verification/platform-capabilities.md); nothing in this folder adds, changes or proves a verification entry.
  - Nothing here has been run as a lab experiment, and nothing here is a decision. Values are attainable values under stated conditions, never realized guarantees.
- **Scope.** Process-level confinement, resource control, lifecycle, cooperation and failure diagnosis of applications and other workloads. GUI display, window, keyboard, mouse and clipboard isolation, screen protection, secure desktops, secure display surfaces, anti-overlay systems and separate-device approval mechanisms are not researched or proposed by this study (the scope correction of 2026-10-19); facts the study gathered about them are not published, except where a display, bus or input channel decides a process-level guarantee as a launcher cell, a named gap or a disclosed dependency.
- **Privacy:** no file describes the owner's own machines, accounts or WSL distributions. Facts the study read from them were removed or restated host-neutrally before publication.
- **Earlier record:** the [2026-10-18 record](../2026-10-18-delegated-execution/README.md) stays as published; its facts (`D-…`) and labs (`LAB-…`, gates G01 … G41) keep their IDs. A `LAB2-…` ID is never the earlier register's `LAB-…` ID of the same number.

## Files

| File | Topic |
|---|---|
| `lab-register.md` | The LAB2 entries (`LAB2-WIN-nn`, `LAB2-LNX-nn`, `LAB2-MAC-nn`, `LAB2-X-nn`), their venues and rules, the gates G42 … G51 and G20-I, the gates of the earlier register they touch, and the minimum set per claim |
| `evidence/win-resource.md` | Windows job objects and resource control of applications |
| `evidence/win-confine.md` | Windows process-level confinement of GUI and headless applications (AppContainer, LPAC, packaging) |
| `evidence/gf09-windows-facts.md` | Windows facts settled across tracks (redirection, notification activation, input methods, Windows on Arm) |
| `evidence/lnx-resource.md` | Linux cgroup v2 and systemd control of applications |
| `evidence/lnx-confine.md` | Linux process-level confinement tiers per display system |
| `evidence/gf08-linux-gui-compat.md` | Linux compatibility surfaces of confined GUI applications (packaging formats, input methods, accessibility, settings) |
| `evidence/macos.md` | macOS capability statements (no decisions) |
| `evidence/resource-api.md` | Cooperative resource coordination semantics |
| `evidence/gf04-coop-api.md` | The cooperative API surface and the caller identity ladder |
| `evidence/gf10-clients.md` | Language-neutral cooperative clients |
| `evidence/gf01-placement.md` | Placement, accounting and default semantics of owner-directed applications |
| `evidence/gf02-vocabulary.md` | The status vocabulary and the diagnosis schema |
| `evidence/diagnostics-identity.md` | Limit-failure diagnosis and application identity |
| `evidence/gf05-access-denial.md` | Access-denial diagnosis for confined applications |
| `evidence/gf06-workload-classes.md` | Third-party workload classes: media, IDEs, services |
| `evidence/games.md` | Games and interactive workloads |
| `evidence/storage.md` | Storage budgets, capacity constructions and private data |
| `evidence/first-party.md` | The first-party reference (ArcSlate as built, unchanged) |
| `evidence/gf12-inter-app.md` | Interactions between applications and delegated operations |
| `evidence/gf07-tamper-human.md` | Owner-directed controls against an application working against the owner (process-level conclusions only) |
| `evidence/gf11-cost.md` | The cost model and maintenance burden |
| `evidence/gf15-control-clients.md` | Control clients (Android, iOS, the Web) |
| `evidence/landscape.md` | The landscape of comparable tools and the rejected product directions |

## Evidence labels

The labels and terms are the [2026-10-18 record](../2026-10-18-delegated-execution/README.md)'s (E1, E1-DP, E2 … E6; SPECIFIED; "E4 → E2 (lab)"; "Analysis, no primary source"), with one addition: the strength HINT (a setting the operating system may not honour, or that the workload can undo; it holds against no adversary class), proposed in chapter 17 §3.2.

Source markers: **pointer** (a single post, issue or forum report; weaker than E3 and never decisive alone) and **vendor-tracker** (an issue in a vendor's public tracker).

## How to read the files

A `gfNN-` prefix is part of a file's stable name and carries no other meaning.

**Evidence files.** Each file has a header, a fact table and a closing "Review corrections" section, as in the 2026-10-18 record.
- **ID** is `D2-<file>-<n>`, stable within its file; the Design cites facts by this ID. Numbers are not reassigned; a fact not published leaves a gap in the numbering.
- **Claim, Evidence, Primary source(s), Report section** as in the 2026-10-18 record. The study's reports, digests and reconciliations are working files and are not published, so "Report section" is provenance only.
- **Review corrections.** Each study report was adversarially verified, and three reconciliations were challenged independently. Where a claim and its correction differ, **the corrected statement governs**, and the correction is given in full.
