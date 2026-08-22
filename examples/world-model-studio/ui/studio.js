const STEPS = [
  { id: "input", label: "输入" },
  { id: "simulate", label: "模拟" },
  { id: "generate", label: "生成" },
  { id: "interact", label: "交互" },
  { id: "evolve", label: "进化" },
  { id: "output", label: "输出" },
  { id: "yield", label: "收益" },
];

const GATES = {
  input: { gate: "G1", loop: "On" },
  simulate: { gate: "G1", loop: "On" },
  generate: { gate: "G2", loop: "On" },
  interact: { gate: "G3", loop: "In" },
  evolve: { gate: "G2", loop: "On" },
  output: { gate: "G3", loop: "In" },
  yield: { gate: "G0", loop: "Above" },
};

function clone(x) {
  return JSON.parse(JSON.stringify(x));
}

const SEED = {
  world_model_id: "wm.hiring.shortlist.staff-eng-2026q3",
  north_star: "quality-adjusted hiring success",
  identities: {
    mirror: "3 名候选人已初筛，短名单未冻结，文化分有默认值。",
    lens: "张力：学历硬门槛 vs 工程证据；未接地文化分冒充确定性。",
    furnace: "人确认后才能写成组织承诺；驳回未接地字段必须回写法则。",
  },
  dimensions: {
    space: { org: "Acme · Platform Engineering", team: "Core Runtime", location: "上海 / 可远程" },
    time: { freeze_by: "2026-08-25", sla: "短名单 ≤ 3 工作日", rollback_window_hours: 48 },
    subject: [
      { id: "sub.hiring-manager", name: "陈可", role: "hiring_manager" },
      { id: "sub.recruiter", name: "周岚", role: "recruiter" },
      { id: "cand.zhang-san", name: "张三", role: "candidate" },
      { id: "cand.li-si", name: "李四", role: "candidate" },
      { id: "cand.wang-min", name: "王敏", role: "candidate" },
    ],
    object: [{ id: "obj.shortlist", type: "shortlist", status: "uncompiled", slots: 2 }],
    feedback: [
      { source: "screening_evidence", grounded: true },
      { source: "culture_fit_default", grounded: false },
    ],
  },
  ideal: {
    shortlist_rule: "2 人 onsite，技能对齐且风险可解释",
    degree_gate: "本科硬门槛",
    culture_known: true,
  },
  reality: {
    candidates: [
      {
        id: "cand.wang-min",
        name: "王敏",
        degree: "本科",
        years: 9,
        skills: "Python / 分布式 / 可观测性",
        note: "门槛对齐；无现场面试",
        risk: [],
      },
      {
        id: "cand.zhang-san",
        name: "张三",
        degree: "专科",
        years: 7,
        skills: "Python / NLP / 项目管理",
        note: "学历不足；领域证据强。culture_fit=60 未接地",
        risk: ["education_below_requirement"],
      },
      {
        id: "cand.li-si",
        name: "李四",
        degree: "专科",
        years: 7,
        skills: "Python / Django",
        note: "Staff 技能覆盖不足",
        risk: ["education_below_requirement", "insufficient_skills"],
      },
    ],
  },
  gaps: [
    { id: "gap.degree", text: "学历硬门槛 vs 不得静默淘汰" },
    { id: "gap.culture", text: "理念假装文化已知 vs 现实无面试" },
  ],
  laws: [
    { id: "LAW-EDU-001", text: "学历不足禁止自动淘汰，升 G3。" },
    { id: "LAW-EVD-001", text: "无面试的 culture_fit 为未接地假设。" },
    { id: "LAW-SUB-001", text: "候选人是主体维度，不是通知附件。" },
    { id: "LAW-GATE-001", text: "短名单冻结 = 组织承诺，In · G3，回滚 48h。" },
    { id: "LAW-EXEC-001", text: "模型提议，平台执行。" },
  ],
  cycle: { current_step: "input", completed: [] },
  decision: { schemes: [], selected_scheme_id: null, human_confirmed: false },
  changeset: [],
  audit: [],
};

const state = {
  stepIndex: 0,
  wm: clone(SEED),
};

