from selenium import webdriver
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import re

class SeleniumTests(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome('./chromedriver.exe')
        self.browser.get('http://127.0.0.1:8000/')
        self.browser.maximize_window()

    def tearDown(self) -> None:
        self.browser.close()

    def testHomePage(self):

        self.assertEqual(
            self.browser.find_element_by_id('div_id_username').text,
            "Username*"
        )
        self.assertEqual(
            self.browser.find_element_by_id('div_id_password').text,
            "Password*"
        )

    def testLogin(self):
        self.browser.find_element_by_name('username').send_keys('tester2')
        self.browser.find_element_by_name('password').send_keys('Abc123def')
        self.browser.find_element_by_id('loginButton').click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="navbarSupportedContent"]/ul/li[7]/a')))
        self.assertTrue(self.browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[7]/a').is_displayed())

    def testRegister(self):
        self.browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a').click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/form/button')))
        self.browser.find_element_by_name('username').send_keys('tester2')
        self.browser.find_element_by_name('email').send_keys('tester@gmail.com')
        self.browser.find_element_by_name('password1').send_keys('Abc123def')
        self.browser.find_element_by_name('password2').send_keys('Abc123def')
        self.browser.find_element_by_xpath('/html/body/div/form/button').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="error_1_id_username"]/strong')))
        self.assertEqual(self.browser.find_element_by_xpath('//*[@id="error_1_id_username"]/strong').text, 'A user with that username already exists.')

    def test_add_ingredient(self):
        self.testLogin()
        self.browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[1]/a').click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/form/button')))
        self.browser.find_element_by_name('name').send_keys('Bananowa Rozkosz')
        self.browser.find_element_by_name('price').send_keys('2.50')
        self.browser.find_element_by_xpath('/html/body/div/form/button').click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/form/button')))
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div')))
        self.assertEqual(self.browser.find_element_by_xpath('/html/body/div/div').text, 'Ingredient successfully added to the database.')

    def test_delete_ingredient(self):
        self.testLogin()
        self.browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/table/tbody/tr[1]/th[1]')))
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.ID,'Bananowa Rozkosz_Delete_Button')))
        element = self.browser.find_element_by_id('Bananowa Rozkosz_Delete_Button')
        self.browser.execute_script("arguments[0].click();", element)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/h1')))
        self.browser.find_element_by_xpath('/html/body/div/form/button').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/h2')))
        self.assertEqual(self.browser.current_url, 'http://127.0.0.1:8000/ingredient/list/')


    def test_add_new_recipe(self):
        self.testLogin()
        self.browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[6]/a').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div[1]/div[1]/div/div/div/h4')))
        self.browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/ul/li[2]/a').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="div_id_name"]/label')))
        self.browser.find_element_by_name('name').send_keys('Sernik babci Maliny')
        self.browser.find_element_by_name('description').send_keys('Sernik taki fajny taki smaczny z truskawkami.')
        sel = Select(self.browser.find_element_by_name('ingredients'))
        sel.select_by_index(0)
        sel.select_by_index(1)
        sel.select_by_index(2)
        sel.select_by_index(3)
        sel.select_by_index(4)
        sel.select_by_index(5)
        self.browser.find_element_by_xpath('/html/body/div/form/button').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div')))
        self.assertEqual(self.browser.find_element_by_xpath('/html/body/div/div').text, "Receipe successfully added to the database.")

    def test_delete_recipe(self):
        self.testLogin()
        self.browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[6]/a').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div[1]/div[1]/div/div/div/h4')))
        self.browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/ul/li[1]/a').click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.ID,'Sernik babci Maliny')))
        self.browser.find_element_by_id('Sernik babci Maliny').click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div[1]/a[1]')))
        self.browser.find_element_by_xpath('/html/body/div/div/div[1]/a[1]').click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]')))
        self.assertTrue(re.match('Recipe with id \d+ deleted successfully.',self.browser.find_element_by_xpath('/html/body/div[1]/div[1]').text))

if __name__ == "__main__":
    unittest.main()