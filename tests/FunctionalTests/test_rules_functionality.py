import random

import pytest
import re

from certoratomation.pages.common import EXPECTED_STATUS_DROPDOWN_LIST
from certoratomation.pages.rules_section import RulesSectionPage


class TestMainRulesFunctionality:

    @pytest.fixture(autouse=True)
    def setup(self, rules_section_page: RulesSectionPage):
        self.rules_section_page = rules_section_page
        rules_section_page.navigate_base_page()

    def test_expand_collapse_rule(self):
        assert self.rules_section_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.rules_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert self.rules_section_page.validate_all_parent_rules_closed()

        assert self.rules_section_page.click_on_expand_rules()
        assert self.rules_section_page.validate_all_parent_rules_open()

        assert self.rules_section_page.click_on_collapse_rules()
        assert self.rules_section_page.validate_all_parent_rules_closed()

    def test_filter_status_text_display(self):
        assert self.rules_section_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.rules_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        filter_drop_text = self.rules_section_page.get_filter_drop_text()
        assert filter_drop_text == 'All Results'

    def test_filter_search_text_display(self):
        assert self.rules_section_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.rules_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        filter_search_text = self.rules_section_page.get_filter_search_text()
        assert filter_search_text == 'Type to filter'

    def test_validate_all_statuses_in_dropdown(self):
        assert self.rules_section_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.rules_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert self.rules_section_page.click_on_status_dropdown()
        status_dropdown_list = self.rules_section_page.get_status_dropdown_list()

        assert len(EXPECTED_STATUS_DROPDOWN_LIST) == len(status_dropdown_list)

        for status in EXPECTED_STATUS_DROPDOWN_LIST:
            assert status in status_dropdown_list

    def test_validate_appearance_by_filter_multiple_statuses(self):
        assert self.rules_section_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.rules_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert self.rules_section_page.click_on_status_dropdown()
        random_statuses = [status for status in EXPECTED_STATUS_DROPDOWN_LIST if random.randint(0, 1)]

        assert self.rules_section_page.click_on_statuses_from_dropdown(random_statuses)
        assert self.rules_section_page.click_on_status_dropdown()

        actual_status_text = self.rules_section_page.get_selected_statuses_from_dropdown_badge_text()

        for random_status in random_statuses:
            assert f'{random_status}\nclear' in actual_status_text

    def test_validate_clear_status_after_filter(self):
        assert self.rules_section_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.rules_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert self.rules_section_page.click_on_status_dropdown()
        random_statuses = [status for status in EXPECTED_STATUS_DROPDOWN_LIST if random.randint(0, 1)]

        assert self.rules_section_page.click_on_statuses_from_dropdown(random_statuses)
        assert self.rules_section_page.click_on_status_dropdown()

        actual_status_text = self.rules_section_page.get_selected_statuses_from_dropdown_badge_text()

        for random_status in random_statuses:
            assert f'{random_status}\nclear' in actual_status_text

        random_status = random_statuses[random.randint(0, len(random_statuses)-1)]
        assert self.rules_section_page.click_on_clear_selected_status(random_status)

        actual_status_text_after_clear = self.rules_section_page.get_selected_statuses_from_dropdown_badge_text()
        assert f'{random_status}\nclear' not in actual_status_text_after_clear

        # TODO: Add here a validation for rules returning

    def test_validate_clear_all_statuses_after_filter(self):
        assert self.rules_section_page.validate_rules_tab_is_selected(), 'Error! Main Window Should Open On Rules Tab!'
        selected_tab_name = self.rules_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert self.rules_section_page.click_on_status_dropdown()
        random_statuses = [status for status in EXPECTED_STATUS_DROPDOWN_LIST if random.randint(0, 1)]

        assert self.rules_section_page.click_on_statuses_from_dropdown(random_statuses)
        assert self.rules_section_page.click_on_status_dropdown()

        actual_status_text = self.rules_section_page.get_selected_statuses_from_dropdown_badge_text()

        for random_status in random_statuses:
            assert f'{random_status}\nclear' in actual_status_text

        assert self.rules_section_page.click_on_clear_all_selected_status()

        actual_status_text_after_clear = self.rules_section_page.get_selected_statuses_from_dropdown_badge_text()
        assert len(actual_status_text_after_clear) == 0

        # TODO: Add here a validation for rules returning



