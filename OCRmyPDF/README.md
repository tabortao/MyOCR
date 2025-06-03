# OCRmyPDF 说明文档

## 项目简介

`OCRmyPDF` 基于 Python 开发，主要用于对 PDF 文件进行批量文字识别（OCR），并生成可搜索的 PDF 文档。

![OCRmyPDF UI](../docs/Image/20250603155601-UI.jpg)

## 目录结构

- `app.py`：负责界面。
- `main.py`：主程序入口。
- `ocr_processor.py`：OCR 处理核心模块，封装了对 PDF 的识别与处理。
- `__pycache__/`：Python 编译生成的缓存文件夹。

## 依赖环境

- Python 3.12 及以上
- 推荐使用虚拟环境
- 主要依赖库：
  - ocrmypdf
  - 其他依赖请参考项目根目录的 `pyproject.toml` 或 `uv.lock`

## 快速开始

1. 安装依赖：
    ```bash
    uv pip install -r pyproject.toml
    ```
2. 运行主程序：
    ```bash
    uv run OCRmyPDF/main.py
    ```

## 功能说明

- 支持批量 PDF 文件 OCR 识别
- 支持命令行与图形界面两种模式
- 识别后生成可搜索的 PDF 文件

## 相关文档

- [批量识别说明](../docs/OCRmyPDF手册/批量识别.md)
- [OCRMyPDF使用说明](../docs/OCRmyPDF手册/OCRMyPDF使用说明.md)

## 联系与反馈

如有问题或建议，请在项目 issue 区留言。
