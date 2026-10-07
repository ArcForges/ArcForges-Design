# Execution terminal state and no-answer registry

This minimum clarification closes the actual generic-string boundary discovered while consuming HAR03. Published ExecutionOutput.state and noAnswerReason do not currently provide generated enum/registry validation. Preserve the accepted HAR03/CON37 producer, optional pre-admission lineage, nullable genuine terminal companions and all existing wire fields/tags. No DTO, package, storage field, clock profile or permission is added.

## 1. Factual terminal state

ExecutionOutput.state is the exact current execution owner's state Key, never output-body availability or stream presentation. A terminal Task uses succeeded, partiallySucceeded, failed, canceled or interrupted; a terminal ChatTurn uses succeeded, failed, canceled or interrupted. partiallySucceeded is Task-only. The value must match the genuine current Progress.Task.state or Progress.turn.state and actual owner identity/revision at the producer's original guarded terminal observation. Nonterminal queued/running/waiting/paused owners are represented by Progress, not a fabricated terminal output. The receipt's available/acknowledged/purged/expired/keyUnavailable states remain separate original receipt/body availability facts and never overwrite this state.

interrupted is a factual owner observation, not proof of success or authority for paid retry; existing resumability/unknown reconciliation rules remain required. A completed presentation stream cannot mint an owner terminal state. Missing, expired or purged answer content does not alter the actual terminal state, create a no-answer reason or authorize a local successful answer commit. Answer/snapshot paths retain their actual required body/owner/attempt/stream/hash lineage. MessageDraft has only Parts/Context, not a role: preserve its complete Context and compare its actual Parts/content-origin to the committed MessageView while requiring the actual terminal MessageView.Role=assistant. Genuine inline Cloud MessageView keeps its actual role/identity unchanged. General Key/ReasonCode compatibility remains unchanged; unknown or state-mismatching terminal policy values are unavailable/unsupported for this consumer, never success.

## 2. Closed metadata-only meanings

The initial owner registry for the specific HAR03 metadata-only terminal path is:

| Exact reason | Genuine current owner state |
| --- | --- |
| execution.no_answer.completed | Task succeeded/partiallySucceeded or ChatTurn succeeded, with an actual declared absence of an answer |
| execution.no_answer.failed | Task/ChatTurn failed |
| execution.no_answer.canceled | Task/ChatTurn canceled |

Each is an exact nonempty ASCII Key<=128. The owner reason (TaskSnapshot.reason or ChatTurnProgress.reason), ExecutionProgress.noAnswerReason and ExecutionOutput.noAnswerReason have the same original registered meaning under the existing immutable owner and actual optional attempt/stream presence guards. Genuinely absent pre-admission attempt/stream remains absent. Unknown, empty, unregistered or state-mismatching strings cannot enter the metadata-only successful/no-answer seal. The generic generated string shape checker establishes no registration by itself. The general ReasonCode wire registry stays open/additive; only this owning terminal admission policy is closed.

These meanings come from the genuine owner terminal decision and are committed with its original safe outcome/usage/settlement facts. EOF, missing body, failed download, timeout, replayed caller string or a completed stream cannot select a key. No empty/fabricated MessageView, MessageDraft, FinalHash, resource, local MessageId or answer receipt is introduced. Original output proof/command framing/migration and no paid retransmit remain unchanged.

## 3. Actual components and ownership

HAR03 owns the actual Task/Chat producer state/reason policy, strict output projection and registered-reason verification. AST01 consumes the actual current owner/proof and preserves the same immutable value before local Complete. Their existing source/test scopes suffice; this decision does not broaden writes or change starts/outcomes/complete acceptance. Required ordinary components cover each factual mapping, Task-only partial success, interrupted non-success, foreign/unknown/empty/mismatched keys/states, body unavailability, mutually exclusive answer/no-answer arms and genuine absent pre-admission IDs. No repeated passed suite, external inference or deployed acceptance is inferred.
