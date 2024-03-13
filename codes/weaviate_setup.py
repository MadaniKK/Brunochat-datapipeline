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

# Create authentication configuration
auth_config = weaviate.AuthApiKey(api_key=weaviate_api_key)

# Create a Weaviate client instance
client = weaviate.Client(url=weaviate_url, auth_client_secret=auth_config)

class_name = "CSWebsiteContent"

# deleting an object:
uuid_to_delete = "2676d9aa-4370-4ef4-9c80-d327edc1d840"  # replace with the id of the object you want to delete

client.data_object.delete(
    uuid=uuid_to_delete,
    class_name=class_name,  # Class of the object to be deleted
)

# # Define your class name representing your data
# class_name = "CSWebsiteContent"

# # Set up a class object
# class_obj = {
#     "class": class_name,
#     "vectorizer": "none",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
# }

# client.schema.create_class(class_obj)
