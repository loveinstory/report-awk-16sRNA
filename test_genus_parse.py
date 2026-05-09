#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试属级分布解析逻辑"""

import sys
sys.path.insert(0, '.')
from pdf_parser import parse_genus_distribution

# 模拟原始报告第12页的属级分布数据
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

# 测试解析
result = parse_genus_distribution(test_text)

print('=== 属级分布解析测试 ===')
print(f'解析到的菌属数量: {len(result)}')
print(f'期望数量: 15')
print(f'是否完整: {len(result) == 15}')
print()
print('详细结果:')
for item in result:
    print(f"{item['rank']}. {item['name']} - {item['ratio']} ({item['category']})")
