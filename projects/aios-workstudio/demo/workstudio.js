window.LTC_WB = (function () {
  const DATA = {
    meta: {
      data_period: "近30天",
      view_cm: "cowen.hua",
      generated_at: "2026-08-21T09:30:00",
      caliber: {
        spend: "Σspend(bus_mtc,近30天)",
        margin: "Σmargin(bus_mtc,近30天)",
        som: "钛动行业消耗/行业市场总消耗(teyan-dashboard)",
        adoption: "已覆盖服务项数/行业peer_P50(service_coverage_opportunity)",
      },
    },
    global_kpi: {
      spend: { value: 4290000, unit: "USD", mom: 0.124 },
      margin: { value: 612000, unit: "USD", mom: 0.071 },
      som: { value: 0.186, mom_pp: 1.2 },
      adoption: { value: 2.03, peer_p50: 2.5, status: "low" },
      conv_rate_30d: { value: 0.38, delta_pp: 4.2 },
      avg_cycle_days: { value: 23, delta: -2 },
      gate_count: 8,
    },
    funnel: [
      { stage: "01_线索", count: 0, gate: false },
      { stage: "02_建联", count: 0, gate: false },
      { stage: "03_拜访", count: 2, gate: true },
      { stage: "04_纪要", count: 0, gate: false },
      { stage: "05_合同", count: 1, gate: true },
      { stage: "06_授信", count: 0, gate: false },
      { stage: "07_下户", count: 1, gate: false },
      { stage: "08_开跑", count: 0, gate: false },
      { stage: "09_涨量", count: 0, gate: false },
      { stage: "10_服务", count: 1, gate: true },
    ],
    customers: [
      {
        customer_uec: "UEC-10293",
        customer_name: "客户A · Shopline",
        current_stage: "03_拜访",
        days_in_stage: 28,
        owner_cm: "cowen.hua",
        owner_bd: "张三",
        health: "gate",
        signal_summary: "阶段停留28天超阈值14天，流失风险↑；仅BD到场·决策链未覆盖；37天未拜访",
        stages: {
          "03_拜访": {
            data: {
              visit_count: 3,
              last_visit_days: 37,
              attendee_level: "BD_only",
              avg_duration_min: 45,
              trend: [
                { month: "2026-03", value: 1 },
                { month: "2026-04", value: 1 },
                { month: "2026-05", value: 0 },
                { month: "2026-06", value: 0 },
                { month: "2026-07", value: 1 },
              ],
            },
            verdict: {
              level: "gate",
              health: "gate",
              title: "决策信号 · 卡口",
              desc: "阶段停留28天超阈值14天，流失风险↑；仅BD到场·决策链未覆盖；37天未拜访",
              signals: [
                { id: "days_in_stage", level: "gate", msg: "阶段停留28天超阈值14天，流失风险↑" },
                { id: "bd_only", level: "gate", msg: "仅BD到场·决策链未覆盖" },
                { id: "no_visit_30d", level: "gate", msg: "37天未拜访" },
              ],
            },
            actions: [
              { p: "P0", text: "本周安排 CM + 客户 C-level 拜访，补齐决策链覆盖", owner: "cowen.hua", collab: "BD·张三", exec: "explore" },
              { p: "P1", text: "补全 KDM 关系图，识别关键决策人与阻力点", owner: "BD·张三", exec: "explore" },
              { p: "P2", text: "同步上次拜访纪要，确认未闭环需求项", owner: "cowen.hua", exec: "runtime" },
            ],
            plan: [
              { task: "约 C-level 拜访会议", owner: "cowen.hua", due: "08-23", p: "P0", status: "overdue" },
              { task: "KDM 关系图梳理", owner: "BD·张三", due: "08-25", p: "P1", status: "doing" },
              { task: "纪要需求闭环确认", owner: "cowen.hua", due: "08-20", p: "P2", status: "done" },
            ],
          },
        },
        stage_history: [
          { stage: "01_线索", entered: "06-10", left: "06-12", days: 2 },
          { stage: "02_建联", entered: "06-12", left: "06-15", days: 3 },
          { stage: "03_拜访", entered: "07-15", left: null, days: 28 },
        ],
      },
      {
        customer_uec: "UEC-20114",
        customer_name: "Kwai · PH",
        current_stage: "03_拜访",
        days_in_stage: 10,
        owner_cm: "cowen.hua",
        owner_bd: "王五",
        health: "ok",
        signal_summary: "正常推进",
        stages: {
          "03_拜访": {
            data: {
              visit_count: 1,
              last_visit_days: 10,
              attendee_level: "CM",
              avg_duration_min: 30,
              trend: [{ month: "2026-07", value: 1 }],
            },
            verdict: {
              level: "ok",
              health: "ok",
              title: "决策信号 · 正常",
              desc: "无异常信号，阶段推进正常。",
              signals: [],
            },
            actions: [{ p: "P1", text: "安排二访并定级", owner: "BD·王五", exec: "explore" }],
            plan: [{ task: "二访日程", owner: "BD·王五", due: "08-24", p: "P1", status: "todo" }],
          },
        },
        stage_history: [{ stage: "03_拜访", entered: "08-11", left: null, days: 10 }],
      },
      {
        customer_uec: "UEC-30021",
        customer_name: "Lazada · TH",
        current_stage: "05_合同",
        days_in_stage: 9,
        owner_cm: "cowen.hua",
        owner_bd: "张三",
        health: "gate",
        signal_summary: "合同周转9天超阈值7天；合同卡审批中",
        stages: {
          "05_合同": {
            data: { approval_status: "pending", contract_amount: 420000 },
            verdict: {
              level: "gate",
              health: "gate",
              title: "决策信号 · 卡口",
              desc: "合同周转9天超阈值7天；合同卡审批中",
              signals: [
                { id: "days_in_stage", level: "gate", msg: "合同周转9天超阈值7天" },
                { id: "approval_stuck", level: "gate", msg: "合同卡审批中" },
              ],
            },
            actions: [{ p: "P0", text: "催法务加急审批", owner: "cowen.hua", collab: "法务", exec: "runtime" }],
            plan: [{ task: "法务审批跟进", owner: "cowen.hua", due: "08-22", p: "P0", status: "overdue" }],
          },
        },
        stage_history: [{ stage: "05_合同", entered: "08-12", left: null, days: 9 }],
      },
      {
        customer_uec: "UEC-40088",
        customer_name: "Shopee · SG",
        current_stage: "07_下户",
        days_in_stage: 2,
        owner_cm: "cowen.hua",
        owner_bd: "张三",
        health: "ok",
        signal_summary: "正常推进",
        stages: {
          "07_下户": {
            data: { qual_ready: true, setup_progress: 0.8 },
            verdict: {
              level: "ok",
              health: "ok",
              title: "决策信号 · 正常",
              desc: "无异常信号，阶段推进正常。",
              signals: [],
            },
            actions: [{ p: "P2", text: "确认账户搭建收尾", owner: "AO·赵六", exec: "runtime" }],
            plan: [{ task: "搭建验收", owner: "AO·赵六", due: "08-25", p: "P2", status: "doing" }],
          },
        },
        stage_history: [{ stage: "07_下户", entered: "08-19", left: null, days: 2 }],
      },
      {
        customer_uec: "UEC-50102",
        customer_name: "Sea Limited",
        current_stage: "10_服务",
        days_in_stage: 0,
        owner_cm: "cowen.hua",
        owner_bd: "张三",
        health: "gate",
        signal_summary: "流失风险；健康度下降；5个工单积压",
        stages: {
          "10_服务": {
            data: { churn_risk: true, health_trend: -1, open_tickets: 5 },
            verdict: {
              level: "gate",
              health: "gate",
              title: "决策信号 · 卡口",
              desc: "流失风险；健康度下降；5个工单积压",
              signals: [
                { id: "churn_risk", level: "gate", msg: "流失风险" },
                { id: "health_down", level: "warn", msg: "健康度下降" },
                { id: "ticket_backlog", level: "warn", msg: "5个工单积压" },
              ],
            },
            actions: [{ p: "P0", text: "启动续费挽回，CM 本周上门", owner: "cowen.hua", exec: "explore" }],
            plan: [{ task: "挽回方案", owner: "cowen.hua", due: "08-23", p: "P0", status: "todo" }],
          },
        },
        stage_history: [{ stage: "10_服务", entered: "2025-09-01", left: null, days: 0 }],
      },
    ],
  };

  const STAGES = ["01_线索", "02_建联", "03_拜访", "04_纪要", "05_合同", "06_授信", "07_下户", "08_开跑", "09_涨量", "10_服务"];

  function fmtMoney(v, unit) {
    return (unit === "USD" ? "$" : "") + Math.round(v).toLocaleString();
  }
  function fmtPct(v) {
    return (v * 100).toFixed(1) + "%";
  }
  function fmtDelta(v, pp) {
    return pp ? "↑" + v.toFixed(1) + "pp" : v >= 0 ? "↑" + (v * 100).toFixed(1) + "%" : "↓" + Math.abs(v * 100).toFixed(1) + "%";
  }
  function tagLabel(h) {
    return h === "gate" ? "卡口" : h === "warn" ? "预警" : "正常";
  }
  function statusLabel(s) {
    return { todo: "待执行", doing: "进行中", done: "已完成", overdue: "逾期" }[s] || s;
  }
  function fieldLabel(k) {
    return (
      {
        visit_count: "拜访次数",
        last_visit: "最近拜访",
        last_visit_days: "最近拜访(天前)",
        attendee_level: "到场级别",
        avg_duration_min: "平均时长",
        connect_rate: "建联率",
        minutes_done: "纪要完成",
        unconfirmed_req_count: "未确认需求",
        approval_status: "审批状态",
        contract_amount: "合同金额",
        credit_usage_rate: "授信使用率",
        qual_ready: "资质齐备",
        setup_progress: "搭建进度",
        launch_spend: "首跑Spend",
        roi: "ROI",
        churn_risk: "流失风险",
        health_trend: "健康趋势",
        open_tickets: "工单",
        lead_pool_count: "线索池",
        high_score_stale_days: "高分滞留(天)",
      }[k] || k
    );
  }
  function fmtFieldVal(k, v) {
    if (typeof v === "boolean") return v ? "是" : "否";
    if (k === "avg_duration_min") return v + "min";
    if (k === "contract_amount" || k === "launch_spend") return "$" + Number(v).toLocaleString();
    if (k === "connect_rate" || k === "credit_usage_rate" || k === "roi") return (v * 100).toFixed(1) + "%";
    if (k === "setup_progress") return v * 100 + "%";
    return String(v);
  }
  function sparkSVG(vals, h) {
    const w = 300;
    const mn = Math.min(...vals);
    const mx = Math.max(...vals);
    const r = mx - mn || 1;
    const pts = vals.map((v, i) => `${(i / (vals.length - 1)) * w},${h - ((v - mn) / r) * (h - 4) - 2}`);
    return `<svg class="spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none"><defs><linearGradient id="ltc-sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3"/><stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/></linearGradient></defs><path d="M${pts.join(" L")}" fill="none" stroke="#3b82f6" stroke-width="2"/><path d="M${pts.join(" L")} L${w},${h} L0,${h}Z" fill="url(#ltc-sg)"/></svg>`;
  }

  function filteredCustomers(f) {
    return DATA.customers.filter((c) => {
      if (f.cm && f.cm !== "all" && c.owner_cm !== f.cm) return false;
      if (f.stage && c.current_stage !== f.stage) return false;
      if (f.status && c.health !== f.status) return false;
      if (f.q) {
        const n = (c.customer_name + c.customer_uec).toLowerCase();
        if (!n.includes(f.q.toLowerCase())) return false;
      }
      return true;
    });
  }

  function buildTaskQueue(fc) {
    const q = { P0: [], P1: [], P2: [] };
    fc.forEach((c) => {
      const sb = c.stages[c.current_stage];
      if (!sb || !sb.actions) return;
      sb.actions.forEach((a) => {
        if (q[a.p]) q[a.p].push({ ...a, cust: c.customer_name, uec: c.customer_uec, health: c.health });
      });
    });
    return q;
  }

  function taskQueueHTML(fc) {
    const q = buildTaskQueue(fc);
    const cols = [
      ["P0", "重要紧急"],
      ["P1", "重要不紧急"],
      ["P2", "紧急不重要"],
    ];
    const total = q.P0.length + q.P1.length + q.P2.length;
    const colHTML = ([p, label]) => {
      const items = q[p];
      const list = items
        .map(
          (it) =>
            `<button type="button" class="pq-item ${p}" data-ltc-cust="${it.uec}" title="跳转到 ${it.cust}"><div class="pq-itxt">${it.text}</div><div class="pq-imeta"><span class="pq-icust ${it.health === "gate" ? "g" : ""}">${it.cust}</span><span class="pq-iowner">${it.owner}${it.collab ? "·" + it.collab : ""}</span></div></button>`
        )
        .join("");
      return `<div class="pq-col"><div class="pq-colhead"><span class="pq-badge ${p}">${p}</span><span class="pq-clabel">${label}</span><span class="pq-ccnt">${items.length}</span></div><div class="pq-list">${list || '<div class="pq-empty">无任务</div>'}</div></div>`;
    };
    return `<div class="ktile tasks"><div class="kt-tasks-head">行动队列 <b>P0·P1·P2</b><span class="section-note" style="margin-left:auto">${total} 项 · 按筛选客户当前阶段聚合 · 点击跳转客户</span></div><div class="pq-cols">${cols.map(colHTML).join("")}</div></div>`;
  }

  function render(ctx) {
    const f = { cm: ctx.cm, q: ctx.q, status: ctx.status, stage: ctx.stage };
    const fc = filteredCustomers(f);
    const g = DATA.global_kpi;
    const adopLow = g.adoption.value < g.adoption.peer_p50;
    const counts = {};
    DATA.funnel.forEach((x) => {
      counts[x.stage] = 0;
    });
    fc.forEach((c) => {
      counts[c.current_stage] = (counts[c.current_stage] || 0) + 1;
    });
    let sel = ctx.selected;
    if (!sel || !fc.find((c) => c.customer_uec === sel)) sel = fc[0] ? fc[0].customer_uec : null;
    const c = DATA.customers.find((x) => x.customer_uec === sel);
    const viewStage = ctx.viewStage || (c && c.current_stage);
    const sb = c && c.stages[viewStage];

    const funnel = DATA.funnel
      .map((x) => {
        const selCls = ctx.stage === x.stage ? "sel" : "";
        return `<button type="button" class="fp ${x.gate ? "gate" : ""} ${selCls}" data-ltc-stage="${x.stage}"><div class="fp-num">${x.stage.slice(0, 2)}</div><div class="fp-name">${x.stage.slice(3)}</div><div class="fp-cnt">${counts[x.stage] || 0}</div></button>`;
      })
      .join("");

    const list = fc
      .map((row) => {
        const days = row.days_in_stage ? `停留 ${row.days_in_stage}天` : "稳态";
        return `<button type="button" class="crow ${row.health} ${row.customer_uec === sel ? "sel" : ""}" data-ltc-cust="${row.customer_uec}"><div class="cr-top"><span class="cr-name">${row.customer_name}</span><span class="cr-tag ${row.health}">${tagLabel(row.health)}</span></div><div class="cr-mid"><span class="cr-stage">${row.current_stage}</span><span>${row.owner_cm ? "CM·" + row.owner_cm : ""}</span></div><div class="cr-bot"><span class="cr-days ${row.health === "gate" ? "gate" : ""}">${days}</span><span class="cr-sig">${row.signal_summary}</span></div></button>`;
      })
      .join("");

    let detail = `<div class="ltc-empty">选择左侧客户查看详情</div>`;
    if (c && !sb) {
      detail = `<div class="ltc-empty">该客户在 ${viewStage} 无快照数据</div>`;
    } else if (c && sb) {
      const v = sb.verdict;
      const d = sb.data;
      const tabs = STAGES.map(
        (s) => `<button type="button" class="stab ${s === viewStage ? "active" : ""}" data-ltc-tab="${s}">${s.slice(3)}</button>`
      ).join("");
      const dtiles = Object.entries(d)
        .filter(([k]) => k !== "trend")
        .map(([k, val]) => `<div class="dtile"><div class="dtile-l">${fieldLabel(k)}</div><div class="dtile-v">${fmtFieldVal(k, val)}</div></div>`)
        .join("");
      const trend = d.trend || [];
      const spark = trend.length >= 2 ? sparkSVG(trend.map((t) => t.value), 30) : "";
      const acts = sb.actions
        .map(
          (a, i) =>
            `<div class="act ${a.p}"><span class="act-tag ${a.p}">${a.p}</span><div><div class="act-txt">${a.text}</div><div class="act-owner">负责人：${a.owner}${a.collab ? " · 协作：" + a.collab : ""}</div><div class="act-go"><button type="button" class="${i === 0 ? "btn-enter" : "btn-enter ghost"}" data-enter="${a.exec || "explore"}" data-enter-item="${c.customer_uec}">进入执行态</button></div></div></div>`
        )
        .join("");
      const rows = sb.plan
        .map(
          (p) =>
            `<tr><td>${p.task}</td><td>${p.owner}</td><td class="mono">${p.due}</td><td><span class="pbadge p">${p.p}</span></td><td><span class="pbadge ${p.status}">${statusLabel(p.status)}</span></td></tr>`
        )
        .join("");
      detail = `<div class="detail"><div class="detail-head"><div class="detail-title">${c.customer_name}</div><div class="detail-sub">CM: ${c.owner_cm} · BD: ${c.owner_bd} · ${viewStage} ${viewStage === c.current_stage ? "· 进入 " + c.days_in_stage + " 天" : ""} · 编码 ${c.customer_uec}</div><div class="stage-tabs">${tabs}</div></div><div class="detail-body">
        <div class="verdict ${v.level === "ok" ? "" : v.level}"><div class="verdict-title">${v.title}</div><div class="verdict-desc">${v.desc}</div></div>
        <div class="dblock"><div class="db-h">数据看板</div><div class="dgrid">${dtiles}</div>${spark ? `<div style="margin-top:8px"><div class="trend-l">趋势</div>${spark}</div>` : ""}</div>
        <div class="dblock"><div class="db-h">行动策略</div>${acts || '<div class="ltc-empty">无行动项</div>'}</div>
        <div class="dblock"><div class="db-h">计划跟踪</div><table class="ptable"><thead><tr><th>任务</th><th>负责人</th><th>截止</th><th>优先级</th><th>状态</th></tr></thead><tbody>${rows || '<tr><td colspan="5">无任务</td></tr>'}</tbody></table></div>
      </div></div>`;
    }

    return `<div class="ltc">
      <div class="section-header"><span class="section-title">全局经营</span><span class="section-badge">客户经理视角</span><span class="section-note">数据周期：${DATA.meta.data_period} · 视角：${DATA.meta.view_cm} · 2026-08-21 09:30</span></div>
      <div class="kpi-strip">
        <div class="ktile kt1 composite">
          <div class="kt-comp-head">经营概览 <b>Spend / Margin / SOM / Adoption</b><span class="section-note" style="margin-left:auto">近30天</span></div>
          <div class="km-grid">
            <div class="km"><div class="km-l">Spend <span class="km-tip">消耗</span></div><div class="km-v">${fmtMoney(g.spend.value, g.spend.unit)}</div><div class="km-sub ${g.spend.mom >= 0 ? "up" : "down"}">${fmtDelta(g.spend.mom)}</div></div>
            <div class="km"><div class="km-l">Margin <span class="km-tip">利润</span></div><div class="km-v">${fmtMoney(g.margin.value, g.margin.unit)}</div><div class="km-sub ${g.margin.mom >= 0 ? "up" : "down"}">${fmtDelta(g.margin.mom)}</div></div>
            <div class="km"><div class="km-l">SOM <span class="km-tip">市场份额</span></div><div class="km-v">${fmtPct(g.som.value)}</div><div class="km-sub ${g.som.mom_pp >= 0 ? "up" : "down"}">${g.som.mom_pp >= 0 ? "↑" : "↓"}${Math.abs(g.som.mom_pp).toFixed(1)}pp</div></div>
            <div class="km"><div class="km-l">Adoption <span class="km-tip">服务项采纳</span></div><div class="km-v">${g.adoption.value}</div><div class="km-sub ${adopLow ? "down" : "up"}">${adopLow ? "低于P50" : "高于P50"}</div></div>
          </div>
        </div>
        ${taskQueueHTML(fc)}
      </div>
      <div class="filter-panel">
        <div class="fg"><div class="fl">客户经理</div><select class="fc" id="f-cm"><option value="cowen.hua" ${ctx.cm === "cowen.hua" ? "selected" : ""}>cowen.hua (我)</option><option value="all" ${ctx.cm === "all" ? "selected" : ""}>全部</option></select></div>
        <div class="fg"><div class="fl">客户</div><input class="fc" id="f-q" value="${ctx.q || ""}" placeholder="搜索客户名/编码"></div>
        <div class="fg"><div class="fl">状态</div><select class="fc" id="f-health"><option value="">全部</option><option value="gate" ${ctx.status === "gate" ? "selected" : ""}>仅卡口</option><option value="warn" ${ctx.status === "warn" ? "selected" : ""}>仅预警</option></select></div>
        <button type="button" class="btn btn-primary" data-ltc-query>查询</button>
        <button type="button" class="btn btn-outline" data-ltc-reset>重置</button>
        <button type="button" class="btn btn-outline" data-ltc-export>导出报告</button>
        <div class="legend"><span><span class="ldot" style="background:#10b981"></span>正常</span><span><span class="ldot" style="background:#f59e0b"></span>预警</span><span><span class="ldot" style="background:#ef4444"></span>卡口</span></div>
      </div>
      <div class="section-header"><span class="section-title">LTC 管线</span><span class="section-badge">10 阶段漏斗</span><span class="section-note">点击阶段 pill → 按阶段筛选客户列表</span></div>
      <div class="funnel">${funnel}</div>
      <div class="workbench">
        <div class="clist">
          <div class="clist-head"><span class="clist-title">客户列表</span><span class="clist-cnt">${fc.length} 条 · ${ctx.stage ? ctx.stage + " 阶段" : "全部"}</span></div>
          <div class="clist-body">${list || '<div class="ltc-empty">无匹配客户</div>'}</div>
        </div>
        <div id="detailSlot">${detail}</div>
      </div>
    </div>`;
  }

  function exportCSV(f) {
    const fc = filteredCustomers(f);
    const headers = ["customer_uec", "customer_name", "current_stage", "days_in_stage", "owner_cm", "owner_bd", "health", "signal_summary"];
    const rows = fc.map((c) => headers.map((h) => `"${c[h] ?? ""}"`).join(","));
    const csv = "\uFEFF" + [headers.join(","), ...rows].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "CM_LTC_工作台.csv";
    a.click();
  }

  return { DATA, STAGES, render, filteredCustomers, exportCSV };
})();


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
    deep: true,
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
      {
        id: "wi-init",
        code: "PJ-010",
        title: "M3 立项预审",
        type: "立项",
        col: "todo",
        owner: "周衡",
        stage: "立项",
        due: "下窗口",
        exec: "explore",
        gate: "G0",
        ought: "立项先写清五维与验收法则。",
        is: "只有口头范围，尚未建模。",
        gap: "未建模不得排进本窗口执行。",
        wm: {
          space: "衡川组合委员会",
          time: "下窗口预审",
          subjects: "周衡；业务发起人",
          objects: "立项书、验收法则",
          feedback: "预审通过才进计划",
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
    deep: true,
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
        stage: "复核",
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
      {
        id: "wi-pool",
        code: "INV-024",
        title: "动量标的入池",
        type: "标的",
        col: "doing",
        owner: "沈澈",
        stage: "池",
        due: "本周",
        exec: "explore",
        gate: "G1",
        ought: "入池须有可回收的有效性口径。",
        is: "已进观察池，交叉核验未完成。",
        gap: "未核验不得升到下单。",
        wm: {
          space: "衡川投研台 · 观察池",
          time: "本周研究窗",
          subjects: "沈澈",
          objects: "观察池标的",
          feedback: "核验通过才出池",
        },
      },
      {
        id: "wi-hold",
        code: "INV-025",
        title: "现有仓位盯盘",
        type: "持仓",
        col: "doing",
        owner: "风控",
        stage: "持仓",
        due: "本窗口",
        exec: "runtime",
        gate: "G4",
        ought: "回撤窗口内不得加仓。",
        is: "敞口 1.2x，已触上限。",
        gap: "复核未过前只许盯盘，不许新开。",
        wm: {
          space: "衡川投研台 · 组合",
          time: "回撤窗口",
          subjects: "风控；沈澈",
          objects: "现有仓位",
          feedback: "敞口与回撤",
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
  cm: null,
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
    spec: {
      badge: "用人经理视角",
      stream: "人才流 5 阶段漏斗",
      ownerLabel: "负责人",
      owners: [
        { value: "all", label: "全部" },
        { value: "林启明", label: "林启明 (我)" },
        { value: "招聘委员会", label: "招聘委员会" },
      ],
      overview: [
        { n: "编制填满", tip: "Fill", v: "72%", sub: "价值流停在短名单", dir: "down" },
        { n: "证据接地", tip: "Ground", v: "61%", sub: "↓4.0pp", dir: "down" },
        { n: "周期", tip: "Cycle", v: "38d", sub: "短名单滞留", dir: "down" },
        { n: "卡口", tip: "Gate", v: "2", sub: "未接地 + 冻结", dir: "down" },
      ],
    },
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
    spec: {
      badge: "PMO 视角",
      stream: "立项到验收 5 阶段漏斗",
      ownerLabel: "负责人",
      owners: [
        { value: "all", label: "全部" },
        { value: "周衡", label: "周衡 (我)" },
        { value: "组合委员会", label: "组合委员会" },
      ],
      overview: [
        { n: "按期", tip: "On-time", v: "64%", sub: "M2 被挡住", dir: "down" },
        { n: "开着的依赖", tip: "Deps", v: "7", sub: "Assignee 为空", dir: "down" },
        { n: "风险开", tip: "Risk", v: "3", sub: "范围未冻", dir: "down" },
        { n: "卡口", tip: "Gate", v: "2", sub: "无 Owner + 未冻", dir: "down" },
      ],
    },
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
      { id: "立项", count: 1, gate: false },
      { id: "计划", count: 1, gate: false },
      { id: "执行", count: 2, gate: true },
      { id: "验收", count: 1, gate: false },
      { id: "收尾", count: 0, gate: false },
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
      "wi-init": {
        health: "ok",
        days: 1,
        signal: "下窗口预审，尚未建模，不进本窗口执行",
        metrics: [
          { n: "五维", v: "草稿" },
          { n: "验收法则", v: "未" },
          { n: "排期", v: "下窗" },
          { n: "停留", v: "1d" },
        ],
        trend: [0, 0, 0, 0, 1],
        verdict: {
          level: "ok",
          title: "决策信号 · 正常",
          desc: "立项预审可做研究。未建模不得挤进 M2 执行。",
          signals: [],
        },
        actions: [{ p: "P2", text: "签发研究：补齐 M3 五维与验收法则", owner: "周衡", exec: "explore", item: "wi-init" }],
        plan: [{ task: "立项五维草稿", owner: "周衡", due: "下窗口", p: "P2", status: "todo", item: "wi-init" }],
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
    spec: {
      badge: "投研视角",
      stream: "研究到复核 5 阶段漏斗",
      ownerLabel: "负责人",
      owners: [
        { value: "all", label: "全部" },
        { value: "沈澈", label: "沈澈 (我)" },
        { value: "风控", label: "风控" },
      ],
      overview: [
        { n: "回撤", tip: "Drawdown", v: "-6.1%", sub: "已触发 G4", dir: "down" },
        { n: "信源等级", tip: "Source", v: "中", sub: "不得单独下单", dir: "down" },
        { n: "因子有效", tip: "Alpha", v: "0.18", sub: "未交叉核验", dir: "down" },
        { n: "卡口", tip: "Gate", v: "2", sub: "回撤 + 下单", dir: "down" },
      ],
    },
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
      { id: "研究", count: 1, gate: false },
      { id: "池", count: 1, gate: false },
      { id: "下单", count: 1, gate: true },
      { id: "持仓", count: 1, gate: true },
      { id: "复核", count: 1, gate: true },
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
      "wi-pool": {
        health: "warn",
        days: 4,
        signal: "已进观察池，交叉核验未完成",
        metrics: [
          { n: "池内", v: "1" },
          { n: "交叉", v: "否" },
          { n: "出池", v: "禁" },
          { n: "停留", v: "4d" },
        ],
        trend: [0, 0, 1, 1, 1],
        verdict: {
          level: "warn",
          title: "决策信号 · 预警",
          desc: "观察池不是下单理由。核验完成前不得升阶段。",
          signals: ["缺第二信源"],
        },
        actions: [{ p: "P1", text: "交叉核验后再决定是否出池", owner: "沈澈", exec: "explore", item: "wi-pool" }],
        plan: [{ task: "出池核验", owner: "沈澈", due: "本周", p: "P1", status: "doing", item: "wi-pool" }],
      },
      "wi-hold": {
        health: "warn",
        days: 2,
        signal: "敞口 1.2x 已触上限，回撤窗口只许盯盘",
        metrics: [
          { n: "敞口", v: "1.2x" },
          { n: "加仓", v: "禁" },
          { n: "门禁", v: "G4" },
          { n: "停留", v: "2d" },
        ],
        trend: [1.0, 1.05, 1.1, 1.18, 1.2],
        verdict: {
          level: "warn",
          title: "决策信号 · 预警",
          desc: "复核未过前不得新开仓。现有仓位只盯盘。",
          signals: ["敞口触上限", "回撤窗口重叠"],
        },
        actions: [{ p: "P1", text: "盯盘并等待回撤复核结论", owner: "风控", exec: "runtime", item: "wi-hold" }],
        plan: [{ task: "敞口盯盘", owner: "风控", due: "本窗口", p: "P1", status: "doing", item: "wi-hold" }],
      },
    },
    assets: [
      { name: "中等级信源不得单独下单", effect: "拦住 1 次下单", pct: 100, status: "生效" },
      { name: "回撤 6% 触发复核", effect: "本窗口已触发", pct: 70, status: "生效" },
    ],
    learn: ["拦住中等级信源下单", "回撤事件记入审计", "法则再次确认", "同类窗口默认先研究", "策略回收待确认"],
  },
  cm: {
    period: "近30天",
    caliber: "Spend=Σspend(bus_mtc) · SOM=钛动行业消耗/市场总消耗 · Adoption=覆盖服务项/peer_P50",
    composite: [],
    kpis: [],
    funnel: [],
    objects: {},
    assets: [
      { name: "阶段停留超阈值不得推进", effect: "拦住 Shopline 拜访 28 天", pct: 100, status: "生效" },
      { name: "决策链必须覆盖 C-level", effect: "BD_only 视为卡口", pct: 100, status: "生效" },
      { name: "合同周转超 7 天升级法务", effect: "Lazada 审批中", pct: 80, status: "生效" },
      { name: "服务健康下降启动挽回", effect: "Sea Limited 工单积压", pct: 60, status: "待用" },
    ],
    learn: ["拜访超 14 天默认卡口", "决策链未覆盖不得进纪要", "合同超 7 天催法务", "服务流失先挽回再涨量", "ChangeSet 待人确认后回写口径"],
  },
};

(function hydrateCm() {
  if (!window.LTC_WB) return;
  const wb = window.LTC_WB;
  const customers = wb.DATA.customers;
  const execOf = {
    "UEC-10293": "explore",
    "UEC-20114": "explore",
    "UEC-30021": "runtime",
    "UEC-40088": "runtime",
    "UEC-50102": "explore",
  };
  const gateOf = {
    "UEC-10293": "G1",
    "UEC-20114": "G0",
    "UEC-30021": "G3",
    "UEC-40088": "G0",
    "UEC-50102": "G2",
  };
  PACKS.cm = {
    id: "cm",
    space: "衡川 · 客户经营工作台",
    deep: true,
    owner: "cowen.hua",
    role: "客户经理",
    tension: "拜访与合同、服务三处卡口同时开着。决策链未覆盖不得推进，合同超阈值须升级法务。",
    dikw: ["bus_mtc / 拜访 / 合同 / 工单", "卡口 3 · 停留超阈", "停留超阈值不得推进", "先过关再涨量"],
    project: {
      id: "prj-ltc",
      code: "PRJ-LTC",
      title: "线索到现金",
      window: "近30天 · 客户经理 cowen.hua",
      cycle: "interact",
      object: "客户 × 阶段 × 决策信号",
    },
    kpis: [
      { id: "spend", n: "Spend", v: "$4,290,000" },
      { id: "gate", n: "卡口", v: "3", hot: true, item: "UEC-10293" },
      { id: "cycle", n: "周期", v: "23d" },
    ],
    goals: [],
    items: customers.map((c) => {
      const sb = c.stages[c.current_stage];
      return {
        id: c.customer_uec,
        code: c.customer_uec,
        title: c.customer_name,
        type: "客户",
        col: c.health === "gate" ? "blocked" : c.health === "warn" ? "doing" : "doing",
        owner: c.owner_cm,
        stage: c.current_stage,
        due: c.days_in_stage ? "停留 " + c.days_in_stage + "d" : "稳态",
        exec: execOf[c.customer_uec] || "explore",
        gate: gateOf[c.customer_uec] || "G1",
        hot: c.health === "gate",
        ought: "按 LTC 阶段阈值与决策链法则推进，卡口不得跳阶段。",
        is: c.signal_summary,
        gap: sb && sb.verdict ? sb.verdict.desc : c.signal_summary,
        wm: {
          space: "衡川客户经营台 · " + c.current_stage,
          time: c.days_in_stage ? "本阶段 " + c.days_in_stage + " 天" : "稳态服务",
          subjects: "CM " + c.owner_cm + "；BD " + c.owner_bd + "；客户 " + c.customer_name,
          objects: c.current_stage + "、决策信号、行动队列",
          feedback: c.health === "gate" ? "卡口未解不得进入下一阶段" : "阶段推进与计划跟踪",
        },
      };
    }),
    risks: customers
      .filter((c) => c.health === "gate")
      .map((c) => ({ id: c.customer_uec, level: "red", title: c.customer_name, detail: c.signal_summary })),
    todos: customers.flatMap((c) =>
      ((c.stages[c.current_stage] || {}).plan || []).map((p) => ({
        id: c.customer_uec,
        pdca: p.p === "P0" ? "P" : p.p === "P1" ? "D" : "C",
        item: p.task,
        owner: p.owner,
        gate: gateOf[c.customer_uec] || "G1",
        exec: execOf[c.customer_uec] || "explore",
      }))
    ),
    evidence: [
      { source: "bus_mtc 近30天", reliability: "高", excerpt: "Spend $4.29M · Margin $612k · SOM 18.6%" },
      { source: "拜访记录 客户A", reliability: "高", excerpt: "37天未拜访，到场仅 BD。" },
      { source: "合同审批 Lazada", reliability: "高", excerpt: "周转 9 天，状态 pending。" },
    ],
    uncertainties: [
      { claim: "Shopline 决策链可补齐", why: "C-level 尚未到场", ask: "本周 CM + C-level 拜访" },
      { claim: "Sea Limited 可挽回", why: "健康度下降且工单积压", ask: "上门挽回方案" },
    ],
    options: [
      { id: "A", summary: "先解拜访与合同卡口，服务走挽回", risk: "涨量延后" },
      { id: "B", summary: "同时铺开跑涨量", risk: "卡口客户流失" },
    ],
    knowledge: [
      { id: "ltc_stage_thresholds.md", type: "法则", installed: true },
      { id: "kdm-coverage", type: "Skill", installed: false },
    ],
    builder: {
      app: "LTC 卡口编译器 0.1.0",
      released: false,
      invariants: [
        { id: "wm_five_dims", ok: true, detail: "五维齐全" },
        { id: "stage_threshold", ok: true, detail: "超阈不得跳阶段" },
        { id: "kdm_required", ok: true, detail: "BD_only 不得进纪要" },
      ],
      cs: [
        { op: "cs.customer.query", level: "L1", side: "读" },
        { op: "cs.contract.approve", level: "L2", side: "写，仅运行" },
      ],
    },
    runtime: {
      instance: "ins-hengchuan-ltc",
      scope: "dept",
      items: customers.map((c) => ({
        name: c.customer_name,
        advice: c.health !== "gate",
        why: c.signal_summary,
      })),
      silent: "静默改合同或对客承诺",
      action: "推进当前阶段动作（须审批）",
    },
  };
  SCENE.cm.funnel = wb.DATA.funnel.map((x) => ({ id: x.stage, count: x.count, gate: x.gate }));
  customers.forEach((c) => {
    const sb = c.stages[c.current_stage] || {};
    SCENE.cm.objects[c.customer_uec] = {
      health: c.health,
      days: c.days_in_stage,
      signal: c.signal_summary,
      metrics: Object.entries(sb.data || {})
        .filter(([k]) => k !== "trend")
        .slice(0, 4)
        .map(([k, v]) => ({ n: k, v: String(v) })),
      trend: ((sb.data && sb.data.trend) || []).map((t) => t.value),
      verdict: sb.verdict || { level: c.health, title: "决策信号", desc: c.signal_summary, signals: [] },
      actions: (sb.actions || []).map((a) => ({ ...a, item: c.customer_uec })),
      plan: (sb.plan || []).map((p) => ({ ...p, item: c.customer_uec })),
      stages: c.stages,
    };
  });
})();

(function hydrateSceneSnapshots() {
  ["ops", "pmo", "invest"].forEach((pid) => {
    const p = PACKS[pid];
    const sc = SCENE[pid];
    if (!p || !sc) return;
    p.items.forEach((it) => {
      const o = sc.objects[it.id];
      if (!o || o.stages) return;
      const data = {};
      (o.metrics || []).forEach((m) => {
        data[m.n] = m.v;
      });
      if (o.trend && o.trend.length) {
        data.trend = o.trend.map((v, i) => ({ month: String(i + 1), value: v }));
      }
      o.stages = {
        [it.stage]: {
          data,
          verdict: o.verdict,
          actions: o.actions,
          plan: o.plan,
        },
      };
    });
  });
})();

const state = {
  layer: "scene",
  pack: "ops",
  view: "loop",
  selectedId: "wi-rao",
  execFocus: "project",
  stageFilter: "",
  healthFilter: "",
  q: "",
  cmOwner: "all",
  ltcViewStage: null,
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
  const own = state.cmOwner;
  return pack()
    .items.map((it) => objOf(it.id))
    .filter((o) => !own || own === "all" || o.owner === own)
    .filter((o) => !state.stageFilter || o.stage === state.stageFilter)
    .filter((o) => !state.healthFilter || o.health === state.healthFilter)
    .filter((o) => !q || `${o.title}${o.code}${o.signal}${o.id}`.toLowerCase().includes(q));
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

function tagLabel(h) {
  return h === "gate" ? "卡口" : h === "warn" ? "预警" : "正常";
}

function planPlain(s) {
  return { todo: "待执行", doing: "进行中", done: "已完成", overdue: "逾期" }[s] || s;
}

function exportSceneCSV() {
  const rows = filteredObjects();
  const headers = ["id", "code", "title", "stage", "owner", "health", "days", "signal"];
  const body = rows.map((o) => headers.map((h) => `"${String(o[h] ?? "").replace(/"/g, '""')}"`).join(","));
  const csv = "\uFEFF" + [headers.join(","), ...body].join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" }));
  a.download = pack().id.toUpperCase() + "_工作台.csv";
  a.click();
}

function queueOf(list) {
  const q = { P0: [], P1: [], P2: [] };
  list.forEach((o) => {
    (o.actions || []).forEach((a) => {
      if (q[a.p]) q[a.p].push({ ...a, title: o.title, id: a.item || o.id, health: o.health });
    });
  });
  return q;
}

function renderLoopMain() {
  const p = pack();
  const sc = scene();
  const spec = sc.spec || { badge: p.role, stream: "价值流漏斗", ownerLabel: "负责人", owners: [{ value: "all", label: "全部" }], overview: sc.composite };
  const list = filteredObjects();
  const current = list.find((o) => o.id === state.selectedId) || list[0] || objOf(state.selectedId);
  const viewStage = state.ltcViewStage || (current && current.stage);
  const snap = current && current.stages ? current.stages[viewStage] : null;
  const counts = {};
  sc.funnel.forEach((f) => {
    counts[f.id] = 0;
  });
  list.forEach((o) => {
    counts[o.stage] = (counts[o.stage] || 0) + 1;
  });
  const q = queueOf(list);
  const total = q.P0.length + q.P1.length + q.P2.length;
  const ov = spec.overview;
  const km = ov
    .map(
      (k) =>
        `<div class="km"><div class="km-l">${esc(k.n)} <span class="km-tip">${esc(k.tip || "")}</span></div><div class="km-v">${esc(k.v)}</div><div class="km-sub ${k.dir === "up" ? "up" : "down"}">${esc(k.sub || "")}</div></div>`
    )
    .join("");
  const cols = [
    ["P0", "重要紧急"],
    ["P1", "重要不紧急"],
    ["P2", "紧急不重要"],
  ]
    .map(([pri, label]) => {
      const items = q[pri]
        .map(
          (it) =>
            `<button type="button" class="pq-item ${pri}" data-ltc-cust="${it.id}" title="跳转到 ${esc(it.title)}"><div class="pq-itxt">${esc(it.text)}</div><div class="pq-imeta"><span class="pq-icust ${it.health === "gate" ? "g" : ""}">${esc(it.title)}</span><span class="pq-iowner">${esc(it.owner)}</span></div></button>`
        )
        .join("");
      return `<div class="pq-col"><div class="pq-colhead"><span class="pq-badge ${pri}">${pri}</span><span class="pq-clabel">${label}</span><span class="pq-ccnt">${q[pri].length}</span></div><div class="pq-list">${items || '<div class="pq-empty">无任务</div>'}</div></div>`;
    })
    .join("");
  const owners = spec.owners
    .map((o) => `<option value="${esc(o.value)}" ${state.cmOwner === o.value ? "selected" : ""}>${esc(o.label)}</option>`)
    .join("");
  const funnel = sc.funnel
    .map((f, i) => {
      const num = String(i + 1).padStart(2, "0");
      return `<button type="button" class="fp ${f.gate ? "gate" : ""} ${state.stageFilter === f.id ? "sel" : ""}" data-ltc-stage="${f.id}"><div class="fp-num">${num}</div><div class="fp-name">${esc(f.id)}</div><div class="fp-cnt">${counts[f.id] || 0}</div></button>`;
    })
    .join("");
  const rows = list
    .map((o) => {
      const days = o.days ? `停留 ${o.days}天` : "稳态";
      return `<button type="button" class="crow ${o.health} ${o.id === (current && current.id) ? "sel" : ""}" data-ltc-cust="${o.id}"><div class="cr-top"><span class="cr-name">${esc(o.title)}</span><span class="cr-tag ${o.health}">${tagLabel(o.health)}</span></div><div class="cr-mid"><span class="cr-stage">${esc(o.stage)}</span><span>${esc(o.owner)}</span></div><div class="cr-bot"><span class="cr-days ${o.health === "gate" ? "gate" : ""}">${days}</span><span class="cr-sig">${esc(o.signal)}</span></div></button>`;
    })
    .join("");
  let detail = `<div class="ltc-empty">选择左侧对象查看详情</div>`;
  if (current && !snap) {
    detail = `<div class="ltc-empty">该对象在 ${esc(viewStage)} 无快照数据</div>`;
  } else if (current && snap) {
    const v = snap.verdict || current.verdict;
    const data = snap.data || {};
    const tabs = sc.funnel
      .map((f) => `<button type="button" class="stab ${f.id === viewStage ? "active" : ""}" data-ltc-tab="${f.id}">${esc(f.id)}</button>`)
      .join("");
    const tiles = Object.entries(data)
      .filter(([k]) => k !== "trend")
      .map(([k, val]) => `<div class="dtile"><div class="dtile-l">${esc(k)}</div><div class="dtile-v">${esc(val)}</div></div>`)
      .join("");
    const trend = (data.trend || []).map((t) => (typeof t === "number" ? t : t.value));
    const sparkHtml = trend.length >= 2 ? spark(trend) : "";
    const acts = (snap.actions || [])
      .map(
        (a, i) =>
          `<div class="act ${a.p}"><span class="act-tag ${a.p}">${a.p}</span><div><div class="act-txt">${esc(a.text)}</div><div class="act-owner">负责人：${esc(a.owner)}${a.collab ? " · 协作：" + esc(a.collab) : ""} · 建议${MODE_ZH[a.exec] || ""}</div><div class="act-go"><button type="button" class="${i === 0 ? "btn-enter" : "btn-enter ghost"}" data-enter="${a.exec || "explore"}" data-enter-item="${a.item || current.id}">进入执行态</button></div></div></div>`
      )
      .join("");
    const planRows = (snap.plan || [])
      .map(
        (r) =>
          `<tr><td>${esc(r.task)}</td><td>${esc(r.owner)}</td><td class="mono">${esc(r.due)}</td><td><span class="pbadge p">${esc(r.p)}</span></td><td><span class="pbadge ${r.status}">${planPlain(r.status)}</span></td></tr>`
      )
      .join("");
    detail = `<div class="detail"><div class="detail-head"><div class="detail-title">${esc(current.title)}</div><div class="detail-sub">${esc(p.role)}: ${esc(current.owner)} · ${esc(viewStage)} ${viewStage === current.stage ? "· 进入 " + current.days + " 天" : ""} · 编码 ${esc(current.code)}</div><div class="stage-tabs">${tabs}</div></div><div class="detail-body">
      <div class="verdict ${v.level === "ok" ? "" : v.level}"><div class="verdict-title">${esc(v.title)}</div><div class="verdict-desc">${esc(v.desc)}</div></div>
      <div class="split3" style="margin-bottom:14px"><div class="panel"><h3>应当</h3><p>${esc(current.ought)}</p></div><div class="panel"><h3>事实</h3><p>${esc(current.is)}</p></div><div class="panel"><h3>缺口</h3><p>${esc(current.gap)}</p></div></div>
      <div class="dblock"><div class="db-h">数据看板</div><div class="dgrid">${tiles}</div>${sparkHtml ? `<div style="margin-top:8px"><div class="trend-l">趋势</div>${sparkHtml}</div>` : ""}</div>
      <div class="dblock"><div class="db-h">行动策略</div>${acts || '<div class="ltc-empty">无行动项</div>'}</div>
      <div class="dblock"><div class="db-h">计划跟踪</div><table class="ptable"><thead><tr><th>任务</th><th>负责人</th><th>截止</th><th>优先级</th><th>状态</th></tr></thead><tbody>${planRows || '<tr><td colspan="5">无任务</td></tr>'}</tbody></table></div>
    </div></div>`;
  }

  return `<div class="ltc">
    <div class="section-header"><span class="section-title">全局经营</span><span class="section-badge">${esc(spec.badge)}</span><span class="section-note">数据周期：${esc(sc.period)} · ${esc(sc.caliber)}</span></div>
    <div class="kpi-strip">
      <div class="ktile kt1 composite">
        <div class="kt-comp-head">经营概览 <b>${ov.map((k) => k.n).join(" / ")}</b><span class="section-note" style="margin-left:auto">${esc(sc.period)}</span></div>
        <div class="km-grid">${km}</div>
      </div>
      <div class="ktile tasks"><div class="kt-tasks-head">行动队列 <b>P0·P1·P2</b><span class="section-note" style="margin-left:auto">${total} 项 · 按筛选对象当前阶段聚合 · 点击跳转</span></div><div class="pq-cols">${cols}</div></div>
    </div>
    <div class="filter-panel">
      <div class="fg"><div class="fl">${esc(spec.ownerLabel)}</div><select class="fc" id="f-cm">${owners}</select></div>
      <div class="fg"><div class="fl">对象</div><input class="fc" id="f-q" value="${esc(state.q)}" placeholder="搜索名称 / 编码"></div>
      <div class="fg"><div class="fl">状态</div><select class="fc" id="f-health"><option value="">全部</option><option value="gate" ${state.healthFilter === "gate" ? "selected" : ""}>仅卡口</option><option value="warn" ${state.healthFilter === "warn" ? "selected" : ""}>仅预警</option></select></div>
      <button type="button" class="btn btn-primary" data-ltc-query>查询</button>
      <button type="button" class="btn btn-outline" data-ltc-reset>重置</button>
      <button type="button" class="btn btn-outline" data-ltc-export>导出报告</button>
      <div class="legend"><span><span class="ldot" style="background:#10b981"></span>正常</span><span><span class="ldot" style="background:#f59e0b"></span>预警</span><span><span class="ldot" style="background:#ef4444"></span>卡口</span></div>
    </div>
    <div class="section-header"><span class="section-title">价值流</span><span class="section-badge">${esc(spec.stream)}</span><span class="section-note">点击阶段 pill → 按阶段筛选对象列表</span></div>
    <div class="funnel" style="--fp-cols:${sc.funnel.length}">${funnel}</div>
    <div class="workbench">
      <div class="clist">
        <div class="clist-head"><span class="clist-title">对象列表</span><span class="clist-cnt">${list.length} 条 · ${state.stageFilter ? esc(state.stageFilter) + " 阶段" : "全部"}</span></div>
        <div class="clist-body">${rows || '<div class="ltc-empty">无匹配对象</div>'}</div>
      </div>
      <div id="detailSlot">${detail}</div>
    </div>
  </div>`;
}

function renderOptimizeMain() {
  const p = pack();
  const sc = scene();
  const plans = p.items.flatMap((it) => (objOf(it.id).plan || []).map((r) => ({ ...r, id: r.item || it.id, title: it.title })));
  const returns = p.items
    .map((it) => ({ it, run: runOf(it.id) }))
    .filter((x) => x.run);
  const overdue = plans.filter((r) => r.status === "overdue");
  return `
    <div class="ltc">
    <div class="section-header"><span class="section-title">优化</span><span class="section-badge">Check / Act</span><span class="section-note">执行回流后的状态挂在对象上，不在聊天里</span></div>
    <p class="lead">${esc(p.tension)}</p>
    ${cycleHtml(p.project.cycle)}
    <div class="panel" style="margin-bottom:12px">
      <h3>卡口回流 ${overdue.length ? "· " + overdue.length + " 项逾期" : ""}</h3>
      ${
        overdue.length
          ? `<ul>${overdue
              .map((r) => `<li><button type="button" class="text-btn" data-item="${r.id}">${esc(r.title || itemById(r.id).title)}</button> · ${esc(r.task)} · ${esc(r.owner)}</li>`)
              .join("")}</ul>`
          : `<p class="empty">本窗口没有逾期计划。先看执行回流。</p>`
      }
    </div>
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
    <div class="section-header"><span class="section-title">本窗口计划</span><span class="section-note">从闭环行动队列回收</span></div>
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
    </div>
  `;
}

function renderDepositMain() {
  const sc = scene();
  const p = pack();
  return `
    <div class="ltc">
    <div class="section-header"><span class="section-title">沉淀</span><span class="section-badge">策略资产</span><span class="section-note">效果回收后等人确认 ChangeSet，禁止静默改知识</span></div>
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
    </div>
  `;
}

function renderSceneMain() {
  if (state.view === "optimize") return renderOptimizeMain();
  if (state.view === "deposit") return renderDepositMain();
  if (state.pack === "cm") {
    return window.LTC_WB.render({
      cm: state.cmOwner,
      q: state.q,
      status: state.healthFilter,
      stage: state.stageFilter,
      selected: state.selectedId,
      viewStage: state.ltcViewStage,
    });
  }
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
  const cm = $("f-cm");
  if (q) {
    q.oninput = () => {
      state.q = q.value;
      render(false);
      const el = $("f-q");
      if (el) {
        el.focus();
        el.selectionStart = el.selectionEnd = el.value.length;
      }
    };
  }
  if (h) {
    h.onchange = () => {
      state.healthFilter = h.value;
      render(false);
    };
  }
  if (cm) {
    cm.onchange = () => {
      state.cmOwner = cm.value;
      render(false);
    };
  }
}

function render(animate) {
  if (!pack().items.some((i) => i.id === state.selectedId)) {
    state.selectedId = pack().items.find((i) => i.hot)?.id || pack().items[0].id;
  }
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
  const ltcStage = e.target.closest("[data-ltc-stage]");
  if (ltcStage) {
    state.stageFilter = state.stageFilter === ltcStage.dataset.ltcStage ? "" : ltcStage.dataset.ltcStage;
    render(false);
    return;
  }
  const ltcCust = e.target.closest("[data-ltc-cust]");
  if (ltcCust) {
    state.selectedId = ltcCust.dataset.ltcCust;
    state.ltcViewStage = null;
    render(false);
    return;
  }
  const ltcTab = e.target.closest("[data-ltc-tab]");
  if (ltcTab) {
    const it = itemById(state.selectedId);
    const cur = it.stage || (window.LTC_WB && (window.LTC_WB.DATA.customers.find((x) => x.customer_uec === state.selectedId) || {}).current_stage);
    state.ltcViewStage = cur && ltcTab.dataset.ltcTab === cur ? null : ltcTab.dataset.ltcTab;
    render(false);
    return;
  }
  if (e.target.closest("[data-ltc-reset]")) {
    state.stageFilter = "";
    state.healthFilter = "";
    state.q = "";
    state.cmOwner = state.pack === "cm" ? "cowen.hua" : "all";
    state.ltcViewStage = null;
    render(false);
    return;
  }
  if (e.target.closest("[data-ltc-query]")) {
    render(false);
    return;
  }
  if (e.target.closest("[data-ltc-export]")) {
    if (state.pack === "cm" && window.LTC_WB) {
      window.LTC_WB.exportCSV({
        cm: state.cmOwner,
        q: state.q,
        status: state.healthFilter,
        stage: state.stageFilter,
      });
      toast("已导出 CM_LTC_工作台.csv");
    } else {
      exportSceneCSV();
      toast("已导出 " + pack().id.toUpperCase() + "_工作台.csv");
    }
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
  state.cmOwner = e.target.value === "cm" ? "cowen.hua" : "all";
  state.ltcViewStage = null;
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
