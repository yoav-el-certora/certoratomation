import pytest
import re

from playwright.sync_api import Page

from certoratomation.pages.main_screen import MainScreenPage


class TestMainScreenNavigation:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.main_screen_page = MainScreenPage(page)
        self.main_screen_page.navigate_base_page()

    def test_navigate_to_rules_tab(self, main_screen_page):
        assert self.main_screen_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.main_screen_page.click_on_rules_tab()

        assert self.main_screen_page.validate_rules_tab_is_selected(), \
            'Error! After Clicking On Rules Tab, Rules Tab Should Be Selected!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name(name='Rules')
        assert selected_tab_name == 'Rules', 'Error! After Clicking On Rules Tab, Header Should Be \"Rules\"!'

    def test_navigate_to_rule_dump_page(self):
        assert self.main_screen_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.main_screen_page.click_on_rules_tab()
        self.main_screen_page.click_on_violated_rule_recursive()

        if not self.main_screen_page.validate_dump_page_should_exist():
            pytest.skip('No Dump Page For Current Rule Report')

        self.main_screen_page.click_on_dump_page_button()

        page_url = self.main_screen_page.get_child_page_url()
        assert re.search(r'Report(.*?).html', page_url), \
            'Error! Click On Dump Page Button Should Navigate To Dump Page Containing Report Call!'

    def test_navigate_to_contracts_tab(self):
        assert not self.main_screen_page.validate_contracts_tab_is_selected(), \
            'Error! Main Window Should Not Open On Contracts Tab!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.main_screen_page.click_on_contracts_tab()

        assert self.main_screen_page.validate_contracts_tab_is_selected(), \
            'Error! After Clicking On Contracts Tab, Contracts Tab Should Be Selected!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name(name='Contracts')
        assert selected_tab_name == 'Contracts',\
            'Error! After Clicking On Contracts Tab, Header Should Be \"Contracts\"!'

    def test_show_all_less_contracts_methods(self):
        assert not self.main_screen_page.validate_contracts_tab_is_selected(), \
            'Error! Main Window Should Not Open On Contracts Tab!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.main_screen_page.click_on_contracts_tab()

        assert self.main_screen_page.validate_contracts_tab_is_selected(), \
            'Error! After Clicking On Contracts Tab, Contracts Tab Should Be Selected!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name(name='Contracts')
        assert selected_tab_name == 'Contracts',\
            'Error! After Clicking On Contracts Tab, Header Should Be \"Contracts\"!'

        self.main_screen_page.expand_all_contracts()

        assert self.main_screen_page.validate_show_all_contracts_methods(), \
            'Error! Clicking On Show All Contract Methods Has Failed!'

        assert self.main_screen_page.validate_show_less_contracts_methods(), \
            'Error! Clicking On Show Less Contract Methods Has Failed!'

    def test_navigate_to_contract_call_resolutions_tab(self):
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        if not self.main_screen_page.validate_contracts_call_resolution_tab_button_should_exist():
            pytest.skip('No Contracts Call Resolution Tab Page For Current Rule Report')

        assert not self.main_screen_page.validate_contracts_call_resolution_tab_is_selected(), \
            'Error! Main Window Should Not Open On Contract Call Resolutions Tab!'

        self.main_screen_page.click_on_contracts_call_resolution_tab()

        assert self.main_screen_page.validate_contracts_call_resolution_tab_is_selected(), \
            'Error! After Clicking On Contract Call Resolutions Tab, Contract Call Resolutions Tab Should Be Selected!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name(name='Contracts Call Resolutions')
        assert selected_tab_name.startswith('Contracts Call Resolutions'), \
            'Error! After Clicking On Contracts Call Resolutions Tab, Header Should Be \"Contracts Call Resolutions\"!'

    def test_navigate_to_job_info_tab(self):
        assert not self.main_screen_page.validate_job_info_tab_is_selected(), \
            'Error! Main Window Should Not Open On Job Info Tab!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.main_screen_page.click_on_job_info_tab()

        assert self.main_screen_page.validate_job_info_tab_is_selected(), \
            'Error! After Clicking On Job Info Tab, Job Info Tab Should Be Selected!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name(name='Job Info')
        assert selected_tab_name == 'Job Info', 'Error! After Clicking On Job Info Tab, Header Should Be \"Job Info\"!'

    def test_navigate_to_logs_page_from_job_info(self):
        assert not self.main_screen_page.validate_job_info_tab_is_selected(), \
            'Error! Main Window Should Not Open On Job Info Tab!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.main_screen_page.click_on_job_info_tab()
        assert self.main_screen_page.validate_job_info_tab_is_selected(), \
            'Error! After Clicking On Job Info Tab, Job Info Tab Should Be Selected!'

        if not self.main_screen_page.validate_log_page_button_should_exist():
            pytest.skip('No Logs Page Button For Current Rule Report')

        self.main_screen_page.click_on_logs_page_button()
        page_url = self.main_screen_page.get_child_page_url()
        assert 'Results.txt' in page_url, \
            'Error! Click On Logs Page Button Should Navigate To Logs Page Containing Results!'

    def test_navigate_to_status_page_from_job_info(self):
        assert not self.main_screen_page.validate_job_info_tab_is_selected(), \
            'Error! Main Window Should Not Open On Job Info Tab!'
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        self.main_screen_page.click_on_job_info_tab()
        assert self.main_screen_page.validate_job_info_tab_is_selected(), \
            'Error! After Clicking On Job Info Tab, Job Info Tab Should Be Selected!'

        if not self.main_screen_page.validate_status_page_button_should_exist():
            pytest.skip('No Status Page Button For Current Rule Report')

        self.main_screen_page.click_on_status_page_button()
        page_url = self.main_screen_page.get_child_page_url()
        assert 'jobStatus' in page_url, \
            'Error! Click On Status Page Button Should Navigate To Status Page Containing jobStatus!'

    def test_navigate_to_problem_section(self):
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert not self.main_screen_page.validate_problem_section_is_visible(), \
            'Error! Problems Inner Section Should Not Be Displayed!'

        self.main_screen_page.click_on_problems_section_button()
        assert self.main_screen_page.validate_problem_section_is_visible(wait_for_open=True), \
            'Error! Problems Inner Section Should Be Displayed!'

        self.main_screen_page.click_on_problems_section_button()
        assert not self.main_screen_page.validate_problem_section_is_visible(), \
            'Error! Problems Inner Section Should Not Be Displayed!'

    def test_hide_open_left_section(self):
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width == 30, 'Error! Left Section Size On Main Window Is Invalid!'

        self.main_screen_page.click_on_left_section_close_button()
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width < 15, 'Error! Left Section Should Be Closed!'

        self.main_screen_page.click_on_left_section_open_button()
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width > 15, 'Error! Left Section Should Be Opened!'

    def test_hide_open_right_section(self):
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width == 40, 'Error! Right Section Size On Main Window Is Invalid!'

        self.main_screen_page.close_some_of_right_section(close_all=True)
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width < 1, 'Error! Right Section Should Be Completely Closed!'

        self.main_screen_page.click_on_right_section_open_button()
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width == 40, 'Error! Right Section Size After Open Is Invalid!'

        self.main_screen_page.open_some_of_right_section(open_all=True)
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width > 99, 'Error! Right Section Should Be Completely Opened!'

        self.main_screen_page.click_on_right_section_narrow_button()
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width == 40, 'Error! Right Section Size After Narrow Is Invalid!'

    def test_drag_left_section(self):
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width == 30, 'Error! Left Section Size On Main Window Is Invalid!'

        self.main_screen_page.close_some_of_left_section()
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width < 30, 'Error! Left Section Should Be Narrower!'

        self.main_screen_page.open_some_of_left_section()
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width == 30, 'Error! Left Section Should Be Opened Back!'

        self.main_screen_page.open_some_of_left_section(repeats=5)
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width > 30, 'Error! Left Section Should Be Opened More Than Regular!'

        self.main_screen_page.close_some_of_left_section(close_all=True)
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width < 15, 'Error! Left Section Should Be Completely Closed!'

        self.main_screen_page.open_some_of_left_section(open_all=True)
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width > 15, 'Error! Left Section Should Be Completely Opened!'

        self.main_screen_page.open_some_of_left_section(repeats=50)
        left_section_width = self.main_screen_page.get_left_section_width()
        assert left_section_width < 79, 'Error! Left Section Should Not Be Opened More Than Limit!'

    def test_drag_right_section(self):
        selected_tab_name = self.main_screen_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width == 40, 'Error! Right Section Size On Main Window Is Invalid!'

        self.main_screen_page.close_some_of_right_section()
        right_section_width = self.main_screen_page.get_right_section_width()
        assert 25 < right_section_width < 40, 'Error! Right Section Should Be Narrower!'

        self.main_screen_page.open_some_of_right_section()
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width > 39, 'Error! Right Section Should Be Opened Back!'

        self.main_screen_page.open_some_of_right_section(repeats=5)
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width > 41, 'Error! Right Section Should Be Opened More Than Regular!'

        self.main_screen_page.close_some_of_right_section(close_all=True)
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width < 1, 'Error! Right Section Should Be Completely Closed!'

        self.main_screen_page.open_some_of_right_section(open_all=True)
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width > 39, 'Error! Right Section Should Be Opened Back!'

        self.main_screen_page.open_some_of_right_section(open_all=True)
        right_section_width = self.main_screen_page.get_right_section_width()
        assert right_section_width > 99, 'Error! Right Section Should Be Completely Opened!'

        self.main_screen_page.close_some_of_right_section(close_all=True)
        right_section_width = self.main_screen_page.get_right_section_width()
        assert 35 < right_section_width < 99, 'Error! Right Section Should Be In Middle Position'
