# M2 责任图 Accountability Graph

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m2`

| 项 | 值 |
|----|----|
| **ID** | `m2` |
| **平面** | K-L0 经营本体 · Console 块 1 |
| **决策** | 自研 · 永不外包 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/graph_store.py` |
| **运行时** | Hub GraphStore · schema 已冻结 |
| **切片** | `harness/slices/M2.md` |
| **需求** | `harness/requirements/REQ-UAS-M02.req.md` |

## 定位

每个可管理位置是同一类节点：Goal × org × KPI × process × 五维 WM。禁止四套树。

## 非职责

时态事实、口径公式引擎

## 设计方案

pack.open 按 position_id × period 切片。NocoBase 块用同一 schema 投影；发布走 ChangeSet。

## 技术选型

PostgreSQL 16 + JSONB · schemas/accountability_graph.schema.json

## 接口

```
hub.scene.pack.open · hub.ops.graph.get/validate/publish
```

## 否决

- Neo4j/Graphiti 当 L0
- NocoBase Collection 当 ag_node

## 验收

- 缺维不可签发 · I-02

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m2 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
