import requests
import shutil

from via_hub_logistc.model.zephry import TestFolder, TestCycle

class ReportManager():

    def __init__(self, host, key):
        self.url = host
        self.token = key

    ### Search key the of project in jira ###
    def get_project_key(self):
        url = self.url + '/rest/api/2/user/search'

        querystring = {"username": self.user}

        headers = {
            "Authorization": f'Basic {self.token}'
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        return response.json()[0]["key"]

    ### Search id the of cycle in jira ###
    def get_cycle_id(self, cycle):

        uri = self.url + f'/testrun/{cycle}?fields=id'

        headers = {
            "Authorization": f'Basic {self.token}'
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["id"]

    ### Add name the of cycle test in jira ###
    def create_cycle_name(self, project_id: int, release: str):
        uri = self.url + \
            f'/rest/tests/1.0/testrun/search?fields=id,key,name&query=testRun.projectId%20IN%20({project_id})'

        headers = {
            "Authorization": f"Basic {self.key}"
        }

        response = requests.request("GET", uri, headers=headers)

        cycles = response.json()['results']

        count_release = 0

        for cycle in cycles:
            if str(cycle['name']).find(release) > 0:
                count_release = count_release + 1

        return f'{release} | C{count_release + 1}'

    ###Create new folder for test regression ###
    def create_folder(self, folder_name: str, projectKey: str):
        uri = self.url + "/rest/atm/1.0/folder"

        headers = {
            "Authorization": f"Basic {self.key}"
        }

        payload = TestFolder(projectKey, folder_name, "TEST_RUN").__dict__

        requests.request("POST", uri, json=payload, headers=headers)

        return folder_name

    ###Create new cycle for test regression ###
    def create_cycle_test(self, folder_name: str, test_plan: str,  key: str, name_cycle: str, descripption: str, iteration: str, owner: str, cycle_date: str, status: str):

        payload = TestCycle(
            name_cycle,
            descripption,
            key,
            folder_name,
            iteration,
            owner,
            test_plan,
            cycle_date,
            status,
            []
        ).__dict__

        uri = self.url + "/rest/atm/1.0/testrun"

        headers = {
            "Authorization": f"Basic {self.key}"
        }

        response = requests.request("POST", uri, json=payload, headers=headers)

        return response.json()["key"]

    ### Add scenarios to an existing cycle ###
    def save_result_runner_tests(self, cycle: str, list_scenarios: dict):

        for scenario in list_scenarios:
            uri = self.url + \
                f'/rest/atm/1.0/testrun/{cycle}/testcase/{scenario["id"]}/testresult'

            headers = {
                "Authorization": f"Basic {self.key}"
            }

            requests.request('POST', uri, json=scenario["tc"], headers=headers)

    ### Add report the runner for existing cycle  ###
    def save_report_rennur(self, cycle, file_path):

        shutil.make_archive(file_path + '/report', 'zip', file_path)

        uri = self.url + f"/rest/atm/1.0/testrun/{cycle}/attachments"

        headers = {
           "Authorization": f"Basic {self.key}"
        }

        requests.request("POST", uri, files={"report_file": f'{file_path}/report.zip'}, headers=headers)

    ### Get info the of created test case ###
    def get_owner_test_case(self, test_key):

        uri = self.url + f'/rest/atm/1.0/testcase/{test_key}'

        headers = {
           "Authorization": f"Basic {self.token}"
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["owner"]
