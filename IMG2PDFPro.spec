# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['IMG2PDFPro\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('IMG2PDFPro/app_icon.ico', 'IMG2PDFPro'), ('IMG2PDFPro/app_icon.png', 'IMG2PDFPro')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='IMG2PDFPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['IMG2PDFPro\\app_icon.ico'],
)
