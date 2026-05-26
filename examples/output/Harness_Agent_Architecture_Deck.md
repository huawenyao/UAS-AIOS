# Harness Agent 架构体系与工程实践

## 宣讲PPT大纲

---

# 第一部分：为什么需要Harness Agent

## 当前AI Agent的困境

**数据触目惊心：**
- 📉 70%的Agent项目在POC阶段失败
- 🤖 幻觉、工具调用失败、上下文丢失
- 🌊 从"会说话"到"能干活"的巨大鸿沟

**典型失败场景：**
```
用户: "帮我预订明天下午3点的会议室"

普通Agent: 
- 调用日历API ❌ (认证失败)
- 忘记检查用户权限
- 没有备选方案
- 对话中断，状态丢失

结果: 任务失败，用户体验极差
```

---

## Harness Agent = 生产级AI系统

**核心理念转变：**

```
❌ 传统视角:  Agent = LLM + Prompt
✅ Harness视角: Agent = LLM + 工程化外壳
```

**Harness的核心价值：**

| 维度 | 传统Agent | Harness Agent |
|------|----------|--------------|
| **可靠性** | 30-50% | 90%+ |
| **可观测性** | 黑盒 | 全链路追踪 |
| **安全性** | 无防护 | 多层防护 |
| **可维护性** | 困难 | 标准化 |
| **生产就绪** | ❌ | ✅ |

**目标：** 让Agent从"有趣的原型"变成"可靠的引擎"

---

# 第二部分：Harness核心理念

## Agent = Model + Harness

**解剖一个生产级Agent：**

```
┌─────────────────────────────────────────────────────────────┐
│                    Harness Agent 架构                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────────────────────────────────────────────┐  │
│   │                 Agent Core (LLM)                     │  │
│   │              (推理/决策核心)                         │  │
│   │  • 理解用户意图                                      │  │
│   │  • 生成行动计划                                      │  │
│   │  • 推理与决策                                        │  │
│   └────────────────────┬───────────────────────────────┘  │
│                        │                                    │
│   ┌────────────────────┴───────────────────────────────┐    │
│   │                 HARNESS LAYER (工程化外壳)           │    │
│   │  ┌───────────────┬───────────────┬─────────────┐ │    │
│   │  │ Memory Mgmt   │ Tool Adapter  │ Sandbox     │ │    │
│   │  │ (记忆管理)     │ (工具适配)    │ (沙箱安全)   │ │    │
│   │  ├───────────────┼───────────────┼─────────────┤ │    │
│   │  │ Policy/Guard  │ Orchestrator  │ Audit Log   │ │    │
│   │  │ (策略防护)    │ (编排器)      │ (审计日志)   │ │    │
│   │  ├───────────────┼───────────────┼─────────────┤ │    │
│   │  │ Validation    │ Recovery      │ Monitor     │ │    │
│   │  │ (验证)        │ (恢复)        │ (监控)       │ │    │
│   │  └───────────────┴───────────────┴─────────────┘ │    │
│   └──────────────────────────────────────────────────┘    │
│                                                              │
│   ┌──────────────────────────────────────────────────┐    │
│   │              EXTERNAL TOOLS (外部工具)              │    │
│   │  • APIs (日历/邮件/数据库)                         │    │
│   │  • 浏览器自动化                                     │    │
│   │  • 代码执行环境                                     │    │
│   │  • 第三方服务                                       │    │
│   └──────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Harness的四大核心能力

### 1. 约束 (Constraint)

**定义：** 为Agent设定不可逾越的安全边界

```python
# 策略防护示例
class PolicyGuard:
    def check(self, action, context):
        # 1. 权限检查
        if action.type == "DELETE" and not context.has_permission("admin"):
            return Reject("无删除权限")
        
        # 2. 数据安全检查
        if action.contains_sensitive_data():
            return RequireApproval("包含敏感数据，需人工确认")
        
        # 3. 资源限制
        if action.estimated_cost > context.budget_limit:
            return Reject("超出预算限制")
        
        return Approve()
```

### 2. 信息 (Inform)

**定义：** 为Agent提供正确的上下文和记忆

```python
# 记忆管理示例
class MemoryManager:
    def __init__(self):
        self.working_memory = WorkingMemory(capacity=7)  # 短期记忆
        self.episodic_memory = EpisodicMemory()        # 情景记忆
        self.semantic_memory = SemanticMemory()          # 语义记忆
    
    def retrieve_context(self, query):
        # 1. 检索工作记忆
        recent = self.working_memory.get_recent()
        
        # 2. 检索相关情景
        relevant_episodes = self.episodic_memory.search(query)
        
        # 3. 检索语义知识
        facts = self.semantic_memory.query(query)
        
        # 4. 压缩整合
        return self.compress(recent, relevant_episodes, facts)
