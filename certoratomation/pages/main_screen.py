import re

from playwright.sync_api import Page, Locator, expect


class MainScreenPage:
    child_page: Page

    def __init__(self, page: Page):
        self.page = page
        self.rules_tab_button = self.page.get_by_role("tab").filter(has_text="checklist")
        self.contracts_tab_button = self.page.get_by_role("tab").filter(has_text="menu_book")
        self.contracts_call_resolution_tab_button = self.page.get_by_role("tab").filter(has_text="mediation")
        self.job_info_tab_button = self.page.get_by_role("tab").filter(has_text="info")

        self.dump_page_button = self.page.locator('button >> [class="q-icon icon-kindbyteCode"]')
        self.status_page_button = self.page.locator('button >> [class="q-icon icon-kindjson"]')
        self.logs_page_button = self.page.locator('button >> [class="q-icon icon-kindlog"]')
        self.problems_section_button = self.page.locator(".q-item__section").get_by_text("keyboard_arrow_down")
        self.problems_section_content = self.page.locator(".q-expansion-item__content.relative-position")

        self.left_section_close_button = self.page.locator(".q-btn__content").get_by_text("chevron_left")
        self.left_section_open_button = self.page.locator(".q-btn__content").get_by_text("chevron_right")
        self.left_section_content = self.page.locator("#one")
        self.left_section_gutter = self.page.locator("#gutter_main")

        self.right_section_open_button = self.page.locator("#inner_gutter_btn").get_by_text("keyboard_arrow_left")
        self.right_section_narrow_button = self.page.locator("#inner_gutter_btn").get_by_text("keyboard_arrow_right")
        self.right_section_content = self.page.locator("#call_two")
        self.right_section_gutter = self.page.locator("#gutter_inner")

    def navigate_base_page(self):
        self.page.goto('/')

    def get_selected_tab_name(self, name: str = None):
        if name:
            expect(self.left_section_content.locator('h6').first).to_contain_text(name, timeout=2000)
        return self.page.inner_text('h6')

    def click_on_rules_tab(self):
        self.rules_tab_button.click()

    def click_on_contracts_tab(self):
        self.contracts_tab_button.click()

    def click_on_contracts_call_resolution_tab(self):
        self.contracts_call_resolution_tab_button.click()

    def click_on_job_info_tab(self):
        self.job_info_tab_button.click()

    def click_on_violated_rule_recursive(self):
        violated_rules = self.left_section_content.locator('.q-icon.status_icon.icon-kindViolated')
        if violated_rules.count() > 0:
            i = 0
            while self.dump_page_button.count() == 0:
                violated_rules.nth(i).click()
                i += 1

    def expand_all_contracts(self):
        contracts_table_list = self.left_section_content.locator('.column.no-wrap').locator(".q-card")
        for i in range(contracts_table_list.count()):
            current_contract = contracts_table_list.nth(i)
            if current_contract.locator(".q-expansion-item__content").get_attribute("style") == 'display: none;':
                current_contract.click()

    def validate_show_all_contracts_methods(self):
        comparator = (lambda new, old: new >= old)
        return self.validate_show_all_less_contracts_methods('Show all', 'Show less', comparator)

    def validate_show_less_contracts_methods(self):
        comparator = (lambda new, old: new <= old)
        return self.validate_show_all_less_contracts_methods('Show less', 'Show all', comparator)

    def validate_show_all_less_contracts_methods(self, current_text: str, new_text: str, comparator):
        output = True
        contracts_table_list = self.left_section_content.locator('.column.no-wrap').locator(".q-card")
        for i in range(contracts_table_list.count()):
            current_contract = contracts_table_list.nth(i)

            text_locator = current_contract.locator('.text-primary')
            if text_locator.count() and current_text in text_locator.inner_text():
                column_style = current_contract.locator('.column.contract_list_expand').get_attribute('style')
                current_column_height = re.search(r' (.*?)px', column_style).group(1)
                current_contract.locator('.text-primary').click()

                expect(text_locator).to_contain_text(new_text)
                column_style = current_contract.locator('.column.contract_list_expand').get_attribute('style')
                new_column_height = re.search(r' (.*?)px', column_style).group(1)

                output = output and comparator(int(new_column_height), int(current_column_height))

        return output

    def validate_rules_tab_is_selected(self):
        return self.validate_tab_is_selected(self.rules_tab_button)

    def validate_contracts_tab_is_selected(self):
        return self.validate_tab_is_selected(self.contracts_tab_button)

    def validate_contracts_call_resolution_tab_is_selected(self):
        return self.validate_tab_is_selected(self.contracts_call_resolution_tab_button)

    def validate_job_info_tab_is_selected(self):
        return self.validate_tab_is_selected(self.job_info_tab_button)

    @staticmethod
    def validate_tab_is_selected(tab: Locator):
        return tab.get_attribute('aria-selected') == 'true'

    def __click_on_popup_page_button(self, popup_page_button: Locator):
        with self.page.expect_popup() as cp:
            popup_page_button.click()
        self.child_page = cp.value

    def click_on_dump_page_button(self):
        self.__click_on_popup_page_button(self.dump_page_button)

    def click_on_logs_page_button(self):
        self.__click_on_popup_page_button(self.logs_page_button)

    def click_on_status_page_button(self):
        self.__click_on_popup_page_button(self.status_page_button)

    def click_on_problems_section_button(self):
        self.problems_section_button.click()

    def validate_problem_section_is_visible(self, wait_for_open: bool = False):
        value_expected = '' if wait_for_open else 'display: none;'
        expect(self.problems_section_content).to_have_attribute('style', value_expected)

        return self.problems_section_content.get_attribute('style') != 'display: none;'

    def click_on_left_section_close_button(self):
        return self.left_section_close_button.click()

    def click_on_left_section_open_button(self):
        return self.left_section_open_button.click()

    def get_left_section_width(self):
        return self.__get_section_width(self.left_section_content)

    def get_right_section_width(self):
        return self.__get_section_width(self.right_section_content)

    def click_on_right_section_narrow_button(self):
        return self.right_section_narrow_button.click()

    def click_on_right_section_open_button(self):
        return self.right_section_open_button.click()

    @staticmethod
    def __get_section_width(section_content: Locator):
        left_section_style = section_content.get_attribute('style')
        left_section_width = re.search(r'\((.*?)%', left_section_style).group(1)
        return float(left_section_width)

    def close_some_of_left_section(self, close_all: bool = False):
        x_coordinate = -100 if close_all else -5
        self.drag_section_to_open_or_close(section=self.left_section_gutter, x_coordinate=x_coordinate, y_coordinate=0)

    def open_some_of_left_section(self, repeats: int = 1, open_all: bool = False):
        x_coordinate = 334 if open_all else 11 * repeats
        self.drag_section_to_open_or_close(section=self.left_section_gutter, x_coordinate=x_coordinate, y_coordinate=0)

    def close_some_of_right_section(self, repeats: int = 1, close_all: bool = False):
        x_coordinate = 334 if close_all else 28 * repeats
        self.drag_section_to_open_or_close(section=self.right_section_gutter, x_coordinate=x_coordinate, y_coordinate=0)

    def open_some_of_right_section(self, repeats: int = 1, open_all: bool = False):
        x_coordinate = -350 if open_all else -22 * repeats
        self.drag_section_to_open_or_close(section=self.right_section_gutter, x_coordinate=x_coordinate, y_coordinate=0)

    @staticmethod
    def drag_section_to_open_or_close(section: Locator, x_coordinate: float, y_coordinate: float):
        target = {
            'x': x_coordinate,
            'y': y_coordinate
        }
        section.drag_to(force=True, target=section, target_position=target)

    def get_child_page_url(self):
        return self.child_page.url

    def validate_dump_page_should_exist(self):
        violated_rules = self.left_section_content.locator('.q-icon.status_icon.icon-kindViolated')
        return violated_rules.count() > 0

    def validate_contracts_call_resolution_tab_button_should_exist(self):
        return self.contracts_call_resolution_tab_button.count() > 0

    def validate_log_page_button_should_exist(self):
        return self.logs_page_button.count() > 0

    def validate_status_page_button_should_exist(self):
        return self.status_page_button.count() > 0

