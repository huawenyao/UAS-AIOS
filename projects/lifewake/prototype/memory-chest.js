/* 空间互动：点地走路、拾物、投入窗台/裂隙/匣子。没有选项卡、没有系统菜单。 */
(function () {
  "use strict";

  var ITEMS = {
    item_moon_hairpin: {
      title: "月光发卡",
      relive: "dusk",
      rewrite: "dusk-fork",
      origin: true,
      home: "reality"
    },
    item_rain_scroll: {
      title: "雨夜爵士回响卷轴",
      relive: "rain",
      rewrite: "dusk-fork",
      origin: true,
      home: "reality"
    },
    item_city_compass: {
      title: "城市寻宝罗盘",
      relive: "city",
      rewrite: "city",
      origin: false,
      home: "fantasy"
    }
  };

  var PLACE_COPY = {
    hall: "你站在门厅中央。地面通向两扇看得见里面的门。脚边是匣子。",
    reality: "发卡和卷轴被玻璃罩着。把它们放到窗台上，就会重温；投进未写下的门，只打开平行世界。",
    fantasy: "罗盘没有玻璃罩。把它投入夜色城门，或叠到合成石上。",
    dusk: "你站在窗边。林妍把发卡别回耳侧，没有说话。空气里有一枚可拾的碎片。",
    rain: "雨打在玻璃上。杯沿还留着你随口哼出的三个音。",
    city: "罗盘停在「月光晚餐」与「心跳唱片」之间。巷口有一张未写完的菜单。",
    "dusk-fork": "她这次先开口，把发卡放回你掌心。原点仍在玻璃匣里。",
    fused: "发卡的月光落到寻宝图上。这是创作，不是原始记忆。"
  };

  var state = {
    place: "hall",
    holding: null,
    chestOpen: false,
    inChest: [],
    originPreserved: true,
    captured: []
  };

  var drag = { active: false, node: null, dx: 0, dy: 0 };

  function $(sel, root) {
    return (root || document).querySelector(sel);
  }
  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function whisper(text) {
    $("#whisper-text").textContent = text;
  }

  function toast(text) {
    var host = $("#toast-region");
    var node = document.createElement("div");
    node.className = "toast";
    node.textContent = text;
    host.appendChild(node);
    setTimeout(function () { node.remove(); }, 2800);
  }

  function warp(then) {
    var overlay = $("#warp");
    overlay.hidden = false;
    setTimeout(function () {
      overlay.hidden = true;
      if (then) then();
    }, 520);
  }

  function showPlace(place) {
    state.place = place;
    document.documentElement.setAttribute("data-place", place);
    $$("[data-place-panel]").forEach(function (panel) {
      panel.hidden = panel.getAttribute("data-place-panel") !== place;
    });
    var chamber = $("#hall-chamber");
    if (chamber) {
      chamber.classList.remove("is-entering-reality", "is-entering-fantasy");
    }
    whisper(PLACE_COPY[place] || "");
  }

  function walk(place) {
    if (place === "dormant") {
      whisper("这座翼还在生长。宫殿只在你真正留下记忆时向外展开。");
      return;
    }
    if (place === state.place) return;
    var chamber = $("#hall-chamber");
    if (chamber && state.place === "hall" && (place === "reality" || place === "fantasy")) {
      chamber.classList.add("is-entering-" + place);
    }
    warp(function () { showPlace(place); });
  }

  function setHolding(itemId, node) {
    state.holding = itemId;
    document.documentElement.setAttribute("data-holding", itemId || "");
    $$(".space-object").forEach(function (el) { el.classList.remove("is-held"); });
    if (itemId) {
      if (node) node.classList.add("is-held");
      $("#hand-hint").hidden = false;
      $("#hand-name").textContent = ITEMS[itemId] ? ITEMS[itemId].title : itemId;
      whisper("手里握着" + $("#hand-name").textContent + "。把它放到窗台、未写下的门、城门或匣子上。");
    } else {
      $("#hand-hint").hidden = true;
    }
  }

  function pick(itemId, node) {
    if (state.holding === itemId) {
      setHolding(null, null);
      return;
    }
    setHolding(itemId, node);
  }

  function dropOn(kind) {
    var itemId = state.holding;
    if (!itemId) {
      whisper("先拾起一件物。空着手推门，时空不会打开。");
      return false;
    }
    var spec = ITEMS[itemId];
    if (kind === "chest") {
      if (state.inChest.indexOf(itemId) === -1) state.inChest.push(itemId);
      openChest(true);
      renderChest();
      setHolding(null, null);
      toast(spec.title + " 被放进匣中");
      whisper("匣子是你的携带空间。下次可以从匣中再取出。");
      return true;
    }
    if (kind === "rift-relive") {
      setHolding(null, null);
      warp(function () { showPlace(spec.relive); });
      toast("重温「" + spec.title + "」· 原点只读");
      return true;
    }
    if (kind === "rift-rewrite") {
      if (spec.origin) {
        state.originPreserved = true;
        setHolding(null, null);
        warp(function () { showPlace(spec.rewrite); });
        toast("平行分支已打开。原点仍在玻璃匣里。");
        whisper("改写发生在未写下的门后。玻璃罩里的发卡与卷轴没有被覆盖。");
      } else {
        setHolding(null, null);
        warp(function () { showPlace(spec.relive); });
        whisper("幻想物本来就可改写，你走进了尚未写完的城。");
      }
      return true;
    }
    if (kind === "fuse") {
      fuseHeld();
      return true;
    }
    return false;
  }

  function fuseHeld() {
    var a = state.holding;
    if (!a) return;
    var other = a === "item_moon_hairpin" ? "item_city_compass" : "item_moon_hairpin";
    if (state.inChest.indexOf(other) === -1 && state.holding !== other) {
      whisper("把另一件物先放进匣子，或把发卡与罗盘叠在合成石上。");
      return;
    }
    state.originPreserved = true;
    setHolding(null, null);
    warp(function () { showPlace("fused"); });
    toast("跨界时空生成。这是创作，不是原始记忆。");
  }

  function capture(label) {
    var id = "capture_" + String(state.captured.length + 1);
    state.captured.push({ id: id, title: label });
    state.inChest.push(id);
    ITEMS[id] = { title: label, relive: state.place, rewrite: state.place, origin: false, home: "hall" };
    openChest(true);
    renderChest();
    toast("碎片「" + label + "」被抓进匣中");
    whisper("一次穿梭，无限产出。碎片已是可携带的新道具。");
  }

  function openChest(force) {
    state.chestOpen = force === undefined ? !state.chestOpen : force;
    $("#chest-visual").classList.toggle("is-open", state.chestOpen);
  }

  function renderChest() {
    var cavity = $("#chest-cavity");
    cavity.innerHTML = "";
    state.inChest.forEach(function (id) {
      var chip = document.createElement("button");
      chip.type = "button";
      chip.className = "space-object is-in-chest";
      chip.setAttribute("data-item", id);
      chip.textContent = (ITEMS[id] && ITEMS[id].title.charAt(0)) || "物";
      chip.setAttribute("aria-label", "从匣中取出 " + (ITEMS[id] ? ITEMS[id].title : id));
      chip.addEventListener("click", function (event) {
        event.stopPropagation();
        pick(id, chip);
      });
      cavity.appendChild(chip);
    });
  }

  function onPointerDown(event) {
    var node = event.currentTarget;
    var itemId = node.getAttribute("data-item");
    if (!itemId) return;
    pick(itemId, node);
    drag.active = true;
    drag.node = node;
    drag.dx = 0;
    drag.dy = 0;
    node.setPointerCapture(event.pointerId);
  }

  function onPointerMove(event) {
    if (!drag.active || !drag.node) return;
    drag.dx += event.movementX;
    drag.dy += event.movementY;
    drag.node.style.transform = "translate(" + drag.dx + "px," + drag.dy + "px)";
  }

  function onPointerUp(event) {
    if (!drag.active) return;
    var target = null;
    if (drag.node) {
      drag.node.style.pointerEvents = "none";
      target = document.elementFromPoint(event.clientX, event.clientY);
      drag.node.style.pointerEvents = "";
      drag.node.style.transform = "";
    }
    drag.active = false;
    drag.node = null;
    var zone = target && target.closest("[data-drop]");
    if (zone) dropOn(zone.getAttribute("data-drop"));
  }

  function lookAround(event) {
    if (state.place !== "hall" || drag.active) return;
    var chamber = $("#hall-chamber");
    if (!chamber) return;
    var x = (event.clientX / window.innerWidth - 0.5) * 28;
    var y = (event.clientY / window.innerHeight - 0.5) * 16;
    chamber.style.setProperty("--look-x", String(-x));
    chamber.style.setProperty("--look-y", String(-y));
  }

  function bind() {
    $$("[data-walk]").forEach(function (btn) {
      btn.addEventListener("click", function () { walk(btn.getAttribute("data-walk")); });
    });
    $$("[data-item]").forEach(function (obj) {
      obj.addEventListener("pointerdown", onPointerDown);
      obj.addEventListener("pointermove", onPointerMove);
      obj.addEventListener("pointerup", onPointerUp);
      obj.addEventListener("dblclick", function () {
        var spec = ITEMS[obj.getAttribute("data-item")];
        if (spec) {
          setHolding(null, null);
          warp(function () { showPlace(spec.relive); });
        }
      });
    });
    $("#treasure-chest").addEventListener("click", function (event) {
      if (event.target.closest("[data-item]")) return;
      if (state.holding) {
        dropOn("chest");
        return;
      }
      openChest();
      whisper(state.chestOpen ? "匣盖打开。里面是你携带的时空锚点。" : "匣盖合上。物还在，只是暂时看不见。");
    });
    $$("[data-drop]").forEach(function (zone) {
      zone.addEventListener("click", function (event) {
        if (state.holding) {
          event.preventDefault();
          dropOn(zone.getAttribute("data-drop"));
        }
      });
    });
    $$("[data-capture]").forEach(function (shard) {
      shard.addEventListener("click", function () {
        capture(shard.getAttribute("data-capture"));
        shard.hidden = true;
      });
    });
    document.addEventListener("pointermove", lookAround);
  }

  bind();
  showPlace("hall");
})();
