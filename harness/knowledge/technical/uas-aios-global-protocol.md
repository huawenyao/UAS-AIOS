# 技术方案：UAS-AIOS 全局协议（Π）

| 项 | 值 |
|----|----|
| 地位 | 24 模块共用信封与 Port SPI；零件可换，方法名不换 |
| 宪法 | `configs/protocol/KERNEL.yaml` |
| 注册表 | `configs/protocol/registry.json` |
| Schema | `schemas/protocol/module_protocol.schema.json` |
| SPI | `services/hub-api/uas_hub/ports.py` |
| 夹具 | `services/hub-api/uas_hub/adapters/` |
| 轨迹 | `harness/traces/hengchuan-ltc/index.json` |

## 规则

1. 一线只走 `hub.*`。集成模块（Cube / Graphiti / Lethe / Temporal / LangGraph / MCP）只经对应 Port。
2. 判定序不可颠倒：inject → tenant → registry → rbac → approval → gates → scope → execute → audit。
3. 开发切片 = 注册表里该模块的 verbs + 红灯测试，不整包读取 design/。
4. `decision=integrate` 必须 `replaceable=true` 且有 `port`。
5. documentary（文件存在）不得把模块标 completed。
