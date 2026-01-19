import os
import time

import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowsePage:
    url = ''
    loader_xpath = (By.XPATH, "//div[@class='oxd-circle-loader']")

    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.web_element = None

    def get_page(self):
        self.driver.get(self.driver.base_url + self.url)

    def get_element(self, locator: tuple[str, str], **kwargs):
        timeout = kwargs.get('timeout', 30)
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        return element

    def get_elements(self, locator: tuple[str, str], **kwargs):
        timeout = kwargs.get('timeout', 5)
        elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        return elements

    def click_btn(self, locator: tuple[str, str], **kwargs):
        timeout = kwargs.get('timeout', 5)
        btn = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        return btn.click()

    def fill_in_with_value(self, field, value, **kwargs):
        timeout = kwargs.get('timeout', 20)
        force_clear = kwargs.get('force_clear', False)
        field_element = self.get_element(field, timeout=timeout)
        self.click_btn(field, timeout=timeout)
        if force_clear:
            field_element.clear()
        field_element.send_keys(value)

    def delay_for_loading(self, **kwargs):
        timeout = kwargs.get('timeout', 20)
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(self.loader_xpath))

    def select(self, element, value):
        return Select(element).select_by_value(value)

    def load_file(self, file_path, **kwargs):
        timeout = kwargs.get('timeout', 2)
        time.sleep(timeout)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + file_path
        pyautogui.write(path)
        pyautogui.press('enter')

    def scroll_to_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        WebDriverWait(self.driver, timeout).until(EC.visibility_of(element))
        return element
