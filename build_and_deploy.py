"""
构建和部署脚本
支持Windows、Linux和Docker部署
"""
import os
import sys
import platform
import subprocess
import argparse
from pathlib import Path


class BuildDeploy:
    """构建和部署类"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.arch = platform.machine().lower()
        self.project_name = "TwitterMonitor"
        
    def build_executable(self, language: str = "zh_CN"):
        """构建可执行文件"""
        print(f"🔨 正在构建 {self.project_name} 可执行文件...")
        print(f"平台: {self.platform}")
        print(f"架构: {self.arch}")
        print(f"语言: {language}")
        
        # 设置环境变量
        os.environ["LANGUAGE"] = language
        
        if self.platform == "windows":
            return self._build_windows()
        else:
            return self._build_unix()
    
    def _build_windows(self):
        """Windows平台构建"""
        try:
            # 检查PyInstaller
            subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
            
            # 构建命令
            cmd = [
                "pyinstaller",
                "--clean",
                "--onefile",
                "--windowed",
                "--name", self.project_name,
                "main.py"
            ]
            
            # 如果有图标文件，添加图标
            if Path("assets/icon.ico").exists():
                cmd.extend(["--icon", "assets/icon.ico"])
            
            print(f"执行命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True)
            
            if result.returncode == 0:
                print("✅ Windows可执行文件构建成功！")
                print(f"文件位置: dist/{self.project_name}.exe")
                return True
            else:
                print("❌ Windows可执行文件构建失败")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 构建过程出错: {e}")
            return False
        except FileNotFoundError:
            print("❌ 未找到PyInstaller，请先安装: pip install pyinstaller")
            return False
    
    def _build_unix(self):
        """Unix/Linux平台构建"""
        try:
            # 检查PyInstaller
            subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
            
            # 构建命令
            cmd = [
                "pyinstaller",
                "--clean",
                "--onefile",
                "--windowed",
                "--name", self.project_name,
                "main.py"
            ]
            
            # 如果有图标文件，添加图标
            if Path("assets/icon.png").exists():
                cmd.extend(["--icon", "assets/icon.png"])
            
            print(f"执行命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True)
            
            if result.returncode == 0:
                print("✅ Unix/Linux可执行文件构建成功！")
                print(f"文件位置: dist/{self.project_name}")
                return True
            else:
                print("❌ Unix/Linux可执行文件构建失败")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 构建过程出错: {e}")
            return False
        except FileNotFoundError:
            print("❌ 未找到PyInstaller，请先安装: pip install pyinstaller")
            return False
    
    def build_docker(self, language: str = "zh_CN"):
        """构建Docker镜像"""
        print(f"🐳 正在构建Docker镜像...")
        print(f"语言: {language}")
        
        try:
            # 设置环境变量
            os.environ["LANGUAGE"] = language
            
            # 构建Docker镜像
            cmd = ["docker", "build", "-t", f"{self.project_name.lower()}:latest", "."]
            print(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, check=True)
            
            if result.returncode == 0:
                print("✅ Docker镜像构建成功！")
                print(f"镜像名称: {self.project_name.lower()}:latest")
                return True
            else:
                print("❌ Docker镜像构建失败")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker构建过程出错: {e}")
            return False
        except FileNotFoundError:
            print("❌ 未找到Docker，请先安装Docker")
            return False
    
    def deploy_docker(self):
        """部署Docker容器"""
        print("🚀 正在部署Docker容器...")
        
        try:
            # 检查docker-compose
            subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
            
            # 启动服务
            cmd = ["docker-compose", "up", "-d"]
            print(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, check=True)
            
            if result.returncode == 0:
                print("✅ Docker容器部署成功！")
                print("服务状态:")
                subprocess.run(["docker-compose", "ps"])
                return True
            else:
                print("❌ Docker容器部署失败")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker部署过程出错: {e}")
            return False
        except FileNotFoundError:
            print("❌ 未找到docker-compose，请先安装Docker Compose")
            return False
    
    def create_package(self, language: str = "zh_CN"):
        """创建发布包"""
        print(f"📦 正在创建发布包...")
        print(f"语言: {language}")
        
        # 创建发布目录
        dist_dir = Path("dist")
        package_dir = dist_dir / f"{self.project_name}_{language}"
        package_dir.mkdir(exist_ok=True)
        
        try:
            # 复制可执行文件
            if self.platform == "windows":
                exe_file = dist_dir / f"{self.project_name}.exe"
                if exe_file.exists():
                    import shutil
                    shutil.copy2(exe_file, package_dir)
                    print(f"✅ 复制可执行文件: {exe_file.name}")
                else:
                    print("❌ 未找到可执行文件，请先构建")
                    return False
            else:
                exe_file = dist_dir / self.project_name
                if exe_file.exists():
                    import shutil
                    shutil.copy2(exe_file, package_dir)
                    print(f"✅ 复制可执行文件: {exe_file.name}")
                else:
                    print("❌ 未找到可执行文件，请先构建")
                    return False
            
            # 复制必要文件
            files_to_copy = [
                "config.json",
                "README.md",
                "LICENSE"
            ]
            
            for file_name in files_to_copy:
                if Path(file_name).exists():
                    import shutil
                    shutil.copy2(file_name, package_dir)
                    print(f"✅ 复制文件: {file_name}")
            
            # 复制目录
            dirs_to_copy = [
                "drivers",
                "assets"
            ]
            
            for dir_name in dirs_to_copy:
                if Path(dir_name).exists():
                    import shutil
                    shutil.copytree(dir_name, package_dir / dir_name, dirs_exist_ok=True)
                    print(f"✅ 复制目录: {dir_name}")
            
            # 创建启动脚本
            if self.platform == "windows":
                self._create_windows_start_script(package_dir)
            else:
                self._create_unix_start_script(package_dir)
            
            print(f"✅ 发布包创建成功！")
            print(f"位置: {package_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 创建发布包失败: {e}")
            return False
    
    def _create_windows_start_script(self, package_dir: Path):
        """创建Windows启动脚本"""
        script_content = f"""@echo off
