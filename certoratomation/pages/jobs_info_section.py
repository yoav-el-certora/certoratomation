import re

from playwright.sync_api import Page, Locator, expect

from certoratomation.pages.common import validate_and_click_button


class JobInfoSectionPage:

    def __init__(self, page: Page):
        self.page = page

        self.job_info_tab_button = self.page.get_by_role("tab").filter(has_text="info")
        self.left_section_content = self.page.locator("#one")
        self.job_info_expand_collapse_button = \
            self.left_section_content.locator('.q-list.q-list--bordered').locator(
                '.q-icon.notranslate', has_text='keyboard_arrow_down')
        self.job_info_filter_search = self.left_section_content.locator('.filter_search')

    def navigate_base_page(self):
        self.page.goto('/')

    def get_selected_tab_name(self, name: str = None):
        if name:
            expect(self.left_section_content.locator('h6').first).to_contain_text(name, timeout=2000)
        return self.page.inner_text('h6')

    def click_on_job_info_tab(self):
        return validate_and_click_button(self.job_info_tab_button)

    def validate_job_info_tab_is_selected(self):
        return self.validate_tab_is_selected(self.job_info_tab_button)

    @staticmethod
    def validate_tab_is_selected(tab: Locator):
        return tab.get_attribute('aria-selected') == 'true'

    def validate_job_info_closed(self):
        return self.validate_job_info_closed_or_open(job_info_opened=False)

    def validate_job_info_open(self):
        return self.validate_job_info_closed_or_open(job_info_opened=True)

    def validate_job_info_first_state(self):
        return self.validate_job_info_closed_or_open(job_info_opened=True, first_state=True)

    def validate_job_info_closed_or_open(self, job_info_opened: bool, first_state: bool = False):
        output = True
        style_attribute = None if first_state \
            else '' if job_info_opened \
            else 'display: none;'

        job_info = self.left_section_content.locator('.q-expansion-item__content').first
        output = output and job_info.get_attribute("style") == style_attribute

        return output

    def get_filter_search_text(self):
        filter_search_text = self.job_info_filter_search.locator('.q-field__native.q-placeholder')
        return filter_search_text.get_attribute('placeholder')

    def get_contract_details_from_job_info_list(self) -> list:
        output = []
        all_job_info = self.left_section_content.locator('.q-card.row')

        for i in range(all_job_info.count()):
            contract_header = all_job_info.nth(i).locator('.q-item__section.column.q-item__section--main')
            output.append([contract_header.locator('span').first.inner_text()])

            all_methods = all_job_info.nth(i).locator('.bg-tras.col.methods_wrapper')
            for j in range(all_methods.count()):
                output[i].append(all_methods.nth(j).inner_text())

        return output

    def get_contract_structure_from_job_info_list(self, contract_index) -> list:
        current_contract = self.left_section_content.locator('.q-card.row').nth(contract_index)

        contract_headers = current_contract.locator('h5')
        return [contract_headers.nth(i).inner_text().strip() for i in range(contract_headers.count())]

    def get_contract_data_from_job_info_list(self, contract_index) -> dict:
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
        self.job_info_filter_search.locator('.q-field__native.q-placeholder').fill(search)

    def clear_filter_by_search_text(self):
        return validate_and_click_button(button=self.job_info_filter_search.get_by_text('clear'))

    def click_on_expand_collapse_job_info(self):
        return validate_and_click_button(button=self.job_info_expand_collapse_button, with_wait=True)
