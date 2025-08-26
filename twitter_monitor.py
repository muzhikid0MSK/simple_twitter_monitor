"""
Twitter监听模块
使用Selenium控制Chrome浏览器监听Twitter账户新帖子
"""
import time
import json
from datetime import datetime
from typing import Optional, Tuple, List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import os


class TwitterMonitor:
    def __init__(self, auth_token: str, headless: bool = False, chrome_driver_path: Optional[str] = None):
        """
        初始化Twitter监听器
        
        Args:
            auth_token: Twitter认证token
            headless: 是否使用无头模式
            chrome_driver_path: ChromeDriver路径
        """
        self.auth_token = auth_token
        self.headless = headless
        self.chrome_driver_path = chrome_driver_path
        self.driver = None
        self.last_tweet_id = None
        self.last_tweet_text = None
        
    def setup_driver(self):
        """设置Chrome驱动"""
        options = Options()
        
        # 基本选项
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Linux服务器特定选项
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        # 设置用户代理
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 无头模式
        if self.headless:
            options.add_argument('--headless=new')
        
        # 设置窗口大小
        options.add_argument('--window-size=1920,1080')
        
        # 创建驱动
        if self.chrome_driver_path:
            print(f"使用指定的ChromeDriver路径: {self.chrome_driver_path}")
            service = Service(self.chrome_driver_path)
        else:
            print("ChromeDriver路径未指定，尝试自动下载...")
            try:
                # 尝试使用webdriver-manager自动下载
                from webdriver_manager.chrome import ChromeDriverManager
                driver_path = ChromeDriverManager().install()
                print(f"ChromeDriver自动下载成功: {driver_path}")
                service = Service(driver_path)
            except Exception as e:
                print(f"自动下载ChromeDriver失败: {e}")
                print("尝试使用系统默认路径...")
                
                # 尝试常见的Linux chromedriver路径
                common_paths = [
                    "/usr/bin/chromedriver",
                    "/usr/local/bin/chromedriver",
                    "/snap/bin/chromedriver",
                    "./chromedriver",
                    "./drivers/chromedriver"
                ]
                
                driver_path = None
                for path in common_paths:
                    if os.path.exists(path):
                        try:
                            # 检查文件权限
                            if os.access(path, os.X_OK):
                                print(f"找到可执行的ChromeDriver: {path}")
                                driver_path = path
                                break
                            else:
                                print(f"找到ChromeDriver但无执行权限: {path}")
                                # 尝试添加执行权限
                                os.chmod(path, 0o755)
                                if os.access(path, os.X_OK):
                                    print(f"已添加执行权限: {path}")
                                    driver_path = path
                                    break
                        except Exception as perm_e:
                            print(f"权限设置失败: {perm_e}")
                
                if driver_path:
                    service = Service(driver_path)
                else:
                    raise Exception("无法找到可用的ChromeDriver，请手动安装或指定路径")
        
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            print("✅ Chrome驱动创建成功")
        except Exception as e:
            print(f"❌ Chrome驱动创建失败: {e}")
            # 提供详细的错误信息和解决方案
            if "chromedriver" in str(e).lower():
                print("\n可能的解决方案:")
                print("1. 手动下载ChromeDriver: https://chromedriver.chromium.org/")
                print("2. 使用包管理器安装: sudo apt-get install chromium-chromedriver")
                print("3. 检查Chrome浏览器是否已安装: google-chrome --version")
                print("4. 确保ChromeDriver版本与Chrome浏览器版本匹配")
            raise
        
        # 执行CDP命令以隐藏自动化特征
        try:
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
        except Exception as e:
            print(f"⚠️ CDP命令执行失败（非致命错误）: {e}")
    
    def login_with_token(self) -> bool:
        """使用token登录Twitter"""
        try:
            print("🔄 正在使用Token登录Twitter...")
            
            # 先访问Twitter主页
            self.driver.get("https://twitter.com")
            time.sleep(3)
            
            # 获取当前域名（可能是twitter.com或x.com）
            current_url = self.driver.current_url
            
            # 根据实际域名设置cookie
            if 'x.com' in current_url:
                cookie_domain = '.x.com'
                print("检测到X.com域名")
            else:
                cookie_domain = '.twitter.com'
                print("检测到Twitter.com域名")
            
            # 注入auth_token cookie
            try:
                self.driver.add_cookie({
                    'name': 'auth_token',
                    'value': self.auth_token,
                    'domain': cookie_domain,
                    'path': '/',
                    'secure': True,
                    'httpOnly': True
                })
            except Exception as e:
                print(f"⚠️ 第一次设置cookie失败，尝试其他方式: {e}")
                # 如果失败，尝试不指定domain
                self.driver.add_cookie({
                    'name': 'auth_token',
                    'value': self.auth_token,
                    'path': '/'
                })
            
            # 刷新页面应用cookie
            self.driver.refresh()
            time.sleep(5)
            
            # 检查是否登录成功（查找首页元素）
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]'))
                )
                print("✅ Token登录成功！")
                return True
            except TimeoutException:
                # 尝试查找其他登录后的元素
                try:
                    self.driver.find_element(By.CSS_SELECTOR, '[role="navigation"]')
                    print("✅ Token登录成功！")
                    return True
                except:
                    print("❌ Token登录失败，请检查Token是否有效")
                    return False
                
        except Exception as e:
            print(f"❌ 登录过程出错：{str(e)}")
            return False
    
    def navigate_to_user(self, username: str) -> bool:
        """导航到指定用户的Twitter页面"""
        try:
            print(f"🔄 正在访问 @{username} 的主页...")
            
            # 去掉@符号（如果有的话）
            username = username.lstrip('@')
            
            # 访问用户主页（支持twitter.com和x.com）
            # 先尝试twitter.com，会自动重定向到x.com
            url = f"https://twitter.com/{username}"
            self.driver.get(url)
            time.sleep(5)
            
            # 检查是否成功加载用户页面
            try:
                # 等待推文列表加载
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
                )
                print(f"✅ 成功访问 @{username} 的主页")
                return True
            except TimeoutException:
                # 检查是否是私密账户或不存在
                try:
                    error_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'This account doesn')]")
                    print(f"❌ 用户 @{username} 不存在")
                    return False
                except:
                    try:
                        private_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'These Tweets are protected')]")
                        print(f"❌ 用户 @{username} 是私密账户")
                        return False
                    except:
                        print(f"⚠️ 用户 @{username} 可能暂时没有推文")
                        return True
                        
        except Exception as e:
            print(f"❌ 访问用户页面出错：{str(e)}")
            return False
    
    def get_latest_tweet(self) -> Optional[Dict[str, str]]:
        """获取最新的推文"""
        try:
            # 刷新页面以获取最新内容
            self.driver.refresh()
            time.sleep(3)
            
            # 等待推文加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
            )
            
            # 获取第一条推文（最新的）
            tweets = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            
            if tweets:
                first_tweet = tweets[0]
                
                # 获取推文文本
                try:
                    tweet_text_element = first_tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    tweet_text = tweet_text_element.text
                except:
                    # 可能是纯图片/视频推文
                    tweet_text = "[媒体内容]"
                
                # 获取推文链接
                try:
                    # 查找时间戳链接（通常是推文的永久链接）
                    time_element = first_tweet.find_element(By.CSS_SELECTOR, 'time')
                    tweet_link_element = time_element.find_element(By.XPATH, '..')
                    tweet_url = tweet_link_element.get_attribute('href')
                    
                    # 如果是相对链接，转换为绝对链接
                    if tweet_url and not tweet_url.startswith('http'):
                        tweet_url = f"https://twitter.com{tweet_url}"
                except:
                    tweet_url = None
                
                # 获取推文ID（用于去重）
                try:
                    tweet_id = first_tweet.get_attribute('data-testid')
                    if not tweet_id:
                        # 使用文本的哈希值作为ID
                        import hashlib
                        tweet_id = hashlib.md5(tweet_text.encode()).hexdigest()
                except:
                    import hashlib
                    tweet_id = hashlib.md5(tweet_text.encode()).hexdigest()
                
                return {
                    'id': tweet_id,
                    'text': tweet_text,
                    'url': tweet_url,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            return None
            
        except TimeoutException:
            print("⏱️ 获取推文超时")
            return None
        except Exception as e:
            print(f"❌ 获取推文出错：{str(e)}")
            return None
    
    def check_for_new_tweet(self) -> Optional[Dict[str, str]]:
        """检查是否有新推文"""
        latest_tweet = self.get_latest_tweet()
        
        if latest_tweet:
            # 首次运行，记录当前最新推文
            if self.last_tweet_id is None:
                self.last_tweet_id = latest_tweet['id']
                self.last_tweet_text = latest_tweet['text']
                print(f"📝 记录初始推文: {latest_tweet['text'][:50]}...")
                return None
            
            # 检查是否是新推文
            if latest_tweet['id'] != self.last_tweet_id or latest_tweet['text'] != self.last_tweet_text:
                self.last_tweet_id = latest_tweet['id']
                self.last_tweet_text = latest_tweet['text']
                print(f"🆕 发现新推文: {latest_tweet['text'][:50]}...")
                return latest_tweet
        
        return None
    
    def start_monitoring(self, username: str, check_interval: int = 60, callback=None):
        """
        开始监听指定用户
        
        Args:
            username: Twitter用户名
            check_interval: 检查间隔（秒）
            callback: 发现新推文时的回调函数
        """
        self.monitoring = True
        
        try:
            # 设置驱动
            if not self.driver:
                self.setup_driver()
            
            # 登录
            if not self.login_with_token():
                print("❌ 登录失败，停止监听")
                return
            
            # 访问用户页面
            if not self.navigate_to_user(username):
                print("❌ 无法访问用户页面，停止监听")
                return
            
            print(f"🔍 开始监听 @{username}，检查间隔：{check_interval}秒")
            
            # 监听循环
            while self.monitoring:
                try:
                    new_tweet = self.check_for_new_tweet()
                    
                    if new_tweet and callback:
                        callback(username, new_tweet)
                    
                    # 等待下次检查
                    print(f"⏰ 等待 {check_interval} 秒后进行下次检查...")
                    time.sleep(check_interval)
                    
                except KeyboardInterrupt:
                    print("\n⏹️ 用户中断监听")
                    break
                except Exception as e:
                    print(f"❌ 监听过程出错：{str(e)}")
                    print(f"🔄 {check_interval} 秒后重试...")
                    time.sleep(check_interval)
                    
        finally:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """停止监听"""
        self.monitoring = False
        if self.driver:
            try:
                self.driver.quit()
                print("✅ 浏览器已关闭")
            except:
                pass
            self.driver = None
