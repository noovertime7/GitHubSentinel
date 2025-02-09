import time
from datetime import datetime, timedelta
from pkg.log import LOG


class Scheduler:
    def __init__(self, github_client, notifier, report_generator, subscription_manager, interval=86400):
        self.github_client = github_client
        self.notifier = notifier
        self.report_generator = report_generator
        self.subscription_manager = subscription_manager
        self.interval = interval

    def start(self):
        self.run()

    def run(self):
        while True:
            subscriptions = self.subscription_manager.get_subscriptions()
            for repo in subscriptions:
                # 获取仓库特定的小时设置
                hours = self.subscription_manager.get_hours(repo)
                since = datetime.utcnow() - timedelta(hours=hours)
                since_iso = since.isoformat() + "Z"  # GitHub API需要ISO 8601格式
                
                LOG.info(f"Fetching updates for {repo} (last {hours} hours)")
                updates = self.github_client.fetch_updates(repo, since=since_iso)
                markdown_file_path = self.report_generator.export_daily_progress(repo, updates)
                report ,report_path =self.report_generator.build_ai_report(markdown_file_path)

                self.notifier.notify(repo, report)
            
            time.sleep(self.interval)
