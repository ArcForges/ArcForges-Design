# Design Governance

## Purpose

ArcForges Design separates source material, canonical requirements, architecture, decisions, delivery planning, and assurance so that each statement has a clear owner.

## Authority

Authority is assigned by concern, as defined in `AGENTS.md`. Informative source material never overrides an accepted canonical document. A later timestamp or filename does not establish authority.

## Change lifecycle

1. Record the motivation and affected concern.
2. Draft the change in the owning canonical document.
3. Add an architecture decision record when the choice is structurally significant, difficult to reverse, or affects a key quality attribute.
4. Update dependent documents and traceability in the same pull request.
5. Review and accept the pull request.
6. Derive or update delivery planning only after the upstream design is accepted.

## Status vocabulary

| Status | Meaning |
|---|---|
| `draft` | Incomplete working material. |
| `proposed` | Ready for a decision review. |
| `accepted` | Approved as the current design for its stated concern. |
| `superseded` | Replaced by a linked newer document or decision. |
| `retired` | No longer applicable and not replaced. |
| `informative` | Context or provenance; never normative. |

Document acceptance and implementation completion are separate states.
