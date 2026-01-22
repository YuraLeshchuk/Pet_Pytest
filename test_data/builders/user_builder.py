from faker import Faker
from test_data.models.users import User
import random
import string

fake = Faker()

GENDERS = ["Male", "Female", "Other"]


class UserBuilder:
    def __init__(self):
        self._first_name = fake.first_name()
        self._last_name = fake.last_name()
        self._gender = random.choice(GENDERS)
        self._phone_number = self._generate_phone_number()
        self._is_registered = False

    def _generate_phone_number(self) -> str:
        return "".join(random.choices(string.digits, k=10))

    def with_gender(self, gender: str):
        if gender not in GENDERS:
            raise ValueError(f"Gender must be one of {GENDERS}")
        self._gender = gender
        return self

    def with_phone_number(self, phone_number: str):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        self._phone_number = phone_number
        return self

    def build(self) -> User:
        return User(
            first_name=self._first_name,
            last_name=self._last_name,
            gender=self._gender,
            phone_number=self._phone_number,
            is_registered=self._is_registered,
        )
