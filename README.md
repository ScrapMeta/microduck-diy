# microduck-diy · 手搓小小鸭

个人 DIY 工程仓，面向 [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) 开源小鸭。

> **本仓同时是本地工作区**：路径 `D:\projects\microduck` **就是本仓的工作树**。
> 只读参考克隆（官方 / 社区 / 教程仓）收在 `refs/`，**已被 `.gitignore` 排除**。

## 目标

- **完美复刻**官方原方案（机身、电控、总线契约与可打印件口径对齐官方资料）
- **完美适配**官方生态（HAT、Dynamixel 总线、策略/运行时与开源契约一致，可直接对接官方软件栈）
- 在官方生态之上，**扩展**各类硬件与玩法（传感器、执行器、外设与新交互），而不是另起平行协议栈

## 关注

- 小红书：**精钢葫芦娃**
- 公众号：**人工具身智能**
- 相关主题：手搓小小鸭

## 去哪找什么

| 入口 | 内容 |
|------|------|
| [`AGENTS.md`](AGENTS.md) | **唯一规则源**：谁能改什么 · 红线 · 记录落点 |
| [`wiki/`](wiki/) | **规格与资料真源** → 导航 [`index.md`](wiki/index.md) · 欠什么 [`tasks.md`](wiki/tasks.md) · 流水 [`log.md`](wiki/log.md) |
| [`.cursor/skills/`](.cursor/skills/) | **角色操作手册**：唤起 `/microduck-pm` · `/microduck-hardware` · `/microduck-software` · `/microduck-structure` |
| [`scripts/`](scripts/) | 台架 / 上机脚本 ＋ `wiki_lint.py` · `refs_lint.py` ＋ `upstreams.lock` |
| [`imu_to_dxl/`](imu_to_dxl/) | 机身 IMU 参考板（v0.3）硬件工程与固件（Dynamixel ID 200） |
| [`cad/`](cad/) | 耐久打印包（`.3mf`） |
| [`image/`](image/) | Zero 3W seed 镜像构建与产物（大文件本地；见该目录 README） |

## 仓库结构

| 目录 | 内容 |
|------|------|
| [`wiki/`](wiki/) | DIY 知识库 ＝ **规格真源** |
| [`scripts/`](scripts/) | 台架 / 上机脚本 · 两台 linter · 上游版本锁定 |
| [`imu_to_dxl/`](imu_to_dxl/) | 机身 IMU v0.3 · 板设计 ＋ 固件 |
| [`cad/`](cad/) | 耐久打印包 |
| [`image/`](image/) | Zero 3W seed 镜像构建与 overlay |
| `refs/` | **只读参考克隆**（ignore）：官方 / 社区 / 教程仓 |
| `microduck_ros2/` | **自有兄弟仓**（ignore）：ROS2 并行移植，独立 push |
| `temp/` `vms/` `.venv-cad/` | 本地临时（ignore）· **非真源** |

## 怎么干活

唤起一个角色就开始干 —— 不设 Issue 路由、不填交接表、不等审批。

```
/microduck-pm          治理 · 台账 · wiki 收口 · 跨域改派（不写实现）
/microduck-hardware    原理图 / PCB · 电气 BOM · 制板接线 · 台架电测
/microduck-software    固件 · 总线协议 · 上机脚本 · 系统镜像 · ROS2 · 训练 / ONNX
/microduck-structure   cad/ 打印件 · 装配 · 机械 BOM 件数
```

## 本地工作区约定

- **只读参考一律放 `refs/`**：新增克隆放这里即自动被 ignore
- **`refs/` 只读**（含禁止在其中留未提交改动）· **禁用 `git clean -x`** · **交付物归自有仓**
  —— 这三条是红线，正文只在 [`AGENTS.md`](AGENTS.md)「红线」，此处不复制
- 路径一律**从根写**：`wiki/…` · `cad/…` · `refs/microduck/scripts/setup-board.sh`
- 全树与各目录角色：`wiki/concepts/local-workspace-layout.md`（**布局真源**）
- **GitHub 只当 git 远端与历史归档**：不建 PR · 不建标签 · **Issue 只作 pm 归档**（开完即关）—— 细则在 [`.cursor/skills/microduck-pm/SKILL.md`](.cursor/skills/microduck-pm/SKILL.md)

## 声明

- Microduck 及相关商标、网格版权归原作者与开源许可方；二次使用请遵守其 LICENSE。
- 本仓库为个人 DIY 记录，与官方量产、售卖无关。
- 打印强度、电气安全与整机可靠性请自行负责。
