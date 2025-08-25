# Twitter Monitor v1.0

English | [中文](README.md)

A powerful Twitter account monitoring program that supports multi-platform operation and multiple email service providers. It can monitor new posts from specified Twitter accounts and send notifications through various email services. (It doesn't use the Twitter's API)

## 🌟 New Features

- 🌍 **Multi-Platform Support**: Windows, Linux, macOS
- 📧 **Multiple Email Service Providers**: Support for 163, QQ, Gmail, Outlook, Yahoo, etc.
- 🌐 **Internationalization Support**: Chinese and English interfaces
- 📦 **One-Click Packaging**: Support for PyInstaller packaging as executable files
- 🐳 **Docker Support**: Containerized deployment
- ⚙️ **Flexible Configuration**: Support for SSL/TLS, SMTP ports, and other advanced configurations

## Features

- 🔍 Real-time monitoring of new posts from specified Twitter accounts
- 📧 Send email notifications through multiple email service providers
- 🔐 Use Token method to log into Twitter (more secure)
- 🖥️ Clean graphical user interface (GUI)
- ⚙️ All configurations can be set in the interface
- 💾 Automatic saving and loading of configurations

## Installation Requirements

- Python 3.7 or higher
- Google Chrome browser (latest version)
- Supported operating systems: Windows, Linux

## Installation Steps

1. **Clone or download the project**
   ```bash
   git clone https://github.com/muzhikid0MSK/simple_twitter_monitor.git
   cd twitter-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the program**
   ```bash
   python main.py
   ```

## Configuration Guide

### 1. Get Twitter Auth Token

1. Use Chrome browser to log into your Twitter account
2. Press F12 to open Developer Tools
3. Switch to the "Application" tab
4. Find "Cookies" -> "https://x.com" on the left side
5. Find the cookie named "auth_token" and copy its value

### 2. Configure Email Services

#### 163 Email
1. Log into 163 email web version
2. Go to "Settings" -> "POP3/SMTP/IMAP"
3. Enable SMTP service
4. Generate authorization code (Note: not the email password)

#### QQ Email
1. Log into QQ email web version
2. Go to "Settings" -> "Account"
3. Enable "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service"
4. Generate authorization code

#### Gmail
1. Enable two-factor authentication
2. Generate app-specific password
3. Use app-specific password to log in

#### Outlook/Hotmail
1. Enable "App passwords"
2. Generate app password
3. Use app password to log in

### 3. Configure in the Program

1. **Twitter Configuration**
   - Monitor Username: Enter the Twitter username to monitor (without @ symbol)
   - Auth Token: Paste the auth_token obtained from the browser
   - Check Interval: Set refresh frequency (recommended 60 seconds or more)

2. **Email Configuration**
   - SMTP Server: Select email service provider or enter manually
   - SMTP Port: Usually 465 (SSL) or 587 (TLS)
   - Sender Email: Your email address
   - Email Password/Authorization Code: Email password or app-specific password
   - Receiver Email: Email address to receive notifications
   - Connection Method: Choose SSL or TLS

3. **Browser Configuration**
   - Headless Mode: Check to run browser in background without displaying window

## Usage

1. After starting the program, fill in all necessary configurations
2. Click "Save Configuration" to save settings
3. Click "Test Email" to confirm email configuration is correct
4. Click "Start Monitoring" to begin monitoring
5. The program will automatically refresh and detect new posts
6. When new posts are found, email notifications will be sent automatically
7. Click "Stop Monitoring" to end monitoring

## Important Notes

1. **Token Validity**: Twitter's auth_token may expire; if login fails, please re-obtain it
2. **Rate Limiting**: Don't set the check interval too short, recommended at least 60 seconds
3. **Email Limits**: 163 email has daily sending limits, please use reasonably
4. **Chrome Version**: The program will automatically download matching ChromeDriver; please ensure Chrome is the latest version
5. **Network Requirements**: Need to be able to normally access Twitter website

## FAQ

**Q: What if Token login fails?**
A: Re-obtain the auth_token, ensure it's copied completely without extra spaces.

**Q: What if email sending fails?**
A: Check if the email has SMTP service enabled, if the password/authorization code is correct, and confirm SMTP server and port configuration.

**Q: The program can't detect new posts?**
A: Check network connection, confirm normal access to Twitter, try turning off headless mode to view browser status.

**Q: How to monitor multiple accounts?**
A: Current version only supports single account monitoring; you can run multiple program instances to monitor different accounts.

**Q: How to switch interface language?**
A: Modify the "system.language" field in the configuration file, supports "zh_CN" and "en_US".

**Q: How to package as executable file?**
A: Use the `python build_all.py` command to generate all platform and language versions.

## 🚀 Advanced Features

### Package as Executable File

#### One-Click Build All Versions
```bash
# Build all versions for current platform and cross-platform
python build_all.py
```

This will generate the following versions:
- Windows Chinese Version
- Windows English Version
- Linux Chinese Version
- Linux English Version

#### Individual Build Scripts
```bash
# Windows
python build_multi_language.py

