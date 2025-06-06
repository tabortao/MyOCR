from tkinterdnd2 import TkinterDnD, DND_FILES
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from logic import images_to_pdf
import os
import time

class Img2PdfApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("IMG2PDFPro")
        self.iconbitmap("./IMG2PDFPro/app_icon.ico")  # 设置应用图标
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(bg="#181c22")  # 整体窗口深色
        self.selected_images = []


        # 手动加载tkdnd库，避免拖拽失效
        try:
            self.tk.call('package', 'require', 'tkdnd')
        except tk.TclError:
            messagebox.showerror("错误", "tkdnd库未正确加载，拖拽功能不可用。请检查tkinterDnD2安装。")

        self.create_widgets()

    def create_widgets(self):
        # 顶部LOGO和标题
        top_frame = ctk.CTkFrame(self, fg_color="#181c22")
        top_frame.pack(fill="x", pady=(10, 0))

        self.title_label = ctk.CTkLabel(top_frame, text="批量图片转PDF工具", font=("微软雅黑", 22, "bold"), text_color="#00bcd4", bg_color="#181c22")
        self.title_label.pack(side="left", expand=True, fill="x", pady=(0, 0))

        # 副标题（去掉，合并到列表区内部）
        # self.subtitle = ctk.CTkLabel(self, text="支持拖拽图片到下方区域，或点击添加文件", font=("微软雅黑", 14), text_color="#26e6fa", bg_color="#181c22")
        # self.subtitle.pack(pady=(2, 8))

        # 主分区Frame（加阴影和圆角）
        self.main_frame = ctk.CTkFrame(self, corner_radius=18, fg_color="#22252a")
        self.main_frame.pack(fill="both", expand=False, padx=28, pady=4)

        # 文件选择说明
        self.label = ctk.CTkLabel(self.main_frame, text="选择图片文件：", font=("微软雅黑", 14), text_color="#b0bec5", bg_color="#22252a")
        self.label.pack(anchor="w", padx=18, pady=(14, 0))

        # 文件列表区（加边框和深色背景）
        list_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#181c22", border_width=2, border_color="#00bcd4")
        list_frame.pack(fill="both", expand=True, padx=16, pady=(6, 8))
        # 拖拽提示合并到列表区内部
        self.img_textbox = tk.Text(list_frame, height=14, font=("Consolas", 11), bg="#181c22", fg="#eeeeee", insertbackground="#eeeeee", relief="flat", borderwidth=0, selectbackground="#393e46", highlightthickness=0)
        self.img_textbox.pack(fill="both", expand=True, padx=6, pady=(18, 6))
        self.img_textbox.config(state="disabled")
        self.img_textbox.drop_target_register(DND_FILES)
        self.img_textbox.dnd_bind('<<Drop>>', self.drop_files)
        # 在Text控件上方添加内嵌提示
        self.list_tip = ctk.CTkLabel(list_frame, text="支持拖拽图片到此区域，或点击添加文件", font=("微软雅黑", 13, "bold"), text_color="#26e6fa", bg_color="#181c22")
        self.list_tip.place(relx=0.5, rely=0.04, anchor="n")

        # 去掉下方拖拽提示条
        # self.drag_tip = ctk.CTkLabel(self.main_frame, text="⬇️  你可以将图片文件直接拖拽到上方区域", font=("微软雅黑", 13, "bold"), text_color="#00bcd4", bg_color="#22252a")
        # self.drag_tip.pack(anchor="w", padx=18, pady=(0, 4))

        # 按钮区（居中）
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="#22252a")
        btn_frame.pack(pady=(0, 8))
        self.select_btn = ctk.CTkButton(btn_frame, text="添加文件", command=self.select_images, width=120, height=32, font=("微软雅黑", 13, "bold"), fg_color="#263238", hover_color="#00bcd4", text_color="#e0f7fa")
        self.select_btn.pack(side="left", padx=(0, 18))
        self.clear_btn = ctk.CTkButton(btn_frame, text="清空列表", command=self.clear_list, width=120, height=32, font=("微软雅黑", 13, "bold"), fg_color="#263238", hover_color="#00bcd4", text_color="#e0f7fa")
        self.clear_btn.pack(side="left")

        # 分隔线
        self.sep1 = ctk.CTkFrame(self, height=2, fg_color="#22252a", corner_radius=1)
        self.sep1.pack(fill="x", padx=28, pady=(10, 0))

        # 操作按钮区（居中）
        op_frame = ctk.CTkFrame(self, fg_color="#181c22")
        op_frame.pack(fill="x", padx=28, pady=(10, 0))
        self.convert_btn = ctk.CTkButton(op_frame, text="开始转换为PDF", command=self.convert_to_pdf, width=240, height=44, font=("微软雅黑", 16, "bold"), fg_color="#00bcd4", hover_color="#26e6fa", text_color="#181c22")
        self.convert_btn.pack(pady=8)

        # 进度条
        self.progress = ctk.CTkProgressBar(self, height=10, fg_color="#263238", progress_color="#00bcd4")
        self.progress.set(0)
        self.progress.pack(fill="x", padx=28, pady=(18, 0))

        # 状态栏
        self.status_label = ctk.CTkLabel(self, text="就绪", font=("微软雅黑", 13), anchor="w", text_color="#b0bec5", bg_color="#181c22")
        self.status_label.pack(fill="x", padx=28, pady=(4, 0))

    def select_images(self):
        files = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg"), ("所有文件", "*.*")]
        )
        if files:
            self.selected_images.extend([f for f in files if f not in self.selected_images])
            self.refresh_listbox()

    def clear_list(self):
        self.selected_images = []
        self.refresh_listbox()
        self.progress.set(0)
        self.status_label.configure(text="已清空文件列表")

    def refresh_listbox(self):
        self.img_textbox.config(state="normal")
        self.img_textbox.delete("1.0", tk.END)
        for img in self.selected_images:
            self.img_textbox.insert(tk.END, img + "\n")
        self.img_textbox.config(state="disabled")

    def convert_to_pdf(self):
        if not self.selected_images:
            messagebox.showwarning("提示", "请先选择图片文件")
            return
        # 自动保存到图片所在文件夹，以时间戳命名
        first_img = self.selected_images[0]
        folder = os.path.dirname(first_img)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        pdf_path = os.path.join(folder, f"{timestamp}.pdf")
        try:
            self.status_label.configure(text="正在转换...")
            self.progress.set(0.2)
            self.update_idletasks()
            images_to_pdf(self.selected_images, pdf_path)
            self.progress.set(1.0)  # 进度条100%
            self.status_label.configure(text=f"PDF已保存到：{pdf_path}")
        except Exception as e:
            self.status_label.configure(text="转换失败")
            messagebox.showerror("错误", f"转换失败：{e}")
        finally:
            # 保持进度条100%一段时间后再归零
            self.after(1200, lambda: self.progress.set(0))

    def drop_files(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")) and file not in self.selected_images:
                self.selected_images.append(file)
        self.refresh_listbox()
