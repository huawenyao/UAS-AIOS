# M9 Skill 协议状态机

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m9`

| 项 | 值 |
|----|----|
| **ID** | `m9` |
| **平面** | 编织面 |
| **决策** | 自研 · discover ≠ execute |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `projects/aios-workstudio/CapabilityHub/capability_hub/skills.py` |
| **运行时** | Hub Skill 状态机 |
| **切片** | `harness/slices/M9.md` |
| **需求** | `harness/requirements/REQ-UAS-M09.req.md` |

## 定位

discover → cite → install → enable。Explore 最高只能 cited。

## 非职责

循环内核、工具实现

## 设计方案

agentskills SKILL.md 头。Pack Studio 货架漏斗。

## 技术选型

Hub 状态机

## 接口

```
hub.skill.discover|preview|cite|install|enable
```

## 否决

- Explore 直接 execute
- 第三套 Agent 循环

## 验收

- explore 不可 execute

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m9 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
