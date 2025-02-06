from datetime import datetime,date
from pkg.log import LOG
from file_manager import FileManager

class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm
        self.file_manager = FileManager()

    def export_daily_progress(self, repo, updates):
        # 生成报告内容
        content = self._generate_content(repo, updates)
        
        # 保存报告
        return self.file_manager.save_report(repo, content, "daily")

    def _generate_content(self, repo, updates):
        """生成报告内容"""
        lines = []
        
        # 添加仓库基本信息
        repo_info = updates.get('repo_info', {})
        if repo_info:
            lines.append(f"- 从: {repo_info['since']}开始查询")
            lines.append(f"# {repo_info['name']} 项目日报 ({date.today()})\n")
            lines.append("## 项目信息")
            lines.append(f"- 项目描述: {repo_info['description']}")
            lines.append(f"- 主要语言: {repo_info['language']}")
            lines.append(f"- Star数量: {repo_info['stars']}")
            if repo_info['topics']:
                lines.append(f"- 主题标签: {', '.join(repo_info['topics'])}")
            lines.append(f"- 最后更新: {repo_info['updated_at']}\n")
        else:
            lines.append(f"# Daily Progress for {repo} ({date.today()})\n")

        # 添加更新信息
        lines.append("## Commits")
        for commit in updates['commits']:
            lines.append(f"- {commit}")
        
        lines.append("\n## Issues")
        for issue in updates['issues']:
            lines.append(f"- {issue}")
        
        lines.append("\n## Pull Requests")
        for pr in updates['pull_requests']:
            lines.append(f"- {pr}")

        return '\n'.join(lines)

    def build_ai_report(self, markdown_file_path):
        # 读取原始报告
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        # 生成AI报告
        report = self.llm.generate(markdown_content)

        # 保存AI报告
        ai_report_path = self.file_manager.save_ai_report(markdown_file_path, report)
        if ai_report_path:
            LOG.info(f"推理成功 保存到文件： {ai_report_path}")
            return report,ai_report_path
        return None

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
