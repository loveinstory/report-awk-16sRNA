with open('test_output/page2.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# 检查是否还有未替换的模板变量
if '{{gmhi_score}}' in content:
    print('✗ gmhi_score 未替换')
else:
    print('✓ gmhi_score 已替换')

if '{{gmhi_label}}' in content:
    print('✗ gmhi_label 未替换')
else:
    print('✓ gmhi_label 已替换')

if '{{gmhi_level}}' in content:
    print('✗ gmhi_level 未替换')
else:
    print('✓ gmhi_level 已替换')

if '{{indices_rows}}' in content:
    print('✗ indices_rows 未替换')
else:
    print('✓ indices_rows 已替换')

if '{{phylum_bars}}' in content:
    print('✗ phylum_bars 未替换')
else:
    print('✓ phylum_bars 已替换')

if '{{genus_bars}}' in content:
    print('✗ genus_bars 未替换')
else:
    print('✓ genus_bars 已替换')

print('\n--- 查看部分HTML内容 ---')
print(content[:2000])
