"""
Twitter Auth Token获取辅助工具
帮助用户从浏览器中获取auth_token
"""
import os
import json
import base64
import sqlite3
import platform
from pathlib import Path
from typing import Optional

try:
    from Crypto.Cipher import AES
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("提示: 安装 pycryptodome 可以自动解密Chrome cookies")
    print("pip install pycryptodome")


def get_chrome_cookies_path() -> Optional[Path]:
    """获取Chrome cookies文件路径"""
    system = platform.system()
    
    if system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            path = Path(local_app_data) / "Google/Chrome/User Data/Default/Cookies"
            if path.exists():
                return path
    
    elif system == "Darwin":  # macOS
        home = Path.home()
        path = home / "Library/Application Support/Google/Chrome/Default/Cookies"
        if path.exists():
            return path
    
    elif system == "Linux":
        home = Path.home()
        path = home / ".config/google-chrome/Default/Cookies"
        if path.exists():
            return path
    
    return None


def get_twitter_token_from_chrome() -> Optional[str]:
    """从Chrome浏览器获取Twitter auth_token"""
    cookies_path = get_chrome_cookies_path()
    
    if not cookies_path:
        print("未找到Chrome cookies文件")
        return None
    
    print(f"找到Chrome cookies文件: {cookies_path}")
    
    # 复制cookies文件（因为Chrome可能正在使用）
    import shutil
    import tempfile
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        shutil.copy2(cookies_path, tmp_path)
        
        # 连接到SQLite数据库
        conn = sqlite3.connect(tmp_path)
        cursor = conn.cursor()
        
        # 查询Twitter的auth_token
        cursor.execute("""
            SELECT name, value, encrypted_value 
            FROM cookies 
            WHERE host_key = '.twitter.com' AND name = 'auth_token'
        """)
        
        result = cursor.fetchone()
        
        if result:
            name, value, encrypted_value = result
            
            if value:
                return value
            elif encrypted_value and CRYPTO_AVAILABLE:
                # 尝试解密（Windows Chrome加密）
                # 注意：这需要更复杂的实现，这里仅作示例
                print("Cookie已加密，需要解密...")
                return None
            else:
                print("Cookie已加密，但未安装解密库")
                return None
        else:
            print("未找到Twitter auth_token")
            return None
            
    except Exception as e:
        print(f"读取cookies出错: {e}")
        return None
    finally:
        conn.close()
        os.unlink(tmp_path)


def manual_guide():
    """手动获取token的指南"""
    print("\n" + "="*60)
    print("手动获取Twitter Auth Token的方法:")
    print("="*60)
    print()
    print("1. 打开Chrome浏览器")
    print("2. 访问 https://twitter.com 并登录你的账户")
    print("3. 登录成功后，按 F12 打开开发者工具")
    print("4. 切换到 'Application'（应用程序）标签")
    print("5. 在左侧展开 'Cookies' -> 'https://twitter.com'")
    print("6. 在右侧找到名为 'auth_token' 的cookie")
    print("7. 复制 'Value'（值）列中的内容")
    print("8. 这就是你的auth_token，将其粘贴到程序配置中")
    print()
    print("注意事项:")
    print("- auth_token通常很长（几百个字符）")
    print("- 确保复制完整，不要包含额外的空格")
    print("- token有有效期，过期后需要重新获取")
    print("- 不要分享你的token给他人")
    print()


def main():
    print("Twitter Auth Token 获取工具")
    print("-" * 40)
    
    # 尝试自动获取
    print("\n尝试自动获取Token...")
    token = get_twitter_token_from_chrome()
    
    if token:
        print("\n✅ 成功获取auth_token!")
        print("-" * 40)
        print(f"Token: {token[:20]}...{token[-20:]}")  # 只显示部分
        print("-" * 40)
        print("\n完整Token已复制到剪贴板（如果支持）")
        
        # 尝试复制到剪贴板
        try:
            import pyperclip
            pyperclip.copy(token)
            print("✅ Token已复制到剪贴板，可以直接粘贴使用")
        except ImportError:
            print("提示: 安装 pyperclip 可以自动复制到剪贴板")
            print("pip install pyperclip")
            print(f"\n完整Token:\n{token}")
    else:
        print("\n❌ 自动获取失败")
        print("可能的原因:")
        print("1. Chrome浏览器未登录Twitter")
        print("2. Cookies文件被加密（需要额外处理）")
        print("3. 使用了其他浏览器或配置文件")
        
        # 显示手动指南
        manual_guide()
    
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
