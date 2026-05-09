import pdfplumber
import re

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 搜索所有页面中包含B/E或双歧杆菌/肠杆菌比值的内容
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            # 检查是否包含双歧杆菌或B/E相关内容
            if '双歧杆菌' in text or 'B/E' in text or '肠杆菌' in text:
                print(f'=== 第{i+1}页 ===')
                lines = text.split('\n')
                for j, line in enumerate(lines):
                    print(f'{j+1:2d}: {repr(line)}')
                print()
