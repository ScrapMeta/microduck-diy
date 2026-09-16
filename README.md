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

## 仓库结构

| 目录 | 内容 |
|------|------|
| [`governance/`](governance/) | **治理细则**（唯一版本源）· 通用模板 · `upstreams.lock` |
| [`wiki/`](wiki/) | DIY 知识库 = **规格真源**（先读 [`wiki/SCHEMA.md`](wiki/SCHEMA.md) → [`wiki/index.md`](wiki/index.md)） |
| [`imu_to_dxl/`](imu_to_dxl/) | 机身 IMU 参考板（v0.3）硬件工程与固件（Dynamixel ID 200） |
| [`cad/`](cad/) | 耐久打印包（`.3mf`） |
| [`image/`](image/) | Zero 3W seed 镜像构建与产物（大文件本地；见该目录 README） |
| [`scripts/`](scripts/) | 台架 / 上机脚本（`dxl_ping.py` 等） |
| [`.cursor/rules/`](.cursor/rules/) | 职能 rule（pm 常驻 + 四职能 + ros2 附件）—— **入仓，受版本控制** |
| [`AGENTS.md`](AGENTS.md) | **Agent 治理入口**：不变量 + 指向 `governance/` |
| `refs/` | **只读参考克隆**（ignore）：官方 / 社区 / 教程仓 |
| `microduck_ros2/` | **自有兄弟仓**（ignore）：ROS2 并行移植，独立 push |
| `temp/` `vms/` `.venv-cad/` | 本地临时（ignore）· **非真源** |

## 本地工作区约定

- **只读参考一律放 `refs/`**：新增克隆放这里即自动被 ignore
- **禁用 `git clean -x`**：它会删除被 ignore 的目录 —— 包括 `refs/` 下全部参考克隆。只用 `git clean -fd`
- **交付物归自有仓**：`refs/` 内只读；产出落本仓或 `microduck_ros2/`，上游不留未提交改动
- 路径一律**从根写**：`governance/…` · `wiki/…` · `refs/microduck/scripts/setup-board.sh`
- 全树与各目录角色：wiki [[local-workspace-layout]]（布局真源）

## 声明

- Microduck 及相关商标、网格版权归原作者与开源许可方；二次使用请遵守其 LICENSE。
- 本仓库为个人 DIY 记录，与官方量产、售卖无关。
- 打印强度、电气安全与整机可靠性请自行负责。
