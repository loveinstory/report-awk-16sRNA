#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""肠道菌群检测报告生成器 - 第2版"""

import os
import math
import re
from weasyprint import HTML

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

# 环形图颜色方案（从深绿到浅绿渐变）
DONUT_COLORS = [
    "#1a5c4b", "#2B6B5E", "#3A9D7C", "#4CAF50", "#66BB6A",
    "#81C784", "#A5D6A7", "#B2DFDB", "#C8E6C9", "#DCEDC8"
]


def read_template(filename):
    """读取HTML模板文件"""
    path = os.path.join(TEMPLATE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_status_label(value_text, desc_text=""):
    """根据文本判断状态标签和样式类"""
    combined = f"{value_text} {desc_text}"
    
    if "优" in combined or "良好" in combined or "理想" in combined:
        return '<span class="result-tag result-good">良好</span>'
    elif "中" in combined or "一般" in combined or "中等" in combined:
        return '<span class="result-tag result-fair">中等</span>'
    elif "低" in combined or "差" in combined or "需关注" in combined or "低于" in combined:
        return '<span class="result-tag result-poor">需关注</span>'
    return ""


def build_page1(data):
    """构建封面页HTML"""
    html = read_template("page1_cover.html")
    
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    
    # 基本信息
    basic_info = data.get("basic_info", {})
    name = basic_info.get("name", "匿名用户")
    gender = basic_info.get("gender", "")
    age = basic_info.get("age", "")
    phone = basic_info.get("phone", "")
    symptoms = basic_info.get("symptoms", "")
    
    # 检测信息
    test_info = data.get("test_info", {})
    unit = test_info.get("unit", "")
    sample_id = test_info.get("sample_id", "")
    sample_type = test_info.get("sample_type", "")
    sample_date = test_info.get("sample_date", "")
    method = test_info.get("method", "")
    
    # 生成报告ID和日期
    import time
    report_id = f"GMB-{int(time.time())}"
    report_date = time.strftime("%Y年%m月%d日")
    
    replacements = {
        "{{name}}": name,
        "{{gender}}": gender,
        "{{age}}": age,
        "{{phone}}": phone,
        "{{symptoms}}": symptoms,
        "{{unit}}": unit,
        "{{sample_id}}": sample_id,
        "{{sample_type}}": sample_type,
        "{{sample_date}}": sample_date,
        "{{method}}": method,
        "{{report_id}}": report_id,
        "{{report_date}}": report_date,
        "{{logo_w_image}}": "file:///" + os.path.join(templates_dir, "logo-w.png").replace("\\", "/"),
        "{{logo02_image}}": "file:///" + os.path.join(templates_dir, "logo02.png").replace("\\", "/"),
    }
    
    for key, val in replacements.items():
        html = html.replace(key, val)
    
    return html


def build_page2(data):
    """构建核心指标页HTML"""
    html = read_template("page2_indices.html")
    
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    
    # 核心指标
    core_indices = data.get("core_indices", [])
    
    # GMHI评分
    gmhi_score = "0"
    gmhi_label = "偏低"
    gmhi_desc = "肠道微生态平衡度一般，建议改善生活方式并关注肠道健康。"
    gmhi_label_class = "label-low"
    
    for idx in core_indices:
        if "GMHI" in idx.get("name", ""):
            gmhi_score = idx.get("result", "0")
            # 根据GMHI值确定等级
            try:
                score_val = float(gmhi_score)
                if score_val >= 70:
                    gmhi_label = "正常"
                    gmhi_desc = "肠道微生态平衡度良好，继续保持健康生活方式。"
                    gmhi_label_class = "label-normal"
                elif score_val >= 60:
                    gmhi_label = "基本健康"
                    gmhi_desc = "肠道微生态基本平衡，建议保持健康饮食习惯。"
                    gmhi_label_class = "label-normal"
                elif score_val >= 40:
                    gmhi_label = "偏低"
                    gmhi_desc = "肠道微生态平衡度一般，建议改善生活方式并关注肠道健康。"
                    gmhi_label_class = "label-low"
                else:
                    gmhi_label = "危险"
                    gmhi_desc = "肠道微生态严重失衡，建议尽快咨询医生进行专业干预。"
                    gmhi_label_class = "label-danger"
            except:
                gmhi_label = "未知"
                gmhi_label_class = "label-low"
            break
    
    # 计算仪表盘参数
    try:
        gmhi_val = float(gmhi_score)
        # 仪表盘角度计算 (0-180度对应0-100分)
        angle = (gmhi_val / 100) * 180
        radian = (angle - 180) * 3.14159 / 180
        gauge_end_x = 100 + 80 * 3.14159 / 180 * radian
        gauge_end_y = 105 + 80 * 3.14159 / 180 * radian
        # 指针位置
        pointer_angle = (gmhi_val / 100) * 180 - 180
        pointer_radian = pointer_angle * 3.14159 / 180
        pointer_length = 50
        pointer_x = 100
        pointer_y = 105
        pointer_x1 = pointer_x + pointer_length * 3.14159 / 180 * pointer_radian
        pointer_y1 = pointer_y + pointer_length * 3.14159 / 180 * pointer_radian
        # 指针宽度
        pointer_width = 4
        pointer_x2 = pointer_x + pointer_width
        pointer_y2 = pointer_y + pointer_width
        # 仪表盘颜色
        if gmhi_val >= 70:
            gauge_color = "#4CAF50"
        elif gmhi_val >= 40:
            gauge_color = "#E8833A"
        else:
            gauge_color = "#E53935"
    except:
        gauge_end_x = 20
        gauge_end_y = 105
        pointer_x = pointer_y = pointer_x1 = pointer_y1 = pointer_x2 = pointer_y2 = 100
        gauge_color = "#e8e8e8"
    
    # 菌群多样性
    diversity_value = "0"
    diversity_label = "正常"
    diversity_label_class = "label-normal"
    for idx in core_indices:
        if "多样性" in idx.get("name", ""):
            diversity_value = idx.get("result", "0")
            # 根据值确定等级
            if diversity_value == "偏低":
                diversity_label = "偏低"
                diversity_label_class = "label-low"
            elif diversity_value == "偏高":
                diversity_label = "偏高"
                diversity_label_class = "label-high"
            else:
                diversity_label = "正常"
                diversity_label_class = "label-normal"
            break
    
    # 肠道年龄
    gut_age = "42"
    real_age = data.get("basic_info", {}).get("age", "35")
    age_label = "正常"
    age_label_class = "label-normal"
    for idx in core_indices:
        if "肠道年龄" in idx.get("name", ""):
            gut_age_str = idx.get("result", "42岁")
            gut_age = gut_age_str.replace("岁", "")
            # 计算肠道年龄差异
            try:
                gut_age_val = int(gut_age)
                real_age_val = int(real_age)
                diff = gut_age_val - real_age_val
                if diff >= 7:
                    age_label = f"偏大{diff}岁"
                    age_label_class = "label-high"
                elif diff <= -5:
                    age_label = f"偏小{abs(diff)}岁"
                    age_label_class = "label-low"
                else:
                    age_label = "正常"
                    age_label_class = "label-normal"
            except:
                age_label = "正常"
                age_label_class = "label-normal"
            break
    
    # 肠型
    enterotype = "B型"
    enterotype_desc = "拟杆菌型"
    enterotype_label = "拟杆菌型"
    enterotype_label_class = "label-normal"
    for idx in core_indices:
        if "肠型" in idx.get("name", ""):
            etype = idx.get("result", "B型")
            enterotype = etype
            if etype.startswith("P") or "普雷沃菌" in etype:
                enterotype = "P型"
                enterotype_desc = "普雷沃菌型"
                enterotype_label = "普雷沃菌型"
            elif etype.startswith("B") or "拟杆菌" in etype:
                enterotype = "B型"
                enterotype_desc = "拟杆菌型"
                enterotype_label = "拟杆菌型"
            else:
                enterotype_desc = "混合型"
                enterotype_label = "混合型"
            break
    
    # B/E比值（双歧杆菌属/肠杆菌科）
    be_ratio = data.get("be_ratio", {})
    be_value = be_ratio.get("value", "1.5")
    be_assessment = be_ratio.get("assessment", "正常")
    be_label = be_assessment
    be_label_class = "label-normal"
    
    try:
        be_val = float(be_value)
        if be_val >= 1:
            be_label = "正常"
            be_label_class = "label-normal"
        elif be_val >= 0.1:
            be_label = "中度受损"
            be_label_class = "label-low"
        else:
            be_label = "重度受损"
            be_label_class = "label-danger"
    except:
        be_label = "正常"
        be_label_class = "label-normal"
    
    # 构建指标表格行
    indices_rows = ""
    # 添加GMHI评分
    indices_rows += f'''<tr>
        <td>GMHI评分</td>
        <td>{gmhi_score}/100</td>
        <td>综合反映肠道微生态整体健康状况</td>
        <td><span class="status-tag {gmhi_label_class}">{gmhi_label}</span></td>
    </tr>'''
    # 添加菌群多样性
    indices_rows += f'''<tr>
        <td>菌群多样性 (Shannon指数)</td>
        <td>{diversity_value}</td>
        <td>数值越高，菌群多样性越好</td>
        <td><span class="status-tag {diversity_label_class}">{diversity_label}</span></td>
    </tr>'''
    # 添加肠道年龄
    indices_rows += f'''<tr>
        <td>肠道年龄</td>
        <td>{gut_age}岁</td>
        <td>肠道年龄与实际年龄的比较</td>
        <td><span class="status-tag {age_label_class}">{age_label}</span></td>
    </tr>'''
    # 添加B/E比值
    indices_rows += f'''<tr>
        <td>B/E比值</td>
        <td>{be_value}</td>
        <td>双歧杆菌属/肠杆菌科比值，参考范围>1</td>
        <td><span class="status-tag {be_label_class}">{be_label}</span></td>
    </tr>'''
    # 添加其他指标
    for idx in core_indices:
        name = idx.get("name", "")
        result = idx.get("result", "")
        description = idx.get("description", "")
        
        # 跳过已处理的指标
        if "GMHI" in name or "多样性" in name or "肠道年龄" in name or "B/E" in name or "肠型" in name:
            continue
        
        # 确定状态
        status = "normal"
        status_label = "正常"
        if "偏低" in result or "不足" in result:
            status = "low"
            status_label = "偏低"
        elif "偏高" in result or "过度" in result:
            status = "high"
            status_label = "偏高"
        elif "受损" in result or "异常" in result:
            status = "danger"
            status_label = "异常"
        
        indices_rows += f'''<tr>
            <td>{name}</td>
            <td>{result}</td>
            <td>{description}</td>
            <td><span class="status-tag tag-{status}">{status_label}</span></td>
        </tr>'''
    
    # 门级分布条形图
    phylum_bars = ""
    phylum_data = data.get("phylum_distribution", [])
    if not phylum_data:
        phylum_data = [
            {"name": "拟杆菌门", "ratio": "60.2%"},
            {"name": "厚壁菌门", "ratio": "30.5%"},
            {"name": "放线菌门", "ratio": "5.3%"},
            {"name": "变形菌门", "ratio": "2.8%"},
            {"name": "梭杆菌门", "ratio": "1.2%"},
        ]
    
    for phylum in phylum_data:
        name = phylum.get("name", "")
        ratio_str = phylum.get("ratio", "0%")
        try:
            ratio = float(ratio_str.replace("%", ""))
        except:
            ratio = 0
        phylum_bars += f'''<div class="bar-item">
            <div class="bar-label">{name}</div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{ratio}%"></div>
            </div>
            <div class="bar-value">{ratio_str}</div>
        </div>'''
    
    # 属级分布条形图
    genus_bars = ""
    genus_data = data.get("genus_distribution", [])
    
    # 过滤无效数据
    filtered_genus = []
    for item in genus_data:
        name = item.get("name", "").strip()
        ratio_str = item.get("ratio", "0%").strip()
        
        # 过滤条件
        if not name or len(name) < 2:
            continue
        if name.isdigit():
            continue
        
        try:
            ratio_val = float(ratio_str.replace("%", ""))
        except:
            continue
        
        if ratio_val <= 0:
            continue
        
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in name)
        if not has_chinese:
            continue
        
        filtered_genus.append(item)
    
    # 如果过滤后没有数据，使用默认数据
    if not filtered_genus:
        filtered_genus = [
            {"name": "普雷沃菌属", "ratio": "26.90%"},
            {"name": "拟杆菌属", "ratio": "10.21%"},
            {"name": "粪杆菌属", "ratio": "8.56%"},
            {"name": "双歧杆菌属", "ratio": "6.32%"},
            {"name": "罗斯氏菌属", "ratio": "5.89%"},
            {"name": "瘤胃球菌属", "ratio": "4.45%"},
            {"name": "毛螺菌属", "ratio": "3.21%"},
            {"name": "梭菌属", "ratio": "2.87%"},
        ]
    
    # 最多显示15条
    filtered_genus = filtered_genus[:15]
    
    for genus in filtered_genus:
        name = genus.get("name", "")
        ratio_str = genus.get("ratio", "0%")
        try:
            ratio = float(ratio_str.replace("%", ""))
        except:
            ratio = 0
        genus_bars += f'''<div class="bar-item">
            <div class="bar-label">{name}</div>
            <div class="bar-track">
                <div class="bar-fill-genus" style="width:{ratio}%"></div>
            </div>
            <div class="bar-value">{ratio_str}</div>
        </div>'''
    
    replacements = {
        "{{logo_w_image}}": "file:///" + os.path.join(templates_dir, "logo-w.png").replace("\\", "/"),
        "{{gmhi_score}}": gmhi_score,
        "{{gmhi_label}}": gmhi_label,
        "{{gmhi_desc}}": gmhi_desc,
        "{{gmhi_label_class}}": gmhi_label_class,
        "{{gauge_end_x}}": f"{gauge_end_x:.2f}",
        "{{gauge_end_y}}": f"{gauge_end_y:.2f}",
        "{{gauge_color}}": gauge_color,
        "{{pointer_x}}": str(pointer_x),
        "{{pointer_y}}": str(pointer_y),
        "{{pointer_x1}}": f"{pointer_x1:.2f}",
        "{{pointer_y1}}": f"{pointer_y1:.2f}",
        "{{pointer_x2}}": str(pointer_x2),
        "{{pointer_y2}}": str(pointer_y2),
        "{{diversity_value}}": diversity_value,
        "{{diversity_label}}": diversity_label,
        "{{diversity_label_class}}": diversity_label_class,
        "{{gut_age}}": gut_age,
        "{{real_age}}": real_age,
        "{{age_label}}": age_label,
        "{{age_label_class}}": age_label_class,
        "{{enterotype}}": enterotype,
        "{{enterotype_desc}}": enterotype_desc,
        "{{enterotype_label}}": enterotype_label,
        "{{enterotype_label_class}}": enterotype_label_class,
        "{{be_value}}": be_value,
        "{{be_label}}": be_label,
        "{{be_label_class}}": be_label_class,
        "{{indices_rows}}": indices_rows,
        "{{phylum_bars}}": phylum_bars,
        "{{genus_bars}}": genus_bars,
    }
    
    for key, val in replacements.items():
        html = html.replace(key, val)
    
    return html


