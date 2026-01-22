from page_object.BooksAPI import BooksAPI
from utils.logger import Logger
from utils import verify
import pytest

user_name = "y"
password = "PJR3Q@fM8@BwiKh"

@pytest.mark.parametrize("api", [(user_name, password)], indirect=True)
def test_add_book_to_profile(api):
    books_api = BooksAPI(api)

    # Logger.step('1', 'Login with test user')
    # api.login(user_name, password)

    Logger.step('2', 'Get random ISBN')
    isbn = books_api.get_random_isbn()

    Logger.step('3', 'Add book by ISBN')
    response = books_api.add_book_to_profile('856a9b4e-73e0-4319-838c-58292726903f', isbn)
    verify.verify_string(response.reason, 'Created')
    verify.verify_string(str(response.status_code), '201')
