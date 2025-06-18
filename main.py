from scraper.driver import get_driver
from scraper.search import get_product_links
from scraper.product import parse_product_page
from scraper.utils import save_to_csv
from datetime import datetime

def main():
    driver = get_driver()
    try:
        query = "womens jwellery"
        links = get_product_links(driver, query, limit=10)
        data = [parse_product_page(driver, link) for link in links]
        scrape_date = datetime.today().strftime('%Y-%m-%d')
        file = f"data/{query.replace(' ', '_')}_{scrape_date}.csv"
        save_to_csv(data, file)
        print(f"Scraping complete. Data saved to {file}.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

