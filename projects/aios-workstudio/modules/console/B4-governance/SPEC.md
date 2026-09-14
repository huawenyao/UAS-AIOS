# Governance Console · B4

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `gov`

| 项 | 值 |
|----|----|
| **ID** | `gov` |
| **平面** | Platform Console（NocoBase 壳内） |
| **决策** | 合规与身份运营壳 |
| **本仓库角色** | Console 可视化壳（不当内核） |
| **代码落点** | `projects/aios-workstudio/Console` |
| **运行时** | NocoBase 治理页 |
| **切片** | `harness/slices/M11.md` |
| **需求** | `harness/requirements/REQ-UAS-M11.req.md` |

## 定位

岗位绑定、双轨抽查、审计导出、遗忘回执、转派记录。合规角色不派业务活。

## 非职责

业务派活、auto_apply

## 设计方案

只读审计检索，写权限走 ChangeSet。

## 技术选型

NocoBase 页 + hub.ops.iam / audit / memory.receipt

## 接口

```
hub.ops.iam.bindings · hub.ops.audit.export · hub.ops.memory.receipt.get
```

## 否决

- 用报告回放经营
- pipaw 读 Lethe

## 验收

- 遗忘回执可检索

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 gov 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
