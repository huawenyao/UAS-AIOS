# NocoBase · Platform Console 壳

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `nb`

| 项 | 值 |
|----|----|
| **ID** | `nb` |
| **平面** | 套件 B 可视化壳 |
| **决策** | 集成壳，不当内核 |
| **本仓库角色** | Console 可视化壳（不当内核） |
| **代码落点** | `projects/aios-workstudio/Console` |
| **运行时** | 未来 services/console-nocobase · 只调 hub.ops.* |
| **切片** | `—` |
| **需求** | `harness/requirements/REQ-UAS-AIOS-002.req.md` |

## 定位

知识管理员的可视化控制台：角色、侧栏（本体 / 图谱 / 法则 / 口径）、页面编排、JSON Schema 表单。三个自定义块是 BlockModel，只调 hub.ops.*。

## 非职责

经营库、口径引擎、双时态图、Hub 门禁、签发任务、写 SoR

## 设计方案

插件 @uas/plugin-console。块 1 责任图投影。块 2 WM 三寿命。块 3 Graphiti 时态浏览。compose profile console，阶段 A 不启动。

## 技术选型

NocoBase client-v2 Plugin · BlockModel（禁止 CollectionBlockModel）

## 接口

```
GET/POST /hub/v1/ops/* · profile 强制 builder · X-Ops-Role: knowledge_admin
```

## 否决

- Graphiti/OSI 打进 Collection
- Workflow 写 CRM
- plugin-ai / mcp-server
- 一线打开 /console

## 验收

- 无 ops/kg/ingest 路由
- submit 后 applied=false
- compiled PATCH 422

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 nb 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
