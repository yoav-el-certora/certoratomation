import re

from playwright.sync_api import Page, Locator, expect

from certoratomation.data_classes.rules_layout import RuleLayout
from certoratomation.pages.common import validate_and_click_button


class RulesSectionPage:

    def __init__(self, page: Page):
        self.page = page
        self.rules_tab_button = self.page.get_by_role("tab").filter(has_text="checklist")
        self.contracts_tab_button = self.page.get_by_role("tab").filter(has_text="menu_book")
        self.contracts_call_resolution_tab_button = self.page.get_by_role("tab").filter(has_text="mediation")
        self.job_info_tab_button = self.page.get_by_role("tab").filter(has_text="info")

        self.left_section_content = self.page.locator("#one")
        self.middle_section_content = self.page.locator("#two")
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
            expect(selected_status).to_be_visible()
            output = output and validate_and_click_button(button=selected_status)

        return output

    def get_selected_statuses_from_dropdown_badge_text(self) -> list:
        output = []
        selected_statuses = self.left_section_content.locator('.q-badge.flex.inline')

        for i in range(selected_statuses.count()):
            output.append(selected_statuses.nth(i).inner_text())

        return output

    def get_statuses_from_rules_list(self) -> list:
        rules_data = self.get_rules_data_from_rules_list()

        def get_rules_status_from_rules_data(rules_data_inner) -> list:
            rules_statuses = []
            for rule in rules_data_inner:
                rules_statuses.append(rule.rule_status)
                if rule.rule_children:
                    rules_statuses.extend(get_rules_status_from_rules_data(rule.rule_children))
            return rules_statuses

        return get_rules_status_from_rules_data(rules_data)

    def get_statuses_from_child_rules_list(self) -> list:
        rules_data = self.get_rules_data_from_rules_list()

        def get_rules_status_from_rules_data(rules_data_inner) -> list:
            rules_statuses = []
            for rule in rules_data_inner:
                if rule.rule_children:
                    rules_statuses.extend(get_rules_status_from_rules_data(rule.rule_children))
                else:
                    rules_statuses.append(rule.rule_status)
            return rules_statuses

        return get_rules_status_from_rules_data(rules_data)

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

        all_rules_locators = \
            [all_rules.nth(i).locator('.q-tree__node-header-content') for i in range(all_rules.count())]

        all_rules_names = \
            [rule_locator.first.locator('.no-margin').inner_text() for rule_locator in all_rules_locators]

        return all_rules_names

    def get_rules_tree_from_rules_list(self) -> list:
        rules_data = self.get_rules_data_from_rules_list()

        def get_rules_name_from_rules_data(rule: RuleLayout):
            if not rule.rule_children:
                return rule.rule_name
            else:
                output = [rule.rule_name]
                output.extend([get_rules_name_from_rules_data(child_rule) for child_rule in rule.rule_children])
                return output

        return [get_rules_name_from_rules_data(rule) for rule in rules_data]

    def get_rules_data_from_rules_list(self) -> list[RuleLayout]:
        all_rules = self.left_section_content.locator('.q-tree__node.relative-position.q-tree__node')

        def get_rules_data_recursive(loc: Locator) -> RuleLayout:
            rule_status = loc.locator('.q-icon.status_icon').first.get_attribute('class')
            rule_status = rule_status.replace('q-icon status_icon icon-kind', '').split('-')[0]

            rule_runtime = loc.locator('.inline.q-ml-xs').first.inner_text()
            rule_runtime = re.search(r'\d+', rule_runtime).group(0)

            inner_loc = loc.locator('.q-tree__node.relative-position.q-tree__node')

            return RuleLayout(
                rule_status=rule_status,
                rule_name=loc.locator('.no-margin').first.inner_text(),
                rule_runtime=rule_runtime,
                rule_children=[get_rules_data_recursive(inner_loc.nth(i)) for i in range(inner_loc.count())]
            )

        all_rules_data = \
            [get_rules_data_recursive(all_rules.nth(i)) for i in range(all_rules.count())]

        def balance_rules_tree_recursive(rules_data: list[RuleLayout]) -> list[RuleLayout]:
            i = 0
            while i < len(rules_data):
                for j in range(len(rules_data[i].rule_children)):
                    del rules_data[i + 1]
                balance_rules_tree_recursive(rules_data[i].rule_children)
                i = i + 1
            return rules_data

        return balance_rules_tree_recursive(all_rules_data)

    def filter_by_search_text(self, search):
        self.rules_filter_search.locator('.q-field__native.q-placeholder').fill(search)

    def clear_filter_by_search_text(self):
        return validate_and_click_button(button=self.rules_filter_search.get_by_text('clear'))

    def validate_rule_is_selected(self):
        output = True
        all_rules = self.left_section_content.locator('.q-tree__node.relative-position.q-tree__node')
        for i in range(all_rules.count()):
            rule = all_rules.nth(i)

            rule_header = rule.locator('.q-tree__node-header.relative-position').first.get_attribute('class')
            output = output and validate_and_click_button(button=rule)

            if 'child' in rule.get_attribute('class') and 'q-focusable' in rule_header:
                rule_header_focusable = \
                    rule.locator('.q-tree__node-header.relative-position').first.get_attribute('class')
                output = output and 'q-tree__node--selected' in rule_header_focusable

        return output

    def validate_rule_selected_path_on_top_screen(self):
        output = True
        all_rules = self.left_section_content.locator('.q-tree__node.relative-position.q-tree__node')

        def validate_rule_path_recursive(loc: Locator, prefix: str = ''):
            rule_path_validated = True
            is_rule_child = 'child' in rule.get_attribute('class')
            rule_header = loc.locator('.q-tree__node-header.relative-position').first.get_attribute('class')

            rule_path_validated = rule_path_validated and validate_and_click_button(button=loc.first)

            rule_name = loc.locator('.q-tree__node-header-content').locator('.no-margin').first.inner_text()

            if is_rule_child and 'q-focusable' in rule_header:
                selected_path = ''
                selected_path_locators = \
                    self.middle_section_content.locator('.crumbs_wrapper.row').locator('.row.items-center'
                                                                                       )
                for k in range(selected_path_locators.count()):
                    selected_path = selected_path + selected_path_locators.nth(k).inner_text()

                selected_path = selected_path.replace('\n', ' ')
                selected_path = re.sub(' +', ' ', selected_path)

                rule_path_validated = rule_path_validated and f'{prefix}{rule_name}' in selected_path

            elif 'q-focusable' in rule_header:
                inner_loc = loc.locator('.q-tree__node.relative-position.q-tree__node')
                for j in range(inner_loc.count()):
                    expected_rule_path = f'{prefix}{rule_name} chevron_right '
                    rule_path_validated = rule_path_validated \
                        and validate_rule_path_recursive(inner_loc.nth(j), expected_rule_path)

            return rule_path_validated

        for i in range(all_rules.count()):
            rule = all_rules.nth(i)
            output = output and validate_rule_path_recursive(rule)

        return output

    def validate_dump_page_button_existence(self):
        output = True
        all_rules = self.left_section_content.locator('.q-tree__node.relative-position.q-tree__node')

        for i in range(all_rules.count()):
            rule = all_rules.nth(i)
            is_rule_child = 'child' in rule.get_attribute('class')
            is_rule_header = \
                'q-focusable' in rule.locator('.q-tree__node-header.relative-position').first.get_attribute('class')

            output = output and validate_and_click_button(button=rule.first)

            if is_rule_child and is_rule_header:
                dump_page_button = \
                    self.middle_section_content.locator('button >> [class="q-icon icon-kindbyteCode"]')

                rule_status = rule.locator('.q-icon.status_icon').first.get_attribute('class')
                rule_status = rule_status.replace('q-icon status_icon icon-kind', '').split('-')[0]

                if rule_status.lower() == 'violated':
                    output = output and dump_page_button.count() == 1
                else:
                    output = output and dump_page_button.count() == 0

        return output

    def click_on_status_dropdown(self):
        output = validate_and_click_button(button=self.rules_filter_drop, with_wait=True)
        return output

    def click_on_expand_rules(self):
        return validate_and_click_button(button=self.rules_expand_button, with_wait=True)

    def click_on_collapse_rules(self):
        return validate_and_click_button(button=self.rules_collapse_button, with_wait=True)

    def click_on_sort_rules_by_name(self):
        return validate_and_click_button(button=self.rules_sort_by_name_button)
