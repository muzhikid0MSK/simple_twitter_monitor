"""
GUI界面模块
使用tkinter创建简单的图形用户界面
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime
from config_manager import ConfigManager
from twitter_monitor import TwitterMonitor
from email_sender import EmailSender


class TwitterMonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        
        # 从环境变量获取语言设置
        from i18n import i18n
        self.language = i18n.get_current_language()
        
        # 设置窗口标题
        if self.language == "zh_CN":
            self.root.title("Twitter监控器 v1.0")
        else:
            self.root.title("Twitter Monitor v1.0")
            
        self.root.geometry("600x1100")
        self.root.resizable(False, False)
        
        # 设置样式
        self.setup_styles()
        
        # 配置管理器
        self.config_manager = ConfigManager()
        
        # 监控器实例
        self.monitor = None
        self.monitor_thread = None
        self.is_monitoring = False
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置
        self.load_config()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 设置颜色
        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.accent_color = "#1DA1F2"
        
        self.root.configure(bg=self.bg_color)
        
        # 自定义按钮样式
        style.configure("Start.TButton", font=('Arial', 10, 'bold'))
        style.configure("Stop.TButton", font=('Arial', 10, 'bold'))
    
    def on_email_provider_changed(self, event=None):
        """邮箱服务商变更时的处理"""
        provider = self.email_provider_var.get()
        
        # 获取预设配置
        from i18n import i18n
        presets = i18n.get_smtp_presets()
        
        if provider in presets:
            # 使用预设配置
            preset = presets[provider]
            self.smtp_server_entry.delete(0, tk.END)
            self.smtp_server_entry.insert(0, preset["server"])
            
            self.smtp_port_entry.delete(0, tk.END)
            self.smtp_port_entry.insert(0, str(preset["port"]))
            
            # 根据服务商设置默认连接方式
            if provider in ["163", "qq"]:
                self.use_ssl_var.set(True)
                self.use_tls_var.set(False)
            elif provider in ["gmail", "outlook", "yahoo"]:
                self.use_ssl_var.set(False)
                self.use_tls_var.set(True)
            
            # 禁用手动编辑
            self.smtp_server_entry.config(state="readonly")
            self.smtp_port_entry.config(state="readonly")
        else:
            # 自定义配置，启用手动编辑
            self.smtp_server_entry.config(state="normal")
            self.smtp_port_entry.config(state="normal")
    
    def on_connection_changed(self):
        """连接方式变更时的处理"""
        # 确保SSL和TLS不会同时选中
        if self.use_tls_var.get():
            self.use_ssl_var.set(False)
        elif self.use_ssl_var.get():
            self.use_tls_var.set(False)
    
    def on_language_changed(self, event=None):
        """语言切换处理"""
        new_language = self.language_var.get()
        if new_language != self.language:
            # 保存语言设置到配置文件
            self.config_manager.config['system']['language'] = new_language
            self.config_manager.save_config(self.config_manager.config)
            
            # 显示提示信息
            if new_language == "zh_CN":
                messagebox.showinfo("提示", "语言已切换到中文，重启程序后生效！")
            else:
                messagebox.showinfo("Info", "Language changed to English, restart program to take effect!")
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.root, bg=self.accent_color, height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        # 根据语言设置标题
        if self.language == "zh_CN":
            title_text = "🐦 Twitter 监控器"
        else:
            title_text = "🐦 Twitter Monitor"
            
        title_label = tk.Label(
            title_frame,
            text=title_text,
            font=('Arial', 18, 'bold'),
            bg=self.accent_color,
            fg='white'
        )
        title_label.pack(expand=True)
        
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Twitter配置区域
        if self.language == "zh_CN":
            twitter_frame = ttk.LabelFrame(main_frame, text="Twitter 配置", padding=10)
        else:
            twitter_frame = ttk.LabelFrame(main_frame, text="Twitter Configuration", padding=10)
        twitter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 用户名
        if self.language == "zh_CN":
            username_label = "监听用户名 (@):"
        else:
            username_label = "Monitor Username (@):"
        tk.Label(twitter_frame, text=username_label).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(twitter_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Auth Token
        tk.Label(twitter_frame, text="Auth Token:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.token_entry = ttk.Entry(twitter_frame, width=30, show="*")
        self.token_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # 检查间隔
        if self.language == "zh_CN":
            interval_label = "检查间隔 (秒):"
        else:
            interval_label = "Check Interval (seconds):"
        tk.Label(twitter_frame, text=interval_label).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.interval_spinbox = ttk.Spinbox(twitter_frame, from_=30, to=3600, width=28)
        self.interval_spinbox.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.interval_spinbox.set(60)
        
        # 邮箱配置区域
        if self.language == "zh_CN":
            email_frame = ttk.LabelFrame(main_frame, text="邮箱配置", padding=10)
        else:
            email_frame = ttk.LabelFrame(main_frame, text="Email Configuration", padding=10)
        email_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 邮箱服务商选择
        if self.language == "zh_CN":
            provider_label = "邮箱服务商:"
        else:
            provider_label = "Email Provider:"
        tk.Label(email_frame, text=provider_label).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_provider_var = tk.StringVar(value="163")
        self.email_provider_combo = ttk.Combobox(email_frame, textvariable=self.email_provider_var, 
                                               values=["163", "qq", "gmail", "outlook", "yahoo", "custom"], 
                                               width=27, state="readonly")
        self.email_provider_combo.grid(row=0, column=1, pady=5, padx=(10, 0))
        self.email_provider_combo.bind("<<ComboboxSelected>>", self.on_email_provider_changed)
        
        # SMTP服务器
        if self.language == "zh_CN":
            smtp_server_label = "SMTP服务器:"
        else:
            smtp_server_label = "SMTP Server:"
        tk.Label(email_frame, text=smtp_server_label).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.smtp_server_entry = ttk.Entry(email_frame, width=30)
        self.smtp_server_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # SMTP端口
        if self.language == "zh_CN":
            smtp_port_label = "SMTP端口:"
        else:
            smtp_port_label = "SMTP Port:"
        tk.Label(email_frame, text=smtp_port_label).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.smtp_port_entry = ttk.Entry(email_frame, width=30)
        self.smtp_port_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # 连接方式
        if self.language == "zh_CN":
            connection_label = "连接方式:"
        else:
            connection_label = "Connection Type:"
        tk.Label(email_frame, text=connection_label).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.connection_frame = tk.Frame(email_frame)
        self.connection_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        self.use_ssl_var = tk.BooleanVar(value=True)
        self.use_tls_var = tk.BooleanVar(value=False)
        
        ttk.Radiobutton(self.connection_frame, text="SSL", variable=self.use_ssl_var, 
                       value=True, command=self.on_connection_changed).pack(side=tk.LEFT)
        ttk.Radiobutton(self.connection_frame, text="TLS", variable=self.use_tls_var, 
                       value=True, command=self.on_connection_changed).pack(side=tk.LEFT, padx=(10, 0))
        if self.language == "zh_CN":
            normal_text = "普通"
        else:
            normal_text = "Normal"
        ttk.Radiobutton(self.connection_frame, text=normal_text, variable=self.use_ssl_var, 
                       value=False, command=self.on_connection_changed).pack(side=tk.LEFT, padx=(10, 0))
        
        # 发件人邮箱
        if self.language == "zh_CN":
            sender_email_label = "发件人邮箱:"
        else:
            sender_email_label = "Sender Email:"
        tk.Label(email_frame, text=sender_email_label).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.sender_email_entry = ttk.Entry(email_frame, width=30)
        self.sender_email_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # 邮箱密码/授权码
        if self.language == "zh_CN":
            password_label = "邮箱密码/授权码:"
        else:
            password_label = "Email Password/Auth Code:"
        tk.Label(email_frame, text=password_label).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.email_password_entry = ttk.Entry(email_frame, width=30, show="*")
        self.email_password_entry.grid(row=5, column=1, pady=5, padx=(10, 0))
        
        # 接收邮箱
        if self.language == "zh_CN":
            receiver_email_label = "接收邮箱:"
        else:
            receiver_email_label = "Receiver Email:"
        tk.Label(email_frame, text=receiver_email_label).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.receiver_email_entry = ttk.Entry(email_frame, width=30)
        self.receiver_email_entry.grid(row=6, column=1, pady=5, padx=(10, 0))
        
        # 浏览器配置区域
        if self.language == "zh_CN":
            browser_frame = ttk.LabelFrame(main_frame, text="浏览器配置", padding=10)
        else:
            browser_frame = ttk.LabelFrame(main_frame, text="Browser Configuration", padding=10)
        browser_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 无头模式
        self.headless_var = tk.BooleanVar()
        if self.language == "zh_CN":
            headless_text = "无头模式（后台运行，不显示浏览器窗口）"
        else:
            headless_text = "Headless Mode (run in background, no browser window)"
        self.headless_check = ttk.Checkbutton(
            browser_frame,
            text=headless_text,
            variable=self.headless_var
        )
        self.headless_check.pack(anchor=tk.W, pady=(0, 5))
        
        # ChromeDriver路径（可选）
        if self.language == "zh_CN":
            driver_path_label = "ChromeDriver路径 (可选):"
        else:
            driver_path_label = "ChromeDriver Path (optional):"
        tk.Label(browser_frame, text=driver_path_label).pack(anchor=tk.W, pady=(5, 0))
        
        # 路径输入框
        path_frame = tk.Frame(browser_frame)
        path_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.chrome_driver_entry = ttk.Entry(path_frame, width=50)
        self.chrome_driver_entry.pack(side=tk.LEFT)
        
        # 提示文字另起一行
        if self.language == "zh_CN":
            auto_download_text = "留空则自动下载"
        else:
            auto_download_text = "Leave empty for auto-download"
        tk.Label(browser_frame, text=auto_download_text, font=('Arial', 8), fg='gray').pack(anchor=tk.W, pady=(2, 0))
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 保存配置按钮
        if self.language == "zh_CN":
            save_text = "💾 保存配置"
        else:
            save_text = "💾 Save Config"
        self.save_button = ttk.Button(
            button_frame,
            text=save_text,
            command=self.save_config
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 测试邮箱按钮
        if self.language == "zh_CN":
            test_text = "📧 测试邮箱"
        else:
            test_text = "📧 Test Email"
        self.test_email_button = ttk.Button(
            button_frame,
            text=test_text,
            command=self.test_email
        )
        self.test_email_button.pack(side=tk.LEFT, padx=5)
        
        # 开始监控按钮
        if self.language == "zh_CN":
            start_text = "▶️ 开始监控"
        else:
            start_text = "▶️ Start Monitor"
        self.start_button = ttk.Button(
            button_frame,
            text=start_text,
            command=self.start_monitoring,
            style="Start.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # 停止监控按钮
        if self.language == "zh_CN":
            stop_text = "⏹️ 停止监控"
        else:
            stop_text = "⏹️ Stop Monitor"
        self.stop_button = ttk.Button(
            button_frame,
            text=stop_text,
            command=self.stop_monitoring,
            style="Stop.TButton",
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 日志区域
        if self.language == "zh_CN":
            log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding=10)
        else:
            log_frame = ttk.LabelFrame(main_frame, text="Run Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=6,
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 语言切换区域
        language_frame = tk.Frame(main_frame, bg=self.bg_color)
        language_frame.pack(fill=tk.X, pady=(0, 10))
        
        if self.language == "zh_CN":
            language_label = "界面语言:"
        else:
            language_label = "Interface Language:"
        tk.Label(language_frame, text=language_label).pack(side=tk.LEFT)
        
        self.language_var = tk.StringVar(value=self.language)
        language_combo = ttk.Combobox(
            language_frame, 
            textvariable=self.language_var,
            values=["zh_CN", "en_US"],
            state="readonly",
            width=10
        )
        language_combo.pack(side=tk.LEFT, padx=(10, 0))
        language_combo.bind("<<ComboboxSelected>>", self.on_language_changed)
        
        # 状态栏
        if self.language == "zh_CN":
            status_text = "就绪"
        else:
            status_text = "Ready"
        self.status_label = tk.Label(
            self.root,
            text=status_text,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=self.bg_color
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log(self, message: str):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def load_config(self):
        """加载配置到界面"""
        config = self.config_manager.config
        
        # Twitter配置
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, config['twitter']['username'])
        
        self.token_entry.delete(0, tk.END)
        self.token_entry.insert(0, config['twitter']['auth_token'])
        
        self.interval_spinbox.delete(0, tk.END)
        self.interval_spinbox.insert(0, str(config['twitter']['check_interval']))
        
        # 邮箱配置
        # 设置邮箱服务商
        email_provider = config['email'].get('provider', '163')
        self.email_provider_var.set(email_provider)
        
        # 设置SMTP服务器和端口
        self.smtp_server_entry.delete(0, tk.END)
        # 从国际化模块获取默认值，避免硬编码
        from i18n import i18n
        default_provider = config['email'].get('provider', '163')
        presets = i18n.get_smtp_presets()
        default_server = presets.get(default_provider, {}).get('server', 'smtp.163.com')
        self.smtp_server_entry.insert(0, config['email'].get('smtp_server', default_server))
        
        self.smtp_port_entry.delete(0, tk.END)
        default_port = presets.get(default_provider, {}).get('port', 465)
        self.smtp_port_entry.insert(0, str(config['email'].get('smtp_port', default_port)))
        
        # 设置连接方式
        self.use_ssl_var.set(config['email'].get('use_ssl', True))
        self.use_tls_var.set(config['email'].get('use_tls', False))
        
        # 设置邮箱地址
        self.sender_email_entry.delete(0, tk.END)
        self.sender_email_entry.insert(0, config['email']['sender_email'])
        
        self.email_password_entry.delete(0, tk.END)
        self.email_password_entry.insert(0, config['email']['sender_password'])
        
        self.receiver_email_entry.delete(0, tk.END)
        self.receiver_email_entry.insert(0, config['email']['receiver_email'])
        
        # 触发邮箱服务商变更事件以设置正确的状态
        self.on_email_provider_changed()
        
        # 浏览器配置
        self.headless_var.set(config['browser']['headless'])
        
        self.chrome_driver_entry.delete(0, tk.END)
        self.chrome_driver_entry.insert(0, config['browser'].get('chrome_driver_path', ''))
        
        self.log("✅ 配置加载成功")
    
    def save_config(self):
        """保存配置"""
        config = self.config_manager.config
        
        # Twitter配置
        config['twitter']['username'] = self.username_entry.get().strip().lstrip('@')
        config['twitter']['auth_token'] = self.token_entry.get().strip()
        config['twitter']['check_interval'] = int(self.interval_spinbox.get())
        
        # 邮箱配置
        config['email']['provider'] = self.email_provider_var.get()
        config['email']['smtp_server'] = self.smtp_server_entry.get().strip()
        config['email']['smtp_port'] = int(self.smtp_port_entry.get().strip())
        config['email']['use_ssl'] = self.use_ssl_var.get()
        config['email']['use_tls'] = self.use_tls_var.get()
        config['email']['sender_email'] = self.sender_email_entry.get().strip()
        config['email']['sender_password'] = self.email_password_entry.get().strip()
        config['email']['receiver_email'] = self.receiver_email_entry.get().strip()
        
        # 浏览器配置
        config['browser']['headless'] = self.headless_var.get()
        config['browser']['chrome_driver_path'] = self.chrome_driver_entry.get().strip()
        
        if self.config_manager.save_config(config):
            self.log("✅ 配置保存成功")
            if self.language == "zh_CN":
                messagebox.showinfo("成功", "配置保存成功！")
            else:
                messagebox.showinfo("Success", "Configuration saved successfully!")
        else:
            self.log("❌ 配置保存失败")
            if self.language == "zh_CN":
                messagebox.showerror("错误", "配置保存失败！")
            else:
                messagebox.showerror("Error", "Failed to save configuration!")
    
    def test_email(self):
        """测试邮箱配置"""
        sender_email = self.sender_email_entry.get().strip()
        sender_password = self.email_password_entry.get().strip()
        receiver_email = self.receiver_email_entry.get().strip()
        
        if not all([sender_email, sender_password, receiver_email]):
            if self.language == "zh_CN":
                messagebox.showwarning("警告", "请填写完整的邮箱配置！")
            else:
                messagebox.showwarning("Warning", "Please complete all email configuration fields!")
            return
        
        self.log("📧 正在测试邮箱配置...")
        
        # 在新线程中测试
        def test():
            smtp_server = self.smtp_server_entry.get().strip()
            smtp_port = int(self.smtp_port_entry.get().strip())
            
            email_sender = EmailSender(
                smtp_server,
                smtp_port,
                sender_email,
                sender_password,
                self.use_ssl_var.get(),
                self.use_tls_var.get()
            )
            
            if email_sender.test_connection(receiver_email):
                self.log("✅ 邮箱测试成功")
                if self.language == "zh_CN":
                    messagebox.showinfo("成功", "测试邮件发送成功！\n请检查接收邮箱。")
                else:
                    messagebox.showinfo("Success", "Test email sent successfully!\nPlease check your inbox.")
            else:
                self.log("❌ 邮箱测试失败")
                if self.language == "zh_CN":
                    messagebox.showerror("错误", "测试邮件发送失败！\n请检查邮箱配置。")
                else:
                    messagebox.showerror("Error", "Failed to send test email!\nPlease check email configuration.")
        
        threading.Thread(target=test, daemon=True).start()
    
    def on_new_tweet(self, username: str, tweet: dict):
        """新推文回调函数"""
        self.log(f"🆕 发现新推文: {tweet['text'][:100]}...")
        
        # 发送邮件通知
        smtp_server = self.smtp_server_entry.get().strip()
        smtp_port = int(self.smtp_port_entry.get().strip())
        sender_email = self.sender_email_entry.get().strip()
        sender_password = self.email_password_entry.get().strip()
        receiver_email = self.receiver_email_entry.get().strip()
        
        email_sender = EmailSender(
            smtp_server,
            smtp_port,
            sender_email,
            sender_password,
            self.use_ssl_var.get(),
            self.use_tls_var.get()
        )
        
        if email_sender.send_notification(
            receiver_email,
            username,
            tweet['text'],
            tweet.get('url')
        ):
            self.log("✅ 邮件通知已发送")
        else:
            self.log("❌ 邮件发送失败")
    
    def start_monitoring(self):
        """开始监控"""
        # 获取配置
        username = self.username_entry.get().strip().lstrip('@')
        auth_token = self.token_entry.get().strip()
        check_interval = int(self.interval_spinbox.get())
        headless = self.headless_var.get()
        
        # 验证配置
        if not username:
            if self.language == "zh_CN":
                messagebox.showwarning("警告", "请输入要监听的Twitter用户名！")
            else:
                messagebox.showwarning("Warning", "Please enter the Twitter username to monitor!")
            return
        
        if not auth_token:
            if self.language == "zh_CN":
                messagebox.showwarning("警告", "请输入Twitter Auth Token！")
            else:
                messagebox.showwarning("Warning", "Please enter Twitter Auth Token!")
            return
        
        # 验证邮箱配置
        smtp_server = self.smtp_server_entry.get().strip()
        smtp_port = self.smtp_port_entry.get().strip()
        sender_email = self.sender_email_entry.get().strip()
        sender_password = self.email_password_entry.get().strip()
        receiver_email = self.receiver_email_entry.get().strip()
        
        if not all([smtp_server, smtp_port, sender_email, sender_password, receiver_email]):
            if self.language == "zh_CN":
                messagebox.showwarning("警告", "请填写完整的邮箱配置！")
            else:
                messagebox.showwarning("Warning", "Please complete all email configuration fields!")
            return
        
        try:
            smtp_port = int(smtp_port)
        except ValueError:
            if self.language == "zh_CN":
                messagebox.showwarning("警告", "SMTP端口必须是数字！")
            else:
                messagebox.showwarning("Warning", "SMTP port must be a number!")
            return
        
        # 更新界面状态
        self.is_monitoring = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        if self.language == "zh_CN":
            status_text = f"监控中: @{username}"
        else:
            status_text = f"Monitoring: @{username}"
        self.status_label.config(text=status_text)
        
        self.log(f"🚀 开始监控 @{username}")
        
        # 获取ChromeDriver路径（如果配置了）
        chrome_driver_path = self.chrome_driver_entry.get().strip()
        if not chrome_driver_path:
            chrome_driver_path = None
        
        # 创建监控器
        self.monitor = TwitterMonitor(auth_token, headless, chrome_driver_path)
        
        # 在新线程中启动监控
        def monitor_thread():
            try:
                self.monitor.start_monitoring(
                    username,
                    check_interval,
                    self.on_new_tweet
                )
            except Exception as e:
                self.log(f"❌ 监控出错: {str(e)}")
            finally:
                self.root.after(0, self.on_monitoring_stopped)
        
        self.monitor_thread = threading.Thread(target=monitor_thread, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """停止监控"""
        if self.monitor:
            self.log("⏹️ 正在停止监控...")
            self.monitor.monitoring = False
            self.monitor.stop_monitoring()
        
        self.on_monitoring_stopped()
    
    def on_monitoring_stopped(self):
        """监控停止后的处理"""
        self.is_monitoring = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.language == "zh_CN":
            status_text = "就绪"
        else:
            status_text = "Ready"
        self.status_label.config(text=status_text)
        self.log("✅ 监控已停止")
    
    def run(self):
        """运行GUI"""
        # 窗口关闭时的处理
        def on_closing():
            if self.is_monitoring:
                if self.language == "zh_CN":
                    if messagebox.askokcancel("退出", "监控正在运行，确定要退出吗？"):
                        self.stop_monitoring()
                        self.root.destroy()
                else:
                    if messagebox.askokcancel("Exit", "Monitoring is running, are you sure you want to exit?"):
                        self.stop_monitoring()
                        self.root.destroy()
            else:
                self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 居中窗口
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()