```

### 3. 验证 (Verify)

**定义：** 确保Agent的输出正确且符合预期

```python
# 验证示例
class Validator:
    def validate(self, output, criteria):
        results = []
        
        # 1. 结构化验证
        if not self.check_schema(output, criteria.schema):
            results.append(ValidationError("结构不符合要求"))
        
        # 2. 逻辑验证
        if not self.check_logic(output):
            results.append(ValidationError("存在逻辑矛盾"))
        
        # 3. 安全验证
        if self.contains_risk(output):
            results.append(ValidationWarning("存在潜在风险"))
        
        # 4. 回归测试
        if not self.regression_test(output):
            results.append(ValidationError("回归测试失败"))
        
        return results
```

### 4. 纠正 (Correct)

**定义：** 当Agent出错时，自动恢复和修复

```python
# 恢复示例
class RecoveryManager:
    def handle_error(self, error, context):
        # 1. 记录错误
        self.log_error(error, context)
        
        # 2. 评估严重程度
        severity = self.assess_severity(error)
        
        # 3. 尝试自动恢复
        if severity == "RECOVERABLE":
            recovery_plan = self.generate_recovery_plan(error)
            if self.execute_recovery(recovery_plan):
                return RecoverySuccess()
        
        # 4. 降级处理
        if severity == "DEGRADABLE":
            fallback = self.activate_fallback(context)
            return DegradedMode(fallback)
        
        # 5. 人工介入
        return HumanEscalation(required=True)
```

---

# 第三部分：五铰链架构体系

## 什么是五铰链（Five Hinges）？

**五铰链是一个基于第一性原理的认知决策框架**

```
┌─────────────────────────────────────────────────────────────┐
│                    五铰链认知框架                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐              │
│   │  Grip   │───▶│  Auger  │───▶│  Shear  │              │
│   │ (咬合颚)│    │(螺旋钻) │    │(切割刃) │              │
│   └─────────┘    └─────────┘    └─────────┘              │
│        │                              │                    │
│        └──────────────┬───────────────┘                    │
│                       ▼                                    │
│   ┌─────────┐    ┌─────────┐                              │
│   │  Coil   │◀──▶│ Stress  │                              │
│   │(张力弹簧)│    │(压力测试)│                              │
│   └─────────┘    └─────────┘                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**五铰链的核心理念**：将混沌输入转化为可执行行动，通过"开合循环"系统化处理不确定性。

---

## T1: Grip - 咬合颚（感知层）

### 核心功能
识别核心变量，建立认知锚点

### 关键概念

**固定颚（Fixed Jaws）**
- 3个不可妥协的绝对公理
- 在特定领域内永恒不变
- 决策的绝对边界

**活动颚（Movable Jaws）**
- 可调节的临时假设
- 标注重要性、验证状态、可调节程度
- 可随新信息调整

### 示例：技术架构决策

```
固定颚（技术架构）：
1. 成本不可能为负（资源有限）
2. 复杂度守恒（简化一处复杂另一处）
3. 性能与灵活性权衡

活动颚：
假设1: "团队将在6个月内扩展到20人"
  - 重要性: 高
  - 已验证: 否（需CEO确认）
  - 可调节程度: 中

核心变量：
- 团队能力（分布式系统经验：低）
- 业务复杂度（模块数：未知）
- 预期增长速度（未确认）
- 运维成熟度（K8s经验：无）
```

---

## T2: Auger - 螺旋钻（分析层）

### 核心功能
5Why钻探，直至第一性原理

### 钻探过程

```
L0: [初始陈述]
    ↓ 为什么？
L1: [根本原因1]
    ↓ 为什么需要这个？
L2: [根本原因2]
    ↓ 为什么会有这个问题？
L3: [根本原因3]
    ↓ 为什么？
L4: [根本原因4]
    ↓ 为什么？
L5: [第一性阻力] ← STOP
```

### 第一性阻力类型

1. **物理定律**：能量守恒、熵增定律
2. **数学真理**：1+1=2、概率总和=1
3. **人性约束**：注意力有限、厌恶损失
4. **经济规律**：资源稀缺、边际效用递减
5. **逻辑公理**：A=A、非矛盾律

### 示例：架构选型钻探

```
L0: "我们需要微服务架构"
    ↓ 为什么？
L1: "因为需要独立部署"
    ↓ 为什么需要这个？
L2: "因为团队分布在3个国家"
    ↓ 为什么会有这个问题？
L3: "因为业务需要24x7运行"
    ↓ 为什么？
L4: "因为客户分布在不同大洲"
    ↓ 为什么？
L5: "因为地球自转造成时区差异" ← 第一性阻力（物理定律）

认知垫片：
- "独立部署 = 降低发布风险"
- "发布依赖 = 代码耦合"
- "耦合源于边界缺失"
```

