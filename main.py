"""
肠道菌群检测报告生成器 - 桌面应用程序
支持批量上传PDF报告并生成美观的标准化报告
"""
import os
import sys
import threading
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pdf_parser import parse_report_pdf
    from report_generator_v2 import generate_report_v2 as generate_report
except ImportError as e:
    print(f"导入模块失败: {e}")
    messagebox.showerror("错误", f"无法导入必要的模块:\n{e}")
    sys.exit(1)


class GutReportApp:
    """肠道菌群检测报告生成器主应用"""

    def __init__(self, root):
        self.root = root
        self.root.title("肠道菌群检测报告生成器 v2.0")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)

        # 设置主题颜色
        self.primary_color = "#2B6B5E"
        self.bg_color = "#F8FAFB"
        self.card_color = "#FFFFFF"

        self.root.configure(bg=self.bg_color)

        # 文件列表
        self.file_list = []
        self.output_dir = ""

        # 创建界面
        self.create_ui()

    def create_ui(self):
        """创建用户界面"""
        # ===== 顶部标题栏 =====
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🧬 肠道菌群检测报告生成器",
            font=("Microsoft YaHei", 16, "bold"),
            fg="white",
            bg=self.primary_color,
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        version_label = tk.Label(
            header_frame,
            text="v2.0 | 安为康功能医学检测",
            font=("Microsoft YaHei", 9),
            fg="#B0D4C8",
            bg=self.primary_color,
        )
        version_label.pack(side=tk.RIGHT, padx=20, pady=15)

        # ===== 主内容区域 =====
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 左侧：文件操作区 ---
        left_frame = tk.Frame(main_frame, bg=self.card_color, relief=tk.FLAT, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # 文件操作按钮区
        btn_frame = tk.Frame(left_frame, bg=self.card_color, pady=10, padx=10)
        btn_frame.pack(fill=tk.X)

        tk.Label(
            btn_frame,
            text="📁 待处理文件列表",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.card_color,
            fg=self.primary_color,
        ).pack(side=tk.LEFT)

        self.btn_clear = tk.Button(
            btn_frame,
            text="清空列表",
            command=self.clear_files,
            font=("Microsoft YaHei", 9),
            bg="#F5F5F5",
            fg="#666666",
            relief=tk.FLAT,
            padx=10,
        )
        self.btn_clear.pack(side=tk.RIGHT, padx=5)

        self.btn_add = tk.Button(
            btn_frame,
            text="+ 添加PDF文件",
            command=self.add_files,
            font=("Microsoft YaHei", 9, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=3,
        )
        self.btn_add.pack(side=tk.RIGHT, padx=5)

        # 文件列表
        list_frame = tk.Frame(left_frame, bg=self.card_color, padx=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # 创建Treeview
        columns = ("filename", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        self.tree.heading("filename", text="文件名")
        self.tree.heading("status", text="状态")
        self.tree.column("filename", width=350)
        self.tree.column("status", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 文件数量统计
        self.file_count_label = tk.Label(
            left_frame,
            text="共 0 个文件",
            font=("Microsoft YaHei", 9),
            bg=self.card_color,
            fg="#999999",
            pady=5,
        )
        self.file_count_label.pack(fill=tk.X, padx=10)

        # --- 右侧：设置和操作区 ---
        right_frame = tk.Frame(main_frame, bg=self.card_color, relief=tk.FLAT, bd=1, width=280)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)

        # 输出设置
        settings_frame = tk.Frame(right_frame, bg=self.card_color, padx=15, pady=15)
        settings_frame.pack(fill=tk.X)

        tk.Label(
            settings_frame,
            text="⚙️ 输出设置",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.card_color,
            fg=self.primary_color,
        ).pack(anchor=tk.W)

        tk.Label(
            settings_frame,
            text="输出目录：",
            font=("Microsoft YaHei", 9),
            bg=self.card_color,
            fg="#666666",
        ).pack(anchor=tk.W, pady=(10, 2))

        dir_frame = tk.Frame(settings_frame, bg=self.card_color)
        dir_frame.pack(fill=tk.X)

        self.output_dir_var = tk.StringVar(value="（与源文件相同目录）")
        self.dir_entry = tk.Entry(
            dir_frame,
            textvariable=self.output_dir_var,
            font=("Microsoft YaHei", 8),
            state="readonly",
            width=20,
        )
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_dir = tk.Button(
            dir_frame,
            text="选择",
            command=self.select_output_dir,
            font=("Microsoft YaHei", 8),
            bg="#F0F0F0",
            relief=tk.FLAT,
            padx=8,
        )
        self.btn_dir.pack(side=tk.RIGHT, padx=(5, 0))

        # 文件命名规则
        tk.Label(
            settings_frame,
            text="输出文件命名：",
            font=("Microsoft YaHei", 9),
            bg=self.card_color,
            fg="#666666",
        ).pack(anchor=tk.W, pady=(15, 2))

        self.naming_var = tk.StringVar(value="prefix")
        tk.Radiobutton(
            settings_frame,
            text="原文件名 + \"_报告\"后缀",
            variable=self.naming_var,
            value="prefix",
            font=("Microsoft YaHei", 9),
            bg=self.card_color,
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            settings_frame,
            text="使用患者姓名命名",
            variable=self.naming_var,
            value="patient_name",
            font=("Microsoft YaHei", 9),
            bg=self.card_color,
        ).pack(anchor=tk.W)

        # 分隔线
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=10)

        # 操作信息
        info_frame = tk.Frame(right_frame, bg=self.card_color, padx=15)
        info_frame.pack(fill=tk.X)

        tk.Label(
            info_frame,
            text="📋 使用说明",
            font=("Microsoft YaHei", 10, "bold"),
            bg=self.card_color,
            fg=self.primary_color,
        ).pack(anchor=tk.W)

        instructions = (
            "1. 点击「添加PDF文件」选择\n"
            "   一个或多个原始报告PDF\n"
            "2. 选择输出目录（可选）\n"
            "3. 点击「开始生成报告」\n"
            "4. 等待处理完成即可"
        )
        tk.Label(
            info_frame,
            text=instructions,
            font=("Microsoft YaHei", 9),
            bg=self.card_color,
            fg="#666666",
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(5, 0))

        # ===== 底部操作栏 =====
        bottom_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        bottom_frame.pack(fill=tk.X)

        # 进度条
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            bottom_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))

        # 状态文字
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = tk.Label(
            bottom_frame,
            textvariable=self.status_var,
            font=("Microsoft YaHei", 9),
            bg=self.bg_color,
            fg="#666666",
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 15))

        # 生成按钮
        self.btn_generate = tk.Button(
            bottom_frame,
            text="🚀 开始生成报告",
            command=self.start_generation,
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=8,
            cursor="hand2",
        )
        self.btn_generate.pack(side=tk.RIGHT)

    def add_files(self):
        """添加PDF文件"""
        files = filedialog.askopenfilenames(
            title="选择PDF报告文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")],
        )
        if files:
            for f in files:
                if f not in self.file_list:
                    self.file_list.append(f)
                    filename = os.path.basename(f)
                    self.tree.insert("", tk.END, values=(filename, "待处理"))
            self.update_file_count()

    def clear_files(self):
        """清空文件列表"""
        self.file_list.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.update_file_count()
        self.progress_var.set(0)
        self.status_var.set("就绪")

    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir = directory
            self.output_dir_var.set(directory)

    def update_file_count(self):
        """更新文件数量显示"""
        count = len(self.file_list)
        self.file_count_label.config(text=f"共 {count} 个文件")

    def start_generation(self):
        """开始生成报告"""
        if not self.file_list:
            messagebox.showwarning("提示", "请先添加PDF文件！")
            return

        # 禁用按钮
        self.btn_generate.config(state=tk.DISABLED, text="⏳ 正在生成...")
        self.btn_add.config(state=tk.DISABLED)

        # 在新线程中执行
        thread = threading.Thread(target=self.generate_reports, daemon=True)
        thread.start()

    def generate_reports(self):
        """批量生成报告（在后台线程中执行）"""
        total = len(self.file_list)
        success_count = 0
        fail_count = 0

        for i, pdf_path in enumerate(self.file_list):
            try:
                # 更新状态
                filename = os.path.basename(pdf_path)
                self.root.after(0, lambda fn=filename: self.status_var.set(f"正在处理: {fn}"))

                # 更新树状态
                item_id = self.tree.get_children()[i]
                self.root.after(0, lambda iid=item_id: self.tree.set(iid, "status", "处理中..."))

                # 记录开始解析日志
                parse_log = f"===== 开始解析: {pdf_path} =====\n"
                
                # 解析PDF
                data = parse_report_pdf(pdf_path)
                
                # 记录解析结果日志
                genus_list = data.get("genus_distribution", [])
                parse_log += f"属级分布识别数量: {len(genus_list)}\n"
                parse_log += "识别的菌属:\n"
                for j, genus in enumerate(genus_list, 1):
                    parse_log += f"  {j}. {genus.get('name', '')} - {genus.get('ratio', '')} - {genus.get('category', '')}\n"
                
                # 检查是否缺少菌属
                expected_genus = [
                    '普雷沃菌属', '拟杆菌属', '粪杆菌属', '双歧杆菌属', '罗斯氏菌属',
                    '瘤胃球菌属', '真杆菌属', '梭菌属', '阿克曼菌属', '链球菌属',
                    '韦荣球菌属', '乳杆菌属', '肠球菌属', '大肠杆菌属', '克雷伯菌属'
                ]
                parse_log += "\n缺失的菌属:\n"
                for g in expected_genus:
                    found = False
                    for genus in genus_list:
                        if g in genus.get('name', ''):
                            found = True
                            break
                    if not found:
                        parse_log += f"  ✗ {g}\n"
                
                print(parse_log)
                
                # 写入解析日志文件
                try:
                    log_filename = f"parse_log_{os.path.splitext(filename)[0]}.txt"
                    with open(log_filename, 'w', encoding='utf-8') as f:
                        f.write(parse_log)
                except Exception as log_err:
                    print(f"写入解析日志失败: {log_err}")

                # 确定输出路径
                if self.output_dir:
                    out_dir = self.output_dir
                else:
                    out_dir = os.path.dirname(pdf_path)

                # 确定输出文件名
                if self.naming_var.get() == "patient_name":
                    patient_name = data.get("basic_info", {}).get("name", "")
                    if patient_name:
                        out_filename = f"{patient_name}_肠道菌群检测报告.pdf"
                    else:
                        base_name = Path(pdf_path).stem
                        out_filename = f"{base_name}_报告.pdf"
                else:
                    base_name = Path(pdf_path).stem
                    out_filename = f"{base_name}_报告.pdf"

                output_path = os.path.join(out_dir, out_filename)

                # 生成报告
                generate_report(data, output_path)

                # 更新状态为成功
                self.root.after(0, lambda iid=item_id: self.tree.set(iid, "status", "✅ 完成"))
                success_count += 1

            except Exception as e:
                # 更新状态为失败
                item_id = self.tree.get_children()[i]
                error_msg = str(e)[:50] if len(str(e)) > 50 else str(e)
                self.root.after(0, lambda iid=item_id, err=error_msg: self.tree.set(iid, "status", f"❌ 失败: {err}"))
                fail_count += 1
                
                # 详细错误日志
                error_log = f"===== 处理失败 {pdf_path} =====\n"
                error_log += f"时间: {os.path.getmtime(pdf_path) if os.path.exists(pdf_path) else 'N/A'}\n"
                error_log += f"错误类型: {type(e).__name__}\n"
                error_log += f"错误信息: {e}\n"
                error_log += f"堆栈跟踪:\n{traceback.format_exc()}\n\n"
                
                print(error_log)
                
                # 写入错误日志文件
                try:
                    with open("error.log", "a", encoding="utf-8") as f:
                        f.write(error_log)
                except Exception as log_err:
                    print(f"写入错误日志失败: {log_err}")

            # 更新进度
            progress = (i + 1) / total * 100
            self.root.after(0, lambda p=progress: self.progress_var.set(p))

        # 完成
        self.root.after(0, lambda: self.on_generation_complete(success_count, fail_count))

    def on_generation_complete(self, success, fail):
        """生成完成回调"""
        self.btn_generate.config(state=tk.NORMAL, text="🚀 开始生成报告")
        self.btn_add.config(state=tk.NORMAL)
        self.status_var.set(f"完成！成功 {success} 个，失败 {fail} 个")

        if fail == 0:
            messagebox.showinfo("完成", f"所有报告已成功生成！\n共处理 {success} 个文件。")
        else:
            messagebox.showwarning("完成", f"处理完成。\n成功：{success} 个\n失败：{fail} 个\n\n请检查失败文件的格式是否正确。")


def main():
    """主函数"""
    root = tk.Tk()

    # 设置DPI感知（Windows）
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    # 设置ttk主题
    style = ttk.Style()
    style.theme_use("clam")

    app = GutReportApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
