import tiktoken

# with open("data/data_text_100.txt", "r") as file:
#     text_string = file.read()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# num_tokens_from_string(
#     text_string,
#     "cl100k_base",
# )
