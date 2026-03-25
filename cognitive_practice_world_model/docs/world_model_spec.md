# 世界模型产品形态与技术形态规格

## 一、五维度数据提取规格

### 1.1 空间关系提取 (Spatial)

**形式化**: `Adjacent(e₁, e₂, t)`

**提取方法**:
- 位置编码解析：从模型隐藏状态提取位置信息
- 距离度量：计算嵌入空间中的向量距离
- 拓扑结构：分析注意力图中的连接模式

**数据结构**:
```json
{
  "dimension": "spatial",
  "entities": [
    {"id": "e1", "position": [x, y, z], "embedding": [...]}
  ],
  "relations": [
    {"from": "e1", "to": "e2", "type": "adjacent", "distance": 0.3, "timestamp": "t1"}
  ],
  "topology": "clustered|distributed|hierarchical"
}
```

### 1.2 时间关系提取 (Temporal)

**形式化**: `Cause(evt₁, evt₂)`

**提取方法**:
- 序列注意力分析：识别因果链
- 事件顺序恢复：从训练数据推断时间序
- 因果归因：干预实验验证因果关系

**数据结构**:
```json
{
  "dimension": "temporal",
  "events": [
    {"id": "evt1", "timestamp": "t1", "state": "..."}
  ],
  "causal_links": [
    {"cause": "evt1", "effect": "evt2", "confidence": 0.85}
  ],
  "timeline": ["evt1", "evt2", "evt3"]
}
```

### 1.3 语义关系提取 (Semantic)

**形式化**: `IsPartOf(e₁, e₂)`

**提取方法**:
- 嵌入空间最近邻聚类
- 概念层次结构发现
- 整体部分关系识别

**数据结构**:
```json
{
  "dimension": "semantic",
  "concepts": [
    {"id": "c1", "name": "动物", "embedding": [...]},
    {"id": "c2", "name": "猫", "embedding": [...]}
  ],
  "relations": [
    {"child": "c2", "parent": "c1", "type": "is_a"}
  ],
  "hierarchy_depth": 3
}
```

### 1.4 因果关系提取 (Causal)

**形式化**: `Affect(e₁, e₂, evt)`

**提取方法**:
- 因果干预实验
- 反事实推理
- 结构方程模型

**数据结构**:
```json
{
  "dimension": "causal",
  "mechanisms": [
    {"source": "e1", "target": "e2", "mechanism": "activation", "strength": 0.7}
  ],
  "interventions": [
    {"do": "e1=1", "effect": "e2=0.8", "probability": 0.9}
  ]
}
```

### 1.5 社会关系提取 (Social)

**形式化**: `Role(e₁, role, e₂)`

**提取方法**:
- 角色嵌入分析
- 对话上下文提取
- 权力关系建模

**数据结构**:
```json
{
  "dimension": "social",
  "agents": [
    {"id": "a1", "role": "provider", "capabilities": [...]},
    {"id": "a2", "role": "consumer", "needs": [...]}
  ],
  "relations": [
    {"from": "a1", "to": "a2", "type": "obligation", "content": "..."}
  ]
}
```

---

## 二、综合模型构建

### 2.1 模型架构

```
输入: LLM 隐藏状态/注意力/嵌入
    ↓
┌─────────────────────────────────────────┐
│  多维度提取器                            │
│  ├─ Spatial Extractor                   │
│  ├─ Temporal Extractor                  │
│  ├─ Semantic Extractor                  │
│  ├─ Causal Extractor                    │
│  └─ Social Extractor                    │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  关系融合层 (Fusion Layer)               │
│  ├─ Cross-dimension Alignment           │
│  ├─ Consistency Check                   │
│  └─ Conflict Resolution                 │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  综合世界模型 IR                         │
│  ComprehensiveWorldModelIR              │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  产品化输出                              │
│  ├─ Ontology Graph (概念图谱)           │
│  ├─ Event Chain (事件链)                │
│  ├─ Spatio-temporal Graph (时空图谱)    │
│  ├─ Knowledge Graph (知识图谱)          │
│  └─ Causal Graph (因果图谱)             │
└─────────────────────────────────────────┘
```

### 2.2 核心数据结构

```python
class ComprehensiveWorldModelIR:
    schema_version: str
    model_id: str
    extraction_timestamp: str

    # 五维度数据
    spatial: SpatialData
    temporal: TemporalData
    semantic: SemanticData
    causal: CausalData
    social: SocialData

    # 综合指标
    coherence_score: float
    completeness_score: float
    confidence: float
```

---

## 三、产品化形态

### 3.1 图谱类产品

| 产品形态 | 数据模型 | 交互方式 | 场景 |
|----------|----------|----------|------|
| 本体图谱 | Ontology Graph | 层级展开 + 查询 | 概念探索 |
| 事件链 | Event Chain | 时间线拖拽 + 缩放 | 过程分析 |
| 时空图谱 | Spatio-temporal | 地图/时间窗 | 轨迹分析 |
| 知识图谱 | Knowledge Graph | 图遍历 + 筛选 | 关系发现 |
| 因果图谱 | Causal Graph | 干预模拟 + what-if | 决策支持 |

### 3.2 交互模式

1. **探索模式**：图谱可视化 + 节点详情
2. **对话模式**：自然语言查询 + 解释生成
3. **监控模式**：实时变化 + 异常告警
4. **编辑模式**：关系增删 + 假设验证

### 3.3 技术栈

- **存储**: Neo4j (图) + PostgreSQL (关系) + Redis (缓存)
- **计算**: PyTorch (提取) + NetworkX (图分析)
- **服务**: FastAPI (API) + WebSocket (实时)
- **前端**: React + D3.js/vis.js

---

## 四、实现路线图

### Phase 1: 基础能力 (MVP)
- [ ] 单维度提取器实现
- [ ] 基础图谱可视化
- [ ] 简单查询 API

### Phase 2: 综合能力
- [ ] 多维度融合
- [ ] 关系一致性校验
- [ ] 对话式解释

### Phase 3: 产品化
- [ ] 多形态切换
- [ ] 实时监控
- [ ] 假设验证

---

## 五、验收标准

| 维度 | 指标 | 阈值 |
|------|------|------|
| 提取覆盖率 | 五维度覆盖度 | ≥80% |
| 关系准确率 | 人工校验准确率 | ≥85% |
| 查询响应 | P99 延迟 | <2s |
| 可用性 | 首屏加载时间 | <3s |