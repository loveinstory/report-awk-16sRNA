#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""端到端调试数据解析"""

import sys
sys.path.insert(0, '.')
from pdf_parser import parse_core_indices
from report_generator_v2 import build_page2

# 模拟用户报告中的数据格式
test_text = """
核心指标
GMHI评分: 58.5
菌群多样性: 2.7578
肠道年龄: 52岁
肠型: B型 拟杆菌型
B/E比值: 1.17

菌群分布
门级水平分布
厚壁菌门 39.11%
拟杆菌门 36.8%
变形菌门 3.89%
放线菌门 2.08%
梭杆菌门 0.47%

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

print('=== 解析核心指标 ===')
indices = parse_core_indices(test_text)
print(f'解析结果: {indices}')

# 构建测试数据
test_data = {
    'basic_info': {'name': '测试用户', 'gender': '男', 'age': '30'},
    'test_info': {},
    'report_info': {},
    'core_indices': indices,
    'phylum_distribution': [
        {'name': '厚壁菌门', 'ratio': '39.11%'},
        {'name': '拟杆菌门', 'ratio': '36.8%'},
        {'name': '变形菌门', 'ratio': '3.89%'},
        {'name': '放线菌门', 'ratio': '2.08%'},
        {'name': '梭杆菌门', 'ratio': '0.47%'},
    ],
    'genus_distribution': [
        {'name': '普雷沃菌属', 'ratio': '26.90%'},
        {'name': '拟杆菌属', 'ratio': '10.21%'},
        {'name': '粪杆菌属', 'ratio': '8.56%'},
        {'name': '双歧杆菌属', 'ratio': '6.32%'},
        {'name': '罗斯氏菌属', 'ratio': '5.89%'},
        {'name': '瘤胃球菌属', 'ratio': '4.65%'},
        {'name': '真杆菌属', 'ratio': '3.21%'},
        {'name': '梭菌属', 'ratio': '2.87%'},
        {'name': '阿克曼菌属', 'ratio': '2.15%'},
        {'name': '链球菌属', 'ratio': '1.89%'},
        {'name': '韦荣球菌属', 'ratio': '1.56%'},
        {'name': '乳杆菌属', 'ratio': '1.34%'},
        {'name': '肠球菌属', 'ratio': '1.12%'},
        {'name': '大肠杆菌属', 'ratio': '0.98%'},
        {'name': '克雷伯菌属', 'ratio': '0.76%'},
    ],
}

print('\n=== 构建页面2 ===')
html = build_page2(test_data)

# 检查变量是否正确替换
print('\n=== 检查替换结果 ===')
print('菌群多样性值 2.7578是否在HTML中:', '2.7578' in html)
print('默认值 2.68是否在HTML中:', '2.68' in html)
print('肠道年龄 52是否在HTML中:', '52' in html)
print('默认值 42是否在HTML中:', '42' in html)

# 统计出现次数
print('\n=== 统计数值出现次数 ===')
print(f"2.7578 出现次数: {html.count('2.7578')}")
print(f"2.68 出现次数: {html.count('2.68')}")
print(f"52 出现次数: {html.count('52')}")
print(f"42 出现次数: {html.count('42')}")

# 保存HTML
with open('debug_full.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\n已保存调试文件: debug_full.html')

# 生成PDF
from weasyprint import HTML
try:
    HTML(string=html).write_pdf('debug_full.pdf')
    print('PDF生成成功: debug_full.pdf')
except Exception as e:
    print(f'PDF生成失败: {e}')
