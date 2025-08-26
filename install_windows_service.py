#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows服务安装脚本
用于将Twitter监控器安装为Windows系统服务
"""

import os
import sys
import winreg
import subprocess
from pathlib import Path


def check_admin():
    """检查是否具有管理员权限"""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def install_pywin32():
    """安装pywin32（如果未安装）"""
    try:
        import win32serviceutil
        import win32service
        import win32event
        print("✅ pywin32已安装")
        return True
    except ImportError:
        print("📦 正在安装pywin32...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
            print("✅ pywin32安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ pywin32安装失败")
            return False


def create_windows_service():
    """创建Windows服务文件"""
    service_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter监控器Windows服务
"""

import sys
import os
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from pathlib import Path

# 添加项目路径到Python路径
project_path = Path(__file__).parent
sys.path.insert(0, str(project_path))

from server_mode import TwitterMonitorServer


class TwitterMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TwitterMonitor"
    _svc_display_name_ = "Twitter Monitor Service"
    _svc_description_ = "Twitter账户监控服务，自动检测新推文并发送邮件通知"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.server = None
        
    def SvcStop(self):
        """停止服务"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.server:
            self.server.stop_monitoring()
        
    def SvcDoRun(self):
        """运行服务"""
        try:
            # 设置工作目录
            os.chdir(str(Path(__file__).parent))
            
            # 创建服务器实例
            self.server = TwitterMonitorServer()
            
            # 启动监控
            self.server.start_monitoring()
            
            # 等待停止信号
            while True:
                if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                    break
                    
        except Exception as e:
            import logging
            logging.error(f"服务运行出错: {e}")
            raise


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TwitterMonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TwitterMonitorService)
'''
    
    service_file = Path("twitter_monitor_service.py")
    with open(service_file, "w", encoding="utf-8") as f:
        f.write(service_code)
    
    print(f"✅ 服务文件已创建: {service_file}")
    return service_file


def install_service(service_file):
    """安装Windows服务"""
    try:
        print("🔧 正在安装Windows服务...")
        
        # 使用pywin32安装服务
        cmd = [sys.executable, str(service_file), "install"]
        subprocess.check_call(cmd)
        
        print("✅ Windows服务安装成功")
        print()
        print("服务信息:")
        print(f"  服务名称: TwitterMonitor")
        print(f"  显示名称: Twitter Monitor Service")
        print(f"  描述: Twitter账户监控服务")
        print()
        print("管理命令:")
        print(f"  启动服务: net start TwitterMonitor")
        print(f"  停止服务: net stop TwitterMonitor")
        print(f"  删除服务: {sys.executable} {service_file} remove")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 服务安装失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🔧 Twitter监控器 - Windows服务安装")
    print("=" * 60)
    
    # 检查管理员权限
    if not check_admin():
        print("❌ 错误: 需要管理员权限来安装Windows服务")
        print("请以管理员身份运行此脚本")
        input("按回车键退出...")
        sys.exit(1)
    
    # 检查pywin32
    if not install_pywin32():
        print("❌ 无法安装pywin32，服务安装失败")
        input("按回车键退出...")
        sys.exit(1)
    
    # 创建服务文件
    service_file = create_windows_service()
    
    # 安装服务
    if install_service(service_file):
        print()
        print("🎉 服务安装完成！")
        print("现在可以通过Windows服务管理器或命令行管理服务")
    else:
        print()
        print("❌ 服务安装失败")
    
    input("按回车键退出...")


if __name__ == "__main__":
    main()
