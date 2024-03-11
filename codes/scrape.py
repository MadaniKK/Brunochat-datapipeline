import scrapy
import json
import scrapy

with open("../data/filtered_links_deepest.json", "r") as file:
    links_by_depth = json.load(file)
    list_1000 = links_by_depth[:1000]


class MySpider(scrapy.Spider):
    name = "myspider"

    # List of URLs to scrape
    # start_urls = list_1000
    start_urls = (
        "https://pyret.cs.brown.edu/assignment/1-BzXD0LYkK7neGbwxcO8XXVJ1KDm48TO"
    )

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.scraped_data = {}  # Initialize an empty dictionary to store scraped data
        self.scraped_text = ""

    def parse(self, response):
        # Extract text content from the response
        # text_content = response.xpath('//p//text() | //h1//text() | //h2//text() | //h3//text() | //h4//text() | //div//text()').getall()

        # header and footer divs excluded

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
        cleaned_text_content = " ".join(cleaned_text_content.split())
        if len(cleaned_text_content) == 0:
            return
        # Store the cleaned text content in the dictionary with the URL as the key
        self.scraped_data[response.url] = cleaned_text_content
        self.scraped_text += cleaned_text_content

    def closed(self, reason):
        # Save the scraped data into a JSON file
        if len(self.scraped_data) == 0:
            return
        with open("scraped_data_1000.json", "w") as f:
            json.dump(self.scraped_data, f)

        with open("data_text_1000.txt", "w") as file:
            # Write the string to the file
            file.write(self.scraped_text)
