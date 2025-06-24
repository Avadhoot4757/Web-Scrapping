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

    # Platform-specific selectors
    selectors = {
        "amazon": {
            "title": (By.ID, "productTitle"),
            "brand": (By.ID, "bylineInfo"),
            "size": 'ul[data-a-button-group*="size_name"]',
            "color": 'ul[data-a-button-group*="color_name"]',
            "availability": (By.ID, "availability"),
            "delivery": (By.ID, "mir-layout-DELIVERY_BLOCK"),
            "seller": (By.ID, "sellerProfileTriggerId"),
            "price": (By.CLASS_NAME, "a-price-whole"),
            "rating": (By.ID, "acrPopover"),
            "rating_count": [(By.ID, "acrCustomerReviewText")]
        },
        "myntra": {
            "title": (By.CLASS_NAME, "pdp-title"),
            "brand": (By.CLASS_NAME, "pdp-brand"),
            "size": 'div.size-buttons-size-container',
            "color": 'div.color-picker-container',
            "availability": (By.CLASS_NAME, "pdp-availability"),
            "delivery": (By.CLASS_NAME, "pdp-delivery"),
            "seller": (By.CLASS_NAME, "pdp-seller-info"),
            "price": (By.CLASS_NAME, "pdp-price"),
            "rating": (By.CLASS_NAME, "rating-average"),
            "rating_count": [(By.CLASS_NAME, "rating-count")]
        },
        "flipkart": {
            "title": (By.CLASS_NAME, "VU-ZEz"),
            "brand": (By.CLASS_NAME, "mEh187"),
            "size": (By.CLASS_NAME, "hSEbzK"),
            "color": (By.CLASS_NAME, "hSEbzK"),
            "availability": (By.CLASS_NAME, "_1r1VYa"),
            "delivery": (By.CLASS_NAME, "Y8v7Fl"),
            "seller": (By.ID , "sellerName"),
            "price": (By.CLASS_NAME, "CxhGGd"),
            "rating": (By.CLASS_NAME, "_6er70b"),
            "rating_count": [(By.CLASS_NAME, "Wphh3N")]
        },
        "tatacliq": {
            "title": (By.CLASS_NAME, "ProductDetails__productTitle"),
            "brand": (By.CLASS_NAME, "ProductDetails__brandName"),
            "size": 'div.size__options',
            "color": 'div.color__options',
            "availability": (By.CLASS_NAME, "ProductDetails__availability"),
            "delivery": (By.CLASS_NAME, "ProductDetails__delivery"),
            "seller": (By.CLASS_NAME, "ProductDetails__seller"),
            "price": (By.CLASS_NAME, "ProductDetails__price"),
            "rating": (By.CLASS_NAME, "ProductDetails__rating"),
            "rating_count": [(By.CLASS_NAME, "ProductDetails__ratingCount")]
        }
    }

    # Determine platform from URL
    platform = next((p for p in selectors if p in url), "amazon")
    s = selectors[platform]

    # Default values
    size_options = []
    color_options = []
    
    # Flipkart-specific logic for color (1st) and size (2nd) element with class 'hSEbzK'
    if platform == "flipkart":
        try:
            containers = driver.find_elements(By.CLASS_NAME, "hSEbzK")
            if len(containers) >= 2:
                color_options = containers[0].find_elements(By.TAG_NAME, "li")
                size_options = containers[1].find_elements(By.TAG_NAME, "li")
        except:
            color_options = []
            size_options = []
    else:
        try:
            size_ul = driver.find_element(By.CSS_SELECTOR, s["size"])
            size_options = size_ul.find_elements(By.TAG_NAME, 'li')
        except:
            size_options = []
    
        try:
            color_ul = driver.find_element(By.CSS_SELECTOR, s["color"])
            color_options = color_ul.find_elements(By.TAG_NAME, 'li')
        except:
            color_options = []
    
    
        try:
            size_ul = driver.find_element(By.CSS_SELECTOR, s["size"])
            size_options = size_ul.find_elements(By.TAG_NAME, 'li')
        except:
            size_options = []
    
        try:
            color_ul = driver.find_element(By.CSS_SELECTOR, s["color"])
            color_options = color_ul.find_elements(By.TAG_NAME, 'li')
        except:
            color_options = []
    
    rating_count = safe_find_any(s["rating_count"])
    
    print(f"Scraping {safe_find(*s['title'])} from {platform}")
    
    return {
        "URL": url,
        "Title": safe_find(*s["title"]),
        "Brand": safe_find(*s["brand"]),
        "SKU Density": len(size_options) + len(color_options),
        "Size Options": len(size_options),
        "Color Options": len(color_options),
        "Availability": safe_find(*s["availability"]),
        "DeliveryEstimate": safe_find(*s["delivery"]),
        "Seller": safe_find(*s["seller"]),
        "Price": safe_find(*s["price"]),
        "Rating": safe_find_by_attribute(*s["rating"], "title") if platform == "amazon" else safe_find(*s["rating"]),
        "Number of Ratings": rating_count,
        "Platform": platform
    }
