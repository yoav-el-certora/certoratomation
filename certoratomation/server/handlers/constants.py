from pathlib import Path


class HandlersConstants:
    TEMP_PATH = Path('/Users/yoavelmalem/GitRep')
    DEV_UTILS = TEMP_PATH.joinpath('DevUtils/Mac')
    NEW_REPORT = TEMP_PATH.joinpath('new_report')
    TEST_PACKAGE = Path('/Users/yoavelmalem/PycharmProjects/certoratomation/tests')
    DEV_UTILS_INSTALL_COMMAND = 'pip install /Users/yoavelmalem/GitRep/DevUtils/Mac'
    NEW_REPORT_INSTALL_COMMAND = 'npm i'
    DEV_UTILS_RUN_COMMAND = 'python3 frontend_mock_api.py -d -c .'
    NEW_REPORT_RUN_COMMAND = 'npm run dev -- --port 3005'
    PLAYWRIGHT_INSTALL = 'playwright install'
    BASE_URL = r'http://localhost:3005/'
    RUN_TEST_COMMAND = fr'poetry run pytest {TEST_PACKAGE} --base-url {BASE_URL}'
