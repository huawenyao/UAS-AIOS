# M24 模型推理 Broker

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m24`

| 项 | 值 |
|----|----|
| **ID** | `m24` |
| **平面** | 编织面 |
| **决策** | 连接任意 LLM · 必须可换 |
| **本仓库角色** | 平台零件 · 不在本产品实现 |
| **代码落点** | `services/hub-api/uas_hub/adapters/broker.py` |
| **运行时** | LLM Broker |
| **切片** | `harness/slices/M24.md` |
| **需求** | `harness/requirements/REQ-UAS-M24.req.md` |

## 定位

按剖面限流、提供商切换。会话不当实例状态。

## 非职责

世界模型、经营承诺

## 设计方案

只在 Broker 内用 Provider SDK。

## 技术选型

Provider SDK 仅 Broker

## 接口

```
hub.ops.model.route
```

## 否决

- 把聊天历史当状态

## 验收

- 换提供商契约不变

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m24 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
