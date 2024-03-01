import scrapy
import json

class BrownCrawlerSpider(scrapy.Spider):
    name = 'browncrawler'
    allowed_domains = ['cs.brown.edu']
    start_urls = ['http://cs.brown.edu/']

    def __init__(self, *args, **kwargs):
        super(BrownCrawlerSpider, self).__init__(*args, **kwargs)
        self.results = {}

    def parse(self, response):
        level = response.meta.get('level', 0)
        url = response.url

        # Extract all links from the current page
        links = response.css('a::attr(href)').getall()

        # Filter out external links and keep only links under cs.brown.edu domain
        internal_links = [link for link in links if 'cs.brown.edu' in link]

        # Count the number of URLs at this level
        url_count = len(internal_links)
        print(f"Level {level} - URLs at {response.url}: {url_count}")

        # Save the results
        self.results[url] = url_count

        # Follow internal links recursively
        for link in internal_links:
            yield scrapy.Request(url=link, callback=self.parse, meta={'level': level + 1})

    def closed(self, reason):
        # Dump the results into a JSON file
        with open('crawl_results.json', 'w') as f:
            json.dump(self.results, f)
