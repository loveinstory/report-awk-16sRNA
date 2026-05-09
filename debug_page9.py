import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 查看第9页（索引为8）- B/E比值
    page = pdf.pages[8]
    text = page.extract_text()
    if text:
        print('=== 第9页 - B/E比值 ===')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            print(f'{i+1:2d}: {repr(line)}')
