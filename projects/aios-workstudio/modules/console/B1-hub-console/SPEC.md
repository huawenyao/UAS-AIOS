# Hub Console · B1 控制中心

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `hubc`

| 项 | 值 |
|----|----|
| **ID** | `hubc` |
| **平面** | Platform Console（NocoBase 壳内） |
| **决策** | 管理壳，不是第二套 Hub |
| **本仓库角色** | Console 可视化壳（不当内核） |
| **代码落点** | `projects/aios-workstudio/Console` |
| **运行时** | NocoBase 页 + hub.ops |
| **切片** | `—` |
| **需求** | `—` |

## 定位

平台管理员：剖面矩阵、租户、门禁试运行、「若现在点写会怎样」。一线账号默认看不到 /console。

## 非职责

签发经营任务、关审计、auto_apply

## 设计方案

数据只调 hub.ops.policy.explain / profile.matrix / tenant.get / health.gate。

## 技术选型

NocoBase 页 + packages/hub-client ops 子集

## 接口

```
hub.ops.policy.explain · hub.ops.profile.matrix · hub.ops.tenant.get
```

## 否决

- 客户端改 profile
- 静默关审计

## 验收

- explain 可用率 100%

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 hubc 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
