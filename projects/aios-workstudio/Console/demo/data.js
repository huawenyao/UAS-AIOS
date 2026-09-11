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
    last_episode: "ep-20260910-visit-rao-042",
    failures: [
      { id: "f1", episode: "ep-20260910-decision-chen-011", reason: "WM_INCOMPLETE · 缺 feedback 维", at: "2026-09-10 18:22" },
      { id: "f2", episode: "ep-20260909-kpi-li-003", reason: "schema drift · subject 字段缺失", at: "2026-09-09 09:15" },
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

  const ESCAPE_LINKS = [
    { id: "temporal", label: "Temporal 工作流", href: "#escape/temporal" },
    { id: "cube", label: "Cube 语义层", href: "#escape/cube" },
    { id: "neo4j", label: "Neo4j 图谱", href: "#escape/neo4j" },
  ];

  const PAGES = [
    { id: "overview", label: "总览", hint: "健康与租户" },
    { id: "integrate", label: "集成", hint: "剖面 dry-run" },
    { id: "control", label: "管控", hint: "租户套件 · 禁令" },
    { id: "ontology", label: "本体", hint: "责任图 · 校验" },
    { id: "mesh", label: "网格", hint: "能力 · 连接器 · MCP" },
    { id: "govern", label: "治理", hint: "法则包 · 策略" },
    { id: "run", label: "运行", hint: "模型 · KG 摄入" },
    { id: "publish", label: "发布", hint: "ChangeSet 队列" },
  ];

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
      seq: 1,
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
    PAGES,
    ROLES,
    createInitialState,
  };
})();
