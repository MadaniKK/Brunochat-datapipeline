import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import networkx as nx
import time
import urllib.parse


REQUEST_TIMEOUT = 8

from collections import deque

import time
import requests
from bs4 import BeautifulSoup
from collections import deque
from bs4 import UnicodeDammit
import networkx as nx
import urllib.parse  # Correct import statement

def crawl_website_bfs(start_url, max_depth=3, keyword='cs.brown.edu'):
    visited = set()
    graph = nx.DiGraph()
    links_by_depth = {}
    queue = deque([(start_url, 0)])  # Initialize queue with start URL and depth 0

    while queue:
        url, current_depth = queue.popleft()  # Dequeue the URL from the front of the queue
        if url in visited or current_depth > max_depth:
            continue

        try:
            start_time = time.time()  # Record the start time of the request
            response = requests.get(url, timeout=8)
            elapsed_time = time.time() - start_time  # Calculate the elapsed time

            if elapsed_time >= 8:
                print(f"Request to {url} timed out")
                continue  # Skip this URL and continue with the next one
            
            if response.status_code == 200:
                visited.add(url)
                if len(visited) % 20 == 0:
                    print(url)
                dammit = UnicodeDammit(response.content)
                soup = BeautifulSoup(dammit.unicode_markup, 'html.parser')
                links = soup.find_all('a', href=True)
                unique_links = set()  # Create a set to store unique URLs at this depth level
                for link in links:
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute URLs
                        full_url = urllib.parse.urljoin(url, href)
                        if (full_url.startswith('http') or full_url.startswith('//')) and keyword in full_url:
                            graph.add_edge(url, full_url)
                            if current_depth + 1 <= max_depth:
                                queue.append((full_url, current_depth + 1))
                            unique_links.add(full_url)  # Add the full URL to the set
                links_by_depth.setdefault(current_depth, set()).update(unique_links)  # Update the set in the dictionary
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    return graph, links_by_depth