import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import time
REQUEST_TIMEOUT = 8

# Function to crawl a website and extract links
def crawl_website(url, max_depth=3, current_depth=0, visited=None, graph=None, links_by_depth=None):
    if visited is None:
        visited = set()
    if graph is None:
        graph = {}
    if links_by_depth is None:
        links_by_depth = {}

    if current_depth > max_depth:
        return graph, links_by_depth
    
    if url in visited:
        return graph, links_by_depth
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            visited.add(url)
            if len(visited) % 10 == 0:
              print(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            links_by_depth.setdefault(current_depth, []).extend(link['href'] for link in links)
            for link in links:
                href = link.get('href')
                if href and href.startswith('http'):
                    graph.setdefault(url, []).append(href)
                    if current_depth < max_depth:
                        crawl_website(href, max_depth, current_depth + 1, visited, graph, links_by_depth)
    except UnicodeDecodeError as e:
        print(f"Error decoding content from URL: {url}")
        print(e) 
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")
    
    return graph, links_by_depth


from collections import deque

def crawl_website_bfs(start_url, max_depth=3, keyword='brown'):
    visited = set()
    graph = {}
    links_by_depth = {}
    queue = deque([(start_url, 0)])  # Initialize queue with start URL and depth 0

    while queue:
        url, current_depth = queue.popleft()  # Dequeue the URL from the front of the queue
        if url in visited or current_depth > max_depth:
            continue

        try:
            start_time = time.time()  # Record the start time of the request
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            elapsed_time = time.time() - start_time  # Calculate the elapsed time

            if elapsed_time >= REQUEST_TIMEOUT:
                print(f"Request to {url} timed out")
                continue  # Skip this URL and continue with the next one
            
            if response.status_code == 200:
                visited.add(url)
                if len(visited) % 20 == 0:
                    print(url)
                dammit = UnicodeDammit(response.content)
                soup = BeautifulSoup(dammit.unicode_markup, 'html.parser')
                links = soup.find_all('a', href=True)
                links_by_depth.setdefault(current_depth, []).extend(link['href'] for link in links)
                for link in links:
                    href = link.get('href')
                    if href and href.startswith('http') and keyword in href:
                        graph.setdefault(url, []).append(href)
                        if current_depth + 1 <= max_depth:
                            queue.append((href, current_depth + 1))
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")
    
    return graph, links_by_depth



# Main function
def main():
    start_url = 'https://cs.brown.edu/'  # Replace with your desired start URL
    max_depth = 3  # Maximum depth to crawl
    keyword = 'cs.brown.edu'  # Keyword to filter URLs

    # Crawl the website
    print(f"Crawling website: {start_url} ...")
    website_graph, links_by_depth = crawl_website_bfs(start_url, max_depth, keyword)
    print("Crawling complete.")

    # Print the number of links at each depth level
    for depth, links in links_by_depth.items():
        print(f"Depth {depth}: {len(links)} links")
    
if __name__ == "__main__":
    main()
