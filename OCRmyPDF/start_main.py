import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import PDFOCRApp

def check_dependencies():
    """检查所需依赖是否安装"""
    missing = []
    if sys.version_info < (3, 8):
        missing.append("Python 3.8+")
    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")
    try:
        import ocrmypdf
    except ImportError:
        missing.append("ocrmypdf")
    try:
        from pdfminer.high_level import extract_text
    except ImportError:
        missing.append("pdfminer.six")
    return missing

def start():
    missing = check_dependencies()
    if missing:
        msg = f"缺少依赖: {', '.join(missing)}\n请运行: pip install customtkinter ocrmypdf pdfminer.six"
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("依赖缺失", msg)
        except Exception:
            print(msg)
        sys.exit(1)
    try:
        app = PDFOCRApp()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(2)
