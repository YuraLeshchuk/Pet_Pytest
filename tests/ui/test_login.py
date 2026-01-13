from page_object.LoginPage import LoginPage
from utils.logger import Logger
from config.read_config import Config

user_name = Config.get("user", "user_name")
pwd = Config.get("user", "password")

def test_1(driver):
    login_page = LoginPage(driver)
    assert user_name == "YL1"

    Logger.step("01", "Open Login Page")
    login_page.load()

    Logger.step("02", "Verify Login Page loaded")
    login_page.verify_page_title()

    Logger.step("03", "Login with default user")
    login_page.login_with_valid_credentials(user_name, pwd)
    login_page.verify_no_login_error()
