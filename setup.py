import sys
from cx_Freeze import setup, Executable

# 依赖项
build_exe_options = {
    "packages": ["tkinter", "PIL", "pyperclip", "pyautogui", "pywin32"],
    "include_files": ["icon.ico"],  # 包含图标文件
    "excludes": [],  # 可以在这里排除不需要的包
}

# 设置基础
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # GUI 应用程序

setup(
    name="VideoParser",
    version="1.0",
    description="VIP白嫖小助手",
    options={"build_exe": build_exe_options},
    executables=[Executable("video_parser.py", base=base, icon="icon.ico")],
)