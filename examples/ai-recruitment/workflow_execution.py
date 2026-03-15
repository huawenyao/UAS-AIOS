import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
import olefile
from docx import Document
import PyPDF2
import re

# 配置（可通过环境变量 RESUME_DIR 或 CLI --resume-dir 覆盖）
DEFAULT_RESUME_DIR = os.environ.get("RESUME_DIR", r"C:\Users\ranwu\Documents")
RESUME_DIR = DEFAULT_RESUME_DIR
JOB_REQUIREMENTS = {
    "position_title": "AI负责人",
    "required_degree": "本科及以上",
    "min_experience_years": 8,
    "management_required": True,
    "required_skills": ["Python", "Java", "C++", "TensorFlow", "PyTorch", "深度学习", "机器学习", "大语言模型", "LLM", "计算机视觉", "CV", "自然语言处理", "NLP", "算法"],
    "bonus_skills": ["团队管理", "项目管理", "技术架构", "技术战略", "产品落地"],
    "target_industry": "互联网/AI",
    "weights": {
        "education": 0.10,
        "experience": 0.25,
        "skill": 0.35,
        "engineering": 0.10,
        "domain": 0.10,
        "potential": 0.10
    }
}

def extract_pdf_text(file_path):
    """提取PDF文件文本"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"PDF提取失败 {file_path}: {e}")
        return ""

def extract_docx_text(file_path):
    """提取DOCX文件文本"""
    try:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        print(f"DOCX提取失败 {file_path}: {e}")
        return ""

def extract_doc_text(file_path):
    """提取DOC文件文本"""
    try:
        if not olefile.isOleFile(file_path):
            return ""
        
        ole = olefile.OleFileIO(file_path)
        if ole.exists('WordDocument'):
            stream = ole.openstream('WordDocument')
            data = stream.read()
            
            text_parts = []
            current = []
            for byte in data:
                if 32 <= byte <= 126 or byte in [10, 13]:
                    current.append(chr(byte))
                else:
                    if len(current) >= 3:
                        text_parts.append(''.join(current))
                    current = []
            
            if current:
                text_parts.append(''.join(current))
            
            return ' '.join(text_parts)
        return ""
    except Exception as e:
        print(f"DOC提取失败 {file_path}: {e}")
        return ""

def extract_resume_text(file_path):
    """统一提取简历文本"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_pdf_text(file_path)
    elif ext == '.docx':
        return extract_docx_text(file_path)
    elif ext == '.doc':
        return extract_doc_text(file_path)
    elif ext == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    return f.read()
            except:
                return ""
    return ""