function applyThrough(index) {
  state.wm = clone(SEED);
  const wm = state.wm;
  const upto = STEPS.slice(0, index + 1).map((s) => s.id);
  if (upto.includes("input")) {
    wm.intent = "冻结 Staff Engineer 短名单（2 人 onsite）；禁止黑箱分数与自动淘汰。";
  }
  if (upto.includes("simulate")) {
    wm.simulation = "编译法则：文化分剥离；学历不足须人确认；李四默认不进短名单。";
  }
  if (upto.includes("generate")) {
    wm.decision.schemes = [
      { id: "scheme.grounded", title: "证据优先", advance: ["王敏", "张三"], hold: ["李四"] },
      { id: "scheme.degree-hard", title: "学历硬门槛（对冲，违法条）", advance: ["王敏"], hold: ["张三", "李四"] },
    ];
  }
  if (upto.includes("interact")) {
    wm.decision.selected_scheme_id = "scheme.grounded";
    wm.decision.human_confirmed = true;
    wm.decision.evidence_box = [
      "王敏：学历/年限/Runtime 技能有简历事实。",
      "张三：领域证据在，学历风险须人确认。",
      "李四：Staff 必备覆盖不足。",
      "culture_fit=60 已从建议剥离。",
    ];
    wm.decision.uncertainties = ["无现场面试", "张三年限未经 HRIS 核对"];
  }
  if (upto.includes("evolve")) {
    wm.ideal.culture_known = false;
    wm.laws.find((l) => l.id === "LAW-EVD-001").text =
      "culture_fit 无面试证据一律 UNGROUNDED，不得写入 overall。";
    wm.changeset = [
      {
        changeset_id: "cs.wm.ui-walkthrough",
        signal: "reject_ungrounded_culture_fit",
        patches: ["LAW-EVD-001 收紧", "ideal.culture_known=false"],
      },
    ];
  }
  if (upto.includes("output")) {
    wm.output = {
      shortlist: ["王敏", "张三"],
      hold: ["李四"],
      cs_preview: { operation: "cs.process.start", executed: false, gate: "G3" },
    };
    wm.dimensions.object[0].status = "frozen_pending_platform";
  }
  if (upto.includes("yield")) {
    wm.yield = {
      attributed: true,
      metrics: { ungrounded_in_recommendation: 0, auto_rejects: 0, human_confirmed: true },
    };
  }
  wm.cycle.current_step = STEPS[index].id;
  wm.cycle.completed = upto;
  wm.audit = upto.map((s, i) => ({ step: s, event: "compiled", n: i + 1 }));
}

