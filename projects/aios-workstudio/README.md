# AIOS WorkStudio

营销作战台产品仓。架构服从 [`docs/strategic/design/uas-aios-cluster.html`](../../docs/strategic/design/uas-aios-cluster.html)。

**三张平面，只通过协议说话。本仓不复制零件内核。**

| 平面 | 本仓落点 | 一线能看见 |
|------|----------|------------|
| 使用平面 | `packages/workstudio-web` · `demo/` | 今日必办 / 作战室 / 指挥舱 |
| 控制平面 | `CapabilityHub/` | 无（只经 hub.*） |
| Console 壳 | `Console/demo/` | 知识管理员；一线默认不可进 |
| 配置与运维零件 | **不在本仓实现** | 见 `modules/ops/*/SPEC.md` |

## 模块定位（总表）

见 [`modules/README.md`](./modules/README.md)。每个模块一份 `SPEC.md`：定位、非职责、设计、选型、接口、否决、验收。

本仓库角色：

| 角色 | 含义 | 例子 |
|------|------|------|
| 本产品实现 | 代码写在这里 | M1 WorkStudio、M6 CapabilityHub 门面 |
| 本产品组合 | UI 在此，内核在 Hub | M5 签发台、进度 SSE |
| 只经 hub.* 消费 | 禁止直连零件 | M2 责任图、M15 Cube |
| Console 壳 | NocoBase，不当内核 | 本体 / 法则 / 口径页 |
| 平台零件 | `services/` | Temporal / LangGraph / Connector |
| 外部系统 | 只连接 | IdP、客户 CRM |

## 目录

```
projects/aios-workstudio/
  demo/                      P0 作战台 HTML 壳
  packages/workstudio-web/   产品路径 Vite+TS
  packages/hub-client/       北向 scene 客户端 + Console ops 客户端
  CapabilityHub/             T1 Hub 门面（复用 uas_hub）
  Console/                   Platform Console：P0 demo + ops 客户端 + NocoBase 占位
  modules/                   30 模块 SPEC（从集群图生成）
```

## 启动

```bash
python projects/aios-workstudio/CapabilityHub/run.py
# Hub: http://127.0.0.1:18088/health
# 作战台 P0: 打开 demo/index.html?hub=http://127.0.0.1:18088
python -m http.server 18089 --directory projects/aios-workstudio/Console/demo
# Console P0: http://127.0.0.1:18089/
```

## 生成 SPEC

```bash
python projects/aios-workstudio/modules/gen_specs.py
python -m unittest discover -s projects/aios-workstudio/tests -v
```
