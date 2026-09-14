# M3 世界模型 Store

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m3`

| 项 | 值 |
|----|----|
| **ID** | `m3` |
| **平面** | K-L0 · Console 块 2 |
| **决策** | 自研 · 三寿命 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/wm_store.py` |
| **运行时** | Hub WmStore |
| **切片** | `harness/slices/M3.md` |
| **需求** | `harness/requirements/REQ-UAS-M03.req.md` |

## 定位

法则编译器的持久化。draft / compiled / live。Runtime 只 PATCH live。

## 非职责

预测器、RAG 索引、聊天 checkpoint

## 设计方案

NocoBase 寿命板三列对照；compiled 列只读。

## 技术选型

与责任图同一 Postgres，不同表

## 接口

```
hub.wm.get/patch · hub.ops.wm.get
```

## 否决

- 把 WM 塞进 Graphiti
- live 改 compiled

## 验收

- Runtime PATCH compiled → 拒绝

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m3 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
