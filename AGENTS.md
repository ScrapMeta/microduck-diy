# Microduck DIY · 手搓小小鸭

`D:\projects\microduck` **就是** `ScrapMeta/microduck-diy` 仓的工作树。
**规则只有本文件** —— 能力在技能，事实在 wiki；冲突以本文件为准。

## 谁能改什么

| 谁 | 范围 | 怎么算数 |
|---|---|---|
| **中立会话** | 规则与全局（本文件 · wiki 规范 · 跨域改派） | 改完**停下，等 Human 确认** |
| **技能会话** | 自己的领地与手册（`.cursor/skills/<role>/`） | 自进化，报备即可；**扩权须走中立会话** |
| **Human** | 决策与审核（Gate · 破坏性动作 · 验收） | **只有本人能签** |

## 红线（不可协商）

1. **凭据不进 Git / 报告 / 回显。**
2. **`refs/` 只读**；交付物落**自有可推送仓**。
3. **破坏性动作先列范围 ＋ 预检，等确认** —— 覆盖 / 删 · 回滚 · 烧录量产固件 · 制板下单 · 强推 · `git clean -x`。
4. **干完即停** —— 不拍板 · 不建 / 不合并 PR · 不扩范围 · 不顺手改别的。
5. **遇阻就停** —— 信息不足、或该 Human 定的，把问题交回；不猜着往下做。
6. **不代签 Gate** —— 上电 · 剪线 / 改线 · 下单 · 验收。

## 找东西

| 要什么 | 去哪 |
|---|---|
| 欠什么 ＋ 当前版本计划 | `wiki/tasks.md` |
| 改过什么（历史） | `wiki/log.md`（**只追加**） |
| 事实 / 规格 | `wiki/index.md`（导航） |
| 谁干什么活、怎么干 | `.cursor/skills/<role>/SKILL.md` |
| 目录与路径怎么写 | `wiki/concepts/local-workspace-layout.md` |
| wiki 硬规范 | `scripts/wiki_lint.py`（**判定即规格**） |

## 记录

- **干活的那个角色直接写 wiki**，不用逐次问 —— 落点写在自己手册里，格式由 linter 机械把关。
- **台账**（`wiki/tasks.md`）**全员可开 / 更新 / 关**；`T-nn` 不复用 · 开 ＋ 关同页 ——
  细则在该页「**通用约定**」（可整段移植到别的工程）。
- **push `main` 与 Issue 归档只有 pm** —— 细则在 `.cursor/skills/microduck-pm/SKILL.md`。

## 术语（只此一套，别再造词）

**台架**（U2D2 / HAT TTL · 6.0 V · 限流 1–3 A）· **主控**（Radxa Zero 3W · `/dev/ttyS2`）·
**仿真**（sim · mjlab / MuJoCo）· **参考克隆**（`refs/`）· **中立会话**（不唤起职能角色）。
定义见 `wiki/concepts/dxl-bench-method.md` · `wiki/concepts/zero3w-bench-plan.md` · `wiki/concepts/local-workspace-layout.md`。
