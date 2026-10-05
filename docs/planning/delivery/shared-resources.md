# Shared Resources and Write Ownership

> Generated from [the delivery graph](delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](README.md).

Each shared file, registry, sequence, environment, key or pointer has exactly one owning role. Tasks declare how they touch it; the owner applies the protocol. Independent worktrees do not remove semantic conflicts, so these declarations are part of task readiness and merge review. A protocol that names an exclusive phase (a live run in a deployed environment, a heavy local build) binds every task that enters that phase, for that phase only, whatever mode the task declares for its other edits ([DLV-11](README.md#rule-dlv-11)).

| Resource | Kind | Owner | Tasks (mode) |
|---|---|---|---|
| [RES-ai-workflow-and-routes](#res-ai-workflow-and-routes) | file | AI integration owner | [SRCH.01](lanes/search.md#task-srch-01) (append), [SRCH.02](lanes/search.md#task-srch-02) (append), [SRCH.06](lanes/search.md#task-srch-06) (append), [AIR.00](lanes/ai-routing.md#task-air-00) (exclusive), [AIR.03](lanes/ai-routing.md#task-air-03) (append), [AIR.05](lanes/ai-routing.md#task-air-05) (append), [AIR.06](lanes/ai-routing.md#task-air-06) (append), [AIR.07](lanes/ai-routing.md#task-air-07) (append), [AIR.08](lanes/ai-routing.md#task-air-08) (append), [HAR.00](lanes/harness.md#task-har-00) (append), [HAR.01](lanes/harness.md#task-har-01) (append), [HAR.02](lanes/harness.md#task-har-02) (append), [HAR.03](lanes/harness.md#task-har-03) (append), [HAR.04](lanes/harness.md#task-har-04) (append), [HAR.05](lanes/harness.md#task-har-05) (append), [HAR.06](lanes/harness.md#task-har-06) (append) |
| [RES-android-signing-and-store](#res-android-signing-and-store) | key | Release Engineering Owner | [AND.16](lanes/android.md#task-and-16) (append), [AND.23](lanes/android.md#task-and-23) (append) |
| [RES-architecture-tests](#res-architecture-tests) | file | each repository integration owner | [GOV.04](lanes/governance.md#task-gov-04) (append), [GOV.05](lanes/governance.md#task-gov-05) (append), [GOV.06](lanes/governance.md#task-gov-06) (append), [GOV.07](lanes/governance.md#task-gov-07) (append), [GOV.09](lanes/governance.md#task-gov-09) (append), [GOV.10](lanes/governance.md#task-gov-10) (append), [GOV.11](lanes/governance.md#task-gov-11) (append), [GOV.12](lanes/governance.md#task-gov-12) (append), [GOV.17](lanes/governance.md#task-gov-17) (append), [GOV.18](lanes/governance.md#task-gov-18) (append), [GOV.20](lanes/governance.md#task-gov-20) (append), [PLT.20](lanes/platform.md#task-plt-20) (append), [PLT.23](lanes/platform.md#task-plt-23) (append), [PLT.28](lanes/platform.md#task-plt-28) (append), [PLT.29](lanes/platform.md#task-plt-29) (append), [PLT.30](lanes/platform.md#task-plt-30) (append), [PLT.31](lanes/platform.md#task-plt-31) (append), [PLT.32](lanes/platform.md#task-plt-32) (append), [PLT.33](lanes/platform.md#task-plt-33) (append), [PLT.37](lanes/platform.md#task-plt-37) (append), [PLT.38](lanes/platform.md#task-plt-38) (append), [PLT.39](lanes/platform.md#task-plt-39) (append), [PLT.40](lanes/platform.md#task-plt-40) (append), [PLT.44](lanes/platform.md#task-plt-44) (append), [PLT.45](lanes/platform.md#task-plt-45) (append), [PLT.48](lanes/platform.md#task-plt-48) (append), [PLT.51](lanes/platform.md#task-plt-51) (append), [PLT.52](lanes/platform.md#task-plt-52) (append), [PLT.57](lanes/platform.md#task-plt-57) (append), [APP.01](lanes/app-composition.md#task-app-01) (append), [APP.07](lanes/app-composition.md#task-app-07) (append) |
| [RES-arcscope-format-fixtures](#res-arcscope-format-fixtures) | file | ArcScope integration owner | [SCOPE.24](lanes/arcscope.md#task-scope-24) (append), [SIM.06](lanes/simulator.md#task-sim-06) (append) |
| [RES-arcscope-migrations](#res-arcscope-migrations) | sequence | ArcScope integration owner | [SCOPE.01](lanes/arcscope.md#task-scope-01) (append), [SCOPE.06](lanes/arcscope.md#task-scope-06) (append) |
| [RES-assistant-store-schema](#res-assistant-store-schema) | sequence | DesktopPlatform integration owner | [PLT.02](lanes/platform.md#task-plt-02) (append), [PLT.06](lanes/platform.md#task-plt-06) (append), [PLT.38](lanes/platform.md#task-plt-38) (append), [AST.01](lanes/assistant.md#task-ast-01) (append), [AST.02](lanes/assistant.md#task-ast-02) (append), [AST.03](lanes/assistant.md#task-ast-03) (append), [AST.04](lanes/assistant.md#task-ast-04) (append), [AST.05](lanes/assistant.md#task-ast-05) (append), [AST.07](lanes/assistant.md#task-ast-07) (append), [EXE.01](lanes/execution.md#task-exe-01) (append), [EXE.04](lanes/execution.md#task-exe-04) (append), [EXE.05](lanes/execution.md#task-exe-05) (append), [EXE.06](lanes/execution.md#task-exe-06) (append), [DEV.05](lanes/device-bridge.md#task-dev-05) (append), [CLOUD.18](lanes/cloud.md#task-cloud-18) (append), [CLOUD.35](lanes/cloud.md#task-cloud-35) (append), [CLOUD.38](lanes/cloud.md#task-cloud-38) (append) |
| [RES-cloud-d1-migrations](#res-cloud-d1-migrations) | sequence | Cloud integration owner | [DEV.01](lanes/device-bridge.md#task-dev-01) (append), [DEV.02](lanes/device-bridge.md#task-dev-02) (append), [DEV.04](lanes/device-bridge.md#task-dev-04) (append), [DEV.06](lanes/device-bridge.md#task-dev-06) (append), [DEV.07](lanes/device-bridge.md#task-dev-07) (append), [DEV.08](lanes/device-bridge.md#task-dev-08) (append), [SIM.01](lanes/simulator.md#task-sim-01) (append), [SIM.04](lanes/simulator.md#task-sim-04) (append), [CLOUD.03](lanes/cloud.md#task-cloud-03) (append), [CLOUD.11](lanes/cloud.md#task-cloud-11) (append), [CLOUD.13](lanes/cloud.md#task-cloud-13) (append), [CLOUD.42](lanes/cloud.md#task-cloud-42) (append), [CLOUD.48](lanes/cloud.md#task-cloud-48) (append), [COM.16](lanes/commerce.md#task-com-16) (append) |
| [RES-cloud-deployment](#res-cloud-deployment) | environment | Cloud integration owner | [PRF.05](lanes/runtime-proofs.md#task-prf-05) (read), [PRF.06](lanes/runtime-proofs.md#task-prf-06) (read), [PRF.07](lanes/runtime-proofs.md#task-prf-07) (append), [CLOUD.01](lanes/cloud.md#task-cloud-01) (append), [CLOUD.05](lanes/cloud.md#task-cloud-05) (append), [CLOUD.07](lanes/cloud.md#task-cloud-07) (append), [CLOUD.09](lanes/cloud.md#task-cloud-09) (append), [CLOUD.10](lanes/cloud.md#task-cloud-10) (append), [CLOUD.69](lanes/cloud.md#task-cloud-69) (append), [CLOUD.70](lanes/cloud.md#task-cloud-70) (append) |
| [RES-cloud-host-composition](#res-cloud-host-composition) | registry | Cloud integration owner | [PRF.07](lanes/runtime-proofs.md#task-prf-07) (append), [CLOUD.01](lanes/cloud.md#task-cloud-01) (append), [CLOUD.02](lanes/cloud.md#task-cloud-02) (append), [COM.05](lanes/commerce.md#task-com-05) (append), [COM.06](lanes/commerce.md#task-com-06) (append), [COM.07](lanes/commerce.md#task-com-07) (append), [COM.08](lanes/commerce.md#task-com-08) (append), [COM.11](lanes/commerce.md#task-com-11) (append), [COM.12](lanes/commerce.md#task-com-12) (append), [COM.13](lanes/commerce.md#task-com-13) (append), [COM.16](lanes/commerce.md#task-com-16) (append), [SRCH.00](lanes/search.md#task-srch-00) (append), [SRCH.01](lanes/search.md#task-srch-01) (append), [SRCH.02](lanes/search.md#task-srch-02) (append), [SRCH.05](lanes/search.md#task-srch-05) (append), [EXT.06](lanes/extensions.md#task-ext-06) (append), [HAR.00](lanes/harness.md#task-har-00) (append), [HAR.02](lanes/harness.md#task-har-02) (append), [HAR.04](lanes/harness.md#task-har-04) (append), [HAR.06](lanes/harness.md#task-har-06) (append) |
| [RES-cloud-leased-singletons](#res-cloud-leased-singletons) | registry | Cloud integration owner | [PRF.07](lanes/runtime-proofs.md#task-prf-07) (append), [SIM.03](lanes/simulator.md#task-sim-03) (append), [SIM.04](lanes/simulator.md#task-sim-04) (append), [SIM.05](lanes/simulator.md#task-sim-05) (append), [SIM.06](lanes/simulator.md#task-sim-06) (append), [SIM.07](lanes/simulator.md#task-sim-07) (append), [CLOUD.33](lanes/cloud.md#task-cloud-33) (append), [CLOUD.39](lanes/cloud.md#task-cloud-39) (append) |
| [RES-cloud-runbooks-and-fixtures](#res-cloud-runbooks-and-fixtures) | file | Operations Owner | [COM.04](lanes/commerce.md#task-com-04) (append), [COM.09](lanes/commerce.md#task-com-09) (append), [COM.10](lanes/commerce.md#task-com-10) (append), [COM.14](lanes/commerce.md#task-com-14) (append), [OPS.01](lanes/operations.md#task-ops-01) (append), [OPS.03](lanes/operations.md#task-ops-03) (append), [OPS.04](lanes/operations.md#task-ops-04) (append), [OPS.05](lanes/operations.md#task-ops-05) (append), [OPS.06](lanes/operations.md#task-ops-06) (append), [OPS.09](lanes/operations.md#task-ops-09) (append) |
| [RES-cloud-storage-plans](#res-cloud-storage-plans) | registry | Cloud integration owner | [PRF.07](lanes/runtime-proofs.md#task-prf-07) (regenerate), [CLOUD.02](lanes/cloud.md#task-cloud-02) (append), [CLOUD.11](lanes/cloud.md#task-cloud-11) (append), [CLOUD.42](lanes/cloud.md#task-cloud-42) (append), [COM.16](lanes/commerce.md#task-com-16) (append) |
| [RES-contract-consumer-pins](#res-contract-consumer-pins) | pointer | each consumer repository integration owner | [PRF.08](lanes/runtime-proofs.md#task-prf-08) (append), [COM.03](lanes/commerce.md#task-com-03) (append), [COM.04](lanes/commerce.md#task-com-04) (append), [COM.06](lanes/commerce.md#task-com-06) (append), [EXT.02](lanes/extensions.md#task-ext-02) (append), [WEB.01](lanes/web.md#task-web-01) (append), [WEB.10](lanes/web.md#task-web-10) (append) |
| [RES-contracts-dokka-profile](#res-contracts-dokka-profile) | pointer | Contracts integration owner | [CON.03](lanes/contracts.md#task-con-03) (exclusive), [CON.07](lanes/contracts.md#task-con-07) (exclusive), [CON.08](lanes/contracts.md#task-con-08) (exclusive), [CON.09](lanes/contracts.md#task-con-09) (exclusive), [CON.10](lanes/contracts.md#task-con-10) (exclusive), [CON.11](lanes/contracts.md#task-con-11) (exclusive), [CON.21](lanes/contracts.md#task-con-21) (exclusive), [CON.22](lanes/contracts.md#task-con-22) (exclusive), [CON.24](lanes/contracts.md#task-con-24) (exclusive), [CON.25](lanes/contracts.md#task-con-25) (exclusive) |
| [RES-contracts-generated-baseline](#res-contracts-generated-baseline) | file | Contracts integration owner | [CON.01](lanes/contracts.md#task-con-01) (regenerate), [CON.02](lanes/contracts.md#task-con-02) (regenerate), [CON.03](lanes/contracts.md#task-con-03) (regenerate), [CON.04](lanes/contracts.md#task-con-04) (regenerate), [CON.05](lanes/contracts.md#task-con-05) (regenerate), [CON.06](lanes/contracts.md#task-con-06) (regenerate), [CON.07](lanes/contracts.md#task-con-07) (regenerate), [CON.08](lanes/contracts.md#task-con-08) (regenerate), [CON.09](lanes/contracts.md#task-con-09) (regenerate), [CON.10](lanes/contracts.md#task-con-10) (regenerate), [CON.11](lanes/contracts.md#task-con-11) (regenerate), [CON.12](lanes/contracts.md#task-con-12) (regenerate), [CON.13](lanes/contracts.md#task-con-13) (regenerate), [CON.14](lanes/contracts.md#task-con-14) (regenerate), [CON.15](lanes/contracts.md#task-con-15) (regenerate), [CON.16](lanes/contracts.md#task-con-16) (regenerate), [CON.17](lanes/contracts.md#task-con-17) (regenerate), [CON.18](lanes/contracts.md#task-con-18) (regenerate), [CON.19](lanes/contracts.md#task-con-19) (regenerate), [CON.21](lanes/contracts.md#task-con-21) (regenerate), [CON.22](lanes/contracts.md#task-con-22) (regenerate), [CON.23](lanes/contracts.md#task-con-23) (regenerate), [CON.90](lanes/contracts.md#task-con-90) (regenerate), [CON.91](lanes/contracts.md#task-con-91) (regenerate), [CON.92](lanes/contracts.md#task-con-92) (regenerate), [CON.24](lanes/contracts.md#task-con-24) (regenerate), [CON.25](lanes/contracts.md#task-con-25) (regenerate) |
| [RES-contracts-publication](#res-contracts-publication) | pointer | Contracts integration owner | [CON.01](lanes/contracts.md#task-con-01) (append), [CON.02](lanes/contracts.md#task-con-02) (append), [CON.03](lanes/contracts.md#task-con-03) (append), [CON.04](lanes/contracts.md#task-con-04) (append), [CON.05](lanes/contracts.md#task-con-05) (append), [CON.06](lanes/contracts.md#task-con-06) (append), [CON.07](lanes/contracts.md#task-con-07) (append), [CON.08](lanes/contracts.md#task-con-08) (append), [CON.09](lanes/contracts.md#task-con-09) (append), [CON.10](lanes/contracts.md#task-con-10) (append), [CON.11](lanes/contracts.md#task-con-11) (append), [CON.12](lanes/contracts.md#task-con-12) (append), [CON.13](lanes/contracts.md#task-con-13) (append), [CON.14](lanes/contracts.md#task-con-14) (append), [CON.15](lanes/contracts.md#task-con-15) (append), [CON.16](lanes/contracts.md#task-con-16) (append), [CON.17](lanes/contracts.md#task-con-17) (append), [CON.18](lanes/contracts.md#task-con-18) (append), [CON.19](lanes/contracts.md#task-con-19) (append), [CON.21](lanes/contracts.md#task-con-21) (append), [CON.22](lanes/contracts.md#task-con-22) (append), [CON.23](lanes/contracts.md#task-con-23) (append), [CON.90](lanes/contracts.md#task-con-90) (append), [CON.91](lanes/contracts.md#task-con-91) (append), [CON.92](lanes/contracts.md#task-con-92) (append), [CON.24](lanes/contracts.md#task-con-24) (append), [CON.25](lanes/contracts.md#task-con-25) (append) |
| [RES-contracts-schema-sources](#res-contracts-schema-sources) | registry | Contracts integration owner | [GOV.05](lanes/governance.md#task-gov-05) (append), [CON.01](lanes/contracts.md#task-con-01) (append), [CON.02](lanes/contracts.md#task-con-02) (append), [CON.03](lanes/contracts.md#task-con-03) (append), [CON.04](lanes/contracts.md#task-con-04) (append), [CON.05](lanes/contracts.md#task-con-05) (append), [CON.06](lanes/contracts.md#task-con-06) (append), [CON.07](lanes/contracts.md#task-con-07) (append), [CON.08](lanes/contracts.md#task-con-08) (append), [CON.09](lanes/contracts.md#task-con-09) (append), [CON.10](lanes/contracts.md#task-con-10) (append), [CON.11](lanes/contracts.md#task-con-11) (append), [CON.12](lanes/contracts.md#task-con-12) (append), [CON.13](lanes/contracts.md#task-con-13) (append), [CON.14](lanes/contracts.md#task-con-14) (append), [CON.15](lanes/contracts.md#task-con-15) (append), [CON.16](lanes/contracts.md#task-con-16) (append), [CON.17](lanes/contracts.md#task-con-17) (append), [CON.18](lanes/contracts.md#task-con-18) (append), [CON.19](lanes/contracts.md#task-con-19) (append), [CON.21](lanes/contracts.md#task-con-21) (append), [CON.22](lanes/contracts.md#task-con-22) (append), [CON.23](lanes/contracts.md#task-con-23) (append), [CON.90](lanes/contracts.md#task-con-90) (append), [CON.91](lanes/contracts.md#task-con-91) (append), [CON.92](lanes/contracts.md#task-con-92) (append), [CON.24](lanes/contracts.md#task-con-24) (append), [CON.25](lanes/contracts.md#task-con-25) (append), [COM.13](lanes/commerce.md#task-com-13) (append), [POL.02](lanes/policy.md#task-pol-02) (append), [POL.03](lanes/policy.md#task-pol-03) (append), [POL.04](lanes/policy.md#task-pol-04) (append), [POL.05](lanes/policy.md#task-pol-05) (append), [POL.09](lanes/policy.md#task-pol-09) (append), [OPS.05](lanes/operations.md#task-ops-05) (append), [OPS.11](lanes/operations.md#task-ops-11) (append), [EXT.02](lanes/extensions.md#task-ext-02) (append), [EXT.04](lanes/extensions.md#task-ext-04) (append), [EXT.08](lanes/extensions.md#task-ext-08) (append) |
| [RES-design-evidence](#res-design-evidence) | file | Design integration owner | [GOV.15](lanes/governance.md#task-gov-15) (append), [SCOPE.10](lanes/arcscope.md#task-scope-10) (append), [REL.11](lanes/release.md#task-rel-11) (append) |
| [RES-desktopplatform-build-config](#res-desktopplatform-build-config) | file | DesktopPlatform integration owner | [GOV.04](lanes/governance.md#task-gov-04) (append), [GOV.12](lanes/governance.md#task-gov-12) (append), [GOV.13](lanes/governance.md#task-gov-13) (append), [GOV.15](lanes/governance.md#task-gov-15) (append), [GOV.17](lanes/governance.md#task-gov-17) (append), [GOV.18](lanes/governance.md#task-gov-18) (append), [GOV.21](lanes/governance.md#task-gov-21) (append), [FND.01](lanes/foundation.md#task-fnd-01) (append), [FND.02](lanes/foundation.md#task-fnd-02) (append), [FND.03](lanes/foundation.md#task-fnd-03) (append), [FND.04](lanes/foundation.md#task-fnd-04) (append), [FND.05](lanes/foundation.md#task-fnd-05) (append), [FND.06](lanes/foundation.md#task-fnd-06) (append), [FND.07](lanes/foundation.md#task-fnd-07) (append), [PRF.04](lanes/runtime-proofs.md#task-prf-04) (append), [PRF.05](lanes/runtime-proofs.md#task-prf-05) (append), [PRF.06](lanes/runtime-proofs.md#task-prf-06) (append), [PRF.09](lanes/runtime-proofs.md#task-prf-09) (append), [PLT.01](lanes/platform.md#task-plt-01) (append), [PLT.05](lanes/platform.md#task-plt-05) (append), [PLT.07](lanes/platform.md#task-plt-07) (append), [PLT.08](lanes/platform.md#task-plt-08) (append), [PLT.09](lanes/platform.md#task-plt-09) (append), [PLT.16](lanes/platform.md#task-plt-16) (append), [PLT.17](lanes/platform.md#task-plt-17) (append), [PLT.19](lanes/platform.md#task-plt-19) (append), [PLT.24](lanes/platform.md#task-plt-24) (append), [PLT.25](lanes/platform.md#task-plt-25) (append), [PLT.26](lanes/platform.md#task-plt-26) (append), [PLT.27](lanes/platform.md#task-plt-27) (append), [PLT.28](lanes/platform.md#task-plt-28) (append), [PLT.33](lanes/platform.md#task-plt-33) (append), [PLT.38](lanes/platform.md#task-plt-38) (append), [PLT.39](lanes/platform.md#task-plt-39) (append), [PLT.40](lanes/platform.md#task-plt-40) (append), [PLT.44](lanes/platform.md#task-plt-44) (append), [PLT.45](lanes/platform.md#task-plt-45) (append), [PLT.51](lanes/platform.md#task-plt-51) (append), [PLT.52](lanes/platform.md#task-plt-52) (append), [PLT.53](lanes/platform.md#task-plt-53) (append), [PLT.57](lanes/platform.md#task-plt-57) (append), [APP.01](lanes/app-composition.md#task-app-01) (append), [APP.08](lanes/app-composition.md#task-app-08) (append), [AST.01](lanes/assistant.md#task-ast-01) (append), [AST.10](lanes/assistant.md#task-ast-10) (append), [AST.11](lanes/assistant.md#task-ast-11) (append), [AST.17](lanes/assistant.md#task-ast-17) (append), [EXE.01](lanes/execution.md#task-exe-01) (append), [CLOUD.38](lanes/cloud.md#task-cloud-38) (append), [EXT.02](lanes/extensions.md#task-ext-02) (append), [UPD.01](lanes/updater.md#task-upd-01) (append), [UPD.03](lanes/updater.md#task-upd-03) (append) |
| [RES-desktopplatform-fixtures](#res-desktopplatform-fixtures) | file | DesktopPlatform integration owner | [PLT.04](lanes/platform.md#task-plt-04) (append) |
| [RES-desktopplatform-native-build](#res-desktopplatform-native-build) | registry | DesktopPlatform integration owner | [GOV.17](lanes/governance.md#task-gov-17) (append), [PRF.02](lanes/runtime-proofs.md#task-prf-02) (append), [PLT.39](lanes/platform.md#task-plt-39) (append), [NAT.06](lanes/native.md#task-nat-06) (append), [NAT.11](lanes/native.md#task-nat-11) (append), [NAT.13](lanes/native.md#task-nat-13) (append), [NAT.14](lanes/native.md#task-nat-14) (append), [NAT.15](lanes/native.md#task-nat-15) (append), [NAT.22](lanes/native.md#task-nat-22) (append), [NAT.24](lanes/native.md#task-nat-24) (append), [NAT.25](lanes/native.md#task-nat-25) (append) |
| [RES-desktopplatform-package-inventory](#res-desktopplatform-package-inventory) | pointer | DesktopPlatform integration owner | [GOV.06](lanes/governance.md#task-gov-06) (read), [GOV.12](lanes/governance.md#task-gov-12) (append), [GOV.17](lanes/governance.md#task-gov-17) (append), [GOV.20](lanes/governance.md#task-gov-20) (read), [FND.01](lanes/foundation.md#task-fnd-01) (append), [FND.02](lanes/foundation.md#task-fnd-02) (append), [FND.03](lanes/foundation.md#task-fnd-03) (append), [FND.04](lanes/foundation.md#task-fnd-04) (append), [FND.05](lanes/foundation.md#task-fnd-05) (append), [FND.06](lanes/foundation.md#task-fnd-06) (append), [FND.07](lanes/foundation.md#task-fnd-07) (append), [PLT.08](lanes/platform.md#task-plt-08) (append), [PLT.16](lanes/platform.md#task-plt-16) (append), [PLT.19](lanes/platform.md#task-plt-19) (append), [PLT.24](lanes/platform.md#task-plt-24) (append), [PLT.25](lanes/platform.md#task-plt-25) (append), [PLT.35](lanes/platform.md#task-plt-35) (append), [PLT.46](lanes/platform.md#task-plt-46) (append), [PLT.53](lanes/platform.md#task-plt-53) (append), [NAT.06](lanes/native.md#task-nat-06) (append), [NAT.13](lanes/native.md#task-nat-13) (append), [NAT.15](lanes/native.md#task-nat-15) (append), [NAT.22](lanes/native.md#task-nat-22) (append), [NAT.24](lanes/native.md#task-nat-24) (append), [NAT.25](lanes/native.md#task-nat-25) (append), [APP.01](lanes/app-composition.md#task-app-01) (append), [UPD.08](lanes/updater.md#task-upd-08) (append) |
| [RES-desktopplatform-policy-data](#res-desktopplatform-policy-data) | registry | DesktopPlatform integration owner | [GOV.01](lanes/governance.md#task-gov-01) (append), [GOV.03](lanes/governance.md#task-gov-03) (append), [GOV.04](lanes/governance.md#task-gov-04) (append), [GOV.06](lanes/governance.md#task-gov-06) (append), [GOV.12](lanes/governance.md#task-gov-12) (append), [GOV.13](lanes/governance.md#task-gov-13) (append), [GOV.14](lanes/governance.md#task-gov-14) (append), [GOV.18](lanes/governance.md#task-gov-18) (append), [GOV.20](lanes/governance.md#task-gov-20) (append), [GOV.21](lanes/governance.md#task-gov-21) (append), [FND.01](lanes/foundation.md#task-fnd-01) (append), [FND.02](lanes/foundation.md#task-fnd-02) (append), [FND.03](lanes/foundation.md#task-fnd-03) (append), [FND.04](lanes/foundation.md#task-fnd-04) (append), [FND.05](lanes/foundation.md#task-fnd-05) (append), [FND.06](lanes/foundation.md#task-fnd-06) (append), [FND.07](lanes/foundation.md#task-fnd-07) (append), [PRF.04](lanes/runtime-proofs.md#task-prf-04) (append), [PRF.05](lanes/runtime-proofs.md#task-prf-05) (append), [PRF.06](lanes/runtime-proofs.md#task-prf-06) (append), [PRF.09](lanes/runtime-proofs.md#task-prf-09) (append), [PLT.03](lanes/platform.md#task-plt-03) (append), [PLT.09](lanes/platform.md#task-plt-09) (append), [PLT.16](lanes/platform.md#task-plt-16) (append), [PLT.19](lanes/platform.md#task-plt-19) (append), [PLT.20](lanes/platform.md#task-plt-20) (append), [PLT.23](lanes/platform.md#task-plt-23) (append), [PLT.24](lanes/platform.md#task-plt-24) (append), [PLT.25](lanes/platform.md#task-plt-25) (append), [PLT.27](lanes/platform.md#task-plt-27) (append), [PLT.28](lanes/platform.md#task-plt-28) (append), [PLT.29](lanes/platform.md#task-plt-29) (append), [PLT.30](lanes/platform.md#task-plt-30) (append), [PLT.31](lanes/platform.md#task-plt-31) (append), [PLT.33](lanes/platform.md#task-plt-33) (append), [PLT.37](lanes/platform.md#task-plt-37) (append), [PLT.38](lanes/platform.md#task-plt-38) (append), [PLT.39](lanes/platform.md#task-plt-39) (append), [PLT.40](lanes/platform.md#task-plt-40) (append), [PLT.44](lanes/platform.md#task-plt-44) (append), [PLT.45](lanes/platform.md#task-plt-45) (append), [PLT.48](lanes/platform.md#task-plt-48) (append), [PLT.51](lanes/platform.md#task-plt-51) (append), [PLT.52](lanes/platform.md#task-plt-52) (append), [PLT.53](lanes/platform.md#task-plt-53) (append), [PLT.57](lanes/platform.md#task-plt-57) (append), [NAT.03](lanes/native.md#task-nat-03) (append), [NAT.06](lanes/native.md#task-nat-06) (append), [NAT.14](lanes/native.md#task-nat-14) (append), [NAT.15](lanes/native.md#task-nat-15) (append), [APP.01](lanes/app-composition.md#task-app-01) (append), [APP.08](lanes/app-composition.md#task-app-08) (append), [AST.09](lanes/assistant.md#task-ast-09) (append), [AST.17](lanes/assistant.md#task-ast-17) (append), [AST.18](lanes/assistant.md#task-ast-18) (append), [EXE.09](lanes/execution.md#task-exe-09) (append), [CLOUD.38](lanes/cloud.md#task-cloud-38) (append), [EXT.02](lanes/extensions.md#task-ext-02) (append), [UPD.06](lanes/updater.md#task-upd-06) (append) |
| [RES-mobile-build-config](#res-mobile-build-config) | file | Mobile integration owner | [GOV.12](lanes/governance.md#task-gov-12) (append), [AND.01](lanes/android.md#task-and-01) (append), [AND.02](lanes/android.md#task-and-02) (exclusive), [AND.03](lanes/android.md#task-and-03) (append), [AND.04](lanes/android.md#task-and-04) (append), [AND.05](lanes/android.md#task-and-05) (append), [AND.12](lanes/android.md#task-and-12) (append), [AND.14](lanes/android.md#task-and-14) (append), [AND.18](lanes/android.md#task-and-18) (append), [AND.20](lanes/android.md#task-and-20) (append) |
| [RES-private-configuration](#res-private-configuration) | registry | Policy integration owner (Cloud) | [SRCH.06](lanes/search.md#task-srch-06) (append), [SRCH.90](lanes/search.md#task-srch-90) (append), [AIR.00](lanes/ai-routing.md#task-air-00) (append), [AIR.01](lanes/ai-routing.md#task-air-01) (append), [AIR.03](lanes/ai-routing.md#task-air-03) (append) |
| [RES-product-solutions](#res-product-solutions) | file | ArcScope integration owner | [GOV.07](lanes/governance.md#task-gov-07) (append), [PRF.02](lanes/runtime-proofs.md#task-prf-02) (append), [SCOPE.02](lanes/arcscope.md#task-scope-02) (append) |
| [RES-production-release-trust](#res-production-release-trust) | key | Release Engineering Owner | [REL.02](lanes/release.md#task-rel-02) (append), [REL.10](lanes/release.md#task-rel-10) (append) |
| [RES-shared-transaction-families](#res-shared-transaction-families) | registry | Architecture Owner | [CLOUD.06](lanes/cloud.md#task-cloud-06) (append), [CLOUD.11](lanes/cloud.md#task-cloud-11) (append), [CLOUD.13](lanes/cloud.md#task-cloud-13) (append), [CLOUD.42](lanes/cloud.md#task-cloud-42) (append), [CLOUD.53](lanes/cloud.md#task-cloud-53) (append) |
| [RES-web-app-routing](#res-web-app-routing) | registry | Web integration owner | [OPS.05](lanes/operations.md#task-ops-05) (append), [OPS.11](lanes/operations.md#task-ops-11) (append), [WEB.07](lanes/web.md#task-web-07) (append), [WEB.10](lanes/web.md#task-web-10) (append), [WEB.16](lanes/web.md#task-web-16) (append), [WEB.19](lanes/web.md#task-web-19) (append) |
| [RES-web-build-config](#res-web-build-config) | file | Web integration owner | [GOV.11](lanes/governance.md#task-gov-11) (append), [PRF.08](lanes/runtime-proofs.md#task-prf-08) (append), [WEB.03](lanes/web.md#task-web-03) (append), [WEB.07](lanes/web.md#task-web-07) (append), [WEB.10](lanes/web.md#task-web-10) (append), [WEB.16](lanes/web.md#task-web-16) (append), [WEB.19](lanes/web.md#task-web-19) (append), [WEB.25](lanes/web.md#task-web-25) (append) |
| [RES-web-shared-ui](#res-web-shared-ui) | file | Web integration owner | [WEB.08](lanes/web.md#task-web-08) (append), [WEB.10](lanes/web.md#task-web-10) (append), [WEB.19](lanes/web.md#task-web-19) (append) |
| [RES-workstation-build-slot](#res-workstation-build-slot) | build-slot | each workstation operator | [GOV.17](lanes/governance.md#task-gov-17) (exclusive), [PRF.02](lanes/runtime-proofs.md#task-prf-02) (exclusive), [PRF.04](lanes/runtime-proofs.md#task-prf-04) (exclusive), [PRF.05](lanes/runtime-proofs.md#task-prf-05) (exclusive), [PRF.06](lanes/runtime-proofs.md#task-prf-06) (exclusive), [PRF.07](lanes/runtime-proofs.md#task-prf-07) (exclusive), [PRF.10](lanes/runtime-proofs.md#task-prf-10) (exclusive), [NAT.06](lanes/native.md#task-nat-06) (exclusive), [NAT.11](lanes/native.md#task-nat-11) (exclusive), [NAT.13](lanes/native.md#task-nat-13) (exclusive), [NAT.14](lanes/native.md#task-nat-14) (exclusive), [NAT.15](lanes/native.md#task-nat-15) (exclusive), [NAT.22](lanes/native.md#task-nat-22) (exclusive), [NAT.24](lanes/native.md#task-nat-24) (exclusive), [NAT.25](lanes/native.md#task-nat-25) (exclusive) |

<a id="res-ai-workflow-and-routes"></a>

### RES-ai-workflow-and-routes — AI Workflow entry, provider adapters and model route-pin table

Repository: AI · Kind: file · Owner: AI integration owner

**Protocol.** The Workflow entry is owned by the turn-loop task; other Harness tasks add steps through their own modules; the route-pin table changes only with a policy snapshot. Any task that runs against the AI deployment environment holds the lease `leases/res-ai-workflow-and-routes` for that live run only.

<a id="res-android-signing-and-store"></a>

### RES-android-signing-and-store — Android permanent signing identity and store listings

Repository: multiple · Kind: key · Owner: Release Engineering Owner

**Protocol.** Used only by release tasks through protected CI environments; no task creates replacement keys or listings.

<a id="res-architecture-tests"></a>

### RES-architecture-tests — Per-repository architecture and policy test suites

Repository: multiple · Kind: file · Owner: each repository integration owner

**Protocol.** Each repository policy task owns its suite; rule additions are append-only.

<a id="res-arcscope-format-fixtures"></a>

### RES-arcscope-format-fixtures — ArcScope format fixtures

Repository: ArcScope · Kind: file · Owner: ArcScope integration owner

**Protocol.** Fixtures are added per task under its own subdirectory; manifests are append-only.

<a id="res-arcscope-migrations"></a>

### RES-arcscope-migrations — ArcScope store migration sequence

Repository: ArcScope · Kind: sequence · Owner: ArcScope integration owner

**Protocol.** Numbered migrations are allocated at merge by the integration owner (a rebase renumbers pending migrations); each migration is forward-only with its recovery and downgrade-refusal tests; no task edits a merged migration.

<a id="res-assistant-store-schema"></a>

### RES-assistant-store-schema — Assistant SQLite schema and migration sequence

Repository: DesktopPlatform · Kind: sequence · Owner: DesktopPlatform integration owner

**Protocol.** Numbered migrations are allocated at merge by the integration owner (a rebase renumbers pending migrations); each migration is forward-only with its recovery and downgrade-refusal tests; no task edits a merged migration.

<a id="res-cloud-d1-migrations"></a>

### RES-cloud-d1-migrations — Cloud D1 global migration sequence

Repository: Cloud · Kind: sequence · Owner: Cloud integration owner

**Protocol.** One global D1 migration sequence: each module task authors migrations under its module prefix; the integration owner assigns the global sequence number at merge, regenerates the plan manifest and rejects edits to merged migrations; the migrator applies in sequence with receipts.

<a id="res-cloud-deployment"></a>

### RES-cloud-deployment — Cloud container image, Worker bindings and deployment environments

Repository: Cloud · Kind: environment · Owner: Cloud integration owner

**Protocol.** Bindings are added by the owning module task in its own section, and the Cloud integration owner resolves ordering conflicts at merge. Any task that runs against the deployed test environment holds the lease `leases/res-cloud-deployment` for that live run only, whatever mode it declares for its binding edits; production deployment belongs to release tasks.

<a id="res-cloud-host-composition"></a>

### RES-cloud-host-composition — Cloud host module registration and route mapping

Repository: Cloud · Kind: registry · Owner: Cloud integration owner

**Protocol.** Each module registers through its own module entry point and route fragment; the host composition only lists modules; route and binding conflicts are resolved by the integration owner at merge.

<a id="res-cloud-leased-singletons"></a>

### RES-cloud-leased-singletons — Leased Cloud singletons and object namespaces

Repository: Cloud · Kind: registry · Owner: Cloud integration owner

**Protocol.** Each publication watermark, Durable Object alarm namespace and R2 prefix has exactly one owning module task; others use its published port; names are reserved in the binding plan before first use.

<a id="res-cloud-runbooks-and-fixtures"></a>

### RES-cloud-runbooks-and-fixtures — Cloud runbooks, monitoring and provider fixtures

Repository: Cloud · Kind: file · Owner: Operations Owner

**Protocol.** One file per runbook, monitor or provider fixture; indexes are append-only; recorded provider fixtures stay test-only.

<a id="res-cloud-storage-plans"></a>

### RES-cloud-storage-plans — Cloud storage plans and plan-manifest hash

Repository: Cloud · Kind: registry · Owner: Cloud integration owner

**Protocol.** Each module owns its own plan directory; the plan-manifest hash is regenerated by the author after rebase and checked in CI.

<a id="res-contract-consumer-pins"></a>

### RES-contract-consumer-pins — Contracts package pins in consumer repositories

Repository: multiple · Kind: pointer · Owner: each consumer repository integration owner

**Protocol.** A consumer task updates the pin it needs through a reviewed dependency change to the exact published candidate containing its closure; no consumer pins an unpublished closure or references Contracts source.

<a id="res-contracts-dokka-profile"></a>

### RES-contracts-dokka-profile — Contracts Dokka active profile pointer and immutable profile/resource successors

Repository: Contracts · Kind: pointer · Owner: Contracts integration owner

**Protocol.** Tasks may prepare source work in parallel. Only on entering its Dokka phase, a task rebases on latest Contracts main and claims this resource exclusively; inspect merged active PROFILE/immutable profile-resource pairs and every live claim/PR durable handoff reservation. If any earlier unmerged reservation exists, immediately release the lease and defer only Dokka work; do not block other preparation or review. With no prior reservation, allocate exactly N=active revision+1 only if both eng/provenance/artifact-profiles/dokka-2-2-0-rN.json and eng/provenance/records/dokka-documentation-resources-rN.json are unoccupied; do not skip, reuse, or prewrite. Update only task-owned generated Kotlin input hashes and exact API page/hash sets for explicitly listed modules, write the matching immutable resource record, preserve all fixed/excluded entries/history, advance only PROFILE to that same successor, push the exact branch head and durably record {resource,rN,exact head/PR} in the claim/PR handoff. Then release the lease before waiting on review or CI. No later task may allocate while that reservation is live; only its merge/release/supersession frees the next number. The integration owner serially merges the exact reviewed head. Any rebase/change requires reclaiming the lease, revalidating the active pointer and N, regenerating, updating the durable reservation and releasing; prior review is invalidated. Candidate pack/check must accept the exact active pointer and immutable history.

<a id="res-contracts-generated-baseline"></a>

### RES-contracts-generated-baseline — Contracts generated sources and descriptor baselines

Repository: Contracts · Kind: file · Owner: Contracts integration owner

**Protocol.** Never hand-edited or hand-merged: after rebasing, the author regenerates with the pinned generator and commits the result; CI rejects drift between schemas, descriptors and generated output.

<a id="res-contracts-publication"></a>

### RES-contracts-publication — Contracts NuGet, npm and Maven publication

Repository: Contracts · Kind: pointer · Owner: Contracts integration owner

**Protocol.** Every merge to main publishes all Contracts packages at one allocated candidate version (Maven main as SNAPSHOT under the publication-channel profile); the integration owner keeps a single merge queue so publications stay ordered; no tag, republication or replacement version is created for verification.

<a id="res-contracts-schema-sources"></a>

### RES-contracts-schema-sources — Contracts schema sources and registries

Repository: Contracts · Kind: registry · Owner: Contracts integration owner

**Protocol.** Each schema closure task edits only its own domain proto or HTTP-schema files and adds its own sharded constraint and fixture files. Schema-closure tasks and Contracts policy tasks that touch package/access/provenance/dependency input registries share this append/rebase protocol: append only task-owned rows and successor receipts to package, compiled access/hash, foundation, operation, constraint, provenance source/output, binding, and dependency-review inventories; preserve prior history and never rewrite another task's rows. Refresh dependency input hashes only for the task-owned closure; do not expand dependency versions or closure except for the two exact task-specific exceptions below. One narrow exception applies only to CON.14: it may add the single ArcForges.Contracts.CloudInternal → existing ArcForges.Contracts.PublicApi package/project edge required for generated OperatorService imports to resolve to their canonical owner, implemented only by one ProjectReference in the CloudInternal csproj, its existing packages.lock.json, and the CloudInternal dependency row in eng/contract-packages.json. This expands only CloudInternal's package-specific closure to include the existing PublicApi package and its existing same-version transitive realization; the lock may add the PublicApi project and already-pinned Grpc.Core.Api 2.84.0, while existing Foundation and Google.Protobuf 3.36.1 entries retain their versions and hashes. The exception permits only the matching exact input-hash refreshes and immutable con-14-r1 successor chained from active con-22-r1. Preserve the aggregate dependency coordinate/version set, package IDs and licences, every other package's dependency usage/closure, Foundation/PublicApi ownership, all prior receipt history, and the PublicApi 1.0.0-ci.113.1 PreviousClient-only fixture classification. A second, CON.11-only exception permits only the already-authorized Events → PublicApi and CloudInternal → Events/PublicApi project references to realize in Events and CloudInternal as the corresponding first-party Project lock entries plus the exact centrally pinned Grpc.Core.Api CentralTransitive row: requested [2.84.0, ), resolved 2.84.0, contentHash p2SOMl6q/GZ4/5MLkgboC/z55g4zKUEruRn/g46QgppjQBVnsLZVBU/9VO7n60ll38G3Eo8Zu9b7x+W01GKFVg==. Only the five existing consumer lockfiles tests/StructureTests/packages.lock.json, tests/public/SerializationProbe/packages.lock.json, src/public/dotnet/ArcForges.Sdk.Client/packages.lock.json, src/public/dotnet/ArcForges.Cli/packages.lock.json, and src/public/dotnet/ArcForges.Contracts.Validation/packages.lock.json may add ArcForges.Contracts.PublicApi [1.0.0-ci.0.0, ) to the existing ArcForges.Contracts.Events Project.dependencies field, exactly as SDK restore requires. In only tests/StructureTests/packages.lock.json and tests/public/SerializationProbe/packages.lock.json, SDK restore may also add ArcForges.Contracts.Events and ArcForges.Contracts.PublicApi [1.0.0-ci.0.0, ) to the existing ArcForges.Contracts.CloudInternal Project.dependencies field, exactly as the already-authorized CloudInternal -> Events/PublicApi project references require; no other field, package/project entry, project dependency, target framework, version, hash, or consumer behavior changes. This exception permits only these matching task-owned lock/policy input-hash refreshes and the immutable con-11-r1 successor, and preserves the aggregate coordinate/version/licence union, all other package usage/closures, existing Foundation, Google.Protobuf and Microsoft.NET.ILLink.Tasks rows, previous receipt history, package identities and the PreviousClient-only fixture classification. No direct package reference, PrivateAssets or asset override, other coordinate/version/hash, project, lock row, licence exception or dependency algorithm change is authorized; all other tasks retain the no-closure-expansion rule. Public Kotlin/Dokka successors are exclusively governed by RES-contracts-dokka-profile. A proto file with several contributing tasks (operator, policy/configuration) has one designated author task and the others request changes through it. Each serialized merge is followed by a rebase and regeneration before integration of the next task.

<a id="res-design-evidence"></a>

### RES-design-evidence — Design assurance and reference-coverage records

Repository: Design · Kind: file · Owner: Design integration owner

**Protocol.** Receipts and gate records are separate files per task or gate; indexes are appended; historical records are not rewritten.

<a id="res-desktopplatform-build-config"></a>

### RES-desktopplatform-build-config — DesktopPlatform solution, central packages, version sources and CI

Repository: DesktopPlatform · Kind: file · Owner: DesktopPlatform integration owner

**Protocol.** Solution/project lists, central package versions and CI job lists are appended by the task that adds a project, dependency or job; dependency additions follow the dependency-admission policy with a reviewed receipt; lock files are regenerated after rebase and never hand-merged; the integration owner resolves ordering conflicts at merge.

<a id="res-desktopplatform-fixtures"></a>

### RES-desktopplatform-fixtures — DesktopPlatform golden format fixtures

Repository: DesktopPlatform · Kind: file · Owner: DesktopPlatform integration owner

**Protocol.** Fixtures are added per task in their own directory; golden files are never regenerated to make a test pass.

<a id="res-desktopplatform-native-build"></a>

### RES-desktopplatform-native-build — DesktopPlatform native toolchain, vcpkg baseline and native workflows

Repository: DesktopPlatform · Kind: registry · Owner: DesktopPlatform integration owner

**Protocol.** The vcpkg baseline and overlay ports change only through a dependency-admission change with licence and provenance receipts; each native family adds its own CMake targets and workflow entries; triplet or port changes are rebased and rebuilt by their author; CPU-heavy native builds use the workstation build slot. PLT.39 may append only a narrowly scoped transport compatibility change to eng/native_provenance.py and offline tests in tests/tooling/test_native_provenance.py: after the verified cache-hit path, pass urllib.request.Request(url, headers={"User-Agent": "ArcForges/1.0 (+https://github.com/ArcForges/DesktopPlatform)"}) only when the complete requested URL equals https://visualstudio.microsoft.com/wp-content/uploads/2025/10/Visual_Studio_2026-License-Community_ENU.docx or https://visualstudio.microsoft.com/wp-content/uploads/2025/10/Visual-C-V14-License-Redistributable_and_Runtime_ENU.docx; preserve all other URL behavior, pinned URLs/hashes, TLS, timeout, redirects, cache, digest verification, temporary cleanup and atomic promotion, with no retries, dependency, workflow or runner changes. The DesktopPlatform integration owner serializes this shared helper append.

<a id="res-desktopplatform-package-inventory"></a>

### RES-desktopplatform-package-inventory — DesktopPlatform package inventory and lockstep NuGet publication

Repository: DesktopPlatform · Kind: pointer · Owner: DesktopPlatform integration owner

**Protocol.** Each producer task adds its own package entry; every merge to main packs and publishes all packages at one version; consumers pin the candidate produced by the merge of the capability they need, never waiting for a package closure task; one merge queue.

<a id="res-desktopplatform-policy-data"></a>

### RES-desktopplatform-policy-data — DesktopPlatform policy data, reason codes, architecture tests and traceability evidence

Repository: DesktopPlatform · Kind: registry · Owner: DesktopPlatform integration owner

**Protocol.** Generated policy data is regenerated from its pinned source and never hand-edited; the reason-code registry is append-only with stable codes; each task adds its own test classes and evidence rows.

<a id="res-mobile-build-config"></a>

### RES-mobile-build-config — Mobile Gradle modules, version catalog, locks and policy data

Repository: Mobile · Kind: file · Owner: Mobile integration owner

**Protocol.** The module skeleton task registers all modules once and holds the lease `leases/res-mobile-build-config` while it restructures the build; later tasks edit only their module; catalog entries are appended and locks regenerated after rebase; dependency additions carry admission receipts.

<a id="res-private-configuration"></a>

### RES-private-configuration — Private configuration.v1 signed bundle

Repository: Cloud · Kind: registry · Owner: Policy integration owner (Cloud)

**Protocol.** Each owning task adds its own configuration section; activation is a signed publication by the policy lane; no task edits another section.

<a id="res-product-solutions"></a>

### RES-product-solutions — ArcScope solution and central package files

Repository: ArcScope · Kind: file · Owner: ArcScope integration owner

**Protocol.** Solution/project lists, central package versions and CI job lists are appended by the task that adds a project, dependency or job; dependency additions follow the dependency-admission policy with a reviewed receipt; lock files are regenerated after rebase and never hand-merged; the integration owner resolves ordering conflicts at merge.

<a id="res-production-release-trust"></a>

### RES-production-release-trust — Production update feeds, code-signing keys and store pointers

Repository: multiple · Kind: key · Owner: Release Engineering Owner

**Protocol.** Changed only by release tasks, once per promoted candidate; test-signed feeds and fixture roots stay separate from production.

<a id="res-shared-transaction-families"></a>

### RES-shared-transaction-families — Shared transaction-family participant list

Repository: Design · Kind: registry · Owner: Architecture Owner

**Protocol.** Adding a participant to a shared atomic family is a design change through the Architecture Owner; module tasks implement only their declared participation.

<a id="res-web-app-routing"></a>

### RES-web-app-routing — Web profile selector, route registration and per-origin edge configuration

Repository: Web · Kind: registry · Owner: Web integration owner

**Protocol.** The application shell task owns root route registration; each surface adds its own route module and per-origin edge directory.

<a id="res-web-build-config"></a>

### RES-web-build-config — Web workspaces, lock file, CI and performance budgets

Repository: Web · Kind: file · Owner: Web integration owner

**Protocol.** Solution/project lists, central package versions and CI job lists are appended by the task that adds a project, dependency or job; dependency additions follow the dependency-admission policy with a reviewed receipt; lock files are regenerated after rebase and never hand-merged; the integration owner resolves ordering conflicts at merge.

<a id="res-web-shared-ui"></a>

### RES-web-shared-ui — Web shared consumer design system

Repository: Web · Kind: file · Owner: Web integration owner

**Protocol.** The design-system task owns the shared UI package; surfaces request components through it; additions after it are additive.

<a id="res-workstation-build-slot"></a>

### RES-workstation-build-slot — CPU-heavy local build and test slot

Repository: workstation · Kind: build-slot · Owner: each workstation operator

**Protocol.** Exclusive per workstation for the duration of each CPU-heavy local build or test, through the workstation lock rather than a Plan lease: run the command as `python tools/delivery.py build-slot run --worker <name> --task <task> -- <command>` with the Plan repository tool, which holds the lock directory `.arcforges/build-slot` in the user profile with an owner record and heartbeat and recovers a lock whose holder stopped. Coding and review continue while a build waits; CI capacity is not limited by this rule.