# Cross-platform build
python build_cross_platform.py
```

### Docker Deployment

#### Build Docker Image
```bash
docker build -t twitter-monitor .
```

#### Use Docker Compose
```bash
docker-compose up -d
```

### Multi-Platform Support

- **Windows**: Generate .exe executable files
- **Linux**: Generate binary executable files
- **Docker**: Containerized deployment, supports all platforms

## 📋 Testing Status

### ✅ Tested Features
- **Platform**: Windows 10/11
- **Email Combination**: 163 Email → QQ Email
- **Core Functions**: Twitter monitoring, email sending, GUI interface, configuration saving

### ⚠️ Features to be Tested
- **Other Platforms**: Linux, macOS
- **Other Emails**: Gmail, Outlook, Yahoo, custom SMTP
- **Cross-Platform Build**: Docker container build

## 🔮 Future Work Plan

### Short-term Goals
1. **Complete testing of all platforms and emails**
   - Test Linux and macOS platforms
   - Test Gmail, Outlook, Yahoo and other email services
   - Verify cross-platform build functionality

2. **Function optimization**
   - Optimize email sending success rate
   - Improve error handling and logging
   - Add more email service provider presets

### Long-term Goals
1. **Multi-account monitoring functionality**
   - Support monitoring multiple Twitter accounts simultaneously
   - Configure different notification emails for different accounts
   - Add account grouping and management functions

2. **Advanced features**
   - Keyword filtering and content analysis
   - Scheduled tasks and planned monitoring
   - Data statistics and report generation

## 🌐 Multi-language README

This project provides README documents in two languages:

- **Chinese Version**: `README.md`
- **English Version**: `README_EN.md` (current file)
- **Index File**: `README_INDEX.md` (view all language versions)

### Switching Languages on GitHub

1. **Quick Switch**: Click on the language links at the top of the page
   - Chinese version top: `[English](README_EN.md)`
   - English version top: `[中文](README.md)`
2. **File Browser**: Click on the corresponding language version in GitHub's file list
3. **Index File**: Check `README_INDEX.md` for an overview of all language versions

### Contributing Translations

If you want to add other language versions, please:
1. Create `README_[language_code].md` file
2. Translate all content
3. Submit a Pull Request

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This program is for learning and personal use only. Please comply with Twitter's terms of service and relevant laws and regulations. The author is not responsible for any issues caused by using this program.

## Author

[@muzhikid0MSK](https://github.com/muzhikid0MSK/)

## Changelog

### v1.0 (2025-8-25)
- 🌍 Added multi-platform support (Windows, Linux, macOS)
- 📧 Support for multiple email service providers (163, QQ, Gmail, Outlook, Yahoo)
- 🌐 Internationalization support (Chinese/English)
- 📦 PyInstaller one-click packaging
- 🐳 Docker containerization support
- ⚙️ Advanced SMTP configuration (SSL/TLS)
- 🔧 Improved build scripts and deployment tools
