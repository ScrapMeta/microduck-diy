# `_archive/governance/` · 停用的治理层（2026-09-19）

> **为什么停用**：治理有 **3 份副本** —— `AGENTS.md` / `governance/agent-governance.md` / `.cursor/rules/*.mdc`，
> 同一套规则写三遍 → 改一处要动三处 = 漂移。改造后收敛为 **单文件规则 ＋ 角色技能 ＋ 两台 linter**：
>
> | 旧 | 新 |
> |---|---|
> | `agent-governance.md`（219 行）· 通用模板（135 行） | 规则收进 [`AGENTS.md`](../../../AGENTS.md)（≤100 行） |
> | `.cursor/rules/*.mdc`（6 个 rule） | `.cursor/skills/<role>/SKILL.md`（4 个角色手册，**能自己进化**） |
> | `upstreams.lock` · `refresh-upstreams.ps1` | `scripts/` —— 它们是**工具**，不是规则 |
> | GitHub Issue 路由 / 标签 / 关单门禁 | `wiki/tasks.md` 台账；历史 Issue 冻结保留只读 |
> | `wiki/SCHEMA.md` | 规范拆开：frontmatter / 行数 / `raw/` 只读 → `AGENTS.md`，由 `scripts/wiki_lint.py` **机械执行**；领域 / 优先级 / 标签表 → `wiki/index.md` |
>
> **本目录保留只读，不删** —— `wiki/log.md` 与历史 Issue 里有指向这些路径的引用。

| 文件 | 原位置 |
|---|---|
| `agent-governance.md` | `governance/agent-governance.md`（v0.12 · §1–§12） |
| `agent-governance-generic.md` | `governance/templates/`（通用模板 G5） |
| `rule-microduck-pm-agent.mdc` | `.cursor/rules/` |
| `rule-microduck-software-agent.mdc` | `.cursor/rules/` |
| `rule-microduck-hardware-agent.mdc` | `.cursor/rules/` |
| `rule-microduck-structure-agent.mdc` | `.cursor/rules/` |
| `rule-microduck-train-agent.mdc` | `.cursor/rules/` —— 职能已并入 `/microduck-software` |
| `rule-microduck-ros2.mdc` | `.cursor/rules/` —— 附件已并入 `/microduck-software` 手册 |

相关：[`_archive/README.md`](../README.md) · [`AGENTS.md`](../../../AGENTS.md)
