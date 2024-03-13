import tiktoken

with open("codes/data_text_1000.txt", "r") as file:
    text_string = file.read()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(num_tokens)
    return num_tokens


num_tokens_from_string(
    "in \Warehouses",
    "cl100k_base",
)
