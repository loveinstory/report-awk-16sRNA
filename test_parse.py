from pdf_parser import parse_report_pdf

# 测试解析功能
pdf_path = r'C:\Users\Administrator\Desktop\AWK-OCR\功能医学检测报告模板（2026.4.3）\P01\人体肠道菌群检测原始报告.pdf'

try:
    data = parse_report_pdf(pdf_path)
    
    print('=== 解析结果 ===')
    print('\n--- 基本信息 ---')
    print('姓名:', data['basic_info'].get('name', '未识别'))
    print('性别:', data['basic_info'].get('gender', '未识别'))
    print('年龄:', data['basic_info'].get('age', '未识别'))
    print('电话:', data['basic_info'].get('phone', '未识别'))
    print('症状:', data['basic_info'].get('symptoms', '未识别'))
    
    print('\n--- 检测信息 ---')
    print('单位:', data['test_info'].get('unit', '未识别'))
    print('样本编号:', data['test_info'].get('sample_id', '未识别'))
    print('样本类型:', data['test_info'].get('sample_type', '未识别'))
    print('采样日期:', data['test_info'].get('sample_date', '未识别'))
    print('检测方法:', data['test_info'].get('method', '未识别'))
    
    print('\n--- 核心指标 ---')
    for idx in data['core_indices']:
        print(f"  {idx.get('name')}: {idx.get('result')}")
    
    print('\n--- 门级分布 ---')
    for phylum in data['phylum_distribution'][:5]:
        print(f"  {phylum.get('name')}: {phylum.get('ratio')}")
    
    print('\n--- 属级分布 ---')
    for genus in data['genus_distribution'][:5]:
        print(f"  {genus.get('name')}: {genus.get('ratio')}")
    
    print('\n✓ 解析成功！')
except Exception as e:
    print(f'✗ 解析失败: {e}')
    import traceback
    traceback.print_exc()
