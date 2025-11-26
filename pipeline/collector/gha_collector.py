import requests

class GHActionsCollector:
    def __init__(self, repo, token):
        self.repo = repo
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_run_log(self, run_id):
        url = f"https://api.github.com/repos/{self.repo}/actions/runs/{run_id}/logs"
        resp = requests.get(url, headers=self.headers)
        return resp.content
