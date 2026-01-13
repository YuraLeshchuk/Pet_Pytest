from page_object.LoginPage import LoginPage
from page_object.EmployeesPage import EmployeesPage
from page_object.EmployeesPage import AddEmployeeModal
from utils.logger import Logger




def test_01_create_user(driver):
    login_page = LoginPage(driver)
    employees_page = EmployeesPage(driver)
    add_employee_modal = AddEmployeeModal(driver)

    photo_path = r"\test_data\duck.jpg"
    file_path = r'\test_data\users.xlsx'

    Logger.step("01", "Open Login Page")
    login_page.load()

    Logger.step("02", "Login with default user")
    login_page.login_with_valid_credentials()
    login_page.verify_no_login_error()

    # Logger.step("03", "Open Employee Page and click Add button")
    # employees_page.load()
    # add_employee_modal.click_add_employee_btn()
    #
    # Logger.step("04", "Fill all fields and click Next")
    # add_employee_modal.load_photo(photo_path)
    # add_employee_modal.crop_photo(0, -40)
    # add_employee_modal.create_user_from_xl(file_path, "users", 1)
