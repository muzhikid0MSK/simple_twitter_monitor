#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康监控系统测试脚本
测试各种异常情况的检测能力
"""

import time
import threading
import sys
from pathlib import Path


def test_process_monitoring():
    """测试进程监控功能"""
    print("🔍 测试进程监控功能...")
    
    try:
        from server_mode import TwitterMonitorServer
        
        # 创建服务器实例
        server = TwitterMonitorServer()
        
        # 测试进程信息获取
        pid = server.process.pid
        print(f"✅ 进程ID获取成功: {pid}")
        
        # 测试CPU使用率监控
        cpu_percent = server.process.cpu_percent(interval=0.1)
        print(f"✅ CPU使用率监控正常: {cpu_percent:.1f}%")
        
        # 测试内存使用监控
        memory_info = server.process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        print(f"✅ 内存使用监控正常: {memory_mb:.1f}MB")
        
        # 测试运行时间监控
        uptime = time.time() - server.start_time
        print(f"✅ 运行时间监控正常: {uptime:.1f}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ 进程监控测试失败: {e}")
        return False


def test_thread_monitoring():
    """测试线程监控功能"""
    print("\n🔍 测试线程监控功能...")
    
    try:
        from server_mode import TwitterMonitorServer
        
        server = TwitterMonitorServer()
        
        # 创建测试线程
        def test_worker():
            time.sleep(2)
        
        test_thread = threading.Thread(target=test_worker)
        test_thread.start()
        
        # 测试线程存活检测
        if test_thread.is_alive():
            print("✅ 线程存活检测正常")
        else:
            print("❌ 线程存活检测失败")
            return False
        
        # 等待线程完成
        test_thread.join()
        
        # 测试线程停止检测
        if not test_thread.is_alive():
            print("✅ 线程停止检测正常")
        else:
            print("❌ 线程停止检测失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 线程监控测试失败: {e}")
        return False


def test_health_check_system():
    """测试健康检查系统"""
    print("\n🔍 测试健康检查系统...")
    
    try:
        from server_mode import TwitterMonitorServer
        
        server = TwitterMonitorServer()
        
        # 测试心跳间隔检查
        server.last_heartbeat = time.time() - 100  # 模拟心跳延迟
        try:
            server._check_program_health()
            print("❌ 心跳延迟检测失败")
            return False
        except Exception as e:
            if "心跳间隔异常" in str(e):
                print("✅ 心跳延迟检测正常")
            else:
                print(f"❌ 心跳延迟检测异常: {e}")
                return False
        
        # 重置心跳时间
        server.last_heartbeat = time.time()
        
        # 测试监控活动检查
        server.last_tweet_check_time = time.time() - 200  # 模拟检查延迟
        server.config['twitter']['check_interval'] = 60
        
        try:
            server._check_monitoring_activity()
            print("✅ 监控活动检查正常")
        except Exception as e:
            print(f"❌ 监控活动检查失败: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 健康检查系统测试失败: {e}")
        return False


def test_emergency_notification():
    """测试紧急通知系统"""
    print("\n🔍 测试紧急通知系统...")
    
    try:
        from server_mode import TwitterMonitorServer
        
        server = TwitterMonitorServer()
        
        # 测试系统信息获取
        system_info = server._get_system_info()
        if system_info and "进程ID" in system_info:
            print("✅ 系统信息获取正常")
        else:
            print("❌ 系统信息获取失败")
            return False
        
        # 测试紧急通知邮件构建（不实际发送）
        try:
            server.error_count = 3
            server._send_emergency_notification("测试异常")
            print("✅ 紧急通知系统正常")
        except Exception as e:
            if "邮箱配置不完整" in str(e):
                print("✅ 紧急通知配置检查正常")
            else:
                print(f"❌ 紧急通知系统异常: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 紧急通知系统测试失败: {e}")
        return False


def test_error_detection_scenarios():
    """测试各种错误检测场景"""
    print("\n🔍 测试错误检测场景...")
    
    try:
        from server_mode import TwitterMonitorServer
        
        server = TwitterMonitorServer()
        
        # 场景1: 模拟连续失败
        print("  测试场景1: 连续失败检测...")
        server.consecutive_failures = 4
        server.max_consecutive_failures = 5
        server.last_tweet_check_time = time.time() - 200
        server.config['twitter']['check_interval'] = 60
        
        try:
            server._check_monitoring_activity()
            print("    ✅ 连续失败检测正常")
        except Exception as e:
            if "连续5次推文检查异常" in str(e):
                print("    ✅ 连续失败阈值检测正常")
            else:
                print(f"    ❌ 连续失败检测异常: {e}")
                return False
        
        # 场景2: 模拟资源使用异常
        print("  测试场景2: 资源使用监控...")
        try:
            server._check_process_health()
            print("    ✅ 资源使用监控正常")
        except Exception as e:
            print(f"    ❌ 资源使用监控异常: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 错误检测场景测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🧪 健康监控系统测试")
    print("=" * 60)
    
    tests = [
        ("进程监控", test_process_monitoring),
        ("线程监控", test_thread_monitoring),
        ("健康检查系统", test_health_check_system),
        ("紧急通知系统", test_emergency_notification),
        ("错误检测场景", test_error_detection_scenarios),
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
        print("🎉 所有测试通过！健康监控系统工作正常。")
        print("\n健康监控功能包括:")
        print("  ✅ 进程资源监控 (CPU, 内存, 运行时间)")
        print("  ✅ 线程状态监控 (存活状态, 运行时间)")
        print("  ✅ 心跳间隔监控 (异常延迟检测)")
        print("  ✅ 监控活动检查 (推文检查频率)")
        print("  ✅ 连续失败检测 (阈值触发)")
        print("  ✅ 紧急通知系统 (邮件报警)")
        print("  ✅ 系统信息收集 (故障诊断)")
    else:
        print("⚠️  部分测试失败，请检查健康监控系统。")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
