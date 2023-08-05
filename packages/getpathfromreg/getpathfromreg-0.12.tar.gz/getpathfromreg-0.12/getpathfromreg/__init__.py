import os

from reggisearch import search_values


def get_bluestacks_user_folder():
    di = search_values(
        mainkeys=r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt", subkeys="UserDefinedDir"
    )
    bstconfigpath = di[r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt"]["UserDefinedDir"]
    return bstconfigpath

def get_bluestacks_config_file():
    bstconfigpath=get_bluestacks_user_folder()
    bstconfigpath = os.path.normpath(os.path.join(bstconfigpath, "bluestacks.conf"))
    return bstconfigpath

def get_tesseract_exe():
    tesserkey = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Tesseract-OCR'
    tesserf='UninstallString'
    di = search_values(mainkeys=tesserkey, subkeys=(tesserf,))
    pa = f'{os.sep}'.join(di[tesserkey][tesserf].split(os.sep)[:-1])
    pa = os.path.normpath(os.path.join(pa,'tesseract.exe'))
    return pa

def get_hd_player_bluestacks():
    di = search_values(
        mainkeys=r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt", subkeys="InstallDir"
    )
    bstconfigpath = di[r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt"]["InstallDir"]
    bstconfigpath = os.path.normpath(os.path.join(bstconfigpath, "HD-Player.exe"))
    return bstconfigpath


