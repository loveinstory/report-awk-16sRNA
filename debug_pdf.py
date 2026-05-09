"""
PDF内容调试工具
用于查看PDF提取的原始文本内容，帮助优化解析规则
"""
import pdfplumber
import sys


def debug_pdf(pdf_path: str):
    """打印PDF提取的原始文本内容"""
    print("=" * 80)
    print(f"PDF文件: {pdf_path}")
    print("=" * 80)
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            print(f"\n{'='*40}")
            print(f"第 {i} 页")
            print(f"{'='*40}\n")
            
            text = page.extract_text()
            if text:
                print(text)
            else:
                print("[该页无文本内容]")
    
    print("\n" + "=" * 80)
    print("调试信息输出完成")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python debug_pdf.py <pdf文件路径>")
        print("示例: python debug_pdf.py D:\\样本报告.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    debug_pdf(pdf_path)
