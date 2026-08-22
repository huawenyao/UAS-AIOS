const $ = (id) => document.getElementById(id);
const esc = (s) =>
  String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const VIEWS = [
  ["loop", "闭环"],
  ["optimize", "优化"],
  ["deposit", "沉淀"],
];
const LEGACY_VIEW = {
  overview: "loop",
  data: "loop",
  goals: "loop",
  status: "loop",
  risks: "loop",
  todos: "optimize",
};

const COLS = [
  ["todo", "待处理"],
  ["doing", "进行中"],
  ["blocked", "阻塞"],
  ["done", "完成"],
];

const DIMS = [
  ["space", "空间"],
  ["time", "时间"],
  ["subjects", "主体"],
  ["objects", "客体"],
  ["feedback", "反馈"],
];

const CYCLE = [
  ["input", "输入"],
  ["simulate", "模拟"],
  ["generate", "生成"],
  ["interact", "交互"],
  ["evolve", "进化"],
  ["output", "输出"],
  ["revenue", "收益"],
];

const MODE_ZH = { explore: "研究", builder: "构建", runtime: "运行" };
const PERM = {
  explore: "sandbox · 禁写生产 · Skill 可 cite",
  builder: "sandbox · 禁写生产 · 可 mock",
  runtime: "gated · cs.* 须审批",
};

