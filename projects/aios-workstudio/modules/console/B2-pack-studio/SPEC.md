# Pack Studio

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `pack`

| 项 | 值 |
|----|----|
| **ID** | `pack` |
| **平面** | Platform Console（NocoBase 壳内） |
| **决策** | 法则 / 技能 / 制品的配置壳 |
| **本仓库角色** | Console 可视化壳（不当内核） |
| **代码落点** | `projects/aios-workstudio/Console` |
| **运行时** | NocoBase 表单 + changeset |
| **切片** | `harness/slices/M4.md` |
| **需求** | `harness/requirements/REQ-UAS-M04.req.md` |

## 定位

知识管理员与实施顾问主战场。发布 = ChangeSet。不直写 compiled。

## 非职责

生产写路径、SoR 密钥

## 设计方案

Law Pack 版本对比、Skill 货架漏斗、制品晋升条。NocoBase 只提供表单底座。

## 技术选型

NocoBase 表单 + hub.ops.changeset.*

## 接口

```
hub.ops.law.diff · hub.ops.skill.* · hub.ops.artifact.* · hub.ops.changeset.submit
```

## 否决

- 模型直接 PATCH 配置文件
- 跳过 invariant 发布

## 验收

- 未审批 ChangeSet 不进 compiled

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 pack 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
