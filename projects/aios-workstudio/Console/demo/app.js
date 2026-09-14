(() => {
  "use strict";

  const F = window.ConsoleFixtures;
  const STORAGE_KEY = "platform-console-state-v3";

  if (new URLSearchParams(location.search).has("reset")) {
    try { sessionStorage.removeItem(STORAGE_KEY); } catch { /* noop */ }
    history.replaceState(null, "", location.pathname + location.hash);
  }

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  const escapeHtml = (v) => String(v).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;",
  })[c]);

  function loadState() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return F.createInitialState();
      const parsed = JSON.parse(raw);
      const base = F.createInitialState();
      return { ...base, ...parsed, health: { ...base.health, ...parsed.health } };
    } catch {
      return F.createInitialState();
    }
  }

  let state = loadState();

  function saveState() {
    try { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch { /* noop */ }
  }

  function toast(msg, ms = 3200) {
    const stack = $("#toast-stack");
    const el = document.createElement("div");
    el.className = "toast";
    el.textContent = msg;
    stack.appendChild(el);
    setTimeout(() => el.remove(), ms);
  }

  function nextCsId() {
    const id = `cs-${String(state.seq).padStart(4, "0")}`;
    state.seq += 1;
    return id;
  }

  function submitChangeSet(type, summary, payload) {
    const local = () => {
      const cs = {
        id: nextCsId(),
        type,
        summary,
        payload,
        applied: false,
        status: "pending",
        created_at: new Date().toISOString(),
      };
      state.changeSets.unshift(cs);
      saveState();
      toast(`已提交 ChangeSet ${cs.id}（待发布确认，未静默生效）`);
      return cs;
    };
    if (!window.HubOps || state.hub_ops !== "ok") return local();
    window.HubOps.changesetSubmit({ kind: type, summary, payload })
      .then((body) => {
        const cs = {
          id: body.changeset_id,
          type,
          summary,
          payload,
          applied: false,
          status: body.status || "pending",
          created_at: new Date().toISOString(),
          auto_apply: false,
        };
        state.changeSets.unshift(cs);
        saveState();
        toast(`已提交 ChangeSet ${cs.id}（待发布确认，未静默生效）`);
        render();
      })
      .catch(() => {
        toast("治理服务提交失败，已降级本地 pending");
        local();
        render();
      });
    return null;
  }

  function isFrontlineLocked() {
    return state.role === "frontline";
  }

  function frontlineLockCopy() {
    return "一线账号看不到 /console";
  }

  function highlightPlanes(page) {
    const govPages = ["govern", "publish", "audit", "dualtrack", "memory", "evolution"];
    const opsPages = ["ontology", "mesh", "run", "automation", "caliber", "workflows", "wm", "control", "integrate"];
    const gov = $("#nav-gov");
    const ops = $("#nav-ops");
    if (gov) gov.classList.toggle("is-on", govPages.includes(page));
    if (ops) ops.classList.toggle("is-on", opsPages.includes(page));
  }

  function isDriftFail() {
    const st = state.schema_drift && state.schema_drift.status;
    return st === "fail" || st === "drift";
  }

  function validateAccountability() {
    const nodes = F.ACCOUNTABILITY_NODES;
    const results = nodes.map((node) => {
      const wm = node.wm;
      const missing = Object.entries(wm).filter(([, ok]) => !ok).map(([k]) => k);
      const caliberOk = node.caliber != null && node.caliber !== "";
      const complete = missing.length === 0 && caliberOk;
      let codes = [];
      if (missing.length) codes.push("WM_INCOMPLETE");
      if (!caliberOk) codes.push("INVARIANT_FAILED");
      return { node, missing, caliberOk, complete, codes };
    });
    const allOk = results.every((r) => r.complete);
    return { results, allOk };
  }

  function pendingChangeSets() {
    return state.changeSets.filter((c) => c.status === "pending");
  }

  function currentPage() {
    const hash = location.hash.replace(/^#\/?/, "") || "overview";
    return F.PAGES.some((p) => p.id === hash) ? hash : "overview";
  }

  function setHash(page) {
    const next = `#/${page}`;
    if (location.hash !== next) location.hash = next;
    else render();
  }

  function renderBanStrip() {
    const el = $("#ban-strip");
    const bans = F.GOVERNANCE.bans;
    el.hidden = false;
    $("#shell").classList.add("has-ban");
    el.innerHTML = `
      <span class="label">永久禁令</span>
      ${bans.map((b) => `<button type="button" class="ban-btn" data-ban="${escapeHtml(b.id)}" title="${escapeHtml(b.reason)}">${escapeHtml(b.label)}</button>`).join("")}
      <span style="color:var(--muted);margin-left:auto;font-size:11px;">auto_apply = OFF · 审计不可关闭</span>
    `;
    $$(".ban-btn", el).forEach((btn) => {
      btn.addEventListener("click", () => {
        const ban = bans.find((b) => b.id === btn.dataset.ban);
        toast(ban ? ban.reason : "该操作永久禁止");
      });
    });
  }

  function renderRail(page) {
    const nav = $("#rail-nav");
    const groups = F.PAGE_GROUPS || [{ group: null, pages: F.PAGES }];
    nav.innerHTML = groups.map((g) => `
      ${g.group ? `<p class="rail-group">${escapeHtml(g.group)}</p>` : ""}
      ${g.pages.map((p) => `
        <button type="button" data-page="${p.id}" class="${p.id === page ? "is-on" : ""}">
          ${escapeHtml(p.label)}
          <small>${escapeHtml(p.hint)}</small>
        </button>
      `).join("")}
    `).join("");
    $$("button[data-page]", nav).forEach((btn) => {
      btn.addEventListener("click", () => setHash(btn.dataset.page));
    });
  }

  function renderRoleSelect() {
    const opts = F.ROLES.map((r) => `<option value="${r.id}" ${r.id === state.role ? "selected" : ""}>${escapeHtml(r.label)}</option>`).join("");
    const sel = $("#role-select");
    sel.innerHTML = opts;
    window.CONSOLE_OPS_ROLE = state.role;
    sel.onchange = () => {
      state.role = sel.value;
      window.CONSOLE_OPS_ROLE = state.role;
      saveState();
      render();
    };
    const lockSel = $("#lock-role-select");
    if (lockSel) {
      lockSel.innerHTML = opts;
      lockSel.onchange = () => {
        state.role = lockSel.value;
        window.CONSOLE_OPS_ROLE = state.role;
        saveState();
        render();
      };
    }
  }

  function metricClass(key, val) {
    if (key === "ungrounded_rate" && val > 0.05) return "bad";
    if (key === "gate_p95_ms" && val > 200) return "warn";
    if (key === "approval_stuck" && val > 0) return "warn";
    if (key === "stale" && val > 0) return "warn";
    return "ok";
  }

  const DIM_ZH = { space: "空间", time: "时间", subject: "主体", object: "客体", feedback: "反馈" };
  const EDGE_ZH = {
    org_cascade: "组织级联",
    kpi_split: "指标拆解",
    stage_split: "阶段拆解",
    object_drill: "对象下钻",
  };

  function pageHead(id) {
    const p = (F.PAGES || []).find((x) => x.id === id) || { label: id, intro: "" };
    const offline = [].includes(id);
    return `
      <div class="page-head">
        <h1>${escapeHtml(p.label)}</h1>
        ${p.intro ? `<p>${escapeHtml(p.intro)}</p>` : ""}
        <div class="page-chips">
          ${p.loop ? `<span class="page-chip">闭环 · ${escapeHtml(p.loop)}</span>` : ""}
          ${p.object ? `<span class="page-chip">对象 · ${escapeHtml(p.object)}</span>` : ""}
          ${offline ? '<span class="page-chip">本战役离线</span>' : ""}
        </div>
      </div>`;
  }

  function renderOverview() {
    const h = state.health;
    const drift = state.schema_drift;
    const pending = pendingChangeSets().length;
    const metrics = [
      { k: "工作台打开", key: "open_ms", v: h.open_ms, fmt: (v) => `${v} ms`, hint: "一线打开看板" },
      { k: "门禁可解释", key: "explain", v: h.explain, fmt: (v) => `${(v * 100).toFixed(0)}%`, hint: "人话覆盖" },
      { k: "未接地建议", key: "ungrounded_rate", v: h.ungrounded_rate, fmt: (v) => `${(v * 100).toFixed(1)}%`, hint: "不得派活" },
      { k: "门禁耗时", key: "gate_p95_ms", v: h.gate_p95_ms, fmt: (v) => `${v} ms`, hint: "确认前等待" },
      { k: "审批滞留", key: "approval_stuck", v: h.approval_stuck, fmt: (v) => String(v), hint: "策略行动卡住" },
      { k: "口径过期", key: "stale", v: h.stale, fmt: (v) => String(v), hint: "数据环节" },
    ];
    const loop = (F.VALUE_LOOP || []).map((s) => `
      <div class="loop-step">
        <b>${escapeHtml(s.label)}</b>
        <p>使用：${escapeHtml(s.use)}</p>
        <p>治理/运维：${escapeHtml(s.ops)}</p>
      </div>`).join("");
    const func = (F.FUNC_OBJECTS || []).map((o) => `
      <div class="obj-card">
        <h3>${escapeHtml(o.name)}</h3>
        <p>${escapeHtml(o.desc)}</p>
        <p class="sub">权威：${escapeHtml(o.store)} · 管理：${escapeHtml(o.manage)} · 闭环：${escapeHtml(o.loop)}</p>
        ${o.page ? `<a href="#/${o.page}">去管理</a>` : "<span class=\"sub\">在 WorkStudio 办</span>"}
      </div>`).join("");
    const data = (F.DATA_OBJECTS || []).map((o) => `
      <div class="obj-card">
        <h3>${escapeHtml(o.name)}</h3>
        <p>${escapeHtml(o.desc)}</p>
        <p class="sub">存处：${escapeHtml(o.store)} · ${escapeHtml(o.not)}</p>
        ${o.page ? `<a href="#/${o.page}">去管理</a>` : ""}
      </div>`).join("");
    return `
      <div class="page-head">
        <h1>总览</h1>
        <p>经营操作系统的管理面：一线在 WorkStudio 走「数据 → 洞察 → 归因 → 预测 → 策略行动 → 效果回收 → 学习沉淀」。这里管对象对不对、谁能改、改了有没有人确认。写配置必须进发布队列，auto_apply 永关。</p>
      </div>
      <div class="loop-strip">${loop}</div>
      <div class="grid-3" style="margin:14px 0">
        <section class="card">
          <h2>使用平面</h2>
          <p class="sub">销售运营 · LTC / 增长管理 / 组合管理</p>
          <p style="font-size:12px;color:var(--muted);margin:0 0 10px">一线只看见并办成。无连接器、无口径公式页。</p>
          <a class="btn primary" href="../../demo/index.html" style="display:inline-block;text-decoration:none">打开 WorkStudio</a>
        </section>
        <section class="card">
          <h2>治理平面</h2>
          <p class="sub">谁能承诺 · 追得回 · 忘得掉</p>
          <p style="font-size:12px;color:var(--muted);margin:0 0 10px">岗位绑定、审计、遗忘回执、法则演化。辅助改动全部进发布队列。</p>
          <a class="btn" href="#/audit">进入治理</a>
        </section>
        <section class="card">
          <h2>运维平面</h2>
          <p class="sub">知识是否正确 · 巡检只产建议</p>
          <p style="font-size:12px;color:var(--muted);margin:0 0 10px">责任图、口径、经营模型、审批滞留。生效必须人工确认。</p>
          <a class="btn" href="#/automation">进入巡检作业</a>
        </section>
      </div>
      <div class="grid-3" style="margin-bottom:14px">
        ${metrics.map((m) => `
          <div class="metric">
            <div class="k">${escapeHtml(m.k)}</div>
            <div class="v ${metricClass(m.key, m.v)}">${escapeHtml(m.fmt(m.v))}</div>
            <div class="k">${escapeHtml(m.hint)}</div>
          </div>
        `).join("")}
      </div>
      <div class="grid-2" style="margin-bottom:14px">
        <section class="card">
          <h2>功能对象</h2>
          <p class="sub">一线和工作台直接操作的能力</p>
          <div class="obj-grid">${func}</div>
        </section>
        <section class="card">
          <h2>数据模型对象</h2>
          <p class="sub">权威存处 · 禁止互冒</p>
          <div class="obj-grid">${data}</div>
        </section>
      </div>
      <div class="grid-2">
        <section class="card">
          <h2>契约一致性</h2>
          <p class="sub">目录 / 门禁 / 发布 三处必须一致</p>
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
            <span class="status-pill ${drift.status === "healthy" ? "ok" : "fail"}">
              <span class="dot"></span>${drift.status === "healthy" ? "一致" : "漂移"} · ${drift.count}
            </span>
            <button type="button" class="btn ghost" data-act="toggle-drift">切换夹具</button>
          </div>
          ${drift.status === "fail" ? '<div class="alert fail">漂移 · 相关变更单发布将被阻断</div>' : '<div class="alert ok">契约一致，可以发布</div>'}
        </section>
        <section class="card">
          <h2>待确认变更单</h2>
          <p class="sub">${pending} 条 pending · <a href="#/publish" style="color:var(--accent)">前往发布确认</a></p>
          ${pending ? pendingChangeSets().slice(0, 3).map((c) => `<div style="font-size:12px;margin:6px 0"><code>${escapeHtml(c.id)}</code> · ${escapeHtml(c.summary)}</div>`).join("") : '<p class="empty">暂无待确认项</p>'}
        </section>
      </div>
      <section class="card" style="margin-top:14px">
        <h2>租户套件 · ${escapeHtml(state.tenant_id)}</h2>
        <p class="sub">切换只生成变更单，不静默生效</p>
        ${renderSuiteRows()}
      </section>
    `;
  }

  function renderSuiteRows() {
    return F.SUITE_DEFS.map((s) => {
      const on = state.suites[s.id];
      return `
        <div class="suite-row">
          <div class="meta">
            <strong>${escapeHtml(s.label)}</strong>
            <small>${escapeHtml(s.desc)}</small>
          </div>
          <label class="inline-check">
            <input type="checkbox" data-suite="${s.id}" ${on ? "checked" : ""} />
            ${on ? "已启用" : "已禁用"}
          </label>
        </div>
      `;
    }).join("");
  }

  function renderIntegrate() {
    const profile = F.PROFILES.find((p) => p.id === state.profile_id) || F.PROFILES[0];
    return `
      ${pageHead("integrate")}
      <div class="grid-2">
        <section class="card">
          <h2>Hub 剖面</h2>
          <div class="field">
            <label>profile</label>
            <select id="profile-select">
              ${F.PROFILES.map((p) => `<option value="${p.id}" ${p.id === state.profile_id ? "selected" : ""}>${escapeHtml(p.label)}</option>`).join("")}
            </select>
          </div>
          <p style="font-size:12px;color:var(--muted)">
            写操作：${profile.forbids_write ? "禁止（403 PROFILE_FORBIDS_SIDE_EFFECT）" : "允许 · 走 L1/L2/L3 + G 层"}
          </p>
          <button type="button" class="btn primary" data-act="dry-run" ${profile.dry_run || profile.id === "builder" ? "" : "disabled"}>
            I-05 · 执行 dry-run
          </button>
        </section>
        <section class="card">
          <h2>dry-run 结果</h2>
          <div id="dry-run-result" class="empty">尚未执行 dry-run</div>
        </section>
      </div>
    `;
  }

  function renderControl() {
    return `
      ${pageHead("control")}
      <div class="grid-2">
        <section class="card">
          <h2>租户套件</h2>
          <p class="sub">US-B-03 · ${escapeHtml(state.tenant_id)}</p>
          ${renderSuiteRows()}
        </section>
        <section class="card">
          <h2>治理开关（只读）</h2>
          <div class="suite-row">
            <div class="meta"><strong>审计链 audit_enabled</strong><small>永久开启 · 不可关闭</small></div>
            <span class="status-pill ok"><span class="dot"></span>ON</span>
          </div>
          <div class="suite-row">
            <div class="meta"><strong>auto_apply</strong><small>ChangeSet 必须人工确认</small></div>
            <span class="status-pill fail"><span class="dot"></span>OFF</span>
          </div>
          <p style="font-size:12px;color:var(--muted);margin-top:10px">点击顶栏禁令按钮会提示永久禁止原因。</p>
          ${state.role === "sre" ? `
            <div class="field" style="margin-top:14px">
              <label class="inline-check">
                <input type="checkbox" id="sre-escape" ${state.sre_escape ? "checked" : ""} />
                零件逃生（SRE 专用 · 默认 OFF）
              </label>
            </div>
            ${state.sre_escape ? `
              <div class="escape-panel">
                ${F.ESCAPE_LINKS.map((l) => `<a href="${l.href}" data-escape="${l.id}">${escapeHtml(l.label)}</a>`).join("")}
              </div>
            ` : ""}
          ` : ""}
        </section>
      </div>
    `;
  }

  function renderOntology() {
    const validation = validateAccountability();
    const proj = state.ontology_projections;
    const activeEdges = Object.entries(proj)
      .filter(([, on]) => on)
      .flatMap(([kind]) => F.ONTOLOGY_EDGES[kind].map((e) => ({ ...e, kind })));

    return `
      ${pageHead("ontology")}
      ${validation.allOk
        ? '<div class="alert ok">五件套通过 · 全部责任节点 空间/时间/主体/客体/反馈 + 口径齐全</div>'
        : `<div class="alert fail">校验失败 · ${validation.results.filter((r) => !r.complete).map((r) => `${r.node.id}: ${r.codes.join(", ")}`).join(" · ")}</div>`}
      <div class="graph-wrap">
        <section class="card">
          <h2>责任节点</h2>
          <div class="node-list">
            ${validation.results.map(({ node, missing, caliberOk, complete, codes }) => `
              <div class="node-card ${complete ? "complete" : "incomplete"}">
                <strong>${escapeHtml(node.label)}</strong>
                <div style="font-size:11px;color:var(--muted)">${escapeHtml(node.id)} · ${escapeHtml(node.owner)}</div>
                <div style="font-size:11px;margin-top:4px">口径: ${caliberOk ? escapeHtml(node.caliber) : "<span style='color:var(--red)'>缺失</span>"}</div>
                <div class="dims">
                  ${Object.entries(node.wm).map(([d, ok]) => `<span class="dim-tag ${ok ? "on" : "off"}">${escapeHtml(DIM_ZH[d] || d)}</span>`).join("")}
                </div>
                ${!complete ? `<div style="font-size:11px;color:var(--red);margin-top:6px">${escapeHtml(codes.join(" · "))}</div>` : ""}
              </div>
            `).join("")}
          </div>
          <button type="button" class="btn" data-act="validate-wm" style="margin-top:12px">重新校验五件套</button>
        </section>
        <section class="card">
          <h2>责任拆解边</h2>
          <p class="sub">切换后只改投影，不改权威图</p>
          ${Object.keys(proj).map((kind) => `
            <label class="inline-check" style="margin-bottom:6px">
              <input type="checkbox" data-projection="${kind}" ${proj[kind] ? "checked" : ""} />
              ${escapeHtml(EDGE_ZH[kind] || kind)}
            </label>
          `).join("")}
          <div class="edge-panel" style="margin-top:10px">
            ${activeEdges.length
              ? activeEdges.map((e) => `<div class="edge-line">${escapeHtml(e.from)} → ${escapeHtml(e.to)} <span style="color:var(--accent)">[${escapeHtml(EDGE_ZH[e.kind] || e.kind)}]</span></div>`).join("")
              : '<div class="empty">未选择拆解边</div>'}
          </div>
        </section>
      </div>
    `;
  }

  function renderMesh() {
    const filteredMcp = F.MCP_TOOLS.filter((t) => {
      if (state.mcp_scene !== "all" && t.scene !== state.mcp_scene) return false;
      if (state.mcp_hide_write && t.write) return false;
      return true;
    });

    return `
      ${pageHead("mesh")}
      <section class="card" style="margin-bottom:14px">
        <h2>能力注册 · approval_level</h2>
        <p class="sub">US-B-07 · 启用与 L1/L2/L3 变更均提交 ChangeSet</p>
        <table class="data">
          <thead><tr><th>操作</th><th>启用</th><th>approval_level</th></tr></thead>
          <tbody>
            ${state.capabilities.map((c, i) => `
              <tr>
                <td><code>${escapeHtml(c.id)}</code></td>
                <td><input type="checkbox" data-cap-idx="${i}" data-cap-field="enabled" ${c.enabled ? "checked" : ""} /></td>
                <td>
                  <select data-cap-idx="${i}" data-cap-field="approval_level">
                    ${["L1", "L2", "L3"].map((l) => `<option ${c.approval_level === l ? "selected" : ""}>${l}</option>`).join("")}
                  </select>
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </section>
      <div class="grid-2">
        <section class="card">
          <h2>连接器槽位</h2>
          <p class="sub">US-B-09 · sandbox ↔ prod · 密钥不出明文</p>
          <table class="data">
            <thead><tr><th>连接器</th><th>槽位</th><th>状态</th><th></th></tr></thead>
            <tbody>
              ${state.connectors.map((c, i) => `
                <tr>
                  <td>${escapeHtml(c.label)}<br><code>${escapeHtml(c.id)}</code></td>
                  <td>
                    <select data-conn-idx="${i}" data-conn-field="slot">
                      <option ${c.slot === "sandbox" ? "selected" : ""}>sandbox</option>
                      <option ${c.slot === "prod" ? "selected" : ""}>prod</option>
                    </select>
                  </td>
                  <td>${escapeHtml(c.status)}</td>
                  <td><button type="button" class="btn ghost" data-act="rotate" data-conn-idx="${i}">轮换密钥</button></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
          <p style="font-size:11px;color:var(--muted);margin-top:8px">secret_ref 仅显示 vault 指针，不展示明文。</p>
        </section>
        <section class="card">
          <h2>MCP 工具</h2>
          <div class="field">
            <label>scene 过滤</label>
            <select id="mcp-scene">
              <option value="all" ${state.mcp_scene === "all" ? "selected" : ""}>全部</option>
              ${[...new Set(F.MCP_TOOLS.map((t) => t.scene))].map((s) => `<option value="${s}" ${state.mcp_scene === s ? "selected" : ""}>${s}</option>`).join("")}
            </select>
          </div>
          <label class="inline-check" style="margin-bottom:10px">
            <input type="checkbox" id="mcp-hide-write" ${state.mcp_hide_write ? "checked" : ""} />
            scene-hides-write（隐藏 write 工具）
          </label>
          <table class="data">
            <thead><tr><th>工具</th><th>scene</th><th>write</th></tr></thead>
            <tbody>
              ${filteredMcp.length
                ? filteredMcp.map((t) => `<tr><td>${escapeHtml(t.name)}</td><td>${escapeHtml(t.scene)}</td><td>${t.write ? "是" : "否"}</td></tr>`).join("")
                : '<tr><td colspan="3" class="empty">无匹配工具</td></tr>'}
            </tbody>
          </table>
        </section>
      </div>
    `;
  }

  function renderGovern() {
    const lp = F.LAW_PACKS;
    return `
      ${pageHead("govern")}
      <div class="grid-2">
        <section class="card">
          <h2>经营法则包</h2>
          <p class="sub">现行与候选必须显式声明冲突</p>
          <div class="suite-row">
            <div class="meta"><strong>现行</strong><small>${escapeHtml(lp.current.label)}</small></div>
            <code>${escapeHtml(lp.current.version)}</code>
          </div>
          <div class="suite-row">
            <div class="meta"><strong>候选</strong><small>${escapeHtml(lp.next.label)}</small></div>
            <code>${escapeHtml(lp.next.version)}</code>
          </div>
        </section>
        <section class="card">
          <h2>版本冲突</h2>
          <table class="data">
            <thead><tr><th>规则</th><th>现行</th><th>候选</th><th>严重度</th></tr></thead>
            <tbody>
              ${lp.conflicts.map((c) => `
                <tr>
                  <td><code>${escapeHtml(c.rule)}</code></td>
                  <td>${escapeHtml(c.current)}</td>
                  <td>${escapeHtml(c.next)}</td>
                  <td><span class="status-pill ${c.severity === "high" ? "fail" : "warn"}">${escapeHtml(c.severity)}</span></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
      </div>
    `;
  }

  function renderRun() {
    const kg = state.kg_ingest;
    return `
      ${pageHead("run")}
      <div class="grid-2">
        <section class="card">
          <h2>模型路由</h2>
          <p class="sub">US-B-18 · 变更提交 ChangeSet 至发布队列</p>
          <table class="data">
            <thead><tr><th>路由</th><th>模型</th><th>rpm</th><th>槽位</th></tr></thead>
            <tbody>
              ${state.models.map((m, i) => `
                <tr>
                  <td>${escapeHtml(m.label)}<br><code>${escapeHtml(m.id)}</code></td>
                  <td><input type="text" data-model-idx="${i}" data-model-field="model" value="${escapeHtml(m.model)}" style="max-width:180px" /></td>
                  <td><input type="number" data-model-idx="${i}" data-model-field="rpm" value="${m.rpm}" min="1" max="999" style="max-width:80px" /></td>
                  <td>${escapeHtml(m.slot)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
        <section class="card">
          <h2>经营事实同步</h2>
          <p class="sub">只读 · 滞后时长 + 最近一条 + 失败清单</p>
          <div style="display:flex;gap:12px;align-items:center;margin-bottom:10px">
            <span class="status-pill ${kg.status === "ok" ? "ok" : "warn"}"><span class="dot"></span>${kg.status === "ok" ? "跟上" : "滞后"}</span>
            <span style="font-size:12px;color:var(--muted)">滞后 ${kg.lag_minutes} 分钟</span>
          </div>
          <p style="font-size:12px">最近一条：${escapeHtml(kg.last_episode)}</p>
          <h3 style="font-size:13px;margin:14px 0 8px">同步失败</h3>
          <table class="data">
            <thead><tr><th>事实</th><th>原因</th><th>时间</th></tr></thead>
            <tbody>
              ${kg.failures.map((f) => `
                <tr>
                  <td><code>${escapeHtml(f.episode)}</code></td>
                  <td>${escapeHtml(f.reason)}</td>
                  <td>${escapeHtml(f.at)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
      </div>
    `;
  }

  function renderPublish() {
    const drift = state.schema_drift;
    const list = state.changeSets;
    return `
      ${pageHead("publish")}
      ${isDriftFail() ? '<div class="alert fail">契约不一致 · 相关发布确认已阻断，请先修复或切换「一致」夹具</div>' : ""}
      <section class="card">
        <h2>变更单队列</h2>
        ${list.length ? `<div class="changeset-list">${list.map((c) => renderChangeSetItem(c)).join("")}</div>` : '<p class="empty">暂无变更单</p>'}
      </section>
    `;
  }

  function renderChangeSetItem(c) {
    const blocked = isDriftFail() && c.status === "pending" && (
      c.type.includes("schema") || c.type.includes("capability") || c.type.includes("connector") || c.type.includes("model")
    );
    return `
      <div class="changeset-item ${c.status}">
        <div class="meta">
          <code>${escapeHtml(c.id)}</code>
          <span>${escapeHtml(c.type)}</span>
          <span>${escapeHtml(c.status)}</span>
          ${c.applied ? "<span>applied</span>" : "<span>applied=false</span>"}
        </div>
        <div>${escapeHtml(c.summary)}</div>
        ${c.status === "pending" ? `
          <div class="actions">
            <button type="button" class="btn primary" data-act="cs-confirm" data-cs-id="${escapeHtml(c.id)}" ${blocked ? "disabled title='Schema drift fail 阻断'" : ""}>确认发布</button>
            <button type="button" class="btn danger" data-act="cs-reject" data-cs-id="${escapeHtml(c.id)}">驳回</button>
          </div>
          ${blocked ? '<div class="alert warn" style="margin-top:8px">因 schema drift=fail，此 ChangeSet 暂不可确认</div>' : ""}
        ` : ""}
      </div>
    `;
  }

  /* ===== 治理平面新增页（UAS_AIOS_CONSOLE_DEMO_DESIGN §5） ===== */

  function sevPill(sev) {
    const cls = sev === "high" ? "fail" : sev === "medium" ? "warn" : "ok";
    return `<span class="status-pill ${cls}">${escapeHtml(sev)}</span>`;
  }

  function renderAudit() {
    const f = state.audit_filter;
    const events = state.audit_events.filter((e) => {
      if (f.actor !== "all" && e.actor !== f.actor) return false;
      if (f.type !== "all" && !e.type.startsWith(f.type)) return false;
      if (f.result !== "all" && e.result !== f.result) return false;
      return true;
    });
    const actors = [...new Set(state.audit_events.map((e) => e.actor))];
    return `
      ${pageHead("audit")}
      <section class="card" style="margin-bottom:14px">
        <h2>AU-01 · 异常模式巡检</h2>
        <p class="sub">自动化作业产出发现 · 处置需人工确认</p>
        <table class="data">
          <thead><tr><th>模式</th><th>actor</th><th>次数</th><th>严重度</th><th></th></tr></thead>
          <tbody>
            ${F.AUDIT_PATTERNS.map((p) => `
              <tr>
                <td>${escapeHtml(p.label)}</td>
                <td><code>${escapeHtml(p.actor)}</code></td>
                <td>${p.count}</td>
                <td>${sevPill(p.severity)}</td>
                <td><button type="button" class="btn ghost" data-act="pattern-ticket" data-pat="${p.id}">生成处置单</button></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </section>
      <section class="card">
        <h2>事件检索</h2>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;align-items:flex-end">
          <div class="field"><label>actor</label>
            <select id="af-actor"><option value="all">全部</option>${actors.map((a) => `<option value="${escapeHtml(a)}" ${f.actor === a ? "selected" : ""}>${escapeHtml(a)}</option>`).join("")}</select>
          </div>
          <div class="field"><label>类型</label>
            <select id="af-type">
              <option value="all" ${f.type === "all" ? "selected" : ""}>全部</option>
              <option value="hub." ${f.type === "hub." ? "selected" : ""}>hub.*</option>
              <option value="ops." ${f.type === "ops." ? "selected" : ""}>ops.*</option>
            </select>
          </div>
          <div class="field"><label>结果</label>
            <select id="af-result">
              ${["all", "ok", "fail", "deny"].map((r) => `<option value="${r}" ${f.result === r ? "selected" : ""}>${r}</option>`).join("")}
            </select>
          </div>
          <button type="button" class="btn" data-act="audit-export">导出（自审）</button>
        </div>
        <table class="data">
          <thead><tr><th>时间</th><th>actor</th><th>类型</th><th>对象</th><th>结果</th><th>hash</th></tr></thead>
          <tbody>
            ${events.map((e) => `
              <tr>
                <td style="font-size:11px">${escapeHtml(e.ts)}</td>
                <td><code>${escapeHtml(e.actor)}</code></td>
                <td><code>${escapeHtml(e.type)}</code></td>
                <td><code>${escapeHtml(e.object)}</code></td>
                <td><span class="status-pill ${e.result === "ok" ? "ok" : e.result === "deny" ? "warn" : "fail"}">${e.result}${e.error_code ? ` · ${escapeHtml(e.error_code)}` : ""}</span></td>
                <td style="font-size:11px;color:var(--muted)">${escapeHtml(e.hash)}</td>
              </tr>
            `).join("") || '<tr><td colspan="6" class="empty">无匹配事件</td></tr>'}
          </tbody>
        </table>
      </section>
    `;
  }

  function renderDualtrack() {
    const scan = state.automation_jobs.find((j) => j.id === "dual_track_scan");
    const personPool = ["rao.w", "chen.y", "li.m", "wang.q"];
    return `
      ${pageHead("dualtrack")}
      <div class="grid-2">
        <section class="card">
          <h2>岗位绑定 · hub.ops.iam.bindings</h2>
          <p class="sub">改派提交 ChangeSet · iam.binding</p>
          <table class="data">
            <thead><tr><th>人员</th><th>角色</th><th>责任节点</th><th>轨</th><th>改派</th></tr></thead>
            <tbody>
              ${state.iam_bindings.map((b, i) => `
                <tr>
                  <td><code>${escapeHtml(b.person)}</code></td>
                  <td>${escapeHtml(b.role)}</td>
                  <td><code>${escapeHtml(b.node_id)}</code></td>
                  <td><span class="status-pill ${b.track === "ΠPaw" ? "warn" : "ok"}">${escapeHtml(b.track)}</span></td>
                  <td>
                    <select data-bind-idx="${i}">
                      <option value="">改派…</option>
                      ${personPool.filter((p) => p !== b.person).map((p) => `<option value="${p}">${p}</option>`).join("")}
                    </select>
                  </td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
        <section class="card">
          <h2>升级请求 · SelfPaw → ΠPaw</h2>
          <p class="sub">升级必须携带证据 · 无证据项禁止通过</p>
          <div class="changeset-list">
            ${state.upgrade_requests.map((r) => `
              <div class="changeset-item ${r.status}">
                <div class="meta"><code>${r.id}</code><span>${escapeHtml(r.from_track)} → ΠPaw</span><span>${r.status}</span></div>
                <div>${escapeHtml(r.summary)}</div>
                <div style="font-size:11px;color:var(--muted)">memory: <code>${r.memory_ref}</code> · 证据: ${r.evidence_ref ? `<code>${r.evidence_ref}</code>` : '<span style="color:var(--red)">缺失</span>'}</div>
                ${r.status === "pending" ? `
                  <div class="actions">
                    <button type="button" class="btn primary" data-act="ur-approve" data-ur="${r.id}" ${r.evidence_ref ? "" : "disabled title='TRACK_ESCALATION_REQUIRED · 升级必须带证据'"}>通过</button>
                    <button type="button" class="btn danger" data-act="ur-reject" data-ur="${r.id}">驳回</button>
                  </div>
                ` : ""}
              </div>
            `).join("")}
          </div>
        </section>
      </div>
      <section class="card" style="margin-top:14px">
        <h2>AU-02 · 双轨未升级扫描</h2>
        <p class="sub">最近运行 ${escapeHtml(scan.last_run)} · schedule ${escapeHtml(scan.schedule)}</p>
        ${scan.findings.map((fd) => `<div style="margin:6px 0">${sevPill(fd.sev)} <span style="font-size:12px">${escapeHtml(fd.summary)}</span></div>`).join("")}
      </section>
    `;
  }

  function renderMemory() {
    const pending = state.forget_requests.filter((r) => r.status === "pending");
    return `
      ${pageHead("memory")}
      <div class="grid-3" style="margin-bottom:14px">
        ${F.MEMORY_DOMAINS.map((d) => `
          <div class="metric"><div class="k">${escapeHtml(d.label)} · ${escapeHtml(d.id)}</div>
          <div class="v ok">${d.count}</div>
          <div style="font-size:11px;color:var(--muted)">${escapeHtml(d.decay)}</div></div>
        `).join("")}
      </div>
      <div class="grid-2">
        <section class="card">
          <h2>遗忘申请 · CR-08</h2>
          <p class="sub">AU-10 离职批量作业汇入 · 执行需二次确认</p>
          ${pending.length ? pending.map((r) => `
            <div class="changeset-item pending">
              <div class="meta"><code>${r.id}</code><span>${escapeHtml(r.kind)}</span><span>${r.status}</span></div>
              <div>${escapeHtml(r.subject)}</div>
              <div style="font-size:11px;color:var(--muted)">范围：${escapeHtml(r.scope)}</div>
              <div class="actions">
                <button type="button" class="btn primary" data-act="forget-exec" data-fr="${r.id}">执行遗忘（生成回执）</button>
                <button type="button" class="btn danger" data-act="forget-cancel" data-fr="${r.id}">撤销申请</button>
              </div>
            </div>
          `).join("") : '<p class="empty">无待处置申请</p>'}
        </section>
        <section class="card">
          <h2>回执登记簿 · 可检索</h2>
          <div class="field"><label>检索 subject</label><input type="text" id="receipt-q" placeholder="输入关键字过滤" /></div>
          <table class="data">
            <thead><tr><th>回执</th><th>对象</th><th>擦除数</th><th>时间</th><th>审计指针</th></tr></thead>
            <tbody id="receipt-rows">
              ${state.forget_receipts.map((r) => `
                <tr data-subject="${escapeHtml(r.subject)}">
                  <td><code>${r.id}</code></td><td>${escapeHtml(r.subject)}</td><td>${r.erased}</td>
                  <td style="font-size:11px">${r.at}</td><td><code>${r.audit_ptr}</code></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
      </div>
    `;
  }

  function renderEvolution() {
    const d = F.EVO_DRAFT;
    const cases = state.evo_cases;
    const anyFail = cases.some((c) => c.result === "fail");
    return `
      ${pageHead("evolution")}
      <div class="alert warn" style="margin-bottom:14px">受控演化：不存在自动应用入口；回归未通过时发布禁用。auto_apply 永久 OFF。</div>
      <div class="grid-2">
        <section class="card">
          <h2>AU-08 · 演化信号聚合</h2>
          <table class="data">
            <thead><tr><th>信号</th><th>来源</th><th>数量</th><th>已聚合</th></tr></thead>
            <tbody>
              ${F.EVO_SIGNALS.map((s) => `
                <tr><td><code>${s.kind}</code></td><td>${escapeHtml(s.source)}</td><td>${s.count}</td><td>${s.aggregated ? "✔" : "—"}</td></tr>
              `).join("")}
            </tbody>
          </table>
        </section>
        <section class="card">
          <h2>回归 CASE</h2>
          <p class="sub">夹具可切换 · fail 时阻断发布</p>
          <table class="data">
            <thead><tr><th>CASE</th><th>结果</th></tr></thead>
            <tbody>
              ${cases.map((c) => `
                <tr><td>${escapeHtml(c.name)}</td><td><span class="status-pill ${c.result === "pass" ? "ok" : "fail"}">${c.result}</span></td></tr>
              `).join("")}
            </tbody>
          </table>
          <button type="button" class="btn ghost" data-act="toggle-cases" style="margin-top:10px">切换回归夹具（全 pass）</button>
        </section>
      </div>
      <section class="card" style="margin-top:14px">
        <h2>草案 · ${escapeHtml(d.pack)}</h2>
        <p class="sub">${escapeHtml(d.base)} → ${escapeHtml(d.target)} · 提交人 <code>${escapeHtml(d.submitted_by)}</code></p>
        <table class="data">
          <thead><tr><th>规则</th><th>现行</th><th>候选</th></tr></thead>
          <tbody>
            ${d.diff.map((x) => `<tr><td><code>${escapeHtml(x.rule)}</code></td><td>${escapeHtml(x.from)}</td><td>${escapeHtml(x.to)}</td></tr>`).join("")}
          </tbody>
        </table>
        <div class="actions" style="margin-top:12px">
          <button type="button" class="btn primary" data-act="evo-promote" ${anyFail ? "disabled title='REGRESSION_NOT_PASSED · 回归未通过'" : ""}>生成 ChangeSet（lawpack.promote）</button>
          ${anyFail ? '<span class="status-pill fail">REGRESSION_NOT_PASSED</span>' : '<span class="status-pill ok">回归通过</span>'}
        </div>
      </section>
    `;
  }

  /* ===== 运维平面新增页（UAS_AIOS_CONSOLE_DEMO_DESIGN §5） ===== */

  function findingActionHtml(j, fd, fi) {
    const base = `data-job="${j.id}" data-fi="${fi}"`;
    switch (fd.action) {
      case "changeset": return `<button type="button" class="btn" data-act="finding-cs" ${base}>转变更单</button>`;
      case "ticket": return `<button type="button" class="btn ghost" data-act="finding-ticket" ${base}>生成处置单</button>`;
      case "signal": return `<button type="button" class="btn ghost" data-act="finding-signal" ${base}>催办</button>`;
      case "review": return `<a class="btn ghost" href="#/dualtrack">前往双轨评审</a>`;
      case "task": return `<button type="button" class="btn ghost" data-act="finding-task" ${base}>转修复任务</button>`;
      default: return `<button type="button" class="btn ghost" data-act="finding-notify" ${base}>通知值班</button>`;
    }
  }

  function renderAutomation() {
    const jobs = state.automation_jobs;
    const totalFindings = jobs.reduce((n, j) => n + j.findings.length, 0);
    return `
      ${pageHead("automation")}
      <div class="alert warn" style="margin-bottom:14px">原则：巡检发现 → 人工确认 → 变更单 / 处置单 → 审计。本页任何按钮都不直接改生产。</div>
      <div class="grid-3" style="margin-bottom:14px">
        <div class="metric"><div class="k">作业数</div><div class="v ok">${jobs.length}</div></div>
        <div class="metric"><div class="k">待处置建议</div><div class="v ${totalFindings > 5 ? "warn" : "ok"}">${totalFindings}</div></div>
        <div class="metric"><div class="k">auto_apply</div><div class="v bad">OFF</div></div>
      </div>
      <section class="card">
        <h2>自动化作业</h2>
        <table class="data">
          <thead><tr><th>作业</th><th>对象</th><th>周期</th><th>最近运行</th><th>状态</th><th>建议</th><th></th></tr></thead>
          <tbody>
            ${jobs.map((j) => `
              <tr>
                <td>${escapeHtml(j.name)}<br><code>${escapeHtml(j.id)}</code></td>
                <td><code>${escapeHtml(j.module)}</code></td>
                <td style="font-size:11px">${escapeHtml(j.schedule)}</td>
                <td style="font-size:11px">${escapeHtml(j.last_run)}</td>
                <td><span class="status-pill ${j.status === "ok" ? "ok" : j.status === "fail" ? "fail" : "warn"}"><span class="dot"></span>${j.status}</span></td>
                <td>${j.findings.length}</td>
                <td><button type="button" class="btn ghost" data-act="run-job" data-job="${j.id}">立即运行</button></td>
              </tr>
              ${j.findings.length ? `<tr><td colspan="7" style="background:rgba(255,255,255,.02)">
                ${j.findings.map((fd, fi) => `
                  <div style="display:flex;align-items:center;gap:10px;padding:5px 0;border-bottom:1px dashed rgba(255,255,255,.06)">
                    ${sevPill(fd.sev)}
                    <span style="font-size:12px;flex:1">${escapeHtml(fd.summary)}</span>
                    ${findingActionHtml(j, fd, fi)}
                  </div>
                `).join("")}
              </td></tr>` : ""}
            `).join("")}
          </tbody>
        </table>
      </section>
    `;
  }

  function renderCaliber() {
    const stale = state.calibers.filter((c) => c.status === "stale");
    return `
      ${pageHead("caliber")}
      ${stale.length ? `<div class="alert warn" style="margin-bottom:14px">过期巡检：${stale.map((c) => `<code>${c.key}</code>`).join("、")} 超窗未回填</div>` : '<div class="alert ok" style="margin-bottom:14px">口径全部新鲜</div>'}
      <section class="card" style="margin-bottom:14px">
        <h2>口径目录</h2>
        <table class="data">
          <thead><tr><th>口径</th><th>负责人</th><th>寿命</th><th>状态</th><th>刷新窗</th><th>最近回填</th><th>计算公式</th><th>操作</th></tr></thead>
          <tbody>
            ${state.calibers.map((c, i) => `
              <tr>
                <td><code>${escapeHtml(c.key)}</code></td>
                <td>${escapeHtml(c.owner)}</td>
                <td>${c.lifecycle === "live" ? "现行" : "草稿"}</td>
                <td><span class="status-pill ${c.status === "fresh" ? "ok" : c.status === "stale" ? "fail" : "warn"}">${c.status === "fresh" ? "新鲜" : c.status === "stale" ? "过期" : "应有"}</span></td>
                <td>${escapeHtml(c.window)}</td>
                <td style="font-size:11px">${escapeHtml(c.last_refresh)}</td>
                <td><code style="font-size:11px">${escapeHtml(c.expr)}</code></td>
                <td>
                  ${c.status === "stale" ? `<button type="button" class="btn" data-act="cal-rerun" data-key="${escapeHtml(c.key)}">重跑</button>` : ""}
                  ${c.lifecycle === "live" ? `<button type="button" class="btn ghost" data-act="cal-edit-live" data-key="${escapeHtml(c.key)}">编辑</button>` : `<button type="button" class="btn ghost" data-act="cal-edit-draft" data-key="${escapeHtml(c.key)}" data-idx="${i}">编辑草稿</button>`}
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </section>
      <section class="card" id="caliber-editor" hidden>
        <h2>草稿编辑 · CR-06</h2>
        <p class="sub" id="caliber-editor-title">—</p>
        <div class="field"><label>计算公式</label><input type="text" id="caliber-expr" style="width:100%;max-width:420px" /></div>
        <button type="button" class="btn primary" data-act="cal-publish">提交 ChangeSet（caliber.publish）</button>
      </section>
    `;
  }

  function renderWorkflows() {
    const st = F.INNER_LOOP_STATS;
    return `
      ${pageHead("workflows")}
      <section class="card" style="margin-bottom:14px">
        <h2>审批与长任务</h2>
        <table class="data">
          <thead><tr><th>审批 / 任务</th><th>所属流程</th><th>阶段</th><th>停留</th><th>状态</th><th></th></tr></thead>
          <tbody>
            ${state.workflow_instances.map((w, i) => `
              <tr>
                <td>${escapeHtml(w.title || w.task)}</td>
                <td style="font-size:12px">${escapeHtml(w.task)}</td>
                <td>${escapeHtml(w.step)}</td>
                <td>${w.wait > 0 ? `<span class="status-pill ${w.wait > 60 ? "fail" : "warn"}">${w.wait} 分钟</span>` : "—"}</td>
                <td>${w.status === "waiting" ? "等待确认" : w.status === "running" ? "进行中" : w.status === "succeeded" ? "已完成" : escapeHtml(w.status)}${w.degraded ? ' <span class="status-pill warn">回写失败</span>' : ""}</td>
                <td>${w.wait > 60 ? `<button type="button" class="btn ghost" data-act="wf-signal" data-idx="${i}">催办</button>` : ""}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
        <p style="font-size:11px;color:var(--muted);margin-top:8px">已完成但回写失败：业务已过，效果回收未落账。一线只见「待你确认」。</p>
      </section>
      <section class="card">
        <h2>待你确认 · 卡口统计</h2>
        <p class="sub">一线只看见确认卡片，不看见内部运行编号</p>
        <div class="grid-3">
          <div class="metric"><div class="k">已确认节点</div><div class="v ok">${st.checkpoints}</div></div>
          <div class="metric"><div class="k">待你确认</div><div class="v warn">${st.interrupts}</div></div>
          <div class="metric"><div class="k">今日确认次数</div><div class="v">${st.tokens_today.toLocaleString()}</div></div>
        </div>
      </section>
    `;
  }

  function renderWm() {
    const by = (l) => state.wm_items.filter((w) => w.lifecycle === l);
    const driftJob = state.automation_jobs.find((j) => j.id === "wm_drift_scan");
    return `
      ${pageHead("wm")}
      <div class="grid-3" style="margin-bottom:14px">
        <div class="metric"><div class="k">草稿</div><div class="v">${by("draft").length}</div></div>
        <div class="metric"><div class="k">编译中</div><div class="v warn">${by("compiling").length}</div></div>
        <div class="metric"><div class="k">现行</div><div class="v ok">${by("live").length}</div></div>
      </div>
      <section class="card" style="margin-bottom:14px">
        <h2>经营模型条目</h2>
        <table class="data">
          <thead><tr><th>id</th><th>类型</th><th>寿命</th><th>责任节点</th><th>摘要</th><th>漂移</th><th>操作</th></tr></thead>
          <tbody>
            ${state.wm_items.map((w) => `
              <tr>
                <td><code>${w.id}</code></td>
                <td>${escapeHtml(w.type)}</td>
                <td><span class="status-pill ${w.lifecycle === "live" ? "ok" : w.lifecycle === "compiling" ? "warn" : ""}">${w.lifecycle === "live" ? "现行" : w.lifecycle === "compiling" ? "编译中" : "草稿"}</span></td>
                <td><code>${escapeHtml(w.node_ref)}</code></td>
                <td style="font-size:12px">${escapeHtml(w.summary)}</td>
                <td>${w.conflict ? '<span class="status-pill fail">冲突</span>' : "—"}</td>
                <td>
                  ${w.lifecycle === "draft" ? `<button type="button" class="btn" data-act="wm-compile" data-wm="${w.id}">提交编译</button>` : ""}
                  ${w.lifecycle === "live" ? `<button type="button" class="btn ghost" data-act="wm-edit-live" data-wm="${w.id}">编辑</button>` : ""}
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </section>
      <section class="card">
        <h2>经营模型漂移扫描</h2>
        <p class="sub">最近运行 ${escapeHtml(driftJob.last_run)} · schedule ${escapeHtml(driftJob.schedule)}</p>
        ${driftJob.findings.map((fd) => `<div style="margin:6px 0">${sevPill(fd.sev)} <span style="font-size:12px">${escapeHtml(fd.summary)}</span></div>`).join("")}
      </section>
    `;
  }

  const PAGE_RENDERERS = {
    overview: renderOverview,
    integrate: renderIntegrate,
    control: renderControl,
    ontology: renderOntology,
    mesh: renderMesh,
    govern: renderGovern,
    run: renderRun,
    publish: renderPublish,
    audit: renderAudit,
    dualtrack: renderDualtrack,
    memory: renderMemory,
    evolution: renderEvolution,
    automation: renderAutomation,
    caliber: renderCaliber,
    workflows: renderWorkflows,
    wm: renderWm,
  };

  function bindPageEvents(page) {
    $$("[data-suite]").forEach((cb) => {
      cb.addEventListener("change", () => {
        const id = cb.dataset.suite;
        const next = cb.checked;
        const prev = state.suites[id];
        if (next === prev) return;
        cb.checked = prev;
        submitChangeSet("tenant.suite", `租户套件 ${id}: ${prev ? "启用" : "禁用"} → ${next ? "启用" : "禁用"}`, { tenant: state.tenant_id, suite: id, from: prev, to: next });
      });
    });

    const driftBtn = $("[data-act=toggle-drift]");
    if (driftBtn) {
      driftBtn.addEventListener("click", () => {
        if (state.schema_drift.status === "healthy") {
          state.schema_drift = { status: "fail", count: 3 };
          toast("已切换 schema drift → fail（红灯）");
        } else {
          state.schema_drift = { status: "healthy", count: 0 };
          toast("已切换 schema drift → healthy");
        }
        saveState();
        render();
      });
    }

    const profileSel = $("#profile-select");
    if (profileSel) {
      profileSel.addEventListener("change", () => {
        state.profile_id = profileSel.value;
        saveState();
        render();
      });
    }

    const dryRunBtn = $("[data-act=dry-run]");
    if (dryRunBtn) {
      dryRunBtn.addEventListener("click", () => {
        const profile = F.PROFILES.find((p) => p.id === state.profile_id);
        const result = $("#dry-run-result");
        const gates = ["G1 tenant scope", "G6 audit pointer", "PROFILE dry-run only"];
        const blocked = profile.forbids_write;
        result.innerHTML = `
          <div class="alert ${blocked ? "ok" : "warn"}">
            profile=${escapeHtml(profile.label)} · ${blocked ? "写操作被拦截（预期）" : "写操作将走真实门禁"}
          </div>
          <ul style="margin:8px 0;padding-left:18px;font-size:12px;color:var(--muted)">
            ${gates.map((g) => `<li>${escapeHtml(g)} · pass</li>`).join("")}
          </ul>
          <p style="font-size:12px">dry-run 不写入生产 · 不产生副作用</p>
        `;
        toast("I-05 dry-run 完成 · 结果已展示");
      });
    }

    const sreEscape = $("#sre-escape");
    if (sreEscape) {
      sreEscape.addEventListener("change", () => {
        state.sre_escape = sreEscape.checked;
        saveState();
        toast(state.sre_escape ? "零件逃生已开启 · 占位链接可见" : "零件逃生已关闭");
        render();
      });
    }

    $$("[data-escape]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        toast(`审计记录 · SRE 逃生占位访问 · ${a.dataset.escape}`);
      });
    });

    $$("[data-act=validate-wm]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const v = validateAccountability();
        toast(v.allOk ? "校验五件套通过" : `校验失败 · ${v.results.filter((r) => !r.complete).map((r) => r.node.id).join(", ")}`);
        render();
      });
    });

    $$("[data-projection]").forEach((cb) => {
      cb.addEventListener("change", () => {
        state.ontology_projections[cb.dataset.projection] = cb.checked;
        saveState();
        render();
      });
    });

    state.capabilities.forEach((cap, i) => {
      $$(`[data-cap-idx="${i}"]`).forEach((el) => {
        el.addEventListener("change", () => {
          const field = el.dataset.capField;
          const prevVal = cap[field];
          const nextVal = field === "enabled" ? el.checked : el.value;
          if (prevVal === nextVal) return;
          if (field === "enabled") el.checked = prevVal;
          else el.value = prevVal;
          submitChangeSet("capability.registry", `${cap.id} · ${field}: ${prevVal} → ${nextVal}`, { cap_id: cap.id, field, from: prevVal, to: nextVal });
        });
      });
    });

    state.connectors.forEach((conn, i) => {
      const sel = $(`[data-conn-idx="${i}"][data-conn-field=slot]`);
      if (sel) {
        sel.addEventListener("change", () => {
          const prev = conn.slot;
          const next = sel.value;
          if (prev === next) return;
          sel.value = prev;
          submitChangeSet("connector.slot", `${conn.id} 槽位 ${prev} → ${next}`, { connector: conn.id, from: prev, to: next });
        });
      }
    });

    $$("[data-act=rotate]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const idx = Number(btn.dataset.connIdx);
        const conn = state.connectors[idx];
        if (!conn) return;
        try {
          if (window.HubOps && typeof HubOps.connectorRotate === "function") {
            const out = await HubOps.connectorRotate({ connector_id: conn.id });
            if (out && out.changeset_id) {
              state.changesets = state.changesets || [];
              state.changesets.unshift({
                id: out.changeset_id,
                kind: "connector.rotate",
                summary: `${conn.id} 密钥轮换（无明文）`,
                status: out.status || "pending",
                auto_apply: false,
                payload: { connector_id: conn.id, secret_ref: out.secret_ref },
              });
            }
            toast("密钥轮换已提交 Hub ChangeSet · 仅 vault 指针");
            render();
            return;
          }
        } catch (e) {
          /* degrade */
        }
        submitChangeSet("connector.rotate", `${conn.id} 密钥轮换（无明文）`, {
          connector: conn.id,
          secret_ref: conn.secret_ref,
        });
        toast("密钥轮换已提交本地 ChangeSet · Hub 不可用");
      });
    });

    const mcpScene = $("#mcp-scene");
    if (mcpScene) {
      mcpScene.addEventListener("change", () => {
        state.mcp_scene = mcpScene.value;
        saveState();
        render();
      });
    }
    const mcpHide = $("#mcp-hide-write");
    if (mcpHide) {
      mcpHide.addEventListener("change", () => {
        state.mcp_hide_write = mcpHide.checked;
        saveState();
        render();
      });
    }

    state.models.forEach((model, i) => {
      $$(`[data-model-idx="${i}"]`).forEach((el) => {
        el.addEventListener("change", () => {
          const field = el.dataset.modelField;
          const prev = model[field];
          const nextVal = field === "rpm" ? Number(el.value) : el.value;
          if (prev === nextVal) return;
          if (field === "rpm") el.value = prev;
          else el.value = prev;
          submitChangeSet("model.route", `${model.id} · ${field}: ${prev} → ${nextVal}`, { route_id: model.id, field, from: prev, to: nextVal });
        });
      });
    });

    $$("[data-act=cs-confirm]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const cs = state.changeSets.find((c) => c.id === btn.dataset.csId);
        if (!cs || cs.status !== "pending") return;
        if (isDriftFail()) {
          toast("Schema drift fail · 发布确认被阻断");
          return;
        }
        const finish = () => {
          cs.status = "applied";
          cs.applied = true;
          applyChangeSet(cs);
          saveState();
          toast(`${cs.id} 已确认发布`);
          render();
        };
        if (window.HubOps && state.hub_ops === "ok") {
          window.HubOps.changesetDecide({ changeset_id: cs.id, approved: true })
            .then(finish)
            .catch(() => {
              toast("治理服务确认失败，请稍后重试");
            });
          return;
        }
        finish();
      });
    });

    $$("[data-act=cs-reject]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const cs = state.changeSets.find((c) => c.id === btn.dataset.csId);
        if (!cs || cs.status !== "pending") return;
        cs.status = "rejected";
        saveState();
        toast(`${cs.id} 已驳回`);
        render();
      });
    });

    bindGovOpsEvents();
  }

  /* ===== 治理/运维平面事件绑定 ===== */

  function localNow(withSeconds = true) {
    const d = new Date();
    const p = (n) => String(n).padStart(2, "0");
    const base = `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
    return withSeconds ? `${base}:${p(d.getSeconds())}` : base;
  }

  function pushAudit(type, object, result = "ok", error_code = null) {
    state.audit_events.unshift({
      id: `ae-${1000 + state.seq}`,
      ts: localNow(true),
      actor: "uas-console",
      type,
      object,
      result,
      error_code,
      corr: `c-demo-${state.seq}`,
      hash: `demo…${String(state.seq).padStart(4, "0")}`,
    });
  }

  function bindGovOpsEvents() {
    /* automation */
    $$("[data-act=run-job]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const job = state.automation_jobs.find((j) => j.id === btn.dataset.job);
        if (!job) return;
        const finish = () => {
          job.last_run = localNow(false);
          pushAudit("ops.automation.run", job.id);
          saveState();
          toast(`作业 ${job.name} 已运行 · findings ${job.findings.length} 条（审计 ops.automation.run）`);
          render();
        };
        if (window.HubOps && state.hub_ops === "ok" && window.HubOps.automationRun) {
          window.HubOps.automationRun({ job_id: job.id })
            .then((body) => {
              if (body && body.changeset_id) {
                state.changeSets.unshift({
                  id: body.changeset_id,
                  type: body.kind || "automation",
                  summary: body.summary || job.name,
                  payload: body.payload || {},
                  applied: false,
                  status: "pending",
                  created_at: new Date().toISOString(),
                  auto_apply: false,
                });
              }
              finish();
            })
            .catch(() => {
              toast("作业服务暂不可用，已降级本地");
              finish();
            });
          return;
        }
        finish();
      });
    });

    $$("[data-act=finding-cs]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const job = state.automation_jobs.find((j) => j.id === btn.dataset.job);
        const fd = job && job.findings[Number(btn.dataset.fi)];
        if (!fd || !fd.ref) return;
        const [type, key] = fd.ref.split(":");
        if (type === "connector.slot") submitChangeSet("connector.slot", `${key} 槽位 prod → sandbox（巡检建议·不自动切）`, { connector: key, from: "prod", to: "sandbox" });
        else if (type === "model.route") submitChangeSet("model.route", `${key} rpm 300 → 200（配额监控建议）`, { route_id: key, field: "rpm", from: 300, to: 200 });
        else if (type === "caliber.rerun") submitChangeSet("caliber.rerun", `口径 ${key} 重跑回填（stale 巡检）`, { key });
        else if (type === "wm.compile") submitChangeSet("wm.compile", `WM ${key} 修订编译（漂移修复）`, { item: key });
        else toast("该 finding 类型不支持转 ChangeSet");
      });
    });

    $$("[data-act=finding-ticket]").forEach((btn) => {
      btn.addEventListener("click", () => { pushAudit("ops.ticket.create", btn.dataset.job); toast("处置单已生成 · 已入审计（演示）"); });
    });
    $$("[data-act=finding-signal]").forEach((btn) => {
      btn.addEventListener("click", () => { pushAudit("ops.workflow.signal", btn.dataset.job); toast("信号已重发 · 已入审计（演示）"); });
    });
    $$("[data-act=finding-task]").forEach((btn) => {
      btn.addEventListener("click", () => { toast("已转本体修复任务（知识管理员队列·演示）"); });
    });
    $$("[data-act=finding-notify]").forEach((btn) => {
      btn.addEventListener("click", () => { toast("已通知值班运营（演示）"); });
    });

    /* audit */
    ["af-actor", "af-type", "af-result"].forEach((id) => {
      const sel = $(`#${id}`);
      if (sel) {
        sel.addEventListener("change", () => {
          const key = id.replace("af-", "");
          state.audit_filter[key] = sel.value;
          saveState();
          render();
        });
      }
    });
    const exportBtn = $("[data-act=audit-export]");
    if (exportBtn) {
      exportBtn.addEventListener("click", () => {
        pushAudit("ops.audit.export", "audit:filtered");
        saveState();
        toast("导出完成 · 导出动作已自审记录（ops.audit.export）");
        render();
      });
    }
    $$("[data-act=pattern-ticket]").forEach((btn) => {
      btn.addEventListener("click", () => {
        pushAudit("ops.ticket.create", btn.dataset.pat);
        saveState();
        toast(`异常模式 ${btn.dataset.pat} → 处置单已生成 · 审计已记录`);
      });
    });

    /* dualtrack */
    $$("[data-bind-idx]").forEach((sel) => {
      sel.addEventListener("change", () => {
        const b = state.iam_bindings[Number(sel.dataset.bindIdx)];
        const next = sel.value;
        if (!b || !next) return;
        sel.value = "";
        submitChangeSet("iam.binding", `岗位绑定 ${b.id} · 人员 ${b.person} → ${next}`, { binding_id: b.id, field: "person", from: b.person, to: next });
      });
    });
    $$("[data-act=ur-approve]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const r = state.upgrade_requests.find((x) => x.id === btn.dataset.ur);
        if (!r || r.status !== "pending") return;
        if (!r.evidence_ref) { toast("TRACK_ESCALATION_REQUIRED · 无证据不可升级"); return; }
        r.status = "approved";
        pushAudit("ops.iam.upgrade", r.id);
        saveState();
        toast(`${r.id} 已升级入 ΠPaw · 证据 ${r.evidence_ref} · 审计已记录`);
        render();
      });
    });
    $$("[data-act=ur-reject]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const r = state.upgrade_requests.find((x) => x.id === btn.dataset.ur);
        if (!r || r.status !== "pending") return;
        r.status = "rejected";
        pushAudit("ops.iam.upgrade_reject", r.id);
        saveState();
        toast(`${r.id} 已驳回`);
        render();
      });
    });

    /* memory */
    $$("[data-act=forget-exec]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const r = state.forget_requests.find((x) => x.id === btn.dataset.fr);
        if (!r || r.status !== "pending") return;
        if (!window.confirm(`确认执行遗忘？\n${r.subject}\n范围：${r.scope}\n该操作不可撤销，将生成回执并入审计。`)) return;
        r.status = "done";
        const receipt = {
          id: `frc-2026-0${15 + state.forget_receipts.length}`,
          request: r.id,
          subject: r.subject,
          erased: 20 + Math.floor(Math.random() * 80),
          at: localNow(false),
          audit_ptr: `ae-${1000 + state.seq}`,
        };
        state.forget_receipts.unshift(receipt);
        pushAudit("ops.memory.forget", r.id);
        saveState();
        toast(`遗忘已执行 · 回执 ${receipt.id} 已生成（可检索）`);
        render();
      });
    });
    $$("[data-act=forget-cancel]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const r = state.forget_requests.find((x) => x.id === btn.dataset.fr);
        if (!r || r.status !== "pending") return;
        r.status = "cancelled";
        saveState();
        toast(`${r.id} 已撤销`);
        render();
      });
    });
    const rq = $("#receipt-q");
    if (rq) {
      rq.addEventListener("input", () => {
        const q = rq.value.trim();
        $$("#receipt-rows tr").forEach((tr) => {
          tr.style.display = !q || (tr.dataset.subject || "").includes(q) ? "" : "none";
        });
      });
    }

    /* evolution */
    const tcBtn = $("[data-act=toggle-cases]");
    if (tcBtn) {
      tcBtn.addEventListener("click", () => {
        state.evo_cases.forEach((c) => { c.result = "pass"; });
        saveState();
        toast("回归夹具已切换：全部 pass");
        render();
      });
    }
    const promoteBtn = $("[data-act=evo-promote]");
    if (promoteBtn) {
      promoteBtn.addEventListener("click", () => {
        if (state.evo_cases.some((c) => c.result === "fail")) {
          toast("REGRESSION_NOT_PASSED · 回归未通过，禁止发布");
          return;
        }
        submitChangeSet("lawpack.promote", `Law Pack ${F.EVO_DRAFT.base} → ${F.EVO_DRAFT.target}（评审通过）`, { pack: F.EVO_DRAFT.target, reviewer_role: state.role });
        toast("评审人 ≠ 提交人 ✔ · ChangeSet 已入发布队列");
      });
    }

    /* caliber */
    $$("[data-act=cal-rerun]").forEach((btn) => {
      btn.addEventListener("click", () => {
        submitChangeSet("caliber.rerun", `口径 ${btn.dataset.key} 重跑回填（stale 巡检处置）`, { key: btn.dataset.key });
      });
    });
    $$("[data-act=cal-edit-live]").forEach((btn) => {
      btn.addEventListener("click", () => {
        toast("COMPILED_IMMUTABLE · live 口径不可原地改，请创建草稿走 ChangeSet");
      });
    });
    $$("[data-act=cal-edit-draft]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const c = state.calibers[Number(btn.dataset.idx)];
        const editor = $("#caliber-editor");
        if (!c || !editor) return;
        editor.hidden = false;
        $("#caliber-editor-title").textContent = `口径 ${c.key} · 草稿编辑`;
        $("#caliber-expr").value = c.expr;
        state.caliber_draft = c.key;
        saveState();
      });
    });
    const calPub = $("[data-act=cal-publish]");
    if (calPub) {
      calPub.addEventListener("click", () => {
        const key = state.caliber_draft;
        const expr = $("#caliber-expr").value.trim();
        if (!key || !expr) { toast("请先选择草稿口径并填写表达式"); return; }
        submitChangeSet("caliber.publish", `口径 ${key} 表达式发布：${expr}`, { key, to: expr });
      });
    }

    /* workflows */
    $$("[data-act=wf-signal]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const w = state.workflow_instances[Number(btn.dataset.idx)];
        if (!w) return;
        w.wait = 0;
        pushAudit("ops.workflow.signal", w.id);
        saveState();
        toast(`已向 ${w.id} 重发信号 · 审计 ops.workflow.signal`);
        render();
      });
    });

    /* wm */
    $$("[data-act=wm-compile]").forEach((btn) => {
      btn.addEventListener("click", () => {
        submitChangeSet("wm.compile", `WM ${btn.dataset.wm} draft → 编译申请`, { item: btn.dataset.wm });
      });
    });
    $$("[data-act=wm-edit-live]").forEach((btn) => {
      btn.addEventListener("click", () => {
        toast("COMPILED_IMMUTABLE · live WM 不可原地改，请修订 draft 走编译");
      });
    });
  }

  function applyChangeSet(cs) {
    const p = cs.payload || {};
    if (cs.type === "tenant.suite" && p.suite) {
      state.suites[p.suite] = p.to;
    }
    if (cs.type === "capability.registry" && p.cap_id) {
      const cap = state.capabilities.find((c) => c.id === p.cap_id);
      if (cap && p.field) cap[p.field] = p.to;
    }
    if (cs.type === "connector.slot" && p.connector) {
      const conn = state.connectors.find((c) => c.id === p.connector);
      if (conn) {
        conn.slot = p.to;
        conn.secret_ref = `vault://${conn.id.split(".")[1]}/${p.to}`;
      }
    }
    if (cs.type === "model.route" && p.route_id) {
      const model = state.models.find((m) => m.id === p.route_id);
      if (model && p.field) model[p.field] = p.to;
    }
    if (cs.type === "caliber.rerun" && p.key) {
      const c = state.calibers.find((x) => x.key === p.key);
      if (c) { c.status = "fresh"; c.last_refresh = "2026-09-11 18:05"; }
    }
    if (cs.type === "caliber.publish" && p.key) {
      const c = state.calibers.find((x) => x.key === p.key);
      if (c) { c.expr = p.to; if (c.lifecycle === "draft") c.lifecycle = "live"; }
    }
    if (cs.type === "wm.compile" && p.item) {
      const w = state.wm_items.find((x) => x.id === p.item);
      if (w) { w.conflict = false; if (w.lifecycle === "draft") w.lifecycle = "compiling"; }
    }
    if (cs.type === "iam.binding" && p.binding_id) {
      const b = state.iam_bindings.find((x) => x.id === p.binding_id);
      if (b && p.field) b[p.field] = p.to;
    }
    /* lawpack.promote / kg.policy / graph.node.update：fixture 页只记录 ChangeSet，不就地改 fixture */
  }

  function render() {
    renderRoleSelect();
    renderBanStrip();
    $("#tenant-chip").textContent = state.tenant_id;

    const locked = isFrontlineLocked();
    $("#lock-overlay").hidden = !locked;
    const lockTitle = $("#lock-overlay h2");
    if (lockTitle) lockTitle.textContent = frontlineLockCopy();

    const page = currentPage();
    highlightPlanes(page);
    renderRail(page);
    const renderer = PAGE_RENDERERS[page] || PAGE_RENDERERS.overview;
    $("#main").innerHTML = renderer();
    bindPageEvents(page);
  }

  function ensureOpsBanner() {
    let el = $("#ops-banner");
    if (el) return el;
    el = document.createElement("div");
    el.id = "ops-banner";
    el.className = "ban-strip";
    const strip = $("#ban-strip");
    if (strip && strip.parentNode) strip.parentNode.insertBefore(el, strip.nextSibling);
    else document.body.prepend(el);
    return el;
  }

  function bootHubOps() {
    if (!window.HubOps) return;
    window.CONSOLE_OPS_ROLE = state.role;
    const banner = ensureOpsBanner();
    Promise.all([
      window.HubOps.tenantGet(),
      window.HubOps.healthSummary(),
      window.HubOps.schemaDrift(),
      window.HubOps.changesetList(),
      window.HubOps.auditSearch(""),
      window.HubOps.iamBindings(),
      window.HubOps.graphGet({}),
      window.HubOps.registryList(),
      window.HubOps.skillList(),
      window.HubOps.caliberStatus(),
      window.HubOps.kgIngestStatus(),
      window.HubOps.runtimeTask(),
      window.HubOps.artifactList(),
      window.HubOps.modelRoute(),
      window.HubOps.memoryReceipt(""),
      window.HubOps.automationJobs(),
      window.HubOps.wmList(),
    ])
      .then(([tenant, health, drift, changes, audit, iam, graph, _reg, _skills, caliber, kgIngest, runtime, artifacts, models, receipts, autoJobs, wmList]) => {
        state.hub_ops = "ok";
        if (tenant && tenant.tenant_id) state.tenant_id = tenant.tenant_id;
        if (health) state.health = { ...state.health, ...health };
        if (drift) state.schema_drift = drift;
        if (changes && Array.isArray(changes.items)) {
          state.changeSets = changes.items.map((c) => ({
            id: c.changeset_id,
            type: c.kind || "manual",
            summary: c.summary || "",
            payload: c.payload || {},
            applied: c.status === "applied",
            status: c.status,
            created_at: c.created_at || new Date().toISOString(),
            auto_apply: false,
          }));
        }
        if (audit && Array.isArray(audit.records) && audit.records.length) {
          state.audit_events = audit.records.map((r, i) => ({
            id: `hub-ae-${i}`,
            ts: r.ts || "",
            actor: r.actor_id || r.actor || "hub",
            type: r.operation || r.type || "hub.ops",
            object: r.note || r.q || "",
            result: "ok",
            error_code: null,
            corr: r.correlation_id || "",
            hash: "",
          }));
        }
        if (iam && Array.isArray(iam.bindings) && iam.bindings.length) {
          state.iam_bindings = iam.bindings.map((b, i) => ({
            id: `iam-${i}`,
            person: b.actor_id,
            position: b.position_id,
            tenant: b.tenant_id,
          }));
        }
        if (caliber && Array.isArray(caliber.items) && caliber.items.length) {
          state.calibers = caliber.items.map((c) => ({
            key: c.key,
            status: c.status || (c.stale ? "stale" : "fresh"),
            expr: c.caliber_id || "",
            last_refresh: c.as_of || "",
            lifecycle: "live",
            stale: !!c.stale,
          }));
        }
        if (kgIngest) {
          state.kg_ingest = {
            status: kgIngest.status || "ok",
            lag_minutes: kgIngest.lag_minutes || 0,
            last_episode: kgIngest.last_episode || "",
            failures: kgIngest.failures || [],
          };
        }
        if (runtime && Array.isArray(runtime.tasks)) {
          state.runtime_tasks = runtime.tasks;
          if (runtime.tasks.length) {
            state.workflow_instances = runtime.tasks.map((t) => ({
              title: t.task_id || "task",
              task: "外环",
              step: t.status || "",
              wait: t.status === "awaiting_approval" ? 5 : 0,
              status: t.status === "awaiting_approval" ? "waiting" : t.status || "running",
              degraded: false,
            }));
          }
        }
        if (artifacts && Array.isArray(artifacts.items)) {
          state.artifacts = artifacts.items;
        }
        if (models && Array.isArray(models.routes) && models.routes.length) {
          state.models = models.routes.map((r) => ({
            id: r.id,
            label: r.id,
            model: r.provider || "fixture",
            provider: r.provider,
            rpm: r.rpm,
            slot: "sandbox",
          }));
        }
        if (receipts && Array.isArray(receipts.receipts)) {
          state.forget_receipts = receipts.receipts.map((r) => ({
            id: r.receipt_id,
            subject: r.actor_id || "",
            erased: r.forgotten ? 1 : 0,
            at: r.ts || "",
            audit_ptr: r.receipt_id || "",
          }));
        }
        if (autoJobs && Array.isArray(autoJobs.jobs) && autoJobs.jobs.length) {
          state.automation_jobs = autoJobs.jobs.map((j) => ({
            id: j.id,
            name: j.name,
            module: j.id,
            schedule: j.schedule || "",
            last_run: j.last_run || "",
            status: "ok",
            findings: (j.findings || []).map((f) => ({
              id: f.id,
              label: f.label,
              summary: f.label,
              sev: f.severity || "medium",
              severity: f.severity || "medium",
              action: "changeset",
            })),
          }));
        }
        if (wmList && Array.isArray(wmList.items) && wmList.items.length) {
          state.wm_items = wmList.items.map((w) => ({
            id: w.world_model_id,
            type: "fixture",
            lifecycle: w.lifetime === "compiled" ? "live" : w.lifetime || "draft",
            conflict: false,
            label: w.world_model_id,
            node_ref: "—",
            summary: (w.keys || []).join(",") || "hub wm",
          }));
        }
        banner.hidden = false;
        banner.dataset.hub = "ok";
        banner.textContent = `治理 Hub 已连接 · ${graph && graph.graph_id ? graph.graph_id : tenant.graph_id || ""}`;
        saveState();
        render();
      })
      .catch(() => {
        state.hub_ops = "degraded";
        banner.hidden = false;
        banner.dataset.hub = "degraded";
        banner.textContent = "治理服务暂不可用，只读降级";
      });
  }

  window.addEventListener("hashchange", render);
  if (!location.hash) location.hash = "#/overview";
  render();
  bootHubOps();
})();
