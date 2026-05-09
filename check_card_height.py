#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查卡片高度"""

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

# 提取cards-right部分
cards_right_match = re.search(r'<div class="cards-right">(.*?)</div>', html, re.DOTALL)
if cards_right_match:
    cards_right = cards_right_match.group(1)
    
    # 提取每个mini-card
    cards = re.findall(r'<div class="mini-card">(.*?)</div>', cards_right, re.DOTALL)
    
    print('=== 四个卡片内容 ===')
    for i, card in enumerate(cards):
        # 移除空白字符
        clean_card = re.sub(r'\s+', ' ', card).strip()
        print(f'\n卡片{i+1}:')
        print(f'内容: {clean_card}')
        print(f'长度: {len(card)}')

# 检查是否有多余的条形图在卡片内
if 'bar-track' in cards_right:
    print('\n警告: cards-right中包含条形图！')
else:
    print('\n正常: cards-right中没有条形图')

# 保存完整HTML用于检查
with open('check_cards.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\n已保存检查文件: check_cards.html')
