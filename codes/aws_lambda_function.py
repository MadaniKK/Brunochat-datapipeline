import scrapy
from scrapy.crawler import CrawlerProcess
from scrape import MySpider  # Import your Scrapy spider class


def lambda_handler(event, context):
    # Configure Scrapy settings
    settings = {
        "LOG_ENABLED": False,  # Disable logging
        # Add any other Scrapy settings here
    }

    # Create a CrawlerProcess with the settings
    process = CrawlerProcess(settings=settings)

    # Add your spider to the process
    process.crawl(MySpider)

    # Start the process
    process.start()

    return {"statusCode": 200, "body": "Scrapy spider executed successfully"}
