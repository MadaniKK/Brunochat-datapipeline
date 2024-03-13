import json
import requests
import weaviate
from dotenv import load_dotenv
import os
from embeddings_utils import turn_text_into_embeddings
from helper import load_data_from_json


# Load environment variables from .env file
load_dotenv()

# Access environment variables
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

# Define your Weaviate instance URL
weaviate_url = "https://2270-test-vectordb-e6tzpuux.weaviate.network"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {weaviate_api_key}",  # Replace with your actual API key
}

model = "text-embedding-3-small"

# Define your class name representing your data
class_name = "CSWebsiteContent"

link_data_collections = load_data_from_json("data/scraped_data_test.json")

skipped_url = []

# load by batch
batch_size = 100
batch_objects = []

for key, url_dic in link_data_collections.items():
    url = key
    text_content = url_dic["text_content"]
    metadata = url_dic["metadata"]

    if int(metadata["token_count_estimate"]) > 8050:
        skipped_url.append(url)
        continue

    metadata["url"] = url
    embedding = turn_text_into_embeddings(model, text_content)
    if embedding is None:
        skipped_url.append(url)
        continue
    metadata["embeddings"] = embedding
    metadata["text_content"] = text_content
    object_to_add = {"class": class_name, "properties": metadata}
    batch_objects.append(object_to_add)

    if len(batch_objects) >= batch_size:
        # Send batch request
        payload_json = json.dumps({"objects": batch_objects})
        response = requests.post(
            f"{weaviate_url}/v1/batch/objects", headers=headers, data=payload_json
        )
        print(response.text)

        # Reset batch_objects list
        batch_objects = []

# Add remaining objects
if batch_objects:
    payload_json = json.dumps({"objects": batch_objects})
    response = requests.post(
        f"{weaviate_url}/v1/batch/objects", headers=headers, data=payload_json
    )
    print(response.text)

if len(skipped_url) != 0:
    with open("../data/skipped_url.json", "w") as f:
        json.dump(skipped_url, f)

# load object one by one

# for key, url_dic in link_data_collections.items():
#     url = key
#     text_content = url_dic["text_content"]
#     metadata = url_dic["metadata"]

#     if int(metadata["token_count_estimate"]) > 8050:
#         skipped_url.append(url)
#         continue

#     metadata["url"] = url
#     embedding = turn_text_into_embeddings(model, text_content)
#     if embedding is None:
#         skipped_url.append(url)
#         continue
#     metadata["embeddings"] = embedding
#     metadata["text_content"] = text_content
#     object_to_add = {"class": class_name, "properties": metadata}
#     payload_json = json.dumps(object_to_add)
#     # print(payload_json)
#     response = requests.post(
#         f"{weaviate_url}/v1/objects", headers=headers, data=payload_json
#     )
#     print(response.text)
#     break
