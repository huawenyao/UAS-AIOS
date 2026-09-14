# 企业 IdP

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `idp`

| 项 | 值 |
|----|----|
| **ID** | `idp` |
| **平面** | 身份源 |
| **决策** | 连接 · 只提供人 |
| **本仓库角色** | 外部系统 · 只连接 |
| **代码落点** | `企业 IdP` |
| **运行时** | OIDC · Hub 换绑定 |
| **切片** | `harness/slices/M8.md` |
| **需求** | `harness/requirements/REQ-UAS-M08.req.md` |

## 定位

OIDC / SAML。岗位与经营承诺权在 Hub。

## 非职责

替代责任图 org.*

## 设计方案

实验室 Keycloak。

## 技术选型

OIDC

## 接口

```
OIDC 授权码 · Hub 换绑定
```

## 否决

- 自研登录
- IdP 角色当承诺权

## 验收

- I-10

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 idp 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
