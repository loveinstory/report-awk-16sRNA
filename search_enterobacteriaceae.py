import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 搜索包含"肠杆菌科"或"Enterobacteriaceae"的页面
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            if '肠杆菌科' in text or 'Enterobacteriaceae' in text:
                print(f'=== 第{i+1}页 ===')
                lines = text.split('\n')
                for j, line in enumerate(lines):
                    print(f'{j+1:2d}: {repr(line)}')
                print()
