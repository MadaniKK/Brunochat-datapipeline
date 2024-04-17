import scrapy
import json
from urllib.parse import urljoin

class BrownCrawlerSpider(scrapy.Spider):
    name = 'browncrawler'
    allowed_domains = ['cs.brown.edu']
    start_urls = ['http://cs.brown.edu/']
    custom_settings = {
        'DEPTH_LIMIT': 0,
    }

    def __init__(self, *args, **kwargs):
        super(BrownCrawlerSpider, self).__init__(*args, **kwargs)
        # Initialize to store URLs by depth
        self.links_by_depth = {}


    def parse(self, response):
        # Extract all links from the current page
        links = response.css('a::attr(href)').getall()

        # Resolve relative URLs to absolute URLs and filter by domain
        absolute_links = {urljoin(response.url, link) for link in links if 'cs.brown.edu' in urljoin(response.url, link)}

        # Current depth
        current_depth = response.meta.get('depth', 0)

        # Initialize the set for this depth if not already
        if current_depth not in self.links_by_depth:
            self.links_by_depth[current_depth] = set()

        # Add the links to the set for the current depth
        self.links_by_depth[current_depth].update(absolute_links)

        # Follow internal links
        for link in absolute_links:
            yield scrapy.Request(url=link, callback=self.parse)


    def closed(self, reason):
         # Log the counts
        for depth, urls in self.links_by_depth.items():
            self.logger.info(f'Depth {depth}: {len(urls)} URLs')

        depth_limit = self.settings.get('DEPTH_LIMIT', 0)
        file_name = f'../data/new_links_by_depth_{depth_limit}.json'
       

        with open(file_name, 'w') as f:
            # Convert sets to lists for JSON serialization
            json.dump({depth: list(urls) for depth, urls in self.links_by_depth.items()}, f)

 