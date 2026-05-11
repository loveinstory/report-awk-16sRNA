"""
PDF数据解析模块
从原始肠道菌群检测报告PDF中提取结构化数据
"""
import re
import pdfplumber
import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_parser.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def parse_report_pdf(pdf_path: str) -> dict:
    """
    解析肠道菌群检测报告PDF，返回结构化数据字典
    """
    data = {
        "basic_info": {},
        "test_info": {},
        "report_info": {},
        "core_indices": [],
        "phylum_distribution": [],
        "genus_distribution": [],
        "beneficial_bacteria": [],
        "harmful_bacteria": [],
        "be_ratio": {},
        "disease_risk": {},
        "metabolism": [],
        "barrier_function": [],
        "ai_conclusion": "",
        "diet_advice": [],
        "probiotic_advice": [],
        "lifestyle_advice": [],
        "intervention_plan": {
            "phase1": [],
            "phase2": [],
            "phase3": [],
        },
        "science_education": {},
    }

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                full_text += f"\n----- 第{i}页 -----\n{text}\n"

    # 解析基本信息
    data["basic_info"] = parse_basic_info(full_text)
    data["test_info"] = parse_test_info(full_text)
    data["report_info"] = parse_report_info(full_text)

    # 解析核心指数
    data["core_indices"] = parse_core_indices(full_text)

    # 解析菌群分布
    data["phylum_distribution"] = parse_phylum_distribution(full_text)
    data["genus_distribution"] = parse_genus_distribution(full_text)

    # 解析有益菌/有害菌
    data["beneficial_bacteria"] = parse_beneficial_bacteria(full_text)
    data["harmful_bacteria"] = parse_harmful_bacteria(full_text)

    # 解析B/E比值
    data["be_ratio"] = parse_be_ratio(full_text)

    # 解析疾病风险
    data["disease_risk"] = parse_disease_risk(full_text)

    # 解析物质代谢
    data["metabolism"] = parse_metabolism(full_text)

    # 解析肠道屏障
    data["barrier_function"] = parse_barrier_function(full_text)

    # 解析AI结论
    data["ai_conclusion"] = parse_ai_conclusion(full_text)

    # 解析健康建议
    data["diet_advice"] = parse_diet_advice(full_text)
    data["probiotic_advice"] = parse_probiotic_advice(full_text)
    data["lifestyle_advice"] = parse_lifestyle_advice(full_text)

    # 解析干预计划
    data["intervention_plan"] = parse_intervention_plan(full_text)

    return data


def extract_field(text: str, field_names: list, end_markers: list = None) -> str:
    """
    通用字段提取函数
    field_names: 字段名的多种可能写法
    end_markers: 结束标记，用于截断
    """
    if end_markers is None:
        end_markers = ["\n", "  ", "\t", "送检", "性别", "样本", "年龄", "检测", "联系", "报告"]
    
    for field_name in field_names:
        # 尝试多种分隔符
        for separator in ["：", ":", " ", ""]:
            pattern = f"{field_name}{separator}([^\n\r]+)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # 根据结束标记截断
                for marker in end_markers:
                    if marker in value:
                        value = value.split(marker)[0].strip()
                if value and value != field_name:
                    return value
    return ""


def parse_basic_info(text: str) -> dict:
    """解析受检者基本信息"""
    info = {}
    
    # 姓名
    info["name"] = extract_field(text, ["姓名", "受检者", "患者姓名"])
    
    # 性别 - 尝试直接匹配
    gender_match = re.search(r"性别[：:]?\s*([男女])", text, re.IGNORECASE)
    if gender_match:
        info["gender"] = gender_match.group(1)
    else:
        info["gender"] = extract_field(text, ["性别"])
    
    # 年龄
    age_match = re.search(r"年龄[：:]?\s*(\d+)", text, re.IGNORECASE)
    if age_match:
        info["age"] = age_match.group(1)
    else:
        info["age"] = extract_field(text, ["年龄", "岁数"])
    
    # 联系电话
    phone_match = re.search(r"(?:联系电话|电话|手机)[：:]?\s*(\d{11}|\d{3,4}-?\d{7,8})", text, re.IGNORECASE)
    if phone_match:
        info["phone"] = phone_match.group(1)
    else:
        info["phone"] = extract_field(text, ["联系电话", "电话", "手机"])
    
    # 主要不适/症状
    info["symptoms"] = extract_field(text, ["主要不适", "不适症状", "症状", "疾病", "诊断"])
    
    return info


