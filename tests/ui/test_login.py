from page_object.LoginPage import LoginPage
from utils.logger import Logger
import os

user_name = os.getenv("UI_USER_NAME")
password = os.getenv("UI_USER_PASSWORD")


def test_login(driver):
    login_page = LoginPage(driver)

    Logger.step("01", "Open Login Page")
    login_page.load()

    Logger.step("02", "Verify Login Page loaded")
    login_page.verify_page_title()

    Logger.step("03", "Login with default user")
    login_page.login_with_valid_credentials(user_name, password)
    login_page.verify_no_login_error()
