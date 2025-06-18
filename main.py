from scraper.driver import get_driver
from scraper.search import get_product_links
from scraper.product import parse_product_page
from scraper.utils import save_to_csv

def main():
    driver = get_driver()
    try:
        query = "mens t shirts"
        links = get_product_links(driver, query, limit=10)
        data = [parse_product_page(driver, link) for link in links]
        save_to_csv(data)
        print("Scraping complete. Data saved to data/products.csv.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

