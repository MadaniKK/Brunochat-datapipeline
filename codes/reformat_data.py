from helper import load_data_from_json
import json
from uuid import uuid4

links_data = load_data_from_json("data/scraped_data_all.json")

for key, value in links_data.items():
    value["uuid"] = str(uuid4())
    if value["metadata"]["last_modified"] == "N/A":
        value["metadata"]["last_modified"] = None

with open("data/scraped_data_all.json", "w") as f:
    json.dump(links_data, f)
