import requests


class GitHubAPI:
    def __init__(self, access_token=None):
        self.access_token = access_token

    def _get_headers(self):
        if self.access_token:
            return {"Authorization": f"Token {self.access_token}"}
        else:
            return {}

    def _get_owner_and_repo(self, repo_url):
        parts = repo_url.split("/")
        owner = parts[-2]
        repo = parts[-1]
        return owner, repo

    def get_latest_release(self, repo_url):
        owner, repo = self._get_owner_and_repo(repo_url)
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None
