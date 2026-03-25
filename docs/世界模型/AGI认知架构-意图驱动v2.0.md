# AGI 认知架构：真正的意图驱动实现方案

> 版本：v2.0 | 核心理念：意图驱动、认知涌现、非预设流程

---

## 一、核心问题诊断

### 硬编码问题列表

```python
# 问题1：意图识别是关键词匹配
self.intent_patterns = {
    "question": ["什么", "为什么", "如何", "?"],
    "request": ["帮我", "请", "能不能"],
}

# 问题2：复杂度估计是规则判断
if len(user_input) > 50:
    complexity += 1

# 问题3：工具选择是硬编码映射
tool_keywords = {
    "search": ["搜索", "查一下"],
    "calculator": ["计算", "多少"],
}

# 问题4：推理类型是关键词选择
if "如果" in user_input:
    return "deductive"

# 问题5：System 1/2 切换是预设分支
if complexity >= 3:
    return CognitionMode.SYSTEM_2
```

---

## 二、意图驱动架构设计

### 2.1 核心理念

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        真正的 AGI 认知循环                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────────────────────────────────────────────────────────────┐     │
│    │                         意图层                                   │     │
│    │  ┌───────────────────────────────────────────────────────────┐  │     │
│    │  │  用户意图 (What does the user REALLY want?)              │  │     │
│    │  │  → 不是意图类型标签，而是期望的结果状态                    │  │     │
│    │  │  → 由 LLM 深层理解，而非关键词匹配                         │  │     │
│    │  └───────────────────────────────────────────────────────────┘  │     │
│    └────────────────────────────┬────────────────────────────────────────┘     │
│                                 │                                              │
│                                 ▼                                              │
│    ┌──────────────────────────────────────────────────────────────────┐     │
│    │                        认知状态                                 │     │
│    │  ┌───────────────────────────────────────────────────────────┐  │     │
│    │  │  当前认知状态 (What do I know now?)                       │  │     │
│    │  │  → 动态更新，非预设                                         │  │     │
│    │  │  → 由推理过程自涌现                                         │  │     │
│    │  └───────────────────────────────────────────────────────────┘  │     │
│    └────────────────────────────┬────────────────────────────────────────┘     │
│                                 │                                              │
│                                 ▼                                              │
│    ┌──────────────────────────────────────────────────────────────────┐     │
│    │                        行动决策                                  │     │
│    │  ┌───────────────────────────────────────────────────────────┐  │     │
│    │  │  下一步行动 (What should I do next?)                     │  │     │
│    │  │  → LLM 自主决策，而非硬编码逻辑                            │  │     │
│    │  │  → 基于当前意图+认知状态                                   │  │     │
│    │  └───────────────────────────────────────────────────────────┘  │     │
│    └────────────────────────────┬────────────────────────────────────────┘     │
│                                 │                                              │
│              ┌──────────────────┼──────────────────┐                           │
│              ▼                  ▼                  ▼                           │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│    │   推理        │  │   工具       │  │   记忆       │                     │
│    │  (Reason)   │  │   (Tool)    │  │  (Memory)   │                     │
│    └──────────────┘  └──────────────┘  └──────────────┘                     │
│              │                  │                  │                           │
│              └──────────────────┼──────────────────┘                           │
│                                 │                                              │
│                                 ▼                                              │
│    ┌──────────────────────────────────────────────────────────────────┐     │
│    │                       状态更新                                  │     │
│    │  ┌───────────────────────────────────────────────────────────┐  │     │
│    │  │  更新认知状态 → 评估是否达成意图 → 继续或终止            │  │     │
│    │  └───────────────────────────────────────────────────────────┘  │     │
│    └──────────────────────────────────────────────────────────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.2 意图驱动的认知循环

