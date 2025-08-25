#!/bin/bash

echo "===================================="
echo "    Twitter监控器 启动脚本"
echo "===================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.7或更高版本"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

echo "[信息] 检测到Python环境: $(python3 --version)"
echo ""

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "[错误] 未检测到pip3，请先安装pip3"
    echo "Ubuntu/Debian: sudo apt-get install python3-pip"
    exit 1
fi

# 检查并安装依赖
echo "[信息] 正在检查依赖包..."
if ! pip3 show selenium &> /dev/null; then
    echo "[信息] 正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖包安装失败"
        exit 1
    fi
    echo "[信息] 依赖包安装完成"
else
    echo "[信息] 依赖包已安装"
fi
echo ""

# 启动程序
echo "[信息] 正在启动Twitter监控器..."
echo ""
python3 main.py

# 程序结束
echo ""
echo "[信息] 程序已退出"
