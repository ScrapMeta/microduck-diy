# Microduck 工作区 · Agents

> **治理全文**：[`governance/agent-governance.md`](governance/agent-governance.md)（**仓内，受版本控制**）
> 本文件是**治理入口**：只列不变量；细则与通用模板在 `governance/`。
> **工作区根 `D:\projects\microduck` 就是本仓（`ScrapMeta/microduck-diy`）的工作树**；
> 只读参考克隆收在 `refs/`（已 ignore）。

## 两项启动前提

1. **GitHub 基础工程**：工作区根 → `ScrapMeta/microduck-diy`（Issue / Milestone / PR / Labels）
2. **llm-wiki**：`wiki/`（先读 SCHEMA → index → log；规格真源）

## 不变量

- **真源**：规格认 wiki · 过程认 Issue · 聊天不算。
- **模型**：只常驻 **pm**；software / hardware / structure / train 按 Issue 新建 → 完成即删。
- **主循环**：pm 开 Issue（类型 + 职能标签 + 验收清单）→ 新建职能会话（`@` rule + Issue URL）
  → 只改本领地 → 回写 Issue → 动规格更 wiki **并 push** → `ready-for-pm` → pm 关单 → 删会话。
- **同刻一个会话**：同一职能同时只跑一个 · 越界请 pm 改派，不自行修改。
- **交付物归自有仓**：`refs/` 内只读；产出必须落到自己有 push 权限的仓。
- **本仓禁用 `git clean -x`**：它会删除被 ignore 的 `refs/` —— 一次误操作即抹掉全部参考克隆。

细则（§1–§12）· 通用模板 · 参考克隆版本锁定（`upstreams.lock`）：见 [`governance/`](governance/)。
全树与各目录角色：wiki [[local-workspace-layout]]（**布局真源**，本文件不重复）。
