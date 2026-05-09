#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试修复IndexError问题"""

import sys
sys.path.insert(0, '.')

from pdf_parser import parse_core_indices

# 测试各种边界情况
test_cases = [
    # 正常情况
    """核心指标
GMHI评分：58.5
菌群多样性：2.7578
肠道年龄：52岁
肠型：B型
B/E比值：1.17

菌群分布""",
    
    # 没有核心指标标题
    """检测报告
GMHI评分：58.5
菌群多样性：2.7578
肠道年龄：52岁
肠型：B型
B/E比值：1.17""",
    
    # 只有GMHI和B/E比值
    """GMHI评分：58.5
B/E比值：1.17""",
    
    # 空文本
    "",
    
    # 只有标题没有内容
    """核心指标""",
]

print('=== 测试修复IndexError问题 ===\n')

for i, test_text in enumerate(test_cases):
    print(f'测试用例{i+1}:')
    print(f'输入文本长度: {len(test_text)}')
    
    try:
        result = parse_core_indices(test_text)
        print(f'解析成功，找到 {len(result)} 个指标')
        for item in result:
            print(f'  - {item["name"]}: {item["result"]}')
    except Exception as e:
        print(f'✗ 解析失败: {type(e).__name__}: {e}')
    
    print()

print('=== 测试完成 ===')
