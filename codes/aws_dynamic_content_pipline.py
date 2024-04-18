from datetime import datetime, timezone
import re
import scrapy
import tiktoken
from email.utils import parsedate_to_datetime
from uuid import uuid4
import os
import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models


load_dotenv()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
client = QdrantClient(
    "https://5ea28872-998e-4878-a3d7-9c2617741409.us-east4-0.gcp.cloud.qdrant.io",
    api_key=QDRANT_API_KEY,
)

# Define your collection name
collection_name = "CSWebsiteContent"


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Access environment variables
api_key = os.getenv("OPENAI_API_KEY")

endpoint_url = "https://api.openai.com/v1/embeddings"

# Define the headers with your API key and content type
headers = {
    "Authorization": f"Bearer {api_key}",
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


class MySpider(scrapy.Spider):
    name = "awsspider"

    # List of URLs to scrape

    start_urls = [
        "https://cs.brown.edu/news/",
        "https://cs.brown.edu/events/",
        # "https://events.brown.edu/all/groups/Computer%20Science",
    ]

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.scraped_data = {}  # Initialize an empty dictionary to store scraped data

    def parse(self, response):
        # Extract text content from the response
        # text_content = response.xpath('//p//text() | //h1//text() | //h2//text() | //h3//text() | //h4//text() | //div//text()').getall()

        # header and footer divs excluded
        url_dict = {}
        metadata = {}

        last_modified = response.headers.get("Last-Modified")
        if last_modified:
            # Convert Last-Modified header to datetime object
            last_modified = last_modified.decode("utf-8")
            last_modified_datetime = parsedate_to_datetime(last_modified)
            last_modified_datetime = last_modified_datetime.replace(tzinfo=timezone.utc)
            last_modified_iso = last_modified_datetime.isoformat(timespec="seconds")

            metadata["last_modified"] = last_modified_iso
        else:
            metadata["last_modified"] = None

        # For scraped_at (also assuming UTC for consistency)
        scraped_at_datetime = datetime.now(timezone.utc)
        scraped_at_iso = scraped_at_datetime.isoformat(timespec="seconds")
        metadata["scraped_at"] = scraped_at_iso

        # headers
        headers = response.xpath("//h1/text() | //h2/text()").getall()
        cleaned_headers = []
        for header in headers:
            # Replace unwanted characters
            cleaned_header = (
                header.replace("\n", "")
                .replace("\r", "")
                .replace("\t", "")
                .replace("\u00a0", "")
            )
            cleaned_header = cleaned_header.strip()
            # Add the cleaned header to the list
            cleaned_headers.append(cleaned_header)
        metadata["headings"] = cleaned_headers

        text_content = response.xpath(
            """
            //body//*[not(self::script or self::style or self::link or self::meta
                        or self::div[@id="header"] or self::div[@id="footer"]
                        or self::ul[@id="navbar2"] or self::ul[@id="navbar3"])
                and not(ancestor::div[@id="header"] or ancestor::div[@id="footer"]
                        or ancestor::ul[@id="navbar2"] or ancestor::ul[@id="navbar3"]
                        or ancestor::style)]
            /text()[normalize-space()]
            """
        ).getall()

        # Clean up the text content by removing unwanted whitespace characters and extra spaces
        if not text_content:
            return
        cleaned_text_content = " ".join(
            text.strip() for text in text_content if text.strip()
        )

        cleaned_text_content = (
            cleaned_text_content.strip()
            .replace("\n", "")
            .replace("\r", "")
            .replace("\t", "")
            .replace("\u00a0", " ")
        )
        pattern = r"[^a-zA-Z0-9 .,-]"

        # Use re.sub() to replace unwanted characters with an empty string
        cleaned_text = re.sub(pattern, "", cleaned_text_content)
        split_text = cleaned_text.split()
        metadata["word_count"] = len(split_text)
        cleaned_text = " ".join(split_text)
        metadata["token_count_estimate"] = num_tokens_from_string(
            cleaned_text, "cl100k_base"
        )

        if len(cleaned_text) == 0:
            return
        # Store the cleaned text content in the dictionary with the URL as the key
        metadata["url"] = response.url
        url_dict["text_content"] = cleaned_text
        url_dict["metadata"] = metadata
        url_dict["uuid"] = str(uuid4())
        self.scraped_data[response.url] = url_dict

    def closed(self, reason):
        print("helloworld")
        # Save the scraped data into a JSON file
        if len(self.scraped_data) == 0:
            return
        points = []
        skipped_url = []

        for key, url_dic in self.scraped_data.items():
            url = key
            text_content = url_dic["text_content"]
            metadata = url_dic["metadata"]

            if int(metadata["token_count_estimate"]) > 8050:
                skipped_url.append(url)
                continue

            embedding = turn_text_into_embeddings(
                "text-embedding-3-small", text_content
            )
            if embedding is None:
                skipped_url.append(url)
                continue

            metadata["url"] = url  # Including URL in the payload
            metadata["text_content"] = (
                text_content  # Including text content in the payload
            )
            uuid = url_dic["uuid"]
            # Prepare the point to be inserted into Qdrant
            point = models.PointStruct(
                id=uuid,
                payload=metadata,
                vector=embedding,
            )
            points.append(point)
        print(points)
        client.upsert(collection_name=collection_name, points=points)
        print(skipped_url)
