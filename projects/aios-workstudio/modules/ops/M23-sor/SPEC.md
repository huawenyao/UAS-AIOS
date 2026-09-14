# M23 主数据 SoR

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m23`

| 项 | 值 |
|----|----|
| **ID** | `m23` |
| **平面** | 系统面 |
| **决策** | 连接，不自研 MDM |
| **本仓库角色** | 外部系统 · 只连接 |
| **代码落点** | `客户 CRM/ERP/仓` |
| **运行时** | 只存 object_ref |
| **切片** | `harness/slices/M23.md` |
| **需求** | `harness/requirements/REQ-UAS-M23.req.md` |

## 定位

UAS 只存 object_ref 与映射，不复制客户主档。

## 非职责

轻量 CRM 当 P0

## 设计方案

默认沙箱 Mock Connector。

## 技术选型

客户已有 CRM / ERP / 仓

## 接口

```
厂商 API 仅连接器内
```

## 否决

- 自研轻量 CRM
- 主档搬进 NocoBase 主库

## 验收

- object_ref 不复制主档

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m23 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
