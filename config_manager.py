"""
配置管理模块
用于保存和加载用户配置
"""
import json
import os
from typing import Dict, Any

CONFIG_FILE = "config.json"


class ConfigManager:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return self.get_default_config()
        return self.get_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.config = config
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "twitter": {
                "username": "",  # 要监听的Twitter用户名（不带@）
                "auth_token": "",  # Twitter auth_token
                "check_interval": 60  # 检查间隔（秒）
            },
            "email": {
                "provider": "163",  # 邮箱服务商：163, qq, gmail, outlook, yahoo, custom
                "smtp_server": "smtp.163.com",
                "smtp_port": 465,
                "sender_email": "",  # 发件人邮箱地址
                "sender_password": "",  # 邮箱密码或授权码
                "receiver_email": "",  # 接收邮件的邮箱
                "use_ssl": True,  # 是否使用SSL连接
                "use_tls": False  # 是否使用TLS连接
            },
            "browser": {
                "headless": False,  # 是否无头模式
                "chrome_driver_path": ""  # ChromeDriver路径（留空则自动下载）
            },
            "system": {
                "language": "zh_CN",  # 界面语言：zh_CN 或 en_US
                "auto_start": False,  # 是否开机自启动
                "minimize_to_tray": True  # 是否最小化到系统托盘
            }
        }
    
    def get(self, key: str, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """设置配置项"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
