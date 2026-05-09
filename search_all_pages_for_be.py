import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 搜索包含"杆菌"或"科"的页面
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            # 检查是否有数值和杆菌相关的内容
            if ('杆菌' in text or '科' in text) and any(c.isdigit() for c in text):
                lines = text.split('\n')
                for line in lines:
                    if '杆菌' in line and '%' in line:
                        print(f'第{i+1}页: {repr(line)}')
