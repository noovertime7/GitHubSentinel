from datetime import  datetime,timedelta

import gradio as gr  # 导入gradio库用于创建GUI
from config import settings
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器

github_client = GitHubClient(settings.github_token)
llm = LLM(settings.api_key)
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(settings.subscriptions_file)


def export_progress_by_date_range(repo, hours):
    print(subscription_manager.get_subscriptions(),repo,hours)

    since = datetime.utcnow() - timedelta(hours=hours)
    since_iso = since.isoformat() + "Z"  # GitHub API需要ISO 8601格式
    updates = github_client.fetch_updates(repo,since_iso)

    markdown_file_path = report_generator.export_daily_progress(repo, updates)

    report ,report_path = report_generator.build_ai_report(markdown_file_path)
    return report,report_path

# 创建Gradio界面
demo = gr.Interface(
    fn=export_progress_by_date_range,  # 指定界面调用的函数
    title="GitHubSentinel",  # 设置界面标题
    inputs=[
        gr.Dropdown(
            subscription_manager.get_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
        ),  # 下拉菜单选择订阅的GitHub项目
        gr.Slider(value=24, minimum=1, maximum=24, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：小时"),
        # 滑动条选择报告的时间范围
    ],
    outputs=[gr.Markdown(), gr.File(label="下载报告")],  # 输出格式：Markdown文本和文件下载
)

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))