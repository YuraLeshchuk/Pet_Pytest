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
    def load(cls):
        if cls._config is None:
            config = configparser.ConfigParser()

            project_root = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            config_path = os.path.join(project_root, "config", "config.ini")

            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file not found: {config_path}")

            config.read(config_path, encoding="utf-8")
            cls._config = config

        return cls._config

    @classmethod
    def get(cls, section: str, key: str, fallback=None):
        config = cls.load()
        return config.get(section, key, fallback=fallback)