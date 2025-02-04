import argparse

from config import settings
from scheduler import Scheduler
from github_client import GitHubClient
from notifier import Notifier
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
from pkg.log import LOG
import threading


def run_scheduler(scheduler):
    scheduler.start()


def add_subscription(args, subscription_manager):
    subscription_manager.add_subscription(args.repo)
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

    scheduler_thread = threading.Thread(target=run_scheduler, args=(scheduler,))
    scheduler_thread.daemon = True
    scheduler_thread.start()

    parser = argparse.ArgumentParser(description='GitHub Sentinel Command Line Interface')
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    parser_add = subparsers.add_parser('add', help='Add a subscription')
    parser_add.add_argument('repo', type=str, help='The repository to subscribe to (e.g., owner/repo)')
    parser_add.set_defaults(func=lambda args: add_subscription(args, subscription_manager))

    parser_remove = subparsers.add_parser('remove', help='Remove a subscription')
    parser_remove.add_argument('repo', type=str, help='The repository to unsubscribe from (e.g., owner/repo)')
    parser_remove.set_defaults(func=lambda args: remove_subscription(args, subscription_manager))

    parser_list = subparsers.add_parser('list', help='List all subscriptions')
    parser_list.set_defaults(func=lambda args: list_subscriptions(args, subscription_manager))

    parser_fetch = subparsers.add_parser('fetch', help='Fetch updates immediately')
    parser_fetch.set_defaults(func=lambda args: fetch_updates(args, github_client, subscription_manager, report_generator))

    args = parser.parse_args()

    if args.command is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
