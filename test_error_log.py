#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""详细错误日志测试"""

import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print('=== 详细错误日志测试 ===\n')

# 测试1: 检查依赖
print('1. 检查依赖...')
try:
    import pdfplumber
    print('   ✓ pdfplumber')
except ImportError as e:
    print(f'   ✗ pdfplumber: {e}')

try:
    import weasyprint
    print('   ✓ weasyprint')
except ImportError as e:
    print(f'   ✗ weasyprint: {e}')

try:
    from report_generator_v2 import generate_report_v2
    print('   ✓ report_generator_v2')
except ImportError as e:
    print(f'   ✗ report_generator_v2: {e}')
    traceback.print_exc()

try:
    from pdf_parser import parse_report_pdf, parse_core_indices
    print('   ✓ pdf_parser')
except ImportError as e:
    print(f'   ✗ pdf_parser: {e}')
    traceback.print_exc()

# 测试2: 检查模板文件
print('\n2. 检查模板文件...')
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
template_files = [
    'page1_basic.html',
    'page2_indices.html', 
    'page3_distribution.html',
    'page4_advice.html',
    'page5_science.html'
]

for f in template_files:
    path = os.path.join(templates_dir, f)
    if os.path.exists(path):
        print(f'   ✓ {f}')
    else:
        print(f'   ✗ {f} - 不存在')

# 测试3: 检查资源文件
print('\n3. 检查资源文件...')
assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
if os.path.exists(assets_dir):
    assets = os.listdir(assets_dir)
    print(f'   ✓ assets目录存在，包含 {len(assets)} 个文件')
else:
    print('   ✗ assets目录不存在')

# 测试4: 测试解析函数
print('\n4. 测试解析函数...')
try:
    test_text = """核心指标
GMHI评分: 58.5
菌群多样性: 2.7578
肠道年龄: 52岁
肠型: B型
B/E比值: 1.17"""
    
    result = parse_core_indices(test_text)
    print(f'   ✓ parse_core_indices 工作正常')
    print(f'     解析结果: {result}')
except Exception as e:
    print(f'   ✗ parse_core_indices 失败: {e}')
    traceback.print_exc()

# 测试5: 测试报告生成
print('\n5. 测试报告生成...')
try:
    test_data = {
        'basic_info': {'name': '测试', 'gender': '男', 'age': '30'},
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
        ],
        'genus_distribution': [
            {'name': '普雷沃菌属', 'ratio': '26.90%', 'category': '中性菌'},
            {'name': '拟杆菌属', 'ratio': '10.21%', 'category': '中性菌'},
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
    
    output_path = 'test_error_log.pdf'
    generate_report_v2(test_data, output_path)
    print(f'   ✓ 报告生成成功: {output_path}')
    
except Exception as e:
    print(f'   ✗ 报告生成失败: {type(e).__name__}: {e}')
    traceback.print_exc()

print('\n=== 测试完成 ===')
