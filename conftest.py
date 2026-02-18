import os
from datetime import datetime

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import read_config
from utils import globals
from utils.api_client import APIClient
from utils.logger import Logger, initialize_logger

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # conftest.py у руті
RUN_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
TEST_RUN_DIR = os.path.join(PROJECT_ROOT, "reports", f"test_run_{RUN_TIMESTAMP}")
os.makedirs(TEST_RUN_DIR, exist_ok=True)


# ==========================================================
#             УТИЛІТА ДЛЯ СТВОРЕННЯ ЛОГУ ТЕСТУ
# ==========================================================
def setup_test_logging(request):
    """
    reports/test_run_<timestamp>/<test_file>/<test_name>/
    """
    globals.list_exceptions = []
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
    options = Options()
    if read_config.driver_mode() == "true":
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.base_url = read_config.get_url()

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
    logger, _ = setup_test_logging(request)
    logger.info("Initialized API client")

    base_url = os.getenv("BASE_URL")

    if hasattr(request, "param"):
        user_name, password = request.param
    else:
        user_name = os.getenv("API_USER")
        password = os.getenv("API_PASSWORD")

    client = APIClient(base_url)
    try:
        Logger.info(f"Login with user: {user_name}")
        client.login(user_name, password)
    except Exception as e:
        logger.error(f"Login failed: {e}")
        yield None
        return

    try:
        yield client
    finally:

        try:
            if client:
                client.close()
        except Exception as e:
            logger.error(f"Error closing API client: {e}")

        try:
            logger.info(f"Test {request.node.nodeid} finished")
            Logger.log_test_summary()
        except Exception as e:
            logger.error(f"Error during logging test summary: {e}")


# ==========================================================
#                       PYTEST HOOKS
# ==========================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if call.excinfo is not None:
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                Logger.save_screenshot(driver)
        if globals.list_exceptions:
            report.outcome = "failed"
            report.longrepr = f"Test failed after execution: {item.name}"


def pytest_addoption(parser):
    parser.addoption("--email", action="store", help="User email for login")
    parser.addoption("--password", action="store", help="User password for login")
    parser.addoption("--base-url", action="store", help="Base API URL")
    parser.addoption(
        "--suite-name",
        action="store",
        default=None,
        help="Name of test suite (used for logging/reporting)",
    )


pytest_plugins = [
    "fixtures.user_fixtures",
]
