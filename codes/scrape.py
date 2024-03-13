from datetime import datetime, timezone
import re
import scrapy
import json
import scrapy
from email.utils import parsedate_to_datetime


with open("../data/filtered_links_deepest.json", "r") as file:
    links_by_depth = json.load(file)
    list_1000 = links_by_depth[:100]


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

            metadata["last-modified"] = last_modified_iso
        else:
            metadata["last-modified"] = "N/A"

        # For Scraped-At (also assuming UTC for consistency)
        scraped_at_datetime = datetime.now(timezone.utc)
        scraped_at_iso = scraped_at_datetime.isoformat(timespec="seconds")
        metadata["scraped-at"] = scraped_at_iso

        # headers
        headers = response.xpath("//h1/text() | //h2/text()").getall()
        for header in headers:
            header = " ".join(word.strip() for word in header if word.strip())
            header.strip().replace("\n", "").replace("\r", "").replace(
                "\t", ""
            ).replace("\u00a0", " ")
        metadata["headings"] = headers
        text_content = response.xpath(
            """
                        //body/*[not(
                            self::div[@id="header"] or 
                            self::div[@id="footer"] or 
                            self::ul[@id="navbar2"] or 
                            self::ul[@id="navbar3"]
                        )   and not(
                            ancestor::div[@id="header"] or 
                            ancestor::div[@id="footer"] or 
                            ancestor::ul[@id="navbar2"] or 
                            ancestor::ul[@id="navbar3"]
                        )]//text()[normalize-space()]
                    """
        ).getall()

        # Concatenate the text content into a single string

        # Clean up the text content by removing unwanted whitespace characters and extra spaces
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

        if len(cleaned_text_content) == 0:
            return
        # Store the cleaned text content in the dictionary with the URL as the key
        url_dict["text_content"] = cleaned_text_content
        url_dict["metadata"] = metadata
        self.scraped_data[response.url] = url_dict
        self.scraped_text += cleaned_text_content

    def closed(self, reason):
        # Save the scraped data into a JSON file
        if len(self.scraped_data) == 0:
            return
        with open("../data/scraped_data_100.json", "w") as f:
            json.dump(self.scraped_data, f)

        with open("../data/data_text_100.txt", "w") as file:
            # Write the string to the file
            file.write(self.scraped_text)
