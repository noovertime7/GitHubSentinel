import os
from datetime import date
from pkg.log import LOG


class FileManager:
    def __init__(self, base_dir="reports"):
        """
        初始化文件管理器
        :param base_dir: 基础目录，默认为 'reports'
        """
        self.base_dir = base_dir
        self._ensure_base_dir()

    def _ensure_base_dir(self):
        """确保基础目录存在"""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            LOG.info(f"Created base directory: {self.base_dir}")

    def get_report_path(self, repo, filename=None):
        """
        获取报告文件的完整路径
        :param repo: 仓库名称 (如 'owner/repo')
        :param filename: 文件名，如果不提供则只返回目录路径
        :return: 完整的文件路径
        """
        # 分割仓库名称
        parts = repo.split('/')
        
        # 创建目录结构
        dir_path = os.path.join(self.base_dir, *parts)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            LOG.info(f"Created directory: {dir_path}")

        if filename:
            return os.path.join(dir_path, filename)
        return dir_path

    def save_report(self, repo, content, report_type="daily"):
        """
        保存报告文件
        :param repo: 仓库名称
        :param content: 报告内容
        :param report_type: 报告类型（daily, weekly 等）
        :return: 保存的文件路径
        """
        today = date.today()
        filename = f"{report_type}_{today}.md"
        file_path = self.get_report_path(repo, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            LOG.info(f"Saved report to: {file_path}")
            return file_path
        except Exception as e:
            LOG.error(f"Error saving report: {str(e)}")
            raise

    def save_ai_report(self, original_path, content):
        """
        保存AI生成的报告
        :param original_path: 原始报告的路径
        :param content: AI生成的内容
        :return: 保存的文件路径
        """
        # 在原始文件名基础上添加 _ai 后缀
        dir_path = os.path.dirname(original_path)
        filename = os.path.basename(original_path)
        name, ext = os.path.splitext(filename)
        ai_filename = f"{name}_ai{ext}"
        ai_path = os.path.join(dir_path, ai_filename)

        try:
            with open(ai_path, 'w', encoding='utf-8') as f:
                f.write(content)
            LOG.info(f"Saved AI report to: {ai_path}")
            return ai_path
        except Exception as e:
            LOG.error(f"Error saving AI report: {str(e)}")
            raise 