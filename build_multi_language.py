"""
多语言构建脚本
生成中文和英文的Windows和Linux安装程序
"""
import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path


class MultiLanguageBuilder:
    """多语言构建器"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.arch = platform.machine().lower()
        self.project_name = "TwitterMonitor"
        self.version = "2.0.0"
        
        # 支持的语言
        self.languages = ["zh_CN", "en_US"]
        
        # 构建目录
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        
    def clean_build_dirs(self):
        """清理构建目录"""
        print("🧹 清理构建目录...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            
        # 重新创建目录
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        print("✅ 构建目录清理完成")
    
    def build_all_versions(self):
        """构建所有版本"""
        print("🚀 开始构建所有版本...")
        print(f"平台: {self.platform}")
        print(f"架构: {self.arch}")
        print(f"项目: {self.project_name} v{self.version}")
        print("="*60)
        
        # 清理构建目录
        self.clean_build_dirs()
        
        success_count = 0
        total_count = len(self.languages)
        
        for language in self.languages:
            print(f"\n🌍 正在构建 {language} 版本...")
            
            if self.build_version(language):
                success_count += 1
                print(f"✅ {language} 版本构建成功")
            else:
                print(f"❌ {language} 版本构建失败")
            
            print("-" * 40)
        
        # 构建结果汇总
        print("\n" + "="*60)
        print("🏁 构建完成！")
        print(f"成功: {success_count}/{total_count}")
        
        if success_count == total_count:
            print("🎉 所有版本构建成功！")
            self.show_output_info()
        else:
            print("⚠️ 部分版本构建失败，请检查错误信息")
    
    def build_version(self, language: str) -> bool:
        """构建指定语言版本"""
        try:
            # 设置Python路径
            os.environ["PYTHONPATH"] = str(Path.cwd())
            
            # 创建语言特定的构建目录
            lang_build_dir = self.build_dir / language
            lang_dist_dir = self.dist_dir / language
            
            lang_build_dir.mkdir(exist_ok=True)
            lang_dist_dir.mkdir(exist_ok=True)
            
            # 构建命令
            cmd = [
                "pyinstaller",
                "--clean",
                "--onefile",
                "--windowed",
                "--name", f"{self.project_name}_{language}",
                "--distpath", str(lang_dist_dir),
                "--workpath", str(lang_build_dir),
                "--specpath", str(lang_build_dir),
                "main.py"
            ]
            
            # 添加图标（如果存在）
            if self.platform == "windows" and Path("assets/icon.ico").exists():
                cmd.extend(["--icon", "assets/icon.ico"])
            elif Path("assets/icon.png").exists():
                cmd.extend(["--icon", "assets/icon.png"])
            
            print(f"执行命令: {' '.join(cmd)}")
            
            # 执行构建
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 复制必要文件
                self.copy_required_files(lang_dist_dir, language)
                return True
            else:
                print(f"构建失败: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"构建过程出错: {e}")
            return False
        except Exception as e:
            print(f"构建异常: {e}")
            return False
    
    def copy_required_files(self, dist_dir: Path, language: str):
        """复制必要的文件到发布目录"""
        print(f"📁 复制必要文件到 {dist_dir}...")
        
        # 复制配置文件并设置语言
        if Path("config.json").exists():
            # 读取原配置文件
            with open("config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 设置目标语言
            config['system']['language'] = language
            
            # 保存到目标目录
            config_path = dist_dir / "config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"✅ 复制配置文件并设置语言为 {language}")
        else:
            # 如果没有配置文件，创建一个默认的
            config = {
                "twitter": {
                    "username": "",
                    "auth_token": "",
                    "check_interval": 60
                },
                "email": {
                    "provider": "163",
                    "smtp_server": "smtp.163.com",
                    "smtp_port": 465,
                    "sender_email": "",
                    "sender_password": "",
                    "receiver_email": "",
                    "use_ssl": True,
                    "use_tls": False
                },
                "browser": {
                    "headless": False,
                    "chrome_driver_path": ""
                },
                "system": {
                    "language": language,
                    "auto_start": False,
                    "minimize_to_tray": True
                }
            }
            
            config_path = dist_dir / "config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"✅ 创建默认配置文件，语言设置为 {language}")
        
        # 复制README
        if Path("README.md").exists():
            shutil.copy2("README.md", dist_dir)
            print("✅ 复制README")
        
        # 复制驱动目录
        if Path("drivers").exists():
            driver_dest = dist_dir / "drivers"
            if driver_dest.exists():
                shutil.rmtree(driver_dest)
            shutil.copytree("drivers", driver_dest)
            print("✅ 复制驱动文件")
        
        # 复制资源目录
        if Path("assets").exists():
            assets_dest = dist_dir / "assets"
            if assets_dest.exists():
                shutil.rmtree(assets_dest)
            shutil.copytree("assets", assets_dest)
            print("✅ 复制资源文件")
        
        # 创建启动脚本
        self.create_start_script(dist_dir, language)
        
        # 创建安装说明
        self.create_install_guide(dist_dir, language)
    
    def create_start_script(self, dist_dir: Path, language: str):
        """创建启动脚本"""
        if self.platform == "windows":
            # Windows批处理文件
            script_content = self.get_windows_start_script(language)
            script_path = dist_dir / "start.bat"
            with open(script_path, "w", encoding="gbk") as f:
                f.write(script_content)
        else:
            # Linux shell脚本
            script_content = self.get_linux_start_script(language)
            script_path = dist_dir / "start.sh"
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            # 设置执行权限
            os.chmod(script_path, 0o755)
        
        print(f"✅ 创建启动脚本: {script_path.name}")
    
    def get_windows_start_script(self, language: str) -> str:
        """获取Windows启动脚本内容"""
        if language == "zh_CN":
            return f"""@echo off
