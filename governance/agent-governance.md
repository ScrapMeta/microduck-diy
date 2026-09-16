# Microduck DIY · Agent 治理方案

> 状态：**v0.11** · 2026-09-16 · 由 **pm** 维护  
> 入口：工作区根 [`AGENTS.md`](../../AGENTS.md)（转发存根）  
> 本文件位置：`microduck-diy/governance/` —— **在基础工程内，受版本控制**
> 目的：人控节奏、Issue 可复查、职能不串台、规格单一真源。  
> **现行：** 两项启动前提 + 只常驻 pm + 四职能按 Issue 启停。

---

## 1. 两项启动前提

### 1.1 GitHub 基础工程（过程真源）

工作区下**指定一个** Git 仓并绑定 GitHub 远程，作为本项目的
**Issue / Milestone / PR / Release / Labels 唯一过程面**。

- 本项目：`microduck-diy/` → `ScrapMeta/microduck-diy`
- 承担：开单、派职能标签、进度评论、`ready-for-pm`、验收关单、里程碑与发版；**不以聊天结案**
- 上游只读克隆、旁路实验仓、临时目录 **不**承担项目管理

### 1.2 基础工程内的 llm-wiki（规格真源）

在基础工程根下建 `wiki/`，完全遵循 llm-wiki。

- 本项目：`microduck-diy/wiki/` —— 会话先读 `SCHEMA.md` → `index.md` → `log.md`
- 最低结构：`SCHEMA.md` · `index.md` · `log.md` · `raw/` · Layer-2（以 SCHEMA 为准）
- 约定：更新 bump `updated` · 入 `index` · **追加** `log`；`raw/` 正文只增不改
- **回写 wiki 必须在同一会话内 `push` 到远端**——只改本地不算真源更新
- 规格冲突先改 wiki

### 1.3 三处定位

| 路径 | 角色 |
|------|------|
| `microduck-diy/` | **基础工程**：项目管理 + 工程代码 + wiki + 治理 |
| `microduck-diy/governance/` | 治理细则与通用模板（**受版本控制**） |
| 工作区根 `AGENTS.md` | 转发存根：只列不变量 + 指向本文件（工作区根不是仓库） |
| 其余目录 | 上游只读引用 / 自有兄弟仓 / 本地临时，非真源 |

**关键原则：交付物必须落在自有 push 权限的仓里。** 上游克隆只读——
不在其中留未提交改动，不把别人的仓当交付物仓库（详见 §11）。

全树见 wiki [[local-workspace-layout]]。

未满足 1.1 + 1.2：**不得**按本方案派职能 agent。

---

## 2. 真源裁决

| 层 | 真源 | 说明 |
|----|------|------|
| **规格与资料** | 基础工程 `wiki/` | 冲突先改 wiki |
| **过程与进度** | 基础工程 GitHub **Issue** | pm 开单、派职能、验收关单 |
| **聊天** | 辅助 | 不当规格、不当关单 |
| **handoff** | **已废止** | 跨域约束写进 Issue 正文/评论；结论进 wiki |

**主循环：**

```text
pm 开 Issue（类型 + 职能标签 + 验收清单）
  → 新建职能会话（@ rule + Issue URL）
  → 执行本领地 → 回写 Issue；动规格则更 wiki 并 push
  → ready-for-pm → pm 审核 → 关单（或改派）→ 删除该职能会话
里程碑：pm 审 Milestone → tag/release；release/qa 另开 Issue（临时会话或 pm 兼）
```

---

## 3. 原则

1. **只常驻 pm**：派单、验收、wiki 收口、跨域改派；默认不写实现。
2. **四职能按需启停**：一个 Issue（或明确一批同职能）→ 一次会话 → 做完即删。
3. **同一职能同刻只允许一个会话**；需要并行 → 拆 Issue 或排队。
4. **规格只认 wiki，过程只认 Issue。**
5. **越界先改派**：pm 转交或新开子 Issue。
6. **专项 rule ≠ 新职能**（ROS2 ⊂ software）。
7. 探索子 agent 更短命，产出落 Issue 或 wiki。

---

## 4. Issue 与标签

### 4.1 标签词表

只此一套；新增标签**先登记本表**再用。

| 标签 | 用途 |
|------|------|
| `task` / `chore` | 类型，二选一 |
| `sw` `hw` `structure` `train` | 执行职能；`task` 必挂其一 |
| `pm` | pm 亲自执行（无职能接管） |
| `bench` | 上机 / 台架验证 |
| `ready-for-pm` | 职能宣告完成、待验收（pm 关单时移除） |

### 4.2 `task`

改契约、跨职能、发板 / 合训练产物、有合并风险等。

- 谁开：默认 **pm**
- 必填：目标 · 不可破约束 · 交付物路径 · 验收清单 · 执行职能
- 正文末行 `assignee-agent: <职能>`（派单指向）
- 跨职能长约束：**全部写在 Issue**（可分节 / 分阶段），必要时拆子 Issue

