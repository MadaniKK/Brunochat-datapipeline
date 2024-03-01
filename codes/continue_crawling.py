from helper import save_as_json_to_data_folder
from crawl import crawl_website_bfs_parallel_continue
import json
from collections import defaultdict

with open('./data/links_by_depth_0.json', 'r') as file:
    links_by_depth_0 = json.load(file)
# Initialize an empty list to store all links
all_links = []
converted_dict = defaultdict(set)
# Iterate through each depth level in the dictionary
for depth, links in links_by_depth_0.items():
    # Extend the list of links at each depth level
    if int(depth) < len(links_by_depth_0) - 1:
        all_links.extend(links)
    converted_dict[int(depth)] = set(links)

# Remove duplicates by converting the list to a set and back to a list
print(len(all_links))
visited = set(all_links)
print(len(visited))



max_depth = 1

new_links_by_death = crawl_website_bfs_parallel_continue(set(), converted_dict, max_depth)

all_unique_links = set()

for depth, links in new_links_by_death.items():
    unique_links = set(links) - all_unique_links
    all_unique_links.update(unique_links)
    print(f"Depth {depth}: {len(unique_links)} unique links")

print(f"Total unique links: {len(all_unique_links)}")


save_as_json_to_data_folder(new_links_by_death, f'links_by_depth_{max_depth}.json')  