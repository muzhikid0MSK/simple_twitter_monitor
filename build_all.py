"""
一键构建脚本
生成所有语言和平台的安装程序
"""
import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path


class AllPlatformBuilder:
    """全平台构建器"""
    
    def __init__(self):
        self.current_platform = platform.system().lower()
        self.project_name = "TwitterMonitor"
        self.version = "2.0.0"
        
        # 支持的语言和平台
        self.languages = ["zh_CN", "en_US"]
        self.platforms = ["windows", "linux"]
        
        # 构建目录
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        
    def check_requirements(self):
        """检查构建要求"""
        print("🔍 检查构建要求...")
        
        # 检查Python
        try:
            python_version = subprocess.run([sys.executable, "--version"], 
                                          capture_output=True, text=True, check=True)
            print(f"✅ Python: {python_version.stdout.strip()}")
        except Exception as e:
            print(f"❌ Python检查失败: {e}")
            return False
        
        # 检查PyInstaller
        try:
            pyinstaller_version = subprocess.run(["pyinstaller", "--version"], 
                                               capture_output=True, text=True, check=True)
            print(f"✅ PyInstaller: {pyinstaller_version.stdout.strip()}")
        except Exception as e:
            print(f"❌ PyInstaller未安装，正在安装...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                             check=True)
                print("✅ PyInstaller安装成功")
            except Exception as e2:
                print(f"❌ PyInstaller安装失败: {e2}")
                return False
        
        # 检查Docker（用于跨平台构建）
        try:
            docker_version = subprocess.run(["docker", "--version"], 
                                          capture_output=True, text=True, check=True)
            print(f"✅ Docker: {docker_version.stdout.strip()}")
            self.docker_available = True
        except Exception as e:
            print(f"⚠️ Docker未安装，将无法进行跨平台构建")
            self.docker_available = False
        
        print("✅ 构建要求检查完成")
        return True
    
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
    
    def build_current_platform(self):
        """构建当前平台版本"""
        print(f"\n🔨 构建当前平台 ({self.current_platform}) 版本...")
        
        success_count = 0
        total_count = len(self.languages)
        
        for language in self.languages:
            print(f"\n🌍 正在构建 {language} 版本...")
            
            if self.build_single_version(language, self.current_platform):
                success_count += 1
                print(f"✅ {language} 版本构建成功")
            else:
                print(f"❌ {language} 版本构建失败")
            
            print("-" * 40)
        
        return success_count, total_count
    
    def build_cross_platform(self):
        """构建跨平台版本"""
        if not self.docker_available:
            print("\n⚠️ Docker不可用，跳过跨平台构建")
            return 0, 0
        
        print(f"\n🌐 构建跨平台版本...")
        
        success_count = 0
        total_count = 0
        
        for target_platform in self.platforms:
            if target_platform == self.current_platform:
                continue  # 跳过当前平台
                
            for language in self.languages:
                total_count += 1
                print(f"\n🌍 正在构建 {target_platform} 平台的 {language} 版本...")
                
                if self.build_with_docker(target_platform, language):
                    success_count += 1
                    print(f"✅ {target_platform} {language} 版本构建成功")
                else:
                    print(f"❌ {target_platform} {language} 版本构建失败")
                
                print("-" * 40)
        
        return success_count, total_count
    
    def build_single_version(self, language: str, target_platform: str):
        """构建单个版本"""
        try:
            # 设置Python路径
            os.environ["PYTHONPATH"] = str(Path.cwd())
            
            # 创建构建目录
            lang_build_dir = self.build_dir / target_platform / language
            lang_dist_dir = self.dist_dir / target_platform / language
            
            lang_build_dir.mkdir(parents=True, exist_ok=True)
            lang_dist_dir.mkdir(parents=True, exist_ok=True)
            
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
            
            # 添加图标
            if target_platform == "windows" and Path("assets/icon.ico").exists():
                cmd.extend(["--icon", "assets/icon.ico"])
            elif Path("assets/icon.png").exists():
                cmd.extend(["--icon", "assets/icon.png"])
            
            print(f"执行命令: {' '.join(cmd)}")
            
            # 执行构建
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 复制必要文件
                self.copy_required_files(lang_dist_dir, language, target_platform)
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
    
    def build_with_docker(self, target_platform: str, language: str):
        """使用Docker构建跨平台版本"""
        print(f"🐳 使用Docker构建 {target_platform} 平台的 {language} 版本...")
        
        # 创建Dockerfile
        dockerfile_content = self.create_dockerfile(target_platform)
        dockerfile_path = Path("Dockerfile.build")
        
        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
        
        try:
            # 构建Docker镜像
            image_name = f"twitter-monitor-builder-{target_platform}"
            build_cmd = [
                "docker", "build", 
                "-f", "Dockerfile.build",
                "-t", image_name,
                "."
            ]
            
            print(f"执行命令: {' '.join(build_cmd)}")
            subprocess.run(build_cmd, check=True)
            print("✅ Docker镜像构建成功")
            
            # 运行Docker容器进行构建
            container_name = f"builder-{target_platform}-{language}"
            run_cmd = [
                "docker", "run", "--rm",
                "--name", container_name,
                "-v", f"{Path.cwd().absolute()}:/workspace",
                "-w", "/workspace",
                "-e", f"LANGUAGE={language}",
                "-e", f"TARGET_PLATFORM={target_platform}",
                image_name,
                "python3", "build_in_container.py", language, target_platform
            ]
            
            print(f"执行命令: {' '.join(run_cmd)}")
            subprocess.run(run_cmd, check=True)
            
            # 清理Docker镜像
            subprocess.run(["docker", "rmi", image_name], check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker构建失败: {e}")
            return False
        finally:
            # 清理Dockerfile
            if dockerfile_path.exists():
                dockerfile_path.unlink()
    
    def create_dockerfile(self, target_platform: str):
        """创建构建用的Dockerfile"""
        return """# 构建环境
FROM ubuntu:20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    python3-dev \\
    build-essential \\
    wget \\
    curl \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# 安装PyInstaller
RUN pip3 install pyinstaller

# 设置工作目录
WORKDIR /workspace

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip3 install -r requirements.txt

# 设置默认命令
CMD ["python3", "build_in_container.py"]
"""
    
    def copy_required_files(self, dist_dir: Path, language: str, target_platform: str):
        """复制必要的文件"""
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
        self.create_start_script(dist_dir, language, target_platform)
        
        # 创建安装说明
        self.create_install_guide(dist_dir, language, target_platform)
    
    def create_start_script(self, dist_dir: Path, language: str, target_platform: str):
        """创建启动脚本"""
        if target_platform == "windows":
            script_content = self.get_windows_start_script(language)
            script_path = dist_dir / "start.bat"
            with open(script_path, "w", encoding="gbk") as f:
                f.write(script_content)
        else:
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
    
    def create_install_guide(self, dist_dir: Path, language: str, target_platform: str):
        """创建安装说明"""
        if language == "zh_CN":
            content = f"""# Twitter监控器 v{self.version} - 中文版

## 安装说明

### 系统要求
- {target_platform.title()} 系统
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
- {target_platform.title()} system
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
    
    def build_all(self):
        """构建所有版本"""
        print("🚀 开始构建所有版本...")
        print(f"当前平台: {self.current_platform}")
        print(f"支持语言: {', '.join(self.languages)}")
        print(f"目标平台: {', '.join(self.platforms)}")
        print("="*60)
        
        # 检查构建要求
        if not self.check_requirements():
            print("❌ 构建要求检查失败")
            return False
        
        # 清理构建目录
        self.clean_build_dirs()
        
        # 构建当前平台版本
        current_success, current_total = self.build_current_platform()
        
        # 构建跨平台版本
        cross_success, cross_total = self.build_cross_platform()
        
        # 汇总结果
        total_success = current_success + cross_success
        total_count = current_total + cross_total
        
        print("\n" + "="*60)
        print("🏁 构建完成！")
        print(f"当前平台成功: {current_success}/{current_total}")
        print(f"跨平台成功: {cross_success}/{cross_total}")
        print(f"总计成功: {total_success}/{total_count}")
        
        if total_success == total_count:
            print("🎉 所有版本构建成功！")
            self.show_output_info()
            return True
        else:
            print("⚠️ 部分版本构建失败，请检查错误信息")
            return False
    
    def show_output_info(self):
        """显示输出信息"""
        print("\n📦 构建输出:")
        print(f"构建目录: {self.build_dir.absolute()}")
        print(f"发布目录: {self.dist_dir.absolute()}")
        
        for platform_name in self.platforms:
            platform_dir = self.dist_dir / platform_name
            if platform_dir.exists():
                print(f"\n{platform_name.upper()} 平台:")
                for language in self.languages:
                    lang_dir = platform_dir / language
                    if lang_dir.exists():
                        exe_files = list(lang_dir.glob(f"{self.project_name}_{language}*"))
                        if exe_files:
                            exe_file = exe_files[0]
                            size_mb = exe_file.stat().st_size / (1024 * 1024)
                            print(f"  {language}: {exe_file.name} ({size_mb:.1f} MB)")
        
        print("\n🎯 下一步:")
        print("1. 检查 dist 目录中的可执行文件")
        print("2. 测试不同平台和语言版本")
        print("3. 打包分发给用户")


def main():
    """主函数"""
    print("="*60)
    print("Twitter监控器 - 全平台构建工具")
    print("="*60)
    
    # 创建构建器
    builder = AllPlatformBuilder()
    
    # 构建所有版本
    if builder.build_all():
        print("\n🎉 构建成功完成！")
    else:
        print("\n❌ 构建失败！")
        sys.exit(1)
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