function render() {
  const step = STEPS[state.stepIndex];
  const wm = state.wm;
  const g = GATES[step.id];

  const nav = document.getElementById("steps");
  nav.innerHTML = STEPS.map((s, i) => {
    const cls = ["step", i === state.stepIndex ? "active" : "", i < state.stepIndex ? "done" : ""].join(" ");
    return `<button class="${cls}" data-i="${i}"><span class="n">0${i + 1}</span>${s.label}</button>`;
  }).join("");
  nav.querySelectorAll("button").forEach((b) =>
    b.addEventListener("click", () => {
      state.stepIndex = Number(b.dataset.i);
      applyThrough(state.stepIndex);
      render();
    })
  );

  document.getElementById("intent-line").textContent =
    wm.intent || "编译「输入」以绑定意图与成功标准。";

  document.getElementById("gate-row").innerHTML = [
    `<span class="chip ${g.gate.toLowerCase()}">${g.gate}</span>`,
    `<span class="chip ${g.loop.toLowerCase()}">${g.loop} the loop</span>`,
    `<span class="chip">回滚 ${wm.dimensions.time.rollback_window_hours}h</span>`,
    `<span class="chip grounded">先解释 · 再建议 · 再动作</span>`,
  ].join("");

  const people = wm.reality.candidates;
  const scheme = (wm.decision.schemes || []).find((s) => s.id === wm.decision.selected_scheme_id);
  const advance = scheme ? scheme.advance : [];
  const hold = scheme ? scheme.hold : people.map((p) => p.name);
  document.getElementById("shortlist").innerHTML = people
    .map((p) => {
      const tag = advance.includes(p.name) ? "advance" : "hold";
      const label = advance.includes(p.name) ? "进入" : "暂缓";
      return `<li><span class="tag ${tag}">${label}</span><div><h4>${p.name}</h4><p>${p.degree} · ${p.years}年 · ${p.skills}<br>${p.note}</p></div></li>`;
    })
    .join("");

  const ev = document.getElementById("evidence-box");
  const un = document.getElementById("uncertainty-box");
  ev.innerHTML = (wm.decision.evidence_box || ["尚未进入交互步。"]).map((t) => `<li>${t}</li>`).join("");
  un.innerHTML = (wm.decision.uncertainties || ["编译到「交互」后出现。"]).map((t) => `<li>${t}</li>`).join("");

  const actions = document.getElementById("actions");
  if (step.id === "interact") {
    actions.innerHTML = `
      <button class="act" id="confirm">确认证据优先方案</button>
      <button class="act ghost" id="hard">查看学历硬门槛（应被拦截）</button>`;
    document.getElementById("confirm").onclick = () => {
      state.wm.decision.human_confirmed = true;
      render();
    };
    document.getElementById("hard").onclick = () => {
      state.wm.decision.selected_scheme_id = "scheme.degree-hard";
      state.wm.decision.human_confirmed = false;
      state.wm.decision.blocked = "CHARTER_VIOLATION:LAW-EDU-001";
      render();
    };
  } else if (state.stepIndex < 6) {
    actions.innerHTML = `<button class="act" id="next">编译下一步</button>`;
    document.getElementById("next").onclick = () => {
      state.stepIndex += 1;
      applyThrough(state.stepIndex);
      render();
    };
  } else {
    actions.innerHTML = `<button class="act ghost" id="reset">重新编译</button>`;
    document.getElementById("reset").onclick = () => {
      state.stepIndex = 0;
      applyThrough(0);
      render();
    };
  }

  document.getElementById("ideal-pane").innerHTML = `
    <p>${wm.ideal.shortlist_rule}</p>
    <p>学历：${wm.ideal.degree_gate}</p>
    <p>文化已知：${wm.ideal.culture_known ? "是（理念过度承诺）" : "否（已与现实对冲）"}</p>`;
  document.getElementById("reality-pane").innerHTML = people
    .map((p) => `<p><strong>${p.name}</strong> ${p.degree} · ${p.note}</p>`)
    .join("");
  document.getElementById("gaps").innerHTML = wm.gaps
    .map((g) => `<div class="gap"><strong>对冲</strong> ${g.text}</div>`)
    .join("");

  const d = wm.dimensions;
  document.getElementById("dims").innerHTML = [
    ["空间", `${d.space.org}<br>${d.space.team}<br>${d.space.location}`],
    ["时间", `冻结 ${d.time.freeze_by}<br>${d.time.sla}<br>回滚 ${d.time.rollback_window_hours}h`],
    ["主体", d.subject.map((s) => `${s.name} · ${s.role}`).join("<br>")],
    ["客体", `短名单 ${d.object[0].status} · ${d.object[0].slots} 席`],
    ["反馈", d.feedback.map((f) => `${f.source} ${f.grounded ? "已接地" : "未接地"}`).join("<br>")],
  ]
    .map(([h, b]) => `<div class="dim"><h4>${h}</h4><div>${b}</div></div>`)
    .join("");

  document.getElementById("laws").innerHTML =
    `<tr><th>ID</th><th>法则</th></tr>` +
    wm.laws.map((l) => `<tr><td>${l.id}</td><td>${l.text}</td></tr>`).join("");

  document.getElementById("changeset").textContent = JSON.stringify(wm.changeset, null, 2);
  document.getElementById("audit").textContent = JSON.stringify(wm.audit, null, 2);
}

async function boot() {
  try {
    const res = await fetch("../database/world_model.json", { cache: "no-store" });
    if (res.ok) {
      const disk = await res.json();
      if (disk.cycle && disk.cycle.completed && disk.cycle.completed.length === 7) {
        SEED.diskNote = "已加载 scripts 落盘的世界模型";
      }
    }
  } catch (_e) {
    /* file:// or first run: use seed */
  }
  applyThrough(0);
  render();
}

boot();
