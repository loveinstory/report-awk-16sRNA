import report_generator_v2 as gen

test_data = {
    'basic_info': {'name': '测试', 'gender': '男', 'age': '30', 'phone': '13800138000', 'symptoms': '无'},
    'test_info': {'unit': '测试单位', 'sample_id': 'S001', 'sample_type': '粪便', 'sample_date': '2024-01-01', 'method': '测试方法'},
    'report_info': {'report_id': 'R001', 'report_date': '2024-01-01'}
}

html = gen.build_page1(test_data)

# 查找logo-area部分
start = html.find('<div class="logo-area">')
if start != -1:
    end = html.find('</div>', start) + 6
    print('=== Logo区域 ===')
    print(html[start:end])

# 查找deco-banner部分
start = html.find('<div class="deco-banner">')
if start != -1:
    end = html.find('</div>', start) + 6
    print('=== Deco-banner区域 ===')
    print(html[start:end])

# 检查变量是否被替换
if '{{logo_w_image}}' in html:
    print('ERROR: logo_w_image 变量未被替换！')
if '{{logo02_image}}' in html:
    print('ERROR: logo02_image 变量未被替换！')
