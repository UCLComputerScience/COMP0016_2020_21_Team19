from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from chromedriver_py import binary_path

class TestSurveyorLoginPage(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(executable_path=binary_path)
        cls.selenium.implicitly_wait(10)

    # @classmethod
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super().tearDownClass()

    # def test_login(self):
    #     self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
    #     username_input = self.selenium.find_element_by_name("username")
    #     username_input.send_keys('myuser')
    #     password_input = self.selenium.find_element_by_name("password")
    #     password_input.send_keys('secret')
    #     self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
    
    def test_dashboard(self):
        pass
    
    # def 

    