```python
"""
真正的意图驱动认知循环

核心理念：
1. 不预设认知流程
2. 每一步由 LLM 自主决策
3. 意图作为持续的目标状态
4. 认知状态动态更新
5. 循环直到意图达成或无法继续
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import asyncio


class CognitiveAction(Enum):
    """认知行动类型 - 由 LLM 自主选择"""
    THINK = "think"              # 深入思考/推理
    RETRIEVE_MEMORY = "retrieve"  # 检索记忆
    USE_TOOL = "tool"            # 使用工具
    ASK_CLARIFICATION = "ask"    # 询问澄清
    RESPOND = "respond"          # 生成响应
    STOP = "stop"                # 停止


@dataclass
class Intention:
    """用户意图 - 深层理解"""
    desired_state: str           # 用户期望的结果状态
    constraints: List[str]       # 约束条件
    implicit_needs: List[str]    # 隐含需求（LLM 推断）
    original_query: str          # 原始query
    

@dataclass
class CognitiveState:
    """动态认知状态"""
    current_knowledge: Dict[str, Any] = field(default_factory=dict)
    gaps: List[str] = field(default_factory=list)      # 认知缺口
    confidence: float = 0.0
    reasoning_steps: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    memory_retrieved: List[Dict] = field(default_factory=list)


@dataclass
class ActionDecision:
    """行动决策 - LLM 自主选择"""
    action: CognitiveAction
    reason: str                  # 为什么选择这个行动
    parameters: Dict[str, Any]   # 行动参数
    expected_outcome: str        # 期望结果


class IntentionDrivenCognition:
    """
    意图驱动的认知引擎
    
    核心区别于 v1.0：
    - 无预设流程
    - LLM 自主决策每一步
    - 意图作为持续目标
    - 认知状态动态涌现
    """
    
    def __init__(self, llm, memory_system, tool_executor):
        self.llm = llm
        self.memory = memory_system
        self.tools = tool_executor
        
        # 循环控制
        self.max_iterations = 10
        self.min_confidence = 0.8
        
    async def process(self, user_query: str) -> Dict[str, Any]:
        """
        意图驱动的认知循环
        
        流程：
        1. 深层理解用户意图
        2. 初始化认知状态
        3. 循环：
           - LLM 决策下一步行动
           - 执行行动
           - 更新认知状态
           - 检查意图是否达成
        4. 生成响应
        """
        
        # ===== 步骤1：深层理解意图 =====
        intention = await self._understand_intention(user_query)
        
        # ===== 步骤2：初始化认知状态 =====
        state = CognitiveState()
        
        # ===== 步骤3：认知循环 =====
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # ===== 3.1 LLM 自主决策下一步 =====
            decision = await self._decide_next_action(
                intention=intention,
                state=state,
                iteration=iteration
            )
            
            # ===== 3.2 记录决策理由 =====
            state.reasoning_steps.append(
                f"[{iteration}] {decision.action.value}: {decision.reason}"
            )
            
            # ===== 3.3 执行行动 =====
            result = await self._execute_action(
                decision=decision,
                intention=intention,
                state=state
            )
            
            # ===== 3.4 更新认知状态 =====
            state = self._update_state(state, decision, result)
            
            # ===== 3.5 检查意图是否达成 =====
            intent_achieved = await self._check_intention_achieved(
                intention=intention,
                state=state
            )
            
            if intent_achieved:
                break
                
            # 如果是 STOP 行动，退出循环
            if decision.action == CognitiveAction.STOP:
                break
        
        # ===== 步骤4：生成最终响应 =====
        response = await self._generate_response(intention, state)
        
        return {
            "response": response,
            "intention": {
                "desired_state": intention.desired_state,
                "implicit_needs": intention.implicit_needs
            },
            "cognitive_trace": state.reasoning_steps,
            "final_state": {
                "confidence": state.confidence,
                "knowledge": state.current_knowledge,
                "gaps": state.gaps
            },
            "iterations": iteration
        }
    
    async def _understand_intention(self, query: str) -> Intention:
        """
        深层理解用户意图
        
        关键：不进行意图分类，而是理解用户真正想要什么
        """
        prompt = f"""深入理解用户的真实意图。

用户说：{query}

请分析：
1. 用户期望达成什么结果状态？（具体描述）
2. 用户有什么隐含需求（没说但可能需要的）？
3. 用户有什么约束条件？

直接输出你的分析，不要问问题。"""
        
        analysis = await self.llm.chat(prompt)
        
        # 解析分析结果（简化版，实际可用结构化输出）
        return Intention(
            desired_state=self._extract_desired_state(analysis),
            constraints=self._extract_constraints(analysis),
            implicit_needs=self._extract_implicit_needs(analysis),
            original_query=query
        )
    
    async def _decide_next_action(
        self,
        intention: Intention,
        state: CognitiveState,
        iteration: int
    ) -> ActionDecision:
        """
        LLM 自主决策下一步行动
        
        这是最关键的差异：不是预设逻辑，而是 LLM 自主判断
        """
        # 构建上下文
        context = self._build_decision_context(
            intention=intention,
            state=state,
            iteration=iteration
        )
        
        prompt = f"""你是 AGI 认知引擎的核心决策模块。

当前情况：
{context}

你需要决定下一步做什么。选择以下行动之一：
- THINK: 需要更多推理/思考
- RETRIEVE_MEMORY: 需要从记忆中获取信息
- USE_TOOL: 需要使用工具获取信息
- ASK_CLARIFICATION: 需要向用户澄清
- RESPOND: 有足够信息可以回答
- STOP: 无法继续，应该停止

决策格式：
行动: [选择]
理由: [为什么]
参数: [具体参数，如工具名、搜索词等]
期望结果: [执行后期望获得什么]

请基于当前情况做出最佳决策："""
        
        decision_text = await self.llm.chat(prompt)
        
        # 解析决策
        return self._parse_decision(decision_text)
    
    async def _execute_action(
        self,
        decision: ActionDecision,
        intention: Intention,
        state: CognitiveState
    ) -> Any:
        """执行决策的行动"""
        
        if decision.action == CognitiveAction.THINK:
            # 深入推理
            return await self._think_deeply(
                intention=intention,
                state=state,
                context=decision.parameters.get("thinking_prompt", "")
            )
            
        elif decision.action == CognitiveAction.RETRIEVE_MEMORY:
            # 检索记忆
            return await self.memory.retrieve(
                query=decision.parameters.get("query", intention.original_query),
                top_k=5
            )
            
        elif decision.action == CognitiveAction.USE_TOOL:
            # 使用工具
            tool_name = decision.parameters.get("tool_name")
            params = decision.parameters.get("params", {})
            return await self.tools.execute(tool_name, params)
            
        elif decision.action == CognitiveAction.ASK_CLARIFICATION:
            # 生成澄清问题
            return decision.parameters.get("question", "我需要更多信息")
            
        elif decision.action == CognitiveAction.RESPOND:
            # 准备响应
            return {"ready_to_respond": True}
            
        elif decision.action == CognitiveAction.STOP:
            return {"stop_reason": decision.parameters.get("reason", "无法继续")}
        
        return None
    
    def _update_state(
        self,
        state: CognitiveState,
        decision: ActionDecision,
        result: Any
    ) -> CognitiveState:
        """根据行动结果更新认知状态"""
        
        new_state = CognitiveState(
            current_knowledge=state.current_knowledge.copy(),
            gaps=state.gaps.copy(),
            reasoning_steps=state.reasoning_steps.copy(),
            tools_used=state.tools_used.copy(),
            memory_retrieved=state.memory_retrieved.copy()
        )
        
        if decision.action == CognitiveAction.THINK:
            # 推理增加知识
            if isinstance(result, dict) and result.get("insights"):
                new_state.current_knowledge.update(result["insights"])
                
        elif decision.action == CognitiveAction.RETRIEVE_MEMORY:
            # 记忆检索结果
            new_state.memory_retrieved = result
            # 从记忆中提取新知识
            for mem in result:
                if mem.get("content"):
                    new_state.current_knowledge[mem.get("source", "memory")] = mem["content"]
                    
        elif decision.action == CognitiveAction.USE_TOOL:
            # 工具执行结果
            new_state.tools_used.append(decision.parameters.get("tool_name"))
            new_state.current_knowledge["tool_result"] = result
            
        # 更新置信度（简化版）
        new_state.confidence = self._estimate_confidence(new_state)
        
        # 识别认知缺口
        new_state.gaps = self._identify_gaps(new_state, decision)
        
        return new_state
    
    async def _check_intention_achieved(
        self,
        intention: Intention,
        state: CognitiveState
    ) -> bool:
        """检查意图是否达成"""
        
        prompt = f"""评估用户意图是否已达成。

用户原始意图：{intention.desired_state}

当前认知状态：
- 已获取知识：{list(state.current_knowledge.keys())}
- 置信度：{state.confidence}
- 认知缺口：{state.gaps}

请判断：
意图是否达成？ 是/否
理由："""
        
        result = await self.llm.chat(prompt)
        return "是" in result and state.confidence >= self.min_confidence
    
    async def _generate_response(
        self,
        intention: Intention,
        state: CognitiveState
    ) -> str:
        """生成最终响应"""
        
        prompt = f"""基于最终认知状态生成响应。

用户意图：{intention.desired_state}

已知信息：
{self._format_knowledge(state.current_knowledge)}

检索到的记忆：
{self._format_memories(state.memory_retrieved)}

请生成最终回答："""
        
        return await self.llm.chat(prompt)
    
    # ===== 辅助方法 =====
    
    def _build_decision_context(
        self,
        intention: Intention,
        state: CognitiveState,
        iteration: int
    ) -> str:
        """构建决策上下文"""
        
        context = f"""
=== 第 {iteration} 轮决策 ===

【用户意图】
期望状态：{intention.desired_state}
隐含需求：{intention.implicit_needs}

【当前认知状态】
已掌握知识：{list(state.current_knowledge.keys())}
置信度：{state.confidence}
已使用工具：{state.tools_used}
已检索记忆：{len(state.memory_retrieved)} 条

【认知缺口】
{state.gaps if state.gaps else "无"}

【已执行步骤】
"""
        for step in state.reasoning_steps[-3:]:
            context += f"- {step}\n"
            
        return context
    
    def _parse_decision(self, decision_text: str) -> ActionDecision:
        """解析 LLM 的决策输出"""
        
        # 简化解析，实际可用更复杂的结构化输出
        lines = decision_text.split("\n")
        
        action = CognitiveAction.THINK
        reason = ""
        params = {}
        expected = ""
        
        for line in lines:
            if line.startswith("行动:"):
                action_str = line.split(":")[1].strip().lower()
                if "tool" in action_str:
                    action = CognitiveAction.USE_TOOL
                elif "memory" in action_str or "retrieve" in action_str:
                    action = CognitiveAction.RETRIEVE_MEMORY
                elif "respond" in action_str:
                    action = CognitiveAction.RESPOND
                elif "ask" in action_str:
                    action = CognitiveAction.ASK_CLARIFICATION
                elif "stop" in action_str:
                    action = CognitiveAction.STOP
            elif line.startswith("理由:"):
                reason = line.split(":")[1].strip()
            elif line.startswith("参数:"):
                # 简化处理
                params = {}
            elif line.startswith("期望"):
                expected = line.split(":")[1].strip() if ":" in line else ""
        
        return ActionDecision(
            action=action,
            reason=reason,
            parameters=params,
            expected_outcome=expected
        )
    
    def _estimate_confidence(self, state: CognitiveState) -> float:
        """估计当前置信度"""
        # 简化版：根据信息量估计
        base = 0.3
        base += min(len(state.current_knowledge) * 0.1, 0.3)
        base += min(len(state.memory_retrieved) * 0.05, 0.2)
        
        if state.tools_used:
            base += 0.1
            
        return min(base, 0.95)
    
    def _identify_gaps(self, state: CognitiveState, last_decision: ActionDecision) -> List[str]:
        """识别认知缺口"""
        gaps = []
        
        # 简化版
        if not state.current_knowledge.get("tool_result"):
            gaps.append("缺乏外部信息")
            
        if not state.memory_retrieved:
            gaps.append("缺乏记忆参考")
            
        return gaps
    
    def _extract_desired_state(self, analysis: str) -> str:
        # 简化实现
        return analysis.split("\n")[0][:200]
    
    def _extract_constraints(self, analysis: str) -> List[str]:
        return []
    
    def _extract_implicit_needs(self, analysis: str) -> List[str]:
        return []
    
    def _format_knowledge(self, knowledge: Dict) -> str:
        return "\n".join([f"- {k}: {v}" for k, v in knowledge.items()])
    
    def _format_memories(self, memories: List) -> str:
        if not memories:
            return "无"
        return "\n".join([f"- {m.get('content', '')[:100]}" for m in memories[:3]])
```

