#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查真实PDF的页面标记格式"""

import sys
sys.path.insert(0, '.')

import pdfplumber

if len(sys.argv) != 2:
    print("用法: python check_page_markers.py <PDF文件路径>")
    sys.exit(1)

pdf_path = sys.argv[1]

print('=== 检查真实PDF的页面标记格式 ===\n')

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if text:
            full_text += f"第{i}页\n{text}\n\n"

# 查找所有可能的页面标记
import re

# 查找所有"第X页"格式
page_markers = re.findall(r'第\s*\d+\s*页', full_text)
print(f'找到的页面标记: {set(page_markers)}')

# 查找包含"菌属"的文本位置
if "菌属" in full_text:
    print('\n✓ 找到"菌属"关键词')
    # 提取附近内容
    idx = full_text.find("菌属")
    print(f'上下文（前200字符）:\n{repr(full_text[max(0,idx-200):idx+200])}')
else:
    print('\n✗ 未找到"菌属"关键词')

# 查找包含"十五种菌属"的文本
if "十五种菌属" in full_text:
    print('\n✓ 找到"十五种菌属"')
    idx = full_text.find("十五种菌属")
    print(f'上下文:\n{repr(full_text[max(0,idx-100):idx+500])}')
else:
    print('\n✗ 未找到"十五种菌属"')

# 查找包含"Top15"或"Top 15"的文本
if "Top15" in full_text or "Top 15" in full_text or "top15" in full_text:
    print('\n✓ 找到Top15标记')
else:
    print('\n✗ 未找到Top15标记')

# 打印前10页的部分内容来了解格式
print('\n\n=== 前3页内容片段 ===')
pages = full_text.split("第")
for i in range(1, min(4, len(pages))):
    if pages[i]:
        print(f'\n--- 第{i}页片段 ---')
        # 找到第一个换行之前的内容
        first_line = pages[i].split('\n')[0][:100]
        print(first_line)