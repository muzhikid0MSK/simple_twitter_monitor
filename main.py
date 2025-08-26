#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter监控器主程序
支持GUI模式和服务器模式
"""

import sys
import os
import argparse
from i18n import set_language, i18n


def show_help():
    """显示帮助信息"""
    help_text = """
Twitter监控器 v2.0

使用方法:
  python main.py [选项]

选项:
  --gui, -g          启动GUI模式（默认）
  --server, -s       启动服务器模式
  --config, -c PATH  指定配置文件路径
  --language, -l LANG 设置语言 (zh_CN/en_US)
  --username, -u USER 要监控的Twitter用户名（服务器模式）
  --token, -t TOKEN   Twitter Auth Token（服务器模式）
  --interval, -i SEC  检查间隔（秒，服务器模式）
  --help, -h         显示此帮助信息

示例:
  # 启动GUI模式
  python main.py
  
  # 启动服务器模式，使用默认配置
  python main.py --server
  
  # 启动服务器模式，指定配置
  python main.py --server --config my_config.json
  
  # 启动服务器模式，命令行指定参数
  python main.py --server --username example --token your_token --interval 120
  
  # 指定语言
  python main.py --language en_US
  python main.py --server --language zh_CN

配置文件:
  默认配置文件: config.json
  可以通过 --config 参数指定其他配置文件

日志文件:
  服务器模式会在 logs/ 目录下生成日志文件
"""
    print(help_text)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Twitter监控器 v2.0',
        add_help=False
    )
    
    parser.add_argument('--gui', '-g', action='store_true', help='启动GUI模式（默认）')
    parser.add_argument('--server', '-s', action='store_true', help='启动服务器模式')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--language', '-l', choices=['zh_CN', 'en_US'], help='设置语言')
    parser.add_argument('--username', '-u', help='要监控的Twitter用户名（服务器模式）')
    parser.add_argument('--token', '-t', help='Twitter Auth Token（服务器模式）')
    parser.add_argument('--interval', '-i', type=int, help='检查间隔（秒，服务器模式）')
    parser.add_argument('--help', '-h', action='store_true', help='显示帮助信息')
    
    args = parser.parse_args()
    
    # 显示帮助信息
    if args.help:
        show_help()
        return
    
    # 设置语言
    if args.language:
        set_language(args.language)
    else:
        # 从配置文件读取语言设置
        try:
            from config_manager import ConfigManager
            config_manager = ConfigManager(args.config)
            language = config_manager.config['system']['language']
            set_language(language)
        except:
            # 如果读取配置失败，使用默认语言
            set_language('zh_CN')
    
    # 确定运行模式
    if args.server:
        # 服务器模式
        print("🚀 启动Twitter监控器服务器模式...")
        try:
            from server_mode import TwitterMonitorServer
            
            # 创建服务器实例
            server = TwitterMonitorServer(args.config, i18n.get_current_language())
            
            # 如果提供了命令行参数，更新配置
            if args.username:
                server.config['twitter']['username'] = args.username.lstrip('@')
            if args.token:
                server.config['twitter']['auth_token'] = args.token
            if args.interval:
                server.config['twitter']['check_interval'] = args.interval
            
            # 运行服务器
            server.run()
            
        except ImportError as e:
            print(f"❌ 导入服务器模块失败: {e}")
            print("请确保所有依赖模块都已正确安装")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 服务器运行失败: {e}")
            sys.exit(1)
            
    else:
        # GUI模式（默认）
        print("🖥️ 启动Twitter监控器GUI模式...")
        try:
            from gui import TwitterMonitorGUI
            
            # 创建并运行GUI
            app = TwitterMonitorGUI()
            app.run()
            
        except ImportError as e:
            print(f"❌ 导入GUI模块失败: {e}")
            print("请确保所有依赖模块都已正确安装")
            sys.exit(1)
        except Exception as e:
            print(f"❌ GUI运行失败: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
