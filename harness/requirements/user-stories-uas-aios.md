# UAS-AIOS 平台用户故事

> 产品权威：[`UAS_AIOS_PLATFORM_PRODUCT.md`](../../docs/strategic/design/UAS_AIOS_PLATFORM_PRODUCT.md)  
> 日期：2026-09-10 · 状态：P0 故事待实现

格式：作为…我想…以便… / Given-When-Then / 界面或接口 / 优先级

---

## 套件 A · WorkStudio（使用）

### US-A-01 打开即见今日必办
作为客户经理，我想打开工作台就看到本岗位本周期卡住的节点，以便不用先聊天或翻报表。  
- Given 已绑定 `pos-cm` 且样例图已发布  
- When 进入 `/today`  
- Then 调用 `hub.scene.pack.open`，gate 节点上浮  
- 界面：WorkStudio / 今日必办 · 接口：C1 pack.open · P0

### US-A-02 客户作战室只读 360
作为客户经理，我想按客户看到责任节点与时间线投影，以便判断卡在哪。  
- Given 已知 `object_ref`  
- When 打开 `/room/:object_ref`  
- Then 只读节点 + `hub.kg.search` 投影，无写按钮可生效  
- 界面：作战室 · P0

### US-A-03 下拆必须接地
作为客户经理，我想对 gate 节点下拆原因，以便建议带证据。  
- Given 节点五维齐全  
- When `insight.drill`  
- Then 返回 Insight；`grounded=false` 不能进入派活  
- 界面：洞察卡接地灯 · P0

### US-A-04 一键派活不写系统
作为客户经理，我想确认后派给 BD，以便活有主且尚未改 CRM。  
- Given Insight `grounded=true`  
- When `task.issue`  
- Then Task=`issued`，无 workflow，SoR 无写  
- 界面：签发抽屉 · P0

### US-A-05 场景点写要人话
作为客户经理，我想在作战台误点「改 CRM」时被拦住并告诉我下一步，以便去签发而不是找 IT。  
- When scene 调写 cs  
- Then 403 + `hub.policy.explain` 展示「请签发后进入运行」  
- 界面：人话条 · P0

### US-A-06 待我确认
作为客户经理，我想在 L2 动作上点确认/驳回，以便人在回路。  
- Given 任务 awaiting_approval  
- When `cycle_step` approved|rejected  
- Then 工作流继续或停止；一线不见 workflow_id  
- 界面：待你确认 · P1

### US-A-07 办完回流
作为客户经理，我想再次打开同一客户时看到指标已变，以便知道活办成了。  
- Given 运行写 SoR 成功  
- When 再次 pack.open  
- Then 同一 `node_id` 的 `kpi.is` 已更新或标 stale  
- 界面：作战室 · P1

### US-A-08 指挥舱子树
作为销售总监，我想按组织/阶段看堵塞，以便调配而不是另开一套报表。  
- When 打开 `/command`  
- Then 责任图投影 `org_cascade`/`kpi_split`，可 `task.transfer`  
- 界面：指挥舱 · P1

### US-A-09 进度可见
作为客户经理，我想看到运行进度，以便不用问「AI 在干什么」。  
- When 任务已 open  
- Then SSE `/hub/v1/exec/{task_id}/events`  
- 界面：进度条 · P1

### US-A-10 个人记忆可删
作为员工（SelfPaw），我想删除个人备忘并拿到回执入口提示，以便行使遗忘。  
- Given track=selfpaw  
- When `memory.self.forget`  
- Then 回执产生；经营节点不变  
- 界面：个人区 · P2

### US-A-11 无岗位打不开
作为未绑定岗位的登录用户，我想被拒绝而不是看空白图，以便去找管理员开通。  
- Then 403，引导联系平台管理员  
- 界面：工作台空态 · P0

---

## 套件 B · Platform Console（运营管理）

### US-B-01 试运行门禁
作为平台管理员，我想输入「若现在 scene 写拜访」并看到人话结果，以便给业务解释规则。  
- 界面：控制 / 试运行 · 接口：`hub.ops.policy.explain` · P0

### US-B-02 剖面矩阵
作为平台管理员，我想一眼看到四剖面的读/写/检索策略，以便检查配置没有复制四套中心。  
- 界面：控制 / 剖面 · `hub.ops.profile.matrix` · P0

### US-B-03 租户开通套件
作为平台管理员，我想开通某租户的 WorkStudio / Console / Services，以便按套件交付。  
- 界面：控制 / 租户 · `hub.ops.tenant.get` · P1

### US-B-04 编辑责任图并发布
作为知识管理员，我想改节点五件套并提交发布，以便下次作战台生效且必须有人确认。  
- When publish  
- Then 只出现 ChangeSet，不立刻改 compiled  
- 界面：本体 / 责任图 · `hub.ops.graph.publish` · P1

### US-B-05 寿命对照
作为知识管理员，我想对照 draft/compiled/live，以便发现有人试图用 live 改法则。  
- 界面：本体 / WM · 禁 live→compiled 按钮 · P1