echo ====================================
echo    Twitter监控器 v1.0
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
start "" "{self.project_name}.exe"

echo [信息] 程序已启动
echo 如果程序没有显示，请检查任务管理器
pause
"""
        
        script_path = package_dir / "start.bat"
        with open(script_path, "w", encoding="gbk") as f:
            f.write(script_content)
        print("✅ 创建启动脚本: start.bat")
    
    def _create_unix_start_script(self, package_dir: Path):
        """创建Unix/Linux启动脚本"""
        script_content = f"""#!/bin/bash

echo "===================================="
echo "    Twitter监控器 v1.0"
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
./{self.project_name} &

echo "[信息] 程序已启动"
echo "进程ID: $!"
echo ""
echo "停止程序: kill $!"
"""
        
        script_path = package_dir / "start.sh"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # 设置执行权限
        os.chmod(script_path, 0o755)
        print("✅ 创建启动脚本: start.sh")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Twitter监控器构建和部署工具")
    parser.add_argument("--action", choices=["build", "docker", "deploy", "package"], 
                       default="build", help="执行的操作")
    parser.add_argument("--language", choices=["zh_CN", "en_US"], 
                       default="zh_CN", help="界面语言")
    parser.add_argument("--platform", choices=["windows", "linux", "docker"], 
                       help="目标平台")
    
    args = parser.parse_args()
    
    print("="*60)
    print("Twitter监控器 - 构建和部署工具")
    print("="*60)
    
    builder = BuildDeploy()
    
    if args.action == "build":
        # 构建可执行文件
        if builder.build_executable(args.language):
            print("\n🎉 构建完成！")
        else:
            print("\n❌ 构建失败！")
            sys.exit(1)
    
    elif args.action == "docker":
        # 构建Docker镜像
        if builder.build_docker(args.language):
            print("\n🎉 Docker镜像构建完成！")
        else:
            print("\n❌ Docker镜像构建失败！")
            sys.exit(1)
    
    elif args.action == "deploy":
        # 部署Docker容器
        if builder.deploy_docker():
            print("\n🎉 Docker容器部署完成！")
        else:
            print("\n❌ Docker容器部署失败！")
            sys.exit(1)
    
    elif args.action == "package":
        # 创建发布包
        if builder.create_package(args.language):
            print("\n🎉 发布包创建完成！")
        else:
            print("\n❌ 发布包创建失败！")
            sys.exit(1)
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
