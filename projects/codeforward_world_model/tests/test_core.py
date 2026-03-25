"""
UAS World Model - 测试套件
"""

import unittest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from intent_understanding import IntentUnderstanding, Intent, OpenAILLM
from knowledge_base import Entity, Relation, Rule, HybridKnowledgeBase, KnowledgeItem
from planning_engine import WorldState, Action, PlanningDrivenReasoning, LLMWorldModel
from world_model_builder import WorldModelProgram, Experience, WorldModelBuilder
from latent_planning import LatentSpacePlanner, LatentState
from knowledge_evolution import KnowledgeGraphEvolver, DriftDetection
from uas_world_model import UASWorldModelService, WMCapability


class TestIntentUnderstanding(unittest.TestCase):
    """测试意图理解模块"""

    def setUp(self):
        self.engine = IntentUnderstanding()

    def test_basic_understanding(self):
        """测试基本意图理解"""
        result = self.engine.understand("优化系统性能，确保响应时间<100ms")

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.intent)
        self.assertIsNotNone(result.intent.normalized)
        self.assertGreater(result.confidence, 0)

    def test_constraint_extraction(self):
        """测试约束提取"""
        result = self.engine.understand("必须完成重要任务，不能失败")

        constraints = result.intent.constraints
        self.assertTrue(len(constraints) > 0)

    def test_priority_calculation(self):
        """测试优先级计算"""
        high_priority = self.engine.understand("紧急任务，必须立即处理")
        normal_priority = self.engine.understand("普通任务")

        self.assertGreater(
            high_priority.intent.priority, normal_priority.intent.priority
        )


class TestKnowledgeBase(unittest.TestCase):
    """测试知识库模块"""

    def setUp(self):
        self.kb = HybridKnowledgeBase()

    def test_add_entity(self):
        """测试添加实体"""
        entity = Entity(name="用户", type="person")
        item = KnowledgeItem(content="用户实体", entity=entity)

        self.kb.add_knowledge(item)
        self.assertEqual(len(self.kb.kg.entities), 1)

    def test_add_relation(self):
        """测试添加关系"""
        e1 = Entity(id="e1", name="用户", type="person")
        e2 = Entity(id="e2", name="订单", type="object")
        r = Relation(source_id="e1", target_id="e2", type="creates")

        item1 = KnowledgeItem(content="用户", entity=e1)
        item2 = KnowledgeItem(content="订单", entity=e2)

        self.kb.add_knowledge(item1)
        self.kb.add_knowledge(item2)

        self.kb.kg.add_relation(r)

        self.assertEqual(len(self.kb.kg.relations), 1)

    def test_retrieve(self):
        """测试检索"""
        entity = Entity(name="测试", type="concept")
        item = KnowledgeItem(
            content="这是一个测试实体", entity=entity, vector_embedding=[0.1] * 16
        )

        self.kb.add_knowledge(item)

        results = self.kb.retrieve("测试", [0.1] * 16)

        self.assertIsNotNone(results)


class TestPlanningEngine(unittest.TestCase):
    """测试规划引擎"""

    def setUp(self):
        self.planner = PlanningDrivenReasoning()

    def test_basic_plan(self):
        """测试基本规划"""
        current = WorldState(description="初始状态", attributes={"progress": 0})

        goal = WorldState(description="完成状态", attributes={"progress": 100})

        actions = [
            Action(name="执行步骤1", cost=1.0),
            Action(name="执行步骤2", cost=1.5),
        ]

        plan = self.planner.plan(current, goal, actions)

        self.assertIsNotNone(plan)


class TestLatentPlanning(unittest.TestCase):
    """测试隐空间规划"""

    def setUp(self):
        self.planner = LatentSpacePlanner(
            {"latent_dim": 16, "action_dim": 4, "imagination_horizon": 5}
        )

    def test_encode(self):
        """测试编码"""
        latent = self.planner.encode_observation("test observation")

        self.assertIsNotNone(latent)
        self.assertEqual(len(latent.vector), 16)

    def test_imagine(self):
        """测试想象力"""
        initial = LatentState(vector=[0.1] * 16)

        trajectory = self.planner.imagine(initial, horizon=3)

        self.assertIsNotNone(trajectory)
        self.assertEqual(len(trajectory.latent_states), 3)


class TestKnowledgeEvolution(unittest.TestCase):
    """测试知识演化"""

    def setUp(self):
        self.evolver = KnowledgeGraphEvolver()

    def test_drift_detection(self):
        """测试漂移检测"""
        feedback = {"expected": "success", "actual": "failed"}

        event = self.evolver.evolve(feedback)

        self.assertIsNotNone(event)


class TestUASWorldModelService(unittest.TestCase):
    """测试UAS统一接口"""

    def setUp(self):
        self.service = UASWorldModelService()

    def test_process_intent(self):
        """测试意图处理"""
        result = self.service.process_intent("优化招聘流程", {"domain": "hr"})

        self.assertIsNotNone(result)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_create_plan(self):
        """测试创建规划"""
        result = self.service.create_plan(
            goal="完成目标",
            context={
                "current_state": "初始状态",
                "state_attributes": {"progress": 0},
                "goal_attributes": {"progress": 100},
            },
            actions=[{"name": "步骤1", "cost": 1.0}, {"name": "步骤2", "cost": 2.0}],
        )

        self.assertIsNotNone(result)

    def test_check_drift(self):
        """测试漂移检测"""
        result = self.service.check_drift(
            expected=100, actual=80, context={"entities": ["progress"]}
        )

        self.assertIsNotNone(result)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流"""
        # 1. 意图理解
        service = UASWorldModelService()
        intent_result = service.process_intent("构建自动化招聘系统")

        self.assertTrue(intent_result["success"])

        # 2. 规划
        plan_result = service.create_plan(
            goal="构建自动化招聘系统",
            context={
                "current_state": "手动招聘",
                "state_attributes": {"自动化程度": 0},
                "goal_attributes": {"自动化程度": 100},
            },
            actions=[
                {"name": "简历筛选", "cost": 1.0},
                {"name": "面试安排", "cost": 1.5},
                {"name": "offer发放", "cost": 1.0},
            ],
        )

        self.assertTrue(plan_result["success"])

        # 3. 漂移检测
        drift_result = service.check_drift(
            expected={"自动化程度": 100}, actual={"自动化程度": 80}
        )

        self.assertIsNotNone(drift_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
