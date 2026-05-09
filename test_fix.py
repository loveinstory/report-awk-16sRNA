#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试修复效果"""

import sys
import re
sys.path.insert(0, '.')
from report_generator_v2 import build_page2

# 测试数据 - 15种菌属
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
    ]
}

html = build_page2(test_data)

# 使用正则表达式分别统计门级和属级条数
phylum_pattern = r'<div class="bar-track"><div class="bar-fill" style="width:[\d.]+%"></div></div>'
phylum_matches = re.findall(phylum_pattern, html)

genus_pattern = r'<div class="bar-track"><div class="bar-fill-genus" style="width:[\d.]+%"></div></div>'
genus_matches = re.findall(genus_pattern, html)

print('=== 测试结果 ===')
print(f'门级分布条数: {len(phylum_matches)}')
print(f'属级分布条数: {len(genus_matches)}')
print(f'总条形数: {len(phylum_matches) + len(genus_matches)}')

# 验证属级是否显示全部15条
print(f'属级显示全部15条: {len(genus_matches) == 15}')

# 检查关键布局元素
print('\n=== 布局检查 ===')
print('1. Shannon指数缩放:', 'transform: scale(0.85)' in html)
print('2. bar-item行间距增加:', 'margin: 2px 0' in html)
print('3. bar-item高度:', 'height: 13px' in html)
print('4. 4个mini-card存在:', html.count('mini-card') >= 4)
print('5. 肠道年龄卡片:', '肠道年龄' in html)
print('6. B/E比值卡片:', 'B/E比值' in html)

# 保存HTML用于检查
with open('test_page2.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\n已保存测试文件: test_page2.html')
