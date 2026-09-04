下面就是 **ArcForges Stage 0–28 的最简总览**，每一阶段只说“它到底负责什么”。

## 一、Stage 0–12：先把商业平台建立起来

| Stage  | 阶段                                            | 核心职责                                                                                |
| ------ | --------------------------------------------- | ----------------------------------------------------------------------------------- |
| **0**  | **Portfolio / Product / Business Foundation** | 定义 ArcForges 整体产品组合、商业模式、Local-first + 开源 + 付费 Cloud 的总定位。                          |
| **1**  | **Identity / Account / Workspace**            | 定义账号、Workspace、Device、Session、Installation，以及登录/本地匿名使用和 Official/Self-host Realm。   |
| **2**  | **Website / Marketing / Product Surfaces**    | 定义官网、产品介绍页、下载入口、账号入口等对外产品门户。                                                        |
| **3**  | **Billing / Payment**                         | 定义付款、订阅购买、续费、退款等商业支付体系。                                                             |
| **4**  | **Entitlement**                               | 定义“用户买了什么、因此有资格使用什么”，严格独立于 Feature Flag 和权限系统。                                      |
| **5**  | **Distribution / Release / Update**           | 定义四个 App 独立安装、版本、发布渠道、更新、回滚、安装包和镜像分发。                                               |
| **6**  | **ArcChat Platform Direction**                | 冻结 ArcChat 的平台角色：Chat + Agent + Task Center + Automation + Capability Hub + 本地 Hub。 |
| **7**  | **Cloud / Mobile / Web**                      | 定义 Cloud 的职责，以及 ArcChat Mobile/Web 作为 Companion，而不是完整专业 App。                        |
| **8**  | **AI Economics / Provider / Cost**            | 定义 AI Provider、Model、BYOK、Managed AI、Credits、成本和商业计费关系。                             |
| **9**  | **Sync / Backup / User Assets**               | 定义 Local-first Sync、Cloud Replica、Blob、Backup、资产上传策略和多设备恢复。                         |
| **10** | **Cloud Production Infrastructure**           | 定义 Azure/Cloudflare、生产部署、安全基础设施、可观测性和运营基础。                                          |
| **11** | **Legal / Open Source**                       | 定义 AGPL、隐私、法律、第三方许可证和开源治理。                                                          |
| **12** | **Growth / Community / Product UX Direction** | 定义增长、社区、生态发现、产品间推荐和“Standalone excellent, together better”的产品方向。                    |

---

# 二、Stage 13–20：把四个真正的产品完整定义出来

| Stage  | 阶段                                                                     | 核心职责                                                                                                             |
| ------ | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **13** | **Product Topology & Architecture Baseline Freeze**                    | 最终冻结 ArcChat / ArcNotes / ArcScope / ArcSlate 四个产品、数据所有权、依赖方向、Hub边界和技术例外。                                        |
| **14** | **Shared Desktop Product Experience Foundation**                       | 定义四个Desktop App共同的 Design System、Command、Shortcut、Settings、窗口、通知、错误、Deep Link、Drag & Drop、多窗口等体验规范。              |
| **15** | **ArcNotes Complete Product Specification**                            | 完整定义 ArcNotes：Notebook、Document、Block、Editor、Link、Tag、Property、附件、History、Search、AI、Knowledge等。                  |
| **16** | **ArcScope Complete Product Specification**                            | 完整定义 ArcScope：Device/Data Source、Connection、Session、Capture、Signal、Trigger、Measurement、Analysis、Decoder、Report等。 |
| **17** | **ArcChat Complete Product Specification**                             | 把ArcChat真正产品化：Home、Conversation、Composer、Project、Task Center、Artifacts、Agents、Skills、MCP、Provider、Search等。       |
| **18** | **ArcChat Mobile & Web Companion Specification**                       | 完整定义Mobile/Web Companion：Remote Task、Approval、Steering、Artifact、Notification、Device Presence、Cloud Task和跨设备连续性。  |
| **19** | **Unified Agent Execution / Task / Automation Model**                  | 统一 Intent → Task → Run → Step → Attempt → Capability，以及Pause、Retry、Checkpoint、Approval、Budget、Automation等执行语义。   |
| **20** | **ArcSlate Complete Product Specification & Olive-to-C# Rewrite Plan** | 完整定义ArcSlate专业视频剪辑产品，并确定Olive能力如何保留/改进/舍弃以及C# + Avalonia重写边界。                                                    |

