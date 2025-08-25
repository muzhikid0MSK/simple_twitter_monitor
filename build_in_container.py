"""
容器内构建脚本
在Docker容器内运行，用于跨平台构建
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_in_container(language: str, target_platform: str):
    """在容器内构建指定版本"""
    print(f"🔨 在容器内构建 {target_platform} 平台的 {language} 版本...")
    
    # 设置环境变量
    os.environ["LANGUAGE"] = language
    os.environ["PYTHONPATH"] = str(Path.cwd())
    
    # 创建构建目录
    build_dir = Path("build") / target_platform / language
    dist_dir = Path("dist") / target_platform / language
    
    build_dir.mkdir(parents=True, exist_ok=True)
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--clean",
        "--onefile",
        "--name", f"TwitterMonitor_{language}",
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "--specpath", str(build_dir),
        "main.py"
    ]
    
    # 根据目标平台调整参数
    if target_platform == "windows":
        cmd.append("--windowed")
        # 添加图标（如果存在）
        if Path("assets/icon.ico").exists():
            cmd.extend(["--icon", "assets/icon.ico"])
    else:
        cmd.append("--windowed")
        # 添加图标（如果存在）
        if Path("assets/icon.png").exists():
            cmd.extend(["--icon", "assets/icon.png"])
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行构建
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 构建成功")
            
            # 复制必要文件
            copy_required_files(dist_dir, language, target_platform)
            
            # 创建启动脚本
            create_start_script(dist_dir, language, target_platform)
            
            return True
        else:
            print(f"❌ 构建失败: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程出错: {e}")
        return False
    except Exception as e:
        print(f"❌ 构建异常: {e}")
        return False


def copy_required_files(dist_dir: Path, language: str, target_platform: str):
    """复制必要的文件"""
    print(f"📁 复制必要文件到 {dist_dir}...")
    
    # 复制配置文件
    if Path("config.json").exists():
        shutil.copy2("config.json", dist_dir)
        print("✅ 复制配置文件")
    
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


def create_start_script(dist_dir: Path, language: str, target_platform: str):
    """创建启动脚本"""
    if target_platform == "windows":
        # Windows批处理文件
        script_content = get_windows_start_script(language)
        script_path = dist_dir / "start.bat"
        with open(script_path, "w", encoding="gbk") as f:
            f.write(script_content)
    else:
        # Linux shell脚本
        script_content = get_linux_start_script(language)
        script_path = dist_dir / "start.sh"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        # 设置执行权限
        os.chmod(script_path, 0o755)
    
    print(f"✅ 创建启动脚本: {script_path.name}")


def get_windows_start_script(language: str) -> str:
    """获取Windows启动脚本内容"""
    if language == "zh_CN":
        return """@echo off
chcp 65001 >nul
echo ====================================
echo    Twitter监控器 v2.0.0 - 中文版
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
start "" "TwitterMonitor_zh_CN.exe"

echo [信息] 程序已启动
echo 如果程序没有显示，请检查任务管理器
pause
"""
    else:
        return """@echo off
echo ====================================
echo    Twitter Monitor v2.0.0 - English
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
start "" "TwitterMonitor_en_US.exe"

echo [Info] Program started
echo If program is not visible, check Task Manager
pause
"""


def get_linux_start_script(language: str) -> str:
    """获取Linux启动脚本内容"""
    if language == "zh_CN":
        return """#!/bin/bash

echo "===================================="
echo "    Twitter监控器 v2.0.0 - 中文版"
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
./TwitterMonitor_zh_CN &

echo "[信息] 程序已启动"
echo "进程ID: $!"
echo ""
echo "停止程序: kill $!"
"""
    else:
        return """#!/bin/bash

echo "===================================="
echo "    Twitter Monitor v2.0.0 - English"
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
./TwitterMonitor_en_US &

echo "[Info] Program started"
echo "Process ID: $!"
echo ""
echo "Stop program: kill $!"
"""


def main():
    """主函数"""
    if len(sys.argv) != 3:
        print("用法: python3 build_in_container.py <language> <target_platform>")
        print("示例: python3 build_in_container.py zh_CN windows")
        sys.exit(1)
    
    language = sys.argv[1]
    target_platform = sys.argv[2]
    
    print("="*60)
    print("Twitter监控器 - 容器内构建工具")
    print("="*60)
    print(f"语言: {language}")
    print(f"目标平台: {target_platform}")
    print("="*60)
    
    # 检查参数
    if language not in ["zh_CN", "en_US"]:
        print(f"❌ 不支持的语言: {language}")
        sys.exit(1)
    
    if target_platform not in ["windows", "linux"]:
        print(f"❌ 不支持的目标平台: {target_platform}")
        sys.exit(1)
    
    # 开始构建
    if build_in_container(language, target_platform):
        print("\n🎉 构建完成！")
        print(f"输出目录: dist/{target_platform}/{language}")
    else:
        print("\n❌ 构建失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
