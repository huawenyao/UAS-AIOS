"""ASUI 项目模板"""

from .selfpaw_template import SELFPAW_SWARM_TEMPLATE
from .triadic_template import TRIADIC_IDEAL_REALITY_SWARM_TEMPLATE

# 默认模板
DEFAULT_TEMPLATE = {
    "CLAUDE.md": """# ASUI 项目

## 系统概述

本项目采用 ASUI（AI-System-UI Integration）架构，以显式知识驱动 AI 与系统执行深度融合。

## 核心命令

- `/start` - 启动主工作流
- `/status` - 查看系统状态

## 知识层

- `configs/workflow_config.json` - 工作流配置
- `.claude/skills/` - 功能模块知识
- `.claude/agents/` - 领域 Agent

## 数据流

1. 用户输入 → AI 解析意图
2. 加载 workflow_config → 生成执行计划
3. 按步骤执行 → 调用脚本/LLM
4. 结构化输出 → 数据库/报告
""",
    ".claude/skills/README.md": "# 功能模块知识\n\n在此目录放置各功能模块的说明文档，供 AI 加载使用。\n",
    ".claude/agents/README.md": "# 领域 Agent\n\n在此目录放置领域特定的 Agent 配置。\n",
    ".claude/commands/README.md": "# 交互命令\n\n定义 /start、/status 等命令的触发逻辑。\n",
    "configs/workflow_config.json": """{
  "version": "v1.0",
  "name": "主工作流",
  "description": "ASUI 默认工作流",
  "steps": [
    {
      "id": "step_1",
      "name": "数据加载",
      "type": "script",
      "description": "加载输入数据"
    },
    {
      "id": "step_2",
      "name": "AI 处理",
      "type": "llm",
      "dependencies": ["step_1"],
      "prompt_template": "根据以下数据进行分析：\\n{{context}}"
    }
  ]
}
""",
    "scripts/README.md": "# 执行脚本\n\n放置 Python/Bash 等执行脚本。\n",
    "database/README.md": "# 数据持久化\n\nSQLite 数据库或数据文件存放目录。\n",
}

# 智能客服模板
CUSTOMER_SERVICE_TEMPLATE = {
    "CLAUDE.md": """# 智能客服系统 (ASUI)

## 系统概述

基于 ASUI 架构的智能客服系统，知识库驱动对话 + 工单系统集成。

## 核心命令

- `/start` - 启动客服会话
- `/ticket [工单ID]` - 查询/创建工单
- `/knowledge` - 更新知识库

## 工作流

1. 用户咨询 → 意图识别
2. 知识库检索 → 生成回复
3. 无法解决 → 创建工单
4. 工单状态同步 → 飞书/钉钉通知

## 知识层

- `configs/workflow_config.json` - 客服工作流
- `.claude/skills/knowledge_base.md` - 产品/FAQ 知识
- `.claude/skills/ticket_rules.md` - 工单分类与升级规则
""",
    ".claude/skills/knowledge_base.md": """# 知识库

## 产品知识

（在此添加产品说明、常见问题等）

## FAQ 模板

- Q: xxx
  A: xxx
""",
    ".claude/skills/ticket_rules.md": """# 工单规则

## 分类标准

- 技术问题 → 技术组
- 退款申请 → 客服主管
- 投诉 → 升级处理

## 响应时效

- P0: 15 分钟
- P1: 1 小时
- P2: 4 小时
""",
    "configs/workflow_config.json": """{
  "version": "v1.0",
  "name": "智能客服工作流",
  "steps": [
    {
      "id": "intent",
      "name": "意图识别",
      "type": "llm",
      "prompt_template": "分析用户意图：{{user_input}}"
    },
    {
      "id": "retrieve",
      "name": "知识检索",
      "type": "llm",
      "dependencies": ["intent"],
      "prompt_template": "根据意图从知识库检索：{{intent}}"
    },
    {
      "id": "reply",
      "name": "生成回复",
      "type": "llm",
      "dependencies": ["retrieve"],
      "prompt_template": "生成客服回复：{{context}}"
    },
    {
      "id": "ticket",
      "name": "工单创建",
      "type": "script",
      "dependencies": ["reply"],
      "description": "无法解决时创建工单"
    }
  ]
}
""",
    "scripts/README.md": "# 执行脚本\n\n- create_ticket.py: 工单创建\n",
    "scripts/create_ticket.py": """#!/usr/bin/env python3
\"\"\"工单创建脚本\"\"\"
import json
import sys

def main():
    data = json.load(sys.stdin)
    # TODO: 对接工单系统 API
    print(json.dumps({"ticket_id": "T001", "status": "created"}))

if __name__ == "__main__":
    main()
""",
}

