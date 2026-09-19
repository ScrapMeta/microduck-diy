# Microduck DIY · 手搓小小鸭

工作目录：`D:\projects\microduck` —— **本目录就是 `ScrapMeta/microduck-diy` 仓库根**。
只读参考克隆在 `refs/`（ignore）· 自有兄弟仓 `microduck_ros2/`（ignore，但是自有仓、**可写**）。

> **一个人 · 本地 wiki · 角色 skill。** 唤起一个角色就开始干 —— 不设 Issue 路由、不填交接表、不等审批。
> **本文件只管三件事**：给 agent 划红线 · 怎么改规则 / 技能 / wiki · 记录怎么写。

**环境叫法（只此一套，别再造词）：** **台架**（U2D2 / HAT TTL · 6.0 V · 限流 1–3 A）· **主控**（Radxa Zero 3W ·
`/dev/ttyS2`）· **仿真**（sim · mjlab / MuJoCo）· **参考克隆**（`refs/`）。
定义 → `wiki/concepts/dxl-bench-method.md` · `wiki/concepts/zero3w-bench-plan.md` · `wiki/concepts/local-workspace-layout.md`。

## 给 agent 的红线（不可协商）

1. **凭据不进 Git · 不进报告 · 不回显。**
2. **`refs/` 只读** —— 正文永不修改，不留未提交改动。要修订就另建页 cite 它。
3. **破坏性操作先列范围 ＋ 预检，等我确认** —— 覆盖 / 删文件 · 回滚 · 烧录量产固件 · 制板下单 · 强推 · `git clean -x`。
4. **干完即停** —— 交完交付物就停：不替我拍板 · **不建 / 不合并 PR** · 不扩范围 · 不顺手改别的。**Issue 只有 pm 能动**（见「GitHub」）—— 职能角色不开、不关、不碰。
5. **遇阻就停** —— 信息不足、或该我决定的事，把问题交回来；不猜着往下做、不降标准。
6. **不代签 Gate** —— 上电 · 剪线 / 改线 · 制板下单 · 验收，只有我本人能签。

## 改规则 / 技能 / wiki

| 改什么 | 谁改 | 怎么算数 |
|---|---|---|
| 技能 `SKILL.md`（职能 · 红线 · 骨架 · 沉淀区） | **角色会话自进化**（改自己的手册）· 或 Human 点中立会话改 | 不得与 `AGENTS.md` 冲突；**扩权**仍须我点头 |
| 规则 `AGENTS.md` | **中立会话**（我拉起 · 不唤起职能角色） | 改完停下等我确认 |
| wiki（`concepts` · `log` · `tasks` · 报告） | **干活的那个角色写** | 按「角色 → 必写记录」直接写，不用逐次问 |

> **技能能自己进化 —— 但技能不是规则源。** 与 `AGENTS.md` 冲突时以 `AGENTS.md` 为准；
> **扩权**（放宽红线 · 绕开确认 · 改本表）不属自进化，仍须我拉起中立会话点头。
> **规则制定统一由我拉起中立会话** —— 职能角色不碰 `AGENTS.md`。

## 记录约定

| 位置 | 写什么 | 规矩 |
|---|---|---|
| `wiki/concepts/` `entities/` `comparisons/` | 现行事实 SSOT | 改完 bump `updated` |
| `wiki/log.md` | 流水（动作 ＋ 主题 ＋ 要点） | **只追加** |
| `wiki/tasks.md` | 任务台账 —— **开 ＋ 关同页**（取代 GitHub Issue） | **任何角色**可新建 / 更新 / 关闭；编号 `T-nn` **不复用**；终态行落 `完成` 表、**关闭理由必须写清**；只追加、不改旧行；四态看板与数量口径见下节 |
| `wiki/index.md` | 导航 ＋ 领域 ＋ 现行优先级 ＋ 标签表 | 增删页时顺手改 |
| `wiki/raw/` | 素材归档（时点快照） | **正文永不改**；索引 `wiki/_meta/raw-inventory.md` |
| `wiki/_archive/` | 暂停 / 过时的页 | 撤出导航，**不删** |

每页 frontmatter：`title` · `created` · `updated` · `type` · `tags`。正文页 ≤ **200 行**，超了拆页。
校验器 `scripts/wiki_lint.py` 机械执行以上三条，**它的判定即规格**；「已知超长 · 只减不增」的记账表也在那个脚本里（欠拆页记在 `tasks.md`）。

**台账**（`wiki/tasks.md`）—— **编号 · 四态看板（`待办` / `执行` / `阻塞` / `完成`）· 完成 / 关闭语义**按**通用方式**写在那页「**通用约定**」（可整段移植到别的工程）；**本文件不复制**。

- **不设数量上限** —— 条数多不构成拒绝开工的理由；台账太长**由人工收拢**（pm 推送时把 `完成` 行一批归档 Issue）。
- **台账不属任何单一角色** —— **谁干的活谁能开 / 更新 / 关自己的任务**；**push 与 Issue 归档只有 pm**。

**谁写什么（角色 → 必写记录）：**

