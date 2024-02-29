from crawl import crawl_website_bfs
from helper import visualize_and_save_topology, save_graph_structure, save_as_json_to_data_folder

import os
import json


# Main function
def main():
    start_url = 'https://cs.brown.edu/'  # Replace with your desired start URL
    max_depth = 2  # Maximum depth to crawl
    keyword = 'cs.brown.edu'  # Keyword to filter URLs
    filename_graphml = f'cs_brown_edu_depth_{max_depth}_topology.graphml'
    filename_image = f'cs_brown_edu_depth_{max_depth}_topology.png'
    
    # Crawl the website
    print(f"Crawling website: {start_url} ...")
    website_graph, links_by_depth = crawl_website_bfs(start_url, max_depth, keyword)
    print("Crawling complete.")

    # Print the number of links at each depth level
    for depth, links in links_by_depth.items():
        print(f"Depth {depth}: {len(links)} links")
    
    current_directory = os.path.dirname(__file__)

    # Path to the parent directory (which contains both codes and data directories)
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

    # Path to the data directory relative to the parent directory
    data_directory = os.path.join(parent_directory, 'data')

    # Save the graph structure
    # save_graph_structure(website_graph, data_directory, filename_graphml)

    # Visualize and save the graph visualization
    # visualize_and_save_topology(website_graph, data_directory, filename_image)

    # Save the dictionary structure
    save_as_json_to_data_folder(links_by_depth, f'links_by_depth_{max_depth}.json')  
        
if __name__ == "__main__":
    main()
