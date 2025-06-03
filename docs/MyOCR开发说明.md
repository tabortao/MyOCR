

# OCRmyPDF 开发说明

## 应用需求
使用python写一个项目MyOCR，使用Tkinter和customTkinter实现UI，选择一个或多个PDF文件，点击按钮后对pdf进行OCR识别，以设置是否输出txt文件。UI要高端美化，ui与逻辑分离。满足如下要求：
1. main.py进行界面调用，UI和逻辑在各自文件夹中保存。
2. PDF可以通过点击按钮选择、或者拖入实现选择PDF文件。
3. 输出结果自动保存到PDF源文件所在文件夹，自动新建的OUTPUT_OCR文件夹中。
4. 可以设置语言，如简体中文和英文混合文档。
5. 可以设置是否生成纯文本，如提取OCR文本到.txt文件。

## 创建环境

```bash
# 项目目前开发环境已经使用uv创建好了，如下：
uv init MyOCR --python 3.12 # 初始化项目
cd MyOCR
uv add  ocrmypdf pdfminer.six customtkinter nuitka
.venv\Scripts\activate # 激活环境
uv sync
uv run OCRmyPDF/main.py # 运行项目
```

## 项目依赖
### Tesseract
> Tesseract 是由 HP（惠普）实验室开发，后由 Google 维护的开源 OCR（光学字符识别）引擎。它支持多种语言和文字，能识别印刷体和部分手写体，广泛应用于文档数字化、自动化数据提取等领域。

1. 下载Tesseract
[Tesseract下载地址](https://tesseract-ocr.github.io/tessdoc/Installation.html),其中[Windows版下载地址](https://github.com/UB-Mannheim/tesseract/wiki),比如我下载了`tesseract-ocr-w64-setup-5.5.0.20241111.exe`。
2. Tesseract安装
双击下载好的exe程序，选择要支持识别的语言。
![](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202506031758216.png)
3. 把`D:\Program Files\Tesseract-OCR`添加到用户环境变量。

![](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202506031756343.png)

### GhostScript
> Ghostscript 是一款开源的 PostScript (PS) 和 PDF 解释器，最初由 Aladdin Enterprises 开发，现由 Artifex Software 维护。它能解析、渲染和转换 PS/EPS/PDF/XPS 文件，支持输出到打印设备或生成栅格化图像（如 JPEG、PNG）。

1. 下载GhostScript
[GhostScript下载地址](https://ghostscript.com/releases/gsdnld.html)
2. GhostScript安装
3. 把`D:\Program Files\gs\gs10.05.1\bin`添加到用户环境变量。


## 开发说明
```bash
# nuitka打包应用，推荐，体积小，但打包速度会慢一些
uv add nuitka # uv用户推荐
# 运行nuitka时，会自动下载指定版本的mingw64
# C:\Users\Lei\AppData\Local\Nuitka\Nuitka\Cache\DOWNLO~1\gcc\x86_64\14.2.0posix-19.1.1-12.0.0-msvcrt-r2\mingw64\bin\
python -m nuitka --standalone --onefile --windows-icon-from-ico=app_icon.ico --output-dir=dist --enable-plugin=tk-inter --windows-disable-console --include-data-file=app_icon.ico=app_icon.ico --include-data-dir=.venv/Lib/site-packages/ocrmypdf/data=ocrmypdf/data --output-filename=OCRmyPDF.exe OCRmyPDF/main.py


# 注意修改include-data-dir 对应的路径，为ocrmypdf/data的相对路径

# 说明：
# --standalone：打包所有依赖为独立目录
# --onefile：生成单一exe（可选，首次启动慢）
# --windows-icon-from-ico=app_icon.ico：指定exe图标
# --windows-disable-console：打包exe时关闭控制台
# --enable-plugin=tk-inter：自动包含tkinter依赖
# --include-data-file/--include-data-dir：如需额外资源（如icon、模型、说明文档等）可用
# --output-dir=dist：输出到dist目录
# --output-filename：指定输出exe文件名
# --onefile-compression=upx：使用UPX压缩exe文件，体积小，但打包速度会慢一些


# 或者pyinstaller打包应用
pyinstaller build.spec

# 使用nuitka打包后的程序大小 27.1MB，可以正常运行；使用pyinstaller打包后程序大小36.0MB，界面可以正常显示，但是点击按钮运行时会闪退，原因暂时未知。
```

## OCRmyPDF基本用法
### 使用示例1

```bash
ocrmypdf                      # it's a scriptable command line program
   -l chi_sim+eng             # it supports multiple languages
   --rotate-pages             # it can fix pages that are misrotated
   --deskew                   # it can deskew crooked PDFs!
   --title "My PDF"           # it can change output metadata
   --jobs 4                   # it uses multiple cores by default
   --output-type pdfa         # it produces PDF/A by default
   input_scanned.pdf          # takes PDF input (or images)
   output_searchable.pdf      # produces validated PDF output
```
### 使用示例2

```bash
# 查看帮助
ocrmypdf -h

# 基本OCR转换：将扫描的 PDF 转换为可搜索的 PDF/A 格式（默认输出）
ocrmypdf input.pdf output.pdf

# 指定语言识别：支持多语言 OCR，例如简体中文和英文混合文档 （chi_sim 为简体中文，eng 为英文）   
ocrmypdf -l chi_sim input.pdf output.pdf

# 图像预处理
# 纠偏（Deskew）：自动校正倾斜的页面
ocrmypdf --deskew input.pdf output.pdf
# 旋转页面：根据内容方向自动旋转
ocrmypdf --rotate-pages input.pdf output.pdf
# 优化图像质量：压缩文件大小并保持清晰度：
ocrmypdf --optimize 3 input.pdf output.pdf

# 高级输出选项    
# 生成纯文本：提取 OCR 文本到 .txt 文件：
ocrmypdf --sidecar output.txt input.pdf output.pdf

# 强制 OCR：即使已有文本层也重新识别：
ocrmypdf --force-ocr input.pdf output.pdf

# 指定输出格式：如普通 PDF 或黑白 PDF
ocrmypdf --output-type pdf input.pdf output.pdf


# 提高图像质量以获得更好的OCR结果
ocrmypdf --deskew --clean input.pdf output.pdf

ocrmypdf --skip-text 'E:\Lei\Downloads\PDF Test\拆分文件\pdf-sample_pages_1-1.pdf' 'E:\Lei\Downloads\PDF Test\拆分文件\pdf-sample_pages_1-1_ocr.pdf'
```

## 参考文章
- [OCRmyPDF官网](https://github.com/ocrmypdf/OCRmyPDF)
- [如何本地部署使用ocrmypdf](https://mp.weixin.qq.com/s/qHxT5tQb6wUnqGhLkezZzw)
- [扫描PDF档案效率提升300%！OCRmyPDF：告别无法搜索的PDF噩梦，这款26K Star的开源神器让文本识别轻松上手！](https://mp.weixin.qq.com/s/xJEgo0LJX0kcAGQpWe3GQg)
- [tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)
- [Tesseract语言数据包下载](https://github.com/tesseract-ocr/tessdata)