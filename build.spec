# build.spec
block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('.venv/Lib/site-packages/customtkinter', 'customtkinter'),
        ('.venv/Lib/site-packages/ocrmypdf/data', 'ocrmypdf/data')
    ],
    hiddenimports=[
        'pkg_resources.py2_warn',
        'pkg_resources.markers',
        'ocrmypdf._exec.ghostscript',
        'ocrmypdf._exec.tesseract',
        'ocrmypdf._exec.pngquant',
        'ocrmypdf._exec.unpaper',
        'ocrmypdf._exec.qpdf',
        'lxml.etree',
        'lxml._elementpath',
        'skimage.filters.rank.core_cy',
        'skimage.filters.rank.generic_cy',
        'skimage.filters.rank.core_cy_3d',
        'skimage.filters.rank.generic_cy_3d',
        'pikepdf._cpphelpers'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF_OCR_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='app_icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)