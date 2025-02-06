import json
from pkg.log import LOG


class SubscriptionManager:
    def __init__(self, subscriptions_file):
        self.subscriptions_file = subscriptions_file
        self.config = self.load_subscriptions()

    def load_subscriptions(self):
        try:
            with open(self.subscriptions_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            LOG.warning(f"Subscriptions file not found: {self.subscriptions_file}, creating default")
            default_config = {
                "settings": {
                    "hours": 24,  # 默认24小时
                    "auto_sync": True
                },
                "repositories": []
            }
            self.save_subscriptions(default_config)
            return default_config

    def save_subscriptions(self, config=None):
        if config is None:
            config = self.config
        with open(self.subscriptions_file, 'w') as f:
            json.dump(config, f, indent=2)

    def get_subscriptions(self):
        """获取所有订阅的仓库名称"""
        data=  [repo["name"] for repo in self.config["repositories"]]
        return data

    def get_repo_config(self, repo_name):
        """获取特定仓库的配置"""
        for repo in self.config["repositories"]:
            if repo["name"] == repo_name:
                return repo
        return None

    def get_hours(self, repo_name=None):
        """获取更新时间范围（小时）"""
        if repo_name:
            repo_config = self.get_repo_config(repo_name)
            if repo_config and "hours" in repo_config:
                return repo_config["hours"]
        return self.config["settings"]["hours"]

    def add_subscription(self, repo, description=None, hours=None):
        """添加订阅"""
        if repo not in self.get_subscriptions():
            new_repo = {"name": repo}
            if description:
                new_repo["description"] = description
            if hours:
                new_repo["hours"] = hours
            self.config["repositories"].append(new_repo)
            self.save_subscriptions()
            LOG.info(f"Added subscription: {repo}")

    def remove_subscription(self, repo):
        """移除订阅"""
        self.config["repositories"] = [
            r for r in self.config["repositories"] if r["name"] != repo
        ]
        self.save_subscriptions()
        LOG.info(f"Removed subscription: {repo}")

    def update_settings(self, hours=None, auto_sync=None):
        """更新全局设置"""
        if hours is not None:
            self.config["settings"]["hours"] = hours
        if auto_sync is not None:
            self.config["settings"]["auto_sync"] = auto_sync
        self.save_subscriptions()
