Janus World Model 工程实现：全部关键决策 “以下每个回答都遵循一个原则：从神经网络和大模型的底层原理出发，而非从理论文档的修辞出发。 理论中的"相变"是美丽的隐喻，但工程实现必须还原为可编译、可测试、可度量的代码。”    第一组：地基审视 Q1. 现有代码与理论的真实距离 诚实评估——逐模块判定： 模块 判定 理由   IntentUnderstanding 保留骨架，替换内核 接口设计合理（understand() → IntentAnalysis），但正则提取必须替换为 LLM 驱动。数据结构 Intent（normalized, constraints, goals, priority）可直接复用。  HybridKnowledgeBase 保留并扩展 KG + VectorStore + RuleEngine 的三层结构正好对应表征面的三种法则形态。eval() 规则引擎需要替换为沙箱执行，但整体架构可用。  PlanningDrivenReasoning 保留骨架 WorldState → Action → Trajectory → Plan 的数据流是对的。LLMWorldModel 的 simulate() 接口是正确抽象——只是实现需要从字符串拼接升级为真正的状态转移。  LatentSpacePlanner 推倒重写 随机投影不是占位符问题，而是整个隐空间规划的前提不成立——在没有训练过的编码器的情况下，隐空间没有语义。需要用预训练 Embedding（LLM 的 hidden states）替代。  WorldModelBuilder 推倒重写 exec() 执行 LLM 生成的 Python 字符串是根本性的安全和可靠性问题。但其"从经验中合成程序"的思路是对的——这就是凝结过程。需要用结构化法则替代裸 Python 字符串。  KnowledgeGraphEvolver 保留并大幅扩展 漂移检测的接口 evolve(feedback) → EvolutionEvent 是对的，但实现（简单相等性检查）远远不够。需要扩展为模式检测 + 法则验证。  PerceptionModule / UnderstandingModule / ReasoningModule 修复并接入 这三个模块是反表征面的雏形。设计意图正确，但 CognitiveEngine 的缺失模块（planning.py, execution.py, reflection.py）需要补齐。   顶层类决策： 不需要推倒 UASWorldModelService。正确做法是在其上方构建 JanusWorldModel 作为编排层，让 UASWorldModelService 退化为表征面的服务接口：   JanusWorldModel（新建，顶层编排）
├── RepresentationalFace（基于现有 UASWorldModelService 扩展）
├── EnactiveFace（基于修复后的 CognitiveEngine 构建）
├── PhaseManager（全新）
└── EvolutionLoop（基于现有 KnowledgeGraphEvolver 扩展）  集成边界： uas_world_model/ 是认知内核（纯 Python 库，无 IO），asui-cli/src/asui/runtime/ 是运行时外壳（负责文件 IO、子进程、工作流编排）。集成点是 RuntimeManager.run() 内部——在执行 LLM 步骤时，不再调用硬编码的 AgentOrchestrator，而是调用 JanusWorldModel.tick()。具体地：   # runtime_manager.py 中的变更
from uas_world_model import JanusWorldModel
 
class RuntimeManager:
    def __init__(self, app_root, ...):
        self.janus = JanusWorldModel(knowledge_base=self._load_knowledge(app_root))
    
    def run(self, topic, ...):
        # 原有的线性工作流保留为"骨架"
        # 但每个步骤的执行委托给 Janus
        for step in workflow_steps:
            result = self.janus.tick(step, cognitive_state)
            # Janus 内部决定用表征面还是反表征面处理    Q2. "表征面"的第一行代码——法则的数据结构 这是零号问题。 一切相变操作都以此为基础。 核心洞察： 从大模型原理看，"法则"本质上是条件不变量（Conditional Invariant）——在特定上下文下稳定成立的因果关系。它不是单一形态的，而是同一知识的多重投影——就像一个三维物体在不同平面上有不同的投影，但指向同一个实体。 具体数据结构定义：   @dataclass
