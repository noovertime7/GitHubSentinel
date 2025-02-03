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
    subscriptions_file: str = "subscriptions.json"
    update_interval: int = 24 * 60 * 60  # Default to 24 hours

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False


# 创建全局配置实例
settings = Settings()

# 使用示例
# from config import settings
# print(settings.github_token)
