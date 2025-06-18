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

    def safe_find_by_attribute(by, selector, attribute):
        try:
            return driver.find_element(by, selector).get_attribute(attribute)
        except:
            return "N/A"

    def safe_find_any(selectors):
        for by, selector in selectors:
            try:
                return driver.find_element(by, selector).text.strip()
            except:
                continue
        return "N/A"

    try:
        size_ul = driver.find_element(By.CSS_SELECTOR, 'ul[data-a-button-group*="size_name"]')
        size_options = size_ul.find_elements(By.TAG_NAME, 'li')
    except:
        size_options = []

    try:
        color_ul = driver.find_element(By.CSS_SELECTOR, 'ul[data-a-button-group*="color_name"]')
        color_options = color_ul.find_elements(By.TAG_NAME, 'li')
    except:
        color_options = []

    rating_count = safe_find_any([
        (By.ID, "acrCustomerReviewText"),
    ])

    print(f"Scraping {safe_find(By.ID, 'productTitle')}")

    return {
        "URL": url,
        "Title": safe_find(By.ID, "productTitle"),
        "Brand": safe_find(By.ID, "bylineInfo"),
        "SKU Density": len(size_options) + len(color_options),
        "Size Options": len(size_options),
        "Color Options": len(color_options),
        "Availability": safe_find(By.ID, "availability"),
        "DeliveryEstimate": safe_find(By.ID, "mir-layout-DELIVERY_BLOCK"),
        "Seller": safe_find(By.ID, "sellerProfileTriggerId"),
        "Price": safe_find(By.CLASS_NAME, "a-price-whole"),
        "Rating": safe_find_by_attribute(By.ID, "acrPopover", "title"),
        "Number of Ratings": rating_count
    }

