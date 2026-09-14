(() => {
  "use strict";

  const F = window.ConsoleFixtures;
  const STORAGE_KEY = "platform-console-state-v1";

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
  }

  function isFrontlineLocked() {
    return state.role === "frontline";
  }

  function isDriftFail() {
    return state.schema_drift.status === "fail";
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
    nav.innerHTML = F.PAGES.map((p) => `
      <button type="button" data-page="${p.id}" class="${p.id === page ? "is-on" : ""}">
        ${escapeHtml(p.label)}
        <small>${escapeHtml(p.hint)}</small>
      </button>
    `).join("");
    $$("button[data-page]", nav).forEach((btn) => {
      btn.addEventListener("click", () => setHash(btn.dataset.page));
    });
  }

  function renderRoleSelect() {
    const sel = $("#role-select");
    sel.innerHTML = F.ROLES.map((r) => `<option value="${r.id}" ${r.id === state.role ? "selected" : ""}>${escapeHtml(r.label)}</option>`).join("");
    sel.onchange = () => {
      state.role = sel.value;
      saveState();
      render();
    };
  }

  function metricClass(key, val) {
    if (key === "ungrounded_rate" && val > 0.05) return "bad";
    if (key === "gate_p95_ms" && val > 200) return "warn";
    if (key === "approval_stuck" && val > 0) return "warn";
    if (key === "stale" && val > 0) return "warn";
    return "ok";
  }

  function renderOverview() {
    const h = state.health;
    const drift = state.schema_drift;
    const pending = pendingChangeSets().length;
    const metrics = [
      { k: "health.use.open_ms", v: h.open_ms, fmt: (v) => `${v} ms` },
      { k: "health.use.explain", v: h.explain, fmt: (v) => `${(v * 100).toFixed(0)}%` },
      { k: "health.use.ungrounded_rate", v: h.ungrounded_rate, fmt: (v) => `${(v * 100).toFixed(1)}%` },
      { k: "health.control.gate_p95_ms", v: h.gate_p95_ms, fmt: (v) => `${v} ms` },
      { k: "approval_stuck", v: h.approval_stuck, fmt: (v) => String(v) },
      { k: "stale", v: h.stale, fmt: (v) => String(v) },
    ];
    return `
      <div class="page-head">
        <h1>总览</h1>
        <p>hub.ops 健康指标与租户 ${escapeHtml(state.tenant_id)} 套件摘要。所有写操作走 ChangeSet，禁止静默应用。</p>
      </div>
      <div class="grid-3" style="margin-bottom:14px">
        ${metrics.map((m) => `
          <div class="metric">
            <div class="k">${escapeHtml(m.k)}</div>
            <div class="v ${metricClass(m.key || m.k.split(".").pop(), m.v)}">${escapeHtml(m.fmt(m.v))}</div>
          </div>
        `).join("")}
      </div>
      <div class="grid-2">
        <section class="card">
          <h2>Schema 漂移</h2>
          <p class="sub">US-B-10 · 交互式 healthy / fail 夹具</p>
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
            <span class="status-pill ${drift.status === "healthy" ? "ok" : "fail"}">
              <span class="dot"></span>${drift.status === "healthy" ? "healthy" : "fail"} · drift=${drift.count}
            </span>
            <button type="button" class="btn ghost" data-act="toggle-drift">切换夹具</button>
          </div>
          ${drift.status === "fail" ? '<div class="alert fail">漂移检测失败 · 相关 ChangeSet 发布将被阻断</div>' : '<div class="alert ok">Schema 与注册中心一致</div>'}
        </section>
        <section class="card">
          <h2>待发布 ChangeSet</h2>
          <p class="sub">${pending} 条 pending · <a href="#/publish" style="color:var(--accent)">前往发布页</a></p>
          ${pending ? pendingChangeSets().slice(0, 3).map((c) => `<div style="font-size:12px;margin:6px 0"><code>${escapeHtml(c.id)}</code> · ${escapeHtml(c.summary)}</div>`).join("") : '<p class="empty">暂无待确认项</p>'}
        </section>
      </div>
      <section class="card" style="margin-top:14px">
        <h2>租户套件 · ${escapeHtml(state.tenant_id)}</h2>
        <p class="sub">US-B-03 · 切换提交 ChangeSet，不静默生效</p>
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
      <div class="page-head">
        <h1>集成</h1>
        <p>剖面策略与 I-05 dry-run。Explore/Builder 禁止写生产；dry-run 仅模拟门禁结果。</p>
      </div>
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
      <div class="page-head">
        <h1>管控</h1>
        <p>租户套件启用与 US-B-21 治理禁令。auto_apply 永久关闭；不存在「关闭审计」控件。</p>
      </div>
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
      <div class="page-head">
        <h1>本体</h1>
        <p>责任链节点与校验五件套。I-02 缺 feedback 维 / 口径 → WM_INCOMPLETE · INVARIANT_FAILED。</p>
      </div>
      ${validation.allOk
        ? '<div class="alert ok">校验五件套通过 · 全部节点 WM 五维 + caliber 齐全</div>'
        : `<div class="alert fail">校验失败 · ${validation.results.filter((r) => !r.complete).map((r) => `${r.node.id}: ${r.codes.join(", ")}`).join(" · ")}</div>`}
      <div class="graph-wrap">
        <section class="card">
          <h2>责任节点</h2>
          <div class="node-list">
            ${validation.results.map(({ node, missing, caliberOk, complete, codes }) => `
              <div class="node-card ${complete ? "complete" : "incomplete"}">
                <strong>${escapeHtml(node.label)}</strong>
                <div style="font-size:11px;color:var(--muted)">${escapeHtml(node.id)} · ${escapeHtml(node.owner)}</div>
                <div style="font-size:11px;margin-top:4px">caliber: ${caliberOk ? escapeHtml(node.caliber) : "<span style='color:var(--red)'>缺失</span>"}</div>
                <div class="dims">
                  ${Object.entries(node.wm).map(([d, ok]) => `<span class="dim-tag ${ok ? "on" : "off"}">${d}</span>`).join("")}
                </div>
                ${!complete ? `<div style="font-size:11px;color:var(--red);margin-top:6px">${escapeHtml(codes.join(" · "))}</div>` : ""}
              </div>
            `).join("")}
          </div>
          <button type="button" class="btn" data-act="validate-wm" style="margin-top:12px">重新校验五件套</button>
        </section>
        <section class="card">
          <h2>投影边种类</h2>
          <p class="sub">P2 · UI 夹具切换</p>
          ${Object.keys(proj).map((kind) => `
            <label class="inline-check" style="margin-bottom:6px">
              <input type="checkbox" data-projection="${kind}" ${proj[kind] ? "checked" : ""} />
              ${escapeHtml(kind)}
            </label>
          `).join("")}
          <div class="edge-panel" style="margin-top:10px">
            ${activeEdges.length
              ? activeEdges.map((e) => `<div class="edge-line">${escapeHtml(e.from)} → ${escapeHtml(e.to)} <span style="color:var(--accent)">[${e.kind}]</span></div>`).join("")
              : '<div class="empty">未选择投影边</div>'}
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
      <div class="page-head">
        <h1>网格</h1>
        <p>能力注册、连接器槽位与 MCP 工具列表。scene 过滤可隐藏 write 类工具。</p>
      </div>
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
      <div class="page-head">
        <h1>治理</h1>
        <p>法则包版本与冲突声明。晋升与回写均须 ChangeSet，禁止静默。</p>
      </div>
      <div class="grid-2">
        <section class="card">
          <h2>Law Pack</h2>
          <p class="sub">P2 · 显式冲突声明</p>
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
      <div class="page-head">
        <h1>运行</h1>
        <p>模型路由与 KG 摄入状态。无 ingest 写按钮 · 无 CRM 写入口。</p>
      </div>
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
          <h2>KG 摄入 · ingest_status</h2>
          <p class="sub">US-B-17 · 只读 · lag + 最近 episode + 失败列表</p>
          <div style="display:flex;gap:12px;align-items:center;margin-bottom:10px">
            <span class="status-pill ${kg.status === "ok" ? "ok" : "warn"}"><span class="dot"></span>${escapeHtml(kg.status)}</span>
            <span style="font-size:12px;color:var(--muted)">lag ${kg.lag_minutes} min</span>
          </div>
          <p style="font-size:12px">最近 episode: <code>${escapeHtml(kg.last_episode)}</code></p>
          <h3 style="font-size:13px;margin:14px 0 8px">失败夹具</h3>
          <table class="data">
            <thead><tr><th>episode</th><th>原因</th><th>时间</th></tr></thead>
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
      <div class="page-head">
        <h1>发布</h1>
        <p>ChangeSet 确认 / 驳回队列。schema drift=fail 时阻断相关发布。</p>
      </div>
      ${isDriftFail() ? '<div class="alert fail">US-B-10 · Schema 漂移 fail · 发布确认已阻断，请先修复漂移或切换 healthy 夹具</div>' : ""}
      <section class="card">
        <h2>ChangeSet 队列</h2>
        ${list.length ? `<div class="changeset-list">${list.map((c) => renderChangeSetItem(c)).join("")}</div>` : '<p class="empty">暂无 ChangeSet</p>'}
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

  const PAGE_RENDERERS = {
    overview: renderOverview,
    integrate: renderIntegrate,
    control: renderControl,
    ontology: renderOntology,
    mesh: renderMesh,
    govern: renderGovern,
    run: renderRun,
    publish: renderPublish,
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
      btn.addEventListener("click", () => {
        const idx = Number(btn.dataset.connIdx);
        const conn = state.connectors[idx];
        submitChangeSet("connector.rotate", `${conn.id} 密钥轮换（无明文）`, { connector: conn.id, secret_ref: conn.secret_ref });
        toast("密钥轮换已提交 ChangeSet · 未展示明文");
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
        cs.status = "applied";
        cs.applied = true;
        applyChangeSet(cs);
        saveState();
        toast(`${cs.id} 已确认发布`);
        render();
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
  }

  function render() {
    renderRoleSelect();
    renderBanStrip();
    $("#tenant-chip").textContent = state.tenant_id;

    const locked = isFrontlineLocked();
    $("#lock-overlay").hidden = !locked;

    const page = currentPage();
    renderRail(page);
    const renderer = PAGE_RENDERERS[page] || PAGE_RENDERERS.overview;
    $("#main").innerHTML = renderer();
    bindPageEvents(page);
  }

  window.addEventListener("hashchange", render);
  if (!location.hash) location.hash = "#/overview";
  render();
})();
