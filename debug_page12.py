import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 查看第12页（索引为11）- 属级水平分布
    page = pdf.pages[11]
    text = page.extract_text()
    if text:
        print('=== 第12页 - 属级水平分布 ===')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            print(f'{i+1:2d}: {repr(line)}')
