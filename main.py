"""
Twitter监控器主程序
监听指定Twitter账户的新帖子并发送邮件通知
"""
import sys
import os
from gui import TwitterMonitorGUI
from i18n import set_language


def main():
    """主函数"""
    # 从配置文件读取语言设置
    from config_manager import ConfigManager
    config_manager = ConfigManager()
    language = config_manager.config.get('system', {}).get('language', 'zh_CN')
    set_language(language)
    
    print("=" * 50)
    if language == "zh_CN":
        print("🐦 Twitter监控器 v1.0")
        print("=" * 50)
        print()
        print("功能说明：")
        print("1. 监听指定Twitter账户的新帖子")
        print("2. 发现新帖子时通过163邮箱发送通知")
        print("3. 支持Token登录和自动刷新")
        print()
        print("正在启动图形界面...")
        print()
    else:
        print("🐦 Twitter Monitor v1.0")
        print("=" * 50)
        print()
        print("Features:")
        print("1. Monitor specified Twitter account for new posts")
        print("2. Send email notifications via 163 email when new posts are found")
        print("3. Support Token login and auto-refresh")
        print()
        print("Starting GUI...")
        print()
    
    try:
        # 创建并运行GUI
        app = TwitterMonitorGUI()
        app.run()
    except Exception as e:
        if language == "zh_CN":
            print(f"❌ 程序运行出错：{str(e)}")
            input("按回车键退出...")
        else:
            print(f"❌ Program error: {str(e)}")
            input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
