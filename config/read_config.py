import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "../config/config.ini")
config.read(config_path)


def get_url():
    url = config.get('environment', 'base_url')
    return url


def driver_mode():
    driver_mode = config.get('driver', 'headless')
    return driver_mode

class Config:
    _config = None

    @classmethod
    def load(cls, path="config.ini"):
        if cls._config is None:
            config = configparser.ConfigParser()
            config.read(path, encoding="utf-8")
            cls._config = config
        return cls._config

    @classmethod
    def get(cls, section: str, key: str, fallback=None):
        config = cls.load()
        return config.get(section, key, fallback=fallback)