# AI 全自动招聘模板
RECRUITMENT_TEMPLATE = {
    "CLAUDE.md": """# AI 全自动招聘系统 (ASUI)

## 系统概述

基于 ASUI 架构的 AI 招聘系统：岗位画像 + 简历匹配 + 面试评估，全流程知识驱动。

## 核心命令

- `/start` - 启动招聘流程
- `/addJob [岗位描述]` - 添加岗位
- `/match [岗位ID]` - 简历匹配
- `/evaluate [候选人ID]` - 面试评估

## 工作流

1. 岗位解析 → 提取 JD 关键要求
2. 简历筛选 → 多维度匹配打分
3. 初筛报告 → 结构化输出
4. 面试评估 → 能力维度判定
5. 推荐决策 → 可审计报告

## 知识层

- `configs/workflow_config.json` - 招聘工作流
- `.claude/skills/jd_parser.md` - 岗位解析规则
- `.claude/skills/evaluation_criteria.md` - 评估标准
""",
    ".claude/skills/jd_parser.md": """# 岗位解析规则

## 提取维度

- 学历要求
- 工作经验
- 技能关键词
- 薪资范围
- 工作地点

## 标准化映射

将非结构化 JD 转为结构化 schema。
""",
    ".claude/skills/evaluation_criteria.md": """# 评估标准

## 简历匹配维度

- 学历匹配度 (0-10)
- 经验匹配度 (0-10)
- 技能匹配度 (0-10)
- 综合推荐分数

## 面试评估维度

- 专业能力
- 沟通表达
- 逻辑思维
- 文化契合
""",
    "configs/workflow_config.json": """{
  "version": "v1.0",
  "name": "AI 招聘工作流",
  "steps": [
    {
      "id": "parse_jd",
      "name": "岗位解析",
      "type": "llm",
      "prompt_template": "解析岗位描述，提取结构化要求：{{job_description}}"
    },
    {
      "id": "match_resume",
      "name": "简历匹配",
      "type": "llm",
      "dependencies": ["parse_jd"],
      "prompt_template": "根据岗位要求匹配简历：{{jd}} {{resume}}"
    },
    {
      "id": "score",
      "name": "匹配打分",
      "type": "llm",
      "dependencies": ["match_resume"],
      "output_schema": {
        "type": "object",
        "properties": {
          "education_score": {"type": "number"},
          "experience_score": {"type": "number"},
          "skill_score": {"type": "number"},
          "total_score": {"type": "number"}
        }
      }
    },
    {
      "id": "report",
      "name": "生成报告",
      "type": "script",
      "dependencies": ["score"],
      "description": "生成可审计的推荐报告"
    }
  ]
}
""",
    "scripts/README.md": "# 执行脚本\n\n- generate_report.py: 招聘报告生成\n",
    "scripts/generate_report.py": """#!/usr/bin/env python3
\"\"\"招聘推荐报告生成\"\"\"
import json
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)
    report_path = Path("reports") / f"candidate_{data.get('candidate_id', 'unknown')}.html"
    report_path.parent.mkdir(exist_ok=True)
    # TODO: 生成 HTML 报告
    report_path.write_text("<html><body>Report placeholder</body></html>", encoding="utf-8")
    print(json.dumps({"report_path": str(report_path)}))

if __name__ == "__main__":
    main()
""",
}


def get_template(name: str) -> dict:
    """获取指定模板"""
    templates = {
        "default": DEFAULT_TEMPLATE,
        "customer-service": CUSTOMER_SERVICE_TEMPLATE,
        "recruitment": RECRUITMENT_TEMPLATE,
        "selfpaw-swarm": SELFPAW_SWARM_TEMPLATE,
        "triadic-ideal-reality-swarm": TRIADIC_IDEAL_REALITY_SWARM_TEMPLATE,
    }
    return templates.get(name, DEFAULT_TEMPLATE)
