from page_object.PracticeForm import PracticeForm
from utils.logger import Logger

xl_file = r'\test_data\users.xlsx'
photo_path = r"\test_data\duck.jpg"

def test_01_register_user(driver):
    practice_form = PracticeForm(driver)

    Logger.step("01", "Open Practice Form")
    practice_form.load()

    Logger.step("02", "Login with default user")
    practice_form.load_photo(photo_path)
    practice_form.create_user_from_xl(xl_file, 'users', 1)
    practice_form.close_submit_form()
