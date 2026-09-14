# Spec-5 · 连接器（connector.rotate）

| 项 | 值 |
|----|-----|
| 状态 | 已确认（用户 2026-09-14「批准」） |
| 日期 | 2026-09-14 |
| 服从 | [Spec-0](./2026-09-12-aios-workstudio-modules-design.md) |
| 前置 | Spec-1…4A |
| 交付 | CapabilityHub ops + Console `#/mesh` |

**一句话：** `POST /hub/v1/ops/connector/rotate` 真实现：只出 `vault://` 指针、无明文；写止于 pending ChangeSet；frontline 403。

**禁止：** 自研 CRM；真 KMS 进程；响应含 password/api_key；NocoBase；改皮肤；git commit。

---

## 出站

| 判据 | 证明 |
|------|------|
| rotate 200 + `secret_ref` 以 `vault://` 开头 | HTTP |
| 响应体无 `password` / `api_key` / 非 vault 明文 | 断言 |
| 返回 ChangeSet `status=pending` `auto_apply=false` | HTTP |
| live `connector/list` **不**因 rotate 立刻改 secret（或仅 pending；确认后才改——本战役：rotate 只产 pending，list 仍旧指针直至 decide） | 测 |
| frontline 403 | HTTP |
| Demo 轮换按钮走 Hub | scaffold / 接线 |

## 端点

- `POST /hub/v1/ops/connector/rotate` body `{connector_id}` → `_put_pending(kind=connector.rotate, payload={connector_id, secret_ref: vault://…/rotated})`；响应含 pending 字段 + `secret_ref` 候选。
- `GET /hub/v1/ops/connector/list`：每项带 `secret_ref`（vault 指针）；无明文。

## Demo

`hub-ops.js` 增 `connectorRotate`；`app.js` rotate 按钮调 Hub。

## 不做

真 vault 轮换；槽位 prod 自动切换；Spec-4b NocoBase。
