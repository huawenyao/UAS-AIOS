#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持续学习与演化架构

实现目标：
1. 经验积累 - 从执行结果中学习
2. 知识更新 - 动态更新知识库
3. 策略优化 - 基于反馈调整策略
4. 自我进化 - 自动发现和修复问题
5. 知识图谱更新 - 维护动态实体关系
"""

from __future__ import print_function
import json
import time
from datetime import datetime
from collections import defaultdict
import random


# ============================================================
# 第一部分：经验积累系统
# ============================================================

class ExperienceAccumulator:
    """经验积累器 - 从执行结果中提取学习"""

    def __init__(self):
        self.experiences = []
        self.episode_count = 0

    def record(self, state, action, result, reward):
        """记录一次经验"""
        episode = {
            "id": self.episode_count,
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "action": action,
            "result": result,
            "reward": reward,
            "learned": False
        }
        self.experiences.append(episode)
        self.episode_count += 1
        return episode

    def get_unlearned(self):
        """获取未学习的经验"""
        return [e for e in self.experiences if not e["learned"]]

    def mark_learned(self, episode_id):
        """标记为已学习"""
        for e in self.experiences:
            if e["id"] == episode_id:
                e["learned"] = True
                break

    def get_recent(self, n=10):
        """获取最近n条经验"""
        return self.experiences[-n:] if len(self.experiences) >= n else self.experiences

    def extract_patterns(self):
        """从经验中提取模式"""
        patterns = {
            "success_patterns": [],
            "failure_patterns": [],
            "reward_distribution": defaultdict(int)
        }

        for exp in self.experiences:
            reward = exp.get("reward", 0)
            if reward > 0.8:
                patterns["success_patterns"].append({
                    "state": exp["state"],
                    "action": exp["action"]
                })
            elif reward < 0.3:
                patterns["failure_patterns"].append({
                    "state": exp["state"],
                    "action": exp["action"]
                })

            # 奖励分布
            bucket = int(reward * 10) / 10
            patterns["reward_distribution"][bucket] += 1

        return patterns


# ============================================================
# 第二部分：知识更新系统
# ============================================================

class KnowledgeUpdater:
    """知识更新器 - 动态更新知识库"""

    def __init__(self):
        self.knowledge_graph = {
            "entities": {},
            "relations": [],
            "rules": [],
            "confidence": {}
        }
        self.update_history = []

    def add_entity(self, entity_id, entity_type, attributes, confidence=0.5):
        """添加实体"""
        if entity_id not in self.knowledge_graph["entities"]:
            self.knowledge_graph["entities"][entity_id] = {
                "type": entity_type,
                "attributes": attributes,
                "created_at": datetime.now().isoformat()
            }
            self.knowledge_graph["confidence"][entity_id] = confidence
            return True
        else:
            # 更新已存在实体
            return self.update_entity(entity_id, attributes)

    def update_entity(self, entity_id, attributes):
        """更新实体属性"""
        if entity_id in self.knowledge_graph["entities"]:
            self.knowledge_graph["entities"][entity_id]["attributes"].update(attributes)
            self.knowledge_graph["entities"][entity_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False

    def add_relation(self, source, target, relation_type, confidence=0.5):
        """添加关系"""
        relation = {
            "source": source,
            "target": target,
            "type": relation_type,
            "confidence": confidence,
            "created_at": datetime.now().isoformat()
        }
        self.knowledge_graph["relations"].append(relation)
        return relation

    def add_rule(self, rule_id, condition, action, confidence=0.5):
        """添加规则"""
        rule = {
            "id": rule_id,
            "condition": condition,
            "action": action,
            "confidence": confidence,
            "usage_count": 0,
            "success_rate": 0.5
        }
        self.knowledge_graph["rules"].append(rule)
        return rule

    def update_rule_performance(self, rule_id, success):
        """更新规则性能"""
        for rule in self.knowledge_graph["rules"]:
            if rule["id"] == rule_id:
                rule["usage_count"] += 1
                # 滑动平均更新成功率
                old_rate = rule["success_rate"]
                rule["success_rate"] = old_rate * 0.9 + (1.0 if success else 0.0) * 0.1
                break

    def merge_experience(self, experience):
        """将经验合并到知识库"""
        state = experience.get("state", {})
        action = experience.get("action", {})
        result = experience.get("result", {})
        reward = experience.get("reward", 0)

        # 从成功经验中学习
        if reward > 0.7:
            # 添加成功模式为规则
            rule_id = "rule_{}_{}".format(
                state.get("layer", "unknown"),
                action.get("type", "unknown")
            )
            self.add_rule(
                rule_id,
                condition=state,
                action=action,
                confidence=reward
            )

        # 更新实体置信度
        for key, value in state.items():
            entity_id = "state_{}".format(key)
            self.add_entity(entity_id, "state_feature", {key: value}, confidence=reward)

        self.update_history.append({
            "timestamp": datetime.now().isoformat(),
            "experience_id": experience.get("id"),
            "reward": reward
        })

    def get_knowledge_summary(self):
        """获取知识摘要"""
        return {
            "entity_count": len(self.knowledge_graph["entities"]),
            "relation_count": len(self.knowledge_graph["relations"]),
            "rule_count": len(self.knowledge_graph["rules"]),
            "avg_confidence": sum(self.knowledge_graph["confidence"].values()) /
                             max(len(self.knowledge_graph["confidence"]), 1),
            "successful_rules": len([r for r in self.knowledge_graph["rules"] if r["success_rate"] > 0.7])
        }


# ============================================================
# 第三部分：策略优化系统
# ============================================================

class StrategyOptimizer:
    """策略优化器 - 基于反馈调整策略"""

    def __init__(self):
        self.strategies = {}
        self.active_strategy = "default"
        self.performance_history = []

    def register_strategy(self, strategy_id, strategy_func, description=""):
        """注册策略"""
        self.strategies[strategy_id] = {
            "func": strategy_func,
            "description": description,
            "performance": [],
            "usage_count": 0
        }

    def select_strategy(self, context):
        """选择最佳策略"""
        if not self.strategies:
            return "default"

        # 基于上下文的策略选择
        layer = context.get("current_layer", "data")
        iteration = context.get("iteration", 0)

        # 简单策略选择规则
        if layer == "data":
            return "perception_focused"
        elif layer == "information":
            return "structure_focused"
        elif layer == "knowledge":
            return "reasoning_focused"
        elif layer == "wisdom":
            return "decision_focused"

        # 计算各策略的历史表现
        best_strategy = self.active_strategy
        best_score = -1

        for sid, strat in self.strategies.items():
            if strat["performance"]:
                avg_perf = sum(strat["performance"]) / len(strat["performance"])
                if avg_perf > best_score:
                    best_score = avg_perf
                    best_strategy = sid

        return best_strategy

    def update_performance(self, strategy_id, reward):
        """更新策略性能"""
        if strategy_id in self.strategies:
            self.strategies[strategy_id]["performance"].append(reward)
            # 限制历史长度
            if len(self.strategies[strategy_id]["performance"]) > 100:
                self.strategies[strategy_id]["performance"] = \
                    self.strategies[strategy_id]["performance"][-100:]

            # 更新活跃策略
            avg_perf = sum(self.strategies[strategy_id]["performance"]) / \
                      len(self.strategies[strategy_id]["performance"])
            if avg_perf > 0.7:
                self.active_strategy = strategy_id


# ============================================================
# 第四部分：自我进化系统
# ============================================================

class SelfEvolutionarySystem:
    """自我进化系统 - 自动发现和修复问题"""

    def __init__(self):
        self.issues = []
        self.fixes = []
        self.evolution_triggers = {
            "performance_degradation": self._detect_performance_issue,
            "knowledge_gap": self._detect_knowledge_gap,
            "strategy_failure": self._detect_strategy_failure
        }

    def analyze(self, metrics):
        """分析系统状态，检测问题"""
        detected_issues = []

        # 检测性能下降
        if self._detect_performance_issue(metrics):
            detected_issues.append({
                "type": "performance_degradation",
                "severity": "high",
                "description": "检测到性能下降",
                "metrics": metrics
            })

        # 检测知识缺口
        if self._detect_knowledge_gap(metrics):
            detected_issues.append({
                "type": "knowledge_gap",
                "severity": "medium",
                "description": "检测到知识缺口",
                "metrics": metrics
            })

        # 检测策略失败
        if self._detect_strategy_failure(metrics):
            detected_issues.append({
                "type": "strategy_failure",
                "severity": "high",
                "description": "检测到策略失败",
                "metrics": metrics
            })

        self.issues.extend(detected_issues)
        return detected_issues

    def _detect_performance_issue(self, metrics):
        """检测性能问题"""
        if "success_rate" in metrics:
            return metrics["success_rate"] < 0.6
        return False

    def _detect_knowledge_gap(self, metrics):
        """检测知识缺口"""
        if "unknown_entities" in metrics:
            return metrics["unknown_entities"] > 5
        return False

    def _detect_strategy_failure(self, metrics):
        """检测策略失败"""
        if "consecutive_failures" in metrics:
            return metrics["consecutive_failures"] > 3
        return False

    def propose_fix(self, issue):
        """为问题提出修复方案"""
        fix = {
            "issue_type": issue["type"],
            "proposed_actions": [],
            "confidence": 0.5,
            "timestamp": datetime.now().isoformat()
        }

        if issue["type"] == "performance_degradation":
            fix["proposed_actions"] = [
                "降低学习率",
                "增加训练数据",
                "简化模型复杂度"
            ]
            fix["confidence"] = 0.8

        elif issue["type"] == "knowledge_gap":
            fix["proposed_actions"] = [
                "主动探索新实体",
                "增加数据源",
                "降低新知识置信度阈值"
            ]
            fix["confidence"] = 0.7

        elif issue["type"] == "strategy_failure":
            fix["proposed_actions"] = [
                "切换到备用策略",
                "重置策略参数",
                "增加策略多样性"
            ]
            fix["confidence"] = 0.9

        self.fixes.append(fix)
        return fix

    def apply_fix(self, fix, system_state):
        """应用修复"""
        # 模拟修复应用
        return {
            "fix_applied": True,
            "fix_id": len(self.fixes),
            "new_system_state": system_state,
            "expected_improvement": fix["confidence"]
        }

    def get_evolution_report(self):
        """获取进化报告"""
        return {
            "issues_detected": len(self.issues),
            "fixes_proposed": len(self.fixes),
            "issue_types": list(set([i["type"] for i in self.issues])),
            "avg_confidence": sum([f["confidence"] for f in self.fixes]) / max(len(self.fixes), 1)
        }


# ============================================================
# 第五部分：统一持续学习引擎
# ============================================================

class ContinuousLearningEngine:
    """
    统一持续学习引擎

    整合：
    1. 经验积累
    2. 知识更新
    3. 策略优化
    4. 自我进化
    """

    def __init__(self):
        self.experience_accumulator = ExperienceAccumulator()
        self.knowledge_updater = KnowledgeUpdater()
        self.strategy_optimizer = StrategyOptimizer()
        self.evolution_system = SelfEvolutionarySystem()

        self.iteration = 0
        self.learning_history = []

        # 注册默认策略
        self._register_default_strategies()

    def _register_default_strategies(self):
        """注册默认策略"""
        self.strategy_optimizer.register_strategy(
            "perception_focused",
            lambda ctx: "强化数据感知能力",
            "专注于数据层处理"
        )
        self.strategy_optimizer.register_strategy(
            "structure_focused",
            lambda ctx: "强化结构化能力",
            "专注于信息层处理"
        )
        self.strategy_optimizer.register_strategy(
            "reasoning_focused",
            lambda ctx: "强化推理能力",
            "专注于知识层处理"
        )
        self.strategy_optimizer.register_strategy(
            "decision_focused",
            lambda ctx: "强化决策能力",
            "专注于智慧层处理"
        )

    def learn(self, state, action, result, reward):
        """执行一次学习迭代"""
        self.iteration += 1

        # 1. 记录经验
        experience = self.experience_accumulator.record(state, action, result, reward)
        print("  [学习] 记录经验 #{} (reward={:.2f})".format(
            experience["id"], reward
        ))

        # 2. 更新知识库
        self.knowledge_updater.merge_experience(experience)
        print("  [学习] 更新知识库 (实体数: {})".format(
            len(self.knowledge_updater.knowledge_graph["entities"])
        ))

        # 3. 更新策略性能
        context = {
            "current_layer": state.get("layer", "unknown"),
            "iteration": self.iteration
        }
        selected = self.strategy_optimizer.select_strategy(context)
        self.strategy_optimizer.update_performance(selected, reward)
        print("  [学习] 策略 {} 性能更新 (当前活跃: {})".format(
            selected, self.strategy_optimizer.active_strategy
        ))

        # 4. 检测并修复问题
        metrics = {
            "success_rate": reward,
            "iteration": self.iteration
        }
        issues = self.evolution_system.analyze(metrics)
        if issues:
            print("  [学习] 检测到 {} 个问题".format(len(issues)))
            for issue in issues:
                fix = self.evolution_system.propose_fix(issue)
                print("    - {}: 置信度 {:.1%}".format(
                    issue["type"], fix["confidence"]
                ))

        # 5. 记录学习历史
        self.learning_history.append({
            "iteration": self.iteration,
            "reward": reward,
            "experience_id": experience["id"],
            "strategy": selected
        })

        return {
            "iteration": self.iteration,
            "reward": reward,
            "knowledge_summary": self.knowledge_updater.get_knowledge_summary(),
            "issues_found": len(issues)
        }

    def get_system_status(self):
        """获取系统状态"""
        return {
            "total_iterations": self.iteration,
            "total_experiences": len(self.experience_accumulator.experiences),
            "knowledge": self.knowledge_updater.get_knowledge_summary(),
            "active_strategy": self.strategy_optimizer.active_strategy,
            "evolution": self.evolution_system.get_evolution_report()
        }

    def auto_evolve(self):
        """自动进化"""
        print("\n" + "="*80)
        print("执行自动进化")
        print("="*80)

        # 基于当前状态生成进化建议
        knowledge = self.knowledge_updater.get_knowledge_summary()

        evolution_plan = {
            "timestamp": datetime.now().isoformat(),
            "knowledge_improvements": [],
            "strategy_improvements": [],
            "expected_benefits": []
        }

        # 知识改进
        if knowledge["entity_count"] < 10:
            evolution_plan["knowledge_improvements"].append(
                "增加实体覆盖率"
            )
            evolution_plan["expected_benefits"].append("+10% 知识完整性")

        if knowledge["successful_rules"] < 5:
            evolution_plan["knowledge_improvements"].append(
                "优化规则性能"
            )
            evolution_plan["expected_benefits"].append("+15% 规则成功率")

        # 策略改进
        evolution_plan["strategy_improvements"].append(
            "根据当前上下文调整策略参数"
        )
        evolution_plan["expected_benefits"].append("+5% 策略适应性")

        return evolution_plan


# ============================================================
# 第六部分：测试验证
# ============================================================

def test_continuous_learning():
    """测试持续学习系统"""

    print("="*80)
    print("持续学习与演化架构测试")
    print("="*80)

    # 初始化引擎
    engine = ContinuousLearningEngine()

    # 模拟学习迭代
    print("\n[模拟学习迭代]")
    for i in range(20):
        # 模拟不同层级的状态
        layers = ["data", "information", "knowledge", "wisdom"]
        state = {
            "layer": layers[i % 4],
            "iteration": i + 1,
            "input_dim": random.randint(10, 100)
        }

        action = {
            "type": random.choice(["transform", "route", "execute", "evaluate"]),
            "target_layer": layers[(i % 4) + 1] if i % 4 < 3 else "action"
        }

        result = {"status": "success", "output_dim": random.randint(1, 10)}
        reward = random.uniform(0.5, 1.0)  # 模拟奖励

        # 执行学习
        learn_result = engine.learn(state, action, result, reward)

        # 每5次迭代输出状态
        if (i + 1) % 5 == 0:
            print("  --- 迭代 {} 状态 ---".format(i + 1))
            print("  知识摘要: 实体={}, 关系={}, 规则={}".format(
                learn_result["knowledge_summary"]["entity_count"],
                learn_result["knowledge_summary"]["relation_count"],
                learn_result["knowledge_summary"]["rule_count"]
            ))

    # 输出系统状态
    print("\n" + "="*80)
    print("系统状态")
    print("="*80)
    status = engine.get_system_status()

    print("总迭代次数: {}".format(status["total_iterations"]))
    print("总经验数: {}".format(status["total_experiences"]))
    print("知识库: {} 实体, {} 关系, {} 规则".format(
        status["knowledge"]["entity_count"],
        status["knowledge"]["relation_count"],
        status["knowledge"]["rule_count"]
    ))
    print("活跃策略: {}".format(status["active_strategy"]))
    print("演化报告: {} 个问题, {} 个修复".format(
        status["evolution"]["issues_detected"],
        status["evolution"]["fixes_proposed"]
    ))

    # 执行自动进化
    evolution_plan = engine.auto_evolve()
    print("\n进化计划:")
    for imp in evolution_plan["knowledge_improvements"]:
        print("  - {}".format(imp))
    for benefit in evolution_plan["expected_benefits"]:
        print("    预期收益: {}".format(benefit))

    return status


if __name__ == "__main__":
    test_continuous_learning()