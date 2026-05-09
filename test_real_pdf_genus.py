#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""完整测试真实PDF解析"""

import sys
sys.path.insert(0, '.')

import pdfplumber
from pdf_parser import parse_genus_distribution

pdf_path = "C:\\Users\\Administrator\\Desktop\\AWK-OCR\\功能医学检测报告模板（2026.4.3）\\P01\\人体肠道菌群检测原始报告.pdf"

print('=== 完整测试真实PDF解析 ===\n')

# 1. 读取PDF文本
full_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if text:
            full_text += f"\n----- 第{i}页 -----\n{text}"

print(f'合并后文本长度: {len(full_text)}')

# 2. 检查是否包含"第12页"
if "----- 第12页 -----" in full_text:
    print('✓ 包含"----- 第12页 -----"标记')
elif "第12页" in full_text:
    print('✓ 包含"第12页"标记')
    idx = full_text.find("第12页")
    print(f'上下文: {repr(full_text[idx:idx+100])}')
else:
    print('✗ 不包含"第12页"标记')

# 3. 检查菌属相关内容
if "您其中占比最高的十五种菌属依次为" in full_text:
    print('\n✓ 包含"您其中占比最高的十五种菌属依次为"')
    idx = full_text.find("您其中占比最高的十五种菌属依次为")
    print(f'上下文: {repr(full_text[idx:idx+200])}')
else:
    print('\n✗ 不包含该菌属描述')

# 4. 直接调用parse_genus_distribution
print('\n=== 调用parse_genus_distribution ===')
genus_data = parse_genus_distribution(full_text)
print(f'解析结果: {len(genus_data)} 个菌属')

if genus_data:
    for i, g in enumerate(genus_data, 1):
        print(f'{i}. {g.get("name")} - {g.get("ratio")}')
else:
    print('未能解析到任何菌属数据')
    # 手动测试正则匹配
    import re
    patterns = [
        r"第12页.*?您其中占比最高的十五种菌属依次为：(.*?)(?=第13页|----- 第|$)",
        r"第12页.*?占比最高的十五种菌属依次为：(.*?)(?=第13页|----- 第|$)",
    ]
    for p in patterns:
        m = re.search(p, full_text, re.DOTALL)
        if m:
            print(f'✓ 模式匹配成功: {p[:50]}...')
            section = m.group(1)[:200]
            print(f'内容片段: {repr(section)}')
            break
        else:
            print(f'✗ 模式失败: {p[:50]}...')
