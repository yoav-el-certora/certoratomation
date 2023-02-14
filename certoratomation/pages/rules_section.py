import re

from playwright.sync_api import Page, Locator, expect

from certoratomation.pages.common import validate_and_click_button


class RulesSectionPage:
    selected_rule: Locator

    def __init__(self, page: Page):
        self.page = page
        self.rules_tab_button = self.page.get_by_role("tab").filter(has_text="checklist")
        self.contracts_tab_button = self.page.get_by_role("tab").filter(has_text="menu_book")
        self.contracts_call_resolution_tab_button = self.page.get_by_role("tab").filter(has_text="mediation")
        self.job_info_tab_button = self.page.get_by_role("tab").filter(has_text="info")

        self.left_section_content = self.page.locator("#one")
        self.status_dropdown_content = self.page.locator("#qvs_1")
        self.rules_expand_button = self.left_section_content.locator('.q-icon.icon-kindexpandAll')
        self.rules_collapse_button = self.left_section_content.locator('.q-icon.icon-kindcollapseAll')
        self.rules_filter_drop = self.left_section_content.locator('.fliter_drop')
        self.rules_filter_search = self.left_section_content.locator('.filter_search')
        self.rules_sort_by_name_button = self.left_section_content.locator('button', has_text='Name')

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

    def validate_rules_tab_is_selected(self):
        return self.validate_tab_is_selected(self.rules_tab_button)

    @staticmethod
    def validate_tab_is_selected(tab: Locator):
        return tab.get_attribute('aria-selected') == 'true'

    def validate_all_parent_rules_closed(self):
        return self.validate_all_parent_rules_closed_or_open(style_attribute='display: none;')

    def validate_all_parent_rules_open(self):
        return self.validate_all_parent_rules_closed_or_open(style_attribute='')

    def validate_all_parent_rules_closed_or_open(self, style_attribute: str):
        output = True
        parent_rules = self.left_section_content.locator('.q-tree__node-collapsible')
        for i in range(parent_rules.count()):
            output = output and parent_rules.nth(i).get_attribute("style") == style_attribute

        return output

    def get_filter_drop_text(self):
        filter_drop_text = self.rules_filter_drop.locator('.q-field__control-container')
        return filter_drop_text.inner_text()

    def get_status_dropdown_list(self):
        all_statuses_from_dropdown = self.status_dropdown_content.locator('.q-item__label')
        return [all_statuses_from_dropdown.nth(i).inner_text() for i in range(all_statuses_from_dropdown.count())]

    def click_on_statuses_from_dropdown(self, statuses: list):
        output = True
        for status in statuses:
            selected_status = self.status_dropdown_content.locator('.q-item__label', has_text=status)
            output = output and validate_and_click_button(button=selected_status)

        return output

    def get_selected_statuses_from_dropdown_badge_text(self) -> list:
        output = []
        selected_statuses = self.left_section_content.locator('.q-badge.flex.inline')

        for i in range(selected_statuses.count()):
            output.append(selected_statuses.nth(i).inner_text())

        return output

    def get_statuses_from_rules_list(self) -> list:
        all_rules = self.left_section_content.locator('.q-tree__node.relative-position.q-tree__node--child')

        all_rules_locators = [all_rules.nth(i).locator('.q-icon.status_icon').first for i in range(all_rules.count())]

        all_rules_icons = [rule_locator.get_attribute('class') for rule_locator in all_rules_locators]

        all_statuses_icons = list(filter(lambda icon: 'kindmesage' not in icon, all_rules_icons))
        all_rules_statuses = [icon.replace('q-icon status_icon icon-kind', '') for icon in all_statuses_icons]
        all_rules_statuses = [status.split('-')[0] for status in all_rules_statuses]

        return all_rules_statuses

    def click_on_clear_selected_statuses(self, statuses: list) -> bool:
        output = True
        for status in statuses:
            selected_status = self.left_section_content.locator('.q-badge.flex.inline', has_text=status)
            output = output and validate_and_click_button(selected_status)

        return output

    def click_on_clear_all_selected_status(self) -> bool:
        selected_status = self.left_section_content.locator('.cursor-pointer.a_decoration', has_text='Clear all')
        return validate_and_click_button(selected_status)

    def get_filter_search_text(self):
        filter_search_text = self.rules_filter_search.locator('.q-field__native.q-placeholder')
        return filter_search_text.get_attribute('placeholder')

    def get_child_rules_names_from_rules_list(self) -> list:
        return self.get_rules_names_from_rules_list(child=True)

    def get_rules_names_from_rules_list(self, child: bool = False) -> list:
        child = '--child' if child else ''
        all_rules = self.left_section_content.locator(f'.q-tree__node.relative-position.q-tree__node{child}')

        def get_rules_name_from_first_inner_text(loc: Locator):
            if loc.count() == 1:
                return loc.locator('.no-margin').inner_text()
            else:
                return loc.first.locator('.no-margin').inner_text()

        all_rules_locators = \
            [all_rules.nth(i).locator('.q-tree__node-header-content') for i in range(all_rules.count())]

        all_rules_names = \
            [get_rules_name_from_first_inner_text(rule_locator) for rule_locator in all_rules_locators]

        return all_rules_names

    def get_rules_tree_from_rules_list(self) -> list:
        all_rules = self.left_section_content.locator('.q-tree__node.relative-position.q-tree__node')

        def get_rules_name_from_first_inner_text(loc: Locator):
            if loc.count() == 1:
                return loc.locator('.no-margin').inner_text()
            else:
                return [get_rules_name_from_first_inner_text(loc.nth(i)) for i in range(loc.count())]

        all_rules_locators = \
            [all_rules.nth(i).locator('.q-tree__node-header-content') for i in range(all_rules.count())]

        all_rules_names = \
            [get_rules_name_from_first_inner_text(rule_locator) for rule_locator in all_rules_locators]

        def balance_rules_tree_recursive(rules_names: list) -> list:
            i = 0
            while i < len(rules_names):
                if type(rules_names[i]) == list:
                    for j in range(len(rules_names[i])-1):
                        if type(rules_names[i+1]) == list:
                            temp = rules_names[i+1]
                            rules_names[i + 1] = rules_names[i][1+j]
                            rules_names[i][1 + j] = temp
                        del rules_names[i+1]
                    balance_rules_tree_recursive(rules_names[i])
                i = i + 1
            return rules_names

        return balance_rules_tree_recursive(all_rules_names)

    def filter_by_search_text(self, search):
        self.rules_filter_search.locator('.q-field__native.q-placeholder').fill(search)

    def clear_filter_by_search_text(self):
        return validate_and_click_button(button=self.rules_filter_search.get_by_text('clear'))

    def click_on_status_dropdown(self):
        return validate_and_click_button(button=self.rules_filter_drop)

    def click_on_expand_rules(self):
        return validate_and_click_button(button=self.rules_expand_button)

    def click_on_collapse_rules(self):
        return validate_and_click_button(button=self.rules_collapse_button)

    def click_on_sort_rules_by_name(self):
        return validate_and_click_button(button=self.rules_sort_by_name_button)
