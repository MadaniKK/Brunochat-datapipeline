import matplotlib.pyplot as plt
import networkx as nx
import os
import json


# Function to save the graph structure
def save_graph_structure(graph, directory, filename):
    # Ensure that the directory exists
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    nx.write_graphml(graph, filepath)

# Function to visualize and save the graph visualization
def visualize_and_save_topology(graph, directory, filename):
    # Ensure that the directory exists
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=10)
    plt.title("Website Topology")
    plt.savefig(filepath)  # Save the visualization as an image file
    plt.show()

def save_as_json_to_data_folder(content, filename):

    data_directory = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
    os.makedirs(data_directory, exist_ok=True)
    json_file_path = os.path.join(data_directory, filename)

    if isinstance(content, dict):
        # Convert sets to lists
        content = {key: list(value) for key, value in content.items() if isinstance(value, set)}

    with open(json_file_path, 'w') as file:
        json.dump(content, file)
    print(f"saved {filename} to ./data ")