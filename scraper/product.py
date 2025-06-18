import time
from selenium.webdriver.common.by import By

def parse_product_page(driver, url):
    driver.get(url)
    time.sleep(2)

    def safe_find(by, selector):
        try:
            return driver.find_element(by, selector).text.strip()
        except:
            return "N/A"

    def find_asin():
        try:
            return driver.find_element(By.XPATH, '//th[contains(text(),"ASIN")]/following-sibling::td').text.strip()
        except:
            return "N/A"

    return {
        "URL": url,
        "Title": safe_find(By.ID, "productTitle"),
        "Brand": safe_find(By.ID, "bylineInfo"),
        "Availability": safe_find(By.ID, "availability"),
        "DeliveryEstimate": safe_find(By.ID, "mir-layout-DELIVERY_BLOCK"),
        "Seller": safe_find(By.ID, "sellerProfileTriggerId")
    }

