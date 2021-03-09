import socket

from django.test import tag, TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django.contrib.auth.models import User
from respondent.models import Respondent, GroupRespondent
from surveyor.models import Surveyor, Question, Task, Group, GroupSurveyor
from core.models import Organisation


@tag('integration')
class LoginTest(StaticLiveServerTestCase):

    def setUp(self):
        self.organisation = Organisation.objects.create(name="Organisation")
        self.user = User.objects.create_user(username='user', email='user@test.com', password='password')
        self.surveyor = Surveyor.objects.create(user=self.user, firstname='Firstname', surname='Surname', organisation=self.organisation)
        self.browser = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)

    def tearDown(self):
        self.browser.quit()

    def test_login_valid(self):
        """
        Entering valid credentials should take us to /dashboard.
        """
        login_url = 'http://web:8000/accounts/login'
        self.browser.get(login_url)
        self.assertIn(self.browser.title, 'Sign In')
        email_input = self.browser.find_element_by_xpath('//*[@id="id_login"]')
        email_input.send_keys('user@test.com')
        password_input = self.browser.find_element_by_xpath('//*[@id="id_password"]')
        password_input.send_keys('password')
        self.browser.find_element_by_xpath('/html/body/div/form/button').click()
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.url_changes(login_url))
        self.assertEqual(self.browser.current_url, 'http://web:8000/dashboard')
    
    # def test_login_valid(self):
    #     """
    #     Entering invalid credentials should keep us on the same page.
    #     """
    #     login_url = 'http://web:8000/accounts/login'
    #     self.browser.get(login_url)
    #     self.assertIn(self.browser.title, 'Sign In')
    #     email_input = self.browser.find_element_by_xpath('//*[@id="id_login"]')
    #     email_input.send_keys('user@test.com')
    #     password_input = self.browser.find_element_by_xpath('//*[@id="id_password"]')
    #     password_input.send_keys('password')
    #     self.browser.find_element_by_xpath('/html/body/div/form/button').click()
    #     wait = WebDriverWait(self.browser, 10)
    #     wait.until(EC.url_changes(login_url))
    #     self.assertEqual(self.browser.current_url, 'http://web:8000/dashboard')