"""
ChromeDriver设置工具
自动检测Chrome版本并下载匹配的ChromeDriver
"""
import os
import sys
import platform
import subprocess
import json
import zipfile
import shutil
from pathlib import Path
import urllib.request


def get_chrome_version():
    """获取Chrome浏览器版本"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows下通过注册表获取Chrome版本
            try:
                import winreg
                key_path = r"SOFTWARE\Google\Chrome\BLBeacon"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version
            except:
                # 尝试通过命令行获取
                paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
                ]
                for path in paths:
                    if os.path.exists(path):
                        result = subprocess.run(
                            [path, "--version"],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            # 格式: Google Chrome 120.0.6099.130
                            version = result.stdout.strip().split()[-1]
                            return version
                            
        elif system == "Darwin":  # macOS
            result = subprocess.run(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                return version
                
        elif system == "Linux":
            result = subprocess.run(
                ["google-chrome", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                return version
                
    except Exception as e:
        print(f"获取Chrome版本失败: {e}")
    
    return None


def download_chromedriver(version):
    """下载对应版本的ChromeDriver"""
    system = platform.system()
    
    # 获取主版本号
    major_version = version.split('.')[0]
    
    print(f"Chrome版本: {version}")
    print(f"正在查找ChromeDriver...")
    
    # ChromeDriver下载地址（新版本）
    if int(major_version) >= 115:
        # 新版本使用Chrome for Testing
        base_url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_"
        
        # 获取对应版本的ChromeDriver版本号
        try:
            version_url = f"{base_url}{major_version}"
            with urllib.request.urlopen(version_url) as response:
                driver_version = response.read().decode('utf-8').strip()
            print(f"找到ChromeDriver版本: {driver_version}")
        except:
            print("无法获取ChromeDriver版本信息")
            return None
        
        # 下载URL
        if system == "Windows":
            if platform.machine().endswith('64'):
                download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/win64/chromedriver-win64.zip"
                filename = "chromedriver-win64.zip"
            else:
                download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/win32/chromedriver-win32.zip"
                filename = "chromedriver-win32.zip"
        elif system == "Darwin":
            download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/mac-x64/chromedriver-mac-x64.zip"
            filename = "chromedriver-mac-x64.zip"
        else:  # Linux
            download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/linux64/chromedriver-linux64.zip"
            filename = "chromedriver-linux64.zip"
    else:
        # 旧版本使用原来的下载地址
        print("Chrome版本较旧，使用旧版ChromeDriver下载方式")
        return None
    
    # 下载文件
    print(f"正在下载ChromeDriver...")
    print(f"下载地址: {download_url}")
    
    try:
        # 创建drivers目录
        drivers_dir = Path("drivers")
        drivers_dir.mkdir(exist_ok=True)
        
        # 下载文件
        zip_path = drivers_dir / filename
        urllib.request.urlretrieve(download_url, zip_path)
        print(f"下载完成: {zip_path}")
        
        # 解压文件
        print("正在解压...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(drivers_dir)
        
        # 查找chromedriver可执行文件
        if system == "Windows":
            chromedriver_name = "chromedriver.exe"
        else:
            chromedriver_name = "chromedriver"
        
        # 在解压的目录中查找chromedriver
        for root, dirs, files in os.walk(drivers_dir):
            if chromedriver_name in files:
                chromedriver_path = Path(root) / chromedriver_name
                
                # 如果在子目录中，移动到drivers目录
                final_path = drivers_dir / chromedriver_name
                if chromedriver_path != final_path:
                    shutil.move(str(chromedriver_path), str(final_path))
                
                # 设置执行权限（Linux/Mac）
                if system != "Windows":
                    os.chmod(final_path, 0o755)
                
                # 清理zip文件和临时目录
                zip_path.unlink()
                for item in drivers_dir.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                
                print(f"✅ ChromeDriver安装成功: {final_path.absolute()}")
                return str(final_path.absolute())
        
        print("❌ 未找到chromedriver文件")
        return None
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None


def test_chromedriver(driver_path):
    """测试ChromeDriver是否能正常工作"""
    print("\n测试ChromeDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.google.com")
        print(f"✅ ChromeDriver测试成功")
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver测试失败: {e}")
        return False


def update_config(driver_path):
    """更新配置文件"""
    config_file = "config.json"
    
    try:
        # 读取现有配置
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            # 使用默认配置
            from config_manager import ConfigManager
            cm = ConfigManager()
            config = cm.get_default_config()
        
        # 更新ChromeDriver路径
        config['browser']['chrome_driver_path'] = driver_path
        
        # 保存配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 配置文件已更新")
        return True
        
    except Exception as e:
        print(f"❌ 更新配置失败: {e}")
        return False


def main():
    print("="*60)
    print("ChromeDriver 设置工具")
    print("="*60)
    
    # 检测Chrome版本
    print("\n检测Chrome浏览器版本...")
    chrome_version = get_chrome_version()
    
    if not chrome_version:
        print("❌ 未检测到Chrome浏览器")
        print("\n请先安装Chrome浏览器:")
        print("https://www.google.com/chrome/")
        input("\n按回车键退出...")
        return
    
    print(f"✅ 检测到Chrome版本: {chrome_version}")
    
    # 检查是否已有ChromeDriver
    existing_paths = [
        "drivers/chromedriver.exe",
        "drivers/chromedriver",
        "chromedriver.exe",
        "chromedriver"
    ]
    
    driver_path = None
    for path in existing_paths:
        if os.path.exists(path):
            print(f"\n发现已存在的ChromeDriver: {path}")
            choice = input("是否使用现有的ChromeDriver? (y/n): ").strip().lower()
            if choice == 'y':
                driver_path = os.path.abspath(path)
                if test_chromedriver(driver_path):
                    update_config(driver_path)
                    print("\n✅ 设置完成！")
                    input("\n按回车键退出...")
                    return
                else:
                    print("现有ChromeDriver不可用，将下载新版本")
    
    # 下载ChromeDriver
    print("\n开始下载ChromeDriver...")
    driver_path = download_chromedriver(chrome_version)
    
    if driver_path:
        # 测试ChromeDriver
        if test_chromedriver(driver_path):
            # 更新配置
            update_config(driver_path)
            print("\n✅ ChromeDriver设置成功！")
            print(f"路径: {driver_path}")
            print("\n现在可以运行主程序了:")
            print("python main.py")
        else:
            print("\n⚠️ ChromeDriver已下载但测试失败")
            print("可能需要手动配置")
    else:
        print("\n❌ ChromeDriver设置失败")
        print("\n您可以:")
        print("1. 手动下载ChromeDriver: https://chromedriver.chromium.org/")
        print("2. 使用pip安装: pip install webdriver-manager")
    
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
