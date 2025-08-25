"""
邮箱配置功能测试脚本
测试不同邮箱服务商的配置
"""
from i18n import i18n, get_text


def test_email_provider_presets():
    """测试邮箱服务商预设配置"""
    print("="*60)
    print("邮箱服务商预设配置测试")
    print("="*60)
    
    # 获取预设配置
    presets = i18n.get_smtp_presets()
    
    for provider, config in presets.items():
        print(f"\n{provider.upper()} 邮箱:")
        print(f"  名称: {config['name']}")
        print(f"  SMTP服务器: {config['server']}")
        print(f"  SMTP端口: {config['port']}")
        
        # 根据服务商推荐连接方式
        if provider in ["163", "qq"]:
            print(f"  推荐连接方式: SSL")
        elif provider in ["gmail", "outlook", "yahoo"]:
            print(f"  推荐连接方式: TLS")
    
    print("\n" + "="*60)


def test_language_switching():
    """测试语言切换功能"""
    print("\n语言切换测试:")
    
    # 测试中文
    i18n.set_language("zh_CN")
    print(f"当前语言: {i18n.get_current_language()}")
    print(f"SMTP服务器标签: {get_text('smtp_server_label')}")
    print(f"邮箱配置: {get_text('email_config')}")
    
    # 测试英文
    i18n.set_language("en_US")
    print(f"\n当前语言: {i18n.get_current_language()}")
    print(f"SMTP服务器标签: {get_text('smtp_server_label')}")
    print(f"邮箱配置: {get_text('email_config')}")
    
    # 恢复中文
    i18n.set_language("zh_CN")


def test_email_config_validation():
    """测试邮箱配置验证"""
    print("\n" + "="*60)
    print("邮箱配置验证测试")
    print("="*60)
    
    # 测试配置示例
    test_configs = [
        {
            "provider": "163",
            "smtp_server": "smtp.163.com",
            "smtp_port": 465,
            "use_ssl": True,
            "use_tls": False
        },
        {
            "provider": "qq",
            "smtp_server": "smtp.qq.com",
            "smtp_port": 587,
            "use_ssl": False,
            "use_tls": True
        },
        {
            "provider": "gmail",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "use_ssl": False,
            "use_tls": True
        },
        {
            "provider": "custom",
            "smtp_server": "smtp.example.com",
            "smtp_port": 25,
            "use_ssl": False,
            "use_tls": False
        }
    ]
    
    for config in test_configs:
        print(f"\n{config['provider'].upper()} 配置:")
        print(f"  SMTP服务器: {config['smtp_server']}")
        print(f"  SMTP端口: {config['smtp_port']}")
        print(f"  SSL: {config['use_ssl']}")
        print(f"  TLS: {config['use_tls']}")
        
        # 验证端口范围
        if config['smtp_port'] < 1 or config['smtp_port'] > 65535:
            print(f"  ❌ 端口号无效: {config['smtp_port']}")
        else:
            print(f"  ✅ 端口号有效: {config['smtp_port']}")
        
        # 验证连接方式
        if config['use_ssl'] and config['use_tls']:
            print(f"  ❌ SSL和TLS不能同时启用")
        else:
            print(f"  ✅ 连接方式配置正确")


def main():
    """主函数"""
    print("邮箱配置功能测试")
    print("="*60)
    
    # 测试邮箱服务商预设配置
    test_email_provider_presets()
    
    # 测试语言切换
    test_language_switching()
    
    # 测试邮箱配置验证
    test_email_config_validation()
    
    print("\n" + "="*60)
    print("测试完成！")
    print("\n现在你可以:")
    print("1. 运行主程序: python main.py")
    print("2. 在邮箱配置中选择不同的服务商")
    print("3. 查看SMTP服务器和端口是否自动配置")
    print("4. 测试不同连接方式")


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
