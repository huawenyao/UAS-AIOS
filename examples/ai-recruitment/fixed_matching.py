import os
import re
import json
from datetime import datetime
import olefile
from docx import Document
import PyPDF2

# --------------------------
# 配置参数
# --------------------------
# AI负责人岗位标准要求
JOB_REQUIREMENTS = {
    "position_title": "AI负责人",
    "required_degree": "本科及以上",
    "min_experience_years": 8,
    "management_required": True,
    "min_team_size": 10,
    "target_industry": "互联网、科技、AI",
    "required_skills": [
        "Python", "Java", "C++", "TensorFlow", "PyTorch", 
        "深度学习", "机器学习", "大语言模型", "LLM",
        "计算机视觉", "CV", "自然语言处理", "NLP",
        "算法", "AI算法", "人工智能"
    ],
    "bonus_skills": [
        "团队管理", "项目管理", "技术架构", "技术战略",
        "产品落地", "团队建设", "跨部门协作", "技术创新"
    ],
    "education_major": ["计算机", "软件工程", "人工智能", "数学", "统计学"]
}

# 支持的简历文件格式
SUPPORTED_EXTENSIONS = ['.doc', '.docx', '.pdf', '.txt']

# 权重配置
WEIGHTS = {
    'skill_match': 0.25,
    'experience_match': 0.20,
    'education_match': 0.15,
    'management_match': 0.20,
    'industry_match': 0.20
}

# --------------------------
# 工具函数
# --------------------------
def scan_resume_directory(directory_path):
    """扫描目录下所有支持的简历文件"""
    resume_files = []
    if not os.path.exists(directory_path):
        print(f"错误：目录不存在 - {directory_path}")
        return resume_files
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                resume_files.append(os.path.join(root, file))
    
    print(f"找到 {len(resume_files)} 份简历文件")
    return resume_files

def extract_text_from_doc(file_path):
    """从.doc文件提取文本"""
    try:
        if not olefile.isOleFile(file_path):
            return ""
        
        ole = olefile.OleFileIO(file_path)
        text_parts = []
        
        try:
            if ole.exists('WordDocument'):
                word_stream = ole.openstream('WordDocument').read()
                current_text = []
                for byte in word_stream:
                    if 32 <= byte <= 126 or 0x4e00 <= byte <= 0x9fff:  # ASCII + 中文
                        current_text.append(chr(byte))
                    else:
                        if len(current_text) >= 3:
                            text_parts.append(''.join(current_text))
                        current_text = []
                
                if len(current_text) >= 3:
                    text_parts.append(''.join(current_text))
        finally:
            ole.close()
        
        return ' '.join(text_parts) if text_parts else ""
    except Exception as e:
        print(f".doc提取失败 {file_path}: {str(e)}")
        return ""

def extract_text_from_docx(file_path):
    """从.docx文件提取文本"""
    try:
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        print(f".docx提取失败 {file_path}: {str(e)}")
        return ""

def extract_text_from_pdf(file_path):
    """从.pdf文件提取文本"""
    try:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f".pdf提取失败 {file_path}: {str(e)}")
        return ""

def extract_text_from_txt(file_path):
    """从.txt文件提取文本"""
    try:
        encodings = ['utf-8', 'gbk', 'gb2312']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        return ""
    except Exception as e:
        print(f".txt提取失败 {file_path}: {str(e)}")
        return ""

