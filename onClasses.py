from abc import ABC, abstractmethod
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
import logging


class Parser():

    def __fake_ua(self): # protected method
        self.ua = UserAgent()
        return self.ua.random()

    @abstractmethod
    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'user-agent={self.__fake_ua()}')

        seleniumwire_options = {
            'addr': 'django',
            'proxy': {
                'http': 'socks5://np436186:n38e7m82@elena.ltespace.com:14384',
                'https': 'socks5://np436186:n38e7m82@elena.ltespace.com:14384',
                'no_proxy': 'localhost,django,127.0.0.1'
            }
        }

        self.browser = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
            options=chrome_options,
            seleniumwire_options=seleniumwire_options
        )

        self.browser.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return self.browser

    @abstractmethod
    def get_keywords(self, queryList: list):
        self.keywords = []
        if not queryList:
            logging.exception("QueryList is null")
            exit(1)
        for query in queryList:
            self.keywords.append(query.lower().replace(" ", "+"))

        return self.keywords

    @abstractmethod
    def parser(self, queryList: list, domens_list: list):
        self.browser = self.init_browser()  # вроде говнокод
        self.keywords = self.get_keywords(queryList)  # вроде говнокод
        try:
            for keyword in self.keywords:
                url = "https://yandex.ru/search/?text=" + keyword
                self.browser.get(url)
                a_tags = self.browser.find_elements(By.XPATH, "")
                # list of hrefs
                href_list = []
                for a_tag in a_tags:
                    href = a_tag.get_attribute("href")
                    href_list.append(href)
                print(href_list)

        except Exception as ex:
            logging.exception(ex)

        if self.browser:
            self.browser.quit()


class Main(Parser):
    parser = Parser()
    print(parser.fake_ua())










