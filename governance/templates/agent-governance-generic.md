# 研发型项目 · Agent 治理通用模板

> 版本：**G4** · 快照于 Microduck 治理 **v0.10**（2026-09-16）
> 用法：提供 §3 信息表 → 按 §4 清单落地。
>
> **快照制：** 本模板是某一时刻的副本，**不要求**与各项目细则逐条同步。
> 项目内**以本地细则为准**；模板按需重编，不反向追改。

---

## 1. 核心约定（六条）

1. **两项启动前提**：① 工作区指定**一个** GitHub 基础工程（Issue/Milestone/PR/Labels 唯一过程面）；
   ② 该仓根下建**完全遵循 llm-wiki** 的 `wiki/`（SCHEMA · index · log · raw · Layer-2）。
   缺任一：先 bootstrap，再派职能。
2. **真源分层**：规格与资料 → `wiki/`；过程与进度 → GitHub Issue；聊天 = 辅助。
   跨域约束**写进 Issue**，结论进 wiki（历史 `handoffs/` 已废止，仅存去向索引）。
3. **只常驻 pm**：派单、验收关单、wiki 收口、跨域改派；默认不写实现。
4. **职能短命**：一 Issue（或一批同职能）→ 一次会话 → 做完即删；**同一职能同刻只跑一个**。
5. **越界先改派**：禁止自行修改他域；跨域约束**写进 Issue**，结论进 wiki。
6. **专项 rule ≠ 新职能**：如 ROS2 ⊂ software，作为附件 rule 按需 `@`。

```text
pm 开 Issue（类型 + 职能标签 + 验收清单）
  → 新建职能会话（@ rule + Issue URL）
  → 只改本领地 → 回写 Issue；动规格更 wiki 并 push
  → ready-for-pm → pm 关单（或改派）→ 删除该职能会话
```

**wiki 回写必须在同一会话内 push**——只改本地不算真源更新。

---

## 2. Issue 与标签

- 标签词表**只此一套**，新增先登记：`task`/`chore`（类型，二选一）·
  `sw` `hw` `structure` `train`（执行职能，`task` 必挂其一）·
  `pm`（pm 亲执行）· `bench`（上机/台架）· `ready-for-pm`（待验收，pm 关单时移除）
- **`task`**：目标 · 不可破约束 · 交付物路径 · 验收清单 · 执行职能；
  正文末行 `assignee-agent: <职能>`
- **`chore`**：不改规格、不跨职能；标题 `[chore]`
- Milestone = 阶段篮子；`release`/`qa` 不设常驻职能

---

## 3. 新开项目信息表

### 必填

| 字段 | 你的值 |
|------|--------|
| `PROJECT_NAME` | |
| `PROJECT_SLUG` | 目录 / rule 前缀（小写连字符） |
| `WORKSPACE_ROOT` | |
| `BASE_REPO_DIR` | |
| `GITHUB_REPO` | `owner/name` |
| `WIKI_DOMAIN` | 一句话领域 |
| `WIKI_PRIORITY` | 现行优先级 1… |
| `ROLES` | 默认 pm + sw + hw + structure + train |
| `ROLE_LANDS` | 各职能默认可写路径 |

### 选填

`EXTRA_SKILL_RULES`（专项附件）· `UPSTREAM_READONLY`（只读上游列表）·
`DEFAULT_MILESTONE` · `LABELS`（额外标签，须登记词表）

---

## 4. Bootstrap 清单

- [ ] 建 `{{BASE_REPO_DIR}}`：`git init` / clone + 设 remote `{{GITHUB_REPO}}`
- [ ] 建 `wiki/`：SCHEMA（写入 DOMAIN / PRIORITY / 约定）· index · log · raw/ · Layer-2
- [ ] GitHub labels（**按 §2 词表**）；可选首个 Milestone
- [ ] 建 `{{BASE_REPO_DIR}}/governance/`：细则 + 本模板（**入仓**）
- [ ] 写工作区根 `AGENTS.md`：**仅转发存根**（不变量 + 指向 `governance/`）
- [ ] 写 `.cursor/rules/{{PROJECT_SLUG}}-{pm,software,hardware,structure,train}-agent.mdc`
- [ ] 写 `{{BASE_REPO_DIR}}/governance/upstreams.lock`（工作区含只读克隆时）
- [ ] wiki `log` 首条：治理启用
- [ ] （若有旧 handoffs 目录）清空为去向索引，禁止新建 handoff

