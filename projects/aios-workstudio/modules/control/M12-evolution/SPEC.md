# M12 Evolution Engine

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m12`

| 项 | 值 |
|----|----|
| **ID** | `m12` |
| **平面** | 演化面 |
| **决策** | 自研 · auto_apply 永关 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/adapters/evolution.py` |
| **运行时** | Hub Evolution · auto_apply 永关 |
| **切片** | `harness/slices/M12.md` |
| **需求** | `harness/requirements/REQ-UAS-M12.req.md` |

## 定位

信号 → 草案 → 人确认 → 回写 Law Pack / Release。

## 非职责

静默写 compiled、会话内改生产知识

## 设计方案

NocoBase 发布按钮只 submit/decide。

## 技术选型

Postgres + JSON Patch · Hub

## 接口

```
hub.ops.changeset.list/submit/decide
```

## 否决

- 模型直接 PATCH 配置
- auto_apply 请求头生效

## 验收

- I-09 未审批不进 compiled

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m12 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
