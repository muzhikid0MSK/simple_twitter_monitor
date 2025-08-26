#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter监控器服务器模式启动脚本
用于在服务器上无界面运行
"""

import sys
import os
import time
from datetime import datetime


def main():
    """主函数"""
    print("=" * 60)
    print("🐦 Twitter监控器 - 服务器模式")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 错误: 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    
    # 检查依赖模块
    required_modules = [
        'config_manager',
        'twitter_monitor', 
        'email_sender',
        'i18n'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ 缺少必要的模块:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\n请运行以下命令安装依赖:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ 依赖检查通过")
    print()
    
    # 启动服务器模式
    try:
        from server_mode import TwitterMonitorServer
        
        # 创建服务器实例
        server = TwitterMonitorServer()
        
        print("🚀 正在启动监控服务器...")
        print("按 Ctrl+C 停止服务器")
        print()
        
        # 运行服务器
        server.run()
        
    except KeyboardInterrupt:
        print("\n🛑 收到停止信号，正在关闭服务器...")
    except Exception as e:
        print(f"\n❌ 服务器运行出错: {e}")
        print("请检查配置文件和相关设置")
        sys.exit(1)
    finally:
        print("✅ 服务器已关闭")
        print(f"关闭时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
