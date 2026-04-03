"""
邮件发送服务模块

提供异步邮件发送功能，用于发送验证码、通知等邮件
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

logger = logging.getLogger(__name__)

# 邮件配置（实际项目中应该从环境变量读取）
SMTP_CONFIG = {
    "hostname": os.getenv("SMTP_HOSTNAME", "smtp.example.com"),  # SMTP 服务器地址
    "port": int(os.getenv("SMTP_PORT", "587")),  # SMTP 端口（587 for TLS, 465 for SSL）
    "username": os.getenv("SMTP_USERNAME", "your-email@example.com"),  # 邮箱账号
    "password": os.getenv("SMTP_PASSWORD", "your-password"),  # 邮箱密码或授权码
    "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true",  # 是否使用 TLS
    "from_email": os.getenv("SMTP_FROM_EMAIL", "your-email@example.com"),  # 发件人邮箱
    "from_name": os.getenv("SMTP_FROM_NAME", "TestingMagPlm")  # 发件人名称
}

# 开发模式：如果为 True，邮件发送失败时仍返回成功，并在控制台打印验证码
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"


async def send_verification_email(to_email: str, code: str) -> bool:
    """
    发送验证码邮件
    
    Args:
        to_email: 收件人邮箱
        code: 验证码
    
    Returns:
        bool: 发送成功返回 True，失败返回 False
    """
    try:
        # 创建邮件内容
        subject = "密码重置验证码 - TestingMagPlm"
        
        # HTML 格式邮件内容
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #6366f1;">密码重置验证码</h2>
                <p>您好！</p>
                <p>您正在请求重置 TestingMagPlm 账户的密码。请使用以下验证码继续操作：</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <span style="display: inline-block; padding: 15px 30px; background-color: #f3f4f6; 
                                 border: 2px dashed #6366f1; border-radius: 8px; font-size: 24px; 
                                 font-weight: bold; color: #6366f1; letter-spacing: 5px;">
                        {code}
                    </span>
                </div>
                
                <p><strong>注意：</strong></p>
                <ul>
                    <li>该验证码将在 <strong>10 分钟</strong> 后失效</li>
                    <li>请勿将验证码泄露给他人</li>
                    <li>如果您没有请求重置密码，请忽略此邮件</li>
                </ul>
                
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                <p style="color: #6b7280; font-size: 14px;">
                    此致<br>
                    TestingMagPlm 团队
                </p>
            </div>
        </body>
        </html>
        """
        
        # 纯文本格式邮件内容（备用）
        text_content = f"""
        您好！
        
        您正在请求重置 TestingMagPlm 账户的密码。请使用以下验证码继续操作：
        
        验证码：{code}
        
        注意：
        - 该验证码将在 10 分钟后失效
        - 请勿将验证码泄露给他人
        - 如果您没有请求重置密码，请忽略此邮件
        
        此致
        TestingMagPlm 团队
        """
        
        # 创建邮件对象
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        msg["To"] = to_email
        
        # 添加纯文本和 HTML 版本
        part1 = MIMEText(text_content, "plain", "utf-8")
        part2 = MIMEText(html_content, "html", "utf-8")
        msg.attach(part1)
        msg.attach(part2)
        
        # 发送邮件
        await aiosmtplib.send(
            msg,
            hostname=SMTP_CONFIG["hostname"],
            port=SMTP_CONFIG["port"],
            username=SMTP_CONFIG["username"],
            password=SMTP_CONFIG["password"],
            start_tls=SMTP_CONFIG["use_tls"]
        )
        
        logger.info(f"验证码邮件已发送至：{to_email}")
        return True
        
    except Exception as e:
        logger.error(f"发送邮件失败：{to_email}, 错误：{str(e)}")
        
        # 开发模式：打印验证码到控制台并返回成功
        if DEV_MODE:
            logger.info(f"=" * 60)
            logger.info(f"开发模式：验证码")
            logger.info(f"收件人：{to_email}")
            logger.info(f"验证码：{code}")
            logger.info(f"=" * 60)
            return True
        
        return False


async def send_welcome_email(to_email: str, username: str) -> bool:
    """
    发送欢迎邮件
    
    Args:
        to_email: 收件人邮箱
        username: 用户名
    
    Returns:
        bool: 发送成功返回 True，失败返回 False
    """
    try:
        subject = "欢迎加入 TestingMagPlm！"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #6366f1;">欢迎加入 TestingMagPlm，{username}！</h2>
                <p>感谢您注册 TestingMagPlm 测试管理平台。</p>
                <p>现在您可以开始使用我们的平台来管理您的测试项目、用例和执行。</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5173/login" 
                       style="display: inline-block; padding: 12px 30px; background-color: #6366f1; 
                              color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">
                        立即登录
                    </a>
                </div>
                
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                <p style="color: #6b7280; font-size: 14px;">
                    此致<br>
                    TestingMagPlm 团队
                </p>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        msg["To"] = to_email
        
        part1 = MIMEText(html_content, "html", "utf-8")
        msg.attach(part1)
        
        await aiosmtplib.send(
            msg,
            hostname=SMTP_CONFIG["hostname"],
            port=SMTP_CONFIG["port"],
            username=SMTP_CONFIG["username"],
            password=SMTP_CONFIG["password"],
            start_tls=SMTP_CONFIG["use_tls"]
        )
        
        logger.info(f"欢迎邮件已发送至：{to_email}")
        return True
        
    except Exception as e:
        logger.error(f"发送欢迎邮件失败：{to_email}, 错误：{str(e)}")
        return False
