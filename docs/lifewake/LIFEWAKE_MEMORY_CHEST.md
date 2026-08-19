# LifeWake × 时空记忆匣：AI 原生叙事空间融合架构

> 状态：Architecture Baseline · Memory P1 可运行原型  
> 定位：LifeWake Memory 域的体验配方，不是第三产品轨，也不是任务驱动开放世界  
> 口号：以记忆筑宫殿，以万物为宝箱，以道具穿时空，人人皆为自己故事的造物主。  
> 可运行入口：`python3 projects/lifewake/scripts/run_memory_chest_demo.py --pretty --write-report`  
> 交互原型：`projects/lifewake/prototype/memory-chest.html`

---

## 0. 融合结论（先说清楚它是什么、不是什么）

**时空记忆匣**把用户提出的三位一体玩法——记忆宫殿、智能百宝箱、时空穿梭机——收敛进既有 LifeWake 产品母体：

```
授权的生命材料 → 可解释的创作 → 合适的时机 → 私人/共同仪式 → 主权记忆 → 受控演化
                                      ▲
                                      │
                         时空记忆匣把「主权记忆」做成可漫游、可穿梭、可生长的私有叙事宇宙
```

| 创意载体 | LifeWake 落点 | 工程对象 | 用户看见的视图 |
|---|---|---|---|
| 记忆宫殿 | Memory / Keepsake Vault 空间化 | `MemoryPalace` + 四层拓扑模板 | 宫殿漫游视图 |
| 智能百宝箱 | Keepsake 物品化，一切可封装、可溯源 | `ChestItem` + 时空溯源 Schema | 百宝箱视图 |
| 时空穿梭机 | P1「记忆时光机」的双向引擎 | `lw.memory.shuttle` / `capture` | 穿梭沉浸视图 |

AI 原生判据（抽掉 AI，核心循环即崩）：模型负责把非结构化记忆变成可计算道具、把道具还原成场景、让人物按图谱活着。平台负责同意、分层、COW 分支、资产治理和仪式信封。这符合 UAS 原则：**模型做演绎，图谱做事实，治理做边界**。

它**不是**：

- 与 SelfPaw / ΠPaw 并列的第三轨；
- 用任务、打怪、签到驱动的传统游戏；
- 把真实人生记忆丢进可随意改写的公共开放世界；
- 用 `lw.twin.draft` 自动代聊的数字分身。

它**是**：私人叙事数字家园，附带游戏化体验。留存靠资产沉淀，不靠推送。现实记忆层与幻想创作层必须隔离；重温与改写必须分模式；原始存档写时复制，永不覆盖。

---

## 1. 道德势术器映射

| 层 | 创意语言 | LifeWake / UAS 落点 |
|---|---|---|
| **道** | 人人皆为自己故事的造物主 | 人对生命意义拥有解释主权（F1）；世界模型是法则编译器 |
| **德** | 绝对私有、可撤回、真实记忆不被篡改 | 灵魂数据主权、Consent Center、现实/幻想双库、原点只读 |
| **势** | 物品—场景—故事—人物的双向张力 | 三视图心智：道具 = 故事的物理锚点 |
| **术** | 物品化、穿梭、抓取、融合、平行分支 | MED：机制固定、表达可变；叙事约束图谱 |
| **器** | 宫殿 / 百宝箱 / 穿梭机 | `lw.memory.*`、`ChestItem`、COW 图谱、宫殿模板 |

---

## 2. 三方 SOTA 专家拆解：关键是什么、如何实现

检索关键词（5）：`AI-native world model` · `memory palace spatial knowledge graph` · `object-as-narrative-portal / keepsake game` · `parallel timeline copy-on-write` · `personal digital memory vault privacy`。下列实现要点同时吸收游戏制作、产品设计、技术架构三方共识。

### 2.1 游戏制作：规则由人定义，AI 只负责表达

**关键**

1. 唯一核心循环是「记忆/故事 → 物品化 → 穿梭 → 新记忆 → 新物品」，拒绝任务通关驱动。内在动机来自收藏、修复遗憾、创造平行分支、重访尘封故事，而不是胜负。
2. 跨分支叙事一致性是最大制作难题。人物、因果、情绪必须以图谱为 ground truth，禁止大模型即兴 OOC。
3. 宫殿是生长式关卡，但必须有空间拓扑约束：底层模板人工预设，AI 只填充装饰与光影；高权重信物增量长出专属房间，禁止全量乱生长。
4. 道具用双层管线：基础 prefab（信物/卷轴/罗盘/宝石）保证可识别、可交互；AI 只改铭文、光晕、叙事描述。
5. 穿梭不是黑屏跳转，转场序列固定为「道具激活 → 空间扭曲 → 记忆碎片闪回 → 场景落地」。

