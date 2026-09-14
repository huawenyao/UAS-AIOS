# M15 口径服务 · Cube + OSI

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m15`

| 项 | 值 |
|----|----|
| **ID** | `m15` |
| **平面** | K-L1 · Console 口径页 |
| **决策** | 集成 Cube Core · YAML 可换服务 |
| **本仓库角色** | 平台零件 · 不在本产品实现 |
| **代码落点** | `services/hub-api/uas_hub/adapters/cube.py` |
| **运行时** | cs.metric.query → Cube |
| **切片** | `harness/slices/M15.md` |
| **需求** | `harness/requirements/REQ-UAS-M15.req.md` |

## 定位

kpi.is 只从口径层回填。失败标 stale。作战台不写 CubeQL。

## 非职责

签发任务、当责任图

## 设计方案

configs/metrics/osi/*.yml。NocoBase 口径页只读 status。

## 技术选型

Cube Core · OSI YAML

## 接口

```
cs.metric.query · hub.ops.caliber.status
```

## 否决

- 作战台写 CubeQL
- LookML 当唯一真相

## 验收

- I-03 失败标 stale

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m15 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
