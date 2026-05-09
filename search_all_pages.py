import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 搜索所有页面中包含数字和比值相关的内容
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            # 检查是否包含数字和可能的比值格式
            if any(char.isdigit() for char in text) and ('/' in text or '比' in text or '指数' in text):
                # 检查是否有类似比值的模式
                lines = text.split('\n')
                for line in lines[:15]:  # 只检查前15行
                    if '/' in line and any(c.isdigit() for c in line):
                        print(f'=== 第{i+1}页 ===')
                        print(f'匹配行: {repr(line)}')
                        print()
