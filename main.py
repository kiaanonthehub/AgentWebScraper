# Main script
import os

from AgentScraper import AgentScraper

if __name__ == "__main__":
    downloads_folder = os.path.expanduser('~/Downloads')
    file_path = os.path.join(downloads_folder, 'agents_info.xlsx')
    base_url = "https://www.remax.co.za/real-estate-agents/south-africa/kwazulu-natal/?page="
    headers = {"User-Agent": "Mozilla/5.0"}

    # Create an instance of the scraper
    scraper = AgentScraper(base_url=base_url, output_path=file_path, headers=headers)

    # Scrape all pages
    scraper.scrape_all_pages()

    # Save the data to Excel
    scraper.save_to_excel()