"""
服务器模式模块
用于在服务器上无界面运行Twitter监控
"""
import time
import signal
import sys
import logging
import threading
import psutil
import os
from datetime import datetime
from config_manager import ConfigManager
from twitter_monitor import TwitterMonitor
from email_sender import EmailSender
from i18n import i18n


class TwitterMonitorServer:
    def __init__(self, config_path=None, language="zh_CN"):
        """初始化服务器模式"""
        # 设置语言
        i18n.set_language(language)
        
        # 配置日志
        self.setup_logging()
        
        # 加载配置
        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        
        # 监控器实例
        self.monitor = None
        self.monitoring = False
        
        # 心跳监控相关
        self.last_heartbeat = time.time()
        self.heartbeat_interval = 30
        self.error_count = 0
        self.max_errors = 3
        
        # 进程监控相关
        self.process = psutil.Process()
        self.start_time = time.time()
        self.last_check_time = time.time()
        self.health_check_interval = 10  # 健康检查间隔（秒）
        
        # 监控状态
        self.monitor_thread = None
        self.monitor_thread_start_time = None
        self.last_tweet_check_time = None
        self.consecutive_failures = 0
        self.max_consecutive_failures = 5
        
        # 信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.logger.info("🚀 Twitter监控服务器已初始化")
    
    def setup_logging(self):
        """设置日志系统"""
        # 创建日志目录
        import os
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 配置日志格式
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # 文件日志
        log_file = f"logs/twitter_monitor_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(file_formatter)
        
        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(log_format, date_format)
        console_handler.setFormatter(console_formatter)
        
        # 配置根日志器
        self.logger = logging.getLogger('TwitterMonitor')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # 防止日志重复
        self.logger.propagate = False
    
    def signal_handler(self, signum, frame):
        """信号处理函数"""
        self.logger.info(f"收到信号 {signum}，正在优雅关闭...")
        self.stop_monitoring()
        sys.exit(0)
    
    def start_heartbeat(self):
        """启动心跳监控"""
        self.logger.info("💓 心跳监控已启动")
        
        while self.monitoring:
            try:
                # 检查程序状态
                self._check_program_health()
                
                # 更新心跳时间
                self.last_heartbeat = time.time()
                
                # 记录心跳状态
                self.logger.info("💓 心跳正常 - 监控运行中")
                
                # 重置错误计数
                self.error_count = 0
                
                # 等待下次心跳
                time.sleep(self.heartbeat_interval)
                
            except Exception as e:
                self.error_count += 1
                error_msg = f"心跳检查出错: {str(e)}"
                self.logger.error(f"❌ {error_msg}")
                
                # 如果错误次数过多，发送紧急通知
                if self.error_count >= self.max_errors:
                    self._send_emergency_notification(error_msg)
                
                # 等待一段时间后继续
                time.sleep(5)
    
    def _check_program_health(self):
        """检查程序健康状态"""
        current_time = time.time()
        
        # 1. 检查心跳间隔是否过长
        if current_time - self.last_heartbeat > self.heartbeat_interval * 2:
            raise Exception("心跳间隔异常")
        
        # 2. 检查监控线程状态
        if self.monitor_thread:
            if not self.monitor_thread.is_alive():
                raise Exception("监控线程已停止运行")
            
            # 检查线程运行时间
            if self.monitor_thread_start_time:
                thread_runtime = current_time - self.monitor_thread_start_time
                if thread_runtime > 3600:  # 1小时
                    self.logger.warning(f"监控线程运行时间过长: {thread_runtime:.0f}秒")
        
        # 3. 检查监控器实例状态
        if self.monitor:
            if not hasattr(self.monitor, 'monitoring') or not self.monitor.monitoring:
                raise Exception("监控器状态异常")
        
        # 4. 检查进程资源使用
        self._check_process_health()
        
        # 5. 检查监控活动
        self._check_monitoring_activity()
    
    def _check_process_health(self):
        """检查进程健康状态"""
        try:
            # 检查CPU使用率
            cpu_percent = self.process.cpu_percent(interval=0.1)
            if cpu_percent > 90:  # CPU使用率超过90%
                self.logger.warning(f"CPU使用率过高: {cpu_percent:.1f}%")
            
            # 检查内存使用
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            if memory_mb > 500:  # 内存使用超过500MB
                self.logger.warning(f"内存使用过高: {memory_mb:.1f}MB")
            
            # 检查进程运行时间
            uptime = time.time() - self.start_time
            if uptime > 86400:  # 运行超过24小时
                self.logger.info(f"进程已运行: {uptime/3600:.1f}小时")
                
        except Exception as e:
            self.logger.warning(f"进程健康检查失败: {e}")
    
    def _check_monitoring_activity(self):
        """检查监控活动状态"""
        current_time = time.time()
        
        # 检查是否有正常的推文检查活动
        if self.last_tweet_check_time:
            time_since_last_check = current_time - self.last_tweet_check_time
            expected_interval = self.config['twitter']['check_interval']
            
            # 如果超过预期检查间隔的2倍，可能有问题
            if time_since_last_check > expected_interval * 2:
                self.logger.warning(f"推文检查间隔异常: {time_since_last_check:.0f}秒 (预期: {expected_interval}秒)")
                
                # 如果连续多次检查异常，增加失败计数
                self.consecutive_failures += 1
                if self.consecutive_failures >= self.max_consecutive_failures:
                    raise Exception(f"连续{self.consecutive_failures}次推文检查异常")
            else:
                # 重置失败计数
                self.consecutive_failures = 0
    
    def _send_emergency_notification(self, error_msg):
        """发送紧急通知邮件"""
        try:
            # 获取邮箱配置
            email_config = self.config['email']
            smtp_server = email_config['smtp_server']
            smtp_port = email_config['smtp_port']
            sender_email = email_config['sender_email']
            sender_password = email_config['sender_password']
            receiver_email = email_config['receiver_email']
            
            if not all([smtp_server, smtp_port, sender_email, sender_password, receiver_email]):
                self.logger.error("❌ 无法发送紧急通知：邮箱配置不完整")
                return
            
            # 创建邮件发送器
            email_sender = EmailSender(
                smtp_server,
                int(smtp_port),
                sender_email,
                sender_password,
                email_config.get('use_ssl', True),
                email_config.get('use_tls', False)
            )
            
            # 构建紧急通知内容
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            subject = "🚨 Twitter监控器紧急通知" if i18n.get_current_language() == "zh_CN" else "🚨 Twitter Monitor Emergency Alert"
            
            # 获取系统信息
            system_info = self._get_system_info()
            
            body = f"""
程序异常通知

时间: {current_time}
错误信息: {error_msg}
错误次数: {self.error_count}/{self.max_errors}
程序状态: {'监控中' if self.monitoring else '待机'}
监控账户: {self.config['twitter']['username']}

系统信息:
{system_info}

请立即检查程序状态并采取相应措施。

---
Twitter监控器 v1.0
            """ if i18n.get_current_language() == "zh_CN" else f"""
Emergency Alert

Time: {current_time}
Error: {error_msg}
Error Count: {self.error_count}/{self.max_errors}
Program Status: {'Monitoring' if self.monitoring else 'Standby'}
Monitored Account: {self.config['twitter']['username']}

System Info:
{system_info}

Please check program status immediately and take appropriate action.

---
Twitter Monitor v1.0
            """
            
            # 发送紧急通知
            if email_sender.send_notification(
                receiver_email,
                "SYSTEM",
                body,
                None,
                subject
            ):
                self.logger.info("📧 紧急通知邮件已发送")
            else:
                self.logger.error("❌ 紧急通知邮件发送失败")
                
        except Exception as e:
            self.logger.error(f"❌ 发送紧急通知时出错: {str(e)}")
    
    def _get_system_info(self):
        """获取系统信息"""
        try:
            info = []
            
            # 进程信息
            info.append(f"进程ID: {self.process.pid}")
            info.append(f"运行时间: {(time.time() - self.start_time)/3600:.1f}小时")
            
            # 资源使用
            cpu_percent = self.process.cpu_percent(interval=0.1)
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            info.append(f"CPU使用率: {cpu_percent:.1f}%")
            info.append(f"内存使用: {memory_mb:.1f}MB")
            
            # 线程信息
            if self.monitor_thread:
                info.append(f"监控线程状态: {'运行中' if self.monitor_thread.is_alive() else '已停止'}")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"获取系统信息失败: {e}"
    
    def on_new_tweet(self, username: str, tweet: dict):
        """新推文回调函数"""
        # 更新最后检查时间
        self.last_tweet_check_time = time.time()
        
        self.logger.info(f"🆕 发现新推文: {tweet['text'][:100]}...")
        
        # 发送邮件通知
        email_config = self.config['email']
        email_sender = EmailSender(
            email_config['smtp_server'],
            int(email_config['smtp_port']),
            email_config['sender_email'],
            email_config['sender_password'],
            email_config.get('use_ssl', True),
            email_config.get('use_tls', False)
        )
        
        if email_sender.send_notification(
            email_config['receiver_email'],
            username,
            tweet['text'],
            tweet.get('url')
        ):
            self.logger.info("✅ 邮件通知已发送")
        else:
            self.logger.error("❌ 邮件发送失败")
    
    def start_monitoring(self):
        """开始监控"""
        try:
            # 获取配置
            twitter_config = self.config['twitter']
            username = twitter_config['username']
            auth_token = twitter_config['auth_token']
            check_interval = twitter_config['check_interval']
            headless = self.config['browser']['headless']
            chrome_driver_path = self.config['browser'].get('chrome_driver_path')
            
            # 验证配置
            if not username:
                raise ValueError("Twitter用户名未配置")
            if not auth_token:
                raise ValueError("Twitter Auth Token未配置")
            
            # 更新心跳间隔
            self.heartbeat_interval = max(10, check_interval // 2)
            
            self.logger.info(f"🚀 开始监控 @{username}")
            self.logger.info(f"检查间隔: {check_interval}秒")
            self.logger.info(f"心跳间隔: {self.heartbeat_interval}秒")
            
            # 创建监控器
            self.monitor = TwitterMonitor(auth_token, headless, chrome_driver_path)
            self.monitoring = True
            
            # 启动心跳监控（在后台线程中）
            heartbeat_thread = threading.Thread(target=self.start_heartbeat, daemon=True)
            heartbeat_thread.start()
            
            # 开始监控
            self.monitor.start_monitoring(
                username,
                check_interval,
                self.on_new_tweet
            )
            
        except Exception as e:
            self.logger.error(f"❌ 启动监控失败: {str(e)}")
            raise
    
    def stop_monitoring(self):
        """停止监控"""
        if self.monitor:
            self.logger.info("⏹️ 正在停止监控...")
            self.monitor.monitoring = False
            self.monitor.stop_monitoring()
        
        self.monitoring = False
        self.logger.info("✅ 监控已停止")
    
    def run(self):
        """运行服务器"""
        try:
            self.logger.info("🔄 启动Twitter监控服务器...")
            self.start_monitoring()
        except KeyboardInterrupt:
            self.logger.info("收到中断信号，正在关闭...")
        except Exception as e:
            self.logger.error(f"服务器运行出错: {str(e)}")
        finally:
            self.stop_monitoring()
            self.logger.info("服务器已关闭")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Twitter监控器服务器模式')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--language', '-l', choices=['zh_CN', 'en_US'], default='zh_CN', help='界面语言')
    parser.add_argument('--username', '-u', help='要监控的Twitter用户名（覆盖配置文件）')
    parser.add_argument('--token', '-t', help='Twitter Auth Token（覆盖配置文件）')
    parser.add_argument('--interval', '-i', type=int, help='检查间隔（秒，覆盖配置文件）')
    
    args = parser.parse_args()
    
    # 创建服务器实例
    server = TwitterMonitorServer(args.config, args.language)
    
    # 如果提供了命令行参数，更新配置
    if args.username:
        server.config['twitter']['username'] = args.username.lstrip('@')
    if args.token:
        server.config['twitter']['auth_token'] = args.token
    if args.interval:
        server.config['twitter']['check_interval'] = args.interval
    
    # 运行服务器
    server.run()


if __name__ == "__main__":
    main()
