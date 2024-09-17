import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Setup logging
logging.basicConfig(filename='scrape_agents.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class AgentScraper:
    def __init__(self, base_url, output_path, headers, start_page=1, end_page=290):
        self.base_url = base_url
        self.output_path = output_path
        self.headers = headers
        self.start_page = start_page
        self.end_page = end_page
        self.all_agents = []

    def scrape_agents(self, page_num):
        logging.info(f"Scraping page {page_num}")
        print(f"Scraping page {page_num}...")
        url = self.base_url + str(page_num)
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        agents = []
        for agent_card in soup.find_all('a', class_='agent-card-link'):
            agent_url = "https://www.remax.co.za" + agent_card['href']
            logging.info(f"Scraping agent at {agent_url}")
            print(f"Scraping agent at {agent_url}...")
            agent_response = requests.get(agent_url, headers=self.headers)
            agent_soup = BeautifulSoup(agent_response.text, 'html.parser')

            agent_name = agent_card.get('title', '').split(' - ')[0]
            agent_office = agent_soup.select_one('.agent-office.width-100')
            address = agent_soup.select_one('p[itemprop="address"]')
            mobile = agent_soup.select_one('.show-btn-mobile')
            phone = agent_soup.select_one('.show-btn-tel')
            email = agent_soup.select_one('.show-btn-email')

            # Extract suburb from URL
            suburb = agent_card['href'].split('/')[4] if len(agent_card['href'].split('/')) > 4 else 'Unknown'

            agent_data = {
                'Name': agent_name,
                'Office': agent_office.text.strip() if agent_office else '',
                'Address': address.text.strip() if address else '',
                'Mobile': mobile['data-agent-mobile'] if mobile else '',
                'Phone': phone['data-agent-tel'] if phone else '',
                'Email': email['data-agent-email'] if email else '',
                'Suburb': suburb
            }

            agents.append(agent_data)
            # Print the scraped data
            print(f"Data scraped for agent: {agent_data}")

        return agents

    def scrape_all_pages(self):
        for page in range(self.start_page, self.end_page + 1):
            logging.info(f"Processing page {page}")
            print(f"Scraping page {page}...")
            self.all_agents.extend(self.scrape_agents(page))

    def save_to_excel(self):
        # Convert to DataFrame
        df = pd.DataFrame(self.all_agents)

        # Create a Pandas Excel writer using openpyxl as the engine
        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            logging.info("Writing data to Excel file")
            for suburb, group_df in df.groupby('Suburb'):
                sheet_name = suburb[:31]  # Excel sheet names can't be longer than 31 chars
                logging.info(f"Writing sheet for suburb: {sheet_name}")
                print(f"Writing sheet for suburb: {sheet_name}")
                group_df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Data saved to {self.output_path}")
        logging.info(f"Data saved to {self.output_path}")


