import os
import re
import json
from datetime import datetime
import PyPDF2
import olefile
from docx import Document

# 配置
RESUME_DIR = r'C:\Users\ranwu\Documents'
OUTPUT_REPORT = r'reports/full_ai_director_matching_result.json'
OUTPUT_DB = r'database/candidates.json'

JOB_REQS = {
    'required_degree': '本科及以上',
    'min_experience_years': 8,
    'management_required': True,
    'min_team_size': 10,
    'required_skills': ['Python', 'Java', 'C++', 'TensorFlow', 'PyTorch', '深度学习', '机器学习', 'LLM', 'NLP', '算法'],
    'bonus_skills': ['团队管理', '项目管理', '技术架构', '产品落地'],
    'weights': {'education':0.1, 'experience':0.25, 'skill':0.35, 'engineering':0.1, 'domain':0.1, 'potential':0.1}
}

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        text = ''
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ''
        return text
    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
    elif ext == '.doc':
        if not olefile.isOleFile(file_path):
            return ''
        ole = olefile.OleFileIO(file_path)
        if ole.exists('WordDocument'):
            stream = ole.openstream('WordDocument')
            data = stream.read()
            text = []
            for b in data:
                if 32 <= b <= 126 or 0x4e00 <= b <= 0x9fff:
                    text.append(chr(b))
            return ''.join(text)
    return ''

def parse_experience_years(text):
    patterns = [
        r'工作年限\s*[：:]\s*(\d+)\s*年',
        r'(\d{4})\.(\d{1,2})\s*[-~至到—]\s*(\d{4})\.(\d{1,2})',
        r'(\d{4})\.(\d{1,2})\s*[-~至到—]\s*(至今|现在)',
        r'(\d{4})\s*[-~至到—]\s*(\d{4})',
        r'(\d{4})\s*[-~至到—]\s*(至今|现在)',
    ]
    current_year = 2026
    years = []
    direct_match = re.search(r'工作年限\s*[：:]\s*(\d+)\s*年', text)
    if direct_match:
        return int(direct_match.group(1))
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                if match[0].isdigit():
                    if len(match) == 4 and match[2].isdigit():
                        y = int(match[2]) - int(match[0])
                        if 0 < y < 60:
                            years.append(y)
                    elif len(match) >=3 and match[2] in ['至今', '现在']:
                        y = current_year - int(match[0])
                        if 0 < y < 60:
                            years.append(y)
                    elif len(match) == 2:
                        if match[1].isdigit():
                            y = int(match[1]) - int(match[0])
                            if 0 < y < 60:
                                years.append(y)
                        elif match[1] in ['至今', '现在']:
                            y = current_year - int(match[0])
                            if 0 < y < 60:
                                years.append(y)
    return max(years) if years else 0

def parse_team_size(text):
    patterns = [r'下属\s*(\d+)\s*人', r'带领\s*(\d+)\s*人', r'团队规模\s*[：:]\s*(\d+)']
    for p in patterns:
        m = re.search(p, text)
        if m:
            return int(m.group(1))
    return 0

def calculate_score(info, reqs):
    scores = {}
    # 学历
    edu_keywords = ['本科', '硕士', '博士']
    has_required_edu = any(kw in info['education'] for kw in edu_keywords)
    scores['education_score'] = 8.0 if has_required_edu else 3.0
    
    # 经验
    exp_years = info['experience_years']
    min_years = reqs['min_experience_years']
    if exp_years >= min_years * 1.5:
        scores['experience_score'] = 9.5
    elif exp_years >= min_years:
        scores['experience_score'] = 8.0
    elif exp_years >= min_years * 0.7:
        scores['experience_score'] = 5.0
    else:
        scores['experience_score'] = 2.0
    
    # 技能
    req_skills = set(reqs['required_skills'])
    bonus_skills = set(reqs['bonus_skills'])
    user_skills = set(info['skills'])
    req_match = len(req_skills & user_skills)
    bonus_match = len(bonus_skills & user_skills)
    req_ratio = req_match / len(req_skills) if req_skills else 0
    bonus_ratio = bonus_match / len(bonus_skills) if bonus_skills else 0
    scores['skill_score'] = req_ratio * 7 + bonus_ratio * 3
    scores['skill_score'] = min(scores['skill_score'], 10)
    
    # 工程
    eng_keywords = ['CI/CD', '架构', 'DevOps', '微服务', '自动化测试']
    eng_count = sum(1 for kw in eng_keywords if kw.lower() in info['raw_text'].lower())
    scores['engineering_score'] = min(eng_count * 2, 10)
    
    # 领域
    domain_keywords = ['AI', '大模型', '深度学习', 'LLM', '算法']
    domain_count = sum(1 for kw in domain_keywords if kw.lower() in info['raw_text'].lower())
    scores['domain_score'] = min(domain_count * 2, 10)
    
    # 潜力
    pot_score = 5.0
    if info['management_experience']:
        pot_score += 2.0
    if info['team_size'] >= 10:
        pot_score += 2.0
    if len(info['skills']) >= 10:
        pot_score += 1.0
    scores['potential_score'] = min(pot_score, 10)
    
    # 总分
    weights = reqs['weights']
    total = sum(scores[k] * weights[k] for k in scores)
    scores['total_score'] = round(total, 2)
    
    # 决策
    if scores['total_score'] >= 8.5:
        decision = 'strong_recommend'
    elif scores['total_score'] >= 7.0:
        decision = 'recommend'
    elif scores['total_score'] >= 5.0:
        decision = 'borderline'
    else:
        decision = 'not_recommend'
    
    return {**scores, 'decision': decision}

