from pdf_parser import parse_report_pdf

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

data = parse_report_pdf(pdf_path)

print('=== B/E比值计算调试 ===')
print('parse_be_ratio结果:', data.get('be_ratio', {}))
print()

# 检查核心指标中是否有B/E比值
print('=== 核心指标 ===')
for idx in data.get('core_indices', []):
    name = idx.get('name', '')
    if 'B/E' in name or '双歧杆菌' in name:
        print(f'  {name}: {idx.get("result")}')

# 检查有益菌数据
print('\n=== 有益菌数据 ===')
for b in data.get('beneficial_bacteria', []):
    print(f'  {b.get("name")}: {b.get("ratio")}')

# 检查有害菌数据
print('\n=== 有害菌数据 ===')
for h in data.get('harmful_bacteria', []):
    print(f'  {h.get("name")}: {h.get("ratio")}')
