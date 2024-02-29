import json
import requests
from bs4 import BeautifulSoup

# Load the GraphML file into a NetworkX graph variable
with open('./data/links_by_depth_3.json', 'r') as file:
    links_by_depth_3 = json.load(file)
# Initialize an empty list to store all links
all_links = []

# Iterate through each depth level in the dictionary
for depth, links in links_by_depth_3.items():
    # Extend the list of links at each depth level
    all_links.extend(links)

# Remove duplicates by converting the list to a set and back to a list
all_links = list(set(all_links))

# If you want to save the unique links back to a JSON file
with open('./data/unique_links_3.json', 'w') as file:
    json.dump(all_links, file, indent=4)

# # Dictionary to store scraped text content (URL as key, text content as value)
# scraped_data = {}

# def scrape_text_from_website(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             # Extract text content from the webpage
#             text_content = soup.get_text()
#             return text_content
#         else:
#             print(f"Failed to fetch content from {url}: HTTP status code {response.status_code}")
#     except Exception as e:
#         print(f"Failed to scrape content from {url}: {e}")
#     return None

# # Scrape text content from each website
# for url in depth_1_links[:5]:
#     text_content = scrape_text_from_website(url)
#     if text_content:
#         scraped_data[url] = text_content
#         print(f"Scraped text content from {url}")

# # Print the scraped data (for demonstration)
# for url, content in scraped_data.items():
#     print(f"URL: {url}")
#     print(content[:100])
#     print("-" * 50)
