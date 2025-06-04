import tkinter as tk
from tkinter import filedialog, messagebox
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkCheckBox, CTkProgressBar, CTkTextbox, CTkScrollableFrame
from customtkinter import set_appearance_mode, set_default_color_theme
import threading
import os
from ocr_processor import OCRProcessor

class PDFOCRApp:
    def __init__(self):
        # 初始化主窗口
        self.root = CTk()
        self.root.title("OCRMyPDF - 极简版")
        self.root.geometry("700x600")
        set_appearance_mode("Dark")
        set_default_color_theme("blue")
        # 变量
        self.selected_files = []
        self.processing = False
        self.txt_var = tk.BooleanVar(value=True)
        self.lang_var = tk.StringVar(value="中英混合")  # 默认显示“中英混合”
        self.create_widgets()

    def create_widgets(self):
        # 主Frame
        self.main_frame = CTkFrame(self.root, corner_radius=12)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)
        # 标题
        CTkLabel(self.main_frame, text="PDF OCR 批量识别工具", font=("Arial", 22, "bold"), text_color="#00adb5").pack(pady=(10, 12))
        # 文件选择区域
        file_frame = CTkFrame(self.main_frame, corner_radius=10)
        file_frame.pack(padx=6, pady=6, fill=tk.X)
        CTkLabel(file_frame, text="选择PDF文件:", font=("Arial", 12)).pack(anchor=tk.W, padx=10, pady=(8, 2))
        self.file_listbox = CTkScrollableFrame(file_frame, height=50)
        self.file_listbox.pack(padx=10, pady=5, fill=tk.BOTH)
        btn_frame = CTkFrame(file_frame, fg_color="transparent")
        btn_frame.pack(pady=5)
        CTkButton(btn_frame, text="添加文件", width=120, command=self.add_files).pack(side=tk.LEFT, padx=8)
        CTkButton(btn_frame, text="清空列表", width=120, command=self.clear_files).pack(side=tk.LEFT, padx=8)
        # 选项
        option_frame = CTkFrame(self.main_frame, corner_radius=10)
        option_frame.pack(padx=6, pady=6, fill=tk.X)
        # 输出文本文件选项
        CTkCheckBox(option_frame, text="输出文本文件 (.txt)", variable=self.txt_var, font=("Arial", 12), width=70, height=16).pack(anchor=tk.W, padx=10, pady=8, side="left")
        # 语言选择下拉框
        CTkLabel(option_frame, text="识别语言:", font=("Arial", 12)).pack(side="left", padx=(20, 2))
        from customtkinter import CTkComboBox
        self.lang_combo = CTkComboBox(option_frame, values=["中文", "英文", "中英混合"], variable=self.lang_var, width=110, font=("Arial", 12))
        self.lang_combo.pack(side="left", padx=2)
        self.lang_combo.set("中英混合")
        # 处理按钮
        self.process_btn = CTkButton(self.main_frame, text="开始OCR处理", font=("Arial", 15, "bold"), height=42, command=self.start_processing)
        self.process_btn.pack(pady=12)
        # 进度条
        self.progress_bar = CTkProgressBar(self.main_frame, height=15)
        self.progress_bar.pack(padx=8, pady=4, fill=tk.X)
        self.progress_bar.set(0)  # 启动时进度为0
        # 状态栏
        self.status_label = CTkLabel(self.main_frame, text="就绪", anchor=tk.W, font=("Arial", 12), height=28)
        self.status_label.pack(fill=tk.X, padx=8, pady=(0, 4))
        self.update_file_list()

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")])
        if files:
            self.selected_files.extend(files)
            self.update_file_list()
            self.log(f"添加了 {len(files)} 个文件")

    def clear_files(self):
        self.selected_files = []
        self.update_file_list()
        self.log("文件列表已清空")

    def update_file_list(self):
        for widget in self.file_listbox.winfo_children():
            widget.destroy()
        for i, file_path in enumerate(self.selected_files):
            file_label = CTkLabel(self.file_listbox, text=f"{i+1}. {os.path.basename(file_path)}", anchor=tk.W)
            file_label.pack(fill=tk.X, pady=2)

    def log(self, message):
        # 只更新状态栏，不显示日志区域
        self.status_label.configure(text=message)

    def start_processing(self):
        if not self.selected_files:
            messagebox.showwarning("警告", "请先选择PDF文件")
            return
        if self.processing:
            return
        self.processing = True
        self.process_btn.configure(state=tk.DISABLED)
        self.log("开始处理文件...")
        threading.Thread(target=self.process_files, daemon=True).start()

    def process_files(self):
        total = len(self.selected_files)
        output_txt = self.txt_var.get()
        lang_map = {"中文": "chi_sim", "英文": "eng", "中英混合": "chi_sim+eng"}
        lang = lang_map.get(self.lang_var.get(), "chi_sim+eng")
        for i, input_path in enumerate(self.selected_files):
            progress = (i / total)
            self.root.after(10, lambda p=progress: self.progress_bar.set(p))
            self.log(f"正在处理: {os.path.basename(input_path)} ({i+1}/{total})")
            output_path = os.path.splitext(input_path)[0] + "_ocr.pdf"
            # 新增：定义日志回调
            def log_callback(msg):
                self.root.after(0, lambda: self.log(msg))
            success, message = OCRProcessor.process_pdf(
                input_path,
                output_path,
                output_txt=output_txt,
                lang=lang,
                log_callback=log_callback  # 传递回调
            )
            self.log(message)
            self.root.after(10, lambda p=(i+1)/total: self.progress_bar.set(p))
        self.processing = False
        self.root.after(10, self.finish_processing)

    def finish_processing(self):
        self.progress_bar.set(1.0)
        self.process_btn.configure(state=tk.NORMAL)
        self.log("所有文件处理完成！")
        self.status_label.configure(text="处理完成")
        # 移除弹窗提示
        # messagebox.showinfo("完成", "所有文件处理完成！")

    def run(self):
        self.root.mainloop()