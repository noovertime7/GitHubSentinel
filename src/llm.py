# src/llm.py

import os
import openai
from click import prompt

from pkg.log import LOG

class LLM:
    def __init__(self, api_key):
        self.api_key = api_key
        LOG.info(f"Initializing LLM with API key: {api_key[:10]}...")  # 只打印前10个字符，保护密钥安全
        openai.api_key = self.api_key
        openai.api_base="https://ark.cn-beijing.volces.com/api/v3"

    def generate_daily_report(self, markdown_content):
        try:
            prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
            # prompt = "你好"
            response = openai.ChatCompletion.create(
                model="ep-20250204164421-6np9l",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            LOG.error(f"Error generating report: {str(e)}")
            return f"Error generating report: {str(e)}"