---

## 三、与 v1.0 的核心差异

| 维度 | v1.0 (硬编码) | v2.0 (意图驱动) |
|------|-------------|----------------|
| **意图理解** | 分类为 question/request/command | 深层理解期望的结果状态 |
| **流程控制** | 预设 System 1 → System 2 分支 | LLM 自主决策每一步 |
| **工具选择** | 关键词匹配工具 | LLM 根据需要自主选择 |
| **推理方式** | 预设演绎/归纳/类比 | LLM 决定需要何种推理 |
| **状态更新** | 固定字段更新 | 动态涌现的知识结构 |
| **停止条件** | 置信度阈值预设 | LLM 判断意图是否达成 |

---

## 四、架构对比图

### v1.0 架构（预设流程）

```
用户输入
    │
    ▼
┌─────────────────┐
│  意图识别       │ ──→ 硬编码意图分类
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  复杂度估计     │ ──→ 规则判断
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
Syst-1   System-2   ← 预设分支
    │         │
    ▼         ▼
预设工具   预设推理
映射       方式
    │         │
    └────┬────┘
         │
         ▼
     生成响应
```

### v2.0 架构（意图驱动）

```
用户输入
    │
    ▼
┌─────────────────┐
│  深层意图理解   │ ← LLM 理解真正想要的
└────────┬────────┘
         │
         ▼
    认知状态初始化
         │
         ▼
   ┌─────┴─────┐
   │  LLM 决策  │ ◄─── 自主判断下一步
   │  下一步    │
   └─────┬─────┘
         │
    ┌────┼────┬────┐
    ▼   ▼   ▼   ▼
  推理 工具 记忆 询问
    │   │   │   │
    └────┼────┴────┘
         │
         ▼
    认知状态更新
         │
         ▼
   LLM 判断意图
    是否达成?
         │
    ┌────┴────┐
    ▼         ▼
  是→响应   否→循环
```

