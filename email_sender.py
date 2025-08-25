"""
邮件发送模块
使用163邮箱SMTP服务器发送邮件
"""
import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
from typing import Optional


class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str, 
                 use_ssl: bool = True, use_tls: bool = False):
        """
        初始化邮件发送器
        
        Args:
            smtp_server: SMTP服务器地址
            smtp_port: SMTP端口
            sender_email: 发送者邮箱
            sender_password: 发送者邮箱密码或授权码
            use_ssl: 是否使用SSL连接
            use_tls: 是否使用TLS连接
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.use_ssl = use_ssl
        self.use_tls = use_tls
    
    def send_notification(self, receiver_email: str, twitter_username: str, 
                         tweet_content: str, tweet_url: Optional[str] = None) -> bool:
        """
        发送Twitter新帖子通知邮件
        
        Args:
            receiver_email: 接收者邮箱
            twitter_username: Twitter用户名
            tweet_content: 推文内容
            tweet_url: 推文链接（可选）
        
        Returns:
            是否发送成功
        """
        try:
            # 创建邮件对象
            message = MIMEMultipart()
            
            # 设置邮件头 - 严格按照RFC标准格式
            # From字段必须使用有效的邮箱地址格式
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = f"🔔 @{twitter_username} 发布了新推文"
            
            # 添加额外的邮件头信息
            message['Reply-To'] = self.sender_email
            message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            # 生成唯一的Message-ID，避免特殊字符
            message['Message-ID'] = f"<{uuid.uuid4().hex}@{self.smtp_server.split('.')[0]}.com>"
            
            # 构建邮件正文
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .header {{ background-color: #1DA1F2; color: white; padding: 15px; border-radius: 10px 10px 0 0; }}
                    .content {{ background-color: #f5f8fa; padding: 20px; border: 1px solid #e1e8ed; border-radius: 0 0 10px 10px; }}
                    .tweet-box {{ background-color: white; padding: 15px; border-radius: 10px; margin: 15px 0; border: 1px solid #e1e8ed; }}
                    .username {{ font-weight: bold; color: #1DA1F2; font-size: 18px; }}
                    .tweet-content {{ margin-top: 10px; line-height: 1.6; color: #14171a; }}
                    .time {{ color: #657786; font-size: 12px; margin-top: 10px; }}
                    .link {{ margin-top: 15px; }}
                    .link a {{ background-color: #1DA1F2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 20px; display: inline-block; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>🐦 Twitter 新推文通知</h2>
                    </div>
                    <div class="content">
                        <p>您关注的用户发布了新推文：</p>
                        <div class="tweet-box">
                            <div class="username">@{twitter_username}</div>
                            <div class="tweet-content">{tweet_content}</div>
                            <div class="time">检测时间：{current_time}</div>
                            {"<div class='link'><a href='" + tweet_url + "'>查看原推文</a></div>" if tweet_url else ""}
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # 同时添加纯文本版本
            text_content = f"""
Twitter 新推文通知

@{twitter_username} 发布了新推文：

{tweet_content}

检测时间：{current_time}
{f"推文链接：{tweet_url}" if tweet_url else ""}
            """
            
            # 添加邮件正文
            message.attach(MIMEText(text_content, 'plain', 'utf-8'))
            message.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # 发送邮件
            if self.use_ssl:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)
            
            print(f"✅ 邮件发送成功！接收者：{receiver_email}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败：{str(e)}")
            return False
    
    def test_connection(self, receiver_email: str) -> bool:
        """
        测试邮件连接和发送
        
        Args:
            receiver_email: 接收者邮箱
        
        Returns:
            是否测试成功
        """
        try:
            # 创建测试邮件
            message = MIMEText('这是一封测试邮件，用于验证邮箱配置是否正确。\n如果您收到这封邮件，说明配置成功！', 'plain', 'utf-8')
            
            # 设置邮件头 - 严格按照RFC标准格式
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = 'Twitter监控器 - 邮箱配置测试'
            
            # 添加额外的邮件头信息
            message['Reply-To'] = self.sender_email
            message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            # 生成唯一的Message-ID，避免特殊字符
            message['Message-ID'] = f"<{uuid.uuid4().hex}@{self.smtp_server.split('.')[0]}.com>"
            
            # 发送邮件
            if self.use_ssl:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)
            
            print(f"✅ 测试邮件发送成功！请检查 {receiver_email} 邮箱")
            return True
            
        except Exception as e:
            print(f"❌ 测试邮件发送失败：{str(e)}")
            return False