**如何实现（本仓库已落地的最小机制）**

- `PREFABS` 固定四类容器与交互；
- `MemoryPalace` 用四层模板 + `weight=high` 增量生长；
- `NarrativeGraph.assert_consistent` 在每次生成场景 spec 时校验人物是否存在于当前分支；
- `_transition()` 输出固定镜头语言，不交给随机生成。

**制作侧坑**：完全放飞 AI 会得到无意义道具、风格割裂的宫殿、穿梭前后故事断裂。评测应用人物一致性、分支因果完整性、穿梭氛围连贯性做降级重生成——原型阶段用图谱拒绝代替模型打分。

### 2.2 产品设计：私人家园，而不是普通游戏

**关键**

1. 心智定位：私人叙事数字家园，附带游戏化。输入分真实人生记忆与幻想创作，产品必须在存储、UI、权限上隔离。
2. 三视图必须可一键互跳，并反复教育「物品 = 故事锚点」。
3. 默认绝对私有；分享是可选导出，现实记忆不参与训练。
4. 留存靠资产沉淀。必须提供归档、封存、融合、删除，否则百宝箱会变成垃圾堆。
5. 穿梭双模式强提示：【重温原始】只读；【开启新平行分支】COW。误改真实记忆是产品事故。
6. 「时空探险」在 LifeWake 里只能是用户主动 pull，不能做成每日推送任务——否则违反慢灵感与反增长护栏。

**如何实现**

溯源 Schema（每个 `ChestItem.provenance()` 必带）：

```json
{
  "item_id": "item_moon_hairpin",
  "item_type": "character",
  "source_timeline_id": "tl_linyan_dusk",
  "parallel_branch_id": "br_linyan_origin",
  "entity_graph_ref": "person_linyan",
  "is_real_memory": true,
  "layer": "real_memory",
  "user_edit_note": "妻子 · 林妍的人物信物，仅本人可唤醒。",
  "sealed": false,
  "archived": false
}
```

治理映射：

| 产品红线 | 机制 |
|---|---|
| 无同意不得物品化/改写 | `memory.itemize` / `memory.revisit` / `memory.rewrite` 分 scope |
| 原始记忆不被覆盖 | 真实层分支 `readonly=true`；改写只克隆幻想子图 |
| 真实 × 幻想融合不冒充记忆 | `fuse()` 产物强制 `is_real_memory=false`、`layer=fantasy` |
| 道具膨胀 | `archive` / `seal`；封存物不可再融合 |
| 不训练用户私有记忆 | purpose 仅 `create_for_user`；审计不含原文私密字段 |

渐进式引导：先给三件示例道具走通闭环，再导入自己的记忆——对应种子 `月光发卡`、`雨夜爵士回响卷轴`、`城市寻宝罗盘`。

### 2.3 技术架构：图谱是大脑，道具只是入口

系统本质：**以叙事物品为唯一锚点的持久化多模态世界模型**。四大硬骨头：

1. 叙事物品化引擎：非结构化记忆 → 带溯源的可计算道具；
2. 记忆宫殿持久存储：图（因果）+ 向量（语义）+ 对象存储（资产）；
3. 时空穿梭引擎：道具 ID → 还原场景/人物/剧情；改写 COW；
4. 多模态渲染管线：Demo 走路线 A（场景 spec + 程序化呈现），商业化再评估路线 B（Genie 类世界模型）。

```
层4  三视图：宫殿 | 百宝箱 | 穿梭
层3  渲染：场景 spec → 原型 HTML / 未来 Unity·Genie
层2  引擎：itemize / shuttle / capture / fuse / palace.grow
层1  事实：NarrativeGraph（COW 分支）+ ChestItem + Palace 模板
层0  治理：ConsentGrant · 现实/幻想隔离 · 审计 · 不训练
```

SOTA 要点：

- **禁止**把全部历史塞进 LLM 窗口；事实在图，模型只演绎。
- 写时复制：改写真实记忆时克隆子图，原点只读。
- 人物 Alive：人格与关系从图读取，而不是模型隐状态。`lw.twin.draft` 仍保留，禁止自动代发。
- 延迟：原型同步生成 spec；上线需对热点分支做缓存，避免点击后空等。
- 隐私：每用户逻辑隔离实例；现实记忆加密；不进训练。

Demo 明确不包含 Neo4j / Milvus / 实时 3D 世界模型，但接口按该分层预留，避免把 LLM 误当成数据库。

