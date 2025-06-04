import os
import ocrmypdf
from pdfminer.high_level import extract_text
import logging
import shutil
import re

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PDF_OCR")

class CallbackHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        msg = self.format(record)
        if self.callback:
            self.callback(msg)

class OCRProcessor:
    @staticmethod
    def process_pdf(input_path, output_path, output_txt=False, lang="chi_sim+eng", 
                   deskew=True, rotate_pages=True, clean=False, optimize_level=1,
                   force_ocr=False, skip_text=False, ocr_engine="tesseract", psm=3, dpi=300,
                   log_callback=None):
        callback_handler = None
        if log_callback:
            callback_handler = CallbackHandler(log_callback)
            callback_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(message)s')
            callback_handler.setFormatter(formatter)
            logging.getLogger().addHandler(callback_handler)
            logging.getLogger("PDF_OCR").addHandler(callback_handler)
            logging.getLogger("ocrmypdf").addHandler(callback_handler)
        try:
            # 自动关闭 clean 选项如果未安装 unpaper
            if clean and shutil.which("unpaper") is None:
                logger.warning("未检测到 unpaper，已自动关闭清理图像选项。")
                clean = False
            # 自动创建输出目录
            out_dir = os.path.dirname(output_path)
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)

            # 创建OCR选项（仅保留最基础参数）
            ocr_options = {
                'output_type': 'pdfa',
                'progress_bar': False,
            }
            if log_callback:
                log_callback(f"开始处理: {input_path}")
            logger.info(f"开始处理: {os.path.basename(input_path)}")
            logger.info(f"OCR选项: {ocr_options}, lang: {lang}")
            if log_callback:
                log_callback("正在进行OCR识别...")
            ocrmypdf.ocr(input_path, output_path, lang=lang, tesseract_pagesegmode=6, **ocr_options)
            if not os.path.exists(output_path):
                return False, f"处理失败: 未生成输出文件 {os.path.basename(output_path)}"
            if output_txt:
                txt_path = os.path.splitext(output_path)[0] + ".txt"
                logger.info(f"提取文本到: {txt_path}")
                try:
                    text = extract_text(output_path)
                    # 优化：去除汉字间多余空格
                    text = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', text)
                    with open(txt_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)
                except Exception as e:
                    logger.warning(f"文本提取失败: {e}")
                    return True, f"PDF处理成功，但文本提取失败: {os.path.basename(input_path)}"
            if log_callback:
                log_callback(f"OCR完成: {output_path}")
            return True, f"处理成功: {os.path.basename(input_path)}"
        except ocrmypdf.exceptions.PriorOcrFoundError:
            return False, f"跳过处理 ({os.path.basename(input_path)}): 文件已有文本层"
        except ocrmypdf.exceptions.EncryptedPdfError:
            return False, f"处理失败 ({os.path.basename(input_path)}): 文件已加密"
        except ocrmypdf.exceptions.InputFileError as e:
            return False, f"输入文件错误 ({os.path.basename(input_path)}): {str(e)}"
        except Exception as e:
            logger.exception("处理过程中发生错误")
            return False, f"处理失败 ({os.path.basename(input_path)}): {str(e)}"
        finally:
            # 移除 handler，避免重复输出
            if callback_handler:
                logging.getLogger().removeHandler(callback_handler)
                logging.getLogger("PDF_OCR").removeHandler(callback_handler)
                logging.getLogger("ocrmypdf").removeHandler(callback_handler)