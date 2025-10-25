import requests

BASE_URL = "https://restful-booker.herokuapp.com"

class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL

    def post(self, endpoint, data=None, headers=None):
        return self.session.post(f"{self.base_url}{endpoint}", json=data, headers=headers)

    def get(self, endpoint, headers=None):
        return self.session.get(f"{self.base_url}{endpoint}", headers=headers)