import scrapy
import json
import scrapy
import json

class MySpider(scrapy.Spider):
    name = 'myspider'
    
    # List of URLs to scrape
    start_urls = [
        'https://cs.brown.edu/',
        "https://cs.brown.edu/people/grad/myuhan/", 
        "https://blog.cs.brown.edu/2023/12/18/research-associate-tom-sgouros-and-brown-cs-students-use-sound-and-ai-make-nasa-imagery-accessible/", 
        "http://wellness.advocates@lists.cs.brown.edu", 
        "https://cs.brown.edu/people/ugrad/stang52/", 
        "https://cs.brown.edu/people/grad/ztang47/", 
        "https://cs.brown.edu/giving", 
        "https://cs.brown.edu/about/system/accounts/", 
        "https://cs.brown.edu/courses/info/data2040/"
        # Add more URLs as needed
    ]

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.scraped_data = {}  # Initialize an empty dictionary to store scraped data

    def parse(self, response):
        # Extract text content from the response
        text_content = response.xpath('//p//text() | //h1//text() | //h2//text() | //h3//text() | //h4//text() | //div//text()').getall()
        
        # Concatenate the text content into a single string
      
        # Clean up the text content by removing unwanted whitespace characters and extra spaces
         # Clean up the text content by removing unwanted whitespace characters and extra spaces
        cleaned_text_content = ' '.join(text.strip() for text in text_content if text.strip())
        
        cleaned_text_content = cleaned_text_content.strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('\u00a0', ' ')
        
        # Store the cleaned text content in the dictionary with the URL as the key
        self.scraped_data[response.url] = cleaned_text_content

    def closed(self, reason):
        # Save the scraped data into a JSON file
        with open('test_scraped_data.json', 'w') as f:
            json.dump(self.scraped_data, f)
