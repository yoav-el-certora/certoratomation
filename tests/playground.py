# import json
# from pathlib import Path
#
# from playwright.sync_api import Page, expect
# import pytest
#
#
# TEMP_PATH = Path('/Users/yoavelmalem/GitRep')
# TREE_VIEW = TEMP_PATH.joinpath('DevUtils/Mac/Reports/treeView')
# TREE_VIEW_STATUS = TREE_VIEW.joinpath('treeViewStatus_0.json')
#
#
# def test_title_name(page: Page):
#     page.goto("https://vaas-stg.certora.com/output/99668/df7cc88dc08f4f58a430b4c6f68a95f3/?anonymousKey=28c1c693bd38374e2ba1a9055877b93819e8d667")
#     x = page.locator('#one > div > div > div.q-splitter__panel.q-splitter__after.col > div > div.q-tab-panels.q-panel-parent.full-height > div > div > div > div.q-scrollarea.main_tree > div.q-scrollarea__container.scroll.relative-position.fit.hide-scrollbar > div > div > div > div')
#     e = x.count()
#     for i in range(e):
#         z = x.nth(i)
#         zz = z.inner_text().strip()
#         expect(z.nth(i)).to_contain_text('envfree')
#         # expect(z.nth(i)).to_have_text('chevron_right\\n\\nenvfreeFuncsStaticCheck\\n\\n0s')
#         print(z.inner_text())
#
#     y = 5
#     #
#     # page.click('button:is(:text("Login"))')
#     # # page.get_by_text("Login").click()
#     # print(page.title())
#     # # page.wait_for_selector("h1[List of jobs]")
#     # # page.wait_for_selector("div[data-target=directory-first-item]")
#     # assert page.inner_text('h1') == 'List of jobs', 'wrong page'
#     # assert page.title() == 'Home page', 'wrong page'
#
#
# def test_rules_list(page: Page):
#     with open(file=TREE_VIEW_STATUS, mode='r', encoding='utf-8') as f:
#         tree_view_status = json.load(f)
#     rules_names = [rule.get('name') for rule in tree_view_status.get('rules')]
#     # rules_names.append('This Will Fail')
#
#     page.goto("/")
#     page.click('i:is(:text("checklist"))')
#
#     for rule_name in rules_names:
#         try:
#             page.get_by_role("paragraph").filter(has_text=rule_name).click()
#         except Exception as e:
#             raise AssertionError(f'Could Not Find Rule Named: {rule_name}')
#
import pytest


#
# def test_title_name(page: Page):
#     page.goto("https://prover.certora.com/")
#     page.locator('input[name=certoraKey]').fill("217e762e7e6dee60367fec88bf140ccc40288884")
#     page.click('button:is(:text("Login"))')
#     print(page.title())
#     assert page.inner_text('h1') == 'List of jobs', 'wrong page'
#     assert page.title() == 'Home page', 'wrong page'
#
#
# def test_rules_list(page: Page, tree_view_status):
#     rules_names = [rule.get('name') for rule in tree_view_status.get('rules')]
#     page.goto("/")
#     page.click('i:is(:text("checklist"))')
#
#     for rule_name in rules_names:
#         try:
#             page.get_by_role("paragraph").filter(has_text=rule_name).click()
#         except Exception as e:
#             raise AssertionError(f'Could Not Find Rule Named: {rule_name}')
#
#
# def test_first_header(page: Page, tree_view_status):
#     contract_name = tree_view_status.get('contract')
#     page.goto("/")
#     page.click('i:is(:text("menu_book"))')
#     assert page.inner_text('h5') == contract_name, 'Main Contract Name Is Incorrect!'

#
# class TestClass:
#     @classmethod
#     def setup_class(cls):
#         print("starting class: {} execution".format(cls.__name__))
#
#     @classmethod
#     def teardown_class(cls):
#        print("starting class: {} execution".format(cls.__name__))
#
#     def setup_method(self, method):
#         print("starting execution of tc: {}".format(method.__name__))
#
#     def teardown_method(self, method):
#         print("Finish execution of tc: {}".format(method.__name__))
#
#     def test_tc1(self):
#         print('TEST1')
#         assert True
#
#     def test_tc2(self):
#         print('TEST2')
#         assert False

# self.page.goto('/')
# self.page.locator('input[name=certoraKey]').fill("217e762e7e6dee60367fec88bf140ccc40288884")
# self.page.click('button:is(:text("Login"))')
# self.page.goto('https://vaas-stg.certora.com/output/99668/df7cc88dc08f4f58a430b4c6f68a95f3/?anonymousKey=28c1c693bd38374e2ba1a9055877b93819e8d667')


class TestClass:
    @pytest.fixture(autouse=True)
    def setup(self, main_screen_page):
        print('setup')
        x = 5
        self.x = main_screen_page
        main_screen_page.navigate_base_page()

    def test_two(self):
        self.x.navigate_base_page()
        print('two')

    def test_three(self):
        print('three')


EXPECTED_STATUS_DROPDOWN_LIST = \
            ['Violated', 'Unknown', 'Error', 'Timeout', 'Skipped', 'Verified', 'Running', 'Sanity failed']


@pytest.fixture(params=EXPECTED_STATUS_DROPDOWN_LIST)
def statuses(request):
    return request.param


def test_two(statuses):
    print(statuses)