const PACKS = {
  ops: {
    id: "ops",
    space: "衡川 · 经营管理工作台",
    deep: true,
    owner: "林启明",
    role: "用人经理",
    tension: "Staff 短名单窗口内，未接地分数仍可能混进建议。法则要求停手核实，不能发 offer。",
    dikw: ["ATS / 面试纪要", "未接地率 61%", "LAW-EVD-001 无面试不得当真", "先研究，不发 offer"],
    project: {
      id: "prj-hire-q3",
      code: "PRJ-HIR",
      title: "Q3 Staff 短名单",
      window: "本周窗口 · 冻结后 48h 回滚",
      cycle: "interact",
      object: "ThemePack → AppRelease → Instance",
    },
    kpis: [
      { id: "fill", n: "编制填满", v: "72%", hint: "价值流仍停在短名单。" },
      { id: "ground", n: "证据接地", v: "61%", hot: true, item: "wi-rao", hint: "下钻到 Rao：culture_fit 无面试。" },
      { id: "cycle", n: "周期", v: "38d", hint: "短名单滞留拉长周期。" },
    ],
    goals: [
      {
        id: "o1",
        title: "O1 本周五给出可解释短名单",
        pct: 45,
        krs: [
          { id: "wi-shortlist", title: "KR1 三人窗口只保留接地建议", pct: 60 },
          { id: "wi-rao", title: "KR2 未接地不得进入建议 = 100%", pct: 40 },
          { id: "wi-freeze", title: "KR3 冻结走 G3 + 48h 回滚", pct: 20 },
        ],
      },
    ],
    items: [
      {
        id: "wi-shortlist",
        code: "HIR-041",
        title: "Q3 Staff 短名单窗口",
        type: "工作项",
        col: "doing",
        owner: "林启明",
        stage: "短名单",
        due: "本周五",
        exec: "explore",
        gate: "G1",
        ought: "短名单只含证据接地的候选人。",
        is: "三人在窗：陈予安接地，Patel 部分不确定，Rao 未接地。",
        gap: "未建模完五维不得签发 offer。",
        wm: {
          space: "衡川招聘委员会，线上材料加 onsite",
          time: "本周窗口，冻结后 48h 回滚",
          subjects: "林启明决策；候选人陈予安 / Patel / Rao",
          objects: "短名单、证据包、法则 Pack",
          feedback: "经理确认或驳回，未接地率",
        },
      },
      {
        id: "wi-rao",
        code: "HIR-042",
        title: "核验 Rao culture_fit",
        type: "阻塞",
        col: "blocked",
        owner: "林启明",
        stage: "短名单",
        due: "今日",
        exec: "explore",
        gate: "G1",
        hot: true,
        ought: "culture_fit 必须有面试记录。",
        is: "分数 0.86 来自简历关键词，无面试。",
        gap: "未接地不得进入建议。",
        wm: {
          space: "衡川招聘委员会",
          time: "本周校准窗口",
          subjects: "林启明；候选人 Rao",
          objects: "culture_fit 分数、面试记录",
          feedback: "停手核实或移出建议",
        },
      },
      {
        id: "wi-chen",
        code: "HIR-043",
        title: "陈予安 面试已接地",
        type: "候选人",
        col: "doing",
        owner: "林启明",
        stage: "短名单",
        due: "本周五",
        exec: "runtime",
        gate: "G3",
        ought: "面试证据进入建议。",
        is: "系统设计当场拆过限流，有可复核题面。",
        gap: "可进建议；冻结仍要 G3。",
        wm: {
          space: "衡川招聘委员会",
          time: "本周窗口",
          subjects: "林启明；陈予安",
          objects: "面试纪要、短名单建议",
          feedback: "冻结短名单",
        },
      },
      {
        id: "wi-patel",
        code: "HIR-044",
        title: "Patel oncall 不确定",
        type: "候选人",
        col: "doing",
        owner: "招聘委员会",
        stage: "短名单",
        due: "本周四",
        exec: "explore",
        gate: "G1",
        ought: "oncall 能力有对内对照。",
        is: "仅公开仓库密度高，无对内绩效。",
        gap: "可进建议但必须标不确定。",
        wm: {
          space: "衡川招聘委员会",
          time: "本周窗口",
          subjects: "林启明；Patel；前任经理待取证",
          objects: "GitHub 公开贡献、oncall 假设",
          feedback: "向前任经理取证",
        },
      },
      {
        id: "wi-freeze",
        code: "HIR-045",
        title: "冻结短名单（组织承诺）",
        type: "门禁",
        col: "todo",
        owner: "招聘委员会",
        stage: "onsite",
        due: "本周五",
        exec: "runtime",
        gate: "G3",
        ought: "冻结是 G3 组织承诺，48h 可回滚。",
        is: "应用已校验，尚未 Release 到实例。",
        gap: "未 Release 不能静默跑生产；冻结须审批。",
        wm: {
          space: "衡川招聘委员会",
          time: "冻结后 48h 回滚",
          subjects: "招聘委员会；林启明",
          objects: "短名单实例 ins-hengchuan-hire-q3",
          feedback: "审计 + 回滚窗口",
        },
      },
    ],
    risks: [
      { id: "wi-rao", level: "red", title: "未接地分数混进建议", detail: "Rao culture_fit=0.86 无面试。LAW-EVD-001。" },
      { id: "wi-freeze", level: "amber", title: "静默发 offer", detail: "个人轨不得持经营轨凭证。TRACK_ESCALATION_REQUIRED。" },
    ],
    todos: [
      { id: "wi-rao", pdca: "P", item: "核验 Rao culture_fit", owner: "林启明", gate: "G1", exec: "explore" },
      { id: "wi-patel", pdca: "D", item: "向前任经理取证 Patel oncall", owner: "招聘委员会", gate: "G1", exec: "explore" },
      { id: "wi-chen", pdca: "C", item: "复核陈予安面试证据包", owner: "林启明", gate: "G0", exec: "runtime" },
      { id: "wi-freeze", pdca: "A", item: "冻结短名单", owner: "招聘委员会", gate: "G3", exec: "runtime" },
    ],
    evidence: [
      { source: "ATS 面试纪要 陈予安", reliability: "高", excerpt: "系统设计当场拆过限流，有可复核题面。" },
      { source: "GitHub public Patel", reliability: "中", excerpt: "分布式提交密度高，无对内绩效对照。" },
      { source: "简历解析 Rao", reliability: "低", excerpt: "无面试。未接地假设。" },
    ],
    uncertainties: [
      { claim: "Rao culture_fit 高", why: "无面试，分数来自关键词", ask: "安排校准面试，或移出建议" },
      { claim: "Patel 能扛 oncall", why: "仅公开仓库", ask: "向前任经理取证" },
    ],
    options: [
      { id: "A", summary: "短名单 = 陈予安 + Patel；Rao 不进建议", risk: "漏掉潜在文化匹配" },
      { id: "B", summary: "三人全进并附警告", risk: "警告会被忽略" },
    ],
    knowledge: [
      { id: "hiring_shortlist_laws.md", type: "法则", installed: true },
      { id: "hiring-signal-triangulation", type: "Skill", installed: false },
      { id: "loop-thinking-enhanced", type: "方法", installed: true },
    ],
    builder: {
      app: "短名单编译器 0.1.0",
      released: false,
      invariants: [
        { id: "wm_five_dims", ok: true, detail: "五维齐全" },
        { id: "ungrounded_not_in_advice", ok: true, detail: "Rao 分数未进入建议" },
        { id: "governance_g3", ok: true, detail: "冻结短名单 G3 + 48h 回滚" },
      ],
      cs: [
        { op: "cs.candidate.query", level: "L1", side: "读" },
        { op: "cs.approval.submit", level: "L2", side: "写，仅运行" },
        { op: "cs.notify.send_email", level: "L2", side: "写，本剖面禁止" },
      ],
    },
    runtime: {
      instance: "ins-hengchuan-hire-q3",
      scope: "tenant",
      items: [
        { name: "陈予安", advice: true, why: "面试证据接地" },
        { name: "Patel", advice: true, why: "公开贡献密度高；oncall 仍标不确定" },
        { name: "Rao", advice: false, why: "culture_fit 未接地，不得进入建议" },
      ],
      silent: "静默给候选人发 offer",
      action: "冻结短名单（G3）",
    },
  },
  pmo: {
    id: "pmo",
    space: "衡川 · 项目管理工作台",
    deep: false,
    owner: "周衡",
    role: "PMO",
    tension: "里程碑 M2 窗口内，7 条跨团队依赖没有 Owner。不能在驾驶舱改计划。",
    dikw: ["依赖图 / 周会纪要", "按期 64%，依赖 7 条开着", "无 Owner 不得验收", "先指定 Owner，不改计划"],
    project: {
      id: "prj-m2",
      code: "PRJ-M2",
      title: "M2 验收窗口",
      window: "本周五冻结",
      cycle: "generate",
      object: "里程碑 × 依赖 × 计划基线",
    },
    kpis: [
      { id: "on", n: "按期", v: "64%", hot: true, item: "wi-m2", hint: "下钻到 M2：验收被挡住。" },
      { id: "dep", n: "开着的依赖", v: "7", item: "wi-deps", hint: "7 条边 Assignee 为空。" },
      { id: "risk", n: "风险开", v: "3", hint: "范围未冻仍算风险。" },
    ],
    goals: [
      {
        id: "o1",
        title: "O1 M2 按窗口验收",
        pct: 36,
        krs: [
          { id: "wi-deps", title: "KR1 7 条依赖均有 Owner", pct: 14 },
          { id: "wi-m2", title: "KR2 无 Owner 不得进验收", pct: 70 },
          { id: "wi-scope", title: "KR3 范围冻结 G3", pct: 20 },
        ],
      },
    ],
    items: [
      {
        id: "wi-m2",
        code: "PJ-012",
        title: "里程碑 M2 验收",
        type: "里程碑",
        col: "blocked",
        owner: "周衡",
        stage: "执行",
        due: "本周五",
        exec: "explore",
        gate: "G1",
        hot: true,
        ought: "进入验收前每条依赖必须有 Owner。",
        is: "7 条跨团队边停在执行，Owner 为空。",
        gap: "无 Owner 不得进验收。",
        wm: {
          space: "衡川组合委员会，跨团队依赖墙",
          time: "M2 窗口，本周五冻结",
          subjects: "周衡协调；各团队 Owner 待指定",
          objects: "依赖边、里程碑、计划基线",
          feedback: "Owner 确认、验收放行",
        },
      },
      {
        id: "wi-deps",
        code: "PJ-013",
        title: "指定 M2 七条依赖 Owner",
        type: "依赖",
        col: "todo",
        owner: "周衡",
        stage: "执行",
        due: "本周三",
        exec: "explore",
        gate: "G1",
        ought: "每条依赖可指认主体与环位。",
        is: "Jira 依赖图 7 条边指向空 Assignee；周会只有口头承诺。",
        gap: "口头不算 Owner。",
        wm: {
          space: "平台组 / 业务组 / 数据组",
          time: "本周三书面指定",
          subjects: "周衡；待定 Owner",
          objects: "依赖边",
          feedback: "书面确认写入计划",
        },
      },
      {
        id: "wi-scope",
        code: "PJ-014",
        title: "冻结 M2 范围",
        type: "门禁",
        col: "todo",
        owner: "组合委员会",
        stage: "计划",
        due: "本周五",
        exec: "runtime",
        gate: "G3",
        ought: "范围冻结是 G3，48h 可回滚。",
        is: "验收门禁尚未校验范围冻结。",
        gap: "未校验不得改计划基线。",
        wm: {
          space: "衡川组合委员会",
          time: "冻结后 48h",
          subjects: "组合委员会；周衡",
          objects: "计划基线",
          feedback: "审计",
        },
      },
      {
        id: "wi-m1",
        code: "PJ-011",
        title: "里程碑 M1",
        type: "里程碑",
        col: "done",
        owner: "周衡",
        stage: "验收",
        due: "已过",
        exec: "runtime",
        gate: "G0",
        ought: "依赖已闭环才验收。",
        is: "M1 依赖已闭环。",
        gap: "无。",
        wm: {
          space: "衡川组合委员会",
          time: "上窗口",
          subjects: "周衡",
          objects: "M1",
          feedback: "已验收",
        },
      },
    ],
    risks: [
      { id: "wi-deps", level: "red", title: "跨团队依赖无 Owner", detail: "7 条边空 Assignee。口头下周再分，未写入。" },
      { id: "wi-scope", level: "amber", title: "范围未冻", detail: "带着空 Owner 强行验收会被门禁拦住。" },
    ],
    todos: [
      { id: "wi-deps", pdca: "P", item: "给 M2 七条依赖指定 Owner", owner: "周衡", gate: "G1", exec: "explore" },
      { id: "wi-m2", pdca: "C", item: "验收门禁复核", owner: "周衡", gate: "G1", exec: "explore" },
      { id: "wi-scope", pdca: "A", item: "冻结 M2 范围", owner: "组合委员会", gate: "G3", exec: "runtime" },
    ],
    evidence: [
      { source: "Jira 依赖图", reliability: "高", excerpt: "7 条边指向空 Assignee。" },
      { source: "周会纪要", reliability: "中", excerpt: "口头说下周再分，无写入。" },
    ],
    uncertainties: [{ claim: "平台组能接 3 条", why: "只有口头承诺", ask: "书面指定 Owner" }],
    options: [
      { id: "A", summary: "先指定 Owner 再谈验收", risk: "窗口可能滑" },
      { id: "B", summary: "带着空 Owner 强行验收", risk: "门禁失败" },
    ],
    knowledge: [
      { id: "pmo_acceptance_laws.md", type: "法则", installed: true },
      { id: "dependency-owner-triangulation", type: "Skill", installed: false },
    ],
    builder: {
      app: "里程碑验收门禁 0.1.0",
      released: false,
      invariants: [
        { id: "wm_five_dims", ok: true, detail: "五维齐全" },
        { id: "owner_required", ok: true, detail: "无 Owner 不得验收" },
        { id: "governance_g3", ok: false, detail: "范围冻结尚未校验" },
      ],
      cs: [
        { op: "cs.project.query", level: "L1", side: "读" },
        { op: "cs.approval.submit", level: "L2", side: "写，仅运行" },
      ],
    },
    runtime: {
      instance: "ins-hengchuan-m2",
      scope: "tenant",
      items: [
        { name: "M1", advice: true, why: "依赖已闭环" },
        { name: "M2", advice: false, why: "7 条依赖无 Owner" },
      ],
      silent: "静默改计划基线",
      action: "冻结 M2 范围（G3）",
    },
  },
  invest: {
    id: "invest",
    space: "衡川 · 金融投资工作台",
    deep: false,
    owner: "沈澈",
    role: "投研负责人",
    tension: "组合回撤 6.1%，信源等级仅为中。中等级信源不得单独触发下单。",
    dikw: ["行情 / 研报 / 审计", "回撤 -6.1%", "中等级信源不得单独下单", "先核验因子，禁止驾驶舱下单"],
    project: {
      id: "prj-book",
      code: "PRJ-INV",
      title: "回撤窗口组合",
      window: "本窗口 · 合规门 G4",
      cycle: "simulate",
      object: "组合 × 因子 × 仓位",
    },
    kpis: [
      { id: "dd", n: "回撤", v: "-6.1%", hot: true, item: "wi-dd", hint: "回撤已触发复核。" },
      { id: "src", n: "信源等级", v: "中", item: "wi-order", hint: "中等级不得单独下单。" },
      { id: "alpha", n: "因子有效", v: "0.18", item: "wi-factor", hint: "有效性未核验。" },
    ],
    goals: [
      {
        id: "o1",
        title: "O1 回撤窗口内不违规下单",
        pct: 40,
        krs: [
          { id: "wi-factor", title: "KR1 动量因子完成核验", pct: 30 },
          { id: "wi-order", title: "KR2 下单须高等级或双源", pct: 80 },
          { id: "wi-dd", title: "KR3 回撤 6% 触发复核", pct: 70 },
        ],
      },
    ],
    items: [
      {
        id: "wi-dd",
        code: "INV-021",
        title: "组合回撤复核",
        type: "持仓",
        col: "blocked",
        owner: "风控",
        stage: "持仓",
        due: "今日",
        exec: "runtime",
        gate: "G4",
        hot: true,
        ought: "回撤 6% 必须复核，不得在驾驶舱下单。",
        is: "回撤 -6.1%，敞口 1.2x。",
        gap: "复核未完成前禁止新开仓。",
        wm: {
          space: "衡川投研台，合规门 G4",
          time: "本窗口",
          subjects: "沈澈；风控",
          objects: "组合、回撤事件",
          feedback: "复核通过或减仓",
        },
      },
      {
        id: "wi-order",
        code: "INV-022",
        title: "待下单单",
        type: "下单",
        col: "blocked",
        owner: "沈澈",
        stage: "下单",
        due: "冻结",
        exec: "explore",
        gate: "G4",
        hot: true,
        ought: "下单必须有高等级信源或双源交叉。",
        is: "当前仅中等级研报。",
        gap: "中等级信源不得单独下单。",
        wm: {
          space: "衡川投研台",
          time: "回撤窗口",
          subjects: "沈澈",
          objects: "待下单单、研报",
          feedback: "合规拦截",
        },
      },
      {
        id: "wi-factor",
        code: "INV-023",
        title: "核验动量因子",
        type: "研究",
        col: "doing",
        owner: "沈澈",
        stage: "研究",
        due: "本周",
        exec: "explore",
        gate: "G1",
        ought: "因子有效性可指认、可回收。",
        is: "有效性 0.18，尚未交叉核验。",
        gap: "未核验不得作为下单理由。",
        wm: {
          space: "衡川投研台",
          time: "本周研究窗",
          subjects: "沈澈",
          objects: "动量因子",
          feedback: "策略回收",
        },
      },
    ],
    risks: [
      { id: "wi-order", level: "red", title: "中等级信源触发下单", detail: "驾驶舱直接下单会被合规门拦住。" },
      { id: "wi-dd", level: "amber", title: "回撤超限", detail: "本窗口已触发 G4 复核。" },
    ],
    todos: [
      { id: "wi-factor", pdca: "P", item: "核验动量因子有效性", owner: "沈澈", gate: "G1", exec: "explore" },
      { id: "wi-dd", pdca: "C", item: "回撤超限复核", owner: "风控", gate: "G4", exec: "runtime" },
      { id: "wi-order", pdca: "A", item: "驳回中等级信源下单", owner: "沈澈", gate: "G4", exec: "explore" },
    ],
    evidence: [
      { source: "组合净值", reliability: "高", excerpt: "回撤 -6.1%，敞口 1.2x。" },
      { source: "卖方研报", reliability: "中", excerpt: "动量因子有效，信源等级中。" },
    ],
    uncertainties: [{ claim: "因子仍有效", why: "未交叉核验", ask: "补第二信源或停手" }],
    options: [
      { id: "A", summary: "先核验因子，不下单", risk: "错过反弹" },
      { id: "B", summary: "中等级信源直接下单", risk: "合规门拦截" },
    ],
    knowledge: [
      { id: "invest_source_laws.md", type: "法则", installed: true },
      { id: "factor-cross-check", type: "Skill", installed: false },
    ],
    builder: {
      app: "下单合规门 0.1.0",
      released: false,
      invariants: [
        { id: "wm_five_dims", ok: true, detail: "五维齐全" },
        { id: "source_grade", ok: true, detail: "中等级不得单独下单" },
        { id: "governance_g4", ok: false, detail: "回撤复核未闭环" },
      ],
      cs: [
        { op: "cs.book.query", level: "L1", side: "读" },
        { op: "cs.order.submit", level: "L3", side: "写，仅运行" },
      ],
    },
    runtime: {
      instance: "ins-hengchuan-book",
      scope: "dept",
      items: [
        { name: "持仓复核", advice: true, why: "回撤事件已入审计" },
        { name: "待下单单", advice: false, why: "信源等级中" },
      ],
      silent: "驾驶舱直接下单",
      action: "回撤超限复核（G4）",
    },
  },
};

