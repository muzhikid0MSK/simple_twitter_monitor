"""
打包配置文件
支持Windows和Linux平台打包
"""
import os
import sys
import platform
from pathlib import Path


class BuildConfig:
    """打包配置类"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.arch = platform.machine().lower()
        self.project_name = "TwitterMonitor"
        self.version = "1.0.0"
        
    def get_pyinstaller_config(self) -> dict:
        """获取PyInstaller配置"""
        base_config = {
            "name": self.project_name,
            "version": self.version,
            "description": "Twitter账户监控器 - 监听新推文并发送邮件通知",
            "author": "Your Name",
            "main_file": "main.py",
            "icon": "assets/icon.ico" if self.platform == "windows" else "assets/icon.png",
            "hidden_imports": [
                "selenium",
                "webdriver_manager",
                "tkinter",
                "tkinter.ttk",
                "tkinter.messagebox",
                "tkinter.scrolledtext"
            ],
            "excludes": [
                "matplotlib",
                "numpy",
                "pandas",
                "scipy",
                "PIL",
                "cv2"
            ],
            "data_files": [
                ("drivers", "drivers"),
                ("assets", "assets"),
                ("i18n", "i18n")
            ]
        }
        
        if self.platform == "windows":
            base_config.update({
                "console": False,  # 无控制台窗口
                "windowed": True,
                "onefile": True,  # 打包为单个文件
                "onedir": False,
                "distpath": "dist/windows",
                "workpath": "build/windows",
                "specpath": "build/windows"
            })
        elif self.platform == "linux":
            base_config.update({
                "console": False,
                "windowed": True,
                "onefile": True,
                "onedir": False,
                "distpath": "dist/linux",
                "workpath": "build/linux",
                "specpath": "build/linux"
            })
        else:
            # macOS
            base_config.update({
                "console": False,
                "windowed": True,
                "onefile": True,
                "onedir": False,
                "distpath": "dist/macos",
                "workpath": "build/macos",
                "specpath": "build/macos"
            })
        
        return base_config
    
    def get_requirements(self) -> list:
        """获取依赖包列表"""
        return [
            "selenium>=4.15.0",
            "webdriver-manager>=4.0.1",
            "pyinstaller>=5.0.0",
            "requests>=2.25.0"
        ]
    
    def create_build_script(self):
        """创建构建脚本"""
        if self.platform == "windows":
            self._create_windows_build_script()
        else:
            self._create_unix_build_script()
    
    def _create_windows_build_script(self):
        """创建Windows构建脚本"""
        script_content = f"""@echo off
echo ====================================
echo    Twitter监控器 构建脚本
echo ====================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python环境
    pause
    exit /b 1
)

echo [信息] 检测到Python环境
echo.

REM 安装依赖
echo [信息] 正在安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 依赖包安装失败
    pause
    exit /b 1
)

echo [信息] 依赖包安装完成
echo.

REM 创建构建目录
if not exist "build" mkdir build
if not exist "dist" mkdir dist

REM 构建可执行文件
echo [信息] 正在构建可执行文件...
pyinstaller --clean --onefile --windowed --icon=assets/icon.ico --name={self.project_name} main.py

if %errorlevel% neq 0 (
    echo [错误] 构建失败
    pause
    exit /b 1
)

echo.
echo [成功] 构建完成！
echo 可执行文件位置: dist\\{self.project_name}.exe
echo.

REM 复制必要文件
echo [信息] 正在复制必要文件...
if exist "drivers" xcopy /E /I drivers dist\\drivers
if exist "assets" xcopy /E /I assets dist\\assets
if exist "config.json" copy config.json dist\\

echo.
echo [完成] 所有文件已准备就绪！
echo 可执行文件: dist\\{self.project_name}.exe
echo 配置文件: dist\\config.json
echo 驱动文件: dist\\drivers\\
echo.

pause
"""
        
        with open("build_windows.bat", "w", encoding="gbk") as f:
            f.write(script_content)
        
        print("✅ Windows构建脚本已创建: build_windows.bat")
    
    def _create_unix_build_script(self):
        """创建Unix/Linux构建脚本"""
        script_content = f"""#!/bin/bash

echo "===================================="
echo "    Twitter监控器 构建脚本"
echo "===================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3环境"
    exit 1
fi

echo "[信息] 检测到Python环境: $(python3 --version)"
echo ""

# 安装依赖
echo "[信息] 正在安装依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 依赖包安装失败"
    exit 1
fi

echo "[信息] 依赖包安装完成"
echo ""

# 创建构建目录
mkdir -p build dist

# 构建可执行文件
echo "[信息] 正在构建可执行文件..."
pyinstaller --clean --onefile --windowed --icon=assets/icon.png --name={self.project_name} main.py

if [ $? -ne 0 ]; then
    echo "[错误] 构建失败"
    exit 1
fi

echo ""
echo "[成功] 构建完成！"
echo "可执行文件位置: dist/{self.project_name}"
echo ""

# 复制必要文件
echo "[信息] 正在复制必要文件..."
if [ -d "drivers" ]; then
    cp -r drivers dist/
fi

if [ -d "assets" ]; then
    cp -r assets dist/
fi

if [ -f "config.json" ]; then
    cp config.json dist/
fi

# 设置执行权限
chmod +x dist/{self.project_name}

echo ""
echo "[完成] 所有文件已准备就绪！"
echo "可执行文件: dist/{self.project_name}"
echo "配置文件: dist/config.json"
echo "驱动文件: dist/drivers/"
echo ""
"""
        
        with open("build_unix.sh", "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # 设置执行权限
        os.chmod("build_unix.sh", 0o755)
        print("✅ Unix/Linux构建脚本已创建: build_unix.sh")
    
    def create_spec_file(self):
        """创建PyInstaller spec文件"""
        config = self.get_pyinstaller_config()
        
        spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{config["main_file"]}'],
    pathex=[],
    binaries=[],
    datas={config["data_files"]},
    hiddenimports={config["hidden_imports"]},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes={config["excludes"]},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{config["name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console={config.get("console", False)},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{config["icon"]}' if os.path.exists('{config["icon"]}') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{config["name"]}',
)
"""
        
        with open(f"{self.project_name}.spec", "w", encoding="utf-8") as f:
            f.write(spec_content)
        
        print(f"✅ PyInstaller spec文件已创建: {self.project_name}.spec")


def main():
    """主函数"""
    print("="*60)
    print("Twitter监控器 - 构建配置工具")
    print("="*60)
    
    config = BuildConfig()
    
    print(f"检测到平台: {config.platform}")
    print(f"架构: {config.arch}")
    print(f"项目名称: {config.project_name}")
    print(f"版本: {config.version}")
    print()
    
    # 创建构建脚本
    print("正在创建构建脚本...")
    config.create_build_script()
    
    # 创建spec文件
    print("正在创建PyInstaller spec文件...")
    config.create_spec_file()
    
    print("\n" + "="*60)
    print("构建配置完成！")
    print()
    
    if config.platform == "windows":
        print("使用方法:")
        print("1. 运行: build_windows.bat")
        print("2. 等待构建完成")
        print("3. 可执行文件将在 dist 目录中")
    else:
        print("使用方法:")
        print("1. 运行: ./build_unix.sh")
        print("2. 等待构建完成")
        print("3. 可执行文件将在 dist 目录中")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
