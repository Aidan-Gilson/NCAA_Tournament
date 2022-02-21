from selenium import webdriver
from selenium.webdriver import Chrome
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager

#Webdriver parser used to extract the brackets
def parse2(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    sleep(3)
    sourceCode = driver.page_source
    return sourceCode


def parse(url):
    response = webdriver.Chrome()
    response.get(url)
    sleep(3)
    sourceCode = response.page_source
    return sourceCode