def build_page3(data):
    """构建菌群组成分析页HTML"""
    html = read_template("page3_composition.html")
    genus_data = data.get("genus_distribution", [])
    beneficial = data.get("beneficial_bacteria", [])
    harmful = data.get("harmful_bacteria", [])
    be_ratio = data.get("be_ratio", {})
    
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    
    # 过滤无效数据
    genus = []
    for item in genus_data:
        name = item.get("name", "").strip()
        ratio_str = item.get("ratio", "0%").strip()
        
        if not name or len(name) < 2:
            continue
        if name.isdigit():
            continue
        
        try:
            ratio_val = float(ratio_str.replace("%", ""))
        except:
            continue
        
        if ratio_val <= 0:
            continue
        
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in name)
        if not has_chinese:
            continue
        
        genus.append(item)
    
    # 如果没有数据，使用默认数据
    if not genus:
        genus = [
            {"rank": 1, "name": "普雷沃菌属", "ratio": "26.90%", "category": "中性菌"},
            {"rank": 2, "name": "拟杆菌属", "ratio": "13.32%", "category": "中性菌"},
            {"rank": 3, "name": "粪杆菌属", "ratio": "8.56%", "category": "有益菌"},
            {"rank": 4, "name": "双歧杆菌属", "ratio": "6.32%", "category": "有益菌"},
            {"rank": 5, "name": "罗斯氏菌属", "ratio": "5.89%", "category": "有益菌"},
            {"rank": 6, "name": "瘤胃球菌属", "ratio": "4.45%", "category": "中性菌"},
            {"rank": 7, "name": "毛螺菌属", "ratio": "3.21%", "category": "中性菌"},
            {"rank": 8, "name": "梭菌属", "ratio": "2.87%", "category": "中性菌"},
            {"rank": 9, "name": "乳杆菌属", "ratio": "2.34%", "category": "有益菌"},
            {"rank": 10, "name": "阿克曼菌属", "ratio": "1.98%", "category": "有益菌"},
        ]
    
    # 最多显示10条（环形图只显示Top 10）
    genus = genus[:10]

    # 构建环形图（SVG）
    total_ratio = sum(float(g.get("ratio", "0").replace("%", "")) for g in genus)
    top10_ratio = f"{total_ratio:.2f}%"
    
    donut_svg = f'''<svg viewBox="0 0 200 200" width="180" height="180" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)">'''

    # 绘制环形图扇区
    start_angle = -90
    for i, g in enumerate(genus):
        try:
            ratio_val = float(g.get("ratio", "0").replace("%", ""))
        except:
            ratio_val = 0
        sweep = ratio_val / total_ratio * 360 if total_ratio > 0 else 0
        color = DONUT_COLORS[i % len(DONUT_COLORS)]

        # 计算SVG弧线
        end_angle = start_angle + sweep
        large_arc = 1 if sweep > 180 else 0

        r_outer = 90
        r_inner = 55
        cx, cy = 100, 100

        # 外弧起点终点
        x1_o = cx + r_outer * math.cos(math.radians(start_angle))
        y1_o = cy + r_outer * math.sin(math.radians(start_angle))
        x2_o = cx + r_outer * math.cos(math.radians(end_angle))
        y2_o = cy + r_outer * math.sin(math.radians(end_angle))
        # 内弧起点终点
        x1_i = cx + r_inner * math.cos(math.radians(end_angle))
        y1_i = cx + r_inner * math.sin(math.radians(end_angle))
        x2_i = cx + r_inner * math.cos(math.radians(start_angle))
        y2_i = cx + r_inner * math.sin(math.radians(start_angle))

        path = f"M {x1_o:.1f} {y1_o:.1f} A {r_outer} {r_outer} 0 {large_arc} 1 {x2_o:.1f} {y2_o:.1f} L {x1_i:.1f} {y1_i:.1f} A {r_inner} {r_inner} 0 {large_arc} 0 {x2_i:.1f} {y2_i:.1f} Z"
        donut_svg += f'<path d="{path}" fill="{color}" stroke="white" stroke-width="1"/>'

        start_angle = end_angle

    donut_svg += '</svg>'

    # 图例（左右分布）
    donut_legend = '<div class="donut-legend">'
    for i, g in enumerate(genus):
        name = g.get("name", "")
        ratio = g.get("ratio", "")
        color = DONUT_COLORS[i % len(DONUT_COLORS)]
        
        # 计算垂直位置（居中分布）
        offset = (i % 5) * 18  # 增加间距避免重叠
        center_offset = offset - 36  # 居中
        
        # 左侧放6-10，右侧放1-5
        if i < 5:
            # 右侧
            donut_legend += f'''<div class="genus-item right" style="top:calc(50% + {center_offset}mm)">
                <div class="genus-rank" style="background:{color}">{i+1}</div>
                <div class="genus-info">
                    <span class="genus-name">{name}</span>
                    <span class="genus-ratio">{ratio}</span>
                </div>
            </div>'''
        else:
            # 左侧
            donut_legend += f'''<div class="genus-item left" style="top:calc(50% + {center_offset}mm)">
                <div class="genus-rank" style="background:{color}">{i+1}</div>
                <div class="genus-info">
                    <span class="genus-name">{name}</span>
                    <span class="genus-ratio">{ratio}</span>
                </div>
            </div>'''
    donut_legend += '</div>'

    donut_chart = donut_svg

    # 有益菌表格行
    beneficial_rows = ""
    
    # 如果没有有益菌数据，使用默认数据
    if not beneficial:
        beneficial = [
            {"name": "双歧杆菌", "result": "6.32%"},
            {"name": "乳杆菌", "result": "2.34%"},
            {"name": "粪杆菌", "result": "8.56%"},
            {"name": "罗斯氏菌", "result": "5.89%"},
            {"name": "阿克曼菌", "result": "1.98%"},
        ]
    
    for b in beneficial:
        name = b.get("name", "")
        result = b.get("result", "")
        # 判断水平
        if "低于检测限" in result or "未检出" in result:
            level = "低"
            tag = '<span class="result-tag result-fair">需关注</span>'
            ratio_display = "&lt;0.01"
        else:
            try:
                val = float(result.replace("%", ""))
                if val >= 5:
                    level = "高"
                    tag = '<span class="result-tag result-good">良好</span>'
                elif val >= 1:
                    level = "中"
                    tag = '<span class="result-tag result-fair">中等</span>'
                else:
                    level = "低"
                    tag = '<span class="result-tag result-poor">需关注</span>'
                ratio_display = f"{val:.2f}"
            except:
                level = "-"
                tag = ""
                ratio_display = result
        
        beneficial_rows += f'''<tr>
            <td class="name-cell">{name}</td>
            <td class="ratio-cell">{ratio_display}%</td>
            <td class="level-cell">{level}</td>
            <td class="tag-cell">{tag}</td>
        </tr>'''
    
    # 有害菌表格行（3列）
    harmful_rows = ""
    
    # 如果没有有害菌数据，使用默认数据（5行，与有益菌保持一致）
    if not harmful:
        harmful = [
            {"name": "沙门氏菌", "result": "未检出"},
            {"name": "志贺氏菌", "result": "未检出"},
            {"name": "弯曲菌", "result": "未检出"},
            {"name": "幽门螺杆菌", "result": "未检出"},
            {"name": "产气荚膜梭菌", "result": "未检出"},
        ]
    
    harmful_summary = "有害菌/致病菌未检出，表明肠道致病菌风险较低，肠道环境相对安全。"
    
    for h in harmful:
        name = h.get("name", "")
        result = h.get("result", "")
        # 判断结果
        if "低于检测限" in result or "未检出" in result:
            tag = '<span class="result-tag result-normal">正常</span>'
            result_display = "未检出"
        else:
            try:
                val = float(result.replace("%", ""))
                if val >= 5:
                    tag = '<span class="result-tag result-fair">需关注</span>'
                    harmful_summary = "检测到有害菌水平较高，建议关注并咨询专业医生。"
                elif val >= 1:
                    tag = '<span class="result-tag result-fair">中等</span>'
                else:
                    tag = '<span class="result-tag result-good">良好</span>'
                result_display = f"{val:.2f}%"
            except:
                tag = ""
                result_display = result
        
        harmful_rows += f'''<tr>
            <td>{name}</td>
            <td>{result_display}</td>
            <td>{tag}</td>
        </tr>'''
    
    # B/E比值（双歧杆菌属/肠杆菌科）
    be_value = be_ratio.get("value", "1.5")
    be_status = "正常"
    be_marker_pos = "50"
    be_advice = "B/E比值在理想范围内，肠道菌群结构较为平衡。"
    
    try:
        be_val = float(be_value)
        if be_val >= 1:
            be_status = "正常"
            be_marker_pos = str(min(be_val * 20 + 30, 95))
            be_advice = "B/E比值正常，肠道菌群结构较为平衡。"
        elif be_val >= 0.1:
            be_status = "中度受损"
            be_marker_pos = str(max(be_val * 50 + 10, 5))
            be_advice = "B/E比值中度偏低，肠道菌群平衡受到一定影响，建议注意饮食调整。"
        else:
            be_status = "重度受损"
            be_marker_pos = "5"
            be_advice = "B/E比值重度偏低，肠道菌群平衡严重失调，建议及时咨询医生进行调理。"
    except:
        pass
    
    replacements = {
        "{{donut_chart}}": donut_chart,
        "{{donut_legend}}": donut_legend,
        "{{top10_ratio}}": top10_ratio,
        "{{beneficial_rows}}": beneficial_rows,
        "{{harmful_rows}}": harmful_rows,
        "{{harmful_summary}}": harmful_summary,
        "{{be_value}}": str(be_value),
        "{{be_status}}": be_status,
        "{{be_marker_pos}}": str(be_marker_pos),
        "{{be_advice}}": be_advice,
        "{{logo_w_image}}": "file:///" + os.path.join(templates_dir, "logo-w.png").replace("\\", "/"),
    }
    
    for key, val in replacements.items():
        html = html.replace(key, val)
    
    return html


