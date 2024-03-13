import json
import requests
from bs4 import BeautifulSoup


# with open("./data/filtered_links_deepest.json", "r") as file:
#     links_by_depth = json.load(file)
# print(len(links_by_depth))
# print(len(list(set(links_by_depth))))
# # Initialize an empty list to store all links
# all_links = []

# # Iterate through each depth level in the dictionary
# for depth, links in links_by_depth.items():
#     # Extend the list of links at each depth level
#     all_links.extend(links)

# # Remove duplicates by converting the list to a set and back to a list
# print(len(all_links))
# all_links = list(set(all_links))

# print(len(all_links))
# print(all_links[:10])

# all_unique_links = set()

# for depth, links in links_by_depth.items():
#     unique_links = set(links) - all_unique_links
#     all_unique_links.update(unique_links)
#     print(f"Depth {depth}: {len(unique_links)} unique links")

# print(f"Total unique links: {len(all_unique_links)}")


# # If you want to save the unique links back to a JSON file
# with open("./data/unique_links_deepest.json", "w") as file:
#     json.dump(list(all_unique_links), file, indent=4)


with open("./data/unique_links_deepest.json", "r") as file:
    urls = json.load(file)

unique_urls = set()

for url in urls:
    # Remove trailing slash if present
    normalized_url = url.rstrip("/")
    unique_urls.add(normalized_url)

urls = list(unique_urls)

unwanted_substrings = [
    "https://cs.brown.edu/courses/cs173/2008/Manual",
    "https://cs.brown.edu/courses/csci1730/2008/Manual",
    ".hqx",
    "http://burlap.cs.brown.edu/doc",
    "Pyret_Style_Guide",
    "mailto:",
    "http://irl.cs.brown.edu/pinball/",
    "#h.",
    ".key",
    ".rkt",
    ".pptx",
    ".ppt",
    ".pdf",
    "php#",
    ".gz",
    ".gif",
    "#",
    ".zip",
    ".png",
    ".jpg",
    ".ps",
    "login",
    "signin",
    ".py",
    ".sty" "http://csci2390-submit.cs.brown.edu",
    "http://plus.google.com/share?url=http%3A//cs.brown.edu/news/",
    "http://vis.cs.brown.edu/docs/",
    "http://vis.cs.brown.edu/resources/doc/",
    ".bib",
    "http://vis.cs.brown.edu/results/images",
    "https://cs.brown.edu/courses/csci1430/",
    ".shtml",
    "https://lists.cs.brown.edu/sympa",
    "https://cs.brown.edu/courses/csci1380/s12/doc/api/",
    "/images/",
    "/Videos",
    ".m",
    "https://cs.brown.edu/courses/csci1950-g/results",
    "https://cs.brown.edu/courses/csed/reactions",
    "https://cs.brown.edu/courses/csed/thoughtful",
    ".java",
    "https://cs.brown.edu/giving/uta/uta/",
    ".txt",
    ".tex",
    "/results/",
    "https://cs.brown.edu/courses/csci0160/static/",
    "https://cs.brown.edu/memex/",
    "https://cs.brown.edu/video/",
    "share=",
    "https://www.vrwiki.cs.brown.edu/vr-visualization-software/visualization-tutorials/paraview",
    "google.com/",
    "https://twitter.com/",
    "http://www.facebook.com/",
    ".doc",
    "binaries",
    ".tgz",
    "https://cs.brown.edu/courses/cs173/2012/Assignments/ParselExtend/reference/",
    "https://cs.brown.edu/courses/cs173/2012/Assignments/ParselTest/Software/",
    "logout",
    "https://cs.brown.edu/people/ugrad/rkrish16/",
    "BorealisDemo",
    ".js",
    ".als",
    ".bz2",
    ".xlsx",
    ".dvi",
    ".plt",
    " ",
    ".swf",
    ".scm",
    "pyret",
]

filtered_urls = [
    url for url in urls if all(unwanted not in url for unwanted in unwanted_substrings)
]

filtered_urls = list(set(filtered_urls))
filtered_urls.sort()
print(len(filtered_urls))

with open("./data/filtered_links_deepest.json", "w") as file:
    json.dump(list(filtered_urls), file, indent=4)
