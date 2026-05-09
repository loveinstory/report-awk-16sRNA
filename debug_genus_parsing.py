#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试属级分布解析问题"""

import sys
import os
sys.path.insert(0, '.')

import pdfplumber

# 查找PDF文件
pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and not f.startswith('test_')]

if not pdf_files:
    print('未找到PDF文件，使用模拟数据')
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
else:
    pdf_path = pdf_files[0]
    print(f'读取PDF: {pdf_path}')
    with pdfplumber.open(pdf_path) as pdf:
        test_text = ''
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                test_text += f'=== 第{page.page_number}页 ===\n{text}\n\n'

print('=== 原始文本预览 ===')
print(test_text[:2000])
print('\n' + '='*50 + '\n')

# 测试解析
from pdf_parser import parse_genus_distribution

result = parse_genus_distribution(test_text)
print(f'解析结果: 找到 {len(result)} 个菌属')
for item in result:
    print(f"  {item['rank']}. {item['name']} - {item['ratio']} - {item['category']}")

# 检查乱码问题
print('\n=== 检查可能的乱码 ===')
for item in result:
    # 检查是否包含非中文字符
    if any(ord(c) > 127 and (ord(c) < 0x4e00 or ord(c) > 0x9fff) for c in item['name']):
        print(f"  警告: {item['name']} 可能包含乱码")
        print(f"        原始字符: {[hex(ord(c)) for c in item['name']]}")
