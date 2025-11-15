import requests

from utils.constants import DEFAULT_TIMEOUT

BASE_URL = "https://restful-booker.herokuapp.com"

class ApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.s = requests.Session()
        self.base_url = base_url

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params=None,
        json=None,
        headers=None,
        timeout=DEFAULT_TIMEOUT,
    ):
        url = f"{self.base_url}{endpoint}"
        return self.s.request(method=method, url=url, params=params, json=json, headers=headers, timeout=timeout)

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)
