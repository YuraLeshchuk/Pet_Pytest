import datetime

from selenium.webdriver.common.by import By
from page_object.general_methods.browse_page import BrowsePage
from utils import verify
from utils import xl_utils
from utils.logger import Logger


class EmployeesPage(BrowsePage):
    url = "/client/#/pim/employees"

    page_title_xpath = (By.XPATH, "//li[contains(@class, 'page-title')]//div")
    add_employee_btn_xpath = (By.XPATH, "//a[@id='addEmployeeButton']")
    loader_xpath = (By.XPATH, "//div[@class='oxd-circle-loader']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def load(self):
        self.get_page()

    def verify_page_title(self):
        verify.verify_element_text(self.driver, self.page_title_xpath, "Employee Management")

    def click_add_employee_btn(self):
        self.click_btn(self.add_employee_btn_xpath, timeout=30)
        self.delay_for_loading()


class AddEmployeeModal(EmployeesPage):
    first_name_field_xpath = (By.XPATH, "//input[@id='first-name-box']")
    middle_name_field_xpath = (By.XPATH, "//input[@id='middle-name-box']")
    last_name_field_xpath = (By.XPATH, "//input[@id='last-name-box']")
    joined_date_field_xpath = (By.XPATH, "//input[@id='joinedDate']")
    location_field_xpath = (By.XPATH, "//div[@id='location']//input")
    photo_frame_xpath = (By.XPATH, "//label[@id='photo-preview-lable']")
    edit_photo_frame_xpath = (By.XPATH, "//img-crop[@id='employeePhotoPreview']//canvas")
    next_btn_xpath = (By.XPATH, "//button[@id='modal-save-button']")
    cancel_btn_xpath = (By.XPATH, "//button[@ng-click='vm.cancel()']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_first_name(self, first_name: str):
        self.fill_in_with_value(self.first_name_field_xpath, first_name)

    def enter_middle_name(self, middle_name: str):
        self.fill_in_with_value(self.middle_name_field_xpath, middle_name)

    def enter_last_name(self, last_name: str):
        self.fill_in_with_value(self.last_name_field_xpath, last_name)

    def enter_joined_date(self, joined_date: str):
        joined_date = datetime.datetime.strptime(str(joined_date), '%Y-%m-%d %H:%M:%S')
        self.fill_in_with_value(self.joined_date_field_xpath, joined_date.strftime('%Y-%m-%d'))

    def enter_location(self, location: str):
        self.get_element(self.location_field_xpath).click()
        self.get_element((By.XPATH, f"//div[@class='custom-dropdown-item-inner-container']"
                                    f"//span[text()='{location}']")).click()

    def click_next_btn(self):
        self.click_btn(self.next_btn_xpath)
        Logger.info("Next button clicked")

    # def load_photo(self, photo_path):
    #     self.get_element(self.photo_frame_xpath).click()
    #     self.load_file(photo_path)

    def crop_photo(self, x, y):
        frame_location = self.get_element(self.edit_photo_frame_xpath).location
        self.set_mouse_cursor(frame_location["x"]+96, frame_location["y"]+235)
        self.click_and_move_mouse_cursor(x, y)

    def create_user_from_xl(self, file, sheet_name, row_id):
        columns = xl_utils.get_column_count(file, sheet_name)
        row_index = xl_utils.get_row_index(file, sheet_name, row_id)
        for i in range(1, columns + 1):
            if xl_utils.read_data(file, sheet_name, 1, i) == "first_name":
                self.enter_first_name(xl_utils.read_data(file, sheet_name, row_index, i))
            elif xl_utils.read_data(file, sheet_name, 1, i) == "middle_name":
                self.enter_middle_name(xl_utils.read_data(file, sheet_name, row_index, i))
            elif xl_utils.read_data(file, sheet_name, 1, i) == "last_name":
                self.enter_last_name(xl_utils.read_data(file, sheet_name, row_index, i))
            elif xl_utils.read_data(file, sheet_name, 1, i) == "joined_date":
                self.enter_joined_date(xl_utils.read_data(file, sheet_name, row_index, i))
            elif xl_utils.read_data(file, sheet_name, 1, i) == "location":
                self.enter_location(xl_utils.read_data(file, sheet_name, row_index, i))

        self.click_next_btn()
