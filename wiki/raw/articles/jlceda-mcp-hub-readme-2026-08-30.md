---
source_url: https://github.com/sengbin/JLCEDA-MCP
ingested: 2026-08-30
sha256: bc47c6a45590147f87660adf5a3c70b9625263948afa25df9ce46ce74d3c0067
---

# JLCEDA-MCP README 要点（ingest 摘录）

双扩展：mcp-hub（VS Code/Cursor）+ mcp-bridge（嘉立创 EDA）。

工具：schematic_read、schematic_review、component_select、component_place；可选 api_index / api_search / eda_context / api_invoke。

约束：电源与地不由 AI 自动放置；放置为侧边栏交互；两扩展须同时安装；仅原理图/PCB 页可连接；默认桥 `ws://127.0.0.1:8765/bridge/ws`。

Cursor 扩展 ID：`chengbin.jlceda-mcp-hub`。
