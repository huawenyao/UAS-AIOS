# Platform Console · 离线 Demo

UAS-AIOS **Suite B** 管理壳：治理平面 + 运维平面。只模拟 `hub.ops.*`。无 hub-api、NocoBase 或后端依赖。

**使用平面不在本壳内**，复用已有 WorkStudio demo：`projects/aios-workstudio/demo/`。

## 启动

必须从产品根目录起服务，三平面互相跳转才能工作：

```bash
cd projects/aios-workstudio
python -m http.server 18090
```

浏览器打开（本机 8765 可能被占用，改用任意空闲端口即可）：

| 平面 | URL |
|------|-----|
| 使用平面 | http://localhost:18090/demo/index.html |
| 治理平面 | http://localhost:18090/Console/demo/index.html#/audit |
| 运维平面 | http://localhost:18090/Console/demo/index.html#/automation |

首次或 stuck 状态可加 `?reset=1` 清空 sessionStorage。

## 页面与模块对应

| 路由 | 平面 | 模块 | 场景 |
|------|------|------|------|
| `#/overview` | 总览 | — | 三平面入口 · 健康 · 漂移夹具 |
| `#/integrate` | 控制 | M6 | 剖面 I-05 dry-run |
| `#/control` | 控制 | M6 | 租户套件 · 永久禁令 |
| `#/ontology` | 运维 | M2 | 责任图五件套校验 |
| `#/mesh` | 运维 | M7/M13/M14 | 目录 · MCP · 连接器槽 |
| `#/govern` | 治理 | M4 | Law Pack 冲突声明 |
| `#/run` | 运维 | M16/M24 | 时态摄入只读 · 模型路由 |
| `#/publish` | 治理 | M12 | ChangeSet 确认 / 驳回 |
| `#/audit` | 治理 | M11 | 检索 / 导出 / 异常巡检 |
| `#/dualtrack` | 治理 | M8 | 岗位绑定 CRUD · 升级评审 |
| `#/memory` | 治理 | M17 | 遗忘处置 → 回执可检索 |
| `#/evolution` | 治理 | M12/M4 | 信号 · 回归门禁 · 法则晋升 |
| `#/automation` | 运维 | 跨模块 | 自动化作业驾驶舱（AU-01~12） |
| `#/caliber` | 运维 | M15 | 口径草稿 / stale 重跑 |
| `#/workflows` | 运维 | M18/M19 | 长任务卡点 · 精确续跑信号 |
| `#/wm` | 运维 | M3 | 世界模型三寿命 |

设计权威：`docs/strategic/design/UAS_AIOS_CONSOLE_DEMO_DESIGN.md`。

## Demo 行为

- **ChangeSet 唯一写通道**：CRUD 与巡检建议都不静默生效；`#/publish` 确认后才 `applied=true`。auto_apply 永久 OFF。
- **自动化只产 findings**：立即运行 / 转 ChangeSet / 处置单 / 重发信号，全部入审计。
- **红线**：无证据升级 disabled；live 口径 / live WM 编辑 → `COMPILED_IMMUTABLE`；一线角色全屏锁定（看不到 `/console`）。
- **产品语言**：Demo JS 不出现零件名；SRE 逃生显示外环 / 口径引擎 / 时态图占位。

## 角色

- `admin` / `operator` / `sre` — 正常使用
- `frontline` — 全控制台锁定 overlay

## 约束

- 纯 fixture + `sessionStorage`，不发起真实 hub 请求
- 禁止 invoke_cs、kg ingest 写、Collection-as-truth
- 一线只走 WorkStudio 的 `hub.scene.*` + SSE
