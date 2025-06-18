from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service('/home/avadhoot/arealis/chromedriver-linux64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

