import smtplib
import markdown2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pkg.log import LOG


class Notifier:
    def __init__(self, email_settings):
        self.email_settings = email_settings
        self.verify_settings()

    def verify_settings(self):
        """验证邮件设置是否完整"""
        required_fields = ['smtp_server', 'smtp_port', 'from', 'to', 'password']
        for field in required_fields:
            if not self.email_settings or field not in self.email_settings:
                LOG.error(f"邮件配置缺少必要字段: {field}")
                return False
        return True

    def notify(self, repo, report):
        if not self.verify_settings():
            LOG.warning("邮件设置未配置正确，无法发送通知")
            return
        self.send_email(repo, report)

    def send_email(self, repo, report):
        try:
            LOG.info("准备发送邮件...")
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_settings['from']
            msg['To'] = self.email_settings['to']
            msg['Subject'] = f"[GitHubSentinel] {repo} 项目进展简报"

            # 添加纯文本和HTML版本
            text_part = MIMEText(report, 'plain', 'utf-8')
            html_part = MIMEText(markdown2.markdown(report), 'html', 'utf-8')
            msg.attach(text_part)
            msg.attach(html_part)

            # 使用with语句确保连接正确关闭
            with smtplib.SMTP_SSL(
                self.email_settings['smtp_server'],
                self.email_settings['smtp_port'],
                timeout=10
            ) as server:
                LOG.debug(f"连接到SMTP服务器: {self.email_settings['smtp_server']}")
                server.login(
                    self.email_settings['from'],
                    self.email_settings['password']
                )
                LOG.debug("SMTP登录成功")
                server.send_message(msg)
                LOG.info(f"邮件发送成功！接收者: {self.email_settings['to']}")

        except smtplib.SMTPAuthenticationError:
            LOG.error("SMTP认证失败，请检查用户名和密码")
        except (smtplib.SMTPException, Exception) as e:
            # 如果是QQ邮箱的特定错误，视为成功
            if "(-1, b'\\x00\\x00\\x00')" in str(e):
                LOG.info(f"邮件发送成功！接收者: {self.email_settings['to']}")
            else:
                LOG.error(f"发送邮件时发生错误: {str(e)}")
        except TimeoutError:
            LOG.error("连接SMTP服务器超时")


if __name__ == '__main__':
    # 测试配置
    email_settings = {
        'smtp_server': 'smtp.qq.com',
        'smtp_port': 465,
        'from': '',  # 替换为你的邮箱
        'password': '',  # 替换为你的密码
        'to': ''  # 替换为接收者邮箱
    }

    notifier = Notifier(email_settings)

    test_repo = "DjangoPeng/openai-quickstart"
    test_report = """
# DjangoPeng/openai-quickstart 项目进展

## 时间周期：2024-02-09

## 新增功能
- Assistants API 代码与文档

## 主要改进
- 适配 LangChain 新版本

## 修复问题
- 关闭了一些未解决的问题。
"""
    notifier.notify(test_repo, test_report)
