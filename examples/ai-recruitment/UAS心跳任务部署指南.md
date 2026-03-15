# UAS-AIOS Subapp 循环进化心跳任务部署指南

## 🚀 任务概述
心跳任务会定期扫描example下所有subapp，调用蜂群智能体和价值评估智能体进行多维度评估和自动优化，确保所有subapp的产品体验和业务价值评分达到95分以上。

## 📋 核心功能
- ✅ 自动扫描所有example下的subapp
- ✅ 蜂群智能体产品体验评估（功能完整性、用户体验、技术架构等）
- ✅ 价值评估智能体业务价值评估（商业价值、市场需求、ROI等）
- ✅ 综合得分计算（产品体验60% + 业务价值40%）
- ✅ 自动生成优化建议
- ✅ 自动执行优化操作
- ✅ 评估状态持久化存储
- ✅ 详细的执行报告生成

## 🔧 部署方式

### 方式1：单次执行（立即评估）
```bash
python uas_subapp_evolution_heartbeat.py --mode once
```

### 方式2：循环执行（后台守护）
```bash
# 每小时执行一次
python uas_subapp_evolution_heartbeat.py --mode loop --interval 3600

# 每30分钟执行一次
python uas_subapp_evolution_heartbeat.py --mode loop --interval 1800
```

### 方式3：Windows定时任务（推荐）
1. 打开"任务计划程序"
2. 创建新任务，设置触发器为"每天"，重复任务间隔为1小时
3. 操作设置为"启动程序"，程序路径选择python.exe，参数为:
   ```
   C:\Users\ranwu\Xiaomi Cloud\UAS-AIOS\examples\ai-recruitment\uas_subapp_evolution_heartbeat.py --mode once
   ```
4. 保存任务即可自动定期执行

## 📊 评估指标

### 产品体验评估维度（60%权重）
- 功能完整性
- 用户体验流畅度
- 技术架构合理性
- 代码质量与可维护性
- 文档完整性
- 错误处理机制

### 业务价值评估维度（40%权重）
- 商业模式清晰度
- 市场需求匹配度
- 技术壁垒与竞争力
- ROI投资回报率
- 可扩展性
- 差异化优势

## 📈 输出说明

### 评估结果存储
- 每个subapp目录下生成 `.evaluation_state.json` 存储历史评估状态
- 每次执行生成报告到 `C:\Users\ranwu\Xiaomi Cloud\UAS-AIOS\heartbeat_logs\`
- 优化记录写入每个subapp目录下的 `optimization_log.md`

### 评分标准
- 95分以上：✅ 优秀，无需优化
- 80-94分：⚠️ 良好，需要针对性优化
- 60-79分：🔴 及格，需要重点优化
- 60分以下：❌ 不合格，需要全面重构

## 🎯 进化目标
通过持续的心跳循环评估和优化，最终实现：
1. 所有subapp综合评分达到95分以上
2. 产品体验零差评
3. 业务价值最大化
4. 技术架构持续迭代进化

## 🔄 工作流程
```
扫描subapp → 蜂群智能体体验评估 → 价值智能体价值评估 → 综合得分计算 → 
生成优化建议 → 自动执行优化 → 保存评估状态 → 生成执行报告 → 下次循环
```

## 📝 首次执行结果
2026-03-15 首次执行完成：
- 发现subapp总数：15个
- 达到95分目标：0个
- 待优化数量：15个
- 平均得分：89.2分
- 本次报告：`C:\Users\ranwu\Xiaomi Cloud\UAS-AIOS\heartbeat_logs\heartbeat_report_20260315_162624.json`

接下来的心跳任务会持续优化所有subapp，直到全部达到95分以上目标。
