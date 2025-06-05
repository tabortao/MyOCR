
## OCRmyPDF应用打包命令
```bash
git clone https://gitee.com/tabortao/MyOCR
cd MyOCR
uv venv .venv # 创建虚拟环境
.venv\Scripts\activate # 激活虚拟环境
uv pip install -r pyproject.toml # 安装依赖
uv add nuitka
python -m nuitka --standalone --show-memory --show-progress --show-scons --nofollow-imports --windows-disable-console --windows-icon-from-ico=app_icon.ico --output-dir=dist --enable-plugin=tk-inter --follow-import-to=OCRmyPDF --include-data-file=app_icon.ico=app_icon.ico --include-data-dir=.venv/Lib/site-packages/ocrmypdf/data=ocrmypdf/data --include-package=ocrmypdf,pdfminer,pikepdf  --output-filename=OCRmyPDF.exe OCRmyPDF/main.py
```
