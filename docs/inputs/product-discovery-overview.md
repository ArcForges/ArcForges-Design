Below is the **minimal overview of ArcForges Stage 0–28**, stating only what each stage is actually responsible for.

## I. Stage 0–12: First, Establish the Commercial Platform

| Stage | Name | Core Responsibilities |
| --- | --- | --- |
| **0** | **Portfolio / Product / Business Foundation** | Define the ArcForges product portfolio as a whole, the business model, and the overall positioning of Local-first + open source + paid Cloud. |
| **1** | **Identity / Account / Workspace** | Define accounts, Workspaces, Devices, Sessions, Installations, as well as login/local anonymous usage and Official/Self-host Realms. |
| **2** | **Website / Marketing / Product Surfaces** | Define the official website, product introduction pages, download entry points, account entry points, and other outward-facing product portals. |
| **3** | **Billing / Payment** | Define the commercial payment system covering payments, subscription purchases, renewals, and refunds. |
| **4** | **Entitlement** | Define "what the user purchased and is therefore eligible to use", strictly independent of Feature Flags and the permission system. |
| **5** | **Distribution / Release / Update** | Define independent installation, versioning, release channels, updates, rollbacks, installers, and mirror distribution for the four Apps. |
| **6** | **ArcChat Platform Direction** | Freeze ArcChat's platform role: Chat + Agent + Task Center + Automation + Capability Hub + Local Hub. |
| **7** | **Cloud / Mobile / Web** | Define the responsibilities of Cloud, and ArcChat Mobile/Web as Companions rather than full professional Apps. |
| **8** | **AI Economics / Provider / Cost** | Define AI Providers, Models, BYOK, Managed AI, Credits, costs, and commercial billing relationships. |
| **9** | **Sync / Backup / User Assets** | Define Local-first Sync, Cloud Replica, Blobs, Backups, asset upload strategies, and multi-device recovery. |
| **10** | **Cloud Production Infrastructure** | Define Azure/Cloudflare, production deployment, security infrastructure, observability, and operational foundations. |
| **11** | **Legal / Open Source** | Define AGPL, privacy, legal, third-party licensing, and open-source governance. |
| **12** | **Growth / Community / Product UX Direction** | Define growth, community, ecosystem discovery, cross-product recommendations, and the "Standalone excellent, together better" product direction. |

---

## II. Stage 13–20: Fully Defining the Four Actual Products

| Stage | Name | Core Responsibilities |
| --- | --- | --- |
| **13** | **Product Topology & Architecture Baseline Freeze** | Final freeze of the four products (ArcChat / ArcNotes / ArcScope / ArcSlate), data ownership, dependency direction, Hub boundaries, and technical exceptions. |
| **14** | **Shared Desktop Product Experience Foundation** | Define shared experience specifications for the four Desktop Apps: Design System, Commands, Shortcuts, Settings, Windows, Notifications, Errors, Deep Links, Drag & Drop, Multi-window, etc. |
| **15** | **ArcNotes Complete Product Specification** | Fully define ArcNotes: Notebooks, Documents, Blocks, Editor, Links, Tags, Properties, Attachments, History, Search, AI, Knowledge, etc. |
| **16** | **ArcScope Complete Product Specification** | Fully define ArcScope: Devices/Data Sources, Connections, Sessions, Capture, Signals, Triggers, Measurements, Analysis, Decoders, Reports, etc. |
| **17** | **ArcChat Complete Product Specification** | Turn ArcChat into a true product: Home, Conversations, Composer, Projects, Task Center, Artifacts, Agents, Skills, MCP, Providers, Search, etc. |
| **18** | **ArcChat Mobile & Web Companion Specification** | Fully define Mobile/Web Companion: Remote Tasks, Approvals, Steering, Artifacts, Notifications, Device Presence, Cloud Tasks, and cross-device continuity. |
| **19** | **Unified Agent Execution / Task / Automation Model** | Unify Intent → Task → Run → Step → Attempt → Capability, along with execution semantics such as Pause, Retry, Checkpoint, Approval, Budget, and Automation. |
| **20** | **ArcSlate Complete Product Specification & Olive-to-C# Rewrite Plan** | Fully define the ArcSlate professional video editing product, and determine which Olive capabilities are retained/improved/dropped, along with the C# + Avalonia rewrite boundaries. |

---

## III. Stage 21–24: Unifying the Four Products into a Platform

| Stage | Name | Core Responsibilities |
| --- | --- | --- |
| **21** | **Cross-App Semantic Capability & Resource Model** | Unify the cross-App business language: App, Instance, Capability, Action, Context, Artifact, ResourceRef, Deep Link, Event, Health, Invocation, Compatibility. |
| **22** | **Local Data / Project Format / Interoperability Architecture** | Define local Canonical Data, DB/File/Hybrid, Project Formats, Autosave, Undo/Revision, Recovery, Migration, Import/Export, Git friendliness, and Portability. |
| **23** | **Knowledge / Search / Retrieval Architecture** | Define Knowledge Sources, Local/Cloud Indexes, Keyword/Semantic/Hybrid Search, AI Retrieval Scope, Evidence, Citations, Exclude from AI, and ArcNotes/ArcChat responsibilities. |
| **24** | **Extension / Integration / Developer Platform** | Unify Skills, Templates, Workflows, MCP, Connectors, External Agents, Extensions, Third-party Apps, SDKs, CLIs, Packages, Catalogs, Publishers, Trust, and Compatibility. |

---

## IV. Stage 25–27: Enabling Long-Term Safe and Stable Platform Evolution

| Stage | Name | Core Responsibilities |
| --- | --- | --- |
| **25** | **Dynamic Configuration & Product Policy Control Plane** | Unify Feature Flags, Rollouts, Kill Switches, Remote Config, Minimum Versions, Provider/Model Availability, and Experiments, strictly distinguished from Settings and Entitlements. |
| **26** | **Product Security / Permission / Trust Closure** | Unify Human/Agent/Automation Actors, Permissions, Approvals, Risk R0–R4, Secrets, Data Egress, Remote permissions, Extension Trust, and Audit. |
| **27** | **Product Quality & Compatibility Contract** | Turn performance, memory, startup, AOT, Accessibility, Localization, Units, version compatibility, Migration, Recovery, Diagnostics, and cross-platform testing into hard release contracts. |

---

## V. Stage 28: Resolving "What to Do When Issues Arise" in Real Operations

| Stage | Name | Core Responsibilities |
| --- | --- | --- |
| **28** | **Support / Feedback / Operator / Trust & Safety Operations** | Define Bug/Feature Feedback, Private Support, Diagnostic Bundles, data recovery, Operator permission boundaries, impersonation prohibition, community reporting, malicious packages, Copyright/Abuse, Removal, Appeals, and Security Advisories. |

---

## Summary of 0–28 in Five Sentences

### **0–12: How the commercial platform is established**

Accounts, Cloud, billing, synchronization, infrastructure, legal, growth.

### **13–20: What the four products actually are**

ArcChat, ArcNotes, ArcScope, ArcSlate, along with the shared desktop experience and agent execution model.

### **21–24: How the four products form a unified platform**

Cross-App semantics, data formats, Knowledge/Search, and Extension/Developer ecosystems.

### **25–27: How this platform evolves safely and stably over the long term**

Dynamic Policy, security permissions, and quality and compatibility contracts.

### **28: How issues are handled once real commercial operations begin**

Support, Recovery, Operator, Trust & Safety, Security Advisories.

So **Stage 0–28** as a whole already forms a very clear closed loop:

> **Commercial foundation → Product definition → Platform interconnection → Safe and stable evolution → Real-world operational safeguards.**