const BUILDER_STEPS = [
  ["intent", "意图归一", true],
  ["wm", "世界模型", true],
  ["template", "模板", true],
  ["blueprint", "蓝图", true],
  ["assets", "资产", false],
  ["validate", "校验", false],
  ["release", "发布", false],
];

const SCENE = {
  ops: {
    period: "本周窗口",
    caliber: "接地率 = 有面试记录的建议 / 全部建议 · ATS + 面试纪要",
    composite: [
      { id: "fill", n: "编制填满", v: "72%", s: "价值流停在短名单" },
      { id: "ground", n: "证据接地", v: "61%", s: "环比 -4pp", hot: true, item: "wi-rao" },
      { id: "cycle", n: "周期", v: "38d", s: "短名单滞留" },
      { id: "gate", n: "卡口", v: "2", s: "未接地 + 冻结未批", hot: true, item: "wi-rao" },
    ],
    kpis: [
      { id: "ground", n: "接地率", v: "61%", s: "法则要求停手", hot: true, item: "wi-rao" },
      { id: "offer", n: "offer 接受", v: "44%", s: "不得用未接地分数" },
      { id: "learn", n: "待回写", v: "1", s: "ChangeSet 待确认" },
    ],
    funnel: [
      { id: "需求", count: 3, gate: false },
      { id: "sourcing", count: 8, gate: false },
      { id: "短名单", count: 3, gate: true },
      { id: "onsite", count: 1, gate: false },
      { id: "到岗", count: 0, gate: false },
    ],
    objects: {
      "wi-shortlist": {
        health: "warn",
        days: 6,
        signal: "三人窗口未关账，未接地仍可能混进建议",
        metrics: [
          { n: "在窗", v: "3" },
          { n: "接地", v: "1" },
          { n: "不确定", v: "1" },
          { n: "未接地", v: "1" },
        ],
        trend: [3, 3, 3, 3, 3],
        verdict: {
          level: "warn",
          title: "决策信号 · 预警",
          desc: "窗口未关。Rao 未接地，不能把三人名单当成可冻结产出。",
          signals: ["未接地分数仍在池里", "冻结尚未走 G3"],
        },
        actions: [
          { p: "P0", text: "核验 Rao culture_fit，未接地移出建议", owner: "林启明", exec: "explore", item: "wi-rao" },
          { p: "P1", text: "Patel oncall 向前任经理取证", owner: "招聘委员会", exec: "explore", item: "wi-patel" },
          { p: "P2", text: "陈予安证据包复核后进入建议", owner: "林启明", exec: "runtime", item: "wi-chen" },
        ],
        plan: [
          { task: "核验 Rao", owner: "林启明", due: "今日", p: "P0", status: "overdue", item: "wi-rao" },
          { task: "Patel 取证", owner: "招聘委员会", due: "本周四", p: "P1", status: "doing", item: "wi-patel" },
          { task: "冻结短名单", owner: "招聘委员会", due: "本周五", p: "P0", status: "todo", item: "wi-freeze" },
        ],
      },
      "wi-rao": {
        health: "gate",
        days: 9,
        signal: "culture_fit=0.86 无面试，阶段停留超阈值",
        metrics: [
          { n: "分数", v: "0.86" },
          { n: "面试", v: "0" },
          { n: "信源", v: "低" },
          { n: "停留", v: "9d" },
        ],
        trend: [0.81, 0.84, 0.86, 0.86, 0.86],
        verdict: {
          level: "gate",
          title: "决策信号 · 卡口",
          desc: "LAW-EVD-001：无面试不得当真。停手核实，不能发 offer。",
          signals: ["简历关键词分数未接地", "ATS 无面试纪要", "若进入建议即违规"],
        },
        actions: [
          { p: "P0", text: "签发研究：对照法则与证据，决定移出或补面试", owner: "林启明", exec: "explore", item: "wi-rao" },
          { p: "P1", text: "安排校准面试或移出建议", owner: "林启明", exec: "explore", item: "wi-rao" },
        ],
        plan: [
          { task: "核验 culture_fit", owner: "林启明", due: "今日", p: "P0", status: "overdue", item: "wi-rao" },
        ],
      },
      "wi-chen": {
        health: "ok",
        days: 4,
        signal: "面试证据接地，可进建议",
        metrics: [
          { n: "面试", v: "1" },
          { n: "信源", v: "高" },
          { n: "建议", v: "是" },
          { n: "停留", v: "4d" },
        ],
        trend: [0, 1, 1, 1, 1],
        verdict: {
          level: "ok",
          title: "决策信号 · 正常",
          desc: "系统设计题面可复核。进入建议；冻结仍要 G3。",
          signals: [],
        },
        actions: [
          { p: "P2", text: "复核证据包后纳入建议名单", owner: "林启明", exec: "runtime", item: "wi-chen" },
        ],
        plan: [{ task: "证据包复核", owner: "林启明", due: "本周五", p: "P2", status: "doing", item: "wi-chen" }],
      },
      "wi-patel": {
        health: "warn",
        days: 7,
        signal: "公开贡献密度高，oncall 无对内对照",
        metrics: [
          { n: "公开仓", v: "高" },
          { n: "对内", v: "无" },
          { n: "建议", v: "可" },
          { n: "停留", v: "7d" },
        ],
        trend: [0.6, 0.7, 0.7, 0.72, 0.72],
        verdict: {
          level: "warn",
          title: "决策信号 · 预警",
          desc: "可进建议但必须标不确定。取证前不当成已过关。",
          signals: ["仅 GitHub 公开仓库", "oncall 假设未核实"],
        },
        actions: [
          { p: "P1", text: "向前任经理取证 Patel oncall", owner: "招聘委员会", exec: "explore", item: "wi-patel" },
        ],
        plan: [{ task: "前任经理取证", owner: "招聘委员会", due: "本周四", p: "P1", status: "doing", item: "wi-patel" }],
      },
      "wi-freeze": {
        health: "warn",
        days: 0,
        signal: "应用已校验，冻结是组织承诺，须 G3",
        metrics: [
          { n: "Release", v: "否" },
          { n: "门禁", v: "G3" },
          { n: "回滚", v: "48h" },
          { n: "审批", v: "待" },
        ],
        trend: [0, 0, 0, 1, 1],
        verdict: {
          level: "warn",
          title: "决策信号 · 预警",
          desc: "未 Release 不能静默跑生产。冻结须审批，禁止场景直接写。",
          signals: ["实例未写入 live", "个人轨不得发 offer"],
        },
        actions: [
          { p: "P0", text: "进入运行：冻结短名单，走 G3 审批", owner: "招聘委员会", exec: "runtime", item: "wi-freeze" },
        ],
        plan: [{ task: "冻结短名单", owner: "招聘委员会", due: "本周五", p: "P0", status: "todo", item: "wi-freeze" }],
      },
    },
    assets: [
      { name: "LAW-EVD-001 无面试不得当真", effect: "拦截 1 次未接地建议", pct: 100, status: "生效" },
      { name: "短名单冻结 = 组织承诺", effect: "回滚窗口 48h，尚未使用", pct: 20, status: "待用" },
    ],
    learn: ["驳回把 Rao 纳入建议", "门禁拦住未接地写入", "法则再次确认", "同类窗口默认走研究", "ChangeSet 待人确认后回写"],
  },
  pmo: {
    period: "M2 窗口",
    caliber: "按期 = 里程碑按基线验收 / 全部里程碑 · 依赖图 + 周会",
    composite: [
      { id: "on", n: "按期", v: "64%", s: "M2 被挡住", hot: true, item: "wi-m2" },
      { id: "dep", n: "开着的依赖", v: "7", s: "Assignee 为空", hot: true, item: "wi-deps" },
      { id: "risk", n: "风险开", v: "3", s: "范围未冻" },
      { id: "gate", n: "卡口", v: "2", s: "无 Owner + 未冻" },
    ],
    kpis: [
      { id: "on", n: "按期", v: "64%", s: "验收门禁触发", hot: true, item: "wi-m2" },
      { id: "scope", n: "范围漂移", v: "12%", s: "基线未冻" },
      { id: "learn", n: "复盘", v: "1", s: "待回写" },
    ],
    funnel: [
      { id: "立项", count: 2, gate: false },
      { id: "计划", count: 3, gate: false },
      { id: "执行", count: 4, gate: true },
      { id: "验收", count: 1, gate: false },
      { id: "收尾", count: 1, gate: false },
    ],
    objects: {
      "wi-m2": {
        health: "gate",
        days: 11,
        signal: "7 条跨团队依赖无 Owner，停留超阈值",
        metrics: [
          { n: "依赖开", v: "7" },
          { n: "Owner", v: "0" },
          { n: "停留", v: "11d" },
          { n: "阈值", v: "7d" },
        ],
        trend: [2, 4, 6, 7, 7],
        verdict: {
          level: "gate",
          title: "决策信号 · 卡口",
          desc: "无 Owner 不得验收。不能在驾驶舱改计划。",
          signals: ["7 条边空 Assignee", "周会只有口头承诺"],
        },
        actions: [
          { p: "P0", text: "给七条依赖书面指定 Owner", owner: "周衡", exec: "explore", item: "wi-deps" },
          { p: "P1", text: "验收门禁复核，确认法则", owner: "周衡", exec: "explore", item: "wi-m2" },
        ],
        plan: [
          { task: "指定 Owner", owner: "周衡", due: "本周三", p: "P0", status: "todo", item: "wi-deps" },
          { task: "验收复核", owner: "周衡", due: "本周五", p: "P1", status: "doing", item: "wi-m2" },
        ],
      },
      "wi-deps": {
        health: "gate",
        days: 11,
        signal: "口头下周再分，未写入",
        metrics: [
          { n: "边", v: "7" },
          { n: "书面", v: "0" },
          { n: "口头", v: "3" },
          { n: "停留", v: "11d" },
        ],
        trend: [7, 7, 7, 7, 7],
        verdict: {
          level: "gate",
          title: "决策信号 · 卡口",
          desc: "口头不算 Owner。先指定再谈验收。",
          signals: ["Jira Assignee 为空"],
        },
        actions: [{ p: "P0", text: "书面指定 7 条依赖 Owner", owner: "周衡", exec: "explore", item: "wi-deps" }],
        plan: [{ task: "书面指定 Owner", owner: "周衡", due: "本周三", p: "P0", status: "todo", item: "wi-deps" }],
      },
      "wi-scope": {
        health: "warn",
        days: 5,
        signal: "范围冻结尚未校验",
        metrics: [
          { n: "冻结", v: "否" },
          { n: "门禁", v: "G3" },
          { n: "回滚", v: "48h" },
          { n: "校验", v: "未" },
        ],
        trend: [0, 0, 0, 0, 0],
        verdict: {
          level: "warn",
          title: "决策信号 · 预警",
          desc: "未校验不得改计划基线。带着空 Owner 强行验收会被拦住。",
          signals: ["governance_g3 未过"],
        },
        actions: [{ p: "P0", text: "进入运行：冻结 M2 范围", owner: "组合委员会", exec: "runtime", item: "wi-scope" }],
        plan: [{ task: "冻结范围", owner: "组合委员会", due: "本周五", p: "P0", status: "todo", item: "wi-scope" }],
      },
      "wi-m1": {
        health: "ok",
        days: 0,
        signal: "依赖已闭环，已验收",
        metrics: [
          { n: "依赖", v: "0" },
          { n: "验收", v: "是" },
          { n: "回写", v: "1" },
          { n: "停留", v: "0" },
        ],
        trend: [4, 2, 1, 0, 0],
        verdict: {
          level: "ok",
          title: "决策信号 · 正常",
          desc: "M1 已过关，可作本窗口对照。",
          signals: [],
        },
        actions: [{ p: "P2", text: "把 M1 过关条件沉淀进验收法则", owner: "周衡", exec: "builder", item: "wi-m1" }],
        plan: [{ task: "复盘回写", owner: "周衡", due: "已过", p: "P2", status: "done", item: "wi-m1" }],
      },
    },
    assets: [
      { name: "无 Owner 不得验收", effect: "拦住 1 次提前验收", pct: 90, status: "生效" },
      { name: "范围冻结 48h 回滚", effect: "尚未使用", pct: 20, status: "待用" },
    ],
    learn: ["发现依赖无 Owner", "验收被门禁拦住", "法则再次确认", "同类里程碑默认先研究", "ChangeSet 待确认"],
  },
  invest: {
    period: "本窗口",
    caliber: "信源等级：高 = 双源交叉；中不得单独下单 · 行情 + 研报 + 审计",
    composite: [
      { id: "dd", n: "回撤", v: "-6.1%", s: "已触发 G4", hot: true, item: "wi-dd" },
      { id: "src", n: "信源等级", v: "中", s: "不得单独下单", hot: true, item: "wi-order" },
      { id: "alpha", n: "因子有效", v: "0.18", s: "未交叉核验", item: "wi-factor" },
      { id: "gate", n: "卡口", v: "2", s: "回撤 + 下单" },
    ],
    kpis: [
      { id: "dd", n: "回撤", v: "-6.1%", s: "超 6% 复核", hot: true, item: "wi-dd" },
      { id: "exp", n: "敞口", v: "1.2x", s: "上限已触" },
      { id: "learn", n: "策略回收", v: "4", s: "待确认" },
    ],
    funnel: [
      { id: "研究", count: 5, gate: false },
      { id: "池", count: 3, gate: false },
      { id: "下单", count: 1, gate: true },
      { id: "持仓", count: 4, gate: true },
      { id: "复核", count: 2, gate: false },
    ],
    objects: {
      "wi-dd": {
        health: "gate",
        days: 2,
        signal: "回撤 -6.1%，复核未完成前禁止新开仓",
        metrics: [
          { n: "回撤", v: "-6.1%" },
          { n: "敞口", v: "1.2x" },
          { n: "门禁", v: "G4" },
          { n: "停留", v: "2d" },
        ],
        trend: [3.1, 4.0, 4.8, 5.5, 6.1],
        verdict: {
          level: "gate",
          title: "决策信号 · 卡口",
          desc: "回撤 6% 必须复核。禁止驾驶舱下单。",
          signals: ["回撤已入审计", "复核未闭环"],
        },
        actions: [{ p: "P0", text: "进入运行：回撤超限复核", owner: "风控", exec: "runtime", item: "wi-dd" }],
        plan: [{ task: "回撤复核", owner: "风控", due: "今日", p: "P0", status: "overdue", item: "wi-dd" }],
      },
      "wi-order": {
        health: "gate",
        days: 1,
        signal: "仅中等级研报，不得单独下单",
        metrics: [
          { n: "信源", v: "中" },
          { n: "交叉", v: "无" },
          { n: "金额", v: "冻结" },
          { n: "停留", v: "1d" },
        ],
        trend: [1, 1, 1, 1, 1],
        verdict: {
          level: "gate",
          title: "决策信号 · 卡口",
          desc: "中等级信源不得单独下单。先核验因子。",
          signals: ["缺第二信源", "回撤窗口重叠"],
        },
        actions: [
          { p: "P0", text: "驳回本笔下单，补交叉核验", owner: "沈澈", exec: "explore", item: "wi-order" },
          { p: "P1", text: "核验动量因子有效性", owner: "沈澈", exec: "explore", item: "wi-factor" },
        ],
        plan: [{ task: "驳回下单", owner: "沈澈", due: "冻结", p: "P0", status: "doing", item: "wi-order" }],
      },
      "wi-factor": {
        health: "warn",
        days: 5,
        signal: "有效性 0.18，尚未交叉核验",
        metrics: [
          { n: "有效", v: "0.18" },
          { n: "交叉", v: "否" },
          { n: "回收", v: "待" },
          { n: "停留", v: "5d" },
        ],
        trend: [0.22, 0.2, 0.19, 0.18, 0.18],
        verdict: {
          level: "warn",
          title: "决策信号 · 预警",
          desc: "未核验不得作为下单理由。研究完成后再谈仓位。",
          signals: ["单一研报"],
        },
        actions: [{ p: "P1", text: "签发研究：交叉核验动量因子", owner: "沈澈", exec: "explore", item: "wi-factor" }],
        plan: [{ task: "因子核验", owner: "沈澈", due: "本周", p: "P1", status: "doing", item: "wi-factor" }],
      },
    },
    assets: [
      { name: "中等级信源不得单独下单", effect: "拦住 1 次下单", pct: 100, status: "生效" },
      { name: "回撤 6% 触发复核", effect: "本窗口已触发", pct: 70, status: "生效" },
    ],
    learn: ["拦住中等级信源下单", "回撤事件记入审计", "法则再次确认", "同类窗口默认先研究", "策略回收待确认"],
  },
};

