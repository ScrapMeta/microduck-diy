---
title: 嘉立创 EDA MCP 接入
created: 2026-08-30
updated: 2026-09-01
type: concept
tags: [workspace, open-source]
sources:
  - raw/articles/jlceda-mcp-hub-readme-2026-08-30.md
confidence: high
related: [imu-schematic-feasibility, imu-to-dxl-v2, elec-rpi-robot-hat]
---

# 嘉立创 EDA MCP 接入

## 推荐方案（官方双扩展）

[JLCEDA-MCP](https://github.com/sengbin/JLCEDA-MCP) = **mcp-hub**（Cursor）+ **MCP Bridge**（嘉立创 EDA 专业版）。

```
嘉立创 EDA（MCP Bridge）
    ↕ WebSocket  ws://127.0.0.1:8765/bridge/ws
Cursor（JLCEDA MCP Hub 扩展）
    ↕ MCP（扩展通过 mcpServerDefinitionProviders 注册）
Agent Chat
```

### 本机状态（2026-09-01 复测）

| 组件 | 状态 |
|------|------|
| Cursor 扩展 `chengbin.jlceda-mcp-hub` **v1.5.4** | **已安装** |
| 嘉立创 EDA 专业版 | **已装** `C:\Program Files\lceda-pro\lceda-pro.exe`，本次已拉起进程 |
| Hub `127.0.0.1:8765` | **未 LISTENING**（Agent 会话里仍看不到 JLCEDA MCP 工具） |
| EDA 侧 MCP Bridge | 须在**原理图页**开「外部交互」后连 `ws://127.0.0.1:8765/bridge/ws` |
| `~/.cursor/mcp.json` 手写 jlceda | **不需要**（Hub 用扩展 Provider 注册） |

### 你需要完成的步骤

1. 安装并打开 **嘉立创 EDA 专业版**
2. 扩展管理器 → 搜索 **「MCP Bridge」** → 安装；桥接地址与 Hub 侧边栏一致（默认 `ws://127.0.0.1:8765/bridge/ws`）
3. **完全重启 Cursor**，打开左侧 **JLCEDA MCP** 侧边栏，确认监听已起
4. EDA 中打开**原理图页**（首聊后 Hub 才起服务；多页时仅活动页执行）
5. 可选：Hub「功能设置」开启 **暴露透传 EDA API 工具**（`api_invoke` 等）

### Hub 能做什么 / 不能做什么

| 能 | 不能 / 弱 |
|----|-----------|
| `schematic_read` / `schematic_review` 读网表与器件 | 电源/地符号 **不会自动放**，要人手加 |
| `component_select` 搜库并由你确认型号 | 放置是 **交互引导**：侧边栏提示，你在 EDA 里点放 |
| `component_place` 按清单引导放置 | **不是**一键从自然语言生成完整可量产原理图 |
| 可选 `api_invoke` 调底层 EDA API | 无实物/网表时无法「还原」闭源板 |

### 其它开源方案（备选）

| 项目 | 特点 |
|------|------|
| [oaslananka/easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro) | 更多原理图 **自动** place/wire 工具（`confirmWrite`） |
| [hyl64/jlcmcp](https://github.com/hyl64/jlcmcp) | PCB 自动化偏强；需自建 relay + `mcp.json` |

本仓库优先官方 Hub；若以后要「Agent 自动连线画草图」，再评估 easyeda-mcp-pro。

相关：[[imu-schematic-feasibility]] · [[imu-to-dxl-v2]] · [[elec-rpi-robot-hat]]
