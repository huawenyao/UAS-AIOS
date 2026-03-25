import PyPDF2
import re

# 读取华文尧简历
file_path = r'C:\Users\ranwu\Documents\华文尧个人简历.pdf'
text = ''
with open(file_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'

print('='*60)
print('华文尧简历内容提取：')
print('='*60)
print(text)
print('\n' + '='*60)
print('关键信息分析：')
print('='*60)

# 提取工作年限
print("\n1. 工作年限识别:")
year_patterns = [
    r'(\d{4})\s*[-~至到]\s*(\d{4}|至今|现在)',
    r'(\d{4})年\s*[-~至到]\s*(\d{4}|至今|现在)年',
    r'工作经验\s*[：:]\s*(\d+)\s*年',
    r'(\d+)\s*年.*工作经验',
    r'从业时间\s*[：:]\s*(\d+)\s*年'
]

all_years = []
for pattern in year_patterns:
    matches = re.findall(pattern, text)
    for match in matches:
        if isinstance(match, tuple):
            start = match[0]
            end = match[1]
            if start.isdigit():
                if end in ['至今', '现在']:
                    end_year = 2026
                elif end.isdigit():
                    end_year = int(end)
                else:
                    continue
                years = end_year - int(start)
                if years > 0 and years < 60:  # 合理范围
                    all_years.append(years)
                    print(f"  匹配到: {start} - {end} = {years}年")
        elif match.isdigit():
            years = int(match)
            all_years.append(years)
            print(f"  直接匹配到: {years}年")

if all_years:
    experience_years = max(all_years)
    print(f"  最终识别工作年限: {experience_years}年")
else:
    experience_years = 0
    print(f"  未识别到有效工作年限，默认: 0年")

# 提取技能
print("\n2. 技能匹配:")
required_skills = ['Python', 'Java', 'C++', 'TensorFlow', 'PyTorch', '深度学习', '机器学习', '大语言模型', 'LLM', '计算机视觉', 'CV', '自然语言处理', 'NLP', '算法']
bonus_skills = ['团队管理', '项目管理', '技术架构', '技术战略', '产品落地']

found_required = [s for s in required_skills if s.lower() in text.lower()]
found_bonus = [s for s in bonus_skills if s.lower() in text.lower()]

print(f"  必备技能匹配: {found_required} ({len(found_required)}/{len(required_skills)})")
print(f"  加分技能匹配: {found_bonus} ({len(found_bonus)}/{len(bonus_skills)})")

# 管理经验
print("\n3. 管理经验:")
mgmt_patterns = [
    r'管理\s*(\d+)\s*人',
    r'团队规模\s*[：:]\s*(\d+)',
    r'带领\s*(\d+)\s*人',
    r'负责\s*(\d+)\s*人团队',
    r'经理|总监|负责人|主管|leader|manager'
]

mgmt_found = []
team_size = 0
for pattern in mgmt_patterns:
    matches = re.findall(pattern, text.lower())
    for match in matches:
        if isinstance(match, str) and match.isdigit():
            team_size = int(match)
            mgmt_found.append(f"团队规模: {team_size}人")
        elif match:
            mgmt_found.append(f"管理关键词: {match}")

print(f"  管理经验识别: {mgmt_found if mgmt_found else '未识别到明确管理经验'}")
print(f"  团队规模: {team_size}人")

# 教育背景
print("\n4. 教育背景:")
edu_patterns = [r'博士|硕士|研究生|本科|大专|大学|学院']
edu_found = []
for pattern in edu_patterns:
    matches = re.findall(pattern, text)
    edu_found.extend(matches)

print(f"  教育背景识别: {list(set(edu_found)) if edu_found else '未识别到教育背景'}")

# 评分计算（按照标准规则）
print("\n" + '='*60)
print("评分计算（标准算法）:")
print('='*60)

weights = {
    'education': 0.10,
    'experience': 0.25,
    'skill': 0.35,
    'engineering': 0.10,
    'domain': 0.10,
    'potential': 0.10
}

# 学历评分 (0-10)
education_score = 8.0 if any(kw in edu_found for kw in ['本科', '硕士', '博士']) else 3.0
print(f"1. 学历评分: {education_score}/10")

# 经验评分 (0-10)
min_required = 8
if experience_years >= min_required * 1.5:
    experience_score = 9.5
elif experience_years >= min_required:
    experience_score = 8.0
elif experience_years >= min_required * 0.7:
    experience_score = 5.0
else:
    experience_score = 2.0
print(f"2. 经验评分: {experience_score}/10 (要求: {min_required}年, 实际: {experience_years}年)")

# 技能评分 (0-10)
required_match_rate = len(found_required) / len(required_skills)
bonus_match_rate = len(found_bonus) / len(bonus_skills) if bonus_skills else 0
skill_score = required_match_rate * 7 + bonus_match_rate * 3
skill_score = min(skill_score, 10)
print(f"3. 技能评分: {skill_score:.1f}/10 (必备匹配率: {required_match_rate:.1%}, 加分匹配率: {bonus_match_rate:.1%})")

# 工程实践评分 (0-10)
engineering_keywords = ['CI/CD', '自动化测试', '单元测试', '代码评审', '架构设计', 'DevOps']
engineering_match = sum(1 for kw in engineering_keywords if kw.lower() in text.lower())
engineering_score = min(engineering_match * 2, 10)
print(f"4. 工程实践评分: {engineering_score}/10 (匹配到 {engineering_match} 项)")

# 领域经验评分 (0-10)
domain_keywords = ['AI', '人工智能', '大模型', '深度学习', '算法']
domain_match = sum(1 for kw in domain_keywords if kw.lower() in text.lower())
domain_score = min(domain_match * 2, 10)
print(f"5. 领域经验评分: {domain_score}/10 (匹配到 {domain_match} 项)")

# 潜力评分 (0-10)
potential_score = 5.0
if mgmt_found:
    potential_score += 2.0
if team_size >= 10:
    potential_score += 2.0
if len(found_required + found_bonus) >= 10:
    potential_score += 1.0
potential_score = min(potential_score, 10)
print(f"6. 潜力评分: {potential_score}/10")

# 总分
total_score = (
    education_score * weights['education'] +
    experience_score * weights['experience'] +
    skill_score * weights['skill'] +
    engineering_score * weights['engineering'] +
    domain_score * weights['domain'] +
    potential_score * weights['potential']
)

print(f"\n加权总分: {total_score:.2f}/10 (百分制: {total_score * 10:.1f}/100)")

# 决策
if total_score >= 8.5:
    decision = "strong_recommend 🌟 强烈推荐"
elif total_score >= 7.0:
    decision = "recommend 👍 推荐"
elif total_score >= 5.0:
    decision = "borderline ⚠️ 待定"
else:
    decision = "not_recommend ❌ 不推荐"

print(f"最终决策: {decision}")

print("\n" + '='*60)
print("低分原因诊断:")
print('='*60)
issues = []
if experience_years < 8:
    issues.append(f"- ❌ 工作经验不足: 仅{experience_years}年，要求8年，拉低了25%权重的经验项得分")
if required_match_rate < 0.5:
    issues.append(f"- ❌ 必备技能匹配率低: {required_match_rate:.1%}，拉低了35%权重的技能项得分")
if not mgmt_found:
    issues.append(f"- ⚠️ 未识别到明确的团队管理经验，影响潜力评分")
if team_size < 10:
    issues.append(f"- ⚠️ 未识别到带领10人以上团队的经验，不符合岗位要求")

if not issues:
    print("✅ 无明显扣分点")
else:
    for issue in issues:
        print(issue)
