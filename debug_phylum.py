import re

# 模拟PDF中的门级分布文本（包含换行）
text = """您其中占比最高的五种菌门依次为：拟杆菌门（Bacteroidota, 39.11%），厚壁菌门（Firmicutes,
33.30%），梭杆菌门（Fusobacteriota, 13.32%），变形菌门（Proteobacteria, 11.3
1%），放线菌门（Actinobacteriota, 0.26%）。"""

print("原始文本:")
print(text)
print("\n" + "="*50 + "\n")

# 测试正则表达式
page11_pattern = r"占比最高的五种菌门依次为：(.+?)(?=。|\n|$)"
match_11 = re.search(page11_pattern, text, re.DOTALL)
if match_11:
    section_text = match_11.group(1)
    print("匹配到的section_text:")
    print(repr(section_text))
    print("\n")
    
    # 匹配格式：拟杆菌门（Bacteroidota, 39.11%）
    phylum_pattern = r"([^（\(\n,，]+?)[（\(][^,]+,\s*([\d.]+)%[）\)]"
    matches = re.findall(phylum_pattern, section_text)
    print(f"找到 {len(matches)} 个匹配:")
    for i, match in enumerate(matches, 1):
        print(f"  {i}: {match}")
else:
    print("没有匹配到门级分布区域")
