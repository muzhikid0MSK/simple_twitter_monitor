"""
模块测试脚本
用于测试各个模块是否正常工作
"""
import sys
import json
from datetime import datetime


def test_imports():
    """测试导入模块"""
    print("测试模块导入...")
    modules_ok = True
    
    # 测试标准库
    try:
        import tkinter
        print("✅ tkinter (GUI库) - OK")
    except ImportError:
        print("❌ tkinter (GUI库) - 未安装")
        modules_ok = False
    
    # 测试第三方库
    try:
        import selenium
        print(f"✅ selenium - OK (版本: {selenium.__version__})")
    except ImportError:
        print("❌ selenium - 未安装，请运行: pip install selenium")
        modules_ok = False
    
    try:
        from selenium import webdriver
        print("✅ selenium.webdriver - OK")
    except ImportError:
        print("❌ selenium.webdriver - 导入失败")
        modules_ok = False
    
    try:
        import webdriver_manager
        print("✅ webdriver_manager - OK")
    except ImportError:
        print("❌ webdriver_manager - 未安装，请运行: pip install webdriver-manager")
        modules_ok = False
    
    # 测试自定义模块
    try:
        import config_manager
        print("✅ config_manager - OK")
    except ImportError as e:
        print(f"❌ config_manager - 导入失败: {e}")
        modules_ok = False
    
    try:
        import email_sender
        print("✅ email_sender - OK")
    except ImportError as e:
        print(f"❌ email_sender - 导入失败: {e}")
        modules_ok = False
    
    try:
        import twitter_monitor
        print("✅ twitter_monitor - OK")
    except ImportError as e:
        print(f"❌ twitter_monitor - 导入失败: {e}")
        modules_ok = False
    
    try:
        import gui
        print("✅ gui - OK")
    except ImportError as e:
        print(f"❌ gui - 导入失败: {e}")
        modules_ok = False
    
    return modules_ok


def test_config_manager():
    """测试配置管理器"""
    print("\n测试配置管理器...")
    
    try:
        from config_manager import ConfigManager
        
        # 创建配置管理器
        cm = ConfigManager()
        print("✅ 创建ConfigManager实例 - OK")
        
        # 测试默认配置
        default_config = cm.get_default_config()
        assert 'twitter' in default_config
        assert 'email' in default_config
        assert 'browser' in default_config
        print("✅ 获取默认配置 - OK")
        
        # 测试获取配置项
        smtp_server = cm.get('email.smtp_server')
        assert smtp_server == 'smtp.163.com'
        print("✅ 获取配置项 - OK")
        
        # 测试设置配置项
        cm.set('twitter.username', 'test_user')
        assert cm.get('twitter.username') == 'test_user'
        print("✅ 设置配置项 - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")
        return False


def test_email_sender():
    """测试邮件发送器（仅测试创建实例）"""
    print("\n测试邮件发送器...")
    
    try:
        from email_sender import EmailSender
        
        # 创建邮件发送器（使用假的配置）
        sender = EmailSender(
            smtp_server="smtp.163.com",
            smtp_port=465,
            sender_email="test@163.com",
            sender_password="test_password"
        )
        print("✅ 创建EmailSender实例 - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送器测试失败: {e}")
        return False


def test_chrome_driver():
    """测试Chrome驱动"""
    print("\n测试Chrome驱动...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        print("正在检查Chrome驱动...")
        
        # 设置选项
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # 尝试创建驱动（仅测试，立即关闭）
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.quit()
            print("✅ Chrome驱动 - OK")
            return True
        except Exception as e:
            print(f"❌ Chrome驱动测试失败: {e}")
            print("请确保已安装Chrome浏览器")
            return False
            
    except ImportError as e:
        print(f"❌ 无法导入selenium模块: {e}")
        return False


def test_gui_creation():
    """测试GUI创建（不显示窗口）"""
    print("\n测试GUI创建...")
    
    try:
        import tkinter as tk
        
        # 创建测试窗口但不显示
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 测试基本组件
        label = tk.Label(root, text="Test")
        button = tk.Button(root, text="Test")
        entry = tk.Entry(root)
        
        root.destroy()
        print("✅ GUI组件创建 - OK")
        return True
        
    except Exception as e:
        print(f"❌ GUI测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("="*60)
    print("Twitter监控器 - 模块测试")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python版本: {sys.version}")
    print("="*60)
    
    all_ok = True
    
    # 1. 测试导入
    if not test_imports():
        all_ok = False
    
    # 2. 测试配置管理器
    if not test_config_manager():
        all_ok = False
    
    # 3. 测试邮件发送器
    if not test_email_sender():
        all_ok = False
    
    # 4. 测试GUI
    if not test_gui_creation():
        all_ok = False
    
    # 5. 测试Chrome驱动（可选）
    print("\n是否测试Chrome驱动？这将下载ChromeDriver（约10MB）")
    choice = input("输入 y 测试，其他键跳过: ").strip().lower()
    if choice == 'y':
        if not test_chrome_driver():
            all_ok = False
    
    # 总结
    print("\n" + "="*60)
    if all_ok:
        print("✅ 所有测试通过！程序可以正常运行。")
        print("\n下一步:")
        print("1. 运行 python main.py 启动程序")
        print("2. 配置Twitter账户和邮箱信息")
        print("3. 开始监控")
    else:
        print("❌ 部分测试失败，请根据错误信息修复问题。")
        print("\n可能的解决方案:")
        print("1. 运行 pip install -r requirements.txt 安装依赖")
        print("2. 确保Python版本 >= 3.7")
        print("3. 确保已安装Chrome浏览器")
    print("="*60)


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
