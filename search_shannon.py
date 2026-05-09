import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 搜索包含"Shannon"或"Chao1"或"ACE"或"多样性指数"的页面
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            if 'Shannon' in text or 'Chao' in text or 'ACE' in text or '多样性指数' in text:
                print(f'=== 第{i+1}页 ===')
                lines = text.split('\n')
                for j, line in enumerate(lines[:20]):
                    print(f'{j+1:2d}: {repr(line)}')
                print()
