import socket

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class SiteTest(StaticLiveServerTestCase):

    # live_server_url = 'http://{}:8000'.format(
    #     socket.gethostbyname(socket.gethostname())
    # )

    def setUp(self):
        self.browser = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)

    def tearDown(self):
        self.browser.quit()

    def test_visit_site(self):
        self.browser.get('http://web:8000/accounts/login')
        self.assertIn(self.browser.title, 'Sign In')