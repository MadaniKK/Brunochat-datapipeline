import matplotlib.pyplot as plt
import networkx as nx
import os


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