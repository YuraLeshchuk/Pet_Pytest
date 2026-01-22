from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    gender: str
    phone_number: str
    is_registered: bool = False
