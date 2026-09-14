# M4 Law Pack

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m4`

| 项 | 值 |
|----|----|
| **ID** | `m4` |
| **平面** | K-L0 / 德 · Pack Studio |
| **决策** | 自研 · 知识即配置 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/adapters/law.py` |
| **运行时** | Hub Law Pack |
| **切片** | `harness/slices/M4.md` |
| **需求** | `harness/requirements/REQ-UAS-M04.req.md` |

## 定位

法则条文版本化。冲突显式。编译进 compiled WM。

## 非职责

Temporal 解释 Law、连接器持条文

## 设计方案

未审批 changeset 不能 law.compile。

## 技术选型

配置文件 + Hub 编译

## 接口

```
hub.law.compile · hub.ops.law.diff
```

## 否决

- 会话内改生产知识

## 验收

- I-09

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m4 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