### US-B-06 法则版本对比
作为知识管理员，我想看条文 diff 和冲突声明，以便评审 ChangeSet。  
- 界面：本体 / Law · `hub.ops.law.diff` · P2

### US-B-07 启用能力
作为平台管理员，我想停用某写操作或提升审批级，以便租户策略可运营。  
- Then 经 ChangeSet；MCP list 随后变化  
- 界面：能力 / 目录 · `hub.ops.registry.patch` · P0

### US-B-08 预览模型能看见的工具
作为平台管理员，我想按剖面预览 tools/list，以便确认场景没有写工具。  
- 界面：能力 / MCP · `hub.ops.mcp.preview` · P1

### US-B-09 连接器槽与轮换
作为值班/实施，我想切换沙箱/生产并轮换凭证且看不到明文，以便安全接入 SoR。  
- 界面：能力 / 连接器 · `hub.ops.connector.slot|rotate` · P1

### US-B-10 契约漂移红灯
作为实施顾问，我想在发布前看到 schema 与 MCP 是否一致，以便禁止带病发布。  
- 界面：能力 / 契约 · `hub.ops.schema.drift` · P0

### US-B-11 岗位绑定
作为平台管理员，我想把 IdP 人绑到责任图岗位，以便无绑定者打不开切片。  
- 界面：治理 / 岗位 · `hub.ops.iam.bindings` · P0

### US-B-12 审计导出
作为合规官，我想按 correlation/node/cs 导出合规包，以便定责；这不是 KPI 墙。  
- 界面：治理 / 审计 · `hub.ops.audit.export` · P1

### US-B-13 确认或驳回变更
作为知识管理员或平台管理员，我想在发布中心处理 ChangeSet，以便法则/目录/口径受控生效。  
- Then `auto_apply` 不存在  
- 界面：发布 · `hub.ops.changeset.decide` · P1

### US-B-14 遗忘回执检索
作为合规官，我想按人检索 forget 回执，以便证明已删个人记忆且未改责任图。  
- 界面：治理 / 遗忘 · `hub.ops.memory.receipt.get` · P2

### US-B-15 按任务查运行
作为值班，我想用 task_id 或源节点查长任务和滞留，以便续跑；不把 Temporal UI 给业务。  
- 界面：运行 / 任务 · `hub.ops.runtime.task.get` `retry` · P1

### US-B-16 口径 stale 告警
作为值班，我想看到哪些 KPI 在用缓存，以便业务菜单上的 stale 灯有后台解释。  
- 界面：运行 / 口径 · `hub.ops.caliber.status` · P1

### US-B-17 时态摄入监视
作为知识运营，我想看到 episode 延迟和失败，以便 Explore 接地可用。  
- 界面：运行 / 时态 · `hub.ops.kg.ingest_status` · P1

### US-B-18 模型路由
作为平台管理员，我想按剖面切换模型且不出现在一线菜单，以便可换模型。  
- 界面：运行 / 模型 · `hub.ops.model.route` + ChangeSet · P2

### US-B-19 Skill 货架
作为知识管理员，我想看到 discover→cited→enabled 漏斗，以便 Explore 没有误执行。  
- 界面：治理 / Skill · P2

### US-B-20 制品不可回放经营
作为构建者，我想晋升 Theme/Release，但不能用报告当 pack 状态。  
- 界面：治理 / 制品 · P2

### US-B-21 禁止关审计
作为平台管理员，我在界面上找不到「关闭审计」或「自动应用法则」。  
- 界面：全局 · P0

---

## 套件 C · System Services（系统服务）

### US-C-01 应用只走 hub 北向
作为前端，我只实现 C1，不链零件 SDK。  
- 接口：§9.1 · P0

### US-C-02 Agent 只见 cs 名
作为内环模型，我通过 MCP 调 `cs.*`，call 仍过门禁。  
- 接口：C3 · 运营预览 US-B-08 · P1

### US-C-03 ETL 摄入不是写 CRM
作为数据工程，我推 episode 到 `hub.kg.ingest_episode`，不调用写 cs。  
- 接口：C4 · P1

### US-C-04 IdP 只提供人
作为企业 IAM，我只做 OIDC；经营写权不在 IdP 组。  
- 接口：C5 · P0

### US-C-05 服务账号分权
作为安全，我要求 ETL 账号不能 `task.issue`，一线账号不能 `connector.rotate`。  
- 见产品定义 §10 · P0

### US-C-06 错误码稳定
作为集成方，我依赖规格错误码与 explain，而不是 HTTP 500 文本。  
- P0

### US-C-07 零件 UI 非产品
作为 SRE，我仅在授权逃生通道打开 Temporal/Cube/Neo4j UI，且每次进入审计。  
- 界面：Console 默认不链出 · P1

### US-C-08 契约浏览器
作为实施，我在 Console 打开 OpenAPI/MCP 清单与变更日志，而不另做门户。  
- 界面：能力 / 契约浏览器 · P1
