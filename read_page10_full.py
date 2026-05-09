import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # 查看第10页（索引为9）- 双歧杆菌属/肠杆菌科指数
    page = pdf.pages[9]
    text = page.extract_text()
    if text:
        print('=== 第10页完整内容 ===')
        print(text)
        print()
        
    # 也查看第11页，可能数据跨页
    page = pdf.pages[10]
    text = page.extract_text()
    if text:
        print('=== 第11页完整内容 ===')
        print(text)
