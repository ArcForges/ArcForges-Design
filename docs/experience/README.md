# Client Experience Specifications

These are implementation authorities under [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012), alongside existing product requirements and the shared design system. They specify surfaces, actions, state, persistence and acceptance; they do not import additional reference-product scope.

- [Embedded application assistant](01-embedded-assistant.md): complete Avalonia package and host integration UX.
- [Kotlin Android companion](02-android-companion.md): routes, layouts, native interaction and one-application targeting.
- [Shared states and acceptance](03-state-and-acceptance.md): authentication, streaming, files, privacy, account and failure behavior with producer assignments.

Web keeps its React Site/Account/Chat/Operations profiles. Chat uses the assistant content and state semantics below, responsive browser controls, cookie/CSRF sessions and Cloud history. It has no local product database, local listener or Android-only permission UI. Professional Notes/Scope/Slate editors remain specified by their product requirements and executable profiles; they embed the assistant without losing their own command/recovery behavior.

AionUi reference: `C:/MyFile/Projects/AionUi`, inspected commit `29c9271a5`; mobile ChatScreen/ChatInputBar/ConfirmationCard/FileContentView/theme and desktop ChatLayout/SendBox. Reuse layout/composer/preview ideas and authorized visual resources with per-file provenance on actual reuse. Its local-server connect/QR protocol is not our login, and its external agent ecosystem is not added. The wireframes here are first-party layout specifications, not copied screenshot assets.
