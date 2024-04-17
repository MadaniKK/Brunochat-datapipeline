from datetime import datetime, timezone
import re
import scrapy
import json
import scrapy
from email.utils import parsedate_to_datetime
from helper import num_tokens_from_string


with open("../data/filtered_links_deepest.json", "r") as file:
    links_by_depth = json.load(file)
    list_1000 = links_by_depth[10:12]


class MySpider(scrapy.Spider):
    name = "myspider"

    # List of URLs to scrape
    start_urls = list_1000
    # start_urls = ["https://uxfactor.cs.brown.edu/clone_privacy_policy.html"]

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.scraped_data = {}  # Initialize an empty dictionary to store scraped data
        self.scraped_text = ""

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
        self.scraped_data[response.url] = url_dict
        self.scraped_text += cleaned_text_content

    def closed(self, reason):
        # Save the scraped data into a JSON file
        if len(self.scraped_data) == 0:
            return
        with open("../data/scraped_data_test.json", "w") as f:
            json.dump(self.scraped_data, f)

        # with open("../data/data_text_1000_1.txt", "w") as file:
        #     # Write the string to the file
        #     file.write(self.scraped_text)
