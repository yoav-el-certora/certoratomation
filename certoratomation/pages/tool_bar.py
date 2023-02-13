from playwright.sync_api import Page, Locator, expect


class ToolBarPage:
    child_page: Page

    def __init__(self, page: Page):
        self.page = page
        self.logo_button = self.page.locator("a:nth-child(1)")
        self.contracts_tab_button = self.page.get_by_role("tab").filter(has_text="menu_book")
        self.discord_button = self.page.locator("a:nth-child(3)")
        self.forum_button = self.page.locator("a:nth-child(4)")
        self.medium_button = self.page.locator("a:nth-child(5)")
        self.mail_button = self.page.locator("a:nth-child(6)")
        self.twitter_button = self.page.locator("a:nth-child(7)")

    def navigate_base_page(self):
        self.page.goto('/')

    def get_toolbar_contract_name(self):
        return self.page.inner_text('h5')

    def get_selected_tab_name(self, name: str = None):
        if name:
            expect(self.page.locator('h6').first).not_to_contain_text(name, timeout=2000)
        return self.page.inner_text('h6')

    def click_on_logo_button(self):
        return self.logo_button.click()

    def click_on_contracts_tab(self):
        return self.contracts_tab_button.click()

    def __click_on_popup_page_button(self, popup_page_button: Locator):
        with self.page.expect_popup() as cp:
            popup_page_button.click()
        self.child_page = cp.value

    def click_on_discord_button(self):
        self.__click_on_popup_page_button(self.discord_button)

    def click_on_forum_button(self):
        self.__click_on_popup_page_button(self.forum_button)

    def click_on_medium_button(self):
        self.__click_on_popup_page_button(self.medium_button)

    def get_mail_button_data(self):
        return self.mail_button.get_attribute('href')

    def click_on_twitter_button(self):
        self.__click_on_popup_page_button(self.twitter_button)

    def get_page_title(self):
        return self.page.title()

    def get_child_page_title(self):
        return self.child_page.title()

    def get_child_page_url(self):
        return self.child_page.url
