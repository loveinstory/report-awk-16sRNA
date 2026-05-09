#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试第12页实际解析效果"""

import sys
sys.path.insert(0, '.')

from pdf_parser import parse_genus_distribution

# 模拟用户提供的第12页内容
page12_text = """第12页占比最高的十五种菌属依次为：普雷沃菌属 9 型（Prevotella_9, 26.90%），梭杆菌属 （Fusobacterium,13.32%），毛梭菌属（Lachnoclostridium,10.19%），拟杆菌属（Bacteroides,9.16%）， 埃希氏菌-志贺氏菌（Escherichia-Shigella, 5.55%），巨单胞菌属（Megamonas, 4.02%），萨特菌属 （Sutterella,3.30%），粪杆菌属（Faecalibacterium,2.36%），普雷沃菌属（Prevotella,2.24%），严 格梭菌1型（Clostridiumsensustricto1, 2.06%），丁酸球菌属（Butyricicoccus, 1.42%），瘤胃球菌 扭链群（[Ruminococcus] torques group, 1.10%），布劳特氏菌属（Blautia, 0.95%），副拟杆菌属 （Parabacteroides, 0.81%），毛螺旋菌属（Lachnospira, 0.48%）。 

第13页"""

print('=== 测试第12页实际解析效果 ===')

# 调用解析函数
result = parse_genus_distribution(page12_text)

print(f'\n解析结果数量: {len(result)}')
print('\n解析结果:')
for i, item in enumerate(result, 1):
    print(f'{i}. {item["name"]} - {item["ratio"]} - {item["category"]}')

# 生成测试报告
from report_generator_v2 import generate_report_v2

test_data = {
    'basic_info': {'name': '测试用户', 'gender': '男', 'age': '30'},
    'test_info': {},
    'report_info': {},
    'core_indices': [],
    'phylum_distribution': [],
    'genus_distribution': result,
    'beneficial_bacteria': [],
    'harmful_bacteria': [],
    'be_ratio': {},
    'ai_conclusion': '测试结论',
    'diet_advice': [],
    'probiotic_advice': [],
    'lifestyle_advice': [],
    'intervention_plan': {'phase1': [], 'phase2': [], 'phase3': []},
    'science_education': {},
}

generate_report_v2(test_data, 'test_page12_real.pdf')
print('\n✓ 报告生成成功: test_page12_real.pdf')
