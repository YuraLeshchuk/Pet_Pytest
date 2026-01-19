import os

from selenium.webdriver.common.by import By
from page_object.general_methods.browse_page import BrowsePage
from utils import verify
from utils.logger import Logger
from utils import xl_utils


class PracticeForm(BrowsePage):
    url = "automation-practice-form"
    page_title = (By.CSS_SELECTOR, 'h1.text-center')
    login_btn = (By.CSS_SELECTOR, 'button#login')
    submit_btn = (By.CSS_SELECTOR, 'button#submit')
    close_form_btn = (By.CSS_SELECTOR, 'button#closeLargeModal')
    firstname_field = (By.CSS_SELECTOR, 'input#firstName')
    lastname_field = (By.CSS_SELECTOR, 'input#lastName')
    phone_field = (By.CSS_SELECTOR, 'input#userNumber')
    upload_field = (By.CSS_SELECTOR, 'input#uploadPicture')


    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def load(self):
        self.get_page()

    def verify_page_title(self):
        verify.verify_element_text(self.driver, self.page_title, "Practice Form")

    def click_submit_btn(self):
        self.click_btn(self.submit_btn)

    def select_gender(self, gender: str):
        if not gender.istitle():
            gender.lower()
            gender = gender.capitalize()
        self.click_btn((By.XPATH, f'//input[@value="{gender}"]/..'))

    def create_user_from_xl(self, file, sheet_name, row_id):
        columns = xl_utils.get_column_count(file, sheet_name)
        row_index = xl_utils.get_row_index(file, sheet_name, row_id)
        for i in range(1, columns + 1):
            if xl_utils.read_data(file, sheet_name, 1, i) == "first_name":
                self.fill_in_with_value(self.firstname_field, xl_utils.read_data(file, sheet_name, row_index, i))
            elif xl_utils.read_data(file, sheet_name, 1, i) == "last_name":
                self.fill_in_with_value(self.lastname_field, xl_utils.read_data(file, sheet_name, row_index, i))
            elif xl_utils.read_data(file, sheet_name, 1, i) == "gender":
                self.select_gender(xl_utils.read_data(file, sheet_name, row_index, i))
            elif xl_utils.read_data(file, sheet_name, 1, i) == "phone":
                self.fill_in_with_value(self.phone_field, xl_utils.read_data(file, sheet_name, row_index, i))

        self.click_submit_btn()

    def close_submit_form(self):
        self.click_btn(self.close_form_btn)

    def load_photo(self, photo_path):
        self.scroll_to_element(self.upload_field)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + photo_path
        self.get_element(self.upload_field).send_keys(path)