| 角色 | 必写 |
|---|---|
| **pm** | 治理与台账 → `AGENTS.md` · `wiki/index.md` · `tasks.md` · `log.md`；**唯一 push ＋ Issue 归档者** |
| **hardware** | 板 · 料号 · 订单 · 台架电测 → `wiki/concepts/board-*.md` · `entities/*.md` · `log.md` |
| **software** | 固件 · 总线 · 镜像 · ROS2 · ONNX → `wiki/concepts/*firmware*|*flash*|*bus*|*bench*.md` · `log.md` |
| **structure** | 打印件 · 装配 · 机械件数 → `wiki/concepts/mechanical-*|print-*|fastener-*.md` · `log.md` |

## 角色（skill = 我的操作手册）

| 角色 | 唤起 | 手册 | 范围 |
|---|---|---|---|
| **pm** | `/microduck-pm` | `.cursor/skills/microduck-pm/SKILL.md` | 治理 · 台账 · wiki 收口 · 跨域改派；不写实现 |
| **hardware** | `/microduck-hardware` | `.cursor/skills/microduck-hardware/SKILL.md` | 原理图 / PCB · 电气 BOM · 制板接线 · 台架电测 |
| **software** | `/microduck-software` | `.cursor/skills/microduck-software/SKILL.md` | 固件 · 总线协议 · 上机脚本 · 系统镜像 · ROS2 · 训练 / ONNX |
| **structure** | `/microduck-structure` | `.cursor/skills/microduck-structure/SKILL.md` | `cad/` 打印件 · 装配 · 机械 BOM 件数 |

角色 = **范围收窄 ＋ 操作手册**：唤起 `/microduck-hardware` 就是「只干这个，别顺手干别的」。
**手册随干活长大** —— 技能可自己改（**自进化**），也可由我点中立会话改；改完报备，等我确认（见上一节）。

**领地 —— 按你正在改的路径认角色：**

| 路径 | 角色 |
|---|---|
| `cad/**` · `wiki/concepts/mechanical-*` `print-*` `fastener-*` | **structure** |
| `imu_to_dxl/hardware/**` · `wiki/concepts/board-*` `elec-*` · `wiki/entities/board*` | **hardware** |
| `imu_to_dxl/firmware/**` · `imu_to_dxl/scripts/**` · `image/**` · `scripts/**` · `microduck_ros2/**` | **software** |
| `AGENTS.md` · `wiki/index.md` · `wiki/log.md` | **pm** |
| `wiki/tasks.md` | **全员** —— 任何角色可开 / 更新 / 关 |

> 旧版 `.mdc` 靠 `globs:` **自动**挂上角色规则；skill 没这个能力（`disable-model-invocation: true` = 只在你打 `/命令` 时加载）。
> **这张表就是那道护栏的替代品** —— 落到谁的地盘就先唤起谁，别顺手改。
> **它约束的是角色会话，不是权限系统**：你自己点名要改的路径，中立会话照做 —— **不存在「越领地」**。
> 表只回答一个问题：**角色会话自己开工时，哪些路径不归它碰**。
> `refs/` 对**所有人**只读（见红线 2）。

## 仓库形态

**工作区根就是本仓工作树**；只有两类目录特殊：

| 类型 | 位置 | 版本控制 | 禁止 |
|---|---|---|---|
| **自有兄弟仓** | `microduck_ros2/` | 独立仓 + 自有远端；**ignore** | 当只读对待 · 留未提交交付物 |
| **只读参考克隆** | `refs/` | 独立克隆；**ignore** | 留未提交改动 · 把交付物放进去 |
| **本地临时** | `temp/` `vms/` `.tmp/` `.venv-cad/` | 无；ignore | 当规格真源 |

- **交付物必须落在自有 push 权限的仓里**：上游克隆里做的工作提交不出去 = 丢失。
- **本仓禁用 `git clean -x`** —— 它会删除被 ignore 的 `refs/`，一次误操作即抹掉全部参考克隆。只用 `git clean -fd`。
- 上游版本用 `scripts/upstreams.lock` 钉住（`scripts/refresh-upstreams.ps1 -Fetch` 重生成；**不带 `-Fetch` 不联网**，
  `Behind=0` 只反映上次 fetch 的快照，不构成「已最新」）。

## GitHub

**只当 git 远端与历史归档**：不建 PR · 不建标签 · 不走近门禁。
历史 Issue（#1–#11）与 Milestone `v0.1` **冻结保留只读**；未完成项已迁入 `wiki/tasks.md`。

- **推送：只有 pm push `main`** —— 其他角色只本地 commit；**推送时顺带收尾**：把 `tasks.md`「完成」里的行归入 Issue 归档 → **从本页删掉**（git 历史留痕）。**归档这个动作只记 `log.md`，不在 `tasks.md` 留任何占位行** —— 否则「记归档的那一行」自己又成了待归档的行，永远收敛不了。
- **Issue：只有 pm 可为归档建 Issue** —— 开完即关，正文含结论 ＋ 出处；**不当路由、不打流程标签、不挂 Milestone**。

## 不收录

技术事实 → `wiki/concepts/`；素材 → `wiki/raw/`；脚本约定 → `scripts/README.md`；布局 → `wiki/concepts/local-workspace-layout.md`。

**本文件只写规则**，以上以那些页为准，不在此复制。
