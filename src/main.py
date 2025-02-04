import argparse
from config import settings
from scheduler import Scheduler
from github_client import GitHubClient
from notifier import Notifier
from report_generator import ReportGenerator
from llm import LLM
from subscription_manager import SubscriptionManager
from pkg.log import LOG


def run_scheduler(scheduler):
    scheduler.start()


def add_subscription(args, subscription_manager):
    subscription_manager.add_subscription(
        args.repo,
        description=args.description,
        hours=args.hours
    )
    print(f"Added subscription: {args.repo}")


def remove_subscription(args, subscription_manager):
    subscription_manager.remove_subscription(args.repo)
    print(f"Removed subscription: {args.repo}")


def list_subscriptions(args, subscription_manager):
    subscriptions = subscription_manager.get_subscriptions()
    print("Current subscriptions:")
    for sub in subscriptions:
        print(f"- {sub}")


def fetch_updates(args, github_client, subscription_manager, report_generator):
    subscriptions = subscription_manager.get_subscriptions()
    updates = github_client.fetch_updates(subscriptions)
    report = report_generator.generate(updates)
    print("Updates fetched:")
    print(report)


def main():
    LOG.info("system start...")
    try:
        LOG.info(f"Loading config: API_KEY={settings.api_key[:10]}...")  # 只打印前10个字符
        github_client = GitHubClient(settings.github_token)
        notifier = Notifier(settings.notification_settings)
        llm = LLM(settings.api_key)
        report_generator = ReportGenerator(llm)
        subscription_manager = SubscriptionManager(settings.subscriptions_file)

        scheduler = Scheduler(
            github_client=github_client,
            notifier=notifier,
            report_generator=report_generator,
            subscription_manager=subscription_manager,
            interval=settings.update_interval
        )

        scheduler.run()
    except Exception as e:
        LOG.error(f"Error in main: {str(e)}")
        raise


if __name__ == "__main__":
    main()
