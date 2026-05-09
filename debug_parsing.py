import pdfplumber

# 读取PDF并显示文本内容
pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 显示前几页的内容
    for i, page in enumerate(pdf.pages[:5], 1):
        text = page.extract_text()
        if text:
            print(f'=== 第{i}页 ===')
            lines = text.split('\n')[:30]  # 只显示前30行
            for j, line in enumerate(lines):
                print(f'{j+1:2d}: {line}')
            print('...')
            print()
