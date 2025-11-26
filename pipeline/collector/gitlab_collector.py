import requests

class GitLabCollector:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip("/")
        self.headers = {"PRIVATE-TOKEN": token}

    def get_job_log(self, project_id, job_id):
        url = f"{self.base_url}/projects/{project_id}/jobs/{job_id}/trace"
        resp = requests.get(url, headers=self.headers)
        return resp.text
