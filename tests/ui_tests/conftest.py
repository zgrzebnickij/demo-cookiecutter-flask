from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import pytest

@pytest.fixture
def browser():
    options = Options()
    # options.add_argument('--headless')
    firefox = Firefox(options=options)
    firefox.implicitly_wait(3)
    firefox.maximize_window()
    firefox.get('http://127.0.0.1:5000/')
    yield firefox
    firefox.quit()