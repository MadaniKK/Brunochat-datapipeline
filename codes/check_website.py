import requests

# The URL you want to check
url = "https://uxfactor.cs.brown.edu/clone_privacy_policy.html"

# Send a HTTP GET request to the URL
response = requests.get(url)

# Check if the 'Last-Modified' header is present
if "Last-Modified" in response.headers:
    print("Last-Modified:", response.headers["Last-Modified"])
else:
    print("The Last-Modified header is not present.")
