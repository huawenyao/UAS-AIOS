/**
 * UniAgent 集群：分析任务流 + L3 协议包动画 + 简易涌现（群体向心对齐）
 * 与 UACA L3 消息类型、合同网、GOSSIP 语义对齐（演示用，非仿真器）
 */
(function () {
  const NODES = {
    coord: { x: 500, y: 88, label: "协调器", sub: "L4 策略 / 合同网" },
    a03: { x: 195, y: 248, label: "agent-03", sub: "分析 / reason" },
    a07: { x: 500, y: 300, label: "agent-07", sub: "执行 / sense" },
    a12: { x: 805, y: 248, label: "agent-12", sub: "worker" },
    sense: { x: 330, y: 428, label: "接地", sub: "sense.poll" },
    wm: { x: 500, y: 532, label: "World", sub: "L5 propose→commit" },
  };

  const EDGES = [
    { from: "coord", to: "a03", kind: "policy" },
    { from: "coord", to: "a07", kind: "policy" },
    { from: "coord", to: "a12", kind: "policy" },
    { from: "a03", to: "a12", kind: "gossip" },
    { from: "a07", to: "sense", kind: "sense" },
    { from: "a07", to: "wm", kind: "propose" },
    { from: "a03", to: "wm", kind: "propose" },
    { from: "a12", to: "wm", kind: "propose" },
  ];

  const MSG_COLORS = {
    TASK_OFFER: "#c9a227",
    TASK_ACK: "#8fb86a",
    DIRECT: "#5eb3c8",
    GOSSIP: "#a896c8",
    PROPOSAL: "#d4654a",
    REWARD: "#c9a227",
    HEARTBEAT: "#6a7a8a",
    BACKPRESSURE: "#b8956a",
  };

  const PIPELINE_STEPS = [
    { key: "offer", title: "TASK_OFFER", desc: "协调器广播任务+约束+reward" },
    { key: "ack", title: "TASK_ACK", desc: "agent-07 接受 / 竞价有效出价" },
    { key: "sense", title: "DIRECT", desc: "sense.poll → 观测写入 L2 包络" },
    { key: "reason", title: "DIRECT", desc: "reason.* → 候选结构（须过 rules）" },
    { key: "propose", title: "PROPOSAL", desc: "world.propose + grounding_chain" },
    { key: "reward", title: "REWARD", desc: "task_id + reward_signal → 适应引擎" },
  ];

  let playing = true;
  let scenario = "analysis";
  let analysisIndex = 0;
  let gossipHop = 0;
  let rafId = null;
  let lastT = 0;
  let accum = 0;

  /** @type {{ el: SVGCircleElement, t: number, dur: number, x0: number, y0: number, x1: number, y1: number, color: string, label: string }[]} */
  let packets = [];

  /** Emergence particles */
  const EMERGENCE_N = 48;
  let particles = [];

  function el(id) {
    return document.getElementById(id);
  }

  function log(line, hot) {
    const box = el("ch-viz-log");
    if (!box) return;
    const div = document.createElement("div");
    div.className = "log-line" + (hot ? " log-line--hot" : "");
    div.textContent = line;
    box.insertBefore(div, box.firstChild);
    while (box.children.length > 24) box.removeChild(box.lastChild);
  }

  function setPipelineActive(index) {
    document.querySelectorAll(".ch-viz-step").forEach((step, i) => {
      step.classList.toggle("is-active", i === index);
    });
    const meter = el("ch-viz-order-meter");
    if (meter) {
      const pct = Math.round(((index + 1) / PIPELINE_STEPS.length) * 100);
      meter.style.width = pct + "%";
    }
  }

  function nodePos(id) {
    const n = NODES[id];
    return { x: n.x, y: n.y };
  }

  function spawnPacket(fromId, toId, color, label, duration = 1.2) {
    const a = nodePos(fromId);
    const b = nodePos(toId);
    const svg = el("ch-viz-svg");
    if (!svg) return;
    const NS = "http://www.w3.org/2000/svg";
    const c = document.createElementNS(NS, "circle");
    c.setAttribute("r", "7");
    c.setAttribute("fill", color);
    c.setAttribute("opacity", "0.95");
    c.setAttribute("filter", "url(#ch-glow)");
    const g = el("ch-packets");
    g.appendChild(c);
    packets.push({
      el: c,
      t: 0,
      dur: duration,
      x0: a.x,
      y0: a.y,
      x1: b.x,
      y1: b.y,
      color,
      label,
    });
    log(`${label}  ${fromId} → ${toId}`, true);
  }

  function clearPackets() {
    const g = el("ch-packets");
    if (!g) return;
    g.innerHTML = "";
    packets = [];
  }

  function runAnalysisBeat() {
    const seq = [
      () => {
        setPipelineActive(0);
        spawnPacket("coord", "a07", MSG_COLORS.TASK_OFFER, "TASK_OFFER");
      },
      () => {
        setPipelineActive(1);
        spawnPacket("a07", "coord", MSG_COLORS.TASK_ACK, "TASK_ACK", 0.9);
      },
      () => {
        setPipelineActive(2);
        spawnPacket("a07", "sense", MSG_COLORS.DIRECT, "DIRECT(sense)");
      },
      () => {
        setPipelineActive(3);
        spawnPacket("a07", "a03", MSG_COLORS.DIRECT, "DIRECT(delegate)", 1);
      },
      () => {
        setPipelineActive(4);
        spawnPacket("a07", "wm", MSG_COLORS.PROPOSAL, "PROPOSAL→L5");
      },
      () => {
        setPipelineActive(5);
        spawnPacket("wm", "coord", MSG_COLORS.REWARD, "REWARD", 1);
      },
    ];
    const i = analysisIndex % seq.length;
    seq[i]();
    analysisIndex = (analysisIndex + 1) % seq.length;
  }

  function runGossipBeat() {
    const ring = ["a03", "a12", "a07", "a03"];
    const a = ring[gossipHop % ring.length];
    const b = ring[(gossipHop + 1) % ring.length];
    spawnPacket(a, b, MSG_COLORS.GOSSIP, "GOSSIP(TTL)", 1.4);
    log(`GOSSIP 信念扩散 hop=${gossipHop % 3}`, false);
    gossipHop++;
    setPipelineActive(-1);
    const meter = el("ch-viz-order-meter");
    if (meter) {
      const converge = 40 + (gossipHop % 5) * 12;
      meter.style.width = Math.min(95, converge) + "%";
    }
  }

  function runTopologyBeat() {
    const e = EDGES[Math.floor(Math.random() * EDGES.length)];
    spawnPacket(e.from, e.to, MSG_COLORS.HEARTBEAT, "HEARTBEAT/背压探测", 0.8);
    log("L4 边状态: active · AoI 采样", false);
    setPipelineActive(-1);
  }

  function initEmergence() {
    const canvas = el("ch-emergence");
    if (!canvas) return;
    const w = canvas.width;
    const h = canvas.height;
    particles = [];
    for (let i = 0; i < EMERGENCE_N; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8,
      });
    }
  }

  function tickEmergence(dt) {
    const canvas = el("ch-emergence");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h / 2;
    let distSum = 0;
    particles.forEach((p) => {
      const dx = cx - p.x;
      const dy = cy - p.y;
      distSum += Math.hypot(dx, dy);
      p.vx += dx * 0.00012 * dt;
      p.vy += dy * 0.00012 * dt;
      p.vx += (Math.random() - 0.5) * 0.02;
      p.vy += (Math.random() - 0.5) * 0.02;
      p.vx *= 0.985;
      p.vy *= 0.985;
      p.x += p.vx * dt * 0.06;
      p.y += p.vy * dt * 0.06;
      p.x = Math.max(4, Math.min(w - 4, p.x));
      p.y = Math.max(4, Math.min(h - 4, p.y));
    });
    const order = 1 - Math.min(1, distSum / (particles.length * 40));
    const label = el("ch-emergence-val");
    if (label) label.textContent = (order * 100).toFixed(0) + "%";

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = getComputedStyle(document.documentElement)
      .getPropertyValue("--ch-lens")
      .trim() || "#5eb3c8";
    particles.forEach((p) => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, 2.2, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  function updateEdgesDim() {
    document.querySelectorAll(".ch-edge").forEach((line) => {
      line.setAttribute("opacity", "0.35");
    });
  }

  function highlightEdge(from, to) {
    updateEdgesDim();
    const id = `edge-${from}-${to}`;
    const line = el(id);
    if (line) line.setAttribute("opacity", "1");
  }

  function tick(ts) {
    if (!lastT) lastT = ts;
    const dt = Math.min(32, ts - lastT);
    lastT = ts;

    if (playing) {
      accum += dt;
      tickEmergence(dt);
      const interval = scenario === "gossip" ? 2200 : scenario === "topology" ? 1800 : 2600;
      if (accum >= interval) {
        accum = 0;
        clearPackets();
        if (scenario === "analysis") runAnalysisBeat();
        else if (scenario === "gossip") runGossipBeat();
        else runTopologyBeat();
      }
    }

    packets = packets.filter((p) => {
      p.t += dt / 1000;
      const u = Math.min(1, p.t / p.dur);
      const x = p.x0 + (p.x1 - p.x0) * easeOutCubic(u);
      const y = p.y0 + (p.y1 - p.y0) * easeOutCubic(u);
      p.el.setAttribute("cx", String(x));
      p.el.setAttribute("cy", String(y));
      if (u >= 1) {
        p.el.remove();
        return false;
      }
      return true;
    });

    rafId = requestAnimationFrame(tick);
  }

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function drawStaticGraph() {
    const gEdges = el("ch-edges");
    const gNodes = el("ch-nodes");
    if (!gEdges || !gNodes) return;
    const NS = "http://www.w3.org/2000/svg";

    EDGES.forEach((e) => {
      const a = NODES[e.from];
      const b = NODES[e.to];
      const line = document.createElementNS(NS, "line");
      line.setAttribute("id", `edge-${e.from}-${e.to}`);
      line.setAttribute("class", "ch-edge");
      line.setAttribute("x1", String(a.x));
      line.setAttribute("y1", String(a.y));
      line.setAttribute("x2", String(b.x));
      line.setAttribute("y2", String(b.y));
      line.setAttribute("stroke", edgeStroke(e.kind));
      line.setAttribute("stroke-width", e.kind === "gossip" ? "1.5" : "2");
      line.setAttribute("stroke-dasharray", e.kind === "gossip" ? "6 6" : "none");
      line.setAttribute("opacity", "0.45");
      gEdges.appendChild(line);
    });

    Object.entries(NODES).forEach(([id, n]) => {
      const gr = document.createElementNS(NS, "g");
      gr.setAttribute("data-node", id);
      const circle = document.createElementNS(NS, "circle");
      circle.setAttribute("cx", String(n.x));
      circle.setAttribute("cy", String(n.y));
      circle.setAttribute("r", id === "coord" ? "36" : id === "wm" ? "40" : "32");
      circle.setAttribute("fill", nodeFill(id));
      circle.setAttribute("stroke", "var(--ch-border, rgba(255,255,255,0.15))");
      circle.setAttribute("stroke-width", "1.5");
      const t1 = document.createElementNS(NS, "text");
      t1.setAttribute("x", String(n.x));
      t1.setAttribute("y", String(n.y - 6));
      t1.setAttribute("text-anchor", "middle");
      t1.setAttribute("fill", "var(--ch-text, #f2ebe3)");
      t1.setAttribute("font-size", "13");
      t1.setAttribute("font-family", "Noto Serif SC, serif");
      t1.textContent = n.label;
      const t2 = document.createElementNS(NS, "text");
      t2.setAttribute("x", String(n.x));
      t2.setAttribute("y", String(n.y + 12));
      t2.setAttribute("text-anchor", "middle");
      t2.setAttribute("fill", "var(--ch-muted, #9a8f82)");
      t2.setAttribute("font-size", "10");
      t2.setAttribute("font-family", "ui-monospace, monospace");
      t2.setAttribute("class", "sec");
      t2.textContent = n.sub;
      gr.appendChild(circle);
      gr.appendChild(t1);
      gr.appendChild(t2);
      gNodes.appendChild(gr);
    });
  }

  function edgeStroke(kind) {
    if (kind === "gossip") return "#a896c8";
    if (kind === "propose") return "#d4654a";
    if (kind === "sense") return "#5eb3c8";
    return "rgba(201, 162, 39, 0.55)";
  }

  function nodeFill(id) {
    if (id === "coord") return "rgba(201, 162, 39, 0.25)";
    if (id === "wm") return "rgba(212, 101, 74, 0.22)";
    if (id === "sense") return "rgba(94, 179, 200, 0.2)";
    return "rgba(26, 23, 20, 0.9)";
  }

  function onScenarioChange() {
    const sel = el("ch-scenario");
    scenario = sel ? sel.value : "analysis";
    analysisIndex = 0;
    gossipHop = 0;
    accum = 0;
    clearPackets();
    setPipelineActive(scenario === "analysis" ? 0 : -1);
    const meter = el("ch-viz-order-meter");
    if (meter && scenario !== "analysis") meter.style.width = "8%";
    log(`— 场景: ${scenario} —`, false);
  }

  document.addEventListener("DOMContentLoaded", () => {
    drawStaticGraph();
    initEmergence();
    PIPELINE_STEPS.forEach((s, i) => {
      const wrap = el("ch-pipeline-steps");
      if (!wrap) return;
      const div = document.createElement("div");
      div.className = "ch-viz-step";
      div.dataset.step = s.key;
      div.innerHTML = `<strong>${s.title}</strong>${s.desc}`;
      wrap.appendChild(div);
    });
    setPipelineActive(0);

    el("ch-scenario")?.addEventListener("change", onScenarioChange);
    el("ch-play-toggle")?.addEventListener("click", () => {
      playing = !playing;
      const b = el("ch-play-toggle");
      if (b) b.textContent = playing ? "暂停" : "播放";
    });

    log("L3 信封: type / msg_id / vector_clock / ttl / idempotency_key", false);
    if (scenario === "analysis") runAnalysisBeat();
    rafId = requestAnimationFrame(tick);
  });
})();