const state = {
  layer: "scene",
  pack: "ops",
  view: "loop",
  selectedId: "wi-rao",
  execFocus: "project",
  stageFilter: "",
  healthFilter: "",
  q: "",
  runs: {},
  hashLock: false,
};

function pack() {
  return PACKS[state.pack];
}

function scene() {
  return SCENE[state.pack];
}

function itemById(id) {
  return pack().items.find((x) => x.id === id) || pack().items[0];
}

function objOf(id) {
  const it = itemById(id);
  return { ...it, ...(scene().objects[id] || { health: "ok", days: 0, signal: it.gap, metrics: [], verdict: { level: "ok", title: "决策信号", desc: it.gap, signals: [] }, actions: [], plan: [] }) };
}

function runKey(id) {
  return state.pack + ":" + id;
}

function runOf(id) {
  return state.runs[runKey(id)] || null;
}

function ensureRun(id, mode) {
  const key = runKey(id);
  if (!state.runs[key]) {
    state.runs[key] = {
      mode: mode || itemById(id).exec,
      plan: "",
      notes: [],
      approved: false,
      denial: "",
      cycle: pack().project.cycle,
    };
  } else if (mode) {
    state.runs[key].mode = mode;
  }
  return state.runs[key];
}

function missingDim(wm) {
  return DIMS.filter(([k]) => !wm[k] || !String(wm[k]).trim()).map((d) => d[1]);
}

