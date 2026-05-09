#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""最终修复测试"""

import sys
sys.path.insert(0, '.')

from pdf_parser import parse_core_indices

# 测试各种文本格式
test_cases = [
    # 格式1: 标准格式（中文冒号）
    """核心指标
GMHI评分：58.5
菌群多样性：2.7578
肠道年龄：52岁
肠型：B型 拟杆菌型
B/E比值：1.17

菌群分布""",
    
    # 格式2: 英文冒号带空格
    """核心指标
GMHI评分 : 58.5
菌群多样性 : 2.7578
肠道年龄 : 52岁
肠型 : B型
B/E比值 : 1.17

菌群分布""",
    
    # 格式3: 混合格式
    """核心指标
GMHI评分: 58.5
菌群多样性 : 2.7578
肠道年龄：52岁
肠型：B型
B/E比值 : 1.17

菌群分布""",
]

print('=== 最终修复测试 ===\n')

for i, test_text in enumerate(test_cases):
    print(f'测试用例{i+1}:')
    print(f'输入文本:\n{test_text}\n')
    
    result = parse_core_indices(test_text)
    print(f'解析结果: {result}')
    
    # 验证结果
    success = True
    expected_names = ['GMHI评分', '菌群多样性', '肠道年龄', '肠型', 'B/E比值']
    actual_names = [item['name'] for item in result]
    
    for expected in expected_names:
        if expected not in actual_names:
            print(f'  ✗ 缺少: {expected}')
            success = False
    
    # 检查是否有错误条目
    for item in result:
        if not item['name'] or item['name'].strip() != item['name']:
            print(f'  ✗ 名称格式错误: {item}')
            success = False
    
    if success:
        print('  ✓ 全部正确')
    print()

# 生成最终测试报告
print('\n=== 生成测试报告 ===')
from report_generator_v2 import generate_report_v2

test_data = {
    'basic_info': {'name': '测试用户', 'gender': '男', 'age': '30'},
    'test_info': {},
    'report_info': {},
    'core_indices': parse_core_indices(test_cases[1]),
    'phylum_distribution': [
        {'name': '厚壁菌门', 'ratio': '39.11%'},
        {'name': '拟杆菌门', 'ratio': '36.8%'},
        {'name': '变形菌门', 'ratio': '3.89%'},
        {'name': '放线菌门', 'ratio': '2.08%'},
        {'name': '梭杆菌门', 'ratio': '0.47%'},
    ],
    'genus_distribution': [
        {'name': '普雷沃菌属', 'ratio': '26.90%', 'category': '中性菌'},
        {'name': '拟杆菌属', 'ratio': '10.21%', 'category': '中性菌'},
        {'name': '粪杆菌属', 'ratio': '8.56%', 'category': '有益菌'},
        {'name': '双歧杆菌属', 'ratio': '6.32%', 'category': '有益菌'},
        {'name': '罗斯氏菌属', 'ratio': '5.89%', 'category': '有益菌'},
        {'name': '瘤胃球菌属', 'ratio': '4.65%', 'category': '中性菌'},
        {'name': '真杆菌属', 'ratio': '3.21%', 'category': '中性菌'},
        {'name': '梭菌属', 'ratio': '2.87%', 'category': '有害菌'},
        {'name': '阿克曼菌属', 'ratio': '2.15%', 'category': '有益菌'},
        {'name': '链球菌属', 'ratio': '1.89%', 'category': '中性菌'},
        {'name': '韦荣球菌属', 'ratio': '1.56%', 'category': '中性菌'},
        {'name': '乳杆菌属', 'ratio': '1.34%', 'category': '有益菌'},
        {'name': '肠球菌属', 'ratio': '1.12%', 'category': '有害菌'},
        {'name': '大肠杆菌属', 'ratio': '0.98%', 'category': '有害菌'},
        {'name': '克雷伯菌属', 'ratio': '0.76%', 'category': '有害菌'},
    ],
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
    generate_report_v2(test_data, 'test_final_report.pdf')
    print('✓ 报告生成成功: test_final_report.pdf')
except Exception as e:
    print(f'✗ 报告生成失败: {e}')
    import traceback
    traceback.print_exc()
