import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from logic import images_to_pdf
import os
import time

class Img2PdfApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IMG2PDFPro")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.selected_images = []

        self.create_widgets()
        self.setup_drag_and_drop()

    def create_widgets(self):
        # 顶部标题
        self.title_label = ctk.CTkLabel(self, text="批量图片转PDF工具", font=("微软雅黑", 22, "bold"), text_color="#00bcd4")
        self.title_label.pack(pady=(18, 8))

        # 主分区Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=16)
        self.main_frame.pack(fill="both", expand=False, padx=18, pady=4)

        # 文件选择说明
        self.label = ctk.CTkLabel(self.main_frame, text="选择图片文件：", font=("微软雅黑", 14))
        self.label.pack(anchor="w", padx=16, pady=(12, 0))

        # 文件列表区
        self.img_textbox = ctk.CTkTextbox(self.main_frame, height=300, font=("Consolas", 11))
        self.img_textbox.pack(fill="both", expand=True, padx=16, pady=(6, 8))
        self.img_textbox.configure(state="disabled")

        # 按钮区
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(0, 8))
        self.select_btn = ctk.CTkButton(btn_frame, text="添加文件", command=self.select_images, width=100)
        self.select_btn.pack(side="left", padx=(0, 10))
        self.clear_btn = ctk.CTkButton(btn_frame, text="清空列表", command=self.clear_list, width=100)
        self.clear_btn.pack(side="left")

        # 分隔线
        self.sep1 = ctk.CTkFrame(self, height=2, fg_color="#222", corner_radius=1)
        self.sep1.pack(fill="x", padx=18, pady=(10, 0))

        # 操作按钮区
        op_frame = ctk.CTkFrame(self, fg_color="transparent")
        op_frame.pack(fill="x", padx=18, pady=(10, 0))
        self.convert_btn = ctk.CTkButton(op_frame, text="开始转换为PDF", command=self.convert_to_pdf, width=200, height=38, font=("微软雅黑", 15, "bold"))
        self.convert_btn.pack(pady=6)

        # 进度条
        self.progress = ctk.CTkProgressBar(self, height=8)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=18, pady=(18, 0))

        # 状态栏
        self.status_label = ctk.CTkLabel(self, text="就绪", font=("微软雅黑", 12), anchor="w")
        self.status_label.pack(fill="x", padx=18, pady=(4, 0))

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
        self.img_textbox.configure(state="normal")
        self.img_textbox.delete("1.0", tk.END)
        for img in self.selected_images:
            self.img_textbox.insert(tk.END, img + "\n")
        self.img_textbox.configure(state="disabled")

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
            self.after(36000, lambda: self.progress.set(0))

    def setup_drag_and_drop(self):
        # 仅Windows下简单实现，需tkinterDnD2等库可更完善
        def drop(event):
            files = self.tk.splitlist(event.data)
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")) and file not in self.selected_images:
                    self.selected_images.append(file)
            self.refresh_listbox()
        try:
            self.img_textbox.drop_target_register(tk.DND_FILES)
            self.img_textbox.dnd_bind('<<Drop>>', drop)
        except Exception:
            pass  # 若无DnD支持则跳过
