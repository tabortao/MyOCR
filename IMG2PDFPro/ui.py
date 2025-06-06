from tkinterdnd2 import TkinterDnD, DND_FILES
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from logic import images_to_pdf
import os
import time
import PIL.Image

class Img2PdfApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # 无边框窗口
        self.title("IMG2PDFPro")
        self.iconbitmap("./IMG2PDFPro/app_icon.ico")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(bg="#181c22")
        self.selected_images = []
        self._drag_data = {'x': 0, 'y': 0}
        # 手动加载tkdnd库，避免拖拽失效
        try:
            self.tk.call('package', 'require', 'tkdnd')
        except tk.TclError:
            messagebox.showerror("错误", "tkdnd库未正确加载，拖拽功能不可用。请检查tkinterDnD2安装。")
        self.create_custom_titlebar()
        self.create_widgets()

    def create_custom_titlebar(self):
        # 自定义黑色标题栏
        self.titlebar = ctk.CTkFrame(self, height=36, fg_color="#181c22", corner_radius=0)
        self.titlebar.pack(fill="x", side="top")
        # 图标（用CTkImage+PIL.Image）
        self.icon_img = ctk.CTkImage(light_image=PIL.Image.open("./IMG2PDFPro/app_icon.png"), size=(25, 25))
        self.icon_label = ctk.CTkLabel(self.titlebar, text="", image=self.icon_img, width=28, height=28, bg_color="#181c22")
        self.icon_label.pack(side="left", padx=(8, 2), pady=2)
        # 标题
        self.title_text = ctk.CTkLabel(self.titlebar, text="IMG2PDFPro 批量图片转PDF工具", font=("微软雅黑", 16, "bold"), text_color="#00bcd4", bg_color="#181c22")
        self.title_text.pack(side="left", padx=(6, 0), pady=0, expand=True, fill="x")
        # 关闭按钮（符号版，最右侧）
        self.close_btn = ctk.CTkButton(self.titlebar, text="x", width=38, height=28, fg_color="#23272e", hover_color="#e53935", text_color="#e0e0e0", font=("微软雅黑", 15, "bold"), command=self.destroy, corner_radius=6)
        self.close_btn.pack(side="right", padx=(0, 8), pady=4)
        # 最大化/还原按钮（关闭按钮左侧）
        self.is_maximized = False
        self.max_btn = ctk.CTkButton(self.titlebar, text="□", width=38, height=28, fg_color="#23272e", hover_color="#00bcd4", text_color="#e0e0e0", font=("微软雅黑", 13), command=self.toggle_maximize, corner_radius=6)
        self.max_btn.pack(side="right", padx=(0, 2), pady=4)
        # 拖动事件
        self.titlebar.bind('<Button-1>', self.start_move)
        self.titlebar.bind('<B1-Motion>', self.do_move)
        self.title_text.bind('<Button-1>', self.start_move)
        self.title_text.bind('<B1-Motion>', self.do_move)
        self.icon_label.bind('<Button-1>', self.start_move)
        self.icon_label.bind('<B1-Motion>', self.do_move)

    def start_move(self, event):
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def do_move(self, event):
        x = self.winfo_pointerx() - self._drag_data['x']
        y = self.winfo_pointery() - self._drag_data['y']
        self.geometry(f'+{x}+{y}')

    def toggle_maximize(self):
        if not hasattr(self, '_normal_geometry'):
            self._normal_geometry = self.geometry()
        if not self.is_maximized:
            self._normal_geometry = self.geometry()
            self.state('zoomed')
            self.is_maximized = True
            self.max_btn.configure(text="❐")
        else:
            self.state('normal')
            self.geometry(self._normal_geometry)
            self.is_maximized = False
            self.max_btn.configure(text="□")

    def create_widgets(self):
        # 主分区Frame（加阴影和圆角）
        self.main_frame = ctk.CTkFrame(self, corner_radius=18, fg_color="#22252a")
        self.main_frame.pack(fill="both", expand=False, padx=28, pady=4)

        # 文件选择说明
        self.label = ctk.CTkLabel(self.main_frame, text="支持拖拽图片到下方区域，或点击添加文件", font=("微软雅黑", 14), text_color="#b0bec5", bg_color="#22252a")
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
        # self.list_tip = ctk.CTkLabel(list_frame, text="支持拖拽图片到此区域，或点击添加文件", font=("微软雅黑", 13, "bold"), text_color="#26e6fa", bg_color="#181c22")
        # self.list_tip.place(relx=0.5, rely=0.04, anchor="n")

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
