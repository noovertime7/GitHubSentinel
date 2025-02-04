from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class NotificationSettings(BaseSettings):
    enabled: bool = True
    frequency: str = "daily"


class Settings(BaseSettings):
    github_token: str = Field(..., env='GITHUB_TOKEN')
    notification_settings: NotificationSettings = NotificationSettings()
    subscriptions_file: str = Field(default="subscriptions.json",env="SubscriptionsFile")
    update_interval: int = Field(default=24 * 60 * 60, env='UPDATE_INTERVAL')  # 可以通过环境变量覆盖

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False


# 创建全局配置实例
settings = Settings()

# 使用示例
# from config import settings
# print(settings.github_token)
