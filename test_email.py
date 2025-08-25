"""
邮件发送测试脚本
用于测试修复后的邮件发送功能
"""
from email_sender import EmailSender


def test_email_sending():
    """测试邮件发送功能"""
    print("="*60)
    print("邮件发送功能测试")
    print("="*60)
    
    # 获取测试配置
    print("\n请输入测试配置:")
    sender_email = input("163邮箱地址: ").strip()
    sender_password = input("163邮箱授权码: ").strip()
    receiver_email = input("接收邮箱 (QQ邮箱): ").strip()
    
    if not all([sender_email, sender_password, receiver_email]):
        print("❌ 请填写完整的配置信息")
        return
    
    print(f"\n配置信息:")
    print(f"发件人: {sender_email}")
    print(f"接收人: {receiver_email}")
    print(f"SMTP服务器: smtp.163.com:465")
    
    # 创建邮件发送器
    try:
        email_sender = EmailSender(
            smtp_server="smtp.163.com",
            smtp_port=465,
            sender_email=sender_email,
            sender_password=sender_password
        )
        print("✅ 邮件发送器创建成功")
    except Exception as e:
        print(f"❌ 创建邮件发送器失败: {e}")
        return
    
    # 测试连接和发送
    print("\n正在测试邮件发送...")
    try:
        if email_sender.test_connection(receiver_email):
            print("\n🎉 测试成功！邮件已发送到QQ邮箱")
            print("请检查QQ邮箱的收件箱和垃圾邮件文件夹")
        else:
            print("\n❌ 测试失败，请检查配置信息")
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_email_sending()
    input("\n按回车键退出...")
