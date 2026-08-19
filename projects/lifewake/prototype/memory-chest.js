/* 空间互动：走门、拾物、投入裂隙/匣子/另一件物。没有选项卡。 */
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
    hall: ["记忆宫殿 · 门厅", "你站在自己的精神家园里", "四扇门通向不同时空。拾起匣中或翼里的物，投进窗台或裂隙。"],
    reality: ["现实记忆层", "原始记忆被玻璃罩着", "把发卡或卷轴放到窗台上重温；投进未写下的门，只生成平行世界。"],
    fantasy: ["幻想故事层", "这座城还没有写完", "罗盘没有玻璃罩。把它叠到真实信物上，会走出跨界时空。"],
    dusk: ["黄昏窗边", "重温 · 原点只读", "窗玻璃上还留着傍晚的暖色。空气里有一枚可拾取的碎片。"],
    rain: ["雨夜咖啡馆", "重温 · 原点只读", "雨点打在窗外。把杯沿的余韵拾起，丢进百宝箱。"],
    city: ["夜色寻宝图", "幻想可改写", "罗盘指向尚未发生的约会。抓取巷口那张未写完的菜单。"],
    "dusk-fork": ["黄昏窗边 · 平行分支", "改写已发生，原点仍在", "她这次先开口。玻璃匣里的发卡没有被覆盖。"],
    fused: ["跨界夜图", "创作，不是原始记忆", "发卡的月光落到寻宝图上。这是派生时空。"]
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
    $("whisper-text").textContent = text;
  }

  function toast(text) {
    var host = $("toast-region");
    var node = document.createElement("div");
    node.className = "toast";
    node.textContent = text;
    host.appendChild(node);
    setTimeout(function () { node.remove(); }, 2800);
  }

  function warp(then) {
    var overlay = $("warp");
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
    var copy = PLACE_COPY[place];
    $("place-kicker").textContent = copy[0];
    $("place-title").textContent = copy[1];
    whisper(copy[2]);
  }

  function walk(place) {
    if (place === "dormant") {
      whisper("这座翼还在生长。宫殿只在你真正留下记忆时向外展开，不会凭空长出大厅。");
      return;
    }
    warp(function () { showPlace(place); });
  }

  function setHolding(itemId, node) {
    state.holding = itemId;
    document.documentElement.setAttribute("data-holding", itemId || "");
    $$(".space-object").forEach(function (el) { el.classList.remove("is-held"); });
    if (itemId) {
      if (node) node.classList.add("is-held");
      $("hand-hint").hidden = false;
      $("hand-name").textContent = ITEMS[itemId] ? ITEMS[itemId].title : itemId;
      whisper("手里握着" + $("hand-name").textContent + "。把它放到窗台、裂隙、未写下的门，或另一件物上。");
    } else {
      $("hand-hint").hidden = true;
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
      whisper("先拾起一件物。空着手推门，门不会为你打开时空。");
      return false;
    }
    var spec = ITEMS[itemId];
    if (kind === "chest") {
      if (state.inChest.indexOf(itemId) === -1) state.inChest.push(itemId);
      openChest(true);
      renderChest();
      setHolding(null, null);
      toast(spec.title + " 被放进匣中");
      whisper("匣子是你的携带空间。下次穿梭，可以从匣中再取出。");
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
    $("chest-visual").classList.toggle("is-open", state.chestOpen);
  }

  function renderChest() {
    var cavity = $("chest-cavity");
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
    $("treasure-chest").addEventListener("click", function (event) {
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
  }

  bind();
  showPlace("hall");
})();
