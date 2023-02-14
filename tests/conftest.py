from pathlib import Path
import pytest
import json

from playwright.async_api import Page

from certoratomation.pages.common import EXPECTED_STATUS_DROPDOWN_LIST
from certoratomation.pages.tool_bar import ToolBarPage
from certoratomation.pages.main_screen import MainScreenPage
from certoratomation.pages.rules_section import RulesSectionPage

TEMP_PATH = Path('/Users/yoavelmalem/GitRep')
TREE_VIEW = TEMP_PATH.joinpath('DevUtils/Mac/Reports/treeView')
TREE_VIEW_STATUS = TREE_VIEW.joinpath('treeViewStatus_10.json')


@pytest.fixture
def tree_view_status(request):
    with open(file=TREE_VIEW_STATUS, mode='r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def tool_bar_page(request, page: Page):
    return ToolBarPage(page=page)


@pytest.fixture
def main_screen_page(request, page: Page):
    return MainScreenPage(page=page)


@pytest.fixture
def rules_section_page(request, page: Page):
    return RulesSectionPage(page=page)


@pytest.fixture(params=EXPECTED_STATUS_DROPDOWN_LIST)
def rules_statuses(request):
    return request.param