---

## 3. 运行闭环（已实现）

```
用户输入记忆/故事
    → lw.memory.weave 物品化（百宝箱）
    → MemoryPalace.assign 锚定（宫殿，高权重增量生长）
    → lw.memory.shuttle 重温 | 改写 | 续写
    → 场景内 lw.memory.capture 反向封装
    → 可选 lw.memory.fuse 跨界合成（产物必为幻想层）
    → 资产治理 archive/seal
    → 无限自循环，原点永不覆盖
```

三件初始可交互道具（可直接用于 demo）：

| 道具 | 品类 | 层 | 穿梭场景 | 设计意图 |
|---|---|---|---|---|
| 月光发卡 | 人物信物 | 现实记忆 | 黄昏窗边 · 林妍 | 把既有情景桌面的关系焦点做成可唤醒信物 |
| 雨夜爵士回响卷轴 | 故事道具 | 现实记忆 | 雨夜咖啡馆 | 把惊喜盲盒的哼唱创作收成可重访剧情 |
| 城市寻宝罗盘 | 场景碎片 | 幻想创作 | 夜色寻宝图 | 把「尚未发生的约会」做成可改写、可融合的场景入口 |

闭环验收：`tests/test_memory_chest.py` 断言原点只读、改写 COW、抓取降为幻想层、融合不冒充真实记忆、同意门禁。

---

## 4. 能力、实体与世界模型增量

新增 `lw.*`（领域命名空间，不上收 `cs.*`）：

| 能力 | 作用 |
|---|---|
| `lw.memory.weave` | 叙事物品化（原 P1 reserved，现启用） |
| `lw.memory.shuttle` | 正向穿梭：relive / rewrite / continue |
| `lw.memory.capture` | 反向封装：场景 → 新道具 |
| `lw.memory.fuse` | 跨界合成，产物强制幻想层 |
| `lw.palace.snapshot` | 宫殿/图谱/道具快照 |

新增实体：`ChestItem`、`TimelineBranch`、`GraphNode`、`PalaceRoom`、`ShuttleSession`。  
`Keepsake` 仍是权利与保留对象；`ChestItem` 是其叙事可计算投影。  
`lw.twin.draft` 继续 `FEATURE_RESERVED`。

世界模型五维扩展：

| 维 | 增量 |
|---|---|
| 空间 | 四层宫殿：现实 / 幻想 / 历史 / 未来 |
| 时间 | 原点时间线 + 平行分支；重温只读 |
| 主体 | 图谱约束的 Alive 人物，非代发分身 |
| 客体 | 四类道具容器 + 溯源码 |
| 反馈 | 穿梭/抓取/融合审计；不把模型分当感受 |

---

## 5. 关键词与资料（5 词 × 约 30 篇）

资料用于约束实现，不把外部产品叙事复制进 LifeWake。LifeWake 的反增长、可撤回同意、非诊断红线仍然优先。

### 5.1 AI-native world model（模型即引擎）

1. DeepMind, *Genie 3: A new frontier for world models*（2025）  
2. DeepMind, Genie 3 模型页：实时可玩环境与 promptable world events  
3. Google, *Project Genie* 研究原型说明  
4. *World Models: The Ultimate Guide (2026 Edition)*：Genie / Oasis / Marble / Dreamer 分类  
5. Decart Oasis：像素世界模型可玩范式（路线 B 对照）  
6. World Labs Marble：空间智能、可导航世界（路线 B 对照）  
7. Hafner et al., DreamerV3：隐空间世界模型（对照「不要把记忆只放在隐状态」）  
8. Microsoft WHAM：游戏环境世界模型研究

**对 LifeWake 的用法**：Demo 走路线 A（场景 spec + 程序化视图）。商业化渲染可替换为 Genie 类世界模型，但事实源仍必须是图谱，因为 Genie 3 自身也声明长时一致性有限。

### 5.2 Memory palace / spatial knowledge graph

9. MemPalace GitHub：wing / room / drawer 空间记忆  
10. MemPalace 官方 *The Palace*：method of loci 层级导航  
11. MemPalace 知识图谱说明：时间有效窗口与实体关系  
12. arXiv:2604.21284 *Spatial Metaphors for LLM Memory*：空间隐喻 vs 向量 metadata 的批判  
13. Alexey On Data, MemPalace 评述：verbatim-first 与层次过滤  
14. Wu et al., LongMemEval：长记忆检索基准  
15. MemPalace Issue #606：把宫殿渲染为可漫游 3D 的社区实验