---

## 五、关键实现要点

### 5.1 决策 Prompt 的重要性

```python
# v2.0 的核心：让 LLM 自己做决策

prompt = f"""你是 AGI 认知引擎的核心决策模块。

当前情况：
{context}

你需要决定下一步做什么。选择以下行动之一：
- THINK: 需要更多推理/思考
- RETRIEVE_MEMORY: 需要从记忆中获取信息
- USE_TOOL: 需要使用工具获取信息
...

请基于当前情况做出最佳决策："""
```

### 5.2 结构化输出的使用

```python
# 可以用结构化输出确保决策可解析
from pydantic import BaseModel

class Decision(BaseModel):
    action: Literal["think", "retrieve", "tool", "ask", "respond", "stop"]
    reason: str
    parameters: Dict[str, Any]
    expected_outcome: str

# 使用 LLM 输出结构化 JSON
decision = llm.chat_json(prompt, response_model=Decision)
```

### 5.3 循环安全机制

```python
# 防止无限循环
self.max_iterations = 10  # 最大迭代次数
self.escalation_threshold = 5  # 多次失败后升级处理
```

---

## 六、总结

**v2.0 的本质变革：**

1. **从预设流程 → 动态涌现**
   - 不再预设"先做什么、后做什么"
   - 每一步由 LLM 自主判断

2. **从意图分类 → 意图理解**
   - 不再将意图分为"question/request/command"
   - 理解用户真正想要的结果状态

3. **从规则匹配 → 自主决策**
   - 工具选择、推理方式不再硬编码
   - LLM 根据上下文自主决定

4. **从状态更新 → 知识涌现**
   - 认知状态不是预设字段
   - 由推理过程动态构建

**代价：**
- 更多的 LLM 调用
- 更高的延迟
- 更复杂的调试

**收益：**
- 真正的通用智能
- 涌现性行为
- 适应未知场景
