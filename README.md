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

## Introduction

BrunoChat is a chatbot designed to serve as an innovative conversational knowledge interface for the Computer Science Department. BrunoChat Data Pipeline is responsible for crawling and scraping web content from the Computer Science Department at Brown University. It is an essential component of the BrunoChat project, providing the necessary data for training and fine-tuning the chatbot's language models.

## Motivation

The motivation behind the BrunoChat Data Pipeline is to collect accurate and up-to-date information from the department's website in an efficient and automated manner. By automating the data collection process, BrunoChat ensures that its knowledge base remains current and relevant to users' inquiries.

## Description

The data pipeline consists of web crawling, web scraping components, writing data to vector database, and automating dynamic content daily updates. 
1. Web crawling component navigates through the department's website, identifying relevant pages to scrape.
2. Web scraping component extracts text content from these pages, which is then used to train and fine-tune the chatbot's language models.
3.[Weaviate](https://weaviate.io/) or [Qdrant](https://qdrant.tech/) databases can be used as the vector database.
4. A script is deployed on `AWS Lambda` to daily scrape dynamic content and update the database

## Getting Started
### 1. Clone the repository
```shell
git clone git@github.com:MadaniKK/2270-crawler-test.git
```
### 2. Activate Virtual Environment
```shell
python -m venv brunochat-env
source brunochat-env/bin/activate
```
### 3. Install dependencies: 
```shell
pip install -r requirements.txt
```
### 4. Prepare Credentials
```shell
echo OPENAI_API_KEY={openai_key}     >> .env
echo QDRANT_API_KEY={weaviate_key} >> .env
echo QDRANT_WCS_URL={server_url}   >> .env
```
### 5. Run Scrapy to crawl all the URLs under the 'cs.brown.edu' domain
```shell
scrapy runspider codes/use_scrapy.py`
```
### 6. Filter out the undesired URLs and preprocessing the data into the desired format
```shell
 python3 codes/check_links.py
```
### 7. Run Scrapy to scrape all the text content from the provided URLs
```shell
`scrapy runspider codes/scrape.py`
```
### 8. Setup and write to the Weaviate/Qdrant vector database.
```shell
python3 codes/weaviate_setup.py
python3 codes/weaviate_data_pipline.py
#or
python3 codes/qdrant_setup.py
python3 codes/qdrant_data_pipline.py
```
### 9. Docker Image for handling Dynamic content on AWS
 `/dynamic_content_aws_docker.zip` handles the dynamic content daily updates. It contains the folder that could be built into a docker image to deploy on AWS Lambda


## Usage

Once the data pipeline is running, it will automatically crawl and scrape web content from the Computer Science Department website. The scraped data will be preprocessed and saved to a vector database for further processing and analysis.

## Contributing

We welcome contributions from the community! If you'd like to contribute to the BrunoChat Data Pipeline, please follow these guidelines:
- Fork the repository
- Create a new branch for your feature or enhancement: `git checkout -b feature-name`
- Make your changes and ensure they adhere to the project's coding standards
- Test your changes thoroughly
- Submit a pull request with a clear description of your changes

