# M19 内环 · LangGraph 1.0

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m19`

| 项 | 值 |
|----|----|
| **ID** | `m19` |
| **平面** | 编织 / 运行 |
| **决策** | 集成默认 LangGraph · 同一 SPI |
| **本仓库角色** | 平台零件 · 不在本产品实现 |
| **代码落点** | `services/hub-api/uas_hub/adapters/inner_loop.py` |
| **运行时** | InnerLoop SPI · 默认 LangGraph |
| **切片** | `harness/slices/M19.md` |
| **需求** | `harness/requirements/REQ-UAS-M19.req.md` |

## 定位

工具回调只能进 Hub。无出站 HTTP 到 CRM。禁止第三套循环。

## 非职责

控制面、经营状态

## 设计方案

业务状态是 live WM + Task + 审计指针，不是消息数组。

## 技术选型

LangGraph 1.0 · InnerLoop SPI

## 接口

```
InnerLoop turn
```

## 否决

- CrewAI
- 第三套循环
- LangGraph 节点直打 CRM

## 验收

- I-07 无出站 CRM

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m19 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
