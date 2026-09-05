# WP-15 — ArcChat Conversation and Project Core

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `14` · Downstream: `17`

> **Goal.** Build ArcChat's own domain — conversation, message, branch, attachment, project, profile and skill — as durable local state with search, history and recovery, independent of any other product.

---

## 1. Scope and purpose

**In scope.** The conversation domain model and its persistence; message composition, streaming assembly and branching; attachments; projects and profiles; skills as declarative guidance; local search over conversation content; and conversation history, export and recovery.

**Out of scope.** Task execution (`16`). Ecosystem capabilities that depend on other products (`20`). Cloud sync (`25`). Managed AI economics (`43`) — providers are adapter-shaped and may be stubbed here.

**Why this package exists.** `I2 §III.4` requires ArcChat to be completed **without dependencies on other products** first. An ArcChat that only works when ArcNotes is running is not an independent product.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcchat.md`](../../requirements/products/arcchat.md) | The full ArcChat product model, V1 scope and acceptance scenarios |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The completed ArcChat Reference Coverage Matrix from `WP-00.04` |
| [`../../architecture/04-desktop-application-architecture.md`](../../architecture/04-desktop-application-architecture.md) | Host structure, MVVM, threading and persistence |
| `WP-07` output | The local store, journal and recovery |
| `WP-14` output | The Hub and a working provider |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The ArcChat Reference Coverage Matrix and licence audit are complete before this package begins** (`DC-02`; gates `PG-01`, `P-02`). |
| BR-02 | **ArcChat is fully usable with every other product absent.** |
| BR-03 | **`Conversation ≠ Project` and `Project ≠ Workspace`.** Three distinct containers with distinct ownership. |
| BR-04 | **A skill is declarative guidance and never code** (`I4 §Stage 24 §4`), and **a skill confers no capability** (`§5` there). |
| BR-05 | **A branch is a first-class structure**, not a hidden copy; branching never mutates the original. |
| BR-06 | **Streaming assembly is a presentation concern.** The durable message is written once, complete; a partial stream is never the stored fact. |
| BR-07 | **An attachment is either managed or referenced**, and the distinction is explicit and visible. |
| BR-08 | **Local search is a first-class capability**, available with no cloud and no account. |
| BR-09 | **A provider adapter is an interface**; the real provider integration lands in `43`. |
| BR-10 | **Hidden reasoning from a model never enters the product model** (`I4 §Stage 24 §50`). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.Domain/` | Conversation, message, branch, attachment, project, profile, skill |
| `src/ArcChat/ArcChat.Application/` | Application services for every operation, shared by UI and RPC |
| `src/ArcChat/ArcChat.Infrastructure/` | Store schema, search index, attachment storage, provider adapter interfaces |
| `src/ArcChat/ArcChat.Presentation/` | View models for conversation, project, profile and skill surfaces |
| `src/ArcChat/ArcChat.Desktop/` | The real ArcChat shell surfaces |
| `fixtures/formats/arcchat/` | The first ArcChat export fixtures |
| `tests/ArcChat.Tests.*` | Domain, application, store, search and recovery suites |

**Major types introduced.** `Conversation`, `Message`, `MessagePart`, `Branch`, `Attachment`, `AttachmentKind`, `Project`, `AgentProfile`, `Skill`, `SkillVersion`, `ConversationSearchIndex`, `ConversationExport`.

---

## 5. Required implementation work

### WP-15.00 — Conversation and message model

**What must be fully done.** Conversations own ordered messages composed of typed parts. Messages are immutable once committed; an edit produces a new revision with the prior one retained. Streaming produces a durable message exactly once at completion, with interruption handled explicitly rather than storing a truncated fragment as fact.

**Testing requirements.** Immutability and revision tests; a stream-interruption test asserting no partial message is stored as complete; large-conversation performance against the scale corpus.

**Completion gate.** A committed message is immutable, an interrupted stream never produces a message claiming to be complete, and large conversations meet the responsiveness budget.

### WP-15.01 — Branching

**What must be fully done.** Branching from any message produces an independent continuation sharing prior history by reference, never by copy. Branch navigation, comparison and deletion are supported. Deleting a branch never affects its parent.

