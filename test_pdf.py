#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试PDF生成"""

import sys
sys.path.insert(0, '.')
from report_generator_v2 import build_page2
from weasyprint import HTML, CSS

# 测试数据
test_data = {
    'basic_info': {'name': '测试', 'gender': '男', 'age': '30'},
    'test_info': {},
    'report_info': {},
    'core_indices': [],
    'phylum_distribution': [
        {'name': '厚壁菌门', 'ratio': '39.11%'},
        {'name': '拟杆菌门', 'ratio': '36.8%'},
        {'name': '变形菌门', 'ratio': '3.89%'},
        {'name': '放线菌门', 'ratio': '2.08%'},
        {'name': '梭杆菌门', 'ratio': '0.47%'},
    ],
    'genus_distribution': [
        {'name': '普雷沃菌属', 'ratio': '26.90%'},
        {'name': '拟杆菌属', 'ratio': '10.21%'},
        {'name': '粪杆菌属', 'ratio': '8.56%'},
        {'name': '双歧杆菌属', 'ratio': '6.32%'},
        {'name': '罗斯氏菌属', 'ratio': '5.89%'},
        {'name': '瘤胃球菌属', 'ratio': '4.65%'},
        {'name': '真杆菌属', 'ratio': '3.21%'},
        {'name': '梭菌属', 'ratio': '2.87%'},
        {'name': '阿克曼菌属', 'ratio': '2.15%'},
        {'name': '链球菌属', 'ratio': '1.89%'},
        {'name': '韦荣球菌属', 'ratio': '1.56%'},
        {'name': '乳杆菌属', 'ratio': '1.34%'},
    ]
}

html = build_page2(test_data)

# 生成PDF
try:
    HTML(string=html).write_pdf('test_page2.pdf')
    print('PDF生成成功: test_page2.pdf')
except Exception as e:
    print(f'PDF生成失败: {e}')
