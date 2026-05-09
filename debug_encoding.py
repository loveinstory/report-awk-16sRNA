#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试编码问题"""

import re

# 测试各种冒号格式
test_cases = [
    "GMHI评分: 58.5",    # 英文冒号无空格
    "GMHI评分 : 58.5",   # 英文冒号有空格
    "GMHI评分：58.5",    # 中文冒号无空格
    "GMHI评分 ： 58.5",  # 中文冒号有空格
]

pattern = r"GMHI[评分]*[：:]?\s*([\d.]+)"

print('=== 测试不同冒号格式 ===')
for test in test_cases:
    match = re.search(pattern, test, re.IGNORECASE)
    print(f"输入: '{test}'")
    print(f"匹配: {'成功' if match else '失败'}")
    if match:
        print(f"  值: {match.group(1)}")
    print()

# 检查实际文本中的字符
text = "GMHI评分 : 58.5"
print('\n=== 检查字符编码 ===')
for i, char in enumerate(text):
    print(f"位置{i}: '{char}' (Unicode: U+{ord(char):04X})")

# 测试菌群多样性模式
print('\n=== 测试菌群多样性模式 ===')
diversity_patterns = [
    r"(?:菌群)?多样性[：:]?\s*([\d.]+)",
    r"(?:菌群)?多样性[\s：:]+\s*([\d.]+)",  # 修改后的模式
]

test_text = "菌群多样性 : 2.7578"
for i, pattern in enumerate(diversity_patterns):
    match = re.search(pattern, test_text, re.IGNORECASE)
    print(f"模式{i+1}: '{pattern}'")
    print(f"匹配: {'成功' if match else '失败'}")
    if match:
        print(f"  值: {match.group(1)}")