def parse_resume_info(text, file_path):
    """解析简历关键信息"""
    info = {
        "candidate_id": f"cand_{int(datetime.now().timestamp())}_{os.path.basename(file_path).split('.')[0][:10]}",
        "name": "",
        "education": [],
        "experience_years": 0,
        "skills": [],
        "management_experience": False,
        "team_size": 0,
        "projects": [],
        "raw_text": text[:1000]  # 保留前1000字符用于证据
    }
    
    # 提取姓名
    name_patterns = [
        r'姓\s*名[：:]\s*([^\n\r\s]{2,4})',
        r'^([^\n\r\s]{2,4})\s*\n',
        r'申请人[：:]\s*([^\n\r\s]{2,4})'
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            info['name'] = match.group(1).strip()
            break
    
    # 提取教育背景
    edu_patterns = [r'(大学|学院|本科|硕士|博士|研究生)\s*[^\n\r]*']
    for pattern in edu_patterns:
        matches = re.findall(pattern, text)
        info['education'].extend(matches)
    
    # 提取工作年限
    year_patterns = [
        r'(\d{4})\s*[-~至]\s*(\d{4}|至今)',
        r'工作经验\s*[：:]\s*(\d+)\s*年',
        r'(\d+)\s*年.*经验'
    ]
    years = []
    current_year = datetime.now().year
    for pattern in year_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                start = match[0]
                end = match[1] if match[1] != '至今' else str(current_year)
                if start.isdigit() and end.isdigit():
                    years.append(int(end) - int(start))
            elif match.isdigit():
                years.append(int(match))
    
    if years:
        info['experience_years'] = max(years)
    
    # 提取技能
    for skill in JOB_REQUIREMENTS['required_skills'] + JOB_REQUIREMENTS['bonus_skills']:
        if skill.lower() in text.lower():
            info['skills'].append(skill)
    
    # 检查管理经验
    mgmt_keywords = ['管理', '负责人', '经理', '主管', '总监', 'leader', 'manager', '带领团队', '团队规模']
    for kw in mgmt_keywords:
        if kw in text:
            info['management_experience'] = True
            # 尝试提取团队规模
            size_match = re.search(r'(\d+)\s*人.*团队', text)
            if size_match:
                info['team_size'] = int(size_match.group(1))
            break
    
    return info

def calculate_professional_score(resume_info, job_req):
    """按照resume_scoring_agentic.md规则计算专业评分"""
    scores = {
        "education_score": 0,
        "experience_score": 0,
        "skill_score": 0,
        "engineering_score": 0,
        "domain_score": 0,
        "potential_score": 0
    }
    
    evidence = []
    risk_flags = []
    
    # 1. 学历评分 (0-10)
    required_degree = job_req['required_degree']
    resume_edu = ' '.join(resume_info['education']).lower()
    
    degree_map = {'大专': 1, '本科': 2, '硕士': 3, '博士': 4}
    required_level = 2  # 默认本科
    for deg, level in degree_map.items():
        if deg in required_degree:
            required_level = level
    
    resume_level = 0
    for deg, level in degree_map.items():
        if deg in resume_edu:
            resume_level = max(resume_level, level)
    
    if resume_level >= required_level:
        scores['education_score'] = 8.0 if resume_level == required_level else 9.5
        evidence.append(f"学历符合要求: {required_degree}，候选人学历：{'/'.join(resume_info['education'][:2])}")
    else:
        scores['education_score'] = 3.0
        risk_flags.append("education_below_requirement")
        evidence.append(f"学历不足：要求{required_degree}，候选人仅{'/'.join(resume_info['education'][:2]) if resume_info['education'] else '未明确'}")
    
    # 2. 经验评分 (0-10)
    min_years = job_req['min_experience_years']
    exp_years = resume_info['experience_years']
    
    if exp_years >= min_years * 1.5:
        scores['experience_score'] = 9.5
        evidence.append(f"经验远超要求：要求{min_years}年，候选人有{exp_years}年经验")
    elif exp_years >= min_years:
        scores['experience_score'] = 8.0
        evidence.append(f"经验符合要求：要求{min_years}年，候选人有{exp_years}年经验")
    elif exp_years >= min_years * 0.7:
        scores['experience_score'] = 5.0
        evidence.append(f"经验接近要求：要求{min_years}年，候选人有{exp_years}年经验")
    else:
        scores['experience_score'] = 2.0
        risk_flags.append("insufficient_experience")
        evidence.append(f"经验不足：要求{min_years}年，候选人仅有{exp_years}年经验")
    
    # 3. 技能评分 (0-10)
    required_skills = job_req['required_skills']
    bonus_skills = job_req['bonus_skills']
    resume_skills = resume_info['skills']
    
    required_match = len(set(required_skills) & set(resume_skills))
    bonus_match = len(set(bonus_skills) & set(resume_skills))
    
    if required_match >= len(required_skills) * 0.8:
        scores['skill_score'] = 8.0 + (bonus_match / len(bonus_skills)) * 2 if bonus_skills else 8.0
        evidence.append(f"技能匹配度高：掌握{required_match}项必备技能，{bonus_match}项加分技能")
    elif required_match >= len(required_skills) * 0.5:
        scores['skill_score'] = 5.0 + (bonus_match / len(bonus_skills)) * 3 if bonus_skills else 5.0
        evidence.append(f"技能基本匹配：掌握{required_match}项必备技能，{bonus_match}项加分技能")
    else:
        scores['skill_score'] = 2.0
        risk_flags.append("insufficient_skills")
        evidence.append(f"技能不足：仅掌握{required_match}项必备技能")
    
    # 4. 工程实践评分 (0-10)
    engineering_keywords = ['CI/CD', '自动化测试', '单元测试', '代码评审', 'Code Review', 'DevOps', '架构设计']
    eng_count = sum(1 for kw in engineering_keywords if kw.lower() in resume_info['raw_text'].lower())
    scores['engineering_score'] = min(eng_count * 2, 10)
    if eng_count > 0:
        evidence.append(f"工程实践：掌握{eng_count}项工程相关技能")
    else:
        evidence.append("工程实践：未提及相关经验，保守评分")
    
    # 5. 领域经验评分 (0-10)
    domain_keywords = ['AI', '人工智能', '大模型', 'LLM', '深度学习', '算法']
    domain_count = sum(1 for kw in domain_keywords if kw.lower() in resume_info['raw_text'].lower())
    scores['domain_score'] = min(domain_count * 2, 10)
    if domain_count > 0:
        evidence.append(f"领域经验：具备{domain_count}项AI领域相关经验")
    else:
        evidence.append("领域经验：未提及AI相关经验，保守评分")
    
    # 6. 潜力评分 (0-10)
    potential_score = 5.0
    if resume_info['management_experience']:
        potential_score += 2.0
    if resume_info['team_size'] >= 10:
        potential_score += 2.0
    if len(resume_info['skills']) >= 10:
        potential_score += 1.0
    scores['potential_score'] = min(potential_score, 10)
    
    if resume_info['management_experience']:
        evidence.append(f"管理经验：具备管理经验，团队规模{resume_info['team_size'] if resume_info['team_size'] > 0 else '未明确'}人")
    
    # 计算总分
    weights = job_req['weights']
    total_score = (
        scores['education_score'] * weights['education'] +
        scores['experience_score'] * weights['experience'] +
        scores['skill_score'] * weights['skill'] +
        scores['engineering_score'] * weights['engineering'] +
        scores['domain_score'] * weights['domain'] +
        scores['potential_score'] * weights['potential']
    )
    
    # 决策
    if total_score >= 8.5:
        decision = "strong_recommend"
    elif total_score >= 7.0:
        decision = "recommend"
    elif total_score >= 5.0:
        decision = "borderline"
    else:
        decision = "not_recommend"
    
    return {
        "candidate_id": resume_info["candidate_id"],
        "job_id": "job-ai-director",
        "name": resume_info["name"] if resume_info["name"] else "未知姓名",
        "scores": {**scores, "total_score": round(total_score, 2)},
        "decision": decision,
        "risk_flags": risk_flags,
        "evidence": evidence,
        "basic_info": {
            "experience_years": resume_info["experience_years"],
            "skills": resume_info["skills"],
            "management_experience": resume_info["management_experience"],
            "team_size": resume_info["team_size"],
            "file_path": resume_info.get("file_path", "")
        }
    }

def main():
    global RESUME_DIR
    parser = argparse.ArgumentParser(description="AI 招聘智能分析工作流：扫描简历目录 → 匹配打分 → 生成报告")
    parser.add_argument("--resume-dir", default=None, help="简历目录路径（默认使用环境变量 RESUME_DIR 或内置默认）")
    args = parser.parse_args()
    if args.resume_dir:
        RESUME_DIR = os.path.abspath(args.resume_dir)
    else:
        RESUME_DIR = DEFAULT_RESUME_DIR

    print("="*60)
    print("AI招聘智能分析工作流 - 专业版")
    print("="*60)
    print(f"简历目录: {RESUME_DIR}")

    # 步骤1：扫描简历
    print("\n[步骤1/4 扫描简历目录]")
    resume_files = []
    for root, dirs, files in os.walk(RESUME_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.pdf', '.docx', '.doc', '.txt']:
                resume_files.append(os.path.join(root, file))
    
    print(f"找到 {len(resume_files)} 份简历文件")
    
    # 步骤2：处理简历
    print("\n[步骤2/4 处理简历文件]")
    results = []
    valid_count = 0
    
    for i, file_path in enumerate(resume_files, 1):
        print(f"处理中 ({i}/{len(resume_files)}): {os.path.basename(file_path)}")
        text = extract_resume_text(file_path)
        
        if len(text.strip()) < 100:
            print(f"  警告：内容过短，跳过")
            continue
        
        valid_count += 1
        resume_info = parse_resume_info(text, file_path)
        resume_info["file_path"] = file_path
        score_result = calculate_professional_score(resume_info, JOB_REQUIREMENTS)
        results.append(score_result)
    
    # 步骤3：排序
    print("\n[步骤3/4 排序结果]")
    results.sort(key=lambda x: x['scores']['total_score'], reverse=True)
    
    # 步骤4：保存结果
    print("\n[步骤4/4 保存结果]")
    
    # 保存到 database（与 entity_schemas 对齐：补全 status、updated_at）
    os.makedirs('database', exist_ok=True)
    now = datetime.now().isoformat()
    for r in results:
        r.setdefault("status", "screened")
        r.setdefault("created_at", now)
        r.setdefault("updated_at", now)
    with open('database/candidates.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("已保存: database/candidates.json")

    # 实体运行时闭环：发布 screening_completed 事件（与 UAS agent runtime 事件驱动一致）
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
        from entity_runtime import emit_event
        job_id = results[0].get("job_id", "job-ai-director") if results else "job-ai-director"
        for r in results:
            emit_event("screening_completed", job_id=job_id, candidate_id=r.get("candidate_id"), payload={"decision": r.get("decision")})
        print("已发布 screening_completed 事件（见 database/events.json）")
    except Exception as e:
        pass  # 无 entity_runtime 时跳过
    
    # 保存到reports
    os.makedirs('reports', exist_ok=True)
    report_file = f'reports/ai_recruitment_workflow_professional_result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"已保存: {report_file}")

    # 为每位候选人生成带证据链与风险标识的 HTML 报告
    root_dir = Path(__file__).resolve().parent
    reports_dir = root_dir / "reports"
    try:
        sys.path.insert(0, str(root_dir / "scripts"))
        from report_renderer import render_html
        for r in results:
            cid = r.get("candidate_id", "unknown")
            html = render_html(
                cid,
                r.get("scores", {}),
                decision=r.get("decision"),
                risk_flags=r.get("risk_flags"),
                evidence=r.get("evidence"),
                name=r.get("name"),
                job_id=r.get("job_id"),
            )
            out_path = reports_dir / f"candidate_{cid}.html"
            out_path.write_text(html, encoding="utf-8")
        print(f"已生成 {len(results)} 份 HTML 报告（含证据链与风险标识）")
    except Exception as e:
        print(f"HTML 报告生成跳过: {e}")
    
    # 输出统计
    print("\n" + "="*60)
    print("执行完成！统计信息：")
    print(f"总简历数: {len(resume_files)}")
    print(f"有效简历数: {valid_count}")
    print(f"平均分: {round(sum(r['scores']['total_score'] for r in results) / len(results) if results else 0, 2)}")
    print("\n各决策级别分布:")
    decisions = {}
    for r in results:
        dec = r['decision']
        decisions[dec] = decisions.get(dec, 0) + 1
    for k, v in decisions.items():
        print(f"  {k}: {v}")
    # 价值感呈现：一句可感知的价值摘要
    recommend_count = sum(decisions.get(d, 0) for d in ["strong_recommend", "recommend", "borderline"])
    print("\n[价值摘要] 本批 {} 份有效简历，推荐/待定共 {} 人，可解释推荐名单已生成，可直接用于面试名单决策。".format(valid_count, recommend_count))