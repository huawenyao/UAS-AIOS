# M7 Capability Registry cs.*

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m7`

| 项 | 值 |
|----|----|
| **ID** | `m7` |
| **平面** | 控制 / 系统面 |
| **决策** | 自研契约 · 名与 schema 不可换 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `configs/capability_registry.json` |
| **运行时** | services/hub-api/uas_hub/registry.py |
| **切片** | `harness/slices/M7.md` |
| **需求** | `harness/requirements/REQ-UAS-M07.req.md` |

## 定位

语义动作目录。启用、审批级、副作用、契约绿灯。MCP 工具名与 cs.* 同源。

## 非职责

实现连接器、解释 Law

## 设计方案

JSON Schema 权威。scene 隐藏写工具。patch 走 ChangeSet。

## 技术选型

JSON Schema · Hub 加载

## 接口

```
hub.ops.registry.list/patch · MCP tools/list 同源
```

## 否决

- 两份手写 schema
- 模型可见 URL/SQL/密钥

## 验收

- I-12 名/字段一致
- I-05 scene 写工具不可见

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m7 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
