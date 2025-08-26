#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChromeDriver故障排除脚本
用于诊断和解决Linux服务器上的chromedriver问题
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, capture_output=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_system_info():
    """检查系统信息"""
    print("=" * 60)
    print("系统信息检查")
    print("=" * 60)
    
    print(f"操作系统: {platform.system()}")
    print(f"架构: {platform.machine()}")
    print(f"Python版本: {sys.version}")
    
    # 检查是否为root用户
    is_root = os.geteuid() == 0
    print(f"Root权限: {'是' if is_root else '否'}")
    
    if not is_root:
        print("⚠️ 建议使用root权限运行此脚本")
    
    return is_root

def check_chrome_installation():
    """检查Chrome浏览器安装"""
    print("\n" + "=" * 60)
    print("Chrome浏览器检查")
    print("=" * 60)
    
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/snap/bin/chromium"
    ]
    
    chrome_installed = False
    chrome_version = None
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ 找到Chrome: {path}")
            chrome_installed = True
            
            # 获取版本
            success, stdout, stderr = run_command(f"{path} --version")
            if success:
                chrome_version = stdout.strip()
                print(f"   版本: {chrome_version}")
            break
    
    if not chrome_installed:
        print("❌ 未找到Chrome浏览器")
        print("建议安装Chrome:")
        print("Ubuntu/Debian: sudo apt-get install google-chrome-stable")
        print("CentOS/RHEL: sudo yum install google-chrome-stable")
        return False, None
    
    return True, chrome_version

def check_chromedriver_installation():
    """检查ChromeDriver安装"""
    print("\n" + "=" * 60)
    print("ChromeDriver检查")
    print("=" * 60)
    
    chromedriver_paths = [
        "/usr/local/bin/chromedriver",
        "/usr/bin/chromedriver",
        "/snap/bin/chromedriver",
        "./chromedriver",
        "./drivers/chromedriver"
    ]
    
    chromedriver_found = False
    chromedriver_path = None
    
    for path in chromedriver_paths:
        if os.path.exists(path):
            print(f"✅ 找到ChromeDriver: {path}")
            chromedriver_found = True
            chromedriver_path = path
            
            # 检查权限
            if os.access(path, os.X_OK):
                print(f"   权限: 可执行")
                
                # 获取版本
                success, stdout, stderr = run_command(f"{path} --version")
                if success:
                    print(f"   版本: {stdout.strip()}")
                else:
                    print(f"   版本检查失败: {stderr}")
            else:
                print(f"   权限: 不可执行")
                print("   尝试修复权限...")
                try:
                    os.chmod(path, 0o755)
                    if os.access(path, os.X_OK):
                        print("   ✅ 权限修复成功")
                    else:
                        print("   ❌ 权限修复失败")
                except Exception as e:
                    print(f"   ❌ 权限修复失败: {e}")
            
            break
    
    if not chromedriver_found:
        print("❌ 未找到ChromeDriver")
        return False, None
    
    return True, chromedriver_path

def check_dependencies():
    """检查系统依赖"""
    print("\n" + "=" * 60)
    print("系统依赖检查")
    print("=" * 60)
    
    # 检查必要的库
    required_libs = [
        "libX11.so.6",
        "libXcomposite.so.1",
        "libXcursor.so.1",
        "libXdamage.so.1",
        "libXext.so.6",
        "libXfixes.so.3",
        "libXi.so.6",
        "libXrandr.so.2",
        "libXrender.so.1",
        "libXss.so.1",
        "libXtst.so.6"
    ]
    
    missing_libs = []
    
    for lib in required_libs:
        success, stdout, stderr = run_command(f"ldconfig -p | grep {lib}")
        if success:
            print(f"✅ {lib}")
        else:
            print(f"❌ {lib}")
            missing_libs.append(lib)
    
    if missing_libs:
        print(f"\n缺少的库: {', '.join(missing_libs)}")
        print("建议安装:")
        print("Ubuntu/Debian: sudo apt-get install libx11-6 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6")
        print("CentOS/RHEL: sudo yum install libX11 libXcomposite libXcursor libXdamage libXext libXfixes libXi libXrandr libXrender libXScrnSaver libXtst")
        return False
    else:
        print("✅ 所有必要的库都已安装")
        return True

