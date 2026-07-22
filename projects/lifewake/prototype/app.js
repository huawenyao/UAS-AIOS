(() => {
  "use strict";

  const sceneData = {
    surprise: {
      label: "惊喜时刻",
      title: "今晚，给{person}一个惊喜",
      subtitle: "让记忆、时间和你的亲笔表达，在黄昏里相遇。",
      note: "黄昏留在窗边，桌上的每件物，都在等你的选择。",
      whisper: "先从你最想让她感受到的那一刻开始。选择始终属于你。",
      suggestion: "从礼物盒选择一条叙事线，再放入只属于你们的细节。",
      atmosphere: "warm",
    },
    distance: {
      label: "异地共鸣",
      title: "让距离，听见{person}的回响",
      subtitle: "用同一段旋律、同一个时刻，让两处空间短暂重叠。",
      note: "窗外很远，桌上的旋律可以把两个夜晚放在一起。",
      whisper: "不必填满沉默。挑一段共同记忆，让它成为远方的轻敲。",
      suggestion: "建议先选择旋律和一个彼此都从容的共鸣时刻。",
      atmosphere: "moon",
    },
    family: {
      label: "家庭纪念",
      title: "把一家人的重要时刻，轻轻留住",
      subtitle: "照片、手写话与家里的光，共同组成一页家庭纪念。",
      note: "旧照片在木桌上摊开，时间不是倒数，而是一种相聚。",
      whisper: "纪念不是复刻过去，而是确认此刻仍愿意彼此靠近。",
      suggestion: "建议展开照片堆，选择一段适合全家共同回看的记忆。",
      atmosphere: "warm",
    },
    self: {
      label: "我的此刻",
      title: "为此刻的自己，留一小块安静",
      subtitle: "不必完成什么。听一段旋律，写下真实感受，就已经足够。",
      note: "桌面暂时不为任何任务服务，只承接你现在的状态。",
      whisper: "你不需要把感受解释完整。先选择一种让身体舒展的光。",
      suggestion: "建议从氛围灯开始，也可以什么都不安排。",
      atmosphere: "stars",
    },
  };

  const subjects = [
    { id: "wife", name: "妻子 · 林妍", person: "她", relation: "彼此选择的伴侣", hint: "关注她，也尊重她未被读取的内心。" },
    { id: "self", name: "自己 · 此刻的我", person: "自己", relation: "自我关照", hint: "把注意力从完成任务转回真实感受。" },
    { id: "parents", name: "父母", person: "他们", relation: "家庭来处", hint: "以共同记忆连接，不推断他们的需要。" },
    { id: "friend", name: "挚友 · 周屿", person: "他", relation: "长久的同行者", hint: "留一点轻松，也留一点真诚。" },
  ];

  const plans = [
    {
      id: "moon-dinner", symbol: "◐", title: "月光晚餐", color: "#7787a5",
      description: "把熟悉的家变成一段缓慢展开的月色叙事。",
      details: ["暖光入场", "一首共同旋律", "餐后亲笔信"],
    },
    {
      id: "city-hunt", symbol: "⌖", title: "城市寻宝", color: "#bb7a45",
      description: "沿着共同记忆留下三枚线索，让城市替你们叙旧。",
      details: ["三张记忆卡", "一处会合时刻", "终点礼物"],
    },
    {
      id: "heartbeat-record", symbol: "◎", title: "心跳唱片", color: "#b4564e",
      description: "把你选的记忆与表达，编成一张只播放一次的唱片。",
      details: ["主题旋律", "记忆采样", "蜡封唱片词"],
    },
  ];

  const memories = [
    { id: "rain", title: "雨停后的那碗面", date: "2022 · 杭州", bg: "linear-gradient(135deg,#687b7d,#d2a16d 58%,#65443a)" },
    { id: "coast", title: "在海边走得很慢", date: "2023 · 平潭", bg: "linear-gradient(135deg,#73939d,#e8c88d 55%,#8c674f)" },
    { id: "home", title: "新家第一盏灯", date: "2024 · 我们家", bg: "linear-gradient(135deg,#796353,#e6b66f 52%,#6a7d68)" },
  ];

  const initialState = {
    subject: "wife",
    scene: "surprise",
    plan: null,
    musicPlaying: false,
    selectedMemories: [],
    time: "20:30",
    letter: "",
    sealed: false,
    atmosphere: "warm",
    positions: {},
    rehearsalStep: 0,
    revoked: false,
  };

  const loadState = () => {
    try {
      return { ...initialState, ...JSON.parse(sessionStorage.getItem("lifewake-state") || "{}"), musicPlaying: false };
    } catch {
      return { ...initialState };
    }
  };

  const state = loadState();
  let audio = { context: null, timer: null, nodes: [] };
  let drag = null;

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const currentSubject = () => subjects.find((item) => item.id === state.subject) || subjects[0];
  const currentScene = () => sceneData[state.scene] || sceneData.surprise;
  const currentPlan = () => plans.find((item) => item.id === state.plan);
  const saveState = () => {
    try { sessionStorage.setItem("lifewake-state", JSON.stringify(state)); } catch { /* private session fallback */ }
  };
  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;",
  })[char]);

  const toast = (message) => {
    const region = $("#toast-region");
    const item = document.createElement("div");
    item.className = "toast";
    item.textContent = message;
    region.append(item);
    window.setTimeout(() => item.remove(), 3600);
  };

  const whisper = (message) => {
    const host = $("#whisper");
    $("#whisper-text").textContent = message;
    host.classList.remove("is-updating");
    requestAnimationFrame(() => host.classList.add("is-updating"));
  };

  const completion = () => {
    let score = 12;
    if (state.plan) score += 25;
    if (state.selectedMemories.length) score += Math.min(18, state.selectedMemories.length * 6);
    if (state.time) score += 10;
    if (state.musicPlaying) score += 8;
    if (state.letter.trim()) score += 15;
    if (state.sealed) score += 12;
    return Math.min(100, score);
  };

  const renderContext = () => {
    const subject = currentSubject();
    const scene = currentScene();
    $("#subject-label").textContent = subject.name;
    $("#frame-name").textContent = state.subject === "wife" ? "林妍" : subject.name.split(" · ")[0];
    $("#frame-relation").textContent = subject.relation;
    $("#scene-kicker").textContent = scene.label;
    $("#scene-title").textContent = scene.title.replace("{person}", subject.person);
    $("#scene-subtitle").textContent = scene.subtitle;
    $("#space-note").textContent = scene.note;
    $("#boundary-beneficiary").textContent = state.subject === "wife" ? "林妍与你" : `${subject.name}与这段关系`;
    const materials = [];
    if (state.plan) materials.push(`策展方案「${currentPlan().title}」`);
    if (state.selectedMemories.length) materials.push(`${state.selectedMemories.length} 段共同记忆`);
    if (state.letter.trim()) materials.push("你的亲笔表达");
    materials.push(`今晚 ${state.time} 的时间决定`);
    $("#boundary-materials").textContent = state.revoked ? "已撤回本次策展材料" : materials.join("、");
    document.documentElement.dataset.atmosphere = state.atmosphere;
    document.documentElement.dataset.subject = state.subject;
    document.title = `LifeWake · ${scene.label}`;
  };

  const renderObjectStates = () => {
    const plan = currentPlan();
    $("#gift-visual").classList.toggle("is-open", Boolean(plan));
    $("#gift-label").textContent = plan ? `已策展 · ${plan.title}` : "惊喜策展台";
    $(".gramophone-object").classList.toggle("is-playing", state.musicPlaying);
    $("#music-label").textContent = state.musicPlaying ? "主题旋律 · 正在回响" : "主题旋律 · 静候";
    $("#photos-label").textContent = `共同记忆 · ${state.selectedMemories.length}/3`;
    $("#clock-label").textContent = `今晚 · ${state.time}`;
    $("#envelope-visual").classList.toggle("is-sealed", state.sealed);
    $("#envelope-label").textContent = state.sealed ? "已封缄 · 只待亲手交付" : state.letter ? "信已写好 · 等你封缄" : "一封未封缄的信";
    const atmosphereNames = { warm: "暖光", moon: "月光", stars: "星光" };
    $("#lamp-label").textContent = atmosphereNames[state.atmosphere];
    $("#notebook-label").textContent = `策展手册 · ${completion()}%`;
  };

  const renderPositions = () => {
    Object.entries(state.positions).forEach(([object, position]) => {
      const element = $(`[data-object="${object}"]`);
      if (element && position) {
        element.style.left = `${position.x}px`;
        element.style.top = `${position.y}px`;
        element.style.setProperty("--x", "0px");
        element.style.setProperty("--y", "0px");
      }
    });
  };

  const renderAll = () => {
    renderContext();
    renderObjectStates();
    renderPositions();
  };

  const drawerTemplates = {
    portrait: () => {
      const subject = currentSubject();
      const isWife = state.subject === "wife";
      return `
        <span class="drawer-kicker">关系焦点 · 不是人物画像</span>
        <h2 id="drawer-title">${escapeHtml(subject.name)}</h2>
        <p>${escapeHtml(subject.hint)}</p>
        <div class="drawer-section">
          <h3>此刻的关系定位</h3>
          <div class="relation-lines">
            <div class="relation-line"><span>关系</span><strong>${escapeHtml(subject.relation)}</strong></div>
            <div class="relation-line"><span>当前情景</span><strong>${escapeHtml(currentScene().label)}</strong></div>
            <div class="relation-line"><span>你的意图</span><strong>${isWife ? "让她感到被认真珍惜" : "用真实的在意连接彼此"}</strong></div>
          </div>
        </div>
        <div class="drawer-section">
          <p class="drawer-note">LifeWake 只组织你主动提供的关系材料。它不监控、不评分，也不推断对方没有表达的情绪。</p>
        </div>`;
    },
    photos: () => `
      <span class="drawer-kicker">可选择的策展材料</span>
      <h2 id="drawer-title">共同记忆</h2>
      <p>展开一段你们都拥有的过去。选中只代表放入本次策展，不改变原始照片。</p>
      <div class="drawer-section memory-list">
        ${memories.map((memory) => `
          <button class="memory-card ${state.selectedMemories.includes(memory.id) ? "is-selected" : ""}" type="button" data-memory="${memory.id}">
            <span class="memory-thumb" style="--memory-bg:${memory.bg}"></span>
            <span><strong>${memory.title}</strong><small>${memory.date}</small></span><i aria-hidden="true"></i>
          </button>`).join("")}
      </div>`,
    clock: () => `
      <span class="drawer-kicker">Timing decision · 不制造焦虑</span>
      <h2 id="drawer-title">今晚，什么时候发生？</h2>
      <p>选择一个你们都能放松进入的时刻。时间是仪式的容器，不是倒数。</p>
      <div class="drawer-section">
        <div class="time-options">
          ${["19:30", "20:30", "21:15"].map((time) => `<button class="time-option ${state.time === time ? "is-active" : ""}" type="button" data-time="${time}">${time}</button>`).join("")}
        </div>
        <div class="timing-decision"><strong>当前决定：今晚 ${state.time}</strong><br>建议在前后各留十五分钟空白，不安排提醒轰炸。</div>
      </div>`,
    envelope: () => `
      <span class="drawer-kicker">你的表达 · AI 不代写</span>
      <h2 id="drawer-title">写给${state.subject === "wife" ? "林妍" : currentSubject().person}的话</h2>
      <p>可以不漂亮，但要是你的。策展低语只提供方向，不生成替你署名的句子。</p>
      <div class="drawer-section">
        <label for="letter-input" class="eyebrow">亲笔表达</label>
        <textarea id="letter-input" class="letter-textarea" maxlength="220" placeholder="从一个真实的瞬间开始……" ${state.sealed ? "disabled" : ""}>${escapeHtml(state.letter)}</textarea>
        <div class="letter-meta"><span>温和提示：说一件具体的小事</span><span id="letter-count">${state.letter.length} / 220</span></div>
        ${state.sealed
          ? `<div class="seal-status">蜡封已落下。文字不会再被自动修改。</div><button class="secondary-action" id="unseal-letter" type="button">由我亲手拆封修改</button>`
          : `<button class="primary-action" id="seal-letter" type="button" ${state.letter.trim() ? "" : "disabled"}>确认文字，并落下蜡封</button>`}
      </div>`,
    lamp: () => `
      <span class="drawer-kicker">空间气息</span>
      <h2 id="drawer-title">让光线先抵达</h2>
      <p>氛围不会替代真心，但能给真心一个更从容的落点。</p>
      <div class="drawer-section atmosphere-options">
        ${[
          ["warm", "暖光", "像家一样松弛"],
          ["moon", "月光", "安静、留白更多"],
          ["stars", "星光", "一点未知与仪式感"],
        ].map(([id, name, copy]) => `<button class="atmosphere-option ${state.atmosphere === id ? "is-active" : ""}" type="button" data-atmosphere="${id}"><strong>${name}</strong><br><small>${copy}</small></button>`).join("")}
      </div>`,
    notebook: () => {
      const progress = completion();
      return `
        <span class="drawer-kicker">今晚的策展结构</span>
        <h2 id="drawer-title">惊喜手册</h2>
        <div class="manual-progress">
          <div class="progress-ring" style="--progress:${progress}"><strong>${progress}%</strong></div>
          <p>${progress < 60 ? "骨架正在形成。你不必把每一项都填满。" : "仪式已经有了清晰轮廓，剩下的留给现场。"}</p>
        </div>
        <div class="chapter-list">
          ${manualChapters().map((chapter) => `
            <div class="chapter"><span class="chapter-mark">${chapter.phase}</span><span><strong>${chapter.title}</strong><small>${chapter.copy}</small></span><em>${chapter.done ? "已就绪" : "待选择"}</em></div>`).join("")}
        </div>
        <button class="primary-action" type="button" data-open-rehearsal>预演这份惊喜</button>`;
    },
  };

  const manualChapters = () => {
    const plan = currentPlan();
    const memory = memories.find((item) => state.selectedMemories.includes(item.id));
    return [
      { phase: "起", title: "空间先开口", copy: `${state.atmosphere === "moon" ? "月光" : state.atmosphere === "stars" ? "星光" : "暖光"}与主题旋律`, done: true },
      { phase: "承", title: "记忆被看见", copy: memory ? memory.title : "选择一段共同记忆", done: Boolean(memory) },
      { phase: "转", title: plan ? plan.title : "惊喜揭晓", copy: plan ? plan.description : "从礼物盒选择叙事线", done: Boolean(plan) },
      { phase: "合", title: "你的表达", copy: state.sealed ? "蜡封已落下" : "等待一封由你写下的信", done: state.sealed },
    ];
  };

  const openDrawer = (type) => {
    if (type === "music") { toggleMusic(); return; }
    if (type === "gift") { openGift(); return; }
    const template = drawerTemplates[type];
    if (!template) return;
    $("#drawer-content").innerHTML = template();
    $("#detail-drawer").classList.add("is-open");
    $("#detail-drawer").setAttribute("aria-hidden", "false");
    $("#drawer-scrim").classList.add("is-visible");
    bindDrawerInteractions(type);
    window.setTimeout(() => $(".drawer-close").focus(), 50);
  };

  const closeDrawer = () => {
    $("#detail-drawer").classList.remove("is-open");
    $("#detail-drawer").setAttribute("aria-hidden", "true");
    $("#drawer-scrim").classList.remove("is-visible");
  };

  const bindDrawerInteractions = (type) => {
    if (type === "photos") {
      $$("[data-memory]", $("#drawer-content")).forEach((button) => button.addEventListener("click", () => {
        const id = button.dataset.memory;
        state.selectedMemories = state.selectedMemories.includes(id)
          ? state.selectedMemories.filter((item) => item !== id)
          : [...state.selectedMemories, id];
        state.revoked = false;
        saveState(); renderObjectStates(); openDrawer("photos");
        whisper(state.selectedMemories.length ? "这段记忆已经放入桌面。它会作为线索，而不是答案。" : "记忆已从本次策展移出，原始材料没有改变。");
        toast(state.selectedMemories.includes(id) ? "已把这段记忆放入策展手册" : "已移出本次策展");
      }));
    }
    if (type === "clock") {
      $$("[data-time]", $("#drawer-content")).forEach((button) => button.addEventListener("click", () => {
        state.time = button.dataset.time;
        saveState(); renderObjectStates(); openDrawer("clock");
        whisper(`${state.time} 被写进手册。前后留白，惊喜才有呼吸。`);
        toast(`惊喜时刻已定为今晚 ${state.time}`);
      }));
    }
    if (type === "envelope") {
      const input = $("#letter-input");
      if (input) input.addEventListener("input", () => {
        state.letter = input.value;
        state.revoked = false;
        $("#letter-count").textContent = `${state.letter.length} / 220`;
        $("#seal-letter").disabled = !state.letter.trim();
        saveState(); renderObjectStates();
      });
      $("#seal-letter")?.addEventListener("click", () => {
        if (!state.letter.trim()) return;
        state.sealed = true; saveState(); renderObjectStates(); openDrawer("envelope");
        whisper("蜡封已经落下。最后一句仍然完全属于你。");
        toast("信已封缄，文字不会被自动改写");
      });
      $("#unseal-letter")?.addEventListener("click", () => {
        state.sealed = false; saveState(); renderObjectStates(); openDrawer("envelope");
        toast("已由你主动拆封，可以继续修改");
      });
    }
    if (type === "lamp") {
      $$("[data-atmosphere]", $("#drawer-content")).forEach((button) => button.addEventListener("click", () => {
        state.atmosphere = button.dataset.atmosphere;
        saveState(); renderContext(); renderObjectStates(); openDrawer("lamp");
        const name = button.querySelector("strong").textContent;
        whisper(`${name}已经铺开。看看桌上的物件是否更接近你想要的感觉。`);
        toast(`空间已切换为${name}`);
      }));
    }
    $("[data-open-rehearsal]", $("#drawer-content"))?.addEventListener("click", openRehearsal);
  };

  const renderSelectors = () => {
    $("#subject-options").innerHTML = subjects.map((subject) => `
      <button class="choice-card ${state.subject === subject.id ? "is-active" : ""}" type="button" data-subject="${subject.id}">
        <strong>${subject.name}</strong><span>${subject.relation} · ${subject.hint}</span>
      </button>`).join("");
    $("#scene-options").innerHTML = Object.entries(sceneData).map(([id, scene]) => `
      <button class="choice-card ${state.scene === id ? "is-active" : ""}" type="button" data-scene="${id}">
        <strong>${scene.label}</strong><span>${scene.suggestion}</span>
      </button>`).join("");
  };

  const openGift = () => {
    $("#gift-visual").classList.add("is-open");
    $("#curation-plans").innerHTML = plans.map((plan) => `
      <button class="plan-card ${state.plan === plan.id ? "is-active" : ""}" style="--plan-color:${plan.color}" type="button" data-plan="${plan.id}">
        <span class="plan-symbol">${plan.symbol}</span><h3>${plan.title}</h3><p>${plan.description}</p>
        <ul>${plan.details.map((detail) => `<li>${detail}</li>`).join("")}</ul>
      </button>`).join("");
    $("#gift-dialog").showModal();
    $$("[data-plan]", $("#gift-dialog")).forEach((button) => button.addEventListener("click", () => {
      state.plan = button.dataset.plan;
      state.revoked = false;
      saveState(); renderObjectStates();
      $("#gift-dialog").close();
      const plan = currentPlan();
      whisper(`“${plan.title}”已成为今晚的叙事骨架。现在，请放入只有你知道的细节。`);
      toast(`已选择「${plan.title}」，策展手册同步更新`);
    }));
  };

  const playTone = (frequency, start, duration) => {
    const oscillator = audio.context.createOscillator();
    const gain = audio.context.createGain();
    oscillator.type = "sine";
    oscillator.frequency.value = frequency;
    gain.gain.setValueAtTime(0.0001, start);
    gain.gain.exponentialRampToValueAtTime(0.035, start + 0.04);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
    oscillator.connect(gain).connect(audio.context.destination);
    oscillator.start(start); oscillator.stop(start + duration + 0.03);
    audio.nodes.push(oscillator);
  };

  const playPhrase = () => {
    if (!state.musicPlaying || !audio.context) return;
    const now = audio.context.currentTime;
    [261.63, 329.63, 392, 329.63, 293.66, 349.23].forEach((note, index) => playTone(note, now + index * 0.42, 0.7));
  };

  const toggleMusic = async () => {
    state.musicPlaying = !state.musicPlaying;
    if (state.musicPlaying) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audio.context = audio.context || new AudioContext();
        await audio.context.resume();
        playPhrase();
        audio.timer = window.setInterval(playPhrase, 3200);
      }
      whisper("旋律开始转动。它只是铺底，真正的主题仍是你想说的话。");
      toast("主题旋律正在回响 · 再次轻触可暂停");
    } else {
      window.clearInterval(audio.timer);
      audio.nodes.forEach((node) => { try { node.stop(); } catch { /* already stopped */ } });
      audio.nodes = [];
      whisper("旋律停在这里。安静也可以成为今晚的一部分。");
      toast("主题旋律已暂停");
    }
    saveState(); renderObjectStates();
  };

  const rehearsalSlides = () => {
    const chapters = manualChapters();
    return [
      { ...chapters[0], object: state.musicPlaying ? "♫" : "◉" },
      { ...chapters[1], object: state.selectedMemories.length ? "▧" : "□" },
      { ...chapters[2], object: currentPlan()?.symbol || "◇" },
      { ...chapters[3], object: state.sealed ? "◉" : "✉" },
    ];
  };

  const renderRehearsal = () => {
    const slides = rehearsalSlides();
    const slide = slides[state.rehearsalStep];
    $("#rehearsal-count").textContent = `0${state.rehearsalStep + 1} / 04`;
    $("#rehearsal-phase").textContent = slide.phase;
    $("#rehearsal-title").textContent = slide.title;
    $("#rehearsal-copy").textContent = slide.copy;
    $("#rehearsal-object").textContent = slide.object;
    $("#rehearsal-dots").innerHTML = slides.map((_, index) => `<i class="${index === state.rehearsalStep ? "is-active" : ""}"></i>`).join("");
    $("#rehearsal-prev").disabled = state.rehearsalStep === 0;
    $("#rehearsal-next").textContent = state.rehearsalStep === 3 ? "回到第一幕" : "下一幕";
  };

  const openRehearsal = () => {
    closeDrawer();
    state.rehearsalStep = 0;
    renderRehearsal();
    $("#rehearsal-dialog").showModal();
  };

  const revokeMaterials = () => {
    state.plan = null;
    state.selectedMemories = [];
    state.letter = "";
    state.sealed = false;
    state.revoked = true;
    saveState(); renderContext(); renderObjectStates();
    $("#sovereignty-dialog").close();
    whisper("本次策展材料已撤回。桌面保留为空白，是否重新开始由你决定。");
    toast("已撤回：照片选择、表达与策展方案已从本次会话移除");
  };

  const activateObject = (object) => {
    const element = $(`[data-object="${object}"]`);
    element?.classList.add("is-pulsing");
    window.setTimeout(() => element?.classList.remove("is-pulsing"), 850);
    openDrawer(object);
  };

  const onPointerDown = (event) => {
    if (window.matchMedia("(max-width: 760px)").matches || event.button !== 0) return;
    const object = event.currentTarget;
    const desk = $("#desk");
    const objectRect = object.getBoundingClientRect();
    const deskRect = desk.getBoundingClientRect();
    drag = {
      object,
      key: object.dataset.object,
      startX: event.clientX,
      startY: event.clientY,
      offsetX: event.clientX - objectRect.left,
      offsetY: event.clientY - objectRect.top,
      deskRect,
      moved: false,
    };
    object.setPointerCapture(event.pointerId);
  };

  const onPointerMove = (event) => {
    if (!drag || drag.object !== event.currentTarget) return;
    if (Math.hypot(event.clientX - drag.startX, event.clientY - drag.startY) < 6 && !drag.moved) return;
    drag.moved = true;
    drag.object.classList.add("is-dragging");
    const maxX = drag.deskRect.width - drag.object.offsetWidth;
    const maxY = drag.deskRect.height - drag.object.offsetHeight;
    const x = Math.max(0, Math.min(maxX, event.clientX - drag.deskRect.left - drag.offsetX));
    const y = Math.max(0, Math.min(maxY, event.clientY - drag.deskRect.top - drag.offsetY));
    drag.object.style.left = `${x}px`;
    drag.object.style.top = `${y}px`;
    drag.object.style.setProperty("--x", "0px");
    drag.object.style.setProperty("--y", "0px");
  };

  const onPointerUp = (event) => {
    if (!drag || drag.object !== event.currentTarget) return;
    const wasMoved = drag.moved;
    drag.object.classList.remove("is-dragging");
    if (wasMoved) {
      state.positions[drag.key] = {
        x: parseFloat(drag.object.style.left),
        y: parseFloat(drag.object.style.top),
      };
      drag.object.dataset.suppressClick = "true";
      saveState();
      toast("物件已放在这里 · 本次会话会记住位置");
      window.setTimeout(() => delete drag.object.dataset.suppressClick, 80);
    }
    drag = null;
  };

  const bindEvents = () => {
    $("#subject-switcher-trigger").addEventListener("click", () => { renderSelectors(); $("#subject-dialog").showModal(); });
    $("#scene-switcher-trigger").addEventListener("click", () => { renderSelectors(); $("#scene-dialog").showModal(); });
    $("#sovereignty-trigger").addEventListener("click", () => $("#sovereignty-dialog").showModal());
    $("#rehearse-trigger").addEventListener("click", openRehearsal);
    $("#revoke-button").addEventListener("click", revokeMaterials);
    $$("[data-close-drawer]").forEach((button) => button.addEventListener("click", closeDrawer));
    $$("[data-dialog-close]").forEach((button) => button.addEventListener("click", () => button.closest("dialog").close()));

    $("#subject-options").addEventListener("click", (event) => {
      const button = event.target.closest("[data-subject]");
      if (!button) return;
      state.subject = button.dataset.subject;
      if (state.subject === "self") state.scene = "self";
      saveState(); renderAll(); $("#subject-dialog").close();
      whisper(`空间的焦点已转向${currentSubject().name}。${currentScene().suggestion}`);
      toast(`关注主体已切换为「${currentSubject().name}」`);
    });
    $("#scene-options").addEventListener("click", (event) => {
      const button = event.target.closest("[data-scene]");
      if (!button) return;
      state.scene = button.dataset.scene;
      state.atmosphere = currentScene().atmosphere;
      saveState(); renderAll(); $("#scene-dialog").close();
      whisper(`${currentScene().whisper} ${currentScene().suggestion}`);
      toast(`生命情景已切换为「${currentScene().label}」`);
    });

    $$(".desk-object").forEach((object) => {
      object.addEventListener("pointerdown", onPointerDown);
      object.addEventListener("pointermove", onPointerMove);
      object.addEventListener("pointerup", onPointerUp);
      object.addEventListener("pointercancel", onPointerUp);
      object.addEventListener("click", () => {
        if (object.dataset.suppressClick) return;
        activateObject(object.dataset.object);
      });
      object.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault(); activateObject(object.dataset.object);
        }
      });
    });
    $$("[data-focus-object]").forEach((button) => button.addEventListener("click", () => activateObject(button.dataset.focusObject)));

    $("#rehearsal-prev").addEventListener("click", () => {
      state.rehearsalStep = Math.max(0, state.rehearsalStep - 1); renderRehearsal();
    });
    $("#rehearsal-next").addEventListener("click", () => {
      state.rehearsalStep = state.rehearsalStep === 3 ? 0 : state.rehearsalStep + 1; renderRehearsal();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeDrawer();
    });
  };

  renderAll();
  renderSelectors();
  bindEvents();
})();
