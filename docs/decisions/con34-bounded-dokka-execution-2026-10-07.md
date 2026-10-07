# CON.34 bounded Dokka execution support

Decision: P2-064. This decision admits one opt-in execution setting in the existing Contracts root Gradle build. It preserves the real documentation generator, all output admission checks and the default build and publication behavior.

## 1. Observed failure and actual boundary

CON.34's source checkpoint `10801218798d2d6e1686ebaadc01b55e2225a5f8` preserves accepted CON.31 `c990df25dbe721b0df2d8e7aedc28e02468ae3e1`. Its actual ordinary C#, TypeScript and Kotlin generated component checks passed. Those source/component facts remain distinct from successful documentation production or publication.

The first actual Dokka attempt exceeded its 840-second budget. A corrected attempt reused genuinely completed unchanged tasks, omitted `--rerun-tasks`, and exceeded its 1800-second budget. Both were stopped through their exact owned process trees before normal workstation-slot release. The retained corrected log and thread diagnostic place the blocked Gradle execution worker in `CaptureOutputsAfterExecutionStep`, `DefaultOutputSnapshotter`, `DirectorySnapshotter` and file hashing after the `:contracts-proto:dokkaGeneratePublicationHtml` action. Neither timeout is a successful documentation receipt, and partial files cannot establish admission.

The existing pinned Gradle is 9.7.1. Its public [`Task.doNotTrackState` API source](https://github.com/gradle/gradle/blob/v9.7.1/subprojects/core-api/src/main/java/org/gradle/api/Task.java) declares the supported task-state control introduced in 7.3. The [official incremental-build guide](https://docs.gradle.org/current/userguide/incremental_build.html#sec:disable_up_to_date_checks) explains that an untracked task executes without Gradle's up-to-date state checks. The current guide is newer than the pinned distribution; no Gradle or Dokka upgrade is admitted.

## 2. Exact source change

CON.34 may append only the following setting to `Contracts:build.gradle.kts`: the project property `arcforgesBoundedDokkaProduction` has a closed literal value `true` when explicitly selected; an absent property leaves the existing behavior unchanged, and any other supplied value fails configuration rather than silently enabling a mode. Only the exact task `:contracts-proto:dokkaGeneratePublicationHtml` receives `Task.doNotTrackState` when that property is explicitly enabled. The reason string identifies the diagnosed Gradle state-snapshot overhead and the separately required immutable documentation admission.

Keep the task's actual Dokka action, inputs, outputs, dependencies, worker isolation and source sets intact. Do not apply the setting to other tasks or projects. Do not add `onlyIf`, task disabling, replacement actions, output exclusions, ignored init scripts, relaxed file/hash checks or altered normalization. Default CI, ordinary Gradle invocations and publication commands do not set this property and retain their current behavior. The opt-in producer executes the actual documentation action; it cannot acknowledge cached partial output as successful generation.

## 3. Actual production and immutable binding

After the reviewed paired admission, execute the existing pinned JDK17/Gradle/Dokka producer with the explicit `-ParcforgesBoundedDokkaProduction=true` argument, the existing release version, `--no-daemon`, `--console=plain` and `--no-build-cache`. Reuse unchanged genuinely completed prerequisites. Retain a finite 1800-second recipe budget, exact command, start/end, exit status, log and owned-process cleanup on failure. A further failure requires diagnosis; this decision authorizes no identical retry or extension of the bound.

Only terminal successful real production supplies the successor's actual page inventory. Bind the exact revised root `build.gradle.kts` bytes and complete producer command/property to CON.34's existing immutable provenance and dependency-review successor protocol. Record the actual source checkpoint, pinned tool identities, actual input and output hashes and whether the opt-in was selected. This setting cannot be omitted from the producer evidence or attributed to the old unmodified source. Preserve the actual evaluated dependency-input map and derive every changed binding from its real bytes; invent no changed dependency, coordinate or receipt count.

P2-062's existing r21-to-r22 scope remains in force. The strict documentation parser, normalizer, resource copying, fixed/excluded/component/font identities, exact source input and output membership, public API marker checks and independent finite historical/successor regression remain unchanged. Preserve every accepted immutable predecessor. A completed generator action without a successful bounded command and those ordinary admission checks does not grant documentation acceptance.

## 4. Ownership and validation

The implementation claimant remains `w-codex-20261006-provider` under CON.34. Only that task gains the exact root-build write entry and this decision note; all other task objects, metadata, edges, obligations, outcomes and completion requirements stay unchanged. Policy is the sole independent full reviewer of this paired planning repair; Root owns the paired fence. Governance retains Contracts integration and normal publication.

Validate the revised configuration's absent, exact-true and malformed-property behavior with bounded affected task configuration checks, then run the one diagnosed real producer and existing output-admission checks. Do not repeat already passing SDK components or add public downloads, installed consumers, OS or live provider tests. Applicable latest-head independent source review, CI, admission and normal publication remain required. This execution repair changes no native possession wire, helper transcript, refresh-context carriage or identity authority and establishes no product or deployment acceptance.
