from time import sleep

from playwright.sync_api import Locator


def validate_and_click_button(button: Locator, with_wait: bool = False):
    if button.count() != 1:
        return False

    button.click()
    if with_wait:
        sleep(0.5)
    return True


EXPECTED_STATUS_DROPDOWN_LIST = \
            ['Violated', 'Unknown', 'Error', 'Timeout', 'Skipped', 'Verified', 'Running', 'Sanity failed']
