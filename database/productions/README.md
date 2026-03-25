# Sub App 生产记录

本目录存放 Agent 自主生产 UAS sub app 的记录，用于审计与演化分析。

## 文件命名

`<app_id>_<timestamp>.json`

示例：`ai-recruitment-os_20250315T120000.json`

## 记录内容

- 意图（intent）
- 方案（blueprint）
- 模板（template）
- 校验结果（validation）
- 生成路径（app_root）
- 生产时间戳

## 参考

- 设计文档：`docs/AGENT_SUBAPP_PRODUCER_DESIGN.md`
- 生产协议：`.claude/skills/subapp_producer_protocol.md`