**Testing requirements.** Branch independence, shared-history integrity and deletion-isolation tests.

**Completion gate.** Branching never mutates the original and never duplicates shared history.

### WP-15.02 — Attachments

**What must be fully done.** Managed attachments enter the managed resource store with integrity verification; referenced attachments record an external location with an availability state. Neither is embedded in message content. Availability changes are surfaced rather than producing an error at read time.

**Testing requirements.** Managed round-trip with integrity verification; reference-unavailable behaviour; a test asserting no attachment body is embedded in message storage.

**Completion gate.** Attachments are stored by reference, integrity is verified, and unavailability is a visible state rather than a failure.

### WP-15.03 — Projects and profiles

**What must be fully done.** A project groups conversations and context with its own settings; an agent profile bundles model choice, mode and behavioural configuration. Both are first-class objects with their own lifecycle. A profile is not a skill and a project is not a workspace.

**Testing requirements.** Lifecycle tests; a distinction test asserting the three container concepts are not interchangeable.

**Completion gate.** Projects and profiles have independent lifecycles and are structurally distinct from workspaces and skills.

### WP-15.04 — Skills

**What must be fully done.** Skills are versioned declarative guidance that reference capabilities without conferring them. A skill update never modifies a historical result. Skills are manageable as first-class objects rather than buried in settings.

**Testing requirements.** A test asserting a skill grants no capability; a versioning test asserting historical results are unchanged by an update.

**Completion gate.** A skill confers no capability, and updating a skill leaves historical results untouched.

### WP-15.05 — Local search

**What must be fully done.** Full-text search over conversation content, attachments' extracted text and project metadata, available with no cloud and no account. The index is a derived store: deleting it rebuilds. Search respects the same permission model as direct access.

**Testing requirements.** Index rebuild-from-scratch test; relevance tests against a fixture corpus; a permission test asserting search reveals nothing direct access would refuse.

**Completion gate.** Search works offline and account-free, the index rebuilds fully, and search never leaks what access would refuse.

### WP-15.06 — History, export and recovery

**What must be fully done.** Conversation history with restoration; export to the portable format and to a human-readable form; recovery after a hard kill with explicit reporting of any uncommitted loss.

**Testing requirements.** Export round-trip; kill-during-write recovery; an export completeness check against the portability requirements.

**Completion gate.** Export round-trips completely, and recovery reports loss explicitly rather than silently discarding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The ArcChat store schema and its first migration baseline |
| Protocol | ArcChat's own capabilities become registrable in `17` |
| UI | The real ArcChat surfaces |
| Security | Attachment handling and search permission boundaries |
| Platform | Attachment and export file handling per platform |
| Migration | ArcChat schema version 1 and its fixture |
| Compatibility | The first ArcChat export format version |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Immutability, streaming and scale results | `WP-15.00` |
| Branch independence results | `WP-15.01` |
| Attachment integrity and availability results | `WP-15.02` |
| Container distinction results | `WP-15.03` |
| Skill capability-free and versioning results | `WP-15.04` |
| Index rebuild, relevance and permission results | `WP-15.05` |
| Export round-trip and recovery results | `WP-15.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. The ArcChat Reference Coverage Matrix and licence audit are complete.
2. Committed messages are immutable; an interrupted stream never stores a fragment as complete; large conversations meet the responsiveness budget.
3. Branching shares history by reference and never mutates the original.
4. Attachments are stored by reference with integrity verification, and unavailability is a visible state.
5. Projects, profiles and skills are structurally distinct, with skills conferring no capability and updates not altering history.
6. Local search works offline and account-free, rebuilds from scratch, and leaks nothing direct access would refuse.
7. Export round-trips completely and recovery reports uncommitted loss explicitly.
8. **ArcChat is fully usable with every other product absent.**

---

## 9. Dependencies

**Upstream.** `14` (Hub and a working provider).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `17` — ArcChat V1A | The domain the independent core completes |
| `20` — First workflow | Conversations and artifacts to attach a real workflow to |
| `25` — Sync | The ArcChat schema and revision semantics |
| `31` — Mobile | The conversation semantics the companion mirrors |