def parse_test_info(text: str) -> dict:
    """解析检测信息"""
    info = {}
    
    # 送检单位
    info["unit"] = extract_field(text, ["送检单位", "单位", "医院", "机构"])
    
    # 样本编号
    sample_id_match = re.search(r"样本编号[：:]?\s*([A-Z0-9\-]+)", text, re.IGNORECASE)
    if sample_id_match:
        info["sample_id"] = sample_id_match.group(1)
    else:
        info["sample_id"] = extract_field(text, ["样本编号", "编号", "条码"])
    
    # 样本类型
    sample_type_match = re.search(r"样本类型[：:]?\s*(粪便|血液|唾液|组织)", text, re.IGNORECASE)
    if sample_type_match:
        info["sample_type"] = sample_type_match.group(1)
    else:
        info["sample_type"] = extract_field(text, ["样本类型", "样本种类", "类型"])
    
    # 采样日期 - 尝试匹配日期格式
    date_match = re.search(r"(?:采样日期|日期|时间)[：:]?\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)", text, re.IGNORECASE)
    if date_match:
        info["sample_date"] = date_match.group(1)
    else:
        info["sample_date"] = extract_field(text, ["采样日期", "采样时间", "日期"])
    
    # 检测方法
    method_match = re.search(r"检测方法[：:]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
    if method_match:
        info["method"] = method_match.group(1).strip()
    else:
        info["method"] = extract_field(text, ["检测方法", "检测方式", "方法", "技术"])
    
    # 检测项目
    test_item_match = re.search(r"检测项目[：:]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
    if test_item_match:
        info["test_item"] = test_item_match.group(1).strip()
    else:
        info["test_item"] = extract_field(text, ["检测项目", "项目"])
    
    return info


def parse_report_info(text: str) -> dict:
    """解析报告信息"""
    info = {}
    
    # 报告编号
    report_id_match = re.search(r"报告编号[：:]?\s*([A-Z0-9\-]+)", text, re.IGNORECASE)
    if report_id_match:
        info["report_id"] = report_id_match.group(1)
    else:
        info["report_id"] = extract_field(text, ["报告编号", "编号"])
    
    # 报告日期
    date_match = re.search(r"(?:报告日期|报告时间)[：:]?\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)", text, re.IGNORECASE)
    if date_match:
        info["report_date"] = date_match.group(1)
    else:
        info["report_date"] = extract_field(text, ["报告日期", "报告时间", "日期"])
    
    return info


def parse_core_indices(text: str) -> list:
    """解析核心检测结果"""
    indices = []
    
    # 直接在整个文本中搜索，不限制区域
    search_text = text
    
    # 清理文本 - 保留换行以便更好地逐行处理
    search_text = re.sub(r'[ \t]+', ' ', search_text)
    search_text = re.sub(r'\n+', '\n', search_text)
    
    # GMHI评分 - 增强匹配
    gmhi_patterns = [
        r"GMHI[评分]*[\s：:]+\s*([\d.]+)",
        r"GMHI\s+([\d.]+)",
        r"肠道健康指数[\s：:]+\s*([\d.]+)",
        # 支持第4页的格式：GMHI<60分后面跟着两行文本后才是数值
        r"GMHI.*?\n.*?\n\s*([\d.]+)\s*\n",
        # 支持更通用的格式：GMHI后面若干字符和换行后出现数值
        r"GMHI[^0-9]*?([\d.]+)",
    ]
    for pattern in gmhi_patterns:
        gmhi_match = re.search(pattern, search_text, re.IGNORECASE)
        if gmhi_match:
            result = gmhi_match.group(1).strip()
            # 验证是有效数字
            if result and re.match(r'^[\d.]+$', result):
                indices.append({
                    "name": "GMHI评分",
                    "result": result,
                    "description": "肠道健康指数"
                })
                break
        
    # 菌群多样性 - 增强匹配（支持定性描述如"偏低"）
    diversity_patterns = [
        r"(?:菌群)?多样性[\s：:]+\s*([\d.]+)",
        r"Shannon[指数]*[\s：:]+\s*([\d.]+)",
        r"多样性指数[\s：:]+\s*([\d.]+)",
        r"(?:菌群)?多样性\s+([\d.]+)",
        # 支持定性描述
        r"(?:菌群)?多样性\s+(偏低|正常|偏高)",
    ]
    for pattern in diversity_patterns:
        diversity_match = re.search(pattern, search_text, re.IGNORECASE)
        if diversity_match:
            result = diversity_match.group(1)
            # 如果是定性描述，保留原值；如果是数字，保持不变
            indices.append({
                "name": "菌群多样性",
                "result": result,
                "description": "菌群丰富度指标"
            })
            break
        
    # 肠道年龄 - 增强匹配（支持跨行匹配："肠道年龄"下一行是数值）
    gut_age_patterns = [
        r"(?:肠道年龄|肠龄)[\s：:]+\s*(\d+)",
        r"(?:肠道年龄|肠龄)\s+(\d+)",
        r"(?:肠道年龄|肠龄)[\s：:]+\s*(\d+)\s*岁",
        # 支持跨行匹配：肠道年龄\n数值
        r"(?:肠道年龄|肠龄)\s*\n\s*(\d+)",
    ]
    for pattern in gut_age_patterns:
        gut_age_match = re.search(pattern, search_text, re.IGNORECASE)
        if gut_age_match:
            indices.append({
                "name": "肠道年龄",
                "result": f"{gut_age_match.group(1)}岁",
                "description": "肠道生理年龄"
            })
            break
        
    # 肠型 - 增强匹配（支持中文名如"普雷沃菌属"）
    enterotype_patterns = [
        r"肠型[\s：:]+\s*([A-Z])型\s+(拟杆菌型|普雷沃菌型|混合型)?\s*$",
        r"肠型[\s：:]+\s*([A-Z])型\s*$",
        r"肠型[\s：:]+\s*([A-Z])\s*$",
        r"Enterotype[\s：:]+\s*([A-Z])",
        r"肠型\s+([A-Z])型?",
        # 支持中文名格式：肠型 普雷沃菌属
        r"肠型\s+(普雷沃菌属|拟杆菌属|混合型)",
    ]
    for pattern in enterotype_patterns:
        enterotype_match = re.search(pattern, search_text, re.IGNORECASE | re.MULTILINE)
        if enterotype_match:
            etype = enterotype_match.group(1)
            # 如果匹配到中文名，转换为类型字母
            if etype == "普雷沃菌属":
                etype = "P"
                desc = "普雷沃菌型"
            elif etype == "拟杆菌属":
                etype = "B"
                desc = "拟杆菌型"
            else:
                desc = "拟杆菌型" if etype.upper() == "B" else "普雷沃菌型" if etype.upper() == "P" else "混合型"
            indices.append({
                "name": "肠型",
                "result": f"{etype}型",
                "description": desc
            })
            break
        
    # B/E比值 - 双歧杆菌属/肠杆菌科比值
    # 首先尝试直接搜索B/E比值
    be_patterns = [
        r"B/E[比值]*[\s：:]+\s*([\d.]+)",
        r"B/E\s+([\d.]+)",
    ]
    
    be_value = None
    for pattern in be_patterns:
        be_match = re.search(pattern, search_text, re.IGNORECASE)
        if be_match:
            be_value = be_match.group(1)
            break
    
    # 如果没有直接匹配到B/E比值，尝试从有益菌/有害菌检测结果中计算
    if be_value is None:
        # 查找双歧杆菌属的百分比（格式：双歧杆菌属 Bifidobacterium 0.0006）
        bifidobacterium_match = re.search(r'双歧杆菌属\s+\S+\s+([\d.]+)', search_text)
        
        # 查找肠杆菌科各属的百分比并汇总（肠杆菌科包括：埃希氏菌属、志贺氏菌属、肠杆菌属等）
        enterobacteriaceae_value = 0.0
        enterobacteriaceae_patterns = [
            r"埃希氏菌-志贺氏菌[^%]*?([\d.]+)%",
            r"埃希氏菌属[^%]*?([\d.]+)%",
            r"志贺氏菌属[^%]*?([\d.]+)%",
            r"肠杆菌属\s+\S+\s+([\d.]+)",
            r"克雷伯氏菌属[^%]*?([\d.]+)%",
        ]
        
        for pattern in enterobacteriaceae_patterns:
            matches = re.findall(pattern, search_text)
            for match in matches:
                try:
                    val = float(match)
                    if val <= 50:  # 排除门级别数据
                        enterobacteriaceae_value += val
                except:
                    continue
        
        if bifidobacterium_match and enterobacteriaceae_value > 0:
            bifido_value = float(bifidobacterium_match.group(1))
            be_value = f"{bifido_value / enterobacteriaceae_value:.6f}"
    
    if be_value:
        indices.append({
            "name": "B/E比值",
            "result": be_value,
            "description": "双歧杆菌属/肠杆菌科比值，评估肠道健康状态"
        })
    
    return indices


def parse_phylum_distribution(text: str) -> list:
    """解析门级水平分布"""
    distribution = []
    
    # 优先匹配第11页的格式（包含中文名、拉丁名、百分比）
    # 格式：拟杆菌门（Bacteroidota, 39.11%），厚壁菌门（Firmicutes, 33.30%）
    page11_pattern = r"占比最高的五种菌门依次为：([\s\S]+?)(?=。|\n\n|$)"
    match_11 = re.search(page11_pattern, text, re.DOTALL)
    if match_11:
        section_text = match_11.group(1)
        # 清理换行符和多余空格以便更好地匹配
        section_text = section_text.replace('\n', '')
        section_text = re.sub(r'\s+', ' ', section_text)
        # 匹配格式：拟杆菌门（Bacteroidota, 39.11%）
        # 支持门名可能被分割的情况，过滤开头的逗号和空格
        phylum_pattern = r"[，,\s]*([^，,（\(\s]+?门)[（\(][^,]+,\s*([\d.]+)%[）\)]"
        matches = re.findall(phylum_pattern, section_text)
        for i, match in enumerate(matches, 1):
            name = match[0].strip()
            ratio = match[1]
            # 过滤无效名称
            if not name or len(name) < 3:
                continue
            if not name.endswith("门"):
                continue
            # 清理名称中的空格（处理"放线 菌门"这种情况）
            name = name.replace(' ', '')
            distribution.append({
                "rank": i,
                "name": name,
                "ratio": f"{ratio}%",
                "status": "正常"
            })
        return distribution
    
    # 备用模式：查找门级分布区域
    section_patterns = [
        r"门级?水平?分布.*?\n(.*?)(?=属级|属水平|有益菌|$)",
        r"2\.1.*?\n(.*?)(?=2\.2|$)",
    ]
    
    section_text = ""
    for pattern in section_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            section_text = match.group(1)
            break
    
    if section_text:
        lines = section_text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line or "菌门" in line and "占比" in line:
                continue
            
            # 匹配模式：拟杆菌门 39.11% 或 拟杆菌门: 39.11%
            match = re.match(r"(.+?门)[\s:：]+([\d.]+)%?\s*(.*)", line)
            if match:
                name = match.group(1).strip()
                ratio = match.group(2).strip()
                status = match.group(3).strip() or "正常"
                
                if not ratio.endswith('%'):
                    ratio += '%'
                
                distribution.append({
                    "name": name,
                    "ratio": ratio,
                    "status": status,
                })
    
    return distribution


def parse_genus_distribution(text: str) -> list:
    """解析属级水平分布Top15"""
    distribution = []
    
    # 优先匹配第12页的格式（包含中文名、拉丁名、百分比）
    # 支持多种变体，考虑页面编号格式："第12 页/共122 页"
    page12_patterns = [
        r"您其中占比最高的十五种菌属依次为：([\s\S]*?)(?=\。地址：|$)",
        r"占比最高的十五种菌属依次为：([\s\S]*?)(?=\。地址：|$)",
        r"十五种菌属依次为：([\s\S]*?)(?=\。地址：|$)",
        r"Top15.*?菌属.*?：([\s\S]*?)(?=\。地址：|$)",
        r"优势菌属.*?：([\s\S]*?)(?=\。地址：|$)",
        r"主要菌属.*?：([\s\S]*?)(?=\。地址：|$)",
        r"占比最高的十五种菌属：([\s\S]*?)(?=\。地址：|$)",
    ]
    
    for pattern_12_page in page12_patterns:
        match_12 = re.search(pattern_12_page, text, re.DOTALL)
        if match_12:
            section_text = match_12.group(1)

            section_text = section_text.replace('\n', ' ')

            genus_pattern = r"[，,\s、]*([^（\(\n]+?)\s*[（\(][^,]+,\s*([\d.]+)%[）\)]"
            matches = re.findall(genus_pattern, section_text)
            
            # 只有识别到5-50条数据时才认为是有效的（放宽条件）
            if 5 <= len(matches) <= 50:
                for i, match in enumerate(matches, 1):
                    chinese_name = match[0].strip()
                    ratio = match[1]
                    
                    # 过滤无效名称
                    if not chinese_name or len(chinese_name) < 2:
                        continue
                    if chinese_name.isdigit():
                        continue
                    
                    # 确定类别
                    beneficial = ['双歧杆菌属', '粪杆菌属', '罗斯氏菌属', '阿克曼菌属', '乳杆菌属']
                    harmful = ['梭杆菌属', '肠球菌属', '大肠杆菌属', '克雷伯菌属', '埃希氏菌-志贺氏菌']
                    
                    if any(h in chinese_name for h in harmful):
                        category = "有害菌"
                    elif any(b in chinese_name for b in beneficial):
                        category = "有益菌"
                    else:
                        category = "中性菌"
                    
                    distribution.append({
                        "rank": i,
                        "name": chinese_name,
                        "ratio": f"{ratio}%",
                        "category": category,
                    })
                
                return distribution
    
    # 如果第12页格式匹配失败或数据不足，返回空列表（使用默认数据）
    # 不再继续其他模式匹配，避免匹配到无效内容
    return distribution


def calculate_evaluation(result: str, ref_range: str, is_beneficial: bool = True) -> str:
    """根据检测结果和参考范围计算评价
    is_beneficial: True表示有益菌，False表示有害菌/中性菌
    """
    try:
        # 解析检测结果
        if result == "ND" or result == "未检出" or result == "低于检测限":
            # 有益菌未检出是偏低，有害菌未检出是正常
            return "偏低" if is_beneficial else "正常"
        
        # 去除百分号
        result_val = float(result.replace("%", ""))
        
        # 解析参考范围
        ref_range = ref_range.strip()
        if "-" in ref_range:
            parts = ref_range.split("-")
            if len(parts) == 2:
                min_ref = float(parts[0].strip())
                max_ref = float(parts[1].strip())
                
                if result_val < min_ref:
                    return "偏低" if is_beneficial else "正常"
                elif result_val > max_ref:
                    return "偏高"
                else:
                    return "正常"
            elif ref_range.startswith(">"):
                min_ref = float(ref_range[1:].strip())
                if result_val < min_ref:
                    return "偏低" if is_beneficial else "正常"
                else:
                    return "正常"
            elif ref_range.startswith("<"):
                max_ref = float(ref_range[1:].strip())
                if result_val > max_ref:
                    return "偏高"
                else:
                    return "正常"
        elif ref_range == "0":
            # 参考范围为0通常表示有害菌不应检出
            return "正常"
    except Exception as e:
        logger.warning(f"计算评价失败: result={result}, ref_range={ref_range}, error={e}")
    
    return ""


def calculate_neutral_evaluation(result: str, ref_range: str) -> str:
    """计算中性菌的评价：未检出、偏低、偏高都算异常"""
    try:
        if result == "ND" or result == "未检出" or result == "低于检测限":
            return "偏低"
        
        result_val = float(result.replace("%", ""))
        
        ref_range = ref_range.strip()
        if "-" in ref_range:
            parts = ref_range.split("-")
            if len(parts) == 2:
                min_ref = float(parts[0].strip())
                max_ref = float(parts[1].strip())
                
                if result_val < min_ref:
                    return "偏低"
                elif result_val > max_ref:
                    return "偏高"
                else:
                    return "正常"
        elif ref_range == "0":
            return "正常"
    except Exception as e:
        logger.warning(f"计算中性菌评价失败: result={result}, ref_range={ref_range}, error={e}")
    
    return ""


def parse_beneficial_bacteria(text: str) -> list:
    """解析有益菌检测（PDF第13-20页）"""
    bacteria = []
    
    # 提取第13-20页的内容
    page_pattern = r"----- 第(\d+)页 -----\n(.*?)(?=----- 第|$)"
    pages = re.findall(page_pattern, text, re.DOTALL)
    
    # 调试：打印所有找到的页码
    logger.info(f"有益菌解析 - 找到的所有页码: {[p[0] for p in pages]}")
    
    # 合并第13-20页的内容
    target_text = ""
    for page_num, page_content in pages:
        if 13 <= int(page_num) <= 20:
            target_text += page_content + "\n"
            logger.info(f"有益菌解析 - 已提取第{page_num}页内容，长度: {len(page_content)}")
    
    logger.info(f"有益菌解析 - 目标文本总长度: {len(target_text)}")
    
    # 调试：打印目标文本的前3000字符
    if target_text:
        logger.info(f"有益菌解析 - 目标文本预览:\n{target_text[:3000]}")
    
    # 查找有益菌相关区域（包含双歧杆菌属、乳杆菌属等有益菌属）
    section_patterns = [
        r"(双歧杆菌属[\s\S]*?)(?=\n\n|\Z)",
        r"(乳杆菌属[\s\S]*?)(?=\n\n|\Z)",
        r"(有益菌检测[\s\S]*?)(?=\n\n|\Z)",
        r"(3\.1.*?有益菌[\s\S]*?)(?=3\.2|有害菌|\n\n\n)",
    ]
    
    section_text = ""
    for i, pattern in enumerate(section_patterns):
        match = re.search(pattern, target_text, re.IGNORECASE)
        if match:
            section_text += match.group(0) + "\n"
            logger.info(f"有益菌解析 - 成功匹配模式{i+1}: {pattern[:30]}...")
            logger.info(f"有益菌解析 - 匹配到的区域长度: {len(section_text)}")
    
    if not section_text:
        logger.warning("有益菌解析 - 未找到有益菌区域，将使用默认数据")
        return bacteria
    
    # 调试：打印完整的区域内容
    logger.info(f"有益菌解析 - 提取到的区域完整内容:\n{section_text}")
    
    if section_text:
        lines = section_text.strip().split("\n")
        logger.info(f"有益菌解析 - 共解析到{len(lines)}行")
        
        # 调试：打印所有行
        for line_num, line in enumerate(lines):
            logger.info(f"有益菌解析 - 第{line_num}行原始内容: '{line.strip()}'")
        
        # 处理跨行数据：将拉丁名和微生物名合并
        merged_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # 如果当前行看起来是拉丁名（全英文），且下一行包含"菌"，则合并
            if re.match(r"^[A-Za-z]+(?:[-.][A-Za-z]+)*$", line) and i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if "菌" in next_line:
                    merged_lines.append(next_line + " " + line)
                    i += 2
                    continue
            
            merged_lines.append(line)
            i += 1
        
        logger.info(f"有益菌解析 - 合并后共{len(merged_lines)}行")
        
        for line_num, line in enumerate(merged_lines):
            line = line.strip()
            
            # 跳过表头和分隔线
            if not line or "菌名" in line or "结果" in line or "---" in line or "相对丰度" in line or "微生物名" in line or "拉丁名" in line or "检测结果" in line or "参考范围" in line or "地址：" in line or "报告编号" in line:
                logger.info(f"有益菌解析 - 第{line_num}行跳过（表头或空行）")
                continue
            
            # 匹配格式：菌属名 [拉丁名] 检测结果 参考范围 [结果评价]
            # 格式1：双歧杆菌属 Bifidobacterium 0.0006 0.0282-15.4602
            # 格式2：粪杆菌属 Faecalibacterium 2.3593 5.0000-15.0000
            pattern = r"(.+?菌属?)\s*(?:[\w.]+\s+)?([\d.]+|ND|未检出|低于检测限)\s+([\d.-]+(?:-[\d.]+)?)\s*([\u4e00-\u9fa5]+)?"
            
            match = re.match(pattern, line)
            if match:
                name = match.group(1).strip()
                result = match.group(2).strip()
                ref_range = match.group(3).strip()
                evaluation = match.group(4).strip() if match.group(4) else ""
                
                logger.info(f"有益菌解析 - 第{line_num}行匹配成功（原始）: name={name}, result={result}, ref_range={ref_range}, evaluation={evaluation}")
                
                # 如果OCR没有识别到评价，根据检测结果和参考范围计算
                if not evaluation:
                    evaluation = calculate_evaluation(result, ref_range, is_beneficial=True)
                    logger.info(f"有益菌解析 - 第{line_num}行计算评价: {evaluation}")
                
                # 只保留评价为偏低或偏高的记录
                if evaluation not in ("偏低", "偏高"):
                    logger.info(f"有益菌解析 - 第{line_num}行跳过（评价不是偏低/偏高）: {evaluation}")
                    continue
                
                # 转换ND为未检出
                if result == "ND":
                    result = "未检出"
                # 添加百分号
                if re.match(r"^[\d.]+$", result):
                    result = f"{result}%"
                
                bacteria.append({
                    "name": name,
                    "result": result,
                    "ref_range": ref_range,
                    "evaluation": evaluation,
                })
                logger.info(f"有益菌解析 - 第{line_num}行已添加: {name} | {result} | {ref_range} | {evaluation}")
                
                # 控制行数在10行
                if len(bacteria) >= 10:
                    logger.info(f"有益菌解析 - 已达到10行限制，停止解析")
                    break
            elif "菌" in line:
                logger.warning(f"有益菌解析 - 第{line_num}行未匹配正则: {line}")
            else:
                logger.info(f"有益菌解析 - 第{line_num}行跳过（不含菌）: {line[:50]}")
    
    logger.info(f"有益菌解析 - 最终提取到{len(bacteria)}条有益菌数据（仅偏低/偏高）")
    for idx, b in enumerate(bacteria):
        logger.info(f"有益菌解析 - 结果[{idx}]: {b['name']} | {b['result']} | {b['ref_range']} | {b['evaluation']}")
    
    return bacteria


def parse_harmful_bacteria(text: str) -> list:
    """解析有害菌/中性菌检测（PDF第13-20页）"""
    bacteria = []
    
    # 有害菌和中性菌列表
    harmful_and_neutral_genera = [
        "产气荚膜梭菌", "肉毒梭菌", "沙门菌属", "大肠埃希菌", "肺炎克雷伯菌",
        "单核细胞增生李斯特菌", "克罗诺杆菌属", "艰难梭菌", "金黄色葡萄球菌",
        "铜绿假单胞菌", "鲍曼不动杆菌", "肠球菌属", "链球菌属", "葡萄球菌属",
        "肠杆菌属", "克雷伯氏菌属", "柠檬酸杆菌属", "沙雷氏菌属", "变形杆菌属",
        "摩根菌属", "普罗威登斯菌属", "假单胞菌属", "不动杆菌属", "放线菌属",
        "梭杆菌属", "韦荣球菌属", "嗜胆菌属", "脱硫弧菌属", "萨特氏菌属",
        "粪芽孢菌属", "真杆菌属", "毛梭菌属", "罗斯氏菌属", "考拉杆菌属"
    ]
    
    # 提取第13-20页的内容
    page_pattern = r"----- 第(\d+)页 -----\n(.*?)(?=----- 第|$)"
    pages = re.findall(page_pattern, text, re.DOTALL)
    
    # 调试：打印所有找到的页码
    logger.info(f"有害菌解析 - 找到的所有页码: {[p[0] for p in pages]}")
    
    # 合并第13-20页的内容
    target_text = ""
    for page_num, page_content in pages:
        if 13 <= int(page_num) <= 20:
            target_text += page_content + "\n"
            logger.info(f"有害菌解析 - 已提取第{page_num}页内容，长度: {len(page_content)}")
    
    logger.info(f"有害菌解析 - 目标文本总长度: {len(target_text)}")
    
    # 调试：打印目标文本的前3000字符
    if target_text:
        logger.info(f"有害菌解析 - 目标文本预览:\n{target_text[:3000]}")
    
    # 分别查找有害菌和中性菌区域
    # 查找有害菌区域（10.4）
    harmful_pattern = r"10\.4.*?有害菌[\s\S]*?(?=10\.5|注：|\n\n\n)"
    harmful_section = ""
    match = re.search(harmful_pattern, target_text, re.IGNORECASE)
    if match:
        harmful_section = match.group(0) + "\n"
        logger.info(f"有害菌解析 - 成功匹配有害菌区域，长度: {len(harmful_section)}")
    
    # 查找中性菌区域（10.5）
    neutral_pattern = r"10\.5.*?中性菌[\s\S]*?(?=\n\n\n|\Z)"
    neutral_section = ""
    match = re.search(neutral_pattern, target_text, re.IGNORECASE)
    if match:
        neutral_section = match.group(0) + "\n"
        logger.info(f"有害菌解析 - 成功匹配中性菌区域，长度: {len(neutral_section)}")
    
    # 如果没有找到分开的区域，尝试其他模式
    if not harmful_section and not neutral_section:
        logger.info("有害菌解析 - 未找到10.4和10.5区域，尝试其他模式")
        section_patterns = [
            r"有害菌[/／]中性菌检测[\s\S]*?(?=\n\n|\Z)",
            r"有害菌[/／]致病菌检测[\s\S]*?(?=\n\n|\Z)",
            r"中性菌检测[\s\S]*?(?=\n\n|\Z)",
            r"产气荚膜梭菌[\s\S]*?(?=\n\n|\Z)",
            r"3\.2.*?有害菌[\s\S]*?(?=3\.3|B/E|\n\n\n)",
        ]
        for i, pattern in enumerate(section_patterns):
            match = re.search(pattern, target_text, re.IGNORECASE)
            if match:
                harmful_section += match.group(0) + "\n"
                logger.info(f"有害菌解析 - 成功匹配模式{i+1}: {pattern[:30]}...")
    
    # 如果没找到区域，使用默认数据
    if not harmful_section and not neutral_section:
        logger.warning("有害菌解析 - 未找到有害菌/中性菌区域，将使用默认数据")
        return bacteria
    
    # 定义一个处理区域的函数
    def process_section(section_text: str, is_neutral: bool = False):
        """处理单个区域的文本，is_neutral=True表示中性菌"""
        section_bacteria = []
        
        if not section_text:
            return section_bacteria
        
        lines = section_text.strip().split("\n")
        logger.info(f"有害菌解析 - {'中性菌' if is_neutral else '有害菌'}区域共解析到{len(lines)}行")
        
        # 调试：打印所有行
        for line_num, line in enumerate(lines):
            logger.info(f"有害菌解析 - 第{line_num}行原始内容: '{line.strip()}'")
        
        # 处理跨行数据：将拉丁名和微生物名合并
        merged_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # 如果当前行看起来是拉丁名（全英文），且下一行包含"菌"，则合并
            if re.match(r"^[A-Za-z]+(?:[-.][A-Za-z]+)*$", line) and i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if "菌" in next_line:
                    merged_lines.append(next_line + " " + line)
                    i += 2
                    continue
            
            merged_lines.append(line)
            i += 1
        
        logger.info(f"有害菌解析 - {'中性菌' if is_neutral else '有害菌'}区域合并后共{len(merged_lines)}行")
        
        for line_num, line in enumerate(merged_lines):
            line = line.strip()
            
            # 跳过表头、分隔线、地址和报告编号
            if not line or "菌名" in line or "结果" in line or "---" in line or "检测结果" in line or "参考范围" in line or "地址：" in line or "报告编号" in line or "注：" in line or "10.4" in line or "10.5" in line:
                logger.info(f"有害菌解析 - 第{line_num}行跳过（表头或空行）")
                continue
            
            # 匹配格式：菌属名 [拉丁名] 检测结果 参考范围 [结果评价]
            pattern = r"(.+?菌属?)\s*(?:[\w.]+\s+)?([\d.]+|ND|未检出|检出)\s+([\d.-]+(?:-[\d.]+)?)\s*([\u4e00-\u9fa5]+)?"
            
            match = re.match(pattern, line)
            if match:
                name = match.group(1).strip()
                result = match.group(2).strip()
                ref_range = match.group(3).strip()
                evaluation = match.group(4).strip() if match.group(4) else ""
                
                logger.info(f"有害菌解析 - 第{line_num}行匹配成功（{'中性菌' if is_neutral else '有害菌'}）: name={name}, result={result}, ref_range={ref_range}, evaluation={evaluation}")
                
                # 如果OCR没有识别到评价，根据检测结果和参考范围计算
                if not evaluation:
                    if is_neutral:
                        # 中性菌：未检出、偏低、偏高都算异常
                        evaluation = calculate_neutral_evaluation(result, ref_range)
                    else:
                        # 有害菌：只有偏高算异常
                        evaluation = calculate_evaluation(result, ref_range, is_beneficial=False)
                    logger.info(f"有害菌解析 - 第{line_num}行计算评价: {evaluation}")
                
                # 保留异常记录
                if evaluation in ("偏低", "偏高", "异常"):
                    # 转换ND为未检出
                    if result == "ND":
                        result = "未检出"
                    # 添加百分号
                    if re.match(r"^[\d.]+$", result):
                        result = f"{result}%"
                    
                    section_bacteria.append({
                        "name": name,
                        "result": result,
                        "ref_range": ref_range,
                        "evaluation": evaluation,
                    })
                    logger.info(f"有害菌解析 - 第{line_num}行已添加: {name} | {result} | {ref_range} | {evaluation}")
                else:
                    logger.info(f"有害菌解析 - 第{line_num}行跳过（评价不是异常）: {evaluation}")
            elif "菌" in line:
                logger.warning(f"有害菌解析 - 第{line_num}行未匹配正则: {line}")
            else:
                logger.info(f"有害菌解析 - 第{line_num}行跳过（不含菌）: {line[:50]}")
        
        return section_bacteria
    
    # 先处理中性菌区域（因为中性菌更可能有异常）
    neutral_bacteria = process_section(neutral_section, is_neutral=True)
    bacteria.extend(neutral_bacteria)
    
    # 然后处理有害菌区域
    harmful_bacteria = process_section(harmful_section, is_neutral=False)
    bacteria.extend(harmful_bacteria)
    
    # 控制总条数在10行
    bacteria = bacteria[:10]
    
    logger.info(f"有害菌解析 - 最终提取到{len(bacteria)}条有害菌/中性菌数据（仅偏低/偏高）")
    for idx, b in enumerate(bacteria):
        logger.info(f"有害菌解析 - 结果[{idx}]: {b['name']} | {b['result']} | {b['ref_range']} | {b['evaluation']}")
    
    return bacteria


def parse_be_ratio(text: str) -> dict:
    """解析B/E比值详情（双歧杆菌属/肠杆菌科）"""
    ratio_data = {}
    
    # 首先尝试直接搜索B/E比值
    be_match = re.search(r"B/E[比值]*[：:]?\s*([\d.]+)", text, re.IGNORECASE)
    if be_match:
        ratio_data["value"] = be_match.group(1)
    
    # 如果没有直接找到，从有益菌和有害菌数据中计算
    if not ratio_data.get("value"):
        # 提取双歧杆菌属的值（从有益菌检测部分）
        bifidobacterium_match = re.search(r"双歧杆菌属\s+Bifidobacterium\s+([\d.]+)", text)
        bifidobacterium_value = 0.0
        if bifidobacterium_match:
            try:
                bifidobacterium_value = float(bifidobacterium_match.group(1))
                ratio_data["bifidobacterium"] = bifidobacterium_match.group(1)
            except:
                pass
        
        # 提取肠杆菌科的值 - 需要汇总所有肠杆菌科属
        # 肠杆菌科包括：埃希氏菌属、志贺氏菌属、肠杆菌属、克雷伯氏菌属、柠檬酸杆菌属等
        # 注意：排除变形菌门（Proteobacteria），只匹配属级别
        enterobacteriaceae_value = 0.0
        enterobacteriaceae_genera = [
            r"埃希氏菌-志贺氏菌[^%]*?([\d.]+)%",  # 埃希氏菌-志贺氏菌复合属
            r"埃希氏菌属[^%]*?([\d.]+)%",         # 埃希氏菌属
            r"志贺氏菌属[^%]*?([\d.]+)%",         # 志贺氏菌属
            r"肠杆菌属\s+Enterobacter\s+([\d.]+)",  # 肠杆菌属
            r"克雷伯氏菌属[^%]*?([\d.]+)%",       # 克雷伯氏菌属
            r"柠檬酸杆菌属[^%]*?([\d.]+)%",       # 柠檬酸杆菌属
            r"沙雷氏菌属[^%]*?([\d.]+)%",         # 沙雷氏菌属
        ]
        
        found_values = []
        for pattern in enterobacteriaceae_genera:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    val = float(match)
                    # 排除大于50%的值（可能是门级别的数据）
                    if val <= 50:
                        enterobacteriaceae_value += val
                        found_values.append(val)
                except:
                    continue
        
        if found_values:
            ratio_data["enterobacteriaceae"] = str(enterobacteriaceae_value)
        
        # 计算B/E比值
        if bifidobacterium_value > 0 and enterobacteriaceae_value > 0:
            be_ratio = bifidobacterium_value / enterobacteriaceae_value
            ratio_data["value"] = str(round(be_ratio, 6))
    
    # 添加参考范围
    ratio_data["normal_range"] = ">1"
    
    # 根据比值给出评估
    if ratio_data.get("value"):
        try:
            be_val = float(ratio_data["value"])
            if be_val >= 1:
                ratio_data["assessment"] = "正常"
            elif be_val >= 0.1:
                ratio_data["assessment"] = "中度受损"
            else:
                ratio_data["assessment"] = "重度受损"
        except:
            ratio_data["assessment"] = "未知"
    
    return ratio_data


def parse_disease_risk(text: str) -> dict:
    """解析疾病风险评估"""
    risk = {}
    
    patterns = {
        "metabolic": r"代谢综合征风险[：:]?\s*(.+?)(?:\n|$)",
        "inflammation": r"肠道炎症风险[：:]?\s*(.+?)(?:\n|$)",
        "cardiovascular": r"心脑血管风险[：:]?\s*(.+?)(?:\n|$)",
        "overall": r"总体评估[：:]?\s*(.+?)(?:\n|$)",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            risk[key] = match.group(1).strip()
    
    return risk


def parse_metabolism(text: str) -> list:
    """解析物质代谢与营养素评估"""
    items = []
    
    section_match = re.search(r"4\.2\s*物质代谢.*?\n(.*?)(?=4\.3|肠道屏障|$)", text, re.DOTALL | re.IGNORECASE)
    if section_match:
        section_text = section_match.group(1)
        lines = section_text.strip().split("\n")
        for line in lines:
            line = line.strip().lstrip("•·●-* ")
            if "：" in line or ":" in line:
                parts = re.split(r"[：:]", line, 1)
                if len(parts) == 2:
                    items.append({
                        "name": parts[0].strip(),
                        "result": parts[1].strip(),
                    })
    
    return items


def parse_barrier_function(text: str) -> list:
    """解析肠道屏障功能评估"""
    items = []
    
    section_match = re.search(r"4\.3\s*肠道屏障.*?\n(.*?)(?=5\s|精准评估|$)", text, re.DOTALL | re.IGNORECASE)
    if section_match:
        section_text = section_match.group(1)
        lines = section_text.strip().split("\n")
        for line in lines:
            line = line.strip().lstrip("•·●-* ")
            if "：" in line or ":" in line:
                parts = re.split(r"[：:]", line, 1)
                if len(parts) == 2:
                    items.append({
                        "name": parts[0].strip(),
                        "result": parts[1].strip(),
                    })
    
    return items


def parse_ai_conclusion(text: str) -> str:
    """解析AI智能解读结论"""
    match = re.search(r"5\.1\s*AI.*?结论.*?\n(.*?)(?=5\.2|饮食调节|$)", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def parse_diet_advice(text: str) -> list:
    """解析饮食调节建议"""
    items = []
    
    section_match = re.search(r"5\.2\s*饮食调节.*?\n(.*?)(?=5\.3|益生菌|$)", text, re.DOTALL | re.IGNORECASE)
    if section_match:
        section_text = section_match.group(1)
        lines = section_text.strip().split("\n")
        for line in lines:
            line = line.strip().lstrip("•·●-* ")
            if line and len(line) > 5:
                items.append(line)
    
    return items


def parse_probiotic_advice(text: str) -> list:
    """解析益生菌补充建议"""
    items = []
    
    section_match = re.search(r"5\.3\s*益生菌.*?\n(.*?)(?=5\.4|运动|$)", text, re.DOTALL | re.IGNORECASE)
    if section_match:
        section_text = section_match.group(1)
        lines = section_text.strip().split("\n")
        for line in lines:
            line = line.strip().lstrip("•·●-* ")
            if line and len(line) > 5:
                items.append(line)
    
    return items


def parse_lifestyle_advice(text: str) -> list:
    """解析运动与生活方式建议"""
    items = []
    
    section_match = re.search(r"5\.4\s*运动.*?\n(.*?)(?=6\s|干预|$)", text, re.DOTALL | re.IGNORECASE)
    if section_match:
        section_text = section_match.group(1)
        lines = section_text.strip().split("\n")
        for line in lines:
            line = line.strip().lstrip("•·●-* ")
            if line and len(line) > 5:
                items.append(line)
    
    return items


def parse_intervention_plan(text: str) -> dict:
    """解析干预随访计划"""
    plan = {"phase1": [], "phase2": [], "phase3": []}
    
    # 第一阶段
    phase1_match = re.search(r"第一阶段[：:]?.*?\n(.*?)(?=第二阶段|$)", text, re.DOTALL | re.IGNORECASE)
    if phase1_match:
        lines = phase1_match.group(1).strip().split("\n")
        for line in lines:
            line = re.sub(r"^\d+\s*", "", line.strip())
            if line:
                plan["phase1"].append(line)
    
    # 第二阶段
    phase2_match = re.search(r"第二阶段[：:]?.*?\n(.*?)(?=第三阶段|$)", text, re.DOTALL | re.IGNORECASE)
    if phase2_match:
        lines = phase2_match.group(1).strip().split("\n")
        for line in lines:
            line = re.sub(r"^\d+\s*", "", line.strip())
            if line:
                plan["phase2"].append(line)
    
    # 第三阶段
    phase3_match = re.search(r"第三阶段[：:]?.*?\n(.*?)(?=7\s|科普|$)", text, re.DOTALL | re.IGNORECASE)
    if phase3_match:
        lines = phase3_match.group(1).strip().split("\n")
        for line in lines:
            line = re.sub(r"^\d+\s*", "", line.strip())
            if line:
                plan["phase3"].append(line)
    
    return plan
