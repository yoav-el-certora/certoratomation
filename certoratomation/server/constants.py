import os
from pathlib import Path


class HandlersConstants:
    ROOT_PATH = Path(__file__).parent.parent.parent

    CONFIG_FILE = ROOT_PATH.joinpath('local/config_file.json')

    DEV_UTILS = ROOT_PATH.joinpath('DevUtils/Mac')
    DEV_UTILS_LOCAL_DATA = ROOT_PATH.joinpath('tests_local_resources')
    LOCAL_DATA_FULL_PATH = DEV_UTILS_LOCAL_DATA.joinpath('Reports/treeView')
    DEV_UTILS_INSTALL_COMMAND = f'pip install {DEV_UTILS}'
    DEV_UTILS_RUN_COMMAND = f'poetry run python3 frontend_mock_api.py -d -c {DEV_UTILS_LOCAL_DATA}'

    NEW_REPORT = ROOT_PATH.parent.joinpath('new_report')
    NEW_REPORT_INSTALL_COMMAND = 'npm i'
    NEW_REPORT_RUN_COMMAND = 'npm run dev -- --port 3005'

    TEST_PACKAGE = ROOT_PATH.joinpath('tests')
    PLAYWRIGHT_INSTALL = 'playwright install'
    RUN_TEST_COMMAND = fr'poetry run pytest {TEST_PACKAGE}'
    RUN_TEST_PARAMS = '--base-url {environment_url} --browser-channel chrome ' \
                      '--html={anonymous_key}.html --self-contained-html'
