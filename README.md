# microduck-diy · 手搓小小鸭

个人 DIY 工程仓，面向 [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) 开源小鸭。

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
| [`imu_to_dxl/`](imu_to_dxl/) | 机身 IMU 参考板（v0.3）硬件工程与固件（Dynamixel ID 200） |
| [`wiki/`](wiki/) | DIY 知识库（先读 [`wiki/SCHEMA.md`](wiki/SCHEMA.md) → [`wiki/index.md`](wiki/index.md)） |
| [`cad/`](cad/) | 耐久打印包（`.3mf`） |

## 声明

- Microduck 及相关商标、网格版权归原作者与开源许可方；二次使用请遵守原 LICENSE。
- 本仓库为个人 DIY 记录，与官方量产、售卖无关。
- 打印强度、电气安全与整机可靠性请自行负责。
