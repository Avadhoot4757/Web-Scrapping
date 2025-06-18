from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def get_product_links(driver, query, limit=50):
    print("Searching links..")
    links = []
    base_url = f"https://www.amazon.in/s?k={query.replace('-', '+')}"
    driver.get(base_url)

    while len(links) < limit:
        time.sleep(2)

        elements = driver.find_elements(By.XPATH, '//a[@class="a-link-normal s-no-outline"]')
        for e in elements:
            href = e.get_attribute('href')
            if href and "amazon.in" in href:
                links.append(href)
            if len(links) >= limit:
                break

        if len(links) >= limit:
            break

        try:
            next_button = driver.find_element(By.XPATH, '//a[contains(@class, "s-pagination-next")]')
            next_button.click()
        except NoSuchElementException:
            break  # No more pages

    return links
