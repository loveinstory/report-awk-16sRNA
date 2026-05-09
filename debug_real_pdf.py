#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试真实PDF解析流程"""

import sys
sys.path.insert(0, '.')

import pdfplumber
from pdf_parser import parse_genus_distribution, parse_report_pdf

# 检查命令行参数
if len(sys.argv) != 2:
    print("用法: python debug_real_pdf.py <PDF文件路径>")
    sys.exit(1)

pdf_path = sys.argv[1]

print('=== 调试真实PDF解析 ===')

# 步骤1: 读取PDF文本
print('\n步骤1 - 读取PDF文本')
try:
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n\n"
    print(f'✓ 成功读取PDF，总字符数: {len(full_text)}')
except Exception as e:
    print(f'✗ 读取PDF失败: {e}')
    sys.exit(1)

# 步骤2: 检查是否包含第12页内容
print('\n步骤2 - 检查第12页内容')
if "第12页" in full_text:
    print('✓ 包含第12页标记')
    
    # 提取第12页附近的内容
    start = full_text.find("第12页")
    end = full_text.find("第13页", start)
    if end == -1:
        end = start + 2000  # 取2000字符
    
    page12_content = full_text[start:min(end, start+2000)]
    print(f'第12页内容片段（前500字符）:')
    print(repr(page12_content[:500]))
else:
    print('✗ 未找到第12页标记')

# 步骤3: 解析菌属分布
print('\n步骤3 - 解析菌属分布')
genus_data = parse_genus_distribution(full_text)
print(f'解析结果数量: {len(genus_data)}')

if genus_data:
    print('解析结果:')
    for i, item in enumerate(genus_data, 1):
        print(f'{i}. {item.get("name", "")} - {item.get("ratio", "")} - {item.get("category", "")}')
else:
    print('✗ 未解析到任何菌属数据')

# 步骤4: 使用完整解析函数
print('\n步骤4 - 使用完整解析函数')
try:
    full_data = parse_report_pdf(pdf_path)
    genus_dist = full_data.get("genus_distribution", [])
    print(f'完整解析的菌属数量: {len(genus_dist)}')
    
    if genus_dist:
        print('菌属数据:')
        for i, item in enumerate(genus_dist, 1):
            print(f'{i}. {item.get("name", "")} - {item.get("ratio", "")}')
    else:
        print('✗ 完整解析未返回菌属数据')
except Exception as e:
    print(f'✗ 完整解析失败: {e}')
    import traceback
    traceback.print_exc()