---

## T3: Shear - 切割刃（决策层）

### 核心功能
将原始混沌切割为SIO格式切片（72小时内可验证）

### SIO格式

```json
{
  "Situation（情境）": {
    "current_state": "当前状态是什么？",
    "key_variables": ["关键变量有哪些？"],
    "constraints": ["约束条件是什么？"]
  },

  "Insight（洞察）": {
    "core_problem": "核心问题是什么？",
    "why_act_now": "为什么现在必须行动？",
    "cost_of_inaction": "不行动的后果是什么？"
  },

  "Outcome（行动）": {
    "action": "具体做什么？（动词开头，可执行）",
    "success_criteria": ["成功标准是什么？（可测量）"],
    "deadline": "完成时限是多久？（≤72小时）"
  }
}
```

### 示例：架构决策SIO

```json
{
  "Situation": {
    "current_state": "团队5人，无分布式系统经验，MVP deadline 3个月",
    "key_variables": [
      "团队分布式经验：低",
      "业务边界清晰度：未定义", 
      "预期增长速度：未确认",
      "运维成熟度：无K8s经验"
    ],
    "constraints": ["3个月MVP deadline", "5人团队", "有限预算"]
  },

  "Insight": {
    "core_problem": "架构复杂度与团队能力不匹配 = 项目失败",
    "why_act_now": "架构决策在MVP阶段锁定，后期重构成本指数级增长",
    "cost_of_inaction": "强行上微服务 → 开发延期 → 错过市场窗口 → 项目失败"
  },

  "Outcome": {
    "action": "采用Monolith架构启动，强制模块化设计，3个月后评估拆分时机",
    "success_criteria": [
      "MVP按时上线（3个月内）",
      "识别3个清晰模块边界",
      "代码模块化评分>8/10",
      "单元测试覆盖率>80%"
    ],
    "deadline": "72小时内完成技术方案设计 + 3个月完成MVP开发"
  }
}
```

---

## T4: Coil - 张力弹簧（执行层）

### 核心功能
压缩不确定性，触发行动阈值

### 张力弹簧机制

```
        高度不确定性（无法行动）
                  ↑
                  │     弹簧压缩
                  │    ╱
                  │   ╱
                  │  ╱
                  │ ╱
                  │╱
                  └──────────→ 行动阈值
                 ╱│
                ╱ │
               ╱  │
              ╱   │
             ╱    │  弹簧释放
            ╱     │
           ↓      ↓
    低不确定性（可以行动）
```

### 不确定性压缩

```python
class UncertaintyCompressor:
    """不确定性压缩器"""
    
    def compress(self, questions, unknowns):
        """
        将不确定性压缩为可行动阈值
        
        压缩策略：
        1. 信息获取成本 < 决策价值 → 获取信息
        2. 信息获取成本 > 决策价值 → 接受不确定性
        3. 可并行执行 → 并行化
        4. 可延迟决策 → 设置触发条件
        """
        
        compressed = []
        
        for q in questions:
            if q.acquisition_cost < q.decision_value:
                # 值得获取信息
                compressed.append(Action("获取信息", q))
            else:
                # 接受不确定性，设置风险对冲
                compressed.append(RiskMitigation(q))
        
        # 计算可压缩性
        compressibility = self.calculate_compressibility(compressed)
        
        return {
            "compressed_actions": compressed,
            "compressibility": compressibility,
            "can_act": compressibility > ACTION_THRESHOLD
        }
```

---

## T5: Stress Test - 压力测试（验证层）

### 核心功能
红队攻击核心假设，识别脆性

### 三种红队攻击

#### 攻击1：反例攻击

```python
def counter_example_attack(assumption):
    """
    提供具体场景使假设失效
    
    示例：
    假设："团队小，选Monolith更简单"
    
    反例：
    "如果团队虽小（5人）但地理分布在3个国家，
     需要独立部署窗口，Monolith反而更复杂"
    """
    
    # 生成反例
    counter_example = generate_counter_scenario(assumption)
    
    # 验证反例是否破坏假设
    if breaks_assumption(counter_example, assumption):
        return {
            "attack_successful": True,
            "counter_example": counter_example,
            "vulnerability": "假设在分布式场景下失效"
        }
    
    return {"attack_successful": False}
```

#### 攻击2：边界条件攻击

```python
def boundary_condition_attack(assumption):
    """
    找出假设失效的临界点
    
