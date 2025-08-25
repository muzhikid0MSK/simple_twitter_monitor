# Twitter监控器 v1.0

[English](README_EN.md) | 中文

一个功能强大的Twitter账户监听程序，支持多平台运行和多邮箱服务商。可以监控指定Twitter账户的新帖子，并通过多种邮箱服务发送通知。（不使用Twitter API）

## 🌟 新特性

- 🌍 **多平台支持**: Windows、Linux、macOS
- 📧 **多邮箱服务商**: 支持163、QQ、Gmail、Outlook、Yahoo等
- 🌐 **国际化支持**: 中文和英文界面
- 📦 **一键打包**: 支持PyInstaller打包为可执行文件
- 🐳 **Docker支持**: 容器化部署
- ⚙️ **灵活配置**: 支持SSL/TLS、SMTP端口等高级配置

## 功能特点

- 🔍 实时监控指定Twitter账户的新帖子
- 📧 通过多种邮箱服务商发送邮件通知
- 🔐 使用Token方式登录Twitter（更安全）
- 🖥️ 简洁的图形用户界面（GUI）
- ⚙️ 所有配置均可在界面上设置
- 💾 自动保存和加载配置

## 安装要求

- Python 3.7 或更高版本
- Google Chrome 浏览器（最新版本）
- 操作系统: Windows、Linux

## 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/muzhikid0MSK/simple_twitter_monitor.git
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
4. 在左侧找到"Cookies" -> "https://x.com"
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
A: 使用`python build_all.py`命令生成所有平台和语言版本。

## 🚀 高级功能

### 打包为可执行文件

#### 一键构建所有版本
```bash
# 构建当前平台和跨平台的所有版本
python build_all.py
```

这将生成以下版本：
- Windows 中文版
- Windows 英文版  
- Linux 中文版
- Linux 英文版

#### 单独构建脚本
```bash
# Windows
python build_multi_language.py

# 跨平台构建
python build_cross_platform.py
```

### Docker部署

#### 构建Docker镜像
```bash
docker build -t twitter-monitor .
```

#### 使用Docker Compose
```bash
docker-compose up -d
```

### 多平台支持

- **Windows**: 生成.exe可执行文件
- **Linux**: 生成二进制可执行文件
- **Docker**: 容器化部署，支持所有平台

## 📋 测试状态

### ✅ 已测试功能
- **平台**: Windows 10/11
- **邮箱组合**: 163邮箱 → QQ邮箱
- **核心功能**: Twitter监听、邮件发送、GUI界面、配置保存

### ⚠️ 待测试功能
- **其他平台**: Linux、macOS
- **其他邮箱**: Gmail、Outlook、Yahoo、自定义SMTP
- **跨平台构建**: Docker容器内构建

## 🔮 后续工作计划

### 短期目标
1. **完成所有平台和邮箱的测试**
   - 测试Linux和macOS平台
   - 测试Gmail、Outlook、Yahoo等邮箱服务
   - 验证跨平台构建功能

2. **功能优化**
   - 优化邮件发送成功率
   - 改进错误处理和日志记录
   - 添加更多邮箱服务商预设

### 长期目标 
1. **多账户监听功能**
   - 支持同时监听多个Twitter账户
   - 为不同账户配置不同的通知邮箱
   - 添加账户分组和管理功能

2. **高级功能**
   - 关键词过滤和内容分析
   - 定时任务和计划监控
   - 数据统计和报告生成


## 🌐 多语言README

本项目提供中英文两种语言的README文档：

- **中文版**: `README.md` (当前文件)
- **English Version**: `README_EN.md`
- **索引文件**: `README_INDEX.md` (查看所有语言版本)

### 在GitHub上切换语言

1. **快速切换**: 点击页面顶部的语言链接
   - 中文版顶部: `[English](README_EN.md)`
   - 英文版顶部: `[中文](README.md)`
2. **文件浏览器**: 在GitHub文件列表中点击对应语言版本
3. **索引文件**: 查看 `README_INDEX.md` 获取所有语言版本概览

### 贡献翻译

如果你希望添加其他语言版本，请：
1. 创建 `README_[语言代码].md` 文件
2. 翻译所有内容
3. 提交Pull Request

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。


## 免责声明

本程序仅供学习和个人使用，请遵守Twitter的使用条款和相关法律法规。作者不对使用本程序造成的任何问题负责。

## 作者

[@muzhikid0MSK](https://github.com/muzhikid0MSK/)

## 更新日志

### v1.0 (2025-8-25)
- 🌍 添加多平台支持 (Windows, Linux, macOS)
- 📧 支持多种邮箱服务商 (163, QQ, Gmail, Outlook, Yahoo)
- 🌐 国际化支持 (中文/英文)
- 📦 PyInstaller一键打包
- 🐳 Docker容器化支持
- ⚙️ 高级SMTP配置 (SSL/TLS)
- 🔧 改进的构建脚本和部署工具


