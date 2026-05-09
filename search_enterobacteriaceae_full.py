import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 搜索所有页面中包含"埃希氏菌"、"志贺氏菌"、"克雷伯氏菌"、"肠杆菌"等肠杆菌科属的数据
    enterobacteriaceae_genera = ['埃希氏菌', '志贺氏菌', '克雷伯氏菌', '肠杆菌属', '变形菌', '柠檬酸杆菌', '沙雷氏菌']
    
    total_enterobacteriaceae = 0.0
    found_genera = []
    
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                for genus in enterobacteriaceae_genera:
                    if genus in line and '%' in line:
                        # 提取数字
                        import re
                        match = re.search(r'([\d.]+)%', line)
                        if match:
                            value = float(match.group(1))
                            total_enterobacteriaceae += value
                            found_genera.append((genus, value, i+1))
    
    print('=== 肠杆菌科各属数据 ===')
    for genus, value, page_num in found_genera:
        print(f'  {genus}: {value}% (第{page_num}页)')
    
    print(f'\n肠杆菌科总计: {total_enterobacteriaceae}%')
    print(f'双歧杆菌属: 0.0006%')
    print(f'B/E比值: {0.0006 / total_enterobacteriaceae if total_enterobacteriaceae > 0 else "N/A"}')
