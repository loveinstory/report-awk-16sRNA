import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 查看第6页（索引为5）- 肠型
    page = pdf.pages[5]
    text = page.extract_text()
    if text:
        print('=== 第6页 - 肠型 ===')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            print(f'{i+1:2d}: {repr(line)}')
    
    print('\n' + '='*50 + '\n')
    
    # 查看第8页（索引为7）- 肠龄
    page = pdf.pages[7]
    text = page.extract_text()
    if text:
        print('=== 第8页 - 肠龄 ===')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            print(f'{i+1:2d}: {repr(line)}')
