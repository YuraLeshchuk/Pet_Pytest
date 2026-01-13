import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import Logger, initialize_logger
from utils import globals
from config import read_config
from dotenv import load_dotenv
from utils.api_client import APIClient

# Завантаження змінних середовища
load_dotenv()

# Створюємо унікальну директорію для запуску
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # conftest.py у руті
RUN_TIMESTAMP = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
TEST_RUN_DIR = os.path.join(PROJECT_ROOT, "reports", f"test_run_{RUN_TIMESTAMP}")
os.makedirs(TEST_RUN_DIR, exist_ok=True)


# ==========================================================
#             УТИЛІТА ДЛЯ СТВОРЕННЯ ЛОГУ ТЕСТУ
# ==========================================================
def setup_test_logging(request):
    """
    Створює вкладену структуру директорій:
    reports/test_run_<timestamp>/<test_file>/<test_name>/
    І ініціалізує логування у файлі <test_name>.log
    """
    test_file_name = os.path.splitext(os.path.basename(request.node.fspath))[0]
    test_name = request.node.name

    # 🧩 Директорія для файлу і окремого тесту
    test_file_dir = os.path.join(TEST_RUN_DIR, f"{test_file_name}_{RUN_TIMESTAMP}")
    test_case_dir = os.path.join(test_file_dir, f"{test_name}_{RUN_TIMESTAMP}")

    globals.test_file_dir = test_case_dir
    globals.test_name = test_name

    os.makedirs(test_case_dir, exist_ok=True)

    log_file_name = f"{test_name}_{RUN_TIMESTAMP}.log"
    initialize_logger(log_file_name, test_case_dir)

    logger = Logger.get_global_logger()
    logger.info(f"Starting test: {request.node.nodeid}")

    return logger, test_case_dir



# ==========================================================
#                    UI FIXTURE (WebDriver)
# ==========================================================
@pytest.fixture(scope="function")
def driver(request):
    """Ініціалізація Chrome WebDriver з логуванням."""
    options = webdriver.ChromeOptions()
    if read_config.driver_mode() == "true":
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.base_url = read_config.get_url()

    # Ініціалізація логування через утиліту
    logger, _ = setup_test_logging(request)
    logger.info("Initialized WebDriver")

    yield driver

    logger.info(f"UI test {request.node.nodeid} finished")
    Logger.log_test_summary()
    driver.quit()


# ==========================================================
#                    API FIXTURE (Requests)
# ==========================================================
@pytest.fixture(scope="function")
def api(request):
    """API клієнт, що створює окремий лог-файл для кожного тесту."""
    logger, _ = setup_test_logging(request)
    logger.info("Initialized API client")

    # --- Збір параметрів ---
    user_name = os.getenv("API_user_name") or "default@example.com"
    password = os.getenv("API_PASSWORD") or "password123"
    base_url = os.getenv("BASE_URL") or "https://demoqa.com"

    # --- Ініціалізація API клієнта ---
    client = APIClient(base_url)
    client.login(user_name, password)

    yield client

    logger.info(f"API test {request.node.nodeid} finished")
    Logger.log_test_summary()
    client.close()


# ==========================================================
#                       PYTEST HOOKS
# ==========================================================
def pytest_runtest_teardown(item):
    """Перевіряє, чи були винятки після виконання тесту."""
    if globals.list_exceptions:
        pytest.fail(f"Test failed after execution: {item.name}", pytrace=False)


def pytest_runtest_makereport(item, call):
    """Зберігає скріншоти при падінні UI тестів."""
    if call.when == "call" and call.excinfo is not None:
        if str(call.excinfo.value) != f"Test failed after execution: {item.name}":
            if 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                Logger.save_screenshot(driver)


def pytest_addoption(parser):
    """CLI параметри для API логіну."""
    parser.addoption("--email", action="store", help="User email for login")
    parser.addoption("--password", action="store", help="User password for login")
    parser.addoption("--base-url", action="store", help="Base API URL")