def main():
    print('='*60)
    print('AI负责人完整匹配流程（修复版）')
    print('='*60)
    
    # 步骤1：扫描目录
    print('\n[步骤1/5 扫描简历目录]')
    resume_files = []
    for root, dirs, files in os.walk(RESUME_DIR):
        for f in files:
            if f.lower().endswith(('.pdf', '.docx', '.doc', '.txt')):
                resume_files.append(os.path.join(root, f))
    print(f'找到 {len(resume_files)} 份简历文件')
    
    # 步骤2：解析简历
    print('\n[步骤2/5 解析简历内容]')
    candidates = []
    for i, file_path in enumerate(resume_files, 1):
        print(f'处理中 ({i}/{len(resume_files)}): {os.path.basename(file_path)}')
        text = extract_text(file_path)
        if len(text.strip()) < 100:
            print(f'  跳过：内容不足')
            continue
        
        # 提取信息
        info = {}
        # 姓名
        name_match = re.search(r'姓名[：:]\s*(\S{2,4})', text)
        info['name'] = name_match.group(1).strip() if name_match else '未知姓名'
        # 教育
        info['education'] = text
        # 工作年限
        info['experience_years'] = parse_experience_years(text)
        # 技能
        all_skills = JOB_REQS['required_skills'] + JOB_REQS['bonus_skills']
        info['skills'] = [s for s in all_skills if s.lower() in text.lower()]
        # 管理经验
        mgmt_keywords = ['管理', '负责人', '经理', '总监', '带领团队']
        info['management_experience'] = any(kw in text for kw in mgmt_keywords)
        # 团队规模
        info['team_size'] = parse_team_size(text)
        # 原始文本
        info['raw_text'] = text[:1000]
        # 文件路径
        info['file_path'] = file_path
        
        # 步骤3：计算得分
        score_result = calculate_score(info, JOB_REQS)
        
        candidates.append({
            'name': info['name'],
            'total_score': round(score_result['total_score'] * 10, 1),
            'detailed_scores': score_result,
            'skills': info['skills'],
            'experience_years': info['experience_years'],
            'management_experience': info['management_experience'],
            'team_size': info['team_size'],
            'decision': score_result['decision'],
            'file_path': file_path
        })
    
    # 步骤4：排序输出
    print('\n[步骤4/5 排序结果]')
    candidates.sort(key=lambda x: x['total_score'], reverse=True)
    
    print('\n🏆 最终排名（前3名）：')
    print('-'*60)
    for i, c in enumerate(candidates[:3], 1):
        print(f'\n第{i}名: {c["name"]}')
        print(f'  总分: {c["total_score"]}/100')
        print(f'  工作经验: {c["experience_years"]}年')
        print(f'  团队规模: {c["team_size"]}人')
        print(f'  决策: {c["decision"]}')
        print(f'  技能: {", ".join(c["skills"][:8])}')
    
    # 步骤5：保存结果
    print('\n[步骤5/5 保存结果]')
    os.makedirs('reports', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f'报告已保存: {OUTPUT_REPORT}')
    
    with open(OUTPUT_DB, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f'数据库已更新: {OUTPUT_DB}')
    
    print('\n✅ 匹配流程执行完成！')

if __name__ == '__main__':
    main()
