import requests
from bs4 import BeautifulSoup, UnicodeDammit
import urllib.parse
import concurrent.futures
from collections import defaultdict, deque
import networkx as nx
import time
from helper import save_as_json_to_data_folder

REQUEST_TIMEOUT = 8
MAX_WORKERS = 20  # Adjust based on your needs and environment capabilities

def fetch_url(url):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return url, response.content
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return url, None

def process_response(url, content, keyword, queue, current_depth, max_depth, visited, links_by_depth):
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
                        if current_depth + 1 <= max_depth and full_url not in visited:
                            # print("hit here")
                            queue.append((full_url, current_depth + 1))
                        links_by_depth[current_depth].add(full_url)  # Change append to add for sets
    except Exception as e:
        print(f"Error processing response from {url}: {e}")
      
def crawl_website_bfs_parallel(start_url, max_depth=3, keyword='cs.brown.edu'):
    visited = set()
    links_by_depth = defaultdict(set)  # Initialize with sets instead of lists
    queue = deque([(start_url, 0)])
    prev_count = 0

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
                    print(f"{len(links_by_depth)}, {len(links_by_depth[len(links_by_depth)-1])}")
                tasks.append(executor.submit(fetch_url, url))

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(tasks):
                url, content = future.result()
                process_response(url, content, keyword, queue, current_depth, max_depth, visited, links_by_depth)

            num_visited = sum(len(links) for links in links_by_depth.values())
            if num_visited >= prev_count + 1000:
                # Save as JSON
                save_as_json_to_data_folder(links_by_depth, f'links_by_depth_{current_depth}.json')
                # Update the previous count
                prev_count = num_visited

    return links_by_depth


def crawl_website_bfs_parallel_continue(visited, links_by_depth, max_depth=3, keyword='cs.brown.edu'):
    prev_count = 0
    entry_level = len(links_by_depth) - 1
    queue = deque([])
    for url in links_by_depth[entry_level]:
        queue.append((url, entry_level))
    print(f"len of queue {len(queue)}")
    


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
                    print(f"{len(links_by_depth)}, {len(links_by_depth[len(links_by_depth)-1])}")
                tasks.append(executor.submit(fetch_url, url))

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(tasks):
                url, content = future.result()
                process_response(url, content, keyword, queue, current_depth, max_depth, visited, links_by_depth)

            num_visited = sum(len(links) for links in links_by_depth.values())
            if num_visited >= prev_count + 1000:
                # Save as JSON
                save_as_json_to_data_folder(links_by_depth, f'links_by_depth_{current_depth}.json')
                # Update the previous count
                prev_count = num_visited

    return links_by_depth