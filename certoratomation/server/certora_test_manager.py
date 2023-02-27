import json
import os
import shutil
import subprocess
from pathlib import Path

from certoratomation.server.clients.certora_cloud_client import CertoraCloudClient
from certoratomation.server.constants import HandlersConstants
from certoratomation.server.handlers.run_environment import run_dev_utils, run_new_report, kill_local_environment


class CertoraTestManager:

    def __init__(self, run_environment: bool = False):
        with open(HandlersConstants.CONFIG_FILE, mode='r', encoding='utf-8') as f:
            self.config_file = json.load(f)

        self.environment = self.config_file.get('environment')
        url = self.config_file.get('environment_urls').get(self.config_file.get('environment'))
        self.certora_could_client = CertoraCloudClient(url)
        self.current_test = None
        self.run_environment = run_environment

        self.clear_previous_reports()
        if self.run_environment:
            self.run_frontend_environment()

    @staticmethod
    def run_frontend_environment():
        run_dev_utils()
        run_new_report()

    @staticmethod
    def clear_files_list(files_list: list, path_prefix: Path = None):
        for file in files_list:
            current_file = path_prefix.joinpath(file) if path_prefix else file
            try:
                if os.path.isfile(current_file):
                    os.remove(current_file)
            except Exception as e:
                pass

    def clear_test_data(self):
        test_data = os.listdir(HandlersConstants.LOCAL_DATA_FULL_PATH)
        self.clear_files_list(files_list=test_data, path_prefix=HandlersConstants.LOCAL_DATA_FULL_PATH)

    def clear_previous_reports(self):
        test_reports = HandlersConstants.TEST_PACKAGE.rglob("*.html")
        self.clear_files_list(files_list=test_reports)

    def init_test_data_local(self):
        tree_view_path = HandlersConstants.DEV_UTILS_LOCAL_DATA.joinpath(self.current_test.get('anonymous_key'))
        tree_view_files = os.listdir(tree_view_path)

        for file in tree_view_files:
            shutil.copy(
                src=tree_view_path.joinpath(file),
                dst=HandlersConstants.LOCAL_DATA_FULL_PATH.joinpath(file)
            )

    def init_test_data_remote(self):
        verification_progress = self.certora_could_client.get_verification_progress(
            user_id=int(self.current_test.get('user_id')),
            job_id=self.current_test.get('job_id'),
            anonymous_key=self.current_test.get('anonymous_key')
        )

        with open(file=HandlersConstants.LOCAL_DATA_FULL_PATH.joinpath('treeViewStatus.json'),
                  mode='w'
                  ) as f:
            json.dump(verification_progress, f)

        self.init_rules_data_recursive(verification_progress['verificationProgress']['rules'])

    def init_rules_data_recursive(self, rules_list: dict):
        for rule in rules_list:
            if rule['output']:
                rule_data = self.certora_could_client.get_asset_output(
                    user_id=int(self.current_test.get('user_id')),
                    job_id=self.current_test.get('job_id'),
                    anonymous_key=self.current_test.get('anonymous_key'),
                    file_name=rule.get('output')
                )

                with open(file=HandlersConstants.LOCAL_DATA_FULL_PATH.joinpath(rule['output']),
                          mode='w',
                          encoding='utf-8'
                          ) as f:
                    json.dump(rule_data, f, ensure_ascii=False, indent=4)

            if rule.get('children'):
                self.init_rules_data_recursive(rule['children'])

            if rule.get('asserts'):
                self.init_rules_data_recursive(rule['asserts'])

    def run_service(self):
        output = 0
        try:

            if not os.path.exists(HandlersConstants.LOCAL_DATA_FULL_PATH):
                os.makedirs(HandlersConstants.LOCAL_DATA_FULL_PATH)

            for test in self.config_file.get('data_candidates'):
                self.current_test = test

                environment_url = self.config_file.get('environment_urls').get(self.config_file.get('environment'))
                data_environment = self.current_test.get('data_environment')

                data_url = self.config_file.get('environment_urls').get(data_environment)
                self.certora_could_client.url = data_url

                self.clear_test_data()
                if data_environment == 'local':
                    self.init_test_data_local()
                else:
                    self.init_test_data_remote()

                pytest_params = HandlersConstants.RUN_TEST_PARAMS.format(
                    environment_url=environment_url,
                    anonymous_key=self.current_test.get("anonymous_key")
                )

                res_code = subprocess.run(
                    args=f'{HandlersConstants.RUN_TEST_COMMAND} {pytest_params}',
                    cwd=HandlersConstants.TEST_PACKAGE,
                    shell=True
                )

                output = output or res_code

        except Exception as e:
            output = -1

        finally:
            if self.run_environment:
                kill_local_environment()

            return output