def test_chromedriver(chromedriver_path):
    """测试ChromeDriver"""
    print("\n" + "=" * 60)
    print("ChromeDriver测试")
    print("=" * 60)
    
    if not chromedriver_path:
        print("❌ 没有可用的ChromeDriver路径")
        return False
    
    try:
        # 尝试导入selenium
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        print("✅ Selenium导入成功")
        
        # 设置Chrome选项
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        
        print("正在测试ChromeDriver...")
        
        # 创建服务
        service = Service(chromedriver_path)
        
        # 创建驱动
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ ChromeDriver创建成功")
        
        # 测试访问网页
        driver.get("https://www.google.com")
        print("✅ 网页访问成功")
        
        # 关闭驱动
        driver.quit()
        print("✅ ChromeDriver测试完全成功")
        return True
        
    except ImportError as e:
        print(f"❌ Selenium导入失败: {e}")
        print("建议安装: pip install selenium")
        return False
    except Exception as e:
        print(f"❌ ChromeDriver测试失败: {e}")
        return False

def download_chromedriver():
    """下载ChromeDriver"""
    print("\n" + "=" * 60)
    print("下载ChromeDriver")
    print("=" * 60)
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("正在使用webdriver-manager下载ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver下载成功: {driver_path}")
        return True, driver_path
        
    except Exception as e:
        print(f"❌ 自动下载失败: {e}")
        print("尝试手动下载...")
        
        # 手动下载逻辑
        success, stdout, stderr = run_command("google-chrome --version")
        if success:
            version = stdout.strip().split()[-1].split('.')[0]
            print(f"Chrome版本: {version}")
            
            if int(version) >= 115:
                # 新版本
                print("使用Chrome for Testing下载...")
                # 这里可以添加手动下载逻辑
                print("请手动下载: https://googlechromelabs.github.io/chrome-for-testing/")
            else:
                # 旧版本
                print("使用旧版下载...")
                print("请手动下载: https://chromedriver.chromium.org/")
        
        return False, None

def main():
    """主函数"""
    print("ChromeDriver故障排除工具")
    print("适用于Linux服务器环境")
    
    # 检查系统信息
    is_root = check_system_info()
    
    # 检查Chrome
    chrome_ok, chrome_version = check_chrome_installation()
    
    # 检查ChromeDriver
    chromedriver_ok, chromedriver_path = check_chromedriver_installation()
    
    # 检查依赖
    deps_ok = check_dependencies()
    
    # 测试ChromeDriver
    if chromedriver_ok and chromedriver_path:
        test_ok = test_chromedriver(chromedriver_path)
    else:
        test_ok = False
    
    # 总结和建议
    print("\n" + "=" * 60)
    print("问题总结和建议")
    print("=" * 60)
    
    if not chrome_ok:
        print("❌ 主要问题: Chrome浏览器未安装")
        print("解决方案: 安装Google Chrome浏览器")
    
    if not chromedriver_ok:
        print("❌ 主要问题: ChromeDriver未安装")
        print("解决方案: 下载并安装ChromeDriver")
    
    if not deps_ok:
        print("❌ 主要问题: 系统依赖缺失")
        print("解决方案: 安装必要的系统库")
    
    if not test_ok and chromedriver_ok:
        print("❌ 主要问题: ChromeDriver无法正常工作")
        print("解决方案: 检查权限和依赖")
    
    if chrome_ok and chromedriver_ok and deps_ok and test_ok:
        print("✅ 所有检查都通过！ChromeDriver应该可以正常工作")
    else:
        print("\n建议按以下顺序解决问题:")
        print("1. 确保Chrome浏览器已安装")
        print("2. 安装必要的系统依赖")
        print("3. 下载并安装ChromeDriver")
        print("4. 设置正确的权限")
        print("5. 测试ChromeDriver")
        
        print("\n或者运行安装脚本:")
        print("chmod +x install_linux_chromedriver.sh")
        print("sudo ./install_linux_chromedriver.sh")

if __name__ == "__main__":
    main()
