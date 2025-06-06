
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