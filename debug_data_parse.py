#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试数据解析问题"""

import sys
sys.path.insert(0, '.')
from pdf_parser import parse_core_indices

# 模拟PDF中的数据格式
test_text = """
核心指标
GMHI评分: 58.5
菌群多样性: 2.7578
肠道年龄: 52岁
肠型: B型 拟杆菌型
B/E比值: 1.17

菌群分布
门级水平分布
...
"""

print('=== 测试解析核心指标 ===')
print(f'输入文本:\n{test_text}')

indices = parse_core_indices(test_text)
print(f'\n解析结果: {indices}')

print('\n=== 检查每个指标 ===')
for idx in indices:
    print(f"名称: {idx.get('name')}, 结果: {idx.get('result')}, 说明: {idx.get('description')}")

# 测试从core_indices提取值的逻辑
print('\n=== 测试提取逻辑 ===')
diversity_value = "2.68"  # 默认值
gut_age = "42"  # 默认值

for idx in indices:
    name = idx.get("name", "")
    result = idx.get("result", "")
    if "多样性" in name:
        import re
        diversity_value = re.search(r'[\d.]+', result).group() if re.search(r'[\d.]+', result) else result
        print(f"菌群多样性提取值: {diversity_value}")
    elif "肠道年龄" in name:
        gut_age = re.search(r'\d+', result).group() if re.search(r'\d+', result) else result
        print(f"肠道年龄提取值: {gut_age}")

print(f'\n最终值:')
print(f"菌群多样性: {diversity_value}")
print(f"肠道年龄: {gut_age}")
