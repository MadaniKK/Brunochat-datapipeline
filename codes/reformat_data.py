from helper import load_data_from_json
import json

links_data = load_data_from_json("data/scraped_data_1000_1.json")

for key, value in links_data.items():
    if value["metadata"]["last_modified"] == "N/A":
        value["metadata"]["last_modified"] = None

with open("data/scraped_data_1000_1.json", "w") as f:
    json.dump(links_data, f)
