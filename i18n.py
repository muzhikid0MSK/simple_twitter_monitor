"""
国际化支持模块
支持中文和英文两种语言
"""
import json
import os
from typing import Dict, Any


class I18nManager:
    """国际化管理器"""
    
    def __init__(self, language: str = "zh_CN"):
        """
        初始化国际化管理器
        
        Args:
            language: 语言代码，支持 'zh_CN' 和 'en_US'
        """
        self.language = language
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """加载翻译文件"""
        translations = {
            "zh_CN": {
                # 主界面
                "app_title": "Twitter监控器 v1.0",
                "twitter_config": "Twitter 配置",
                "username_label": "监听用户名 (@):",
                "auth_token_label": "Auth Token:",
                "check_interval_label": "检查间隔 (秒):",
                
                # 邮箱配置
                "email_config": "邮箱配置",
                "smtp_server_label": "SMTP服务器:",
                "smtp_port_label": "SMTP端口:",
                "sender_email_label": "发件人邮箱:",
                "sender_password_label": "邮箱密码/授权码:",
                "receiver_email_label": "接收邮箱:",
                
                # 浏览器配置
                "browser_config": "浏览器配置",
                "headless_mode": "无头模式（后台运行，不显示浏览器窗口）",
                "chrome_driver_path": "ChromeDriver路径 (可选):",
                "auto_download": "留空则自动下载",
                
                # 按钮
                "save_config": "💾 保存配置",
                "test_email": "📧 测试邮箱",
                "start_monitoring": "▶️ 开始监控",
                "stop_monitoring": "⏹️ 停止监控",
                
                # 日志区域
                "run_log": "运行日志",
                "status_ready": "就绪",
                "status_monitoring": "监控中",
                
                # 消息框
                "warning": "警告",
                "error": "错误",
                "success": "成功",
                "info": "信息",
                
                # 提示信息
                "enter_username": "请输入要监听的Twitter用户名！",
                "enter_token": "请输入Twitter Auth Token！",
                "complete_email_config": "请填写完整的邮箱配置！",
                "config_saved": "配置保存成功！",
                "config_save_failed": "配置保存失败！",
                "email_test_success": "测试邮件发送成功！请检查接收邮箱。",
                "email_test_failed": "测试邮件发送失败！请检查邮箱配置。",
                "monitoring_started": "开始监控",
                "monitoring_stopped": "监控已停止",
                "exit_confirm": "监控正在运行，确定要退出吗？",
                
                # 日志消息
                "config_loaded": "✅ 配置加载成功",
                "config_saved_log": "✅ 配置保存成功",
                "config_save_failed_log": "❌ 配置保存失败",
                "email_testing": "📧 正在测试邮箱配置...",
                "email_test_success_log": "✅ 邮箱测试成功",
                "email_test_failed_log": "❌ 邮箱测试失败",
                "monitoring_start": "🚀 开始监控",
                "monitoring_stop": "⏹️ 正在停止监控...",
                "monitoring_stopped_log": "✅ 监控已停止",
                "new_tweet_found": "🆕 发现新推文",
                "email_sent": "✅ 邮件通知已发送",
                "email_send_failed": "❌ 邮件发送失败",
                
                # 邮件内容
                "email_subject_new_tweet": "🔔 @{username} 发布了新推文",
                "email_subject_test": "Twitter监控器 - 邮箱配置测试",
                "email_content_test": "这是一封测试邮件，用于验证邮箱配置是否正确。\n如果您收到这封邮件，说明配置成功！",
                "email_content_new_tweet": "Twitter 新推文通知\n\n@{username} 发布了新推文：\n\n{content}\n\n检测时间：{time}",
                
                # 默认配置
                "default_smtp_servers": {
                    "163": "smtp.163.com",
                    "qq": "smtp.qq.com",
                    "gmail": "smtp.gmail.com",
                    "outlook": "smtp-mail.outlook.com",
                    "yahoo": "smtp.mail.yahoo.com"
                },
                "default_smtp_ports": {
                    "163": 465,
                    "qq": 587,
                    "gmail": 587,
                    "outlook": 587,
                    "yahoo": 587
                }
            },
            "en_US": {
                # Main interface
                "app_title": "Twitter Monitor v1.0",
                "twitter_config": "Twitter Configuration",
                "username_label": "Username to monitor (@):",
                "auth_token_label": "Auth Token:",
                "check_interval_label": "Check Interval (seconds):",
                
                # Email configuration
                "email_config": "Email Configuration",
                "smtp_server_label": "SMTP Server:",
                "smtp_port_label": "SMTP Port:",
                "sender_email_label": "Sender Email:",
                "sender_password_label": "Email Password/App Password:",
                "receiver_email_label": "Receiver Email:",
                
                # Browser configuration
                "browser_config": "Browser Configuration",
                "headless_mode": "Headless mode (run in background)",
                "chrome_driver_path": "ChromeDriver Path (optional):",
                "auto_download": "Leave empty for auto-download",
                
                # Buttons
                "save_config": "💾 Save Config",
                "test_email": "📧 Test Email",
                "start_monitoring": "▶️ Start Monitoring",
                "stop_monitoring": "⏹️ Stop Monitoring",
                
                # Log area
                "run_log": "Run Log",
                "status_ready": "Ready",
                "status_monitoring": "Monitoring",
                
                # Message boxes
                "warning": "Warning",
                "error": "Error",
                "success": "Success",
                "info": "Information",
                
                # Prompt messages
                "enter_username": "Please enter the Twitter username to monitor!",
                "enter_token": "Please enter Twitter Auth Token!",
                "complete_email_config": "Please complete email configuration!",
                "config_saved": "Configuration saved successfully!",
                "config_save_failed": "Configuration save failed!",
                "email_test_success": "Test email sent successfully! Please check your receiver email.",
                "email_test_failed": "Test email failed! Please check email configuration.",
                "monitoring_started": "Monitoring started",
                "monitoring_stopped": "Monitoring stopped",
                "exit_confirm": "Monitoring is running, are you sure to exit?",
                
                # Log messages
                "config_loaded": "✅ Configuration loaded successfully",
                "config_saved_log": "✅ Configuration saved successfully",
                "config_save_failed_log": "❌ Configuration save failed",
                "email_testing": "📧 Testing email configuration...",
                "email_test_success_log": "✅ Email test successful",
                "email_test_failed_log": "❌ Email test failed",
                "monitoring_start": "🚀 Start monitoring",
                "monitoring_stop": "⏹️ Stopping monitoring...",
                "monitoring_stopped_log": "✅ Monitoring stopped",
                "new_tweet_found": "🆕 New tweet found",
                "email_sent": "✅ Email notification sent",
                "email_send_failed": "❌ Email sending failed",
                
                # Email content
                "email_subject_new_tweet": "🔔 @{username} posted a new tweet",
                "email_subject_test": "Twitter Monitor - Email Configuration Test",
                "email_content_test": "This is a test email to verify email configuration.\nIf you receive this email, the configuration is successful!",
                "email_content_new_tweet": "Twitter New Tweet Notification\n\n@{username} posted a new tweet:\n\n{content}\n\nDetection time: {time}",
                
                # Default configuration
                "default_smtp_servers": {
                    "163": "smtp.163.com",
                    "qq": "smtp.qq.com",
                    "gmail": "smtp.gmail.com",
                    "outlook": "smtp-mail.outlook.com",
                    "yahoo": "smtp.mail.yahoo.com"
                },
                "default_smtp_ports": {
                    "163": 465,
                    "qq": 587,
                    "gmail": 587,
                    "outlook": 587,
                    "yahoo": 587
                }
            }
        }
        return translations
    
    def get(self, key: str, **kwargs) -> str:
        """
        获取翻译文本
        
        Args:
            key: 翻译键
            **kwargs: 格式化参数
        
        Returns:
            翻译后的文本
        """
        if self.language not in self.translations:
            self.language = "zh_CN"  # 默认使用中文
        
        if key not in self.translations[self.language]:
            # 如果找不到翻译，返回键名
            return key
        
        text = self.translations[self.language][key]
        
        # 如果有格式化参数，进行格式化
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text
    
    def set_language(self, language: str):
        """设置语言"""
        if language in ["zh_CN", "en_US"]:
            self.language = language
        else:
            self.language = "zh_CN"
    
    def get_current_language(self) -> str:
        """获取当前语言"""
        return self.language
    
    def get_available_languages(self) -> list:
        """获取可用语言列表"""
        return list(self.translations.keys())
    
    def get_smtp_presets(self) -> Dict[str, Dict[str, Any]]:
        """获取SMTP预设配置"""
        return {
            "163": {
                "server": self.get("default_smtp_servers")["163"],
                "port": self.get("default_smtp_ports")["163"],
                "name": "163邮箱 (163.com)"
            },
            "qq": {
                "server": self.get("default_smtp_servers")["qq"],
                "port": self.get("default_smtp_ports")["qq"],
                "name": "QQ邮箱 (qq.com)"
            },
            "gmail": {
                "server": self.get("default_smtp_servers")["gmail"],
                "port": self.get("default_smtp_ports")["gmail"],
                "name": "Gmail (gmail.com)"
            },
            "outlook": {
                "server": self.get("default_smtp_servers")["outlook"],
                "port": self.get("default_smtp_ports")["outlook"],
                "name": "Outlook (outlook.com)"
            },
            "yahoo": {
                "server": self.get("default_smtp_servers")["yahoo"],
                "port": self.get("default_smtp_ports")["yahoo"],
                "name": "Yahoo Mail (yahoo.com)"
            }
        }


# 全局国际化管理器实例
# 从配置文件读取语言设置
try:
    from config_manager import ConfigManager
    config_manager = ConfigManager()
    default_language = config_manager.config.get('system', {}).get('language', 'zh_CN')
except ImportError:
    # 如果导入失败，使用默认语言
    default_language = "zh_CN"

i18n = I18nManager(default_language)


def get_text(key: str, **kwargs) -> str:
    """获取翻译文本的便捷函数"""
    return i18n.get(key, **kwargs)


def set_language(language: str):
    """设置语言的便捷函数"""
    i18n.set_language(language)
