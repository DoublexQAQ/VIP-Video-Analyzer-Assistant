# 此代码为VIP视频解析器，仅供学习交流使用，请勿用于商业用途。
# 请支持正版，购买视频网站会员。
# 作者：Double
# QQ群：563079037
# 赞助作者：https://afdian.com/a/DoubleQAQ
# 免责声明：本软件仅供学习交流使用，严禁用于商业用途。
# 请支持正版，购买视频网站会员。
# 本软件不存储任何视频内容。
# 使用本软件所产生的一切后果由用户自行承担。    
import tkinter as tk
import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk
import pyperclip
from urllib.parse import urlparse
import re
import pyautogui
import time
import keyboard
import os
import sys
import base64
import tempfile
import io

# 资源文件的 base64 编码

ICON_BASE64 = ''''''

GIF_BASE64 = ''''''

def get_icon():
    """获取图标的 PhotoImage 对象"""
    try:
        icon_data = base64.b64decode(ICON_BASE64)
        icon_image = Image.open(io.BytesIO(icon_data))
        return ImageTk.PhotoImage(icon_image)
    except Exception:
        return None

def get_gif():
    """获取 GIF 图像对象"""
    try:
        gif_data = base64.b64decode(GIF_BASE64)
        return Image.open(io.BytesIO(gif_data))
    except Exception:
        return None

def resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class VideoParser:
    def __init__(self):
        try:
            import selenium
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            self.show_warning(
                "首次使用需要安装必要组件！\n\n"
                "请执行以下命令：\n"
                "pip install selenium webdriver-manager"
            )
            sys.exit(1)
        
        # 设置主题和颜色
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("VIP视频解析")
        self.root.geometry("800x500")
        self.root.attributes('-topmost', True)
        
        # 设置窗口图标
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        
        # 设置透明效果和背景色
        self.root.attributes('-alpha', 0.95)  # 设置主窗口透明度
        
        # 扩展平台链接字典
        self.platform_urls = {
            "优酷视频": "https://www.youku.com/",
            "爱奇艺": "https://www.iqiyi.com/",
            "腾讯视频": "https://v.qq.com/",
            "哔哩哔哩": "https://www.bilibili.com/",
            "芒果TV": "https://www.mgtv.com/",
            "乐视视频": "https://www.le.com/",
            "暴风影音": "http://www.baofeng.com/",
            "搜狐视频": "https://tv.sohu.com/",
            "1905电影": "https://www.1905.com/",
            "PPTV": "https://www.pptv.com/",
            "风行视频": "http://www.fun.tv/",
            "AcFun": "https://www.acfun.cn/"
        }
        
        # 添加解析接口字典
        self.parse_apis = {
            "路线①": "https://www.yemu.xyz/?url=",
            "路线②": "https://www.8090g.cn/?url=",
            "路线③(加载有广告)": "https://im1907.top/?jx=",
            "路线④": "https://jx.playerjy.com/?url=",
            "路线⑤": "https://jx.xmflv.com/?url=",
            "路线⑥": "https://jx.m3u8.tv/jiexi/?url=",
            "路线⑦": "http://www.jzmhtt.com/zdy/vip/?url="
        }
        
        self.current_frame = None  # 用于跟踪当前显示的frame
        self.create_ui()
        
        # 显示防倒卖提示和免责声明
        self.show_warning("警告：本软件完全免费！\n如果你是购买的，说明你被骗了！\n\n本软件仅供学习交流使用，请勿用于商业用途。\n请支持正版，购买视频网站会员。")
        
    def create_ui(self):
        # 左侧面板
        left_panel = ctk.CTkFrame(
            self.root, 
            fg_color="#f0f0f0",
            width=200
        )
        left_panel.pack(side="left", fill="y", padx=2, pady=2)
        left_panel.pack_propagate(False)
        
        # 作者信息按钮
        author_btn = ctk.CTkButton(
            left_panel,
            text="关于作者",
            height=35,
            command=self.show_about,
            fg_color="#e0e0e0",
            hover_color="#c0c0c0",
            text_color="#000000",
            corner_radius=8
        )
        author_btn.pack(pady=20, padx=20, fill="x", side="bottom")
        
        # 添加动态GIF
        try:
            # 加载GIF图片
            gif = Image.open(resource_path("animation.gif"))
            
            # 获取GIF的所有帧
            frames = []
            try:
                while True:
                    frame = ImageTk.PhotoImage(gif.copy().resize((180, 180)))
                    frames.append(frame)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass
            
            if frames:
                # 创建标签显示GIF
                gif_label = tk.Label(left_panel, bg="#f0f0f0")
                gif_label.pack(expand=True)
                
                # 保存frames引用防止被垃圾回收
                self.frames = frames
                
                # 动画更新函数
                def update_frame(frame_index=0):
                    frame = self.frames[frame_index]
                    gif_label.configure(image=frame)
                    next_frame = (frame_index + 1) % len(self.frames)
                    self.root.after(50, update_frame, next_frame)
                
                # 开始动画
                update_frame()
        except Exception as e:
            pass
        
        # 右侧主面板
        self.main_panel = ctk.CTkFrame(
            self.root, 
            fg_color="#ffffff"  # 主面板背景色
        )
        self.main_panel.pack(side="right", fill="both", expand=True, padx=2, pady=2)
        
        # 创建主界面和关于作者界面
        self.create_main_frame()
        self.create_about_frame()
        
        # 默认显示主界面
        self.show_main_frame()
        
    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(
            self.main_panel, 
            fg_color="#e0f7fa"  # 主界面背景色
        )
        
        # 添加平台选择下拉框区域
        platform_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        platform_frame.pack(fill="x", padx=30, pady=(30, 0))
        
        # 平台选择标签
        platform_label = ctk.CTkLabel(
            platform_frame,
            text="选择视频平台：",
            font=ctk.CTkFont(size=14),
            text_color="#000000"  # 标签文本颜色
        )
        platform_label.pack(side="left", padx=(0, 10))
        
        # 创建平台列表
        platform_names = list(self.platform_urls.keys())
        
        # 创建下拉菜单
        self.platform_var = ctk.StringVar(value=platform_names[0])
        platform_dropdown = ctk.CTkOptionMenu(
            platform_frame,
            values=platform_names,
            variable=self.platform_var,
            width=200,
            height=35,
            fg_color="#e0e0e0",  # 下拉菜单背景色
            button_color="#c0c0c0",  # 按钮颜色
            button_hover_color="#b0b0b0",  # 悬停颜色
            dropdown_fg_color="#e0e0e0",  # 下拉菜单背景色
            dropdown_hover_color="#b0b0b0",  # 悬停颜色
            dropdown_text_color="#000000",  # 下拉菜单文本颜色
            text_color="#000000",  # 文本颜色
            font=ctk.CTkFont(size=13)
        )
        platform_dropdown.pack(side="left", padx=5)
        
        # 访问网站按钮
        visit_btn = ctk.CTkButton(
            platform_frame,
            text="访问网站",
            width=100,
            height=35,
            command=self.visit_selected_platform,
            fg_color="#e0e0e0",  # 按钮背景色
            hover_color="#c0c0c0",  # 悬停颜色
            text_color="#000000",  # 按钮文本颜色
            corner_radius=8
        )
        visit_btn.pack(side="left", padx=10)
        
        # 添加解析接口选择区域
        api_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        api_frame.pack(fill="x", padx=30, pady=(20, 0))
        
        # 解析接口选择标签
        api_label = ctk.CTkLabel(
            api_frame,
            text="选择解析接口：",
            font=ctk.CTkFont(size=14),
            text_color="#000000"
        )
        api_label.pack(side="left", padx=(0, 10))
        
        # 创建解析接口下拉菜单
        api_names = list(self.parse_apis.keys())
        self.api_var = ctk.StringVar(value=api_names[0])
        api_dropdown = ctk.CTkOptionMenu(
            api_frame,
            values=api_names,
            variable=self.api_var,
            width=200,
            height=35,
            fg_color="#e0e0e0",
            button_color="#c0c0c0",
            button_hover_color="#b0b0b0",
            dropdown_fg_color="#e0e0e0",
            dropdown_hover_color="#b0b0b0",
            dropdown_text_color="#000000",
            text_color="#000000",
            font=ctk.CTkFont(size=13)
        )
        api_dropdown.pack(side="left", padx=5)
        
        # URL输入区域
        url_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        url_frame.pack(fill="x", padx=30, pady=(20, 20))
        
        # URL输入框
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="请输入视频链接...",
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#ffffff",
            border_color="#c0c0c0",
            text_color="#000000",
            corner_radius=8
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 获取链接按钮
        get_url_btn = ctk.CTkButton(
            url_frame,
            text="获取链接",
            width=100,
            height=40,
            command=self.get_current_url,
            fg_color="#e0e0e0",
            hover_color="#c0c0c0",
            text_color="#000000",
            corner_radius=8
        )
        get_url_btn.pack(side="right", padx=5)
        
        # 清空输入框按钮
        clear_btn = ctk.CTkButton(
            url_frame,
            text="清空",
            width=100,
            height=40,
            command=lambda: self.url_entry.delete(0, 'end'),
            fg_color="#e0e0e0",
            hover_color="#c0c0c0",
            text_color="#000000",
            corner_radius=8
        )
        clear_btn.pack(side="right", padx=5)
        
        # 解析按钮
        parse_btn = ctk.CTkButton(
            url_frame,
            text="开始解析",
            width=100,
            height=40,
            command=self.parse_video,
            fg_color="#00bcd4",
            hover_color="#80deea",
            text_color="#000000",
            corner_radius=8
        )
        parse_btn.pack(side="right")
        
        # 分割线
        separator = ctk.CTkFrame(
            self.main_frame, 
            height=2, 
            fg_color="#c0c0c0"  # 分割线颜色
        )
        separator.pack(fill="x", padx=30, pady=30)
        
        # 使用说明
        tip_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tip_frame.pack(fill="x", padx=30)
        
        tips = [
            "使用说明：",
            "1. 点击按钮访问视频网站",
            "2. 找到想看的视频页面",
            "3. 点击'获取链接'按钮获取视频地址，或者手动复制输入视频地址",
            "4. 点击'开始解析'按钮观看视频"
        ]
        
        for i, tip in enumerate(tips):
            color = "#000000" if i == 0 else "#333333"  # 标题用黑色，内容用深灰色
            tip_label = ctk.CTkLabel(
                tip_frame,
                text=tip,
                font=ctk.CTkFont(size=13),
                text_color=color
            )
            tip_label.pack(anchor="w", pady=2)
            
    def create_about_frame(self):
        self.about_frame = ctk.CTkFrame(
            self.main_panel, 
            fg_color="#ffffff"
        )
        
        # 作者信息容器
        info_frame = ctk.CTkFrame(
            self.about_frame, 
            fg_color="#f0f0f0",
            corner_radius=15
        )
        info_frame.pack(padx=30, pady=30, fill="both", expand=True)
        
        # 标题
        title = ctk.CTkLabel(
            info_frame,
            text="作者信息",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#000000"
        )
        title.pack(pady=20)
        
        # 作者信息
        info_items = [
            ("作者", "Double"),
            ("QQ群", "563079037")
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            item_frame.pack(pady=10, fill="x", padx=30)
            
            label = ctk.CTkLabel(
                item_frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=14),
                text_color="#333333"
            )
            label.pack(side="left")
            
            value_label = ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color="#000000"
            )
            value_label.pack(side="right")
        
        # 添加免责声明
        disclaimer_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        disclaimer_frame.pack(pady=20, padx=30)
        
        disclaimer_text = (
            "免责声明：\n\n"
            "1. 本软件仅供学习交流使用，严禁用于商业用途\n"
            "2. 请支持正版，购买视频网站会员\n"
            "3. 本软件不存储任何视频内容\n"
            "4. 使用本软件所产生的一切后果由用户自行承担"
        )
        
        disclaimer_label = ctk.CTkLabel(
            disclaimer_frame,
            text=disclaimer_text,
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            justify="left"
        )
        disclaimer_label.pack(anchor="w")
        
        # 赞助按钮
        sponsor_btn = ctk.CTkButton(
            info_frame,
            text="赞助作者",
            command=lambda: webbrowser.open("https://afdian.com/a/DoubleQAQ"),
            height=40,
            fg_color="#00bcd4",
            hover_color="#80deea",
            text_color="#000000",
            corner_radius=8
        )
        sponsor_btn.pack(pady=20)
        
        # 返回按钮
        back_btn = ctk.CTkButton(
            info_frame,
            text="返回主页",
            command=self.show_main_frame,
            height=40,
            fg_color="#e0e0e0",
            hover_color="#c0c0c0",
            text_color="#000000",
            corner_radius=8
        )
        back_btn.pack(pady=(0, 20))
    
    def show_main_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.current_frame = self.main_frame
        
    def show_about(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.about_frame.pack(fill="both", expand=True)
        self.current_frame = self.about_frame
    
    def parse_video(self):
        url = self.url_entry.get()
        if url:
            selected_api = self.api_var.get()
            parse_url = f"{self.parse_apis[selected_api]}{url}"
            webbrowser.open(parse_url)
        else:
            self.show_warning("请先获取视频链接！")
            
    def open_platform(self, url):
        webbrowser.open(url)
        
    def get_current_url(self):
        try:
            # 清空剪贴板
            pyperclip.copy('')
            time.sleep(0.2)
            
            # 使用 F6 快捷键选中地址栏（适用于大多数浏览器）
            keyboard.press_and_release('f6')
            time.sleep(0.2)
            keyboard.press_and_release('f6')  # 某些浏览器需要按两次
            time.sleep(0.2)
            keyboard.press_and_release('f6')  # Edge浏览器可能需要按三次
            time.sleep(0.2)
            
            # 复制地址
            keyboard.press_and_release('ctrl+c')
            time.sleep(0.2)
            
            # 获取剪贴板内容
            url = pyperclip.paste().strip()
            
            # 如果获取失败，尝试使用 Alt+D
            if not url or not self.is_valid_video_url(url) or url == self.url_entry.get():
                pyperclip.copy('')  # 再次清空剪贴板
                time.sleep(0.2)
                keyboard.press_and_release('alt+d')  # 使用 Alt+D 选中地址栏
                time.sleep(0.2)
                keyboard.press_and_release('ctrl+c')
                time.sleep(0.2)
                url = pyperclip.paste().strip()
            
            # 验证并填入URL
            if url and self.is_valid_video_url(url) and url != self.url_entry.get():
                self.url_entry.delete(0, 'end')
                self.url_entry.insert(0, url)
            else:
                self.show_warning(
                    "获取链接失败！\n\n"
                    "请确保：\n"
                    "1. 浏览器窗口已打开视频页面\n"
                    "2. 点击获取前先切换到浏览器窗口\n"
                    "3. 如果还是无法获取，请手动复制视频链接"
                )
        except Exception as e:
            self.show_warning(
                "获取链接失败！\n\n"
                "请手动复制视频链接，或按F6选中地址栏后按Ctrl+C复制"
            )

    def paste_url(self):
        try:
            url = pyperclip.paste().strip()
            if url and self.is_valid_video_url(url):
                self.url_entry.delete(0, 'end')
                self.url_entry.insert(0, url)
            else:
                self.show_warning(
                    "无效的视频链接！\n\n"
                    "请确保复制的是视频播放页面的网址"
                )
        except Exception as e:
            self.show_warning("粘贴失败，请重试")
        
    def extract_url_from_title(self, title):
        # 从浏览器标题中提取URL
        for platform, domain in [
            ("腾讯视频", "v.qq.com"),
            ("爱奇艺", "iqiyi.com"),
            ("优酷", "youku.com"),
            ("哔哩哔哩", "bilibili.com")
        ]:
            if domain in title:
                # 使用正则表达式匹配URL
                url_pattern = f"https?://[\\w.-]+{domain}[\\w./-]*"
                match = re.search(url_pattern, title)
                if match:
                    return match.group(0)
        return None
        
    def is_valid_video_url(self, url):
        if not url:
            return False
        
        try:
            parsed = urlparse(url)
            # 扩展支持的域名列表和具体的URL模式
            supported_patterns = [
                ('youku.com', r'v\.youku\.com/v_show/id_'),
                ('iqiyi.com', r'www\.iqiyi\.com/[vw]_'),
                ('v.qq.com', r'v\.qq\.com/x/cover/|v\.qq\.com/x/page/'),
                ('bilibili.com', r'www\.bilibili\.com/video/'),
                ('mgtv.com', r'www\.mgtv\.com/b/'),
                ('le.com', r'www\.le\.com/ptv/vplay/'),
                ('sohu.com', r'tv\.sohu\.com/v/'),
                ('1905.com', r'www\.1905\.com/vod/play/'),
                ('pptv.com', r'v\.pptv\.com/show/'),
                ('fun.tv', r'www\.fun.tv/vplay/'),
                ('acfun.cn', r'www\.acfun\.cn/v/')
            ]
            
            return any(
                domain in parsed.netloc and re.search(pattern, url)
                for domain, pattern in supported_patterns
            )
        except:
            return False
        
    def show_warning(self, message):
        warning_window = ctk.CTkToplevel()
        warning_window.title("提示")
        warning_window.geometry("400x250")  # 增加窗口大小
        warning_window.attributes('-topmost', True)
        warning_window.transient(self.root)
        warning_window.configure(fg_color="#ffffff")
        
        # 设置提示窗口图标
        try:
            warning_window.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        
        # 创建一个框架来容纳文本
        text_frame = ctk.CTkFrame(
            warning_window,
            fg_color="transparent"
        )
        text_frame.pack(expand=True, fill="both", padx=20, pady=(20, 10))
        
        label = ctk.CTkLabel(
            text_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="#000000",
            wraplength=360,  # 设置文本换行宽度
            justify="center"
        )
        label.pack(expand=True)
        
        # 创建一个框架来容纳按钮
        button_frame = ctk.CTkFrame(
            warning_window,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        btn = ctk.CTkButton(
            button_frame,
            text="确定",
            command=warning_window.destroy,
            width=100,
            height=35,
            fg_color="#00bcd4",
            hover_color="#80deea",
            text_color="#000000",
            corner_radius=8
        )
        btn.pack(pady=10)
        
        # 设置窗口最小大小
        warning_window.update()
        warning_window.minsize(warning_window.winfo_width(), warning_window.winfo_height())
        
        # 将窗口居中显示
        window_width = warning_window.winfo_width()
        window_height = warning_window.winfo_height()
        screen_width = warning_window.winfo_screenwidth()
        screen_height = warning_window.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        warning_window.geometry(f"+{x}+{y}")

    def run(self):
        self.root.mainloop()

    def visit_selected_platform(self):
        selected_platform = self.platform_var.get()
        url = self.platform_urls[selected_platform]
        webbrowser.open(url)

if __name__ == "__main__":
    app = VideoParser()
    app.run() 