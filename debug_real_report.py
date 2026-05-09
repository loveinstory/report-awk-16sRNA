#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试实际PDF报告解析 - 详细日志记录"""

import sys
import os
import re

sys.path.insert(0, '.')

import pdfplumber
from pdf_parser import parse_report_pdf, parse_genus_distribution

def analyze_pdf(pdf_path):
    """分析PDF文件并记录详细日志"""
    print(f"=== 开始分析PDF: {pdf_path} ===")
    
    # 创建日志文件
    base_name = os.path.basename(pdf_path)
    log_file = f"debug_{base_name.replace('.pdf', '')}.log"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"===== PDF分析日志 =====\n")
        f.write(f"文件: {pdf_path}\n")
        f.write(f"时间: {os.path.getmtime(pdf_path)}\n\n")
        
        # 读取PDF内容
        with pdfplumber.open(pdf_path) as pdf:
            f.write(f"===== PDF页面信息 =====\n")
            f.write(f"总页数: {len(pdf.pages)}\n\n")
            
            # 逐页提取文本
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                f.write(f"===== 第{page_num}页 =====\n")
                if text:
                    f.write(f"文本长度: {len(text)}字符\n")
                    f.write(f"文本内容:\n{text}\n\n")
                    
                    # 检查是否包含菌属相关内容
                    if "菌属" in text:
                        f.write("*** 发现菌属相关内容 ***\n")
                        lines = text.split('\n')
                        for line in lines:
                            if "菌属" in line:
                                f.write(f"  菌属行: {line}\n")
                else:
                    f.write("无文本内容\n\n")
        
        # 解析完整报告
        f.write("\n===== 完整报告解析 =====\n")
        try:
            data = parse_report_pdf(pdf_path)
            
            # 记录属级分布
            f.write("\n===== 属级水平分布解析结果 =====\n")
            genus_list = data.get("genus_distribution", [])
            f.write(f"识别到 {len(genus_list)} 种菌属\n\n")
            
            for i, genus in enumerate(genus_list, 1):
                f.write(f"{i}. 名称: {genus.get('name', '')}\n")
                f.write(f"   排名: {genus.get('rank', '')}\n")
                f.write(f"   比例: {genus.get('ratio', '')}\n")
                f.write(f"   类别: {genus.get('category', '')}\n")
                f.write(f"   --- \n")
            
            # 检查是否缺少菌属
            expected_genus = [
                '普雷沃菌属', '拟杆菌属', '粪杆菌属', '双歧杆菌属', '罗斯氏菌属',
                '瘤胃球菌属', '真杆菌属', '梭菌属', '阿克曼菌属', '链球菌属',
                '韦荣球菌属', '乳杆菌属', '肠球菌属', '大肠杆菌属', '克雷伯菌属'
            ]
            
            f.write("\n===== 菌属识别对比 =====\n")
            f.write("期望识别的15种菌属:\n")
            for g in expected_genus:
                found = False
                for genus in genus_list:
                    if g in genus.get('name', ''):
                        found = True
                        break
                status = "✓" if found else "✗"
                f.write(f"  {status} {g}\n")
            
            # 记录异常条目
            f.write("\n===== 异常条目检查 =====\n")
            for genus in genus_list:
                name = genus.get('name', '')
                # 检查名称是否合理
                if len(name) < 3:
                    f.write(f"  ⚠ 名称过短: {name}\n")
                if not "菌属" in name:
                    f.write(f"  ⚠ 名称不含菌属: {name}\n")
                if name.isdigit():
                    f.write(f"  ⚠ 名称为纯数字: {name}\n")
            
            print(f"✓ 日志已保存到: {log_file}")
            
        except Exception as e:
            f.write(f"\n===== 解析错误 =====\n")
            f.write(f"错误类型: {type(e).__name__}\n")
            f.write(f"错误信息: {e}\n")
            import traceback
            f.write(f"堆栈跟踪:\n{traceback.format_exc()}\n")
            print(f"✗ 解析失败，日志已保存到: {log_file}")

if __name__ == "__main__":
    # 优先从命令行参数获取PDF路径
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if not os.path.exists(pdf_path):
            print(f"错误：文件不存在: {pdf_path}")
            sys.exit(1)
        print(f"使用命令行指定的PDF: {pdf_path}")
    else:
        # 查找PDF文件
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') 
                     and not f.startswith('test_') 
                     and not f.startswith('debug_')]
        
        if not pdf_files:
            print("未找到PDF文件，请将PDF文件放在当前目录，或使用命令行参数指定路径")
            print("用法: python debug_real_report.py <PDF文件路径>")
            sys.exit(1)
        
        print("找到以下PDF文件:")
        for i, f in enumerate(pdf_files, 1):
            print(f"{i}. {f}")
        
        # 选择第一个PDF进行分析
        pdf_path = pdf_files[0]
    
    analyze_pdf(pdf_path)
    
    # 输出摘要
    print("\n=== 解析摘要 ===")
    with open(f"debug_{pdf_path.replace('.pdf', '')}.log", 'r', encoding='utf-8') as f:
        content = f.read()
        
        # 提取关键信息
        genus_count = re.search(r'识别到 (\d+) 种菌属', content)
        if genus_count:
            print(f"识别到菌属数量: {genus_count.group(1)}")
        
        # 显示识别结果
        print("\n识别的菌属列表:")
        genus_lines = re.findall(r'\d+\.\s*名称:\s*(.+?)\n', content)
        for i, name in enumerate(genus_lines, 1):
            print(f"{i}. {name}")
