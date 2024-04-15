import json
import os
from uuid import uuid4
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from embeddings_utils import turn_text_into_embeddings
from helper import load_data_from_json

# Load environment variables from .env file
load_dotenv()

# Access environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


client = QdrantClient(
    "https://5ea28872-998e-4878-a3d7-9c2617741409.us-east4-0.gcp.cloud.qdrant.io",
    api_key=QDRANT_API_KEY,
)

# Define your collection name
collection_name = "CSWebsiteContent"

link_data_collections = load_data_from_json("data/scraped_data_all.json")

skipped_url = []

# Load by batch
batch_size = 100
points = []

for key, url_dic in link_data_collections.items():
    url = key
    text_content = url_dic["text_content"]
    metadata = url_dic["metadata"]

    if int(metadata["token_count_estimate"]) > 8050:
        skipped_url.append(url)
        continue

    embedding = turn_text_into_embeddings("text-embedding-3-small", text_content)
    if embedding is None:
        skipped_url.append(url)
        continue

    metadata["url"] = url  # Including URL in the payload
    metadata["text_content"] = text_content  # Including text content in the payload
    uuid = url_dic["uuid"]
    # Prepare the point to be inserted into Qdrant
    point = models.PointStruct(
        id=uuid,
        payload=metadata,
        vector=embedding,  # using URL as the unique identifier
    )
    points.append(point)

    # Send batch request
    if len(points) >= batch_size:
        client.upsert(collection_name=collection_name, points=points)
        points = []  # Reset points list

# Upsert remaining points
if points:
    client.upsert(collection_name=collection_name, points=points)

if len(skipped_url) != 0:
    print("Skipped URLs due to size or other issues:", skipped_url)