def build_page4(data):
    """构建建议页HTML"""
    html = read_template("page4_advice.html")
    
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    
    # AI结论
    ai_conclusion = data.get("ai_conclusion", "") or "您的肠道菌群整体状态良好，多样性丰富。建议保持当前健康的生活方式，注意饮食均衡，适当补充膳食纤维和益生菌。"
    
    # 饮食建议
    diet_items = ""
    diet_list = data.get("diet_suggestions", []) or [
        "增加膳食纤维摄入，多吃蔬菜、水果和全谷物",
        "适量摄入发酵食品，如酸奶、泡菜、纳豆",
        "减少高糖、高脂食物的摄入",
        "保证充足的水分摄入，每天1.5-2升水",
        "适量摄入优质蛋白质，如鱼、禽肉、豆类",
    ]
    
    for item in diet_list[:6]:
        diet_items += f'<div class="suggestion-item">• {item}</div>'
    
    # 益生菌建议
    probiotic_items = ""
    probiotic_list = data.get("probiotic_suggestions", []) or [
        "双歧杆菌：有助于调节肠道菌群平衡",
        "乳酸菌：促进营养物质消化吸收",
        "推荐选择含多种菌株的益生菌补充剂",
    ]
    
    for item in probiotic_list[:4]:
        probiotic_items += f'<div class="suggestion-item">• {item}</div>'
    
    # 生活方式建议
    lifestyle_items = ""
    lifestyle_list = data.get("lifestyle_suggestions", []) or [
        "保持规律作息，避免熬夜",
        "每周进行3-5次有氧运动",
        "学会调节情绪，减轻压力",
        "戒烟限酒",
        "保持良好的个人卫生习惯",
    ]
    
    for item in lifestyle_list[:5]:
        lifestyle_items += f'<div class="suggestion-item">• {item}</div>'
    
    # 阶段性目标
    phase1_desc = "第1-2周"
    phase1_goal = "基础调理期"
    
    phase2_desc = "第3-4周"
    phase2_goal = "强化改善期"
    
    phase3_desc = "第5-8周"
    phase3_goal = "巩固维护期"
    
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    replacements = {
        "{{ai_conclusion}}": ai_conclusion,
        "{{diet_items}}": diet_items,
        "{{probiotic_items}}": probiotic_items,
        "{{lifestyle_items}}": lifestyle_items,
        "{{icon_diet}}": os.path.join(assets_dir, "icon_diet_small.png"),
        "{{icon_probiotic}}": os.path.join(assets_dir, "icon_probiotic_small.png"),
        "{{icon_exercise}}": os.path.join(assets_dir, "icon_exercise_small.png"),
        "{{phase1_desc}}": phase1_desc,
        "{{phase2_desc}}": phase2_desc,
        "{{phase3_desc}}": phase3_desc,
        "{{phase1_goal}}": phase1_goal,
        "{{phase2_goal}}": phase2_goal,
        "{{phase3_goal}}": phase3_goal,
        "{{logo_w_image}}": "file:///" + os.path.join(templates_dir, "logo-w.png").replace("\\", "/"),
    }
    
    for key, val in replacements.items():
        html = html.replace(key, val)
    
    return html


