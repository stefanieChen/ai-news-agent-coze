from langchain.tools import tool, ToolRuntime
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, formatdate, make_msgid
from coze_workload_identity import Client
from cozeloop.decorator import observe
from coze_coding_utils.runtime_ctx.context import new_context

client = Client()

def get_email_config():
    """获取邮件配置信息"""
    email_credential = client.get_integration_credential("integration-email-imap-smtp")
    return json.loads(email_credential)

@tool
@observe
def send_news_email(subject: str, content: str, to_email: str, runtime: ToolRuntime = None) -> str:
    """
    发送AI新闻汇总邮件
    
    Args:
        subject: 邮件主题
        content: 邮件正文内容（HTML格式）
        to_email: 收件人邮箱地址
    
    Returns:
        发送结果信息
    """
    try:
        # 获取邮件配置
        config = get_email_config()
        
        # 验证收件人邮箱
        if not to_email or "@" not in to_email:
            return "发送失败：收件人邮箱地址无效"
        
        # 创建HTML格式邮件
        msg = MIMEText(content, "html", "utf-8")
        msg["From"] = formataddr(("AI新闻助手", config["account"]))
        msg["To"] = to_email
        msg["Subject"] = Header(subject, "utf-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()
        
        # 创建SSL上下文
        ctx = ssl.create_default_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # 尝试发送邮件（最多3次）
        attempts = 3
        last_err = None
        
        for i in range(attempts):
            try:
                with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"], context=ctx, timeout=30) as server:
                    server.ehlo()
                    server.login(config["account"], config["auth_code"])
                    server.sendmail(config["account"], [to_email], msg.as_string())
                    server.quit()
                return f"邮件成功发送到 {to_email}"
            except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, 
                   smtplib.SMTPDataError, smtplib.SMTPHeloError, ssl.SSLError, OSError) as e:
                last_err = e
                if i < attempts - 1:  # 如果不是最后一次尝试，等待后重试
                    import time
                    time.sleep(1 * (i + 1))
                continue
        
        # 所有尝试都失败
        if last_err:
            return f"发送失败: {last_err.__class__.__name__} - {str(last_err)}"
        return "发送失败: 未知错误"
        
    except smtplib.SMTPAuthenticationError as e:
        return f"认证失败: 请检查邮箱授权码是否正确。错误信息: {str(e)}"
    except smtplib.SMTPRecipientsRefused as e:
        return f"收件人被拒绝: {to_email}"
    except smtplib.SMTPSenderRefused as e:
        return f"发件人被拒绝: {e.smtp_code} {e.smtp_error}"
    except smtplib.SMTPDataError as e:
        return f"数据被拒绝: {e.smtp_code} {e.smtp_error}"
    except smtplib.SMTPConnectError as e:
        return f"连接失败: {str(e)}"
    except Exception as e:
        return f"发送失败: {str(e)}"