def extract_resume_content(file_path):
    """根据文件类型提取简历内容"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.doc':
        return extract_text_from_doc(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        return ""

def parse_resume_info(text):
    """解析简历关键信息"""
    info = {
        'name': '',
        'education': [],
        'experience_years': 0,
        'skills': [],
        'management_experience': False,
        'team_size': 0,
        'industry_experience': []
    }
    
    # 提取姓名
    name_patterns = [
        r'姓名[：:]\s*(\S{2,4})',
        r'^(\S{2,4})\s*[男|女]',
        r'^(\S{2,4})\s*\d{4,}'
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            info['name'] = match.group(1)
            break
    
    # 提取教育背景
    edu_keywords = ['大学', '学院', '本科', '硕士', '博士', '研究生']
    sentences = re.split(r'[。\n！；]', text)
    for sent in sentences:
        if any(kw in sent for kw in edu_keywords):
            info['education'].append(sent.strip())
    
    # 提取工作经验年限（修复：支持多种时间格式）
    year_patterns = [
        r'(\d{4})\.(\d{1,2})\s*[-~至到—]\s*(\d{4})\.(\d{1,2})',  # 2025.08 - 2026.03
        r'(\d{4})\.(\d{1,2})\s*[-~至到—]\s*(至今|现在)',         # 2025.08 - 至今
        r'(\d{4})年\s*[-~至到—]\s*(\d{4})年',                   # 2025年 - 2026年
        r'(\d{4})年\s*[-~至到—]\s*(至今|现在)',                 # 2025年 - 至今
        r'(\d{4})\s*[-~至到—]\s*(\d{4})',                       # 2025 - 2026
        r'(\d{4})\s*[-~至到—]\s*(至今|现在)',                   # 2025 - 至今
        r'工作年限\s*[：:]\s*(\d+)\s*年',                        # 工作年限：12年
        r'(\d+)\s*年.*工作经验'                                 # 12年工作经验
    ]
    
    current_year = datetime.now().year
    max_years = 0
    
    for pattern in year_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                # 处理带月份的格式
                if len(match) == 4 and match[0].isdigit() and match[2].isdigit():
                    start_year = int(match[0])
                    end_year = int(match[2])
                    years = end_year - start_year
                    if years > max_years and years < 60:
                        max_years = years
                # 处理带至今的格式
                elif len(match) == 3 and match[0].isdigit() and match[2] in ['至今', '现在']:
                    start_year = int(match[0])
                    years = current_year - start_year
                    if years > max_years and years < 60:
                        max_years = years
                # 处理年份范围
                elif len(match) == 2 and match[0].isdigit():
                    if match[1].isdigit():
                        start_year = int(match[0])
                        end_year = int(match[1])
                        years = end_year - start_year
                    elif match[1] in ['至今', '现在']:
                        start_year = int(match[0])
                        years = current_year - start_year
                    else:
                        continue
                    if years > max_years and years < 60:
                        max_years = years
            elif match.isdigit():
                years = int(match)
                if years > max_years and years < 60:
                    max_years = years
    
    # 如果直接匹配到工作年限字段，优先使用
    direct_exp_match = re.search(r'工作年限[：:]\s*(\d+)\s*年', text)
    if direct_exp_match:
        direct_years = int(direct_exp_match.group(1))
        if direct_years > max_years:
            max_years = direct_years
    
    info['experience_years'] = max_years
    
    # 提取技能
    all_skills = JOB_REQUIREMENTS['required_skills'] + JOB_REQUIREMENTS['bonus_skills']
    for skill in all_skills:
        if skill.lower() in text.lower():
            info['skills'].append(skill)
    
    # 提取管理经验
    mgmt_keywords = ['负责人', '经理', '组长', '主管', '总监', 'leader', 'manager', '管理', '带领', '团队']
    if any(kw in text.lower() for kw in mgmt_keywords):
        info['management_experience'] = True
    
    # 提取团队规模
    team_patterns = [
        r'(\d+)\s*人团队',
        r'下属\s*(\d+)\s*人',
        r'团队规模\s*[：:]\s*(\d+)',
        r'带领\s*(\d+)\s*人'
    ]
    
    for pattern in team_patterns:
        team_match = re.search(pattern, text)
        if team_match:
            info['team_size'] = int(team_match.group(1))
            break
    
    return info

def calculate_match_score(resume_info, job_requirements):
    """计算简历与岗位的匹配度"""
    scores = {
        'skill_match': 0,
        'experience_match': 0,
        'education_match': 0,
        'management_match': 0,
        'industry_match': 0
    }
    
    # 1. 技能匹配度
    required_skills = set(job_requirements['required_skills'])
    bonus_skills = set(job_requirements['bonus_skills'])
    resume_skills = set(resume_info['skills'])
    
    required_match = len(required_skills & resume_skills)
    bonus_match = len(bonus_skills & resume_skills)
    
    if required_skills:
        skill_score = (required_match / len(required_skills)) * 70
        if bonus_skills:
            skill_score += (bonus_match / len(bonus_skills)) * 30
        scores['skill_match'] = min(skill_score, 100)
    
    # 2. 经验匹配度
    required_years = job_requirements['min_experience_years']
    resume_years = resume_info['experience_years']
    
    if required_years > 0:
        exp_ratio = min(resume_years / required_years, 1.5)
        scores['experience_match'] = (exp_ratio / 1.5) * 100
    
    # 3. 教育匹配度
    required_degree = job_requirements['required_degree']
    resume_edu = ' '.join(resume_info['education']).lower()
    
    degree_levels = {'博士': 4, '硕士': 3, '研究生': 3, '本科': 2, '大专': 1}
    required_level = 0
    resume_level = 0
    
    for degree, level in degree_levels.items():
        if degree in required_degree:
            required_level = level
        if degree in resume_edu:
            resume_level = level
    
    if required_level > 0:
        scores['education_match'] = (min(resume_level, required_level) / required_level) * 100
    
    # 4. 管理能力匹配
    required_mgmt = job_requirements['management_required']
    required_team_size = job_requirements['min_team_size']
    resume_mgmt = resume_info['management_experience']
    resume_team_size = resume_info['team_size']
    
    if required_mgmt:
        if resume_mgmt:
            if resume_team_size >= required_team_size:
                scores['management_match'] = 100
            else:
                scores['management_match'] = (resume_team_size / required_team_size) * 80 + 20
        else:
            scores['management_match'] = 0
    else:
        scores['management_match'] = 100 if resume_mgmt else 50
    
    # 5. 行业匹配度
    industry_keywords = ['互联网', '科技', 'AI', '人工智能', '软件', 'IT', '信息技术']
    resume_text = str(resume_info).lower()
    industry_match = sum(1 for kw in industry_keywords if kw.lower() in resume_text)
    scores['industry_match'] = min((industry_match / len(industry_keywords)) * 100, 100)
    
    # 计算总分
    total_score = sum(scores[key] * WEIGHTS[key] for key in scores)
    
    return {
        'detailed_scores': scores,
        'total_score': round(total_score, 2),
        'percentage': round(total_score, 1)
    }

def generate_candidate_report(candidate_info, match_result):
    """生成候选人报告"""
    return {
        'name': candidate_info['name'] or '未知姓名',
        'total_score': match_result['percentage'],
        'detailed_scores': match_result['detailed_scores'],
        'skills': candidate_info['skills'],
        'experience_years': candidate_info['experience_years'],
        'management_experience': candidate_info['management_experience'],
        'team_size': candidate_info['team_size'],
        'core_advantages': [
            f"掌握技能: {', '.join(candidate_info['skills'][:10])}",
            f"工作经验: {candidate_info['experience_years']}年",
            f"管理经验: {'有' if candidate_info['management_experience'] else '无'}",
            f"团队规模: {candidate_info['team_size']}人" if candidate_info['team_size'] > 0 else "团队规模: 未明确"
        ]
    }

def main(resume_directory, top_n=5):
    """主函数"""
    print("=" * 60)
    print("AI负责人岗位简历匹配系统（修复版）")
    print("=" * 60)
    
    # 1. 扫描简历目录
    print("\n[步骤1/5 扫描简历目录: {}]".format(resume_directory))
    resume_files = scan_resume_directory(resume_directory)
    if not resume_files:
        print("未找到任何简历文件")
        return
    
    # 2. 处理每份简历
    print("\n[步骤2/5 处理简历文件，共 {} 份]".format(len(resume_files)))
    candidates = []
    
    for i, file_path in enumerate(resume_files, 1):
        print("处理中 ({}/{}): {}".format(i, len(resume_files), os.path.basename(file_path)))
        
        # 提取内容
        content = extract_resume_content(file_path)
        if not content:
            print("  警告：未能提取到内容，跳过")
            continue
        
        # 解析信息
        resume_info = parse_resume_info(content)
        
        # 计算匹配度
        match_result = calculate_match_score(resume_info, JOB_REQUIREMENTS)
        
        # 生成报告
        report = generate_candidate_report(resume_info, match_result)
        report['file_path'] = file_path
        
        candidates.append(report)
    
    # 3. 排序结果
    print("\n[步骤3/5 排序匹配结果]")
    candidates_sorted = sorted(candidates, key=lambda x: x['total_score'], reverse=True)
    
    # 4. 输出结果
    print("\n[步骤4/