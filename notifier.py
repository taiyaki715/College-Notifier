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

        # chrome-driverを設定
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--lang=ja-JP')
        driver = webdriver.Chrome(options=options)

        # ポータルサイトアクセス
        driver.get(SITE_URL)
        print("access OK")

        # メールアドレス入力
        mail_address_element = driver.find_element_by_xpath("//input[@type='email']")
        mail_address_element.send_keys(self.USER_MAIL_ADDRESS)
        mail_address_element.send_keys(Keys.ENTER)
        time.sleep(3)
        print("address OK")

        # パスワード入力
        password_element = driver.find_element_by_xpath("//input[@type='password']")
        password_element.send_keys(self.USER_PASSWORD)
        password_element.send_keys(Keys.ENTER)
        time.sleep(3)
        print("password OK")

        driver.save_screenshot('/tmp/ss.png')
        notifier = Notifier('ow1snOdCNyTHIUsfOLxwp3w9anjqEkm2UJJLjEm3rO0')
        notifier.send(image='/tmp/ss.png')
        time.sleep(120)

        # ページソース取得
        source = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')

        # 新着ニュース取得
        news_list = [news_with_tag.text for news_with_tag in soup.select('ul.front_news_list > li > a > p')]
        print("scrape COMPLETE")
        return news_list[:n_news]


class Notifier:
    def __init__(self, token):
        self.URL = 'https://notify-api.line.me/api/notify'
        self.TOKEN = token

        self.header = {'Authorization': 'Bearer ' + self.TOKEN}

    def send(self, message='', image=None):
        payload = {}
        files = {}

        if message:
            payload.setdefault('message', message)
        if image:
            files.setdefault('imageFile', open(image, 'rb'))

        requests.post(self.URL, headers=self.header, params=payload, files=files)
