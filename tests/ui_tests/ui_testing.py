from gevent import config
from selenium.webdriver.support.ui import WebDriverWait #1


def test_registration_form_too_short_password(browser): #2
    browser.find_element_by_link_text('Create account'). click() #3
    WebDriverWait(browser, timeout=3).until( #4
        lambda d: d.find_element_by_css_selector ('#registerForm #username') #5
    ).send_keys("jan") #6
    WebDriverWait(browser, timeout=3).until( #4
        lambda d: d.find_element_by_css_selector ('#registerForm #email') #5
    ).send_keys("as@as.as") #6
    WebDriverWait(browser, timeout=3).until( #4
        lambda d: d.find_element_by_css_selector ('#registerForm #password') #5
    ).send_keys("jan") #6
    WebDriverWait(browser, timeout=3).until( #4
        lambda d: d.find_element_by_css_selector ('#registerForm #confirm') #5
    ).send_keys("jan") #6
    browser.find_element_by_xpath('//input[@type="submit"]').click() #7
    content =  WebDriverWait(browser, timeout=3).until( #8
        lambda d: d.find_element_by_xpath('//div[@class="alert alert-warning"]') #9
    ).text
    assert 'Field must be between 6 and 40 characters long' in content, content

import unittest
from urllib.request import urlopen

from flask_testing import LiveServerTestCase
from selenium import webdriver

from my_flask_app.app import create_app
from my_flask_app.user.models import User
from flask_sqlalchemy import SQLAlchemy

class TestBase(LiveServerTestCase):
    PORT = 8943

    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            # Specify the test database
            # SQLALCHEMY_DATABASE_URI='sqlite:///sample.db',
            # Change the port that the liveserver listens on
            SQLALCHEMY_DATABASE_URI = "sqlite://",
            TESTING = True,
            LIVESERVER_PORT=self.PORT
        )
        self.db = SQLAlchemy(app)
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Firefox()
        self.driver.get(self.get_server_url())

        self.db.session.commit()
        self.db.drop_all()
        self.db.create_all()

        self.db.session.commit()


    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        self.driver.get(f'http://127.0.0.1:{self.PORT}/')
        page = self.driver.page_source
        assert 'My Flask App' in page

    def test_server_login(self):
        user = User(username='Adam', email='adam@as.pl', password='secret')
        self.db.session.add(user)
        self.db.session.commit()
        assert user in self.db.session
        self.driver.get(f'http://127.0.0.1:{self.PORT}/')
        WebDriverWait(self.driver, timeout=3).until( 
        lambda d: d.find_element_by_css_selector('#loginForm #username') 
        ).send_keys("Adam") 
        WebDriverWait(self.driver, timeout=3).until( 
            lambda d: d.find_element_by_css_selector('#loginForm #password') 
        ).send_keys("secret") 
        self.driver.find_element_by_xpath('//button[@type="submit"]').click() 
        page = self.driver.page_source
        assert 'You are logged in.' in page, page

if __name__ == '__main__':
    unittest.main()