from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_object.general_methods.browse_page import BrowsePage
from utils import verify
from utils.logger import Logger
from utils import globals


class ProfilePage(BrowsePage):
    url = "profile"
    user_name_label = (By.CSS_SELECTOR, 'label#userName-label')
    user_name_value = (By.CSS_SELECTOR, 'label#userName-value')
    log_out = (By.CSS_SELECTOR, '#userName-value + button')
    search_field = (By.CSS_SELECTOR, 'input#searchBox')
    search_btn = (By.CSS_SELECTOR, 'span#basic-addon2')
    book_store_btn = (By.CSS_SELECTOR, 'button#gotoStore')
    del_all_books_btn = (By.XPATH, "//button[contains(text(), 'Delete All Books')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def load(self):
        self.get_page()

    def click_log_out_btn(self):
        self.click_btn(self.log_out)