from selenium.webdriver.common.by import By

def get_product_links(driver, query, limit=10):
    url = f"https://www.amazon.in/s?k={query.replace('-', '+')}"
    driver.get(url)
    elements = driver.find_elements(By.XPATH, '//a[@class="a-link-normal s-no-outline"]')
    
    links = []
    for e in elements:
        href = e.get_attribute('href')
        if href and "amazon.in" in href:
            links.append(href)
        if len(links) >= limit:
            break
    return links

