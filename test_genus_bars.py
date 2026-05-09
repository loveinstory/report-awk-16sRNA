#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试genus_bars生成"""

import sys
sys.path.insert(0, '.')

# 模拟genus_bars生成逻辑
genus_data = [
    {"name": "普雷沃菌属", "ratio": "26.90%"},
    {"name": "拟杆菌属", "ratio": "10.21%"},
    {"name": "粪杆菌属", "ratio": "8.56%"},
    {"name": "双歧杆菌属", "ratio": "6.32%"},
    {"name": "罗斯氏菌属", "ratio": "5.89%"},
    {"name": "瘤胃球菌属", "ratio": "4.65%"},
    {"name": "真杆菌属", "ratio": "3.21%"},
    {"name": "梭菌属", "ratio": "2.87%"},
    {"name": "阿克曼菌属", "ratio": "2.15%"},
    {"name": "链球菌属", "ratio": "1.89%"},
    {"name": "韦荣球菌属", "ratio": "1.56%"},
    {"name": "乳杆菌属", "ratio": "1.34%"},
    {"name": "肠球菌属", "ratio": "1.12%"},
    {"name": "大肠杆菌属", "ratio": "0.98%"},
    {"name": "克雷伯菌属", "ratio": "0.76%"},
]

print(f'genus_data长度: {len(genus_data)}')
print(f'genus_data内容: {genus_data}')

genus_bars = ""
for item in genus_data:
    name = item.get("name", "")
    ratio_str = item.get("ratio", "0%")
    try:
        ratio_val = float(ratio_str.replace("%", ""))
    except:
        ratio_val = 0
    bar_width = min(ratio_val / 30 * 100, 100)
    genus_bars += f'''<div class="bar-item">
        <div class="bar-label">{name}</div>
        <div class="bar-track"><div class="bar-fill-genus" style="width:{bar_width}%"></div></div>
        <div class="bar-value">{ratio_str}</div>
    </div>\n'''

print(f'\ngenus_bars长度: {len(genus_bars)}')
print(f'genus_bars内容预览:\n{genus_bars[:500]}...')

# 统计条形图数量
import re
bars = re.findall(r'<div class="bar-fill-genus', genus_bars)
print(f'\n条形图数量: {len(bars)}')
