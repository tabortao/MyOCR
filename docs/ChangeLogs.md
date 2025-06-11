## IMG2PDFPro
IMG2PDFPro 是一款基于 Python、Tkinter 和 customtkinter 开发的高颜值批量图片转 PDF 工具。支持通过按钮选择或拖拽图片文件，一键自动生成 PDF 文件，适合批量图片归档、资料整理等场景。


### v0.1.1 (2025-06-11)
- 修改代码，确保可以成功使用pyinstaller打包。

### v0.1.0 (2025-06-06)
- 实现图片批量转PDF工具。
- 实现自定义标题栏,添加最大化、关闭按钮
- 实现拖拽图片文件

![IMG2PDFPro](../docs/Image/20250611164058-img2pdf-UI.jpg)


## OCRmyPDF

### TODO:
- 使用Nuitka编译源码为pyd

### v0.1.2 (2025-06-06)
- 以API方式调用OCRmyPDF，替代之前的CLI方式调用，实现批量识别。
- 以Python Embed 方式对项目进行打包。

### v0.1.1 (2025-06-04)
- 修复打包后应用无法执行的问题。
- 取消psm参数（Page Segmentation Mode，页面分割模式，Tesseract OCR 的一个参数）。

### v0.1.0 (2025-06-03)
- 使用Python构件的开源程序[OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) UI界面，方便使用。
- 优化UI，使其更简洁。
- 修复OCR识别汉字中间空格较多的问题。
- 调整项目结构。
- 需自行安裝Tesseract、GhostScript并添加到环境变量。

![20250603155601-UI](https://github.com/user-attachments/assets/512a2b46-6f12-4567-ac6f-8bbae8d50c55)