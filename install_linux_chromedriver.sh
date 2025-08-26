#!/bin/bash

# Linux服务器ChromeDriver安装脚本
# 适用于Ubuntu/Debian/CentOS/RHEL等系统

echo "=========================================="
echo "Linux服务器ChromeDriver安装脚本"
echo "=========================================="

# 检测系统类型
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "无法检测操作系统类型"
    exit 1
fi

echo "检测到操作系统: $OS $VER"

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用root权限运行此脚本"
    exit 1
fi

# 安装Chrome浏览器
install_chrome() {
    echo "正在安装Google Chrome浏览器..."
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        # Ubuntu/Debian
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
        apt-get update
        apt-get install -y google-chrome-stable
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        # CentOS/RHEL
        yum install -y wget
        wget -O /etc/yum.repos.d/google-chrome.repo https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable.repo
        yum install -y google-chrome-stable
    else
        echo "不支持的操作系统: $OS"
        exit 1
    fi
    
    if command -v google-chrome &> /dev/null; then
        echo "✅ Chrome浏览器安装成功"
        google-chrome --version
    else
        echo "❌ Chrome浏览器安装失败"
        exit 1
    fi
}

# 安装ChromeDriver
install_chromedriver() {
    echo "正在安装ChromeDriver..."
    
    # 获取Chrome版本
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}')
    echo "Chrome版本: $CHROME_VERSION"
    
    # 创建临时目录
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # 下载ChromeDriver
    if [ "$CHROME_VERSION" -ge 115 ]; then
        # 新版本使用Chrome for Testing
        echo "使用Chrome for Testing下载ChromeDriver..."
        
        # 获取对应版本的ChromeDriver版本号
        DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION")
        echo "ChromeDriver版本: $DRIVER_VERSION"
        
        # 下载ChromeDriver
        wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$DRIVER_VERSION/linux64/chromedriver-linux64.zip"
    else
        # 旧版本
        echo "Chrome版本较旧，使用旧版下载方式..."
        wget -O chromedriver.zip "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION"
    fi
    
    if [ -f chromedriver.zip ]; then
        echo "下载完成，正在解压..."
        unzip -q chromedriver.zip
        
        # 查找chromedriver文件
        CHROMEDRIVER_PATH=$(find . -name "chromedriver" -type f | head -1)
        
        if [ -n "$CHROMEDRIVER_PATH" ]; then
            # 移动到系统路径
            mv "$CHROMEDRIVER_PATH" /usr/local/bin/chromedriver
            chmod +x /usr/local/bin/chromedriver
            
            echo "✅ ChromeDriver安装成功: /usr/local/bin/chromedriver"
            
            # 测试ChromeDriver
            if /usr/local/bin/chromedriver --version; then
                echo "✅ ChromeDriver测试成功"
            else
                echo "❌ ChromeDriver测试失败"
            fi
        else
            echo "❌ 未找到ChromeDriver文件"
            exit 1
        fi
    else
        echo "❌ ChromeDriver下载失败"
        exit 1
    fi
    
    # 清理临时文件
    cd /
    rm -rf "$TEMP_DIR"
}

# 安装系统依赖
install_dependencies() {
    echo "正在安装系统依赖..."
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        apt-get update
        apt-get install -y wget unzip curl
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        yum install -y wget unzip curl
    fi
}

# 检查现有安装
check_existing() {
    echo "检查现有安装..."
    
    if command -v google-chrome &> /dev/null; then
        echo "✅ Chrome浏览器已安装"
        google-chrome --version
    else
        echo "Chrome浏览器未安装"
        install_chrome
    fi
    
    if command -v chromedriver &> /dev/null; then
        echo "✅ ChromeDriver已安装"
        chromedriver --version
    else
        echo "ChromeDriver未安装"
        install_chromedriver
    fi
}

# 设置环境变量
setup_environment() {
    echo "设置环境变量..."
    
    # 添加到PATH
    if ! grep -q "/usr/local/bin" /etc/environment; then
        echo 'PATH="/usr/local/bin:$PATH"' >> /etc/environment
    fi
    
    # 设置DISPLAY变量（用于无头模式）
    if ! grep -q "DISPLAY" /etc/environment; then
        echo 'DISPLAY=:99' >> /etc/environment
    fi
    
    echo "✅ 环境变量设置完成"
}

# 创建启动脚本
create_startup_script() {
    echo "创建启动脚本..."
    
    cat > /usr/local/bin/start_twitter_monitor.sh << 'EOF'
#!/bin/bash

# Twitter监控器启动脚本
export DISPLAY=:99
export PATH="/usr/local/bin:$PATH"

# 启动虚拟显示（如果需要）
if ! pgrep -x "Xvfb" > /dev/null; then
    Xvfb :99 -screen 0 1920x1080x24 &
    sleep 2
fi

# 切换到项目目录
cd /path/to/your/twitter_monitor

# 启动监控器
python3 main.py
EOF
    
    chmod +x /usr/local/bin/start_twitter_monitor.sh
    echo "✅ 启动脚本创建完成: /usr/local/bin/start_twitter_monitor.sh"
}

# 主函数
main() {
    echo "开始安装..."
    
    install_dependencies
    check_existing
    setup_environment
    create_startup_script
    
    echo ""
    echo "=========================================="
    echo "安装完成！"
    echo "=========================================="
    echo ""
    echo "下一步操作："
    echo "1. 编辑启动脚本中的项目路径"
    echo "2. 运行: /usr/local/bin/start_twitter_monitor.sh"
    echo "3. 或者直接运行: python3 main.py"
    echo ""
    echo "如果遇到问题，请检查："
    echo "- Chrome浏览器版本: google-chrome --version"
    echo "- ChromeDriver版本: chromedriver --version"
    echo "- 系统依赖: ldd /usr/local/bin/chromedriver"
}

# 运行主函数
main
