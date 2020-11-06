import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class Scraper:
    def __init__(self, address, password):
        self.USER_MAIL_ADDRESS = address
        self.USER_PASSWORD = password

    def get_news(self, n_news=3):

        SITE_URL = 'https://service.cloud.teu.ac.jp/inside2/hachiouji/computer_science/'

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--lang=ja-JP')
        driver = webdriver.Chrome(options=options)

        driver.get(SITE_URL)
        print("access OK")

        print(driver.current_url)
        mail_address_element = driver.find_element_by_xpath("//input[@type='email']")
        mail_address_element.send_keys(self.USER_MAIL_ADDRESS)
        mail_address_element.send_keys(Keys.ENTER)
        time.sleep(3)
        print("address OK")

        print(driver.current_url)
        password_element = driver.find_element_by_xpath("//input[@type='password']")
        password_element.send_keys(self.USER_PASSWORD)
        password_element.send_keys(Keys.ENTER)
        time.sleep(3)
        print("password OK")

        print(driver.current_url)
        source = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')

        news_list = [news_with_tag.text for news_with_tag in soup.select('ul.front_news_list > li > a > p')]
        print("scrape COMPLETE")
        return news_list[:n_news]


class Notifier:
    def __init__(self, token):
        self.URL = 'https://notify-api.line.me/api/notify'
        self.TOKEN = token

        self.header = {'Authorization': 'Bearer ' + self.TOKEN}

    def send(self, message):
        if message:
            payload = {'message': message}
            requests.post(self.URL, headers=self.header, params=payload)
