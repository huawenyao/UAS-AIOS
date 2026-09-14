# Console · Platform Console 壳

定位与契约见 [`modules/console/nocobase-shell/SPEC.md`](../modules/console/nocobase-shell/SPEC.md)。

NocoBase 是未来运行时壳，不当内核。现阶段用 **P0 HTML demo** 把 B1–B5 管理面与模块集成交互跑通；客户端只调 `hub.ops.*`。

```
demo/index.html        # P0 管理后台（总览 / 集成 / 控制 / 本体 / 能力 / 治理 / 运行 / 发布）
src/hubOps.ts          # 只再导出 packages/hub-client ops 客户端
plugin/.gitkeep        # 未来 @uas/plugin-console
```

## 启动 demo

```bash
python -m http.server 18089 --directory projects/aios-workstudio/Console/demo
# 打开 http://127.0.0.1:18089/
```

一线账号切到「一线客户经理」会看到锁页：WorkStudio 不得打开 `/console`。

不要在此创建经营 Collection，不要启 Workflow / AI / MCP Server。禁止 `invoke_cs` 与 `kg/ingest` UI。
