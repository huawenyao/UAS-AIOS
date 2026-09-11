# Platform Console · 离线 Demo

UAS-AIOS **Suite B** 管理壳，仅模拟 `hub.ops.*` 读写。无 hub-api、NocoBase 或后端依赖。

## 启动

```bash
cd projects/aios-workstudio/Console/demo
python -m http.server 8765
```

浏览器打开 `http://localhost:8765/#/overview`。

首次或 stuck 状态时可加 `?reset=1` 清空 sessionStorage：`http://localhost:8765/?reset=1#/overview`。

## 页面

| 路由 | 说明 |
|------|------|
| `#/overview` | 健康指标、Schema 漂移夹具、租户套件摘要 |
| `#/integrate` | Hub 剖面与 I-05 dry-run |
| `#/control` | 租户套件、治理禁令、SRE 零件逃生 |
| `#/ontology` | 责任节点校验五件套、投影边切换 |
| `#/mesh` | 能力 approval_level、连接器槽位、MCP 过滤 |
| `#/govern` | Law Pack 版本冲突声明 |
| `#/run` | 模型路由 ChangeSet、KG ingest 只读状态 |
| `#/publish` | ChangeSet 确认 / 驳回队列 |

## Demo 行为（P0 / P1）

- **US-B-03** — 租户 `t-hengchuan` 套件启用切换 → 提交 pending ChangeSet（不静默生效）
- **US-B-07** — Mesh 能力表可改 `approval_level` L1/L2/L3 与启用开关 → ChangeSet
- **US-B-10** — Schema drift healthy ↔ fail 夹具；fail 时红灯并阻断发布页确认
- **I-02** — 责任节点缺 WM 维 / caliber → 校验五件套报 `WM_INCOMPLETE` / `INVARIANT_FAILED`；`an-stage-visit` 保持完整
- **Overview** — 展示 `health.use.ungrounded_rate`、`health.control.gate_p95_ms` 及 open_ms / explain / approval_stuck / stale
- **US-B-21** — 顶栏永久禁令条：无「关闭审计」、auto_apply 永久 OFF；点击显示 toast
- **US-B-09** — 连接器 sandbox ↔ prod 槽位切换（无明文密钥）；轮换仍走 ChangeSet
- **US-B-17** — Run 页 KG ingest_status：lag、最近 episode、失败列表夹具（无写入按钮）
- **US-B-18** — 模型 / rpm 变更 → 发布队列 ChangeSet
- **SRE** — 角色=sre 时可见「零件逃生」开关；ON 显示 Temporal/Cube/Neo4j 占位链接 + 审计 toast

## P2（附加）

- **Law Pack** — 现行 vs 候选版本及显式冲突规则表
- **Ontology** — 投影边 `org_cascade` / `kpi_split` / `stage_split` / `object_drill` UI 切换

## 角色

- `admin` / `operator` / `sre` — 正常使用
- `frontline` — 全控制台锁定 overlay

## 约束

- 纯 fixture + `sessionStorage`，不发起真实 hub 请求
- 禁止 invoke_cs、kg ingest 写、Workflow、Collection-as-truth
- 所有配置变更经 ChangeSet → 发布页人工确认后才 `applied=true`

## 规格引用

- `docs/strategic/design/UAS_AIOS_PLATFORM_PRODUCT.md` §8（若已入库）
- `harness/requirements/user-stories-uas-aios.md` US-B-01..21
- `docs/strategic/design/uas-aios-cluster.html` 原则