**rule 写法：** 只写本职能**特有条款**（领地 / 禁止 / 边界）；
公共流程由细则承载，**不在各 rule 里重复**（避免多副本漂移）。

**归属写法：** 领地**只列自有仓**路径；上游克隆只读，产出必须导出到自有仓。

---

## 5. 工作区形态（多仓）

工作区根是**纯目录**，不是仓、不承担项目管理——因为典型工作区里绝大多数目录是**别人的仓**。

| 类型 | 做法 |
|------|------|
| 自有仓（基础工程 + 自有兄弟仓） | 独立 Git 仓 + 自有远端；职能可写可推 |
| 上游只读克隆 | 独立克隆，**不进任何仓**、不钉版本；禁止留未提交改动 |
| 本地临时 | 无版本控制，非真源 |

**不用子模块**（上游无 push 权限 → detached HEAD，改了提交不出去）。
上游版本用 `governance/upstreams.lock` 记录 remote / 分支 / HEAD / 脏状态。

**硬约束：交付物必须落在自有 push 权限的仓里。**

---

## 附录 A · `AGENTS.md` 骨架

```markdown
# {{PROJECT_NAME}} 工作区 · Agents

> **治理全文**：`{{BASE_REPO_DIR}}/governance/agent-governance.md`
> 本文件是**转发存根**（工作区根不是仓）；细则与模板都在基础工程内。

## 两项启动前提
1. **GitHub 基础工程**：`{{BASE_REPO_DIR}}/` → `{{GITHUB_REPO}}`
2. **llm-wiki**：`{{BASE_REPO_DIR}}/wiki/`（先读 SCHEMA → index → log）

## 不变量
- **真源**：规格认 wiki · 过程认 Issue · 聊天不算。
- **模型**：只常驻 pm；software / hardware / structure / train 按 Issue 新建 → 完成即删。
- **主循环**：pm 开 Issue（类型 + 职能标签 + 验收清单）→ 新建职能会话（@ rule + Issue URL）
  → 只改本领地 → 回写 Issue → 动规格更 wiki **并 push** → ready-for-pm → pm 关单 → 删会话。
- **同刻一个会话**：同一职能同时只跑一个 · 越界请 pm 改派。
- **交付物归自有仓**：上游克隆只读，产出必须落到自有 push 权限的仓。
```

---

## 附录 B · 职能 rule 骨架

```markdown
---
description: {{ROLE}} — {{SCOPE}}; ephemeral per Issue
globs: ["{{GLOB}}"]
alwaysApply: false
---

# {{PROJECT_NAME}} · {{ROLE}}

按 Issue 新建的**短命**职能会话，非常驻。

## 领地（可写）
- {{LAND}}

## 禁止
- {{越界项 → 指向对应职能}}

流程见细则 §5 · §6。中文沟通；标识符英文。
```

---

## 附录 C · llm-wiki SCHEMA 最小头

```markdown
# Wiki Schema（llm-wiki · {{PROJECT_NAME}}）

> Agent 每次先读：本文件 → index.md → log.md

## Domain
{{WIKI_DOMAIN}}

## 现行优先级
{{WIKI_PRIORITY}}

## Conventions
- 文件名英文小写连字符；正文中文为主
- frontmatter；[[wikilinks]]；更新 bump updated；入 index；**追加** log
- 禁止修改 raw/ 正文
- **回写后 push**；只改本地不算更新
```

---

## 修订

模板升 G 版本；各项目由 **pm** 改本地细则并写 wiki log。模板**不反向追改**。
