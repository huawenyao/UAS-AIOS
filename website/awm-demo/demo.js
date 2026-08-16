(function () {
  const data = window.AWM_DEMO;
  if (!data) {
    document.getElementById("highlight").textContent = "请先运行 python3 scripts/awm_demo_loop.py";
    return;
  }

  const beats = data.beats;
  const nav = document.getElementById("beats");
  const body = document.getElementById("beat-body");
  const highlight = document.getElementById("highlight");
  const explain = document.getElementById("explain-list");
  const skuPill = document.getElementById("sku-pill");
  const sitId = document.getElementById("sit-id");
  const sitGap = document.getElementById("sit-gap");
  const chips = document.getElementById("intent-chips");
  const trayStatus = document.getElementById("tray-status");
  const trayMeta = document.getElementById("tray-meta");
  const btnMain = document.getElementById("btn-main");
  const toast = document.getElementById("toast");
  const labels = ["匹配", "看见", "意图", "计划", "推演", "门控", "回看"];
  let index = 0;
  let approved = false;

  skuPill.textContent = "SKU · " + String(data.match.sku).toUpperCase();
  sitId.textContent = beats[1].situation;
  sitGap.textContent = beats[1].gaps[0];
  const intent = beats[2].intent;
  chips.innerHTML = Object.entries(intent.constraints)
    .map(function (entry) {
      return "<span>" + entry[0] + " " + entry[1] + "</span>";
    })
    .join("");

  beats.forEach(function (beat, i) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = i + 1 + " " + labels[i];
    button.dataset.index = String(i);
    button.addEventListener("click", function () {
      show(i);
    });
    nav.appendChild(button);
  });

  function riskClass(risk) {
    return risk === "low" ? "risk-low" : "risk-medium";
  }

  function render(beat) {
    if (beat.id === "match") {
      return (
        "<div class='card'><p>五问已答。推荐 Domain Pack <code>" +
        beat.domain_pack +
        "</code>，UX 模式 <code>" +
        beat.ux_mode +
        "</code>。</p><ul>" +
        beat.reasons.map(function (r) { return "<li>" + r + "</li>"; }).join("") +
        "</ul></div>"
      );
    }
    if (beat.id === "lens") {
      const f = beat.facts;
      return (
        "<div class='card'><p>在手 <span class='metric'>" +
        f.on_hand +
        "</span> · 在途 " +
        f.inbound +
        " · 需求 14d " +
        f.forecast_demand_14d +
        "</p><p>缺货风险 <strong class='risk-medium'>" +
        Math.round(f.stockout_risk * 100) +
        "%</strong>，阈值 5%。</p></div>"
      );
    }
    if (beat.id === "intent") {
      return (
        "<div class='card'><p>" +
        beat.intent.goal +
        "</p><p class='muted'>成功度量 " +
        beat.intent.success_metric +
        "</p></div>"
      );
    }
    if (beat.id === "plan") {
      const ops = beat.operations
        .map(function (op, i) {
          const pol = beat.policy.steps[i];
          return (
            "<div class='card op'><div><code>" +
            op.action +
            "</code><div class='muted'>" +
            pol.kind +
            "</div></div><span class='" +
            riskClass(pol.risk) +
            "'>" +
            pol.decision +
            "</span></div>"
          );
        })
        .join("");
      return "<div class='ops'>" + ops + "</div>";
    }
    if (beat.id === "stage") {
      return (
        "<div class='split'><div class='card'><div class='k'>Now</div><div class='metric'>" +
        beat.now.on_hand +
        "</div><p>风险 " +
        Math.round(beat.now.stockout_risk * 100) +
        "%</p></div><div class='card maybe'><div class='k'>Maybe</div><div class='metric'>" +
        beat.maybe.expected_on_hand +
        "</div><p>风险 " +
        Math.round(beat.maybe.stockout_risk * 100) +
        "%</p></div></div><p class='ribbon'>仿真未写入 · writes_facts=" +
        beat.writes_facts +
        "</p>"
      );
    }
    if (beat.id === "gate") {
      const blocked = beat.blocked.status;
      const committed = approved ? beat.committed.status : "blocked";
      return (
        "<div class='card'><p>未批准：<code>" +
        blocked +
        "</code></p><p>当前写回：<code>" +
        committed +
        "</code></p><p class='muted'>采购数量 80 · 金额 6,400 · 可回滚 cancel_purchase_order</p></div>"
      );
    }
    const obs = beat.observe;
    return (
      "<div class='split'><div class='card maybe'><div class='k'>预测</div><div class='metric'>" +
      Math.round(obs.predicted.stockout_risk * 100) +
      "%</div></div><div class='card'><div class='k'>观测</div><div class='metric'>" +
      Math.round(obs.actual.stockout_risk * 100) +
      "%</div></div></div><p>校准 " +
      (obs.calibrated ? "通过" : "未通过") +
      " · DIKW publishable=" +
      beat.dikw.publishable +
      "</p>"
    );
  }

  function explainFor(beat) {
    if (beat.id === "observe") {
      return [
        "S 因为 " + beat.explain.situation,
        "I 因为 " + beat.explain.intent,
        "O 所以 " + beat.explain.operations.join(" → "),
        "W 观测校准 " + (beat.observe.calibrated ? "通过" : "未通过"),
      ];
    }
    if (beat.id === "plan") {
      return ["动作来自注册表", "未注册动作将被拒绝", "采购单 risk=medium → escalate"];
    }
    if (beat.id === "stage") {
      return ["PREDICT 与事实分离", "expected_on_hand 仅存在于 Maybe 栏"];
    }
    return [beat.highlight];
  }

  const mains = ["进入世界", "解释这个对象", "生成计划", "演一遍", "提交审批", "批准写回", "结束本轮"];

  function show(i) {
    index = i;
    const beat = beats[i];
    document.body.dataset.beat = beat.id;
    highlight.textContent = beat.highlight;
    body.innerHTML = render(beat);
    explain.innerHTML = explainFor(beat)
      .map(function (item) {
        return "<li>" + item + "</li>";
      })
      .join("");
    btnMain.textContent = mains[i];
    Array.prototype.forEach.call(nav.querySelectorAll("button"), function (el, idx) {
      el.classList.toggle("is-active", idx === i);
    });
    if (beat.id === "gate") {
      trayStatus.textContent = approved ? "committed" : "blocked · 待审批";
      trayMeta.textContent = "sku:A · wh:W1 · qty 80";
    } else if (beat.id === "observe") {
      trayStatus.textContent = "已回看";
      trayMeta.textContent = "预测未当作事实写入";
    } else {
      trayStatus.textContent = "尚未提交";
      trayMeta.textContent = "";
    }
  }

  btnMain.addEventListener("click", function () {
    const beat = beats[index];
    if (beat.id === "gate" && !approved) {
      approved = true;
      show(index);
      return;
    }
    if (index < beats.length - 1) show(index + 1);
  });

  document.getElementById("btn-illegal").addEventListener("click", function () {
    const message = beats[3].type_error || "unregistered action";
    toast.hidden = false;
    toast.textContent = message;
    setTimeout(function () {
      toast.hidden = true;
    }, 2800);
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-role]"), function (el) {
    el.addEventListener("click", function () {
      document.body.dataset.role = el.dataset.role;
      Array.prototype.forEach.call(document.querySelectorAll("[data-role]"), function (btn) {
        btn.classList.toggle("is-active", btn === el);
      });
      if (el.dataset.role === "approver") show(5);
    });
  });

  document.getElementById("fab-chat").addEventListener("click", function () {
    const chat = document.getElementById("chat");
    chat.hidden = !chat.hidden;
  });

  show(0);
})();
