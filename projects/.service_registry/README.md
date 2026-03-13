# Shared Service Registry

本目录用于存放共享 `UASRuntimeService` 的平台级状态：

- `registry.json`：sub uas app 服务注册快照
- `queue/`：待处理与已完成的共享任务队列

目录会由运行时动态写入，但位置是平台标准的一部分。
