#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""端到端测试：模拟真实使用场景"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print('=== 端到端测试开始 ===')

try:
    print('1. 导入模块...')
    from pdf_parser import parse_report_pdf
    from report_generator_v2 import generate_report_v2 as generate_report
    print('   ✓ 模块导入成功')
    
    # 查找测试PDF文件
    print('\n2. 查找测试PDF文件...')
    pdf_files = []
    for f in os.listdir('.'):
        if f.endswith('.pdf') and not f.startswith('test_') and not f.startswith('debug_'):
            pdf_files.append(f)
    
    if not pdf_files:
        print('   ✗ 未找到PDF文件，使用模拟数据测试')
        # 使用模拟数据
        test_data = {
            'basic_info': {'name': '测试用户', 'gender': '男', 'age': '30'},
            'test_info': {},
            'report_info': {},
            'core_indices': [
                {'name': 'GMHI评分', 'result': '58.5', 'description': '肠道健康指数'},
                {'name': '菌群多样性', 'result': '2.7578', 'description': '菌群丰富度指标'},
                {'name': '肠道年龄', 'result': '52岁', 'description': '肠道生理年龄'},
                {'name': '肠型', 'result': 'B型', 'description': '拟杆菌型'},
                {'name': 'B/E比值', 'result': '1.17', 'description': '菌群平衡指标'},
            ],
            'phylum_distribution': [
                {'name': '厚壁菌门', 'ratio': '39.11%'},
                {'name': '拟杆菌门', 'ratio': '36.8%'},
                {'name': '变形菌门', 'ratio': '3.89%'},
                {'name': '放线菌门', 'ratio': '2.08%'},
                {'name': '梭杆菌门', 'ratio': '0.47%'},
            ],
            'genus_distribution': [
                {'name': '普雷沃菌属', 'ratio': '26.90%', 'category': '中性菌'},
                {'name': '拟杆菌属', 'ratio': '10.21%', 'category': '中性菌'},
                {'name': '粪杆菌属', 'ratio': '8.56%', 'category': '有益菌'},
                {'name': '双歧杆菌属', 'ratio': '6.32%', 'category': '有益菌'},
                {'name': '罗斯氏菌属', 'ratio': '5.89%', 'category': '有益菌'},
                {'name': '瘤胃球菌属', 'ratio': '4.65%', 'category': '中性菌'},
                {'name': '真杆菌属', 'ratio': '3.21%', 'category': '中性菌'},
                {'name': '梭菌属', 'ratio': '2.87%', 'category': '有害菌'},
                {'name': '阿克曼菌属', 'ratio': '2.15%', 'category': '有益菌'},
                {'name': '链球菌属', 'ratio': '1.89%', 'category': '中性菌'},
                {'name': '韦荣球菌属', 'ratio': '1.56%', 'category': '中性菌'},
                {'name': '乳杆菌属', 'ratio': '1.34%', 'category': '有益菌'},
                {'name': '肠球菌属', 'ratio': '1.12%', 'category': '有害菌'},
                {'name': '大肠杆菌属', 'ratio': '0.98%', 'category': '有害菌'},
                {'name': '克雷伯菌属', 'ratio': '0.76%', 'category': '有害菌'},
            ],
            'beneficial_bacteria': [],
            'harmful_bacteria': [],
            'be_ratio': {},
            'ai_conclusion': '测试结论',
        }
        
        print('\n3. 生成报告...')
        output_path = 'test_e2e_report.pdf'
        generate_report(test_data, output_path)
        print(f'   ✓ 报告生成成功: {output_path}')
        
    else:
        print(f'   ✓ 找到 {len(pdf_files)} 个PDF文件')
        
        for pdf_path in pdf_files[:1]:  # 只测试第一个
            print(f'\n3. 解析PDF: {pdf_path}')
            data = parse_report_pdf(pdf_path)
            print(f'   ✓ PDF解析成功')
            print(f'   - 基本信息: {data.get("basic_info", {})}')
            print(f'   - 核心指标数量: {len(data.get("core_indices", []))}')
            print(f'   - 门级分布数量: {len(data.get("phylum_distribution", []))}')
            print(f'   - 属级分布数量: {len(data.get("genus_distribution", []))}')
            
            print('\n4. 生成报告...')
            base_name = os.path.splitext(pdf_path)[0]
            output_path = f'{base_name}_报告.pdf'
            generate_report(data, output_path)
            print(f'   ✓ 报告生成成功: {output_path}')
    
    print('\n=== 端到端测试完成 ===')
    
except Exception as e:
    print(f'\n✗ 错误: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
