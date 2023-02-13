import pytest
from playwright.sync_api import Page

from certoratomation.pages.tool_bar import ToolBarPage


class TestToolBarNavigation:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.tool_bar_page = ToolBarPage(page)
        self.tool_bar_page.navigate_base_page()

    def test_contract_name_validation(self, tree_view_status):
        contract_name = tree_view_status.get('contract')
        tool_bar_contract_name = self.tool_bar_page.get_toolbar_contract_name()
        assert tool_bar_contract_name == contract_name, 'Error! Main Contract Name Is Incorrect!'

    def test_logo_button(self):
        selected_tab_name = self.tool_bar_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.tool_bar_page.click_on_contracts_tab()
        selected_tab_name = self.tool_bar_page.get_selected_tab_name(name='Rules')
        assert selected_tab_name != 'Rules', 'Error! After Clicking On Different Tab, Header Should Not Be \"Rules\"!'

        self.tool_bar_page.click_on_logo_button()
        selected_tab_name = self.tool_bar_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! After Clicking On Rules Tab, Header Should Be \"Rules\"!'

    def test_discord_button(self):
        self.tool_bar_page.click_on_discord_button()

        page_url = self.tool_bar_page.get_child_page_url()
        assert 'discord.com' in page_url, \
            'Error! Click On Discord Page Should Navigate To Discord!'

    def test_forum_button(self):
        self.tool_bar_page.click_on_forum_button()

        page_url = self.tool_bar_page.get_child_page_url()
        assert page_url == 'https://forum.certora.com/', \
            'Error! Click On Forum Page Should Navigate To Certora Forum!'

    def test_medium_button(self):
        self.tool_bar_page.click_on_medium_button()

        page_url = self.tool_bar_page.get_child_page_title()
        assert page_url == 'Certora – Medium', \
            'Error! Click On Medium Page Should Navigate To Certora Medium!'

    def test_mail_button(self):
        mail_button_data = self.tool_bar_page.get_mail_button_data()
        assert mail_button_data == 'mailto:support@certora.com?subject=Demo', \
            'Error! Click On Mail Page Should Open New Mail To Certora!'

    def test_twitter_button(self):
        self.tool_bar_page.click_on_twitter_button()

        page_url = self.tool_bar_page.get_child_page_url()
        assert 'twitter.com' in page_url, \
            'Error! Click On Twitter Page Should Navigate To Certora Twitter Page!'