chcp 65001 >nul
echo ====================================
echo    Twitter监控器 v{self.version} - 中文版
echo ====================================
echo.

REM 检查配置文件
if not exist "config.json" (
    echo [错误] 未找到配置文件 config.json
    echo 请先配置程序参数
    pause
    exit /b 1
)

echo [信息] 正在启动Twitter监控器...
echo.

REM 启动程序
start "" "{self.project_name}_{language}.exe"

echo [信息] 程序已启动
echo 如果程序没有显示，请检查任务管理器
pause
"""
        else:
            return f"""@echo off
echo ====================================
echo    Twitter Monitor v{self.version} - English
echo ====================================
echo.

REM Check configuration file
if not exist "config.json" (
    echo [Error] Configuration file config.json not found
    echo Please configure program parameters first
    pause
    exit /b 1
)

echo [Info] Starting Twitter Monitor...
echo.

REM Start program
start "" "{self.project_name}_{language}.exe"

echo [Info] Program started
echo If program is not visible, check Task Manager
pause
"""
    
    def get_linux_start_script(self, language: str) -> str:
        """获取Linux启动脚本内容"""
        if language == "zh_CN":
            return f"""#!/bin/bash

echo "===================================="
echo "    Twitter监控器 v{self.version} - 中文版"
echo "===================================="
echo ""

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "[错误] 未找到配置文件 config.json"
    echo "请先配置程序参数"
    exit 1
fi

echo "[信息] 正在启动Twitter监控器..."
echo ""

# 启动程序
./{self.project_name}_{language} &

echo "[信息] 程序已启动"
echo "进程ID: $!"
echo ""
echo "停止程序: kill $!"
"""
        else:
            return f"""#!/bin/bash

echo "===================================="
echo "    Twitter Monitor v{self.version} - English"
echo "===================================="
echo ""

# Check configuration file
if [ ! -f "config.json" ]; then
    echo "[Error] Configuration file config.json not found"
    echo "Please configure program parameters first"
    exit 1
fi

echo "[Info] Starting Twitter Monitor..."
echo ""

# Start program
./{self.project_name}_{language} &

echo "[Info] Program started"
echo "Process ID: $!"
echo ""
echo "Stop program: kill $!"
"""
    
    def create_install_guide(self, dist_dir: Path, language: str):
        """创建安装说明"""
        if language == "zh_CN":
            content = f"""# Twitter监控器 v{self.version} - 中文版

## 安装说明

### 系统要求
- Windows 10/11 或 Linux (Ubuntu 18.04+)
- 至少 4GB 内存
- 至少 500MB 可用磁盘空间

### 安装步骤
1. 解压所有文件到目标目录
2. 双击运行 `start.bat` (Windows) 或 `./start.sh` (Linux)
3. 首次运行会自动创建配置文件
4. 在程序界面中配置Twitter和邮箱设置
5. 点击"开始监控"开始工作

### 注意事项
- 首次运行需要配置Twitter Auth Token
- 确保邮箱SMTP服务已开启
- 建议使用Chrome浏览器

### 技术支持
如有问题，请查看README.md文件或联系技术支持。
"""
        else:
            content = f"""# Twitter Monitor v{self.version} - English

## Installation Guide

### System Requirements
- Windows 10/11 or Linux (Ubuntu 18.04+)
- At least 4GB RAM
- At least 500MB free disk space

### Installation Steps
1. Extract all files to target directory
2. Double-click `start.bat` (Windows) or `./start.sh` (Linux)
3. Configuration file will be created automatically on first run
4. Configure Twitter and email settings in program interface
5. Click "Start Monitoring" to begin

### Notes
- First run requires Twitter Auth Token configuration
- Ensure email SMTP service is enabled
- Chrome browser is recommended

### Technical Support
For issues, please check README.md file or contact technical support.
"""
        
        guide_path = dist_dir / f"INSTALL_{language.upper()}.md"
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 创建安装说明: {guide_path.name}")
    
    def show_output_info(self):
        """显示输出信息"""
        print("\n📦 构建输出:")
        print(f"构建目录: {self.build_dir.absolute()}")
        print(f"发布目录: {self.dist_dir.absolute()}")
        
        for language in self.languages:
            lang_dir = self.dist_dir / language
            if lang_dir.exists():
                exe_files = list(lang_dir.glob(f"{self.project_name}_{language}*"))
                if exe_files:
                    exe_file = exe_files[0]
                    size_mb = exe_file.stat().st_size / (1024 * 1024)
                    print(f"  {language}: {exe_file.name} ({size_mb:.1f} MB)")
        
        print("\n🎯 下一步:")
        print("1. 检查 dist 目录中的可执行文件")
        print("2. 测试不同语言版本")
        print("3. 打包分发给用户")


def main():
    """主函数"""
    print("="*60)
    print("Twitter监控器 - 多语言构建工具")
    print("="*60)
    
    # 检查PyInstaller
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到PyInstaller，请先安装:")
        print("pip install pyinstaller")
        return
    
    # 创建构建器
    builder = MultiLanguageBuilder()
    
    # 构建所有版本
    builder.build_all_versions()
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
