import requests
from base64 import b64encode


class Jira():
    def __init__(self, url, usr, pwd):
        self.url = url
        self.user = usr
        self.pwd = pwd

    def load_key(self):
        url = self.url + '/rest/api/2/user/search'

        querystring = {"username": self.user}

        headers = {
            "Authorization": "Basic " + b64encode(f"{self.user}:{self.pwd}".encode('utf-8')).decode("ascii")
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        return response.json()[0]["key"]

    def load_key_test_cycle(self, cycle):

        uri = self.url + f'/testrun/{cycle}?fields=id'

        headers = {
            "Authorization": "Basic " + b64encode(f"{self.user}:{self.pwd}".encode('utf-8')).decode("ascii")
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["id"]
