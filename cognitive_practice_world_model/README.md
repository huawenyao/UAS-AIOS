# cognitive_practice_world_model

> 世界模型认知实践 - Harness Engineering 项目

## 核心理念

从大模型中提取五维度数据，构建综合世界模型，实现 AI 理解能力的可解释化输出。

### 五维度数据模型

| 维度 | 形式化 | 说明 |
|------|--------|------|
| **空间** | `Adjacent(e₁, e₂, t)` | 位置、距离、拓扑结构 |
| **时间** | `Cause(evt₁, evt₂)` | 先后、因果、同时性 |
| **语义** | `IsPartOf(e₁, e₂)` | 上下位、整体部分 |
| **因果** | `Affect(e₁, e₂, evt)` | 作用、反作用 |
| **社会** | `Role(e₁, role, e₂)` | 角色、权力、义务 |

### 产品化形态

- **本体图谱** (Ontology Graph) - 概念层级可视化
- **事件链** (Event Chain) - 时序因果追踪
- **时空图谱** (Spatio-temporal) - 轨迹与位置分析
- **知识图谱** (Knowledge Graph) - 实体关系网络
- **因果图谱** (Causal Graph) - 干预与反事实推理

## 快速开始

### 安装依赖

```bash
pip install numpy networkx
```

### 提取数据

```python
from scripts.extraction.base_extractor import ExtractorFactory

# 创建提取器
extractors = ExtractorFactory.create_all({
    "spatial": {"name": "spatial", "threshold": 0.1},
    "temporal": {"name": "temporal", "confidence_threshold": 0.7},
    "semantic": {"name": "semantic", "k_neighbors": 10},
    "causal": {"name": "causal", "n_samples": 100},
    "social": {"name": "social", "role_types": ["provider", "consumer"]}
})

# 提取数据
spatial_data = extractors["spatial"].extract(model_output)
```

### 融合模型

```python
from scripts.processing.fusion import WorldModelFusion, create_comprehensive_model

# 融合五维度数据
fusion = WorldModelFusion()
ir = fusion.fuse(spatial, temporal, semantic, causal, social)

# 转换为产品视图
from scripts.processing.fusion import ProductViewGenerator
kg_view = ProductViewGenerator.to_knowledge_graph(ir)
```

## 目录结构

```
cognitive_practice_world_model/
├── CLAUDE.md                      # 项目说明
├── README.md                      # 本文件
├── docs/
│   ├── LOOP_THINKING.md           # 方法论框架
│   └── world_model_spec.md        # 产品技术规格
├── configs/
│   ├── extraction_config.json     # 提取配置
│   └── product_config.json        # 产品配置
├── scripts/
│   ├── extraction/
│   │   └── base_extractor.py      # 五维度提取器
│   └── processing/
│       └── fusion.py              # 数据融合与产品化
└── database/
    ├── raw/                       # 原始数据
    ├── processed/                 # 处理后数据
    └── models/                    # 构建的模型
```

## 方法论

遵循 **Loop-Thinking / SIO-MMOS** 框架：

- **Phase 0**: 任务理解与澄清
- **Phase 1**: 信息搜集
- **Phase 2**: 深度分析（五维）
- **Phase 3**: Gap分析与行动计划

详见 `docs/LOOP_THINKING.md`

## 路线图

### Phase 1: MVP
- [x] 项目初始化
- [x] 五维度提取器基类
- [x] 数据融合模块
- [ ] 基础图谱可视化

### Phase 2: 综合能力
- [ ] 多维度融合优化
- [ ] 关系一致性校验
- [ ] 对话式解释

### Phase 3: 产品化
- [ ] 多形态切换
- [ ] 实时监控
- [ ] 假设验证

## 许可证

MIT