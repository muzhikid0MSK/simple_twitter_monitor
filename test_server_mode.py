#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器模式测试脚本
用于测试服务器模式的基本功能
"""

import sys
import os
import time
import json
from pathlib import Path


def test_config_loading():
    """测试配置加载"""
    print("🔍 测试配置加载...")
    
    try:
        from config_manager import ConfigManager
        config_manager = ConfigManager()
        config = config_manager.config
        
        print(f"✅ 配置加载成功")
        print(f"  Twitter用户名: {config['twitter']['username']}")
        print(f"  检查间隔: {config['twitter']['check_interval']}秒")
        print(f"  邮箱服务商: {config['email']['provider']}")
        print(f"  系统语言: {config['system']['language']}")
        
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False


def test_email_sender():
    """测试邮件发送器"""
    print("\n🔍 测试邮件发送器...")
    
    try:
        from email_sender import EmailSender
        
        # 创建测试实例（不实际发送邮件）
        email_sender = EmailSender(
            "smtp.test.com",
            587,
            "test@example.com",
            "password",
            False,
            True
        )
        
        print("✅ 邮件发送器创建成功")
        return True
    except Exception as e:
        print(f"❌ 邮件发送器测试失败: {e}")
        return False


def test_twitter_monitor():
    """测试Twitter监控器"""
    print("\n🔍 测试Twitter监控器...")
    
    try:
        from twitter_monitor import TwitterMonitor
        
        # 创建测试实例（不实际启动监控）
        monitor = TwitterMonitor("test_token", True)
        
        print("✅ Twitter监控器创建成功")
        return True
    except Exception as e:
        print(f"❌ Twitter监控器测试失败: {e}")
        return False


def test_i18n():
    """测试国际化模块"""
    print("\n🔍 测试国际化模块...")
    
    try:
        from i18n import i18n
        
        # 测试语言切换
        current_lang = i18n.get_current_language()
        print(f"✅ 当前语言: {current_lang}")
        
        # 测试SMTP预设
        presets = i18n.get_smtp_presets()
        print(f"✅ SMTP预设数量: {len(presets)}")
        
        return True
    except Exception as e:
        print(f"❌ 国际化模块测试失败: {e}")
        return False


def test_server_mode():
    """测试服务器模式模块"""
    print("\n🔍 测试服务器模式模块...")
    
    try:
        from server_mode import TwitterMonitorServer
        
        # 创建测试实例（不实际启动服务）
        server = TwitterMonitorServer()
        
        print("✅ 服务器模式模块加载成功")
        return True
    except Exception as e:
        print(f"❌ 服务器模式模块测试失败: {e}")
        return False


def test_logging():
    """测试日志系统"""
    print("\n🔍 测试日志系统...")
    
    try:
        # 创建logs目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 测试日志文件创建
        test_log_file = log_dir / "test.log"
        with open(test_log_file, "w", encoding="utf-8") as f:
            f.write("测试日志\n")
        
        print("✅ 日志系统测试成功")
        
        # 清理测试文件
        test_log_file.unlink()
        
        return True
    except Exception as e:
        print(f"❌ 日志系统测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🧪 Twitter监控器服务器模式测试")
    print("=" * 60)
    
    tests = [
        ("配置加载", test_config_loading),
        ("邮件发送器", test_email_sender),
        ("Twitter监控器", test_twitter_monitor),
        ("国际化模块", test_i18n),
        ("服务器模式模块", test_server_mode),
        ("日志系统", test_logging),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！服务器模式可以正常使用。")
        print("\n使用示例:")
        print("  python main.py --server")
        print("  python start_server.py")
    else:
        print("⚠️  部分测试失败，请检查相关模块。")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
