# M6 Capability Hub 控制面

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m6`

| 项 | 值 |
|----|----|
| **ID** | `m6` |
| **平面** | 控制平面 |
| **决策** | 自研 · 进程 hub-api · 本产品门面 CapabilityHub |
| **本仓库角色** | 本产品实现 |
| **代码落点** | `projects/aios-workstudio/CapabilityHub` |
| **运行时** | CapabilityHub + services/hub-api（同一进程 :18088） |
| **切片** | `harness/slices/M6.md` |
| **需求** | `harness/requirements/REQ-UAS-M06.req.md` |

## 定位

所有下游的唯一门禁。剖面由路由强制。判定序不可颠倒：tenant → registry → RBAC → approval → gates → scope → execute → audit。

## 非职责

实现循环内核、持有 SoR 密钥、当 BI

## 设计方案

EnvelopeMiddleware + ProfileInjector。Thread 的 profile 不可变。hub.policy.explain 把错误码映射成人话与下一步。组合根是 Port/Adapter。

## 技术选型

FastAPI + uvicorn · 自研 PolicyChain

## 接口

```
/hub/v1/scene|exec|ops|wm|kg|metric · 信封 tenant/actor/profile/track/correlation/idempotency
```

## 否决

- Dify / Copilot Studio 当 Hub
- 一上来 OPA 当 OS
- Celery 当 Runtime 寿命
- Node 写门禁

## 验收

- scene 调写 cs → 403 + 人话
- 同一 Thread 改 profile → 409

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m6 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
