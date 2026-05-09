#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试真实PDF解析流程"""

import sys
sys.path.insert(0, '.')

# 模拟真实PDF中的文本提取结果（可能有各种格式问题）
real_pdf_text = """
本检测报告包含以下内容：

核心指标

GMHI评分 : 58.5 
菌群多样性 : 2.7578  
肠道年龄 : 52岁
肠型 : B型 

B/E比值 : 1.17

检测日期：2024年1月15日

菌群分布

门级水平分布

1 厚壁菌门 39.11%

2 拟杆菌门 36.8%

3 变形菌门 3.89%

4 放线菌门 2.08%

5 梭杆菌门 0.47%

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

"""

print('=== 模拟真实PDF文本 ===')
print(real_pdf_text[:500], '...')

# 解析PDF
from pdf_parser import parse_core_indices, parse_phylum_distribution, parse_genus_distribution

print('\n=== 解析核心指标 ===')
core_indices = parse_core_indices(real_pdf_text)
print(f'解析结果: {core_indices}')

print('\n=== 解析门级分布 ===')
phylum_dist = parse_phylum_distribution(real_pdf_text)
print(f'解析结果: {phylum_dist}')

print('\n=== 解析属级分布 ===')
genus_dist = parse_genus_distribution(real_pdf_text)
print(f'解析结果: {genus_dist}')
print(f'属级数量: {len(genus_dist)}')

# 构建报告数据
from report_generator_v2 import build_page2, generate_report_v2

test_data = {
    'basic_info': {'name': '测试用户', 'gender': '男', 'age': '30'},
    'test_info': {},
    'report_info': {},
    'core_indices': core_indices,
    'phylum_distribution': phylum_dist,
    'genus_distribution': genus_dist,
}

print('\n=== 构建页面2 ===')
html = build_page2(test_data)

# 检查关键值
print('\n=== 验证结果 ===')
print(f"菌群多样性 2.7578: {'2.7578' in html}")
print(f"肠道年龄 52: {'52' in html}")
print(f"肠型 B型: {'B型' in html}")
print(f"B/E比值 1.17: {'1.17' in html}")

# 保存并生成PDF
with open('test_real_parse.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\n已保存测试文件: test_real_parse.html')

from weasyprint import HTML
try:
    HTML(string=html).write_pdf('test_real_parse.pdf')
    print('PDF生成成功: test_real_parse.pdf')
except Exception as e:
    print(f'PDF生成失败: {e}')

print('\n=== 检查具体数值 ===')
# 提取卡片值
import re
diversity_match = re.search(r'mini-card-value">([\d.]+)<', html)
gut_age_match = re.search(r'mini-card-value">(\d+)<span style="font-size:8px">岁</span>', html)

print(f"菌群多样性值: {diversity_match.group(1) if diversity_match else '未找到'}")
print(f"肠道年龄值: {gut_age_match.group(1) if gut_age_match else '未找到'}")
