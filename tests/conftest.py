import multiprocessing
from pathlib import Path
import pytest
import json

from playwright.async_api import Page

from certoratomation.pages.common import EXPECTED_STATUS_DROPDOWN_LIST
from certoratomation.pages.contracts_section import ContractsSectionPage
from certoratomation.pages.jobs_info_section import JobInfoSectionPage
from certoratomation.pages.tool_bar import ToolBarPage
from certoratomation.pages.main_screen import MainScreenPage
from certoratomation.pages.rules_section import RulesSectionPage
from certoratomation.server.handlers.run_environment import run_dev_utils, run_new_report

ROOT_PATH = Path(__file__).parent.parent
LOCAL_DATA = ROOT_PATH.joinpath('tests_local_resources/Reports/treeView')
TREE_VIEW_STATUS = LOCAL_DATA.joinpath('treeViewStatus.json')


@pytest.fixture
def tree_view_status(request):
    with open(file=TREE_VIEW_STATUS, mode='r', encoding='utf-8') as f:
        verification_progress = json.load(f)
    return verification_progress.get('verificationProgress')


@pytest.fixture
def tool_bar_page(request, page: Page):
    return ToolBarPage(page=page)


@pytest.fixture
def main_screen_page(request, page: Page):
    return MainScreenPage(page=page)


@pytest.fixture
def rules_section_page(request, page: Page):
    return RulesSectionPage(page=page)


@pytest.fixture
def contract_section_page(request, page: Page):
    return ContractsSectionPage(page=page)


@pytest.fixture
def job_info_section_page(request, page: Page):
    return JobInfoSectionPage(page=page)


@pytest.fixture(params=EXPECTED_STATUS_DROPDOWN_LIST)
def rules_statuses(request):
    return request.param


def run_local_environment():
    run_dev_utils()
    run_new_report()


@pytest.fixture()
def frontend_local_server():
    local_server_process = multiprocessing.Process(
        target=run_local_environment,
        name='certora automation localhost',
        daemon=True
    )

    local_server_process.start()




