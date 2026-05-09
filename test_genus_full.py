from pdf_parser import parse_report_pdf

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

data = parse_report_pdf(pdf_path)

print('=== 属级分布完整列表 ===')
print(f'总数: {len(data["genus_distribution"])}种')
print()
for genus in data['genus_distribution']:
    print(f"{genus['rank']:2d}. {genus['name']}: {genus['ratio']} ({genus['category']})")

print('\n' + '='*50 + '\n')
print('=== 核心指标 ===')
for idx in data['core_indices']:
    print(f"  {idx.get('name')}: {idx.get('result')}")