class Law:
    """Janus World Model 的原子知识单元"""
    
    id: str                          # 全局唯一标识
    version: int                     # 版本号，支持演化追踪
    
    # ===== 表征投影 1：自然语言（供 LLM 消费/活化） =====
    natural_language: str
    # 例："当候选人的核心技能与岗位 JD 的必需技能重叠度 ≥ 70% 时，
    #      该候选人进入面试的概率显著高于平均水平。"
    
    # ===== 表征投影 2：结构化谓词（供符号匹配/检索） =====
    predicate: LawPredicate
    # predicate.condition = {"skill_overlap": {"op": ">=", "value": 0.7}}
    # predicate.consequence = {"interview_probability": {"op": ">", "value": "avg"}}
    # predicate.scope = {"domain": "recruitment", "entity_types": ["Candidate", "Job"]}
    
    # ===== 表征投影 3：可执行函数（供验证/测试） =====
    executable: Optional[Callable]
    # def law_fn(candidate, job) -> LawResult:
    #     overlap = skill_overlap(candidate.skills, job.required_skills)
    #     return LawResult(holds=(overlap >= 0.7), confidence=...)
    # 注：不用 exec()，而是注册的 Python 函数引用
    
    # ===== 表征投影 4：因果子图（供推理/传播） =====
    causal_fragment: Optional[CausalGraph]
    # nodes: [SkillOverlap, InterviewProbability]
    # edges: [SkillOverlap --causes--> InterviewProbability]
    
    # ===== 元数据：溯源与治理 =====
    provenance: LawProvenance
    # origin: "crystallized" | "injected" | "sublimated"
    # source_experiences: List[str]   # 凝结自哪些经验
    # created_at: datetime
    # validated: bool
    # validation_method: str          # "replay" | "ab_test" | "expert_review"
    # confidence: float               # 0.0 ~ 1.0
    # usage_count: int                # 被活化的次数
    # success_rate: float             # 活化后验证成功率
 
@dataclass
class LawPredicate:
    condition: Dict[str, Any]         # 触发条件（结构化）
    consequence: Dict[str, Any]       # 预期结果（结构化）
    scope: Dict[str, Any]             # 适用范围（领域/实体类型/场景）
    negation: Optional[Dict]          # 反面——何时此法则不成立  一致性保障机制： 四种投影不是独立维护的，而是从同一个 canonical form 生成。canonical form 选择自然语言 + 结构化谓词的组合（这两者信息量最大），然后： • executable 由 LLM 从 natural_language + predicate 生成（代码生成），经沙箱测试后注册 • causal_fragment 由 predicate 的条件/结果自动提取 • 当任一投影被修改时，触发一致性检查（其他投影是否需要同步更新）  第一行代码：定义 Law 和 LawStore，然后将现有 configs/ 中的 JSON 规则迁移为第一批法则。   Q3. "反表征面"的第一行代码 关键认知：在纯软件系统中，"环境"就是业务领域的状态空间。 大模型的根本原理是：它通过 next-token prediction 学到了一个隐式的世界模型——给定上下文，预测下一步。反表征面要做的，就是让这个隐式世界模型与外部业务状态形成闭环。 Agent 感知的"环境"：   环境 = {
    业务状态: 数据库中的实体状态（candidates, jobs, evaluations...）
    认知状态: CognitiveStateStore 中的当前思考进度
    法则库状态: 哪些法则可用、哪些已激活
    交互历史: 最近 N 次行动及其结果
}  耦合回路的实现——扩展的 ReAct，但不是经典 ReAct： 经典 ReAct 是 Thought → Action → Observation → Thought → ...，线性且无记忆。Janus 的耦合回路是有状态的、法则引导的 ReAct：   class EnactiveFace:
    """反表征面：感知-行动耦合引擎"""
    
    def coupling_loop(self, task, env_state, active_laws: List[Law]) -> CouplingResult:
        """一次完整的耦合循环"""
        
        # 1. 感知（Perception）—— 不是"读取"环境，而是"关注"环境
        #    active_laws 决定了关注什么（类似注意力机制）
        perception = self.perceive(env_state, attention_filter=active_laws)
        
        # 2. 理解（Understanding）—— LLM 作为理解引擎
        #    将感知到的信号与任务上下文融合
        understanding = self.understand(perception, task)
        
        # 3. 决策（Decision）—— 法则引导但不限定
        #    active_laws 作为 soft constraints 注入 LLM prompt
        #    LLM 在法则约束空间内自主选择行动
        action = self.decide(understanding, active_laws)
        
        # 4. 执行（Action）—— 通过 ToolGateway 与环境交互
        outcome = self.act(action, env_state)
        
        # 5. 反馈（Feedback）—— 记录经验元组
        experience = Experience(
            state_before=env_state,
            perception=perception,
            action=action,
            outcome=outcome,
            active_laws=[l.id for l in active_laws],
            timestamp=now()
        )
        self.experience_buffer.append(experience)
        
        return CouplingResult(action=action, outcome=outcome, experience=experience)  对现有模块的决策：修复 CognitiveEngine 路径。 理由：PerceptionModule、UnderstandingModule、ReasoningModule 的设计意图与反表征面高度一致。需要补齐缺失的三个模块（PlanningModule、ExecutionModule、ReflectionModule），并将 CognitiveEngine 的六阶段管道改造为上述耦合回路。不是另起炉灶，而是填补断裂，然后升级。   第二组：相变机制 Q4. 凝结的触发条件 从大模型原理看凝结的本质： 凝结 = 从经验序列中提取可压缩的不变量。这在信息论中有精确对应——如果一组经验可以被一条法则显著压缩（描述长度大幅缩短），那么这条法则就是"真的"。 模式检测算法——三级递进：   Level 1：统计频率（简单但有效）
