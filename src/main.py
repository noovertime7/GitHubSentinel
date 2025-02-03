
from config import settings
from scheduler import Scheduler
from github_client import GitHubClient
from notifier import Notifier
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
from pkg.log import  LOG

def main():
    LOG.info("system start...")
    github_client = GitHubClient(settings.github_token)
    notifier = Notifier(settings.notification_settings)
    report_generator = ReportGenerator()
    subscription_manager = SubscriptionManager(settings.subscriptions_file)

    scheduler = Scheduler(
        github_client=github_client,
        notifier=notifier,
        report_generator=report_generator,
        subscription_manager=subscription_manager,
        interval=settings.update_interval
    )

    scheduler.start()

if __name__ == "__main__":
    main()
