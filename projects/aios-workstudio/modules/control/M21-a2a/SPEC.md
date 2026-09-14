# M21 跨岗位委托 · A2A

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m21`

| 项 | 值 |
|----|----|
| **ID** | `m21` |
| **平面** | 编织 / 协议 |
| **决策** | P0 transfer · P1+ A2A Agent Card |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/hub.py` |
| **运行时** | P0 hub.task.transfer |
| **切片** | `harness/slices/M21.md` |
| **需求** | `harness/requirements/REQ-UAS-M21.req.md` |

## 定位

跨岗位委托不用自研总线。对端仍进对方 Hub。跨租户默认拒绝。

## 非职责

替代 Hub 门禁

## 设计方案

P0 hub.task.transfer。P1 岗位级 Agent Card。

## 技术选型

A2A 协议 · 双方 Hub OIDC

## 接口

```
hub.task.transfer
```

## 否决

- Card 签名替代门禁
- P0 上跨租户 A2A

## 验收

- 转派后源节点与审计仍在

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m21 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
