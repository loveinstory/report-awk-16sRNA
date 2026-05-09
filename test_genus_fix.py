#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试属级分布修复"""

import sys
sys.path.insert(0, '.')

from pdf_parser import parse_genus_distribution

# 测试标准格式
test_text = """第12页

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

第13页"""

print('=== 测试属级分布解析 ===')
result = parse_genus_distribution(test_text)
print(f'找到 {len(result)} 个菌属')

# 验证是否正确识别15种菌
expected_names = [
    '普雷沃菌属', '拟杆菌属', '粪杆菌属', '双歧杆菌属', '罗斯氏菌属',
    '瘤胃球菌属', '真杆菌属', '梭菌属', '阿克曼菌属', '链球菌属',
    '韦荣球菌属', '乳杆菌属', '肠球菌属', '大肠杆菌属', '克雷伯菌属'
]

missing = []
extra = []
for expected in expected_names:
    found = False
    for item in result:
        if expected in item['name']:
            found = True
            break
    if not found:
        missing.append(expected)

for item in result:
    if item['name'] not in expected_names:
        extra.append(item['name'])

if missing:
    print(f'\n✗ 缺少: {missing}')
else:
    print('\n✓ 所有15种菌都已识别')

if extra:
    print(f'✗ 多余: {extra}')
else:
    print('✓ 无多余条目')

# 生成测试报告
print('\n=== 生成测试报告 ===')
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
    generate_report_v2(test_data, 'test_genus_fix.pdf')
    print('✓ 报告生成成功: test_genus_fix.pdf')
except Exception as e:
    print(f'✗ 报告生成失败: {e}')
    import traceback
    traceback.print_exc()
