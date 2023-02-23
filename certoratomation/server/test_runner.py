import json
import os
import subprocess

from certoratomation.server.clients.certora_cloud_client import CertoraCloudClient
from certoratomation.server.constants import HandlersConstants


class CertoraTestRunner:

    def __init__(self, env):
        url = 'vaas-stg.certora.com' if env == 'stg' else 'prover.certora.com'
        self.certora_could_client = CertoraCloudClient(url)

    @staticmethod
    def clear_test_data():
        test_data = os.listdir(HandlersConstants.LOCAL_DATA_FULL_PATH)

        for data in test_data:
            if os.path.isfile(HandlersConstants.LOCAL_DATA_FULL_PATH.joinpath(data)):
                os.remove(HandlersConstants.LOCAL_DATA_FULL_PATH.joinpath(data))

    def init_test_data(self):
        if not os.path.exists(HandlersConstants.LOCAL_DATA_FULL_PATH):
            os.makedirs(HandlersConstants.LOCAL_DATA_FULL_PATH)
        else:
            self.clear_test_data()

        verification_progress = self.certora_could_client.get_verification_progress(
            user_id=99668,
            job_id='df7cc88dc08f4f58a430b4c6f68a95f3',
            anonymous_key='28c1c693bd38374e2ba1a9055877b93819e8d667'
        )

        with open(file=HandlersConstants.LOCAL_DATA_FULL_PATH.joinpath('treeViewStatus.json'),
                  mode='w'
                  ) as f:
            json.dump(verification_progress, f)

        verification_progress_rules = json.loads(verification_progress['verificationProgress'])['rules']

        for rule in verification_progress_rules:
            if rule['output']:
                rule_data = self.certora_could_client.get_asset_output(
                    user_id=99668,
                    job_id='df7cc88dc08f4f58a430b4c6f68a95f3',
                    anonymous_key='28c1c693bd38374e2ba1a9055877b93819e8d667',
                    file_name=rule['output']
                )

                with open(file=HandlersConstants.LOCAL_DATA_FULL_PATH.joinpath(rule['output']),
                          mode='w',
                          encoding='utf-8'
                          ) as f:
                    json.dump(rule_data, f, ensure_ascii=False, indent=4)

    def run_tests(self):
        self.init_test_data()

        return subprocess.run(
            args=HandlersConstants.RUN_TEST_COMMAND,
            cwd=HandlersConstants.TEST_PACKAGE,
            shell=True
        )

