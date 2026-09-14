# M22 Utopia（可选 Spike）

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m22`

| 项 | 值 |
|----|----|
| **ID** | `m22` |
| **平面** | 知识工程 |
| **决策** | 默认不部署 · 只读导出 |
| **本仓库角色** | 默认不部署 |
| **代码落点** | `默认不部署` |
| **运行时** | Compose profile optional |
| **切片** | `harness/slices/M22.md` |
| **需求** | `harness/requirements/REQ-UAS-M22.req.md` |

## 定位

审冲突 → 导出候选 → 人走 ChangeSet。无 CRM Action。

## 非职责

生产写、替代 Graphiti

## 设计方案

与 NocoBase 图谱页纪律相同。

## 技术选型

Utopia v0.1 观察

## 接口

```
只读导出到 ChangeSet
```

## 否决

- 当 L2
- 生产写按钮

## 验收

- 默认不部署

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m22 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
