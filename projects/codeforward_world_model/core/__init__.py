"""
UAS World Model - Core Package

定位：UAS 元Agent 的认知引擎组件
- 不独立运行
- 被 UAS Intent/Planning/AgentFabric 调用
- 提供目标理解、动态规划、系统建模能力
"""

from .intent_understanding import (
    Intent,
    IntentAnalysis,
    IntentUnderstanding,
    IntentUnderstandingWithRAG,
    LLMInterface,
    OpenAILLM,
)

from .knowledge_base import (
    Entity,
    Relation,
    Rule,
    KnowledgeItem,
    KnowledgeType,
    KnowledgeGraph,
    VectorStore,
    RuleEngine,
    HybridKnowledgeBase,
)

from .planning_engine import (
    WorldState,
    Action,
    Trajectory,
    Plan,
    PlanningState,
    WorldModelInterface,
    LLMWorldModel,
    PlanningDrivenReasoning,
    ReactiveReasoning,
)

from .world_model_builder import (
    WorldModelProgram,
    Experience,
    SynthesisResult,
    ProgramState,
    WorldModelBuilder,
    SymbolicWorldModel,
    WorldModelLibrary,
)

from .latent_planning import (
    LatentState,
    ImaginedTrajectory,
    Encoder,
    Decoder,
    DynamicsModel,
    SimpleEncoder,
    SimpleDecoder,
    SimpleDynamics,
    RewardPredictor,
    Critic,
    Actor,
    LatentSpacePlanner,
    HybridPlanner,
)

from .knowledge_evolution import (
    EvolutionState,
    EvolutionEvent,
    DriftDetection,
    EntityType,
    KnowledgeGraphEvolver,
    MultiAgentKGBuilder,
)

from .uas_world_model import (
    WMCapability,
    WMInput,
    WMOutput,
    WorldModelInterface,
    UASWorldModel,
    UASWorldModelService,
)

__all__ = [
    # Intent Understanding
    "Intent",
    "IntentAnalysis",
    "IntentUnderstanding",
    "IntentUnderstandingWithRAG",
    "LLMInterface",
    "OpenAILLM",
    # Knowledge Base
    "Entity",
    "Relation",
    "Rule",
    "KnowledgeItem",
    "KnowledgeType",
    "KnowledgeGraph",
    "VectorStore",
    "RuleEngine",
    "HybridKnowledgeBase",
    # Planning Engine
    "WorldState",
    "Action",
    "Trajectory",
    "Plan",
    "PlanningState",
    "WorldModelInterface",
    "LLMWorldModel",
    "PlanningDrivenReasoning",
    "ReactiveReasoning",
    # World Model Builder
    "WorldModelProgram",
    "Experience",
    "SynthesisResult",
    "ProgramState",
    "WorldModelBuilder",
    "SymbolicWorldModel",
    "WorldModelLibrary",
    # Latent Planning
    "LatentState",
    "ImaginedTrajectory",
    "Encoder",
    "Decoder",
    "DynamicsModel",
    "SimpleEncoder",
    "SimpleDecoder",
    "SimpleDynamics",
    "RewardPredictor",
    "Critic",
    "Actor",
    "LatentSpacePlanner",
    "HybridPlanner",
    # Knowledge Evolution
    "EvolutionState",
    "EvolutionEvent",
    "DriftDetection",
    "EntityType",
    "KnowledgeGraphEvolver",
    "MultiAgentKGBuilder",
    # UAS World Model Interface
    "WMCapability",
    "WMInput",
    "WMOutput",
    "WorldModelInterface",
    "UASWorldModel",
    "UASWorldModelService",
]
