import json

from requests import (
    get as requests_get,
    post as requests_post,
    patch as requests_patch,
)


class CertoraCloudClient:
    _url: str
    _port: int

    def __init__(self, url: str, port: int = None):
        self._url = url
        self._port = port

    @property
    def url(self):
        return f'http://{self._url}:{self._port}' if self._port else f'http://{self._url}'

    @url.setter
    def url(self, url):
        self._url = url

    def get_tree_view_output(self, user_id, job_id, anonymous_key=''):
        url = f'{self.url}/output/{user_id}/{job_id}/?anonymousKey={anonymous_key}'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        resp = requests_get(url, headers=headers)
        assert resp.status_code == 200, f'Get Progress API Call Failed! \nurl: {url} \noutput: {resp.text}'

        raw_data = resp.json()
        return raw_data

    def get_verification_progress(self, user_id, job_id, anonymous_key=''):
        url = f'{self.url}/progress/{user_id}/{job_id}/?anonymousKey={anonymous_key}'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        resp = requests_get(url, headers=headers)
        assert resp.status_code == 200, f'Get Progress API Call Failed! \nurl: {url} \noutput: {resp.text}'

        raw_data = resp.json()
        raw_data['verificationProgress'] = json.loads(raw_data['verificationProgress'])
        return raw_data

    def get_asset_output(self, user_id, job_id, anonymous_key, file_name):
        url = f'{self.url}/result/{user_id}/{job_id}/?anonymousKey={anonymous_key}&output={file_name}'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        resp = requests_get(url, headers=headers)
        assert resp.status_code == 200, f'Get Progress API Call Failed! \nurl: {url} \noutput: {resp.text}'

        raw_data = resp.json()
        return raw_data

