import subprocess
import sys
import time

import pytest
import requests
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def fastapi_server():
    """Start the FastAPI server for E2E tests and stop afterward."""
    fastapi_process = subprocess.Popen([sys.executable, "main.py"])

    server_url = "http://127.0.0.1:8000/"
    timeout = 30
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    else:
        fastapi_process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout period.")

    yield

    fastapi_process.terminate()
    fastapi_process.wait()


@pytest.fixture(scope="session")
def playwright_instance_fixture():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
