# M8 Identity & Policy

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m8`

| 项 | 值 |
|----|----|
| **ID** | `m8` |
| **平面** | 治理面 |
| **决策** | 自研绑定 · 身份源接 IdP |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/adapters/iam.py` |
| **运行时** | Hub IAM 绑定 · IdP 只提供人 |
| **切片** | `harness/slices/M8.md` |
| **需求** | `harness/requirements/REQ-UAS-M08.req.md` |

## 定位

岗位绑定责任图 org.*。双轨分名。无岗位绑定的人打不开切片。

## 非职责

当 IdP；用 Entra 组替代 org.*

## 设计方案

OIDC 只提供人。经营承诺权在 Hub。权限变更走 permissionChangeSet。

## 技术选型

Keycloak 实验室 / 企业 Entra·Okta

## 接口

```
hub.ops.iam.bindings · hub.iam.*
```

## 否决

- 自研登录
- 把 IdP 角色当经营承诺权

## 验收

- I-10 无岗位打不开切片

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m8 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
