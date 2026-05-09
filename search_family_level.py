import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 搜索所有页面中包含"科"和数字的行
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                if '科' in line and '%' in line:
                    print(f'第{i+1}页: {repr(line)}')
