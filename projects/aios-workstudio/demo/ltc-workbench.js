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