─────────────────────────────
从 experience_buffer 中提取 (condition, consequence) 对
统计频率：当 condition 出现时，consequence 出现的条件概率 P(consequence|condition)
如果 P > threshold 且样本量 > min_samples → 候选法则

Level 2：LLM 归纳总结（处理模糊模式）
─────────────────────────────────────
将最近 N 条经验打包送入 LLM：
"以下是系统最近的 {N} 次决策经验。请识别其中反复出现的因果模式。
 对每个模式，给出：条件、结果、你的置信度。
 只报告出现 3 次以上的模式。"

Level 3：因果验证（区分相关与因果）
─────────────────────────────────
对 Level 1/2 产出的候选法则，进行反事实检验：
在历史数据中找到"条件成立但未执行该行动"的案例
检查结果是否不同 → 如果不同，支持因果关系  将 DriftDetection 升级为模式发现：   class PatternDetector:
    """从 DriftDetection 升级：不仅检测偏差，还发现新模式"""
    
    def detect(self, experience_buffer: List[Experience]) -> List[CandidateLaw]:
        candidates = []
        
        # 1. 频率分析
        freq_patterns = self._frequency_analysis(experience_buffer)
        
        # 2. LLM 归纳（批量，非逐条）
        if len(experience_buffer) >= self.batch_threshold:
            llm_patterns = self._llm_induction(experience_buffer[-self.window_size:])
            freq_patterns = self._merge_patterns(freq_patterns, llm_patterns)
        
        # 3. 对每个候选模式，生成 CandidateLaw
        for pattern in freq_patterns:
            candidate = CandidateLaw(
                natural_language=pattern.description,
                predicate=pattern.to_predicate(),
                confidence=pattern.frequency_confidence,
                source_experiences=pattern.evidence_ids,
                needs_validation=True
            )
            candidates.append(candidate)
        
        return candidates  验证标准——"法则"vs"噪声"的区分： 核心标准是跨场景可复现性。一条法则必须在至少 3 个不同的场景实例中成立。验证流程： 1. 历史回放验证：在 experience_buffer 中回放——候选法则是否能正确预测已观察到的结果？准确率 > 80% 才通过。 2. 前瞻验证：将候选法则标记为 provisional，在后续 N 次实践中观察其预测是否成立。成功率 > 70% 才升级为 validated。 3. G 层审核：validated 的法则进入治理审核队列，审核通过后正式入库。    Q5. 活化的工程实现 "引导但不限定"的精确工程含义： 从大模型原理看，这就是条件化生成（Conditioned Generation）。法则作为软约束注入 LLM 的上下文，影响但不完全决定输出分布。 三层活化机制：   Layer 1：Prompt 注入（最轻量）
──────────────────────────
将相关法则的 natural_language 注入 system prompt：
"以下是当前场景的已知规律（仅供参考，非硬性规则）：
 1. {law.natural_language}
 2. {law.natural_language}
 请在决策时考虑这些规律，但允许根据具体情况做出例外判断。"

