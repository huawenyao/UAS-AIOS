# M10 Artifact Store

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m10`

| 项 | 值 |
|----|----|
| **ID** | `m10` |
| **平面** | 运行面 |
| **决策** | 自研元数据 · 存储引擎可换 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/adapters/artifact.py` |
| **运行时** | Hub Artifact 夹具 · P1 MinIO |
| **切片** | `harness/slices/M10.md` |
| **需求** | `harness/requirements/REQ-UAS-M10.req.md` |

## 定位

Insight/Task → ThemePack → Blueprint → Release → Instance。报告禁止当 pack.open 状态源。

## 非职责

世界模型、主数据

## 设计方案

元数据在 Postgres，字节在对象存储。晋升条件不可换。

## 技术选型

MinIO 实验室 / S3

## 接口

```
hub.ops.artifact.*
```

## 否决

- 制品只放本地磁盘当生产
- 用报告回放经营

## 验收

- file kind 不能驱动 pack.open

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m10 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
