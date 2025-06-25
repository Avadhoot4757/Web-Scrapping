import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def get_product_links(driver, query, platform, limit=50):
    print(f"Searching links for '{query}' on {platform}...")
    links = []
    base_urls = {
        "amazon": f"https://www.amazon.in/s?k={query.replace(' ', '+')}",
        "flipkart": f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    }

    if platform not in base_urls:
        print(f"Unsupported platform: {platform}")
        return links

    driver.get(base_urls[platform])
    time.sleep(2)

    while len(links) < limit:
        time.sleep(2)

        # Use Selenium XPath for other platforms
        xpath_selectors = {
            "amazon": '//a[@class="a-link-normal s-no-outline"]',
            "flipkart": '//a[@class="rPDeLR"]',
        }
        elements = driver.find_elements(By.XPATH, xpath_selectors.get(platform, '//a'))
        for e in elements:
            href = e.get_attribute('href')
            if href and platform in href and href not in links:
                links.append(href)
            if len(links) >= limit:
                break

        if len(links) >= limit:
            break

        try:
            next_button_selectors = {
                "amazon": '//a[contains(@class, "s-pagination-next")]',
                "flipkart": '//a[@class="_9QVEpD"]',
            }
            next_button = driver.find_element(By.XPATH, next_button_selectors.get(platform))
            next_button.click()
        except NoSuchElementException:
            break  # No more pages

    return links[:limit]