→ LLM 的注意力机制自然地将法则融入推理过程
→ "仅供参考" 的措辞确保不限定

Layer 2：规划约束（中等强度）
───────────────────────────
将法则的 predicate 转化为规划器的约束条件：
PlanningDrivenReasoning.plan(
    current_state, goal_state, actions,
    soft_constraints=[law.predicate for law in active_laws]
)

→ 在 trajectory 评估时，符合法则的路径获得奖励加成
→ 违反法则的路径获得惩罚，但不被排除

Layer 3：环境规则（最强力度）
───────────────────────────
将法则的 executable 注册为环境的验证规则：
每次行动前，执行 law.executable(state, action)
如果返回 violation → 发出警告但不阻断（软约束）
如果返回 critical_violation → 阻断并要求重新规划（硬约束）  法则冲突处理：   def resolve_conflicts(active_laws: List[Law], context) -> List[Law]:
    """当多条法则冲突时的消解策略"""
    
    # 1. 特异性优先：scope 更窄的法则优先于更宽的
    #    （类似 CSS 选择器的特异性规则）
    laws_by_specificity = sorted(active_laws, key=lambda l: l.predicate.scope_specificity, reverse=True)
    
    # 2. 置信度加权：高置信度法则优先
    
    # 3. 新鲜度：最近被验证过的法则优先
    
    # 4. 如果仍然冲突 → 提交给 LLM 裁决
    #    "以下两条规律对当前场景给出了矛盾的指引。
    #     请根据当前具体上下文，判断哪条更适用，并解释原因。"
    
    # 5. 裁决结果本身可能成为一条新的候选法则（凝结的种子）  改造线性管道： 不是消灭线性工作流，而是在每个步骤内部嵌入动态行为空间：   # 原来：每个步骤固定执行一个操作
for step in workflow_steps:
    result = execute_step(step)  # 硬编码
 
# 改造后：每个步骤是一个"耦合点"，Janus 决定如何执行
for step in workflow_steps:
    # 1. 活化相关法则
    active_laws = janus.representational_face.retrieve_laws(step.context)
    
    # 2. 在法则引导下执行耦合循环（可能多轮）
    result = janus.enactive_face.coupling_loop(
        task=step, env_state=current_state, active_laws=active_laws
    )
    
    # 3. 记录经验（为未来凝结积累素材）
    janus.experience_buffer.record(result.experience)    Q6. 蒸发与凝华 区分"涌现"与"聚合"的判据： 从信息论出发——涌现 = 整体的信息量 > 部分之和。具体度量：   def is_emergence(agent_outputs: List[str], fused_output: str, llm) -> EmergenceMetric:
    """判断融合结果是否构成涌现"""
    
    # 1. 新颖度：融合结果中包含多少"不在任何单个 Agent 输出中"的信息
    novel_claims = extract_claims(fused_output) - union(extract_claims(o) for o in agent_outputs)
    novelty = len(novel_claims) / len(extract_claims(fused_output))
    
    # 2. 非可导出性：这些新信息能否从单个输出逻辑推导出？
    #    让 LLM 判断：每个 novel_claim 是否是某个 agent_output 的逻辑推论
    non_derivable = [c for c in novel_claims if not llm.is_derivable(c, agent_outputs)]
    emergence_ratio = len(non_derivable) / max(len(novel_claims), 1)
    
    # 3. 结构性：新信息是否引入了新的概念/关系/维度
    new_concepts = extract_concepts(non_derivable) - union(extract_concepts(o) for o in agent_outputs)
    
    return EmergenceMetric(
        novelty=novelty,
        emergence_ratio=emergence_ratio,
        new_concepts=new_concepts,
        is_genuine_emergence=(emergence_ratio > 0.3 and len(new_concepts) > 0)
    )  凝华的识别机制——三重门控：   Gate 1（自动）：涌现度量
    emergence_ratio > 0.3 且 new_concepts 非空
    → 进入凝华候选队列

Gate 2（自动）：可复现性
    在后续 3+ 次蜂群运行中，类似的涌现模式再次出现
    → 升级为"稳定涌现模式"

