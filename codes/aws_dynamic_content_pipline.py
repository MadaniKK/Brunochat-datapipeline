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
from datetime import datetime, timezone
from aws_utils import (
    num_tokens_from_string,
    handle_calendar_api_data,
    turn_text_into_embeddings,
)


load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
client = QdrantClient(
    "https://5ea28872-998e-4878-a3d7-9c2617741409.us-east4-0.gcp.cloud.qdrant.io",
    api_key=QDRANT_API_KEY,
)
collection_name = "CSWebsiteContent"
# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
endpoint_url = "https://api.openai.com/v1/embeddings"
openai_headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}


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
        metadata["text_content"] = cleaned_text
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
        urls = [
            "https://events.brown.edu/live/calendar/view/all/groups/Computer%20Science?user_tz=EST&template_vars=id,href,image_src,title,time,title_link,latitude,longitude,location,online_url,online_button_label,online_instructions,until,repeats,is_multi_day,is_first_multi_day,multi_day_span,tag_classes,category_classes,online_type,has_map,custom_ticket_required&syntax=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22thumb_width%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22hide_repeats%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22show_groups%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22show_locations%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22show_tags%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22use_tag_classes%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22search_all_events_only%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22use_modular_templates%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22display_all_day_events_last%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22format_single_image%22%3E%0A%20%20%20%20%7Bimage%7D%0A%20%20%20%20%7B%3Cdiv%20class%3D%22lw_image_caption%22%3E%7Ccaption%7C%3C%2Fdiv%3E%7D%0A%20%20%20%20%7B%3Cdiv%20class%3D%22lw_image_credit%20test1%22%3E%7Ccredit%7C%3C%2Fdiv%3E%7D%0A%20%20%3C%2Farg%3E%3C%2Fwidget%3E"
        ]
        for url in urls:
            # Headers to specify accepted content type
            headers = {"Accept": "application/json"}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Parse the JSON data from response
                data = response.json()
            else:
                print("Failed to retrieve data")
            text_content = handle_calendar_api_data(data)
            url_dict = {}
            metadata = {}
            metadata["text_content"] = text_content
            if (
                url
                == "https://events.brown.edu/live/calendar/view/all/groups/Computer%20Science?user_tz=EST&template_vars=id,href,image_src,title,time,title_link,latitude,longitude,location,online_url,online_button_label,online_instructions,until,repeats,is_multi_day,is_first_multi_day,multi_day_span,tag_classes,category_classes,online_type,has_map,custom_ticket_required&syntax=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22thumb_width%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22hide_repeats%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22show_groups%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22show_locations%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22show_tags%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22use_tag_classes%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22search_all_events_only%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22use_modular_templates%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22display_all_day_events_last%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22format_single_image%22%3E%0A%20%20%20%20%7Bimage%7D%0A%20%20%20%20%7B%3Cdiv%20class%3D%22lw_image_caption%22%3E%7Ccaption%7C%3C%2Fdiv%3E%7D%0A%20%20%20%20%7B%3Cdiv%20class%3D%22lw_image_credit%20test1%22%3E%7Ccredit%7C%3C%2Fdiv%3E%7D%0A%20%20%3C%2Farg%3E%3C%2Fwidget%3E"
            ):
                url = "https://events.brown.edu/all/groups/Computer%20Science"
            metadata["url"] = url
            metadata["token_count_estimate"] = num_tokens_from_string(
                text_content, "cl100k_base"
            )
            metadata["word_count"] = len(text_content.split())
            url_dict["metadata"] = metadata
            url_dict["uuid"] = str(uuid4())
            self.scraped_data[url] = url_dict

        for key, url_dic in self.scraped_data.items():
            url = key
            metadata = url_dic["metadata"]

            if int(metadata["token_count_estimate"]) > 8050:
                skipped_url.append(url)
                continue

            embedding = turn_text_into_embeddings(
                "text-embedding-3-small",
                text_content,
                endpoint_url,
                openai_headers=openai_headers,
            )
            if embedding is None:
                skipped_url.append(url)
                continue

            metadata["url"] = url  # Including URL in the payload
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
