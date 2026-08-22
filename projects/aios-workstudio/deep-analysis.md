# 深度分析 · WorkStudio 三场景 × Capability Hub

> Phase 2 · SIO-MMOS · 2026-08-22

---

## 道 · 这件事在闭环的哪几步

三场景不是三个并列 App，而是 **价值闭环 7 步的产品化切分**：

```
Explore     输入 → 模拟 → 生成          问题变成可编译的主题方案
Builder     交互 → 进化（知识固化）      方案变成可运行的应用（知识即配置）
Runtime     输出 → 收益                  应用介入真实岗位，收益回流 Hub
```

道-1：缺任一场景，产品会停在对话、停在仓库或停在无反馈运行。  
道-2：三个场景读写的是同一世界模型的不同生命周期（draft / compiled / live），不是三份 RAG。  
道-3：首屏只暴露当前场景的工作对象，不把 Hub 全家桶铺开。  
道-4：Builder 的本质是把 Explore 的判断写成可运行知识；Runtime 改行为走法则/Skill，不发版。  
道-5：Explore/员工 Copilot 默认个人轨；Runtime 写库、对外、承诺走经营轨升级。  
道-6：Explore 必须同时产出 ought 与 is；Runtime 必须对冲；Builder 把对冲编进 App 的评价器。

反例：把三场景做成 WorkBuddy 式「日常/设计/代码」——那是内容类型切片，不是认知实践切片。

---

## 德 · 对谁有利、红线在哪

| 主体 | Explore | Builder | Runtime |
|------|---------|---------|---------|
| 员工 | 变强：把模糊问题做成过关方案 | 变强：把方案变成可交接应用 | 变强：在权限内完成岗位动作 |
| 组织 | 得到可审计的问题模型，而非聊天记录 | 得到可验证 subapp，而非人设 | 得到闭环与收益，而非自动化率 |
| 被作用客体 | 研究结论须标不确定 | 应用不得默认全自动伤害 | 高影响须解释、可申诉、可回滚 |

红线：Explore **禁止** cs.* 写操作；Builder **禁止** 跳过 invariant 上线；Runtime **禁止** LLM 持生产凭证；三场景都禁止把未接地陈述当事实。

---

## 势 · 张力表（本设计降低哪一侧）

| 张力 | 当前摩擦 | 设计选择 | 牺牲 |
|------|----------|----------|------|
| 已有 Skill vs 开放研究 | 工作台把能力锁在已安装目录 | Explore **不限** 已装 Skill，用方法论驱动检索与构建 | 研究过程更长、须标信源 |
| 聊天入口 vs 工作对象 | 巨头首页是对话框 | 每场景一个一级对象：Theme / App / Instance | 学习成本略高于「随便问」 |
| 构建速度 vs 可运行质量 | 低代码快但不审计 | Builder 强制走 spec harness 门禁 | 不能「一句话生成就上生产」 |
| 个人加速 vs 组织承诺 | Copilot 好用越权 | Runtime 全量 G 层；Explore 默认只读世界 | 研究爽、执行慢是故意的 |
| Hub 复杂 vs 前台降维 | 后台能力很多 | 前台只暴露当前对象 + 证据 + 门禁 | Hub 细节进「展开」 |

主摩擦：用户看不见「研究→应用→运行」是一条价值流。设计必须让 **晋升**（Promote）成为主按钮，而不是三个断开的菜单。

---

## 术 · 方法与对象流

统一对象链（人机共同语言的载体）：

```
Problem  →  ThemePack(draft WM)  →  AppBlueprint  →  AppRelease  →  AppInstance(live WM)
 Explore                         Builder                         Runtime
```

每步输出固定结构（对齐 T0）：意图理解 · 所用知识 · 证据 · 不确定点 · 建议 · 门禁 · 回滚。

方法论：Explore 内置 loop-thinking-enhanced / 五铰链 / domain_builder 分析段；Builder 内置 subapp 生产协议 + reqharness 七阶段；Runtime 内置认知循环 7 步读写 live WM。

智能投放：Explore 按问题价值加深（与千问 41 分钟 / WorkBuddy 7 分钟同一机制，但是场景内路由，不是产品站队）。

---

## 器 · 必须被体验到的结构

1. WorkStudio Shell：场景切换器 + 当前对象 + 五维条 + 证据盒 + 环位。  
2. Capability Hub：同一中枢，三套 **策略剖面**（explore / builder / runtime），不是三套系统。  
3. Promote 动作：ThemePack → Builder；AppRelease → Runtime。失败要写原因（invariant / 门禁 / 五维缺失）。  
4. 治理可见：草稿 / 要批 / 禁止 必须在 Runtime 主路径，Explore 以「不确定」为主路径。

---

## 综合洞察

WorkBuddy 的工作台切的是 **交付物类型**（文档、代码、设计）。  
WorkStudio 切的是 **认知实践阶段**（研究、编译、运行）。

这是品类句「过关的工作」的器层落地：过关先有问题模型（Explore），再有可运行法则（Builder），最后有带权运行（Runtime）。Capability Hub 是编译器后端；三场景是编译器的三个操作模式。