Gate 3（人机混合）：G 层治理
    稳定涌现模式提交人类审核（或高置信度 LLM 审核）
    审核通过 → 正式凝华为 Law
    审核不通过 → 标记为"已知涌现但不固化"    第三组：相变管理器 Q7. 认知状态评估指标 每个指标的具体计算：   class CognitiveStateAssessor:
    
    def assess(self, env_state, law_store, experience_buffer) -> CognitiveState:
        return CognitiveState(
            novelty=self._compute_novelty(env_state, law_store),
            representation_coverage=self._compute_coverage(env_state, law_store),
            pattern_stability=self._compute_stability(experience_buffer),
            task_complexity=self._compute_complexity(env_state)
        )
    
    def _compute_novelty(self, env_state, law_store) -> float:
        """当前输入与已知法则的最小距离"""
        # 将 env_state 编码为向量（LLM embedding）
        state_vec = self.encoder.encode(env_state.to_description())
        # 找最近的法则
        nearest_law, distance = law_store.nearest(state_vec)
        # 归一化到 [0, 1]——距离越大，新颖度越高
        return min(distance / self.novelty_scale, 1.0)
    
    def _compute_coverage(self, env_state, law_store) -> float:
        """法则覆盖了当前场景多少特征"""
        # 提取当前场景的特征集
        features = extract_features(env_state)
        # 检查每个特征是否有至少一条法则的 scope 覆盖
        covered = sum(1 for f in features if law_store.has_law_covering(f))
        return covered / max(len(features), 1)
    
    def _compute_stability(self, experience_buffer) -> float:
        """最近经验中模式的重复度"""
        if len(experience_buffer) < 10:
            return 0.0
        recent = experience_buffer[-50:]
        # 提取 (condition_hash, consequence_hash) 对
        pairs = [hash_pair(exp) for exp in recent]
        # 计算最频繁模式的频率
        counter = Counter(pairs)
        most_common_freq = counter.most_common(1)[0][1] / len(recent)
        return most_common_freq  阈值设定——自适应而非手动： 初始阈值从保守值开始（novelty_threshold=0.7, stability_threshold=0.4），然后基于相变成功率自适应调整：   # 如果最近 10 次凝结尝试中 >7 次成功 → 降低 stability_threshold（更积极凝结）
# 如果最近 10 次凝结尝试中 <3 次成功 → 提高 stability_threshold（更保守）
# 同理适用于其他阈值  元-元认知——不需要。 通过延迟确认避免误判：相变决策不是立即执行的，而是产生一个"相变提案"，在下一轮 tick 中确认或撤销。如果相变后的效果（通过反馈测量）比相变前差，自动回滚。这不需要额外的管理层，只需要相变操作的可逆性。   Q8. "训练"范式 "训练"在 Janus 中是三件不同的事： 阶段 含义 方法   冷启动 构建初始法则库 从现有 configs/ 规则迁移 + 从 docs/ 用 LLM 提取 + 领域专家注入  在线学习 系统运行中积累经验、凝结新法则 经验缓冲区 → 模式检测 → 候选法则 → 验证 → 入库  模拟训练 用模拟环境加速经验积累 历史数据回放 + 扰动（加噪声/改变条件）   模拟环境设计——Gym-like 抽象接口：   class DomainEnvironment(ABC):
    """领域环境抽象——Janus 的训练场"""
    
    @abstractmethod
    def reset(self, scenario_config) -> EnvState:
        """重置到初始状态"""
    
    @abstractmethod
    def step(self, action) -> Tuple[EnvState, float, bool, Dict]:
        """执行行动，返回 (新状态, 奖励, 是否结束, 额外信息)"""
    
    @abstractmethod
    def get_observation(self) -> Dict:
        """获取当前可观测状态"""
 
