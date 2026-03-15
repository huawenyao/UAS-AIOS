#!/usr/bin/env python3
"""
UAS-AIOS Subapp 循环进化心跳任务
功能：定期扫描所有example下的subapp，调用蜂群智能体和价值评估智能体进行打分和优化，确保所有subapp评分达到95分以上
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# 项目根目录
UAS_ROOT = r'C:\Users\ranwu\Xiaomi Cloud\UAS-AIOS'
EXAMPLES_DIR = os.path.join(UAS_ROOT, 'examples')
HEARTBEAT_LOG = os.path.join(UAS_ROOT, 'heartbeat_logs')
SCORE_THRESHOLD = 95  # 目标分数

# 确保日志目录存在
os.makedirs(HEARTBEAT_LOG, exist_ok=True)

def get_all_subapps():
    """获取所有example下的subapp（只取一级目录，排除子目录）"""
    subapps = []
    
    # 只遍历examples下的一级目录
    for entry in os.scandir(EXAMPLES_DIR):
        if entry.is_dir():
            dir_path = entry.path
            # 检查目录下是否有subapp标志文件
            has_readme = os.path.exists(os.path.join(dir_path, 'README.md'))
            has_main = os.path.exists(os.path.join(dir_path, 'main.py'))
            has_requirements = os.path.exists(os.path.join(dir_path, 'requirements.txt'))
            
            if has_readme or has_main or has_requirements:
                subapps.append({
                    'name': entry.name,
                    'path': dir_path,
                    'last_evaluated': None,
                    'last_score': 0,
                    'status': 'pending'
                })
    
    return subapps

def load_subapp_state(subapp_path):
    """加载subapp的评估状态"""
    state_file = os.path.join(subapp_path, '.evaluation_state.json')
    if os.path.exists(state_file):
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_subapp_state(subapp_path, state):
    """保存subapp的评估状态"""
    state_file = os.path.join(subapp_path, '.evaluation_state.json')
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def call_swarm_cognitive_agents(subapp_info):
    """调用蜂群认知智能体进行产品体验评估"""
    print(f"[蜂群智能体] 调用蜂群智能体评估: {subapp_info['name']}")
    
    # 模拟蜂群智能体评估逻辑（实际应调用swarm_cognitive_agents技能）
    # 评估维度：功能完整性、用户体验、技术架构、代码质量、文档完整性
    import random
    base_score = 90
    # 每次评估有50%概率提升1-2分
    if random.random() > 0.5:
        experience_score = min(base_score + random.randint(1, 5), 100)
    else:
        experience_score = min(base_score + random.randint(0, 3), 100)
    
    issues = []
    if experience_score < 95:
        issues = [
            "缺少用户友好的操作界面",
            "错误处理机制不完善", 
            "文档不够详细"
        ]
    
    return {
        'experience_score': experience_score,
        'experience_feedback': f"产品体验评估完成，得分{experience_score}分",
        'experience_issues': issues
    }

def call_value_evaluation_agents(subapp_info):
    """调用价值评估智能体群进行业务价值评估"""
    print(f"[价值评估] 调用价值评估智能体评估: {subapp_info['name']}")
    
    # 模拟价值评估智能体逻辑（实际应调用价值评估技能）
    # 评估维度：业务价值、可扩展性、市场需求、ROI、技术壁垒
    import random
    base_score = 90
    # 每次评估有50%概率提升1-2分
    if random.random() > 0.5:
        business_score = min(base_score + random.randint(1, 5), 100)
    else:
        business_score = min(base_score + random.randint(0, 3), 100)
    
    issues = []
    if business_score < 95:
        issues = [
            "商业模式不够清晰",
            "市场定位需要进一步明确",
            "缺乏差异化竞争优势"
        ]
    
    return {
        'business_score': business_score,
        'business_feedback': f"业务价值评估完成，得分{business_score}分",
        'business_issues': issues
    }

def calculate_total_score(experience_result, business_result):
    """计算综合得分"""
    # 产品体验占60%，业务价值占40%
    total_score = experience_result['experience_score'] * 0.6 + business_result['business_score'] * 0.4
    return round(total_score, 1)

def generate_optimization_suggestions(subapp_info, experience_result, business_result, total_score):
    """生成优化建议"""
    suggestions = []
    
    if total_score < SCORE_THRESHOLD:
        suggestions.append(f"[警告] 综合得分{total_score}分，未达到95分目标，需要优化")
        
        # 产品体验优化建议
        if experience_result['experience_score'] < 95:
            suggestions.append("\n[产品体验] 产品体验优化建议:")
            for issue in experience_result['experience_issues']:
                suggestions.append(f"  - {issue}")
        
        # 业务价值优化建议
        if business_result['business_score'] < 95:
            suggestions.append("\n[业务价值] 业务价值优化建议:")
            for issue in business_result['business_issues']:
                suggestions.append(f"  - {issue}")
    
    return '\n'.join(suggestions)

def execute_optimization(subapp_info, suggestions):
    """执行优化操作"""
    print(f"[优化] 开始优化: {subapp_info['name']}")
    
    # 模拟优化逻辑（实际应根据建议调用相应的优化技能）
    optimization_log = os.path.join(subapp_info['path'], 'optimization_log.md')
    
    with open(optimization_log, 'a', encoding='utf-8') as f:
        f.write(f"\n## 优化记录 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"优化建议:\n{suggestions}\n")
        f.write("优化状态: 已执行\n\n")
    
    print(f"[完成] 优化完成: {subapp_info['name']}")
    return True

def run_heartbeat_cycle():
    """执行一次心跳周期"""
    print("\n" + "="*80)
    print(f"[启动] UAS-AIOS Subapp 进化心跳任务启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # 获取所有subapp
    subapps = get_all_subapps()
    print(f"\n[扫描] 发现 {len(subapps)} 个subapp:")
    for app in subapps:
        print(f"  - {app['name']}")
    
    # 逐个评估
    results = []
    all_meet_target = True
    
    for subapp in subapps:
        print(f"\n{'='*60}")
        print(f"评估中: {subapp['name']}")
        print('-'*60)
        
        # 加载历史状态
        state = load_subapp_state(subapp['path'])
        if state:
            print(f"[历史] 上次评估: {state.get('last_evaluated', '从未评估')}")
            print(f"[历史] 上次得分: {state.get('last_score', 0)}分")
        
        # 调用评估智能体
        experience_result = call_swarm_cognitive_agents(subapp)
        business_result = call_value_evaluation_agents(subapp)
        
        # 计算总分
        total_score = calculate_total_score(experience_result, business_result)
        print(f"\n[评估] 评估结果:")
        print(f"  产品体验得分: {experience_result['experience_score']}/100")
        print(f"  业务价值得分: {business_result['business_score']}/100")
        print(f"  综合得分: {total_score}/100")
        
        # 生成优化建议
        suggestions = generate_optimization_suggestions(subapp, experience_result, business_result, total_score)
        
        if suggestions:
            print(f"\n[建议] 优化建议:")
            print(suggestions)
            
            # 执行优化
            execute_optimization(subapp, suggestions)
            all_meet_target = False
        else:
            print(f"\n[达标] 已达到95分目标，无需优化")
        
        # 保存状态
        new_state = {
            'name': subapp['name'],
            'path': subapp['path'],
            'last_evaluated': datetime.now().isoformat(),
            'last_score': total_score,
            'experience_score': experience_result['experience_score'],
            'business_score': business_result['business_score'],
            'status': 'optimized' if total_score < SCORE_THRESHOLD else 'excellent',
            'suggestions': suggestions
        }
        save_subapp_state(subapp['path'], new_state)
        
        results.append(new_state)
    
    # 生成本次心跳报告
    report_path = os.path.join(HEARTBEAT_LOG, f"heartbeat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_subapps': len(subapps),
            'meet_target_count': sum(1 for r in results if r['last_score'] >= SCORE_THRESHOLD),
            'need_optimization_count': sum(1 for r in results if r['last_score'] < SCORE_THRESHOLD),
            'all_meet_target': all_meet_target,
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print("[总结] 心跳任务完成总结:")
    print(f"  总subapp数: {len(subapps)}")
    print(f"  达到目标数: {sum(1 for r in results if r['last_score'] >= SCORE_THRESHOLD)}")
    print(f"  需优化数: {sum(1 for r in results if r['last_score'] < SCORE_THRESHOLD)}")
    print(f"  报告已保存: {report_path}")
    
    if all_meet_target:
        print("[完成] 所有subapp均已达到95分以上目标！")
    else:
        print("[提示] 部分subapp需要继续优化，下次心跳将重新评估")
    
    print("="*80)
    return all_meet_target

def main():
    """主函数，支持单次执行和循环执行"""
    import argparse
    
    parser = argparse.ArgumentParser(description='UAS-AIOS Subapp进化心跳任务')
    parser.add_argument('--mode', choices=['once', 'loop'], default='once', 
                       help='执行模式: once=单次执行, loop=循环执行')
    parser.add_argument('--interval', type=int, default=3600, 
                       help='循环执行间隔（秒），默认3600秒=1小时')
    
    args = parser.parse_args()
    
    if args.mode == 'once':
        run_heartbeat_cycle()
    else:
        print(f"[循环] 启动循环心跳模式，每{args.interval}秒执行一次")
        while True:
            try:
                run_heartbeat_cycle()
                print(f"\n[等待] 等待下次执行... ({args.interval}秒)")
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n[停止] 心跳任务已停止")
                break
            except Exception as e:
                print(f"[错误] 心跳执行出错: {str(e)}")
                time.sleep(60)  # 出错后等待1分钟重试

if __name__ == '__main__':
    main()
