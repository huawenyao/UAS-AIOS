# AI 全自动招聘系统 (ASUI 验证项目)

## 系统概述

基于 ASUI 架构的 AI 招聘系统验证项目。岗位画像 + 简历匹配 + 面试评估，全流程知识驱动，初筛效率提升 5 倍。

## 核心命令

- `/start` - 启动招聘流程
- `/addJob [岗位描述]` - 添加岗位并解析 JD
- `/match [岗位ID] [简历]` - 简历匹配打分
- `/evaluate [候选人ID]` - 面试评估（多维度判定）

## 工作流

1. **岗位解析** - 从 JD 提取结构化要求（学历、经验、技能、薪资）
2. **简历匹配** - 多维度匹配打分（学历/经验/技能）
3. **初筛报告** - 生成可审计的推荐报告
4. **面试评估** - 能力维度判定（专业/沟通/逻辑/文化契合）

## 知识层

| 文件 | 用途 |
|------|------|
| configs/workflow_config.json | 招聘工作流定义 |
| .claude/skills/jd_parser.md | 岗位解析规则 |
| .claude/skills/evaluation_criteria.md | 评估标准 |

## 验证标准

- [x] 知识驱动：修改 evaluation_criteria.md 即改变打分逻辑
- [x] 构建即运行：新增评估维度无需改代码
- [x] 结构化输出：匹配结果写入 database/candidates.json
- [x] 可审计：生成 HTML 报告含证据链

## 数据流

```
岗位JD → 解析(LLM) → 结构化要求
                        ↓
简历 → 匹配(LLM) → 多维度打分 → 报告生成(script)
                        ↓
              database/candidates.json
              reports/candidate_xxx.html
```