class RecruitmentEnvironment(DomainEnvironment):
    """招聘领域的模拟环境——基于历史数据回放"""
    
    def __init__(self, historical_data_path):
        self.historical_cases = load_cases(historical_data_path)
        # 每个 case = (candidate_profile, job_description, actual_outcome)
    
    def reset(self, scenario_config=None):
        self.current_case = random.choice(self.historical_cases)
        return self._to_env_state(self.current_case)
    
    def step(self, action):
        # action = Agent 的评估/匹配决策
        # 奖励 = 与历史实际结果的一致性
        reward = self._compute_reward(action, self.current_case.actual_outcome)
        return new_state, reward, True, {"actual": self.current_case.actual_outcome}  冷启动的具体步骤：   Step 1: 迁移现有规则（机械操作）
    configs/workflow_config.json → Law 对象
    configs/evaluation_criteria.json → Law 对象
    .claude/skills/*.md → LLM 提取 → Law 对象

Step 2: 从理论文档提取（LLM 辅助）
    docs/AI招聘世界模型.md → 提取领域法则
    docs/entity_event_model.md → 提取实体关系法则

Step 3: 标记为 "injected"（与凝结出的法则区分）
    所有冷启动法则的 provenance.origin = "injected"
    confidence 初始化为 0.5（需要通过实践验证才能升级）    第四组：与现实的碰撞 Q9. 第一个验证场景 选择 ai-recruitment-os。 理由：唯一健康运行的 sub app，有真实的业务逻辑，有足够的配置和规则可迁移。 招聘场景中的法则示例：   # 法则 1（粒度适中——实体级别）
Law(
    natural_language="当候选人简历中的核心技能与 JD 必需技能重叠度 ≥ 70% 时，初筛通过率显著高于平均水平",
    predicate=LawPredicate(
        condition={"skill_overlap": {"op": ">=", "value": 0.7}},
        consequence={"screening_pass_rate": {"op": ">", "value": "domain_avg"}},
        scope={"domain": "recruitment", "stage": "screening"}
    ),
    provenance=LawProvenance(origin="injected", confidence=0.5)
)
 
# 法则 2（更高层——流程级别）
Law(
    natural_language="初筛阶段的多维度评估（学历、经验、技能）比单一维度评估产生更稳定的面试通过预测",
    predicate=LawPredicate(
        condition={"evaluation_dimensions": {"op": ">=", "value": 3}},
        consequence={"prediction_stability": {"op": ">", "value": "single_dimension"}},
        scope={"domain": "recruitment", "stage": "screening"}
    )
)
 
# 法则 3（涌现候选——可能从蜂群中发现）
# 预期：多个评估 Agent 独立评分后，系统可能发现
# "当候选人的项目经验与岗位所在行业高度匹配时，
#  即使技能关键词重叠度较低，面试表现也往往优于预期"
# 这条法则不是预设的，而是凝结出来的  最小可验证实验（MVE）：   目标：在招聘场景中跑通一次完整的"活化→实践→凝结"闭环

前提条件：
    - 冷启动法则库（从 configs/ 迁移 5~10 条法则）
    - 3 组历史招聘案例作为模拟数据

实验步骤：
    1. 冷启动：将 evaluation_criteria.json 转化为 Law 对象，注入 LawStore
    2. 活化：对一个新的招聘任务，从 LawStore 检索相关法则，
       注入到评估 Agent 的 prompt 中
    3. 实践：Agent 执行简历评估，产生 experience
    4. 积累：运行 10 个案例，积累 experience_buffer
    5. 凝结触发：PatternDetector 从 10 条经验中检测是否有新模式
    6. 验证：如果检测到候选法则，在剩余历史数据上验证
    7. 可观测结果：
       - LawStore 中新增了 0~N 条法则（有就是成功凝结）
       - 新法则的验证通过率 > 50%（区分于噪声）

涉及的代码变更：
    - 新增：uas_world_model/core/law.py（Law 数据结构）
    - 新增：uas_world_model/core/law_store.py（法则存储与检索）
    - 新增：uas_world_model/core/pattern_detector.py（模式检测）
    - 新增：uas_world_model/core/janus.py（JanusWorldModel 顶层编排）
    - 修改：asui-cli/src/asui/runtime/runtime_manager.py（集成点）
    - 新增：uas_world_model/tests/test_crystallization.py（验证测试）    Q10. LLM 的确切角色 LLM 是"语义引擎"——既不是大脑，也不是顾问，而是"翻译官"。 从大模型原理出发：LLM 的核心能力是语义理解与生成——它能理解自然语言描述的法则，能将结构化数据翻译为人类可读的洞察，能将模糊的涌现模式命名为清晰的概念。但 LLM 不是可靠的推理器（会幻觉）、不是精确的计算器、不是确定性的状态机。 角色矩阵： 环节 LLM 的角色 非 LLM 的替代/补充   意图理解 主力——理解用户自然语言 结构化提取后交给符号系统验证  法则活化 翻译官——将结构化法则转为 prompt 法则检索由向量搜索完成  感知-行动耦合 决策建议——在法则约束下建议行动 行动执行由确定性系统完成  凝结（模式归纳） 辅助——帮助将统计模式命名为自然语言 模式检测由统计算法完成  凝华（涌现→法则） 催化剂——命名和描述涌现模式 涌现检测由信息论度量完成  规划 初稿生成——生成候选计划 计划验证由符号规划器完成  法则验证 不参与——验证必须是确定性的 历史数据回放 + 统计检验   关键原则：LLM 的输出永远不是最终决策，而是候选方案。 最终决策由符号系统（法则匹配、约束检查、统计验证）做出。这样可以： • 利用 LLM 的语义能力（理解、翻译、归纳） • 规避 LLM 的弱点（幻觉、不确定性、不可审计） • 保持系统的可解释性和可审计性（G 层要求）    Q11. 状态持久化 分层持久化策略： 数据类型 存储方案 理由   法则库（LawStore） JSON 文件 + Git 版本控制 法则数量有限（百~千级），需要版本追踪和回滚，Git diff 天然支持审计  认知状态 JSON 文件（保持现状） 与现有 CognitiveStateStore 兼容，状态量小  经验缓冲区 JSONL 追加文件 高写入频率，无需随机读取，只需顺序扫描  知识图谱 JSON 序列化（Phase 1）→ SQLite（Phase 2）→ 图数据库（Phase 3+） 渐进式升级，避免早期引入重依赖  相变历史 JSONL 审计日志 与现有 AuditEngine 对齐   法则版本控制：   class LawStore:
    def update_law(self, law_id, updates, reason):
        old_version = self.get(law_id)
        new_version = old_version.evolve(updates)  # 创建新版本，version += 1
        
        # 旧版本移入历史
        self.history[law_id].append(old_version)
        # 新版本成为当前版本
        self.current[law_id] = new_version
        
        # 记录审计日志
        self.audit.record(LawChangeEvent(
            law_id=law_id,
            old_version=old_version.version,
            new_version=new_version.version,
            reason=reason,
            timestamp=now()
        ))
    
    def rollback(self, law_id, to_version):
        """G 层治理可以触发回滚"""
        historical = self.history[law_id][to_version]
        self.current[law_id] = historical  崩溃恢复——不需要 WAL。 理由：相变操作是幂等的。如果凝结过程中崩溃，候选法则丢失，下一轮 tick 会重新检测模式并再次尝试凝结。如果活化过程中崩溃，Agent 的行动未完成，RuntimeManager 会重新调度。经验缓冲区用 JSONL 追加写入，天然抗崩溃。   第五组：优先级排序 Q12. 第一个 Pull Request 先实现的相变：活化（表征→实践）。 理由： 1. 活化是最简单的相变——从已有的法则库中检索法则，注入到 Agent 的执行上下文中。不需要模式检测、不需要涌现度量。 2. 活化有立即可测量的效果——加入法则后，Agent 的决策质量是否提升？ 3. 活化是凝结的前提——没有活化产生的经验，就没有凝结的素材。  先搭建的层：表征层（R-Layer）。 理由：表征层是整个系统的"地基"——Law 数据结构、LawStore、法则检索。没有它，其他三层都无从谈起。 端到端最小闭环描述：   输入：一个招聘任务（"为高级后端工程师岗位评估候选人 A"）
    │
    │ Step 1: 冷启动法则库（5 条从 configs/ 迁移的法则）
    ▼
表征层：LawStore.retrieve(context="高级后端工程师 + 候选人 A")
    → 返回 3 条相关法则
    │
    │ Step 2: 活化——法则注入 Agent prompt
    ▼
反表征层：CouplingLoop.run(task, env_state, active_laws)
    → Agent 执行评估，产生 experience
    │
    │ Step 3: 经验积累（重复 10 次）
    ▼
元认知层：PatternDetector.detect(experience_buffer)
    → 发现候选法则（或未发现）
    │
    │ Step 4: 如果发现 → 验证 → 凝结入库
    ▼
输出：LawStore 可能新增 0~N 条法则 + 评估结果

涉及变更的文件：
    新增 4 个文件（law.py, law_store.py, pattern_detector.py, janus.py）
    修改 1 个文件（runtime_manager.py 的集成点）
    新增 1 个测试文件（test_mvp_loop.py）    Q13. 如何度量进展 Phase 1 完成标志（凝结-活化双向通道）： 指标 目标 度量方法   冷启动法则数 ≥ 10 条 LawStore.count(origin="injected")  活化命中率 ≥ 60% 在 10 个测试案例中，检索到的法则确实与场景相关  凝结产出率 ≥ 1 条 / 20 次实践 每 20 次实践至少凝结出 1 条通过验证的新法则  凝结法则验证通过率 ≥ 60% 凝结的候选法则在历史数据回放中的准确率  活化效果增益 > 0 有法则引导的决策质量 vs 无法则引导的决策质量（通过与历史实际结果对比）   评估基准（Benchmark）：   class JanusBenchmark:
    """Janus World Model 的评估基准"""
    
    scenarios: List[Scenario]       # 20 个招聘场景（来自历史数据）
    expected_laws: List[Law]        # 5 条领域专家预设的"应该能发现的法则"
    noise_patterns: List[Pattern]   # 10 个"看起来像法则但不是"的噪声模式
    
    def evaluate(self, janus: JanusWorldModel) -> BenchmarkResult:
        # 1. 活化测试：法则检索的相关性
        activation_score = self._test_activation(janus)
        
        # 2. 凝结测试：从场景中能否发现 expected_laws
        crystallization_score = self._test_crystallization(janus)
        
        # 3. 抗噪测试：是否错误地将 noise_patterns 凝结为法则
        noise_rejection_score = self._test_noise_rejection(janus)
        
        return BenchmarkResult(activation_score, crystallization_score, noise_rejection_score)  避免"demo 驱动开发"的关键措施： 1. 法则验证必须用确定性方法（历史数据回放 + 统计检验），不能用 LLM 判断"这个法则看起来对不对"。 2. 凝结出的法则必须能被反例推翻——在 benchmark 中专门包含应该使法则失效的边界案例。 3. 活化效果必须有 baseline 对比——同一任务，有法则引导 vs 无法则引导，定量对比结果差异。 4. 每条法则的 usage_count 和 success_rate 是硬指标——如果一条法则被活化 10 次但成功率 < 50%，它应该被自动降级或淘汰，无论它"看起来"多合理。    核心路线总结   Sprint 0（地基）
├── 定义 Law 数据结构（law.py）
├── 实现 LawStore（CRUD + 向量检索 + 版本控制）
├── 将 configs/ 中的规则迁移为初始法则
└── 测试：法则的创建、检索、序列化

Sprint 1（活化通道）
├── 实现法则检索（基于场景上下文的语义匹配）
├── 实现法则注入（三层活化机制的 Layer 1：Prompt 注入）
├── 集成到 RuntimeManager（替换硬编码的 AgentOrchestrator）
└── 测试：活化命中率 benchmark

Sprint 2（凝结通道）
├── 实现 Experience 记录与缓冲区
├── 实现 PatternDetector（Level 1 统计频率 + Level 2 LLM 归纳）
├── 实现法则验证（历史数据回放）
└── 测试：MVE 闭环——从 20 次实践中凝结出 ≥1 条法则

Sprint 3（闭环验证）
├── 在 ai-recruitment-os 上运行完整的活化→实践→凝结闭环
├── 构建 JanusBenchmark，量化评估
├── 对比实验：有 Janus vs 无 Janus 的决策质量
└── 产出：Benchmark 报告 + 法则库快照

Sprint 4+（涌现通道，待 Sprint 3 验证通过后）
├── 蜂群涌现检测
├── 凝华机制
├── PhaseManager
└── ...  一句话总结：先让法则能存储和检索（Sprint 0），再让法则能引导行动（Sprint 1），再让行动能产出新法则（Sprint 2），最后验证这个闭环确实产生了价值（Sprint 3）。涌现和超智能是后面的事——先把"冰"和"水"的相变做通，再考虑"蒸汽"。