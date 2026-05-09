#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试第12页格式解析"""

import sys
sys.path.insert(0, '.')

from pdf_parser import parse_genus_distribution

# 测试第12页的实际格式
test_text = """第12页占比最高的十五种菌属依次为：普雷沃菌属 9 型（Prevotella_9, 26.90%），梭杆菌属 （Fusobacterium,13.32%），毛梭菌属（Lachnoclostridium,10.19%），拟杆菌属（Bacteroides,9.16%）， 埃希氏菌-志贺氏菌（Escherichia-Shigella, 5.55%），巨单胞菌属（Megamonas, 4.02%），萨特菌属 （Sutterella,3.30%），粪杆菌属（Faecalibacterium,2.36%），普雷沃菌属（Prevotella,2.24%），严 格梭菌1型（Clostridiumsensustricto1, 2.06%），丁酸球菌属（Butyricicoccus, 1.42%），瘤胃球菌 扭链群（[Ruminococcus] torques group, 1.10%），布劳特氏菌属（Blautia, 0.95%），副拟杆菌属 （Parabacteroides, 0.81%），毛螺旋菌属（Lachnospira, 0.48%）。 

第13页"""

print('=== 测试第12页格式解析 ===')
result = parse_genus_distribution(test_text)
print(f'识别到 {len(result)} 种菌属')

# 验证是否正确识别15种菌
expected = [
    '普雷沃菌属', '梭杆菌属', '毛梭菌属', '拟杆菌属', '埃希氏菌-志贺氏菌',
    '巨单胞菌属', '萨特菌属', '粪杆菌属', '严 格梭菌1型', '丁酸球菌属',
    '瘤胃球菌 扭链群', '布劳特氏菌属', '副拟杆菌属', '毛螺旋菌属'
]

print('\n识别结果:')
for item in result:
    print(f"{item['rank']}. {item['name']} - {item['ratio']} - {item['category']}")

print('\n验证:')
missing = []
for exp in expected:
    found = False
    for item in result:
        if exp in item['name']:
            found = True
            break
    if not found:
        missing.append(exp)

if missing:
    print(f'✗ 缺少: {missing}')
else:
    print('✓ 所有菌属都已识别')

# 生成测试报告
if len(result) == 15:
    from report_generator_v2 import generate_report_v2
    
    test_data = {
        'basic_info': {'name': '测试用户', 'gender': '男', 'age': '30'},
        'test_info': {},
        'report_info': {},
        'core_indices': [
            {'name': 'GMHI评分', 'result': '58.5', 'description': '肠道健康指数'},
            {'name': '菌群多样性', 'result': '2.7578', 'description': '菌群丰富度指标'},
            {'name': '肠道年龄', 'result': '52岁', 'description': '肠道生理年龄'},
            {'name': '肠型', 'result': 'B型', 'description': '拟杆菌型'},
            {'name': 'B/E比值', 'result': '1.17', 'description': '菌群平衡指标'},
        ],
        'phylum_distribution': [
            {'name': '厚壁菌门', 'ratio': '39.11%'},
            {'name': '拟杆菌门', 'ratio': '36.8%'},
            {'name': '变形菌门', 'ratio': '3.89%'},
            {'name': '放线菌门', 'ratio': '2.08%'},
            {'name': '梭杆菌门', 'ratio': '0.47%'},
        ],
        'genus_distribution': result,
        'beneficial_bacteria': [],
        'harmful_bacteria': [],
        'be_ratio': {},
        'ai_conclusion': '测试结论',
        'diet_advice': [],
        'probiotic_advice': [],
        'lifestyle_advice': [],
        'intervention_plan': {
            'phase1': [],
            'phase2': [],
            'phase3': [],
        },
        'science_education': {},
    }
    
    try:
        generate_report_v2(test_data, 'test_page12_format.pdf')
        print('\n✓ 报告生成成功: test_page12_format.pdf')
    except Exception as e:
        print(f'\n✗ 报告生成失败: {e}')
        import traceback
        traceback.print_exc()