### 4.3 `chore`

不改规格、不跨职能、不进正式发版闸门。标题 `[chore] …` + 一句话目标 + 路径；
pm 确认无规格漂移后 Close。

### 4.4 里程碑 / 发布

Milestone = 阶段篮子。`release` / `qa` 不设常驻职能。

---

## 5. 职能与领地

| 职能 | 驻留 | 范畴 | 默认可写领地 |
|------|------|------|--------------|
| **pm** | 常驻 | Issue/Milestone · 派单改派 · 验收关单 · wiki 收口 · 发版组织 | `microduck-diy/governance/`（治理）· 工作区根 `AGENTS.md`（存根）· `wiki/` 总述·index·log 收口（各职能写本视角页）· 该仓 Issue/PR/Milestone |
| **software** | 短命 | 固件 · 总线/协议 · 上机脚本 · 系统镜像 | `microduck-diy/imu_to_dxl/` `image/` `scripts/`；ROS2 时 `microduck_ros2/` |
| **hardware** | 短命 | 原理图/PCB · 电气 BOM · 制板接线 | `microduck-diy/imu_to_dxl/hardware/`（板设计）· 订单资产 · wiki 电气页 |
| **structure** | 短命 | 打印件 · 装配 · 机械 BOM | `microduck-diy/cad/`；机械件数 |
| **train** | 短命 | 仿真训练 · 评测 · ONNX 与契约 | 默认只读上游 `microduck_rl/`；产物落 Issue 指定目录 |

- 各职能**只改本行领地**；越界 → 请 **pm** 改派（新开会话），不自行修改
- 本工作区职能**只此 5 个**；BOM / release / qa / ROS2 均不单设
- pm 不直接改 PCB/固件/训练/CAD 实现（除非用户明确代劳）
- **领地只含自有仓**：上游克隆（`elec_RPI_Robot_HAT/` `microduck-replica/` `OpenRB-150/` 等）
  仅作参考；在其中产生的交付物必须**导出到自有仓**（§11）

**职能公共流程：** 新建会话（`@` rule + Issue URL）→ 只改本领地 → 回写 Issue →
动规格更 wiki 并 push → 标 `ready-for-pm` → pm 关单 → **删会话**。

---

## 6. 职能会话生命周期

1. 新聊天；标题 `<职能>|#<Issue>-<短述>`；`@` 本职能 rule；首条 **Issue URL**。
2. 只改本领地；进度写 Issue（**禁止**用聊天摘要代替 Issue）。
3. 规格进 wiki 并 push；标 `ready-for-pm`。
4. pm 验收 / 改派（下一职能另开新会话）。
5. pm 关单并**移除 `ready-for-pm` 标签**，确认删除该职能会话。

---

## 7. Cursor Rule

| Rule | 用途 |
|------|------|
| `microduck-pm-agent.mdc` | 常驻 pm |
| `microduck-software-agent.mdc` | software |
| `microduck-hardware-agent.mdc` | hardware |
| `microduck-structure-agent.mdc` | structure |
| `microduck-train-agent.mdc` | train |
| `microduck-ros2.mdc` | software 的 ROS2 **附件**（非职能，不单独启会话） |

一律 `alwaysApply: false`。
rule 只写**本职能特有条款**（领地 / 禁止 / 边界）；公共流程见 §5，不重复。

---

## 8. 验收（pm）

- **task：** 清单勾完（或 pm **书面写进 Issue** 的豁免项）· 动规格则 wiki 已更**且已 push**
  · 交付路径可开 · 未越界 · 职能会话可删
- **chore：** 范围对 · 有路径 · 无规格漂移 → Close
- **里程碑：** Issue 关闭或书面延期 · 版本写清

---

## 9. 新开同类项目

向执行方（人或 pm agent）提供 §9.1 信息表，按 §9.3 清单落地，即可复制本治理结构。

### 9.1 必填信息

| 字段 | 说明 | 本项目示例 |
|------|------|------------|
| `PROJECT_NAME` | 显示名 | Microduck DIY |
| `PROJECT_SLUG` | 目录/rule 前缀（小写连字符） | `microduck` |
| `WORKSPACE_ROOT` | 本地工作区根 | `D:\projects\microduck` |
| `BASE_REPO_DIR` | 基础工程相对路径 | `microduck-diy` |
| `GITHUB_REPO` | `owner/name` | `ScrapMeta/microduck-diy` |
| `WIKI_DOMAIN` | SCHEMA 一句话领域 | Microduck DIY 复刻知识库 |
| `WIKI_PRIORITY` | 现行优先级若干条 | 机身 IMU → 装机电控 → BOM |
| `ROLES` | 职能列表（默认四职能） | sw / hw / structure / train |
| `ROLE_LANDS` | 各职能默认可写路径 | 见 §5 |

