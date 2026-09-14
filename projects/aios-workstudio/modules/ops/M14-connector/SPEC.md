# M14 System Connector

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m14`

| 项 | 值 |
|----|----|
| **ID** | `m14` |
| **平面** | 系统面 |
| **决策** | 自研适配器 SPI |
| **本仓库角色** | 平台零件 · 不在本产品实现 |
| **代码落点** | `services/hub-api/uas_hub/adapters/connector.py` |
| **运行时** | 每 SoR 一进程（阶段 B） |
| **切片** | `harness/slices/M14.md` |
| **需求** | `harness/requirements/REQ-UAS-M14.req.md` |

## 定位

密钥只在本进程读 KMS 引用。写必须幂等键。WorkStudio 永不直连。

## 非职责

自研 CRM/ERP；对模型暴露 REST

## 设计方案

字段映射 YAML。一线菜单不得出现连接器。

## 技术选型

httpx + 有限重试

## 接口

```
内部 Invoke · hub.ops.connector.list/rotate/slot
```

## 否决

- 在 LangGraph 节点里 httpx CRM
- 生产凭证写进 Demo

## 验收

- Worker 环境无 SoR 明文

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m14 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
