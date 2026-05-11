from pdf_parser import parse_report_pdf
from report_generator_v2 import build_page1, build_page2, build_page3, build_page4, build_page5
import os

pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

try:
    # 解析PDF
    print('正在解析PDF...')
    data = parse_report_pdf(pdf_path)
    
    # 生成页面
    print('正在生成页面1...')
    page1 = build_page1(data)
    
    print('正在生成页面2...')
    page2 = build_page2(data)
    
    print('正在生成页面3...')
    page3 = build_page3(data)
    
    print('正在生成页面4...')
    page4 = build_page4(data)
    
    print('正在生成页面5...')
    page5 = build_page5(data)
    
    # 保存测试输出
    output_dir = 'test_output'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'page1.html'), 'w', encoding='utf-8') as f:
        f.write(page1)
    
    with open(os.path.join(output_dir, 'page2.html'), 'w', encoding='utf-8') as f:
        f.write(page2)
    
    with open(os.path.join(output_dir, 'page3.html'), 'w', encoding='utf-8') as f:
        f.write(page3)
    
    with open(os.path.join(output_dir, 'page4.html'), 'w', encoding='utf-8') as f:
        f.write(page4)
    
    with open(os.path.join(output_dir, 'page5.html'), 'w', encoding='utf-8') as f:
        f.write(page5)
    
    print('\n=== 解析结果摘要 ===')
    print('基本信息:')
    print(f'  姓名: {data["basic_info"].get("name", "未识别")}')
    print(f'  性别: {data["basic_info"].get("gender", "未识别")}')
    print(f'  年龄: {data["basic_info"].get("age", "未识别")}')
    print(f'  电话: {data["basic_info"].get("phone", "未识别")}')
    print(f'  症状: {data["basic_info"].get("symptoms", "未识别")}')
    
    print('\n检测信息:')
    print(f'  单位: {data["test_info"].get("unit", "未识别")}')
    print(f'  样本编号: {data["test_info"].get("sample_id", "未识别")}')
    print(f'  样本类型: {data["test_info"].get("sample_type", "未识别")}')
    print(f'  采样日期: {data["test_info"].get("sample_date", "未识别")}')
    print(f'  检测方法: {data["test_info"].get("method", "未识别")}')
    
    print('\n核心指标:')
    for idx in data['core_indices']:
        print(f'  {idx.get("name")}: {idx.get("result")}')
    
    print('\n门级分布:')
    for phylum in data['phylum_distribution'][:5]:
        print(f'  {phylum.get("name")}: {phylum.get("ratio")}')
    
    print('\n属级分布:')
    for genus in data['genus_distribution'][:5]:
        print(f'  {genus.get("name")}: {genus.get("ratio")}')
    
    print('\n✓ 报告生成成功！')
    
except Exception as e:
    print(f'✗ 失败: {e}')
    import traceback
    traceback.print_exc()
