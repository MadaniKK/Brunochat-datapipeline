import json
import tiktoken


def load_data_from_json(filepath):
    with open(filepath, "r") as file:
        links_data_collection = json.load(file)
    return links_data_collection


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
