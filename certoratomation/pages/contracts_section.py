import re

from playwright.sync_api import Page, Locator, expect

from certoratomation.pages.common import validate_and_click_button


class ContractsSectionPage:

    def __init__(self, page: Page):
        self.page = page

        self.contracts_tab_button = self.page.get_by_role("tab").filter(has_text="menu_book")
        self.left_section_content = self.page.locator("#one")
        self.contracts_expand_button = self.left_section_content.locator('.q-icon.icon-kindexpandAll')
        self.contracts_collapse_button = self.left_section_content.locator('.q-icon.icon-kindcollapseAll')
        self.contracts_filter_search = self.left_section_content.locator('.filter_search')

    def navigate_base_page(self):
        self.page.goto('/')

    def get_selected_tab_name(self, name: str = None):
        if name:
            expect(self.left_section_content.locator('h6').first).to_contain_text(name, timeout=2000)
        return self.page.inner_text('h6')

    def click_on_contracts_tab(self):
        return validate_and_click_button(self.contracts_tab_button)

    def validate_contracts_tab_is_selected(self):
        return self.validate_tab_is_selected(self.contracts_tab_button)

    @staticmethod
    def validate_tab_is_selected(tab: Locator):
        return tab.get_attribute('aria-selected') == 'true'

    def validate_all_contracts_closed(self):
        return self.validate_all_contracts_closed_or_open(contracts_opened=False)

    def validate_all_contracts_open(self):
        return self.validate_all_contracts_closed_or_open(contracts_opened=True)

    def validate_contracts_first_state(self):
        return self.validate_all_contracts_closed_or_open(contracts_opened=True, first_state=True)

    def validate_all_contracts_closed_or_open(self, contracts_opened: bool, first_state: bool = False):
        output = True
        style_attribute = None if first_state \
            else '' if contracts_opened else 'display: none;'

        contracts = self.left_section_content.locator('.q-expansion-item__content')
        for i in range(contracts.count()):
            output = output and contracts.nth(i).get_attribute("style") == style_attribute
            style_attribute = 'display: none;' if first_state else style_attribute
            first_state = False

        return output

    def get_filter_search_text(self):
        filter_search_text = self.contracts_filter_search.locator('.q-field__native.q-placeholder')
        return filter_search_text.get_attribute('placeholder')

    def get_contract_details_from_contracts_list(self) -> list:
        output = []
        all_contracts = self.left_section_content.locator('.q-card.row')

        for i in range(all_contracts.count()):
            contract_header = all_contracts.nth(i).locator('.q-item__section.column.q-item__section--main')
            output.append([contract_header.locator('span').first.inner_text()])

            all_methods = all_contracts.nth(i).locator('.bg-tras.col.methods_wrapper')
            for j in range(all_methods.count()):
                output[i].append(all_methods.nth(j).inner_text())

        return output

    def get_contract_structure_from_contracts_list(self, contract_index) -> list:
        current_contract = self.left_section_content.locator('.q-card.row').nth(contract_index)

        contract_headers = current_contract.locator('h5')
        return [contract_headers.nth(i).inner_text().strip() for i in range(contract_headers.count())]

    def get_contract_data_from_contracts_list(self, contract_index) -> dict:
        output = {}
        current_contract = self.left_section_content.locator('.q-card.row').nth(contract_index)

        contract_headers = current_contract.locator('h5')
        for i in range(contract_headers.count()):
            match contract_headers.nth(i).inner_text().strip():
                case 'Name':
                    header_name = current_contract.locator('.q-item__section.column.q-item__section--main')
                    output.update({'name': header_name.locator('span').first.inner_text()})
                case 'Contract Links':
                    all_links = current_contract.locator('.q-badge.flex.inline.items-center')
                    output.update({
                        'storageLinks':
                        [all_links.nth(j).inner_text() for j in range(all_links.count())]
                    })
                case 'Methods':
                    all_methods = current_contract.locator('.bg-tras.col.methods_wrapper')
                    output.update({
                        'methods':
                        [all_methods.nth(j).inner_text() for j in range(all_methods.count())]
                    })
                case _:
                    # TODO : Add Failure Mechanism For Unrecognized Cases
                    pass

        return output

    def filter_by_search_text(self, search):
        self.contracts_filter_search.locator('.q-field__native.q-placeholder').fill(search)

    def clear_filter_by_search_text(self):
        return validate_and_click_button(button=self.contracts_filter_search.get_by_text('clear'))

    def click_on_expand_contracts(self):
        return validate_and_click_button(button=self.contracts_expand_button)

    def click_on_collapse_contracts(self):
        return validate_and_click_button(button=self.contracts_collapse_button)
