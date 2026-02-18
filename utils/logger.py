import logging
import os
from datetime import datetime

from utils import globals

_global_logger = None


def initialize_logger(log_file_name: str, test_file_dir: str):
    global _global_logger
    if not os.path.exists(test_file_dir):
        os.makedirs(test_file_dir)

    _global_logger = logging.getLogger("LOGGER")
    _global_logger.setLevel(logging.INFO)

    if _global_logger.handlers:
        for handler in _global_logger.handlers:
            _global_logger.removeHandler(handler)

    log_file = os.path.join(test_file_dir, log_file_name)
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    _global_logger.addHandler(file_handler)


class Logger:
    @staticmethod
    def get_global_logger() -> logging.Logger:
        if _global_logger is None:
            raise ValueError("Logger is not initialized.")
        return _global_logger

    @staticmethod
    def save_screenshot(driver):
        if not globals.test_file_dir or not globals.test_name:
            _global_logger.error("test_file_dir or test_name is not set in globals.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_name = f"{globals.test_name}_{timestamp}.png"
        screenshot_path = os.path.join(globals.test_file_dir, screenshot_name)

        _global_logger.info(f"Attempting to save screenshot to: {screenshot_path}")
        try:
            driver.save_screenshot(screenshot_path)
            _global_logger.info(f"Screenshot saved at: {screenshot_path}")
        except Exception as e:
            _global_logger.error(f"Failed to save screenshot: {e}")

    @staticmethod
    def step(step_number: str, description: str):
        if _global_logger:
            msg = f"STEP {step_number}: {description}"
            _global_logger.info(msg)
        else:
            raise ValueError("Logger is not initialized.")

    @staticmethod
    def checkpoint(msg):
        if _global_logger:
            globals.int_total_checkpoints += 1
            msg = f"CHECKPOINT {globals.int_total_checkpoints}: {msg}"
            _global_logger.info(msg)
        else:
            raise ValueError("Logger is not initialized.")

    @staticmethod
    def error(msg, error):
        if _global_logger:
            _global_logger.error(msg)
            raise error
        else:
            raise ValueError("Logger is not initialized.")

    @staticmethod
    def info(msg):
        if _global_logger:
            _global_logger.info(msg)
        else:
            raise ValueError("Logger is not initialized.")

    @staticmethod
    def exception(driver=None, msg: str = ""):
        if _global_logger:
            _global_logger.error(msg)
            globals.list_exceptions.append(msg)

            if driver:
                Logger.save_screenshot(driver)
        else:
            raise ValueError("Logger is not initialized.")

    @staticmethod
    def log_test_summary():
        _global_logger.info("*******************************************************")
        _global_logger.info("**************** TEST SCENARIO SUMMARY ****************")
        _global_logger.info("*******************************************************")
        _global_logger.info(f"    TOTAL CHECKPOINTS: {len(globals.list_checkpoints)}")
        _global_logger.info(f"    TOTAL WARNINGS: {len(globals.list_warnings)}")
        _global_logger.info(f"    TOTAL EXCEPTIONS: {len(globals.list_exceptions)}")