def build_page5(data):
    """构建科普页HTML"""
    html = read_template("page5_science.html")

    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

    # 提取年龄数据
    basic_age = data.get("basic_info", {}).get("age", "35")
    try:
        real_age = str(int(basic_age))
    except:
        real_age = "35"
    
    gut_age = "42"
    for idx in data.get("core_indices", []):
        if "肠道年龄" in idx.get("name", ""):
            gut_age_match = re.search(r'\d+', idx.get("result", ""))
            if gut_age_match:
                gut_age = gut_age_match.group()

    replacements = {
        "{{real_age}}": real_age,
        "{{gut_age}}": gut_age,
        "{{gut_age_image}}": os.path.join(assets_dir, "gut_age_illustration_small.png"),
        "{{balance_image}}": os.path.join(assets_dir, "balance_illustration_small.png"),
        "{{food_good_image}}": os.path.join(assets_dir, "food_good_small.png"),
        "{{food_bad_image}}": os.path.join(assets_dir, "food_bad_small.png"),
        "{{logo_w_image}}": "file:///" + os.path.join(templates_dir, "logo-w.png").replace("\\", "/"),
    }
    
    for key, val in replacements.items():
        html = html.replace(key, val)
    
    return html


def generate_report_v2(data, output_path):
    """生成完整报告"""
    pages = []
    
    # 页面1：封面
    pages.append(build_page1(data))
    
    # 页面2：核心指标
    pages.append(build_page2(data))
    
    # 页面3：菌群组成分析
    pages.append(build_page3(data))
    
    # 页面4：建议
    pages.append(build_page4(data))
    
    # 页面5：科普
    pages.append(build_page5(data))
    
    # 合并所有页面
    full_html = "\n".join(pages)
    
    # 生成PDF
    HTML(string=full_html).write_pdf(output_path)
    
    return output_path