function toast(msg) {
  const el = $("toast");
  el.hidden = false;
  el.innerHTML = msg;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => {
    el.hidden = true;
  }, 4200);
}

function route() {
  if (state.layer === "scene") return "#/" + state.pack + "/scene/" + state.view;
  if (state.execFocus === "task") return "#/" + state.pack + "/exec/task/" + state.selectedId;
  return "#/" + state.pack + "/exec/project";
}

function syncHash(push) {
  const next = route();
  if (location.hash === next) return;
  state.hashLock = true;
  if (push) history.pushState(null, "", next);
  else history.replaceState(null, "", next);
  queueMicrotask(() => {
    state.hashLock = false;
  });
}

function readHash() {
  const raw = location.hash.replace(/^#\/?/, "");
  const parts = raw.split("/").filter(Boolean);
  if (!parts.length) return false;
  if (PACKS[parts[0]]) {
    state.pack = parts[0];
    $("pack").value = state.pack;
  }
  if (parts[1] === "exec") {
    state.layer = "execute";
    if (parts[2] === "task" && parts[3] && pack().items.some((i) => i.id === parts[3])) {
      state.execFocus = "task";
      state.selectedId = parts[3];
    } else {
      state.execFocus = "project";
    }
    return true;
  }
  if (parts[1] === "scene") {
    state.layer = "scene";
    const view = LEGACY_VIEW[parts[2]] || parts[2];
    if (view && VIEWS.some((v) => v[0] === view)) state.view = view;
    return true;
  }
  return false;
}

function setLayer(layer, push) {
  state.layer = layer;
  if (layer === "execute" && state.execFocus !== "task") state.execFocus = "project";
  render(true);
  syncHash(push);
}

function kpiCards() {
  return `<div class="kpis">${pack()
    .kpis.map(
      (k) =>
        `<button type="button" class="kpi ${k.hot ? "hot" : ""}" data-kpi="${k.id}">
          <span>${esc(k.n)}</span><b>${esc(k.v)}</b>
        </button>`
    )
    .join("")}</div>`;
}

function table(rows, cols) {
  return `<table class="table">
    <thead><tr>${cols.map((c) => `<th>${c[1]}</th>`).join("")}</tr></thead>
    <tbody>${rows
      .map((r) => {
        const pick = r.id && pack().items.some((i) => i.id === r.id);
        return `<tr${pick ? ` data-item="${r.id}"` : ""} class="${pick && state.selectedId === r.id ? "is-on" : ""}">${cols
          .map((c) => `<td>${c[2](r)}</td>`)
          .join("")}</tr>`;
      })
      .join("")}</tbody>
  </table>`;
}

function itemCols() {
  return [
    ["code", "编号", (r) => `<span class="tag">${esc(r.code)}</span>`],
    ["title", "工作项", (r) => `${r.hot ? '<span class="dot red"></span>' : ""}<strong>${esc(r.title)}</strong>`],
    ["stage", "阶段", (r) => esc(r.stage)],
    ["owner", "负责人", (r) => esc(r.owner)],
    ["col", "状态", (r) => COLS.find((c) => c[0] === r.col)?.[1] || r.col],
    ["due", "窗口", (r) => esc(r.due)],
  ];
}

function renderRail() {
  $("nav-space").textContent = pack().space;
  if (state.layer === "scene") {
    $("rail-nav").innerHTML = VIEWS.map(
      ([id, name]) =>
        `<button type="button" data-view="${id}" class="${state.view === id ? "is-on" : ""}">${name}</button>`
    ).join("");
    return;
  }
  const prj = pack().project;
  const onPrj = state.execFocus === "project";
  $("rail-nav").innerHTML = `
    <p class="rail-label">项目</p>
    <button type="button" data-exec-focus="project" class="${onPrj ? "is-on" : ""}">
      ${esc(prj.title)}
      <small>${esc(prj.code)} · ${esc(prj.window)}</small>
    </button>
    <p class="rail-label">任务</p>
    ${pack()
      .items.map((it) => {
        const run = runOf(it.id);
        const mode = run ? MODE_ZH[run.mode] : "未进入";
        return `<button type="button" class="child ${state.execFocus === "task" && state.selectedId === it.id ? "is-on" : ""}" data-exec-task="${it.id}">
          ${esc(it.title)}
          <small>${esc(it.code)} · ${mode} · ${esc(it.owner)}</small>
        </button>`;
      })
      .join("")}
  `;
}

function filteredObjects() {
  const q = state.q.trim().toLowerCase();
  return pack()
    .items.map((it) => objOf(it.id))
    .filter((o) => !state.stageFilter || o.stage === state.stageFilter)
    .filter((o) => !state.healthFilter || o.health === state.healthFilter)
    .filter((o) => !q || `${o.title}${o.code}${o.signal}`.toLowerCase().includes(q));
}

function spark(points) {
  if (!points || points.length < 2) return "";
  const w = 120;
  const h = 28;
  const max = Math.max(...points);
  const min = Math.min(...points);
  const d = points
    .map((p, i) => {
      const x = (i / (points.length - 1)) * w;
      const y = h - ((p - min) / (max - min || 1)) * (h - 4) - 2;
      return `${i ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
  return `<svg class="spark" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" aria-hidden="true"><path d="${d}" fill="none" stroke="#3370ff" stroke-width="1.6"/></svg>`;
}

function healthTag(h) {
  if (h === "gate") return `<span class="tag hot">卡口</span>`;
  if (h === "warn") return `<span class="tag warn">预警</span>`;
  return `<span class="tag ok">正常</span>`;
}

function planStatus(s) {
  const map = { todo: "待做", doing: "进行", done: "完成", overdue: "逾期" };
  const cls = s === "overdue" ? "hot" : s === "done" ? "ok" : s === "doing" ? "mode" : "";
  return `<span class="tag ${cls}">${map[s] || s}</span>`;
}

function renderLoopMain() {
  const p = pack();
  const sc = scene();
  const list = filteredObjects();
  const current = objOf(state.selectedId);
  const cols = sc.funnel.length;
  const shallow = p.deep
    ? ""
    : `<p class="lead">T0 浅壳：同一套数据 → 决策 → 优化 → 沉淀，客体换成${p.id === "pmo" ? "项目与里程碑" : "组合与仓位"}。</p>`;

  return `
    <div class="loop" aria-hidden="true">
      <i class="on">数据</i><i class="on">决策</i><i>优化</i><i>沉淀</i>
    </div>
    <div class="sec"><h2>数据</h2><span class="note">${esc(sc.period)} · ${esc(sc.caliber)}</span></div>
    ${shallow}
    <div class="loop-kpis">
      <button type="button" class="ktile" data-kpi="${sc.composite[1].id}">
        <div class="l">当前主张力</div>
        <div class="v">${esc(sc.composite.filter((x) => x.hot)[0]?.v || sc.composite[0].v)}</div>
        <div class="s">${esc(p.tension)}</div>
        <div class="km-grid">${sc.composite
          .map(
            (k) =>
              `<div class="km"><div class="l">${esc(k.n)}</div><div class="v ${k.hot ? "hot" : ""}">${esc(k.v)}</div></div>`
          )
          .join("")}</div>
      </button>
      ${sc.kpis
        .map(
          (k) =>
            `<button type="button" class="ktile ${k.hot ? "hot" : ""}" data-kpi="${k.id}">
              <div class="l">${esc(k.n)}</div>
              <div class="v">${esc(k.v)}</div>
              <div class="s">${esc(k.s)}</div>
            </button>`
        )
        .join("")}
    </div>
    <div class="filter-bar">
      <label>搜索<input id="f-q" value="${esc(state.q)}" placeholder="编号 / 对象 / 信号" /></label>
      <label>健康
        <select id="f-health">
          <option value="">全部</option>
          <option value="gate" ${state.healthFilter === "gate" ? "selected" : ""}>仅卡口</option>
          <option value="warn" ${state.healthFilter === "warn" ? "selected" : ""}>仅预警</option>
          <option value="ok" ${state.healthFilter === "ok" ? "selected" : ""}>仅正常</option>
        </select>
      </label>
      <div class="legend">
        <span><span class="dot green"></span>正常</span>
        <span><span class="dot amber"></span>预警</span>
        <span><span class="dot red"></span>卡口</span>
      </div>
    </div>
    <div class="sec"><h2>价值流</h2><span class="note">点阶段筛选对象，再看 360 决策信号</span></div>
    <div class="funnel" style="grid-template-columns:repeat(${cols},minmax(0,1fr))">
      ${sc.funnel
        .map(
          (f) =>
            `<button type="button" class="fp ${f.gate ? "gate" : ""} ${state.stageFilter === f.id ? "is-on" : ""}" data-stage="${f.id}">
              <div class="n">${f.gate ? "卡口" : "阶段"}</div>
              <div class="name">${esc(f.id)}</div>
              <div class="c">${f.count}</div>
            </button>`
        )
        .join("")}
    </div>
    <div class="sec"><h2>决策</h2><span class="note">过关判断留下五维，动作进入执行态</span></div>
    <div class="workbench">
      <div class="clist">
        <div class="clist-head"><span>对象</span><span>${list.length}</span></div>
        <div class="clist-body">
          ${
            list.length
              ? list
                  .map(
                    (o) => `
            <button type="button" class="crow ${o.health} ${state.selectedId === o.id ? "is-on" : ""}" data-item="${o.id}">
              <div class="mid"><strong>${esc(o.title)}</strong>${healthTag(o.health)}</div>
              <div class="mid"><span>${esc(o.stage)}</span><span>${o.days}d</span></div>
              <div class="sig">${esc(o.signal)}</div>
            </button>`
                  )
                  .join("")
              : `<p class="empty">没有匹配对象。重置筛选。</p>`
          }
        </div>
      </div>
      <article class="detail">
        <div class="detail-head">
          <h1>${esc(current.title)}</h1>
          <p class="meta">${esc(current.code)} · ${esc(current.owner)} · ${esc(current.gate)} · 停留 ${current.days}d</p>
          <div class="stabs">
            ${sc.funnel
              .map(
                (f) =>
                  `<button type="button" class="stab ${current.stage === f.id ? "on" : ""}" data-stage="${f.id}">${esc(f.id)}</button>`
              )
              .join("")}
          </div>
        </div>
        <div class="detail-body">
          <div class="verdict ${current.verdict.level}">
            <b>${esc(current.verdict.title)}</b>
            <p>${esc(current.verdict.desc)}</p>
          </div>
          <div class="dgrid">
            ${(current.metrics || [])
              .map((m) => `<div class="dtile"><div class="l">${esc(m.n)}</div><div class="v">${esc(m.v)}</div></div>`)
              .join("")}
          </div>
          ${current.trend ? `<div class="block"><h3>趋势</h3>${spark(current.trend)}</div>` : ""}
          <div class="split3" style="margin-bottom:14px">
            <div class="panel"><h3>应当</h3><p>${esc(current.ought)}</p></div>
            <div class="panel"><h3>事实</h3><p>${esc(current.is)}</p></div>
            <div class="panel"><h3>缺口</h3><p>${esc(current.gap)}</p></div>
          </div>
          <div class="block">
            <h3>过关动作</h3>
            ${(current.actions || [])
              .map(
                (a, i) => `
              <div class="act ${a.p.toLowerCase()}">
                <span class="act-tag">${a.p}</span>
                <div>
                  <div>${esc(a.text)}</div>
                  <div class="meta" style="margin:4px 0 0">${esc(a.owner)} · 建议${MODE_ZH[a.exec]}</div>
                  <div class="row" style="margin-top:8px">
                    <button type="button" class="${i === 0 ? "primary" : "ghost"}" data-enter="${a.exec}" data-enter-item="${a.item || current.id}">进入${MODE_ZH[a.exec]}</button>
                  </div>
                </div>
              </div>`
              )
              .join("")}
          </div>
          <div class="block">
            <h3>计划</h3>
            ${table(
              (current.plan || []).map((r, i) => ({ ...r, id: r.item || current.id + "-p" + i })),
              [
                ["p", "级", (r) => esc(r.p)],
                ["task", "事项", (r) => esc(r.task)],
                ["owner", "负责人", (r) => esc(r.owner)],
                ["due", "窗口", (r) => esc(r.due)],
                ["status", "状态", (r) => planStatus(r.status)],
              ]
            )}
          </div>
          <p class="meta">场景态只做数据到决策。写生产必须进执行态运行环位。</p>
        </div>
      </article>
    </div>
  `;
}

function renderOptimizeMain() {
  const p = pack();
  const sc = scene();
  const plans = p.items.flatMap((it) => (objOf(it.id).plan || []).map((r) => ({ ...r, id: r.item || it.id, title: it.title })));
  const returns = p.items
    .map((it) => ({ it, run: runOf(it.id) }))
    .filter((x) => x.run);
  return `
    <div class="loop" aria-hidden="true">
      <i>数据</i><i>决策</i><i class="on">优化</i><i>沉淀</i>
    </div>
    <div class="sec"><h2>优化</h2><span class="note">执行回流后的 Check / Act。状态不在聊天里。</span></div>
    <p class="lead">${esc(p.tension)}</p>
    ${cycleHtml(p.project.cycle)}
    <div class="panel" style="margin-bottom:12px">
      <h3>执行回流</h3>
      ${
        returns.length
          ? `<ul>${returns
              .map(
                (x) =>
                  `<li><button type="button" class="text-btn" data-open-exec="task" data-item="${x.it.id}">${esc(x.it.title)}</button> · ${MODE_ZH[x.run.mode]} · ${
                    x.run.approved ? "已写入 live" : x.run.notes.length ? x.run.notes.length + " 条注释" : "进行中"
                  }</li>`
              )
              .join("")}</ul>`
          : `<p class="empty">还没有任务从执行态回来。先在闭环里点过关动作。</p>`
      }
    </div>
    <div class="sec"><h2>本窗口计划</h2></div>
    ${table(plans, [
      ["title", "对象", (r) => esc(r.title || itemById(r.id).title)],
      ["p", "级", (r) => esc(r.p)],
      ["task", "事项", (r) => esc(r.task)],
      ["owner", "负责人", (r) => esc(r.owner)],
      ["status", "状态", (r) => planStatus(r.status)],
    ])}
    <div class="panel" style="margin-top:14px">
      <h3>下一轮该改什么</h3>
      <ol>${sc.learn.map((x) => `<li>${esc(x)}</li>`).join("")}</ol>
    </div>
  `;
}

function renderDepositMain() {
  const sc = scene();
  const p = pack();
  return `
    <div class="loop" aria-hidden="true">
      <i>数据</i><i>决策</i><i>优化</i><i class="on">沉淀</i>
    </div>
    <div class="sec"><h2>沉淀</h2><span class="note">策略资产与法则回写。禁止静默改知识。</span></div>
    <p class="lead">效果回收后，人确认 ChangeSet，才变成下一轮数据的口径。</p>
    ${sc.assets
      .map(
        (a) => `
      <article class="goal">
        <h3>${esc(a.name)} <span class="tag ${a.status === "生效" ? "ok" : "warn"}">${esc(a.status)}</span></h3>
        <p class="meta">${esc(a.effect)}</p>
        <div class="bar"><i style="width:${a.pct}%"></i></div>
      </article>`
      )
      .join("")}
    <div class="panel">
      <h3>待确认回写</h3>
      <p>${esc(sc.learn[sc.learn.length - 1])}</p>
      <div class="row">
        <button type="button" class="ghost" data-act="changeset">生成 ChangeSet（待人确认）</button>
        <button type="button" class="danger" data-act="silent-learn">静默回写法则</button>
      </div>
    </div>
    <p class="meta">${esc(p.dikw[3])} ← 上一轮 ${esc(p.dikw[0])}</p>
  `;
}

function renderSceneMain() {
  if (state.view === "optimize") return renderOptimizeMain();
  if (state.view === "deposit") return renderDepositMain();
  return renderLoopMain();
}

function cycleHtml(current) {
  const idx = CYCLE.findIndex((c) => c[0] === current);
  return `<div class="cycle">${CYCLE.map(
    ([id, n], i) => `<span class="${id === current ? "on" : i < idx ? "done" : ""}">${esc(n)}</span>`
  ).join("")}</div>`;
}

function dimsHtml(wm) {
  return `<div class="dims">${DIMS.map(
    ([k, n]) =>
      `<article><b>${n}</b><p>${wm[k] ? esc(wm[k]) : '<span class="tag hot">缺失</span>'}</p></article>`
  ).join("")}</div>`;
}

function renderProjectMain() {
  const p = pack();
  const prj = p.project;
  const entered = p.items.filter((i) => runOf(i.id)).length;
  const blocked = p.items.filter((i) => i.col === "blocked").length;
  return `
    <div class="object-bar">
      <div>
        <h1>${esc(prj.title)}</h1>
        <p class="meta">${esc(prj.code)} · ${esc(p.owner)} / ${esc(p.role)} · ${esc(prj.window)}</p>
      </div>
    </div>
    <p class="lead">${esc(p.tension)}</p>
    ${cycleHtml(prj.cycle)}
    <div class="kpis">
      <button type="button" class="kpi"><span>任务</span><b>${p.items.length}</b></button>
      <button type="button" class="kpi"><span>已进入执行</span><b>${entered}</b></button>
      <button type="button" class="kpi ${blocked ? "hot" : ""}"><span>阻塞</span><b>${blocked}</b></button>
    </div>
    <div class="panel" style="margin-bottom:16px">
      <h3>对象链</h3>
      <p>${esc(prj.object)}</p>
      <p class="meta" style="margin:8px 0 0">执行态看的是项目与任务，不是对话 session。</p>
    </div>
    ${table(
      p.items,
      [
        ...itemCols(),
        [
          "run",
          "执行环位",
          (r) => {
            const run = runOf(r.id);
            return run ? `<span class="tag mode">${MODE_ZH[run.mode]}</span>` : `<span class="tag">未进入</span>`;
          },
        ],
      ]
    )}
  `;
}

function exploreCanvas(p, it, run) {
  return `
    <div class="split3">
      <div class="panel"><h3>应当</h3><p>${esc(it.ought)}</p></div>
      <div class="panel"><h3>事实</h3><p>${esc(it.is)}</p></div>
      <div class="panel"><h3>缺口</h3><p>${esc(it.gap)}</p></div>
    </div>
    <div class="panel" style="margin-bottom:12px">
      <h3>证据</h3>
      ${table(
        p.evidence.map((e, i) => ({ ...e, id: "ev-" + i })),
        [
          ["source", "来源", (r) => esc(r.source)],
          ["reliability", "等级", (r) => esc(r.reliability)],
          ["excerpt", "摘录", (r) => esc(r.excerpt)],
        ]
      )}
    </div>
    <div class="panorama">
      <div class="panel">
        <h3>不确定点</h3>
        <ul>${p.uncertainties.map((u) => `<li><b>${esc(u.claim)}</b>：${esc(u.why)}。${esc(u.ask)}</li>`).join("")}</ul>
      </div>
      <div class="panel">
        <h3>方案对冲</h3>
        <ul>${p.options.map((o) => `<li><b>${o.id}</b> ${esc(o.summary)}（风险：${esc(o.risk)}）</li>`).join("")}</ul>
      </div>
    </div>
    <div class="panel">
      <h3>所用知识</h3>
      <ul>${p.knowledge
        .map(
          (k) =>
            `<li>${esc(k.id)} · ${esc(k.type)} · ${
              k.installed ? '<span class="tag ok">已装</span>' : '<span class="tag warn">未装，仅 cite</span>'
            }</li>`
        )
        .join("")}</ul>
    </div>
    ${run.plan ? `<div class="panel" style="margin-top:12px"><h3>计划</h3><p>${esc(run.plan)}</p></div>` : ""}
  `;
}

function builderCanvas(p, run) {
  const b = p.builder;
  return `
    <p class="lead">应用：${esc(b.app)}。无世界模型分析不得生成资产。${b.released ? "已 Release。" : "尚未 Release。"}</p>
    <ul class="steps">${BUILDER_STEPS.map(
      ([id, n, ok]) =>
        `<li><span class="dot ${ok ? "green" : "gray"}"></span><span>${esc(n)}</span><span class="tag">${ok ? "过" : "未过"}</span></li>`
    ).join("")}</ul>
    <div class="panel" style="margin:12px 0">
      <h3>Invariants</h3>
      <ul>${b.invariants
        .map((i) => `<li>${esc(i.id)} · ${i.ok ? '<span class="tag ok">过</span>' : '<span class="tag hot">挡</span>'} ${esc(i.detail)}</li>`)
        .join("")}</ul>
    </div>
    <div class="panel">
      <h3>cs.* 绑定</h3>
      <ul>${b.cs.map((c) => `<li><code>${esc(c.op)}</code> ${esc(c.level)} · ${esc(c.side)}</li>`).join("")}</ul>
    </div>
    ${run.plan ? `<div class="panel" style="margin-top:12px"><h3>计划</h3><p>${esc(run.plan)}</p></div>` : ""}
  `;
}

function runtimeCanvas(p, run) {
  const r = p.runtime;
  return `
    <p class="lead">实例 ${esc(r.instance)} · scope ${esc(r.scope)}。状态在世界模型，不在聊天。</p>
    ${cycleHtml(run.cycle)}
    <div class="panel" style="margin-bottom:12px">
      <h3>建议动作</h3>
      ${table(
        r.items.map((x, i) => ({ ...x, id: "rt-" + i })),
        [
          ["name", "客体", (row) => esc(row.name)],
          ["advice", "进入建议", (row) => (row.advice ? '<span class="tag ok">是</span>' : '<span class="tag hot">否</span>')],
          ["why", "理由", (row) => esc(row.why)],
        ]
      )}
    </div>
    ${
      run.approved
        ? `<p class="meta">已批准写入 live，记入审计。回滚窗口 48h。</p>
           <div class="diff"><span class="del">- instance.status: draft</span>
<span class="add">+ instance.status: committed
+ audit.append: ${esc(r.action)}</span></div>`
        : `<div class="approval">
            <p>${esc(r.action)} 待批。通过后才写入 live。</p>
            <div class="row">
              <button type="button" class="primary" data-act="approve">批准写入</button>
              <button type="button" class="ghost" data-act="reject-write">驳回</button>
            </div>
          </div>`
    }
    ${run.denial ? `<p class="deny">${esc(run.denial)}</p>` : ""}
    ${run.plan ? `<div class="panel" style="margin-top:12px"><h3>计划</h3><p>${esc(run.plan)}</p></div>` : ""}
  `;
}

function renderTaskMain() {
  const p = pack();
  const it = itemById(state.selectedId);
  const run = runOf(it.id);
  const mode = run ? run.mode : it.exec;
  const entered = !!run;
  return `
    <div class="object-bar">
      <div>
        <h1>${esc(it.title)}</h1>
        <p class="meta">${esc(it.code)} · ${esc(it.type)} · ${esc(it.owner)} · ${esc(it.gate)} · ${esc(it.due)} · ${
          entered ? MODE_ZH[mode] : "尚未进入执行环位"
        }</p>
      </div>
      <div class="modes">
        ${["explore", "builder", "runtime"]
          .map(
            (m) =>
              `<button type="button" class="ghost ${entered && mode === m ? "is-on" : ""}" data-enter="${m}">${MODE_ZH[m]}</button>`
          )
          .join("")}
      </div>
    </div>
    ${dimsHtml(it.wm)}
    ${
      entered
        ? mode === "explore"
          ? exploreCanvas(p, it, run)
          : mode === "builder"
            ? builderCanvas(p, run)
            : runtimeCanvas(p, run)
        : `<div class="split3">
            <div class="panel"><h3>应当</h3><p>${esc(it.ought)}</p></div>
            <div class="panel"><h3>事实</h3><p>${esc(it.is)}</p></div>
            <div class="panel"><h3>缺口</h3><p>${esc(it.gap)}</p></div>
          </div>
          <p class="lead">这是任务对象，不是一段对话。选择研究 / 构建 / 运行后，核心信息留在本页。</p>`
    }
    ${
      run?.notes?.length
        ? `<div class="panel" style="margin-top:12px"><h3>任务注释</h3><ul class="note-list">${run.notes
            .map((n) => `<li>${esc(n)}</li>`)
            .join("")}</ul></div>`
        : ""
    }
  `;
}

function renderInspector() {
  const it = itemById(state.selectedId);
  const miss = missingDim(it.wm);
  const run = runOf(it.id);

  if (state.layer === "scene") {
    const o = objOf(it.id);
    $("inspector").innerHTML = `
      <h2>${esc(it.title)}</h2>
      <p class="meta">${esc(it.code)} · ${healthTag(o.health)} · ${esc(it.gate)}</p>
      <div class="block"><h3>决策信号</h3><p>${esc(o.verdict?.desc || it.gap)}</p></div>
      <p class="meta">数据 → 决策在闭环页。这里把过关动作送进执行态。</p>
      <div class="row">
        <button type="button" class="primary" data-enter="${it.exec}">进入${MODE_ZH[it.exec]}</button>
        <button type="button" class="ghost" data-view="loop">回闭环</button>
      </div>
      ${miss.length ? `<p class="meta">缺 ${esc(miss.join("、"))}，不能当生产动作。</p>` : ""}
      <div class="row"><button type="button" class="danger" data-act="scene-write">在场景直接改生产</button></div>
    `;
    return;
  }

  if (state.execFocus === "project") {
    const prj = pack().project;
    $("inspector").innerHTML = `
      <h2>${esc(prj.title)}</h2>
      <p class="meta">${esc(prj.code)} · ${esc(pack().owner)}</p>
      <div class="block"><h3>当前张力</h3><p>${esc(pack().tension)}</p></div>
      <div class="block"><h3>价值闭环</h3>${cycleHtml(prj.cycle)}</div>
      <p class="meta">点左侧任务看对象详情。对话不是这一层的根。</p>
      <div class="row"><button type="button" class="ghost" data-layer="scene">回场景闭环</button></div>
    `;
    return;
  }

  const mode = run ? run.mode : it.exec;
  $("inspector").innerHTML = `
    <h2>${esc(it.title)}</h2>
    <p class="meta">${esc(it.code)} · ${run ? MODE_ZH[mode] : "未进入"} · ${esc(it.gate)}</p>
    <div class="block"><h3>权限</h3><p class="perm">${esc(PERM[mode])}</p></div>
    <div class="block"><h3>下一步</h3>
      <p>${
        !run
          ? "进入研究，先把五维和证据摊开。"
          : mode === "explore"
            ? "五维与证据齐后，晋升到构建。"
            : mode === "builder"
              ? pack().builder.invariants.every((i) => i.ok)
                ? "Invariants 已过，可晋升到运行。"
                : "有 invariant 未过，不能上运行。"
              : "写操作须批准。禁止静默对外承诺。"
      }</p>
    </div>
    <div class="row">
      ${
        run?.mode === "explore"
          ? `<button type="button" class="primary" data-act="promote">晋升到构建</button>`
          : run?.mode === "builder"
            ? `<button type="button" class="primary" data-act="promote">晋升到运行</button>`
            : ""
      }
      <button type="button" class="ghost" data-layer="scene">回场景定位</button>
    </div>
    <div class="row"><button type="button" class="danger" data-act="silent">${esc(pack().runtime.silent)}</button></div>
  `;
}

function renderDock() {
  const show = state.layer === "execute" && state.execFocus === "task" && !!runOf(state.selectedId);
  $("dock").hidden = !show;
  if (!show) return;
  const run = runOf(state.selectedId);
  $("perm-badge").textContent = PERM[run.mode];
  $("dock-hint").textContent =
    run.mode === "runtime" ? "注释挂在实例上，不覆盖 live 状态。" : "补充写入当前任务对象。";
}

function bindSceneFilters() {
  const q = $("f-q");
  const h = $("f-health");
  if (q) {
    q.oninput = () => {
      state.q = q.value;
      render(false);
      $("f-q")?.focus();
      const el = $("f-q");
      if (el) el.selectionStart = el.selectionEnd = el.value.length;
    };
  }
  if (h) {
    h.onchange = () => {
      state.healthFilter = h.value;
      render(false);
    };
  }
}

function render(animate) {
  document.querySelectorAll("[data-layer]").forEach((b) => {
    b.classList.toggle("is-on", b.dataset.layer === state.layer);
  });
  $("workspace").classList.toggle("wide", state.layer === "scene" && state.view === "loop");
  renderRail();
  const html =
    state.layer === "scene"
      ? renderSceneMain()
      : state.execFocus === "project"
        ? renderProjectMain()
        : renderTaskMain();
  const main = $("main");
  main.innerHTML = html;
  if (animate) {
    main.classList.remove("is-swap");
    void main.offsetWidth;
    main.classList.add("is-swap");
  }
  renderInspector();
  renderDock();
  bindSceneFilters();
}

function enterTask(id, mode, fromScene) {
  const it = itemById(id);
  const miss = missingDim(it.wm);
  if (mode === "runtime" && miss.length) {
    toast(`任务未建模：缺 ${esc(miss.join("、"))}。`);
    return;
  }
  if (mode === "builder" && miss.length) {
    toast(`不能进入构建：缺 ${esc(miss.join("、"))}。`);
    return;
  }
  if (mode === "runtime") {
    const existing = runOf(id);
    if (existing && existing.mode !== "runtime") {
      const blocked = pack().builder.invariants.some((i) => !i.ok);
      if (blocked) {
        toast("Builder invariant 未过，不能上运行。");
        return;
      }
    }
  }
  state.selectedId = id;
  state.execFocus = "task";
  state.layer = "execute";
  ensureRun(id, mode || it.exec);
  render(true);
  syncHash(true);
  if (fromScene) toast(`已进入${MODE_ZH[runOf(id).mode]}。对象仍是 ${esc(it.code)}。`);
}

function promote() {
  const run = runOf(state.selectedId);
  const it = itemById(state.selectedId);
  if (!run) return;
  if (run.mode === "explore") {
    const miss = missingDim(it.wm);
    if (miss.length) {
      toast(`不能晋升：缺 ${esc(miss.join("、"))}。`);
      return;
    }
    run.mode = "builder";
    toast("已晋升到构建。Theme 绑定到 Blueprint。");
  } else if (run.mode === "builder") {
    if (pack().builder.invariants.some((i) => !i.ok)) {
      toast("invariant 未过，不能创建实例。");
      return;
    }
    run.mode = "runtime";
    toast("已晋升到运行。等待门禁批准后写入 live。");
  }
  render(true);
  syncHash(false);
}

function writeNote(text, asPlan) {
  const run = runOf(state.selectedId);
  if (!run) {
    toast("先进入研究 / 构建 / 运行，再写进任务。");
    return;
  }
  const raw = (text || "").trim();
  if (asPlan) {
    run.plan =
      run.mode === "explore"
        ? "规格 → 信源分级 → 五维对照法则 → 主题方案。未装 Skill 只 cite。"
        : run.mode === "builder"
          ? "跑 invariants；不过门禁不得 Release。cs.* 只绑定不执行。"
          : "只提交带权动作。高影响升级。状态写实例，不写对话。";
    toast("计划已写进任务对象。");
    render(false);
    return;
  }
  if (!raw) return;
  const wantsWrite = /offer|下单|改计划|发信|cs\.|冻结|写生产|直接执行/.test(raw);
  if (run.mode !== "runtime" && wantsWrite) {
    run.denial = "PROFILE_FORBIDS_SIDE_EFFECT · 研究/构建禁写生产。";
    toast("已拒绝写入生产。注释未当作动作。");
  } else if (run.mode === "runtime" && /offer|下单|发信|静默/.test(raw)) {
    run.denial = "TRACK_ESCALATION_REQUIRED · 个人轨不得对外承诺。";
    toast("已升级拦截。live 未改。");
  } else {
    run.notes.push(raw);
    toast("已写入任务注释。");
  }
  $("composer-input").value = "";
  render(false);
}

function approveWrite(ok) {
  const run = runOf(state.selectedId);
  if (!run || run.mode !== "runtime") {
    toast("只有运行环位才能批准写入。");
    return;
  }
  run.approved = ok;
  run.denial = ok ? "" : "已驳回。live 未改。";
  toast(ok ? "已写入 live，并记入审计。" : "已驳回。");
  render(false);
}

document.addEventListener("click", (e) => {
  const layer = e.target.closest("[data-layer]");
  if (layer) {
    if (layer.dataset.layer === "scene") {
      state.layer = "scene";
      if (!VIEWS.some((v) => v[0] === state.view)) state.view = "loop";
      render(true);
      syncHash(true);
    } else {
      state.layer = "execute";
      state.execFocus = "task";
      render(true);
      syncHash(true);
    }
    return;
  }
  const view = e.target.closest("[data-view]");
  if (view) {
    state.view = view.dataset.view;
    render(true);
    syncHash(true);
    return;
  }
  const stage = e.target.closest("[data-stage]");
  if (stage && state.layer === "scene") {
    state.stageFilter = state.stageFilter === stage.dataset.stage ? "" : stage.dataset.stage;
    const list = filteredObjects();
    if (list.length && !list.some((o) => o.id === state.selectedId)) state.selectedId = list[0].id;
    render(true);
    syncHash(false);
    return;
  }
  const kpi = e.target.closest("[data-kpi]");
  if (kpi && state.layer === "scene") {
    const meta = [...scene().composite, ...scene().kpis].find((k) => k.id === kpi.dataset.kpi);
    if (meta?.item) {
      state.selectedId = meta.item;
      state.view = "loop";
    }
    toast(esc(meta?.s || "已下钻到对象。"));
    render(true);
    syncHash(true);
    return;
  }
  const item = e.target.closest("[data-item]");
  if (item) {
    state.selectedId = item.dataset.item;
    if (item.hasAttribute("data-open-exec")) {
      state.execFocus = "task";
      setLayer("execute", true);
      return;
    }
    if (state.layer === "execute") state.execFocus = "task";
    render(true);
    syncHash(true);
    return;
  }
  const focus = e.target.closest("[data-exec-focus]");
  if (focus) {
    state.execFocus = "project";
    render(true);
    syncHash(true);
    return;
  }
  const task = e.target.closest("[data-exec-task]");
  if (task) {
    state.selectedId = task.dataset.execTask;
    state.execFocus = "task";
    render(true);
    syncHash(true);
    return;
  }
  const open = e.target.closest("[data-open-exec]");
  if (open) {
    state.execFocus = "task";
    setLayer("execute", true);
    return;
  }
  const enter = e.target.closest("[data-enter]");
  if (enter) {
    const id = enter.dataset.enterItem || state.selectedId;
    enterTask(id, enter.dataset.enter, state.layer === "scene");
    return;
  }
  const act = e.target.closest("[data-act]");
  if (!act) return;
  if (act.dataset.act === "plan") writeNote("", true);
  if (act.dataset.act === "promote") promote();
  if (act.dataset.act === "approve") approveWrite(true);
  if (act.dataset.act === "reject-write") approveWrite(false);
  if (act.dataset.act === "scene-write") {
    toast("场景态禁止 <code>cs.*</code> 写生产。进入运行并走门禁。");
  }
  if (act.dataset.act === "changeset") {
    toast("已生成 ChangeSet 草稿。等人确认后才回写法则，不静默生效。");
  }
  if (act.dataset.act === "silent-learn") {
    toast("升维回写禁止静默。与 Runtime 相同，必须走 ChangeSet。");
  }
  if (act.dataset.act === "silent") {
    const run = runOf(state.selectedId);
    if (!run || run.mode !== "runtime") {
      toast("PROFILE_FORBIDS_SIDE_EFFECT · 先进入运行环位，且须审批。");
    } else {
      run.denial = "TRACK_ESCALATION_REQUIRED · 禁止静默对外承诺。";
      toast("已拦截。live 未改。");
      render(false);
    }
  }
});

$("pack").addEventListener("change", (e) => {
  state.pack = e.target.value;
  state.selectedId = pack().items.find((i) => i.hot)?.id || pack().items[0].id;
  state.view = "loop";
  state.stageFilter = "";
  state.healthFilter = "";
  state.q = "";
  state.execFocus = "project";
  render(true);
  syncHash(true);
});

$("dock").addEventListener("submit", (e) => {
  e.preventDefault();
  writeNote($("composer-input").value, false);
});

window.addEventListener("hashchange", () => {
  if (state.hashLock) return;
  if (readHash()) render(true);
});

window.addEventListener("popstate", () => {
  if (readHash()) render(true);
});

if (!readHash()) syncHash(false);
render(false);
