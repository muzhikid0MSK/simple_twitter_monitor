@echo off
echo ====================================
echo    Twitter监控器 启动脚本
echo ====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [信息] 检测到Python环境
echo.

REM 检查并安装依赖
echo [信息] 正在检查依赖包...
pip show selenium >nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 正在安装依赖包...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖包安装失败
        pause
        exit /b 1
    )
    echo [信息] 依赖包安装完成
) else (
    echo [信息] 依赖包已安装
)
echo.

REM 启动程序
echo [信息] 正在启动Twitter监控器...
echo.
python main.py

REM 程序结束
echo.
echo [信息] 程序已退出
pause
