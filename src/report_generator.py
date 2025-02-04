import os
import time
from datetime import date

from llm import LLM

class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def export_daily_progress(self, repo, updates):
        file_path = f'{repo.replace("/", "_")}_{date.today()}.md'
        with open(file_path, 'w',encoding='utf-8') as file:
            file.write(f"# Daily Progress for {repo} ({date.today()})\n\n")
            file.write("## Commits\n")
            for commit in updates['commits']:
                file.write(f"- {commit}\n")
            file.write("\n## Issues\n")
            for issue in updates['issues']:
                file.write(f"- {issue}\n")
            file.write("\n## Pull Requests\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr}\n")
        return file_path

    def generate_daily_report(self, markdown_file_path):
        with open(markdown_file_path, 'r',encoding='utf-8') as file:
            markdown_content = file.read()

        report = self.llm.generate_daily_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + "_report.md"
        with open(report_file_path, 'w',encoding='utf-8') as report_file:
            report_file.write(report)

        print(f"推理成功 保存到文件： {report_file_path}")

    def parse_section(self, content, section):
        lines = content.split("\n")
        section_lines = []
        capture = False

        for line in lines:
            if line.strip() == section:
                capture = True
                continue
            if capture and line.startswith("##"):
                break
            if capture:
                section_lines.append(line.strip())

        return section_lines
