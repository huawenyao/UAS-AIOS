/* Platform Console demo. 只模拟 hub.ops.*；禁止写生产与时态摄入入口。 */
(function () {
  const D = window.CONSOLE_DATA;
  const $ = (sel, el = document) => el.querySelector(sel);
  const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));

  const state = {
    role: "knowledge_admin",
    page: "overview",
    proto: "all",
    flow: "all",
    module: "m6",
    integration: "I-05",
    profile: "scene",
    op: "cs.visit.schedule",
    node: "an-stage-visit",
    mcpProfile: "scene",
    auditQ: "",
    wmDraft: D.wm.draft.laws.join("\n"),
    changesets: D.changesets.map((c) => ({ ...c })),
    registryOn: Object.fromEntries(D.ops.map((o) => [o.id, true])),
    playing: false,
  };

  function roleOf() {
    return D.roles.find((r) => r.id === state.role);
  }

  function canSee(page) {
    const r = roleOf();
    return r.sees.includes(page);
  }

  function toast(msg, kind = "") {
    const box = $("#toast");
    const el = document.createElement("div");
    el.className = "item " + kind;
    el.textContent = msg;
    box.appendChild(el);
    setTimeout(() => el.remove(), 3200);
  }

  function navHtml() {
    return D.pages.map((p) => {
      const locked = !canSee(p.id) || state.role === "frontline";
      const cls = [
        state.page === p.id && state.role !== "frontline" ? "active" : "",
        locked ? "locked" : "",
      ].join(" ");
      const guard = locked ? `aria-disabled="true" tabindex="-1"` : "";
      return `<a href="#/${p.id}" data-page="${p.id}" class="${cls}" ${guard}>
        <i class="tick"></i>
        <span>${esc(p.label)}<small>${esc(p.hint)}</small></span>
      </a>`;
    }).join("");
  }

  function renderChrome() {
    $("#role").value = state.role;
    $("nav").innerHTML = navHtml();
    const page = D.pages.find((p) => p.id === state.page) || D.pages[0];
    if (state.role === "frontline") {
      $("#page-stamp").textContent = "CONSOLE · DENIED";
      $("#page-title").textContent = "看不到 /console";
    } else {
      $("#page-stamp").textContent = "CONSOLE · " + page.stamp;
      $("#page-title").textContent = page.label;
    }
    $("#pills").innerHTML = [
      `<span class="pill">${esc(D.tenant.tenant_id)}</span>`,
      `<span class="pill">${esc(roleOf().label)}</span>`,
      `<span class="pill">profile 由入口强制</span>`,
      `<span class="pill v">auto_apply = 关</span>`,
    ].join("");
  }

  function render() {
    renderChrome();
    const view = $("#view");
    if (state.role === "frontline") {
      view.innerHTML = `<div class="lock">
        <div class="stamp" style="color:var(--v)">一线账号</div>
        <h2>看不到 /console</h2>
        <p>一线只走 WorkStudio 北向 hub.scene.*。连接器、口径公式、Law 条文和工作流检索不在一线菜单。</p>
        <p class="note">请切换为知识管理员或平台管理员查看运营产品。</p>
      </div>`;
      return;
    }
    if (!canSee(state.page)) {
      view.innerHTML = `<div class="lock">
        <h2>当前角色不能打开此页</h2>
        <p>${esc(roleOf().label)} 的可管对象见产品矩阵。写配置一律进 ChangeSet。</p>
      </div>`;
      return;
    }
    const fn = pages[state.page] || pages.overview;
    view.innerHTML = fn();
    bindView();
  }

  const pages = {
    overview: pageOverview,
    integrate: pageIntegrate,
    control: pageControl,
    ontology: pageOntology,
    mesh: pageMesh,
    govern: pageGovern,
    run: pageRun,
    publish: pagePublish,
  };

  function pageOverview() {
    const h = D.health;
    return `
      <p class="note">运营后台是正式产品，不是零件原生 UI。平面 SLO 用经营语言；零件名只在 SRE 逃生通道出现。</p>
      <div class="row g4">
        <div class="metric ok"><b>${h.use.open_ms} ms</b><span>打开作战台</span></div>
        <div class="metric ok"><b>${Math.round(h.control.explain_coverage * 100)}%</b><span>explain 覆盖</span></div>
        <div class="metric warn"><b>${h.runtime.approval_stuck}</b><span>审批滞留</span></div>
        <div class="metric ${h.caliber.stale_nodes ? "warn" : "ok"}"><b>${h.caliber.stale_nodes}</b><span>口径延迟节点</span></div>
      </div>
      <div class="row split">
        <div class="panel">
          <h3>三条流必须分名 <span class="sub">控制 / 数据 / 管理</span></h3>
          <table>
            <thead><tr><th>流</th><th>携带</th><th>禁止</th></tr></thead>
            <tbody>${D.flows.map((f) => `<tr>
              <td>${esc(f.name)}</td><td>${esc(f.carry)}</td><td class="muted">${esc(f.ban)}</td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
        <div class="panel">
          <h3>待发布</h3>
          ${pendingList()}
          <p class="note">所有配置写汇合到 ChangeSet。未审批不进 compiled。</p>
          <a class="btn primary" href="#/publish">打开发布台</a>
        </div>
      </div>
      <div class="row g2">
        <div class="panel">
          <h3>集群心跳（管理流可见）</h3>
          <table>
            <thead><tr><th>事件</th><th>发出</th><th>消费</th></tr></thead>
            <tbody>${D.events.map((e) => `<tr>
              <td class="mono">${esc(e.id)}</td><td>${esc(e.from)}</td><td class="muted">${esc(e.to)}</td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
        <div class="panel">
          <h3>硬隔离</h3>
          <ul class="iso">${D.isolations.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>
        </div>
      </div>`;
  }

  function pendingList() {
    const rows = state.changesets.filter((c) => c.status === "pending");
    if (!rows.length) return `<p class="ok-line">没有待确认草案。</p>`;
    return `<table><tbody>${rows.map((c) => `<tr>
      <td class="mono">${esc(c.id)}</td>
      <td>${esc(c.title)}</td>
      <td><span class="pill ${c.invariant === "pass" ? "ok" : "bad"}">${esc(c.invariant)}</span></td>
    </tr>`).join("")}</tbody></table>`;
  }

  function pageIntegrate() {
    const integ = D.integrations.find((x) => x.id === state.integration);
    const mods = D.modules;
    return `
      <p class="note">模块之间不进对方数据库。点协议、点验收对、点模块，看信封与管理落点。</p>
      <div class="toolbar">
        <button class="btn ${state.proto === "all" ? "active" : ""}" data-proto="all">全协议</button>
        ${D.protocols.map((p) => `<button class="btn ${state.proto === p.id ? "active" : ""}" data-proto="${p.id}">${esc(p.name)}</button>`).join("")}
        <span class="grow"></span>
        <button class="btn primary" id="play-i">${state.playing ? "停止回放" : "回放 I-05 写拒绝"}</button>
      </div>
      <div class="row split">
        <div class="panel">
          ${integrateSvg()}
        </div>
        <div class="panel">
          <h3>验收 ${esc(integ.id)} <span class="sub">${esc(integ.pair)}</span></h3>
          <p>${esc(integ.pass)}</p>
          <div class="trace" id="trace">${traceFor(integ.id)}</div>
          <h3 style="margin-top:12px">集成对</h3>
          <table>
            <tbody>${D.integrations.map((x) => `<tr class="click ${x.id === state.integration ? "sel" : ""}" data-int="${x.id}">
              <td class="mono">${esc(x.id)}</td><td>${esc(x.pair)}</td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
      </div>
      <div class="panel">
        <h3>模块管理落点</h3>
        <table>
          <thead><tr><th>模块</th><th>平面</th><th>协议</th><th>管理产品</th><th>接口</th></tr></thead>
          <tbody>${mods.map((m) => `<tr class="click ${m.id === state.module ? "sel" : ""}" data-mod="${m.id}">
            <td>${esc(m.t)}</td>
            <td class="muted">${esc(m.plane)}</td>
            <td class="mono">${esc(m.proto)}</td>
            <td>${esc(m.manage)}</td>
            <td class="mono">${esc(m.api)}</td>
          </tr>`).join("")}</tbody>
        </table>
      </div>`;
  }

  function integrateSvg() {
    const on = (set) => {
      if (state.proto === "all") return "";
      return set.includes(state.proto) ? "" : " is-dim";
    };
    return `<svg class="int-map" viewBox="0 0 760 280" role="img" aria-label="三平面集成">
      <rect x="8" y="8" width="744" height="68" fill="#0e2a33" stroke="#4fc3f744"/>
      <text x="20" y="28" fill="#4fc3f7" font-size="11">使用平面</text>
      <g class="mod${on("n")}" data-pick="m1"><rect x="40" y="36" width="160" height="32" fill="#123844" stroke="#4fc3f7"/><text x="120" y="56" text-anchor="middle" fill="#d7e6ee" font-size="12">WorkStudio</text></g>
      <g class="mod${on("n")}" data-pick="m5"><rect x="220" y="36" width="140" height="32" fill="#123844" stroke="#4fc3f799"/><text x="290" y="56" text-anchor="middle" fill="#d7e6ee" font-size="12">签发台</text></g>
      <rect x="8" y="88" width="744" height="92" fill="#0c1d2c" stroke="#90caf944"/>
      <text x="20" y="108" fill="#90caf9" font-size="11">控制平面</text>
      <g class="mod${on("n")}" data-pick="m6"><rect x="40" y="120" width="180" height="44" fill="#14324a" stroke="#90caf9"/><text x="130" y="146" text-anchor="middle" fill="#d7e6ee" font-size="13">Capability Hub</text></g>
      <g class="mod${on("s")}" data-pick="m7"><rect x="240" y="122" width="110" height="40" fill="#12263a" stroke="#66bb6a"/><text x="295" y="146" text-anchor="middle" fill="#d7e6ee" font-size="11">Registry</text></g>
      <g class="mod${on("s")}" data-pick="m13"><rect x="360" y="122" width="110" height="40" fill="#12263a" stroke="#66bb6a"/><text x="415" y="146" text-anchor="middle" fill="#d7e6ee" font-size="11">MCP</text></g>
      <g class="mod${on("v")}" data-pick="m12"><rect x="490" y="122" width="110" height="40" fill="#12263a" stroke="#ffe082"/><text x="545" y="146" text-anchor="middle" fill="#d7e6ee" font-size="11">Evolution</text></g>
      <g class="mod${on("i")}" data-pick="m8"><rect x="620" y="122" width="110" height="40" fill="#12263a" stroke="#90caf9"/><text x="675" y="146" text-anchor="middle" fill="#d7e6ee" font-size="11">IAM</text></g>
      <rect x="8" y="192" width="744" height="80" fill="#0c141e" stroke="#80cbc444"/>
      <text x="20" y="212" fill="#80cbc4" font-size="11">配置与运维</text>
      <g class="mod${on("n")}" data-pick="m2"><rect x="40" y="224" width="100" height="32" fill="#12263a" stroke="#80cbc4"/><text x="90" y="244" text-anchor="middle" fill="#d7e6ee" font-size="11">责任图</text></g>
      <g class="mod${on("k")}" data-pick="m15"><rect x="160" y="224" width="100" height="32" fill="#12263a" stroke="#80cbc4"/><text x="210" y="244" text-anchor="middle" fill="#d7e6ee" font-size="11">口径</text></g>
      <g class="mod${on("k")}" data-pick="m16"><rect x="280" y="224" width="100" height="32" fill="#12263a" stroke="#80cbc4"/><text x="330" y="244" text-anchor="middle" fill="#d7e6ee" font-size="11">时态</text></g>
      <g class="mod${on("e")}" data-pick="m18"><rect x="400" y="224" width="100" height="32" fill="#12263a" stroke="#ffb74d"/><text x="450" y="244" text-anchor="middle" fill="#d7e6ee" font-size="11">外环</text></g>
      <g class="mod${on("s")}" data-pick="m14"><rect x="520" y="224" width="100" height="32" fill="#12263a" stroke="#66bb6a"/><text x="570" y="244" text-anchor="middle" fill="#d7e6ee" font-size="11">连接器</text></g>
      <g class="mod${on("k")}" data-pick="m17"><rect x="640" y="224" width="100" height="32" fill="#12263a" stroke="#ef9a9a"/><text x="690" y="244" text-anchor="middle" fill="#d7e6ee" font-size="11">记忆</text></g>
      <line class="flow" x1="120" y1="68" x2="130" y2="120" stroke="#4fc3f7" stroke-width="1.4"/>
      <line class="flow" x1="220" y1="142" x2="240" y2="142" stroke="#66bb6a" stroke-width="1.4"/>
      <line class="flow" x1="130" y1="164" x2="90" y2="224" stroke="#80cbc4" stroke-width="1.4"/>
    </svg>`;
  }

  function traceFor(id) {
    const map = {
      "I-01": `GET WorkStudio\n  → POST /hub/v1/scene/pack/open\n  envelope.profile = scene  (路由强制，客户端伪造作废)\n  ← 责任图切片 · 无人零件 SDK`,
      "I-02": `pack.open node=an-incomplete\n  missing wm.feedback\n  → 422 WM_INCOMPLETE\n  ${D.explain.WM_INCOMPLETE.message}`,
      "I-03": `cs.metric.query kpi-visit-dwell\n  ← is=28 as_of=2026-08-22 stale=true\n  作战台展示「口径延迟」，不假装实时`,
      "I-04": `insight.drill node=an-stage-visit evidence_refs=[]\n  → 422 UNGROUNDED_INSIGHT\n  ${D.explain.UNGROUNDED_INSIGHT.message}`,
      "I-05": `profile=scene  invoke cs.visit.schedule\n  chain tenant→registry→RBAC → STOP\n  → 403 PROFILE_FORBIDS_SIDE_EFFECT\n  ${D.explain.PROFILE_FORBIDS_SIDE_EFFECT.message}\n  next: ${D.explain.PROFILE_FORBIDS_SIDE_EFFECT.next}`,
      "I-06": `exec.open task-visit-uec-10293\n  Worker Activity 回调 Hub 门禁\n  一线只见「待你确认」，不展示工作流编号`,
      "I-07": `InnerLoop turn\n  tools/call 只能进 Hub\n  静态检查：无出站 CRM HTTP`,
      "I-08": `track=pipaw  hub.memory.self.get\n  → 403 MEMORY_TRACK_FORBIDDEN\n  forget → receipt rec-forget-20260911 可检索`,
      "I-09": `changeset.submit target=law_pack\n  applied=false auto_apply=false\n  compiled PATCH 被拒绝，直到 decide=confirm`,
      "I-10": `actor 无 position_id\n  pack.open → 403 SCOPE_DENIED\n  人从 IdP 来，经营承诺权在岗位绑定`,
      "I-11": `cs.visit.schedule 成功\n  RefreshKpi → an-stage-visit.is 合流\n  指挥舱与作战台同一 node_id`,
      "I-12": `registry cs.visit.schedule\n  MCP tools/list 同名同字段\n  drift=0`,
    };
    return map[id] || "";
  }

  function pageControl() {
    const p = D.profiles;
    const chain = D.chain;
    const op = D.ops.find((o) => o.id === state.op);
    const result = dryRun(state.profile, op);
    const stopped = result.stopAt;
    return `
      <p class="note">Hub Console 不是第二套 Hub。数据只调 hub.ops.policy.explain / profile.matrix / tenant.get。禁止关审计，禁止客户端改 profile。</p>
      <div class="row split">
        <div class="panel">
          <h3>剖面矩阵 <span class="sub">四剖面 × 写生产</span></h3>
          <table class="matrix">
            <thead><tr><th></th><th>scene</th><th>explore</th><th>builder</th><th>runtime</th></tr></thead>
            <tbody>
              <tr><td>写 SoR</td>${writeCell(p.scene.cs_write)}${writeCell(p.explore.cs_write)}${writeCell(p.builder.cs_write)}${writeCell(p.runtime.cs_write)}</tr>
              <tr><td>执行 Skill</td>${boolCell(p.scene.skill_execute)}${boolCell(p.explore.skill_execute)}${boolCell(p.builder.skill_execute)}${boolCell(p.runtime.skill_execute)}</tr>
              <tr><td>Skill 上限</td><td>${p.scene.skill_max}</td><td>${p.explore.skill_max}</td><td>${p.builder.skill_max}</td><td>${p.runtime.skill_max}</td></tr>
            </tbody>
          </table>
        </div>
        <div class="panel">
          <h3>若现在点写会怎样</h3>
          <div class="toolbar">
            <div class="field"><label>剖面（入口强制）</label>
              <select id="profile">${["scene", "explore", "builder", "runtime"].map((x) =>
                `<option ${x === state.profile ? "selected" : ""}>${x}</option>`).join("")}</select>
            </div>
            <div class="field grow"><label>拟调用</label>
              <select id="op">${D.ops.map((o) =>
                `<option value="${esc(o.id)}" ${o.id === state.op ? "selected" : ""}>${esc(o.id)}</option>`).join("")}</select>
            </div>
            <button class="btn primary" id="explain">试运行</button>
          </div>
          <div class="chain">${chain.map((s, i) => {
            const mark = i < stopped ? "on" : i === stopped ? "block" : "";
            return `<span class="step ${mark}">${esc(s)}</span>${i < chain.length - 1 ? `<span class="arr">→</span>` : ""}`;
          }).join("")}</div>
          <div class="trace" style="margin-top:10px">${result.html}</div>
        </div>
      </div>
      <div class="panel">
        <h3>403 分类（本租户）</h3>
        <p class="note">explain 可用率必须 100%。有码就有人话和下一步。</p>
        <table>
          <thead><tr><th>码</th><th>人话</th><th>下一步</th></tr></thead>
          <tbody>${Object.entries(D.explain).map(([k, v]) => `<tr>
            <td class="mono">${esc(k)}</td><td>${esc(v.message)}</td><td class="mono">${esc(v.next)}</td>
          </tr>`).join("")}</tbody>
        </table>
      </div>`;
  }

  function writeCell(v) {
    if (v === true) return `<td class="dot-on">允许</td>`;
    if (v === "dry-run") return `<td class="dot-dry">dry-run</td>`;
    return `<td class="dot-off">拒绝</td>`;
  }
  function boolCell(v) {
    return v ? `<td class="dot-on">是</td>` : `<td class="dot-off">否</td>`;
  }

  function dryRun(profile, op) {
    const steps = D.chain;
    let html = `<span class="info">envelope.profile=${esc(profile)}  (忽略客户端伪造)</span>\n`;
    html += `<span class="info">op=${esc(op.id)}  write=${op.write}  ${esc(op.level)}</span>\n`;
    if (op.write && profile === "scene") {
      const e = D.explain.PROFILE_FORBIDS_SIDE_EFFECT;
      html += `<span class="bad">403 PROFILE_FORBIDS_SIDE_EFFECT</span>\n${esc(e.message)}\nnext: ${esc(e.next)}`;
      return { html, stopAt: 2 };
    }
    if (op.write && profile === "explore") {
      html += `<span class="bad">403 PROFILE_FORBIDS_SIDE_EFFECT</span>\n研究剖面不能写生产。`;
      return { html, stopAt: 2 };
    }
    if (op.write && profile === "builder") {
      html += `<span class="v">dry-run 通过，不落 SoR</span>\n审计写入 ops.registry 试运行，applied=false`;
      return { html, stopAt: steps.length };
    }
    if (op.write && profile === "runtime" && op.level === "L3") {
      html += `<span class="bad">403 GATE_BLOCKED</span>\n${esc(D.explain.GATE_BLOCKED.message)}\n需要 L3 审批信号`;
      return { html, stopAt: 3 };
    }
    html += `<span class="ok">判定序走完 · 可执行（演示）</span>\n审计类型 ${op.write ? "cs.invoked" : "cs.read"}`;
    return { html, stopAt: steps.length };
  }

  function pageOntology() {
    const node = D.graph.nodes.find((n) => n.node_id === state.node);
    const incomplete = nodeIncomplete(node);
    return `
      <p class="note">本体工作室：责任图画布、WM 三寿命、Law Pack。拖改不落生产。发布只走 ChangeSet。compiled 列只读。</p>
      <div class="row split">
        <div class="panel">
          <h3>责任图 <span class="sub">${esc(D.graph.graph_id)} · 投影 kpi_split</span></h3>
          ${graphSvg()}
          <p class="${incomplete ? "bad-line" : "ok-line"}">${incomplete ? "缺维：" + incomplete : "五件套齐全"}</p>
        </div>
        <div class="panel">
          <h3>节点 ${esc(node.node_id)}</h3>
          <dl class="kv">
            <dt>goal</dt><dd>${esc(node.goal.statement)}</dd>
            <dt>org</dt><dd class="mono">${esc(node.org.position_id)} · ${esc(node.org.owner_id)}</dd>
            <dt>kpi</dt><dd>${esc(node.kpi.name)} ought=${esc(node.kpi.ought)} is=${esc(node.kpi.is)}
              <span class="pill ${node.kpi.stale ? "warn" : "ok"}">${node.kpi.stale ? "stale" : "fresh"}</span></dd>
            <dt>process</dt><dd class="mono">read ${esc(node.process.cs_read.join(", ") || "—")}<br>write ${esc(node.process.cs_write.join(", ") || "—")}</dd>
            <dt>wm</dt><dd class="mono">${esc(Object.entries(node.wm).map(([k, v]) => k + "=" + v).join(" · "))}</dd>
          </dl>
          <button class="btn" id="validate">校验五件套</button>
          <button class="btn primary" id="pub-graph">提交发布</button>
        </div>
      </div>
      <div class="panel">
        <h3>世界模型寿命板 <span class="sub">${esc(D.wm.world_model_id)}</span></h3>
        <div class="wm-grid">
          <div class="wm-col">
            <h4>draft</h4>
            <textarea id="wm-draft">${esc(state.wmDraft)}</textarea>
            <p class="muted">可改。未发布。</p>
          </div>
          <div class="wm-col compiled">
            <h4>compiled · 只读</h4>
            <textarea disabled>${esc(D.wm.compiled.laws.join("\n"))}</textarea>
            <p class="muted">Runtime 不得 PATCH。改法则走 ChangeSet。</p>
          </div>
          <div class="wm-col live">
            <h4>live</h4>
            <p class="mono">${esc(D.wm.live.patch)}</p>
            <p class="muted">运行补丁。不是新法则。</p>
          </div>
        </div>
      </div>
      <div class="panel">
        <h3>Law Pack 版本对比</h3>
        <div class="row g2">
          <div><div class="muted">${esc(D.laws.current.version)}</div><p>${esc(D.laws.current.text)}</p></div>
          <div><div class="muted">${esc(D.laws.next.version)}</div><p>${esc(D.laws.next.text)}</p></div>
        </div>
        <button class="btn primary" id="pub-law">提交法则 ChangeSet</button>
      </div>`;
  }

  function nodeIncomplete(node) {
    for (const k of ["goal", "org", "kpi", "process", "wm"]) if (!node[k]) return k;
    const missing = ["space", "time", "subject", "object", "feedback"].filter((d) => !node.wm[d]);
    if (missing.length) return "wm." + missing.join(",");
    if (!node.kpi.caliber) return "caliber";
    return null;
  }

  function graphSvg() {
    const a = D.graph.nodes[0];
    const b = D.graph.nodes[1];
    const sel = (id) => (id === state.node ? "is-on" : "");
    return `<svg class="graph-svg" viewBox="0 0 640 200">
      <line x1="170" y1="88" x2="360" y2="88" stroke="#80cbc4"/>
      <text x="250" y="78" fill="#7a93a3" font-size="10">kpi_split</text>
      <g class="node-card ${sel(a.node_id)}" data-node="${a.node_id}">
        <rect x="24" y="40" width="200" height="96" fill="#0e2430" stroke="${a.kpi.status === "watch" ? "#ffb74d" : "#4fc3f7"}"/>
        <text x="124" y="78" text-anchor="middle" fill="#d7e6ee" font-size="13">${esc(a.node_id)}</text>
        <text x="124" y="100" text-anchor="middle" fill="#7a93a3" font-size="11">${esc(a.kpi.name)} · ${esc(a.kpi.status)}</text>
      </g>
      <g class="node-card ${sel(b.node_id)}" data-node="${b.node_id}">
        <rect x="380" y="40" width="220" height="96" fill="#0e2430" stroke="#ef9a9a"/>
        <text x="490" y="78" text-anchor="middle" fill="#d7e6ee" font-size="13">${esc(b.node_id)}</text>
        <text x="490" y="100" text-anchor="middle" fill="#7a93a3" font-size="11">${esc(b.kpi.name)} ${esc(b.kpi.is)}d · gate</text>
      </g>
    </svg>`;
  }

  function pageMesh() {
    const tools = D.ops.filter((o) => {
      if (state.mcpProfile === "scene" || state.mcpProfile === "explore") return !o.write;
      return state.registryOn[o.id];
    });
    return `
      <p class="note">能力网格展示模型可见名 / 审批级 / 副作用 / 租户开关，不展示 REST。密钥不明文回显。patch 进 ChangeSet。</p>
      <div class="row split">
        <div class="panel">
          <h3>目录 cs.*</h3>
          <table>
            <thead><tr><th>启用</th><th>operation</th><th>写</th><th>审批</th><th>副作用</th></tr></thead>
            <tbody>${D.ops.map((o) => `<tr>
              <td><input type="checkbox" data-reg="${esc(o.id)}" ${state.registryOn[o.id] ? "checked" : ""}></td>
              <td class="mono">${esc(o.id)}</td>
              <td>${o.write ? "是" : "否"}</td>
              <td>${esc(o.level)}</td>
              <td class="muted">${esc(o.effects.join(", ") || "无")}</td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
        <div class="panel">
          <h3>MCP 预览 <span class="sub">list 过滤不能跳过 call 判定</span></h3>
          <div class="toolbar">
            <select id="mcp-profile">${["scene", "explore", "builder", "runtime"].map((x) =>
              `<option ${x === state.mcpProfile ? "selected" : ""}>${x}</option>`).join("")}</select>
          </div>
          <table>
            <thead><tr><th>tools/list</th></tr></thead>
            <tbody>${tools.map((o) => `<tr><td class="mono">${esc(o.id)}</td></tr>`).join("")}</tbody>
          </table>
          <p class="muted">scene 隐藏写工具。call 仍走同一判定序。</p>
        </div>
      </div>
      <div class="row g2">
        <div class="panel">
          <h3>连接器槽</h3>
          <table>
            <thead><tr><th>id</th><th>槽</th><th>状态</th><th>密钥</th></tr></thead>
            <tbody>${D.connectors.map((c) => `<tr>
              <td class="mono">${esc(c.id)}</td>
              <td>${esc(c.slot)}</td>
              <td><span class="pill ${c.status === "up" ? "ok" : "warn"}">${esc(c.status)}</span></td>
              <td class="mono">${esc(c.secret)}</td>
            </tr>`).join("")}</tbody>
          </table>
          <button class="btn" id="rotate">轮换沙箱密钥</button>
        </div>
        <div class="panel">
          <h3>契约漂移</h3>
          <p class="ok-line">drift = 0 · Registry 与 MCP 名/字段一致（I-12）</p>
          <p class="muted">一份 JSON Schema 生成 Pydantic / MCP / 连接器校验。</p>
        </div>
      </div>`;
  }

  function pageGovern() {
    const bins = { discover: [], cited: [], installed: [], enabled: [] };
    D.skills.forEach((s) => {
      if (s.state === "enabled") bins.enabled.push(s);
      else if (s.state === "installed") bins.installed.push(s);
      else if (s.state === "cited") bins.cited.push(s);
      else bins.discover.push(s);
    });
    const q = state.auditQ.trim().toLowerCase();
    const audits = D.audit.filter((a) => !q || JSON.stringify(a).toLowerCase().includes(q));
    return `
      <p class="note">治理中心：岗位绑定、技能货架、制品晋升、审计导出、遗忘回执、转派。合规不派业务活。auto_apply 永关。</p>
      <div class="panel">
        <h3>岗位绑定</h3>
        <table>
          <thead><tr><th>人</th><th>岗位</th><th>org</th><th>track</th></tr></thead>
          <tbody>${D.bindings.map((b) => `<tr>
            <td class="mono">${esc(b.actor)}</td><td>${esc(b.position)}</td><td>${esc(b.org)}</td><td>${esc(b.track)}</td>
          </tr>`).join("")}</tbody>
        </table>
      </div>
      <div class="panel">
        <h3>技能货架 <span class="sub">discover → cite → install → enable · Explore 最高 cited</span></h3>
        <div class="funnel">
          ${["discover", "cited", "installed", "enabled"].map((k) => `<div class="bin"><b>${k}</b>
            ${bins[k].map((s) => `<div>${esc(s.name)}</div>`).join("") || `<span class="muted">空</span>`}
          </div>`).join("")}
        </div>
      </div>
      <div class="panel">
        <h3>制品晋升</h3>
        <div class="promote">${D.artifacts.map((a, i) => `
          <div class="art ${i < 2 ? "on" : ""}"><b>${esc(a.kind)}</b><div class="mono">${esc(a.id)}</div><div class="muted">${esc(a.status)}</div></div>
          ${i < D.artifacts.length - 1 ? `<span class="arr">→</span>` : ""}
        `).join("")}</div>
        <p class="muted">禁止「用报告回放经营」。file kind 不能驱动 pack.open。</p>
      </div>
      <div class="row g2">
        <div class="panel">
          <h3>审计检索</h3>
          <div class="toolbar">
            <input id="audit-q" placeholder="correlation / node / cs" value="${esc(state.auditQ)}">
            <button class="btn" id="audit-go">检索</button>
            <button class="btn" id="audit-export">导出合规包</button>
          </div>
          <table>
            <thead><tr><th>时间</th><th>类型</th><th>cs</th><th>剖面</th></tr></thead>
            <tbody>${audits.map((a) => `<tr>
              <td class="mono">${esc(a.ts)}</td><td>${esc(a.type)}</td>
              <td class="mono">${esc(a.cs || "—")}</td><td>${esc(a.profile)}</td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
        <div class="panel">
          <h3>遗忘回执</h3>
          <table>
            <tbody>${D.receipts.map((r) => `<tr>
              <td class="mono">${esc(r.id)}</td><td>${esc(r.scope)}</td>
              <td><span class="pill ok">${esc(r.status)}</span></td>
            </tr>`).join("")}</tbody>
          </table>
          <h3 style="margin-top:14px">转派</h3>
          <table>
            <tbody>${D.transfers.map((t) => `<tr>
              <td class="mono">${esc(t.task_id)}</td>
              <td>${esc(t.from)} → ${esc(t.to)}</td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
      </div>`;
  }

  function pageRun() {
    return `
      <p class="note">运行与知识运营用经营语言。按 task_id / source_node_id 检索。零件原生控制台仅 SRE 逃生，默认关。</p>
      <div class="panel">
        <h3>长任务</h3>
        <table>
          <thead><tr><th>任务</th><th>源节点</th><th>一线可见</th><th>滞留</th></tr></thead>
          <tbody>${D.runtime.map((t) => `<tr>
            <td class="mono">${esc(t.task_id)}</td>
            <td class="mono">${esc(t.node)}</td>
            <td>${esc(t.label)}</td>
            <td>${t.sla_hours}h</td>
          </tr>`).join("")}</tbody>
        </table>
        <button class="btn primary" id="retry">精确续跑 task-visit-uec-10293</button>
      </div>
      <div class="row g3">
        <div class="panel">
          <h3>口径</h3>
          <table>
            <tbody>${D.caliber.map((c) => `<tr>
              <td class="mono">${esc(c.kpi_id)}</td>
              <td>${esc(c.as_of)}</td>
              <td><span class="pill ${c.stale ? "warn" : "ok"}">${c.stale ? "stale" : "fresh"}</span></td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
        <div class="panel">
          <h3>时态摄入</h3>
          <p>延迟 ${D.kg.lag_s}s · 最近 ${esc(D.kg.last_episode)}</p>
          <p class="muted">白名单 ${esc(D.kg.whitelist.join(" / "))}</p>
          <p class="bad-line">本页无「在图上改 CRM」。无时态写入入口。</p>
        </div>
        <div class="panel">
          <h3>模型路由</h3>
          <table>
            <tbody>${D.models.map((m) => `<tr>
              <td>${esc(m.profile)}</td><td class="mono">${esc(m.model)}</td><td>${m.rpm} rpm</td>
            </tr>`).join("")}</tbody>
          </table>
        </div>
      </div>`;
  }

  function pagePublish() {
    return `
      <p class="note">发布台是所有配置写的汇合点。decide = confirm | reject。请求头 auto_apply 不生效。</p>
      <div class="panel">
        <h3>ChangeSet</h3>
        <table>
          <thead><tr><th>id</th><th>目标</th><th>标题</th><th>invariant</th><th>applied</th><th></th></tr></thead>
          <tbody>${state.changesets.map((c) => `<tr>
            <td class="mono">${esc(c.id)}</td>
            <td>${esc(c.target)}</td>
            <td>${esc(c.title)}</td>
            <td><span class="pill ${c.invariant === "pass" ? "ok" : "bad"}">${esc(c.invariant)}</span></td>
            <td>${c.applied ? "true" : "false"}</td>
            <td>
              <button class="btn primary" data-dec="confirm" data-cs="${esc(c.id)}" ${c.status !== "pending" || c.invariant !== "pass" ? "disabled" : ""}>确认</button>
              <button class="btn danger" data-dec="reject" data-cs="${esc(c.id)}" ${c.status !== "pending" ? "disabled" : ""}>驳回</button>
            </td>
          </tr>`).join("")}</tbody>
        </table>
        <p class="muted">auto_apply 开关已从界面移除。未审批不进 compiled（I-09）。</p>
      </div>`;
  }

  function submitChangeset(target, title, invariant) {
    const id = "cs-" + Date.now().toString(36);
    state.changesets.unshift({
      id, target, title, submitted_by: state.role, applied: false, auto_apply: false, status: "pending", invariant,
    });
    toast("已提交 " + id + "，applied=false", "warn");
    location.hash = "#/publish";
  }

  function bindView() {
    $$("[data-proto]").forEach((b) => b.addEventListener("click", () => {
      state.proto = b.dataset.proto;
      render();
    }));
    $$("[data-int]").forEach((r) => r.addEventListener("click", () => {
      state.integration = r.dataset.int;
      render();
    }));
    $$("[data-mod]").forEach((r) => r.addEventListener("click", () => {
      state.module = r.dataset.mod;
      render();
    }));
    $$("[data-pick]").forEach((g) => g.addEventListener("click", () => {
      state.module = g.dataset.pick;
      render();
    }));
    const play = $("#play-i");
    if (play) play.addEventListener("click", () => {
      state.integration = "I-05";
      state.proto = "s";
      state.playing = !state.playing;
      render();
      toast(state.playing ? "scene 写路径被门禁拦住，explain 已给出下一步" : "停止回放");
    });
    const profile = $("#profile");
    if (profile) profile.addEventListener("change", () => { state.profile = profile.value; });
    const op = $("#op");
    if (op) op.addEventListener("change", () => { state.op = op.value; });
    const explain = $("#explain");
    if (explain) explain.addEventListener("click", () => { render(); toast("试运行完成，profile 仍由入口强制"); });
    $$("[data-node]").forEach((g) => g.addEventListener("click", () => {
      state.node = g.dataset.node;
      render();
    }));
    const validate = $("#validate");
    if (validate) validate.addEventListener("click", () => {
      const node = D.graph.nodes.find((n) => n.node_id === state.node);
      const miss = nodeIncomplete(node);
      toast(miss ? "INVARIANT_FAILED · " + miss : "五件套通过", miss ? "bad" : "");
    });
    const pubG = $("#pub-graph");
    if (pubG) pubG.addEventListener("click", () => submitChangeset("release", "责任图切片发布 " + state.node, "pass"));
    const pubL = $("#pub-law");
    if (pubL) pubL.addEventListener("click", () => submitChangeset("law_pack", D.laws.next.version + " 决策链覆盖", "pass"));
    const draft = $("#wm-draft");
    if (draft) draft.addEventListener("input", () => { state.wmDraft = draft.value; });
    const mcp = $("#mcp-profile");
    if (mcp) mcp.addEventListener("change", () => { state.mcpProfile = mcp.value; render(); });
    $$("[data-reg]").forEach((cb) => cb.addEventListener("change", () => {
      state.registryOn[cb.dataset.reg] = cb.checked;
      submitChangeset("permission", (cb.checked ? "启用 " : "停用 ") + cb.dataset.reg, "pass");
    }));
    const rotate = $("#rotate");
    if (rotate) rotate.addEventListener("click", () => toast("密钥已轮换，屏幕仍只显示 kms:// 引用"));
    const aq = $("#audit-q");
    if (aq) aq.addEventListener("change", () => { state.auditQ = aq.value; });
    const ago = $("#audit-go");
    if (ago) ago.addEventListener("click", () => { state.auditQ = $("#audit-q").value; render(); });
    const aex = $("#audit-export");
    if (aex) aex.addEventListener("click", () => toast("合规包已生成（演示）：audit-hengchuan-20260911.json"));
    const retry = $("#retry");
    if (retry) retry.addEventListener("click", () => toast("已从断点续跑。一线仍只见「待你确认」。"));
    $$("[data-dec]").forEach((b) => b.addEventListener("click", () => {
      const cs = state.changesets.find((c) => c.id === b.dataset.cs);
      if (!cs) return;
      if (b.dataset.dec === "confirm") {
        if (cs.invariant !== "pass") {
          toast("invariant 未过，不能进入 compiled", "bad");
          return;
        }
        cs.status = "confirmed";
        cs.applied = true;
        toast(cs.id + " 已确认，下次 compiled 生效");
      } else {
        cs.status = "rejected";
        cs.applied = false;
        toast(cs.id + " 已驳回", "warn");
      }
      render();
    }));
  }

  function route() {
    const hash = (location.hash || "#/overview").replace(/^#\/?/, "");
    const id = hash.split("/")[0] || "overview";
    state.page = D.pages.some((p) => p.id === id) ? id : "overview";
    render();
  }

  $("#role").addEventListener("change", (e) => {
    state.role = e.target.value;
    if (state.role === "frontline") toast("一线账号不能进入 /console", "warn");
    render();
  });
  window.addEventListener("hashchange", route);
  route();
})();
