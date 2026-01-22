import os


class Env:
    @staticmethod
    def ui_user():
        return os.getenv("UI_USER_NAME")

    @staticmethod
    def ui_password():
        return os.getenv("UI_USER_PASSWORD")
