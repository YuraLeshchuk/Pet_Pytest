from utils.api_client import APIClient
from utils.logger import Logger
import random


class BooksAPI(APIClient):
    endpoint = "/BookStore/v1/Books"

    def __init__(self, api_client: APIClient):
        self.__dict__ = api_client.__dict__

    def get_books(self):
        response = self.get(self.endpoint).json()
        books = response['books']
        return books

    def get_random_isbn(self):
        book_list = self.get_books()
        index = random.randint(0, len(book_list)-1)
        isbn = book_list[index]['isbn']
        Logger.info(f'ISBN = {isbn}')

        return isbn

    def add_book_to_profile(self, user_id, isbn):
        data = {"userId": user_id,
                "collectionOfIsbns": [
                    {"isbn": isbn}]
                }
        response = self.post(self.endpoint, data)
        return response