### 9.2 选填

`EXTRA_SKILL_RULES`（专项附件，如 ros2 ⊂ software）· `UPSTREAM_READONLY`（只读上游列表）
· `DEFAULT_MILESTONE` · `LABELS`（额外标签，须登记词表）

### 9.3 Bootstrap 输出物

1. `{{BASE_REPO_DIR}}/` Git 仓 + GitHub 远程 + 默认分支
2. `{{BASE_REPO_DIR}}/wiki/` 完整 llm-wiki 骨架（SCHEMA / index / log / raw / Layer-2）
3. GitHub：labels（`task` `chore` `ready-for-pm` + 职能标签）· 可选首个 Milestone
4. `{{BASE_REPO_DIR}}/governance/`：细则 + 通用模板（**入仓**，不放在工作区根）
5. 工作区根 `AGENTS.md`：仅**转发存根**（不变量 + 指向 4）
6. `.cursor/rules/{{PROJECT_SLUG}}-*-agent.mdc`
7. `{{BASE_REPO_DIR}}/governance/upstreams.lock`：上游克隆清单（若工作区含只读克隆）
8. wiki `log` 首条：治理启用

可复用填空稿：[`templates/agent-governance-generic.md`](templates/agent-governance-generic.md)。

---

## 10. 工作区形态（多仓布局）

**工作区根是纯目录，不是仓、不承担项目管理。** 因为典型工作区里绝大多数目录是
**别人的仓**（上游 / 社区 / 教程），只有基础工程属于自己。

### 10.1 三种目录，三种待遇

| 类型 | 做法 | 禁止 |
|------|------|------|
| **自有仓**（基础工程 + 自有兄弟仓） | 独立 Git 仓 + 自有 GitHub 远端；职能可写可推 | — |
| **上游只读克隆** | 独立克隆，**不进任何仓**、不钉版本 | 留未提交改动 · 把交付物放进去 |
| **本地临时**（`temp/` `vms/` 等） | 无版本控制 | 当规格真源 |

### 10.2 为什么不用子模块

- 上游仓**没有 push 权限**；子模块里一改就是 detached HEAD + 永远提交不出去
- 活跃开发的仓需要频繁提交，子模块会持续制造摩擦
- 参考克隆应当**可随时删除重克隆**，子模块把它变成工作流

**判据：** 活跃开发 → 独立兄弟仓；构建依赖且只需钉版本 → 子模块；只读参考 → 独立克隆。

### 10.3 上游版本靠 lock，不靠子模块

`governance/upstreams.lock` 记录每个克隆的 目录 / remote / 分支 / HEAD / 脏状态 / 落后提交数。
用 `governance/refresh-upstreams.ps1` 重新生成。这样既拿到「钉版本」的好处，
又不必把上游仓纳入本仓。

---

## 11. 交付物归属（硬约束）

> **交付物必须落在自己拥有 push 权限的仓里。**

- 上游克隆只读：在其中做的工作**无法提交、无法推送、无法复审**，等于不可恢复的丢失
- 需要改上游才能出成果时 → 先把**交付物**落到自有仓（或另建自有仓），上游改动只作参考
- 「同物多份」必须定真源：同一设计出现多份副本时，**一份为真源**，其余标注派生或删除
- pm 验收时检查：交付路径是否在自有仓内（§8）

### 11.1 二进制改动的判读（先看大小，再决定要不要细查）

`git diff` 对二进制只给字节数，看不出是设计改动还是工具噪声。按此顺序，**够用即止**：

| 步 | 动作 | 结论 |
|----|------|------|
| 1 | `git diff --stat` 看**文件大小** | **大小变了 → 视为真改动，直接提交** |
| 2 | 大小**完全没变** → 花几秒定性 | zip：比对条目数；SQLite：比对修订计数器 |
| 3 | 仍定性不了，才深挖 | 逐表/逐条目比对；结论写进 wiki |

**已知噪声源（勿提交）：**

- `.eprj2`（EasyEDA Pro SQLite 工程库）：**打开即自增** `project_structures.ticket`，
  而 `structure` 设计正文逐字节不变 → 4 MB 纯计数器位移。判别：`ticket` 变 / `structure` 一致 → `git checkout --`
- 其余 EDA / 切片工具的同类型「修订计数器 / 会话 / 缓存」字段同理

> 判据：**只提交你能说清改了什么的东西**。说不清且大小为 0 变化 → 默认撤销，别把它塞进历史。
> 深挖成本高于收益时，宁可先撤销——需要时工具里随时能重新导出。

---

## 12. 版本与修订

本文件是治理的**唯一版本源**；别处只引用路径，**不写版本号**（避免改一处要动多处）。

变更 → **pm** 同步 `AGENTS.md`（若涉及不变量）+ 本文件 → `microduck-diy/wiki/log.md` 留一条。
版本号只在本文件首行与 `wiki/log.md` 出现。
