from scraper.driver import get_driver
from scraper.search import get_product_links
from scraper.product import parse_product_page
from scraper.utils import save_to_csv
from datetime import datetime

def main(queries, platforms, n):
    driver = get_driver()
    try:
        all_data = []
        for query in queries:
            for platform in platforms:
                print(f"Scraping {n} results for '{query}' on {platform}")
                links = get_product_links(driver, query, platform, limit=n)
                print(links)
                for link in links:
                    product_data = parse_product_page(driver, link)
                    product_data["Platform"] = platform  # Add platform to data
                    all_data.append(product_data)
                
                # Save data for each query-platform combination
                scrape_date = datetime.today().strftime('%Y-%m-%d')
                query_safe = query.replace(' ', '_')
                file = f"data/{query_safe}_{platform}_{scrape_date}.csv"
                save_to_csv(all_data, file)
                print(f"Data saved to {file}")
                all_data = []  # Reset for next platform/query
    finally:
        driver.quit()

if __name__ == "__main__":
    queries = ["womens t-shirts"]
    platforms = ["flipkart"]
    n = 75
    main(queries, platforms, n)
