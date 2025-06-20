import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def get_product_links(driver, query, platform, limit=50):
    print(f"Searching links for '{query}' on {platform}...")
    links = []
    base_urls = {
        "amazon": f"https://www.amazon.in/s?k={query.replace(' ', '+')}",
        "myntra": f"https://www.myntra.com/{query.replace(' ', '-')}",
        "flipkart": f"https://www.flipkart.com/search?q={query.replace(' ', '+')}",
        "tatacliq": f"https://www.tatacliq.com/search/?searchCategory=all&text={query.replace(' ', '%20')}"
    }
    
    if platform not in base_urls:
        print(f"Unsupported platform: {platform}")
        return links

    driver.get(base_urls[platform])
    time.sleep(2)

    while len(links) < limit:
        time.sleep(2)
        
        xpath_selectors = {
            "amazon": '//a[@class="a-link-normal s-no-outline"]',
            "myntra": '//li[@class="product-base"]//a[@data-refreshpage="true" and .//div[contains(@class, "product-productMetaInfo")]]',
            "flipkart": '//a[@class="rPDeLR"]',
            "tatacliq": '//a[@class="ProductModule__imageAndDescriptionWrapper"]'
        }
        
        elements = driver.find_elements(By.XPATH, xpath_selectors.get(platform, '//a'))
        for e in elements:
            href = e.get_attribute('href')
            if href and platform in href:
                links.append(href)
            if len(links) >= limit:
                break

        if len(links) >= limit:
            break

        try:
            next_button_selectors = {
                "amazon": '//a[contains(@class, "s-pagination-next")]',
                "myntra": '//li[@class="pagination-next"]/a',
                "flipkart": '//a[@class="_1LKTO3"]',
                "tatacliq": '//a[@class="pagination__next"]'
            }
            next_button = driver.find_element(By.XPATH, next_button_selectors.get(platform))
            next_button.click()
        except NoSuchElementException:
            break  # No more pages

    return links[:limit]
