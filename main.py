import time

from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager


def fake_ua() -> UserAgent:
    ua = UserAgent()
    return ua.random

# params: queryList - list of
def get_keyword(queryList: list) -> list:
    keywords = []
    if not queryList:
        logging.exception("QueryList is null")
        exit(1)
    for query in queryList:
        keywords.append(query.lower().replace(" ", "+"))
    return keywords


def parse(domen_list: list): #domens_list: list
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    browser = Chrome(service=Service(ChromeDriverManager().install()))
    keywords = get_keyword(['кухни зов в майкопе', 'зов кухни'])

    href_list = {}
    domen_ad = 'yabs.yandex.ru'
    for keyword in keywords:
        url = "https://yandex.ru/search/?text=" + keyword
        try:
            browser.get(url)
            time.sleep(5)
            dns = browser.find_elements(By.XPATH,'//div[@class="Path Organic-Path path organic__path"]//a')
            # print(len(dns))
            href_list = {i+1: dns[i].get_attribute('href') for i in range(0, len(dns))}

        except Exception as ex:
            logging.exception(ex)

        # print(href_list)
        if browser:
            browser.quit() # закрывать либо левее, либо в фор добавить инициализацию

        href_list = check(href_list, domen_ad) # словарь с сайтами без рекламы
        # print(href_list)
        for key, value in href_list.items():
             print(f"{key} : {value}")

        print('Позиция сайта на странице:')
        for domen in domen_list:
            for key,value in href_list.items():
                if value.startswith(domen, 8):  # or value.startswith(domen, 8)  domen in value.strip('/')[2]
                    print(f"{key} : {value}")
                    break


def check(href_list, domen_ad) -> dict:  # проверка на рекламу
    href_list = {key: value for key, value in href_list.items() if not value.startswith(domen_ad, 8)}
    return href_list


def main():
    parse(['zov01.ru', '023-kuhni-lime.ru', 'maikop.mebelister.ru', 'vk.com', 'zovrus.ru']) # 023-kuhni-lime.ru


main()