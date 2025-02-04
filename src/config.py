from dynaconf import Dynaconf
from pkg.log import LOG

settings = Dynaconf(
    settings_files=['config.yaml'],  # 配置文件路径
    environments=True,  # 启用环境支持
    load_dotenv=False,  # 禁用 .env 文件加载
)

# 验证必要的配置项
required_settings = [
    'github_token',
    'api_key',
    'update_interval',
    'notification_settings',
    'subscriptions_file'
]

for setting in required_settings:
    if not settings.get(setting):
        raise ValueError(f"Missing required setting: {setting}")

LOG.info("Configuration loaded successfully")
