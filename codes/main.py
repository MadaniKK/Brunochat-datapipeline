from crawl import crawl_website_bfs_parallel
from helper import visualize_and_save_topology, save_graph_structure, save_as_json_to_data_folder

import os
import json


# Main function
def main():
    start_url = 'https://cs.brown.edu/'  # Replace with your desired start URL
    max_depth = 0  # Maximum depth to crawl
    keyword = 'cs.brown.edu'  # Keyword to filter URLs
    filename_graphml = f'cs_brown_edu_depth_{max_depth}_topology.graphml'
    filename_image = f'cs_brown_edu_depth_{max_depth}_topology.png'
    
    # Crawl the website
    print(f"Crawling website: {start_url} ...")
    links_by_depth = crawl_website_bfs_parallel(start_url, max_depth, keyword)
    print("Crawling complete.")

    # Print the number of links at each depth level
    # Initialize a set to store all unique links encountered so far
    all_unique_links = set()

    # Print the number of unique links at each depth level
    for depth, links in links_by_depth.items():
        # Convert the list of links to a set to remove duplicates
        unique_links = set(links)
        # Remove links that have already been encountered in previous levels
        unique_links -= all_unique_links
        # Update the set of all unique links with the new links from this level
        all_unique_links.update(unique_links)
        print(f"Depth {depth}: {len(unique_links)} unique links")

    # Print the total number of unique links across all depth levels
    print(f"Total unique links: {len(all_unique_links)}")

    # Save the graph structure
    # save_graph_structure(website_graph, data_directory, filename_graphml)

    # Visualize and save the graph visualization
    # visualize_and_save_topology(website_graph, data_directory, filename_image)

    # Save the dictionary structure
    save_as_json_to_data_folder(links_by_depth, f'links_by_depth_{max_depth}.json')  
        
if __name__ == "__main__":
    main()
