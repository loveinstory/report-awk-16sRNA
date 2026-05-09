import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 查看第10页（索引为9）- 双歧杆菌属/肠杆菌科指数
    page = pdf.pages[9]
    text = page.extract_text()
    if text:
        print('=== 第10页 - 双歧杆菌属/肠杆菌科指数 ===')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            print(f'{i+1:2d}: {repr(line)}')
    
    # 查看第13页（有益菌检测）
    print('\n' + '='*50 + '\n')
    page = pdf.pages[12]
    text = page.extract_text()
    if text:
        print('=== 第13页 - 有益菌检测 ===')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            print(f'{i+1:2d}: {repr(line)}')
    
    # 查看有害菌检测页面
    print('\n' + '='*50 + '\n')
    page = pdf.pages[14]
    text = page.extract_text()
    if text:
        print('=== 第15页 - 有害菌检测 ===')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            print(f'{i+1:2d}: {repr(line)}')
