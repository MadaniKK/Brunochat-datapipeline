import json
import requests
from bs4 import BeautifulSoup


with open('./data/new_links_by_depth_0.json', 'r') as file:
    links_by_depth = json.load(file)
# # Initialize an empty list to store all links
# all_links = []

# Iterate through each depth level in the dictionary
# for depth, links in links_by_depth.items():
#     # Extend the list of links at each depth level
#     all_links.extend(links)

# # Remove duplicates by converting the list to a set and back to a list
# print(len(all_links))
# all_links = list(set(all_links))

# print(len(all_links))
    
all_unique_links = set()

for depth, links in links_by_depth.items():
    unique_links = set(links) - all_unique_links
    all_unique_links.update(unique_links)
    print(f"Depth {depth}: {len(unique_links)} unique links")

print(f"Total unique links: {len(all_unique_links)}")





# If you want to save the unique links back to a JSON file
with open('./data/unique_links_deepest.json', 'w') as file:
    json.dump(list(all_unique_links), file, indent=4)


