# -*- mode: python -*-

block_cipher = None


a = Analysis(['qt5_irDataViewerv11-pyWindows.py'],
             pathex=['C:\\Users\\KarlP\\Documents\\GitHub\\purethermal1-uvc-capture\\ui_software\\Post_Process_IR'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='qt5_irDataViewerv11-pyWindows',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='qt5_irDataViewerv11-pyWindows')
