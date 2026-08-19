/* LifeWake 时空记忆匣前端。无外部依赖；状态在内存中模拟引擎不变量。 */
(function () {
  "use strict";

  var SEED = {
    items: [
      {
        item_id: "item_moon_hairpin",
        item_type: "character",
        title: "月光发卡",
        vessel: "人物信物",
        glyph: "钗",
        inscription: "她侧脸被月光镀亮的那一夜",
        is_real_memory: true,
        layer: "real_memory",
        wing: "现实记忆层",
        room: "林妍专属锚点",
        grown: true,
        sceneTitle: "黄昏窗边",
        opening: "窗玻璃上还留着傍晚的暖色。林妍把发卡别回耳侧，没有说话，只是看向你。"
      },
      {
        item_id: "item_rain_scroll",
        item_type: "story",
        title: "雨夜爵士回响卷轴",
        vessel: "剧情卷轴",
        glyph: "卷",
        inscription: "你无意识哼出的动机，被编成只属于你的爵士",
        is_real_memory: true,
        layer: "real_memory",
        wing: "现实记忆层",
        room: "人生展厅",
        grown: false,
        sceneTitle: "雨夜咖啡馆",
        opening: "雨点打在窗外。你随口哼出的三个音，在空气里慢慢长成一段爵士主题。"
      },
      {
        item_id: "item_city_compass",
        item_type: "scene",
        title: "城市寻宝罗盘",
        vessel: "场景罗盘",
        glyph: "盘",
        inscription: "把一次尚未发生的约会，折进可穿梭的夜色地图",
        is_real_memory: false,
        layer: "fantasy",
        wing: "幻想故事层",
        room: "创世工坊",
        grown: false,
        sceneTitle: "夜色寻宝图",
        opening: "罗盘指针停在「月光晚餐」与「心跳唱片」之间。这座城还没有被写完。"
      }
    ]
  };

  var state = {
    view: "palace",
    selected: "item_moon_hairpin",
    mode: "relive",
    items: SEED.items.slice(),
    log: [],
    originPreserved: true
  };

  function $(id) {
    return document.getElementById(id);
  }

  function selectedItem() {
    return state.items.filter(function (item) {
      return item.item_id === state.selected;
    })[0];
  }

  function log(message) {
    state.log.unshift(message);
    renderLog();
  }

  function setView(view) {
    state.view = view;
    ["palace", "chest", "shuttle"].forEach(function (name) {
      $( "view-" + name ).setAttribute("aria-pressed", String(view === name));
      $(name + "-root").hidden = view !== name;
    });
    $("primary-title").textContent = {
      palace: "记忆宫殿",
      chest: "智能百宝箱",
      shuttle: "时空穿梭机"
    }[view];
    $("primary-hint").textContent = {
      palace: "四层私有空间。高权重信物会在对应翼里长出专属锚点，不会全量重建宫殿。",
      chest: "一切可物品化。道具不是装饰，而是故事的物理锚点，携带完整溯源元数据。",
      shuttle: "正向：点击道具进入原生时空。反向：在场景中抓取片段，封装为新道具。"
    }[view];
  }

  function renderPalace() {
    var wings = {};
    state.items.forEach(function (item) {
      wings[item.wing] = wings[item.wing] || [];
      wings[item.wing].push(item);
    });
    $("palace-root").innerHTML = Object.keys(wings).map(function (wing) {
      var rooms = wings[wing].map(function (item) {
        return (
          '<button class="room-chip' + (item.grown ? " grown" : "") + '" data-select="' + item.item_id + '" type="button">' +
          "<strong>" + item.room + "</strong><span>" + item.title + "</span></button>"
        );
      }).join("");
      return '<div class="wing"><div class="wing-title">' + wing + '</div><div class="rooms">' + rooms + "</div></div>";
    }).join("");
  }

  function renderChest() {
    $("chest-root").innerHTML =
      '<div class="chest-list">' +
      state.items.map(function (item) {
        return (
          '<button class="item-card" type="button" data-select="' + item.item_id + '" aria-pressed="' +
          String(item.item_id === state.selected) + '">' +
          '<span class="vessel" aria-hidden="true">' + item.glyph + "</span>" +
          "<span><strong>" + item.title + "</strong><div class='meta'>" + item.inscription + "</div></span>" +
          '<span class="badge ' + (item.is_real_memory ? "real" : "fantasy") + '">' +
          (item.is_real_memory ? "原始记忆" : "幻想/平行") +
          "</span></button>"
        );
      }).join("") +
      "</div>";
  }

  function renderDetail() {
    var item = selectedItem();
    if (!item) {
      $("item-detail").textContent = "";
      return;
    }
    $("item-detail").innerHTML =
      "<p><strong>" + item.title + "</strong> · " + item.vessel + "</p>" +
      "<p class='meta'>item_type=" + item.item_type +
      " · layer=" + item.layer +
      " · is_real_memory=" + item.is_real_memory + "</p>" +
      "<p class='meta'>溯源：场景「" + item.sceneTitle + "」可被穿梭、抓取、封存，但不能覆盖原点。</p>";
  }

  function renderLog() {
    $("event-log").innerHTML = state.log.slice(0, 8).map(function (line) {
      return "<li>" + line + "</li>";
    }).join("");
  }

  function renderScene(opening) {
    var item = selectedItem();
    $("scene-kicker").textContent = item.vessel + " · " + (state.mode === "relive" ? "重温" : "平行分支");
    $("scene-title").textContent = item.sceneTitle;
    $("scene-opening").textContent = opening || item.opening;
  }

  function selectItem(itemId) {
    state.selected = itemId;
    renderChest();
    renderDetail();
    renderScene();
    log("选中道具：" + selectedItem().title);
  }

  function shuttle() {
    var item = selectedItem();
    if (state.mode === "relive") {
      renderScene(item.opening);
      log("重温「" + item.title + "」。原始时间线只读，未写入图谱。");
      return;
    }
    if (item.is_real_memory) {
      var child = {
        item_id: item.item_id + "_fork_" + String(state.items.length),
        item_type: item.item_type,
        title: item.title + " · 平行分支",
        vessel: item.vessel,
        glyph: item.glyph,
        inscription: "她这次先开口，把发卡放回你掌心。",
        is_real_memory: false,
        layer: "fantasy",
        wing: "幻想故事层",
        room: "跨界桥",
        grown: false,
        sceneTitle: item.sceneTitle + " · 平行宇宙",
        opening: "平行分支已打开。原点「" + item.title + "」完整保留，互不覆盖。"
      };
      state.items.push(child);
      state.selected = child.item_id;
      state.originPreserved = true;
      renderPalace();
      renderChest();
      renderDetail();
      renderScene(child.opening);
      log("改写采用写时复制。子道具 " + child.title + " 已存入幻想层。");
      return;
    }
    renderScene(item.opening + " 故事在幻想层继续生长。");
    log("幻想层允许续写，仍不触碰现实记忆库。");
  }

  function capture() {
    var item = selectedItem();
    var gem = {
      item_id: "item_capture_" + String(state.items.length),
      item_type: "emotion",
      title: item.title + " · 新片段",
      vessel: "情绪宝石",
      glyph: "晶",
      inscription: "从当前场景抓取的可携带片段",
      is_real_memory: false,
      layer: "fantasy",
      wing: "幻想故事层",
      room: "跨界桥",
      grown: false,
      sceneTitle: "抓取后的私有片段",
      opening: "一键封装完成。新道具进入百宝箱，宫殿库存被扩容，原点仍在。"
    };
    state.items.push(gem);
    state.selected = gem.item_id;
    renderPalace();
    renderChest();
    setView("chest");
    renderDetail();
    log("反向封装：场景 → 新物品「" + gem.title + "」。");
  }

  function fuse() {
    var fused = {
      item_id: "item_fused_city_hairpin",
      item_type: "scene",
      title: "林妍走进夜色寻宝图",
      vessel: "场景罗盘",
      glyph: "界",
      inscription: "真实信物与幻想罗盘合成后，必须标注为派生创作",
      is_real_memory: false,
      layer: "fantasy",
      wing: "幻想故事层",
      room: "跨界桥",
      grown: false,
      sceneTitle: "跨界夜图",
      opening: "发卡的月光落到寻宝图上。这是创作，不是原始记忆。"
    };
    state.items.push(fused);
    state.selected = fused.item_id;
    renderPalace();
    renderChest();
    renderDetail();
    renderScene(fused.opening);
    setView("shuttle");
    log("融合完成。真实记忆标记被降为 false，防止认知混淆。");
  }

  function onClick(event) {
    var target = event.target.closest("[data-select]");
    if (target) {
      selectItem(target.getAttribute("data-select"));
      if (state.view === "palace") setView("chest");
    }
  }

  $("view-palace").addEventListener("click", function () { setView("palace"); });
  $("view-chest").addEventListener("click", function () { setView("chest"); });
  $("view-shuttle").addEventListener("click", function () { setView("shuttle"); renderScene(); });
  $("shuttle-trigger").addEventListener("click", shuttle);
  $("capture-trigger").addEventListener("click", capture);
  $("fuse-trigger").addEventListener("click", fuse);
  document.querySelectorAll("input[name='mode']").forEach(function (input) {
    input.addEventListener("change", function (event) {
      state.mode = event.target.value;
      $("mode-warning").textContent = state.mode === "relive"
        ? "重温不会改写原始记忆。改写将复制子图，原点完整保留。"
        : "改写模式会生成平行宇宙。原始发卡、雨夜卷轴不会被覆盖。";
    });
  });
  $("palace-root").addEventListener("click", onClick);
  $("chest-root").addEventListener("click", onClick);

  renderPalace();
  renderChest();
  renderDetail();
  log("三件初始道具已锚定：月光发卡、雨夜爵士回响卷轴、城市寻宝罗盘。");
  setView("palace");
})();
