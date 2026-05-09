#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""详细调试解析步骤"""

import sys
sys.path.insert(0, '.')
from pdf_parser import parse_core_indices

# 模拟真实PDF中的文本提取结果
real_pdf_text = """
本检测报告包含以下内容：

核心指标

GMHI评分 : 58.5
菌群多样性 : 2.7578     
肠道年龄 : 52岁
肠型 : B型

B/E比值 : 1.17

检测日期：2024年1月15日 

菌群分布

门级水平分布

1 厚壁菌门 39.11%       

2 拟杆菌门 36.8%        

3 变形菌门 3.89%        

4 放线菌门 2.08%        

5 梭杆菌门 0.47%        

属级水平分布

1 普雷沃菌属 26.90% 中性菌

2 拟杆菌属 10.21% 中性菌

3 粪杆菌属 8.56% 有益菌

4 双歧杆菌属 6.32% 有益菌

5 罗斯氏菌属 5.89% 有益菌

6 瘤胃球菌属 4.65% 中性菌

7 真杆菌属 3.21% 中性菌

8 梭菌属 2.87% 有害菌

9 阿克曼菌属 2.15% 有益菌

10 链球菌属 1.89% 中性菌

11 韦荣球菌属 1.56% 中性菌

12 乳杆菌属 1.34% 有益菌

13 肠球菌属 1.12% 有害菌

14 大肠杆菌属 0.98% 有害菌

15 克雷伯菌属 0.76% 有害菌

"""

print('=== 手动模拟parse_core_indices步骤 ===')

import re

# 步骤1: 查找核心指标区域
section_patterns = [
    r"(?:核心指标|检测结果|核心数据)\s*\n(.*?)(?=\n\n菌群分布|\n\n门级|\n\n属级|$)",
    r"(?:核心指标|检测结果|核心数据)[\s\S]*?(?=菌群分布|门级|属级|$)",
    r"(GMHI评分[\s\S]*?B/E比值[\s\S]*?)(?=\n\n|$)",
]

section_text = ""
for i, pattern in enumerate(section_patterns):
    core_section = re.search(pattern, real_pdf_text, re.DOTALL | re.IGNORECASE)
    if core_section:
        section_text = core_section.group(1)
        print(f"使用模式{i+1}")
        break

print(f"\n提取的section_text:\n'{section_text}'")

# 步骤2: 清理文本
section_text_clean = re.sub(r'[ \t]+', ' ', section_text)
section_text_clean = re.sub(r'\n+', '\n', section_text_clean)

print(f"\n清理后的section_text:\n'{section_text_clean}'")

# 步骤3: 尝试匹配各个指标
print('\n=== 尝试匹配各指标 ===')

# GMHI评分
gmhi_patterns = [
    r"GMHI[评分]*[：:]?\s*([\d.]+)",
    r"GMHI\s+([\d.]+)",
    r"肠道健康指数[：:]?\s*([\d.]+)",
]
print("\nGMHI评分匹配:")
for pattern in gmhi_patterns:
    match = re.search(pattern, section_text_clean, re.IGNORECASE)
    print(f"  模式 '{pattern}': {'成功' if match else '失败'}")
    if match:
        print(f"    匹配值: {match.group(1)}")
        break

# 菌群多样性
diversity_patterns = [
    r"(?:菌群)?多样性[：:]?\s*([\d.]+)",
    r"Shannon[指数]*[：:]?\s*([\d.]+)",
    r"多样性指数[：:]?\s*([\d.]+)",
    r"(?:菌群)?多样性\s+([\d.]+)",
]
print("\n菌群多样性匹配:")
for pattern in diversity_patterns:
    match = re.search(pattern, section_text_clean, re.IGNORECASE)
    print(f"  模式 '{pattern}': {'成功' if match else '失败'}")
    if match:
        print(f"    匹配值: {match.group(1)}")
        break

# 肠道年龄
gut_age_patterns = [
    r"(?:肠道年龄|肠龄)[：:]?\s*(\d+)",
    r"(?:肠道年龄|肠龄)\s+(\d+)",
    r"(?:肠道年龄|肠龄)[：:]?\s*(\d+)\s*岁",
]
print("\n肠道年龄匹配:")
for pattern in gut_age_patterns:
    match = re.search(pattern, section_text_clean, re.IGNORECASE)
    print(f"  模式 '{pattern}': {'成功' if match else '失败'}")
    if match:
        print(f"    匹配值: {match.group(1)}")
        break

# 肠型
enterotype_patterns = [
    r"肠型[：:]?\s*([A-Z])[型\s]*(.+?)?(?=\s|$)",
    r"肠型[：:]?\s*([A-Z])型",
    r"Enterotype[：:]?\s*([A-Z])",
]
print("\n肠型匹配:")
for pattern in enterotype_patterns:
    match = re.search(pattern, section_text_clean, re.IGNORECASE)
    print(f"  模式 '{pattern}': {'成功' if match else '失败'}")
    if match:
        print(f"    匹配值: {match.group(1)}")
        break

# B/E比值
be_patterns = [
    r"B/E[比值]*[：:]?\s*([\d.]+)",
    r"B/E\s+([\d.]+)",
    r"Bacteroides.*?Enterobacteriaceae.*?([\d.]+)",
]
print("\nB/E比值匹配:")
for pattern in be_patterns:
    match = re.search(pattern, section_text_clean, re.IGNORECASE)
    print(f"  模式 '{pattern}': {'成功' if match else '失败'}")
    if match:
        print(f"    匹配值: {match.group(1)}")
        break

print('\n=== 调用实际函数 ===')
result = parse_core_indices(real_pdf_text)
print(f"parse_core_indices结果: {result}")
