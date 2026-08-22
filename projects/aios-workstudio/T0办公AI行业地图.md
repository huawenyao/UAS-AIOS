# AIOS WorkStudio · 办公 AI 行业地图（T0 附录）

> 作用：把 2026-08 的 harness / 办公产品对照落盘，供 `T0产品定义.md` 与 `T0竞争焦点与领先路径.md` 引用。  
> 不是产品契约。结论以那两份 T0 为准。  
> 日期：2026-08-22

---

## 1. 能力公式

```
OfficeAgent = Model × Harness × Context × Tools × Policy × Interface
```

模型可替换。后五项才是产品资产。OpenAI 2026-08-20：应用拥有界面、业务规则、系统记录；Codex harness 拥有循环、沙箱、事件、审批暂停。Harness 会改分数：保留推理 + 压缩，GPT-5.6 Sol 在 ARC-AGI-3 从 13.3% → 38.3%，输出 token 约 1/6。

---

## 2. 开发者 harness（循环层）

| | Codex | Claude Code | OpenClaw | Hermes |
|--|-------|-------------|---------|--------|
| 哲学 | 循环做成别人产品里的引擎 | 最干净的编码交付 | Agent 活在已有通道 | 用得越久越懂你 |
| 运行时 | Rust Codex core | TS 单线程循环 | 嵌入 Pi `AgentSession` | Python `AIAgent` |
| 协议 | App Server JSON-RPC；Thread / Turn / Item | Agent SDK + CLI | Gateway WS | CLI / Gateway / ACP |
| Skill | 元数据进 prompt，正文按需 | YAML 头常驻，正文按需 | ClawHub + 三层目录 | 索引常驻，可自创写回 |
| 记忆 | Thread 事件史 | CLAUDE.md 每轮重注 | MEMORY.md + 日记 | MEMORY/USER + Honcho |
| 不做 | 不强迫所有工作进聊天框 | 不做操作员 OS | 不为纯 Git 做最薄壳 | 不为单一编码做最强约束 |

公共原语已收敛：Agent Loop、`SKILL.md` 渐进披露、`AGENTS.md`/`CLAUDE.md`、MCP、沙箱+审批、compact、subagent、cron/heartbeat。`agentskills.io` 是最接近知识协议的公共层。

Skill 支持不足的根因：缺渐进披露加载、缺稳定循环原语、权限在循环外、产品把人格当世界模型。用 OpenClaw/Hermes/Pi **替换循环层**合理；用它们 **替换世界模型 / 治理** 是错层。

---

## 3. 办公产品（前台层）

同一具身智能周报（2026-08-12 评测）：WorkBuddy 7 分钟、TRAE Work 16 分钟、千问办公 41 分钟。耗时是智能投入策略，不是能力排名。

| 产品 | 用户假设 | Agent 角色 | 失败模式 |
|------|----------|------------|----------|
| WorkBuddy | 要下午能改的初稿 | 高效执行者 | 没找到 ≈ 没发生 |
| TRAE Work | 要更宽的信息网 | 信息助手 | 链接多 ≠ 密度 |
| 千问办公 | 要敢信的判断过程 | 判断协作者 | 链路重、Token 贵 |

积木同构：工作台、Skill、专家/套件、连接器、IM 遥控、定时、项目/企业空间。  
阿里千问办公 = QoderWork（本地）+ 悟空（IM）+ MuleRun（云端长程）。腾讯 WorkBuddy Enterprise = CodeBuddy + WorkBuddy + Managed Agents（云端 harness）。办公被选中，因为高频、刚需、嵌生产流程，距离 Token 闭环最近。

三种用户假设都会长期存在。成熟形态是按任务价值动态加深，而不是站队。

---

## 4. 不可约简的阻力

1. 注意力稀缺：不能每件事 41 分钟。  
2. 判断可分担、承诺不可外包：必须带证据、边界、取舍。  
3. 上下文守恒：知识必须渐进披露。  
4. 复杂度守恒：界面变简单，循环和治理必须变厚。  
5. 信任不对称：一次胡说吃掉一周效率红利。

---

## 5. 对 WorkStudio 的直接推论

- 前台可像工作台，以免用户失语；后台必须是可执行商业世界模型。  
- 循环外购（Codex / Pi 级），法则、五维、双轨、门禁自有。  
- 心智不抢「AI 同事」，抢「过关的工作」。  
- 市场不抢 2000 万白领面积，先抢一条岗位闭环。

详见 `T0竞争焦点与领先路径.md`。
