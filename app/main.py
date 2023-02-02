import os.path
import time
# from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver import DesiredCapabilities
import json
from random import randrange
from seleniumwire import webdriver
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(f'user-agent={generate_fake_ua()}')
    seleniumwire_options = {
        'addr': 'django',
        'proxies': {
            'addr': 'django',
            "http": "socks5://1fnvs1zk:q6q7fran@dina.ltespace.com:13574",
            "https": "socks5://1fnvs1zk:q6q7fran@dina.ltespace.com:13574",
            'no_proxy': 'localhost,django,127.0.0.1'
        }
    }

    browser = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
        options=chrome_options,
        seleniumwire_options=seleniumwire_options
    )
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return browser

def generate_fake_ua() -> UserAgent:
    ua = UserAgent()
    return ua.random


def get_keywords_list(queryList: list) -> list:
    keywords = []
    if not queryList:
        logging.exception("QueryList is null")
        exit(1)
    for query in queryList:
        keywords.append(query.lower().replace(" ", "+"))
    return keywords


def get_new_yandex_regions_json():
    if not os.path.isfile('resource/new_yandex_region'):
        with open('resource/yandex_region.json', 'r') as f:
            data =  json.load(f)

        with open('resource/new_yandex_region', 'w') as nf:
            json.dump(data, nf, ensure_ascii=False, indent=4)


def get_region_id_by_title(title: str, path = 'resource/new_yandex_region' ) -> int:
    with open(path, 'r') as f:
        data = json.load(f)
        for elem in data:
            if elem['title'] == title:
                return elem['id']


def parse(domain_list: list, keywords: list, region_id: int):
    browser = init_driver()
    # keywords = get_keywords_list(['кухни зов в майкопе', 'зов кухни'])
    href_dict = {}
    result = []
    DOMAIN_AD = 'yabs.yandex.ru'
    for page in range(0,1):
        for keyword in keywords:
            if page == 0:
                url ='https://yandex.ru/search/?text=' + keyword + '&lr=' + str(region_id)
            else:
                url = 'https://yandex.ru/search/?text=' + keyword + '&lr=' + str(region_id) + '&p=' + str(page)
            try:
                browser.get(url)
                dns = browser.find_elements(
                    By.XPATH,'//div[@class="Path Organic-Path path organic__path"]//a')

                href_dict = {i+1: dns[i].get_attribute('href') for i in range(0, len(dns))}
            except Exception as ex:
                logging.exception(ex)

            href_dict = check_for_ads(href_dict, DOMAIN_AD) # словарь с сайтами без рекламы
            for key, value in href_dict.items():
                 print(f"{key} : {value}")

            dict_res = {}
            for domain in domain_list:
                for key,value in href_dict.items():
                    if value.startswith(domain, 8):
                      dict_res[key] = value
            result.append(dict_res)
            time.sleep(randrange(2,5))  # пауза между запросами, спасение от бана или капчи

    if browser:
        browser.quit()

    return  result


def check_for_ads(href_dict, domain_ad) -> dict:  # проверка на рекламный домен
    href_dict = {key: value for key, value in href_dict.items() if not value.startswith(domain_ad, 8)}
    return href_dict


def main():
    query_list  =  [
        'кухни зов ',
        'купить кухни'
        ]

    domain_list = [
         'zov01.ru',
         '023-kuhni-lime.ru',
         'maikop.mebelister.ru',
         'vk.com',
         'zovrus.ru'
     ]

    region_title = 'Краснодар'
    result = parse(domain_list, get_keywords_list(query_list), get_region_id_by_title(region_title))
    print('Позиция сайта на странице:')
    print(result) # TODO: вывод в формате json


main()