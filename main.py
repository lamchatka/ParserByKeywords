

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

def parser(): #domens_list: list
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    browser = Chrome(service=Service(ChromeDriverManager().install()))
    keywords = "кухни зов в майкопе"
    url = "https://yandex.ru/search/?text=" + keywords
    try:
        browser.get(url)

        # time.sleep(120)

        # dns = driver.find_elements(By.XPATH,'//li[@class="serp-item serp-item_card"]')
        # print(len(dns))
        # for i in dns:
        #     print(i.get_attribute('href'))

    except Exception as ex:
        print(ex)
    # browser = init_driver()
    # keywords = get_keyword(queryList)
    # try:
    #     for keyword in keywords:
    #         url = "https://yandex.ru/search/?text=" + keyword
    #         browser.get(url)
    #         a_tags = browser.find_elements(By.XPATH, "")
    #         # list of hrefs
    #         href_list = []
    #         for a_tag in a_tags:
    #            href = a_tag.get_attribute("href")
    #            href_list.append(href)
    #         print(href_list)
    #
    # except Exception as ex:
    #     logging.exception(ex)

    if browser:
        browser.quit()


def main():
    parser()


main()