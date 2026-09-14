/** Platform Console demo fixtures. 真相仍应走 hub.ops.*；本文件只服务离线演示。 */
window.CONSOLE_DATA = {
  tenant: {
    tenant_id: "t-hengchuan",
    name: "恒川 LTC",
    suites: ["WorkStudio", "Platform Console", "System Services"],
    period: { grain: "month", from: "2026-08-01", to: "2026-08-31" },
    graph_id: "ag-hengchuan-ltc",
    world_model_id: "wm-hengchuan-ltc",
    position_id: "pos-cm",
  },

  roles: [
    { id: "knowledge_admin", label: "知识管理员", sees: ["overview", "integrate", "ontology", "mesh", "run", "publish"] },
    { id: "platform_admin", label: "平台管理员", sees: ["overview", "integrate", "control", "mesh", "publish"] },
    { id: "compliance", label: "合规", sees: ["overview", "integrate", "govern", "publish"] },
    { id: "sre", label: "SRE", sees: ["overview", "integrate", "run", "mesh"] },
    { id: "frontline", label: "一线客户经理", sees: [] },
  ],

  pages: [
    { id: "overview", label: "总览", stamp: "HEALTH", hint: "平面 SLO，不暴露零件名" },
    { id: "integrate", label: "集成", stamp: "Π", hint: "模块只通过协议说话" },
    { id: "control", label: "控制 B1", stamp: "HUB", hint: "剖面 · 试运行 · 门禁" },
    { id: "ontology", label: "本体 B2", stamp: "ONTOLOGY", hint: "责任图 · WM · 法则" },
    { id: "mesh", label: "能力 B3", stamp: "MESH", hint: "目录 · MCP · 连接器" },
    { id: "govern", label: "治理 B4", stamp: "GOV", hint: "身份 · 审计 · 技能 · 制品" },
    { id: "run", label: "运行 B5", stamp: "RUNTIME", hint: "任务寿命 · 口径 · 时态" },
    { id: "publish", label: "发布", stamp: "CHANGESET", hint: "所有配置写的汇合点" },
  ],

  health: {
    use: { open_ms: 860, issue_to_progress_ms: 2100, ungrounded_rate: 0.08 },
    control: { explain_coverage: 1, gate_p95_ms: 42, forbid_403: 18 },
    runtime: { approval_stuck: 2, retry_ok: 1 },
    caliber: { stale_nodes: 1, as_of: "2026-08-31" },
    compliance: { forget_receipt: 1, missing_receipt: 0 },
  },

  profiles: {
    scene: { cs_write: false, skill_execute: false, skill_max: "previewed", artifacts: ["insight", "task"], loop: "看见并办成" },
    explore: { cs_write: false, skill_execute: false, skill_max: "cited", artifacts: ["theme"], loop: "长文红队" },
    builder: { cs_write: "dry-run", skill_execute: true, skill_max: "installed", artifacts: ["blueprint", "release"], loop: "可重复可验证" },
    runtime: { cs_write: true, skill_execute: true, skill_max: "executed", artifacts: ["instance"], loop: "低漂移可打断" },
  },

  chain: ["tenant", "registry", "RBAC", "approval", "gates", "scope", "execute", "audit"],

  explain: {
    PROFILE_FORBIDS_SIDE_EFFECT: { message: "现在是作战台，不能改 CRM。请签发任务后进入运行。", next: "hub.scene.task.issue" },
    UNGROUNDED_INSIGHT: { message: "建议还没有证据，不能派活。", next: "补时间线或口径证据后再 drill" },
    WM_INCOMPLETE: { message: "这个位置还没建模完整（缺五维），不能签发。", next: "请知识管理员补世界模型投影" },
    MEMORY_TRACK_FORBIDDEN: { message: "经营轨道不能读个人记忆。", next: "使用岗位上下文而不是个人备忘" },
    SKILL_NOT_EXECUTABLE_IN_PROFILE: { message: "当前剖面最高只能引用技能，不能执行。", next: "安装后在 runtime 执行" },
    GATE_BLOCKED: { message: "治理门禁拒绝了这次调用。", next: "查看审计与门禁说明" },
    INVARIANT_FAILED: { message: "发布前检查没过，不能进入运行。", next: "补五件套或口径后再提交 ChangeSet" },
  },

  ops: [
    { id: "cs.customer.get_profile", write: false, level: "L1", gates: ["G1", "G6"], effects: [] },
    { id: "cs.visit.list", write: false, level: "L1", gates: ["G1"], effects: [] },
    { id: "cs.metric.query", write: false, level: "L1", gates: ["G1"], effects: [] },
    { id: "cs.visit.schedule", write: true, level: "L2", gates: ["G1", "G6"], effects: ["event.visit.scheduled"] },
    { id: "cs.approval.submit", write: true, level: "L2", gates: ["G1", "G6"], effects: ["event.approval.submitted"] },
    { id: "cs.approval.approve", write: true, level: "L3", gates: ["G6", "G7"], effects: [] },
    { id: "cs.notify.send_im", write: true, level: "L2", gates: ["G1", "G6"], effects: ["event.notify.sent"] },
  ],

  graph: {
    graph_id: "ag-hengchuan-ltc",
    nodes: [
      {
        node_id: "an-cm-portfolio",
        parent_id: null,
        goal: { statement: "客户经理组合近30天消耗与转化达标", horizon: "2026-08" },
        org: { unit_id: "ou-customer-success", position_id: "pos-cm", owner_id: "cowen.hua", raci: "A" },
        kpi: { kpi_id: "kpi-spend", name: "消耗", unit: "USD", caliber: "Σspend(bus_mtc,近30天)", ought: 5000000, is: 4290000, delta: 0.124, status: "watch", stale: false },
        process: { value_stream: "LTC", stage: null, cs_read: ["cs.customer.get_profile", "cs.metric.query"], cs_write: [] },
        wm: { space: "cm.ltc", time: "近30天", subject: "cowen.hua", object: "portfolio", feedback: "spend_vs_target" },
        object_refs: ["UEC-10293", "UEC-20114", "UEC-30021"],
      },
      {
        node_id: "an-stage-visit",
        parent_id: "an-cm-portfolio",
        goal: { statement: "拜访阶段停留不超过14天且决策链覆盖", horizon: "stage-SLA" },
        org: { unit_id: "ou-customer-success", position_id: "pos-cm", owner_id: "cowen.hua", raci: "R" },
        kpi: { kpi_id: "kpi-visit-dwell", name: "拜访阶段停留天数", unit: "day", caliber: "now - stage_entered_at", ought: 14, is: 28, status: "gate", stale: true },
        process: { value_stream: "LTC", stage: "03_拜访", cs_read: ["cs.visit.list"], cs_write: ["cs.visit.schedule"] },
        wm: { space: "cm.ltc.visit", time: "SLA-14d", subject: "cowen.hua + BD", object: "UEC-10293", feedback: "days_in_stage" },
        object_refs: ["UEC-10293"],
      },
    ],
    edges: [{ from: "an-cm-portfolio", to: "an-stage-visit", kind: "kpi_split" }],
  },

  wm: {
    world_model_id: "wm-hengchuan-ltc",
    draft: { version: 2, space: "cm.ltc", time: "近30天", subject: "pos-cm", object: "account", feedback: "ought/is", laws: ["LP-VISIT-14", "LP-NO-UNGROUNDED"] },
    compiled: { version: 1, space: "cm.ltc", time: "近30天", subject: "pos-cm", object: "account", feedback: "ought/is", laws: ["LP-VISIT-14"] },
    live: { version: 1, patch: "visit_dwell=28d · UEC-10293", subject: "cowen.hua", object: "UEC-10293" },
  },

  laws: {
    current: { id: "LP-VISIT-14", version: "1.2", text: "拜访阶段停留 > 14 天 → 节点 status=gate，禁止口头改口径。" },
    next: { id: "LP-VISIT-14", version: "1.3-draft", text: "拜访阶段停留 > 14 天 → status=gate；决策链未覆盖时不得签发 cs.visit.schedule。" },
  },

  skills: [
    { id: "sk-visit-brief", name: "拜访简报", state: "enabled", profile_max: { explore: "cited", builder: "installed", runtime: "executed" } },
    { id: "sk-quote-guard", name: "报价红线", state: "installed", profile_max: { explore: "cited", builder: "installed", runtime: "executed" } },
    { id: "sk-redteam", name: "口径红队", state: "cited", profile_max: { explore: "cited", builder: "installed", runtime: "executed" } },
  ],

  artifacts: [
    { kind: "Insight", id: "ins-an-stage-visit-20260822", status: "grounded" },
    { kind: "Task", id: "task-visit-uec-10293", status: "issued" },
    { kind: "ThemePack", id: "theme-ltc-visit", status: "draft" },
    { kind: "Blueprint", id: "bp-cm-ltc", status: "compiled" },
    { kind: "Release", id: "rel-cm-2026-08", status: "live" },
  ],

  connectors: [
    { id: "connector.crm.sandbox", slot: "sandbox", status: "up", secret: "kms://crm/sandbox#v3" },
    { id: "connector.crm.prod", slot: "prod", status: "standby", secret: "kms://crm/prod#v1" },
    { id: "connector.dwh.cube", slot: "sandbox", status: "stale", secret: "kms://dwh/cube#v2" },
  ],

  bindings: [
    { actor: "cowen.hua", position: "pos-cm", org: "ou-customer-success", track: "pipaw" },
    { actor: "knowledge.admin", position: "pos-knowledge", org: "ou-platform", track: "scene" },
    { actor: "lin.sre", position: "pos-sre", org: "ou-platform", track: "scene" },
  ],

  audit: [
    { ts: "2026-09-11T08:12:03Z", corr: "corr-7f21", type: "cs.invoked", node: "an-stage-visit", cs: "cs.visit.list", profile: "runtime" },
    { ts: "2026-09-11T08:12:41Z", corr: "corr-7f21", type: "PROFILE_FORBIDS_SIDE_EFFECT", node: "an-stage-visit", cs: "cs.visit.schedule", profile: "scene" },
    { ts: "2026-09-11T09:01:10Z", corr: "corr-8aa0", type: "ops.changeset.submitted", node: null, cs: null, profile: "builder" },
    { ts: "2026-09-11T09:40:22Z", corr: "corr-91c2", type: "memory.forgotten", node: null, cs: null, profile: "selfpaw" },
  ],

  receipts: [
    { id: "rec-forget-20260911", actor: "selfpaw:cowen.hua", at: "2026-09-11T09:40:22Z", scope: "personal_notes", status: "archived" },
  ],

  transfers: [
    { task_id: "task-visit-uec-10293", from: "pos-cm", to: "pos-bd", node: "an-stage-visit", at: "2026-09-10T16:02:00Z" },
  ],

  runtime: [
    { task_id: "task-visit-uec-10293", node: "an-stage-visit", state: "waiting_human", sla_hours: 18, label: "待你确认" },
    { task_id: "task-quote-uec-20114", node: "an-cm-portfolio", state: "running", sla_hours: 4, label: "执行中" },
  ],

  caliber: [
    { kpi_id: "kpi-spend", as_of: "2026-08-31", stale: false, yaml: "configs/metrics/osi/kpi-spend.yml" },
    { kpi_id: "kpi-visit-dwell", as_of: "2026-08-22", stale: true, yaml: "configs/metrics/osi/kpi-visit-dwell.yml" },
  ],

  kg: { lag_s: 90, last_episode: "ep-visit-uec-10293", whitelist: ["Account", "Visit", "DecisionMaker"] },

  models: [
    { profile: "scene", model: "qwen-plus", rpm: 60 },
    { profile: "explore", model: "qwen-max", rpm: 20 },
    { profile: "builder", model: "qwen-plus", rpm: 30 },
    { profile: "runtime", model: "qwen-plus", rpm: 40 },
  ],

  changesets: [
    {
      id: "cs-20260911-01",
      target: "law_pack",
      title: "拜访 14 天法则增加决策链覆盖",
      submitted_by: "knowledge.admin",
      applied: false,
      auto_apply: false,
      status: "pending",
      invariant: "pass",
    },
    {
      id: "cs-20260911-02",
      target: "caliber",
      title: "kpi-visit-dwell 水合窗口改为 T+0",
      submitted_by: "knowledge.admin",
      applied: false,
      auto_apply: false,
      status: "pending",
      invariant: "fail",
    },
  ],

  protocols: [
    { id: "n", name: "北向 hub.*", use: "使用平面 ↔ Hub", color: "n" },
    { id: "s", name: "南向 MCP / cs.*", use: "Hub ↔ 连接器 / SoR", color: "s" },
    { id: "e", name: "东向外环", use: "长任务寿命 / 人在回路", color: "e" },
    { id: "w", name: "西向内环", use: "InnerLoop SPI", color: "w" },
    { id: "k", name: "知识向", use: "口径 / 时态 / 记忆", color: "k" },
    { id: "h", name: "水平 A2A", use: "跨岗位委托", color: "h" },
    { id: "i", name: "身份 OIDC", use: "人进 Hub，承诺权在岗位", color: "i" },
    { id: "v", name: "演化 ChangeSet", use: "配置写的唯一出口", color: "v" },
  ],

  flows: [
    { id: "control", name: "控制流", carry: "剖面、track、审批、门禁、Thread", ban: "SoR 密钥、SQL" },
    { id: "data", name: "数据流", carry: "责任图切片、kpi.is、证据、Task、live 补丁", ban: "聊天全文当状态" },
    { id: "manage", name: "管理流", carry: "Pack 版本、连接器启用、口径 YAML、ChangeSet", ban: "后台直接改生产 JSON" },
  ],

  isolations: [
    "个人记忆 ↛ 责任图 / 时态图 / 口径",
    "时态图 mutation ↛ cs.* 写",
    "口径 ↛ 签发 Task",
    "外环运行时 ↛ 解释 Law Pack",
    "WorkStudio ↛ 直连任何零件",
  ],

  modules: [
    { id: "m1", t: "WorkStudio", plane: "use", proto: "n", manage: "使用平面产品，无连接器页", api: "hub.scene.* + SSE" },
    { id: "m6", t: "Capability Hub", plane: "ctrl", proto: "n", manage: "B1 控制中心", api: "信封 + 判定序" },
    { id: "m2", t: "责任图", plane: "ops", proto: "n", manage: "本体工作室块 1", api: "hub.ops.graph.*" },
    { id: "m3", t: "WM Store", plane: "ops", proto: "n", manage: "寿命板", api: "hub.ops.wm.get" },
    { id: "m4", t: "Law Pack", plane: "ops", proto: "v", manage: "Pack Studio 法则页", api: "hub.ops.law.diff" },
    { id: "m5", t: "Insight→Task", plane: "use", proto: "n", manage: "签发台（嵌作战台）", api: "insight.drill / task.issue" },
    { id: "m7", t: "Registry cs.*", plane: "ctrl", proto: "s", manage: "能力目录", api: "hub.ops.registry.*" },
    { id: "m8", t: "IAM / Policy", plane: "ctrl", proto: "i", manage: "岗位绑定", api: "hub.ops.iam.bindings" },
    { id: "m9", t: "Skill 状态机", plane: "ctrl", proto: "n", manage: "技能货架", api: "hub.ops.skill.*" },
    { id: "m10", t: "Artifact", plane: "ctrl", proto: "n", manage: "制品晋升条", api: "hub.ops.artifact.*" },
    { id: "m11", t: "Audit", plane: "ctrl", proto: "n", manage: "审计台", api: "hub.ops.audit.*" },
    { id: "m12", t: "Evolution", plane: "ctrl", proto: "v", manage: "演化台", api: "hub.ops.changeset.*" },
    { id: "m13", t: "MCP Gateway", plane: "ctrl", proto: "s", manage: "剖面工具预览", api: "hub.ops.mcp.preview" },
    { id: "m14", t: "Connector", plane: "ops", proto: "s", manage: "连接器槽", api: "hub.ops.connector.*" },
    { id: "m15", t: "口径", plane: "ops", proto: "k", manage: "口径运营", api: "hub.ops.caliber.status" },
    { id: "m16", t: "时态知识", plane: "ops", proto: "k", manage: "摄入监视", api: "hub.ops.kg.ingest_status" },
    { id: "m17", t: "个人记忆", plane: "ops", proto: "k", manage: "遗忘回执", api: "hub.ops.memory.receipt" },
    { id: "m18", t: "外环运行时", plane: "ops", proto: "e", manage: "按任务检索", api: "hub.ops.runtime.task" },
    { id: "m19", t: "内环", plane: "ops", proto: "w", manage: "后端开关（SRE）", api: "InnerLoop SPI" },
    { id: "m20", t: "Schema", plane: "ctrl", proto: "s", manage: "契约漂移灯", api: "hub.ops.schema.drift" },
    { id: "m21", t: "A2A / 转派", plane: "ctrl", proto: "h", manage: "岗位委托运营", api: "hub.task.transfer" },
    { id: "m24", t: "模型路由", plane: "ops", proto: "w", manage: "按剖面限流", api: "hub.ops.model.route" },
  ],

  integrations: [
    { id: "I-01", pair: "WorkStudio ↔ Hub", pass: "作战台零零件 SDK；断零件人话降级", demo: "n" },
    { id: "I-02", pair: "Hub ↔ 责任图", pass: "pack.open 缺维不能签发", demo: "n" },
    { id: "I-03", pair: "Hub ↔ 口径", pass: "is 带 as_of；失败标 stale", demo: "k" },
    { id: "I-04", pair: "Hub ↔ 时态", pass: "未接地 Insight 不能 task.issue", demo: "k" },
    { id: "I-05", pair: "Hub ↔ Registry/MCP", pass: "scene 调写 cs → 403 且 explain", demo: "s" },
    { id: "I-06", pair: "Hub ↔ 外环", pass: "Worker 调 cs 仍走门禁", demo: "e" },
    { id: "I-07", pair: "内环 ↔ Hub", pass: "无出站 HTTP 到 CRM", demo: "w" },
    { id: "I-08", pair: "Hub ↔ 记忆", pass: "pipaw 调 memory → 403；forget 有回执", demo: "k" },
    { id: "I-09", pair: "演化 ↔ Law", pass: "未审批 ChangeSet 不进 compiled", demo: "v" },
    { id: "I-10", pair: "IAM ↔ IdP", pass: "无岗位绑定打不开切片", demo: "i" },
    { id: "I-11", pair: "事件 ↔ 指挥舱", pass: "写成功后同一 node_id 的 is 合流", demo: "n" },
    { id: "I-12", pair: "Schema ↔ MCP", pass: "Registry 与 tools/list 名/字段一致", demo: "s" },
  ],

  events: [
    { id: "pack.opened", from: "Hub", to: "WorkStudio" },
    { id: "kpi.stale", from: "口径适配", to: "作战台" },
    { id: "insight.ungrounded", from: "Hub", to: "签发器" },
    { id: "task.issued", from: "Hub", to: "外环（尚未 start）" },
    { id: "exec.opened", from: "Hub", to: "外环" },
    { id: "approval.wait", from: "外环", to: "作战台 SSE" },
    { id: "cs.invoked", from: "Gateway", to: "审计" },
    { id: "changeset.drafted", from: "Evolution", to: "治理台" },
    { id: "memory.forgotten", from: "记忆", to: "合规" },
  ],
};
