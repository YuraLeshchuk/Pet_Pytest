import logging
import os

_global_logger = None

def initialize_logger(log_file_name: str, test_file_dir: str):
    """
    Ініціалізація глобального логера.
    """
    global _global_logger
    if not os.path.exists(test_file_dir):
        os.makedirs(test_file_dir)

    _global_logger = logging.getLogger("GlobalLogger")
    _global_logger.setLevel(logging.DEBUG)

    # Видаляємо старі хендлери
    if _global_logger.handlers:
        for handler in _global_logger.handlers:
            _global_logger.removeHandler(handler)

    # Додавання FileHandler
    log_file = os.path.join(test_file_dir, log_file_name)
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    _global_logger.addHandler(file_handler)

class Logger:
    @staticmethod
    def get_global_logger() -> logging.Logger:
        if _global_logger is None:
            raise ValueError("Global Logger is not initialized.")
        return _global_logger

    @staticmethod
    def step(step_number: str, description: str):
        """
        Логування кроку тесту у форматі:
        STEP [номер]: опис
        """
        if _global_logger:
            msg = f"STEP {step_number}: {description}"
            _global_logger.info(msg)
        else:
            raise ValueError("Global Logger is not initialized.")

    @staticmethod
    def save_screenshot(driver, test_file_dir, screenshot_name):
        screenshot_path = os.path.join(test_file_dir, screenshot_name)
        driver.save_screenshot(screenshot_path)
        _global_logger.info(f"Screenshot saved at: {screenshot_path}")
