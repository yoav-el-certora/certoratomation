from playwright.sync_api import Locator


def validate_and_click_button(button: Locator):
    if button.count() != 1:
        return False

    button.click()
    return True


# EXPECTED_STATUS_DROPDOWN_LIST = \
#             ['Violated', 'Verified']

EXPECTED_STATUS_DROPDOWN_LIST = \
            ['Violated', 'Unknown', 'Error', 'Timeout', 'Skipped', 'Verified', 'Running', 'Sanity failed']