**对 LifeWake 的用法**：宫殿是可漫游的记忆索引，不是公共 MMO 地图。采用「模板拓扑 + 增量生长」。批判论文提醒我们：不要把 UI 空间隐喻误当成已经解决了长记忆。

### 5.3 Object-as-narrative-portal / keepsake games

16. Tanenbaum, Antle et al., *The Reading Glove*：物可读取记忆的 tangible narrative  
17. Shing Yin Khor, *Keepsake Games and Object Narratives*  
18. Khor, *Remember August* post-mortem：玩即留下纪念物  
19. Sidequest, Shim & Khor 访谈：keepsake / connected path  
20. Patreon, *Keepsake and Connected Path Games* 定义  
21. Hellboy / psychometry 母题（Reading Glove 论文中的设计隐喻）：触物见史

**对 LifeWake 的用法**：LifeWake 的 Keepsake 本来就是纪念物。百宝箱把「玩的过程留下可携带物」做成核心机制；道具必须能被用户理解、编辑备注、导出删除，而不是黑盒掉落。

### 5.4 Parallel timeline / branching narrative

22. *Detroit: Become Human* 官方/Wiki：预置流程图式分支  
23. Interactive Pasts, DBH 选择与合流分析：预置分支终将收束  
24. Liu, DBH instruction design：选择幻觉与路径再中心化  
25. L0stInFades/dbh-engine-analysis：预烘焙 sequence 而非运行时 COW  
26. 对照结论：AI 原生无限分支不能走 DBH 预写流程图，必须运行时写时复制

**对 LifeWake 的用法**：真实记忆原点 = 只读主时间线；每一次改写 = 新 `branch_id`。这不是「流程图里再开一个节点」，而是子图克隆。DBH 证明了人工预写分支会合流；本产品要的是永久并存、互不覆盖。

### 5.5 Personal digital memory vault / privacy

27. MemX, *Your AI Companion Remembers Everything. Who Else?*：所有权优先的记忆层  
28. arXiv:2409.11192, *Ethical Personal AI Applications*：长期记忆助手的同意与删除  
29. Maren：私有记忆、不训练、可导出删除  
30. Dina Kernel：本地加密分仓、外发前脱敏  
31. LinkedIn *Personal AI: Memory, Privacy, and Context-Aware Intelligence*：个人记忆金库  
32. Mozilla 2024 伴侣应用隐私审查（经 MemX 转述）：默认分享/不可删除是反模式  
33. 本仓库 ADR-UAS-003：体验域同意/仪式/情感影响上收 G/E/Π，领域能力留在 `lw.*`

**对 LifeWake 的用法**：现实记忆库额外加密、不训练、可撤回；幻想库才允许融合乱序穿梭。双库若混淆，属于严重产品事故，而不是玩法特性。

---

## 6. 与宪章的冲突检查

| 宪章 / 法则 | 记忆匣做法 |
|---|---|
| 不做无限信息流、签到、羞耻召回 | 无每日强制探险推送；探险是 pull |
| 不做数字分身代聊 | Alive 角色只在穿梭场景内、受图谱约束；`lw.twin.draft` 仍保留 |
| 不做诊断/画像 | 物品化目的仅 `create_for_user` |
| F6 记忆依赖来源与控制权 | 每件道具有 provenance、可封存/归档/删除 |
| F5 稀缺保护仪式 | 不靠道具刷屏制造 DAU |
| 未成年人 | 现实记忆导入与外发仍走既有安全门禁；本原型不向未成年人推广 |

---

## 7. 成熟度

| 维度 | 本增量 | 下一闭环 |
|---|---|---|
| 产品定义 | Memory P1 配方已写入本文件与蓝图 | 用户研究：真实记忆误改恐惧、三视图是否可理解 |
| 契约 | `lw.memory.*` 启用 | 与 `RitualEnvelope` / `Keepsake` adapter 完全对齐 |
| 可运行 | 引擎 + CASE 级单测 + CLI demo + 静态三视图原型 | SelfPaw Core 身份/记忆接入；向量检索 |
| 渲染 | 路线 A 文案场景 spec | 可选 Unity 或世界模型流 |
| 生产治理 | 原点 COW、分层、同意 scope | 持久化加密、删除证明、多人争议 |

相关代码：

- `projects/lifewake/lifewake/memory_chest.py`
- `projects/lifewake/configs/memory_chest_seed.json`
- `projects/lifewake/scripts/run_memory_chest_demo.py`
- `projects/lifewake/tests/test_memory_chest.py`
- `projects/lifewake/prototype/memory-chest.html`
