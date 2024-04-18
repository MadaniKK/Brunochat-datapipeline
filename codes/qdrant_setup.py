import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# Access environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


qdrant_client = QdrantClient(
    "https://5ea28872-998e-4878-a3d7-9c2617741409.us-east4-0.gcp.cloud.qdrant.io",
    api_key=QDRANT_API_KEY,
)

collections_info = qdrant_client.get_collections()
print("Collections:", collections_info)

# qdrant_client.create_payload_index(
#     collection_name="CSWebsiteContent",
#     field_name="last_modified",
#     field_schema="datetime",
# )

today_date = datetime.datetime.now().date().isoformat()
print(today_date)
