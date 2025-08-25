@echo off
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
pyinstaller --clean --onefile --windowed --icon=assets/icon.ico --name=TwitterMonitor main.py

if %errorlevel% neq 0 (
    echo [错误] 构建失败
    pause
    exit /b 1
)

echo.
echo [成功] 构建完成！
echo 可执行文件位置: dist\TwitterMonitor.exe
echo.

REM 复制必要文件
echo [信息] 正在复制必要文件...
if exist "drivers" xcopy /E /I drivers dist\drivers
if exist "assets" xcopy /E /I assets dist\assets
if exist "config.json" copy config.json dist\

echo.
echo [完成] 所有文件已准备就绪！
echo 可执行文件: dist\TwitterMonitor.exe
echo 配置文件: dist\config.json
echo 驱动文件: dist\drivers\
echo.

pause
