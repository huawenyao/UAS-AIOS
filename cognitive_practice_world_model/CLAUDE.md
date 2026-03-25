# cognitive_practice_world_model

> 世界模型认知实践 - Harness Engineering 项目

## 项目定位

基于大模型提取五维度数据（空间、时间、语义、因果、社会关系），构建综合世界模型，实现 AI 理解能力的可解释化输出。

## 核心理论

### 五维度数据模型

| 维度 | 形式化 | 用途 |
|------|--------|------|
| 空间关系 | `Adjacent(e₁, e₂, t)` | 位置、距离、拓扑结构 |
| 时间关系 | `Cause(evt₁, evt₂)` | 先后、因果、同时性 |
| 语义关系 | `IsPartOf(e₁, e₂)` | 上下位、整体部分 |
| 因果关系 | `Affect(e₁, e₂, evt)` | 作用、反作用 |
| 社会关系 | `Role(e₁, role, e₂)` | 角色、权力、义务 |

### 产品化形态

- **概念模型** → 本体图谱 (Ontology Graph)
- **事件模型** → 事件链 (Event Chain)
- **时空模型** → 时空图谱 (Spatio-temporal Graph)
- **本体模型** → 知识图谱 (Knowledge Graph)
- **交互形态**：图谱可视化、对话式解释、实时监控

## 目录结构

```
cognitive_practice_world_model/
├── CLAUDE.md                    # 本文件
├── docs/
│   ├── LOOP_THINKING.md         # 方法论框架
│   ├── wm_theory.md             # 世界模型理论
│   └── product_spec.md          # 产品规格
├── configs/
│   ├── extraction_config.json   # 提取配置
│   └── product_config.json      # 产品配置
├── scripts/
│   ├── extraction/              # 数据提取脚本
│   └── processing/              # 数据处理脚本
├── database/
│   ├── raw/                     # 原始提取数据
│   ├── processed/               # 处理后数据
│   └── models/                  # 构建的模型
└── product/
    ├── api/                     # API服务
    └── ui/                      # 前端界面
```

## 核心命令

- `/init` - 初始化项目结构
- `/extract [dimension]` - 提取指定维度数据
- `/build` - 构建综合模型
- `/serve` - 启动产品服务

## 方法论

遵循 **Loop-Thinking / SIO-MMOS** 框架：
- Phase 0: 任务理解与澄清
- Phase 1: 信息搜集
- Phase 2: 深度分析（五维）
- Phase 3: Gap分析与行动计划

详见 `docs/LOOP_THINKING.md`

---

## 知识体系索引

> 本项目依赖的核心知识文件，来自 `docs/世界模型/` 目录

### 理论核心

| 文件 | 用途 | 关键内容 |
|------|------|----------|
| `docs/世界模型/wm_theory.md` | 世界模型基础理论 | 本源法则、降维重构、五维认知 |
| `docs/世界模型/wm_system_logic_and_product_stack.md` | 体系化逻辑与产品栈（WM-SLPS） | L0–L5 堆栈、操作演算、门控、度量、WM-CMM |
| `docs/世界模型/wm_unit_agent_macro_brain.md` | Unit Agent 宏观脑范式 | 微观脑/宏观脑、认知闭包、与 IR 映射、四阶段路径 |
| `docs/世界模型/世界模型.md` | 法则编译器深度解析 | 三重身份：镜像/透镜/熔炉 |
| `docs/世界模型/world_model_agi_path.md` | AGI实现路径 | World Model + AI Agent |

### 认知架构

| 文件 | 用途 | 关键内容 |
|------|------|----------|
| `docs/世界模型/AGI认知架构方案v2.0.md` | AGI认知架构 | 意图驱动、认知闭环 |
| `docs/世界模型/AGI认知架构-意图驱动v2.0.md` | 意图驱动架构 | 意图激活→理解→规划→执行 |
| `docs/世界模型/Cognitive_Agent体系修正.md` | Agent体系 | 主体性、认知平衡 |

### 产品与技术

| 文件 | 用途 | 关键内容 |
|------|------|----------|
| `docs/世界模型/认知智能-产品与技术形态.md` | 产品形态 | 本项目直接参考 |
| `docs/世界模型/AI_Agent演进逻辑与产品趋势.md` | 产品趋势 | 演进逻辑、市场格局 |

### 研究与深度

| 文件 | 用途 | 关键内容 |
|------|------|----------|
| `docs/世界模型/world_model_research.md` | 研究调研 | 学术前沿、技术路线 |
| `docs/世界模型/world_model_contradiction_analysis.md` | 矛盾分析 | 理论冲突、解决路径 |
| `docs/认知超智能/UACA_UniAgent_TOGAF_Architecture.md` | UniAgent 标准化与群体网络规范 | L0–L5、能力清单、网络构造、L3 消息、L5 提交；TOGAF 附录 |

---

### 知识调用约定

在项目中引用理论时，使用以下格式：

```
// 引用格式
@see docs/世界模型/wm_theory.md §2.1  // 具体章节
@ref 认知智能-产品与技术形态.md       // 简写
```

### 核心依赖

- **五维度模型**：空间/时间/语义/因果/社会 → 对应 `wm_theory.md` 的五维认知
- **产品化形态**：图谱/事件链/因果链 → 参考 `认知智能-产品与技术形态.md`
- **方法论**：Loop-Thinking → `docs/LOOP_THINKING.md`