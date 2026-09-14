# M16 时态知识 · Graphiti

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m16`

| 项 | 值 |
|----|----|
| **ID** | `m16` |
| **平面** | K-L2 · Console 块 3 |
| **决策** | 集成 · 可换图运行时 |
| **本仓库角色** | 平台零件 · 不在本产品实现 |
| **代码落点** | `services/hub-api/uas_hub/adapters/kg.py` |
| **运行时** | hub.kg.search |
| **切片** | `harness/slices/M16.md` |
| **需求** | `harness/requirements/REQ-UAS-M16.req.md` |

## 定位

事实何时为真。ingest 不是 cs 写。图谱页只搜不写。

## 非职责

经营本体、签发、cs 写

## 设计方案

episode id 禁 an-*。Console 不暴露 ingest。

## 技术选型

Graphiti · Neo4j 5 或 FalkorDB

## 接口

```
hub.kg.search · hub.ops.kg.search
```

## 否决

- Dify 知识库当 L2
- 图谱页写 CRM

## 验收

- I-04 未接地不得签发

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m16 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
