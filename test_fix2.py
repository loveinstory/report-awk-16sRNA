#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试修复效果"""

import sys
import re
sys.path.insert(0, '.')
from report_generator_v2 import build_page2

# 测试数据 - 包含15种菌属
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

# 使用正则表达式统计属级条数
genus_pattern = r'<div class="bar-fill-genus" style="width:[\d.]+%"></div>'
genus_matches = re.findall(genus_pattern, html)

print('=== 测试结果 ===')
print(f'属级分布条数: {len(genus_matches)}')
print(f'期望数量: 15')

# 检查关键布局元素
print('\n=== 布局检查 ===')
print('1. bar-label宽度:', 'width: 55px' in html)
print('2. bar-label字体:', 'font-size: 8px' in html)
print('3. mini-card最大高度:', 'max-height: 60px' in html)
print('4. 4个mini-card存在:', html.count('mini-card') >= 4)

# 检查菌群多样性卡片内容
print('\n=== 菌群多样性卡片内容 ===')
if '菌群多样性' in html:
    print('菌群多样性卡片存在')
    # 检查是否有多余内容
    diversity_card = re.search(r'<div class="mini-card">.*?菌群多样性.*?</div>', html, re.DOTALL)
    if diversity_card:
        card_content = diversity_card.group(0)
        print(f'卡片内容长度: {len(card_content)}')
        # 检查是否有条形图
        if 'bar-track' in card_content:
            print('警告: 菌群多样性卡片中包含条形图')
        else:
            print('正常: 菌群多样性卡片中没有条形图')

# 保存HTML用于检查
with open('test_page2_fixed.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\n已保存测试文件: test_page2_fixed.html')

# 生成PDF
from weasyprint import HTML
try:
    HTML(string=html).write_pdf('test_page2_fixed.pdf')
    print('PDF生成成功: test_page2_fixed.pdf')
except Exception as e:
    print(f'PDF生成失败: {e}')
