import requests
from bs4 import BeautifulSoup, UnicodeDammit
import urllib.parse
import concurrent.futures
from collections import defaultdict, deque
import networkx as nx
import time

REQUEST_TIMEOUT = 8
MAX_WORKERS = 10  # Adjust based on your needs and environment capabilities

def fetch_url(url):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return url, response.content
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return url, None

from bs4 import BeautifulSoup, UnicodeDammit
import urllib.parse
import concurrent.futures
from collections import defaultdict, deque
import networkx as nx

def process_response(url, content, keyword, graph, queue, current_depth, max_depth, visited, links_by_depth):
    try:
        if content:
            dammit = UnicodeDammit(content)
            soup = BeautifulSoup(dammit.unicode_markup, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urllib.parse.urljoin(url, href)
                    if (full_url.startswith('http') or full_url.startswith('//')) and keyword in full_url:
                        graph.add_edge(url, full_url)
                        if current_depth + 1 <= max_depth and full_url not in visited:
                            queue.append((full_url, current_depth + 1))
                        links_by_depth[current_depth].append(full_url)
    except Exception as e:
        print(f"Error processing response from {url}: {e}")
        # Here, we simply log the exception and continue with the next URL without stopping the crawler.

def crawl_website_bfs_parallel(start_url, max_depth=3, keyword='cs.brown.edu'):
    visited = set()
    graph = nx.DiGraph()
    links_by_depth = defaultdict(list)
    queue = deque([(start_url, 0)])

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while queue:
            tasks = []
            # Build tasks for all URLs in the queue up to the max worker limit
            while queue and len(tasks) < MAX_WORKERS:
                url, current_depth = queue.popleft()
                if url in visited or current_depth > max_depth:
                    continue
                visited.add(url)  # Mark as visited early to avoid race conditions
                if len(visited) % 200 == 0:
                    print(f"Depth {current_depth}: total {len(visited)} links, current url: {url}")
                tasks.append(executor.submit(fetch_url, url))

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(tasks):
                url, content = future.result()
                process_response(url, content, keyword, graph, queue, current_depth, max_depth, visited, links_by_depth)

    for depth, links_list in links_by_depth.items():
        links_by_depth[depth] = list(set(links_list))

    return graph, links_by_depth
