#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试真实PDF的文本格式"""

import re

# 真实PDF提取的文本片段
real_text = """----- 第12页 -----
人 体 肠 道 菌 群 检 测 报 告
10.2 肠道菌群属级水平分布
您其中占比最高的十五种菌属依次为：普雷沃菌
属 9 型（Prevotella_9, 26.90%），梭杆菌属
（Fusobacterium,13.32%），毛梭菌属（L
achnoclostridium,10.19%），拟杆菌属（Bacteroides,9.16%），
埃希氏菌-志贺氏菌（Escherichia-Shigella, 5.55%），巨单胞菌属（Megamonas, 4.02%），萨特菌属
（Sutterella,3.30%），粪杆菌属（Faecalibacterium,2.36%），普雷沃菌属（Prevotella,2.24%），严
格梭菌1型（Clostridiumsensustricto1, 2.06%），丁酸球菌属（Butyricicoccus, 1.42%），瘤胃球菌
扭链群（[Ruminococcus] torques group, 1.10%），布劳特氏菌属（Blautia, 0.95%），副拟杆菌属
（Parabacteroides, 0.81%），毛螺旋菌属（Lachnospira, 0.48%）。
地址：安徽省合肥市庐阳区临泉路7266号安创大楼 客
服支持：400-158-"""

print('=== 测试正则表达式 ===')

# 当前的正则表达式
genus_pattern = r"[，,\s、]*([^（\(\n]+?)\s*[（\(][^,]+,\s*([\d.]+)%[）\)]"
matches = re.findall(genus_pattern, real_text)
print(f'当前正则匹配结果: {len(matches)} 个')
for m in matches[:3]:
    print(f'  {m}')

# 修改后的正则表达式，支持换行符
genus_pattern2 = r"[，,\s、]*([^（\(\n]+?)\s*[（\(][^,]+,\s*([\d.]+)%[）\)]"
# 替换\n为空格
real_text_cleaned = real_text.replace('\n', ' ')
matches2 = re.findall(genus_pattern2, real_text_cleaned)
print(f'\n清理换行后匹配结果: {len(matches2)} 个')
for m in matches2[:3]:
    print(f'  {m}')

# 测试原始模式能否匹配"您其中占比最高的十五种菌属依次为"
pattern = r"第12页.*?您其中占比最高的十五种菌属依次为：(.*?)(?=第13页|----- 第|$)"
match = re.search(pattern, real_text, re.DOTALL)
if match:
    print(f'\n✓ 页面标记匹配成功')
    section = match.group(1)
    print(f'匹配到的内容长度: {len(section)}')
    # 清理换行后再次匹配
    section_cleaned = section.replace('\n', ' ')
    matches3 = re.findall(genus_pattern, section_cleaned)
    print(f'清理后匹配到 {len(matches3)} 个菌属')
else:
    print(f'\n✗ 页面标记匹配失败')
    # 尝试更简单的模式
    pattern2 = r"第12页.*?(?:您其中)?占比最高的十五种菌属依次为：(.*)"
    match2 = re.search(pattern2, real_text, re.DOTALL)
    if match2:
        print(f'简化模式匹配成功，内容: {match2.group(1)[:100]}...')
