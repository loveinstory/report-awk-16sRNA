# 肠道菌群检测报告生成器 v2.0

## 简介

本软件是一个专业的肠道菌群检测健康管理报告生成工具，能够自动解析原始检测报告PDF文件中的数据，并基于精心设计的HTML模板生成美观、规范的标准化报告。支持批量处理多个患者报告。

V2版本采用 HTML+CSS 渲染引擎（WeasyPrint），完美复现安为康功能医学检测的专业报告模板样式，包含仪表盘、环形图、渐变色刻度尺等丰富的数据可视化元素。

## 功能特点

| 功能 | 说明 |
|------|------|
| PDF智能解析 | 自动识别并提取报告中的患者信息、检测数据、菌群分布等结构化数据 |
| 精美模板生成 | 基于HTML+CSS渲染，SVG可视化图表，完美复现专业医疗报告模板 |
| 批量处理 | 支持一次性导入多个PDF文件，自动批量生成报告 |
| 灵活命名 | 支持按原文件名或患者姓名自动命名输出文件 |
| 桌面GUI | 图形化操作界面，简单易用 |

## 报告内容（5页）

1. **封面页** - 品牌logo、报告编号、受检者信息、检测信息、服务亮点
2. **肠道健康核心指数** - GMHI仪表盘、菌群多样性、肠道年龄、B/E比值、核心指标表格、门级分布条形图
3. **菌群精细组成分析** - Top10菌属SVG环形图、有益菌/有害菌检测表、B/E比值渐变刻度尺
4. **精准评估与健康管理建议** - AI智能解读、饮食/益生菌/运动三大建议模块、干预随访时间轴
5. **科普前沿** - 肠龄知识、B/E比值科普、饮食建议、医学声明

## 系统要求

- **操作系统**：Windows 10/11、macOS、Linux
- **Python版本**：Python 3.9 或更高版本
- **磁盘空间**：约 200MB（含依赖）

## 安装步骤

### Windows 用户（推荐）

1. 确保已安装 Python 3.9+（[下载地址](https://www.python.org/downloads/)）
   - 安装时务必勾选 "Add Python to PATH"
2. 解压本软件包到任意目录
3. 双击 `install_and_run.bat` 即可自动安装依赖并启动程序

### 手动安装（所有平台）

```bash
cd gut_report_generator
pip install -r requirements.txt
python main.py
```

## 使用方法

1. **启动程序**：双击 `start.bat`（Windows）或运行 `python3 main.py`
2. **添加文件**：点击「+ 添加PDF文件」按钮，选择一个或多个原始报告PDF文件
3. **设置输出**：（可选）点击「选择」按钮指定输出目录
4. **选择命名**：选择输出文件的命名方式（原文件名或患者姓名）
5. **生成报告**：点击「开始生成报告」按钮，等待处理完成

## 输入文件要求

本软件适用于安为康功能医学检测的肠道菌群检测报告PDF，需包含：

- 受检者基本信息（姓名、性别、年龄等）
- 检测信息（样本编号、采样日期、检测方法等）
- 肠道健康核心指数（GMHI评分、菌群多样性、肠道年龄等）
- 菌群组成数据（门级/属级分布）
- 有益菌/有害菌检测结果
- 健康管理建议

## 项目结构

```
gut_report_generator/
├── main.py                    # 桌面GUI主程序
├── pdf_parser.py              # PDF数据解析模块
├── report_generator_v2.py     # HTML模板报告生成引擎
├── templates/                 # HTML页面模板
│   ├── page1_cover.html       # 封面页模板
│   ├── page2_indices.html     # 核心指数页模板
│   ├── page3_composition.html # 菌群组成页模板
│   ├── page4_advice.html      # 建议页模板
│   └── page5_science.html     # 科普页模板
├── output/                    # 默认输出目录
├── requirements.txt           # Python依赖
├── install_and_run.bat        # Windows一键安装启动
├── start.bat                  # Windows快速启动
└── README.md                  # 本文件
```

## 自定义模板

如需修改报告样式，可直接编辑 `templates/` 目录下的HTML文件。模板使用标准HTML+CSS，支持：

- 修改颜色方案（主色调、辅助色等）
- 调整布局和间距
- 自定义图表样式
- 修改文字内容和字体

## 常见问题

**Q: 报告生成失败怎么办？**
A: 请确保输入的PDF文件格式与安为康检测报告一致。不同格式的PDF可能需要调整解析规则。

**Q: 中文显示异常？**
A: 请确保系统安装了中文字体（如微软雅黑、思源黑体等）。WeasyPrint会自动使用系统字体。

**Q: WeasyPrint安装报错？**
A: Windows用户可能需要安装GTK运行时。请参考 [WeasyPrint安装文档](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)。

## 技术栈

- **PDF解析**: pdfplumber + PyMuPDF
- **报告生成**: WeasyPrint (HTML/CSS → PDF)
- **可视化**: SVG内联图表（仪表盘、环形图、条形图、渐变刻度尺）
- **桌面GUI**: tkinter

---
*本软件由AI辅助开发，仅供医疗机构内部使用。*
