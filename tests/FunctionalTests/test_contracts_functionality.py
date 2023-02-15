import random

import pytest
from certoratomation.pages.contracts_section import ContractsSectionPage


class TestMainRulesFunctionality:

    @pytest.fixture(autouse=True)
    def setup(self, contract_section_page: ContractsSectionPage):
        self.contract_section_page = contract_section_page
        contract_section_page.navigate_base_page()

        assert not self.contract_section_page.validate_contracts_tab_is_selected(),\
            'Error! Main Window Should Not Open On Contracts Tab!'
        selected_tab_name = self.contract_section_page.get_selected_tab_name()
        assert selected_tab_name == 'Rules', 'Error! Main Window Should Open On Rules Tab!'

        assert self.contract_section_page.click_on_contracts_tab()

        assert self.contract_section_page.validate_contracts_tab_is_selected(), \
            'Error! After Clicking On Contracts Tab, Contracts Tab Should Be Selected!'
        selected_tab_name = self.contract_section_page.get_selected_tab_name(name='Contracts')
        assert selected_tab_name == 'Contracts', \
            'Error! After Clicking On Contracts Tab, Header Should Be \"Contracts\"!'

    def test_expand_collapse_contracts(self):
        assert self.contract_section_page.validate_contracts_first_state()

        assert self.contract_section_page.click_on_collapse_contracts()
        assert self.contract_section_page.validate_all_contracts_closed()

        assert self.contract_section_page.click_on_expand_contracts()
        assert self.contract_section_page.validate_all_contracts_open()

        assert self.contract_section_page.click_on_collapse_contracts()
        assert self.contract_section_page.validate_all_contracts_closed()

    def test_filter_search_text_display(self):
        filter_search_text = self.contract_section_page.get_filter_search_text()
        assert filter_search_text == 'Type to filter'

    def test_filter_by_search_text(self):
        nested_contracts_details = self.contract_section_page.get_contract_details_from_contracts_list()

        text_to_filter = []
        for contract_details in nested_contracts_details:
            text_to_filter.extend([details for details in contract_details if random.randint(0, 1)])

        for text in text_to_filter:
            self.contract_section_page.filter_by_search_text(text)
            contracts_details_after_filter = self.contract_section_page.get_contract_details_from_contracts_list()

            for contract_details in contracts_details_after_filter:
                assert any(text in detail for detail in contract_details)

            assert self.contract_section_page.clear_filter_by_search_text()

    def test_validate_contract_section_structure(self, tree_view_status: dict):
        expected_contracts_list = tree_view_status.get('availableContracts')

        for index, expected_contract in enumerate(expected_contracts_list):
            contract_structure = self.contract_section_page.get_contract_structure_from_contracts_list(index)

            assert 'Name' in contract_structure
            assert len(expected_contract.get('storageLinks')) == 0 or 'Contract Links' in contract_structure
            assert 'Methods' in contract_structure

    def test_validate_contract_section_data(self, tree_view_status: dict):
        expected_contracts_list = tree_view_status.get('availableContracts')

        for index, expected_contract in enumerate(expected_contracts_list):
            contract_structure = self.contract_section_page.get_contract_data_from_contracts_list(index)

            assert expected_contract.get('name') == contract_structure.get('name')

            if contract_structure.get('storageLinks'):
                for expected, actual in zip(expected_contract.get('storageLinks'), contract_structure.get('storageLinks')):
                    assert expected == actual

            if contract_structure.get('methods'):
                for expected, actual in zip(expected_contract.get('methods'), contract_structure.get('methods')):
                    assert expected == actual
