


## 应用需求
使用python写一个项目IMG2PDFPro(代码存放到IMG2PDFPro文件夹)，使用Tkinter和customTkinter实现UI，通过[img2pdf](https://pypi.org/project/img2pdf/)，选择一个或多个图像文件(支持png\jpg\jpeg等img2pdf支持的格式)，点击按钮后选择要保存的PDF文件位置和文件名，自动将图片转为PDF文件。UI要高端美化，ui与逻辑分离。满足如下要求：
1. main.py进行界面调用，UI和逻辑在各自文件中保存。
2. 图片可以通过点击按钮选择、或者拖入实现选择图片文件。

## 创建环境

```bash
# 项目目前开发环境已经使用uv创建好了，如下：
.venv\Scripts\activate # 激活环境
uv add tkinterdnd2 # 实现拖入文件到UI的功能
uv run IMG2PDFPro/main.py # 运行项目

pip freeze > requirements.txt # 导出依赖
pip install -r requirements.txt # 安装依赖
uv pip install -r pyproject.toml # 安装依赖

uv remove nuitka pyinstaller

```

## 参考代码

```bash
import img2pdf

# opening from filename
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg'))

# opening from file handle
with open("name.pdf","wb") as f1, open("test.jpg") as f2:
	f1.write(img2pdf.convert(f2))

# opening using pathlib
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(pathlib.Path('test.jpg')))

# using in-memory image data
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert("\x89PNG...")

# multiple inputs (variant 1)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert("test1.jpg", "test2.png"))

# multiple inputs (variant 2)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(["test1.jpg", "test2.png"]))

# convert all files ending in .jpg inside a directory
dirname = "/path/to/images"
imgs = []
for fname in os.listdir(dirname):
	if not fname.endswith(".jpg"):
		continue
	path = os.path.join(dirname, fname)
	if os.path.isdir(path):
		continue
	imgs.append(path)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(imgs))

# convert all files ending in .jpg in a directory and its subdirectories
dirname = "/path/to/images"
imgs = []
for r, _, f in os.walk(dirname):
	for fname in f:
		if not fname.endswith(".jpg"):
			continue
		imgs.append(os.path.join(r, fname))
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(imgs))


# convert all files matching a glob
import glob
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(glob.glob("/path/to/*.jpg")))

# convert all files matching a glob using pathlib.Path
from pathlib import Path
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(*Path("/path").glob("**/*.jpg")))

# ignore invalid rotation values in the input images
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg'), rotation=img2pdf.Rotation.ifvalid)

# writing to file descriptor
with open("name.pdf","wb") as f1, open("test.jpg") as f2:
	img2pdf.convert(f2, outputstream=f1)

# specify paper size (A4)
a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4inpt)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg', layout_fun=layout_fun))

# use a fixed dpi of 300 instead of reading it from the image
dpix = dpiy = 300
layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg', layout_fun=layout_fun))

# create a PDF/A-1b compliant document by passing an ICC profile
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert('test.jpg', pdfa="/usr/share/color/icc/sRGB.icc"))
```

## pyinstaller打包应用
```bash
# 隐藏控制台窗口（正式发布用）：
.venv\Scripts\activate # 激活环境
pyinstaller -F -w --icon=IMG2PDFPro/app_icon.ico --add-data "IMG2PDFPro/app_icon.ico;IMG2PDFPro" --add-data "IMG2PDFPro/app_icon.png;IMG2PDFPro" --name=IMG2PDFPro IMG2PDFPro/main.py
# --add-data "源文件;目标目录" Windows下分号;，Linux/macOS下用冒号:。
```