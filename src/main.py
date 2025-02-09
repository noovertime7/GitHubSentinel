from pkg.log import  LOG
import sys
from datetime import datetime,timedelta
import signal  # 导入signal库，用于信号处理
import schedule # 导入 schedule 实现定时任务执行器
import time  # 导入time库，用于控制时间间隔
from llm import LLM
from github_client import GitHubClient
from config import settings
from report_generator import ReportGenerator
from notifier import Notifier
from subscription_manager import  SubscriptionManager

def graceful_shutdown(signum, frame):
    # 优雅关闭程序的函数，处理信号时调用
    LOG.info("[优雅退出]守护进程接收到终止信号")
    sys.exit(0)  # 安全退出程序

def github_job(subscription_manager, github_client, report_generator, notifier):
    LOG.info("[开始执行定时任务]")
    subscriptions = subscription_manager.get_subscriptions()  # 获取当前所有订阅
    LOG.info(f"订阅列表：{subscriptions}")
    for repo in subscriptions:
        hours = subscription_manager.get_hours(repo)

        since = datetime.utcnow() - timedelta(hours=hours)
        since_iso = since.isoformat() + "Z"  # GitHub API需要ISO 8601格式

        updates = github_client.fetch_updates(repo, since_iso)
        # 遍历每个订阅的仓库，执行以下操作
        markdown_file_path = report_generator.export_daily_progress(repo, updates)
        # 从Markdown文件自动生成进展简报
        report, report_file_path = report_generator.build_ai_report(markdown_file_path)
        notifier.notify(repo, report)
    LOG.info(f"[定时任务执行完毕]")


def main():
    LOG.info("system start...")
    # 设置信号处理器
    signal.signal(signal.SIGTERM, graceful_shutdown)
    llm = LLM(settings.api_key)
    report_generator = ReportGenerator(llm)
    github_client = GitHubClient(settings.github_token)
    subscription_manager = SubscriptionManager(settings.subscriptions_file)
    notifier=Notifier(settings.email)

    LOG.info(f"Loading config: API_KEY={settings.api_key[:10]}...")  # 只打印前10个字符

 # 启动时立即执行（如不需要可注释）
    github_job(subscription_manager, github_client, report_generator, notifier)

    # 安排每天的定时任务
    schedule.every(1).days.at(
        settings.exec_time
    ).do(github_job, subscription_manager, github_client, report_generator, notifier)

    try:
        # 在守护进程中持续运行
        while True:
            schedule.run_pending()
            time.sleep(1)  # 短暂休眠以减少 CPU 使用
    except Exception as e:
        LOG.error(f"主进程发生异常: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()