#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试属级分布解析逻辑"""

import sys
import re
sys.path.insert(0, '.')

# 模拟原始报告第12页的属级分布数据
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

# 测试section_patterns
section_patterns = [
    r"属级?水平?分布.*?\n(.*?)(?=3\.1|有益菌|有害菌|$)",
    r"2\.2.*?\n(.*?)(?=3\.|有益菌|有害菌|$)",
    r"肠道菌群属水平分布.*?\n(.*?)(?=有益菌|有害菌|$)",
    r"Top.*?菌属.*?\n(.*?)(?=排名|3\.|$)",
    r"优势菌属.*?\n(.*?)(?=有益菌|有害菌|$)",
    r"菌群组成.*?\n(.*?)(?=3\.|有益菌|$)",
    r"相对丰度.*?\n(.*?)(?=门|科|有益菌|$)",
    r"主要菌属.*?\n(.*?)(?=有益菌|有害菌|$)",
    r"第12页.*?\n(.*?)(?=第13页|$)",
    r"菌属.*?\n(.*?)(?=\d+\.|排名|$)",
    r"(\d+\s+.+?菌属\s+[\d.]+%?.*?)(?=\n\d+\s+|$)",
]

print('=== 测试section_patterns ===')
for i, pattern in enumerate(section_patterns):
    match = re.search(pattern, test_text, re.DOTALL | re.IGNORECASE)
    if match:
        print(f'模式{i+1}匹配成功:')
        print(f'匹配内容:\n{repr(match.group(1)[:200])}...')
        print()

# 测试逐行匹配
print('=== 测试逐行匹配 ===')
lines = test_text.split('\n')
patterns = [
    r"(\d+)[\.\s、]+(.+?菌属)\s+([\d.]+)%?\s*(.*)",
    r"(\d+)[\.\s、]+(.+?)\s+([\d.]+)%?\s*(.*)",
    r"(.+?菌属)\s*[:：]\s*([\d.]+)%?",
    r"(.+?菌属)\s+([\d.]+)%?\s*(.*)",
    r"(.+?菌属)\s+([\d.]+)\s*$",
    r"(\d+)\s+(.+?菌属)\s+([\d.]+)\s*$",
    r"([\d.]+)%?\s+(.+?菌属)",
    r"(.+?菌属)\s*-\s*([\d.]+)%?",
    r"(\d+)\)\s+(.+?菌属)\s+([\d.]+)%?",
    r"(.+?菌属)\s+占比\s*([\d.]+)%?",
    r"(.+?菌属)\s+([\d.]+)\s+%",
    r"(\d+)[\.\s、]+(.+?菌属)\s+([\d.]+)\s+%",
]

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    for j, pattern in enumerate(patterns):
        match = re.match(pattern, line)
        if match:
            print(f'行: {line}')
            print(f'  模式{j+1}匹配成功')
            print(f'  分组: {match.groups()}')
            break
    else:
        print(f'行: {line}')
        print(f'  未匹配到任何模式')
    print()
