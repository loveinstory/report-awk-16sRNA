with open('test_output/page2.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# 检查关键内容
check_items = [
    ('GMHI评分', 'gmhi_score'),
    ('58.5', 'gmhi_value'),
    ('偏低', 'gmhi_label'),
    ('菌群多样性', 'diversity'),
    ('肠道年龄', 'gut_age'),
    ('52', 'gut_age_value'),
    ('B/E比值', 'be_ratio'),
    ('45岁', 'real_age'),
    ('拟杆菌门', 'phylum_bacteroidetes'),
    ('厚壁菌门', 'phylum_firmicutes'),
    ('门级水平分布', 'phylum_section'),
    ('属级水平分布', 'genus_section'),
]

print('=== 页面2内容检查 ===')
for text, desc in check_items:
    if text in content:
        print(f'✓ {desc}: 包含 "{text}"')
    else:
        print(f'✗ {desc}: 缺少 "{text}"')

# 检查是否还有未替换的模板变量
template_vars = ['{{gmhi_score}}', '{{diversity_value}}', '{{gut_age}}', '{{be_value}}', '{{indices_rows}}', '{{phylum_bars}}', '{{genus_bars}}']
print('\n=== 模板变量检查 ===')
for var in template_vars:
    if var in content:
        print(f'✗ 未替换: {var}')
    else:
        print(f'✓ 已替换: {var}')
