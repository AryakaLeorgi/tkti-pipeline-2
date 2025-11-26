import requests
import base64
import json

class JenkinsCollector:
    def __init__(self, base_url, username, api_token):
        self.base_url = base_url.rstrip("/")
        self.auth = base64.b64encode(f"{username}:{api_token}".encode()).decode()

    def get_build_log(self, job_name, build_number):
        url = f"{self.base_url}/job/{job_name}/{build_number}/consoleText"
        headers = {"Authorization": f"Basic {self.auth}"}

        resp = requests.get(url, headers=headers)

        if resp.status_code != 200:
            raise Exception(f"Failed to fetch Jenkins log: {resp.text}")

        return resp.text
