# M20 工具类型 · JSON Schema

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m20`

| 项 | 值 |
|----|----|
| **ID** | `m20` |
| **平面** | 协议面 |
| **决策** | 一份权威，三处生成 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `schemas/` |
| **运行时** | CI 漂移检测 |
| **切片** | `harness/slices/M20.md` |
| **需求** | `harness/requirements/REQ-UAS-M20.req.md` |

## 定位

schemas/*.json + registry 生成 Pydantic、MCP schema、连接器校验。

## 非职责

给模型宽松、给连接器严格的双份

## 设计方案

前台用 JSON Schema 校验，不手写第三份 TS 模型。

## 技术选型

JSON Schema 2020-12 · Pydantic v2

## 接口

```
hub.ops.schema.drift
```

## 否决

- 只写 Pydantic 再反推
- 任意 dict 进连接器

## 验收

- I-12 改字段未生成则 CI 失败

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m20 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
