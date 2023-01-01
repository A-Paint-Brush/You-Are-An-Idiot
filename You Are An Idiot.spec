# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'Background.py', 'Mouse.py', 'Text.py', 'Time.py', 'Widgets.py'],
    pathex=[],
    binaries=[],
    datas=[(".\\Fonts\\*.ttf", ".\\Fonts"),
           (".\\Images\\Icon Resources\\16x16.bmp", ".\\Images\\Icon Resources"),
           (".\\Images\\UI Assets\\*.bmp", ".\\Images\\UI Assets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    name='You Are An Idiot',
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
    icon=['Images\\Icon Resources\\exe_icon.ico'],
)
