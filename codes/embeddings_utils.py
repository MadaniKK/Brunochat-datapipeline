from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("OPENAI_API_KEY")

endpoint_url = "https://api.openai.com/v1/embeddings"

# Define the headers with your API key and content type
headers = {
    "Authorization": f"Bearer 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",
    "Content-Type": "application/json",
}


def turn_text_into_embeddings(model, text):
    payload = {"model": model, "input": text}
    # Make the POST request to the OpenAI API
    response = requests.post(endpoint_url, headers=headers, json=payload)
    if response.status_code == 200:
        # Extract the embeddings from the response
        data = response.json().get("data", [])
        embedding = [item["embedding"] for item in data if "embedding" in item][0]
        # print("Embeddings:", embedding)
        return embedding
    else:
        print("Failed to generate embeddings:", response.text)
        return None
