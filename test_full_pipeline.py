#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""完整端到端测试"""

import sys
import re
sys.path.insert(0, '.')
from report_generator_v2 import build_page2

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
        {'name': '肠球菌属', 'ratio': '1.12%'},
        {'name': '大肠杆菌属', 'ratio': '0.98%'},
        {'name': '克雷伯菌属', 'ratio': '0.76%'},
    ],
    'diversity_value': '7',
    'diversity_label': '偏低',
    'diversity_label_class': 'label-low',
    'gut_age': '42',
    'real_age': '30',
    'age_label': '偏高',
    'age_label_class': 'label-high',
    'enterotype': 'B型',
    'enterotype_desc': '拟杆菌型',
    'enterotype_label': '临床理想型',
    'enterotype_label_class': 'label-normal',
    'be_value': '1.17',
    'be_label': '正常',
    'be_label_class': 'label-normal',
}

html = build_page2(test_data)

# 检查变量替换
print('=== 变量替换检查 ===')
print('菌群多样性值:', '7' in html)
print('肠道年龄:', '42' in html)
print('肠型:', 'B型' in html)
print('B/E比值:', '1.17' in html)
print('普雷沃菌属:', '普雷沃菌属' in html)
print('拟杆菌属:', '拟杆菌属' in html)
print('双歧杆菌属:', '双歧杆菌属' in html)

# 检查模板标签是否被替换
print('\n=== 模板标签检查 ===')
print('{{diversity_value}}是否存在:', '{{diversity_value}}' in html)
print('{{genus_bars}}是否存在:', '{{genus_bars}}' in html)
print('{{enterotype}}是否存在:', '{{enterotype}}' in html)

# 统计属级条形图数量
genus_count = html.count('bar-fill-genus')
print(f'\n属级条形图数量: {genus_count}')

# 统计门级条形图数量
phylum_count = html.count('bar-fill">') - html.count('bar-fill-genus')
print(f'门级条形图数量: {phylum_count}')

# 保存HTML
with open('test_full.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\n已保存测试文件: test_full.html')

# 生成PDF
from weasyprint import HTML
try:
    HTML(string=html).write_pdf('test_full.pdf')
    print('PDF生成成功: test_full.pdf')
except Exception as e:
    print(f'PDF生成失败: {e}')
