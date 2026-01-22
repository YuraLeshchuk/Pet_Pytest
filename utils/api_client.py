import requests
import time
from utils.logger import Logger


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
        self.logger = Logger.get_global_logger()

    def _log_request(self, method: str, url: str, **kwargs):
        self.logger.info(f"[{method}] {url}")
        if kwargs.get("json"):
            self.logger.debug(f"Request body: {kwargs['json']}")
        if kwargs.get("params"):
            self.logger.debug(f"Query params: {kwargs['params']}")

    def _log_response(self, response, elapsed_time):
        self.logger.info(f"Status: {response.status_code} | Time: {elapsed_time:.2f}s")
        try:
            self.logger.debug(f"Response JSON: {response.json()}")
        except Exception:
            self.logger.debug(f"Response text: {response.text[:500]}")

    def login(self, user_name: str, password: str):
        endpoint = f"{self.base_url}/Account/v1/GenerateToken"
        payload = {"userName": user_name, "password": password}

        self._log_request("POST", endpoint, json=payload)

        start = time.time()
        response = self.session.post(endpoint, json=payload)
        elapsed = time.time() - start

        self._log_response(response, elapsed)

        if response.status_code != 200:
            self.logger.error(
                f"Login failed: {response.status_code} - {response.text}"
            )
            return response

        try:
            data = response.json()
        except ValueError:
            self.logger.error("Login response is not JSON")
            return response

        self.token = data.get("token")
        if self.token:
            self.session.headers.update(
                {"Authorization": f"Bearer {self.token}"}
            )
            self.logger.info(f"Token saved: {self.token}")
        else:
            self.logger.warning("Token not found in response")

        return response

    def get(self, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("GET", url, **kwargs)

        start = time.time()
        response = self.session.get(url, **kwargs)
        elapsed = time.time() - start

        self._log_response(response, elapsed)
        return response

    def post(self, endpoint: str, data=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("POST", url, json=data, **kwargs)

        start = time.time()
        r = self.session
        response = self.session.post(url, json=data, **kwargs)
        elapsed = time.time() - start

        self._log_response(response, elapsed)
        return response

    def put(self, endpoint: str, data=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("PUT", url, json=data, **kwargs)

        start = time.time()
        response = self.session.put(url, json=data, **kwargs)
        elapsed = time.time() - start

        self._log_response(response, elapsed)
        return response

    def delete(self, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("DELETE", url, **kwargs)

        start = time.time()
        response = self.session.delete(url, **kwargs)
        elapsed = time.time() - start

        self._log_response(response, elapsed)
        return response

    def close(self):
        self.session.close()
        self.logger.info("API session closed.")
