import re
import pdfplumber

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[3]  # 第4页
    text = page.extract_text()
    
print('=== 原始文本 ===')
print(repr(text))
print('\n' + '='*50 + '\n')

# 清理文本
search_text = re.sub(r'[ \t]+', ' ', text)
search_text = re.sub(r'\n+', '\n', search_text)

print('=== 清理后的文本 ===')
print(repr(search_text))
print('\n' + '='*50 + '\n')

# 测试各个模式
gmhi_patterns = [
    r"GMHI[评分]*[\s：:]+\s*([\d.]+)",
    r"GMHI\s+([\d.]+)",
    r"肠道健康指数[\s：:]+\s*([\d.]+)",
    # 支持第4页的格式：GMHI<60分后面跟着单独一行的数值
    r"GMHI.*?\n\s*([\d.]+)\s*\n",
]

print('=== 测试GMHI模式 ===')
for i, pattern in enumerate(gmhi_patterns):
    match = re.search(pattern, search_text, re.IGNORECASE)
    print(f'模式{i+1}: {pattern}')
    print(f'  匹配结果: {match.group(1) if match else "未匹配"}')
