from selenium.webdriver.common.by import By
from page_object.general_methods.browse_page import BrowsePage
from page_object.ProfilePage import ProfilePage
from utils import verify
from utils.logger import Logger
import os


class LoginPage(BrowsePage):
    url = "login"
    page_title = (By.CSS_SELECTOR, 'h1.text-center')
    login_btn = (By.CSS_SELECTOR, 'button#login')
    register_btn = (By.CSS_SELECTOR, 'button#register')
    new_user_btn = (By.CSS_SELECTOR, 'button#newUser')
    user_name_field = (By.CSS_SELECTOR, 'input#userName')
    psw_field = (By.CSS_SELECTOR, 'input#password')
    firstname_field = (By.CSS_SELECTOR, 'input#firstname')
    lastname_field = (By.CSS_SELECTOR, 'input#lastname')
    login_error_form = (By.CSS_SELECTOR, 'p#name.mb-1')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def load(self):
        self.get_page()

    def verify_page_title(self):
        verify.verify_element_text(self.driver, self.page_title, "Login")

    def click_login_btn(self):
        self.click_btn(self.login_btn)

    def fill_user_name(self, user_name: str):
        self.fill_in_with_value(self.user_name_field, user_name)

    def fill_psw(self, psw: str):
        self.fill_in_with_value(self.psw_field, psw)

    def login_with_valid_credentials(self, user_name, psw):
        self.fill_user_name(user_name)
        self.fill_psw(psw)
        self.click_login_btn()
        try:
            user_name = self.get_element(ProfilePage.search_field)
            Logger.checkpoint(f"User: {user_name.text} is Logged In")
        except:
            Logger.error(f"User is not Logged In", error=Exception)

    def verify_no_login_error(self):
        verify.element_not_exists(self.driver, self.login_error_form, element_name="Invalid username or password!", timeout=0)

    def create_new_user(self, first_name, last_name, usr_name, pwd):
        self.click_btn(self.new_user_btn)
        self.fill_in_with_value(self.firstname_field, first_name)
        self.fill_in_with_value(self.lastname_field, last_name)
        self.fill_user_name(usr_name)
        self.fill_psw(pwd)
        self.click_btn(self.register_btn)
