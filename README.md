# Twitter监控器 v2.0

一个功能强大的Twitter账户监听程序，支持多平台运行和多邮箱服务商。可以监控指定Twitter账户的新帖子，并通过多种邮箱服务发送通知。

## 🌟 新特性

- 🌍 **多平台支持**: Windows、Linux、macOS
- 📧 **多邮箱服务商**: 支持163、QQ、Gmail、Outlook、Yahoo等
- 🌐 **国际化支持**: 中文和英文界面
- 📦 **一键打包**: 支持PyInstaller打包为可执行文件
- 🐳 **Docker支持**: 容器化部署
- ⚙️ **灵活配置**: 支持SSL/TLS、SMTP端口等高级配置

## 功能特点

- 🔍 实时监控指定Twitter账户的新帖子
- 📧 通过163邮箱SMTP服务器发送邮件通知
- 🔐 使用Token方式登录Twitter（更安全）
- 🖥️ 简洁的图形用户界面（GUI）
- ⚙️ 所有配置均可在界面上设置
- 💾 自动保存和加载配置

## 安装要求

- Python 3.7 或更高版本
- Google Chrome 浏览器（最新版本）
- 支持的操作系统: Windows、macOS、Linux

## 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/yourusername/twitter-monitor.git
   cd twitter-monitor
   ```

2. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

## 配置说明

### 1. 获取Twitter Auth Token

1. 使用Chrome浏览器登录Twitter账户
2. 按F12打开开发者工具
3. 切换到"Application"（应用程序）标签
4. 在左侧找到"Cookies" -> "https://twitter.com"
5. 找到名为"auth_token"的cookie，复制其值

### 2. 配置邮箱服务

#### 163邮箱
1. 登录163邮箱网页版
2. 进入"设置" -> "POP3/SMTP/IMAP"
3. 开启SMTP服务
4. 生成授权码（注意：不是邮箱密码）

#### QQ邮箱
1. 登录QQ邮箱网页版
2. 进入"设置" -> "账户"
3. 开启"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 生成授权码

#### Gmail
1. 开启两步验证
2. 生成应用专用密码
3. 使用应用专用密码登录

#### Outlook/Hotmail
1. 开启"应用密码"
2. 生成应用密码
3. 使用应用密码登录

### 3. 在程序中配置

1. **Twitter配置**
   - 监听用户名：输入要监听的Twitter用户名（不需要@符号）
   - Auth Token：粘贴从浏览器获取的auth_token
   - 检查间隔：设置刷新频率（建议60秒以上）

2. **邮箱配置**
   - SMTP服务器：选择邮箱服务商或手动输入
   - SMTP端口：通常465(SSL)或587(TLS)
   - 发件人邮箱：你的邮箱地址
   - 邮箱密码/授权码：邮箱密码或应用专用密码
   - 接收邮箱：接收通知的邮箱地址
   - 连接方式：选择SSL或TLS

3. **浏览器配置**
   - 无头模式：勾选后浏览器在后台运行，不显示窗口

## 使用方法

1. 启动程序后，填写所有必要配置
2. 点击"保存配置"保存设置
3. 点击"测试邮箱"确认邮箱配置正确
4. 点击"开始监控"开始监听
5. 程序会自动刷新并检测新帖子
6. 发现新帖子时会自动发送邮件通知
7. 点击"停止监控"结束监听

## 注意事项

1. **Token有效期**：Twitter的auth_token可能会过期，如果登录失败请重新获取
2. **频率限制**：不要将检查间隔设置得太短，建议至少60秒
3. **邮箱限制**：163邮箱有每日发送限制，请合理使用
4. **Chrome版本**：程序会自动下载匹配的ChromeDriver，请确保Chrome是最新版本
5. **网络要求**：需要能够正常访问Twitter网站

## 常见问题

**Q: Token登录失败怎么办？**
A: 重新获取auth_token，确保复制完整且没有额外空格。

**Q: 邮件发送失败怎么办？**
A: 检查邮箱是否开启SMTP服务，密码/授权码是否正确，确认SMTP服务器和端口配置。

**Q: 程序无法检测到新帖子？**
A: 检查网络连接，确认能正常访问Twitter，尝试关闭无头模式查看浏览器状态。

**Q: 如何监听多个账户？**
A: 当前版本只支持单账户监听，可以运行多个程序实例监听不同账户。

**Q: 如何切换界面语言？**
A: 在配置文件中修改"system.language"字段，支持"zh_CN"和"en_US"。

**Q: 如何打包为可执行文件？**
A: 使用`python build_and_deploy.py --action build`命令，或运行`build_windows.bat`(Windows)或`./build_unix.sh`(Linux)。

## 🚀 高级功能

### 打包为可执行文件

#### 方法1: 使用构建脚本
```bash
# Windows
build_windows.bat

# Linux/macOS
./build_unix.sh
```

#### 方法2: 使用Python脚本
```bash
# 构建可执行文件
python build_and_deploy.py --action build --language zh_CN

# 创建发布包
python build_and_deploy.py --action package --language zh_CN
```

### Docker部署

#### 构建Docker镜像
```bash
python build_and_deploy.py --action docker --language zh_CN
```

#### 部署Docker容器
```bash
python build_and_deploy.py --action deploy
```

#### 使用Docker Compose
```bash
docker-compose up -d
```

### 多平台支持

- **Windows**: 生成.exe可执行文件
- **Linux**: 生成二进制可执行文件
- **Docker**: 容器化部署，支持所有平台

## 免责声明

本程序仅供学习和个人使用，请遵守Twitter的使用条款和相关法律法规。作者不对使用本程序造成的任何问题负责。

## 许可证

MIT License

## 作者

@muzhikid0MSK

## 更新日志

### v1.0 (2024-01-01)
- 初始版本发布
- 支持Token登录
- 支持邮件通知
- 简单GUI界面
