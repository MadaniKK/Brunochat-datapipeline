import json

with open('./data/unique_links_2.json', 'r') as file:
    links_by_depth_2 = json.load(file)

print(len(links_by_depth_2))