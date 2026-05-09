#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""详细调试解析逻辑"""

import re

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

print('=== 测试各模式匹配 ===')

# 测试各个模式
patterns = [
    r"(?:核心指标|检测结果|核心数据)\s*\n(.*?)(?=\n\n菌群分布|\n\n门级|\n\n属级|$)",
    r"(?:核心指标|检测结果|核心数据)[\s\S]*?(?=菌群分布|门级|属级|$)",
    r"(GMHI评分[\s\S]*?B/E比值[\s\S]*?)(?=\n\n|$)",
]

for i, pattern in enumerate(patterns):
    match = re.search(pattern, real_pdf_text, re.DOTALL | re.IGNORECASE)
    if match:
        print(f"\n模式{i+1}匹配成功:")
        print(f"匹配内容:\n'{match.group(1)[:200]}...'")
    else:
        print(f"\n模式{i+1}匹配失败")

print('\n=== 测试直接在全文本中查找 ===')
# 测试直接在全文本中查找
diversity_match = re.search(r"(?:菌群)?多样性[：:]?\s*([\d.]+)", real_pdf_text, re.IGNORECASE)
if diversity_match:
    print(f"菌群多样性匹配成功: {diversity_match.group(1)}")
else:
    print("菌群多样性匹配失败")

gut_age_match = re.search(r"(?:肠道年龄|肠龄)[：:]?\s*(\d+)", real_pdf_text, re.IGNORECASE)
if gut_age_match:
    print(f"肠道年龄匹配成功: {gut_age_match.group(1)}")
else:
    print("肠道年龄匹配失败")

gmhi_match = re.search(r"GMHI[评分]*[：:]?\s*([\d.]+)", real_pdf_text, re.IGNORECASE)
if gmhi_match:
    print(f"GMHI评分匹配成功: {gmhi_match.group(1)}")
else:
    print("GMHI评分匹配失败")

enterotype_match = re.search(r"肠型[：:]?\s*([A-Z])[型]?", real_pdf_text, re.IGNORECASE)
if enterotype_match:
    print(f"肠型匹配成功: {enterotype_match.group(1)}")
else:
    print("肠型匹配失败")

be_match = re.search(r"B/E[比值]*[：:]?\s*([\d.]+)", real_pdf_text, re.IGNORECASE)
if be_match:
    print(f"B/E比值匹配成功: {be_match.group(1)}")
else:
    print("B/E比值匹配失败")

print('\n=== 测试逐行解析 ===')
lines = real_pdf_text.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # 检查是否匹配任何指标
    if '多样性' in line:
        match = re.search(r'[\d.]+', line)
        if match:
            print(f"多样性行: {line} -> 值: {match.group()}")
    elif '肠道年龄' in line:
        match = re.search(r'\d+', line)
        if match:
            print(f"肠道年龄行: {line} -> 值: {match.group()}")
    elif 'GMHI' in line:
        match = re.search(r'[\d.]+', line)
        if match:
            print(f"GMHI行: {line} -> 值: {match.group()}")
    elif '肠型' in line:
        match = re.search(r'[A-Z]型?', line)
        if match:
            print(f"肠型行: {line} -> 值: {match.group()}")
    elif 'B/E' in line:
        match = re.search(r'[\d.]+', line)
        if match:
            print(f"B/E行: {line} -> 值: {match.group()}")
