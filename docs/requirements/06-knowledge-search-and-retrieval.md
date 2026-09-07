# Knowledge, Search and Retrieval Requirements
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md), [`05-ai-and-agent-execution.md`](05-ai-and-agent-execution.md), [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md)

The pipeline, fixed:

```
Knowledge Source → Scope → Index → Search → Retrieval → Evidence → Citation → AI Context
```

Two ownership statements govern everything below:

> **ArcNotes is the long-term knowledge authority. ArcChat is the cross-source retrieval and agent-retrieval orchestrator, and never a second knowledge store.**

---

## 1. Knowledge Source

**Knowledge Source = an authoritative source of content that may be discovered, retrieved, or used to answer knowledge questions.** It is **not** a copy of the data.

| # | Requirement |
|---|---|
| KS-01 | **Knowledge Source ≠ Data Copy** ([I-130](01-normative-glossary-and-invariants.md#rule-i-130)). Declaring a source never duplicates its content into a knowledge store. |
| KS-02 | **Knowledge Source ≠ Context Provider** ([I-131](01-normative-glossary-and-invariants.md#rule-i-131)). A context provider answers "what is the user looking at now"; a knowledge source is a durable retrievable corpus. A context provider may point at a resource inside a knowledge source. |
| KS-03 | **Knowledge Source ≠ Import** ([I-132](01-normative-glossary-and-invariants.md#rule-i-132)). Adding a source does not create new owned resources. |
| KS-04 | **Declaring a source never changes ownership.** An ArcNotes notebook used as a knowledge source is still owned by ArcNotes. |
| KS-05 | A Knowledge Source definition carries at minimum: identity, owning application, scope of inclusion, a policy set (§4), and its current index state. |
| <a id="rule-ks-06"></a>KS-06 | A source may represent a **collection** (a notebook, a project, a folder). An individual resource inside it may **override** the collection policy, and the resource-level override takes precedence. |

### 1.1 Per-product sources

| Product | What is a knowledge source | What is not |
|---|---|---|
| **ArcNotes** | Notebooks, folders, documents, blocks, managed attachments with extracted text | — |
| **ArcChat** | Its own conversations, projects and artifacts | **ArcChat is not the user's long-term knowledge base** |
| **ArcScope** | Project, session and report metadata; findings; annotations; reports | **Raw telemetry is not a plain text corpus** |
| **ArcSlate** | Project and media metadata; transcripts; subtitles; markers | **Raw video is not a default vector corpus** |

| # | Requirement |
|---|---|
| KS-10 | **Raw ArcScope capture data does not become an ordinary text knowledge source** ([I-160](01-normative-glossary-and-invariants.md#rule-i-160)). It is reached through ArcScope's professional query, measurement and analysis capabilities. |
| KS-11 | **Raw ArcSlate video is not a default vector corpus** ([I-161](01-normative-glossary-and-invariants.md#rule-i-161)). Multimodal video embedding is not a V1 dependency. |
| KS-12 | **Web search results are not a long-term knowledge source by default** ([I-149](01-normative-glossary-and-invariants.md#rule-i-149)). Retaining web content long-term is an explicit act that creates an owned resource in an owning application. |

---

## 2. Knowledge Scope and Index Scope

**Knowledge Scope = which knowledge sources and resources a search or retrieval is permitted to consider.**

| # | Requirement |
|---|---|
| SC-01 | **Knowledge Scope ≠ Index Scope** ([I-133](01-normative-glossary-and-invariants.md#rule-i-133)). Knowledge scope is a query-time boundary; index scope is what has actually been indexed. A resource may be in scope and not yet indexed, and vice versa. |
| SC-02 | Scope may be **fixed** (these notebooks) or **dynamic** (documents modified this week, unresolved findings). |
| SC-03 | **Knowledge Scope is not an ownership boundary**. ArcChat scoping a search across ArcNotes and ArcScope does not make ArcChat their owner. |
| SC-04 | **Scope always obeys realm and workspace.** Crossing either requires an explicit user switch or authorization; it never happens implicitly. |
| SC-05 | **A Local Profile is a legal scope.** `Realm = Local`, workspace = none — a signed-out user has a complete local knowledge scope. |

---

## 3. Indexes

**The index is always a derived projection.**

| # | Requirement |
|---|---|
| <a id="rule-ix-01"></a>IX-01 | **Index ≠ Canonical Data** ([I-134](01-normative-glossary-and-invariants.md#rule-i-134)); **Search Index ≠ Knowledge Authority** ([I-135](01-normative-glossary-and-invariants.md#rule-i-135)); **Semantic Index ≠ Knowledge** ([I-138](01-normative-glossary-and-invariants.md#rule-i-138)). Every index may be deleted and rebuilt without losing user data. |
| IX-02 | Four index kinds exist: **metadata**, **keyword/lexical**, **semantic**, and **specialised domain** indexes. |
| <a id="rule-ix-03"></a>IX-03 | **Keyword search must work with no AI model present.** It is the baseline capability, never a fallback for a failed model. |
| <a id="rule-ix-04"></a>IX-04 | **Semantic search is never the only search capability.** A semantic backend outage degrades ranking, never search itself. |
| IX-05 | **Not everything becomes a vector.** Structured measurements, timecodes and typed properties use specialised domain indexes owned by their products. |
| <a id="rule-ix-06"></a>IX-06 | **There is no central ArcForges graph database as the authority for all data.** Link-graph retrieval is one signal, owned as a derived domain relation by the product that owns the links. |
| IX-07 | Each product owns native lexical/domain indexes over available local data; Cloud owns its derived semantic index. ArcChat cannot read another product index database directly. |
| IX-08 | The index carries an **`IndexSchemaVersion`** and an **`ExtractionProfile`** version, so a pipeline change is a rebuild rather than silent inconsistency. |
| IX-09 | **The index is protected data.** It contains user content in derived form and is subject to the same confidentiality, isolation and deletion rules as its source. |
| <a id="rule-ix-10"></a>IX-10 | **Index engine choice is not frozen here.** Swapping the lexical, vector or specialised engine must never change resource identity, and must never require a knowledge source to be re-added — only a derived rebuild. |
| IX-11 | Replacing a **semantic model** likewise leaves resource identity, source revision and knowledge source membership unchanged; only the derived representation changes. |

### 3.1 Indexing pipeline

`Extract → Normalise → Chunk → Embed / Tokenise → Store → Watermark`

| # | Requirement |
|---|---|
| IP-01 | **Extraction is owner-specific.** Each owning product produces the best representation of its own data; a generic extractor must not be imposed on a specialised domain. |
| IP-02 | **Writes and indexing are not one transaction** ([SY-38](03-cloud-services-and-sync.md#rule-sy-38)). A write is durable immediately; the index catches up. Search is an eventual projection. |
| <a id="rule-ip-03"></a>IP-03 | **An index failure is not a source failure** ([I-166](01-normative-glossary-and-invariants.md#rule-i-166) family). The resource remains fully usable; only its searchability is degraded, and that state is visible. |
| IP-04 | **Search must know its own freshness.** `IndexWatermark` and per-result freshness are first-class, so a stale result can be labelled as such. |
| IP-05 | **Keyword index updates should be as fast as practical**, because users expect a just-saved document to be findable. |
| <a id="rule-ip-06"></a>IP-06 | Indexing is a bounded product/platform Job with progress, cancellation and recovery, not an Agent Task by default. Model-based embedding/reranking runs in Cloud; native lexical index maintenance requires no model. |
| IP-07 | Index build is **bounded**: a background resource budget, plus power and device policy (for example not on battery, not on a metered connection where cloud work is involved). |
| IP-08 | Cloud indexing carries a **cost policy**, visible and controllable, because embedding and reranking are real cost of goods. |
| <a id="rule-ip-09"></a>IP-09 | Attachment text extraction and OCR are **derived pipeline** outputs, never canonical assets. OCR output anchors back to page and region so a citation can point at the original. |
| IP-10 | **Knowledge Source Health** is exposed: healthy, partially indexed, failing, stale — with counts and last-attempt information. |

### 3.2 Retrieval units and chunking

| # | Requirement |
|---|---|
| RU-01 | **Retrieval Unit ≠ Domain Resource** ([I-154](01-normative-glossary-and-invariants.md#rule-i-154)). A retrieval unit is a derived index representation. |
| RU-02 | **A retrieval-unit identifier is never citation authority** ([I-153](01-normative-glossary-and-invariants.md#rule-i-153)). A citation must never be a vector-database chunk id. |
| RU-03 | **Every retrieval unit carries a Source Anchor** locating it in the owner's own addressing scheme: document and block, page and region, session and time range, timecode. |
| RU-04 | **Chunking is content-aware** and must not destroy semantic boundaries. Chunk size is an implementation parameter, not a permanent contract — changing it triggers a rebuild. |
| RU-05 | **Changing an embedding does not change the source revision** ([I-165](01-normative-glossary-and-invariants.md#rule-i-165)). The source did not change; its derived representation did. Index entries track their processing version separately. |
| RU-06 | Different content types may use different embedding strategies. Text-first is the V1 baseline; forcing one embedding across all content types is prohibited. |

---

## 4. Knowledge policy: processing and retrieval boundaries

Search visibility, Cloud indexing, AI retrieval and provider processing have distinct permissions. No local semantic-model mode exists.

| Dimension | Question |
|---|---|
| **Searchable** | May it appear in search results at all? |
| **Cloud Index Allowed** | May a derived index be built in the cloud? |
| **AI Retrieval Allowed** | May its content be retrieved as evidence for an AI answer? |
| **Managed AI Processing Allowed** | May its content be sent to a managed AI provider? |

| # | Requirement |
|---|---|
| PL-01 | Exclude from AI denies model-based processing and AI retrieval, including new embedding/reranking calls, independently of ordinary keyword search. Apply the deny before every dispatch/retrieval; already-sent data cannot be recalled and must not be described as never processed. |
| PL-02 | **Exclude from AI ≠ Hide from Search** ([I-144](01-normative-glossary-and-invariants.md#rule-i-144)). An excluded document may still be findable by title and keyword; its content simply never reaches a model. |
| PL-03 | No local embedding/model loop or local semantic provider configuration. Native keyword/metadata search over available content remains distinct from Cloud semantic retrieval. |
| PL-04 | **Cloud managed semantic indexing requires Managed AI Processing permission**, because it sends content to managed AI infrastructure. |
| PL-05 | Cloud embedding/reranking for eligible indexed content is subscription-funded platform cost, measured under the AI usage contract and bounded by workspace indexing/resource policy. It does not silently spend purchased credits. New model calls stop outside an active service term. |
| <a id="rule-pl-06"></a>PL-06 | **Sync ≠ AI** ([I-182](01-normative-glossary-and-invariants.md#rule-i-182)) and **Cloud Sync ≠ Cloud Index** ([I-140](01-normative-glossary-and-invariants.md#rule-i-140)) and **Cloud Index ≠ AI Retrieval** ([I-141](01-normative-glossary-and-invariants.md#rule-i-141)) and **AI Retrieval ≠ Managed AI Processing** ([I-143](01-normative-glossary-and-invariants.md#rule-i-143)). Four independent gates. |
| PL-07 | Policy **inherits** from source to resource, with resource-level override winning. |
| PL-08 | Realm and owner workspace policy may prohibit overrides. A resource-level or one-request choice cannot loosen a governing deny. |
| PL-09 | A **temporary AI override** for one request is permitted where policy allows it; it must not silently change the durable source policy. |
| PL-10 | **Explicit context selection is still subject to Exclude from AI.** A user attaching an excluded document does not thereby override the exclusion; the product states why it cannot be used. |

---

## 5. Search versus retrieval

| Concept | Purpose | Output |
|---|---|---|
| **Search** | Find resources | A ranked list of `SearchResult` |
| **Retrieval** | Gather evidence for an AI answer | An `EvidenceSet` |

| # | Requirement |
|---|---|
| SR-01 | **Search ≠ Retrieval** ([I-146](01-normative-glossary-and-invariants.md#rule-i-146)) and **Search ≠ Ask AI** ([I-147](01-normative-glossary-and-invariants.md#rule-i-147)). Search need not invoke any generative model. |
| SR-02 | **`SearchResult` is not a `Citation`** ([I-152](01-normative-glossary-and-invariants.md#rule-i-152)). |
| <a id="rule-sr-03"></a>SR-03 | **ArcChat Global Search is federated**, querying each owning product and merging results. ArcChat does **not** maintain a central local full-text index of all products' data ([I-031](01-normative-glossary-and-invariants.md#rule-i-031)). |
| <a id="rule-sr-04"></a>SR-04 | **ArcChat must not read another product's index database directly.** Federation goes through capability calls. |
| SR-05 | When an owning product is not running, ArcChat may **launch it on demand** to serve a federated query, subject to the ordinary capability and permission model. |
| SR-06 | A lightweight federated-search cache is permitted; it is **disposable**, records source and revision, and is never a write point. |
| SR-07 | **Cloud Search is a derived cloud projection** over data that legitimately entered the cloud and is permitted to be cloud-indexed. It is never business authority. |
| <a id="rule-sr-08"></a>SR-08 | **A local-only resource never appears in cloud search.** The cloud does not know its content, and must not acquire it in order to make search work. |
| <a id="rule-sr-09"></a>SR-09 | **Search result rows display their owner**, so the user always knows where the thing actually lives. |
| SR-10 | **There is no universal property database for unified filtering.** Platform-level filters are platform semantics; product-specific filters are product contracts served by the owner. |
| <a id="rule-sr-11"></a>SR-11 | **Mobile and web search cloud-visible data by default.** Searching a desktop's local data from mobile is an **explicit remote search Task**, subject to remote authorization. |
| SR-12 | **Remote search results are not an upload.** Returning matches does not transfer the source into the cloud. |
| SR-13 | Search surfaces **indexing status** so an incomplete result set is legible rather than mysterious. |

### 5.1 Hybrid retrieval

| # | Requirement |
|---|---|
| HR-01 | **Keyword + semantic + metadata form hybrid retrieval.** `Keyword Search ≠ Semantic Search` ([I-145](01-normative-glossary-and-invariants.md#rule-i-145)); both are first-class. |
| HR-02 | **Hybrid is not the sum of two scores.** Ranking fusion with normalisation is required; naive score addition across incomparable scales is prohibited. |
| HR-03 | **Exact match receives strong priority.** Lexical exactness stays first-class — a user searching a precise technical term must find it. |
| HR-04 | **Reranking is an optional enhancement layer.** A reranker failure degrades ordering; it must never fail the retrieval. |
| HR-05 | Managed reranking is subject to managed AI policy. |

### 5.2 Retrieval budget

| # | Requirement |
|---|---|
| RB-01 | Retrieval is **not a fixed Top-K**. A `RetrievalBudget` governs candidate count, evidence count and context construction size. |
| RB-02 | A **per-source cap** and a diversity policy prevent one large source from crowding out every other. |
| RB-03 | **Deduplication uses identity and content**, not titles. |
| RB-04 | Where a local and a cloud index return the same logical resource, **the local current version takes precedence**; a cloud result arriving first must not win by timing. |
| RB-05 | **Local and cloud indexes are not two resource identities** ([SY-10](03-cloud-services-and-sync.md#rule-sy-10)). One logical `ResourceRef` underlies both. |
| RB-06 | Graph expansion across links is **budgeted and loop-protected**. A source graph may contain cycles; traversal must deduplicate and bound depth. |
| RB-07 | **A link is a retrieval signal, not a relevance guarantee.** |
| RB-08 | **User pinning outranks automatic retrieval.** Explicitly attached context is always eligible within permission and policy. |

---

## 6. Permission and the index

| # | Requirement |
|---|---|
| PM-01 | **The index can never expand permission** ([I-139](01-normative-glossary-and-invariants.md#rule-i-139)). *If you cannot read the resource, you cannot search its contents.* |
| PM-02 | Permission is applied as early as possible — **authorization-aware retrieval** narrows candidates rather than filtering after the fact. |
| PM-03 | **Evidence fetch re-checks current authorization** at the moment of materialisation, not only at candidate time. |
| PM-04 | **A permission change triggers index reconciliation.** Content must stop being returned immediately; query visibility must be correct immediately, even if the physical index reconciliation completes asynchronously. |
| <a id="rule-pm-05"></a>PM-05 | Cloud indexes are **partitioned by realm and workspace**. A cross-workspace probe must fail on partitioning, not on filtering. |
| PM-06 | **Embedding is not anonymisation** ([I-139](01-normative-glossary-and-invariants.md#rule-i-139)). An embedding is a derived representation of user content and carries the same protection obligations. |
| PM-07 | **Knowledge eligibility ≠ read permission** ([I-253](01-normative-glossary-and-invariants.md#rule-i-253)). Being permitted to read something does not make it AI-eligible, and vice versa. |
| PM-08 | A **searchable but locked** resource is legitimate: it is discoverable, and access is governed by the owner's authorization policy. |

### 6.1 Removal and deletion

| # | Requirement |
|---|---|
| RM-01 | **Source Removal ≠ Delete Files** ([I-168](01-normative-glossary-and-invariants.md#rule-i-168)). Removing a knowledge source stops indexing and retrieval; it does not delete the user's data. |
| RM-02 | Excluding a source enters a **purge and invalidation** process for its derived index entries. |
| RM-03 | Deleting a resource in its owning product **is** an owner domain delete, and propagates to derived indexes ([DE-04](03-cloud-services-and-sync.md#rule-de-04), [DE-05](03-cloud-services-and-sync.md#rule-de-05)). |
| RM-04 | Index deletion and privacy withdrawal delete the derived semantic index **without** deleting canonical cloud data. |
| RM-05 | **Search stops finding a deleted resource.** An older conversation citation may still exist as provenance history, but it is marked as pointing at deleted content. |

---

## 7. Evidence and citation

**Evidence = a specific source fragment, validated against scope, permission, freshness and source, and permitted to be supplied to a particular AI retrieval.**

**Citation = a verifiable reference from an AI output to an item of Evidence.**

| # | Requirement |
|---|---|
| EC-01 | **Retrieval Candidate ≠ Evidence ≠ Citation** ([I-150](01-normative-glossary-and-invariants.md#rule-i-150), [I-151](01-normative-glossary-and-invariants.md#rule-i-151)). Three stages, three types. |
| EC-02 | Evidence binds: source resource, source revision, anchor, the permission decision that admitted it, and its freshness at the time. |
| EC-03 | **Citations are produced by the system's evidence mapping**, never by the model. A model must not be able to author a citation identity. |
| EC-04 | **A citation can never point to a vector chunk id** ([I-153](01-normative-glossary-and-invariants.md#rule-i-153)). It points at the owner's addressable anchor. |
| EC-05 | Per-product citation anchors: ArcNotes opens the document at the cited block; a PDF opens the page and region; ArcScope opens the session at the cited measurement, range or finding; ArcSlate opens the timecode; ArcChat opens the message. |
| EC-06 | **Citations carry the source revision.** Where the historical revision is still retrievable, the citation resolves to it; where it is not, the citation states that the content has changed since it was cited. |
| EC-07 | A small **Evidence Digest** excerpt may be retained for display. **Copying an entire source into ArcChat is prohibited.** |
| EC-08 | **A citation points at the original source first.** A derived summary may be used as evidence, but must be **marked derived** and must carry the source revision of what it derived from. |
| <a id="rule-ec-09"></a>EC-09 | **AI answers that use knowledge cite by default**, and evidence must be traceable. |
| EC-10 | **An unevidenced internal citation cannot be fabricated.** A claim with no admitted evidence carries no citation. |
| EC-11 | Model knowledge and user knowledge are distinguished as far as practical, so the user can tell which claims are retrieval-grounded. |
| EC-12 | Citations and search results support **deep link and handoff**. On a device lacking the owning application, a preview or cloud representation is offered — the full text is never copied to the cloud merely to make a mobile link clickable on a local-only resource. |

### 7.1 Revalidation

| # | Requirement |
|---|---|
| RV-01 | **AI must revalidate before actually using a retrieved result.** A candidate found in a stale index is confirmed against the authoritative owner before it becomes evidence. |
| RV-02 | Where the resource changed since indexing, the retrieval either re-fetches, re-anchors, or drops the candidate — it never presents stale content as current. |
| RV-03 | **AI retrieval is stricter on a stale index than search is.** Search may return a labelled stale hit; retrieval requires authoritative fetch or revalidation. |

### 7.2 Freshness

Three separate freshness notions ([I-166](01-normative-glossary-and-invariants.md#rule-i-166)):

| Kind | Meaning |
|---|---|
| **Source Freshness** | When the authoritative resource last changed |
| **Index Freshness** | When the derived index last caught up to it |
| **Derived Artifact Freshness** | When a derived summary or analysis was produced, and against which source revision |

Search results may display a stale status; the AI path must resolve staleness rather than display it.

---

## 8. AI retrieval scope — the privacy boundary

This is the most consequential privacy control in the product.

| # | Requirement |
|---|---|
| AS-01 | Scope resolution is **explicit or inherited**, in a defined priority: an explicitly attached context; the project's configured knowledge scope; the agent profile's configured default scope; then nothing. |
| <a id="rule-as-02"></a>AS-02 | **There is no default that lets an ordinary conversation search everything the user owns.** A conversation outside a project has no ambient knowledge scope. |
| AS-03 | A **project conversation** may see the project's configured knowledge scope, and only that. |
| AS-04 | An **agent profile may carry a default knowledge scope**, but only when the user explicitly configured it. |
| <a id="rule-as-05"></a>AS-05 | **AI cannot silently expand scope.** Any expansion is a user-visible act. |
| <a id="rule-as-06"></a>AS-06 | **Scope expansion enters the Retrieval Trace.** |
| <a id="rule-as-07"></a>AS-07 | **An automation's knowledge scope is stable and frozen into the run's evidence scope** at Run start. It must not drift while the Task executes, and must not expand indefinitely. |
| <a id="rule-as-08"></a>AS-08 | **Data minimisation is the retrieval principle**: retrieve the minimum evidence necessary to answer the task. |
| AS-09 | **AI retrieval permission is not unlimited context** ([I-155](01-normative-glossary-and-invariants.md#rule-i-155)). Permission to retrieve from a source does not authorise dumping the source into a prompt. |
| AS-10 | **The model cannot bypass retrieval policy by calling an owner capability for a full dump.** Capability-level guards apply the same policy. |

### 8.1 Retrieval trace

| # | Requirement |
|---|---|
| RT-01 | **Retrieval Trace is first-class operational data**: what was searched, in what scope, what candidates were considered, what was admitted as evidence, what was excluded and why. |
| RT-02 | **Retrieval Trace ≠ chain-of-thought** ([I-167](01-normative-glossary-and-invariants.md#rule-i-167)). It records verifiable search and retrieval operations, not hidden reasoning. |
| <a id="rule-rt-03"></a>RT-03 | An **AI Context Inspector** lets the user see what the model was actually given, before or after the answer, including sources used and sources excluded with reasons. |

### 8.2 Context pack

**Context Pack = the authorised evidence plus necessary context finally supplied to the model.**

| # | Requirement |
|---|---|
| CP-01 | **Context Pack ≠ entire knowledge source** ([I-155](01-normative-glossary-and-invariants.md#rule-i-155)). |
| <a id="rule-cp-02"></a>CP-02 | **Retrieve references first, materialise content last.** The pack is kept as small as the task allows. |
| <a id="rule-cp-03"></a>CP-03 | **Large resources stay on the owner's side** and are reached by owner-side query. ArcScope answers with measurements and analysis rather than raw capture; ArcSlate answers with transcripts, metadata and timecodes rather than video. |
| CP-04 | **Retrieval uses the owner's best representation of the data**: text and document retrieval for ArcNotes, structured analytical retrieval for ArcScope, transcript/metadata/timecode retrieval for ArcSlate, text chunks plus vectors for general prose. |

---

## 9. Per-product responsibilities

| Product | Knowledge responsibility |
|---|---|
| **ArcNotes** | The user's long-term knowledge authority. Owns documents, blocks, links, tags, typed properties, attachments and their extracted text; owns its local index; owns citation anchors; is the destination when a user promotes something into long-term knowledge. |
| **ArcChat** | Knowledge **retrieval orchestrator**: global federated search, project knowledge scopes, AI retrieval orchestration, hybrid retrieval, context packing, internal citations, retrieval trace. Indexes **only its own data** — conversations, projects, its own artifacts. **Never copies the ArcNotes knowledge store.** |
| **ArcScope** | Specialist knowledge provider: searchable project/session/report metadata, findings, annotations and reports; structured measurement and analysis retrieval through professional capabilities. |
| **ArcSlate** | Specialist knowledge provider: project and media metadata search, transcript/subtitle/marker search, timecode citations, through professional media capabilities. |
| **Cloud** | Derived cloud projection: cloud-visible keyword search, cloud resource search, optional semantic index, permission-aware query, mobile and web search. |

| # | Requirement |
|---|---|
| PR-01 | **ArcChat Personal Memory does not enter the knowledge corpus** ([I-156](01-normative-glossary-and-invariants.md#rule-i-156), [I-157](01-normative-glossary-and-invariants.md#rule-i-157)). It is ArcChat-owned preference recall, not a searchable corpus of everything the user ever said. |
| PR-02 | **Conversation context is not a knowledge source** ([I-159](01-normative-glossary-and-invariants.md#rule-i-159)). |
| PR-03 | Cross-application search uses the unified cross-application `ResourceRef` model. |

---

## 10. Knowledge pollution control

| # | Requirement |
|---|---|
| <a id="rule-kp-01"></a>KP-01 | **An AI-generated analysis does not automatically become knowledge** ([I-164](01-normative-glossary-and-invariants.md#rule-i-164)). Model output is not silently written into the long-term corpus. |
| KP-02 | **Knowledge promotion is explicit**: the user asks, and the owning product creates a formal resource. |
| KP-03 | **A derived AI summary carries the source revision it derived from**, so its staleness is computable. |
| KP-04 | This rule exists to prevent a feedback loop in which the model's own past output becomes the evidence for its future output. |

---

## 11. External sources

| # | Requirement |
|---|---|
| ES-01 | An external source — an MCP server, a connector — **still has an owner**, expressed as an external integration adapter, and carries its own policy set. |
| ES-02 | Three external source shapes are distinguished: **Live Remote Source** (queried at the provider on demand), **Imported Snapshot** (creates a new owned resource in an owning product), **Synced External Projection** (a derived replica with explicit replica semantics). |
| ES-03 | **Knowledge does not automatically index the whole computer.** Sources, folders and projects are added explicitly. |
| ES-04 | External drives are not indexed by default. |
| ES-05 | **MCP tool descriptions, resource contents and prompts are untrusted data**, never instructions ([I-262](01-normative-glossary-and-invariants.md#rule-i-262), [I-263](01-normative-glossary-and-invariants.md#rule-i-263)). |

---

## 12. Separation from adjacent systems

| # | Statement |
|---|---|
| SP-01 | **Knowledge ≠ Backup.** Cloud backup may hold data that search must not parse or index; index eligibility is a separate decision from backup inclusion. |
| SP-02 | **Knowledge ≠ Sync.** Synchronising a resource does not make it AI-eligible or cloud-indexable. |
| SP-03 | **Knowledge ≠ Semantic.** Semantic indexing is one retrieval technique, not the definition of knowledge. |
| SP-04 | **Web search ≠ knowledge** ([I-148](01-normative-glossary-and-invariants.md#rule-i-148), [I-149](01-normative-glossary-and-invariants.md#rule-i-149)). Web results are transient, cost credits, and are labelled distinctly from cloud search in the interface. |

---

## 13. Quality assurance

| # | Requirement |
|---|---|
| <a id="rule-qa-01"></a>QA-01 | A **Knowledge Evaluation Set** exists and is run as automated regression: representative queries with expected results, run against every index and retrieval change. |
| QA-02 | **Citation accuracy is tested**, not assumed: does the anchor resolve, does it point at the cited content, does it survive a revision change. |
| QA-03 | **Index freshness is tested**: time from write to lexical searchability, and from write to semantic availability. |
| <a id="rule-qa-04"></a>QA-04 | **Search quality is not assumed to follow from a larger model.** Retrieval quality is measured directly and governed by the quality contract in [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md). |

---

## 14. V1 scope

**Required in V1**, per product, as listed in §9.

**Explicitly not required in V1** — architecturally supported, deliberately deferred:

- Full multimodal video embeddings
- An image semantic corpus spanning everything
- A global knowledge-graph engine
- Automatic whole-filesystem indexing
- Advanced graph RAG
- Cross-owner or cross-realm federated search
- Every external SaaS connector
- Complex learned reranking
- Real-time collaborative knowledge curation

---

## 15. Domain model

```
KnowledgeSource · KnowledgeSourcePolicy · KnowledgeScope · KnowledgeScopeBinding
IndexPartition · IndexState · IndexWatermark · IndexSchemaVersion · ExtractionProfile
RetrievalUnit · RetrievalAnchor
LexicalIndexEntry · SemanticIndexEntry · SpecializedIndexReference
SearchQuery · SearchScope · SearchFilter · SearchResult · SearchMatchKind
RetrievalQuery · RetrievalBudget · RetrievalCandidate
Evidence · EvidenceRef · EvidenceSet · ContextPack
Citation · CitationRef · RetrievalTrace
KnowledgeFreshness · AIEligibility · CloudIndexEligibility · SemanticIndexEligibility
```

---

## 16. Acceptance scenarios

**Local search** — an authorized hydrated ArcNotes corpus remains keyword/metadata searchable offline; an exact technical term is found without model execution or fresh Cloud access.

**Semantic failure** — the semantic backend is unavailable; keyword search continues to work and the degradation is visible.

**Index rebuild** — the entire index is deleted; user data is intact; the rebuild is a cancellable, resumable, bounded background task; search returns to full quality.

**Freshness** — a just-saved document is findable quickly; a stale result is labelled; AI retrieval revalidates before using it.

**Exclude from AI** — an excluded document is still findable by title; its content never enters a model context; an explicit attachment of it is refused with a reason.

**Search without AI** — native keyword/metadata search works on available cached content while AI retrieval is disabled; no local embedding model runs.

**Cloud sync ≠ AI** — a synced notebook is not thereby AI-eligible or cloud-indexed.

**Local-only source** — never appears in cloud search; a mobile search does not surface it; an explicit remote search Task can find it without uploading it.

**Federated search** — results merged across products with owners shown; a closed application is launched on demand or reported as unavailable.

**Citation** — a citation opens the exact block, page region, session range or timecode; a citation to a changed revision reports the change; a citation to a deleted resource remains as provenance and is marked.

**Scope** — a non-project conversation retrieves nothing implicitly; a project conversation retrieves only its configured scope; an automation's scope is frozen at run start.

**Workspace isolation** — a cross-workspace query is refused by partitioning.

**Permission revocation** — content stops being returned immediately; index reconciliation follows.

**Duplicate local/cloud** — one logical resource, local current version preferred.

**Index failure** — the source remains usable, the failure is visible, and retry is bounded.

**Source removal** — indexing and retrieval stop; no user file is deleted.

**Web search** — labelled distinctly from cloud search, costs credits, and does not silently become long-term knowledge.

**AI pollution prevention** — a generated analysis does not enter the knowledge corpus without explicit promotion.

---

## 17. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 23` | The entire knowledge, search and retrieval architecture, including the four-dimension policy model, evidence and citation semantics, retrieval scope as the privacy boundary, and the V1 scope split |
| `I4 §Stage 7 §22–26` | Cloud search levels, workspace scoping, respect for product data policy |
| `I4 §Stage 9` | Derived-data classification, deletion propagation, index rebuildability |
| `I4 §Stage 15`, `§Stage 16`, `§Stage 20` | Per-product knowledge responsibilities and citation anchors |
| **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** | Managed embedding and reranking are cost of goods, not user-credit consumption |
