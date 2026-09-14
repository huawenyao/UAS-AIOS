/* Platform Console offline fixtures — hub.ops.* simulation only */
(() => {
  "use strict";

  const TENANT_ID = "t-hengchuan";

  const SUITE_DEFS = [
    { id: "workstudio", label: "WorkStudio", desc: "场景态 / 执行态前台" },
    { id: "platform_console", label: "Platform Console", desc: "hub.ops 管理壳（本页）" },
    { id: "system_services", label: "System Services", desc: "身份 · 审计 · 事件总线" },
  ];

  const HEALTH_BASE = {
    open_ms: 142,
    explain: 0.91,
    approval_stuck: 2,
    stale: 1,
    ungrounded_rate: 0.038,
    gate_p95_ms: 186,
  };

  const CAPABILITIES = [
    { id: "cs.customer.get_profile", service: "cs.customer", op: "get_profile", enabled: true, approval_level: "L1" },
    { id: "cs.customer.query", service: "cs.customer", op: "query", enabled: true, approval_level: "L1" },
    { id: "cs.lead.qualify_lead", service: "cs.lead", op: "qualify_lead", enabled: true, approval_level: "L2" },
    { id: "cs.approval.submit", service: "cs.approval", op: "submit", enabled: true, approval_level: "L2" },
    { id: "cs.approval.approve", service: "cs.approval", op: "approve", enabled: false, approval_level: "L3" },
    { id: "cs.process.start", service: "cs.process", op: "start", enabled: true, approval_level: "L2" },
    { id: "cs.notify.send_im", service: "cs.notify", op: "send_im", enabled: true, approval_level: "L1" },
  ];

  const CONNECTORS = [
    { id: "connector.crm", label: "CRM 主数据", slot: "sandbox", status: "connected", secret_ref: "vault://crm/sandbox" },
    { id: "connector.bpm", label: "BPM 审批", slot: "sandbox", status: "connected", secret_ref: "vault://bpm/sandbox" },
    { id: "connector.itsm", label: "ITSM 工单", slot: "prod", status: "degraded", secret_ref: "vault://itsm/prod" },
  ];

  const MCP_TOOLS = [
    { id: "mcp.read_kpi", name: "read_kpi", scene: "read", write: false },
    { id: "mcp.list_audit", name: "list_audit", scene: "read", write: false },
    { id: "mcp.dry_run_profile", name: "dry_run_profile", scene: "integrate", write: false },
    { id: "mcp.submit_changeset", name: "submit_changeset", scene: "govern", write: true },
    { id: "mcp.rotate_secret", name: "rotate_secret", scene: "mesh", write: true },
    { id: "mcp.ingest_episode", name: "ingest_episode", scene: "run", write: true },
  ];

  const PROFILES = [
    { id: "scene", label: "scene", forbids_write: true },
    { id: "explore", label: "explore", forbids_write: true },
    { id: "builder", label: "builder", forbids_write: true, dry_run: true },
    { id: "runtime", label: "runtime", forbids_write: false },
  ];

  const ACCOUNTABILITY_NODES = [
    {
      id: "an-stage-visit",
      label: "阶段拜访 · LTC",
      owner: "客户经理 Rao",
      caliber: "visit_completion",
      wm: { space: true, time: true, subject: true, object: true, feedback: true },
    },
    {
      id: "I-02",
      label: "责任链 I-02 · 决策覆盖",
      owner: "售前 Chen",
      caliber: null,
      wm: { space: true, time: true, subject: true, object: true, feedback: false },
    },
    {
      id: "an-kpi-split",
      label: "KPI 拆分 · 区域口径",
      owner: "经营分析 Li",
      caliber: "kpi_attribution",
      wm: { space: true, time: true, subject: false, object: true, feedback: true },
    },
  ];

  const ONTOLOGY_EDGES = {
    org_cascade: [
      { from: "org.hq", to: "org.region-east", kind: "org_cascade" },
      { from: "org.region-east", to: "org.team-ltc", kind: "org_cascade" },
    ],
    kpi_split: [
      { from: "kpi.revenue", to: "kpi.visit_rate", kind: "kpi_split" },
      { from: "kpi.revenue", to: "kpi.win_rate", kind: "kpi_split" },
    ],
    stage_split: [
      { from: "stage.qualify", to: "stage.proposal", kind: "stage_split" },
      { from: "stage.proposal", to: "stage.close", kind: "stage_split" },
    ],
    object_drill: [
      { from: "obj.account", to: "obj.contact", kind: "object_drill" },
      { from: "obj.account", to: "obj.opportunity", kind: "object_drill" },
    ],
  };

  const LAW_PACKS = {
    current: { version: "lp-2026.08.1", label: "LTC 经营法则包 · 现行" },
    next: { version: "lp-2026.09.0", label: "LTC 经营法则包 · 候选" },
    conflicts: [
      { id: "c1", rule: "visit_sla_days", current: "14 天", next: "10 天", severity: "medium" },
      { id: "c2", rule: "escalation_without_evidence", current: "禁止", next: "L2 可例外", severity: "high" },
    ],
  };

  const MODELS = [
    { id: "route.default", label: "默认路由", model: "gpt-4.1-mini", rpm: 120, slot: "prod" },
    { id: "route.batch", label: "批处理路由", model: "gpt-4.1", rpm: 60, slot: "sandbox" },
    { id: "route.embed", label: "嵌入路由", model: "text-embedding-3-large", rpm: 300, slot: "prod" },
  ];

  const KG_INGEST = {
    status: "degraded",
    lag_minutes: 47,
    last_episode: "拜访纪要 · 客户经理 Rao",
    failures: [
      { id: "f1", episode: "售前决策链 · Chen", reason: "经营模型不完整 · 缺反馈维", at: "2026-09-10 18:22" },
      { id: "f2", episode: "区域口径拆解 · Li", reason: "契约漂移 · 缺主体字段", at: "2026-09-09 09:15" },
    ],
  };

  const GOVERNANCE = {
    audit_enabled: true,
    auto_apply: false,
    bans: [
      { id: "ban-audit-off", label: "关闭审计", reason: "永久禁止 · 合规红线" },
      { id: "ban-auto-apply", label: "自动应用 ChangeSet (auto_apply)", reason: "永久关闭 · 必须人工确认" },
    ],
  };

  /* ===== 治理/运维平面扩展 fixtures（UAS_AIOS_CONSOLE_DEMO_DESIGN §6） ===== */

  const AUTOMATION_JOBS = [
    { id: "audit_scan", name: "审计异常巡检", module: "M11", plane: "gov", schedule: "*/15min", last_run: "2026-09-11 17:30", status: "warn",
      findings: [
        { sev: "high", summary: "一线销售助手连续 4 次越权写尝试（工作台剖面禁止改生产）", action: "ticket", ref: "pat-p1" },
        { sev: "medium", summary: "管理面写草稿连续失败 3 次（当前剖面不允许改责任图）", action: "notify", ref: null },
      ] },
    { id: "dual_track_scan", name: "双轨未升级扫描", module: "M8/M17", plane: "gov", schedule: "hourly", last_run: "2026-09-11 17:00", status: "warn",
      findings: [
        { sev: "medium", summary: "经营轨证据引用了未升级的个人备忘，不得当作岗位承诺", action: "review", ref: "ur-02" },
      ] },
    { id: "stale_watch", name: "指标过期巡检", module: "M15", plane: "ops", schedule: "*/30min", last_run: "2026-09-11 17:45", status: "warn",
      findings: [
        { sev: "medium", summary: "赢单率口径超刷新窗 90 分钟未回填，已过期", action: "changeset", ref: "caliber.rerun:win_rate" },
      ] },
    { id: "connector_health", name: "连接器健康巡检", module: "M14", plane: "ops", schedule: "*/5min", last_run: "2026-09-11 17:50", status: "fail",
      findings: [
        { sev: "high", summary: "工单主数据连接失败率 12%（阈值 5%），建议切到沙箱", action: "changeset", ref: "connector.slot:connector.itsm" },
      ] },
    { id: "kg_lag_watch", name: "经营事实滞后检测", module: "M16", plane: "ops", schedule: "*/10min", last_run: "2026-09-11 17:40", status: "warn",
      findings: [
        { sev: "medium", summary: "经营事实同步滞后 47 分钟（阈值 30 分钟），2 条缺反馈维", action: "task", ref: "ontology.fix" },
      ] },
    { id: "wm_drift_scan", name: "经营模型漂移扫描", module: "M3", plane: "ops", schedule: "daily", last_run: "2026-09-11 06:00", status: "ok",
      findings: [
        { sev: "low", summary: "现行经营模型与责任图「组织级联」冲突 1 处", action: "changeset", ref: "wm.compile:wm-4412" },
      ] },
    { id: "approval_stuck_watch", name: "审批卡点巡检", module: "M18", plane: "ops", schedule: "*/15min", last_run: "2026-09-11 17:45", status: "warn",
      findings: [
        { sev: "medium", summary: "合同审批停留 95 分钟（阈值 60 分钟），策略行动卡住", action: "signal", ref: "wf-7731" },
      ] },
    { id: "model_quota_watch", name: "模型配额监控", module: "M24", plane: "ops", schedule: "*/5min", last_run: "2026-09-11 17:50", status: "warn",
      findings: [
        { sev: "medium", summary: "嵌入路由用量达配额 86%，建议降到经济档", action: "changeset", ref: "model.route:route.embed" },
      ] },
  ];

  const AUDIT_EVENTS = [
    { id: "ae-1001", ts: "2026-09-11 17:52:01", actor: "uas-console", type: "ops.changeset.submit", object: "cs-0041", result: "ok", error_code: null, corr: "c-9f21", hash: "a91f…c204" },
    { id: "ae-1002", ts: "2026-09-11 17:50:44", actor: "connector.itsm", type: "hub.connector.call", object: "cs.ticket.create", result: "fail", error_code: "UPSTREAM_TIMEOUT", corr: "c-9f1e", hash: "77b0…e9a1" },
    { id: "ae-1003", ts: "2026-09-11 17:48:10", actor: "sales-bot", type: "hub.runtime.task_exec", object: "task-5520", result: "deny", error_code: "PROFILE_FORBIDS_SIDE_EFFECT", corr: "c-9eec", hash: "04cd…8812" },
    { id: "ae-1004", ts: "2026-09-11 17:47:55", actor: "sales-bot", type: "hub.runtime.task_exec", object: "task-5520", result: "deny", error_code: "PROFILE_FORBIDS_SIDE_EFFECT", corr: "c-9eeb", hash: "bc51…0f77" },
    { id: "ae-1005", ts: "2026-09-11 17:47:41", actor: "sales-bot", type: "hub.runtime.task_exec", object: "task-5520", result: "deny", error_code: "PROFILE_FORBIDS_SIDE_EFFECT", corr: "c-9eea", hash: "19aa…6d3e" },
    { id: "ae-1006", ts: "2026-09-11 17:47:30", actor: "sales-bot", type: "hub.runtime.task_exec", object: "task-5519", result: "deny", error_code: "PROFILE_FORBIDS_SIDE_EFFECT", corr: "c-9ee9", hash: "5e02…f1b9" },
    { id: "ae-1007", ts: "2026-09-11 17:41:02", actor: "knowledge_admin", type: "ops.graph.submit_draft", object: "an-kpi-split", result: "ok", error_code: null, corr: "c-9ed0", hash: "8c44…2a06" },
    { id: "ae-1008", ts: "2026-09-11 17:36:19", actor: "agent-scm", type: "hub.a2a.delegate", object: "task-5518", result: "ok", error_code: null, corr: "c-9eb8", hash: "d3f7…55c0" },
    { id: "ae-1009", ts: "2026-09-11 17:22:48", actor: "uas-console", type: "ops.audit.export", object: "audit:2026-09-10", result: "ok", error_code: null, corr: "c-9e77", hash: "61e9…aa37" },
    { id: "ae-1010", ts: "2026-09-11 16:58:33", actor: "etl-bot", type: "hub.kg.ingest_episode", object: "ep-20260911-ltc-0091", result: "fail", error_code: "WM_INCOMPLETE", corr: "c-9e01", hash: "f0b6…13d8" },
    { id: "ae-1011", ts: "2026-09-11 16:40:12", actor: "tenant:t-other", type: "hub.scene.pack.open", object: "pack-ltc", result: "deny", error_code: "TENANT_SCOPE_VIOLATION", corr: "c-9df2", hash: "2b7c…9e44" },
    { id: "ae-1012", ts: "2026-09-11 16:05:57", actor: "uas-console", type: "ops.caliber.publish", object: "win_rate@1.3.0", result: "ok", error_code: null, corr: "c-9d80", hash: "aa10…72bf" },
  ];

  const AUDIT_PATTERNS = [
    { id: "pat-p1", label: "一线连续越权写尝试", actor: "sales-bot", count: 4, severity: "high", event_ids: ["ae-1003", "ae-1004", "ae-1005", "ae-1006"] },
    { id: "pat-p2", label: "跨租户访问尝试", actor: "tenant:t-other", count: 1, severity: "high", event_ids: ["ae-1011"] },
    { id: "pat-p3", label: "管理面连续失败", actor: "uas-console", count: 3, severity: "medium", event_ids: ["ae-1007"] },
  ];

  const IAM_BINDINGS = [
    { id: "b-01", person: "rao.w", role: "CM", node_id: "an-stage-visit", track: "ΠPaw", status: "active" },
    { id: "b-02", person: "chen.y", role: "售前", node_id: "I-02", track: "ΠPaw", status: "active" },
    { id: "b-03", person: "li.m", role: "经营分析", node_id: "an-kpi-split", track: "ΠPaw", status: "active" },
    { id: "b-04", person: "rao.w", role: "SelfPaw", node_id: "—", track: "SelfPaw", status: "active" },
  ];

  const UPGRADE_REQUESTS = [
    { id: "ur-01", from_track: "SelfPaw", memory_ref: "mem-8802", evidence_ref: "ev-2019", summary: "拜访话术偏好 → 岗位执行建议", status: "pending" },
    { id: "ur-02", from_track: "SelfPaw", memory_ref: "mem-8821", evidence_ref: null, summary: "客户线索直觉（无证据链）", status: "pending" },
    { id: "ur-03", from_track: "SelfPaw", memory_ref: "mem-8710", evidence_ref: "ev-1977", summary: "折扣谈判经验", status: "rejected" },
  ];

  const MEMORY_DOMAINS = [
    { id: "episodes", label: "情景记忆", count: 1284, decay: "90 天半衰" },
    { id: "insights", label: "洞察记忆", count: 96, decay: "手动固化" },
    { id: "preferences", label: "偏好记忆", count: 41, decay: "常驻" },
  ];

  const FORGET_REQUESTS = [
    { id: "fr-01", kind: "离职", subject: "zhang.s（已离职 09-08）", scope: "全记忆域", status: "pending" },
    { id: "fr-02", kind: "合规申请", subject: "customer:Shopline 联系人", scope: "episodes ∩ 近 12 月", status: "pending" },
  ];

  const FORGET_RECEIPTS = [
    { id: "frc-2026-014", request: "fr-00", subject: "wang.q（离职）", erased: 213, at: "2026-09-02 11:20", audit_ptr: "ae-0812" },
    { id: "frc-2026-013", request: "fr-9", subject: "customer:ACME 合规", erased: 37, at: "2026-08-27 15:02", audit_ptr: "ae-0644" },
  ];

  const EVO_SIGNALS = [
    { id: "sig-01", kind: "经验候选", count: 12, source: "关账 / 拜访反馈", aggregated: true },
    { id: "sig-02", kind: "未接地洞察", count: 3, source: "接地校验", aggregated: true },
    { id: "sig-03", kind: "须升级岗位承诺", count: 1, source: "双轨门禁", aggregated: false },
  ];

  const EVO_DRAFT = {
    id: "draft-lp-2026.09.0",
    pack: "LTC 经营法则包",
    base: "lp-2026.08.1",
    target: "lp-2026.09.0",
    diff: [
      { rule: "visit_sla_days", from: "14 天", to: "10 天" },
      { rule: "escalation_without_evidence", from: "禁止", to: "L2 可例外（须附证据）" },
      { rule: "新增 stale_sla_window", from: "—", to: "90min" },
    ],
    submitted_by: "knowledge_admin",
  };

  const REGRESSION_CASES = [
    { id: "case-01", name: "工作台写生产恒拒绝", result: "pass" },
    { id: "case-02", name: "个人备忘不得当岗位承诺", result: "pass" },
    { id: "case-03", name: "二级例外审批链路", result: "fail" },
    { id: "case-04", name: "过期口径不得向下传播", result: "pass" },
  ];

  const CALIBERS = [
    { key: "visit_completion", owner: "经营分析 Li", status: "fresh", window: "24h", last_refresh: "2026-09-11 06:00", lifecycle: "live", expr: "sum(visits_done) / sum(visits_planned)" },
    { key: "win_rate", owner: "经营分析 Li", status: "stale", window: "1h", last_refresh: "2026-09-11 16:10", lifecycle: "live", expr: "count(won) / count(closed)" },
    { key: "kpi_attribution", owner: "平台管理员", status: "ought", window: "24h", last_refresh: "—", lifecycle: "draft", expr: "sum(attr.amount) by node" },
    { key: "pipeline_coverage", owner: "经营分析 Li", status: "fresh", window: "6h", last_refresh: "2026-09-11 12:00", lifecycle: "live", expr: "sum(pipeline) / quota" },
  ];

  const WORKFLOW_INSTANCES = [
    { id: "wf-7731", title: "合同审批", task: "销售运营 · 合同签署", step: "三级审批", wait: 95, status: "waiting", degraded: false },
    { id: "wf-7728", title: "拜访安排", task: "销售运营 · 客户拜访", step: "执行中", wait: 0, status: "running", degraded: false },
    { id: "wf-7721", title: "报价审批", task: "销售运营 · 合同签署", step: "回写", wait: 0, status: "succeeded", degraded: true },
    { id: "wf-7719", title: "线索分配", task: "销售运营 · 线索获取", step: "完成", wait: 0, status: "succeeded", degraded: false },
  ];

  const INNER_LOOP_STATS = { checkpoints: 412, interrupts: 7, avg_steps: 5.2, tokens_today: 184220, impl: "内环 SPI 默认实现" };

  const WM_ITEMS = [
    { id: "wm-4412", type: "市场假设", lifecycle: "live", node_ref: "an-stage-visit", conflict: true, summary: "华东区 Q3 拜访节奏假设" },
    { id: "wm-4501", type: "对象状态", lifecycle: "live", node_ref: "an-kpi-split", conflict: false, summary: "客户分层阈值" },
    { id: "wm-4550", type: "主体假设", lifecycle: "compiling", node_ref: "I-02", conflict: false, summary: "决策链覆盖假设 v2" },
    { id: "wm-4600", type: "反馈环", lifecycle: "draft", node_ref: "an-stage-visit", conflict: false, summary: "拜访→转化反馈环修订" },
    { id: "wm-4601", type: "时窗假设", lifecycle: "draft", node_ref: "an-kpi-split", conflict: false, summary: "口径回填时窗假设" },
  ];

  const ESCAPE_LINKS = [
    { id: "outer-loop", label: "外环运行时（SRE 逃生）", href: "#escape/outer" },
    { id: "caliber-engine", label: "口径引擎（SRE 逃生）", href: "#escape/caliber" },
    { id: "graph-runtime", label: "时态图运行时（SRE 逃生）", href: "#escape/kg" },
  ];

  const PAGE_GROUPS = [
    { group: "控制与发布", pages: [
      { id: "overview", label: "总览", hint: "闭环健康 · 对象", object: "功能对象 / 数据模型", loop: "全环", intro: "一线走闭环；这里管对象对不对、谁能改、改了有没有人确认。" },
      { id: "integrate", label: "集成试运行", hint: "剖面 dry-run", object: "能力门禁", loop: "预测 → 策略行动", intro: "写生产前先试运行：谁能写、写到哪。I-05 dry-run 只模拟门禁，不落生产。" },
      { id: "control", label: "管控", hint: "租户套件 · 禁令", object: "租户套件 / 禁令", loop: "学习沉淀", intro: "管租户开了哪些套件。auto_apply 永久关闭；不存在「关闭审计」控件。" },
      { id: "ontology", label: "责任图", hint: "节点五件套", object: "责任节点", loop: "洞察 / 归因", intro: "目标拆到可办的责任节点。五件套（空间/时间/主体/客体/反馈 + 口径）缺一不可派活。" },
      { id: "mesh", label: "能力与连接", hint: "目录 · 槽位", object: "能力目录 / 主数据连接", loop: "数据", intro: "一线能调什么、主数据从哪来。改启用级别或槽位都进发布队列。" },
      { id: "govern", label: "法则包", hint: "冲突与策略", object: "经营法则", loop: "归因 → 学习沉淀", intro: "过关条件与否决。现行与候选冲突必须显式声明，晋升走变更单。" },
      { id: "run", label: "运行观测", hint: "事实同步 · 路由", object: "时态事实 / 模型路由", loop: "数据", intro: "经营事实是否跟上、模型路由是否健康。本页无写入入口。" },
      { id: "publish", label: "发布确认", hint: "变更单队列", object: "变更单", loop: "学习沉淀", intro: "配置唯一写通道。契约不一致时相关发布被阻断。auto_apply 永关。" },
    ] },
    { group: "治理 · 谁能做什么", pages: [
      { id: "audit", label: "审计检索", hint: "异常巡检 · 导出自审", object: "审计事件", loop: "效果回收", intro: "谁做了什么可追。记录不可改删；导出动作自身也入审计。巡检只产建议。" },
      { id: "dualtrack", label: "岗位与权限", hint: "绑定 · 双轨升级", object: "岗位绑定", loop: "策略行动", intro: "谁能对哪个责任节点承诺。个人备忘升到岗位承诺必须带证据。岗位绑定改派进发布队列。" },
      { id: "memory", label: "个人记忆", hint: "遗忘申请 · 回执", object: "个人备忘", loop: "学习沉淀", intro: "个人备忘不得冒充经营状态。遗忘必须有回执且可检索。" },
      { id: "evolution", label: "法则演化", hint: "信号 · 回归 · 发布", object: "经营法则", loop: "学习沉淀", intro: "效果回收后的经验回写法则包。回归未过禁止发布。auto_apply 永久 OFF。" },
    ] },
    { group: "运维 · 知识是否正确", pages: [
      { id: "automation", label: "巡检作业", hint: "自动化作业只产建议", object: "巡检发现", loop: "全环健康", intro: "自动化作业只产建议与草稿，不直写生产。生效必须人工确认。" },
      { id: "caliber", label: "指标口径", hint: "过期巡检 · 草稿发布", object: "指标口径 / 口径值", loop: "数据", intro: "目标值与实际值怎么算。过期口径不得派活；现行口径不可原地改。" },
      { id: "workflows", label: "审批与长任务", hint: "滞留催办 · 不暴露内部编号", object: "审批单 / 长任务", loop: "策略行动", intro: "策略行动是否卡住。一线只见「待你确认」，不展示内部运行编号。" },
      { id: "wm", label: "经营模型", hint: "草稿 / 已编译 / live", object: "经营模型", loop: "预测 / 归因", intro: "草稿 → 编译中 → 现行 三寿命。现行不可原地改；编译申请走变更单。" },
    ] },
  ];

  const VALUE_LOOP = [
    { id: "data", label: "数据", use: "看板上的口径值与客户行", ops: "口径是否过期 · 主数据槽健康" },
    { id: "insight", label: "洞察", use: "接地后的卡口原因", ops: "责任节点五件套是否齐全" },
    { id: "cause", label: "归因", use: "应当 / 事实 / 缺口对照", ops: "法则包与口径定义" },
    { id: "forecast", label: "预测", use: "不行动会丢单或关不了账", ops: "模型路由与经营模型漂移" },
    { id: "act", label: "策略行动", use: "待你确认后的派活与写入", ops: "审批滞留 · 长任务催办" },
    { id: "recover", label: "效果回收", use: "同一节点指标回流", ops: "审计链 · 写入回执" },
    { id: "learn", label: "学习沉淀", use: "人确认后回写法则", ops: "变更单 · 演化回归" },
  ];

  const FUNC_OBJECTS = [
    { name: "岗位工作", desc: "一线看见并办成的任务", store: "任务对象", manage: "签发 / 待你确认", page: null, loop: "策略行动" },
    { name: "经营法则", desc: "过关条件与否决", store: "法则包", manage: "条文修订 → 发布队列", page: "evolution", loop: "学习沉淀" },
    { name: "指标口径", desc: "目标值与实际值怎么算", store: "口径定义", manage: "草稿校验 → 发布", page: "caliber", loop: "数据" },
    { name: "岗位权限", desc: "谁能对哪个节点承诺", store: "岗位绑定", manage: "改派 / 双轨升级", page: "dualtrack", loop: "策略行动" },
    { name: "个人备忘", desc: "不得冒充经营状态", store: "个人记忆", manage: "遗忘申请与回执", page: "memory", loop: "学习沉淀" },
  ];

  const DATA_OBJECTS = [
    { name: "责任节点", desc: "目标拆到可办的节点", store: "责任图", not: "不是图库节点、不是记忆行", page: "ontology" },
    { name: "经营模型", desc: "草稿 / 已编译 / live 三寿命", store: "模型仓库", not: "不是聊天、不是检索库", page: "wm" },
    { name: "口径值", desc: "实际值 + 时点 + 是否过期", store: "指标查询缓存", not: "不是口头公式", page: "caliber" },
    { name: "时态事实", desc: "某日决策链是谁", store: "经营事实层", not: "不是经营承诺", page: "run" },
    { name: "变更单", desc: "配置唯一写通道", store: "发布队列", not: "不是会话内直接改", page: "publish" },
    { name: "审计事件", desc: "调用链可检索", store: "审计链", not: "不是指挥舱 KPI", page: "audit" },
  ];

  const PAGES = PAGE_GROUPS.flatMap((g) => g.pages);

  const ROLES = [
    { id: "admin", label: "平台管理员" },
    { id: "operator", label: "运营指挥" },
    { id: "sre", label: "SRE" },
    { id: "frontline", label: "一线员工", locked: true },
  ];

  function createInitialState() {
    return {
      tenant_id: TENANT_ID,
      role: "admin",
      suites: { workstudio: true, platform_console: true, system_services: true },
      health: { ...HEALTH_BASE },
      schema_drift: { status: "healthy", count: 0 },
      capabilities: CAPABILITIES.map((c) => ({ ...c })),
      connectors: CONNECTORS.map((c) => ({ ...c })),
      models: MODELS.map((m) => ({ ...m })),
      kg_ingest: JSON.parse(JSON.stringify(KG_INGEST)),
      changeSets: [],
      mcp_scene: "all",
      mcp_hide_write: true,
      profile_id: "builder",
      ontology_projections: {
        org_cascade: true,
        kpi_split: true,
        stage_split: false,
        object_drill: false,
      },
      sre_escape: false,
      seq: 41,
      automation_jobs: JSON.parse(JSON.stringify(AUTOMATION_JOBS)),
      audit_events: AUDIT_EVENTS.map((e) => ({ ...e })),
      audit_filter: { actor: "all", type: "all", result: "all" },
      iam_bindings: IAM_BINDINGS.map((b) => ({ ...b })),
      upgrade_requests: UPGRADE_REQUESTS.map((r) => ({ ...r })),
      forget_requests: FORGET_REQUESTS.map((r) => ({ ...r })),
      forget_receipts: FORGET_RECEIPTS.map((r) => ({ ...r })),
      evo_cases: REGRESSION_CASES.map((c) => ({ ...c })),
      calibers: CALIBERS.map((c) => ({ ...c })),
      caliber_draft: "",
      workflow_instances: WORKFLOW_INSTANCES.map((w) => ({ ...w })),
      wm_items: WM_ITEMS.map((w) => ({ ...w })),
    };
  }

  window.ConsoleFixtures = {
    TENANT_ID,
    SUITE_DEFS,
    HEALTH_BASE,
    CAPABILITIES,
    CONNECTORS,
    MCP_TOOLS,
    PROFILES,
    ACCOUNTABILITY_NODES,
    ONTOLOGY_EDGES,
    LAW_PACKS,
    MODELS,
    KG_INGEST,
    GOVERNANCE,
    ESCAPE_LINKS,
    PAGE_GROUPS,
    PAGES,
    VALUE_LOOP,
    FUNC_OBJECTS,
    DATA_OBJECTS,
    ROLES,
    AUTOMATION_JOBS,
    AUDIT_EVENTS,
    AUDIT_PATTERNS,
    MEMORY_DOMAINS,
    EVO_SIGNALS,
    EVO_DRAFT,
    INNER_LOOP_STATS,
    createInitialState,
  };
})();
