# BrunoChat Data Pipeline

## BrunoChat Repository
Refer to [BrunoChat](https://github.com/aetherrine/BrunoChat) for more information！

## Table of Contents
1. [Introduction](#introduction)
2. [Motivation](#motivation)
3. [Description](#description)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

BrunoChat is a chatbot designed to serve as an innovative conversational knowledge interface for the Computer Science Department. BrunoChat Data Pipeline is responsible for crawling and scraping web content from the Computer Science Department at Brown University. It is an essential component of the BrunoChat project, providing the necessary data for training and fine-tuning the chatbot's language models.

## Motivation

The motivation behind the BrunoChat Data Pipeline is to collect accurate and up-to-date information from the department's website in an efficient and automated manner. By automating the data collection process, BrunoChat ensures that its knowledge base remains current and relevant to users' inquiries.

## Description

The data pipeline consists of web crawling and web scraping components. The web crawling component navigates through the department's website, identifying relevant pages to scrape. The web scraping component extracts text content from these pages, which is then used to train and fine-tune the chatbot's language models.

## Getting Started
1. Clone the repository: `git clone git@github.com:MadaniKK/2270-crawler-test.git`
2. Install dependencies: `pip install -r requirements.txt`
3. `cd codes` to go to the codes directory
4. `scrapy runspider use_scrapy.py` will run Scrapy to crawl all the URLs under the 'cs.brown.edu' domain.
5. `scrapy runspider scrape.py` will run Scrapy to scrape all the text content from the provided URLs.
6. `check_links.py` is for filtering out the undesired URLs and preprocessing the data into the desired format. 
7.  `weaviate_setup.py` is for the initial setup for the Weaviate vector database and defining classes.
8.  `qdrant_setup.py` is for the initial setup for the Weaviate vector database and defining classes.
9.  `data_pipline.py` is for turning the webpage content into embeddings via OpenAI APIs and storing them in Weaviate.


## Usage

Once the data pipeline is running, it will automatically crawl and scrape web content from the Computer Science Department website. The scraped data will be preprocessed and saved to a vector database for further processing and analysis.

## Contributing

We welcome contributions from the community! If you'd like to contribute to the BrunoChat Data Pipeline, please follow these guidelines:
- Fork the repository
- Create a new branch for your feature or enhancement: `git checkout -b feature-name`
- Make your changes and ensure they adhere to the project's coding standards
- Test your changes thoroughly
- Submit a pull request with a clear description of your changes