---

# 三、Stage 21–24：让四个产品真正组成一个平台

| Stage  | 阶段                                                              | 核心职责                                                                                                                                          |
| ------ | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **21** | **Cross-App Semantic Capability & Resource Model**              | 统一跨App业务语言：App、Instance、Capability、Action、Context、Artifact、ResourceRef、Deep Link、Event、Health、Invocation、Compatibility。                       |
| **22** | **Local Data / Project Format / Interoperability Architecture** | 定义本地Canonical Data、DB/File/Hybrid、Project Format、Autosave、Undo/Revision、Recovery、Migration、Import/Export、Git友好和Portability。                   |
| **23** | **Knowledge / Search / Retrieval Architecture**                 | 定义Knowledge Source、Local/Cloud Index、Keyword/Semantic/Hybrid Search、AI Retrieval Scope、Evidence、Citation、Exclude from AI以及ArcNotes/ArcChat职责。 |
| **24** | **Extension / Integration / Developer Platform**                | 统一Skill、Template、Workflow、MCP、Connector、External Agent、Extension、第三方App、SDK、CLI、Package、Catalog、Publisher、Trust与Compatibility。                |

---

# 四、Stage 25–27：让平台能够长期安全稳定演进

| Stage  | 阶段                                                       | 核心职责                                                                                                                               |
| ------ | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **25** | **Dynamic Configuration & Product Policy Control Plane** | 统一Feature Flag、Rollout、Kill Switch、Remote Config、Minimum Version、Provider/Model Availability和Experiment，严格区别于Settings和Entitlement。 |
| **26** | **Product Security / Permission / Trust Closure**        | 统一Human/Agent/Automation Actor、Permission、Approval、Risk R0–R4、Secret、Data Egress、Remote权限、Extension Trust和Audit。                   |
| **27** | **Product Quality & Compatibility Contract**             | 把性能、内存、启动、AOT、Accessibility、Localization、Units、版本兼容、Migration、Recovery、Diagnostics和跨平台测试变成Release硬合同。                              |

---

# 五、Stage 28：解决产品真正运营以后“出事怎么办”

| Stage  | 阶段                                                            | 核心职责                                                                                                                                                        |
| ------ | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **28** | **Support / Feedback / Operator / Trust & Safety Operations** | 定义Bug/Feature Feedback、Private Support、Diagnostic Bundle、数据恢复、Operator权限边界、禁止Impersonation、社区举报、恶意Package、Copyright/Abuse、Removal、Appeal和Security Advisory。 |

---

# 最后可以把 0–28 记成这五句话

### **0–12：商业平台怎么成立**

账号、Cloud、付费、同步、基础设施、法律、增长。

### **13–20：四个产品到底是什么**

ArcChat、ArcNotes、ArcScope、ArcSlate，以及共同Desktop体验和Agent运行模型。

### **21–24：四个产品怎么组成一个平台**

跨App语义、数据格式、Knowledge/Search、Extension/Developer生态。

### **25–27：这个平台怎么长期安全稳定地演进**

动态Policy、安全权限、质量与兼容合同。

### **28：真正商业运营以后出问题怎么处理**

Support、Recovery、Operator、Trust & Safety、Security Advisory。

所以整个 **Stage 0–28** 实际已经构成一条非常清楚的闭环：

> **商业成立 → 产品定义 → 平台互联 → 安全稳定演进 → 真实运营兜底。**
