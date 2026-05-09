#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""详细检查PDF文本提取格式"""

import sys
sys.path.insert(0, '.')

import pdfplumber

if len(sys.argv) != 2:
    print("用法: python inspect_pdf_text.py <PDF文件路径>")
    sys.exit(1)

pdf_path = sys.argv[1]

print('=== 详细检查PDF文本提取 ===\n')

with pdfplumber.open(pdf_path) as pdf:
    # 检查每一页的文本
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if text and "菌属" in text:
            print(f'第{i}页包含"菌属"关键词')
            print(f'该页文本长度: {len(text)}')
            print(f'该页文本内容（前1000字符）:')
            print('='*50)
            print(text[:1000])
            print('='*50)

            # 查找"第12页"的位置
            if "第12页" in text:
                print('\n✓ 该页包含"第12页"')
                idx = text.find("第12页")
                print(f'上下文: {repr(text[max(0,idx-20):idx+200])}')
            elif "第 12 页" in text or "第12 " in text:
                print('\n找到变体页面标记')

            # 查找菌属相关内容
            if "十五种菌属" in text:
                idx = text.find("十五种菌属")
                print(f'\n找到"十五种菌属"，上下文:')
                print(repr(text[max(0,idx-50):idx+300]))

            break

# 另外测试合并所有文本后的情况
print('\n\n=== 合并所有页面后的文本 ===')
full_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if text:
            full_text += f"\n----- 第{i}页 -----\n{text}"

# 在合并文本中查找
if "第12页" in full_text:
    print('✓ 合并后包含"第12页"')
    idx = full_text.find("第12页")
    print(f'上下文: {repr(full_text[max(0,idx-30):idx+400])}')
else:
    print('✗ 合并后不包含"第12页"')

if "第 12 页" in full_text:
    print('\n✓ 合并后包含"第 12 页"（有空格）')
    idx = full_text.find("第 12 页")
    print(f'上下文: {repr(full_text[max(0,idx-30):idx+400])}')
