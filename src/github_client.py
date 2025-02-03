import requests
from pkg.log  import LOG


class GitHubClient:
    def __init__(self, token):
        self.token = token

    def fetch_updates(self, subscriptions):
        headers = {
            'Authorization': f'token {self.token}'
        }
        updates = {}
        for repo in subscriptions:
            url = f'https://api.github.com/repos/{repo}/releases/latest'
            LOG.info(f'fetching {url}')

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                updates[repo] = response.json()
            else:
                LOG.error(f'failed to fetch {url},msg {response.json()}')
        return updates
