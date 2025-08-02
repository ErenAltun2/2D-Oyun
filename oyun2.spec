# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['oyun2.py'],
    pathex=[],
    binaries=[],
    datas=[('arka_plan1.png', '.'), ('arka_plan2.jpg', '.'), ('arka_plan3.png', '.'), ('tebrikler.png', '.'), ('oyuncu_mermi.png', '.'), ('uzayli.png', '.'), ('uzayli_mermi.png', '.'), ('oyuncu_mermi.wav', '.'), ('uzayli_vurus.wav', '.'), ('oyuncu_vurus.wav', '.'), ('altaylardan tunaya.wav', '.'), ('olurum.wav', '.'), ('deniz.wav', '.'), ('oyun_font.ttf', '.'), ('uzayli_mermi.wav', '.'), ('uzayli_mermi.wav', '.')],
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
    name='oyun2',
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
)
