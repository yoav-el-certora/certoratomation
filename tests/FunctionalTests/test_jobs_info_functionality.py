import random

import pytest
from certoratomation.pages.jobs_info_section import JobInfoSectionPage


class TestContractsFunctionality:

    @pytest.fixture(autouse=True)
    def setup(self, job_info_section_page: JobInfoSectionPage):
        self.job_info_section_page = job_info_section_page
        job_info_section_page.navigate_base_page()

        assert not self.job_info_section_page.validate_job_info_tab_is_selected(),\
            'Error! Main Window Should Not Open On Job Info Tab!'
        selected_tab_name = self.job_info_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert self.job_info_section_page.click_on_job_info_tab()

        assert self.job_info_section_page.validate_job_info_tab_is_selected(), \
            'Error! After Clicking On Job Info Tab, Job Info Tab Should Be Selected!'
        selected_tab_name = self.job_info_section_page.get_selected_tab_name(name='Job Info')
        assert selected_tab_name == 'Job Info', \
            'Error! After Clicking On Job Info Tab, Header Should Be \"Job Info\"!'

    def test_expand_collapse_job_info(self):
        assert self.job_info_section_page.validate_job_info_first_state()

        assert self.job_info_section_page.click_on_expand_collapse_job_info()
        assert self.job_info_section_page.validate_job_info_closed()

        assert self.job_info_section_page.click_on_expand_collapse_job_info()
        assert self.job_info_section_page.validate_job_info_open()

        assert self.job_info_section_page.click_on_expand_collapse_job_info()
        assert self.job_info_section_page.validate_job_info_closed()

    def test_filter_search_text_display(self):
        filter_search_text = self.job_info_section_page.get_filter_search_text()
        assert filter_search_text == 'Type to filter'

    def test_filter_by_search_text(self):
        nested_contracts_details = self.job_info_section_page.get_contract_details_from_contracts_list()

        text_to_filter = []
        for contract_details in nested_contracts_details:
            text_to_filter.extend([details for details in contract_details if random.randint(0, 1)])

        for text in text_to_filter:
            self.job_info_section_page.filter_by_search_text(text)
            contracts_details_after_filter = self.job_info_section_page.get_contract_details_from_contracts_list()

            for contract_details in contracts_details_after_filter:
                assert any(text in detail for detail in contract_details)

            assert self.job_info_section_page.clear_filter_by_search_text()

    def test_validate_contract_section_structure(self, tree_view_status: dict):
        expected_contracts_list = tree_view_status.get('availableContracts')

        for index, expected_contract in enumerate(expected_contracts_list):
            contract_structure = self.job_info_section_page.get_contract_structure_from_contracts_list(index)

            assert 'Name' in contract_structure
            assert len(expected_contract.get('storageLinks')) == 0 or 'Contract Links' in contract_structure
            assert 'Methods' in contract_structure

    def test_validate_contract_section_data(self, tree_view_status: dict):
        expected_contracts_list = tree_view_status.get('availableContracts')

        for index, expected_contract in enumerate(expected_contracts_list):
            contract_structure = self.job_info_section_page.get_contract_data_from_contracts_list(index)

            assert expected_contract.get('name') == contract_structure.get('name')

            if contract_structure.get('storageLinks'):
                for expected, actual in zip(expected_contract.get('storageLinks'), contract_structure.get('storageLinks')):
                    assert expected == actual

            if contract_structure.get('methods'):
                for expected, actual in zip(expected_contract.get('methods'), contract_structure.get('methods')):
                    assert expected == actual
