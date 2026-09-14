# M13 MCP Gateway

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m13`

| 项 | 值 |
|----|----|
| **ID** | `m13` |
| **平面** | 协议面 |
| **决策** | 自研壳 + 开源 MCP 协议 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/adapters/mcp.py` |
| **运行时** | POST /hub/v1/mcp/tools/{list,call} |
| **切片** | `harness/slices/M13.md` |
| **需求** | `harness/requirements/REQ-UAS-M13.req.md` |

## 定位

按剖面过滤 tools/list。call 仍走同一 PolicyChain。list 已过滤不能跳过 call 判定。

## 非职责

循环内核、持 SoR 密钥

## 设计方案

HTTP 企业网关。description 无 URL/Token/SQL。

## 技术选型

MCP 2025+

## 接口

```
POST /hub/v1/mcp/tools/list · /tools/call
```

## 否决

- WebSocket 私有帧当标准
- 密钥进 tool description

## 验收

- I-05 call 仍 403

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m13 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
