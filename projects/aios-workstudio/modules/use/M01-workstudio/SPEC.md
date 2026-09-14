# M1 WorkStudio · 使用平面

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m1`

| 项 | 值 |
|----|----|
| **ID** | `m1` |
| **平面** | 使用平面 · 套件 A |
| **决策** | 自研产品壳 · workstudio-web |
| **本仓库角色** | 本产品实现 |
| **代码落点** | `projects/aios-workstudio/packages/workstudio-web` |
| **运行时** | packages/workstudio-web · demo/ |
| **切片** | `harness/slices/M1.md` |
| **需求** | `harness/requirements/REQ-UAS-M01.req.md` |

## 定位

岗位工作台。路由即场景：/today 今日必办、/room/:object_ref 作战室、/command 指挥舱、/exec/:task_id 执行态。打开首页 = pack.open 责任图切片，不是空白对话。

## 非职责

门禁、循环、口径计算、SoR 写、密钥

## 设计方案

启动 POST /hub/v1/scene/pack/open。签发嵌在作战台调 M5。进度 EventSource /hub/v1/exec/{id}/events。403 渲染人话 + policy.explain。状态在 URL + pack 快照，刷新再 open。

## 技术选型

P0 demo HTML · 产品路径 Vite 6 + TypeScript 5 · fetch + OIDC PKCE

## 接口

```
只消费 hub.scene.* 与 SSE
```

## 否决

- 前端 SDK 直连 Cube / Graphiti / CRM
- Next/Remix
- 聊天全文当实例状态
- 一线菜单出现连接器

## 验收

- 零零件 SDK
- 断零件时人话降级

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m1 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
