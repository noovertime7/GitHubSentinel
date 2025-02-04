import datetime
import requests
from pkg.log import LOG


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'token {self.token}'}

    def _make_request(self, endpoint, params=None):
        """通用的请求方法"""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            LOG.error(f"Error making request to {endpoint}: {str(e)}")
            return None

    def fetch_updates(self, repo, since=None, until=None):
        # 获取仓库基本信息
        repo_info = self.fetch_repo_info(repo)

        # 构建时间参数
        params = {}
        if since:
            params['since'] = since
            repo_info['since'] = since
        if until:
            params['until'] = until
            repo_info['until'] = until

        # 获取特定 repo 的更新
        updates = {
            'repo_info': repo_info,
            'commits': self.fetch_commits(repo, params) or [],
            'issues': self.fetch_issues(repo, params) or [],
            'pull_requests': self.fetch_pull_requests(repo, params) or []
        }
        return updates

    def fetch_repo_info(self, repo):
        """获取仓库的基本信息"""
        data = self._make_request(f"repos/{repo}")
        if data:
            return {
                'name': data['name'],
                'full_name': data['full_name'],
                'description': data['description'],
                'stars': data['stargazers_count'],
                'language': data['language'],
                'created_at': data['created_at'],
                'updated_at': data['updated_at'],
                'homepage': data['homepage'],
                'topics': data.get('topics', [])
            }
        return None

    def fetch_commits(self, repo, params=None):
        """获取提交记录"""
        data = self._make_request(f"repos/{repo}/commits", params)
        if data:
            return [{"commit": item["commit"]} for item in data]
        return None

    def fetch_issues(self, repo, params=None):
        """获取问题列表"""
        data = self._make_request(f"repos/{repo}/issues", params)
        if data:
            # 保留关键信息
            out = []
            for item in data:
                issue = {
                    'number': item['number'],
                    'title': item['title'],
                    'state': item['state'],
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    'author': item['user']['login'],
                    'labels': [label['name'] for label in item['labels']],
                    'body': item['body'],
                }
                if item['assignee']:
                    issue['assignee'] = item['assignee']['login']
                out.append(issue)
            return out
        return None

    def fetch_pull_requests(self, repo, params=None):
        """获取PR列表"""
        data = self._make_request(f"repos/{repo}/pulls", params)
        if data:
            # 保留关键信息
            out = []
            for item in data:
                pr = {
                    'number': item['number'],
                    'title': item['title'],
                    'state': item['state'],
                    'body': item['body'],
                    'html_url': item['html_url'],
                }
                if item['assignee']:
                    pr['assignee'] = item['assignee']['login']
                out.append(pr)
            return out
        return None
